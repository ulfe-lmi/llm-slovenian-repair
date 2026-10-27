"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Bounded main-body capture.

Order 017-a acceptance coverage.

Direct collector boundaries over real http.client response plumbing
(socketpairs):

* UTF-8 code points split across wire chunks (2/3/4-byte, emoji) are
  carried, never rejected at the chunk boundary; a truncated final
  code point or a genuinely invalid byte is a bounded main failure at
  the known body end;
* declared Content-Length bodies deliver exactly the advertised bytes
  (early EOF fails; over-read bytes beyond the declaration are
  ignored), and only unknown-length delivery may terminate at the SSE
  terminal marker (keep-alive without EOF, body over-read into the
  buffered reader before ``begin()``);
* one finite positive monotonic body budget anchored at collection
  entry for declared, close-delimited and chunked delivery: slow drips
  fail at the budget (byte arrival never resets it; the producer's
  sent bytes are observed so a timeout cannot pass without traffic),
  and the budget covers the stdlib chunk-size/trailer lines;
* the bounded chunk-framing state machine accepts fast fragmented
  size lines and rejects invalid, overlong and truncated framing;
* close-delimited EOF leaves the socket usable (the stdlib
  connection-closing read path is never entered);
* nonfinite, nonpositive or nonnumeric budgets are rejected.

Actual proxy HTTP (real ConceptProxy -> real RepairEngine with the
qualified Pandoc and a real tiny SQLite index -> real ResponsesReviewer;
synthetic main/reviewer upstreams only):

* known-length JSON/SSE drips fail at the body budget within a
  generous finite tolerance while fast identical bytes succeed;
* close/chunked healthy JSON works; slow chunk-size/trailer drips fail
  at the budget; slow headers with a fast body stay outside the body
  budget (the separate, unfinished header axis);
* declared-length truncation fails even when the delivered envelope is
  structurally complete and valid (the declared length is advertised
  8 bytes beyond a complete body);
* whole versus split-at-each-byte 2/3/4-byte Unicode (real wire
  UTF-8, not escaped ASCII), emoji and CRLF SSE delimiters produce
  identical valid semantics (byte-identical no-edit output; useful
  two-target repair preserves protected slices);
* malformed/truncated UTF-8 remains 502 with zero review calls and
  zero engine.repair calls (call-through observation at the actual
  engine boundary proves no analysis before valid capture);
* declared framing preserves the complete body including trailing
  bytes after the SSE terminal marker; keep-alive completion without
  EOF returns before the held connection is released.

A hanging producer runs in an ordinary Python subprocess child (its
own process group) with the full real chain: the request fails at the
finite body budget with zero review and zero engine calls, and the
parent enforces a finite deadline, kills the process group and reaps
it, so no producer or reviewer thread or task outlives the test.

One real-TLS actual-HTTP matrix runs in a subprocess child against a
TLS main upstream using an owned ephemeral self-signed certificate
trusted only inside that child via SSL_CERT_FILE: whole,
split-3-byte and split-4-byte code points and a fragmented chunk-size
line all succeed identically, covering the nonblocking TLS readiness
path so a TLS-invalid shortcut cannot pass HTTP-only tests.  No
private fixture paths are referenced by the committed tests.

Only the main and reviewer upstreams are synthetic; no live service,
model, GPU or network boundary is touched.
"""

from __future__ import annotations

import http.client
import json
import os
import select
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import proxy  # noqa: E402
from proxy import ProxyError, _bounded_read  # noqa: E402
from qwen_client import ResponsesReviewer  # noqa: E402
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

# A clean answer: no detected suspicion, so healthy cases stay on the
# no-edit byte-identical path with zero review calls.
CLEAN = "To je tako zapisano."
# NFC-stable real 2/3/4-byte Unicode: e-acute (2), euro (3), emoji (4).
CLEAN_UNICODE = "To je tako zapisano \u00e9 \u20ac \U0001F600."
# Two reviewable occurrences with the supported je/target/zapisano
# local context (the established qualified pair), plus a protected code
# span and real 2/3/4-byte Unicode on a separate paragraph: both
# supported edits are accepted while the protected code span and the
# separate Unicode line are preserved (order 017-a, acceptance 2).
USEFUL = (
    "To je presenetliv zapisano, to je presenetliv zapisano.\n"
    "`presenetliv` \u00e9 \u20ac \U0001F600"
)
EXPECTED_USEFUL = (
    "To je tako zapisano, to je tako zapisano.\n"
    "`presenetliv` \u00e9 \u20ac \U0001F600"
)

_SSE_HEADERS = b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\n\r\n"
_JSON_HEADERS = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"


def _sse_baseline_utf8(text: str) -> bytes:
    """One-answer SSE baseline carrying real wire UTF-8.

    Mirrors the established one-answer terminal-copy baseline, but all
    JSON is serialized with ensure_ascii=False so the actual 2/3/4-byte
    code units of ``text`` appear on the wire (the shared fixture
    escapes to ASCII and cannot prove chunk-boundary tolerance).
    """

    def j(value: object) -> bytes:
        return json.dumps(value, ensure_ascii=False).encode()

    message = {
        "type": "message",
        "id": "m",
        "role": "assistant",
        "status": "completed",
        "output_index": 0,
        "content": [
            {"type": "output_text", "text": text, "content_index": 0}
        ],
    }
    delta = (
        b'{"type":"response.output_text.delta","item_id":"m","delta":'
        + j(text)
        + b"}"
    )
    part_done = (
        b'{"type":"response.content_part.done","item_id":"m","part":{"type":"output_text","text":'
        + j(text)
        + b"}"
        + b"}"
    )
    item = {
        "type": "message",
        "id": "m",
        "role": "assistant",
        "status": "completed",
        "content": [{"type": "output_text", "text": text}],
    }
    item_done = b'{"type":"response.output_item.done","item":' + j(item) + b"}"
    response = {
        "object": "response",
        "id": "r",
        "status": "completed",
        "usage": {"total_tokens": 4},
        "output": [message],
    }
    completed = b'{"type":"response.completed","response":' + j(response) + b"}"
    return b"".join(
        b"data: " + event + b"\n\n"
        for event in (delta, part_done, item_done, completed)
    )


def _with_content_length(headers: bytes, length: int) -> bytes:
    return headers[: -len(b"\r\n")] + f"Content-Length: {length}\r\n\r\n".encode()


def _start(
    status_headers: bytes, *, content_length: int | None = None
) -> tuple[http.client.HTTPResponse, socket.socket, socket.socket]:
    client, server = socket.socketpair()
    client.settimeout(5.0)
    if content_length is not None:
        status_headers = _with_content_length(status_headers, content_length)
    server.sendall(status_headers)
    response = http.client.HTTPResponse(client)
    response.begin()
    return response, client, server


def _start_buffered(
    status_headers: bytes, body: bytes
) -> tuple[http.client.HTTPResponse, socket.socket, socket.socket]:
    """Single-segment headers+body before begin().

    ``begin()`` (the same status/header parsing as ``getresponse``)
    over-reads the whole body into the buffered reader, so the raw
    socket is then quiet with no EOF: the buffered-overread
    precondition of the retained keep-alive semantics.
    """
    client, server = socket.socketpair()
    server.sendall(status_headers + body)
    client.settimeout(5.0)
    response = http.client.HTTPResponse(client)
    response.begin()
    return response, client, server


class _ProducerState:
    """Observed producer outcome so timeouts cannot pass with no traffic."""

    __slots__ = ("error", "sent", "started")

    def __init__(self) -> None:
        self.sent = 0
        self.error: BaseException | None = None
        self.started = threading.Event()


def _producer(
    sock: socket.socket, parts: list[tuple[float, bytes]], state: _ProducerState
) -> None:
    try:
        for delay, chunk in parts:
            if delay:
                time.sleep(delay)
            sock.sendall(chunk)
            state.sent += len(chunk)
            state.started.set()
    except BaseException as exc:  # noqa: B036 - observed by the test
        state.error = exc


class CollectorDirectTests(unittest.TestCase):
    """Order 017-a requirements 2-4 at the collector boundary."""

    def test_split_codepoint_across_wire_chunks(self) -> None:
        body = _sse_baseline_utf8(CLEAN_UNICODE)
        marker = "\U0001F600".encode()
        self.assertIn(marker, body)
        at = body.index(marker)
        response, client, server = _start(_SSE_HEADERS)
        state = _ProducerState()
        thread = threading.Thread(
            target=_producer, args=(server, [(0.05, body[at + 1 :])], state),
            daemon=True,
        )
        server.sendall(body[: at + 1])  # first byte of a 4-byte code point
        thread.start()
        try:
            out = _bounded_read(response, 1_000_000, 3.0, require_complete_sse=True)
            self.assertEqual(out, body)
            self.assertIsNone(state.error)
            self.assertEqual(state.sent, len(body) - at - 1)
        finally:
            client.close()
            server.close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_split_two_and_three_byte_codepoints(self) -> None:
        for char, width in (("\u00e9", 2), ("\u20ac", 3)):
            encoded = char.encode()
            self.assertEqual(len(encoded), width)
            body = _sse_baseline_utf8("To je tako zapisano " + char + ".")
            self.assertIn(encoded, body)
            at = body.index(encoded)
            response, client, server = _start(_SSE_HEADERS)
            rest = body[at + 1 :]
            if width == 2:
                parts: list[tuple[float, bytes]] = [(0.03, rest)]
            else:
                parts = [(0.03, rest[:1]), (0.03, rest[1:])]
            state = _ProducerState()
            thread = threading.Thread(
                target=_producer, args=(server, parts, state), daemon=True
            )
            server.sendall(body[: at + 1])  # first byte of the code point
            thread.start()
            try:
                out = _bounded_read(
                    response, 1_000_000, 3.0, require_complete_sse=True
                )
                self.assertEqual(out, body)
                self.assertIsNone(state.error)
                self.assertEqual(state.sent, len(rest))
            finally:
                client.close()
                server.close()
                thread.join(5)
                self.assertFalse(thread.is_alive())

    def test_truncated_final_codepoint_rejected(self) -> None:
        body = (
            b'data: {"type":"response.created"}\n\n'
            b"zapisano \xe2\x82"  # first two bytes of a 3-byte euro sign
        )
        response, client, server = _start(_SSE_HEADERS)
        try:
            server.sendall(body)
            server.close()
            with self.assertRaisesRegex(ProxyError, "not valid UTF-8"):
                _bounded_read(response, 1_000_000, 2.0, require_complete_sse=True)
        finally:
            client.close()

    def test_invalid_utf8_byte_rejected(self) -> None:
        body = b'data: {"type":"response.created"}\n\xff\n\n'
        response, client, server = _start(_SSE_HEADERS)
        try:
            server.sendall(body)
            server.close()
            with self.assertRaisesRegex(ProxyError, "not valid UTF-8"):
                _bounded_read(response, 1_000_000, 2.0, require_complete_sse=True)
        finally:
            client.close()

    def test_declared_length_truncated_fails(self) -> None:
        response, client, server = _start(_JSON_HEADERS, content_length=100)
        try:
            server.sendall(b"x" * 40)
            server.close()
            with self.assertRaisesRegex(
                ProxyError, "ended before declared length"
            ):
                _bounded_read(response, 1_000_000, 2.0)
        finally:
            client.close()

    def test_declared_length_exact_ignores_overread(self) -> None:
        response, client, server = _start(_JSON_HEADERS, content_length=5)
        try:
            server.sendall(b"hello" + b"EXTRA")
            self.assertEqual(_bounded_read(response, 1_000_000, 2.0), b"hello")
        finally:
            client.close()
            server.close()

    def test_declared_length_drip_times_out(self) -> None:
        response, client, server = _start(_JSON_HEADERS, content_length=1000)
        drip: list[tuple[float, bytes]] = [(0.0, b"y" * 10)] + [
            (0.05, b"y" * 10) for _ in range(9)
        ]
        state = _ProducerState()
        thread = threading.Thread(
            target=_producer, args=(server, drip, state), daemon=True
        )
        thread.start()
        try:
            self.assertTrue(state.started.wait(5), "producer sent no bytes at all")
            started = time.monotonic()
            with self.assertRaisesRegex(ProxyError, "timeout"):
                _bounded_read(response, 1_000_000, 0.15)
            elapsed = time.monotonic() - started
            self.assertGreater(state.sent, 0)
            self.assertGreaterEqual(elapsed, 0.13)
            self.assertLessEqual(elapsed, 1.5)
        finally:
            client.close()
            server.close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_close_drip_times_out(self) -> None:
        response, client, server = _start(_SSE_HEADERS)
        drip: list[tuple[float, bytes]] = [(0.0, b"z")] + [
            (0.05, b"z") for _ in range(9)
        ]
        state = _ProducerState()
        thread = threading.Thread(
            target=_producer, args=(server, drip, state), daemon=True
        )
        thread.start()
        try:
            self.assertTrue(state.started.wait(5), "producer sent no bytes at all")
            started = time.monotonic()
            with self.assertRaisesRegex(ProxyError, "timeout"):
                _bounded_read(response, 1_000_000, 0.15, require_complete_sse=True)
            elapsed = time.monotonic() - started
            self.assertGreater(state.sent, 0)
            self.assertGreaterEqual(elapsed, 0.13)
            self.assertLessEqual(elapsed, 1.5)
        finally:
            client.close()
            server.close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_chunked_fragmented_size_line(self) -> None:
        body = _sse_baseline_utf8(CLEAN)
        size_line = format(len(body), "x").encode() + b"\r\n"
        ending = b"\r\n0\r\n\r\n"
        response, client, server = _start(
            b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\n"
            b"Transfer-Encoding: chunked\r\n\r\n"
        )
        parts = [
            (0.0, size_line[:1]),
            (0.02, size_line[1:2]),
            (0.02, size_line[2:] + body),
            (0.02, ending),
        ]
        state = _ProducerState()
        thread = threading.Thread(
            target=_producer, args=(server, parts, state), daemon=True
        )
        thread.start()
        try:
            out = _bounded_read(response, 1_000_000, 3.0, require_complete_sse=True)
            self.assertEqual(out, body)
        finally:
            client.close()
            server.close()
            thread.join(5)
            self.assertFalse(thread.is_alive())
        # Chunked SSE terminates at the delimited terminal marker; the
        # trailing zero-chunk framing is request-scoped and need not be
        # sent, but the framing through the chunk data must be observed.
        self.assertGreaterEqual(state.sent, len(size_line) + len(body))

    def test_chunked_slow_size_line_times_out(self) -> None:
        size_line = b"64\r\n"
        response, client, server = _start(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            b"Transfer-Encoding: chunked\r\n\r\n"
        )
        parts = [(0.06, bytes([byte])) for byte in size_line]
        state = _ProducerState()
        thread = threading.Thread(
            target=_producer, args=(server, parts, state), daemon=True
        )
        thread.start()
        try:
            self.assertTrue(state.started.wait(5), "producer sent no bytes at all")
            started = time.monotonic()
            with self.assertRaisesRegex(ProxyError, "timeout"):
                _bounded_read(response, 1_000_000, 0.15)
            elapsed = time.monotonic() - started
            self.assertGreater(state.sent, 0)
            self.assertGreaterEqual(elapsed, 0.13)
            self.assertLessEqual(elapsed, 1.5)
        finally:
            client.close()
            server.close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_chunked_slow_trailer_times_out(self) -> None:
        response, client, server = _start(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            b"Transfer-Encoding: chunked\r\n\r\n"
        )
        parts: list[tuple[float, bytes]] = [
            (0.0, b"5\r\nhello\r\n0\r\ntrail: 1\r\nx"),
            (0.06, b"\r"),
            (0.06, b"\n"),
        ]
        state = _ProducerState()
        thread = threading.Thread(
            target=_producer, args=(server, parts, state), daemon=True
        )
        thread.start()
        try:
            self.assertTrue(state.started.wait(5), "producer sent no bytes at all")
            started = time.monotonic()
            with self.assertRaisesRegex(ProxyError, "timeout"):
                _bounded_read(response, 1_000_000, 0.15)
            elapsed = time.monotonic() - started
            self.assertGreater(state.sent, 0)
            self.assertGreaterEqual(elapsed, 0.13)
            self.assertLessEqual(elapsed, 1.5)
        finally:
            client.close()
            server.close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_chunked_invalid_size_rejected(self) -> None:
        response, client, server = _start(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            b"Transfer-Encoding: chunked\r\n\r\n"
        )
        try:
            server.sendall(b"zz\r\n")
            server.close()
            with self.assertRaisesRegex(ProxyError, "chunk framing"):
                _bounded_read(response, 1_000_000, 2.0)
        finally:
            client.close()

    def test_chunked_overlong_size_line_rejected(self) -> None:
        response, client, server = _start(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            b"Transfer-Encoding: chunked\r\n\r\n"
        )
        try:
            server.sendall(b"1" * 300 + b"\r\n")
            server.close()
            with self.assertRaisesRegex(ProxyError, "chunk framing"):
                _bounded_read(response, 1_000_000, 2.0)
        finally:
            client.close()

    def test_chunked_truncated_rejected(self) -> None:
        response, client, server = _start(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            b"Transfer-Encoding: chunked\r\n\r\n"
        )
        try:
            server.sendall(b"64\r\n" + b"0" * 10)
            server.close()
            with self.assertRaisesRegex(ProxyError, "chunk framing"):
                _bounded_read(response, 1_000_000, 2.0)
        finally:
            client.close()

    def test_chunked_huge_size_exceeds_bound(self) -> None:
        response, client, server = _start(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            b"Transfer-Encoding: chunked\r\n\r\n"
        )
        try:
            server.sendall(b"7d0\r\n" + b"Q" * 200)
            server.close()
            with self.assertRaisesRegex(ProxyError, "exceeds capture bound"):
                _bounded_read(response, 100, 2.0)
        finally:
            client.close()

    def test_budget_validation_rejects_nonfinite_nonpositive(self) -> None:
        response, client, server = _start(_JSON_HEADERS, content_length=1)
        try:
            server.sendall(b"1")
            bad_values: tuple[object, ...] = (
                0, -1, float("nan"), float("inf"), True
            )
            for bad in bad_values:
                with self.assertRaisesRegex(
                    ProxyError, "finite positive duration"
                ):
                    _bounded_read(response, 100, bad)  # type: ignore[arg-type]
        finally:
            client.close()
            server.close()

    def test_close_eof_keeps_socket_usable(self) -> None:
        body = b'{"ok":true}'
        response, client, server = _start(_JSON_HEADERS)
        try:
            server.sendall(body)
            server.close()
            out = _bounded_read(response, 1_000_000, 2.0)
            self.assertEqual(out, body)
            # The reader must not have closed the socket (the stdlib
            # connection-closing read path is never entered).
            self.assertNotEqual(client.fileno(), -1)
        finally:
            client.close()

    def test_keepalive_buffered_terminal_event(self) -> None:
        # Headers and the complete body share one segment before
        # begin(), so the body sits in the buffered reader while the
        # wire is quiet: the retained buffered-overread precondition.
        body = (
            b": keep this comment\n\n"
            b'data: {"type":"response.created"}\n\n'
            b'data: {"type":"response.completed","response":{}}\n\n'
        )
        response, client, server = _start_buffered(_SSE_HEADERS, body)
        try:
            raw_socket = response.fp.raw._sock  # type: ignore[attr-defined]
            ready, _, _ = select.select([raw_socket], [], [], 0.2)
            self.assertFalse(ready)  # precondition: wire quiet, no EOF
            started = time.monotonic()
            out = _bounded_read(response, 1_000_000, 2.0, require_complete_sse=True)
            self.assertLess(time.monotonic() - started, 1.0)
            self.assertEqual(out, body)
        finally:
            client.close()
            server.close()


class _WireMain(BaseHTTPRequestHandler):
    """Synthetic main upstream: raw wire steps with per-step delays."""

    protocol_version = "HTTP/1.1"
    steps: tuple[tuple[float, bytes], ...] = ()
    hold: float = 0.0
    served: int = 0

    def do_POST(self) -> None:  # noqa: N802
        self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.__class__.served += 1
        try:
            for delay, wire in self.steps:
                if delay:
                    time.sleep(delay)
                self.wfile.write(wire)
                self.wfile.flush()
            if self.hold:
                time.sleep(self.hold)
                self.close_connection = False
            else:
                self.close_connection = True
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True

    def log_message(self, *_args: object) -> None:
        return


# The shared healthy corpus plus the real 2/3/4-byte wire-UTF-8 marker
# that is a word token (e-acute; euro and emoji are symbols and never
# tokenize).  With a count above the detector threshold the marker is a
# known word, so the no-edit path stays genuinely no-candidate.
_BUILD_UNIGRAM: list[tuple[str, object]] = [
    ("to", 100),
    ("je", 100),
    ("tako", 100),
    ("presenetljiv", 50),
    ("zapisano", 50),
    ("\u00e9", 20),
]


class _CaptureHarness:
    """One real proxy with a raw-wire synthetic main and fake reviewer.

    Real ConceptProxy -> real RepairEngine (qualified Pandoc, real tiny
    SQLite index) -> real ResponsesReviewer; synthetic upstreams only.
    ``engine_calls`` is the call-through observation at the actual
    engine.repair boundary (Pandoc, corpus, detection): a bounded main
    failure must leave it empty, proving zero analysis before valid
    capture rather than mere HTTP-call absence.
    """

    def __init__(self, budget: float = 5.0) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "capture.sqlite"
        _build_db(self.db, unigram=_BUILD_UNIGRAM)
        self.main_server = HTTPServer(("127.0.0.1", 0), _WireMain)
        self.review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        self.threads: list[threading.Thread] = []
        for server in (self.main_server, self.review_server):
            thread = threading.Thread(target=server.serve_forever, daemon=True)
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

        self._repair_patch = mock.patch.object(
            self.engine, "repair", observed_repair
        )
        self._repair_patch.start()
        self.proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{self.main_server.server_port}",
            self.engine,
            timeout=budget,
        )
        thread = threading.Thread(target=self.proxy_server.serve_forever, daemon=True)
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
        _WireMain.steps = steps
        _WireMain.hold = hold
        _WireMain.served = 0
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
                "X-Concept-Request-ID": "req017a",
            },
        )
        response = client.getresponse()
        payload = response.read()
        wall = time.monotonic() - started
        client.close()
        return response.status, payload, wall

    def close(self) -> None:
        self._repair_patch.stop()
        for server in (self.proxy_server, self.main_server, self.review_server):
            server.shutdown()
        for server in (self.proxy_server, self.main_server, self.review_server):
            server.server_close()
        for thread in self.threads:
            thread.join(5)
        assert not any(thread.is_alive() for thread in self.threads)
        self.temp.cleanup()


def _assert_wire_steps(steps: object) -> None:
    # Guard against flat (delay, bytes) items leaking into step lists:
    # every entry must be a (number, bytes) pair before product code
    # sees the wire fixture.
    assert isinstance(steps, tuple), type(steps)
    for item in steps:
        assert isinstance(item, tuple) and len(item) == 2, repr(item)[:80]
        assert isinstance(item[0], (int, float)) and not isinstance(
            item[0], bool
        ), repr(item)[:80]
        assert isinstance(item[1], (bytes, bytearray)), repr(item)[:80]


def _chunk_wire(content: bytes) -> tuple[bytes, bytes]:
    size_line = format(len(content), "x").encode() + b"\r\n"
    ending = b"\r\n0\r\n\r\n"
    return size_line, ending


def _drip(body: bytes, stride: int, delay: float) -> list[tuple[float, bytes]]:
    pieces = [body[i : i + stride] for i in range(0, len(body), stride)]
    return [(0.0, pieces[0])] + [(delay, p) for p in pieces[1:]]


def _assert_unicode_on_wire(content: bytes) -> None:
    for marker in ("\u00e9", "\u20ac", "\U0001F600"):
        assert marker.encode() in content


class CaptureHttpTests(unittest.TestCase):
    """Order 017-a acceptance criteria 1-3 over actual proxy HTTP."""

    def _sse_headers(self) -> bytes:
        return b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\n\r\n"

    def _json_headers(self) -> bytes:
        return b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"

    def test_length_drip_fails_at_budget(self) -> None:
        for stream, content in (
            (False, _json_completed(CLEAN)),
            (True, _sse_baseline_utf8(CLEAN)),
        ):
            headers = self._sse_headers() if stream else self._json_headers()
            headers = _with_content_length(headers, len(content))
            harness = _CaptureHarness(budget=0.15)
            try:
                steps = ((0.0, headers),) + tuple(_drip(content, 16, 0.04))
                started = time.monotonic()
                status, _payload, wall = harness.post(
                    steps=steps, stream=stream, input_text=CLEAN,
                    review=_review_payload([_prop("t0")]),
                )
                self.assertLessEqual(time.monotonic() - started, 2.0)
                self.assertEqual(status, 502)
                self.assertEqual(_WireMain.served, 1)
                self.assertEqual(len(_FakeUpstream.recorded), 0)
                self.assertEqual(harness.engine_calls, [])
                self.assertGreaterEqual(wall, 0.13)
                self.assertLessEqual(wall, 1.3)
            finally:
                harness.close()

    def test_length_whole_fast_succeeds(self) -> None:
        for stream, content in (
            (False, _json_completed(CLEAN)),
            (True, _sse_baseline_utf8(CLEAN)),
        ):
            headers = self._sse_headers() if stream else self._json_headers()
            headers = _with_content_length(headers, len(content))
            harness = _CaptureHarness()
            try:
                status, payload, _wall = harness.post(
                    steps=((0.0, headers + content),),
                    stream=stream, input_text=CLEAN,
                    review=_review_payload([_prop("t0")]),
                )
                self.assertEqual(status, 200)
                self.assertEqual(payload, content)
                self.assertEqual(len(_FakeUpstream.recorded), 0)
                self.assertEqual(harness.engine_calls, [CLEAN])
            finally:
                harness.close()

    def test_close_json_works(self) -> None:
        content = _json_completed(CLEAN)
        harness = _CaptureHarness()
        try:
            headers = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
            status, payload, _wall = harness.post(
                steps=((0.0, headers + content),),
                stream=False, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, content)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [CLEAN])
        finally:
            harness.close()

    def test_chunked_json_works(self) -> None:
        content = _json_completed(CLEAN)
        size_line, ending = _chunk_wire(content)
        harness = _CaptureHarness()
        try:
            headers = (
                b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                b"Transfer-Encoding: chunked\r\n\r\n"
            )
            status, payload, _wall = harness.post(
                steps=((0.0, headers + size_line + content + ending),),
                stream=False, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, content)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [CLEAN])
        finally:
            harness.close()

    def test_chunked_fragmented_size_line_works(self) -> None:
        content = _json_completed(CLEAN)
        size_line, ending = _chunk_wire(content)
        harness = _CaptureHarness()
        try:
            headers = (
                b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                b"Transfer-Encoding: chunked\r\n\r\n"
            )
            steps = (
                (0.0, headers + size_line[:1]),
                (0.02, size_line[1:2]),
                (0.02, size_line[2:] + content),
                (0.02, ending),
            )
            status, payload, _wall = harness.post(
                steps=steps, stream=False, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, content)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [CLEAN])
        finally:
            harness.close()

    def test_chunked_slow_size_and_trailer_fail_at_budget(self) -> None:
        content = _json_completed(CLEAN)
        size_line, ending = _chunk_wire(content)
        base = (
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            b"Transfer-Encoding: chunked\r\n\r\n"
        )
        # Slow size line: the budget must cover the stdlib chunk-size read.
        harness = _CaptureHarness(budget=0.15)
        try:
            steps = ((0.0, base),) + tuple(
                (0.06, bytes([byte])) for byte in size_line
            )
            status, _payload, wall = harness.post(
                steps=steps, stream=False, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 502)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [])
            self.assertGreaterEqual(wall, 0.13)
            self.assertLessEqual(wall, 1.3)
        finally:
            harness.close()
        # Slow trailer after the terminating zero chunk.
        harness = _CaptureHarness(budget=0.15)
        try:
            steps = (
                (0.0, base + size_line + content + b"\r\n0\r\ntrail: 1\r\nx"),
                (0.06, b"\r"),
                (0.06, b"\n"),
                (0.06, b"y"),  # peer still active past the deadline
            )
            status, _payload, wall = harness.post(
                steps=steps, stream=False, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 502)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [])
            self.assertGreaterEqual(wall, 0.13)
            self.assertLessEqual(wall, 1.3)
        finally:
            harness.close()

    def test_slow_headers_fast_body_outside_body_budget(self) -> None:
        # The header phase is the separate unfinished header axis: with a
        # fast body the request must succeed even though the headers take
        # far longer than the body budget.
        content = _json_completed(CLEAN)
        headers = self._json_headers()
        harness = _CaptureHarness(budget=0.15)
        try:
            chunks = [headers[i : i + 8] for i in range(0, len(headers), 8)]
            steps = ((0.0, chunks[0]),) + tuple(
                (0.06, chunk) for chunk in chunks[1:]
            ) + ((0.0, content),)
            status, payload, wall = harness.post(
                steps=steps, stream=False, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, content)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [CLEAN])
            self.assertGreaterEqual(wall, 0.3)
        finally:
            harness.close()

    def test_declared_truncation_fails(self) -> None:
        for stream, content in (
            (False, _json_completed(CLEAN)),
            (True, _sse_baseline_utf8(CLEAN)),
        ):
            headers = self._sse_headers() if stream else self._json_headers()
            # The complete, structurally valid envelope is delivered in
            # full while the declared length exceeds it by 8 bytes: only
            # the declared-length contract can fail, not structure.
            declared = _with_content_length(headers, len(content) + 8)
            harness = _CaptureHarness()
            try:
                status, _payload, _wall = harness.post(
                    steps=((0.0, declared), (0.0, content)),
                    stream=stream, input_text=CLEAN,
                    review=_review_payload([_prop("t0")]),
                )
                self.assertEqual(status, 502)
                self.assertEqual(len(_FakeUpstream.recorded), 0)
                self.assertEqual(harness.engine_calls, [])
            finally:
                harness.close()

    def _split_identical(
        self,
        content: bytes,
        stream: bool,
        input_text: str,
        chunked: bool,
        answer: str,
    ) -> None:
        if chunked:
            size_line, ending = _chunk_wire(content)
            base = (
                b"HTTP/1.1 200 OK\r\nContent-Type: "
                + (b"text/event-stream" if stream else b"application/json")
                + b"\r\nTransfer-Encoding: chunked\r\n\r\n"
            )
            framed = size_line + content
            whole_steps = ((0.0, base + framed + ending),)
            split_steps = (
                (0.0, base + framed[:1]),
            ) + tuple((0.0, bytes([byte])) for byte in framed[1:]) + (
                (0.0, ending),
            )
        else:
            base = self._sse_headers() if stream else self._json_headers()
            whole_steps = ((0.0, base + content),)
            split_steps = ((0.0, base + content[:1]),) + tuple(
                (0.0, bytes([byte])) for byte in content[1:]
            )
        harness = _CaptureHarness()
        try:
            status, whole_payload, _wall = harness.post(
                steps=whole_steps, stream=stream, input_text=input_text,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200)
            self.assertEqual(whole_payload, content)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [answer])
            status, split_payload, _wall = harness.post(
                steps=split_steps, stream=stream, input_text=input_text,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200)
            self.assertEqual(split_payload, content)
            self.assertEqual(whole_payload, split_payload)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [answer])
        finally:
            harness.close()

    def test_split_utf8_close_identical(self) -> None:
        content = _sse_baseline_utf8(CLEAN_UNICODE)
        _assert_unicode_on_wire(content)
        self._split_identical(content, True, CLEAN, chunked=False, answer=CLEAN_UNICODE)

    def test_split_utf8_chunked_identical(self) -> None:
        content = _sse_baseline_utf8(CLEAN_UNICODE)
        _assert_unicode_on_wire(content)
        self._split_identical(content, True, CLEAN, chunked=True, answer=CLEAN_UNICODE)

    def test_split_crlf_delimiters_identical(self) -> None:
        content = _sse_baseline_utf8(CLEAN_UNICODE).replace(b"\n\n", b"\r\n\r\n")
        _assert_unicode_on_wire(content)
        self._split_identical(
            content, True, CLEAN, chunked=False, answer=CLEAN_UNICODE
        )

    def test_split_useful_repair_preserves_protection(self) -> None:
        review = _review_payload([_prop("t0"), _prop("t1")])
        for stream in (False, True):
            content = (
                _sse_baseline_utf8(USEFUL) if stream else _json_completed(USEFUL)
            )
            _assert_unicode_on_wire(content)
            base = self._sse_headers() if stream else self._json_headers()
            harness = _CaptureHarness()
            try:
                status, whole_payload, _wall = harness.post(
                    steps=((0.0, base + content),),
                    stream=stream, input_text=TEXT,
                    review=review,
                )
                self.assertEqual(status, 200, whole_payload)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                self.assertEqual(harness.engine_calls, [USEFUL])
                split_steps = ((0.0, base + content[:1]),) + tuple(
                    (0.0, bytes([byte])) for byte in content[1:]
                )
                status, split_payload, _wall = harness.post(
                    steps=split_steps, stream=stream, input_text=TEXT,
                    review=review,
                )
                self.assertEqual(status, 200, split_payload)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                self.assertEqual(harness.engine_calls, [USEFUL])
                self.assertEqual(whole_payload, split_payload)
                if stream:
                    final = [
                        json.loads(block[5:])
                        for block in split_payload.decode().split("\n\n")
                        if block.startswith("data:")
                    ]
                    completed = next(
                        e for e in final if e.get("type") == "response.completed"
                    )
                    text = completed["response"]["output"][0]["content"][0]["text"]
                    self.assertEqual(text, EXPECTED_USEFUL)
                else:
                    envelope = json.loads(split_payload.decode())
                    text = envelope["output"][0]["content"][0]["text"]
                    self.assertEqual(text, EXPECTED_USEFUL)
                self.assertIn(b"`presenetliv`", split_payload)
            finally:
                harness.close()

    def test_bad_utf8_502_zero_review(self) -> None:
        bad = _json_completed(CLEAN).replace(b"zapisano", b"\xffzapisano")
        declared = _with_content_length(self._json_headers(), len(bad))
        harness = _CaptureHarness()
        try:
            status, _payload, _wall = harness.post(
                steps=((0.0, declared + bad),),
                stream=False, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 502)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [])
        finally:
            harness.close()
        # Truncated final 4-byte code point at a known body end
        # (close-delimited SSE): an encoding failure, not mere
        # incompleteness.
        body = _sse_baseline_utf8(CLEAN_UNICODE)
        at = body.index("\U0001F600".encode())
        truncated = body[: at + 1]  # ends inside the emoji code point
        harness = _CaptureHarness()
        try:
            status, _payload, _wall = harness.post(
                steps=((0.0, self._sse_headers() + truncated),),
                stream=True, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 502)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [])
        finally:
            harness.close()

    def test_declared_tail_preserved(self) -> None:
        # Declared framing must deliver every advertised byte: the SSE
        # terminal marker never terminates a Content-Length body early.
        content = _sse_baseline_utf8(CLEAN) + b": preserved trailing comment\n\n"
        declared = _with_content_length(self._sse_headers(), len(content))
        harness = _CaptureHarness()
        try:
            status, payload, _wall = harness.post(
                steps=((0.0, declared + content),),
                stream=True, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, content)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [CLEAN])
        finally:
            harness.close()

    def test_keepalive_delayed_completion(self) -> None:
        content = _sse_baseline_utf8(CLEAN)
        harness = _CaptureHarness()
        try:
            started = time.monotonic()
            status, payload, _wall = harness.post(
                steps=((0.0, self._sse_headers() + content),),
                stream=True, input_text=CLEAN,
                review=_review_payload([_prop("t0")]),
                hold=1.2,
            )
            self.assertLess(time.monotonic() - started, 0.9)
            self.assertEqual(status, 200)
            self.assertEqual(payload, content)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(harness.engine_calls, [CLEAN])
        finally:
            harness.close()


def _run_child_bounded(
    script: str,
    args: list[str],
    *,
    deadline: float,
    env: dict[str, str],
) -> bytes:
    """Run an ordinary Python child in its own process group.

    The parent waits for one RESULT line under a finite deadline and
    always kills the process group and reaps the child, so no producer
    or reviewer thread or task outlives the test (order 017-a,
    acceptance 3).
    """
    child = subprocess.Popen(
        [sys.executable, "-B", "-c", script, *args],
        cwd=ROOT.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        start_new_session=True,
    )
    result_line: bytes | None = None
    try:
        assert child.stdout is not None
        fd = child.stdout.fileno()
        buffer = b""
        end = time.monotonic() + deadline
        while time.monotonic() < end:
            ready, _, _ = select.select([fd], [], [], 0.5)
            if ready:
                chunk = os.read(fd, 65536)
                if not chunk:
                    if child.poll() is not None:
                        break
                    continue
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if line.startswith(b"RESULT "):
                        result_line = line
            elif child.poll() is not None:
                break
            if result_line is not None:
                break
    finally:
        # Finite parent deadline with kill/reap/cleanup on every path:
        # the child runs in its own process group, so a hanging
        # producer thread cannot outlive the test.
        if child.poll() is None:
            try:
                os.killpg(os.getpgid(child.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                child.kill()
        child.wait(timeout=10)
        assert child.returncode is not None
        if child.stderr is not None:
            child.stderr.read()
        if child.stdout is not None:
            child.stdout.close()
    return result_line or b""


class HangingProducerTests(unittest.TestCase):
    """A hanging producer fails at the finite body budget with zero
    review and zero engine calls, and no child process or thread
    outlives the test (order 017-a, acceptance 3).

    The whole chain runs in an ordinary Python subprocess child with
    its own process group: real ConceptProxy (timeout 0.3) -> real
    RepairEngine (qualified Pandoc spec, real tiny SQLite index) ->
    real ResponsesReviewer, with a synthetic main upstream that sends
    one SSE event and then hangs without ever completing or closing.
    The parent enforces a finite deadline, kills the process group and
    reaps it on every path.
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


class _HangingMain(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    release = threading.Event()

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.wfile.write(
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/event-stream\r\n\r\n"
            b'data: {"type":"response.created"}\n\n'
        )
        self.wfile.flush()
        self.release.wait(30.0)  # hang: never completes, never closes

    def log_message(self, *_args):
        return


def main():
    temp = tempfile.TemporaryDirectory()
    db = Path(temp.name) / "hang.sqlite"
    _build_db(db)
    main_server = HTTPServer(("127.0.0.1", 0), _HangingMain)
    review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
    for server in (main_server, review_server):
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
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
        f"http://127.0.0.1:{main_server.server_port}",
        engine,
        timeout=0.3,
    )
    threading.Thread(target=proxy_server.serve_forever, daemon=True).start()
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
            "X-Concept-Request-ID": "req017a-hang",
        },
    )
    response = client.getresponse()
    payload = response.read()
    wall = time.monotonic() - started
    client.close()
    _HangingMain.release.set()
    for server in (proxy_server, main_server, review_server):
        server.shutdown()
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

    def test_hanging_producer_fails_at_budget_child_reaped(self) -> None:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        line = _run_child_bounded(
            self._CHILD, [str(ROOT.parent)], deadline=60.0, env=env
        )
        self.assertTrue(line.startswith(b"RESULT "), line[:200])
        result = json.loads(line[len(b"RESULT ") :].decode())
        self.assertEqual(result["status"], 502)
        self.assertGreaterEqual(result["wall"], 0.28)
        self.assertLessEqual(result["wall"], 1.8)
        self.assertEqual(result["review_calls"], 0)
        self.assertEqual(result["engine_calls"], 0)


class CaptureTlsTests(unittest.TestCase):
    temp: tempfile.TemporaryDirectory[str]
    cert: Path
    key: Path

    """Actual nonblocking TLS body capture over the real proxy chain.

    A subprocess child runs the full chain against a TLS main upstream
    using an owned ephemeral self-signed certificate trusted only
    inside that child via SSL_CERT_FILE.  Whole, split-3-byte and
    split-4-byte code points and a fragmented chunk-size line all
    succeed identically, so the nonblocking TLS readiness path (read
    and peek both surface SSLWantReadError as not-ready) is covered by
    a versioned regression and cannot be satisfied by HTTP-only tests.
    No private fixture paths are referenced.
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
from http.server import BaseHTTPRequestHandler, HTTPServer
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
from tests.test_responses_contract import _json_completed, _review_payload
from tests.test_runtime_corpus import _build_db
from tests.test_capture_transport import (
    CLEAN,
    CLEAN_UNICODE,
    _BUILD_UNIGRAM,
    _sse_baseline_utf8,
)

SSE = _sse_baseline_utf8(CLEAN_UNICODE)
JSON = _json_completed(CLEAN_UNICODE)
for marker in ("\u00e9", "\u20ac", "\U0001F600"):
    assert marker.encode() in SSE and marker.encode() in JSON

SSE_HEADERS = b"HTTP/1.1 200 OK\r\nContent-Type: text/event-stream\r\n\r\n"
JSON_HEADERS = (
    b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
)


def with_length(headers, length):
    return headers[: -len(b"\r\n")] + f"Content-Length: {length}\r\n\r\n".encode()


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
    db = Path(temp.name) / "tls.sqlite"
    _build_db(db, unigram=_BUILD_UNIGRAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(str(cert), str(key))
    main_server = HTTPServer(("127.0.0.1", 0), _TlsMain)
    main_server.socket = context.wrap_socket(main_server.socket, server_side=True)
    review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
    for server in (main_server, review_server):
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
    reviewer = ResponsesReviewer(
        f"http://127.0.0.1:{review_server.server_port}/v1",
        "test-model",
        timeout=5.0,
        api_key="fake-review-key",
    )
    engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
    proxy_server = proxy.ConceptProxy(
        ("127.0.0.1", 0),
        f"https://127.0.0.1:{main_server.server_port}",
        engine,
        timeout=5.0,
    )
    threading.Thread(target=proxy_server.serve_forever, daemon=True).start()

    def post(steps, stream):
        _TlsMain.steps = steps
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.recorded = []
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
                "X-Concept-Request-ID": "req017a-tls",
            },
        )
        response = client.getresponse()
        payload = response.read()
        client.close()
        return response.status, payload

    cases = {}
    # (a) whole declared-length SSE control over TLS.
    status, payload = post(
        ((0.0, with_length(SSE_HEADERS, len(SSE)) + SSE),), True
    )
    cases["whole_length_sse"] = (
        status == 200 and payload == SSE and not _FakeUpstream.recorded
    )
    # (b) 3-byte euro sign split across the wire with TLS delays.
    at = SSE.index("\u20ac".encode())
    status, payload = post(
        (
            (0.0, SSE_HEADERS + SSE[: at + 1]),
            (0.05, SSE[at + 1 : at + 2]),
            (0.05, SSE[at + 2 :]),
        ),
        True,
    )
    cases["split_three_byte_sse"] = (
        status == 200 and payload == SSE and not _FakeUpstream.recorded
    )
    # (c) 4-byte emoji split across the wire with TLS delays.
    at = SSE.index("\U0001F600".encode())
    status, payload = post(
        (
            (0.0, SSE_HEADERS + SSE[: at + 1]),
            (0.05, SSE[at + 1 : at + 2]),
            (0.05, SSE[at + 2 :]),
        ),
        True,
    )
    cases["split_four_byte_sse"] = (
        status == 200 and payload == SSE and not _FakeUpstream.recorded
    )
    # (d) chunked JSON with a byte-by-byte fragmented chunk-size line.
    size_line = format(len(JSON), "x").encode() + b"\r\n"
    ending = b"\r\n0\r\n\r\n"
    chunked_headers = (
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
        b"Transfer-Encoding: chunked\r\n\r\n"
    )
    status, payload = post(
        (
            (0.0, chunked_headers + size_line[:1]),
            (0.05, size_line[1:2]),
            (0.05, size_line[2:] + JSON),
            (0.0, ending),
        ),
        False,
    )
    cases["fragmented_chunk_size_json"] = (
        status == 200 and payload == JSON and not _FakeUpstream.recorded
    )
    for server in (proxy_server, main_server, review_server):
        server.shutdown()
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

    def test_tls_capture_matrix(self) -> None:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        line = _run_child_bounded(
            self._CHILD,
            [str(ROOT.parent), str(self.cert), str(self.key)],
            deadline=90.0,
            env=env,
        )
        self.assertTrue(line.startswith(b"RESULT "), line[:200])
        result = json.loads(line[len(b"RESULT ") :].decode())
        for name in (
            "whole_length_sse",
            "split_three_byte_sse",
            "split_four_byte_sse",
            "fragmented_chunk_size_json",
        ):
            self.assertTrue(result["cases"][name], result)
