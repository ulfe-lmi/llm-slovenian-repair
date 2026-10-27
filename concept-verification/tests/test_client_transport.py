"""Order 020-a: bounded client request intake and exact body capture.

Proves, with real loopback wire traffic only, that the runnable proxy
bounds incoming client request intake under one finite positive
monotonic deadline anchored when handling the accepted connection
BEFORE any request-line/header/body read and before the guard starts;
the deadline covers the first byte, the request line, all headers and
the exact advertised body and never resets; the owned guard is a pure
timer that interrupts only the exact accepted client socket and is
cancelled and actually joined on every path; strict unambiguous
framing (repeated Content-Length fields, comma lists, any
Transfer-Encoding or unsupported Expect) is rejected with a fixed
content-free 400 before any body read or forwarding; an EOF-delivered
body shorter than the advertised length is a 400 even when its prefix
is complete valid JSON; and no intake failure reaches main, analysis,
evidence or review, with healthy same-proxy recovery afterward.
"""

from __future__ import annotations

import contextlib
import http.client
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from dataclasses import dataclass
from http.server import (  # noqa: E402
    BaseHTTPRequestHandler,
    HTTPServer,
    ThreadingHTTPServer,
)
from pathlib import Path
from typing import cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import client_transport  # noqa: E402
import proxy  # noqa: E402
from config import (  # noqa: E402
    API_MAX_REQUEST_BYTES,
    CLIENT_REQUEST_TIMEOUT_SECONDS,
    MAIN_HEADER_TIMEOUT_SECONDS,
    REVIEWER_HTTP_TIMEOUT_SECONDS,
)
from pandoc_protection import (  # noqa: E402
    PandocSpec,
    PandocStartupError,
    check_pandoc,
)
from qwen_client import ResponsesReviewer  # noqa: E402
from tests.test_capture_transport import (  # noqa: E402
    _BUILD_UNIGRAM,
    CLEAN,
    _sse_baseline_utf8,
)
from tests.test_header_transport import (  # noqa: E402
    EXPECTED_USEFUL_018,
    USEFUL_018,
    _DummyEngine,
)
from tests.test_responses_contract import (  # noqa: E402
    _Harness,
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


@dataclass(frozen=True)
class _DrainResult:
    """Bounded read result: ``closed`` is True only on an actual EOF
    (or a peer reset while reading), never on an observation
    timeout; an observation timeout must fail the test, not masquerade
    as a closed connection."""

    data: bytes
    closed: bool


def _drain(sock: socket.socket, timeout: float = 6.0) -> _DrainResult:
    """Read until EOF within a bounded observation timeout.

    Only an actual EOF or the expected peer-reset conditions count as
    closed; an observation TimeoutError returns closed=False and any
    other transport fault propagates to the test instead of being
    laundered into evidence.
    """
    sock.settimeout(timeout)
    buf = b""
    while True:
        try:
            chunk = sock.recv(65536)
        except TimeoutError:
            return _DrainResult(buf, False)
        except (
            ConnectionResetError,
            BrokenPipeError,
            ConnectionAbortedError,
        ):
            return _DrainResult(buf, True)
        if not chunk:
            return _DrainResult(buf, True)
        buf += chunk


def _head(
    body_len: int,
    extra: tuple[tuple[str, str], ...] = (),
    content_length: str | None = None,
) -> bytes:
    lines = ["POST /v1/responses HTTP/1.1", "Host: localhost"]
    for name, value in extra:
        lines.append(f"{name}: {value}")
    lines.append(
        f"Content-Length: {body_len if content_length is None else content_length}"
    )
    return "".join(line + "\r\n" for line in lines).encode() + b"\r\n"


def _raw_post(
    proxy_server: proxy.ConceptProxy,
    data: bytes,
    *,
    half_close: bool = False,
) -> tuple[_DrainResult, int, int]:
    """Send raw bytes to the real proxy over an owned socket.

    Returns (bounded drain result, main-forward count, review-call
    count).
    """
    sock = socket.create_connection(
        ("127.0.0.1", proxy_server.server_port), timeout=5
    )
    try:
        with contextlib.suppress(ConnectionResetError, BrokenPipeError, OSError):
            sock.sendall(data)
        if half_close:
            with contextlib.suppress(OSError):
                sock.shutdown(socket.SHUT_WR)
        result = _drain(sock)
    finally:
        sock.close()
    return (
        result,
        len(_MainUpstream.recorded),
        len(_FakeUpstream.recorded),
    )


class _OwnedThreadingServer(ThreadingHTTPServer):
    """Owned loopback HTTP server: every request handler is a known
    non-daemon thread retained for an asserted actual join."""

    def __init__(
        self,
        address: tuple[str, int],
        handler: type[BaseHTTPRequestHandler],
    ) -> None:
        super().__init__(address, handler)
        self.handler_threads: list[threading.Thread] = []

    def process_request(
        self, request: object, client_address: tuple[str, int]
    ) -> None:
        thread = threading.Thread(
            target=self.process_request_thread,
            args=(request, client_address),
            daemon=False,
        )
        self.handler_threads.append(thread)
        thread.start()


class _ObservedEngine(proxy.RepairEngine):
    """Real RepairEngine with a test-side call-through observation at
    the actual engine.repair boundary (controlled orchestration proof;
    the frozen engine logic runs unchanged via super()).  The base is
    a dataclass without a base-level post-init hook, so the test
    observer state is initialized in this explicit initializer around
    the inherited generated construction."""

    repair_calls: list[str]

    def __init__(
        self,
        index: Path,
        reviewer: proxy.Reviewer,
        mode: str = "local-context",
        pandoc: PandocSpec | None = None,
    ) -> None:
        super().__init__(index, reviewer, mode=mode, pandoc=pandoc)
        self.repair_calls = []

    def repair(self, text: str) -> str:
        self.repair_calls.append(text)
        return super().repair(text)


class _TimedHarness:
    """One real ConceptProxy with an explicit bounded intake budget
    (client_timeout), a real engine (qualified Pandoc, real tiny
    SQLite), a real validating reviewer, and synthetic main/review
    upstreams.  All owned server and handler threads are actually
    joined with assertions on close."""

    def __init__(self, client_timeout: float = 5.0) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "timed.sqlite"
        _build_db(self.db, unigram=_BUILD_UNIGRAM)
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = _json_completed(CLEAN)
        _MainUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        _FakeUpstream.recorded = []
        self.main_server = _OwnedThreadingServer(("127.0.0.1", 0), _MainUpstream)
        self.review_server = _OwnedThreadingServer(("127.0.0.1", 0), _FakeUpstream)
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
        self.engine = _ObservedEngine(self.db, reviewer, pandoc=_real_spec())
        self.proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{self.main_server.server_port}",
            self.engine,
            client_timeout=client_timeout,
        )
        thread = threading.Thread(
            target=self.proxy_server.serve_forever, daemon=True
        )
        thread.start()
        self.threads.append(thread)

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


@dataclass(frozen=True)
class _DripResult:
    """Bounded drip-then-drain result with faithful send observation:
    a phase timestamp is recorded only when every byte of that phase
    was actually sent; a failed or peer-closed send marks the drip
    incomplete instead of counting as a completed phase."""

    data: bytes
    closed: bool
    closed_at: float | None
    completed: bool
    connect_at: float
    observed: dict[str, float]


def _send_dripped(
    sock: socket.socket,
    data: bytes,
    steps: int,
    gap: float,
) -> tuple[int, bool]:
    """Send ``data`` in equal fragments with a sleep between
    fragments.  Returns (bytes actually sent, peer closed mid-send);
    sending stops as soon as the peer is gone, so failed sends never
    count as sent bytes or completed phases."""
    step = max(1, len(data) // steps)
    chunks = [data[index : index + step] for index in range(0, len(data), step)]
    sent = 0
    for index, chunk in enumerate(chunks):
        try:
            sock.sendall(chunk)
        except OSError:
            # Any send failure on the owned loopback socket means the
            # peer is gone; report what actually went out.
            return sent, True
        sent += len(chunk)
        if index < len(chunks) - 1:
            time.sleep(gap)
    return sent, False


def _drip_request(
    port: int,
    phases: list[tuple[bytes, int, float, str]],
    *,
    observer_timeout: float = 8.0,
) -> _DripResult:
    """Drip named byte phases to the proxy and drain the result; only
    fully sent phases get completion timestamps."""
    connect_at = time.monotonic()
    observed: dict[str, float] = {}
    completed = True
    sock = socket.create_connection(("127.0.0.1", port), timeout=5)
    try:
        for data, steps, gap, name in phases:
            if not completed:
                break
            sent, peer_closed = _send_dripped(sock, data, steps, gap)
            if peer_closed or sent != len(data):
                completed = False
                break
            observed[name] = time.monotonic()
        drained = _drain(sock, observer_timeout)
        closed_at = time.monotonic() if drained.closed else None
        return _DripResult(
            data=drained.data,
            closed=drained.closed,
            closed_at=closed_at,
            completed=completed,
            connect_at=connect_at,
            observed=observed,
        )
    finally:
        sock.close()


def _guard_threads() -> list[threading.Thread]:
    """Only the product's own intake guard threads (known owned name);
    no unrelated process or thread scanning."""
    return [th for th in threading.enumerate() if th.name == "concept-client-intake-guard"]


def _request_parts(body: bytes) -> tuple[bytes, bytes]:
    line = b"POST /v1/responses HTTP/1.1\r\n"
    headers = (
        b"Host: localhost\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n\r\n"
    )
    return line, headers


def _harness_post(
    proxy_server: proxy.ConceptProxy, *, stream: bool = False
) -> tuple[int, bytes]:
    """One healthy contract request through the real proxy (owned
    HTTP client, bounded)."""
    body = _contract_body(stream, input_text=CLEAN)
    client = http.client.HTTPConnection(
        "127.0.0.1", proxy_server.server_port, timeout=20
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
        return response.status, payload
    finally:
        client.close()


class IntakeTimeoutProxyTests(unittest.TestCase):
    """Order 020-a requirements 1, 2, 4 and 6 at the actual proxy
    boundary: one anchored monotonic elapsed deadline over raw loopback
    wire traffic; byte arrival never resets it; the owned guard is
    joined on every path; zero main/analysis/evidence/review on every
    intake failure with same-proxy recovery."""

    def test_idle_accepted_client_closed_near_budget_zero_downstream(self) -> None:
        harness = _TimedHarness(client_timeout=1.0)
        try:
            started = time.monotonic()
            sock = socket.create_connection(
                ("127.0.0.1", harness.proxy_port), timeout=5
            )
            result = _drain(sock, 6.0)
            sock.close()
            elapsed = time.monotonic() - started
            # Bounded quiet close near the anchored budget: before a
            # request line is safely available a quiet close is the
            # ordered behavior (no bytes are owed).
            self.assertTrue(result.closed, "idle client connection not closed")
            self.assertEqual(result.data, b"")
            self.assertGreaterEqual(elapsed, 0.85)
            self.assertLess(elapsed, 4.0)
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
            # Same-proxy recovery: a healthy request afterward succeeds.
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
            self.assertEqual(len(_MainUpstream.recorded), 1)
        finally:
            harness.close()


    def _drip_case(
        self,
        budget: float,
        phases: list[tuple[bytes, int, float, str]],
    ) -> tuple[_DripResult, _TimedHarness]:
        harness = _TimedHarness(client_timeout=budget)
        return _drip_request(harness.proxy_port, phases), harness

    def test_dripped_request_line_past_budget_zero_downstream(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        line, _headers = _request_parts(body)
        # 20 fragments x 0.1 s gap: the request line alone is still
        # arriving long after the anchored 1.0 s deadline.
        result, harness = self._drip_case(
            1.0, [(line, 20, 0.1, "line_done")]
        )
        try:
            self.assertTrue(result.closed)
            assert result.closed_at is not None
            # The connection stayed open at least until the anchored
            # deadline and only then closed, with zero downstream
            # work; the drip itself was scheduled past the budget.
            self.assertGreaterEqual(result.closed_at - result.connect_at, 0.9)
            self.assertLess(result.closed_at - result.connect_at, 4.0)
            self.assertNotIn(b"200", result.data.split(b"\r\n", 1)[0])
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
        finally:
            harness.close()

    def test_dripped_headers_past_budget_zero_downstream(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        line, headers = _request_parts(body)
        # The line arrives immediately; headers drip to ~1.2 s.
        result, harness = self._drip_case(
            1.0,
            [
                (line, 1, 0.0, "line_done"),
                (headers, 12, 0.1, "headers_done"),
            ],
        )
        try:
            self.assertTrue(result.closed)
            assert result.closed_at is not None
            self.assertGreaterEqual(result.closed_at - result.connect_at, 0.9)
            self.assertLess(result.closed_at - result.connect_at, 4.0)
            # The request line phase did fully complete before the
            # deadline; the headers phase was still open at expiry.
            self.assertIn("line_done", result.observed)
            self.assertLess(result.observed["line_done"] - result.connect_at, 0.9)
            self.assertNotIn("headers_done", result.observed)
            self.assertNotIn(b"200", result.data.split(b"\r\n", 1)[0])
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
        finally:
            harness.close()

    def test_dripped_body_past_budget_zero_downstream(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        line, headers = _request_parts(body)
        # Line and headers arrive immediately; the body drips to ~1.5 s.
        result, harness = self._drip_case(
            1.0,
            [
                (line, 1, 0.0, "line_done"),
                (headers, 1, 0.0, "headers_done"),
                (body, 10, 0.15, "body_done"),
            ],
        )
        try:
            self.assertTrue(result.closed)
            assert result.closed_at is not None
            self.assertGreaterEqual(result.closed_at - result.connect_at, 0.9)
            self.assertLess(result.closed_at - result.connect_at, 4.0)
            # Line and headers phases fully completed before the
            # deadline; the body phase was still open at expiry, so
            # it must not be counted as completed.
            self.assertIn("headers_done", result.observed)
            self.assertLess(
                result.observed["headers_done"] - result.connect_at, 0.9
            )
            self.assertNotIn("body_done", result.observed)
            self.assertNotIn(b"200", result.data.split(b"\r\n", 1)[0])
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
        finally:
            harness.close()

    def test_dripped_full_request_within_budget_reaches_producer(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        line, headers = _request_parts(body)
        # Same drip producer under a generous budget: every phase
        # completes well inside the anchored 5.0 s deadline, so the
        # request must reach the actual main producer.
        result, harness = self._drip_case(
            5.0,
            [
                (line, 5, 0.05, "line_done"),
                (headers, 5, 0.05, "headers_done"),
                (body, 5, 0.05, "body_done"),
            ],
        )
        try:
            # Every byte of every phase was actually sent before the
            # anchored deadline: the request reached the real main
            # producer and completed.
            self.assertTrue(result.completed)
            self.assertTrue(result.closed)
            self.assertTrue(
                result.data.startswith(b"HTTP/1.0 200 OK"), result.data[:80]
            )
            assert result.closed_at is not None
            self.assertEqual(_MainUpstream.recorded[0]["body"], body)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine.repair_calls, [CLEAN])
            self.assertLess(result.closed_at - result.connect_at, 4.5)
        finally:
            harness.close()

    def test_cumulative_each_phase_below_short_budget_over(self) -> None:
        # The ordered cumulative case: EACH actual measured phase
        # (line, headers, body) is below the short 1.0 s budget, but
        # the anchored deadline - never reset by byte arrival -
        # expires during the body phase.  A separate per-phase idle
        # timeout could not fail this; the one elapsed deadline does.
        body = _contract_body(False, input_text=CLEAN)
        line, headers = _request_parts(body)
        phases: list[tuple[bytes, int, float, str]] = [
            (line, 8, 0.06, "line_done"),
            (headers, 8, 0.06, "headers_done"),
            (body, 8, 0.06, "body_done"),
        ]
        result, harness = self._drip_case(1.0, phases)
        try:
            t0 = result.connect_at
            # Each actually completed phase (line, then headers) is
            # below the short budget on its own...
            self.assertIn("line_done", result.observed)
            self.assertIn("headers_done", result.observed)
            self.assertLess(result.observed["line_done"] - t0, 1.0)
            self.assertLess(
                result.observed["headers_done"] - result.observed["line_done"],
                1.0,
            )
            # ...while the anchored cumulative intake (never reset by
            # byte arrival) exceeds it: the connection stayed open
            # past the budget and was then closed with zero downstream
            # work.  A separate per-phase idle timeout could not fail
            # this shape.
            self.assertTrue(result.closed)
            assert result.closed_at is not None
            self.assertGreater(result.closed_at - t0, 0.95)
            self.assertLess(result.closed_at - t0, 4.0)
            self.assertNotIn("body_done", result.observed)
            self.assertNotIn(b"200", result.data.split(b"\r\n", 1)[0])
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
        finally:
            harness.close()
        # Generous positive control with the SAME producer: the same
        # drip schedule under a 5.0 s budget completes and forwards.
        result, harness = self._drip_case(5.0, phases)
        try:
            self.assertTrue(result.completed)
            self.assertTrue(
                result.data.startswith(b"HTTP/1.0 200 OK"), result.data[:80]
            )
            self.assertTrue(result.closed)
            self.assertEqual(_MainUpstream.recorded[0]["body"], body)
            self.assertEqual(harness.engine.repair_calls, [CLEAN])
        finally:
            harness.close()

    def test_completion_after_expiry_rejected(self) -> None:
        # The final header byte arrives after the anchored 0.6 s
        # deadline; the body follows immediately.  A late or racing
        # completion loses to the expired clock and can never reach
        # main, analysis or review.
        body = _contract_body(False, input_text=CLEAN)
        line, headers = _request_parts(body)
        result, harness = self._drip_case(
            0.6,
            [
                (line, 1, 0.0, "line_done"),
                (headers, 8, 0.09, "headers_done"),
                (body, 1, 0.0, "body_done"),
            ],
        )
        try:
            self.assertTrue(result.closed)
            assert result.closed_at is not None
            # The drip was still in flight at the anchored deadline
            # (headers scheduled to ~0.72 s); the connection was held
            # open until the expiry and then closed with the late
            # completion rejected.
            self.assertGreaterEqual(result.closed_at - result.connect_at, 0.55)
            self.assertLess(result.closed_at - result.connect_at, 3.0)
            self.assertNotIn("headers_done", result.observed)
            self.assertNotIn(b"200", result.data.split(b"\r\n", 1)[0])
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
        finally:
            harness.close()

    def test_stalled_body_closed_near_budget_zero_downstream(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        line, headers = _request_parts(body)
        # Headers complete and a few body bytes arrive, then silence:
        # the anchored deadline must close the stalled intake near the
        # budget with zero downstream work.
        started = time.monotonic()
        harness = _TimedHarness(client_timeout=1.0)
        try:
            sock = socket.create_connection(
                ("127.0.0.1", harness.proxy_port), timeout=5
            )
            with contextlib.suppress(
                ConnectionResetError, BrokenPipeError, OSError
            ):
                sock.sendall(line + headers + body[:20])
            result = _drain(sock, 6.0)
            sock.close()
            elapsed = time.monotonic() - started
            self.assertTrue(result.closed)
            self.assertGreaterEqual(elapsed, 0.85)
            self.assertLess(elapsed, 4.0)
            self.assertNotIn(b"200", result.data.split(b"\r\n", 1)[0])
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
        finally:
            harness.close()


class FramingProxyTests(unittest.TestCase):
    """Order 020-a requirement 3 at the actual proxy boundary: raw
    loopback wire traffic, real proxy/engine/Pandoc/SQLite/reviewer,
    synthetic main/review upstreams only (the CLEAN answer has no
    suspicion, so the healthy 200 path makes zero review calls)."""

    def _harness(self) -> _Harness:
        harness = _Harness()
        _MainUpstream.source = _json_completed(CLEAN)
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        return harness

    def test_complete_valid_body_200_forwarded_once_exact_bytes(self) -> None:
        harness = self._harness()
        try:
            body = _contract_body(False, input_text=CLEAN)
            data = _head(len(body), (("Content-Type", "application/json"),)) + body
            response, forwards, reviews = _raw_post(harness.proxy_server, data)
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 200 OK"), response.data[:80]
            )
            # The complete request is served and the connection is
            # actually closed (HTTP/1.0 close semantics preserved).
            self.assertTrue(response.closed)
            self.assertEqual(forwards, 1)
            self.assertEqual(reviews, 0)
            self.assertEqual(_MainUpstream.recorded[0]["path"], "/v1/responses")
            self.assertEqual(_MainUpstream.recorded[0]["body"], body)
            _status_line, _headers, payload = response.data.partition(b"\r\n\r\n")
            self.assertEqual(payload, _json_completed(CLEAN))
        finally:
            harness.close()

    def test_short_eof_complete_valid_json_prefix_400_zero_forward(self) -> None:
        # The advertised body is 11 bytes longer than the delivered
        # bytes; the delivered prefix is complete valid request JSON.
        # A complete valid JSON prefix is NOT a complete advertised
        # body: fixed content-free 400, always closes, zero main and
        # zero review (order 020-a, requirement 4).
        harness = self._harness()
        try:
            body = _contract_body(False, input_text=CLEAN)
            data = _head(
                len(body) + 11, (("Content-Type", "application/json"),)
            ) + body
            response, forwards, reviews = _raw_post(
                harness.proxy_server, data, half_close=True
            )
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 400 Bad Request"),
                response.data[:80],
            )
            # The incomplete-body error is always delivered with an
            # actual connection close.
            self.assertTrue(response.closed)
            self.assertIn(b"REQUEST_BODY_INCOMPLETE", response.data)
            self.assertEqual(forwards, 0)
            self.assertEqual(reviews, 0)
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
        finally:
            harness.close()

    def _duplicate_case(
        self, second_length: str
    ) -> None:
        harness = self._harness()
        try:
            body = _contract_body(False, input_text=CLEAN)
            data = (
                b"POST /v1/responses HTTP/1.1\r\n"
                b"Host: localhost\r\n"
                b"Content-Type: application/json\r\n"
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                b"Content-Length: " + second_length.encode() + b"\r\n"
                b"\r\n" + body
            )
            response, forwards, reviews = _raw_post(harness.proxy_server, data)
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 400 Bad Request"),
                response.data[:80],
            )
            self.assertTrue(response.closed)
            self.assertIn(b"REQUEST_FRAMING", response.data)
            self.assertEqual(forwards, 0)
            self.assertEqual(reviews, 0)
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
        finally:
            harness.close()

    def test_duplicate_content_length_equal_400_zero_forward(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        self._duplicate_case(str(len(body)))

    def test_duplicate_content_length_conflicting_400_zero_forward(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        self._duplicate_case(str(len(body) + 7))

    def _framing_case(self, data: bytes) -> tuple[bytes, bool, int, int]:
        harness = self._harness()
        try:
            response, forwards, reviews = _raw_post(harness.proxy_server, data)
            return response.data, response.closed, forwards, reviews
        finally:
            harness.close()

    def test_comma_list_length_400_zero_forward(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        data = (
            b"POST /v1/responses HTTP/1.1\r\n"
            b"Host: localhost\r\n"
            b"Content-Length: " + str(len(body)).encode() + b", "
            + str(len(body)).encode() + b"\r\n"
            b"\r\n" + body
        )
        payload, closed, forwards, reviews = self._framing_case(data)
        self.assertTrue(payload.startswith(b"HTTP/1.0 400 Bad Request"), payload[:80])
        self.assertTrue(closed)
        self.assertIn(b"REQUEST_FRAMING", payload)
        self.assertEqual((forwards, reviews), (0, 0))

    def test_transfer_encoding_400_zero_forward(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        data = (
            b"POST /v1/responses HTTP/1.1\r\n"
            b"Host: localhost\r\n"
            b"Transfer-Encoding: chunked\r\n"
            b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            b"\r\n" + body
        )
        payload, closed, forwards, reviews = self._framing_case(data)
        self.assertTrue(payload.startswith(b"HTTP/1.0 400 Bad Request"), payload[:80])
        self.assertTrue(closed)
        self.assertIn(b"REQUEST_FRAMING", payload)
        self.assertEqual((forwards, reviews), (0, 0))

    def test_expect_400_zero_forward(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        data = (
            b"POST /v1/responses HTTP/1.1\r\n"
            b"Host: localhost\r\n"
            b"Expect: 100-continue\r\n"
            b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            b"\r\n" + body
        )
        payload, closed, forwards, reviews = self._framing_case(data)
        self.assertTrue(payload.startswith(b"HTTP/1.0 400 Bad Request"), payload[:80])
        self.assertTrue(closed)
        self.assertIn(b"REQUEST_FRAMING", payload)
        self.assertEqual((forwards, reviews), (0, 0))

    def _size_policy_case(self, content_length: str) -> None:
        data = (
            b"POST /v1/responses HTTP/1.1\r\n"
            b"Host: localhost\r\n"
            b"Content-Length: " + content_length.encode() + b"\r\n"
            b"\r\n"
        )
        harness = self._harness()
        try:
            response, forwards, reviews = _raw_post(harness.proxy_server, data)
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 413 Request Entity Too Large"),
                response.data[:80],
            )
            self.assertTrue(response.closed)
            self.assertEqual(forwards, 0)
            self.assertEqual(reviews, 0)
        finally:
            harness.close()

    def test_missing_length_413(self) -> None:
        data = (
            b"POST /v1/responses HTTP/1.1\r\n"
            b"Host: localhost\r\n"
            b"\r\n"
        )
        harness = self._harness()
        try:
            response, forwards, reviews = _raw_post(harness.proxy_server, data)
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 413 Request Entity Too Large"),
                response.data[:80],
            )
            self.assertTrue(response.closed)
            self.assertEqual((forwards, reviews), (0, 0))
        finally:
            harness.close()

    def test_negative_length_413(self) -> None:
        self._size_policy_case("-5")

    def test_nondecimal_length_413(self) -> None:
        self._size_policy_case("abc")

    def test_overlarge_length_413_before_body(self) -> None:
        # The declaration alone exceeds the existing byte cap; no body
        # bytes are sent or read.
        self._size_policy_case(str(API_MAX_REQUEST_BYTES + 1))

    def _zero_padded_case(self, zeros: int) -> None:
        harness = self._harness()
        try:
            body = _contract_body(False, input_text=CLEAN)
            data = (
                b"POST /v1/responses HTTP/1.1\r\n"
                b"Host: localhost\r\n"
                b"Content-Length: " + b"0" * zeros + str(len(body)).encode() + b"\r\n"
                b"\r\n" + body
            )
            response, forwards, reviews = _raw_post(harness.proxy_server, data)
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 200 OK"), response.data[:80]
            )
            self.assertTrue(response.closed)
            self.assertEqual(forwards, 1)
            self.assertEqual(reviews, 0)
            # The exact declared (unpadded) number of body bytes was
            # captured and forwarded byte-for-byte.
            self.assertEqual(_MainUpstream.recorded[0]["body"], body)
        finally:
            harness.close()

    def test_zero_padded_length_32_zeros_200(self) -> None:
        self._zero_padded_case(32)

    def test_zero_padded_length_100_zeros_200(self) -> None:
        self._zero_padded_case(100)

    def test_zero_padded_length_50000_zeros_200(self) -> None:
        self._zero_padded_case(50000)

    def test_exact_byte_cap_2000000_legal_whitespace_200(self) -> None:
        # A valid small contract body padded with LEGAL trailing JSON
        # whitespace to exactly the existing request byte cap: the
        # independent input-codepoint cap is not bypassed, and the
        # full 2,000,000 declared bytes must be captured and forwarded
        # exactly (order 020-a, requirement 3 boundary at the cap).
        harness = self._harness()
        try:
            body = _contract_body(False, input_text=CLEAN)
            padded = body + b" " * (API_MAX_REQUEST_BYTES - len(body))
            self.assertEqual(len(padded), API_MAX_REQUEST_BYTES)
            data = _head(len(padded), (("Content-Type", "application/json"),)) + padded
            response, forwards, reviews = _raw_post(harness.proxy_server, data)
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 200 OK"), response.data[:80]
            )
            self.assertTrue(response.closed)
            self.assertEqual(forwards, 1)
            self.assertEqual(reviews, 0)
            self.assertEqual(_MainUpstream.recorded[0]["body"], padded)
        finally:
            harness.close()

    def test_trailing_bytes_never_second_request(self) -> None:
        # A second full request queued behind the first advertised
        # request must never become a second upstream request (HTTP/1.0
        # close, no pipelining): exactly one forward.
        body = _contract_body(False, input_text=CLEAN)
        one = _head(len(body), (("Content-Type", "application/json"),)) + body
        harness = self._harness()
        try:
            response, forwards, reviews = _raw_post(
                harness.proxy_server, one + one
            )
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 200 OK"), response.data[:80]
            )
            self.assertTrue(response.closed)
            self.assertEqual(forwards, 1)
            self.assertEqual(reviews, 0)
            self.assertEqual(len(_MainUpstream.recorded), 1)
        finally:
            harness.close()

    def test_other_path_404_preserved(self) -> None:
        body = _contract_body(False, input_text=CLEAN)
        data = _head(len(body)).replace(
            b"POST /v1/responses HTTP/1.1", b"POST /other HTTP/1.1"
        ) + body
        harness = self._harness()
        try:
            response, forwards, reviews = _raw_post(harness.proxy_server, data)
            self.assertTrue(
                response.data.startswith(b"HTTP/1.0 404 Not Found"),
                response.data[:80],
            )
            self.assertTrue(response.closed)
            self.assertEqual((forwards, reviews), (0, 0))
        finally:
            harness.close()

class GuardDirectTests(unittest.TestCase):
    """Order 020-a requirement 2 on the owned guard primitives: real
    socketpair transport, real timer thread/Event, actual joins on
    every path, exact captured-socket interruption, and bounded
    budget representability (no silently disabled timer)."""

    def test_interrupts_waiting_read_at_the_deadline(self) -> None:
        a, b = socket.socketpair()
        a.settimeout(3.0)
        guard = client_transport.IntakeGuard(a, 0.4)
        started = time.monotonic()
        try:
            with contextlib.suppress(OSError):
                a.recv(64)
        finally:
            elapsed = time.monotonic() - started
            expired = guard.release()
        self.assertTrue(expired)
        self.assertGreaterEqual(elapsed, 0.3)
        self.assertLess(elapsed, 2.5)
        self.assertFalse(guard._guard.is_alive())
        self.assertEqual(_guard_threads(), [])
        a.close()
        b.close()

    def test_fast_completion_not_expired_and_joined(self) -> None:
        a, b = socket.socketpair()
        a.settimeout(3.0)
        b.settimeout(3.0)
        guard = client_transport.IntakeGuard(a, 10.0)

        def producer() -> None:
            time.sleep(0.05)
            with contextlib.suppress(OSError):
                b.sendall(b"x")

        thread = threading.Thread(target=producer)
        thread.start()
        try:
            data = a.recv(64)
            thread.join(2)
            self.assertFalse(thread.is_alive())
            expired = guard.release()
        finally:
            a.close()
            b.close()
        self.assertEqual(data, b"x")
        self.assertFalse(expired)
        self.assertFalse(guard._guard.is_alive())

    def test_released_guard_same_socket_late_traffic(self) -> None:
        # A completed intake cancels and joins the real guard; exact
        # bytes sent on the same socket AFTER the original deadline
        # must still flow (release fully ends the timer's ownership).
        a, b = socket.socketpair()
        a.settimeout(3.0)
        b.settimeout(3.0)
        guard = client_transport.IntakeGuard(a, 0.3)

        def producer() -> None:
            time.sleep(0.05)
            with contextlib.suppress(OSError):
                b.sendall(b"first")

        thread = threading.Thread(target=producer)
        thread.start()
        try:
            first = a.recv(64)
            thread.join(2)
            self.assertFalse(thread.is_alive())
            early_expired = guard.release()
            self.assertFalse(guard._guard.is_alive())
            # Wait past the original 0.3 s deadline before sending.
            time.sleep(0.35)
            b.sendall(b"synthetic-late")
            late = a.recv(64)
        finally:
            a.close()
            b.close()
        self.assertEqual(first, b"first")
        self.assertFalse(early_expired)
        self.assertEqual(late, b"synthetic-late")

    def test_racing_completion_loses_to_expiry(self) -> None:
        a, b = socket.socketpair()
        a.settimeout(3.0)
        b.settimeout(3.0)
        # The byte is produced AFTER the anchored 0.05 s deadline: a
        # late or racing completion loses to the expired clock.
        guard = client_transport.IntakeGuard(a, 0.05)

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
        guard = client_transport.IntakeGuard(a, 10.0)
        first = guard.release()
        second = guard.release()
        self.assertFalse(first)
        self.assertFalse(second)
        self.assertFalse(guard._guard.is_alive())
        self.assertEqual(_guard_threads(), [])
        a.close()
        b.close()

    def test_expired_guard_other_connection_genuinely_late_traffic(self) -> None:
        a, b = socket.socketpair()
        other_a, other_b = socket.socketpair()
        b.settimeout(2.0)
        other_a.settimeout(2.0)
        other_b.settimeout(2.0)
        # A's guard expires and joins; B is a different live
        # connection whose genuinely late traffic still flows exactly.
        guard = client_transport.IntakeGuard(a, 0.4)
        eof = b.recv(64)
        expired = guard.release()
        self.assertEqual(eof, b"")
        self.assertTrue(expired)
        self.assertFalse(guard._guard.is_alive())
        other_b.sendall(b"synthetic-late")
        self.assertEqual(other_a.recv(64), b"synthetic-late")
        a.close()
        b.close()
        other_a.close()
        other_b.close()

    def test_controlled_startup_delay_charged_to_the_deadline(self) -> None:
        # Controlled orchestration proof: a startup delay introduced
        # around the real Thread.start (before the native start) is
        # charged to the one anchored clock and can itself consume a
        # short budget.
        a, b = socket.socketpair()
        a.settimeout(3.0)
        b.settimeout(3.0)
        real_start = threading.Thread.start

        def delayed_start(thread: threading.Thread) -> None:
            time.sleep(0.09)
            real_start(thread)

        started = time.monotonic()
        with mock.patch.object(threading.Thread, "start", delayed_start):
            guard = client_transport.IntakeGuard(a, 0.04)
        expired = guard.release()
        elapsed = time.monotonic() - started
        with contextlib.suppress(OSError):
            eof = b.recv(64)
        self.assertTrue(expired)
        self.assertEqual(eof, b"")
        self.assertGreaterEqual(elapsed, 0.09)
        self.assertFalse(guard._guard.is_alive())
        a.close()
        b.close()

    def test_unstarted_startup_failure_never_joins(self) -> None:
        # The injected start fails BEFORE the native start: the
        # product must not join an unstarted thread and must leave
        # nothing owned behind.
        product_joins: list[threading.Thread] = []
        real_join = threading.Thread.join

        def injected_start(thread: threading.Thread) -> None:
            raise RuntimeError("SYNTHETIC_STARTUP_FAILURE")

        def observe_join(
            thread: threading.Thread, timeout: float | None = None
        ) -> None:
            if (
                sys._getframe(1).f_code.co_filename
                == str(ROOT / "client_transport.py")
            ):
                product_joins.append(thread)
            real_join(thread, timeout)

        a, b = socket.socketpair()
        try:
            with (
                mock.patch.object(threading.Thread, "start", injected_start),
                mock.patch.object(threading.Thread, "join", observe_join),
                self.assertRaises(RuntimeError),
            ):
                client_transport.IntakeGuard(a, 1.0)
            self.assertEqual(product_joins, [])
            self.assertEqual(_guard_threads(), [])
        finally:
            a.close()
            b.close()

    def test_started_startup_failure_joined_by_product_before_raise(self) -> None:
        # The injected start performs the REAL native start and only
        # then fails: the product must cancel and actually join that
        # known owned thread before the failure propagates.
        product_joins: list[dict[str, object]] = []
        real_start = threading.Thread.start
        real_join = threading.Thread.join

        def injected_start(thread: threading.Thread) -> None:
            real_start(thread)
            raise RuntimeError("SYNTHETIC_STARTUP_FAILURE")

        def observe_join(
            thread: threading.Thread, timeout: float | None = None
        ) -> None:
            if (
                sys._getframe(1).f_code.co_filename
                == str(ROOT / "client_transport.py")
            ):
                product_joins.append(
                    {
                        "thread": thread,
                        "alive_at_join_entry": thread.is_alive(),
                    }
                )
            real_join(thread, timeout)

        a, b = socket.socketpair()
        started_threads: list[threading.Thread] = []
        try:
            with (
                mock.patch.object(threading.Thread, "start", injected_start),
                mock.patch.object(threading.Thread, "join", observe_join),
                self.assertRaises(RuntimeError),
            ):
                client_transport.IntakeGuard(a, 30.0)
            self.assertEqual(len(product_joins), 1)
            joined = cast(threading.Thread, product_joins[0]["thread"])
            self.assertTrue(cast(bool, product_joins[0]["alive_at_join_entry"]))
            self.assertFalse(joined.is_alive())
            started_threads.append(joined)
            self.assertEqual(_guard_threads(), [])
        finally:
            for thread in started_threads:
                self.assertFalse(thread.is_alive())
            a.close()
            b.close()

    def test_ended_startup_failure_still_joined_by_product(self) -> None:
        # The injected start performs the REAL native start, then a
        # real bounded join lets the short-budget guard run to its
        # natural end BEFORE the injected failure raises: the product
        # must still cancel and actually join that already-started
        # (already ended) exact thread before the failure propagates.
        product_joins: list[threading.Thread] = []
        real_start = threading.Thread.start
        real_join = threading.Thread.join

        def injected_start(thread: threading.Thread) -> None:
            real_start(thread)
            # Let the 0.025 s guard run to its natural end before the
            # startup failure is injected.
            real_join(thread, 5.0)
            # The known started guard must actually have ended BEFORE
            # the failure is injected (not merely after product
            # cleanup).
            assert not thread.is_alive()
            raise RuntimeError("SYNTHETIC_STARTUP_FAILURE")

        def observe_join(
            thread: threading.Thread, timeout: float | None = None
        ) -> None:
            if (
                sys._getframe(1).f_code.co_filename
                == str(ROOT / "client_transport.py")
            ):
                product_joins.append(thread)
            real_join(thread, timeout)

        a, b = socket.socketpair()
        a.settimeout(2.0)
        b.settimeout(2.0)
        try:
            with (
                mock.patch.object(threading.Thread, "start", injected_start),
                mock.patch.object(threading.Thread, "join", observe_join),
                self.assertRaises(RuntimeError) as raised,
            ):
                client_transport.IntakeGuard(a, 0.025)
            self.assertIn(
                "SYNTHETIC_STARTUP_FAILURE", str(raised.exception)
            )
            self.assertEqual(len(product_joins), 1)
            self.assertFalse(product_joins[0].is_alive())
            self.assertEqual(_guard_threads(), [])
            with contextlib.suppress(OSError):
                self.assertEqual(b.recv(64), b"")
        finally:
            a.close()
            b.close()

    def test_huge_budget_rejected_without_dead_timer(self) -> None:
        # A numerically finite setting the platform wait cannot
        # represent must be rejected before any timer starts; the
        # owned socket stays usable and nothing is left behind.
        a, b = socket.socketpair()
        a.settimeout(2.0)
        try:
            with self.assertRaises(ValueError):
                client_transport.IntakeGuard(a, 1e300)
            with self.assertRaises(ValueError):
                client_transport.IntakeGuard(a, 10**400)
            with self.assertRaises(ValueError):
                client_transport.IntakeGuard(
                    a, threading.TIMEOUT_MAX * 2
                )
            self.assertEqual(_guard_threads(), [])
            # The captured socket was never interrupted: live traffic
            # on the exact socket still works.
            b.settimeout(2.0)
            b.sendall(b"synthetic")
            self.assertEqual(a.recv(64), b"synthetic")
        finally:
            a.close()
            b.close()

    def test_platform_upper_bound_guard_releases_immediately(self) -> None:
        # A near-supported upper bound is representable: the guard
        # constructs, cancels and actually joins immediately without
        # waiting (and without any native wait overflow).
        a, b = socket.socketpair()
        try:
            guard = client_transport.IntakeGuard(a, threading.TIMEOUT_MAX)
            expired = guard.release()
            self.assertFalse(expired)
            self.assertFalse(guard._guard.is_alive())
            self.assertEqual(_guard_threads(), [])
        finally:
            a.close()
            b.close()


class StartupFailureProxyTests(unittest.TestCase):
    """Order 020-a requirement 2 at the actual handler boundary:
    controlled Thread.start failures before/after the real native
    start on the real ConceptProxy; the product contains its owned
    guard work, the failed request reaches zero downstream, and the
    same proxy recovers with a healthy request."""

    def _failure_case(self, mode: str) -> None:
        harness = _Harness()
        _MainUpstream.source = _json_completed(CLEAN)
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        real_start = threading.Thread.start
        real_join = threading.Thread.join
        product_joins: list[dict[str, object]] = []
        started: list[threading.Thread] = []

        def injected_start(thread: threading.Thread) -> None:
            if mode == "after_real_start":
                real_start(thread)
                started.append(thread)
            raise RuntimeError("SYNTHETIC_STARTUP_FAILURE")

        def observe_join(
            thread: threading.Thread, timeout: float | None = None
        ) -> None:
            if (
                sys._getframe(1).f_code.co_filename
                == str(ROOT / "client_transport.py")
            ):
                product_joins.append(
                    {
                        "thread": thread,
                        "alive_at_join_entry": thread.is_alive(),
                    }
                )
            real_join(thread, timeout)

        try:
            with (
                mock.patch.object(threading.Thread, "start", injected_start),
                mock.patch.object(threading.Thread, "join", observe_join),
            ):
                client = socket.create_connection(
                    ("127.0.0.1", harness.proxy_server.server_port),
                    timeout=5,
                )
                client.settimeout(5)
                body = _contract_body(False, input_text=CLEAN)
                data = _head(
                    len(body), (("Content-Type", "application/json"),)
                ) + body
                with contextlib.suppress(
                    ConnectionResetError, BrokenPipeError, OSError
                ):
                    client.sendall(data)
                result = _drain(client)
                client.close()
            self.assertTrue(result.closed)
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            for thread in started:
                self.assertFalse(thread.is_alive())
            if mode == "before_native_start":
                self.assertEqual(product_joins, [])
            else:
                self.assertEqual(len(product_joins), 1)
                joined = cast(threading.Thread, product_joins[0]["thread"])
                self.assertIn(joined, started)
                self.assertTrue(
                    cast(bool, product_joins[0]["alive_at_join_entry"])
                )
            # Same real proxy recovers with a healthy request.
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
        finally:
            harness.close()

    def test_guard_start_failure_before_native_start(self) -> None:
        self._failure_case("before_native_start")

    def test_guard_start_failure_after_real_start(self) -> None:
        self._failure_case("after_real_start")



class ConstructorWiringTests(unittest.TestCase):
    """Order 020-a requirement 8: the actual constructor
    default/override/rejection-before-bind, owned loopback port 0
    only (the fixed service port is never bound)."""

    def test_default_client_budget_is_the_configured_constant(self) -> None:
        server = proxy.ConceptProxy(
            ("127.0.0.1", 0), "http://127.0.0.1:1", _DummyEngine()
        )
        try:
            self.assertEqual(
                server.client_timeout, CLIENT_REQUEST_TIMEOUT_SECONDS
            )
            self.assertEqual(server.header_timeout, MAIN_HEADER_TIMEOUT_SECONDS)
            self.assertEqual(server.capture_timeout, 30.0)
        finally:
            server.server_close()

    def test_explicit_client_budget_stored(self) -> None:
        server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            "http://127.0.0.1:1",
            _DummyEngine(),
            client_timeout=7.5,
        )
        try:
            self.assertEqual(server.client_timeout, 7.5)
        finally:
            server.server_close()

    def test_positional_client_budget_rejected(self) -> None:
        # Deliberate: the 8th positional argument must be rejected
        # (client_timeout is keyword-only, appended after all existing
        # parameters without reordering them).
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
            )

    def test_invalid_client_budget_rejected_before_bind(self) -> None:
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
        ):
            BindObserving.bound = False
            with self.assertRaises(ValueError):
                BindObserving(
                    ("127.0.0.1", 0),
                    "http://127.0.0.1:1",
                    _DummyEngine(),
                    client_timeout=cast(float, bad),
                )
            self.assertFalse(BindObserving.bound)

    def test_legacy_positional_shape_compatibility(self) -> None:
        # The pre-020 positional constructor shape keeps working on an
        # owned loopback port 0: timeout, trace_dir and usage_observer
        # stay in their original positions and client_timeout keeps
        # its named 30 s default.
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
            self.assertEqual(
                server.client_timeout, CLIENT_REQUEST_TIMEOUT_SECONDS
            )
            self.assertEqual(server.header_timeout, MAIN_HEADER_TIMEOUT_SECONDS)
        finally:
            server.server_close()
            temp.cleanup()


class MainWiringTests(unittest.TestCase):
    """Order 020-a requirement 1 normal entry: main() reads
    CONCEPT_REQUEST_TIMEOUT into the real validated constructor; the
    real constructor binds an owned ephemeral port (never the fixed
    service port) and no serving happens."""

    def test_main_reads_concept_request_timeout(self) -> None:
        configured = os.environ.get("CONCEPT_PANDOC", "").strip()
        if not configured:
            raise unittest.SkipTest("qualified CONCEPT_PANDOC not configured")
        temp = tempfile.TemporaryDirectory()
        try:
            db = Path(temp.name) / "main-wire.sqlite"
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
                    seen["client_timeout"] = self.client_timeout
                    seen["header_timeout"] = self.header_timeout
                    seen["timeout"] = self.capture_timeout
                    created.append(self)

                def serve_forever(self, poll_interval: float = 0.5) -> None:
                    return

            base_env = {
                "CONCEPT_INDEX": str(db),
                "CONCEPT_UPSTREAM_URL": "http://127.0.0.1:1",
                "CONCEPT_REVIEWER_URL": "http://127.0.0.1:9/v1",
                "CONCEPT_PANDOC": configured,
            }
            with mock.patch.object(proxy, "ResponsesReviewer", Recorder), (
                mock.patch.object(proxy, "ConceptProxy", Port0Proxy)
            ):
                # Explicit override: intake 7.25 independent of
                # header 0.9, body 0.8 and the fixed 15 s reviewer.
                env = dict(
                    base_env,
                    CONCEPT_REQUEST_TIMEOUT="7.25",
                    CONCEPT_HEADER_TIMEOUT="0.9",
                    CONCEPT_TIMEOUT="0.8",
                )
                with mock.patch.dict(os.environ, env, clear=True):
                    self.assertEqual(proxy.main(), 0)
                self.assertEqual(seen["client_timeout"], 7.25)
                self.assertEqual(seen["header_timeout"], 0.9)
                self.assertEqual(seen["timeout"], 0.8)
                self.assertEqual(len(created), 1)
                self.assertGreater(created[0].server_address[1], 1024)
                self.assertNotEqual(created[0].server_address[1], 18024)
                reviewer = cast(ResponsesReviewer, created[0].engine.reviewer)
                self.assertEqual(reviewer.timeout, REVIEWER_HTTP_TIMEOUT_SECONDS)
                for server in created:
                    server.server_close()
                created.clear()

                # Unconfigured: the named 30 s constructor default
                # governs (the real constructor validates and sets it).
                with mock.patch.dict(os.environ, base_env, clear=True):
                    self.assertEqual(proxy.main(), 0)
                self.assertEqual(
                    seen["client_timeout"], CLIENT_REQUEST_TIMEOUT_SECONDS
                )
                self.assertEqual(len(created), 1)
                for server in created:
                    server.server_close()
                created.clear()

                # Invalid values are rejected before any validated
                # construction or owned bind.
                for bad_env in ("abc", "inf", "0", "1e300"):
                    env_bad = dict(base_env, CONCEPT_REQUEST_TIMEOUT=bad_env)
                    with (
                        mock.patch.dict(os.environ, env_bad, clear=True),
                        self.assertRaises(ValueError),
                    ):
                        proxy.main()
                    self.assertEqual(created, [])
        finally:
            temp.cleanup()



class _DelayedMain(BaseHTTPRequestHandler):
    """Synthetic main upstream that delays its complete response
    after reading the request (downstream work longer than the
    intake budget)."""

    protocol_version = "HTTP/1.1"
    source: bytes = b""
    delay: float = 0.0
    recorded: list[dict[str, object]] = []

    def do_POST(self) -> None:  # noqa: N802
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.__class__.recorded.append({"path": self.path, "body": body})
        if self.__class__.delay:
            time.sleep(self.__class__.delay)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(self.__class__.source)))
        self.end_headers()
        self.wfile.write(self.__class__.source)

    def log_message(self, *_args: object) -> None:
        return


class ChainProxyTests(unittest.TestCase):
    """Order 020-a requirement 7: real ConceptProxy + RepairEngine +
    qualified Pandoc + SQLite + ResponsesReviewer with synthetic
    loopback main/review; complete timely intake releases the guard
    before downstream, intake failures reach zero downstream with
    same-proxy recovery, and other connections stay isolated."""

    def test_chain_useful_two_targets_json_and_sse(self) -> None:
        for stream in (False, True):
            with self.subTest(stream=stream):
                harness = _TimedHarness(client_timeout=5.0)
                try:
                    _FakeUpstream.payload = _review_payload(
                        [_prop("t0"), _prop("t1")],
                        usage={
                            "input_tokens": 4,
                            "output_tokens": 6,
                            "total_tokens": 10,
                        },
                    )
                    source = (
                        _sse_baseline_utf8(USEFUL_018)
                        if stream
                        else _json_completed(USEFUL_018)
                    )
                    _MainUpstream.source = source
                    _MainUpstream.content_type = (
                        "text/event-stream" if stream else "application/json"
                    )
                    status, payload = _harness_post(
                        harness.proxy_server, stream=stream
                    )
                    self.assertEqual(status, 200, payload[:200])
                    self.assertEqual(len(_FakeUpstream.recorded), 1)
                    self.assertEqual(harness.engine.repair_calls, [USEFUL_018])
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
                        self.assertEqual(text, EXPECTED_USEFUL_018)
                    else:
                        text = json.loads(payload.decode())[
                            "output"
                        ][0]["content"][0]["text"]
                        self.assertEqual(text, EXPECTED_USEFUL_018)
                    # Protected slices are preserved exactly in the
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
                finally:
                    harness.close()

    def test_chain_no_suspicion_zero_review_exact_bytes(self) -> None:
        harness = _TimedHarness(client_timeout=5.0)
        try:
            source = _sse_baseline_utf8(CLEAN)
            _MainUpstream.source = source
            _MainUpstream.content_type = "text/event-stream"
            status, payload = _harness_post(
                harness.proxy_server, stream=True
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, source)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine.repair_calls, [CLEAN])
        finally:
            harness.close()

    def test_chain_incomplete_ingress_zero_then_healthy_next_same_proxy(self) -> None:
        harness = _TimedHarness(client_timeout=5.0)
        try:
            # Incomplete ingress: complete valid JSON prefix 11 bytes
            # short at EOF -> 400, zero main/analysis/review.
            body = _contract_body(False, input_text=CLEAN)
            data = _head(
                len(body) + 11, (("Content-Type", "application/json"),)
            ) + body
            result, forwards, reviews = _raw_post(
                harness.proxy_server, data, half_close=True
            )
            self.assertTrue(
                result.data.startswith(b"HTTP/1.0 400 Bad Request"),
                result.data[:80],
            )
            self.assertTrue(result.closed)
            self.assertEqual((forwards, reviews), (0, 0))
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
            # Healthy next request on the SAME proxy repairs.
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t1")]
            )
            _MainUpstream.source = _json_completed(USEFUL_018)
            _MainUpstream.content_type = "application/json"
            status, payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(harness.engine.repair_calls, [USEFUL_018])
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(
                json.loads(payload.decode())["output"][0]["content"][0][
                    "text"
                ],
                EXPECTED_USEFUL_018,
            )
        finally:
            harness.close()

    def test_chain_intake_timeout_zero_then_healthy_next_same_proxy(self) -> None:
        harness = _TimedHarness(client_timeout=1.0)
        try:
            body = _contract_body(False, input_text=CLEAN)
            line, headers = _request_parts(body)
            started = time.monotonic()
            sock = socket.create_connection(
                ("127.0.0.1", harness.proxy_port), timeout=5
            )
            with contextlib.suppress(
                ConnectionResetError, BrokenPipeError, OSError
            ):
                sock.sendall(line + headers + body[:20])
            result = _drain(sock, 6.0)
            sock.close()
            elapsed = time.monotonic() - started
            self.assertTrue(result.closed)
            self.assertGreaterEqual(elapsed, 0.85)
            self.assertLess(elapsed, 4.0)
            self.assertEqual(_MainUpstream.recorded, [])
            self.assertEqual(_FakeUpstream.recorded, [])
            self.assertEqual(harness.engine.repair_calls, [])
            # Same proxy recovers with a healthy request.
            _MainUpstream.source = _json_completed(CLEAN)
            _MainUpstream.content_type = "application/json"
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(harness.engine.repair_calls, [CLEAN])
        finally:
            harness.close()

    def test_chain_downstream_longer_than_intake_budget_still_succeeds(self) -> None:
        # Complete timely intake releases/joins the guard BEFORE the
        # engine work: downstream main work that outlasts the intake
        # budget must still complete and be repaired, not be
        # interrupted by the (already released) intake timer.
        temp = tempfile.TemporaryDirectory()
        serving: list[tuple[HTTPServer, threading.Thread]] = []
        handler_servers: list[_OwnedThreadingServer] = []
        closed_servers: list[HTTPServer] = []
        try:
            db = Path(temp.name) / "delayed.sqlite"
            _build_db(db, unigram=_BUILD_UNIGRAM)
            _DelayedMain.source = _json_completed(USEFUL_018)
            _DelayedMain.delay = 1.5
            _DelayedMain.recorded = []
            _FakeUpstream.status = 200
            _FakeUpstream.delay = 0.0
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t1")]
            )
            _FakeUpstream.recorded = []
            main_server = _OwnedThreadingServer(
                ("127.0.0.1", 0), _DelayedMain
            )
            closed_servers.append(main_server)
            handler_servers.append(main_server)
            review_server = _OwnedThreadingServer(
                ("127.0.0.1", 0), _FakeUpstream
            )
            closed_servers.append(review_server)
            handler_servers.append(review_server)
            for srv in (main_server, review_server):
                thread = threading.Thread(
                    target=srv.serve_forever, daemon=True
                )
                thread.start()
                serving.append((srv, thread))
            reviewer = ResponsesReviewer(
                f"http://127.0.0.1:{review_server.server_port}/v1",
                "test-model",
                timeout=5.0,
                api_key="fake-key",
            )
            engine = _ObservedEngine(db, reviewer, pandoc=_real_spec())
            proxy_server = proxy.ConceptProxy(
                ("127.0.0.1", 0),
                f"http://127.0.0.1:{main_server.server_port}",
                engine,
                client_timeout=1.0,
            )
            closed_servers.append(proxy_server)
            thread = threading.Thread(
                target=proxy_server.serve_forever, daemon=True
            )
            thread.start()
            serving.append((proxy_server, thread))

            body = _contract_body(False, input_text=USEFUL_018)
            client = http.client.HTTPConnection(
                "127.0.0.1", proxy_server.server_port, timeout=30
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
            self.assertEqual(response.status, 200, payload[:200])
            self.assertEqual(len(_DelayedMain.recorded), 1)
            self.assertEqual(_DelayedMain.recorded[0]["body"], body)
            self.assertEqual(engine.repair_calls, [USEFUL_018])
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(
                json.loads(payload.decode())["output"][0]["content"][0][
                    "text"
                ],
                EXPECTED_USEFUL_018,
            )
        finally:
            # Partial-setup-safe owned cleanup: shutdown only the
            # servers whose serve_forever thread actually started,
            # join only the known started threads, and close every
            # constructed owned server.
            for closed_srv, thread in serving:
                closed_srv.shutdown()
                thread.join(10)
                assert not thread.is_alive()
            for hsrv in handler_servers:
                for handler_thread in hsrv.handler_threads:
                    handler_thread.join(10)
                    assert not handler_thread.is_alive()
            for closed in closed_servers:
                closed.server_close()
            temp.cleanup()

    def test_chain_other_connection_isolation_genuinely_late(self) -> None:
        # A stalls mid-body on the single-threaded proxy.  B's
        # connection is established while A is in flight and B sends
        # NO request bytes until the real A guard has been released
        # and its owned timer thread actually joined (call-through
        # constructor/release observers on the known A guard identity,
        # matched by the exact accepted-socket peer of the bound
        # owned client).  Only then, at or after A's original
        # anchored deadline, does B send its full request.  A's guard
        # interrupted only A's exact socket, so B's exact socket
        # survives and B completes normally.  No fake guard, clock or
        # parser; no unrelated thread or process scanning.
        harness = _TimedHarness(client_timeout=1.0)
        sockets: list[socket.socket] = []
        a_started = threading.Event()
        a_released = threading.Event()
        observations: dict[str, object] = {}
        owned: list[tuple[object, object, tuple[str, int]]] = []
        a_endpoint: tuple[str, int] | None = None
        b_endpoint: tuple[str, int] | None = None
        real_init = client_transport.IntakeGuard.__init__
        real_release = client_transport.IntakeGuard.release

        def observe_init(
            guard: client_transport.IntakeGuard,
            sock: socket.socket,
            budget: float,
        ) -> None:
            real_init(guard, sock, budget)
            peer = sock.getpeername()
            owned.append((guard, sock, peer))
            if a_endpoint is not None and peer == a_endpoint:
                observations["a_guard"] = guard
                a_started.set()

        def observe_release(guard: client_transport.IntakeGuard) -> bool:
            expired = real_release(guard)
            if guard is observations.get("a_guard") and not a_released.is_set():
                a_guard = cast(
                    client_transport.IntakeGuard, observations["a_guard"]
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
            _MainUpstream.source = _json_completed(CLEAN)
            _MainUpstream.content_type = "application/json"
            body_a = _contract_body(False, input_text=CLEAN)
            body_b = _contract_body(False, input_text=CLEAN)
            line_a, headers_a = _request_parts(body_a)
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
                    client_transport.IntakeGuard, "__init__", observe_init
                ),
                mock.patch.object(
                    client_transport.IntakeGuard, "release", observe_release
                ),
            ):
                a.connect(("127.0.0.1", harness.proxy_port))
                with contextlib.suppress(
                    ConnectionResetError, BrokenPipeError, OSError
                ):
                    a.sendall(line_a + headers_a + body_a[:20])
                self.assertTrue(a_started.wait(3.0))
                # B's connection is established while A is still in
                # flight; B sends no request bytes yet.
                b.connect(("127.0.0.1", harness.proxy_port))
                self.assertFalse(a_released.is_set())
                # Wait for the observed real A guard release (the
                # product cancelled and actually joined the owned
                # timer before the call-through release returned).
                self.assertTrue(a_released.wait(5.0))
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
                b.sendall(full_b)
                a_result = _drain(a, 5.0)
                b_result = _drain(b, 5.0)
            # The exact A guard was observed released, expired, with
            # its owned timer thread actually ended before any B
            # request byte was sent (zero downstream work).
            self.assertTrue(cast(bool, observations["a_expired"]))
            self.assertTrue(
                cast(bool, observations["a_owned_thread_ended"])
            )
            self.assertEqual(
                cast("list[int]", observations["counts_before_b_send"]),
                [0, 0, 0],
            )
            # A closed without a 200; B's exact socket survived and
            # completed with the exact forwarded request.
            self.assertTrue(a_result.closed)
            self.assertNotIn(b"200", a_result.data.split(b"\r\n", 1)[0])
            self.assertTrue(
                b_result.data.startswith(b"HTTP/1.0 200 OK"),
                b_result.data[:80],
            )
            self.assertTrue(b_result.closed)
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(_MainUpstream.recorded[0]["body"], body_b)
            self.assertEqual(harness.engine.repair_calls, [CLEAN])
            self.assertEqual(_FakeUpstream.recorded, [])
            # Exactly the two owned guards: A's and B's, captured on
            # distinct socket objects for exactly the two known bound
            # client peers.
            self.assertEqual(len(owned), 2)
            assert b_endpoint is not None
            self.assertEqual(
                {peer for _guard, _sock, peer in owned},
                {a_endpoint, b_endpoint},
            )
            captured = [sock for _guard, sock, _peer in owned]
            self.assertIsNot(captured[0], captured[1])
        finally:
            for sock in sockets:
                sock.close()
            harness.close()



_HANGING_CHILD_SCRIPT = r"""
import socket, sys, time
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
cv = repo / "concept-verification"
sys.path.insert(0, str(cv))

from tests.test_client_transport import (  # noqa: E402
    CLEAN,
    _FakeUpstream,
    _MainUpstream,
    _TimedHarness,
    _contract_body,
    _harness_post,
    _request_parts,
)


def main() -> int:
    # The actual existing harness: real proxy/engine/qualified Pandoc/
    # SQLite/ResponsesReviewer with synthetic main/review; every owned
    # server and thread is actually joined on close.
    harness = _TimedHarness(client_timeout=1.0)
    try:
        body = _contract_body(False, input_text=CLEAN)
        line, headers = _request_parts(body)
        sock = socket.create_connection(
            ("127.0.0.1", harness.proxy_port), timeout=5
        )
        started = time.monotonic()
        try:
            sock.sendall(line + headers + body[:10])
            while True:
                try:
                    chunk = sock.recv(65536)
                except TimeoutError:
                    raise SystemExit("child: intake close exceeded 5 s")
                if not chunk:
                    break
        finally:
            sock.close()
        elapsed = time.monotonic() - started
        if not (0.85 <= elapsed <= 4.0):
            print(
                "child: close elapsed "
                f"{elapsed:.3f} outside 0.85-4.0"
            )
            return 1
        # The incomplete ingress reached zero downstream work.
        if (
            len(_MainUpstream.recorded)
            or len(harness.engine.repair_calls)
            or len(_FakeUpstream.recorded)
        ):
            print("child: incomplete ingress reached downstream")
            return 1
        # The same real proxy recovers with a healthy request.
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


class IntakePrivacyCleanupTests(unittest.TestCase):
    """Order 020-a requirement 8: privacy with permitted synthetic
    canaries on every intake failure path, zero downstream work,
    resource cleanup, and the actual silent handle_error boundary
    (controlled synthetic loopback fixtures only; not a general
    privacy or security certification)."""

    _CANARY = "SYNTHETIC_020_INTAKE_PRIVACY_CANARY_NOT_A_CREDENTIAL"

    @staticmethod
    def _fail_start(marker: str) -> Callable[[threading.Thread], None]:
        def fail_start(_thread: threading.Thread) -> None:
            raise RuntimeError(marker)

        return fail_start

    def _intake_case(
        self,
        harness: _TimedHarness,
        data: bytes,
        *,
        half_close: bool,
        expected_status: int | None,
    ) -> None:
        before = (
            len(_MainUpstream.recorded),
            len(harness.engine.repair_calls),
            len(_FakeUpstream.recorded),
        )
        sock = socket.create_connection(
            ("127.0.0.1", harness.proxy_port), timeout=3
        )
        try:
            with contextlib.suppress(
                ConnectionResetError, BrokenPipeError, OSError
            ):
                sock.sendall(data)
            if half_close:
                with contextlib.suppress(OSError):
                    sock.shutdown(socket.SHUT_WR)
            result = _drain(sock, 3.0)
        finally:
            sock.close()
        self.assertTrue(result.closed, result.data[:80])
        if expected_status is not None:
            self.assertTrue(
                result.data.startswith(
                    f"HTTP/1.0 {expected_status} ".encode()
                ),
                result.data[:80],
            )
        self.assertNotIn(self._CANARY.encode(), result.data)
        self.assertEqual(
            (
                len(_MainUpstream.recorded),
                len(harness.engine.repair_calls),
                len(_FakeUpstream.recorded),
            ),
            before,
        )

    def test_synthetic_canary_absent_from_all_intake_failures(self) -> None:
        marker = self._CANARY
        harness = _TimedHarness(client_timeout=0.25)
        stdout = io.StringIO()
        stderr = io.StringIO()
        try:
            body = _contract_body(False, input_text=marker)
            header = (
                ("Authorization", "Bearer " + marker),
                ("X-Synthetic-Private", marker),
                ("Content-Type", "application/json"),
            )
            cases: list[
                tuple[str, bytes, bool, str | None, int | None]
            ] = [
                (
                    "duplicate_length",
                    _head(
                        len(body),
                        header + (("Content-Length", str(len(body))),),
                    )
                    + body,
                    False,
                    None,
                    400,
                ),
                (
                    "malformed_length",
                    _head(len(body), header, content_length=marker) + body,
                    False,
                    None,
                    413,
                ),
                (
                    "incomplete_body",
                    _head(len(body) + 11, header) + body,
                    True,
                    None,
                    400,
                ),
                (
                    "intake_timeout",
                    _head(len(body), header) + body[:20],
                    False,
                    None,
                    None,
                ),
                (
                    "startup_before_native",
                    _head(len(body), header) + body,
                    False,
                    "failure",
                    None,
                ),
            ]
            with (
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                for name, data, half_close, failure, expected_status in cases:
                    with self.subTest(case=name):
                        if failure is not None:
                            with mock.patch.object(
                                threading.Thread,
                                "start",
                                self._fail_start(marker),
                            ):
                                self._intake_case(
                                    harness,
                                    data,
                                    half_close=half_close,
                                    expected_status=expected_status,
                                )
                        else:
                            self._intake_case(
                                harness,
                                data,
                                half_close=half_close,
                                expected_status=expected_status,
                            )
            logs = stdout.getvalue() + stderr.getvalue()
            self.assertNotIn(marker, logs)
        finally:
            harness.close()

    def test_no_guard_threads_after_mixed_sequence(self) -> None:
        harness = _TimedHarness(client_timeout=1.0)
        try:
            # 200 healthy
            status, _payload = _harness_post(harness.proxy_server)
            self.assertEqual(status, 200)
            # 400 ambiguous framing (duplicate length)
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
            # 413 missing length
            no_len = (
                b"POST /v1/responses HTTP/1.1\r\n"
                b"Host: localhost\r\n"
                b"Content-Type: application/json\r\n"
                b"\r\n" + body
            )
            _response2, _f2, _r2 = _raw_post(harness.proxy_server, no_len)
            # idle accepted client closed at the budget
            line, _headers = _request_parts(body)
            sock = socket.create_connection(
                ("127.0.0.1", harness.proxy_port), timeout=5
            )
            with contextlib.suppress(
                ConnectionResetError, BrokenPipeError, OSError
            ):
                sock.sendall(line)
            result = _drain(sock, 6.0)
            sock.close()
            self.assertTrue(result.closed)
        finally:
            harness.close()
        # The client's EOF is not server-cleanup completion: the owned
        # guard completion is asserted only after the harness has
        # actually shut down and joined every handler and serve
        # thread (each guard is released and joined by its handler
        # before that handler can finish).
        self.assertEqual(_guard_threads(), [])

    def test_handle_error_silent_on_owned_proxy(self) -> None:
        harness = _TimedHarness(client_timeout=5.0)
        try:
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                harness.proxy_server.handle_error(
                    object(), ("127.0.0.1", 0)
                )
            self.assertEqual(stderr.getvalue(), "")
        finally:
            harness.close()


class HangingChildTests(unittest.TestCase):
    """Order 020-a requirement 8: a slow-client/hanging boundary runs
    in an owned finite parent-supervised test subprocess with bounded
    kill/reap cleanup, so a bug cannot hang CI.  The actual resolved
    Pandoc binary is explicitly qualified before the child proof (an
    absent explicit env with a qualified PATH binary is supported; an
    explicit missing or wrong-version binary fails here, not via the
    engine's completed-original fallback)."""

    def test_hanging_client_bounded_in_finite_child(self) -> None:
        try:
            check_pandoc(_real_spec())
        except PandocStartupError as exc:
            self.fail(f"qualified Pandoc prerequisite failed: {exc}")
        proc = subprocess.Popen(
            [
                sys.executable,
                "-B",
                "-c",
                _HANGING_CHILD_SCRIPT,
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
                "hanging child exceeded the finite 120 s parent bound "
                f"(killed/reaped); stderr tail: {err[-500:]}"
            )
        self.assertEqual(
            proc.returncode,
            0,
            f"stdout={out[-800:]} / stderr={err[-800:]}",
        )
        self.assertIn("CHILD_OK", out)


if __name__ == "__main__":
    unittest.main()
