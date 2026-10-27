"""Order 019-a: one owned elapsed reviewer exchange budget.

Proves, with real subprocesses and loopback wire traffic only, that
``review_batch`` runs the whole batch-review exchange under one finite
positive monotonic deadline anchored at entry: process startup, IPC,
and the owned child's actual resolver/connect/TLS/upload/status/
header/body work, plus result transfer and parent validation.  A late
or racing success is a failure, the exact child is terminated and
actually reaped before return, the IPC channel is strictly versioned
and capped, the child environment carries only explicit TLS trust
references, and the legacy protected source sections remain
byte-identical to the trusted accepted base.
"""

from __future__ import annotations

import ast
import contextlib
import fcntl
import hashlib
import http.client
import json
import os
import shutil
import socket
import ssl
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from pathlib import Path
from typing import Any, cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import qwen_client  # noqa: E402
import review_transport as rt  # noqa: E402
from batch_review import (  # noqa: E402
    REASON_HTTP_FAILED,
    REASON_HTTP_NOT_OK,
    REASON_INVALID_ENCODING,
    REASON_MISSING_ID,
    BatchTarget,
    build_prompt,
    build_request_body,
    prepare_targets,
)
from config import (  # noqa: E402
    REVIEW_BATCH_MAX_REQUEST_BYTES,
    REVIEWER_HTTP_TIMEOUT_SECONDS,
)
from qwen_client import ResponsesReviewer, ReviewerError  # noqa: E402
from tests.test_capture_transport import (  # noqa: E402
    _BUILD_UNIGRAM,
    CLEAN,
    USEFUL,
    _sse_baseline_utf8,
)
from tests.test_responses_contract import (  # noqa: E402
    _json_completed,
    _review_payload,
)
from tests.test_review_batch import (  # noqa: E402
    TEXT,
    _build_corpus,
    _contract_body,
    _envelope,
    _FakeUpstream,
    _occurrences,
    _prop,
    _real_spec,
    _valid_inner,
)
from tests.test_runtime_corpus import _build_db  # noqa: E402

WORKER_PATH = ROOT / "review_worker.py"
TARGETS: tuple[BatchTarget, ...] = prepare_targets(TEXT, _occurrences(TEXT), ()) or ()

# Trusted accepted-base section constants (order 019-a, "Exact legacy
# source preservation"); recomputed from the actual candidate bytes.
_PROTECTED_SECTIONS: dict[str, tuple[str, int]] = {
    "Proposal": (
        "fb3e78e9a6b18ea2590b2e92cc93823b9306679eb7da29a77d62598264257d34",
        110,
    ),
    "responses_path": (
        "c107eefb7a4a5d94af755609f098a74c4028e34bdef825da83d6ea805a9fb096",
        226,
    ),
    "parse_proposal": (
        "aa4fa3fb35ff4043ee413878aa2fab7e2839c35c76b226963afb6f996ac21597",
        2061,
    ),
    "prompt": (
        "c9b63a680630b7ef82d62c458620b07063e3bb4354d09a9ff5c7b0674a68bad5",
        669,
    ),
    "ResponsesReviewer.review": (
        "40c10409fc4e2e7726500c4c5a85233ebf3ebfe80ca5c1404109d1144e8b5c72",
        1713,
    ),
}


def _fake_worker_script(body_statements: str) -> str:
    """One owned fake-worker source: pure stdlib, no imports of the
    product, executed by the real parent through the real argv."""
    return (
        "import os\n"
        "import sys\n"
        "data = b''\n"
        "while True:\n"
        "    chunk = os.read(0, 65536)\n"
        "    if not chunk:\n"
        "        break\n"
        "    data += chunk\n"
        + body_statements
    )


def _write_worker(path: Path, source: str) -> Path:
    path.write_text(source)
    return path


class FrameCodecTests(unittest.TestCase):
    def _request_frame(
        self,
        *,
        scheme: str = "http",
        host: str = "127.0.0.1",
        port: int | None = None,
        path: str = "/v1/responses",
        auth: str | None = "k",
        remaining: float = 1.0,
        body: bytes = b"{}",
    ) -> bytes:
        return rt.encode_request_frame(
            scheme=scheme,
            host=host,
            port=port,
            path=path,
            auth=auth,
            remaining_seconds=remaining,
            body=body,
        )

    def test_request_round_trip_fields(self) -> None:
        for scheme in ("http", "https"):
            for port in (None, 1, 65535):
                for auth in (None, "tok-123"):
                    with self.subTest(scheme=scheme, port=port, auth=auth):
                        encoded = self._request_frame(
                            scheme=scheme, port=port, auth=auth,
                            body=b"x" * 100,
                        )
                        (declared,) = rt._FRAME_PREFIX.unpack(encoded[:8])
                        decoded = rt.decode_request_frame(encoded[8 : 8 + declared])
                        self.assertEqual(decoded.scheme, scheme)
                        self.assertEqual(decoded.port, port)
                        self.assertEqual(decoded.auth, auth)
                        self.assertEqual(decoded.path, "/v1/responses")
                        self.assertEqual(decoded.body, b"x" * 100)
                        self.assertTrue(decoded.remaining_seconds > 0)

    def test_request_port_semantics(self) -> None:
        # Explicit 0 is rejected, never aliased to the default.
        with self.assertRaises(rt.FrameMalformed):
            self._request_frame(port=0)
        # None encodes the default-port alias; decode restores None.
        decoded = rt.decode_request_frame(self._request_frame(port=None)[8:])
        self.assertIsNone(decoded.port)
        # Full 16-bit meaning otherwise.
        decoded = rt.decode_request_frame(self._request_frame(port=65535)[8:])
        self.assertEqual(decoded.port, 65535)
        for bad in (65536, -1, True, "80"):
            with self.assertRaises(rt.FrameMalformed):
                self._request_frame(port=cast(int, bad))

    def test_request_encode_rejects_bad_fields(self) -> None:
        cases = {
            "scheme": dict(scheme="ftp"),
            "host_oversize": dict(host="h" * 256),
            "path_oversize": dict(path="p" * 2049),
            "auth_oversize": dict(auth="a" * 4097),
            "body_oversize": dict(body=b"b" * (REVIEW_BATCH_MAX_REQUEST_BYTES + 1)),
            "remaining_zero": dict(remaining=0.0),
            "remaining_negative": dict(remaining=-1.0),
            "remaining_nan": dict(remaining=float("nan")),
            "remaining_inf": dict(remaining=float("inf")),
        }
        for name, kwargs in cases.items():
            with self.subTest(case=name), self.assertRaises(rt.FrameMalformed):
                self._request_frame(**kwargs)  # type: ignore[arg-type]

    def test_request_decode_rejects_wire_deviations(self) -> None:
        good = self._request_frame()
        frame = good[8:]
        mutations: dict[str, bytes] = {}

        def mutate(label: str, data: bytes) -> None:
            mutations[label] = data

        head = bytearray(frame)
        head[0:4] = b"XXXX"
        mutate("magic", bytes(head))
        head = bytearray(frame)
        head[4] = 99
        mutate("version", bytes(head))
        head = bytearray(frame)
        head[5] = 7
        mutate("kind", bytes(head))
        mutate("truncated", frame[: len(frame) - 1])
        mutate("extra_byte", frame + b"\x00")
        # Length-inconsistent: header claims one more byte of body.
        head = bytearray(frame)
        struct.pack_into(
            ">I", head, rt._REQUEST_HEADER.size - 4, rt._REQUEST_HEADER.unpack_from(frame, 0)[9] + 1
        )
        mutate("body_len_mismatch", bytes(head))
        # Non-UTF-8 host: rebuild with a one-byte host of 0xFF.
        rebuilt = rt._REQUEST_HEADER.pack(
            rt._MAGIC,
            rt.REVIEW_TRANSPORT_VERSION,
            rt._KIND_REQUEST,
            rt._SCHEME_HTTP,
            0,
            1,
            len(b"/v1/responses"),
            0,
            1.0,
            len(b"{}"),
        ) + b"\xff" + b"/v1/responses" + b"{}"
        mutate("host_not_utf8", rebuilt)
        # Nonpositive remaining on the wire.
        fields = list(rt._REQUEST_HEADER.unpack_from(frame, 0))
        fields[8] = 0.0
        mutate(
            "remaining_zero_wire",
            rt._REQUEST_HEADER.pack(*fields) + frame[rt._REQUEST_HEADER.size :],
        )
        for name, data in mutations.items():
            with self.subTest(case=name), self.assertRaises(rt.FrameMalformed):
                rt.decode_request_frame(data)
        with self.assertRaises(rt.FrameMalformed):
            rt.decode_request_frame(b"x" * (rt.REQUEST_FRAME_MAX_BYTES + 1))

    def test_request_decode_enforces_body_cap_despite_total(self) -> None:
        # The per-field body cap is enforced at decode time: a
        # consistent frame whose body alone exceeds _BODY_MAX_BYTES
        # (whole-frame total still below the frame cap) must be
        # rejected, and the exact cap is the boundary (order 019-a,
        # requirement 3).
        def raw(body: bytes) -> bytes:
            return rt._REQUEST_HEADER.pack(
                rt._MAGIC,
                rt.REVIEW_TRANSPORT_VERSION,
                rt._KIND_REQUEST,
                rt._SCHEME_HTTP,
                0,
                len(b"h"),
                len(b"/p"),
                0,
                1.0,
                len(body),
            ) + b"h" + b"/p" + body

        over = raw(b"x" * (rt._BODY_MAX_BYTES + 1))
        assert len(over) < rt.REQUEST_FRAME_MAX_BYTES
        with self.assertRaises(rt.FrameMalformed):
            rt.decode_request_frame(over)
        at_cap = b"x" * rt._BODY_MAX_BYTES
        request = rt.decode_request_frame(raw(at_cap))
        self.assertEqual(len(request.body), rt._BODY_MAX_BYTES)
        self.assertEqual(request.body, at_cap)

    def test_response_round_trip_and_failure_normalization(self) -> None:
        for payload in (b"", b'{"ok": true}'):
            for status in (0, 200, 599):
                with self.subTest(payload=payload[:12], status=status):
                    encoded = rt.encode_response_frame(
                        ok=True, http_status=status, payload=payload
                    )
                    (declared,) = rt._FRAME_PREFIX.unpack(encoded[:8])
                    decoded = rt.decode_response_frame(encoded[8 : 8 + declared])
                    self.assertTrue(decoded.ok)
                    self.assertEqual(decoded.http_status, status)
                    self.assertEqual(decoded.payload, payload)
        encoded = rt.encode_response_frame(ok=False, http_status=500, payload=b"junk")
        (declared,) = rt._FRAME_PREFIX.unpack(encoded[:8])
        decoded = rt.decode_response_frame(encoded[8 : 8 + declared])
        self.assertFalse(decoded.ok)
        self.assertEqual(decoded.http_status, 0)
        self.assertEqual(decoded.payload, b"")

    def test_response_encode_rejects_bad_fields(self) -> None:
        with self.assertRaises(rt.FrameMalformed):
            rt.encode_response_frame(
                ok=True, http_status=200,
                payload=b"p" * (rt._PAYLOAD_MAX_BYTES + 2),
            )
        for bad in (-1, 65536):
            with self.assertRaises(rt.FrameMalformed):
                rt.encode_response_frame(ok=True, http_status=bad, payload=b"")

    def test_response_decode_rejects_wire_deviations(self) -> None:
        good = rt.encode_response_frame(ok=True, http_status=200, payload=b"ok")
        frame = good[8:]
        head = bytearray(frame)
        head[0:4] = b"YYYY"
        with self.assertRaises(rt.FrameMalformed):
            rt.decode_response_frame(bytes(head))
        head = bytearray(frame)
        head[5] = 9
        with self.assertRaises(rt.FrameMalformed):
            rt.decode_response_frame(bytes(head))
        head = bytearray(frame)
        head[6] = 9
        with self.assertRaises(rt.FrameMalformed):
            rt.decode_response_frame(bytes(head))
        with self.assertRaises(rt.FrameMalformed):
            rt.decode_response_frame(frame[:-1])
        with self.assertRaises(rt.FrameMalformed):
            rt.decode_response_frame(frame + b"Z")
        with self.assertRaises(rt.FrameMalformed):
            rt.decode_response_frame(
                b"x" * (rt.RESPONSE_FRAME_MAX_BYTES + 1)
            )


class _RecordingMain(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    payload: bytes = b'{"ok": true}'
    requests: list[dict[str, object]] = []

    def do_POST(self) -> None:  # noqa: N802
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.__class__.requests.append(
            {"path": self.path, "body": body, "auth": self.headers.get("Authorization")}
        )
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(self.__class__.payload)))
        self.end_headers()
        self.wfile.write(self.__class__.payload)

    def log_message(self, *_args: object) -> None:
        return


def _tracked_popen(observed: list[subprocess.Popen[bytes]]) -> Any:
    """Patch subprocess.Popen with a transparent forwarding wrapper
    that preserves the real spawn unchanged and records the actual
    Popen objects the product creates (original captured before the
    patch).  The product reaps its children itself; tests observe
    ``returncode`` on these owned objects without any test-side
    poll/wait that could secretly reap and mask a leak."""
    real_popen = subprocess.Popen

    def spy_popen(*args: Any, **kwargs: Any) -> subprocess.Popen[bytes]:
        proc: subprocess.Popen[bytes] = real_popen(*args, **kwargs)
        observed.append(proc)
        return proc

    return mock.patch.object(subprocess, "Popen", spy_popen)

class _WorkerBase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.workers: list[Path] = []
        self.server: ThreadingHTTPServer | None = None
        self.thread: threading.Thread | None = None

    def tearDown(self) -> None:
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
        if self.thread is not None:
            self.thread.join(5)
            self.assertFalse(self.thread.is_alive())
        for worker in self.workers:
            with contextlib.suppress(OSError):
                worker.unlink()
        self.temp.cleanup()

    def _write(self, source: str) -> Path:
        path = Path(self.temp.name) / f"fake_worker_{len(self.workers)}.py"
        self.workers.append(path)
        return _write_worker(path, source)

    def _start_upstream(self, payload: bytes = b'{"ok": true}') -> int:
        _RecordingMain.payload = payload
        _RecordingMain.requests = []
        assert self.server is None
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _RecordingMain)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self.server.server_address[1]

    def _exchange(
        self,
        worker: Path,
        *,
        port: int,
        budget: float,
        body: bytes = b"x",
        auth: str | None = "k",
    ) -> tuple[int, bytes]:
        return rt.run_review_exchange(
            scheme="http",
            host="127.0.0.1",
            port=port,
            path="/v1/responses",
            body=body,
            auth=auth,
            deadline=time.monotonic() + budget,
            worker_path=worker,
        )

    def _run_worker_direct(self, worker: Path, stdin_bytes: bytes) -> tuple[int, bytes, bytes]:
        """Run the exact product argv; the owned child is always
        killed and reaped on timeout or failure."""
        proc = subprocess.Popen(
            [sys.executable, "-I", "-S", "-B", str(worker)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            out, err = proc.communicate(stdin_bytes, timeout=15)
            self.assertIsNotNone(proc.poll())
            return proc.returncode, out, err
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate(timeout=10)
            self.assertIsNotNone(proc.poll())
            raise


# Inline (no product import) response-frame writer for owned fake workers.
_FAKE_RESPONSE = (
    "frame = b'RRTX' + struct.pack('>BBBHI', 1, 2, {status_byte}, {http_status},"
    " len(payload)) + payload\n"
    "sys.stdout.buffer.write(struct.pack('>Q', len(frame)) + frame)\n"
    "sys.stdout.buffer.flush()\n"
    "sys.exit({exit_code})\n"
)


class WorkerSubprocessTests(_WorkerBase):
    """Owned-child boundaries over the exact product argv.

    The real-worker cases prove the actual worker/HTTP transport; the
    fake-worker cases (owned temp scripts driven by the real parent
    controller) cover IPC-fault injection only and are labelled as
    controlled orchestration, never as real transport success."""

    def test_real_worker_success_exit_zero_silent_stderr(self) -> None:
        port = self._start_upstream()
        frame = rt.encode_request_frame(
            scheme="http", host="127.0.0.1", port=port, path="/v1/responses",
            auth="k", remaining_seconds=5.0, body=b"hello",
        )
        code, out, err = self._run_worker_direct(WORKER_PATH, frame)
        self.assertEqual(code, 0, f"stderr={err!r}")
        self.assertEqual(err, b"")
        (declared,) = rt._FRAME_PREFIX.unpack(out[:8])
        self.assertEqual(len(out), 8 + declared)
        response = rt.decode_response_frame(out[8 : 8 + declared])
        self.assertTrue(response.ok)
        self.assertEqual(response.http_status, 200)
        self.assertEqual(response.payload, b'{"ok": true}')
        self.assertEqual(len(_RecordingMain.requests), 1)
        self.assertEqual(_RecordingMain.requests[0]["path"], "/v1/responses")
        self.assertEqual(_RecordingMain.requests[0]["body"], b"hello")
        self.assertEqual(_RecordingMain.requests[0]["auth"], "Bearer k")

    def test_real_worker_bad_request_frame_exit_nonzero_no_http(self) -> None:
        port = self._start_upstream()
        frame = rt.encode_request_frame(
            scheme="http", host="127.0.0.1", port=port, path="/p",
            auth=None, remaining_seconds=5.0, body=b"{}",
        )
        bad = b"NOPE" + frame[4:]
        code, _out, _err = self._run_worker_direct(WORKER_PATH, bad)
        self.assertNotEqual(code, 0)
        self.assertEqual(_RecordingMain.requests, [])

    def test_real_worker_trailing_stdin_byte_rejected_before_http(self) -> None:
        port = self._start_upstream()
        frame = rt.encode_request_frame(
            scheme="http", host="127.0.0.1", port=port, path="/p",
            auth=None, remaining_seconds=5.0, body=b"{}",
        )
        code, _out, _err = self._run_worker_direct(WORKER_PATH, frame + b"X")
        self.assertNotEqual(code, 0)
        self.assertEqual(_RecordingMain.requests, [])

    def test_real_worker_late_stdin_byte_held_pipe_rejected(self) -> None:
        # The pipe stays open after the frame: the worker must not start
        # HTTP before the channel's actual EOF, and a late byte still
        # rejects (order 019-a, requirement 3).
        port = self._start_upstream()
        frame = rt.encode_request_frame(
            scheme="http", host="127.0.0.1", port=port, path="/p",
            auth=None, remaining_seconds=5.0, body=b"{}",
        )
        proc = subprocess.Popen(
            [sys.executable, "-I", "-S", "-B", str(WORKER_PATH)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            assert proc.stdin is not None
            proc.stdin.write(frame)
            proc.stdin.flush()
            time.sleep(1.0)
            self.assertEqual(_RecordingMain.requests, [], "HTTP began before channel EOF")
            proc.stdin.write(b"X")
            proc.stdin.close()
            proc.stdin = None
            out, err = proc.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate(timeout=10)
            self.fail("owned worker child did not exit after the late byte")
        self.assertIsNotNone(proc.poll())
        self.assertNotEqual(proc.returncode, 0, f"out={out!r} err={err!r}")
        self.assertEqual(_RecordingMain.requests, [])

    def test_hanging_fake_worker_terminated_and_reaped(self) -> None:
        worker = self._write(_fake_worker_script("import time\ntime.sleep(30)\n"))
        observed: list[subprocess.Popen[bytes]] = []
        started = time.monotonic()
        with _tracked_popen(observed), self.assertRaises(rt.ReviewTransportError) as caught:
            self._exchange(worker, port=1, budget=0.6)
        wall = time.monotonic() - started
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        self.assertLess(wall, 2.5, f"wall={wall:.2f}")
        # The product reaped the exact owned child (no test-side wait).
        self.assertEqual(len(observed), 1)
        self.assertIsNotNone(observed[0].returncode)

    def test_late_success_frame_not_transferred(self) -> None:
        # A real, valid success frame that only exists after the deadline
        # is never salvaged (order 019-a, requirement 1).
        port = self._start_upstream()
        worker = self._write(
            _fake_worker_script(
                "import time\n"
                "time.sleep(0.9)\n"
                "import struct\n"
                'payload = b\'{"ok": true}\'\n'
                + _FAKE_RESPONSE.format(status_byte=0, http_status=200, exit_code=0)
            )
        )
        started = time.monotonic()
        observed: list[subprocess.Popen[bytes]] = []
        with _tracked_popen(observed), self.assertRaises(
            rt.ReviewTransportError
        ) as caught:
            self._exchange(worker, port=port, budget=0.5)
        wall = time.monotonic() - started
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        self.assertLess(wall, 2.5, f"wall={wall:.2f}")
        # The product reaped the exact owned child (no test-side wait).
        self.assertEqual(len(observed), 1)
        self.assertIsNotNone(observed[0].returncode)

    def test_fake_worker_malformed_reply_rejected(self) -> None:
        worker = self._write(_fake_worker_script(
            "sys.stdout.buffer.write(b'garbage-garbage-garbage')\n"
            "sys.stdout.buffer.flush()\n"
            "sys.exit(0)\n"
        ))
        with self.assertRaises(rt.ReviewTransportError) as caught:
            self._exchange(worker, port=1, budget=2.0)
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)

    def test_fake_worker_oversized_reply_rejected(self) -> None:
        worker = self._write(_fake_worker_script(
            "import struct\n"
            f"payload = b'x' * {rt._PAYLOAD_MAX_BYTES + 2}\n"
            + _FAKE_RESPONSE.format(status_byte=0, http_status=200, exit_code=0)
        ))
        with self.assertRaises(rt.ReviewTransportError) as caught:
            self._exchange(worker, port=1, budget=2.0)
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)

    def test_fake_worker_extra_frame_rejected(self) -> None:
        worker = self._write(_fake_worker_script(
            "import struct\n"
            'payload = b\'{"ok": true}\'\n'
            "frame = b'RRTX' + struct.pack('>BBBHI', 1, 2, 0, 200, len(payload)) + payload\n"
            "sys.stdout.buffer.write(struct.pack('>Q', len(frame)) + frame)\n"
            "sys.stdout.buffer.write(struct.pack('>Q', len(frame)) + frame)\n"
            "sys.stdout.buffer.flush()\n"
            "sys.exit(0)\n"
        ))
        with self.assertRaises(rt.ReviewTransportError) as caught:
            self._exchange(worker, port=1, budget=2.0)
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)

    def test_fake_worker_nonzero_exit_rejected(self) -> None:
        worker = self._write(_fake_worker_script(
            "import struct\n"
            'payload = b\'{"ok": true}\'\n'
            + _FAKE_RESPONSE.format(status_byte=0, http_status=200, exit_code=7)
        ))
        with self.assertRaises(rt.ReviewTransportError) as caught:
            self._exchange(worker, port=1, budget=2.0)
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)

    def test_child_environment_carries_only_tls_refs(self) -> None:
        worker = self._write(_fake_worker_script(
            "import json, struct\n"
            "with open('/proc/self/cmdline', 'rb') as handle:\n"
            "    raw = handle.read()\n"
            "cmdline = [part.decode() for part in raw.split(b'\\0') if part]\n"
            "payload = json.dumps({'env': dict(os.environ), 'cmdline': cmdline}).encode()\n"
            + _FAKE_RESPONSE.format(status_byte=0, http_status=200, exit_code=0)
        ))
        port = self._start_upstream()
        polluted = {
            "QWEN_API_KEY": "must-not-leak",
            "CONCEPT_TIMEOUT": "999",
            "CONCEPT_REVIEWER_URL": "http://127.0.0.1:9/v1",
            "HOME": "/tmp/fake-home",
            "SSL_CERT_FILE": "/tmp/ca.pem",
        }
        with mock.patch.dict(os.environ, polluted):
            status, payload = self._exchange(worker, port=port, budget=3.0)
        self.assertEqual(status, 200)
        dump = json.loads(payload)
        env = cast(dict[str, str], dump["env"])
        # Only the explicit TLS trust reference is forwarded; the sole
        # other entry is CPython's own interpreter-startup default
        # (verified against a clean -I -S -B child), never an operator
        # or credential field.
        self.assertTrue(set(env) <= {"SSL_CERT_FILE", "SSL_CERT_DIR", "LC_CTYPE"}, env)
        self.assertEqual(env.get("SSL_CERT_FILE"), "/tmp/ca.pem")
        for key in ("QWEN_API_KEY", "CONCEPT_TIMEOUT", "CONCEPT_REVIEWER_URL",
                    "CONCEPT_REVIEWER_PROFILE", "HOME", "PATH"):
            self.assertNotIn(key, env, f"{key} leaked into the child environment")
        # The exact product argv at execve (order 019-a, requirement 2):
        # running interpreter, isolated/minimal/no-bytecode flags, the
        # versioned worker - nothing else, so no credential or body in
        # argv.
        cmdline = cast(list[str], dump["cmdline"])
        self.assertEqual(cmdline, [sys.executable, "-I", "-S", "-B", str(worker)])
        self.assertNotIn("must-not-leak", json.dumps(dump))

    def test_child_stderr_silenced_frame_intact(self) -> None:
        worker = self._write(_fake_worker_script(
            "os.write(2, b'SECRET-STDERR-TEXT')\n"
            "import struct\n"
            'payload = b\'{"ok": true}\'\n'
            + _FAKE_RESPONSE.format(status_byte=0, http_status=200, exit_code=0)
        ))
        port = self._start_upstream()
        status, payload = self._exchange(worker, port=port, budget=3.0)
        self.assertEqual(status, 200)
        self.assertEqual(payload, b'{"ok": true}')


class SmallPipeTests(_WorkerBase):
    """A shrunken (4096-byte) real pipe: governed partial writes/reads."""

    def _shrunken_pipe(self) -> Callable[[], tuple[int, int]]:
        real_pipe = os.pipe

        def factory() -> tuple[int, int]:
            read_fd, write_fd = real_pipe()
            fcntl.fcntl(read_fd, fcntl.F_SETPIPE_SZ, 4096)
            fcntl.fcntl(write_fd, fcntl.F_SETPIPE_SZ, 4096)
            return read_fd, write_fd

        return factory

    def test_small_pipe_positive_real_child_full_body(self) -> None:
        port = self._start_upstream()
        body = b"x" * REVIEW_BATCH_MAX_REQUEST_BYTES
        with mock.patch.object(os, "pipe", self._shrunken_pipe()):
            status, payload = self._exchange(
                WORKER_PATH, port=port, budget=10.0, body=body
            )
        self.assertEqual(status, 200)
        self.assertEqual(payload, b'{"ok": true}')
        self.assertEqual(len(_RecordingMain.requests), 1)
        self.assertEqual(_RecordingMain.requests[0]["body"], body)

    def test_small_pipe_stalled_reader_bounded_deadline(self) -> None:
        # A read end that stays open without consuming: the governed
        # partial write must hit the deadline, never a parent-hung block.
        worker = self._write(_fake_worker_script("import time\ntime.sleep(30)\n"))
        body = b"x" * REVIEW_BATCH_MAX_REQUEST_BYTES
        observed: list[subprocess.Popen[bytes]] = []
        started = time.monotonic()
        with (
            mock.patch.object(os, "pipe", self._shrunken_pipe()),
            _tracked_popen(observed),
            self.assertRaises(rt.ReviewTransportError) as caught,
        ):
            self._exchange(worker, port=1, budget=0.3, body=body)
        wall = time.monotonic() - started
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        self.assertLess(wall, 1.5, f"wall={wall:.2f}")
        # The product reaped the exact owned child (no test-side wait).
        self.assertEqual(len(observed), 1)
        self.assertIsNotNone(observed[0].returncode)


class _ScriptedHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    status: int = 200
    payload: bytes = b"{}"
    pre_status_delay: float = 0.0
    pre_body_delay: float = 0.0
    interim_100: bool = False
    close_after: bool = False
    chunked: bool = False
    split_bytes: int = 0
    extra_bytes: bytes = b""
    requests: list[dict[str, object]] = []

    def do_POST(self) -> None:  # noqa: N802
        cls = self.__class__
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        cls.requests.append(
            {
                "path": self.path,
                "body": body,
                "auth": self.headers.get("Authorization"),
                "ctype": self.headers.get("Content-Type"),
            }
        )
        if cls.pre_status_delay:
            time.sleep(cls.pre_status_delay)
        if cls.interim_100:
            self.wfile.write(b"HTTP/1.1 100 Continue\r\n\r\n")
            self.wfile.flush()
        if cls.pre_body_delay:
            time.sleep(cls.pre_body_delay)
        if cls.chunked:
            self.send_response(self.status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            chunk = cls.payload
            self.wfile.write(f"{len(chunk):x}\r\n".encode() + chunk + b"\r\n")
            self.wfile.write(b"0\r\n\r\n")
        else:
            self.send_response(self.status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(cls.payload)))
            if cls.close_after:
                self.send_header("Connection", "close")
                self.close_connection = True
            self.end_headers()
            if cls.split_bytes:
                for index in range(0, len(cls.payload), cls.split_bytes):
                    self.wfile.write(cls.payload[index : index + cls.split_bytes])
                    self.wfile.flush()
                    time.sleep(0.01)
            else:
                self.wfile.write(cls.payload)
        if cls.extra_bytes:
            self.wfile.write(cls.extra_bytes)
            self.wfile.flush()

    def log_message(self, *_args: object) -> None:
        return


class _DripHandler(BaseHTTPRequestHandler):
    """Actual wire drips: bytes arrive in small fragments with
    inter-fragment gaps far below a per-read inactivity timeout, so
    cumulative elapsed time - not byte arrival - is what the anchored
    whole-exchange deadline must catch (order 019-a, requirement 7).
    Observed fragment timestamps make the phase times evidence rather
    than inferred sleeps."""

    protocol_version = "HTTP/1.1"
    mode: str = "status"  # status | headers | body | interim | cumulative
    gap: float = 0.03
    payload: bytes = b"{}"
    body_frag: int = 2
    header_marks: int = 0
    completed: threading.Event = threading.Event()
    requests: list[dict[str, object]] = []
    marks: list[float] = []
    header_done_at: float | None = None
    body_done_at: float | None = None

    def _drip(self, data: bytes, frag: int = 2) -> None:
        cls = self.__class__
        for index in range(0, len(data), frag):
            self.wfile.write(data[index : index + frag])
            self.wfile.flush()
            cls.marks.append(time.monotonic())
            time.sleep(cls.gap)

    def do_POST(self) -> None:  # noqa: N802
        cls = self.__class__
        cls.marks = []
        cls.header_done_at = None
        cls.body_done_at = None
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        cls.requests.append({"path": self.path, "body": body, "started": time.monotonic()})
        if cls.mode == "status":
            # The status line itself drips (no byte arrives before the
            # status line completes).
            self._drip(
                b"HTTP/1.1 200 OK\r\nContent-Type: application/json"
                + f"\r\nContent-Length: {len(cls.payload)}\r\n\r\n".encode()
                + cls.payload
            )
        elif cls.mode == "headers":
            self.wfile.write(b"HTTP/1.1 200 OK\r\n")
            self.wfile.flush()
            self._drip(b"Content-Type: application/json\r\nContent-Length: 2\r\n\r\n")
            cls.header_done_at = time.monotonic()
            self.wfile.write(b"{}")
        elif cls.mode == "body":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(cls.payload)))
            self.end_headers()
            cls.header_done_at = time.monotonic()
            self._drip(cls.payload)
            cls.body_done_at = time.monotonic()
        elif cls.mode == "interim":
            # Interim 100, dripped, then the final status drips: the 100
            # must not reset the anchored deadline.
            self._drip(b"HTTP/1.1 100 Continue\r\n\r\n")
            self._drip(
                b"HTTP/1.1 200 OK\r\nContent-Type: application/json"
                + f"\r\nContent-Length: {len(cls.payload)}\r\n\r\n".encode()
                + cls.payload
            )
        elif cls.mode == "cumulative":
            # A finite producer: the header phase drips in 3-byte
            # fragments, the body phase in body_frag-byte fragments;
            # both phases complete, each below the short budget,
            # jointly over it (order 019-a, requirement 7).
            self.wfile.write(b"HTTP/1.1 200 OK\r\n")
            self.wfile.flush()
            self._drip(
                b"Content-Type: application/json"
                + f"\r\nContent-Length: {len(cls.payload)}\r\n\r\n".encode(),
                frag=3,
            )
            cls.header_done_at = time.monotonic()
            cls.header_marks = len(cls.marks)
            self._drip(cls.payload, frag=cls.body_frag)
            cls.body_done_at = time.monotonic()
        else:  # pragma: no cover - test fixture invariant
            raise AssertionError(cls.mode)
        # Bounded actual producer completion: set after every byte and
        # every bookkeeping stamp is done (the trailing drip sleep runs
        # after the last byte, so the client may legitimately finish
        # the transport before the handler's final stamp).
        cls.completed.set()

    def log_message(self, *_args: object) -> None:
        return


def _reset_scripted() -> None:
    _ScriptedHandler.status = 200
    _ScriptedHandler.payload = b"{}"
    _ScriptedHandler.pre_status_delay = 0.0
    _ScriptedHandler.pre_body_delay = 0.0
    _ScriptedHandler.interim_100 = False
    _ScriptedHandler.close_after = False
    _ScriptedHandler.chunked = False
    _ScriptedHandler.split_bytes = 0
    _ScriptedHandler.extra_bytes = b""
    _ScriptedHandler.requests = []


class BatchExchangeTests(unittest.TestCase):
    """Actual review_batch through the real owned child, per wire case."""

    def setUp(self) -> None:
        _reset_scripted()
        self.temp = tempfile.TemporaryDirectory()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _ScriptedHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(5)
        self.assertFalse(self.thread.is_alive())
        self.temp.cleanup()

    def _reviewer(
        self, timeout: float = 5.0, api_key: str | None = "fake-key",
        host: str | None = None,
    ) -> ResponsesReviewer:
        return ResponsesReviewer(
            f"http://{host or '127.0.0.1'}:{self.port}/v1",
            "test-model",
            timeout=timeout,
            api_key=api_key,
        )

    def _done_payload(self) -> bytes:
        envelope = _envelope(_valid_inner([_prop("t1"), _prop("t0")]))
        envelope["usage"] = {"input_tokens": 5, "output_tokens": 7, "total_tokens": 12}
        return json.dumps(envelope, ensure_ascii=False).encode()

    def test_fast_positive_exact_route_body_auth_reordered(self) -> None:
        _ScriptedHandler.payload = self._done_payload()
        reviewer = self._reviewer()
        result = reviewer.review_batch(TEXT, TARGETS)
        self.assertEqual(len(_ScriptedHandler.requests), 1)
        record = _ScriptedHandler.requests[0]
        self.assertEqual(record["path"], "/v1/responses")
        self.assertEqual(record["auth"], "Bearer fake-key")
        self.assertEqual(record["ctype"], "application/json")
        self.assertEqual(
            cast(bytes, record["body"]),
            build_request_body("test-model", cast(str, build_prompt(TARGETS))),
        )
        self.assertEqual(set(result.proposals), {"t0", "t1"})
        self.assertEqual(result.proposals["t0"].replacement, "tako")
        self.assertEqual(result.proposals["t1"].replacement, "tako")
        assert result.usage is not None
        self.assertEqual(
            (result.usage.input_tokens, result.usage.output_tokens, result.usage.total_tokens),
            (5, 7, 12),
        )

    def test_no_api_key_omits_authorization(self) -> None:
        _ScriptedHandler.payload = self._done_payload()
        with mock.patch.dict(os.environ, {}, clear=True):
            reviewer = self._reviewer(api_key=None)
            reviewer.review_batch(TEXT, TARGETS)
        self.assertIsNone(_ScriptedHandler.requests[0]["auth"])

    def test_non_200_http_not_ok(self) -> None:
        _ScriptedHandler.status = 500
        _ScriptedHandler.payload = b"{}"
        with self.assertRaises(ReviewerError) as caught:
            self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(caught.exception.reason, REASON_HTTP_NOT_OK)

    def test_oversized_payload_http_not_ok(self) -> None:
        prefix = b'{"object": "response", "status": "completed", "pad": "'
        suffix = b'"}'
        body = prefix + b"x" * (40000 - len(prefix) - len(suffix)) + suffix
        assert len(body) == 40000
        _ScriptedHandler.payload = body
        with self.assertRaises(ReviewerError) as caught:
            self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(caught.exception.reason, REASON_HTTP_NOT_OK)

    def test_invalid_utf8_invalid_encoding(self) -> None:
        _ScriptedHandler.payload = b'{"object": "\xff\xfe"}'
        with self.assertRaises(ReviewerError) as caught:
            self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(caught.exception.reason, REASON_INVALID_ENCODING)

    def test_invalid_json_rejected(self) -> None:
        _ScriptedHandler.payload = b"[1, 2, 3]"
        with self.assertRaises(ReviewerError) as caught:
            self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(caught.exception.reason, "REVIEW_INVALID_JSON")

    def test_envelope_missing_id_rejected(self) -> None:
        _ScriptedHandler.payload = json.dumps(
            _envelope(_valid_inner([_prop("t1")])), ensure_ascii=False
        ).encode()
        with self.assertRaises(ReviewerError) as caught:
            self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(caught.exception.reason, REASON_MISSING_ID)

    def test_hanging_status_http_failed_bounded(self) -> None:
        _ScriptedHandler.payload = self._done_payload()
        _ScriptedHandler.pre_status_delay = 5.0
        started = time.monotonic()
        with self.assertRaises(ReviewerError) as caught:
            self._reviewer(timeout=0.7).review_batch(TEXT, TARGETS)
        wall = time.monotonic() - started
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        self.assertLess(wall, 3.0, f"wall={wall:.2f}")
        self.assertEqual(len(_ScriptedHandler.requests), 1)

    def _drip_server(
        self,
        mode: str,
        payload: bytes = b"{}",
        gap: float = 0.03,
        body_frag: int = 2,
    ) -> tuple[int, _OwnedThreadingServer, threading.Thread]:
        _DripHandler.mode = mode
        _DripHandler.gap = gap
        _DripHandler.payload = payload
        _DripHandler.body_frag = body_frag
        _DripHandler.header_marks = 0
        _DripHandler.completed = threading.Event()
        _DripHandler.requests = []
        server = _OwnedThreadingServer(("127.0.0.1", 0), _DripHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server.server_address[1], server, thread

    def _drip_reviewer(self, port: int, timeout: float) -> ResponsesReviewer:
        return ResponsesReviewer(f"http://127.0.0.1:{port}/v1", "test-model",
                                 timeout=timeout, api_key="fake-key")

    def test_status_drip_positive_reaches_actual_producer(self) -> None:
        # The whole dripped status/headers arrive within budget: success,
        # and the producer is observed to have actually sent fragments.
        port, server, thread = self._drip_server(
            "status", payload=self._done_payload()
        )
        try:
            result = self._drip_reviewer(port, 10.0).review_batch(TEXT, TARGETS)
            self.assertEqual(set(result.proposals), {"t0", "t1"})
        finally:
            server.shutdown()
            for handler_thread in server.handler_threads:
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())
        self.assertEqual(len(_DripHandler.requests), 1)
        self.assertGreater(len(_DripHandler.marks), 10)
        self.assertGreater(_DripHandler.marks[-1] - _DripHandler.marks[0], 0.3)

    def test_status_drip_past_budget_fails(self) -> None:
        port, server, thread = self._drip_server("status")
        try:
            started = time.monotonic()
            with self.assertRaises(ReviewerError) as caught:
                self._drip_reviewer(port, 0.7).review_batch(TEXT, TARGETS)
            wall = time.monotonic() - started
            self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
            self.assertLess(wall, 3.0, f"wall={wall:.2f}")
        finally:
            server.shutdown()
            for handler_thread in server.handler_threads:
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())
        # The drip actually reached the producer before the deadline cut.
        self.assertEqual(len(_DripHandler.requests), 1)
        self.assertGreater(len(_DripHandler.marks), 10)

    def test_header_drip_past_budget_fails(self) -> None:
        port, server, thread = self._drip_server("headers")
        try:
            with self.assertRaises(ReviewerError) as caught:
                self._drip_reviewer(port, 0.7).review_batch(TEXT, TARGETS)
            self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        finally:
            server.shutdown()
            for handler_thread in server.handler_threads:
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())
        self.assertEqual(len(_DripHandler.requests), 1)
        self.assertGreater(len(_DripHandler.marks), 10)

    def test_body_drip_past_budget_fails(self) -> None:
        # Header arrives complete and fast; the body bytes then drip
        # up to the anchored budget (the header phase was below it).
        body = json.dumps(
            _envelope(_valid_inner([_prop("t1"), _prop("t0")])), ensure_ascii=False
        ).encode()
        port, server, thread = self._drip_server("body", payload=body)
        started = time.monotonic()
        try:
            with self.assertRaises(ReviewerError) as caught:
                self._drip_reviewer(port, 0.7).review_batch(TEXT, TARGETS)
            self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        finally:
            server.shutdown()
            for handler_thread in server.handler_threads:
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())
        self.assertEqual(len(_DripHandler.requests), 1)
        assert _DripHandler.header_done_at is not None
        assert _DripHandler.marks
        # Observed: the header phase finished well under the budget...
        self.assertLess(
            _DripHandler.header_done_at - started,
            0.4,
        )
        # ...and the body drip kept arriving right up to the anchored
        # deadline: the anchored budget, not any per-phase timer,
        # cut the exchange.
        self.assertGreater(_DripHandler.marks[-1] - started, 0.65)

    def test_interim_100_drip_past_budget_fails(self) -> None:
        # The dripped interim 100 never restarts the anchored deadline.
        port, server, thread = self._drip_server("interim")
        try:
            with self.assertRaises(ReviewerError) as caught:
                self._drip_reviewer(port, 0.7).review_batch(TEXT, TARGETS)
            self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        finally:
            server.shutdown()
            for handler_thread in server.handler_threads:
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())
        self.assertEqual(len(_DripHandler.requests), 1)
        self.assertGreater(len(_DripHandler.marks), 10)

    def test_interim_100_drip_then_success(self) -> None:
        # A dripped interim 100 within a generous budget still
        # succeeds: the 100 is real observed wire traffic and the
        # anchored deadline is not restarted by it.
        port, server, thread = self._drip_server("interim", payload=self._done_payload())
        try:
            result = self._drip_reviewer(port, 10.0).review_batch(TEXT, TARGETS)
            self.assertEqual(set(result.proposals), {"t0", "t1"})
        finally:
            server.shutdown()
            for handler_thread in server.handler_threads:
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())
        self.assertEqual(len(_DripHandler.requests), 1)
        self.assertGreater(len(_DripHandler.marks), 10)

    def test_cumulative_header_plus_body_each_below_budget_jointly_over(self) -> None:
        # A finite two-phase producer: both observed phases complete
        # below the short budget, jointly over it.  The generous-budget
        # positive measures the complete phases (each below the short
        # budget, joint over it); the same producer under the short
        # anchored budget fails, while separate per-phase timers of
        # the same size would pass (order 019-a, requirement 7).
        body = self._done_payload()
        # Scale the finite body fragments to the actual payload length
        # so the complete body phase measures ~0.66 s (22 fragments).
        body_frag = max(2, -(-len(body) // 22))
        port, server, thread = self._drip_server(
            "cumulative", payload=body, gap=0.03, body_frag=body_frag
        )
        try:
            result = self._drip_reviewer(port, 5.0).review_batch(TEXT, TARGETS)
            self.assertEqual(set(result.proposals), {"t0", "t1"})
            # Bounded actual producer completion: the handler's final
            # stamp lands only after its trailing drip sleep, so wait
            # for it before reading the measured phase times.
            self.assertTrue(_DripHandler.completed.wait(5.0))
            assert _DripHandler.header_done_at is not None
            assert _DripHandler.body_done_at is not None
            handler_start = cast(float, _DripHandler.requests[0]["started"])
            header_phase = _DripHandler.header_done_at - handler_start
            body_phase = _DripHandler.body_done_at - _DripHandler.header_done_at
            joint = _DripHandler.body_done_at - handler_start
            # Measured complete phases: each below the short budget,
            # jointly over it.
            self.assertLess(header_phase, 1.0, f"header={header_phase:.3f}")
            self.assertLess(body_phase, 1.0, f"body={body_phase:.3f}")
            self.assertGreater(joint, 1.0, f"joint={joint:.3f}")
        finally:
            server.shutdown()
            for handler_thread in server.handler_threads:
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

        port2, server2, thread2 = self._drip_server(
            "cumulative", payload=body, gap=0.03, body_frag=body_frag
        )
        started = time.monotonic()
        try:
            with self.assertRaises(ReviewerError) as caught:
                self._drip_reviewer(port2, 1.0).review_batch(TEXT, TARGETS)
            self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        finally:
            server2.shutdown()
            for handler_thread in server2.handler_threads:
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
            server2.server_close()
            thread2.join(5)
            self.assertFalse(thread2.is_alive())
        assert _DripHandler.header_done_at is not None
        assert _DripHandler.marks
        handler_start2 = cast(float, _DripHandler.requests[0]["started"])
        # Observed: the header phase completed below the short budget,
        # body bytes were still arriving at the anchored deadline, and
        # the body phase never completed before the cancellation.
        self.assertLess(_DripHandler.header_done_at - handler_start2, 1.0)
        self.assertGreater(len(_DripHandler.marks) - _DripHandler.header_marks, 3)
        self.assertGreater(_DripHandler.marks[-1] - started, 0.9)
        self.assertIsNone(_DripHandler.body_done_at)

    def test_localhost_hostname_positive(self) -> None:
        # Real resolver path for a real hostname (order 019-a,
        # requirement 8); no protected resolver reconfiguration.
        _ScriptedHandler.payload = self._done_payload()
        result = self._reviewer(host="localhost").review_batch(TEXT, TARGETS)
        self.assertEqual(set(result.proposals), {"t0", "t1"})

    def test_declared_close_delivery(self) -> None:
        _ScriptedHandler.payload = self._done_payload()
        _ScriptedHandler.close_after = True
        result = self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(set(result.proposals), {"t0", "t1"})

    def test_chunked_delivery(self) -> None:
        _ScriptedHandler.payload = self._done_payload()
        _ScriptedHandler.chunked = True
        result = self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(set(result.proposals), {"t0", "t1"})

    def test_buffered_overread_keepalive_trailing_bytes(self) -> None:
        _ScriptedHandler.payload = self._done_payload()
        _ScriptedHandler.extra_bytes = b"TRAILER-BYTES"
        result = self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(set(result.proposals), {"t0", "t1"})

    def test_split_utf8_multi_byte_segments(self) -> None:
        # Real 2/3/4-byte wire Unicode delivered in tiny fragments.
        text = "tako \u00e9 \u20ac \U0001F600"
        inner = _valid_inner([
            {"id": "t1", "keep": False, "replacement": text, "needs_wider_edit": False},
            {"id": "t0", "keep": True, "replacement": None, "needs_wider_edit": False},
        ])
        _ScriptedHandler.payload = json.dumps(
            _envelope(inner), ensure_ascii=False
        ).encode()
        _ScriptedHandler.split_bytes = 3
        result = self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(result.proposals["t1"].replacement, text)

    def test_split_invalid_utf8_rejected(self) -> None:
        _ScriptedHandler.payload = b'{"object": "\xc3"}'
        _ScriptedHandler.split_bytes = 1
        with self.assertRaises(ReviewerError) as caught:
            self._reviewer().review_batch(TEXT, TARGETS)
        self.assertEqual(caught.exception.reason, REASON_INVALID_ENCODING)

    def test_startup_charged_tight_budget_zero_upstream_requests(self) -> None:
        # Controlled orchestration proof: the owned fake worker
        # performs a real 0.3 s of injected work (around process
        # startup, inside the child) before it would emit a valid
        # frame.  A 0.2 s whole-exchange budget fails at the anchored
        # deadline with zero HTTP requests reaching the upstream and
        # the exact child reaped; a generous budget succeeds with the
        # frame at ~0.3 s.  The delay is owned-child work, not an
        # external DNS/resolver qualification (order 019-a,
        # requirement 8).
        payload = self._done_payload()
        _ScriptedHandler.payload = payload
        fake = Path(self.temp.name) / "startup_fake_worker.py"
        fake.write_text(
            _fake_worker_script(
                "import time\n"
                "time.sleep(0.3)\n"
                "import struct\n"
                f"payload = {payload!r}\n"
                + _FAKE_RESPONSE.format(status_byte=0, http_status=200, exit_code=0)
            )
        )
        observed: list[subprocess.Popen[bytes]] = []
        started = time.monotonic()
        with (
            mock.patch.object(qwen_client, "_REVIEW_WORKER_PATH", fake),
            _tracked_popen(observed),
            self.assertRaises(ReviewerError) as caught,
        ):
            self._reviewer(timeout=0.2).review_batch(TEXT, TARGETS)
        wall = time.monotonic() - started
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        self.assertEqual(_ScriptedHandler.requests, [])
        self.assertLess(wall, 2.5, f"wall={wall:.2f}")
        # The product reaped the exact owned child (no test-side wait).
        self.assertEqual(len(observed), 1)
        self.assertIsNotNone(observed[0].returncode)
        # The same owned child under a generous budget succeeds with
        # its frame at ~0.3 s and zero upstream requests (the frame is
        # embedded owned-child work).
        _ScriptedHandler.requests = []
        observed2: list[subprocess.Popen[bytes]] = []
        with (
            mock.patch.object(qwen_client, "_REVIEW_WORKER_PATH", fake),
            _tracked_popen(observed2),
        ):
            result = self._reviewer(timeout=5.0).review_batch(TEXT, TARGETS)
        self.assertEqual(set(result.proposals), {"t0", "t1"})
        self.assertEqual(_ScriptedHandler.requests, [])
        self.assertEqual(len(observed2), 1)
        self.assertIsNotNone(observed2[0].returncode)
        # Positive control: the real worker under the same budget makes
        # exactly one real upstream request.
        _ScriptedHandler.requests = []
        result2 = self._reviewer(timeout=5.0).review_batch(TEXT, TARGETS)
        self.assertEqual(set(result2.proposals), {"t0", "t1"})
        self.assertEqual(len(_ScriptedHandler.requests), 1)

    def _incomplete_case(self, declared: int, delivered: bytes) -> None:
        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(declared))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(delivered)

            def log_message(self, *_args: object) -> None:
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            reviewer = ResponsesReviewer(
                f"http://127.0.0.1:{server.server_address[1]}/v1",
                "test-model",
                timeout=5.0,
                api_key="k",
            )
            with self.assertRaises(ReviewerError) as caught:
                reviewer.review_batch(TEXT, TARGETS)
            self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_incomplete_declared_near_complete_valid_json(self) -> None:
        body = b'{"object": "response", "status": "completed"'
        self._incomplete_case(declared=len(body) + 6, delivered=body)

    def test_incomplete_declared_far_short(self) -> None:
        self._incomplete_case(declared=100, delivered=b'{"a":1')

    def test_incomplete_declared_oversized_declaration(self) -> None:
        # The exact strategy reproduction: a valid, complete small JSON
        # batch with a declaration far above the response cap.
        body = self._done_payload()
        self._incomplete_case(declared=len(body) + 50000, delivered=body)

    def test_complete_oversized_delivery_http_not_ok(self) -> None:
        # A payload that actually exceeds the cap keeps the existing
        # oversized-payload rejection path (not the incomplete label).
        prefix = b'{"object": "response", "status": "completed", "pad": "'
        suffix = b'"}'
        body = prefix + b"x" * (40000 - len(prefix) - len(suffix)) + suffix
        assert len(body) == 40000

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args: object) -> None:
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            reviewer = ResponsesReviewer(
                f"http://127.0.0.1:{server.server_address[1]}/v1",
                "test-model",
                timeout=5.0,
                api_key="k",
            )
            with self.assertRaises(ReviewerError) as caught:
                reviewer.review_batch(TEXT, TARGETS)
            self.assertEqual(caught.exception.reason, REASON_HTTP_NOT_OK)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_late_parent_validation_recheck(self) -> None:
        # Mechanism proof of the post-parse deadline recheck: the
        # exchange returns a valid frame, then the anchored deadline is
        # treated as passed before the result is transferred, so the
        # batch fails as a unit with the fixed transport label.
        _ScriptedHandler.payload = self._done_payload()
        reviewer = self._reviewer(timeout=5.0)
        real_exchange = rt.run_review_exchange
        state = {"jumped": False}

        def wrapped_exchange(**kwargs: Any) -> tuple[int, bytes]:
            result = real_exchange(**kwargs)
            state["jumped"] = True
            return result

        real_monotonic = time.monotonic

        def gated_monotonic() -> float:
            value = real_monotonic()
            return value + 5.0 if state["jumped"] else value

        with (
            mock.patch.object(qwen_client, "run_review_exchange", wrapped_exchange),
            mock.patch.object(time, "monotonic", gated_monotonic),
            self.assertRaises(ReviewerError) as caught,
        ):
            reviewer.review_batch(TEXT, TARGETS)
        self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        self.assertEqual(len(_ScriptedHandler.requests), 1)


class _OwnedThreadingServer(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int], handler: type[BaseHTTPRequestHandler]) -> None:
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


class ProxyIntegrationTests(unittest.TestCase):
    """Real ConceptProxy + RepairEngine + Pandoc + SQLite + real owned
    reviewer child; synthetic loopback main/review upstreams only."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        # The qualified unigram table (includes the protected Unicode
        # word of the useful answer); bigram/trigram/middle use the
        # frozen healthy defaults.
        self.db = self.root / "tiny.sqlite"
        _build_db(self.db, unigram=_BUILD_UNIGRAM)
        self.servers: list[HTTPServer] = []
        self.threads: list[threading.Thread] = []

    def tearDown(self) -> None:
        for server in self.servers:
            server.shutdown()
        for thread in self.threads:
            thread.join(5)
            self.assertFalse(thread.is_alive())
        for server in self.servers:
            for handler_thread in getattr(server, "handler_threads", ()):
                handler_thread.join(5)
                self.assertFalse(handler_thread.is_alive())
        for server in self.servers:
            server.server_close()
        self.temp.cleanup()

    def _start(self, handler_cls: type[BaseHTTPRequestHandler]) -> tuple[int, ThreadingHTTPServer]:
        server = _OwnedThreadingServer(("127.0.0.1", 0), handler_cls)
        self.servers.append(server)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)
        return server.server_address[1], server

    def _harness(
        self,
        main_port: int,
        *,
        timeout: float = 5.0,
        usage_records: list[dict[str, object]] | None = None,
    ) -> Any:
        import proxy

        reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.review_port}/v1",
            "test-model",
            timeout=timeout,
            api_key="fake-key",
        )
        engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{main_port}",
            engine,
            usage_observer=(
                (lambda record: usage_records.append(record)) if usage_records is not None else None
            ),
        )
        self.servers.append(proxy_server)
        thread = threading.Thread(target=proxy_server.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)
        return proxy_server

    def _post(self, proxy_port: int, source: bytes, *, stream: bool = True) -> tuple[int, bytes]:
        client = http.client.HTTPConnection("127.0.0.1", proxy_port, timeout=30)
        body = _contract_body(stream)
        client.request(
            "POST", "/v1/responses", body=body,
            headers={"Content-Length": str(len(body))},
        )
        response = client.getresponse()
        result = response.read()
        client.close()
        return response.status, result

    def _sse_main(self, source: bytes) -> int:
        class Main(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(source)))
                self.end_headers()
                self.wfile.write(source)

            def log_message(self, *_args: object) -> None:
                return

        port, _ = self._start(Main)
        return port

    def _json_main(self, source: bytes) -> int:
        class Main(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(source)))
                self.end_headers()
                self.wfile.write(source)

            def log_message(self, *_args: object) -> None:
                return

        port, _ = self._start(Main)
        return port

    def _review_main(self, payload: bytes, delay: float = 0.0) -> int:
        _FakeUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.payload = payload
        _FakeUpstream.delay = delay
        port, _ = self._start(_FakeUpstream)
        self.review_port = port
        return port

    review_port: int

    def test_chain_useful_two_targets_json_and_sse(self) -> None:
        for stream in (False, True):
            with self.subTest(stream=stream):
                self._review_main(
                    _review_payload(
                        [_prop("t1"), _prop("t0")],
                        usage={
                            "input_tokens": 4,
                            "output_tokens": 6,
                            "total_tokens": 10,
                        },
                    )
                )
                if stream:
                    main_port = self._sse_main(_sse_baseline_utf8(USEFUL))
                else:
                    main_port = self._json_main(_json_completed(USEFUL))
                proxy_server = self._harness(main_port)
                status, result = self._post(proxy_server.server_port, source=b"", stream=stream)
                self.assertEqual(status, 200)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                # Both supported occurrences edited...
                self.assertIn(b"To je tako zapisano, to je tako zapisano.", result)
                # ...while the protected code span and the separate
                # Unicode paragraph are preserved exactly.
                self.assertIn(b"`presenetliv`", result)
                self.assertIn("\u00e9 \u20ac \U0001F600".encode(), result)
                self.assertNotIn(b"presenetliv zapisano", result)

    def test_chain_no_suspicion_zero_review_exact_bytes(self) -> None:
        self._review_main(_review_payload([_prop("t0")]))
        sse_source = _sse_baseline_utf8(CLEAN)
        main_port = self._sse_main(sse_source)
        proxy_server = self._harness(main_port)
        status, result = self._post(proxy_server.server_port, source=b"", stream=True)
        self.assertEqual(status, 200)
        self.assertEqual(result, sse_source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_reviewer_hang_small_timeout_original_unknown_usage(self) -> None:
        records: list[dict[str, object]] = []
        sse_source = _sse_baseline_utf8(TEXT)
        # The review upstream receives the request, then hangs past the
        # small whole-exchange budget.
        self._review_main(self._done_review_payload(), delay=2.0)
        main_port = self._sse_main(sse_source)
        proxy_server = self._harness(main_port, timeout=0.7, usage_records=records)
        status, result = self._post(proxy_server.server_port, source=b"", stream=True)
        self.assertEqual(status, 200)
        self.assertEqual(result, sse_source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertEqual(records, [{"review_calls": 1, "reviewer_usage": "unknown"}])

    def test_chain_main_error_and_incomplete_capture_zero_review(self) -> None:
        self._review_main(self._done_review_payload())

        class ErrorMain(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(b"{}")

            def log_message(self, *_args: object) -> None:
                return

        # A genuine upstream non-200 HTTP status keeps its own status
        # and exact body (preserved semantics, not remapped to 502):
        # zero engine analysis and zero review.
        main_port, _ = self._start(ErrorMain)
        proxy_server = self._harness(main_port)
        status, result = self._post(proxy_server.server_port, source=b"", stream=True)
        self.assertEqual(status, 500)
        self.assertEqual(result, b"{}")
        self.assertEqual(len(_FakeUpstream.recorded), 0)

        # An incomplete main capture (declared longer than delivered)
        # still returns 502 with zero review before completion.
        class IncompleteMain(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(a_source) + 10))
                self.send_header("Connection", "close")
                self.close_connection = True
                self.end_headers()
                self.wfile.write(a_source)

            def log_message(self, *_args: object) -> None:
                return

        a_source = _sse_baseline_utf8(TEXT)
        main_port, _ = self._start(IncompleteMain)
        proxy_server = self._harness(main_port)
        status, _ = self._post(proxy_server.server_port, source=b"", stream=True)
        self.assertEqual(status, 502)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_healthy_after_reviewer_timeout_no_carryover(self) -> None:
        # First request: review hangs past the budget -> exact original.
        # Second request: healthy repair with a fresh known usage.
        self._review_main(self._done_review_payload(), delay=2.0)
        main_port = self._sse_main(_sse_baseline_utf8(TEXT))
        proxy_server = self._harness(main_port, timeout=0.7)
        status, result = self._post(proxy_server.server_port, source=b"", stream=True)
        self.assertEqual(status, 200)
        self.assertEqual(result, _sse_baseline_utf8(TEXT))

        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = _review_payload(
            [_prop("t1"), _prop("t0")],
            usage={"input_tokens": 9, "output_tokens": 3, "total_tokens": 12},
        )
        status, result = self._post(proxy_server.server_port, source=b"", stream=True)
        self.assertEqual(status, 200)
        self.assertIn(b"To je tako zapisano, to je tako zapisano.", result)
        self.assertNotIn(b"presenetliv", result)
        self.assertEqual(len(_FakeUpstream.recorded), 2)

    def test_chain_no_usage_carryover_between_batches(self) -> None:
        records: list[dict[str, object]] = []
        known = {"input_tokens": 9, "output_tokens": 3, "total_tokens": 12}
        self._review_main(_review_payload([_prop("t1"), _prop("t0")], usage=known))
        main_port = self._sse_main(_sse_baseline_utf8(TEXT))
        proxy_server = self._harness(main_port, usage_records=records)
        status, _ = self._post(proxy_server.server_port, source=b"", stream=True)
        self.assertEqual(status, 200)

        _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
        status, _ = self._post(proxy_server.server_port, source=b"", stream=True)
        self.assertEqual(status, 200)
        self.assertEqual(
            records,
            [
                {"review_calls": 1, "reviewer_usage": dict(known)},
                {"review_calls": 1, "reviewer_usage": "unknown"},
            ],
        )

    def _done_review_payload(self) -> bytes:
        return _review_payload(
            [_prop("t1"), _prop("t0")],
            usage={"input_tokens": 4, "output_tokens": 6, "total_tokens": 10},
        )

    def test_chain_other_connection_isolation_unbuffered_body(self) -> None:
        # Request A triggers a reviewer exchange that hangs past its
        # budget; request B runs through a second live proxy whose own
        # main upstream connection and 200/SSE headers are established
        # while A's exchange is still in flight (before A's anchored
        # deadline expires).  B's new body bytes are held at the source
        # and released unbuffered (flushed 16-byte fragments) only
        # after A has returned - i.e. only after A's timed-out child
        # was terminated and reaped.  A's kill must never touch B's
        # socket: B then completes with its exact original
        # no-suspicion answer and no review of its own.
        a_done = threading.Event()
        observed: dict[str, float | None] = {
            "b_headers_at": None,
            "b_first_byte_at": None,
        }

        a_source = _sse_baseline_utf8(TEXT)
        b_source = _sse_baseline_utf8(CLEAN)

        class AMain(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(a_source)))
                self.end_headers()
                self.wfile.write(a_source)

            def log_message(self, *_args: object) -> None:
                return

        class BMain(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(b_source)))
                self.end_headers()
                observed["b_headers_at"] = time.monotonic()
                # Hold the new body bytes until A has fully returned.
                if not a_done.wait(20.0):
                    raise AssertionError("request A never returned")
                for index in range(0, len(b_source), 16):
                    self.wfile.write(b_source[index : index + 16])
                    self.wfile.flush()
                    if observed["b_first_byte_at"] is None:
                        observed["b_first_byte_at"] = time.monotonic()
                    time.sleep(0.01)

            def log_message(self, *_args: object) -> None:
                return

        a_port = self._start(AMain)[0]
        b_port = self._start(BMain)[0]
        # The shared review upstream hangs A's one exchange attempt.
        self._review_main(self._done_review_payload(), delay=2.0)
        a_proxy = self._harness(a_port, timeout=0.7)
        b_proxy = self._harness(b_port, timeout=0.7)

        a_result: dict[str, object] = {}
        b_result: dict[str, object] = {}
        a_returned_at: float | None = None

        def call_a() -> None:
            nonlocal a_returned_at
            status, result = self._post(a_proxy.server_port, source=b"", stream=True)
            a_result["status"] = status
            a_result["result"] = result
            a_returned_at = time.monotonic()
            a_done.set()

        def call_b() -> None:
            status, result = self._post(b_proxy.server_port, source=b"", stream=True)
            b_result["status"] = status
            b_result["result"] = result

        a_started_at = time.monotonic()
        a_thread = threading.Thread(target=call_a)
        a_thread.start()
        time.sleep(0.05)  # let A's capture and anchored deadline start
        b_thread = threading.Thread(target=call_b)
        b_thread.start()
        a_thread.join(20.0)
        self.assertFalse(a_thread.is_alive(), "request A did not complete")
        b_thread.join(30.0)
        self.assertFalse(b_thread.is_alive(), "request B did not complete")

        assert a_returned_at is not None
        b_headers_at = observed["b_headers_at"]
        b_first_byte_at = observed["b_first_byte_at"]
        self.assertIsNotNone(b_headers_at, "B's headers never reached its upstream")
        self.assertIsNotNone(b_first_byte_at, "B's body never flowed")
        assert b_headers_at is not None
        assert b_first_byte_at is not None
        # B's own live connection and headers existed while A's
        # exchange was still in flight and before A's 0.7 s anchored
        # budget expired (A's fast main capture starts it early).
        self.assertLess(b_headers_at, a_returned_at)
        self.assertLess(b_headers_at - a_started_at, 0.65)
        # B's new body bytes flowed only after A had returned (reaped).
        self.assertGreaterEqual(b_first_byte_at, a_returned_at - 0.02)
        self.assertEqual(a_result["status"], 200)
        self.assertEqual(a_result["result"], a_source)
        self.assertEqual(b_result["status"], 200)
        self.assertEqual(b_result["result"], b_source)
        # A made the one review attempt; B's no-suspicion answer made none.
        self.assertEqual(len(_FakeUpstream.recorded), 1)


class TlsExchangeTests(unittest.TestCase):
    """Actual HTTPS reviewer exchange with an owned ephemeral
    certificate trusted only through the forwarded SSL_CERT_FILE."""

    temp: tempfile.TemporaryDirectory[str]
    cert: Path
    key: Path

    @classmethod
    def setUpClass(cls) -> None:
        if shutil.which("openssl") is None:
            raise unittest.SkipTest("openssl not available")
        cls.temp = tempfile.TemporaryDirectory()
        cls.cert = Path(cls.temp.name) / "cert.pem"
        cls.key = Path(cls.temp.name) / "key.pem"
        proc = subprocess.run(
            [
                "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                "-keyout", str(cls.key), "-out", str(cls.cert),
                "-days", "1", "-subj", "/CN=127.0.0.1",
                "-addext", "subjectAltName=IP:127.0.0.1",
            ],
            capture_output=True,
            timeout=60,
        )
        assert proc.returncode == 0, proc.stderr.decode(errors="replace")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def _tls_upstream(self, payload: bytes) -> tuple[int, ThreadingHTTPServer, threading.Thread]:
        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers.get("Content-Length", "0")))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *_args: object) -> None:
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(str(self.cert), str(self.key))
        server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server.server_address[1], server, thread

    def test_tls_positive_real_reviewer_owned_trust(self) -> None:
        payload = json.dumps(
            _envelope(_valid_inner([_prop("t1"), _prop("t0")])), ensure_ascii=False
        ).encode()
        port, server, thread = self._tls_upstream(payload)
        try:
            with mock.patch.dict(os.environ, {"SSL_CERT_FILE": str(self.cert)}):
                reviewer = ResponsesReviewer(
                    f"https://127.0.0.1:{port}/v1", "test-model",
                    timeout=8.0, api_key="k",
                )
                result = reviewer.review_batch(TEXT, TARGETS)
            self.assertEqual(set(result.proposals), {"t0", "t1"})
        finally:
            server.shutdown()
            server.server_close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_tls_handshake_stall_bounded_reaped(self) -> None:
        # The owned listener accepts TCP, observes the actual TLS
        # ClientHello, and then holds the connection without ever
        # completing the handshake: the stall is genuinely in the TLS
        # phase (not an early worker startup failure), and the owned
        # child must be killed and reaped at the whole-exchange budget.
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", 0))
        listener.listen(4)
        port = listener.getsockname()[1]
        accepted: list[socket.socket] = []
        hello_seen = threading.Event()
        stop = threading.Event()

        def acceptor() -> None:
            try:
                while not stop.is_set():
                    conn, _address = listener.accept()
                    accepted.append(conn)
                    with contextlib.suppress(OSError):
                        conn.settimeout(2.0)
                        head = conn.recv(16)
                    if head[:1] == b"\x16":
                        # A real TLS handshake record reached the
                        # fixture: the stall is after the connection.
                        hello_seen.set()
                    # Hold the connection without handshake progress.
                    while not stop.is_set():
                        time.sleep(0.05)
            except OSError:
                return

        thread = threading.Thread(target=acceptor)
        thread.start()
        try:
            started = time.monotonic()
            reviewer = ResponsesReviewer(
                f"https://127.0.0.1:{port}/v1", "test-model",
                timeout=0.7, api_key="k",
            )
            with self.assertRaises(ReviewerError) as caught:
                reviewer.review_batch(TEXT, TARGETS)
            wall = time.monotonic() - started
            self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
            self.assertLess(wall, 3.0, f"wall={wall:.2f}")
            # The connection actually reached the fixture and began
            # TLS before the bounded failure.
            self.assertTrue(hello_seen.wait(2.0),
                            "no TLS ClientHello reached the owned listener")
            self.assertTrue(accepted)
        finally:
            stop.set()
            listener.close()
            for conn in accepted:
                with contextlib.suppress(OSError):
                    conn.close()
            thread.join(5)
            self.assertFalse(thread.is_alive())

    def test_tls_unknown_ca_verification_fails(self) -> None:
        # Without trust for the ephemeral certificate, HTTPS verification
        # must fail: verification is never disabled.
        payload = json.dumps(
            _envelope(_valid_inner([_prop("t1"), _prop("t0")])), ensure_ascii=False
        ).encode()
        port, server, thread = self._tls_upstream(payload)
        try:
            clean = {
                k: v for k, v in os.environ.items()
                if k not in ("SSL_CERT_FILE", "SSL_CERT_DIR")
            }
            with mock.patch.dict(os.environ, clean, clear=True):
                reviewer = ResponsesReviewer(
                    f"https://127.0.0.1:{port}/v1", "test-model",
                    timeout=5.0, api_key="k",
                )
                with self.assertRaises(ReviewerError) as caught:
                    reviewer.review_batch(TEXT, TARGETS)
                self.assertEqual(caught.exception.reason, REASON_HTTP_FAILED)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(5)


class ConstructorWiringTests(unittest.TestCase):
    def test_timeout_validation_negatives(self) -> None:
        # Deliberately invalid argument values, typed as object so the
        # negative constructor boundary is exercised with exact types.
        bad_values: tuple[object, ...] = (
            True, False, 0, -1, 0.0, -0.5, float("nan"),
            float("inf"), -float("inf"), "15", None,
        )
        for bad in bad_values:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                ResponsesReviewer(
                    "http://127.0.0.1:9/v1", "m", timeout=cast(float, bad)
                )

    def test_default_timeout_is_ordered_cap(self) -> None:
        self.assertEqual(REVIEWER_HTTP_TIMEOUT_SECONDS, 15.0)
        reviewer = ResponsesReviewer("http://127.0.0.1:9/v1", "m")
        self.assertEqual(reviewer.timeout, 15.0)

    def test_main_wires_validated_real_constructor(self) -> None:
        # main() must reach real ConceptProxy construction: the real
        # validated constructor (upstream check, budget validation,
        # real owned bind) with the real validating ResponsesReviewer
        # and the ordered 15 s cap; the qualified Pandoc startup
        # check runs for real.  Only the bind address is redirected to
        # an owned loopback port 0; the fixed service port is never
        # bound and no serving happens.
        import proxy

        configured = os.environ.get("CONCEPT_PANDOC", "").strip()
        if not configured:
            raise unittest.SkipTest("CONCEPT_PANDOC not configured")

        captured: dict[str, object] = {}
        created: list[proxy.ConceptProxy] = []
        created_reviewers: list[Recorder] = []

        class Recorder(ResponsesReviewer):
            def __init__(
                self,
                base_url: str,
                model: str,
                timeout: float = REVIEWER_HTTP_TIMEOUT_SECONDS,
                api_key: str | None = None,
                profile: str | Path | None = None,
            ) -> None:
                captured["timeout"] = timeout
                captured["base_url"] = base_url
                created_reviewers.append(self)
                super().__init__(
                    base_url, model, timeout=timeout, api_key=api_key,
                    profile=profile,
                )

        class Port0Proxy(proxy.ConceptProxy):
            # Exercises the real validated constructor while
            # redirecting only the fixture address to an owned
            # port 0 (never the fixed service port).
            def __init__(
                self,
                address: tuple[str, int],
                upstream: str,
                engine: proxy.RepairEngine,
                timeout: float = 30.0,
                trace_dir: Path | None = None,
                usage_observer: Callable[[dict[str, object]], None] | None = None,
                *,
                header_timeout: float = 30.0,
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
                captured["port"] = self.server_address[1]
                captured["proxy"] = self
                created.append(self)
                self.server_close()
                raise SystemExit("stop before serve_forever")

        with tempfile.TemporaryDirectory() as tmp:
            db = _build_corpus(Path(tmp))
            env = {
                "CONCEPT_INDEX": str(db),
                "CONCEPT_REVIEWER_URL": "http://127.0.0.1:9/v1",
                "CONCEPT_TIMEOUT": "999",
                "CONCEPT_PANDOC": configured,
            }
            with (
                mock.patch.dict(os.environ, env, clear=True),
                mock.patch.object(proxy, "ResponsesReviewer", Recorder),
                mock.patch.object(proxy, "ConceptProxy", Port0Proxy),
                self.assertRaises(SystemExit) as raised,
            ):
                proxy.main()
        self.assertEqual(str(raised.exception), "stop before serve_forever")
        self.assertEqual(captured["timeout"], REVIEWER_HTTP_TIMEOUT_SECONDS)
        self.assertEqual(captured["base_url"], "http://127.0.0.1:9/v1")
        self.assertEqual(len(created), 1)
        # A real ephemeral loopback port was bound (never 0, never the
        # fixed service port) and then closed before serving.
        port = created[0].server_address[1]
        self.assertGreater(port, 1024)
        self.assertNotEqual(port, 18024)
        self.assertEqual(created[0].socket.fileno(), -1)
        # The real engine and real validating reviewer were wired.
        engine = created[0].engine
        self.assertIsInstance(engine, proxy.RepairEngine)
        self.assertIsInstance(engine.reviewer, Recorder)
        self.assertEqual(len(created_reviewers), 1)
        self.assertIs(engine.reviewer, created_reviewers[0])
        self.assertEqual(created_reviewers[0].timeout, REVIEWER_HTTP_TIMEOUT_SECONDS)


class LegacyPreservationTests(unittest.TestCase):
    def test_protected_qwen_sections_byte_identical(self) -> None:
        source = (ROOT / "qwen_client.py").read_text()
        lines = source.splitlines(keepends=True)
        tree = ast.parse(source)
        members = {
            n.name: n for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))
        }
        cls = cast(ast.ClassDef, members["ResponsesReviewer"])
        method = next(
            n for n in cls.body
            if isinstance(n, ast.FunctionDef) and n.name == "review"
        )
        targets: dict[str, ast.FunctionDef | ast.ClassDef] = {
            "Proposal": cast(ast.ClassDef, members["Proposal"]),
            "responses_path": cast(ast.FunctionDef, members["responses_path"]),
            "parse_proposal": cast(ast.FunctionDef, members["parse_proposal"]),
            "prompt": cast(ast.FunctionDef, members["prompt"]),
            "ResponsesReviewer.review": method,
        }
        for name, node in targets.items():
            start = min((d.lineno for d in node.decorator_list), default=node.lineno)
            data = "".join(lines[start - 1 : node.end_lineno]).encode()
            expected_sha, expected_len = _PROTECTED_SECTIONS[name]
            with self.subTest(section=name):
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected_sha)
                self.assertEqual(len(data), expected_len)


if __name__ == "__main__":
    unittest.main()
