"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Order 026-a
accepted-request admission: permanent controller and real-proxy tests.

Covers the order's admission requirements (1-8) at both boundaries:
the pure validation policy (exact int/float rules, before-bind
rejection, immutable per-instance retention), the direct controller
(FIFO, capacity, expiry, claim re-check, no thread per rejected
connection, no registry accumulation) and the real ConceptProxy
(fixed 503 codes, zero downstream for rejected entries, owned
startup/shutdown, first-control preservation at worker owner
boundaries, existing contract semantics preserved under admission).
Lifecycle faults are ONE-SHOT (a later attempt delegates to the real
operation): a persistent synthetic join fault would be an invalid
repeat against a settlement loop intended to resolve transient
interruptions.  All owned threads are actually joined with asserted
termination; rejected peers are observed on their real sockets
(exact packet where readable, RST tolerated where the proxy never
read the rejected entry's request bytes).
"""

from __future__ import annotations

import contextlib
import http.client
import io
import json
import socket
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import cast
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import config  # noqa: E402
import proxy  # noqa: E402
import request_admission as ra  # noqa: E402
from qwen_client import ResponsesReviewer  # noqa: E402
from tests.test_capture_transport import _BUILD_UNIGRAM, CLEAN  # noqa: E402
from tests.test_client_transport import (  # noqa: E402
    _drain,
    _head,
    _OwnedThreadingServer,
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
    _sse_completed,
    _sse_delta,
)
from tests.test_runtime_corpus import _build_db  # noqa: E402

_MONITOR = ra._MONITOR_NAME
_WORKER = ra._WORKER_NAME


def _expect_packet(code: str) -> bytes:
    """The fixed content-free bounded 503 for one admission code."""
    body = json.dumps(
        {"error": {"type": "request_admission_error", "code": code}},
        separators=(",", ":"),
    ).encode()
    return (
        b"HTTP/1.0 503 Service Unavailable\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
        b"Connection: close\r\n"
        b"\r\n" + body
    )


def _admission_threads() -> list[threading.Thread]:
    return [
        t
        for t in threading.enumerate()
        if t.name in (_MONITOR, _WORKER) and t.is_alive()
    ]


def _wait(
    predicate: Callable[[], bool], timeout: float = 10.0
) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.005)
    return predicate()


def _raw_fire(port: int, body: bytes) -> socket.socket:
    """Send one request to the proxy and return the un-drained socket."""
    sock = socket.create_connection(("127.0.0.1", port), timeout=5)
    sock.sendall(_head(len(body)) + body)
    return sock


class _DelayedMain(_MainUpstream):
    """Main upstream with a finite response delay for marker bodies.

    Only requests whose body carries the b"held-A-" marker are
    delayed, so concurrent control probes hit the upstream
    immediately while the held request occupies the one active slot.
    """

    delay: float = 0.0

    def do_POST(self) -> None:  # noqa: N802
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.__class__.recorded.append(
            {"path": self.path, "headers": dict(self.headers.items()), "body": body}
        )
        if self.delay and b"held-A-" in body:
            time.sleep(self.delay)
        self.send_response(self.status)
        self.send_header("Content-Type", self.content_type)
        self.send_header("Content-Length", str(len(self.__class__.source)))
        self.end_headers()
        self.wfile.write(self.__class__.source)


class _SseUpstream(_MainUpstream):
    """SSE main upstream that writes its finite source in two parts
    with a small finite delay between them (bounded, test-only)."""

    split_at: int = 0
    gap: float = 0.3

    def do_POST(self) -> None:  # noqa: N802
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.__class__.recorded.append(
            {"path": self.path, "headers": dict(self.headers.items()), "body": body}
        )
        source = self.__class__.source
        self.send_response(self.status)
        self.send_header("Content-Type", self.content_type)
        self.send_header("Content-Length", str(len(source)))
        self.end_headers()
        if self.split_at and 0 < self.split_at < len(source):
            self.wfile.write(source[: self.split_at])
            self.wfile.flush()
            time.sleep(self.gap)
            self.wfile.write(source[self.split_at :])
        else:
            self.wfile.write(source)


class _AdmissionHarness:
    """One real ConceptProxy whose admission policy is the test-only
    patched CURRENT config values for construction only (running
    instances retain their immutable policy).  Real engine (qualified
    Pandoc, real tiny SQLite), real validating reviewer, synthetic
    main/review upstreams; every actually-started owned thread is
    actually joined with asserted termination on close.
    """

    def __init__(
        self,
        *,
        max_queued: int = 16,
        wait_seconds: float = 2.0,
        usage_observer: Callable[[dict[str, object]], None] | None = None,
        main_handler: type[BaseHTTPRequestHandler] = _DelayedMain,
    ) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "admission.sqlite"
        _build_db(self.db, unigram=_BUILD_UNIGRAM)
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = _json_completed(CLEAN)
        _MainUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        _FakeUpstream.recorded = []
        self.main_server = _OwnedThreadingServer(
            ("127.0.0.1", 0), main_handler
        )
        self.review_server = _OwnedThreadingServer(
            ("127.0.0.1", 0), _FakeUpstream
        )
        self.threads: list[threading.Thread] = []
        for server in (self.main_server, self.review_server):
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            self.threads.append(thread)
        reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.review_server.server_port}/v1",
            "test-model",
            timeout=5.0,
            api_key="fake-key",
        )
        self.engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        with (
            mock.patch.object(config, "PROXY_MAX_QUEUED_REQUESTS", max_queued),
            mock.patch.object(config, "PROXY_QUEUE_WAIT_SECONDS", wait_seconds),
        ):
            self.proxy_server = proxy.ConceptProxy(
                ("127.0.0.1", 0),
                f"http://127.0.0.1:{self.main_server.server_port}",
                self.engine,
                usage_observer=usage_observer,
            )
        self.proxy_thread = threading.Thread(
            target=self.proxy_server.serve_forever, daemon=True
        )
        self.proxy_thread.start()
        self.threads.append(self.proxy_thread)

    @property
    def proxy_port(self) -> int:
        return self.proxy_server.server_port

    def post(self, body: bytes) -> tuple[int, bytes]:
        client = http.client.HTTPConnection(
            "127.0.0.1", self.proxy_port, timeout=20
        )
        client.request(
            "POST",
            "/v1/responses",
            body=body,
            headers={"Content-Length": str(len(body))},
        )
        response = client.getresponse()
        payload = response.read()
        client.close()
        return response.status, payload

    def fire(self, body: bytes) -> socket.socket:
        return _raw_fire(self.proxy_port, body)

    def close(self) -> None:
        # Plain helper (not a TestCase): every ownership check is an
        # explicit AssertionError, never a missing assert method.
        # This harness asserts its OWN controller's exact workers and
        # pending ownership; global admission-thread absence is
        # asserted by tests only after every owned instance is
        # closed, so a second healthy instance is never falsely
        # implicated.
        self.proxy_server.shutdown()
        self.main_server.shutdown()
        self.review_server.shutdown()
        for thread in self.threads:
            thread.join(10)
            if thread.is_alive():
                raise AssertionError(
                    "owned serve_forever thread not ended"
                )
        for server in (self.main_server, self.review_server):
            for handler_thread in server.handler_threads:
                handler_thread.join(10)
                if handler_thread.is_alive():
                    raise AssertionError(
                        "owned handler thread not ended"
                    )
        self.proxy_server.server_close()
        self.main_server.server_close()
        self.review_server.server_close()
        admission = self.proxy_server._admission
        for worker in (admission._monitor, admission._worker):
            if (
                worker is not None
                and worker.ident is not None
                and worker.is_alive()
            ):
                raise AssertionError(
                    "owned admission worker not ended"
                )
        if admission.pending_count() != 0:
            raise AssertionError("owned admission entries not released")
        self.temp.cleanup()


class _GatedServer:
    """Controllable admission server boundary (test-only): handler
    runs for the exact admitted entry and blocks until released, so
    the single active slot can be held deterministically."""

    def __init__(self) -> None:
        self.calls: list[tuple[socket.socket, tuple[str, int]]] = []
        self._lock = threading.Lock()
        self._released = 0
        self._cond = threading.Condition(self._lock)

    def release(self) -> None:
        with self._cond:
            self._released += 1
            self._cond.notify_all()

    def wait_calls(self, count: int, timeout: float = 10.0) -> bool:
        with self._cond:
            return self._cond.wait_for(
                lambda: len(self.calls) >= count, timeout
            )

    def finish_request(
        self, request: socket.socket, client_address: tuple[str, int]
    ) -> None:
        with self._cond:
            index = len(self.calls)
            self.calls.append((request, client_address))
            # Wake waiters: the recorded-call predicate changed.
            self._cond.notify_all()
            while self._released <= index:
                if not self._cond.wait(20.0):
                    break

    def process_request(
        self, request: socket.socket, client_address: tuple[str, int]
    ) -> None:
        # Standard BaseServer boundary (finish plus shutdown of
        # the exact accepted connection), as the controller
        # drives it.
        self.finish_request(request, client_address)
        self.shutdown_request(request)

    def shutdown_request(self, request: socket.socket) -> None:
        with contextlib.suppress(Exception):
            request.close()

    def handle_error(self, request: object, client_address: object) -> None:
        return


class _PlainServer:
    """Immediately completing admission server boundary (test-only)."""

    def __init__(self) -> None:
        self.calls: list[tuple[socket.socket, tuple[str, int]]] = []

    def finish_request(
        self, request: socket.socket, client_address: tuple[str, int]
    ) -> None:
        self.calls.append((request, client_address))

    def process_request(
        self, request: socket.socket, client_address: tuple[str, int]
    ) -> None:
        # Standard BaseServer boundary (finish plus shutdown of
        # the exact accepted connection), as the controller
        # drives it.
        self.finish_request(request, client_address)
        self.shutdown_request(request)

    def shutdown_request(self, request: socket.socket) -> None:
        with contextlib.suppress(Exception):
            request.close()

    def handle_error(self, request: object, client_address: object) -> None:
        return


class _JoinState:
    """Observation state for one-shot join fault wrappers."""

    def __init__(self) -> None:
        self.used = False
        self.real_joins = 0
        self.joined: list[tuple[str, bool]] = []


def _one_shot_join_fault(
    target: threading.Thread, exc: BaseException, state: _JoinState
) -> Callable[..., None]:
    """Raise ``exc`` exactly once, BEFORE the native join, for the
    exact target thread; every later join attempt (any thread)
    delegates to the real join and is observed."""
    real_join = threading.Thread.join

    def fake_join(
        self: threading.Thread, timeout: float | None = None
    ) -> None:
        if self is target and not state.used:
            state.used = True
            raise exc
        state.real_joins += 1
        state.joined.append((self.name, self.is_alive()))
        real_join(self, timeout)

    return fake_join


def _start_fault(
    name: str,
    exc: BaseException,
    fired: list[bool] | None = None,
) -> Callable[[threading.Thread], None]:
    """Named-thread-qualified start fault: raise ``exc`` only for the
    exact thread name; every other start delegates to the real start
    (order 026-a, requirement 7 pattern).  When ``fired`` is given,
    each actual injection appends one True to it so the caller can
    assert the fault really executed."""
    real_start = threading.Thread.start

    def fail_start(thread: threading.Thread) -> None:
        if thread.name == name:
            if fired is not None:
                fired.append(True)
            raise exc
        real_start(thread)

    return fail_start


class AdmissionPolicyTests(unittest.TestCase):
    """Requirement 1: the pure exact validation of the two limits."""

    def test_invalid_waiting_capacity_rejected(self) -> None:
        class _IntSub(int):
            pass

        for bad in (0, -1, True, "16", 16.0, None, 1.5, _IntSub(16)):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                ra.validate_admission_policy(bad, 2.0)

    def test_invalid_queue_wait_rejected(self) -> None:
        class _FloatSub(float):
            pass

        class _IntSub(int):
            pass

        for bad in (
            0,
            -1,
            True,
            "2.0",
            None,
            float("nan"),
            float("inf"),
            1e300,
            10**400,
            threading.TIMEOUT_MAX * 2,
            _FloatSub(2.0),
            _IntSub(2),
        ):
            with self.subTest(value=repr(bad)), self.assertRaises(ValueError):
                # A huge int must be a plain ValueError, never an
                # OverflowError from a premature float conversion.
                ra.validate_admission_policy(16, bad)

    def test_valid_policies(self) -> None:
        for wait in (1, 2, 2.0, 0.5, threading.TIMEOUT_MAX, 10**6):
            with self.subTest(value=wait):
                policy = ra.validate_admission_policy(16, wait)
                self.assertEqual(policy, ra.AdmissionPolicy(16, float(wait)))

    def test_current_policy_reads_config(self) -> None:
        self.assertEqual(
            ra.current_admission_policy(), ra.AdmissionPolicy(16, 2.0)
        )
        with (
            mock.patch.object(config, "PROXY_MAX_QUEUED_REQUESTS", 7),
            mock.patch.object(config, "PROXY_QUEUE_WAIT_SECONDS", 1.5),
        ):
            self.assertEqual(
                ra.current_admission_policy(),
                ra.AdmissionPolicy(7, 1.5),
            )


class AdmissionConstructorTests(unittest.TestCase):
    """Requirement 1/5 constructor boundaries: before-bind rejection,
    the native bind failure path, and immutable per-instance policy."""

    def test_invalid_policy_rejected_before_bind(self) -> None:
        class BindObserving(proxy.ConceptProxy):
            bound = False

            def server_bind(self) -> None:
                type(self).bound = True
                super().server_bind()

        for bad in (0, True, "2.0", None, 10**400):
            with self.subTest(wait=repr(bad)):
                BindObserving.bound = False
                with (
                    mock.patch.object(config, "PROXY_MAX_QUEUED_REQUESTS", 16),
                    mock.patch.object(config, "PROXY_QUEUE_WAIT_SECONDS", bad),
                    self.assertRaises(ValueError),
                ):
                    BindObserving(
                        ("127.0.0.1", 0),
                        "http://127.0.0.1:1",
                        _DummyEngine(),
                    )
                self.assertFalse(BindObserving.bound)

    def test_occupied_port_preserves_original_bind_error(self) -> None:
        occupied = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        occupied.bind(("127.0.0.1", 0))
        occupied.listen(1)
        port = occupied.getsockname()[1]
        captured: dict[str, proxy.ConceptProxy] = {}

        class Capturing(proxy.ConceptProxy):
            def __init__(
                self,
                address: tuple[str, int],
                upstream: str,
                engine: proxy.RepairEngine,
            ) -> None:
                try:
                    super().__init__(address, upstream, engine)
                except BaseException:
                    captured["inst"] = self
                    raise

        try:
            with self.assertRaises(OSError) as ctx:
                Capturing(
                    ("127.0.0.1", port),
                    "http://127.0.0.1:1",
                    _DummyEngine(),
                )
        finally:
            # The pre-existing occupied socket stays intact and usable.
            probe = socket.create_connection(("127.0.0.1", port), timeout=3)
            conn, _ = occupied.accept()
            conn.close()
            probe.close()
            occupied.close()
        self.assertNotIsInstance(ctx.exception, AttributeError)
        self.assertIn(
            getattr(ctx.exception, "errno", None), (98, 10048)
        )
        inst = captured.get("inst")
        self.assertIsNotNone(inst)
        if inst is not None and hasattr(inst, "socket"):
            # The partially constructed owned listener socket is
            # closed by the native bind-failure close path.
            self.assertEqual(inst.socket.fileno(), -1)

    def test_running_instance_retains_policy_under_new_config(self) -> None:
        first = _AdmissionHarness()
        try:
            self.assertEqual(
                first.proxy_server._admission.policy,
                ra.AdmissionPolicy(16, 2.0),
            )
            # The second instance is constructed from the CURRENT
            # labelled test-only defaults 5/1.0 via the harness's
            # own before-construction patch, so it really does read
            # the intended CURRENT config (order 026-a,
            # requirement 1); the first running instance keeps its
            # immutable policy.
            second = _AdmissionHarness(max_queued=5, wait_seconds=1.0)
            try:
                self.assertEqual(
                    second.proxy_server._admission.policy,
                    ra.AdmissionPolicy(5, 1.0),
                )
                self.assertEqual(
                    first.proxy_server._admission.policy,
                    ra.AdmissionPolicy(16, 2.0),
                )
            finally:
                second.close()
        finally:
            first.close()
        # Global admission-thread absence holds only after BOTH
        # owned instances are closed.
        self.assertEqual(_admission_threads(), [])


class AdmissionControllerTests(unittest.TestCase):
    """Requirements 2/3 at the direct controller boundary."""

    def test_queue_full_exact_packet_no_thread_no_upstream(self) -> None:
        server = _GatedServer()
        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(2, 20.0)
        )
        controller.start()
        pairs = [socket.socketpair() for _ in range(4)]
        try:
            # Prove A holds the one active slot BEFORE the waiting
            # entries exist, so the capacity count cannot race
            # actual monitor ownership.
            controller.dispatch(pairs[0][0], ("127.0.0.1", 11001))
            self.assertTrue(server.wait_calls(1), "A not admitted")
            controller.dispatch(pairs[1][0], ("127.0.0.1", 11002))
            controller.dispatch(pairs[2][0], ("127.0.0.1", 11003))
            self.assertTrue(
                _wait(lambda: controller.pending_count() == 3),
                "waiting ownership not established",
            )
            # A, B, C owned (active + 2 waiting = exact capacity);
            # D must be rejected inline with the exact fixed full
            # packet.
            controller.dispatch(pairs[3][0], ("127.0.0.1", 11004))
            result = _drain(pairs[3][1], timeout=5.0)
            self.assertEqual(result.data, _expect_packet(ra.CODE_QUEUE_FULL))
            self.assertTrue(result.closed)
            self.assertEqual(controller.pending_count(), 3)
            self.assertEqual(len(_admission_threads()), 2)
            self.assertEqual(len(server.calls), 1)
            # Release the actual three in FIFO order: every admitted
            # entry completes exactly; D never reaches the handler.
            for _ in range(3):
                server.release()
            self.assertTrue(server.wait_calls(3), "later entries blocked")
            self.assertTrue(
                _wait(lambda: controller.pending_count() == 0),
                "ownership not released",
            )
            self.assertEqual(len(server.calls), 3)
        finally:
            for a, b in pairs:
                with contextlib.suppress(Exception):
                    a.close()
                with contextlib.suppress(Exception):
                    b.close()
            for _ in range(4):
                server.release()
            controller.stop()
        self.assertEqual(_admission_threads(), [])

    def test_fifo_order_behind_held_active(self) -> None:
        server = _GatedServer()
        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(4, 20.0)
        )
        controller.start()
        pairs = [socket.socketpair() for _ in range(4)]
        try:
            for index in range(4):
                controller.dispatch(
                    pairs[index][0], ("127.0.0.1", 12001 + index)
                )
            self.assertTrue(server.wait_calls(1), "first not admitted")
            # Every admitted entry needs its own gate release;
            # releasing fewer leaves the fourth held.
            for _ in range(4):
                server.release()
            self.assertTrue(server.wait_calls(4), "FIFO order broken")
            self.assertEqual(
                [addr for _sock, addr in server.calls],
                [("127.0.0.1", 12001 + index) for index in range(4)],
            )
            self.assertTrue(
                _wait(lambda: controller.pending_count() == 0),
                "ownership not released",
            )
        finally:
            for a, b in pairs:
                with contextlib.suppress(Exception):
                    a.close()
                with contextlib.suppress(Exception):
                    b.close()
            for _ in range(4):
                server.release()
            controller.stop()
        self.assertEqual(_admission_threads(), [])

    def test_expired_head_cannot_block_later_eligible(self) -> None:
        server = _GatedServer()
        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0)
        )
        controller.start()
        a = socket.socketpair()
        b = socket.socketpair()
        c = socket.socketpair()
        try:
            controller.dispatch(a[0], ("127.0.0.1", 13001))
            self.assertTrue(
                _wait(lambda: len(server.calls) == 1), "A not admitted"
            )
            start = time.monotonic()
            controller.dispatch(b[0], ("127.0.0.1", 13002))
            self.assertLess(time.monotonic() - start, 0.1)
            time.sleep(0.4)
            controller.dispatch(c[0], ("127.0.0.1", 13003))
            # B's deadline is t0+2.0 and C's is t0+2.4.  Observe B's
            # expiry as actual ownership removal (pending falls to
            # A active + C waiting) BEFORE releasing A, so the
            # release lands inside C's remaining 0.4 s window: C
            # survives while B's expiry cannot block it.
            self.assertTrue(
                _wait(
                    lambda: controller.pending_count() == 2,
                    timeout=6.0,
                ),
                "B expiry not processed",
            )
            server.release()
            self.assertTrue(
                server.wait_calls(2), "C blocked by expired B"
            )
            result_b = _drain(b[1], timeout=5.0)
            self.assertEqual(
                result_b.data, _expect_packet(ra.CODE_QUEUE_TIMEOUT)
            )
            self.assertTrue(result_b.closed)
            self.assertEqual(
                [addr for _sock, addr in server.calls],
                [("127.0.0.1", 13001), ("127.0.0.1", 13003)],
            )
            server.release()
            self.assertTrue(
                _wait(lambda: controller.pending_count() == 0),
                "pending not released",
            )
        finally:
            for sock_pair in (a, b, c):
                with contextlib.suppress(Exception):
                    sock_pair[0].close()
                with contextlib.suppress(Exception):
                    sock_pair[1].close()
            for _ in range(3):
                server.release()
            controller.stop()
        self.assertEqual(_admission_threads(), [])

    def test_sequential_requests_release_pending(self) -> None:
        server = _PlainServer()
        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0)
        )
        controller.start()
        try:
            for index in range(5):
                a, b = socket.socketpair()
                try:
                    controller.dispatch(a, ("127.0.0.1", 14001 + index))
                    self.assertTrue(
                        _wait(lambda: controller.pending_count() == 0),
                        f"entry {index} pending",
                    )
                finally:
                    with contextlib.suppress(Exception):
                        a.close()
                    with contextlib.suppress(Exception):
                        b.close()
            self.assertEqual(len(server.calls), 5)
        finally:
            # Normal cleanup: an unexpected control here is a real
            # failure and must surface, not be laundered.
            controller.stop()
        self.assertEqual(_admission_threads(), [])


class AdmissionExpiryTests(unittest.TestCase):
    """Requirement 3 / T3: accepted-waiting expiry while active work
    remains held - exact fixed packet for the readable client,
    bounded closure for a nonreading client that must not stall the
    listener, and the actual claim after elapsed expiry denied even
    when the timer notification was delayed."""

    def test_readable_client_expiry_exact_packet_while_active_held(
        self,
    ) -> None:
        harness = _AdmissionHarness(max_queued=2, wait_seconds=0.6)
        a: socket.socket | None = None
        b: socket.socket | None = None
        try:
            _DelayedMain.delay = 1.2
            a = harness.fire(
                _contract_body(False, input_text="held-A-expiry-" + "x" * 40)
            )
            time.sleep(0.1)
            b = harness.fire(
                _contract_body(False, input_text="queued-B-expiry-" + "x" * 40)
            )
            # B's deadline (t0+0.7) passes while A's held work
            # (t0+1.25) still runs: exact fixed timeout packet.
            result_b = _drain(b, timeout=6.0)
            self.assertEqual(
                result_b.data, _expect_packet(ra.CODE_QUEUE_TIMEOUT)
            )
            self.assertTrue(result_b.closed)
            # A completes normally: its socket was never touched by
            # the expiry path.
            result_a = _drain(a, timeout=10.0)
            self.assertTrue(result_a.closed)
            head_a, _sep, body_a = result_a.data.partition(b"\r\n\r\n")
            self.assertTrue(head_a.startswith(b"HTTP/1.0 200 OK"), head_a[:80])
            self.assertEqual(body_a, _json_completed(CLEAN))
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertIn(
                b"held-A-expiry-",
                cast(bytes, _MainUpstream.recorded[0]["body"]),
            )
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            for sock in (a, b):
                if sock is not None:
                    with contextlib.suppress(Exception):
                        sock.close()
            _DelayedMain.delay = 0.0
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_nonreader_expiry_closes_bounded_and_listener_unstalled(
        self,
    ) -> None:
        harness = _AdmissionHarness(max_queued=2, wait_seconds=0.8)
        a: socket.socket | None = None
        b: socket.socket | None = None
        try:
            _DelayedMain.delay = 1.2
            a = harness.fire(
                _contract_body(
                    False, input_text="held-A-nonreader-" + "x" * 40
                )
            )
            time.sleep(0.1)
            # B sends a bounded request body and NEVER reads its
            # socket: the bounded best-effort rejection (1 s send
            # bound) plus close must still terminate it, RST
            # tolerated (the proxy never reads a rejected entry's
            # request bytes).
            b = _raw_fire(harness.proxy_port, b"x" * (64 * 1024))
            admission = harness.proxy_server._admission
            self.assertTrue(
                _wait(
                    lambda: admission.pending_count() <= 1, timeout=6.0
                ),
                "nonreader B not rejected boundedly",
            )
            result_b = _drain(b, timeout=5.0)
            self.assertTrue(result_b.closed)
            if result_b.data:
                self.assertEqual(
                    result_b.data, _expect_packet(ra.CODE_QUEUE_TIMEOUT)
                )
            # A is still held; C's deadline (t0+1.65) survives A's
            # release (~t0+1.25), so C must be admitted and answered:
            # the listener stayed unstalled through the unread
            # rejection.
            status_c, body_c = harness.post(
                _contract_body(False, input_text="fresh-C-nonreader-" + "x" * 40)
            )
            self.assertEqual(status_c, 200, body_c[:200])
            self.assertEqual(body_c, _json_completed(CLEAN))
            result_a = _drain(a, timeout=10.0)
            self.assertTrue(result_a.closed)
            head_a, _sep, body_a = result_a.data.partition(b"\r\n\r\n")
            self.assertTrue(head_a.startswith(b"HTTP/1.0 200 OK"), head_a[:80])
            self.assertEqual(body_a, _json_completed(CLEAN))
            self.assertEqual(len(_MainUpstream.recorded), 2)
            self.assertIn(
                b"held-A-nonreader-",
                cast(bytes, _MainUpstream.recorded[0]["body"]),
            )
            self.assertIn(
                b"fresh-C-nonreader-",
                cast(bytes, _MainUpstream.recorded[1]["body"]),
            )
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            for sock in (a, b):
                if sock is not None:
                    with contextlib.suppress(Exception):
                        sock.close()
            _DelayedMain.delay = 0.0
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_late_claim_loses_to_elapsed_expiry(self) -> None:
        server = _GatedServer()
        cell = [100.0]
        gate = threading.Event()
        claim_seen = threading.Event()
        holder: dict[str, ra.RequestAdmissionController] = {}

        def clock() -> float:
            controller = holder.get("ctrl")
            if (
                controller is not None
                and controller._handoff is not None
                and controller._worker is threading.current_thread()
            ):
                # The worker's claim clock read - the actual claim
                # for handler execution: hold it until the observer
                # advances the clock past the deadline.
                claim_seen.set()
                gate.wait(5.0)
            return cell[0]

        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0), clock=clock
        )
        holder["ctrl"] = controller
        controller.start()
        e1: tuple[socket.socket, socket.socket] | None = None
        e2: tuple[socket.socket, socket.socket] | None = None
        try:
            e1 = socket.socketpair()
            controller.dispatch(e1[0], ("127.0.0.1", 17001))
            self.assertTrue(
                _wait(
                    lambda: controller._handoff is not None, timeout=5.0
                ),
                "E1 not handed off",
            )
            self.assertTrue(claim_seen.wait(5.0), "claim clock not reached")
            cell[0] = 200.0
            gate.set()
            self.assertTrue(
                _wait(
                    lambda: controller.pending_count() == 0, timeout=5.0
                ),
                "expired E1 not released",
            )
            result_e1 = _drain(e1[1], timeout=5.0)
            self.assertEqual(
                result_e1.data, _expect_packet(ra.CODE_QUEUE_TIMEOUT)
            )
            self.assertTrue(result_e1.closed)
            self.assertEqual(server.calls, [])
            # A fresh unexpired entry is still admitted on the same
            # controller: no leaked slot, no delayed timer.
            e2 = socket.socketpair()
            controller.dispatch(e2[0], ("127.0.0.1", 17002))
            self.assertTrue(server.wait_calls(1), "E2 not admitted")
            server.release()
            self.assertTrue(
                _wait(lambda: controller.pending_count() == 0),
                "E2 not released",
            )
        finally:
            for pair in (e1, e2):
                if pair is not None:
                    with contextlib.suppress(Exception):
                        pair[0].close()
                    with contextlib.suppress(Exception):
                        pair[1].close()
            server.release()
            controller.stop()
        self.assertEqual(_admission_threads(), [])


class AdmissionLifecycleTests(unittest.TestCase):
    """Requirement 5 / T4: native partial worker/guard startup fault
    matrix with exact ownership and caller control - one-shot faults
    only (a persistent synthetic fault would be an invalid repeat
    against a settlement loop), never-started/already-ended states,
    shutdown/close with waiting and active work, and actual joins
    before the owning close returns."""

    def test_monitor_start_ki_oneshot_join_fault_preserves_control(
        self,
    ) -> None:
        ki = KeyboardInterrupt("monitor-start-KI")
        mem = MemoryError("one-shot-join-MemoryError")
        server = _GatedServer()
        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0)
        )
        monitor: dict[str, threading.Thread] = {}
        state = _JoinState()
        real_start = threading.Thread.start
        real_join = threading.Thread.join

        def fake_start(self: threading.Thread) -> None:
            if self.name == _MONITOR:
                monitor["t"] = self
                real_start(self)
                raise ki
            real_start(self)

        def fake_join(
            self: threading.Thread, timeout: float | None = None
        ) -> None:
            if self is monitor.get("t") and not state.used:
                state.used = True
                raise mem  # one-shot, BEFORE the native join
            state.real_joins += 1
            state.joined.append((self.name, self.is_alive()))
            real_join(self, timeout)

        try:
            with (
                mock.patch.object(threading.Thread, "start", fake_start),
                mock.patch.object(threading.Thread, "join", fake_join),
                self.assertRaises(KeyboardInterrupt) as ctx,
            ):
                controller.start()
            self.assertIs(ctx.exception, ki)
            self.assertIs(ctx.exception.__cause__, mem)
            mt = monitor.get("t")
            self.assertIsNotNone(mt)
            self.assertIs(controller._monitor, mt)
            if mt is not None:
                self.assertFalse(mt.is_alive())
            worker = controller._worker
            self.assertIsNotNone(worker)
            if worker is not None:
                self.assertIsNone(
                    worker.ident, "never-started thread joined"
                )
            self.assertTrue(controller._closed)
            # The one-shot join fault is not a join: exactly one
            # actual native join of the exact monitor completed
            # before the first control propagated; the never-started
            # worker was never joined.
            self.assertEqual(state.real_joins, 1)
            self.assertEqual(state.joined[0][0], _MONITOR)
            self.assertEqual(controller.pending_count(), 0)
            self.assertEqual(_admission_threads(), [])
        finally:
            # Failure-path cleanup: if the fault did not fire, an
            # idempotent owning close stops the live lifecycle so
            # non-daemon workers are never left behind.
            controller.stop()

    def test_worker_start_ki_after_real_start_settles_both(self) -> None:
        ki = KeyboardInterrupt("worker-start-KI")
        server = _GatedServer()
        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0)
        )
        state = _JoinState()
        real_start = threading.Thread.start
        real_join = threading.Thread.join

        def fake_start(self: threading.Thread) -> None:
            real_start(self)
            if self.name == _WORKER:
                raise ki

        def fake_join(
            self: threading.Thread, timeout: float | None = None
        ) -> None:
            state.real_joins += 1
            state.joined.append((self.name, self.is_alive()))
            real_join(self, timeout)

        try:
            with (
                mock.patch.object(threading.Thread, "start", fake_start),
                mock.patch.object(threading.Thread, "join", fake_join),
                self.assertRaises(KeyboardInterrupt) as ctx,
            ):
                controller.start()
            self.assertIs(ctx.exception, ki)
            self.assertIsNone(ctx.exception.__cause__)
            monitor = controller._monitor
            worker = controller._worker
            self.assertIsNotNone(monitor)
            self.assertIsNotNone(worker)
            if monitor is not None:
                self.assertFalse(monitor.is_alive())
            if worker is not None:
                self.assertFalse(worker.is_alive())
            self.assertTrue(controller._closed)
            # Both actually-started threads were actually joined
            # exactly once each, in ownership order.
            self.assertEqual(
                [name for name, _alive in state.joined],
                [_MONITOR, _WORKER],
            )
            self.assertEqual(state.real_joins, 2)
            self.assertEqual(controller.pending_count(), 0)
            self.assertEqual(_admission_threads(), [])
        finally:
            # Failure-path cleanup: an idempotent owning close stops
            # a live lifecycle if the fault did not fire.
            controller.stop()

    def test_readiness_commit_control_settles_started_workers(self) -> None:
        # One-shot control at the dispatch-readiness notification
        # itself, AFTER both native starts: the exact started workers
        # must be stopped and actually joined before the first
        # control propagates (order 026-a, requirement 5).  The
        # first notify on this exact condition is the readiness
        # commit - nothing else notifies it before dispatch is
        # committed.
        server = _GatedServer()
        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0)
        )
        ki = KeyboardInterrupt("readiness-commit-KI")
        used = False
        real_notify = controller._woken.notify_all

        def commit_notify() -> None:
            nonlocal used
            if not used:
                used = True
                raise ki
            real_notify()

        try:
            with mock.patch.object(
                controller._woken, "notify_all", commit_notify
            ), self.assertRaises(KeyboardInterrupt) as ctx:
                controller.start()
            self.assertIs(ctx.exception, ki)
            self.assertIsNone(ctx.exception.__cause__)
            monitor = controller._monitor
            worker = controller._worker
            self.assertIsNotNone(monitor)
            self.assertIsNotNone(worker)
            if monitor is not None:
                self.assertFalse(monitor.is_alive())
            if worker is not None:
                self.assertFalse(worker.is_alive())
            self.assertTrue(controller._closed)
            self.assertEqual(controller.pending_count(), 0)
            self.assertEqual(_admission_threads(), [])
        finally:
            # Failure-path cleanup: an idempotent owning close stops
            # a live lifecycle if the fault did not fire.
            controller.stop()
        self.assertTrue(controller._closed)
        self.assertEqual(controller.pending_count(), 0)
        self.assertEqual(_admission_threads(), [])

    def test_worker_claim_clock_ki_preserved_at_owning_stop(self) -> None:
        ki = KeyboardInterrupt("worker-claim-KI")
        server = _GatedServer()
        holder: dict[str, ra.RequestAdmissionController] = {}
        state = {"calls": 0}

        def clock() -> float:
            controller = holder.get("ctrl")
            if (
                controller is not None
                and controller._handoff is not None
                and controller._worker is threading.current_thread()
            ):
                state["calls"] += 1
                if state["calls"] == 1:
                    raise ki
            return time.monotonic()

        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0), clock=clock
        )
        holder["ctrl"] = controller
        controller.start()
        a, b = socket.socketpair()
        try:
            controller.dispatch(a, ("127.0.0.1", 15001))
            self.assertTrue(
                _wait(lambda: controller._worker_control is not None),
                "worker control not preserved",
            )
            # The exact first control is re-raised at the documented
            # owning close, after the exact owned cleanup.
            with self.assertRaises(KeyboardInterrupt) as ctx:
                controller.stop()
            self.assertIs(ctx.exception, ki)
            # The reserved handoff entry never entered the handler:
            # closed with the fixed closed packet, handler untouched.
            result = _drain(b, timeout=5.0)
            self.assertEqual(
                result.data, _expect_packet(ra.CODE_QUEUE_CLOSED)
            )
            self.assertTrue(result.closed)
            self.assertEqual(controller.pending_count(), 0)
            self.assertEqual(server.calls, [])
            self.assertIsNone(
                controller._worker_control, "control not consumed"
            )
        finally:
            with contextlib.suppress(Exception):
                a.close()
            with contextlib.suppress(Exception):
                b.close()
            server.release()
            # Idempotent owning close: the workers are joined and the
            # control consumed, so this cleanup close is clean - an
            # unexpected control here is a real failure.
            controller.stop()
        self.assertEqual(_admission_threads(), [])

    def test_monitor_claim_clock_ki_preserved_at_owning_stop(self) -> None:
        ki = KeyboardInterrupt("monitor-claim-KI")
        server = _GatedServer()
        holder: dict[str, ra.RequestAdmissionController] = {}
        state = {"calls": 0}

        def clock() -> float:
            controller = holder.get("ctrl")
            if (
                controller is not None
                and controller._waiting
                and controller._handoff is None
                and controller._active is None
            ):
                state["calls"] += 1
                if state["calls"] == 2:
                    raise ki
            return time.monotonic()

        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0), clock=clock
        )
        holder["ctrl"] = controller
        controller.start()
        a, b = socket.socketpair()
        try:
            # The first registered call is the monitor prune check;
            # the second is the actual FIFO claim re-check, where the
            # entry is still registered in the queue, so the control
            # can never orphan the connection.
            controller.dispatch(a, ("127.0.0.1", 16001))
            self.assertTrue(
                _wait(lambda: controller._worker_control is not None),
                "worker control not preserved",
            )
            with self.assertRaises(KeyboardInterrupt) as ctx:
                controller.stop()
            self.assertIs(ctx.exception, ki)
            result = _drain(b, timeout=5.0)
            self.assertEqual(
                result.data, _expect_packet(ra.CODE_QUEUE_CLOSED)
            )
            self.assertTrue(result.closed)
            self.assertEqual(controller.pending_count(), 0)
            self.assertEqual(server.calls, [])
            self.assertIsNone(
                controller._worker_control, "control not consumed"
            )
        finally:
            with contextlib.suppress(Exception):
                a.close()
            with contextlib.suppress(Exception):
                b.close()
            server.release()
            controller.stop()
        self.assertEqual(_admission_threads(), [])

    def test_dispatch_anchor_clock_control_closes_accepted_socket(
        self,
    ) -> None:
        ki = KeyboardInterrupt("anchor-KI")
        server = _GatedServer()
        state = {"called": False}

        def clock() -> float:
            if not state["called"]:
                state["called"] = True
                raise ki
            return time.monotonic()

        controller = ra.RequestAdmissionController(
            server, ra.validate_admission_policy(16, 2.0), clock=clock
        )
        controller.start()
        a, b = socket.socketpair()
        try:
            # The first clock call overall is the dispatch deadline
            # anchor: the accepted socket must be closed by the
            # dispatch failure path and the exact control propagated.
            with self.assertRaises(KeyboardInterrupt) as ctx:
                controller.dispatch(a, ("127.0.0.1", 17001))
            self.assertIs(ctx.exception, ki)
            result = _drain(b, timeout=5.0)
            self.assertEqual(result.data, b"")
            self.assertTrue(result.closed)
            self.assertEqual(controller.pending_count(), 0)
            self.assertEqual(server.calls, [])
            # Clean owning close: no leaked slot, no delayed timer.
            controller.stop()
        finally:
            with contextlib.suppress(Exception):
                a.close()
            with contextlib.suppress(Exception):
                b.close()
            # Idempotent on the success path; stops a live lifecycle
            # if a mid-test assertion failed.
            controller.stop()
        self.assertEqual(_admission_threads(), [])

    def test_shutdown_with_active_and_waiting_work(self) -> None:
        harness = _AdmissionHarness(max_queued=4, wait_seconds=3.0)
        a: socket.socket | None = None
        b: socket.socket | None = None
        try:
            _DelayedMain.delay = 1.0
            a = harness.fire(
                _contract_body(False, input_text="held-A-shutdown-" + "x" * 40)
            )
            time.sleep(0.1)
            b = harness.fire(
                _contract_body(
                    False, input_text="queued-B-shutdown-" + "x" * 40
                )
            )
            admission = harness.proxy_server._admission
            self.assertTrue(
                _wait(lambda: admission._active is not None), "A not active"
            )
            # B must be an actually registered entry before the
            # owning shutdown: a connection still sitting in the OS
            # pre-accept backlog is outside admission ownership
            # (the native accept loop may stop on the shutdown
            # request without draining it), so the closed-packet
            # expectation applies only to a real waiting entry.
            self.assertTrue(
                _wait(lambda: admission.pending_count() == 2),
                "B not registered before shutdown",
            )
            # Normal owning shutdown: the waiting entry is canceled
            # with the fixed closed packet; the in-flight active
            # work takes its existing bounded time and completes.
            harness.proxy_server.shutdown()
            result_b = _drain(b, timeout=5.0)
            self.assertEqual(
                result_b.data, _expect_packet(ra.CODE_QUEUE_CLOSED)
            )
            self.assertTrue(result_b.closed)
            result_a = _drain(a, timeout=10.0)
            self.assertTrue(result_a.closed)
            head_a, _sep, body_a = result_a.data.partition(b"\r\n\r\n")
            self.assertTrue(head_a.startswith(b"HTTP/1.0 200 OK"), head_a[:80])
            self.assertEqual(body_a, _json_completed(CLEAN))
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertIn(
                b"held-A-shutdown-",
                cast(bytes, _MainUpstream.recorded[0]["body"]),
            )
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(admission.pending_count(), 0)
        finally:
            for sock in (a, b):
                if sock is not None:
                    with contextlib.suppress(Exception):
                        sock.close()
            _DelayedMain.delay = 0.0
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_intake_guard_start_ki_preserved_at_shutdown(self) -> None:
        # The actual named intake-guard Thread.start failure fires
        # AFTER admission (the entry is admitted and dispatched),
        # so the nonordinary control is preserved at the worker
        # owner boundary and re-raised at the owning shutdown - no
        # accidental successful answer, zero downstream.
        harness = _AdmissionHarness()
        ki = KeyboardInterrupt("intake-guard-KI")
        sock: socket.socket | None = None
        try:
            admission = harness.proxy_server._admission
            with mock.patch.object(
                threading.Thread,
                "start",
                _start_fault("concept-client-intake-guard", ki),
            ):
                sock = harness.fire(
                    _contract_body(False, input_text="guard-KI-" + "x" * 40)
                )
                self.assertTrue(
                    _wait(lambda: admission._worker_control is not None),
                    "worker control not preserved",
                )
            with self.assertRaises(KeyboardInterrupt) as ctx:
                harness.proxy_server.shutdown()
            self.assertIs(ctx.exception, ki)
            # Closed before any status line; the fault precedes
            # forwarding, so zero main/review.
            result = _drain(sock, timeout=5.0)
            self.assertEqual(result.data, b"")
            self.assertTrue(result.closed)
            self.assertEqual(len(_MainUpstream.recorded), 0)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            # The shutdown control path finalized the listener.
            self.assertEqual(harness.proxy_server.socket.fileno(), -1)
        finally:
            if sock is not None:
                with contextlib.suppress(Exception):
                    sock.close()
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_dead_accept_loop_server_close_clean(self) -> None:
        # A dispatch control that kills the accepting loop is an
        # actual loop failure, not an admission lifecycle failure:
        # the accepted socket is closed at the dispatch anchor, and
        # the documented owning close still settles the live
        # admission workers cleanly.
        p = proxy.ConceptProxy(
            ("127.0.0.1", 0), "http://127.0.0.1:1", _DummyEngine()
        )
        serve = threading.Thread(target=p.serve_forever, daemon=True)
        serve.start()
        ki = KeyboardInterrupt("accept-loop-KI")
        state = {"called": False}

        def clock() -> float:
            if not state["called"]:
                state["called"] = True
                raise ki
            return time.monotonic()

        seen: list[BaseException] = []

        def hook(args: threading.ExceptHookArgs) -> None:
            if args.exc_value is not None:
                seen.append(args.exc_value)

        p._admission._clock = clock
        client: socket.socket | None = None
        with mock.patch.object(threading, "excepthook", hook):
            try:
                client = _raw_fire(
                    p.server_port,
                    _contract_body(False, input_text="dead-loop-" + "x" * 40),
                )
                self.assertTrue(
                    _wait(lambda: not serve.is_alive(), timeout=10.0),
                    "accept loop did not die on the dispatch control",
                )
                serve.join(5)
                self.assertFalse(serve.is_alive())
                # The exact control is what killed the accept loop.
                self.assertEqual(len(seen), 1)
                self.assertIs(seen[0], ki)
                result = _drain(client, timeout=5.0)
                self.assertEqual(result.data, b"")
                self.assertTrue(result.closed)
                self.assertEqual(p._admission.pending_count(), 0)
                # Owning close on the dead loop: clean settlement of
                # the still-live admission workers, listener closed.
                p.server_close()
                self.assertEqual(p.socket.fileno(), -1)
            finally:
                if client is not None:
                    with contextlib.suppress(Exception):
                        client.close()
                p.server_close()
        self.assertEqual(_admission_threads(), [])

    def test_server_close_with_worker_control(self) -> None:
        # The documented owning close: the preserved worker control
        # is re-raised at server_close AFTER the exact worker
        # settlement and the listener close.
        p = proxy.ConceptProxy(
            ("127.0.0.1", 0), "http://127.0.0.1:1", _DummyEngine()
        )
        serve = threading.Thread(target=p.serve_forever, daemon=True)
        serve.start()
        ki = KeyboardInterrupt("serverclose-KI")
        state = {"calls": 0}
        real_clock = time.monotonic

        def clock() -> float:
            c = p._admission
            if (
                c._waiting
                and c._handoff is None
                and c._active is None
            ):
                state["calls"] += 1
                if state["calls"] == 2:
                    raise ki
            return real_clock()

        p._admission._clock = clock
        client: socket.socket | None = None
        try:
            # First registered call: monitor prune check. Second:
            # the actual FIFO claim re-check, with the entry still
            # registered in the queue.
            client = _raw_fire(
                p.server_port,
                _contract_body(False, input_text="sc-KI-" + "x" * 40),
            )
            self.assertTrue(
                _wait(lambda: p._admission._worker_control is not None),
                "worker control not preserved",
            )
            with self.assertRaises(KeyboardInterrupt) as ctx:
                p.server_close()
            self.assertIs(ctx.exception, ki)
            result = _drain(client, timeout=5.0)
            self.assertEqual(
                result.data, _expect_packet(ra.CODE_QUEUE_CLOSED)
            )
            self.assertTrue(result.closed)
            self.assertEqual(p.socket.fileno(), -1)
            monitor = p._admission._monitor
            worker = p._admission._worker
            self.assertIsNotNone(monitor)
            self.assertIsNotNone(worker)
            if monitor is not None:
                self.assertFalse(monitor.is_alive())
            if worker is not None:
                self.assertFalse(worker.is_alive())
            self.assertEqual(p._admission.pending_count(), 0)
            # The accept loop is still running: the preserved
            # control was consumed at the owning close, so the
            # documented owning shutdown close is now clean.
            p.shutdown()
        finally:
            if client is not None:
                with contextlib.suppress(Exception):
                    client.close()
            serve.join(5)
            self.assertFalse(serve.is_alive())
        self.assertEqual(_admission_threads(), [])


class AdmissionProxyTests(unittest.TestCase):
    """Requirement 5 / T5 at the actual proxy: one active whole
    handler with the concurrent fake-upstream positive control, zero
    main/review for rejected entries, healthy recovery, and exact
    raw body/status/content-type plus request-local usage fidelity
    across two admitted requests."""

    def test_held_active_queued_full_exact_codes_zero_downstream(
        self,
    ) -> None:
        harness = _AdmissionHarness(max_queued=2, wait_seconds=0.8)
        sockets: list[socket.socket] = []
        try:
            _DelayedMain.delay = 1.2
            a = harness.fire(
                _contract_body(False, input_text="held-A-proxy-" + "x" * 40)
            )
            sockets.append(a)
            time.sleep(0.1)
            b = harness.fire(
                _contract_body(False, input_text="queued-B-proxy-" + "x" * 40)
            )
            sockets.append(b)
            time.sleep(0.1)
            c = harness.fire(
                _contract_body(False, input_text="queued-C-proxy-" + "x" * 40)
            )
            sockets.append(c)
            time.sleep(0.1)
            d = harness.fire(
                _contract_body(False, input_text="extra-D-proxy-" + "x" * 40)
            )
            sockets.append(d)
            # A active + B, C waiting = exact capacity: D is
            # rejected inline, immediately, with the fixed full
            # packet.
            result_d = _drain(d, timeout=5.0)
            self.assertEqual(
                result_d.data, _expect_packet(ra.CODE_QUEUE_FULL)
            )
            self.assertTrue(result_d.closed)
            # B (deadline ~t0+0.9) and C (~t0+1.0) both expire
            # before A releases (~t0+1.25): exact timeout packets,
            # zero downstream for both.
            result_b = _drain(b, timeout=8.0)
            self.assertEqual(
                result_b.data, _expect_packet(ra.CODE_QUEUE_TIMEOUT)
            )
            self.assertTrue(result_b.closed)
            result_c = _drain(c, timeout=8.0)
            self.assertEqual(
                result_c.data, _expect_packet(ra.CODE_QUEUE_TIMEOUT)
            )
            self.assertTrue(result_c.closed)
            result_a = _drain(a, timeout=10.0)
            self.assertTrue(result_a.closed)
            head_a, _sep, body_a = result_a.data.partition(b"\r\n\r\n")
            self.assertTrue(head_a.startswith(b"HTTP/1.0 200 OK"), head_a[:80])
            self.assertEqual(body_a, _json_completed(CLEAN))
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertIn(
                b"held-A-proxy-",
                cast(bytes, _MainUpstream.recorded[0]["body"]),
            )
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            # A healthy fresh request recovers on the same instance.
            status_e, body_e = harness.post(
                _contract_body(False, input_text="fresh-E-proxy-" + "x" * 40)
            )
            self.assertEqual(status_e, 200, body_e[:200])
            self.assertEqual(body_e, _json_completed(CLEAN))
        finally:
            for sock in sockets:
                with contextlib.suppress(Exception):
                    sock.close()
            _DelayedMain.delay = 0.0
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_concurrent_fake_upstream_positive_control(self) -> None:
        harness = _AdmissionHarness(max_queued=2, wait_seconds=0.8)
        a: socket.socket | None = None
        try:
            _DelayedMain.delay = 1.2
            a = harness.fire(
                _contract_body(False, input_text="held-A-control-" + "x" * 40)
            )
            time.sleep(0.2)
            admission = harness.proxy_server._admission
            self.assertTrue(
                _wait(lambda: admission._active is not None), "A not active"
            )
            # A direct probe to the fake main upstream - bypassing
            # the proxy queue entirely - must answer promptly while
            # A is held: the upstream is not the bottleneck, the
            # proxy queue is the behavior under test.
            probe_start = time.monotonic()
            client = http.client.HTTPConnection(
                "127.0.0.1", harness.main_server.server_port, timeout=5
            )
            try:
                probe_body = _contract_body(
                    False, input_text="direct-probe-" + "x" * 40
                )
                client.request(
                    "POST",
                    "/v1/responses",
                    body=probe_body,
                    headers={"Content-Length": str(len(probe_body))},
                )
                probe = client.getresponse()
                probe.read()
                probe_status = probe.status
            finally:
                client.close()
            probe_elapsed = time.monotonic() - probe_start
            self.assertEqual(probe_status, 200)
            self.assertLess(probe_elapsed, 0.5)
            self.assertTrue(
                admission._active is not None, "A released too early"
            )
            result_a = _drain(a, timeout=10.0)
            self.assertTrue(result_a.closed)
            head_a, _sep, body_a = result_a.data.partition(b"\r\n\r\n")
            self.assertTrue(head_a.startswith(b"HTTP/1.0 200 OK"), head_a[:80])
            self.assertEqual(body_a, _json_completed(CLEAN))
        finally:
            if a is not None:
                with contextlib.suppress(Exception):
                    a.close()
            _DelayedMain.delay = 0.0
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_two_admitted_requests_usage_and_body_fidelity(self) -> None:
        observer: list[dict[str, object]] = []
        harness = _AdmissionHarness(usage_observer=observer.append)
        try:
            # Request 1: useful repair - main returns the suspect
            # completed JSON and the real engine (qualified Pandoc,
            # real validating reviewer) repairs it.
            _MainUpstream.source = _json_completed(USEFUL_018)
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t1")],
                usage={
                    "input_tokens": 4,
                    "output_tokens": 6,
                    "total_tokens": 10,
                },
            )
            status_1, payload_1 = harness.post(_contract_body(False))
            self.assertEqual(status_1, 200, payload_1[:200])
            text_1 = (
                json.loads(payload_1.decode())
                ["output"][0]["content"][0]["text"]
            )
            self.assertEqual(text_1, EXPECTED_USEFUL_018)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            # Request 2: no suspicion - the exact raw main body and
            # status are preserved with zero review and unknown
            # usage: no stale details/usage carried over.
            _MainUpstream.source = _json_completed(CLEAN)
            client = http.client.HTTPConnection(
                "127.0.0.1", harness.proxy_port, timeout=20
            )
            try:
                body_2 = _contract_body(False, input_text=CLEAN)
                client.request(
                    "POST",
                    "/v1/responses",
                    body=body_2,
                    headers={"Content-Length": str(len(body_2))},
                )
                response_2 = client.getresponse()
                payload_2 = response_2.read()
                status_2 = response_2.status
                content_type_2 = response_2.getheader("Content-Type")
            finally:
                client.close()
            self.assertEqual(status_2, 200)
            self.assertEqual(payload_2, _json_completed(CLEAN))
            self.assertEqual(content_type_2, "application/json")
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(
                observer,
                [
                    {
                        "review_calls": 1,
                        "reviewer_usage": {
                            "input_tokens": 4,
                            "output_tokens": 6,
                            "total_tokens": 10,
                        },
                    },
                    {"review_calls": 0, "reviewer_usage": "unknown"},
                ],
            )
        finally:
            harness.close()
        self.assertEqual(_admission_threads(), [])


class AdmissionContractTests(unittest.TestCase):
    """Requirement 6 / T6: existing contract semantics preserved
    under admission - supported framing 400, non-200 upstream
    passthrough, mode mismatch 502 (never an admission 503), exact
    raw delayed-SSE passthrough, and the actual named intake-guard
    Thread.start failure after admission."""

    def test_duplicate_content_length_is_400_not_admission_503(self) -> None:
        harness = _AdmissionHarness()
        sock: socket.socket | None = None
        try:
            body = _contract_body(False, input_text="dup-cl-" + "x" * 40)
            data = (
                _head(len(body), extra=(("Content-Length", str(len(body))),))
                + body
            )
            sock = _raw_fire(harness.proxy_port, data)
            result = _drain(sock, timeout=5.0)
            self.assertTrue(result.data.startswith(b"HTTP/1.0 400 "))
            self.assertNotIn(b"request_admission_error", result.data)
            self.assertTrue(result.closed)
            self.assertEqual(len(_MainUpstream.recorded), 0)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            if sock is not None:
                with contextlib.suppress(Exception):
                    sock.close()
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_non200_upstream_preserved_under_admission(self) -> None:
        harness = _AdmissionHarness()
        original_body = (
            b'{"error":{"message":"synthetic upstream failure"}}'
        )
        try:
            _MainUpstream.status = 500
            _MainUpstream.source = original_body
            status, payload = harness.post(
                _contract_body(False, input_text="non200-" + "x" * 40)
            )
            self.assertEqual(status, 500)
            self.assertEqual(payload, original_body)
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            # Recovery on the same instance: back to a healthy 200.
            _MainUpstream.status = 200
            _MainUpstream.source = _json_completed(CLEAN)
            status_2, payload_2 = harness.post(_contract_body(False))
            self.assertEqual(status_2, 200)
            self.assertEqual(payload_2, _json_completed(CLEAN))
        finally:
            _MainUpstream.status = 200
            _MainUpstream.source = _json_completed(CLEAN)
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_mode_mismatch_is_502_not_admission_503(self) -> None:
        cases: list[tuple[str, bool, str, bytes]] = [
            (
                "json_main_stream_request",
                True,
                "application/json",
                b'{"object":"response"}',
            ),
            (
                "sse_main_nonstream_request",
                False,
                "text/event-stream",
                _sse_delta("m", "To je tako zapisano.") + _sse_completed(),
            ),
        ]
        for name, stream, content_type, source in cases:
            with self.subTest(case=name):
                harness = _AdmissionHarness()
                try:
                    _MainUpstream.content_type = content_type
                    _MainUpstream.source = source
                    _FakeUpstream.payload = _review_payload([_prop("t0")])
                    status, payload = harness.post(_contract_body(stream))
                    self.assertEqual(status, 502)
                    self.assertNotIn(b"request_admission_error", payload)
                    self.assertEqual(
                        json.loads(payload),
                        {
                            "error": {
                                "type": "upstream_protocol_error",
                                "code": "RESPONSE_MODE_MISMATCH",
                            }
                        },
                    )
                    self.assertEqual(len(_FakeUpstream.recorded), 0)
                finally:
                    _MainUpstream.content_type = "application/json"
                    harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_delayed_sse_exact_passthrough_under_admission(self) -> None:
        completed = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {
                            "type": "output_text",
                            "text": CLEAN,
                            "content_index": 0,
                        }
                    ],
                }
            ],
        }
        source = _sse_delta("m", CLEAN) + _sse_completed(completed)
        harness = _AdmissionHarness(main_handler=_SseUpstream)
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = source
            _SseUpstream.split_at = len(source) // 2
            _SseUpstream.gap = 0.3
            client = http.client.HTTPConnection(
                "127.0.0.1", harness.proxy_port, timeout=20
            )
            try:
                body = _contract_body(True, input_text=CLEAN)
                client.request(
                    "POST",
                    "/v1/responses",
                    body=body,
                    headers={"Content-Length": str(len(body))},
                )
                response = client.getresponse()
                payload = response.read()
                status = response.status
                content_type = response.getheader("Content-Type")
            finally:
                client.close()
            # No-suspicion SSE: the exact raw main bytes (including
            # the split write timing) and content type are preserved.
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(payload, source)
            self.assertEqual(content_type, "text/event-stream")
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            _MainUpstream.content_type = "application/json"
            _SseUpstream.split_at = 0
            _SseUpstream.gap = 0.3
            harness.close()
        self.assertEqual(_admission_threads(), [])

    def test_intake_guard_start_fault_closed_quiet_and_recovers(self) -> None:
        # The actual named intake-guard Thread.start failure (an
        # ordinary error) after admission: the connection closes
        # quietly with no status line, zero downstream, no privacy
        # leak, and the same instance recovers.  The exact-name
        # fault patch is held until the actual injection and the
        # closed peer are observed: pending_count()==0 is also
        # true before the just-sent TCP connection is accepted,
        # so an initially empty registry is not proof the request
        # ran and finished.
        harness = _AdmissionHarness()
        marker = "SYNTHETIC_026_GUARD_FAULT_NOT_A_CREDENTIAL"
        stdout = io.StringIO()
        stderr = io.StringIO()
        fired: list[bool] = []
        sock: socket.socket | None = None
        try:
            with (
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
                mock.patch.object(
                    threading.Thread,
                    "start",
                    _start_fault(
                        "concept-client-intake-guard",
                        RuntimeError(marker),
                        fired,
                    ),
                ),
            ):
                sock = harness.fire(
                    _contract_body(
                        False, input_text="guard-fault-" + "x" * 40
                    )
                )
                # The faulted (or regressed healthy) request ends
                # with this peer socket closed; the patch stays
                # installed for the whole drain and its assertions.
                result = _drain(sock, timeout=5.0)
                self.assertTrue(result.closed)
                self.assertEqual(result.data, b"")
                # The injection really fired, exactly once, for the
                # exact frozen guard name.
                self.assertEqual(fired, [True])
            self.assertEqual(len(_MainUpstream.recorded), 0)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            logs = stdout.getvalue() + stderr.getvalue()
            self.assertNotIn(marker, logs)
            admission = harness.proxy_server._admission
            self.assertTrue(
                _wait(lambda: admission.pending_count() == 0, timeout=5.0),
                "faulted entry not released",
            )
            # Same instance recovers to a healthy 200 (patch gone).
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(payload, _json_completed(CLEAN))
        finally:
            if sock is not None:
                with contextlib.suppress(Exception):
                    sock.close()
            harness.close()
        self.assertEqual(_admission_threads(), [])


if __name__ == "__main__":
    unittest.main()
