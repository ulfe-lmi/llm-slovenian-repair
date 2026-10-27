"""Order 021-a: bounded final response delivery on the accepted client
socket.

Proves, with real loopback wire traffic only, that the runnable proxy
bounds the final post-intake response emission (status line, headers,
body and the actual flush) under one finite positive monotonic
delivery deadline anchored immediately before emission and before the
owned guard starts; response-ready work (upstream capture and optional
repair) is outside the phase; byte progress never resets the deadline;
a stalled or slowly reading client is closed boundedly by a pure timer
that interrupts only the exact accepted socket object; the guard is
cancelled and actually joined on every path; once any response
emission began no second response or fallback is attempted; and a
healthy next request on the same proxy succeeds.  Controlled
call-through delays are clearly separated from the native wire
proofs.  Synthetic loopback fixtures only: no live Qwen, no delivery
acknowledgment and no hard-real-time claim.
"""

from __future__ import annotations

import contextlib
import http.client
import io
import json
import os
import socket
import socketserver
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Protocol, cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import delivery_transport  # noqa: E402
import proxy  # noqa: E402
from batch_review import BatchResult, BatchTarget  # noqa: E402
from config import (  # noqa: E402
    CLIENT_DELIVERY_TIMEOUT_SECONDS,
    CLIENT_REQUEST_TIMEOUT_SECONDS,
    MAIN_HEADER_TIMEOUT_SECONDS,
    REVIEWER_HTTP_TIMEOUT_SECONDS,
)
from pandoc_protection import (  # noqa: E402
    PandocStartupError,
    check_pandoc,
)
from qwen_client import ResponsesReviewer  # noqa: E402
from tests.test_capture_transport import (  # noqa: E402
    _BUILD_UNIGRAM,
    CLEAN,
    _sse_baseline_utf8,
)
from tests.test_client_transport import (  # noqa: E402
    _DelayedMain,
    _drain,
    _harness_post,
    _head,
    _ObservedEngine,
    _OwnedThreadingServer,
    _raw_post,
    _request_parts,
)
from tests.test_header_transport import (  # noqa: E402
    EXPECTED_USEFUL_018,
    USEFUL_018,
    _DummyEngine,
)
from tests.test_responses_contract import (  # noqa: E402
    _json_completed,
    _MainUpstream,
    _review_payload,
)
from tests.test_review_batch import (  # noqa: E402
    _contract_body,
    _FakeUpstream,
    _prop,
    _real_spec,
)
from tests.test_runtime_corpus import _build_db  # noqa: E402

_GUARD_NAME = "concept-client-delivery-guard"
# A legal completed answer whose exact delivered JSON body is far
# larger than the loopback kernel buffer, so a nonreading or slowly
# reading client stalls the handler inside the actual socket write.
_STALL_N = 300_000
# Explicit bounded buffer size for the matched paced-reader pair:
# the kernel cannot accept the whole moderate payload before the
# first paced read.
_PACED_BUF = 4096


def _delivery_guard_threads() -> list[threading.Thread]:
    """Only the product's own delivery guard threads (known owned
    name); no unrelated process or thread scanning."""
    return [th for th in threading.enumerate() if th.name == _GUARD_NAME]



def _guard_observations() -> tuple[
    list[delivery_transport.DeliveryGuard],
    contextlib.AbstractContextManager[object],
]:
    guards: list[delivery_transport.DeliveryGuard] = []
    real_guard = delivery_transport.DeliveryGuard

    def make_guard(
        sock: socket.socket, budget: float
    ) -> delivery_transport.DeliveryGuard:
        guard = real_guard(sock, budget)
        guards.append(guard)
        return guard

    return guards, mock.patch.object(
        delivery_transport, "DeliveryGuard", side_effect=make_guard
    )


def _stall_answer() -> str:
    return (CLEAN + " ") * _STALL_N


class _WriterLike(Protocol):
    """The minimal structural view of the stdlib unbuffered writer the
    proxy handler owns (socketserver._SocketWriter), observed by the
    flush/write call-through fixtures without touching its source."""

    _sock: socket.socket

    def flush(self) -> None: ...

    def write(self, b: bytes) -> int: ...


def _writer_cls() -> type[_WriterLike]:
    """The owned stdlib writer class by exact attribute (a private
    name absent from the checked stdlib stubs)."""
    return cast("type[_WriterLike]", vars(socketserver)["_SocketWriter"])


class _Stoppable(Protocol):
    """Minimal owned-patcher interface: the bounded start()/stop()
    pair used by the startup-failure containment fixtures."""

    def start(self) -> object: ...

    def stop(self) -> None: ...


class _FirstSocketProxy(proxy.ConceptProxy):
    """Real ConceptProxy that records the exact first accepted socket
    object and when its handler actually completed (fixture call-
    through observers only; product construction and handling run
    unchanged through super())."""

    def __init__(
        self,
        address: tuple[str, int],
        upstream: str,
        engine: _ObservedEngine,
        client_timeout: float,
        delivery_timeout: float,
    ) -> None:
        self.first_accepted: socket.socket | None = None
        self.first_finished = threading.Event()
        self.first_finished_at: float | None = None
        super().__init__(
            address,
            upstream,
            engine,
            client_timeout=client_timeout,
            delivery_timeout=delivery_timeout,
        )

    def get_request(self) -> tuple[socket.socket, object]:
        sock, addr = super().get_request()
        if self.first_accepted is None:
            self.first_accepted = sock
        return sock, addr

    def process_request(
        self,
        request: socket.socket | tuple[bytes, socket.socket],
        client_address: object,
    ) -> None:
        first = self.first_accepted is not None and request is self.first_accepted
        try:
            return super().process_request(request, client_address)
        finally:
            if first:
                self.first_finished_at = time.monotonic()
                self.first_finished.set()


class _DelayedSseMain(BaseHTTPRequestHandler):
    """Synthetic main upstream that delays its complete SSE response
    after reading the request (downstream work longer than the
    delivery budget is possible); class-level source/delay/recorded
    like the frozen JSON-only _DelayedMain."""

    protocol_version = "HTTP/1.1"
    source: bytes = b""
    delay: float = 0.0
    recorded: list[dict[str, object]] = []

    def do_POST(self) -> None:  # noqa: N802
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.__class__.recorded.append(
            {
                "path": self.path,
                "headers": dict(self.headers.items()),
                "body": body,
            }
        )
        if self.__class__.delay:
            time.sleep(self.__class__.delay)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(self.__class__.source)))
        self.end_headers()
        self.wfile.write(self.__class__.source)

    def log_message(self, *_args: object) -> None:
        return


class _PacedSocketProxy(_FirstSocketProxy):
    """Real ConceptProxy that additionally constrains the accepted
    socket's explicit send buffer (bounded fixture control): the
    kernel cannot fully accept the moderate matched payload before
    the first paced read, so both the short-budget negative and the
    matched generous positive run the identical native backpressure
    producer."""

    def get_request(self) -> tuple[socket.socket, object]:
        sock, addr = super().get_request()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, _PACED_BUF)
        return sock, addr


ProxyFactory = Callable[
    [tuple[str, int], str, _ObservedEngine, float, float], proxy.ConceptProxy
]


class _DeliveryHarness:
    """One real ConceptProxy with an explicit final-delivery budget
    (delivery_timeout) and incoming-intake budget (client_timeout),
    a real engine (qualified Pandoc, real tiny SQLite), a real
    validating reviewer and synthetic loopback main/review upstreams.
    All owned serve/handler threads are actually joined with
    assertions on close."""

    def __init__(
        self,
        delivery_timeout: float = CLIENT_DELIVERY_TIMEOUT_SECONDS,
        client_timeout: float = CLIENT_REQUEST_TIMEOUT_SECONDS,
        main_handler: type[BaseHTTPRequestHandler] = _MainUpstream,
        proxy_factory: ProxyFactory | None = None,
        usage_observer: Callable[[dict[str, object]], None] | None = None,
    ) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "delivery.sqlite"
        _build_db(self.db, unigram=_BUILD_UNIGRAM)
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = _json_completed(CLEAN)
        _MainUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        _FakeUpstream.recorded = []
        # Partial-setup ownership: track constructed servers and
        # actually started serve threads separately; on any setup
        # failure, join every actually started thread and close every
        # constructed server (never shutdown an unstarted server),
        # preserving the original setup exception.
        constructed: list[HTTPServer] = []
        serving: list[tuple[HTTPServer, threading.Thread]] = []
        try:
            self.main_server = _OwnedThreadingServer(
                ("127.0.0.1", 0), main_handler
            )
            constructed.append(self.main_server)
            self.review_server = _OwnedThreadingServer(
                ("127.0.0.1", 0), _FakeUpstream
            )
            constructed.append(self.review_server)
            for server in (self.main_server, self.review_server):
                thread = threading.Thread(
                    target=server.serve_forever, daemon=True
                )
                # Owned BEFORE the fallible start: a start that
                # succeeds and then raises still leaves this exact
                # thread for the containment cleanup below.
                serving.append((server, thread))
                thread.start()
            reviewer = ResponsesReviewer(
                f"http://127.0.0.1:{self.review_server.server_port}/v1",
                "test-model",
                timeout=5.0,
                api_key="fake-key",
            )
            self.engine = _ObservedEngine(
                self.db, reviewer, pandoc=_real_spec()
            )
            if proxy_factory is None:

                def proxy_factory(
                    address: tuple[str, int],
                    upstream: str,
                    engine: _ObservedEngine,
                    client: float,
                    delivery: float,
                ) -> proxy.ConceptProxy:
                    return proxy.ConceptProxy(
                        address,
                        upstream,
                        engine,
                        client_timeout=client,
                        delivery_timeout=delivery,
                        usage_observer=usage_observer,
                    )

            self.proxy_server = proxy_factory(
                ("127.0.0.1", 0),
                f"http://127.0.0.1:{self.main_server.server_port}",
                self.engine,
                client_timeout,
                delivery_timeout,
            )
            constructed.append(self.proxy_server)
            thread = threading.Thread(
                target=self.proxy_server.serve_forever, daemon=True
            )
            # Owned BEFORE the fallible start (same window as above).
            serving.append((self.proxy_server, thread))
            thread.start()
        except BaseException:
            # Only a TRULY started serve loop (thread ident set) is
            # shut down and joined; a never-started one is skipped.
            # Every constructed server socket is closed, and the
            # original setup exception is preserved.
            for srv, thread in serving:
                if thread.ident is None:
                    continue
                srv.shutdown()
                thread.join(10)
                assert not thread.is_alive(), (
                    "owned serve thread did not end on partial setup"
                )
            for srv in constructed:
                srv.server_close()
            self.temp.cleanup()
            raise
        self.threads = [thread for _srv, thread in serving]

    @property
    def proxy_port(self) -> int:
        return self.proxy_server.server_port

    def close(self) -> None:
        self.proxy_server.shutdown()
        self.main_server.shutdown()
        self.review_server.shutdown()
        for thread in self.threads:
            thread.join(10)
            assert not thread.is_alive(), "owned serve_forever thread not ended"
        for server in (self.main_server, self.review_server):
            for handler_thread in server.handler_threads:
                handler_thread.join(10)
                assert not handler_thread.is_alive(), (
                    "owned handler thread not ended"
                )
        self.proxy_server.server_close()
        self.main_server.server_close()
        self.review_server.server_close()
        self.temp.cleanup()


class DeliveryGuardDirectTests(unittest.TestCase):
    """Order 021-a requirements 1/3/7 on the owned guard primitives:
    real socketpair transport, real timer thread/Event, actual joins
    on every path, exact captured-socket interruption, bounded
    startup charging, partial-start containment and budget
    representability (no silently disabled timer)."""

    def test_validate_rejects_invalid_and_unsupported_durations(self) -> None:
        for bad in (
            True,
            False,
            "30",
            None,
            0,
            -1,
            float("nan"),
            float("inf"),
            float("-inf"),
            1e300,
            10**400,
            threading.TIMEOUT_MAX * 2,
        ):
            with self.assertRaises(ValueError):
                delivery_transport.validate_delivery_budget(bad)
        self.assertEqual(
            delivery_transport.validate_delivery_budget(30.0), 30.0
        )
        self.assertEqual(delivery_transport.validate_delivery_budget(1), 1.0)

    def test_interrupts_blocked_write_at_the_deadline(self) -> None:
        a, b = socket.socketpair()
        guard = delivery_transport.DeliveryGuard(a, 0.4)
        started = time.monotonic()
        try:
            with contextlib.suppress(OSError):
                a.sendall(b"x" * 8_000_000)
            elapsed = time.monotonic() - started
            expired = guard.release()
        finally:
            a.close()
            b.close()
        self.assertTrue(expired)
        self.assertGreaterEqual(elapsed, 0.3)
        self.assertLess(elapsed, 2.5)
        self.assertFalse(guard._guard.is_alive())
        self.assertEqual(_delivery_guard_threads(), [])

    def test_fast_write_not_expired_and_joined(self) -> None:
        a, b = socket.socketpair()
        a.settimeout(3.0)
        b.settimeout(3.0)
        guard = delivery_transport.DeliveryGuard(a, 10.0)
        try:
            a.sendall(b"synthetic-final")
            self.assertEqual(b.recv(64), b"synthetic-final")
            expired = guard.release()
        finally:
            a.close()
            b.close()
        self.assertFalse(expired)
        self.assertFalse(guard._guard.is_alive())
        self.assertEqual(_delivery_guard_threads(), [])

    def test_released_guard_same_socket_late_traffic(self) -> None:
        # A completed delivery cancels and joins the real guard;
        # traffic on the SAME socket after the original deadline must
        # still flow (release fully ends the timer's ownership).
        a, b = socket.socketpair()
        a.settimeout(3.0)
        b.settimeout(3.0)
        guard = delivery_transport.DeliveryGuard(a, 0.3)
        try:
            a.sendall(b"first")
            self.assertEqual(b.recv(5), b"first")
            early = guard.release()
            self.assertFalse(guard._guard.is_alive())
            time.sleep(0.35)
            a.sendall(b"synthetic-late")
            self.assertEqual(b.recv(15), b"synthetic-late")
        finally:
            a.close()
            b.close()
        self.assertFalse(early)

    def test_racing_late_completion_loses_to_expiry(self) -> None:
        a, b = socket.socketpair()
        a.settimeout(3.0)
        b.settimeout(3.0)
        # The byte is produced AFTER the anchored 0.05 s deadline: a
        # late or racing completion loses to the expired clock.
        guard = delivery_transport.DeliveryGuard(a, 0.05)

        def late_producer() -> None:
            time.sleep(0.2)
            with contextlib.suppress(OSError):
                b.sendall(b"late")

        thread = threading.Thread(target=late_producer)
        thread.start()
        try:
            with contextlib.suppress(OSError):
                a.recv(64)
            thread.join(2)
            self.assertFalse(thread.is_alive())
            expired = guard.release()
        finally:
            a.close()
            b.close()
        self.assertTrue(expired)
        self.assertFalse(guard._guard.is_alive())

    def test_release_is_idempotent_and_thread_ends(self) -> None:
        a, b = socket.socketpair()
        guard = delivery_transport.DeliveryGuard(a, 10.0)
        first = guard.release()
        second = guard.release()
        self.assertFalse(first)
        self.assertFalse(second)
        self.assertFalse(guard._guard.is_alive())
        self.assertEqual(_delivery_guard_threads(), [])
        a.close()
        b.close()

    def test_expired_guard_other_socket_late_traffic(self) -> None:
        a, b = socket.socketpair()
        other_a, other_b = socket.socketpair()
        for s in (a, b, other_a, other_b):
            s.settimeout(2.0)
        # A's guard expires and joins; B is a different live
        # connection whose genuinely late traffic still flows exactly.
        guard = delivery_transport.DeliveryGuard(a, 0.3)
        try:
            time.sleep(0.35)
            expired = guard.release()
            self.assertTrue(expired)
            self.assertFalse(guard._guard.is_alive())
            other_a.sendall(b"other-late")
            self.assertEqual(other_b.recv(64), b"other-late")
        finally:
            a.close()
            b.close()
            other_a.close()
            other_b.close()

    def test_deadline_anchors_before_guard_startup(self) -> None:
        # Startup is inside the clock: a deliberately delayed guard
        # thread start consumes real budget before the timer runs.
        a, b = socket.socketpair()
        real_start = threading.Thread.start
        delay = 0.3

        def controlled_start(thread: threading.Thread) -> None:
            if thread.name == _GUARD_NAME:
                time.sleep(delay)
            return real_start(thread)

        with mock.patch.object(threading.Thread, "start", controlled_start):
            guard = delivery_transport.DeliveryGuard(a, 2.0)
        try:
            remaining = guard._deadline - time.monotonic()
            self.assertLess(remaining, 2.0 - delay + 0.05)
            self.assertGreater(remaining, 2.0 - delay - 0.3)
            expired = guard.release()
        finally:
            a.close()
            b.close()
        self.assertFalse(expired)
        self.assertFalse(guard._guard.is_alive())

    def test_before_start_failure_never_joins_unstarted_thread(self) -> None:
        a, b = socket.socketpair()
        seen: list[threading.Thread] = []
        joins: list[float] = []
        patchers: list[_Stoppable] = []
        real_start = threading.Thread.start

        def fail_before(thread: threading.Thread) -> None:
            if thread.name == _GUARD_NAME:
                seen.append(thread)
                # Observe any join attempt on this exact unstarted
                # thread instance.
                real_join = thread.join

                def observed_join(timeout: float | None = None) -> None:
                    joins.append(time.monotonic())
                    return real_join(timeout)

                patchers.append(
                    mock.patch.object(thread, "join", observed_join)
                )
                patchers[-1].start()
                raise RuntimeError("synthetic before-start failure")
            return real_start(thread)

        try:
            with (
                mock.patch.object(threading.Thread, "start", fail_before),
                self.assertRaisesRegex(RuntimeError, "synthetic before-start"),
            ):
                delivery_transport.DeliveryGuard(a, 1.0)
        finally:
            for patcher in patchers:
                patcher.stop()
            a.close()
            b.close()
        self.assertEqual(len(seen), 1)
        # A never-started thread has no ident and must never be
        # joined: zero observed join calls on the exact instance, and
        # no owned guard thread survives the failure.
        self.assertIsNone(seen[0].ident)
        self.assertEqual(joins, [])
        self.assertEqual(_delivery_guard_threads(), [])

    def test_after_start_failure_cancels_and_joins_started_thread(self) -> None:
        a, b = socket.socketpair()
        seen: list[threading.Thread] = []
        joins: list[float] = []
        patchers: list[_Stoppable] = []
        real_start = threading.Thread.start

        def fail_after(thread: threading.Thread) -> None:
            if thread.name == _GUARD_NAME:
                real_start(thread)
                seen.append(thread)
                real_join = thread.join

                def observed_join(timeout: float | None = None) -> None:
                    joins.append(time.monotonic())
                    return real_join(timeout)

                patchers.append(
                    mock.patch.object(thread, "join", observed_join)
                )
                patchers[-1].start()
                raise RuntimeError("synthetic after-start failure")
            return real_start(thread)

        try:
            with (
                mock.patch.object(threading.Thread, "start", fail_after),
                self.assertRaisesRegex(RuntimeError, "synthetic after-start"),
            ):
                delivery_transport.DeliveryGuard(a, 10.0)
        finally:
            for patcher in patchers:
                patcher.stop()
            a.close()
            b.close()
        # The actually started guard was cancelled and ACTUALLY joined
        # (one real owner join on the exact known thread) before the
        # failure propagated.
        self.assertEqual(len(seen), 1)
        self.assertIsNotNone(seen[0].ident)
        self.assertEqual(len(joins), 1)
        self.assertFalse(seen[0].is_alive())
        self.assertEqual(_delivery_guard_threads(), [])

    def test_already_ended_started_thread_is_joined(self) -> None:
        a, b = socket.socketpair()
        seen: list[threading.Thread] = []
        joins: list[float] = []
        patchers: list[_Stoppable] = []
        real_start = threading.Thread.start

        def fail_after_ended(thread: threading.Thread) -> None:
            if thread.name == _GUARD_NAME:
                real_start(thread)
                seen.append(thread)
                # Controlled bounded join establishes that the
                # tiny-budget guard ACTUALLY ended before the startup
                # failure is raised.
                thread.join(2.0)
                self.assertFalse(thread.is_alive())
                real_join = thread.join

                def observed_join(timeout: float | None = None) -> None:
                    joins.append(time.monotonic())
                    return real_join(timeout)

                patchers.append(
                    mock.patch.object(thread, "join", observed_join)
                )
                patchers[-1].start()
                raise RuntimeError("synthetic ended-thread failure")
            return real_start(thread)

        try:
            with (
                mock.patch.object(threading.Thread, "start", fail_after_ended),
                self.assertRaisesRegex(
                    RuntimeError, "synthetic ended-thread"
                ),
            ):
                delivery_transport.DeliveryGuard(a, 0.02)
        finally:
            for patcher in patchers:
                patcher.stop()
            a.close()
            b.close()
        # A guard thread that started and already ended still receives
        # a separate actual owner join (on the exact known thread)
        # before the failure propagates.
        self.assertEqual(len(seen), 1)
        self.assertIsNotNone(seen[0].ident)
        self.assertEqual(len(joins), 1)
        self.assertFalse(seen[0].is_alive())
        self.assertEqual(_delivery_guard_threads(), [])


class DeliveryConstructorWiringTests(unittest.TestCase):
    """Order 021-a requirement 1/8: the actual constructor
    default/override/rejection-before-bind, owned loopback port 0
    only (the fixed service port is never bound)."""

    def test_default_delivery_budget_is_the_configured_constant(self) -> None:
        server = proxy.ConceptProxy(
            ("127.0.0.1", 0), "http://127.0.0.1:1", _DummyEngine()
        )
        try:
            self.assertEqual(
                server.delivery_timeout, CLIENT_DELIVERY_TIMEOUT_SECONDS
            )
            self.assertEqual(
                server.client_timeout, CLIENT_REQUEST_TIMEOUT_SECONDS
            )
            self.assertEqual(server.header_timeout, MAIN_HEADER_TIMEOUT_SECONDS)
            self.assertEqual(server.capture_timeout, 30.0)
        finally:
            server.server_close()

    def test_explicit_delivery_budget_stored(self) -> None:
        server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            "http://127.0.0.1:1",
            _DummyEngine(),
            delivery_timeout=7.5,
        )
        try:
            self.assertEqual(server.delivery_timeout, 7.5)
        finally:
            server.server_close()

    def test_positional_delivery_budget_rejected(self) -> None:
        # Deliberate: delivery_timeout is keyword-only, appended AFTER
        # the existing parameters without reordering them, so a 9th
        # positional argument must be rejected.
        with self.assertRaises(TypeError):
            proxy.ConceptProxy(  # type: ignore[call-arg]
                ("127.0.0.1", 0),
                "http://127.0.0.1:1",
                _DummyEngine(),
                30.0,
                None,
                None,
                5.0,
                1.0,
                2.0,
            )

    def test_invalid_delivery_budget_rejected_before_bind(self) -> None:
        # Invalid budgets must raise before any bind allocation:
        # server_bind is observed, not just "a ValueError somewhere".
        class BindObserving(proxy.ConceptProxy):
            bound = False

            def server_bind(self) -> None:
                type(self).bound = True
                super().server_bind()

        for bad in (
            True,
            False,
            "30",
            None,
            float("inf"),
            float("-inf"),
            float("nan"),
            0,
            -1,
            1e300,
            10**400,
            threading.TIMEOUT_MAX * 2,
        ):
            BindObserving.bound = False
            with self.assertRaises(ValueError):
                BindObserving(
                    ("127.0.0.1", 0),
                    "http://127.0.0.1:1",
                    _DummyEngine(),
                    delivery_timeout=cast(float, bad),
                )
            self.assertFalse(BindObserving.bound)
        # The observing subclass itself must be closed if a bind did
        # occur (it never does for the rejected values above).
        BindObserving.bound = False

    def test_legacy_positional_shape_compatibility(self) -> None:
        # The pre-021 positional constructor shape keeps working on an
        # owned loopback port 0: timeout, trace_dir and usage_observer
        # stay in their original positions and delivery_timeout keeps
        # its named 30 s default.
        temp = tempfile.TemporaryDirectory()
        observer: list[dict[str, object]] = []
        server: proxy.ConceptProxy | None = None
        try:
            server = proxy.ConceptProxy(
                ("127.0.0.1", 0),
                "http://127.0.0.1:1",
                _DummyEngine(),
                5.0,
                Path(temp.name),
                observer.append,
            )
            self.assertEqual(server.capture_timeout, 5.0)
            self.assertEqual(
                server.delivery_timeout, CLIENT_DELIVERY_TIMEOUT_SECONDS
            )
            self.assertEqual(
                server.client_timeout, CLIENT_REQUEST_TIMEOUT_SECONDS
            )
            self.assertEqual(server.header_timeout, MAIN_HEADER_TIMEOUT_SECONDS)
        finally:
            if server is not None:
                server.server_close()
            temp.cleanup()


class DeliveryNativeProxyTests(unittest.TestCase):
    """Order 021-a requirement 6 on the actual proxy: real loopback
    main server and client, native kernel-bounded writes, measured
    elapsed observations and same-proxy recovery (no live Qwen)."""

    def test_nonreading_client_stalled_write_closed_bounded(self) -> None:
        # The client sends the request and then neither reads nor
        # closes: only the server-side delivery deadline can release
        # the native blocking write.  Handler completion is observed
        # by an actual server-side call-through, and the stalled
        # socket is drained only AFTER the handler returned and a
        # healthy next request completed.
        harness = _DeliveryHarness(
            delivery_timeout=1.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        clients: list[socket.socket] = []
        try:
            answer = _stall_answer()
            _MainUpstream.source = _json_completed(answer)
            body = _contract_body(False, input_text=CLEAN)
            data = _head(
                len(body), (("Content-Type", "application/json"),)
            ) + body
            a = socket.create_connection(
                ("127.0.0.1", harness.proxy_port), timeout=5
            )
            clients.append(a)
            started = time.monotonic()
            a.sendall(data)
            self.assertTrue(first.first_finished.wait(6.0))
            self.assertIsNotNone(first.first_finished_at)
            elapsed = cast(float, first.first_finished_at) - started
            # The close is bounded by the 1.0 s delivery budget, not
            # by the fixture closing the client first.
            self.assertGreaterEqual(elapsed, 0.85)
            self.assertLess(elapsed, 6.0)
            # The exact accepted socket object is actually closed by
            # the product after the stalled delivery (direct object
            # proof, not an event assumption).
            accepted = first.first_accepted
            self.assertIsNotNone(accepted)
            assert accepted is not None
            self.assertEqual(accepted.fileno(), -1)
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(harness.engine.repair_calls, [answer])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(_delivery_guard_threads(), [])
            # Healthy next request on the SAME real proxy (starts
            # only after the first handler returned).
            _MainUpstream.source = _json_completed(CLEAN)
            status, payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(len(_MainUpstream.recorded), 2)
            # Now, and only now, the stalled socket is drained
            # (bounded): the server closed it, so the peer observes
            # reset/EOF with a partial body and exactly one status
            # line.
            full = len(_json_completed(answer))
            result = _drain(a, 5.0)
            self.assertTrue(result.closed)
            self.assertTrue(
                result.data.startswith(b"HTTP/1.0 200 OK"), result.data[:80]
            )
            self.assertEqual(result.data.count(b"HTTP/1.0 "), 1)
            self.assertLess(len(result.data), full)
            self.assertGreater(len(result.data), 1000)
        finally:
            for sock in clients:
                with contextlib.suppress(OSError):
                    sock.close()
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])

    def test_paced_reader_matched_pair_short_budget_vs_generous(self) -> None:
        # Finite native matched pair (order 021-a requirement 6):
        # the SAME moderately sized completed JSON, the SAME
        # explicitly constrained accepted-send and client-receive
        # buffers, the SAME recv-4096 + 0.01 s progress schedule and
        # the SAME real upstream/handler differ ONLY in the delivery
        # budget.  Continuous slow progress would defeat any
        # per-write idle timeout, so only the one absolute deadline
        # can close the short-budget send (partial body, one status
        # line, quiet close while the peer stays open); the
        # identical producer under the generous budget delivers the
        # exact complete body with real EOF.
        for budget in (0.12, 3.0):
            with self.subTest(budget=budget):
                harness = _DeliveryHarness(
                    delivery_timeout=budget,
                    client_timeout=30.0,
                    proxy_factory=_PacedSocketProxy,
                )
                first = cast(_FirstSocketProxy, harness.proxy_server)
                guards, guard_patch = _guard_observations()
                clients: list[socket.socket] = []
                try:
                    # The identical moderately sized legal completed
                    # answer in both budgets (the real engine runs
                    # unchanged on it; zero suspicion -> zero review).
                    answer = "a" * 500_000
                    _MainUpstream.source = _json_completed(answer)
                    expected = _MainUpstream.source
                    body = _contract_body(False, input_text=CLEAN)
                    line, headers = _request_parts(body)
                    sock = socket.socket()
                    sock.setsockopt(
                        socket.SOL_SOCKET, socket.SO_RCVBUF, _PACED_BUF
                    )
                    clients.append(sock)
                    started = time.monotonic()
                    try:
                        with guard_patch:
                            sock.settimeout(10.0)
                            sock.connect(("127.0.0.1", harness.proxy_port))
                            sock.sendall(line + headers + body)
                            received = b""
                            progress: list[float] = []
                            try:
                                while True:
                                    chunk = sock.recv(4096)
                                    if not chunk:
                                        break
                                    received += chunk
                                    progress.append(time.monotonic())
                                    time.sleep(0.01)
                            except TimeoutError:
                                self.fail(
                                    "paced client observation timed out "
                                    "without data or EOF"
                                )
                        # Server-side actual handler completion
                        # before any fixture close/drain conclusion.
                        self.assertTrue(first.first_finished.wait(5.0))
                        self.assertIsNotNone(first.first_finished_at)
                    finally:
                        with contextlib.suppress(OSError):
                            sock.close()
                    finished_at = cast(float, first.first_finished_at)
                    elapsed = finished_at - started
                    head, sep, payload = received.partition(b"\r\n\r\n")
                    self.assertTrue(sep)
                    self.assertTrue(
                        head.startswith(b"HTTP/1.0 200 OK"), head[:80]
                    )
                    self.assertEqual(received.count(b"HTTP/1.0 "), 1)
                    # The declared header is exact in both budgets:
                    # the real body length and content type were
                    # announced (the short case still announced the
                    # full body even though only a prefix arrived).
                    self.assertIn(b"Content-Type: application/json", head)
                    self.assertTrue(
                        head.endswith(
                            f"Content-Length: {len(expected)}".encode()
                        )
                    )
                    # Continuous native progress on the identical
                    # schedule: actual byte-progress observations
                    # before the handler finished, every gap far
                    # below a 0.12 s per-write idle reference.
                    before_finish = [t for t in progress if t < finished_at]
                    self.assertGreaterEqual(len(before_finish), 3)
                    gaps = [
                        later - earlier
                        for earlier, later in zip(
                            before_finish, before_finish[1:], strict=False
                        )
                    ]
                    self.assertGreater(len(gaps), 0)
                    self.assertLess(max(gaps), 0.12)
                    self.assertEqual(len(_MainUpstream.recorded), 1)
                    self.assertEqual(harness.engine.repair_calls, [answer])
                    self.assertEqual(len(_FakeUpstream.recorded), 0)
                    self.assertEqual(len(guards), 1)
                    self.assertTrue(guards[0]._released)
                    if budget == 0.12:
                        # The absolute deadline lost: partial payload
                        # (never labelled complete), elapsed at the
                        # budget, guard expired, owned close.
                        self.assertGreater(len(received), 1000)
                        self.assertLess(len(payload), len(expected))
                        self.assertGreaterEqual(elapsed, 0.1)
                        self.assertLess(elapsed, 5.0)
                        self.assertTrue(guards[0]._state["expired"])
                    else:
                        # The identical producer, generous budget:
                        # exact complete body and real EOF, guard
                        # released without expiry.
                        self.assertEqual(payload, expected)
                        self.assertLess(elapsed, 5.0)
                        self.assertFalse(guards[0]._state["expired"])
                    self.assertFalse(guards[0]._guard.is_alive())
                    accepted = first.first_accepted
                    self.assertIsNotNone(accepted)
                    assert accepted is not None
                    self.assertEqual(accepted.fileno(), -1)
                    self.assertEqual(_delivery_guard_threads(), [])
                    # Healthy next request on the SAME real proxy.
                    _MainUpstream.source = _json_completed(CLEAN)
                    status, _payload = _harness_post(harness.proxy_server)
                    self.assertEqual(status, 200)
                finally:
                    for client in clients:
                        with contextlib.suppress(OSError):
                            client.close()
                    harness.close()
                self.assertEqual(_delivery_guard_threads(), [])


    def test_spent_startup_closes_before_emission(self) -> None:
        # Successful guard startup that already consumed the whole
        # budget: the anchored absolute clock has passed before the
        # owning handler can begin emission (and the real worker
        # target has not yet run), so the handler closes quietly with
        # zero status/body bytes - one attempt, actual joined guard,
        # no second response.
        harness = _DeliveryHarness(
            delivery_timeout=0.08,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        # The timer interrupt is shutdown(SHUT_RDWR) on the exact
        # socket; the ordinary product close path (socketserver
        # shutdown_request) always performs shutdown(SHUT_WR) first,
        # so only a SHUT_RDWR call proves the timer target ran.
        rdwr_calls: list[float] = []
        run_patchers: list[_Stoppable] = []
        real_shutdown = socket.socket.shutdown

        def observed_shutdown(sock: socket.socket, how: int) -> None:
            if (
                first.first_accepted is not None
                and sock is first.first_accepted
                and how == socket.SHUT_RDWR
            ):
                rdwr_calls.append(time.monotonic())
            return real_shutdown(sock, how)

        try:
            _MainUpstream.source = _json_completed(CLEAN)
            real_start = threading.Thread.start

            def slow_start(thread: threading.Thread) -> None:
                if thread.name == _GUARD_NAME:
                    # Startup consumes the whole 0.08 s budget, and
                    # a further finite scheduler delay keeps the real
                    # pure-timer target from having run by the time
                    # the handler performs its pre-emission check.
                    time.sleep(0.12)
                    real_run = thread.run

                    def delayed_run() -> None:
                        time.sleep(0.2)
                        real_run()

                    # Properly scoped patch: it STAYS ACTIVE through
                    # the actual owner join / handler completion
                    # (stopped only after the handler returned), so
                    # restoring it when Thread.start returns could
                    # not invalidate the unscheduled-target premise.
                    run_patchers.append(
                        mock.patch.object(thread, "run", delayed_run)
                    )
                    run_patchers[-1].start()
                return real_start(thread)

            body = _contract_body(False, input_text=CLEAN)
            data = _head(
                len(body), (("Content-Type", "application/json"),)
            ) + body
            try:
                with (
                    mock.patch.object(
                        threading.Thread, "start", slow_start
                    ),
                    mock.patch.object(
                        socket.socket, "shutdown", observed_shutdown
                    ),
                ):
                    result, forwards, reviews = _raw_post(
                        harness.proxy_server, data
                    )
                # Actual handler-completion proof (server-side
                # call-through) BEFORE the scoped run patch is
                # stopped: the owned guard was cancelled and actually
                # joined inside the handler, not inferred from the
                # client wire.
                self.assertTrue(first.first_finished.wait(5.0))
            finally:
                # Stop the scoped run patch reliably even if an
                # assertion or the request itself raises.
                for patcher in run_patchers:
                    patcher.stop()
            self.assertTrue(result.closed)
            self.assertEqual(result.data, b"")
            self.assertEqual((forwards, reviews), (1, 0))
            self.assertEqual(harness.engine.repair_calls, [CLEAN])
            # The real timer target never interrupted the exact
            # socket: zero SHUT_RDWR (timer) calls, so the quiet
            # close came from the synchronous pre-emission expired
            # check, not from the timer worker.
            self.assertEqual(rdwr_calls, [])
            self.assertEqual(_delivery_guard_threads(), [])
            # Healthy next request on the SAME real proxy.
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])

    def test_successful_completion_guard_joined_not_expired(self) -> None:
        # One healthy small response: the observed real guard is
        # released before the handler returns, its thread actually
        # ended, and the elapsed state is not expired.
        harness = _DeliveryHarness(
            delivery_timeout=10.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        guards: list[delivery_transport.DeliveryGuard] = []
        real_guard = delivery_transport.DeliveryGuard
        try:
            _MainUpstream.source = _json_completed(CLEAN)

            def make_guard(
                sock: socket.socket, budget: float
            ) -> delivery_transport.DeliveryGuard:
                guard = real_guard(sock, budget)
                guards.append(guard)
                return guard

            with mock.patch.object(
                delivery_transport, "DeliveryGuard", side_effect=make_guard
            ):
                status, payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(
                json.loads(payload.decode())["output"][0]["content"][0][
                    "text"
                ],
                CLEAN,
            )
            self.assertEqual(len(guards), 1)
            # Guard state is observed only after the handler actually
            # returned (server-side call-through completion).
            self.assertTrue(first.first_finished.wait(5.0))
            guard = guards[0]
            self.assertTrue(guard._released)
            self.assertFalse(guard._guard.is_alive())
            self.assertFalse(guard._state["expired"])
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(_delivery_guard_threads(), [])
        finally:
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])


class DeliveryPhaseErrorTests(unittest.TestCase):
    """Order 021-a requirements 2/4/7 on the actual proxy: controlled
    call-through delays and failures at the owned stdlib writer
    boundary (clearly separated from the native wire proofs above),
    each with matched generous positives and ACTUAL measured phase
    timings (requested sleep durations are never treated as measured
    durations)."""

    # Bounded privacy-canary cases (requirement 8): the request
    # canary must never reach the diagnostic streams; the response
    # canary legitimately rides the intended client wire as partial
    # body bytes; the exception canary (thrown in the synthetic
    # failure) must never reach the diagnostic streams either.
    _RESPONSE_CANARY = "SYNTHETIC_021_DELIVERY_RESPONSE_CANARY_NOT_A_CREDENTIAL"
    _EXCEPTION_CANARY = "SYNTHETIC_021_DELIVERY_EXCEPTION_CANARY_NOT_A_CREDENTIAL"

    def _delayed_write(
        self, first: _FirstSocketProxy, delays: dict[int, float]
    ) -> tuple[contextlib.AbstractContextManager[object], list[dict[str, object]]]:
        writer_cls = _writer_cls()
        real_write = writer_cls.write
        counts = {"n": 0}
        phases: list[dict[str, object]] = []
        names = {1: "status_headers", 2: "body"}

        def delayed_write(writer: _WriterLike, b: bytes) -> int:
            if first.first_accepted is not None and writer._sock is first.first_accepted:
                counts["n"] += 1
                name = names.get(counts["n"], f"write_{counts['n']}")
                start_at = time.monotonic()
                delay = delays.get(counts["n"], 0.0)
                if delay:
                    time.sleep(delay)
                try:
                    result = real_write(writer, b)
                except OSError:
                    # A failed write is a measured phase too (its
                    # attempt finished against the one clock).
                    phases.append(
                        {
                            "name": name,
                            "start_at": start_at,
                            "done_at": time.monotonic(),
                            "ok": False,
                        }
                    )
                    raise
                phases.append(
                    {
                        "name": name,
                        "start_at": start_at,
                        "done_at": time.monotonic(),
                        "ok": True,
                    }
                )
                return result
            return real_write(writer, b)

        return mock.patch.object(writer_cls, "write", delayed_write), phases

    def _phase(self, phases: list[dict[str, object]], name: str) -> dict[str, object]:
        for phase in phases:
            if phase["name"] == name:
                return phase
        raise AssertionError(f"measured phase {name} not observed: {phases}")

    def test_status_header_phase_delay_loses_to_budget(self) -> None:
        # Controlled call-through: the status/header phase (one
        # native buffered write) is delayed past the whole delivery
        # budget, so no response byte is accepted and the connection
        # closes with zero bytes.
        for budget, expect_ok in ((1.0, False), (3.0, True)):
            with self.subTest(budget=budget):
                harness = _DeliveryHarness(
                    delivery_timeout=budget,
                    client_timeout=30.0,
                    proxy_factory=_FirstSocketProxy,
                )
                first = cast(_FirstSocketProxy, harness.proxy_server)
                guards, guard_patch = _guard_observations()
                delay_patch, phases = self._delayed_write(first, {1: 1.3})
                try:
                    _MainUpstream.source = _json_completed(CLEAN)
                    expected = _MainUpstream.source
                    with guard_patch, delay_patch:
                        client = http.client.HTTPConnection(
                            "127.0.0.1", harness.proxy_port, timeout=10
                        )
                        try:
                            body = _contract_body(False, input_text=CLEAN)
                            client.request(
                                "POST",
                                "/v1/responses",
                                body=body,
                                headers={"Content-Length": str(len(body))},
                            )
                            started = time.monotonic()
                            if expect_ok:
                                response = client.getresponse()
                                payload = response.read()
                                elapsed = time.monotonic() - started
                                self.assertEqual(response.status, 200)
                                self.assertEqual(payload, expected)
                                self.assertLess(elapsed, 3.0)
                            else:
                                with self.assertRaises(
                                    (
                                        http.client.RemoteDisconnected,
                                        ConnectionResetError,
                                    )
                                ):
                                    client.getresponse()
                                elapsed = time.monotonic() - started
                                self.assertGreaterEqual(elapsed, 0.9)
                                self.assertLess(elapsed, 4.0)
                        finally:
                            client.close()
                    self.assertEqual(len(guards), 1)
                    self.assertTrue(first.first_finished.wait(5.0))
                    header = self._phase(phases, "status_headers")
                    header_duration = cast(float, header["done_at"]) - cast(
                        float, header["start_at"]
                    )
                    self.assertGreater(header_duration, 0.9)
                    self.assertEqual(
                        guards[0]._state["expired"], not expect_ok
                    )
                    self.assertFalse(guards[0]._guard.is_alive())
                    self.assertEqual(len(_MainUpstream.recorded), 1)
                    self.assertEqual(_delivery_guard_threads(), [])
                    # Healthy next request on the SAME real proxy.
                    status, _payload = _harness_post(harness.proxy_server)
                    self.assertEqual(status, 200)
                finally:
                    harness.close()
                self.assertEqual(_delivery_guard_threads(), [])

    def test_cumulative_phases_each_below_jointly_over_budget(self) -> None:
        # Controlled call-through: the measured status/header phase
        # and the measured body phase each fit below the budget
        # individually, but their sum exceeds it - only the one
        # absolute deadline can catch this.  The same producer and
        # delay map run the matched generous positive.
        for budget, expect_ok in ((1.0, False), (3.0, True)):
            with self.subTest(budget=budget):
                harness = _DeliveryHarness(
                    delivery_timeout=budget,
                    client_timeout=30.0,
                    proxy_factory=_FirstSocketProxy,
                )
                first = cast(_FirstSocketProxy, harness.proxy_server)
                guards, guard_patch = _guard_observations()
                delay_patch, phases = self._delayed_write(
                    first, {1: 0.6, 2: 0.6}
                )
                try:
                    _MainUpstream.source = _json_completed(CLEAN)
                    expected = _MainUpstream.source
                    with guard_patch, delay_patch:
                        client = http.client.HTTPConnection(
                            "127.0.0.1", harness.proxy_port, timeout=10
                        )
                        try:
                            body = _contract_body(False, input_text=CLEAN)
                            client.request(
                                "POST",
                                "/v1/responses",
                                body=body,
                                headers={"Content-Length": str(len(body))},
                            )
                            if expect_ok:
                                response = client.getresponse()
                                payload = response.read()
                                self.assertEqual(response.status, 200)
                                self.assertEqual(payload, expected)
                            else:
                                # Headers were delivered (each phase
                                # fit); the body write lands after
                                # expiry.
                                response = client.getresponse()
                                self.assertEqual(response.status, 200)
                                with self.assertRaises(
                                    (
                                        http.client.IncompleteRead,
                                        http.client.RemoteDisconnected,
                                        ConnectionResetError,
                                    )
                                ):
                                    response.read()
                        finally:
                            client.close()
                    self.assertEqual(len(guards), 1)
                    self.assertTrue(first.first_finished.wait(5.0))
                    header = self._phase(phases, "status_headers")
                    body_phase = self._phase(phases, "body")
                    header_duration = cast(float, header["done_at"]) - cast(
                        float, header["start_at"]
                    )
                    body_duration = cast(float, body_phase["done_at"]) - cast(
                        float, body_phase["start_at"]
                    )
                    self.assertEqual(len(phases), 2)
                    # ACTUAL measured phase durations: each phase
                    # below the 1.0 s budget, while the combined
                    # phases (header entry to body completion,
                    # failed write included) exceed it.
                    self.assertLess(header_duration, 1.0)
                    self.assertLess(body_duration, 1.0)
                    self.assertGreater(
                        cast(float, body_phase["done_at"])
                        - cast(float, header["start_at"]),
                        1.0,
                    )
                    self.assertEqual(
                        guards[0]._state["expired"], not expect_ok
                    )
                    self.assertFalse(guards[0]._guard.is_alive())
                    self.assertEqual(len(_MainUpstream.recorded), 1)
                    self.assertEqual(_delivery_guard_threads(), [])
                    status, _payload = _harness_post(harness.proxy_server)
                    self.assertEqual(status, 200)
                finally:
                    harness.close()
                self.assertEqual(_delivery_guard_threads(), [])

    def test_late_body_completion_loses_to_expiry(self) -> None:
        # Controlled call-through: headers emit promptly, then the
        # body write completes after the anchored deadline - the late
        # (racing) completion loses to expiry.
        for budget, expect_ok in ((1.0, False), (3.0, True)):
            with self.subTest(budget=budget):
                harness = _DeliveryHarness(
                    delivery_timeout=budget,
                    client_timeout=30.0,
                    proxy_factory=_FirstSocketProxy,
                )
                first = cast(_FirstSocketProxy, harness.proxy_server)
                guards, guard_patch = _guard_observations()
                delay_patch, phases = self._delayed_write(first, {2: 1.3})
                try:
                    _MainUpstream.source = _json_completed(CLEAN)
                    expected = _MainUpstream.source
                    with guard_patch, delay_patch:
                        client = http.client.HTTPConnection(
                            "127.0.0.1", harness.proxy_port, timeout=10
                        )
                        try:
                            body = _contract_body(False, input_text=CLEAN)
                            client.request(
                                "POST",
                                "/v1/responses",
                                body=body,
                                headers={"Content-Length": str(len(body))},
                            )
                            if expect_ok:
                                response = client.getresponse()
                                payload = response.read()
                                self.assertEqual(response.status, 200)
                                self.assertEqual(payload, expected)
                            else:
                                response = client.getresponse()
                                self.assertEqual(response.status, 200)
                                with self.assertRaises(
                                    (
                                        http.client.IncompleteRead,
                                        http.client.RemoteDisconnected,
                                        ConnectionResetError,
                                    )
                                ):
                                    response.read()
                        finally:
                            client.close()
                    self.assertEqual(len(guards), 1)
                    self.assertTrue(first.first_finished.wait(5.0))
                    body_phase = self._phase(phases, "body")
                    body_duration = cast(float, body_phase["done_at"]) - cast(
                        float, body_phase["start_at"]
                    )
                    self.assertGreater(body_duration, 0.9)
                    self.assertEqual(
                        guards[0]._state["expired"], not expect_ok
                    )
                    self.assertFalse(guards[0]._guard.is_alive())
                    self.assertEqual(len(_MainUpstream.recorded), 1)
                    self.assertEqual(_delivery_guard_threads(), [])
                    status, _payload = _harness_post(harness.proxy_server)
                    self.assertEqual(status, 200)
                finally:
                    harness.close()
                self.assertEqual(_delivery_guard_threads(), [])

    def _raw_wire_post(
        self,
        harness: _DeliveryHarness,
        body: bytes,
        extra: tuple[tuple[str, str], ...] = (),
    ) -> tuple[bytes, bool]:
        """One contract request on a raw owned socket, draining the
        FULL wire until actual EOF/reset so appended bytes after the
        first declared body are visible (HTTPResponse.read stops at
        the first Content-Length)."""
        sock = socket.create_connection(
            ("127.0.0.1", harness.proxy_port), timeout=10
        )
        try:
            sock.sendall(
                _head(
                    len(body),
                    (("Content-Type", "application/json"),) + extra,
                )
                + body
            )
            result = _drain(sock, 10.0)
        finally:
            sock.close()
        return result.data, result.closed

    def test_flush_failure_quiet_close_no_second_response(self) -> None:
        # Controlled call-through: the common explicit flush after a
        # completed body write fails; the handler closes quietly with
        # no second response and no hang.  The full raw wire until
        # actual EOF is captured so an appended partial second
        # response could not hide behind the first declared
        # Content-Length.
        harness = _DeliveryHarness(
            delivery_timeout=10.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        writer_cls = _writer_cls()
        real_flush = writer_cls.flush
        flushes: list[dict[str, object]] = []
        failed_once = {"done": False}
        guards, guard_patch = _guard_observations()

        def failing_flush(writer: _WriterLike) -> None:
            if (
                first.first_accepted is not None
                and writer._sock is first.first_accepted
            ):
                # Scalar snapshot AT the flush call (mutable guard
                # fields must not be re-read after the join).
                flushes.append(
                    {
                        "released": [g._released for g in guards],
                        "alive": [g._guard.is_alive() for g in guards],
                    }
                )
                if not failed_once["done"]:
                    failed_once["done"] = True
                    raise OSError("synthetic flush failure")
            return real_flush(writer)

        try:
            _MainUpstream.source = _json_completed(CLEAN)
            expected = _MainUpstream.source
            with guard_patch, mock.patch.object(
                writer_cls, "flush", failing_flush
            ):
                body = _contract_body(False, input_text=CLEAN)
                wire, closed = self._raw_wire_post(harness, body)
            self.assertTrue(closed)
            # Exactly one status line on the FULL wire, the exact
            # expected first body, and nothing appended after it.
            self.assertEqual(wire.count(b"HTTP/1.0 "), 1)
            head, sep, payload = wire.partition(b"\r\n\r\n")
            self.assertTrue(sep)
            self.assertTrue(head.startswith(b"HTTP/1.0 200 OK"), head[:80])
            self.assertEqual(payload, expected)
            self.assertEqual(len(guards), 1)
            self.assertTrue(first.first_finished.wait(5.0))
            # The FIRST actual flush is the common explicit one
            # inside the active delivery guard (before release); the
            # later stdlib no-op flushes happen after the actual
            # join.
            self.assertTrue(flushes)
            self.assertEqual(flushes[0]["released"], [False])
            self.assertEqual(flushes[0]["alive"], [True])
            self.assertFalse(guards[0]._state["expired"])
            self.assertFalse(guards[0]._guard.is_alive())
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(_delivery_guard_threads(), [])
            # Healthy next request on the SAME real proxy.
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])

    def test_flush_delay_consumes_same_anchored_clock(self) -> None:
        # Controlled call-through (labeled controlled orchestration,
        # separated from native wire proof): the first actual flush
        # is delayed past the anchored budget.  The native
        # unbuffered flush is a no-op, so the bytes may already have
        # reached the client before expiry - the proof is the
        # internal expiry classification, the actual flush phase
        # measurement, the owned close and the no-second-response
        # full-wire check, with a matched generous positive.
        for budget, expect_ok in ((1.0, False), (3.0, True)):
            with self.subTest(budget=budget):
                harness = _DeliveryHarness(
                    delivery_timeout=budget,
                    client_timeout=30.0,
                    proxy_factory=_FirstSocketProxy,
                )
                first = cast(_FirstSocketProxy, harness.proxy_server)
                writer_cls = _writer_cls()
                real_flush = writer_cls.flush
                flush_phases: list[dict[str, object]] = []
                guards, guard_patch = _guard_observations()

                def delayed_flush(
                    writer: _WriterLike,
                    bound_first: _FirstSocketProxy = first,
                    bound_flush_phases: list[dict[str, object]] = flush_phases,
                    bound_real_flush: Callable[
                        [_WriterLike], None
                    ] = real_flush,
                ) -> None:
                    if (
                        bound_first.first_accepted is not None
                        and writer._sock is bound_first.first_accepted
                    ) and not bound_flush_phases:
                        start_at = time.monotonic()
                        time.sleep(1.3)
                        try:
                            return bound_real_flush(writer)
                        finally:
                            # The measured phase surrounds the REAL
                            # flush call: completion is recorded
                            # around the actual call (finally also on
                            # failure), like the measured write
                            # phases - never a timestamp named before
                            # the call.
                            bound_flush_phases.append(
                                {
                                    "start_at": start_at,
                                    "done_at": time.monotonic(),
                                }
                            )
                    return bound_real_flush(writer)

                try:
                    _MainUpstream.source = _json_completed(CLEAN)
                    expected = _MainUpstream.source
                    with guard_patch, mock.patch.object(
                        writer_cls, "flush", delayed_flush
                    ):
                        body = _contract_body(False, input_text=CLEAN)
                        wire, closed = self._raw_wire_post(harness, body)
                    self.assertTrue(closed)
                    self.assertEqual(wire.count(b"HTTP/1.0 "), 1)
                    head, sep, payload = wire.partition(b"\r\n\r\n")
                    self.assertTrue(sep)
                    self.assertTrue(
                        head.startswith(b"HTTP/1.0 200 OK"), head[:80]
                    )
                    self.assertEqual(payload, expected)
                    self.assertEqual(len(guards), 1)
                    self.assertTrue(first.first_finished.wait(5.0))
                    self.assertEqual(len(flush_phases), 1)
                    flush_duration = cast(
                        float, flush_phases[0]["done_at"]
                    ) - cast(float, flush_phases[0]["start_at"])
                    self.assertGreater(flush_duration, 0.9)
                    if not expect_ok:
                        self.assertGreater(flush_duration, 1.0)
                    # The delayed flush is classified against the
                    # SAME anchored clock as the rest of the phase.
                    self.assertEqual(
                        guards[0]._state["expired"], not expect_ok
                    )
                    self.assertFalse(guards[0]._guard.is_alive())
                    self.assertEqual(len(_MainUpstream.recorded), 1)
                    self.assertEqual(_delivery_guard_threads(), [])
                    status, _payload = _harness_post(harness.proxy_server)
                    self.assertEqual(status, 200)
                finally:
                    harness.close()
                self.assertEqual(_delivery_guard_threads(), [])

    def test_early_client_disconnect_quiet_close(self) -> None:
        # Native: the client disconnects (RST) while the bounded send
        # is in flight; the handler closes quietly with zero second
        # response and the same proxy recovers.
        harness = _DeliveryHarness(
            delivery_timeout=10.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        clients: list[socket.socket] = []
        sock: socket.socket | None = None
        try:
            answer = _stall_answer()
            _MainUpstream.source = _json_completed(answer)
            body = _contract_body(False, input_text=CLEAN)
            line, headers = _request_parts(body)
            sock = socket.create_connection(
                ("127.0.0.1", harness.proxy_port), timeout=5
            )
            clients.append(sock)
            sock.sendall(line + headers + body)
            sock.settimeout(10.0)
            received = b""
            while len(received) < 1_000_000:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                received += chunk
            # Force an RST so the in-flight native write fails.
            sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0)
            )
            with contextlib.suppress(OSError):
                sock.close()
            clients.remove(sock)
            sock = None
            self.assertTrue(first.first_finished.wait(6.0))
            accepted = first.first_accepted
            self.assertIsNotNone(accepted)
            assert accepted is not None
            self.assertEqual(accepted.fileno(), -1)
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(harness.engine.repair_calls, [answer])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(_delivery_guard_threads(), [])
            # Healthy next request on the SAME real proxy.
            _MainUpstream.source = _json_completed(CLEAN)
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            if sock is not None:
                with contextlib.suppress(OSError):
                    sock.close()
            for client in clients:
                with contextlib.suppress(OSError):
                    client.close()
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])


    def test_partial_body_unexpected_exception_no_second_response(self) -> None:
        # Actual handler / full raw wire (order 021-a requirements
        # 3/4/7): the exact accepted writer call-through emits the
        # status/headers and a small prefix of the real body, then
        # raises a synthetic unexpected exception (RuntimeError)
        # while the peer remains connected and writable and the
        # generous guard has not expired.  With emission already
        # begun, the outer generic exception path must close quietly:
        # the FULL wire to actual EOF shows exactly one status line
        # and only that known partial body - no appended 502 or
        # fallback bytes, no second writer write - and the exact
        # owned guard is released and actually ended before the same
        # proxy is reused.  The externally required no-second-
        # response behavior is proven on the wire, not by a boolean
        # source detail.
        #
        # The same case doubles as a bounded requirement 8 privacy-
        # canary case: the synthetic canary in the request text and
        # Authorization header is absent from every observable
        # output (the full wire and the captured std streams, whose
        # product diagnostic boundary is the silent handle_error).
        canary = "SYNTHETIC_021_DELIVERY_PRIVACY_CANARY_NOT_A_CREDENTIAL"
        prefix_len = 256
        harness = _DeliveryHarness(
            delivery_timeout=10.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        writer_cls = _writer_cls()
        real_write = writer_cls.write
        writes = {"n": 0}
        failed = {"done": False}
        guards, guard_patch = _guard_observations()
        stdout_sink = io.StringIO()
        stderr_sink = io.StringIO()

        def partial_write(writer: _WriterLike, b: bytes) -> int:
            if (
                first.first_accepted is not None
                and writer._sock is first.first_accepted
            ):
                writes["n"] += 1
                if writes["n"] == 2 and not failed["done"]:
                    # The body write: only a small prefix of the
                    # real body reaches the still-connected peer,
                    # then the synthetic unexpected exception.
                    real_write(writer, b[:prefix_len])
                    failed["done"] = True
                    # The synthetic unexpected exception message
                    # itself carries the exception canary.
                    raise RuntimeError(
                        "synthetic mid-body failure: "
                        + self._EXCEPTION_CANARY
                    )
            return real_write(writer, b)

        try:
            # The completed synthetic answer itself carries the
            # response canary: legitimate response bytes on the
            # intended client wire (its partial prefix).
            answer = (self._RESPONSE_CANARY + " ") * 50
            _MainUpstream.source = _json_completed(answer)
            expected = _MainUpstream.source
            self.assertGreater(len(expected), prefix_len)
            with (
                guard_patch,
                mock.patch.object(writer_cls, "write", partial_write),
                contextlib.redirect_stdout(stdout_sink),
                contextlib.redirect_stderr(stderr_sink),
            ):
                body = _contract_body(False, input_text=canary)
                wire, closed = self._raw_wire_post(
                    harness,
                    body,
                    extra=(("Authorization", "Bearer " + canary),),
                )
            self.assertTrue(closed)
            # Exactly one status line on the FULL wire and nothing
            # appended after the known partial body.
            self.assertEqual(wire.count(b"HTTP/1.0 "), 1)
            head, sep, payload = wire.partition(b"\r\n\r\n")
            self.assertTrue(sep)
            self.assertTrue(head.startswith(b"HTTP/1.0 200 OK"), head[:80])
            # The declared length is the REAL body length; only the
            # known prefix was delivered.
            self.assertTrue(
                head.endswith(f"Content-Length: {len(expected)}".encode())
            )
            self.assertEqual(payload, expected[:prefix_len])
            self.assertLess(len(payload), len(expected))
            # Exactly two writer writes on the accepted socket
            # (status/headers + partial body): no second response
            # was attempted through the writer after the exception.
            self.assertEqual(writes["n"], 2)
            self.assertTrue(failed["done"])
            # Bounded privacy canaries: the request canary is
            # absent from the wire and from the actual diagnostic
            # streams; the response and exception canaries are
            # absent from the diagnostic streams (the response
            # canary legitimately appears in the delivered partial
            # body bytes - no general response secrecy is claimed
            # on the intended client wire).
            self.assertNotIn(canary.encode(), wire)
            logs = stdout_sink.getvalue() + stderr_sink.getvalue()
            self.assertNotIn(canary, logs)
            self.assertNotIn(self._RESPONSE_CANARY, logs)
            self.assertNotIn(self._EXCEPTION_CANARY, logs)
            # One main, one repair (the delivered CLEAN answer),
            # zero review, one delivery attempt.
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(harness.engine.repair_calls, [answer])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            # Guard state observed only after the handler actually
            # returned (server-side call-through completion).
            self.assertTrue(first.first_finished.wait(5.0))
            self.assertEqual(len(guards), 1)
            self.assertTrue(guards[0]._released)
            self.assertFalse(guards[0]._state["expired"])
            self.assertFalse(guards[0]._guard.is_alive())
            accepted = first.first_accepted
            self.assertIsNotNone(accepted)
            assert accepted is not None
            self.assertEqual(accepted.fileno(), -1)
            self.assertEqual(_delivery_guard_threads(), [])
            # The same real proxy is reused healthy after the
            # failed partial delivery.
            _MainUpstream.source = _json_completed(CLEAN)
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])

class DeliveryFailureBoundaryTests(unittest.TestCase):
    """Order 021-a requirements 4/5/8 on the actual handler: failed
    guard startup, contract 400 flush ownership, protocol 502 and
    original non-200 upstream semantics, all under the one delivery
    lifecycle."""

    def test_guard_startup_failure_quiet_close_no_second_response(self) -> None:
        # Real handler: the guard's real Thread.start fails on the
        # FIRST attempt (after main and engine work already
        # completed).  The handler closes quietly with zero response
        # bytes - no second response, no 502, one attempt - and the
        # same proxy recovers.
        harness = _DeliveryHarness(delivery_timeout=10.0, client_timeout=30.0)
        started: list[threading.Thread] = []
        real_start = threading.Thread.start

        def controlled_start(thread: threading.Thread) -> None:
            if thread.name == _GUARD_NAME:
                started.append(thread)
                if len(started) == 1:
                    raise RuntimeError("synthetic delivery startup failure")
            return real_start(thread)

        try:
            _MainUpstream.source = _json_completed(CLEAN)
            body = _contract_body(False, input_text=CLEAN)
            data = _head(
                len(body), (("Content-Type", "application/json"),)
            ) + body
            with mock.patch.object(threading.Thread, "start", controlled_start):
                result, forwards, reviews = _raw_post(
                    harness.proxy_server, data
                )
            self.assertEqual(len(started), 1)
            self.assertTrue(all(not t.is_alive() for t in started))
            self.assertTrue(result.closed)
            self.assertEqual(result.data, b"")
            self.assertEqual((forwards, reviews), (1, 0))
            self.assertEqual(harness.engine.repair_calls, [CLEAN])
            self.assertEqual(_delivery_guard_threads(), [])
            # Healthy next request on the SAME real proxy.
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])

    def test_contract_400_first_actual_flush_inside_guard(self) -> None:
        # Real handler: the fixed content-free contract 400 (store
        # capability) is a post-intake response, so its FIRST actual
        # flush must be observed inside the active delivery guard
        # (released False, guard alive) - scalar snapshots taken at
        # each flush call on the exact accepted socket.
        harness = _DeliveryHarness(
            delivery_timeout=10.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        writer_cls = _writer_cls()
        real_flush = writer_cls.flush
        flushes: list[dict[str, object]] = []
        guards: list[delivery_transport.DeliveryGuard] = []
        real_guard = delivery_transport.DeliveryGuard

        def make_guard(
            sock: socket.socket, budget: float
        ) -> delivery_transport.DeliveryGuard:
            guard = real_guard(sock, budget)
            guards.append(guard)
            return guard

        def observed_flush(writer: _WriterLike) -> None:
            if (
                first.first_accepted is not None
                and writer._sock is first.first_accepted
            ):
                # Scalar snapshot AT the flush call.
                flushes.append(
                    {
                        "released": [g._released for g in guards],
                        "alive": [g._guard.is_alive() for g in guards],
                    }
                )
            return real_flush(writer)

        try:
            with mock.patch.object(
                delivery_transport, "DeliveryGuard", side_effect=make_guard
            ), mock.patch.object(writer_cls, "flush", observed_flush):
                body = json.dumps(
                    {
                        "model": "m",
                        "input": "synthetic",
                        "store": True,
                        "stream": False,
                    }
                ).encode()
                client = http.client.HTTPConnection(
                    "127.0.0.1", harness.proxy_port, timeout=10
                )
                try:
                    client.request(
                        "POST",
                        "/v1/responses",
                        body=body,
                        headers={"Content-Type": "application/json"},
                    )
                    response = client.getresponse()
                    payload = response.read()
                    self.assertEqual(response.status, 400)
                    self.assertIn(b"invalid_request", payload)
                finally:
                    client.close()
            self.assertEqual(len(_MainUpstream.recorded), 0)
            self.assertEqual(harness.engine.repair_calls, [])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(len(guards), 1)
            self.assertTrue(flushes)
            self.assertEqual(flushes[0]["released"], [False])
            self.assertEqual(flushes[0]["alive"], [True])
            self.assertTrue(first.first_finished.wait(5.0))
            self.assertFalse(guards[0]._guard.is_alive())
        finally:
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])

    def test_protocol_502_under_delivery_then_healthy(self) -> None:
        # Real handler: a declared stream request answered with a
        # non-SSE content type is a bounded upstream protocol 502
        # (fixed payload), emitted under the delivery lifecycle,
        # with zero engine/review work and same-proxy recovery.
        harness = _DeliveryHarness(delivery_timeout=10.0, client_timeout=30.0)
        try:
            _MainUpstream.source = _json_completed(CLEAN)
            _MainUpstream.content_type = "application/json"
            body = _contract_body(True, input_text=CLEAN)
            data = _head(
                len(body), (("Content-Type", "application/json"),)
            ) + body
            result, forwards, reviews = _raw_post(harness.proxy_server, data)
            self.assertTrue(result.data.startswith(b"HTTP/1.0 502"), result.data[:80])
            self.assertTrue(result.closed)
            self.assertEqual((forwards, reviews), (1, 0))
            self.assertEqual(harness.engine.repair_calls, [])
            self.assertEqual(_delivery_guard_threads(), [])
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])

    def test_original_non200_upstream_kept_not_blanket_502(self) -> None:
        # Real handler: a genuine upstream non-200 keeps its original
        # status and exact body (no blanket 502, no repair, no
        # review), still under the delivery lifecycle.
        harness = _DeliveryHarness(
            delivery_timeout=10.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        try:
            original_body = (
                b'{"error":{"message":"synthetic upstream failure"}}'
            )
            _MainUpstream.status = 500
            _MainUpstream.source = original_body
            body = _contract_body(False, input_text=CLEAN)
            client = http.client.HTTPConnection(
                "127.0.0.1", harness.proxy_port, timeout=10
            )
            try:
                client.request(
                    "POST",
                    "/v1/responses",
                    body=body,
                    headers={"Content-Length": str(len(body))},
                )
                response = client.getresponse()
                payload = response.read()
                self.assertEqual(response.status, 500)
                self.assertEqual(payload, original_body)
            finally:
                client.close()
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(harness.engine.repair_calls, [])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            # Guard-thread state is observed only after the handler
            # actually returned (server-side call-through
            # completion).
            self.assertTrue(first.first_finished.wait(5.0))
            self.assertEqual(_delivery_guard_threads(), [])
            # Recovery: back to a healthy 200 on the same proxy.
            _MainUpstream.status = 200
            _MainUpstream.source = _json_completed(CLEAN)
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])
class DeliveryChainTests(unittest.TestCase):
    """Order 021-a requirement 8 (with the frozen chain semantics
    preserved): real JSON and delayed-SSE integration through the
    actual proxy/RepairEngine/qualified Pandoc/tiny
    SQLite/ResponsesReviewer with synthetic loopback main/review -
    useful two-target exact repair preserving Unicode/combining/
    code/math/HTML/links, exact allowlisted forward body and
    credentials, isolated one-review shape/usage, no-suspicion zero
    review, safely completed-original fallback, and downstream
    phases that outlast the short delivery budget before it anchors."""

    def test_chain_useful_two_targets_json_and_delayed_sse(self) -> None:
        for stream in (False, True):
            with self.subTest(stream=stream):
                usage: list[dict[str, object]] = []
                harness = _DeliveryHarness(
                    delivery_timeout=30.0,
                    client_timeout=30.0,
                    main_handler=_DelayedSseMain if stream else _MainUpstream,
                    usage_observer=usage.append,
                )
                try:
                    _FakeUpstream.payload = _review_payload(
                        [_prop("t0"), _prop("t1")],
                        usage={
                            "input_tokens": 4,
                            "output_tokens": 6,
                            "total_tokens": 10,
                        },
                    )
                    if stream:
                        _DelayedSseMain.source = _sse_baseline_utf8(USEFUL_018)
                        _DelayedSseMain.delay = 0.0
                        _DelayedSseMain.recorded = []
                    else:
                        _MainUpstream.source = _json_completed(USEFUL_018)
                        _MainUpstream.content_type = "application/json"
                    body = _contract_body(stream, input_text=USEFUL_018)
                    client = http.client.HTTPConnection(
                        "127.0.0.1", harness.proxy_port, timeout=30
                    )
                    try:
                        client.request(
                            "POST",
                            "/v1/responses",
                            body=body,
                            headers={
                                "Content-Type": "application/json",
                                "Accept": "application/json",
                                "Authorization": "Bearer synthetic-main-key",
                                "Host": "synthetic-client-host.invalid",
                                "X-Concept-Request-ID": "synthetic-client-id",
                            },
                        )
                        response = client.getresponse()
                        payload = response.read()
                    finally:
                        client.close()
                    self.assertEqual(response.status, 200, payload[:200])
                    self.assertEqual(len(_FakeUpstream.recorded), 1)
                    self.assertEqual(harness.engine.repair_calls, [USEFUL_018])
                    # Exact allowlisted forward: the exact body, and
                    # only content-type/accept/authorization reach
                    # main (never hop-by-hop, ids or the reviewer
                    # credential).
                    main_recorded = (
                        _DelayedSseMain.recorded
                        if stream
                        else _MainUpstream.recorded
                    )
                    self.assertEqual(len(main_recorded), 1)
                    record = main_recorded[0]
                    self.assertEqual(record["body"], body)
                    fwd = cast(dict[str, str], record["headers"])
                    self.assertEqual(
                        fwd.get("Authorization"), "Bearer synthetic-main-key"
                    )
                    self.assertEqual(fwd.get("Content-Type"), "application/json")
                    # The client's own Host (and request id) are
                    # allowlist-dropped; the outbound Host recorded
                    # by main is the http.client-generated upstream
                    # one, never the client's value.
                    self.assertNotEqual(
                        fwd.get("Host"), "synthetic-client-host.invalid"
                    )
                    self.assertNotIn("X-Concept-Request-ID", fwd)
                    if stream:
                        final = [
                            json.loads(block[5:])
                            for block in payload.decode().split("\n\n")
                            if block.startswith("data:")
                        ]
                        completed = next(
                            e
                            for e in final
                            if e.get("type") == "response.completed"
                        )
                        text = completed["response"]["output"][0][
                            "content"
                        ][0]["text"]
                    else:
                        text = json.loads(payload.decode())[
                            "output"
                        ][0]["content"][0]["text"]
                    self.assertEqual(text, EXPECTED_USEFUL_018)
                    # Protected slices preserved exactly in the
                    # decoded final composed answer (code, TeX, HTML,
                    # link and the NFC-unstable decomposed/combining
                    # line); the raw wire escapes TeX backslashes, so
                    # the decoded text is the comparison basis.
                    for marker in (
                        "`presenetliv`",
                        "\\(x^2\\)",
                        "<b>presenetliv</b>",
                        "[zapis](http://example.com/slo)",
                        "e\u0301",
                    ):
                        self.assertIn(marker, text)
                    # Isolated single text-only batch request: the
                    # actual recorded review route/headers/body carry
                    # the separate fake review key, the ordered two
                    # targets, the exact bounded output cap, and no
                    # main credential, session or media linkage (the
                    # actual request key set is exactly this).
                    self.assertEqual(len(_FakeUpstream.recorded), 1)
                    rrecord = _FakeUpstream.recorded[0]
                    self.assertEqual(rrecord["path"], "/v1/responses")
                    rheaders = cast(dict[str, str], rrecord["headers"])
                    self.assertEqual(
                        rheaders.get("Authorization"), "Bearer fake-key"
                    )
                    self.assertEqual(
                        rheaders.get("Content-Type"), "application/json"
                    )
                    rval = json.loads(cast(bytes, rrecord["body"]))
                    self.assertEqual(
                        set(rval),
                        {
                            "model",
                            "stream",
                            "store",
                            "max_output_tokens",
                            "input",
                        },
                    )
                    self.assertEqual(rval["model"], "test-model")
                    self.assertIs(rval["stream"], False)
                    self.assertIs(rval["store"], False)
                    self.assertEqual(rval["max_output_tokens"], 1536)
                    rinput = rval["input"]
                    self.assertEqual(len(rinput), 1)
                    self.assertEqual(rinput[0]["role"], "user")
                    rcontent = cast(list[dict[str, str]], rinput[0]["content"])
                    self.assertEqual(len(rcontent), 1)
                    self.assertEqual(rcontent[0]["type"], "input_text")
                    rprompt = rcontent[0]["text"]
                    # Ordered two targets: t0 (first occurrence) is
                    # before t1 in the actual prompt.
                    self.assertLess(rprompt.index("t0"), rprompt.index("t1"))
                    self.assertNotIn(
                        "synthetic-main-key", cast(bytes, rrecord["body"]).decode()
                    )
                    # Isolated one-review usage record.
                    self.assertEqual(
                        usage,
                        [
                            {
                                "review_calls": 1,
                                "reviewer_usage": {
                                    "input_tokens": 4,
                                    "output_tokens": 6,
                                    "total_tokens": 10,
                                },
                            }
                        ],
                    )
                finally:
                    harness.close()

    def test_chain_no_suspicion_zero_review_exact_bytes(self) -> None:
        # Delayed-SSE main with no suspicion: the exact unchanged
        # main bytes are forwarded with zero review calls.
        harness = _DeliveryHarness(
            delivery_timeout=30.0,
            client_timeout=30.0,
            main_handler=_DelayedSseMain,
        )
        try:
            _DelayedSseMain.source = _sse_baseline_utf8(CLEAN)
            _DelayedSseMain.delay = 0.0
            _DelayedSseMain.recorded = []
            status, payload = _harness_post(
                harness.proxy_server, stream=True
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, _DelayedSseMain.source)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine.repair_calls, [CLEAN])
        finally:
            harness.close()

    def test_chain_completed_original_fallback_on_reviewer_failure(self) -> None:
        # A reviewer transport failure (500) still delivers only an
        # already completed original: exact main body, status 200,
        # with same-proxy recovery once the reviewer is healthy.
        harness = _DeliveryHarness(delivery_timeout=30.0, client_timeout=30.0)
        try:
            source = _json_completed(USEFUL_018)
            _MainUpstream.source = source
            _MainUpstream.content_type = "application/json"
            _FakeUpstream.status = 500
            _FakeUpstream.payload = b'{"error":"synthetic reviewer failure"}'
            status, payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(payload, source)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            # Recovery on the SAME proxy once the reviewer is healthy.
            _FakeUpstream.status = 200
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t1")]
            )
            _MainUpstream.source = _json_completed(CLEAN)
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            harness.close()

    def test_chain_long_main_and_review_outlast_short_delivery_budget(self) -> None:
        # Requirement 5: a healthy main phase (1.5 s) and a healthy
        # review phase (1.2 s) that BOTH outlast the 1.0 s delivery
        # budget still deliver the complete repaired answer: the
        # delivery deadline anchors only after response-ready work,
        # so no earlier-started guard or residual timer can cut it
        # off (JSON and delayed-SSE variants).
        for stream in (False, True):
            with self.subTest(stream=stream):
                harness = _DeliveryHarness(
                    delivery_timeout=1.0,
                    client_timeout=30.0,
                    main_handler=_DelayedSseMain if stream else _DelayedMain,
                )
                forward_calls: list[tuple[float, float]] = []
                review_calls: list[tuple[float, float]] = []
                guards, guard_patch = _guard_observations()
                real_forward = proxy.ConceptProxy.forward
                real_review_batch = harness.engine.reviewer.review_batch

                def observed_forward(
                    self: proxy.ConceptProxy,
                    body: bytes,
                    incoming: dict[str, str],
                    bound_real_forward: Callable[
                        [
                            proxy.ConceptProxy,
                            bytes,
                            dict[str, str],
                        ],
                        proxy.Forwarded,
                    ] = real_forward,
                    bound_forward_calls: list[tuple[float, float]] = (
                        forward_calls
                    ),
                ) -> proxy.Forwarded:
                    started_at = time.monotonic()
                    try:
                        return bound_real_forward(self, body, incoming)
                    finally:
                        bound_forward_calls.append(
                            (started_at, time.monotonic())
                        )

                def observed_review_batch(
                    sentence: str,
                    targets: tuple[BatchTarget, ...],
                    bound_real_review_batch: Callable[
                        [str, tuple[BatchTarget, ...]], BatchResult
                    ] = real_review_batch,
                    bound_review_calls: list[tuple[float, float]] = (
                        review_calls
                    ),
                ) -> BatchResult:
                    started_at = time.monotonic()
                    try:
                        return bound_real_review_batch(sentence, targets)
                    finally:
                        bound_review_calls.append(
                            (started_at, time.monotonic())
                        )

                try:
                    _FakeUpstream.delay = 1.2
                    _FakeUpstream.payload = _review_payload(
                        [_prop("t0"), _prop("t1")]
                    )
                    if stream:
                        _DelayedSseMain.source = _sse_baseline_utf8(USEFUL_018)
                        _DelayedSseMain.delay = 1.5
                        _DelayedSseMain.recorded = []
                    else:
                        _DelayedMain.source = _json_completed(USEFUL_018)
                        _DelayedMain.delay = 1.5
                        _DelayedMain.recorded = []
                    started = time.monotonic()
                    with (
                        guard_patch,
                        mock.patch.object(
                            proxy.ConceptProxy, "forward", observed_forward
                        ),
                        mock.patch.object(
                            harness.engine.reviewer,
                            "review_batch",
                            observed_review_batch,
                        ),
                    ):
                        status, payload = _harness_post(
                            harness.proxy_server, stream=stream
                        )
                    wall = time.monotonic() - started
                    self.assertEqual(status, 200, payload[:200])
                    if stream:
                        self.assertEqual(len(_DelayedSseMain.recorded), 1)
                        final = [
                            json.loads(block[5:])
                            for block in payload.decode().split("\n\n")
                            if block.startswith("data:")
                        ]
                        completed = next(
                            e
                            for e in final
                            if e.get("type") == "response.completed"
                        )
                        text = completed["response"]["output"][0][
                            "content"
                        ][0]["text"]
                    else:
                        self.assertEqual(len(_DelayedMain.recorded), 1)
                        text = json.loads(payload.decode())[
                            "output"
                        ][0]["content"][0]["text"]
                    self.assertEqual(text, EXPECTED_USEFUL_018)
                    self.assertEqual(len(_FakeUpstream.recorded), 1)
                    self.assertEqual(harness.engine.repair_calls, [USEFUL_018])
                    # Measured ACTUAL phase boundaries (call-through
                    # at the real forward/reviewer-exchange entry
                    # points): each measured phase outlasted the 1.0
                    # s delivery budget - requested sleeps are not
                    # measured durations.
                    self.assertEqual(len(forward_calls), 1)
                    self.assertEqual(len(review_calls), 1)
                    forward_duration = forward_calls[0][1] - forward_calls[0][0]
                    review_duration = review_calls[0][1] - review_calls[0][0]
                    self.assertGreater(forward_duration, 1.0)
                    self.assertGreater(review_duration, 1.0)
                    # The delivery deadline anchored only AFTER both
                    # measured response-ready phases had completed.
                    self.assertEqual(len(guards), 1)
                    anchor_at = guards[0]._deadline - 1.0
                    self.assertGreaterEqual(anchor_at, forward_calls[0][1])
                    self.assertGreaterEqual(anchor_at, review_calls[0][1])
                    # The whole request took at least the delayed
                    # main phase, yet completed well inside the
                    # bounded observation.
                    self.assertGreaterEqual(wall, 1.5)
                    self.assertLess(wall, 15.0)
                finally:
                    harness.close()


class DeliveryIsolationTests(unittest.TestCase):
    """Order 021-a requirement 7: B's TCP connection is established
    while A is in flight (kernel backlog), but B's request BYTES are
    genuinely late - sent only after the first delivery guard has
    actually been released/joined and its original anchored deadline
    passed.  The guard interrupted only the exact first socket, so
    the second socket survives and completes normally."""

    def test_other_connection_isolation_genuinely_late(self) -> None:
        harness = _DeliveryHarness(
            delivery_timeout=1.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        sockets: list[socket.socket] = []
        a_anchored = threading.Event()
        a_released = threading.Event()
        observations: dict[str, object] = {}
        owned: list[tuple[object, object, tuple[str, int]]] = []
        a_endpoint: tuple[str, int] | None = None
        b_endpoint: tuple[str, int] | None = None
        real_init = delivery_transport.DeliveryGuard.__init__
        real_release = delivery_transport.DeliveryGuard.release

        def observe_init(
            guard: delivery_transport.DeliveryGuard,
            sock: socket.socket,
            budget: float,
        ) -> None:
            real_init(guard, sock, budget)
            peer = sock.getpeername()
            owned.append((guard, sock, peer))
            if a_endpoint is not None and peer == a_endpoint:
                observations["a_guard"] = guard
                a_anchored.set()

        def observe_release(guard: delivery_transport.DeliveryGuard) -> bool:
            expired = real_release(guard)
            if guard is observations.get("a_guard") and not a_released.is_set():
                a_guard = cast(
                    delivery_transport.DeliveryGuard, observations["a_guard"]
                )
                observations.update(
                    a_expired=expired,
                    a_release_at=time.monotonic(),
                    a_owned_thread_ended=not a_guard._guard.is_alive(),
                    a_deadline=a_guard._deadline,
                    counts_before_b_send=[
                        len(_MainUpstream.recorded),
                        len(harness.engine.repair_calls),
                        len(_FakeUpstream.recorded),
                    ],
                )
                a_released.set()
            return expired

        try:
            answer_a = _stall_answer()
            _MainUpstream.source = _json_completed(answer_a)
            _MainUpstream.content_type = "application/json"
            body_a = _contract_body(False, input_text=CLEAN)
            body_b = _contract_body(False, input_text=CLEAN)
            full_a = _head(
                len(body_a), (("Content-Type", "application/json"),)
            ) + body_a
            full_b = _head(
                len(body_b), (("Content-Type", "application/json"),)
            ) + body_b

            a = socket.socket()
            a.bind(("127.0.0.1", 0))
            a.settimeout(5)
            sockets.append(a)
            a_endpoint = a.getsockname()
            b = socket.socket()
            b.bind(("127.0.0.1", 0))
            b.settimeout(5)
            sockets.append(b)
            b_endpoint = b.getsockname()
            with (
                mock.patch.object(
                    delivery_transport.DeliveryGuard, "__init__", observe_init
                ),
                mock.patch.object(
                    delivery_transport.DeliveryGuard, "release", observe_release
                ),
            ):
                a.connect(("127.0.0.1", harness.proxy_port))
                with contextlib.suppress(
                    ConnectionResetError, BrokenPipeError, OSError
                ):
                    a.sendall(full_a)
                # A's delivery guard is anchored and the send is in
                # flight (stalling on the nonreading peer) before B's
                # connection is even established.
                self.assertTrue(a_anchored.wait(6.0))
                b.connect(("127.0.0.1", harness.proxy_port))
                self.assertFalse(a_released.is_set())
                # Wait for the observed real A guard release (the
                # product cancelled and actually joined the owned
                # timer before the call-through release returned).
                self.assertTrue(a_released.wait(6.0))
                # Only now - at or after A's original anchored
                # deadline AND after the observed real A guard
                # release/join - does B send its full request.
                b_send_at = time.monotonic()
                self.assertGreaterEqual(
                    b_send_at, cast(float, observations["a_deadline"])
                )
                self.assertGreaterEqual(
                    b_send_at, cast(float, observations["a_release_at"])
                )
                # A's downstream is complete; B's own main capture
                # (happening after B's send) uses the small CLEAN
                # answer.
                _MainUpstream.source = _json_completed(CLEAN)
                b.sendall(full_b)
                a_result = _drain(a, 6.0)
                b_result = _drain(b, 6.0)
            # The exact A guard was observed released, expired, with
            # its owned timer thread actually ended before any B
            # request byte was sent (A's own downstream work done).
            self.assertTrue(cast(bool, observations["a_expired"]))
            self.assertTrue(cast(bool, observations["a_owned_thread_ended"]))
            self.assertEqual(
                cast("list[int]", observations["counts_before_b_send"]),
                [1, 1, 0],
            )
            # A closed with one status line and a PARTIAL body (the
            # stalled delivery was never completed); B's exact
            # socket survived and completed with the exact response.
            self.assertTrue(a_result.closed)
            self.assertEqual(a_result.data.count(b"HTTP/1.0 "), 1)
            self.assertTrue(
                a_result.data.startswith(b"HTTP/1.0 200 OK"),
                a_result.data[:80],
            )
            full_a_len = len(_json_completed(answer_a))
            self.assertLess(len(a_result.data), full_a_len)
            self.assertGreater(len(a_result.data), 1000)
            self.assertTrue(
                b_result.data.startswith(b"HTTP/1.0 200 OK"),
                b_result.data[:80],
            )
            self.assertTrue(b_result.closed)
            self.assertEqual(b_result.data.count(b"HTTP/1.0 "), 1)
            _bhead, bsep, bpayload = b_result.data.partition(b"\r\n\r\n")
            self.assertTrue(bsep)
            # B's raw-EOF response keeps the exact status/type and
            # declared length of the small CLEAN answer.
            self.assertTrue(_bhead.startswith(b"HTTP/1.0 200 OK"), _bhead[:80])
            self.assertIn(b"Content-Type: application/json", _bhead)
            self.assertTrue(
                _bhead.endswith(
                    f"Content-Length: {len(_json_completed(CLEAN))}".encode()
                )
            )
            self.assertEqual(bpayload, _json_completed(CLEAN))
            self.assertEqual(len(_MainUpstream.recorded), 2)
            self.assertEqual(harness.engine.repair_calls, [answer_a, CLEAN])
            self.assertEqual(_FakeUpstream.recorded, [])
            # Exactly the two owned guards: A's and B's, captured on
            # distinct socket objects for exactly the two known bound
            # client peers; B's guard ended without expiry.
            self.assertEqual(len(owned), 2)
            assert a_endpoint is not None
            assert b_endpoint is not None
            self.assertEqual(
                {peer for _guard, _sock, peer in owned},
                {a_endpoint, b_endpoint},
            )
            captured = [sock for _guard, sock, _peer in owned]
            self.assertIsNot(captured[0], captured[1])
            b_guard = next(
                guard
                for guard, _sock, peer in owned
                if peer == b_endpoint
            )
            self.assertTrue(
                cast(delivery_transport.DeliveryGuard, b_guard)._released
            )
            self.assertFalse(
                cast(delivery_transport.DeliveryGuard, b_guard)._state[
                    "expired"
                ]
            )
            self.assertFalse(
                cast(delivery_transport.DeliveryGuard, b_guard)._guard.is_alive()
            )
        finally:
            for sock in sockets:
                with contextlib.suppress(OSError):
                    sock.close()
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])
class DeliveryMainWiringTests(unittest.TestCase):
    """Order 021-a requirement 1 normal entry: main() reads
    CONCEPT_DELIVERY_TIMEOUT into the real validated constructor;
    the unconfigured entry and old constructor adapters retain the
    compatible named default; invalid values are rejected before
    any validated construction or owned bind; no serving happens
    and the normal 18024 port is never bound."""

    def test_main_reads_concept_delivery_timeout(self) -> None:
        configured = os.environ.get("CONCEPT_PANDOC", "").strip()
        if not configured:
            raise unittest.SkipTest("qualified CONCEPT_PANDOC not configured")
        temp = tempfile.TemporaryDirectory()
        try:
            db = Path(temp.name) / "delivery-main.sqlite"
            _build_db(db, unigram=_BUILD_UNIGRAM)
            seen: dict[str, object] = {}
            created: list[proxy.ConceptProxy] = []

            class Recorder(ResponsesReviewer):
                def __init__(
                    self,
                    base_url: str,
                    model: str,
                    timeout: float = REVIEWER_HTTP_TIMEOUT_SECONDS,
                    api_key: str | None = None,
                    profile: str | Path | None = None,
                ) -> None:
                    super().__init__(
                        base_url,
                        model,
                        timeout=timeout,
                        api_key=api_key,
                        profile=profile,
                    )

            class Port0Proxy(proxy.ConceptProxy):
                def __init__(
                    self,
                    address: tuple[str, int],
                    upstream: str,
                    engine: proxy.RepairEngine,
                    timeout: float = 30.0,
                    trace_dir: Path | None = None,
                    usage_observer: (
                        Callable[[dict[str, object]], None] | None
                    ) = None,
                    *,
                    header_timeout: float = MAIN_HEADER_TIMEOUT_SECONDS,
                    client_timeout: float = CLIENT_REQUEST_TIMEOUT_SECONDS,
                    delivery_timeout: float = CLIENT_DELIVERY_TIMEOUT_SECONDS,
                ) -> None:
                    super().__init__(
                        ("127.0.0.1", 0),
                        upstream,
                        engine,
                        timeout=timeout,
                        trace_dir=trace_dir,
                        usage_observer=usage_observer,
                        header_timeout=header_timeout,
                        client_timeout=client_timeout,
                        delivery_timeout=delivery_timeout,
                    )
                    seen["delivery_timeout"] = self.delivery_timeout
                    created.append(self)

                def serve_forever(self, poll_interval: float = 0.5) -> None:
                    return

            class LegacyPort0Proxy(proxy.ConceptProxy):
                """Old constructor adapter WITHOUT the new keyword:
                the real constructor must apply and validate the
                named default."""

                def __init__(
                    self,
                    address: tuple[str, int],
                    upstream: str,
                    engine: proxy.RepairEngine,
                    timeout: float = 30.0,
                    trace_dir: Path | None = None,
                    usage_observer: (
                        Callable[[dict[str, object]], None] | None
                    ) = None,
                    *,
                    header_timeout: float = MAIN_HEADER_TIMEOUT_SECONDS,
                    client_timeout: float = CLIENT_REQUEST_TIMEOUT_SECONDS,
                ) -> None:
                    super().__init__(
                        ("127.0.0.1", 0),
                        upstream,
                        engine,
                        timeout=timeout,
                        trace_dir=trace_dir,
                        usage_observer=usage_observer,
                        header_timeout=header_timeout,
                        client_timeout=client_timeout,
                    )
                    seen["delivery_timeout"] = self.delivery_timeout
                    created.append(self)

                def serve_forever(self, poll_interval: float = 0.5) -> None:
                    return

            base_env = {
                "CONCEPT_INDEX": str(db),
                "CONCEPT_UPSTREAM_URL": "http://127.0.0.1:1",
                "CONCEPT_REVIEWER_URL": "http://127.0.0.1:9/v1",
                "CONCEPT_PANDOC": configured,
            }
            with mock.patch.object(proxy, "ResponsesReviewer", Recorder):
                # Explicit override: delivery 7.25 independent of
                # the other budgets, on the real validated
                # constructor.
                env = dict(base_env, CONCEPT_DELIVERY_TIMEOUT="7.25")
                with (
                    mock.patch.object(proxy, "ConceptProxy", Port0Proxy),
                    mock.patch.dict(os.environ, env, clear=True),
                ):
                    self.assertEqual(proxy.main(), 0)
                self.assertEqual(seen["delivery_timeout"], 7.25)
                self.assertEqual(len(created), 1)
                self.assertGreater(created[0].server_address[1], 1024)
                self.assertNotEqual(created[0].server_address[1], 18024)
                for server in created:
                    server.server_close()
                created.clear()
                seen.clear()

                # Unconfigured normal entry: the named 30 s
                # constructor default governs, observed through the
                # OLD adapter shape (no delivery keyword at all).
                with (
                    mock.patch.object(proxy, "ConceptProxy", LegacyPort0Proxy),
                    mock.patch.dict(os.environ, base_env, clear=True),
                ):
                    self.assertEqual(proxy.main(), 0)
                self.assertEqual(
                    seen["delivery_timeout"], CLIENT_DELIVERY_TIMEOUT_SECONDS
                )
                self.assertEqual(len(created), 1)
                for server in created:
                    server.server_close()
                created.clear()
                seen.clear()

                # Invalid values are rejected before any validated
                # construction or owned bind.
                for bad_env in ("abc", "inf", "0", "1e300"):
                    env_bad = dict(base_env, CONCEPT_DELIVERY_TIMEOUT=bad_env)
                    with (
                        mock.patch.object(proxy, "ConceptProxy", Port0Proxy),
                        mock.patch.dict(os.environ, env_bad, clear=True),
                        self.assertRaises(ValueError),
                    ):
                        proxy.main()
                    self.assertEqual(created, [])
        finally:
            # Owned bound sockets are closed even on failed
            # assertions (cleanup belongs in finally, not after
            # success lines).
            for server in created:
                server.server_close()
            temp.cleanup()


class DeliveryPrivacyCleanupTests(unittest.TestCase):
    """Order 021-a requirement 8 (bounded): permitted synthetic
    canaries on the delivery failure paths (non-reading stall and
    contract 400) with bounded captured stdout/stderr, default
    tracing off, the actual silent handle_error boundary, and owned
    delivery-guard cleanup after a mixed sequence.  Synthetic
    loopback fixtures only; not a general privacy or security
    certification."""

    _CANARY = "SYNTHETIC_021_DELIVERY_PRIVACY_CANARY_NOT_A_CREDENTIAL"

    def test_synthetic_canary_absent_from_delivery_failures(self) -> None:
        canary = self._CANARY
        harness = _DeliveryHarness(
            delivery_timeout=1.0,
            client_timeout=30.0,
            proxy_factory=_FirstSocketProxy,
        )
        first = cast(_FirstSocketProxy, harness.proxy_server)
        stdout = io.StringIO()
        stderr = io.StringIO()
        clients: list[socket.socket] = []
        try:
            self.assertIsNone(harness.proxy_server.trace_dir)
            body = _contract_body(False, input_text=canary)
            header = (
                ("Authorization", "Bearer " + canary),
                ("X-Synthetic-Private", canary),
                ("Content-Type", "application/json"),
            )
            with (
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                # 1) Non-reading stall: the canary request is fully
                # captured and repaired, then the delivery stalls
                # and closes (client stays OPEN AND UNREAD until the
                # real server-side handler completion is observed;
                # the bounded drain runs only after).  The canary
                # must be absent from the wire and the captured
                # streams, and the stall must not replay downstream
                # work.
                _MainUpstream.source = _json_completed(_stall_answer())
                data = _head(len(body), header) + body
                a = socket.create_connection(
                    ("127.0.0.1", harness.proxy_port), timeout=5
                )
                clients.append(a)
                with contextlib.suppress(
                    ConnectionResetError, BrokenPipeError, OSError
                ):
                    a.sendall(data)
                self.assertTrue(first.first_finished.wait(6.0))
                result = _drain(a, 5.0)
                self.assertTrue(result.closed)
                self.assertNotIn(canary.encode(), result.data)
                self.assertEqual(len(_MainUpstream.recorded), 1)
                self.assertEqual(len(_FakeUpstream.recorded), 0)
                # 2) Contract 400 (store capability): fixed
                # content-free rejection under the delivery
                # lifecycle with the canary in body and headers;
                # zero downstream work, zero canary in the wire.
                before = (
                    len(_MainUpstream.recorded),
                    len(harness.engine.repair_calls),
                    len(_FakeUpstream.recorded),
                )
                store_body = json.dumps(
                    {
                        "model": "m",
                        "input": canary,
                        "store": True,
                        "stream": False,
                    }
                ).encode()
                result2, _f, _r = _raw_post(
                    harness.proxy_server, _head(len(store_body), header) + store_body
                )
                self.assertTrue(
                    result2.data.startswith(b"HTTP/1.0 400"),
                    result2.data[:80],
                )
                self.assertNotIn(canary.encode(), result2.data)
                self.assertEqual(
                    (
                        len(_MainUpstream.recorded),
                        len(harness.engine.repair_calls),
                        len(_FakeUpstream.recorded),
                    ),
                    before,
                )
            # Bounded captured streams: the product diagnostic
            # boundary is the silent handle_error, so nothing
            # request-derived may appear.
            logs = stdout.getvalue() + stderr.getvalue()
            self.assertNotIn(canary, logs)
        finally:
            for sock in clients:
                with contextlib.suppress(OSError):
                    sock.close()
            harness.close()
        self.assertEqual(_delivery_guard_threads(), [])

    def test_no_delivery_guard_threads_after_mixed_sequence(self) -> None:
        harness = _DeliveryHarness(delivery_timeout=1.0, client_timeout=30.0)
        try:
            # 200 healthy
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
            # 400 duplicate Content-Length framing
            body = _contract_body(False, input_text=CLEAN)
            dup = (
                b"POST /v1/responses HTTP/1.1\r\n"
                b"Host: localhost\r\n"
                b"Content-Type: application/json\r\n"
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                b"\r\n" + body
            )
            _response, _f, _r = _raw_post(harness.proxy_server, dup)
            # Large healthy READING response (complete delivery;
            # the actual stall proof lives in the dedicated
            # nonreading test and the finite child - an all-reading
            # send is not stall evidence).
            _MainUpstream.source = _json_completed(_stall_answer())
            status, payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
            self.assertGreater(len(payload), 1_000_000)
        finally:
            harness.close()
        # Every owned guard is released and actually joined by its
        # handler before the harness has joined every handler and
        # serve thread.
        self.assertEqual(_delivery_guard_threads(), [])

    def test_handle_error_silent_on_owned_proxy(self) -> None:
        harness = _DeliveryHarness(delivery_timeout=10.0, client_timeout=30.0)
        try:
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                harness.proxy_server.handle_error(
                    object(), ("127.0.0.1", 0)
                )
            self.assertEqual(stderr.getvalue(), "")
        finally:
            harness.close()


_DELIVERY_HANGING_CHILD_SCRIPT = r"""
import socket, sys, time
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
cv = repo / "concept-verification"
sys.path.insert(0, str(cv))

from tests.test_delivery_transport import (  # noqa: E402
    CLEAN,
    _FakeUpstream,
    _FirstSocketProxy,
    _MainUpstream,
    _contract_body,
    _drain,
    _head,
    _harness_post,
    _stall_answer,
    _DeliveryHarness,
)
from tests.test_responses_contract import _json_completed  # noqa: E402


def main() -> int:
    # The actual existing harness with the real handler-completion
    # observer: real proxy/engine/qualified Pandoc/SQLite/
    # ResponsesReviewer with synthetic main/review; every owned
    # server and thread is actually joined on close.
    harness = _DeliveryHarness(
        delivery_timeout=1.0,
        client_timeout=30.0,
        proxy_factory=_FirstSocketProxy,
    )
    first = harness.proxy_server
    try:
        _MainUpstream.source = _json_completed(_stall_answer())
        body = _contract_body(False, input_text=CLEAN)
        data = _head(len(body), (("Content-Type", "application/json"),)) + body
        sock = socket.create_connection(
            ("127.0.0.1", harness.proxy_port), timeout=5
        )
        started = time.monotonic()
        try:
            sock.sendall(data)
            # The client stays OPEN AND UNREAD: only the server-side
            # delivery deadline can close the stalled native write.
            # Completion is observed by the real server-side
            # call-through (never by reading the peer first).
            if not first.first_finished.wait(6.0):
                print("child: stalled handler did not complete in 6 s")
                return 1
            if first.first_finished_at is None:
                print("child: no handler completion timestamp")
                return 1
            elapsed = first.first_finished_at - started
            if not (0.85 <= elapsed <= 6.0):
                print(
                    f"child: close elapsed {elapsed:.3f} outside 0.85-6.0"
                )
                return 1
            # Only NOW (after actual completion, peer still open) is
            # the bounded drain used: partial body, one status line,
            # real close.
            result = _drain(sock, 5.0)
            if not result.closed:
                print("child: drain after completion saw no close")
                return 1
            if result.data.count(b"HTTP/1.0 ") != 1:
                print("child: expected exactly one status line")
                return 1
            if not result.data.startswith(b"HTTP/1.0 200 OK"):
                print("child: unexpected status line")
                return 1
        finally:
            sock.close()
        # The stalled delivery replayed no extra downstream work.
        if (
            len(_MainUpstream.recorded) != 1
            or len(harness.engine.repair_calls) != 1
            or len(_FakeUpstream.recorded) != 0
        ):
            print("child: stall reached the wrong downstream counts")
            return 1
        # The same real proxy recovers with a healthy request.
        _MainUpstream.source = _json_completed(CLEAN)
        status, _payload = _harness_post(harness.proxy_server)
        if status != 200:
            print(f"child: healthy next status {status}")
            return 1
    finally:
        harness.close()
    print("CHILD_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""


class DeliveryHangingChildTests(unittest.TestCase):
    """Order 021-a requirement 7: a nonreading stalled delivery
    runs in an owned finite parent-supervised ordinary test process
    with bounded kill/reap cleanup, so a bug cannot hang CI.  The
    actual resolved Pandoc binary is explicitly qualified before
    the child proof (an absent explicit env with a qualified PATH
    binary is supported; an explicit missing or wrong-version
    binary fails here, not via the engine's completed-original
    fallback)."""

    def test_hanging_delivery_bounded_in_finite_child(self) -> None:
        try:
            check_pandoc(_real_spec())
        except PandocStartupError as exc:
            self.fail(f"qualified Pandoc prerequisite failed: {exc}")
        proc = subprocess.Popen(
            [
                sys.executable,
                "-B",
                "-c",
                _DELIVERY_HANGING_CHILD_SCRIPT,
                str(REPO_ROOT),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            out, err = proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            proc.kill()
            try:
                out, err = proc.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                self.fail(
                    "bounded post-kill drain of the exact owned child "
                    "did not complete"
                )
            self.fail(
                "hanging delivery child exceeded the finite 120 s "
                f"parent bound (killed/reaped); stderr tail: {err[-500:]}"
            )
        self.assertEqual(
            proc.returncode, 0, f"stdout={out[-800:]} / stderr={err[-800:]}"
        )
        self.assertIn("CHILD_OK", out)
