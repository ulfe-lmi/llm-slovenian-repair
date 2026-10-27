"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Owned
elapsed response-header budget.

Order 018-a acceptance coverage.

Direct guard boundaries over real stdlib HTTPConnection/getresponse
plumbing (real loopback sockets; no fake parser):

* one absolute monotonic deadline anchored before guard startup and
  before acquisition: guard-start overhead is not concealed (a
  0.12-s delayed status line still expires at a 0.03-s budget);
* slow status-line, slow header-line, interim-100 and racing-completion
  deliveries all expire at the budget; a legitimate 100-to-final
  response within the budget still succeeds;
* byte arrival never resets the deadline; a successful acquisition is
  never touched by a late timer (the body may arrive after the header
  budget passes);
* a guard never affects another owned connection;
* a racing or late parsed response is explicitly closed and never
  transferred; no guard thread outlives acquisition;
* genuine transport errors before the deadline propagate unchanged;
* bool/nonnumeric/nonfinite/nonpositive budgets are rejected.

Constructor and main() wiring (owned loopback port 0 only, never the
fixed service port): the keyword-only header_timeout default and
storage, rejection before bind, the legacy positional constructor shape
still works, and main() reads CONCEPT_HEADER_TIMEOUT with the ordered
default while CONCEPT_TIMEOUT keeps its existing meaning.

Actual proxy HTTP (real ConceptProxy -> real RepairEngine with the
qualified Pandoc and a real tiny SQLite index -> real ResponsesReviewer;
synthetic main/reviewer upstreams only):

* fast-header JSON/SSE positives with real wire UTF-8 and a useful
  two-target repair preserving protected slices;
* slow status-line and slow header-line negatives: 502 with zero
  engine.repair calls (call-through observation at the actual engine
  boundary) and zero reviewer calls;
* interim-100 deadline and positive control;
* header/body budget independence in both directions (a body arriving
  after the header budget but within the body budget succeeds; slow
  headers under a generous header budget with a short body budget
  succeed);
* expiration recovery on the same proxy and concurrent other-proxy
  isolation; no guard threads outlive acquisition;
* the default header budget is wired through the real constructor.

One real-TLS actual-HTTP matrix runs in a subprocess child against a
TLS main upstream using an owned ephemeral self-signed certificate
trusted only inside that child via SSL_CERT_FILE: fast TLS headers
succeed identically while slow TLS status/header drips fail at the
budget with zero review and zero engine calls.

A hanging main upstream (no status ever sent) runs in an ordinary
Python subprocess child with its own process group: the request fails
at the finite header budget with zero review and zero engine calls,
and the parent enforces a finite deadline, kills the process group and
reaps it.  No private fixture paths are referenced by the committed
tests.

Only the main and reviewer upstreams are synthetic; no live service,
model, GPU or network boundary is touched.
"""

from __future__ import annotations

import contextlib
import http.client
import http.server
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
    ThreadingHTTPServer,
)
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import header_transport  # noqa: E402
import proxy  # noqa: E402
from config import MAIN_HEADER_TIMEOUT_SECONDS  # noqa: E402
from qwen_client import ResponsesReviewer  # noqa: E402
from tests.test_capture_transport import (  # noqa: E402
    _BUILD_UNIGRAM,
    CLEAN,
    CLEAN_UNICODE,
    _assert_unicode_on_wire,
    _assert_wire_steps,
    _run_child_bounded,
    _sse_baseline_utf8,
    _WireMain,
    _with_content_length,
)
from tests.test_responses_contract import (  # noqa: E402
    _json_completed,
    _review_payload,
)
from tests.test_review_batch import (  # noqa: E402
    TEXT,
    _contract_body,
    _FakeUpstream,
    _prop,
    _real_spec,
)
from tests.test_runtime_corpus import _build_db  # noqa: E402

_SSE_HEADERS = b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\n\r\n"
_JSON_HEADERS = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
_INTERIM_100 = b"HTTP/1.1 100 Continue\r\n\r\n"

# Self-contained useful original for order 018-a, acceptance 2: two
# supported repairable occurrences on the first paragraph; protected
# code, TeX, HTML and link spans on the second (the marker word
# inside them has no supported local context); and the NFC-unstable
# decomposed/combining protected line kept on its own separate
# paragraph, where it is unprovable by design without touching the
# repairable first paragraph (017 discriminator).
USEFUL_018 = (
    "To je presenetliv zapisano, to je presenetliv zapisano.\n"
    "`presenetliv` \\(x^2\\) <b>presenetliv</b> [zapis](http://example.com/slo)\n"
    "e\u0301 \u20ac \U0001F600"
)
EXPECTED_USEFUL_018 = (
    "To je tako zapisano, to je tako zapisano.\n"
    "`presenetliv` \\(x^2\\) <b>presenetliv</b> [zapis](http://example.com/slo)\n"
    "e\u0301 \u20ac \U0001F600"
)

_GUARD_THREAD_NAME = "concept-header-guard"


def _guard_threads() -> list[threading.Thread]:
    return [th for th in threading.enumerate() if th.name == _GUARD_THREAD_NAME]


class _RawUpstream:
    """One real loopback TCP upstream driving a scripted raw byte stream."""

    def __init__(self, script: list[tuple[float, bytes]], hold: float = 0.3) -> None:
        self._script = script
        self._hold = hold
        self._listener = socket.socket()
        self._listener.bind(("127.0.0.1", 0))
        self._listener.listen(1)
        self.port = self._listener.getsockname()[1]
        self._thread: threading.Thread | None = None

    def _serve(self) -> None:
        try:
            conn, _ = self._listener.accept()
        except OSError:
            return
        try:
            for delay, chunk in self._script:
                if delay:
                    time.sleep(delay)
                conn.sendall(chunk)
            time.sleep(self._hold)
        except OSError:
            pass
        finally:
            with contextlib.suppress(OSError):
                conn.close()

    def start(self) -> None:
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def connect(self) -> http.client.HTTPConnection:
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.port, timeout=5.0
        )
        connection.connect()
        connection.request(
            "POST", "/", body=b"{}", headers={"Content-Length": "2"}
        )
        return connection

    def close(self) -> None:
        self._listener.close()
        if self._thread is not None:
            self._thread.join(5)
            assert not self._thread.is_alive()


def _bounded_acquire(
    connection: http.client.HTTPConnection,
    budget: float,
    limit: float = 10.0,
) -> http.client.HTTPResponse:
    """Run the guard under a finite watchdog.

    A regression that blocks inside the guard fails the test without
    hanging the suite (the worker is a daemon thread and dies with the
    process); the bounded/kill/reap containment for blocking cases is
    carried by the subprocess children below.
    """
    box: dict[str, object] = {}

    def _run() -> None:
        try:
            box["response"] = header_transport.acquire_response(
                connection, budget
            )
        except BaseException as exc:  # noqa: B036 - re-raised by the owner
            box["error"] = exc

    worker = threading.Thread(target=_run, daemon=True)
    worker.start()
    worker.join(limit)
    assert not worker.is_alive(), (
        "header guard did not terminate within the finite watchdog"
    )
    error = box.get("error")
    if error is not None:
        assert isinstance(error, BaseException)
        raise error
    response = box.get("response")
    assert isinstance(response, http.client.HTTPResponse), (
        "acquisition finished without a transferred response"
    )
    return response


class DirectGuardTests(unittest.TestCase):
    """Order 018-a requirements 2/4/5 over real stdlib getresponse."""

    def _fast(self) -> tuple[_RawUpstream, bytes]:
        body = b"x\r"
        wire = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            b"Content-Length: 2\r\n\r\n" + body
        )
        return _RawUpstream([(0.0, wire)]), body

    def test_budget_validation_rejects(self) -> None:
        for bad in (True, False, "30", None, float("inf"), float("-inf"),
                    float("nan"), 0, -1, object()):
            with self.assertRaises(ValueError):
                header_transport.validate_header_budget(bad)
        self.assertEqual(header_transport.validate_header_budget(30), 30.0)

    def test_fast_headers_succeed_and_guard_terminates(self) -> None:
        upstream, body = self._fast()
        upstream.start()
        connection = upstream.connect()
        try:
            response = _bounded_acquire(connection, 2.0)
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), body)
            response.close()
        finally:
            connection.close()
            upstream.close()
        self.assertEqual(_guard_threads(), [])

    def test_startup_overhead_not_concealed(self) -> None:
        # (a) a normal fast response under a generous budget succeeds;
        # scheduling jitter is not the boundary, so no tight wall-clock
        # assertion is made here.
        upstream, body = self._fast()
        upstream.start()
        connection = upstream.connect()
        try:
            response = _bounded_acquire(connection, 2.0)
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), body)
            response.close()
        finally:
            connection.close()
            upstream.close()
        self.assertEqual(_guard_threads(), [])
        # (b) the concrete delayed guard Thread.start regression: only
        # the guard thread's start is delayed 0.12 s (after the thread
        # is launched, on the owning thread), modelling guard startup
        # overhead; the complete response is already on the wire.  A
        # deadline anchored after the guard starts (the reviewed draft
        # bug) would accept this at ~0.121 s; the absolute deadline
        # anchored before startup must reject it.
        upstream2, _body2 = self._fast()
        upstream2.start()
        connection2 = upstream2.connect()
        original_start = threading.Thread.start

        def delayed_start(self: threading.Thread) -> None:
            original_start(self)
            if self.name == _GUARD_THREAD_NAME:
                time.sleep(0.12)

        started = time.monotonic()
        try:
            with (
                mock.patch.object(threading.Thread, "start", delayed_start),
                self.assertRaises(header_transport.HeaderTimeoutError),
            ):
                _bounded_acquire(connection2, 0.03)
        finally:
            connection2.close()
            upstream2.close()
        wall = time.monotonic() - started
        self.assertGreaterEqual(wall, 0.11)
        self.assertLessEqual(wall, 1.5)
        self.assertEqual(_guard_threads(), [])

    def test_slow_status_line_expires(self) -> None:
        wire = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            b"Content-Length: 2\r\n\r\nx\r"
        )
        upstream = _RawUpstream([(0.4, wire)])
        upstream.start()
        connection = upstream.connect()
        started = time.monotonic()
        with self.assertRaises(header_transport.HeaderTimeoutError):
            _bounded_acquire(connection, 0.15)
        wall = time.monotonic() - started
        connection.close()
        upstream.close()
        self.assertGreaterEqual(wall, 0.13)
        self.assertLessEqual(wall, 1.2)
        self.assertEqual(_guard_threads(), [])

    def test_slow_header_lines_expires(self) -> None:
        head = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
        tail = b"Content-Length: 2\r\n\r\n"
        script = [(0.0, head[:24])]
        script += [(0.06, head[24:48])]
        script += [(0.06, head[48:] + tail[:10])]
        script += [(0.06, tail[10:] + b"x\r")]
        upstream = _RawUpstream(script)
        upstream.start()
        connection = upstream.connect()
        started = time.monotonic()
        with self.assertRaises(header_transport.HeaderTimeoutError):
            _bounded_acquire(connection, 0.15)
        wall = time.monotonic() - started
        connection.close()
        upstream.close()
        self.assertGreaterEqual(wall, 0.13)
        self.assertLessEqual(wall, 1.2)
        self.assertEqual(_guard_threads(), [])

    def test_interim_100_never_resets_deadline(self) -> None:
        final = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            b"Content-Length: 2\r\n\r\nx\r"
        )
        upstream = _RawUpstream([(0.0, _INTERIM_100), (0.3, final)])
        upstream.start()
        connection = upstream.connect()
        started = time.monotonic()
        with self.assertRaises(header_transport.HeaderTimeoutError):
            _bounded_acquire(connection, 0.15)
        wall = time.monotonic() - started
        connection.close()
        upstream.close()
        self.assertGreaterEqual(wall, 0.13)
        self.assertLessEqual(wall, 1.2)
        self.assertEqual(_guard_threads(), [])

    def test_interim_100_to_final_within_budget_succeeds(self) -> None:
        final = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            b"Content-Length: 2\r\n\r\nx\r"
        )
        upstream = _RawUpstream([(0.0, _INTERIM_100), (0.05, final)])
        upstream.start()
        connection = upstream.connect()
        try:
            response = _bounded_acquire(connection, 1.0)
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), b"x\r")
            response.close()
        finally:
            connection.close()
            upstream.close()
        self.assertEqual(_guard_threads(), [])

    def test_racing_completion_expires(self) -> None:
        # The final header byte lands just after the deadline: completion
        # racing expiration loses to expiration.
        head = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            b"Content-Length: 2\r\n\r\nx\r"
        )
        upstream = _RawUpstream(
            [(0.0, head[:-12]), (0.04, head[-12:])]
        )
        upstream.start()
        connection = upstream.connect()
        started = time.monotonic()
        with self.assertRaises(header_transport.HeaderTimeoutError):
            _bounded_acquire(connection, 0.03)
        wall = time.monotonic() - started
        connection.close()
        upstream.close()
        self.assertGreaterEqual(wall, 0.02)
        self.assertLessEqual(wall, 0.25)
        self.assertEqual(_guard_threads(), [])

    def test_racing_completion_explicit_close(self) -> None:
        # A racing parser return after the deadline (observed through a
        # real stdlib begin() subclass that calls the actual begin and
        # then delays its return) must be explicitly closed by the
        # helper: completion racing expiration loses to expiration and
        # the parsed response is never transferred.
        # Connection: close detaches stdlib ownership from the
        # connection (getresponse closes the connection and retains no
        # response), so exactly one close of the parsed response is
        # attributable: the helper's explicit one.
        wire = (
            b"HTTP/1.1 200 OK\r\nConnection: close\r\n"
            b"Content-Type: text/plain\r\nContent-Length: 2\r\n\r\nx\r"
        )
        upstream = _RawUpstream([(0.0, wire)])
        observed: list[http.client.HTTPResponse] = []
        closes: list[http.client.HTTPResponse] = []

        class ObservedResponse(http.client.HTTPResponse):
            def begin(self) -> None:
                observed.append(self)
                super().begin()
                time.sleep(0.08)  # parser return races past the deadline

            def close(self) -> None:
                closes.append(self)
                super().close()

        upstream.start()
        connection = upstream.connect()
        connection.response_class = ObservedResponse
        started = time.monotonic()
        try:
            with self.assertRaises(header_transport.HeaderTimeoutError):
                _bounded_acquire(connection, 0.03)
            # The helper must have explicitly closed the racing parsed
            # response before any caller cleanup runs.
            self.assertEqual(len(observed), 1)
            self.assertEqual(len(closes), 1)
            self.assertIs(observed[0], closes[0])
            self.assertTrue(observed[0].closed)
        finally:
            connection.close()
            upstream.close()
        wall = time.monotonic() - started
        self.assertGreaterEqual(wall, 0.07)
        self.assertLessEqual(wall, 1.5)
        self.assertEqual(_guard_threads(), [])

    def test_no_late_timer_after_success(self) -> None:
        # A fast header followed by a body arriving after the header
        # budget (but within a generous body budget) must succeed: no
        # late timer may close the acquired connection.
        head = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            b"Content-Length: 2\r\n\r\n"
        )
        upstream = _RawUpstream([(0.0, head), (0.8, b"xy")])
        upstream.start()
        connection = upstream.connect()
        try:
            response = _bounded_acquire(connection, 0.5)
            self.assertEqual(response.status, 200)
            time.sleep(0.6)  # let the header budget pass with nothing pending
            self.assertEqual(response.read(), b"xy")
            response.close()
        finally:
            connection.close()
            upstream.close()
        self.assertEqual(_guard_threads(), [])

    def test_guard_isolation_other_connection(self) -> None:
        # A never-touches-B property: while A's guard is armed and about
        # to expire, B's acquisition succeeds untouched, and B stays
        # usable after A's expiration.
        a_wire = (
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n"
            b"Content-Length: 2\r\n\r\nA\r"
        )
        upstream_a = _RawUpstream([(0.4, a_wire)])
        upstream_b, b_body = self._fast()
        upstream_a.start()
        upstream_b.start()
        connection_a = upstream_a.connect()
        connection_b = upstream_b.connect()
        box: dict[str, object] = {}

        def _expire_a() -> None:
            try:
                box["response"] = header_transport.acquire_response(
                    connection_a, 0.15
                )
            except BaseException as exc:  # noqa: B036 - observed
                box["error"] = exc

        worker = threading.Thread(target=_expire_a, daemon=True)
        worker.start()
        time.sleep(0.05)  # A is in flight under its armed guard
        try:
            response_b = _bounded_acquire(connection_b, 2.0)
            self.assertEqual(response_b.status, 200)
            # Keep B's response open across A's expiration: a guard
            # shutdown of B's owned socket would break this read.
            worker.join(5)
            assert not worker.is_alive(), "A's acquisition did not finish"
            self.assertIsNone(box.get("response"))
            self.assertIsInstance(
                box.get("error"), header_transport.HeaderTimeoutError
            )
            self.assertEqual(response_b.read(), b_body)
            response_b.close()
        finally:
            worker.join(5)
            connection_a.close()
            connection_b.close()
            upstream_a.close()
            upstream_b.close()
        self.assertEqual(_guard_threads(), [])

    def test_setup_error_without_owned_socket(self) -> None:
        connection = http.client.HTTPConnection("127.0.0.1", 1, timeout=5.0)
        with self.assertRaises(header_transport.HeaderSetupError):
            header_transport.acquire_response(connection, 5.0)

    def test_transport_error_before_deadline_propagates(self) -> None:
        upstream = _RawUpstream([(0.0, b"GARBAGE\r\n\r\n")])
        upstream.start()
        connection = upstream.connect()
        with self.assertRaises(http.client.BadStatusLine):
            _bounded_acquire(connection, 2.0)
        connection.close()
        upstream.close()
        self.assertEqual(_guard_threads(), [])


class _MainBase(_WireMain):
    """Per-harness owner of the shared raw-wire main state."""


def _new_main_handler() -> type[_MainBase]:
    """A fresh per-harness subclass so concurrent harnesses keep
    distinct wire steps (the shared base keeps class-level state)."""

    cls: type[_MainBase] = type("_MainHeader", (_MainBase,), {})
    cls.steps = ()
    cls.hold = 0.0
    cls.served = 0
    return cls


class _OwnedThreadingServer(ThreadingHTTPServer):
    """Threading main server with owned non-daemon handler threads.

    ``server.shutdown()``/``server_close()`` alone do not join the
    per-connection handler threads; the fixture retains every handler
    thread and joins it explicitly on close, so no fixture work
    outlives the harness (order 018-a, requirement 5).
    """

    def __init__(
        self,
        server_address: tuple[str, int],
        handler: type[BaseHTTPRequestHandler],
    ) -> None:
        super().__init__(server_address, handler)
        self.handler_threads: list[threading.Thread] = []

    def process_request(self, request: object, client_address: object) -> None:
        thread = threading.Thread(
            target=self.process_request_thread,
            args=(request, client_address),
            daemon=False,
        )
        self.handler_threads.append(thread)
        thread.start()


class _HeaderHarness:
    """One real proxy with a raw-wire synthetic main and fake reviewer.

    Real ConceptProxy -> real RepairEngine (qualified Pandoc, real tiny
    SQLite index) -> real ResponsesReviewer; synthetic upstreams only.
    ``engine_calls`` is the call-through observation at the actual
    engine.repair boundary (Pandoc, corpus, detection): a bounded main
    failure must leave it empty, proving zero analysis before valid
    capture rather than mere HTTP-call absence.
    """

    def __init__(
        self,
        *,
        body_budget: float = 5.0,
        header_budget: float | None = None,
    ) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "header.sqlite"
        _build_db(self.db, unigram=_BUILD_UNIGRAM)
        self._main = _new_main_handler()
        self.main_server = _OwnedThreadingServer(("127.0.0.1", 0), self._main)
        self.review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        self.threads: list[threading.Thread] = []
        for server in (self.main_server, self.review_server):
            thread = threading.Thread(
                target=server.serve_forever, daemon=True
            )
            thread.start()
            self.threads.append(thread)
        reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.review_server.server_port}/v1",
            "test-model",
            timeout=5.0,
            api_key="fake-review-key",
        )
        self.engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        self.engine_calls: list[str] = []
        base_repair = self.engine.repair

        def observed_repair(text: str) -> str:
            self.engine_calls.append(text)
            return base_repair(text)

        self._repair_patch = mock.patch.object(self.engine, "repair", observed_repair)
        self._repair_patch.start()
        url = f"http://127.0.0.1:{self.main_server.server_port}"
        if header_budget is not None:
            self.proxy_server = proxy.ConceptProxy(
                ("127.0.0.1", 0),
                url,
                self.engine,
                timeout=body_budget,
                header_timeout=header_budget,
            )
        else:
            self.proxy_server = proxy.ConceptProxy(
                ("127.0.0.1", 0),
                url,
                self.engine,
                timeout=body_budget,
            )
        thread = threading.Thread(
            target=self.proxy_server.serve_forever, daemon=True
        )
        thread.start()
        self.threads.append(thread)

    def post(
        self,
        *,
        steps: tuple[tuple[float, bytes], ...],
        stream: bool,
        input_text: str,
        review: bytes,
        hold: float = 0.0,
        client_timeout: float = 10.0,
    ) -> tuple[int, bytes, float]:
        _assert_wire_steps(steps)
        self._main.steps = steps
        self._main.hold = hold
        self._main.served = 0
        _FakeUpstream.payload = review
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.recorded = []
        self.engine_calls = []
        body = _contract_body(stream, input_text)
        client = http.client.HTTPConnection(
            "127.0.0.1", self.proxy_server.server_port, timeout=client_timeout
        )
        started = time.monotonic()
        client.request(
            "POST",
            "/v1/responses",
            body=body,
            headers={
                "Content-Length": str(len(body)),
                "X-Concept-Request-ID": "req018a",
            },
        )
        response = client.getresponse()
        payload = response.read()
        wall = time.monotonic() - started
        client.close()
        return response.status, payload, wall

    @property
    def served(self) -> int:
        return self._main.served

    def close(self) -> None:
        self._repair_patch.stop()
        for server in (self.proxy_server, self.main_server, self.review_server):
            server.shutdown()
        for thread in self.threads:
            thread.join(5)
        for handler_thread in self.main_server.handler_threads:
            handler_thread.join(5)
        assert not any(thread.is_alive() for thread in self.threads)
        assert not any(
            thread.is_alive() for thread in self.main_server.handler_threads
        )
        for server in (self.proxy_server, self.main_server, self.review_server):
            server.server_close()
        self.temp.cleanup()


class _DummyEngine(proxy.RepairEngine):
    """Constructor-only stand-in: the wiring tests bind no traffic and
    never invoke the engine."""

    def __init__(self) -> None:
        return


class ConstructorWiringTests(unittest.TestCase):
    """Constructor and main() wiring (owned loopback port 0 only)."""

    def test_default_header_budget_is_the_configured_constant(self) -> None:
        server = proxy.ConceptProxy(
            ("127.0.0.1", 0), "http://127.0.0.1:1", _DummyEngine()
        )
        try:
            self.assertEqual(server.header_timeout, MAIN_HEADER_TIMEOUT_SECONDS)
            self.assertEqual(server.capture_timeout, 30.0)
        finally:
            server.server_close()

    def test_explicit_header_budget_stored(self) -> None:
        server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            "http://127.0.0.1:1",
            _DummyEngine(),
            header_timeout=7.5,
        )
        try:
            self.assertEqual(server.header_timeout, 7.5)
        finally:
            server.server_close()

    def test_positional_header_budget_rejected(self) -> None:
        # Deliberate: the 7th positional argument must be rejected
        # (header_timeout is keyword-only).
        with self.assertRaises(TypeError):
            proxy.ConceptProxy(  # type: ignore[call-arg]
                ("127.0.0.1", 0),
                "http://127.0.0.1:1",
                _DummyEngine(),
                30.0,
                None,
                None,
                5.0,
            )

    def test_invalid_header_budget_rejected_before_bind(self) -> None:
        # An invalid budget must raise before any bind allocation:
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
        ):
            BindObserving.bound = False
            # Deliberate invalid budget value.
            with self.assertRaises(ValueError):
                BindObserving(
                    ("127.0.0.1", 0),
                    "http://127.0.0.1:1",
                    _DummyEngine(),
                    header_timeout=bad,  # type: ignore[arg-type]
                )
            self.assertFalse(BindObserving.bound)

    def test_legacy_positional_shape_compatibility(self) -> None:
        # The pre-018 positional constructor shape keeps working:
        # timeout, trace_dir and usage_observer stay in their original
        # positions; header_timeout is keyword-only after them.
        temp = tempfile.TemporaryDirectory()
        observer: list[dict[str, object]] = []
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
            self.assertEqual(server.header_timeout, MAIN_HEADER_TIMEOUT_SECONDS)
        finally:
            server.server_close()
            temp.cleanup()

    def test_main_reads_concept_header_timeout(self) -> None:
        pandoc = os.environ.get("CONCEPT_PANDOC", "").strip()
        if not pandoc:
            raise unittest.SkipTest("qualified CONCEPT_PANDOC not configured")
        temp = tempfile.TemporaryDirectory()
        try:
            db = Path(temp.name) / "main-wire.sqlite"
            _build_db(db, unigram=_BUILD_UNIGRAM)
            seen: dict[str, object] = {}
            created: list[proxy.ConceptProxy] = []

            class Recorder(proxy.ConceptProxy):
                # Exercises the real validated constructor (upstream
                # URL check, budget validation, real bind) while
                # redirecting only the fixture address to an owned
                # port 0 (never the fixed service port).
                def __init__(
                    self,
                    address: tuple[str, int],
                    upstream: str,
                    engine: proxy.RepairEngine,
                    timeout: float = 30.0,
                    trace_dir: Path | None = None,
                    usage_observer: Callable[
                        [dict[str, object]], None
                    ] | None = None,
                    *,
                    header_timeout: float = MAIN_HEADER_TIMEOUT_SECONDS,
                ) -> None:
                    super().__init__(
                        ("127.0.0.1", 0),
                        upstream,
                        engine,
                        timeout=timeout,
                        trace_dir=trace_dir,
                        usage_observer=usage_observer,
                        header_timeout=header_timeout,
                    )
                    seen["timeout"] = self.capture_timeout
                    seen["header_timeout"] = self.header_timeout
                    created.append(self)

                def serve_forever(self, poll_interval: float = 0.5) -> None:
                    return

            base_env = dict(os.environ)
            base_env.pop("CONCEPT_TIMEOUT", None)
            base_env.pop("CONCEPT_HEADER_TIMEOUT", None)
            base_env["CONCEPT_INDEX"] = str(db)
            base_env["CONCEPT_UPSTREAM_URL"] = "http://127.0.0.1:1"
            base_env["CONCEPT_PANDOC"] = pandoc
            with mock.patch.object(proxy, "ConceptProxy", Recorder):
                env = dict(base_env, CONCEPT_HEADER_TIMEOUT="7.5")
                with mock.patch.dict(os.environ, env, clear=True):
                    self.assertEqual(proxy.main(), 0)
                self.assertEqual(seen["header_timeout"], 7.5)
                self.assertEqual(seen["timeout"], 30.0)
                self.assertEqual(len(created), 1)
                # The real constructor bound an owned port, never the
                # fixed service port.
                self.assertNotEqual(created[0].server_address[1], 18024)
                for server in created:
                    server.server_close()
                created.clear()

                seen.clear()
                with mock.patch.dict(os.environ, base_env, clear=True):
                    self.assertEqual(proxy.main(), 0)
                self.assertEqual(
                    seen["header_timeout"], MAIN_HEADER_TIMEOUT_SECONDS
                )
                self.assertEqual(seen["timeout"], 30.0)
                self.assertEqual(len(created), 1)
                for server in created:
                    server.server_close()
                created.clear()

                # Invalid values: float() or the constructor's budget
                # validation rejects before any validated construction
                # or owned bind.
                for bad_env in ("abc", "inf", "0"):
                    seen.clear()
                    env_bad = dict(base_env, CONCEPT_HEADER_TIMEOUT=bad_env)
                    with (
                        mock.patch.dict(os.environ, env_bad, clear=True),
                        self.assertRaises(ValueError),
                    ):
                        proxy.main()
                    self.assertEqual(created, [])
        finally:
            temp.cleanup()


class ProxyHeaderHttpTests(unittest.TestCase):
    """Order 018-a actual proxy HTTP acceptance over the header budget."""

    def _full(self, stream: bool, content: bytes) -> bytes:
        headers = _SSE_HEADERS if stream else _JSON_HEADERS
        return _with_content_length(headers, len(content)) + content

    def test_fast_header_json_positive(self) -> None:
        content = _json_completed(CLEAN)
        harness = _HeaderHarness(body_budget=5.0)
        try:
            status, payload, _wall = harness.post(
                steps=((0.0, self._full(False, content)),),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload, content)
            self.assertEqual(harness.engine_calls, [CLEAN])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            harness.close()

    def test_fast_header_sse_unicode_positive(self) -> None:
        content = _sse_baseline_utf8(CLEAN_UNICODE)
        _assert_unicode_on_wire(content)
        harness = _HeaderHarness(body_budget=5.0)
        try:
            status, payload, _wall = harness.post(
                steps=((0.0, self._full(True, content)),),
                stream=True,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload, content)
            self.assertEqual(harness.engine_calls, [CLEAN_UNICODE])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            _assert_unicode_on_wire(payload)
        finally:
            harness.close()

    def test_slow_status_line_zero_analysis(self) -> None:
        for stream in (False, True):
            content = (
                _sse_baseline_utf8(CLEAN) if stream else _json_completed(CLEAN)
            )
            harness = _HeaderHarness(body_budget=5.0, header_budget=0.15)
            try:
                status, _payload, wall = harness.post(
                    steps=((0.4, self._full(stream, content)),),
                    stream=stream,
                    input_text=CLEAN,
                    review=_review_payload([_prop("t0")]),
                )
                self.assertEqual(status, 502, _payload)
                self.assertEqual(harness.engine_calls, [])
                self.assertEqual(len(_FakeUpstream.recorded), 0)
                self.assertEqual(harness.served, 1)
                self.assertGreaterEqual(wall, 0.13)
                self.assertLessEqual(wall, 1.5)
            finally:
                harness.close()

    def test_slow_header_lines_zero_analysis(self) -> None:
        content = _json_completed(CLEAN)
        headers = _with_content_length(_JSON_HEADERS, len(content))
        pieces = [headers[i : i + 8] for i in range(0, len(headers), 8)]
        steps: list[tuple[float, bytes]] = [(0.0, pieces[0])]
        steps += [(0.06, piece) for piece in pieces[1:]]
        steps.append((0.06, content))
        harness = _HeaderHarness(body_budget=5.0, header_budget=0.15)
        try:
            status, _payload, wall = harness.post(
                steps=tuple(steps),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 502, _payload)
            self.assertEqual(harness.engine_calls, [])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertGreaterEqual(wall, 0.13)
            self.assertLessEqual(wall, 1.5)
        finally:
            harness.close()

    def test_interim_100_deadline_expires(self) -> None:
        content = _json_completed(CLEAN)
        final = self._full(False, content)
        harness = _HeaderHarness(body_budget=5.0, header_budget=0.15)
        try:
            status, _payload, wall = harness.post(
                steps=((0.0, _INTERIM_100), (0.3, final)),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 502, _payload)
            self.assertEqual(harness.engine_calls, [])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertGreaterEqual(wall, 0.13)
            self.assertLessEqual(wall, 1.5)
        finally:
            harness.close()

    def test_interim_100_to_final_within_budget_succeeds(self) -> None:
        content = _json_completed(CLEAN)
        harness = _HeaderHarness(body_budget=5.0, header_budget=1.0)
        try:
            status, payload, _wall = harness.post(
                steps=((0.0, _INTERIM_100), (0.05, self._full(False, content))),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload, content)
            self.assertEqual(harness.engine_calls, [CLEAN])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            harness.close()

    def test_body_after_header_budget_within_body_budget(self) -> None:
        # Fast headers, then the body at 0.3 s: after the 0.15 s header
        # budget has elapsed.  A single combined deadline anchored at
        # acquisition would reject this; the independent body budget
        # succeeds.
        content = _json_completed(CLEAN)
        headers = _with_content_length(_JSON_HEADERS, len(content))
        harness = _HeaderHarness(body_budget=5.0, header_budget=0.15)
        try:
            status, payload, wall = harness.post(
                steps=((0.0, headers), (0.3, content)),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload, content)
            self.assertEqual(harness.engine_calls, [CLEAN])
            self.assertGreaterEqual(wall, 0.28)
            self.assertLessEqual(wall, 2.0)
        finally:
            harness.close()

    def test_slow_headers_generous_header_short_body(self) -> None:
        # ~0.6 s of slow headers under a 3.0 s header budget with a
        # 0.5 s body budget: each axis bounds its own phase.
        content = _json_completed(CLEAN)
        headers = _with_content_length(_JSON_HEADERS, len(content))
        half = len(headers) // 2
        harness = _HeaderHarness(body_budget=0.5, header_budget=3.0)
        try:
            status, payload, wall = harness.post(
                steps=((0.3, headers[:half]), (0.3, headers[half:] + content)),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload, content)
            self.assertEqual(harness.engine_calls, [CLEAN])
            self.assertGreaterEqual(wall, 0.55)
            self.assertLessEqual(wall, 2.5)
        finally:
            harness.close()

    def test_expiration_recovery_same_proxy(self) -> None:
        content = _json_completed(CLEAN)
        full = self._full(False, content)
        harness = _HeaderHarness(body_budget=5.0, header_budget=0.15)
        try:
            status, _payload, _wall = harness.post(
                steps=((0.4, full),),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 502, _payload)
            self.assertEqual(harness.engine_calls, [])
            status, payload, _wall = harness.post(
                steps=((0.0, full),),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload, content)
            self.assertEqual(harness.engine_calls, [CLEAN])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            harness.close()

    def test_concurrent_other_proxy_isolation(self) -> None:
        content = _json_completed(CLEAN)
        full = self._full(False, content)
        harness1 = _HeaderHarness(body_budget=5.0, header_budget=0.15)
        harness2 = _HeaderHarness(body_budget=5.0)
        results: dict[str, object] = {}

        def _run_h2() -> None:
            status, payload, _wall = harness2.post(
                steps=((0.0, full),),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            results["status"] = status
            results["payload"] = payload

        try:
            worker = threading.Thread(target=_run_h2)
            worker.start()
            time.sleep(0.05)  # h2 in flight while h1's guard is armed
            status1, _payload1, _wall1 = harness1.post(
                steps=((0.4, full),),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            worker.join(10)
            assert not worker.is_alive(), "other proxy did not finish"
            self.assertEqual(status1, 502)
            self.assertEqual(harness1.engine_calls, [])
            self.assertEqual(results["status"], 200)
            self.assertEqual(results["payload"], content)
            self.assertEqual(harness2.engine_calls, [CLEAN])
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            worker.join(10)
            harness1.close()
            harness2.close()
        self.assertEqual(_guard_threads(), [])

    def test_no_guard_threads_after_mixed_posts(self) -> None:
        content = _json_completed(CLEAN)
        full = self._full(False, content)
        harness = _HeaderHarness(body_budget=5.0, header_budget=0.15)
        try:
            status, _payload, _wall = harness.post(
                steps=((0.4, full),),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 502)
            status, payload, _wall = harness.post(
                steps=((0.0, full),),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload, content)
        finally:
            harness.close()
        self.assertEqual(_guard_threads(), [])

    def test_useful_two_target_repair_under_header_budget(self) -> None:
        # Full order 018-a useful coverage: two supported edits are
        # applied while protected code, TeX, HTML, link and the
        # NFC-unstable decomposed/combining line are preserved exactly
        # in the final composed answer for both declared modes.
        review = _review_payload([_prop("t0"), _prop("t1")])
        for stream in (False, True):
            content = (
                _sse_baseline_utf8(USEFUL_018)
                if stream
                else _json_completed(USEFUL_018)
            )
            for marker in (
                "\u20ac".encode(),
                "\U0001F600".encode(),
                "e\u0301".encode(),
            ):
                self.assertIn(marker, content)
            harness = _HeaderHarness(body_budget=5.0, header_budget=1.0)
            try:
                status, payload, _wall = harness.post(
                    steps=((0.0, self._full(stream, content)),),
                    stream=stream,
                    input_text=TEXT,
                    review=review,
                )
                self.assertEqual(status, 200, payload)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                self.assertEqual(harness.engine_calls, [USEFUL_018])
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
                    text = completed["response"]["output"][0]["content"][0][
                        "text"
                    ]
                    self.assertEqual(text, EXPECTED_USEFUL_018)
                else:
                    text = json.loads(payload.decode())[
                        "output"
                    ][0]["content"][0]["text"]
                    self.assertEqual(text, EXPECTED_USEFUL_018)
                # Protected slices are preserved exactly in the final
                # composed answer (no NFC normalization of the
                # decomposed line either).
                for marker in (
                    b"`presenetliv`",
                    b"\\\\(x^2\\\\)",
                    b"<b>presenetliv</b>",
                    b"[zapis](http://example.com/slo)",
                    "e\u0301".encode(),
                ):
                    self.assertIn(marker, payload)
            finally:
                harness.close()

    def test_default_header_budget_wired(self) -> None:
        # No explicit header budget: the real constructor default
        # (MAIN_HEADER_TIMEOUT_SECONDS) is wired and tolerates a 0.5 s
        # header drip while the body arrives immediately after.
        content = _json_completed(CLEAN)
        headers = _with_content_length(_JSON_HEADERS, len(content))
        half = len(headers) // 2
        harness = _HeaderHarness(body_budget=5.0)
        try:
            status, payload, wall = harness.post(
                steps=((0.25, headers[:half]), (0.25, headers[half:] + content)),
                stream=False,
                input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200, payload)
            self.assertEqual(payload, content)
            self.assertEqual(harness.engine_calls, [CLEAN])
            self.assertGreaterEqual(wall, 0.45)
            self.assertLessEqual(wall, 2.0)
        finally:
            harness.close()


class TlsHeaderTests(unittest.TestCase):
    temp: tempfile.TemporaryDirectory[str]
    cert: Path
    key: Path

    """Actual TLS response-header budget over the real proxy chain.

    A subprocess child runs the full chain against a TLS main upstream
    using an owned ephemeral self-signed certificate trusted only
    inside that child via SSL_CERT_FILE.  Fast TLS headers succeed
    identically while slow TLS status-line and slow header-line
    drips fail at the 0.15 s header budget with zero review and zero
    engine calls.  No private fixture paths are referenced.
    """

    _CHILD = r"""
import http.client
import json
import os
import ssl
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from pathlib import Path

repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "concept-verification"))
# Trust the owned ephemeral certificate only inside this child.
os.environ["SSL_CERT_FILE"] = sys.argv[2]

import proxy
from qwen_client import ResponsesReviewer
from tests.test_review_batch import (
    _FakeUpstream,
    _contract_body,
    _prop,
    _real_spec,
)
from tests.test_responses_contract import _review_payload
from tests.test_runtime_corpus import _build_db
from tests.test_capture_transport import (
    CLEAN,
    CLEAN_UNICODE,
    _BUILD_UNIGRAM,
    _sse_baseline_utf8,
)

SSE = _sse_baseline_utf8(CLEAN_UNICODE)
for marker in ("\u00e9", "\u20ac", "\U0001F600"):
    assert marker.encode() in SSE

SSE_HEADERS = b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\n\r\n"


def with_length(headers, length):
    return headers[: -len(b"\r\n")] + f"Content-Length: {length}\r\n\r\n".encode()


class _TlsMainServer(ThreadingHTTPServer):
    # Owned non-daemon handler threads: shutdown/server_close alone do
    # not join them, so the child retains and joins each before RESULT.
    def __init__(self, address, handler):
        super().__init__(address, handler)
        self.handler_threads = []

    def process_request(self, request, client_address):
        thread = threading.Thread(
            target=self.process_request_thread,
            args=(request, client_address),
            daemon=False,
        )
        self.handler_threads.append(thread)
        thread.start()


class _TlsMain(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    steps = ()

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", "0")))
        try:
            for delay, wire in self.__class__.steps:
                if delay:
                    time.sleep(delay)
                self.wfile.write(wire)
                self.wfile.flush()
            self.close_connection = True
        except (BrokenPipeError, ConnectionResetError, ssl.SSLError):
            self.close_connection = True

    def log_message(self, *_args):
        return


def main():
    cert, key = Path(sys.argv[2]), Path(sys.argv[3])
    temp = tempfile.TemporaryDirectory()
    db = Path(temp.name) / "tls-header.sqlite"
    _build_db(db, unigram=_BUILD_UNIGRAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(str(cert), str(key))
    main_server = _TlsMainServer(("127.0.0.1", 0), _TlsMain)
    main_server.socket = context.wrap_socket(main_server.socket, server_side=True)
    review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
    reviewer = ResponsesReviewer(
        f"http://127.0.0.1:{review_server.server_port}/v1",
        "test-model",
        timeout=5.0,
        api_key="fake-review-key",
    )
    engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
    engine_calls = []
    base_repair = engine.repair

    def observed_repair(text):
        engine_calls.append(text)
        return base_repair(text)

    engine.repair = observed_repair
    proxy_server = proxy.ConceptProxy(
        ("127.0.0.1", 0),
        f"https://127.0.0.1:{main_server.server_port}",
        engine,
        timeout=5.0,
        header_timeout=0.15,
    )
    threads = []
    for server in (main_server, review_server, proxy_server):
        thread = threading.Thread(target=server.serve_forever, daemon=False)
        thread.start()
        threads.append(thread)

    def post(steps, stream):
        _TlsMain.steps = steps
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.recorded = []
        engine_calls.clear()
        # The proxy's own server is plain HTTP; the TLS leg is the
        # proxy->upstream connection only.
        client = http.client.HTTPConnection(
            "127.0.0.1", proxy_server.server_port, timeout=10.0
        )
        body = _contract_body(stream, CLEAN)
        client.request(
            "POST",
            "/v1/responses",
            body=body,
            headers={
                "Content-Length": str(len(body)),
                "X-Concept-Request-ID": "req018a-tls",
            },
        )
        response = client.getresponse()
        payload = response.read()
        client.close()
        return response.status, payload, list(engine_calls)

    cases = {}
    # (a) fast whole declared-length SSE over TLS.
    status, payload, engine = post(
        ((0.0, with_length(SSE_HEADERS, len(SSE)) + SSE),), True
    )
    cases["fast_sse"] = (
        status == 200
        and payload == SSE
        and not _FakeUpstream.recorded
        and engine == [CLEAN_UNICODE]
    )
    # (b) slow TLS status line at the 0.15 s header budget.
    status, _payload, engine = post(
        ((0.4, with_length(SSE_HEADERS, len(SSE)) + SSE),), True
    )
    cases["slow_status_502"] = (
        status == 502 and not _FakeUpstream.recorded and engine == []
    )
    # (c) slow TLS header lines at the 0.15 s header budget.
    header = with_length(SSE_HEADERS, len(SSE))
    pieces = [header[i : i + 8] for i in range(0, len(header), 8)]
    steps = [(0.0, pieces[0])]
    steps += [(0.06, piece) for piece in pieces[1:]]
    steps.append((0.0, SSE))
    status, _payload, engine = post(tuple(steps), True)
    cases["slow_headers_502"] = (
        status == 502 and not _FakeUpstream.recorded and engine == []
    )
    for server in (proxy_server, main_server, review_server):
        server.shutdown()
    for thread in threads:
        thread.join(5)
    for handler_thread in main_server.handler_threads:
        handler_thread.join(5)
    for server in (proxy_server, main_server, review_server):
        server.server_close()
    temp.cleanup()
    print("RESULT " + json.dumps({"cases": cases}), flush=True)


main()
"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.cert = Path(cls.temp.name) / "cert.pem"
        cls.key = Path(cls.temp.name) / "key.pem"
        if shutil.which("openssl") is None:
            raise unittest.SkipTest("openssl not available")
        proc = subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                str(cls.key),
                "-out",
                str(cls.cert),
                "-days",
                "1",
                "-subj",
                "/CN=127.0.0.1",
                "-addext",
                "subjectAltName=IP:127.0.0.1",
            ],
            capture_output=True,
            timeout=60,
        )
        assert proc.returncode == 0, proc.stderr.decode(errors="replace")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def test_tls_header_matrix(self) -> None:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        line = _run_child_bounded(
            self._CHILD,
            [str(ROOT.parent), str(self.cert), str(self.key)],
            deadline=90.0,
            env=env,
        )
        self.assertTrue(line.startswith(b"RESULT "), line[:200])
        result = json.loads(line[len(b"RESULT ") :].decode())
        for name in ("fast_sse", "slow_status_502", "slow_headers_502"):
            self.assertTrue(result["cases"][name], f"{name} failed: {result}")


class HangingHeaderTests(unittest.TestCase):
    """A main upstream that never sends a status line fails at the
    finite header budget with zero review and zero engine calls; the
    child runs in its own process group and the parent enforces a
    finite deadline, kills the process group and reaps it (order
    018-a, acceptance 3).
    """

    _CHILD = r"""
import http.client
import json
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "concept-verification"))
import proxy
from qwen_client import ResponsesReviewer
from tests.test_review_batch import (
    _FakeUpstream,
    _contract_body,
    _real_spec,
)
from tests.test_runtime_corpus import _build_db


class _SilentMain(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    release = threading.Event()

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.release.wait(30.0)  # never send a status or header line

    def log_message(self, *_args):
        return


def main():
    temp = tempfile.TemporaryDirectory()
    db = Path(temp.name) / "header-hang.sqlite"
    _build_db(db)
    main_server = HTTPServer(("127.0.0.1", 0), _SilentMain)
    review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
    reviewer = ResponsesReviewer(
        f"http://127.0.0.1:{review_server.server_port}/v1",
        "test-model",
        timeout=5.0,
        api_key="fake-review-key",
    )
    engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
    engine_calls = []
    base_repair = engine.repair

    def observed_repair(text):
        engine_calls.append(text)
        return base_repair(text)

    engine.repair = observed_repair
    # Generous socket/body budget so only the short elapsed header
    # budget can explain the bounded failure below.
    proxy_server = proxy.ConceptProxy(
        ("127.0.0.1", 0),
        f"http://127.0.0.1:{main_server.server_port}",
        engine,
        timeout=5.0,
        header_timeout=0.3,
    )
    threads = []
    for server in (main_server, review_server, proxy_server):
        thread = threading.Thread(target=server.serve_forever, daemon=False)
        thread.start()
        threads.append(thread)
    client = http.client.HTTPConnection(
        "127.0.0.1", proxy_server.server_port, timeout=10.0
    )
    body = _contract_body(True, "To je tako zapisano.")
    started = time.monotonic()
    client.request(
        "POST",
        "/v1/responses",
        body=body,
        headers={
            "Content-Length": str(len(body)),
            "X-Concept-Request-ID": "req018a-header-hang",
        },
    )
    response = client.getresponse()
    payload = response.read()
    wall = time.monotonic() - started
    client.close()
    _SilentMain.release.set()
    for server in (proxy_server, main_server, review_server):
        server.shutdown()
    for thread in threads:
        thread.join(5)
    for server in (proxy_server, main_server, review_server):
        server.server_close()
    temp.cleanup()
    print(
        "RESULT "
        + json.dumps(
            {
                "status": response.status,
                "wall": round(wall, 3),
                "review_calls": len(_FakeUpstream.recorded),
                "engine_calls": len(engine_calls),
            }
        ),
        flush=True,
    )


main()
"""

    def test_hanging_header_fails_at_budget_child_reaped(self) -> None:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        line = _run_child_bounded(
            self._CHILD, [str(ROOT.parent)], deadline=60.0, env=env
        )
        self.assertTrue(line.startswith(b"RESULT "), line[:200])
        result = json.loads(line[len(b"RESULT ") :].decode())
        self.assertEqual(result["status"], 502)
        self.assertGreaterEqual(result["wall"], 0.25)
        self.assertLessEqual(result["wall"], 2.0)
        self.assertEqual(result["review_calls"], 0)
        self.assertEqual(result["engine_calls"], 0)
