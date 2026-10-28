"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Upstream setup.

Order 022-a acceptance coverage for the one bounded main-upstream setup
phase in the runnable proxy: the finite setup budget validator, the
strict versioned resolver frame codec, the owned pure-timer
SetupGuard lifecycle (exact-socket interruption, adopt refusal after
expiry, partial-startup containment, no surviving threads), the real
owned resolver child (argv/env/reaping, literal fast path, deadline,
late and racing completion, trailing/malformed frames, controlled
call-through delay, controlled caller interruption during the real
start seam before and after actual child creation), the real
forward setup phases against owned
loopback HTTP and TLS endpoints (stalled TLS handshake, nonreading and
slow-reading upload, cumulative each-phase-fits/sum-expires, bounded
connect attempts, exact header allowlist), same-proxy recovery after a
failed setup, and the real constructor/main default, override and
invalid-before-bind behavior.

Every fixture is owned and actually joined/reaped/closed; synthetic
fixture payloads are labeled synthetic; no live model, DNS service or
credential is exercised beyond the owned loopback endpoints.
"""

from __future__ import annotations

import contextlib
import http.client
import io
import ipaddress
import json
import os
import signal
import socket
import ssl
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable, Iterator
from contextlib import contextmanager, suppress
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
    ThreadingHTTPServer,
)
from pathlib import Path
from typing import NoReturn, cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import proxy  # noqa: E402
import upstream_setup  # noqa: E402
from batch_review import BatchTarget  # noqa: E402
from config import (  # noqa: E402
    CLIENT_DELIVERY_TIMEOUT_SECONDS,
    CLIENT_REQUEST_TIMEOUT_SECONDS,
    MAIN_HEADER_TIMEOUT_SECONDS,
    MAIN_SETUP_TIMEOUT_SECONDS,
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
)
from tests.test_responses_contract import (  # noqa: E402
    _Harness,
    _json_completed,
    _MainUpstream,
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


def _guard_threads() -> list[threading.Thread]:
    return [t for t in threading.enumerate() if t.name == "concept-setup-guard"]


class ValidateSetupBudgetTests(unittest.TestCase):
    """Order 022-a requirement 1: the finite positive setup budget."""

    def test_accepts_finite_positive_values(self) -> None:
        for value, expected in (
            (30, 30.0),
            (30.0, 30.0),
            (1, 1.0),
            (1.0, 1.0),
            (0.5, 0.5),
            (0.001, 0.001),
        ):
            self.assertEqual(
                upstream_setup.validate_setup_budget(value), expected
            )
        self.assertIsInstance(
            upstream_setup.validate_setup_budget(30), float
        )

    def test_rejects_nonpositive_and_nonnumeric(self) -> None:
        for bad in (0, 0.0, -1, -0.5, "30", "30.0", "", None, [], {}, object()):
            with self.assertRaises(ValueError):
                upstream_setup.validate_setup_budget(bad)

    def test_rejects_bools(self) -> None:
        for bad in (True, False):
            with self.assertRaises(ValueError):
                upstream_setup.validate_setup_budget(bad)

    def test_rejects_nonfinite(self) -> None:
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                upstream_setup.validate_setup_budget(bad)

    def test_rejects_platform_unrepresentable_durations(self) -> None:
        # Finite but above the platform bounded wait: must reject,
        # never silently disable the deadline.
        for bad in (
            threading.TIMEOUT_MAX + 1.0,
            threading.TIMEOUT_MAX * 2.0,
            1e300,
        ):
            with self.assertRaises(ValueError):
                upstream_setup.validate_setup_budget(bad)

    def test_rejects_huge_int_that_cannot_convert(self) -> None:
        with self.assertRaises(ValueError):
            upstream_setup.validate_setup_budget(10**400)

    def test_accepts_at_the_platform_bound(self) -> None:
        self.assertEqual(
            upstream_setup.validate_setup_budget(threading.TIMEOUT_MAX),
            threading.TIMEOUT_MAX,
        )


class FrameCodecTests(unittest.TestCase):
    """Order 022-a requirement 4: the strict versioned frame contract."""

    def _request_frame(self, host: str, port: int) -> bytes:
        return upstream_setup.encode_request_frame(host=host, port=port)

    @staticmethod
    def _raw(frame: bytes) -> bytes:
        # The encoders emit the wire-ready 8-byte length prefix plus
        # frame; the decoders validate the frame without the prefix
        # (the I/O layer splits it).  Check the prefix, return frame.
        (declared,) = struct.Struct(">Q").unpack(frame[:8])
        assert declared == len(frame) - 8
        return frame[8:]

    def test_wire_framing_boundary(self) -> None:
        # The wire framing contract itself: the outer 8-byte >Q
        # prefix carries the inner frame length, and the payload
        # decoders consume ONLY the inner frame - passing the whole
        # wire straight in is a protocol deviation, not an alternate
        # accepted form.
        prefix = struct.Struct(">Q")
        for wire in (
            self._request_frame("example.test", 8080),
            upstream_setup.encode_response_frame(
                addresses=[(upstream_setup._FAMILY_INET, "10.0.0.1")]
            ),
            upstream_setup.encode_failure_frame(),
        ):
            self.assertGreaterEqual(len(wire), 8)
            self.assertEqual(
                prefix.unpack(wire[:8]), (len(wire) - 8,)
            )
        request_wire = self._request_frame("example.test", 8080)
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_request_frame(request_wire)
        response_wire = upstream_setup.encode_response_frame(
            addresses=[(upstream_setup._FAMILY_INET, "10.0.0.1")]
        )
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_response_frame(response_wire)
        # The total wire cap is the prefix plus the inner bound.
        self.assertEqual(
            len(request_wire),
            prefix.size
            + len(self._raw(request_wire)),
        )
        self.assertLessEqual(
            len(request_wire), prefix.size
            + upstream_setup.REQUEST_FRAME_MAX_BYTES
        )

    def test_request_round_trip(self) -> None:
        for host, port in (
            ("example.test", 8080),
            ("localhost", 1),
            ("a-b.example", 65535),
        ):
            frame = self._request_frame(host, port)
            raw = self._raw(frame)
            self.assertLessEqual(
                len(raw), upstream_setup.REQUEST_FRAME_MAX_BYTES
            )
            self.assertEqual(
                upstream_setup.decode_request_frame(raw), (host, port)
            )

    def test_request_host_bounds(self) -> None:
        ok = "h" * 255
        self.assertEqual(
            upstream_setup.decode_request_frame(
                self._raw(self._request_frame(ok, 80))
            ),
            (ok, 80),
        )
        with self.assertRaises(upstream_setup.FrameMalformed):
            self._request_frame("h" * 256, 80)
        with self.assertRaises(upstream_setup.FrameMalformed):
            self._request_frame("", 80)
        # NUL is rejected by the strict decoder (the encoder bounds
        # length/emptiness; the codec split is deliberate).
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_request_frame(
                struct.Struct(">4sBBHH").pack(b"USTX", 1, 1, 3, 80)
                + b"a\x00b"
            )

    def test_request_port_bounds(self) -> None:
        for bad in (0, 65536, True, False, -1, 1.0):
            with self.assertRaises(upstream_setup.FrameMalformed):
                self._request_frame("example.test", bad)  # type: ignore[arg-type]

    def test_request_decode_rejects_identity_and_length_deviation(self) -> None:
        good = self._raw(self._request_frame("example.test", 8080))
        for frame in (
            good[:-1],  # truncated host
            good + b"x",  # inconsistent declared length
            b"\x00" * (upstream_setup.REQUEST_FRAME_MAX_BYTES + 1),
            b"\x00" * 5,  # below fixed header
        ):
            with self.assertRaises(upstream_setup.FrameMalformed):
                upstream_setup.decode_request_frame(frame)
        header = struct.Struct(">4sBBHH")
        # wrong magic / version / kind
        for offset, bad_value in (
            (0, b"USTY"),
            (4, 2),
            (5, 2),
        ):
            raw = bytearray(good)
            if isinstance(bad_value, bytes):
                raw[offset : offset + 4] = bad_value
            else:
                raw[offset] = bad_value
            with self.assertRaises(upstream_setup.FrameMalformed):
                upstream_setup.decode_request_frame(bytes(raw))
        # port out of range inside the frame
        raw = bytearray(good)
        struct.pack_into(">H", raw, 8, 0)
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_request_frame(bytes(raw))
        # NUL and non-UTF8 host
        for bad_host in (b"a\x00b", b"\xff\xfe"):
            bad_frame = header.pack(
                b"USTX", 1, 1, len(bad_host), 80
            ) + bad_host
            if len(bad_frame) <= upstream_setup.REQUEST_FRAME_MAX_BYTES:
                with self.assertRaises(upstream_setup.FrameMalformed):
                    upstream_setup.decode_request_frame(bad_frame)

    def test_response_round_trip(self) -> None:
        addresses = [
            (upstream_setup._FAMILY_INET, "127.0.0.1"),
            (upstream_setup._FAMILY_INET6, "2001:db8::1"),
        ]
        frame = upstream_setup.encode_response_frame(addresses=addresses)
        raw = self._raw(frame)
        self.assertLessEqual(
            len(raw), upstream_setup.RESPONSE_FRAME_MAX_BYTES
        )
        self.assertEqual(upstream_setup.decode_response_frame(raw), addresses)

    def test_response_failure_frame(self) -> None:
        frame = upstream_setup.encode_failure_frame()
        self.assertEqual(
            upstream_setup.decode_response_frame(self._raw(frame)), []
        )

    def test_response_encode_bounds(self) -> None:
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.encode_response_frame(
                addresses=[(1, "127.0.0.1")] * 17
            )
        self.assertLessEqual(
            len(
                self._raw(
                upstream_setup.encode_response_frame(
                    addresses=[
                        (upstream_setup._FAMILY_INET, f"10.0.0.{i}")
                        for i in range(16)
                    ]
                )
                )
            ),
            upstream_setup.RESPONSE_FRAME_MAX_BYTES,
        )
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.encode_response_frame(
                addresses=[(upstream_setup._FAMILY_INET, "h" * 65)]
            )
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.encode_response_frame(addresses=[(3, "10.0.0.1")])
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.encode_response_frame(
                addresses=[
                    (upstream_setup._FAMILY_INET, "10.0.0.1"),
                    (upstream_setup._FAMILY_INET, "10.0.0.1"),
                ]
            )

    def test_response_decode_rejections(self) -> None:
        good = self._raw(
            upstream_setup.encode_response_frame(
                addresses=[(upstream_setup._FAMILY_INET, "127.0.0.1")]
            )
        )
        failures = [
            good[:-1],  # truncated
            good + b"x",  # extra data
            b"\x00" * (upstream_setup.RESPONSE_FRAME_MAX_BYTES + 1),
            b"\x00" * 5,
        ]
        for frame in failures:
            with self.assertRaises(upstream_setup.FrameMalformed):
                upstream_setup.decode_response_frame(frame)
        header = struct.Struct(">4sBBBH")

        def with_header(**changes: object) -> bytes:
            values: dict[str, object] = dict(
                magic=b"USTX", version=1, kind=2, status=0, count=1
            )
            values.update(changes)
            packed: list[object] = [
                values["magic"], values["version"], values["kind"],
                values["status"], values["count"],
            ]
            return header.pack(*packed) + b"\x01\x09" + b"127.0.0.1"

        # identity / status / count deviations
        for frame in (
            with_header(magic=b"USTY"),
            with_header(version=2),
            with_header(kind=1),
            with_header(status=2),
            with_header(count=0),
            with_header(count=17),
        ):
            with self.assertRaises(upstream_setup.FrameMalformed):
                upstream_setup.decode_response_frame(frame)
        # status-OK frame with no entries (the encoder allows the
        # degenerate frame; the decoder must reject it)
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_response_frame(
                header.pack(b"USTX", 1, 2, 0, 0)
            )
        # failure frame carrying data
        failed = header.pack(b"USTX", 1, 2, 1, 0) + b"\x01\x03abc"
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_response_frame(failed)
        # family byte disagrees with the address text (wrong kind)
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_response_frame(
                with_header().replace(
                    b"\x01\x09" + b"127.0.0.1",
                    b"\x02\x09" + b"127.0.0.1",
                    1,
                )
            )
        # address text that is not an IP literal
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_response_frame(
                header.pack(b"USTX", 1, 2, 0, 1)
                + b"\x01\x09"
                + b"localhost"
            )
        # non-UTF8 address bytes
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_response_frame(
                header.pack(b"USTX", 1, 2, 0, 1) + b"\x01\x02" + b"\xff\xfe"
            )
        # zero-length address
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_response_frame(
                header.pack(b"USTX", 1, 2, 0, 1) + b"\x01\x00"
            )
        # duplicate entries
        dup = header.pack(b"USTX", 1, 2, 0, 2) + (
            b"\x01\x09" + b"127.0.0.1"
        ) * 2
        with self.assertRaises(upstream_setup.FrameMalformed):
            upstream_setup.decode_response_frame(dup)


class SetupGuardLifecycleTests(unittest.TestCase):
    """Order 022-a requirement 3: the owned pure-timer guard."""

    def test_release_before_expiry_cancels_pending_timer(self) -> None:
        a, b = socket.socketpair()
        try:
            guard = upstream_setup.SetupGuard(time.monotonic() + 0.25)
            self.assertTrue(guard.adopt(a))
            self.assertFalse(guard.release())
            # Past the anchored deadline: the cancelled timer must
            # not interrupt the socket after release.
            time.sleep(0.6)
            a.send(b"x")
            self.assertEqual(b.recv(1), b"x")
        finally:
            a.close()
            b.close()
        self.assertEqual(_guard_threads(), [])

    def test_expiry_interrupts_only_the_exact_adopted_socket(self) -> None:
        a, b = socket.socketpair()
        c, d = socket.socketpair()
        try:
            guard = upstream_setup.SetupGuard(time.monotonic() + 0.2)
            self.assertTrue(guard.adopt(a))
            time.sleep(0.5)
            self.assertTrue(guard.is_expired())
            with self.assertRaises(OSError):
                a.send(b"x")
            self.assertEqual(b.recv(1), b"")
            # A different live socket pair is untouched.
            c.send(b"y")
            self.assertEqual(d.recv(1), b"y")
            # Post-expiry adopt refuses: the new socket is not
            # re-targeted and not interrupted.
            self.assertFalse(guard.adopt(c))
            c.send(b"z")
            self.assertEqual(d.recv(1), b"z")
            self.assertTrue(guard.release())
            self.assertTrue(guard.release())
        finally:
            a.close()
            b.close()
            c.close()
            d.close()
        self.assertEqual(_guard_threads(), [])

    def test_nonfinite_deadline_rejected(self) -> None:
        for bad in (float("inf"), float("-inf"), float("nan")):
            with self.assertRaises(ValueError):
                upstream_setup.SetupGuard(bad)
        self.assertEqual(_guard_threads(), [])

    def test_past_deadline_guard_refuses_adoption(self) -> None:
        guard = upstream_setup.SetupGuard(time.monotonic() - 1)
        try:
            a, b = socket.socketpair()
            try:
                self.assertFalse(guard.adopt(a))
            finally:
                a.close()
                b.close()
            self.assertTrue(guard.is_expired())
        finally:
            guard.release()
        self.assertEqual(_guard_threads(), [])

    def test_no_thread_growth_over_many_guards(self) -> None:
        baseline = len(_guard_threads())
        for _ in range(5):
            guard = upstream_setup.SetupGuard(time.monotonic() + 30)
            guard.release()
        self.assertEqual(len(_guard_threads()), baseline)
        self.assertEqual(_guard_threads(), [])

    def test_release_actually_joins_the_exact_guard_thread(self) -> None:
        with mock.patch.object(threading, "Thread", _JoinObservingThread):
            _JoinObservingThread.created.clear()
            guard = upstream_setup.SetupGuard(time.monotonic() + 30)
            a, b = socket.socketpair()
            try:
                self.assertTrue(guard.adopt(a))
                self.assertFalse(guard.release())
            finally:
                a.close()
                b.close()
        self.assertEqual(len(_JoinObservingThread.created), 1)
        thread = _JoinObservingThread.created[0]
        self.assertIs(guard._guard, thread)
        # release() really joined the exact known worker.
        self.assertGreaterEqual(len(thread.join_calls), 1)
        self.assertEqual(_guard_threads(), [])


class _JoinObservingThread(threading.Thread):
    """Real Thread with a transparent call-through join observation:
    every join() is recorded on the exact known instance before the
    real join runs - never a fake successful join."""

    created: list[_JoinObservingThread] = []

    def __init__(self, *args: object, **kwargs: object) -> None:
        base_init = cast("Callable[..., None]", super().__init__)
        base_init(*args, **kwargs)
        self.join_calls: list[float] = []
        type(self).created.append(self)

    def join(self, timeout: float | None = None) -> None:
        self.join_calls.append(time.monotonic())
        super().join(timeout)


class _StartedThenFailing(_JoinObservingThread):
    """Real start, then an injected startup failure (still running)."""

    def start(self) -> None:
        super().start()
        raise RuntimeError("injected startup failure")


class _EndedThenFailing(_JoinObservingThread):
    """Real start, forced to end, then the injected failure.  The
    fixture's own pre-failure join is recorded first; any further
    join on the same instance is the production cleanup join."""

    def start(self) -> None:
        self._target = None
        super().start()
        self.join()
        raise RuntimeError("injected startup failure")


class _NeverStartedFailing(_JoinObservingThread):
    """Injected failure before the thread ever starts."""

    def start(self) -> None:
        raise RuntimeError("injected startup failure")


class SetupGuardPartialStartupTests(unittest.TestCase):
    """Order 022-a requirement 3: partial-startup containment, proven
    by actual owner join observations on the exact known thread."""

    def _expect_injected_failure(
        self, thread_cls: type[_JoinObservingThread]
    ) -> _JoinObservingThread:
        thread_cls.created.clear()
        with mock.patch.object(threading, "Thread", thread_cls), self.assertRaises(
            RuntimeError
        ) as ctx:
            upstream_setup.SetupGuard(time.monotonic() + 30)
        self.assertEqual(str(ctx.exception), "injected startup failure")
        self.assertEqual(len(thread_cls.created), 1)
        return thread_cls.created[0]

    def test_started_then_failed_guard_is_cancelled_and_joined(self) -> None:
        thread = self._expect_injected_failure(_StartedThenFailing)
        # The owner really joined the exact known still-running
        # worker (at least one recorded call-through join).
        self.assertGreaterEqual(len(thread.join_calls), 1)
        self.assertEqual(_guard_threads(), [])

    def test_already_ended_guard_gets_additional_owner_join(self) -> None:
        thread = self._expect_injected_failure(_EndedThenFailing)
        # Exactly one recorded join is the fixture's own
        # pre-failure join; the mandated production cleanup join is
        # an ADDITIONAL call on the same known thread.
        self.assertGreaterEqual(len(thread.join_calls), 2)
        self.assertEqual(_guard_threads(), [])

    def test_never_started_thread_is_never_joined(self) -> None:
        thread = self._expect_injected_failure(_NeverStartedFailing)
        # Zero owner join calls on the known never-started thread:
        # a swallowed join RuntimeError would still be recorded.
        self.assertEqual(thread.join_calls, [])
        self.assertEqual(_guard_threads(), [])


class PartialPipeAllocationTests(unittest.TestCase):
    """Order 022-a requirement 3: owned cleanup over the pipe
    allocation/startup stage itself, using known real FDs."""

    def _first_pipe_with_second_allocation_failure(
        self, fail: BaseException
    ) -> tuple[list[int], BaseException | None]:
        real_pipe = os.pipe
        captured: dict[str, tuple[int, int]] = {}

        def flaky_pipe() -> tuple[int, int]:
            if "pair" not in captured:
                pair = real_pipe()
                captured["pair"] = pair
                return pair
            raise fail

        with mock.patch.object(os, "pipe", flaky_pipe):
            try:
                upstream_setup.resolve_addresses(
                    "localhost", 1, time.monotonic() + 5
                )
                return (
                    list(captured["pair"]) if "pair" in captured else [],
                    None,
                )
            except BaseException as exc:
                return (
                    list(captured["pair"]) if "pair" in captured else [],
                    exc,
                )

    def test_ordinary_error_closes_the_first_pipe(self) -> None:
        fds, exc = self._first_pipe_with_second_allocation_failure(
            OSError(24, "EMFILE")
        )
        self.assertEqual(len(fds), 2)
        self.assertIsInstance(exc, upstream_setup.UpstreamSetupError)
        self.assertEqual(
            cast(upstream_setup.UpstreamSetupError, exc).reason,
            upstream_setup.REASON_TRANSPORT,
        )
        for fd in fds:
            with self.assertRaises(OSError):
                os.fstat(fd)

    def test_caller_interruption_propagates_and_closes(self) -> None:
        fds, exc = self._first_pipe_with_second_allocation_failure(
            KeyboardInterrupt()
        )
        self.assertEqual(len(fds), 2)
        self.assertIsInstance(exc, KeyboardInterrupt)
        for fd in fds:
            with self.assertRaises(OSError):
                os.fstat(fd)


# Owned resolver-child scripts: the parent's deadline governs these
# real subprocesses; every one is reaped by the product before the
# call returns.  Synthetic fixture data only.
_SLOW_CHILD = """import sys
import time
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
time.sleep(@DELAY@)
frame = us.encode_response_frame(
    addresses=[(us._FAMILY_INET, "127.0.0.1")]
)
sys.stdout.buffer.write(frame)
sys.stdout.buffer.flush()
"""

_RACING_EXIT_CHILD = """import sys
import time
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
frame = us.encode_response_frame(
    addresses=[(us._FAMILY_INET, "127.0.0.1")]
)
sys.stdout.buffer.write(frame)
sys.stdout.buffer.flush()
time.sleep(@SLEEP@)
"""

_TRAILING_CHILD = """import sys
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
frame = us.encode_response_frame(
    addresses=[(us._FAMILY_INET, "127.0.0.1")]
)
sys.stdout.buffer.write(frame + b"X")
sys.stdout.buffer.flush()
"""

_NONZERO_CHILD = """import sys
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
frame = us.encode_response_frame(
    addresses=[(us._FAMILY_INET, "127.0.0.1")]
)
sys.stdout.buffer.write(frame)
sys.stdout.buffer.flush()
sys.exit(5)
"""

_FAILURE_CHILD = """import sys
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
sys.stdout.buffer.write(us.encode_failure_frame())
sys.stdout.buffer.flush()
"""

_CALLTHROUGH_CHILD = """import socket
import sys
import time
sys.path.insert(0, "@ROOT@")
_orig = socket.getaddrinfo
def _slow(host, port, *args, **kwargs):
    time.sleep(@DELAY@)
    return _orig(host, port, *args, **kwargs)
socket.getaddrinfo = _slow
import upstream_setup as us
sys.exit(us.worker_main())
"""


def _spy_popen() -> tuple[
    Callable[[], mock._patch[object]],
    list[tuple[tuple[object, ...], dict[str, object]]],
    list[subprocess.Popen[bytes]],
]:
    # Transparent real-construction forwarding over the owned start
    # seam: capture the original Popen.__init__ before patching,
    # forward it unchanged, and record the exact pre-allocated
    # process object (recorded even when the real construction
    # fails, so a spawn failure proves no child exists).
    real_init = subprocess.Popen.__init__
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
    procs: list[subprocess.Popen[bytes]] = []

    def tracked_init(
        self: subprocess.Popen[bytes],
        args: list[str],
        *,
        stdin: int | None = None,
        stdout: int | None = None,
        stderr: int | None = None,
        env: dict[str, str] | None = None,
        close_fds: bool = True,
    ) -> None:
        calls.append(
            (
                (args,),
                {
                    "stdin": stdin,
                    "stdout": stdout,
                    "stderr": stderr,
                    "env": env,
                    "close_fds": close_fds,
                },
            )
        )
        procs.append(self)
        real_init(
            self,
            args,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            env=env,
            close_fds=close_fds,
        )

    def spy() -> mock._patch[object]:
        return mock.patch.object(subprocess.Popen, "__init__", tracked_init)

    return spy, calls, procs


class ResolverChildTests(unittest.TestCase):
    """Order 022-a requirement 4: the real owned resolver child."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_child(self, name: str, template: str, **values: object) -> Path:
        body = template
        for key, value in values.items():
            body = body.replace(f"@{key}@", str(value))
        path = self.root / name
        path.write_text(body, encoding="utf-8")
        return path

    def _child_argv_patch(self, script: Path) -> mock._patch[Callable[[], list[str]]]:
        argv = [sys.executable, "-I", "-S", "-B", str(script)]
        return mock.patch.object(
            upstream_setup, "_resolver_argv", lambda: list(argv)
        )

    def test_ip_literal_fast_path_needs_no_child(self) -> None:
        spy, _calls, procs = _spy_popen()
        with spy():
            self.assertEqual(
                upstream_setup.resolve_addresses(
                    "127.0.0.1", 80, time.monotonic() + 5
                ),
                [(socket.AF_INET, "127.0.0.1")],
            )
            self.assertEqual(
                upstream_setup.resolve_addresses(
                    "10.9.8.7", 80, time.monotonic() + 5
                ),
                [(socket.AF_INET, "10.9.8.7")],
            )
            self.assertEqual(
                upstream_setup.resolve_addresses(
                    "2001:db8::1", 80, time.monotonic() + 5
                ),
                [(socket.AF_INET6, "2001:db8::1")],
            )
        self.assertEqual(procs, [])

    def test_real_child_argv_env_and_reaping(self) -> None:
        spy, calls, procs = _spy_popen()
        with spy():
            addresses = upstream_setup.resolve_addresses(
                "localhost", 80, time.monotonic() + 10
            )
        self.assertEqual(len(procs), 1)
        self.assertEqual(len(calls), 1)
        args, kwargs = calls[0]
        self.assertEqual(
            args[0],
            [sys.executable, "-I", "-S", "-B", str(ROOT / "upstream_worker.py")],
        )
        self.assertEqual(kwargs.get("env"), {})
        self.assertIs(kwargs.get("close_fds"), True)
        self.assertEqual(kwargs.get("stderr"), subprocess.DEVNULL)
        self.assertIn("stdin", kwargs)
        self.assertIn("stdout", kwargs)
        for family, address in addresses:
            self.assertIn(family, (socket.AF_INET, socket.AF_INET6))
            value = ipaddress.ip_address(address)
            self.assertTrue(value.is_loopback)
        proc = procs[0]
        self.assertIsNotNone(proc.poll())
        self.assertEqual(proc.returncode, 0)

    def test_spawn_failure_is_bounded_transport(self) -> None:
        spy, _calls, procs = _spy_popen()
        with (
            mock.patch.object(
                upstream_setup,
                "_resolver_argv",
                lambda: ["/nonexistent/concept-resolver-child", "-I"],
            ),
            spy(),
            self.assertRaises(upstream_setup.UpstreamSetupError) as ctx,
        ):
            upstream_setup.resolve_addresses(
                "localhost", 1, time.monotonic() + 5
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_TRANSPORT)
        # The pre-allocated instance is recorded.  On this platform
        # the failed construction still forks a child whose exec
        # fails, so its pid is set; whichever the spawn path takes,
        # the product must actually reap that exact child before
        # return - no zombie survives a failed start.
        self.assertEqual(len(procs), 1)
        failed_proc = procs[0]
        if getattr(failed_proc, "pid", None) is not None:
            self.assertIsNotNone(failed_proc.poll())

    def test_deadline_rejects_late_valid_frame(self) -> None:
        script = self._write_child(
            "slow.py", _SLOW_CHILD, ROOT=ROOT, DELAY=0.6
        )
        spy, _calls, procs = _spy_popen()
        with (
            self._child_argv_patch(script),
            spy(),
            self.assertRaises(upstream_setup.UpstreamSetupError) as ctx,
        ):
            upstream_setup.resolve_addresses(
                "localhost", 1, time.monotonic() + 0.25
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_DEADLINE)
        self.assertEqual(len(procs), 1)
        proc = procs[0]
        self.assertIsNotNone(proc.poll())
        self.assertNotEqual(proc.returncode, 0)

    def test_deadline_rejects_racing_exit_after_valid_frame(self) -> None:
        # The valid frame arrives in time; the child's completion
        # (exit) races past the anchored deadline and must lose.
        script = self._write_child(
            "racing.py", _RACING_EXIT_CHILD, ROOT=ROOT, SLEEP=0.5
        )
        spy, _calls, procs = _spy_popen()
        with (
            self._child_argv_patch(script),
            spy(),
            self.assertRaises(upstream_setup.UpstreamSetupError) as ctx,
        ):
            upstream_setup.resolve_addresses(
                "localhost", 1, time.monotonic() + 0.25
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_DEADLINE)
        self.assertEqual(len(procs), 1)
        proc = procs[0]
        self.assertIsNotNone(proc.poll())
        self.assertNotEqual(proc.returncode, 0)

    def test_trailing_byte_after_frame_is_rejected(self) -> None:
        script = self._write_child(
            "trailing.py", _TRAILING_CHILD, ROOT=ROOT
        )
        spy, _calls, procs = _spy_popen()
        with (
            self._child_argv_patch(script),
            spy(),
            self.assertRaises(upstream_setup.UpstreamSetupError) as ctx,
        ):
            upstream_setup.resolve_addresses(
                "localhost", 1, time.monotonic() + 5
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_TRANSPORT)
        # The parent rejects the extra byte BEFORE waiting for exit,
        # so the child either finished 0 first or was terminated
        # while still alive; both are actually reaped.
        self.assertIsNotNone(procs[0].poll())
        self.assertIn(procs[0].returncode, (0, -15))

    def test_nonzero_child_exit_is_rejected(self) -> None:
        script = self._write_child(
            "nonzero.py", _NONZERO_CHILD, ROOT=ROOT
        )
        spy, _calls, procs = _spy_popen()
        with (
            self._child_argv_patch(script),
            spy(),
            self.assertRaises(upstream_setup.UpstreamSetupError) as ctx,
        ):
            upstream_setup.resolve_addresses(
                "localhost", 1, time.monotonic() + 5
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_TRANSPORT)
        self.assertEqual(procs[0].returncode, 5)

    def test_malformed_frames_are_rejected(self) -> None:
        template = """import sys
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
frame = us.encode_response_frame(
    addresses=[(us._FAMILY_INET, "127.0.0.1")]
)
sys.stdout.buffer.write(@PAYLOAD@)
sys.stdout.buffer.flush()
"""
        for name, payload in (
            ("garbage.py", 'b"not-a-frame-at-all-garbage"'),
            ("truncated.py", "frame[:14]"),
        ):
            script = self._write_child(
                name, template, ROOT=ROOT, PAYLOAD=payload
            )
            spy, _calls, procs = _spy_popen()
            with (
                self._child_argv_patch(script),
                spy(),
                self.assertRaises(
                    upstream_setup.UpstreamSetupError
                ) as ctx,
            ):
                upstream_setup.resolve_addresses(
                    "localhost", 1, time.monotonic() + 5
                )
            self.assertEqual(
                ctx.exception.reason, upstream_setup.REASON_TRANSPORT, name
            )
            # Rejection lands before the exit wait: the child either
            # exited 0 first or was terminated while still alive.
            self.assertIsNotNone(procs[0].poll(), name)
            self.assertIn(procs[0].returncode, (0, -15), name)

    def test_failure_frame_is_bounded_transport(self) -> None:
        script = self._write_child(
            "failure.py", _FAILURE_CHILD, ROOT=ROOT
        )
        spy, _calls, procs = _spy_popen()
        with (
            self._child_argv_patch(script),
            spy(),
            self.assertRaises(upstream_setup.UpstreamSetupError) as ctx,
        ):
            upstream_setup.resolve_addresses(
                "localhost", 1, time.monotonic() + 5
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_TRANSPORT)
        self.assertEqual(procs[0].returncode, 0)

    def test_callthrough_delay_late_and_gentle_positive(self) -> None:
        # Same controlled call-through producer: a 0.6 s resolver
        # loses to a 0.25 s budget; a 0.2 s delay succeeds under a
        # generous budget.
        late = self._write_child(
            "late.py", _CALLTHROUGH_CHILD, ROOT=ROOT, DELAY=0.6
        )
        spy, _calls, procs = _spy_popen()
        with (
            self._child_argv_patch(late),
            spy(),
            self.assertRaises(upstream_setup.UpstreamSetupError) as ctx,
        ):
            upstream_setup.resolve_addresses(
                "localhost", 1, time.monotonic() + 0.25
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_DEADLINE)
        self.assertIsNotNone(procs[0].poll())
        self.assertNotEqual(procs[0].returncode, 0)

        gentle = self._write_child(
            "gentle.py", _CALLTHROUGH_CHILD, ROOT=ROOT, DELAY=0.2
        )
        spy, _calls, procs = _spy_popen()
        with (
            self._child_argv_patch(gentle),
            spy(),
        ):
            addresses = upstream_setup.resolve_addresses(
                "localhost", 1, time.monotonic() + 5
            )
        self.assertEqual(len(procs), 1)
        self.assertEqual(procs[0].returncode, 0)
        for _family, address in addresses:
            self.assertTrue(ipaddress.ip_address(address).is_loopback)


class ResolverStartInterruptionTests(unittest.TestCase):
    """Order 022-a requirement 3: caller interruption during the
    real Popen start seam, before and after actual child creation,
    on the actual parent/production-worker boundary.  A transparent
    _execute_child call-through performs the real child creation
    and then injects the interrupt; a scheduler-hold SIGSTOP models
    a held child.  Every test that can leave a known real child
    carries a failure-safe finally that resumes/terminates/kills
    and actually reaps ONLY that test's known pid, so a product
    regression cannot orphan a child or turn a failing assertion
    into a pass; the potentially-hanging held-child scenario
    additionally runs under a finite owned parent supervisor of an
    isolated process group with a terminate/kill escape for the
    exact known tree.  Controlled fault evidence only: no claim of
    spontaneous native failure, and no DNS/HTTP/model call."""

    _HELD_CHILD_SUPERVISOR = """import contextlib
import json
import os
import signal
import subprocess
import sys
import time

sys.path.insert(0, "@ROOT@")
import upstream_setup  # noqa: E402


def _closed(fd):
    try:
        os.fstat(fd)
        return False
    except OSError:
        return True


def _fds():
    return set(os.listdir("/proc/self/fd"))


real_execute = subprocess.Popen._execute_child
captured = {}


def fault_execute(self, *args, **kwargs):
    real_execute(self, *args, **kwargs)
    pid = self.pid
    captured["pid"] = pid
    captured["proc"] = self
    os.kill(pid, signal.SIGSTOP)
    time.sleep(0.05)
    stat = open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1]
    captured["state"] = stat.split()[0]
    raise KeyboardInterrupt("controlled start interruption")


before = _fds()
real_pipe = os.pipe
pairs = []


def recording_pipe():
    pair = real_pipe()
    pairs.append(pair)
    return pair


os.pipe = recording_pipe
subprocess.Popen._execute_child = fault_execute
try:
    upstream_setup.resolve_addresses(
        "localhost", 80, time.monotonic() + 10
    )
    print("RESULT " + json.dumps({"ok": False, "why": "no-interrupt"}))
    sys.exit(2)
except KeyboardInterrupt as exc:
    result = {"ok": "controlled start interruption" in str(exc)}
    pid = captured.get("pid")
    if isinstance(pid, int):
        try:
            os.waitpid(pid, os.WNOHANG)
            result["reaped"] = False
            result["why"] = "child-not-reaped"
        except ChildProcessError:
            result["reaped"] = True
    result["fds_closed"] = all(
        _closed(fd) for pair in pairs for fd in pair
    )
    result["no_new_fd"] = before.issuperset(_fds())
    result["state"] = captured.get("state")
    print("RESULT " + json.dumps(result))
    sys.exit(0 if result.get("ok") and result.get("reaped") else 4)
finally:
    # Script-side failure-safe cleanup of the known worker AFTER
    # every observation: on a product regression the stopped
    # worker must not survive this process; the failed rc above is
    # kept, never converted into a pass by the cleanup.
    proc = captured.get("proc")
    if isinstance(proc, subprocess.Popen) and proc.poll() is None:
        with contextlib.suppress(OSError):
            proc.send_signal(signal.SIGCONT)
        with contextlib.suppress(OSError):
            proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(OSError):
                proc.kill()
            proc.wait(timeout=10)
"""

    def _owned_fds(self) -> set[int]:
        return {int(name) for name in os.listdir("/proc/self/fd")}

    def _pipe_recorder(
        self,
    ) -> tuple[list[tuple[int, int]], object]:
        real_pipe = os.pipe
        pairs: list[tuple[int, int]] = []

        def recording_pipe() -> tuple[int, int]:
            pair = real_pipe()
            pairs.append(pair)
            return pair

        return pairs, recording_pipe

    def _assert_owned_fds_closed(
        self, before: set[int], pairs: list[tuple[int, int]]
    ) -> None:
        # Main proof: every known owned pipe descriptor is closed
        # (EBADF).  The FD set diff is supplementary only.
        for pair in pairs:
            for fd in pair:
                with self.assertRaises(OSError):
                    os.fstat(fd)
        self.assertTrue(before.issuperset(self._owned_fds()))

    def _fail_safe_reap_known_child(self, captured: dict[str, object]) -> None:
        """Failure-safe cleanup for this test's known real child:
        when the actual Popen object retained at construction still
        reports a live child, resume, terminate, SIGKILL-escalate,
        and actually wait it with a bounded timeout; an already
        ended/reaped child is a no-op.  It signals only the exact
        known object (no global waitpid, no pid-recycling risk),
        and it never converts a failing product assertion into a
        pass: assertions run before this cleanup, which only
        prevents an orphaned known child."""
        proc = captured.get("proc")
        if not isinstance(proc, subprocess.Popen):
            return
        if proc.poll() is None:
            with contextlib.suppress(OSError):
                proc.send_signal(signal.SIGCONT)
            with contextlib.suppress(OSError):
                proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(OSError):
                proc.kill()
            proc.wait(timeout=10)
        self.assertIsNotNone(proc.poll())

    def _run_supervised_tree(
        self, script: Path, parent_bound: float
    ) -> tuple[int, str, str]:
        """Finite owned parent supervision of an owned process
        group: the supervised child starts its own session, so the
        nested owned worker shares the child's process group and a
        forced escape terminates/kills the exact known tree
        (including a stopped member).  A forced escape is a FAILED
        outcome, never a partial pass (order 022-a, requirement 7);
        the final group kill is unconditional on escape because a
        stopped member cannot process TERM after the leader exited,
        so cleanup never depends on leader liveness or pipe EOF."""
        proc = subprocess.Popen(
            [sys.executable, "-I", "-B", str(script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            timed_out = False
            try:
                out, err = proc.communicate(timeout=parent_bound)
            except subprocess.TimeoutExpired:
                timed_out = True
                with contextlib.suppress(OSError):
                    os.killpg(proc.pid, signal.SIGTERM)
                try:
                    out, err = proc.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    with contextlib.suppress(OSError):
                        os.killpg(proc.pid, signal.SIGKILL)
                    out, err = proc.communicate(timeout=5)
            if timed_out:
                # Unconditional final kill of the exact owned group
                # and bounded reap of the leader before the FAILED
                # outcome: a SIGSTOPped nested member cannot process
                # the TERM above even after the leader exited (the
                # leader's EOF returns the second communicate early),
                # so the escape must not depend on the leader still
                # being alive.
                with contextlib.suppress(OSError):
                    os.killpg(proc.pid, signal.SIGKILL)
                with contextlib.suppress(subprocess.TimeoutExpired):
                    proc.wait(timeout=10)
                self.fail(
                    "owned supervised start-interruption tree exceeded "
                    f"the finite parent bound {parent_bound}s and was "
                    "terminated/killed/reaped: the product did not reap "
                    "the held child. stderr tail: "
                    + err.decode("utf-8", "replace")[-2000:]
                )
            self.assertIsNotNone(proc.returncode)
            return (
                proc.returncode,
                out.decode("utf-8", "replace"),
                err.decode("utf-8", "replace"),
            )
        finally:
            # Owned group cleanup/reap on EVERY outcome (natural
            # exit, nonzero exit, forced escape, unexpected
            # exception): the isolated start_new_session group
            # confines this to the exact owned tree, and for an
            # already-exited group the killpg is a no-op.
            with contextlib.suppress(OSError):
                os.killpg(proc.pid, signal.SIGKILL)
            proc.wait(timeout=10)

    def test_interruption_before_child_creation_leaves_no_child(self) -> None:
        real_init = subprocess.Popen.__init__
        captured: dict[str, object] = {}

        def tracking_init(
            self: subprocess.Popen[bytes],
            args: list[str],
            *,
            stdin: int | None = None,
            stdout: int | None = None,
            stderr: int | None = None,
            env: dict[str, str] | None = None,
            close_fds: bool = True,
        ) -> None:
            captured["instance"] = self
            real_init(
                self,
                args,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                env=env,
                close_fds=close_fds,
            )

        def fault_execute(
            self: subprocess.Popen[bytes], *args: object, **kwargs: object
        ) -> None:
            # Interrupt BEFORE any child can be created: the only
            # fork/spawn step inside the real construction is
            # replaced, never called.
            raise KeyboardInterrupt("controlled pre-fork interruption")

        before = self._owned_fds()
        pairs, recording_pipe = self._pipe_recorder()
        with (
            mock.patch.object(subprocess.Popen, "__init__", tracking_init),
            mock.patch.object(
                subprocess.Popen, "_execute_child", fault_execute
            ),
            mock.patch.object(os, "pipe", recording_pipe),
            self.assertRaises(KeyboardInterrupt) as ctx,
        ):
            upstream_setup.resolve_addresses(
                "localhost", 80, time.monotonic() + 10
            )
        self.assertIn(
            "controlled pre-fork interruption", str(ctx.exception)
        )
        # The exact pre-allocated object from the intercepted
        # construction has no pid: the real fork step was never
        # reached, so no child exists to wait for (the product
        # cleanup must not wait on the never-created state).
        instance = captured.get("instance")
        self.assertIsInstance(instance, subprocess.Popen)
        self.assertIsNone(getattr(instance, "pid", None))
        self._assert_owned_fds_closed(before, pairs)

    def test_interruption_after_ended_child_reaps_without_signal(self) -> None:
        real_execute = getattr(subprocess.Popen, "_execute_child")  # noqa: B009 - untyped seam
        flexible_execute = cast("Callable[..., None]", real_execute)
        captured: dict[str, object] = {}

        def fault_execute(
            self: subprocess.Popen[bytes], *args: object, **kwargs: object
        ) -> None:
            flexible_execute(self, *args, **kwargs)
            pid = self.pid
            captured["pid"] = pid
            captured["proc"] = self
            os.kill(pid, signal.SIGKILL)
            # Establish the actual known-PID exit WITHOUT reaping
            # it (bounded WNOWAIT observation), so the interrupt
            # lands on an already-ended child; a ChildProcessError
            # here would mean an early reap: invalid fixture.
            end_deadline = time.monotonic() + 5
            while True:
                try:
                    observed = os.waitid(
                        os.P_PID,
                        pid,
                        os.WEXITED | os.WNOWAIT | os.WNOHANG,
                    )
                except ChildProcessError:
                    raise AssertionError(
                        "known child was reaped before the "
                        "controlled post-exit observation"
                    ) from None
                if observed is not None:
                    # The known-PID exit event is observed WITHOUT
                    # reaping it; the caller interruption now lands
                    # on the already-ended child.
                    raise KeyboardInterrupt(
                        "controlled post-exit interruption"
                    )
                if time.monotonic() >= end_deadline:
                    raise AssertionError(
                        "known child did not end under SIGKILL "
                        "within the bounded observation"
                    )
                time.sleep(0.01)

        real_terminate = subprocess.Popen.terminate
        real_kill = subprocess.Popen.kill

        def rec_terminate(self: subprocess.Popen[bytes]) -> None:
            if getattr(self, "pid", None) == captured.get("pid"):
                captured["terminated"] = True
            real_terminate(self)

        def rec_kill(self: subprocess.Popen[bytes]) -> None:
            if getattr(self, "pid", None) == captured.get("pid"):
                captured["killed"] = True
            real_kill(self)

        before = self._owned_fds()
        pairs, recording_pipe = self._pipe_recorder()
        try:
            with (
                mock.patch.object(
                    subprocess.Popen, "_execute_child", fault_execute
                ),
                mock.patch.object(
                    subprocess.Popen, "terminate", rec_terminate
                ),
                mock.patch.object(subprocess.Popen, "kill", rec_kill),
                mock.patch.object(os, "pipe", recording_pipe),
                self.assertRaises(KeyboardInterrupt) as ctx,
            ):
                upstream_setup.resolve_addresses(
                    "localhost", 80, time.monotonic() + 10
                )
            self.assertIn(
                "controlled post-exit interruption", str(ctx.exception)
            )
            pid = cast(int, captured["pid"])
            # The already-ended child is actually reaped BEFORE
            # this test's own cleanup: no zombie remains.
            with self.assertRaises(ChildProcessError):
                os.waitpid(pid, os.WNOHANG)
            # The product reaped it on its first poll: no
            # terminate/kill signal reached the known object.
            self.assertNotIn("terminated", captured)
            self.assertNotIn("killed", captured)
            self._assert_owned_fds_closed(before, pairs)
        finally:
            self._fail_safe_reap_known_child(captured)

    def test_held_child_under_finite_supervised_tree(self) -> None:
        # The potentially-hanging held-child scenario under a
        # finite owned parent supervisor of an isolated process
        # group: the natural outcome is the supervised child's own
        # exit 0 after the product reaped the held worker; a
        # regressed product is contained by the bounded tree
        # escape and reported FAILED, never partially passed.
        temp = tempfile.TemporaryDirectory()
        try:
            script = Path(temp.name) / "held_child_supervisor.py"
            script.write_text(
                self._HELD_CHILD_SUPERVISOR.replace("@ROOT@", str(ROOT)),
                encoding="utf-8",
            )
            code, out, err = self._run_supervised_tree(script, 30.0)
            self.assertEqual(code, 0, err)
            value = HangingNativeSupervisedTests._result_line(out)
            self.assertTrue(value.get("ok"), value)
            self.assertTrue(value.get("reaped"), value)
            self.assertTrue(value.get("fds_closed"), value)
            self.assertTrue(value.get("no_new_fd"), value)
            self.assertEqual(value.get("state"), "T", value)
        finally:
            temp.cleanup()

    @staticmethod
    def _faulting_popen(
        failure: MemoryError | KeyboardInterrupt,
    ) -> object:
        """Throwaway Popen subclass whose allocation always fails
        with the exact controlled exception instance.  The instance
        is bound as a parameter (not a loop variable), and the
        subclass is bound to the module attribute for one call: the
        real Popen class and its special slots are never mutated,
        so the next real Popen construction is uncontaminated."""

        class _FaultingPopen(subprocess.Popen[bytes]):
            def __new__(
                cls, *args: object, **kwargs: object
            ) -> NoReturn:
                raise failure

        return _FaultingPopen

    def test_preallocation_failure_closes_pipes_without_child(self) -> None:
        # A failure of the pre-allocation itself - before any child
        # can exist - must still close every owned pipe descriptor
        # for both an allocation error and a caller interruption;
        # the original exception is preserved, and the
        # never-created state is never waited on (a known
        # unreaped zombie child of this test process must not be
        # stolen by a blanket waitpid).
        for failure in (
            MemoryError("controlled allocation failure"),
            KeyboardInterrupt("controlled pre-allocation interruption"),
        ):

            fault_popen = self._faulting_popen(failure)
            sentinel = subprocess.Popen(
                [sys.executable, "-I", "-S", "-B", "-c", "pass"]
            )
            z_deadline = time.monotonic() + 5
            while True:
                stat = Path(f"/proc/{sentinel.pid}/stat").read_text()
                state = stat.rsplit(")", 1)[1].split()[0]
                if state == "Z":
                    break
                if time.monotonic() >= z_deadline:
                    sentinel.kill()
                    sentinel.wait()
                    self.fail("sentinel child did not end in bound")
                time.sleep(0.01)

            before = self._owned_fds()
            pairs, recording_pipe = self._pipe_recorder()
            try:
                with (
                    mock.patch.object(subprocess, "Popen", fault_popen),
                    mock.patch.object(os, "pipe", recording_pipe),
                    self.assertRaises(type(failure)) as ctx,
                ):
                    upstream_setup.resolve_addresses(
                        "localhost", 80, time.monotonic() + 10
                    )
                self.assertIs(ctx.exception, failure)
                # The known unreaped zombie is still pending: the
                # never-created state was not waited on.
                self.assertTrue(
                    Path(f"/proc/{sentinel.pid}/stat").exists()
                )
                self._assert_owned_fds_closed(before, pairs)
            finally:
                sentinel.wait()


# ------------------------------------------------------------------
# Owned loopback fixtures for the real forward setup phases.
# Synthetic wire data only; every server/thread is actually joined.


class _OwnedThreadingServer(ThreadingHTTPServer):
    """Owned loopback HTTP server: every request handler is a known
    non-daemon thread retained for an asserted actual join.

    ``listener_rcvbuf``, when set, is applied to the listening
    socket BEFORE listen: the accepted connections inherit that
    initial receive window (setting the buffer on the accepted
    socket later is not the same initial advertised window).
    ``accepted_rcvbuf`` keeps the previous explicit per-accepted-
    socket bound.
    """

    listener_rcvbuf: int | None = None
    accepted_rcvbuf: int | None = 262_144

    def server_bind(self) -> None:
        super().server_bind()
        if self.__class__.listener_rcvbuf is not None:
            with suppress(OSError):
                self.socket.setsockopt(
                    socket.SOL_SOCKET,
                    socket.SO_RCVBUF,
                    self.__class__.listener_rcvbuf,
                )

    def __init__(
        self,
        address: tuple[str, int],
        handler: type[BaseHTTPRequestHandler],
    ) -> None:
        super().__init__(address, handler)
        self.handler_threads: list[threading.Thread] = []
        self.live_requests: list[socket.socket] = []

    def process_request(
        self, request: object, client_address: tuple[str, int]
    ) -> None:
        # Bound the server-side receive window explicitly so a stalled
        # or slow-reading peer cannot hide upload bytes in a large
        # kernel buffer; the deadline - not buffer size - is what the
        # test proves.
        sock = cast("socket.socket", request)
        if self.__class__.accepted_rcvbuf is not None:
            with suppress(OSError):
                sock.setsockopt(
                    socket.SOL_SOCKET,
                    socket.SO_RCVBUF,
                    self.__class__.accepted_rcvbuf,
                )

        def run() -> None:
            try:
                self.process_request_thread(sock, client_address)
            finally:
                with suppress(ValueError):
                    self.live_requests.remove(sock)

        self.live_requests.append(sock)
        thread = threading.Thread(
            target=run, daemon=False, name="setup-test-handler"
        )
        self.handler_threads.append(thread)
        thread.start()


class _RecordingMain(BaseHTTPRequestHandler):
    """Owned main upstream with selectable body-read behavior:
    ``normal`` (read and answer), ``paced`` (read in bounded chunks
    with a fixed inter-chunk delay) or ``none`` (never read the body
    and hold the connection without answering)."""

    protocol_version = "HTTP/1.1"
    status: int = 200
    content_type: str = "application/json"
    source: bytes = b"{}"
    read_mode: str = "normal"
    read_delay: float = 0.0
    body_hold: float = 0.0
    stop_event: threading.Event | None = None
    recorded: list[dict[str, object]] = []
    first_body_at: float | None = None
    last_body_at: float | None = None

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        if self.__class__.read_mode == "none":
            stop = self.__class__.stop_event
            while stop is not None and not stop.is_set():
                time.sleep(0.05)
            return
        if self.__class__.body_hold:
            # R6 matched producer: fixture hold between the header
            # read and the body read (identical for the short and
            # generous budgets).
            time.sleep(self.__class__.body_hold)
        body = b""
        while len(body) < length:
            # Read at most the actual remaining declared bytes: a
            # larger request would wait for bytes beyond
            # Content-Length on the persistent connection.
            chunk = self.rfile.read(min(65536, length - len(body)))
            if not chunk:
                break
            if self.__class__.first_body_at is None:
                self.__class__.first_body_at = time.monotonic()
            self.__class__.last_body_at = time.monotonic()
            body += chunk
            if self.__class__.read_delay:
                time.sleep(self.__class__.read_delay)
        self.__class__.recorded.append(
            {
                "path": self.path,
                "headers": dict(self.headers.items()),
                "body": body,
            }
        )
        self.send_response(self.__class__.status)
        self.send_header("Content-Type", self.__class__.content_type)
        self.send_header("Content-Length", str(len(self.__class__.source)))
        self.end_headers()
        self.wfile.write(self.__class__.source)

    def log_message(self, *_args: object) -> None:
        return


@contextmanager
def _http_server(
    stop_event: threading.Event | None = None,
    read_mode: str = "normal",
    read_delay: float = 0.0,
    port: int = 0,
    body_hold: float = 0.0,
    listener_rcvbuf: int | None = None,
    accepted_rcvbuf: int | None = 262_144,
) -> Iterator[_OwnedThreadingServer]:
    handler = _RecordingMain
    handler.recorded = []
    handler.read_mode = read_mode
    handler.read_delay = read_delay
    handler.body_hold = body_hold
    handler.stop_event = stop_event
    handler.first_body_at = None
    handler.last_body_at = None
    _OwnedThreadingServer.listener_rcvbuf = listener_rcvbuf
    _OwnedThreadingServer.accepted_rcvbuf = accepted_rcvbuf
    server = _OwnedThreadingServer(("127.0.0.1", port), handler)
    thread = threading.Thread(
        target=server.serve_forever, daemon=False, name="setup-test-serve"
    )
    thread.start()
    try:
        yield server
    finally:
        if stop_event is not None:
            stop_event.set()
        server.shutdown()
        thread.join(10)
        assert not thread.is_alive(), "owned serve_forever thread not ended"
        # Known shutdown/close of every still-live accepted
        # fixture socket BEFORE the handler joins: a handler
        # blocked in a keep-alive read is woken by its own
        # socket, not left to the join timeout.
        for request_sock in list(server.live_requests):
            with suppress(OSError):
                request_sock.shutdown(socket.SHUT_RDWR)
            with suppress(OSError):
                request_sock.close()
        for handler_thread in server.handler_threads:
            handler_thread.join(10)
            assert not handler_thread.is_alive(), (
                "owned handler thread not ended"
            )
        server.server_close()


def _make_self_signed_cert(directory: Path) -> tuple[Path, Path]:
    key = directory / "key.pem"
    cert = directory / "cert.pem"
    subprocess.run(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
            "-keyout", str(key), "-out", str(cert), "-days", "1",
            "-subj", "/CN=127.0.0.1",
            "-addext", "subjectAltName=IP:127.0.0.1",
        ],
        check=True,
        capture_output=True,
    )
    return cert, key


def _read_http_request(tls: ssl.SSLSocket) -> bytes:
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = tls.recv(65536)
        if not chunk:
            break
        data += chunk
    head, _, rest = data.partition(b"\r\n\r\n")
    length = 0
    for line in head.split(b"\r\n"):
        if line.lower().startswith(b"content-length:"):
            length = int(line.split(b":", 1)[1].strip())
    while len(rest) < length:
        chunk = tls.recv(65536)
        if not chunk:
            break
        rest += chunk
    return head + rest


def _tls_acceptor(
    cert: Path,
    key: Path,
    *,
    stall: bool = False,
    stall_first_only: bool = False,
    stall_delay: float = 0.0,
) -> tuple[socket.socket, threading.Thread, threading.Event, dict[str, object]]:
    """Owned raw TLS acceptor.

    The accept loop uses a bounded socket timeout (closing the
    listener from another thread need not wake a blocked accept), the
    ClientHello byte is observed with MSG_PEEK (never consumed, so the
    real SSL stream stays intact), and every owned accepted socket,
    the listener and the thread are stopped/closed/joined on all
    paths.  ``stall`` holds every accepted connection after the
    non-consuming observation; ``stall_first_only`` stalls connection
    #1 and serves later ones (same-proxy recovery).
    """
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    ctx.set_alpn_protocols(["http/1.1"])
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(2)
    listener.settimeout(0.2)
    stop = threading.Event()
    connections = 0
    observed: dict[str, object] = {"connections": 0, "current_conn": None}

    def loop() -> None:
        nonlocal connections
        while not stop.is_set():
            try:
                conn, _addr = listener.accept()
            except TimeoutError:
                continue
            except OSError:
                return
            connections += 1
            count = connections
            observed["connections"] = count
            observed["current_conn"] = conn
            stall_this = stall or (stall_first_only and count == 1)
            # The accepted socket gets a bounded read/handshake
            # lifetime: the accept-loop timeout alone does not cap
            # a blocking handshake on the accepted socket.
            conn.settimeout(5.0)
            try:
                with suppress(OSError):
                    first = conn.recv(1, socket.MSG_PEEK)
                observed[f"hello_{count}"] = first
                if stall_this:
                    while not stop.is_set():
                        time.sleep(0.05)
                    continue
                if stall_delay:
                    # Fixed finite hold after the non-consuming
                    # observation, before the handshake: the R6
                    # matched producer (identical for the short and
                    # generous budgets).
                    hold_until = time.monotonic() + stall_delay
                    while time.monotonic() < hold_until:
                        time.sleep(0.02)
                tls = ctx.wrap_socket(conn, server_side=True)
                # The wrap detaches the raw socket: track the
                # wrapped object for the pre-join close.
                observed["current_conn"] = tls
                try:
                    observed[f"alpn_{count}"] = tls.selected_alpn_protocol()
                    observed[f"request_{count}"] = _read_http_request(tls)
                    body = b'{"ok":true}'
                    head = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/json\r\n"
                        f"Content-Length: {len(body)}\r\n"
                        "Connection: close\r\n\r\n"
                    ).encode() + body
                    tls.sendall(head)
                finally:
                    with suppress(OSError):
                        tls.close()
            except (OSError, ssl.SSLError):
                pass
            finally:
                observed["current_conn"] = None
                # Explicitly close the exact raw socket on EVERY
                # path (after the wrapped object, where one was
                # created); clearing the tracker alone is not a
                # close.
                with suppress(OSError):
                    conn.close()

    thread = threading.Thread(
        target=loop, daemon=False, name="setup-test-tls-acceptor"
    )
    thread.start()
    return listener, thread, stop, observed


def _close_tls_acceptor(
    listener: socket.socket,
    thread: threading.Thread,
    stop: threading.Event,
    observed: dict[str, object],
) -> None:
    stop.set()
    # Close/shutdown the exact live owned connection BEFORE the
    # join: the acceptor thread may be inside the bounded-but-
    # blocked handshake or read on that socket.
    current = observed.get("current_conn")
    if isinstance(current, socket.socket):
        with suppress(OSError):
            current.close()
    thread.join(5)
    assert not thread.is_alive(), "owned TLS acceptor thread not ended"
    with suppress(OSError):
        listener.close()


def _snbuf_socket_factory(
    snbuf: int,
) -> tuple[Callable[..., socket.socket], list[socket.socket]]:
    """Transparent call-through around socket.socket: every created
    socket is the real one, with a bounded send window set before
    first use.  This lets a permitted-size payload (<=
    API_MAX_REQUEST_BYTES) actually meet backpressure on loopback;
    it observes, never replaces, the real transport."""
    real_socket = socket.socket
    created: list[socket.socket] = []

    def factory(
        family: int,
        type: int = socket.SOCK_STREAM,
        proto: int = 0,
        fileno: int | None = None,
    ) -> socket.socket:
        # socket.accept() creates the accepted socket through the same
        # class call (fileno=...): forward transparently.  The bounded
        # send window applies to client-created sockets only.
        sock = real_socket(family, type, proto, fileno)
        if fileno is None:
            with suppress(OSError):
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, snbuf)
        created.append(sock)
        return sock

    return factory, created


def _phase_call_through(
    fn: Callable[..., object], marks: dict[str, float], name: str
) -> Callable[..., object]:
    """Transparent call-through around a product phase function: the
    original function executes unchanged; its entry and its
    successful return are timed against the anchored clock.  A
    failing call records its entry only, so a successful local write
    completion is never confused with a write failure (the request
    phase returns only after the last body byte is handed to the
    local transport)."""

    def wrapper(*args: object, **kwargs: object) -> object:
        marks[f"{name}_start"] = time.monotonic()
        result = fn(*args, **kwargs)
        marks[f"{name}_end"] = time.monotonic()
        return result

    return wrapper


_TWO_ADDRESS_CHILD = """import sys
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
frame = us.encode_response_frame(
    addresses=[
        (us._FAMILY_INET, "@DEAD@"),
        (us._FAMILY_INET, "@LIVE@"),
    ]
)
sys.stdout.buffer.write(frame)
sys.stdout.buffer.flush()
"""

_SETUP_BODY = b'{"model":"m","input":"x","store":false,"stream":false}'
# Permitted request payloads (<= API_MAX_REQUEST_BYTES = 2 000 000);
# backpressure comes from the bounded owned socket buffers, never
# from an over-cap request.  Sizes are measured, not nominal.
_UPLOAD_BODY = b"0" * 1_500_000
_CLIENT_SNDBUF = 262_144
_SERVER_RCVBUF = 262_144


class SetupForwardPhaseTests(unittest.TestCase):
    """Order 022-a requirement 6: the real forward setup phases.

    Direct-helper proof (``open_upstream_connection``); every body is
    within the permitted request cap and its length is asserted."""

    def _open_http(
        self,
        server_port: int,
        *,
        host: str = "127.0.0.1",
        body: bytes = _SETUP_BODY,
        deadline: float | None = None,
        capture_timeout: float = 10,
        nodelay_out: list[int] | None = None,
    ) -> tuple[int, bytes]:
        if deadline is None:
            deadline = time.monotonic() + 10
        connection = upstream_setup.open_upstream_connection(
            scheme="http",
            host=host,
            port=server_port,
            request_path="/v1/responses",
            body=body,
            headers={"Content-Type": "application/json"},
            deadline=deadline,
            capture_timeout=capture_timeout,
        )
        try:
            if nodelay_out is not None and connection.sock is not None:
                nodelay_out.append(
                    cast("socket.socket", connection.sock).getsockopt(
                        socket.IPPROTO_TCP, socket.TCP_NODELAY
                    )
                )
            response = connection.getresponse()
            payload = response.read()
            return response.status, payload
        finally:
            connection.close()

    def _owned_dead_endpoint(self) -> tuple[socket.socket, int]:
        # A reserved loopback endpoint: bound but non-listening, held
        # alive through the attempt, so the refused-connect proof does
        # not assume an unrelated port is free.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.2", 0))
        return sock, sock.getsockname()[1]

    def test_baseline_http_request_write(self) -> None:
        nodelay: list[int] = []
        with _http_server() as server:
            status, payload = self._open_http(
                server.server_port, nodelay_out=nodelay
            )
        self.assertEqual(status, 200)
        # The original connected-socket transport profile is
        # preserved by the new owned connector.
        self.assertEqual(nodelay, [1])
        self.assertEqual(payload, b"{}")
        self.assertEqual(len(_RecordingMain.recorded), 1)
        record = _RecordingMain.recorded[0]
        self.assertEqual(record["path"], "/v1/responses")
        self.assertEqual(record["body"], _SETUP_BODY)
        headers = cast(dict[str, str], record["headers"])
        self.assertEqual(headers.get("Content-Type"), "application/json")
        self.assertEqual(headers.get("Content-Length"), str(len(_SETUP_BODY)))
        self.assertEqual(_guard_threads(), [])

    def test_dead_port_is_bounded_transport(self) -> None:
        dead, dead_port = self._owned_dead_endpoint()
        try:
            with self.assertRaises(upstream_setup.UpstreamSetupError) as ctx:
                upstream_setup.open_upstream_connection(
                    scheme="http",
                    host="127.0.0.2",
                    port=dead_port,
                    request_path="/v1/responses",
                    body=_SETUP_BODY,
                    headers={},
                    deadline=time.monotonic() + 5,
                    capture_timeout=5,
                )
        finally:
            dead.close()
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_TRANSPORT)
        self.assertEqual(_guard_threads(), [])

    def test_invalid_scheme_is_bounded_transport(self) -> None:
        with self.assertRaises(upstream_setup.UpstreamSetupError) as ctx:
            upstream_setup.open_upstream_connection(
                scheme="ftp",
                host="127.0.0.1",
                port=1,
                request_path="/v1/responses",
                body=_SETUP_BODY,
                headers={},
                deadline=time.monotonic() + 5,
                capture_timeout=5,
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_TRANSPORT)

    def test_past_deadline_is_deadline(self) -> None:
        with self.assertRaises(upstream_setup.UpstreamSetupError) as ctx:
            upstream_setup.open_upstream_connection(
                scheme="http",
                host="127.0.0.1",
                port=1,
                request_path="/v1/responses",
                body=_SETUP_BODY,
                headers={},
                deadline=time.monotonic() - 1,
                capture_timeout=5,
            )
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_DEADLINE)

    def test_bounded_connect_attempts_dead_then_live(self) -> None:
        # Named host (the IP-literal fast path is NOT taken): the
        # owned child is actually spawned and reports the reserved
        # dead loopback address first and the live address second.
        # The dead endpoint is an owned bound non-listening socket
        # held through the attempt; the live server is bound on the
        # SAME port at 127.0.0.1.  Bounded attempts: the dead connect
        # is refused, the live connect completes, exactly one POST,
        # no retry.
        dead, port = self._owned_dead_endpoint()
        temp = tempfile.TemporaryDirectory()
        try:
            script = Path(temp.name) / "two_addr.py"
            script.write_text(
                _TWO_ADDRESS_CHILD.replace("@ROOT@", str(ROOT))
                .replace("@DEAD@", "127.0.0.2")
                .replace("@LIVE@", "127.0.0.1"),
                encoding="utf-8",
            )
            argv = [sys.executable, "-I", "-S", "-B", str(script)]
            spy, calls, procs = _spy_popen()
            with (
                mock.patch.object(upstream_setup, "_resolver_argv", lambda: list(argv)),
                spy(),
                _http_server(port=port) as server,
            ):
                status, payload = self._open_http(
                    server.server_port, host="localhost"
                )
            self.assertEqual(status, 200)
            self.assertEqual(payload, b"{}")
            # The named resolver path was actually used: one real
            # owned child, actually reaped.
            self.assertEqual(len(procs), 1)
            self.assertIsNotNone(procs[0].poll())
            self.assertEqual(procs[0].returncode, 0)
            # Exactly one POST on the live endpoint, no retry.
            self.assertEqual(len(_RecordingMain.recorded), 1)
            # The reserved dead endpoint never saw an established
            # connection (connect was refused, not accepted).
            dead.settimeout(0.3)
            with self.assertRaises(OSError):
                dead.accept()
        finally:
            dead.close()
            temp.cleanup()
        self.assertEqual(_guard_threads(), [])

    def test_all_dead_addresses_are_transport(self) -> None:
        dead, dead_port = self._owned_dead_endpoint()
        try:
            with self.assertRaises(upstream_setup.UpstreamSetupError) as ctx:
                upstream_setup.open_upstream_connection(
                    scheme="http",
                    host="127.0.0.2",
                    port=dead_port,
                    request_path="/v1/responses",
                    body=_SETUP_BODY,
                    headers={},
                    deadline=time.monotonic() + 5,
                    capture_timeout=5,
                )
        finally:
            dead.close()
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_TRANSPORT)
        self.assertEqual(_guard_threads(), [])

    def test_real_tls_handshake_completes_under_gentle_budget(self) -> None:
        temp = tempfile.TemporaryDirectory()
        try:
            cert, key = _make_self_signed_cert(Path(temp.name))
        except BaseException:
            temp.cleanup()
            raise
        listener, thread, stop, observed = _tls_acceptor(cert, key)
        try:
            port = listener.getsockname()[1]
            with mock.patch.dict(os.environ, {"SSL_CERT_FILE": str(cert)}):
                connection = upstream_setup.open_upstream_connection(
                    scheme="https",
                    host="127.0.0.1",
                    port=port,
                    request_path="/v1/responses",
                    body=_SETUP_BODY,
                    headers={"Content-Type": "application/json"},
                    deadline=time.monotonic() + 10,
                    capture_timeout=10,
                )
                try:
                    # Capture the negotiated ALPN while the handshake
                    # socket is still attached (a closed-delta response
                    # detaches it on completion).
                    alpn = cast(
                        "ssl.SSLSocket", connection.sock
                    ).selected_alpn_protocol()
                    nodelay = cast("socket.socket", connection.sock).getsockopt(
                        socket.IPPROTO_TCP, socket.TCP_NODELAY
                    )
                    response = connection.getresponse()
                    payload = response.read()
                finally:
                    connection.close()
        finally:
            _close_tls_acceptor(listener, thread, stop, observed)
        temp.cleanup()
        self.assertEqual(response.status, 200)
        self.assertEqual(payload, b'{"ok":true}')
        # The intact TLS record negotiated the real ALPN profile and
        # the full HTTP request (including body) reached the peer.
        self.assertEqual(alpn, "http/1.1")
        self.assertEqual(nodelay, 1)
        self.assertEqual(observed["alpn_1"], "http/1.1")
        request = cast("bytes", observed["request_1"])
        self.assertIn(b"POST /v1/responses HTTP/1.1", request)
        self.assertIn(_SETUP_BODY, request)
        self.assertEqual(_guard_threads(), [])

    def test_tls_untrusted_ca_is_bounded_transport(self) -> None:
        temp = tempfile.TemporaryDirectory()
        other = tempfile.TemporaryDirectory()
        try:
            cert, key = _make_self_signed_cert(Path(temp.name))
            other_cert, _other_key = _make_self_signed_cert(Path(other.name))
        except BaseException:
            temp.cleanup()
            other.cleanup()
            raise
        listener, thread, stop, observed = _tls_acceptor(cert, key)
        try:
            port = listener.getsockname()[1]
            # The client trust reference is a DIFFERENT self-signed
            # certificate: the original stdlib trust profile must
            # reject the server certificate (verification, not a
            # corrupted record).
            with mock.patch.dict(
                os.environ, {"SSL_CERT_FILE": str(other_cert)}
            ), self.assertRaises(
                upstream_setup.UpstreamSetupError
            ) as ctx:
                upstream_setup.open_upstream_connection(
                    scheme="https",
                    host="127.0.0.1",
                    port=port,
                    request_path="/v1/responses",
                    body=_SETUP_BODY,
                    headers={"Content-Type": "application/json"},
                    deadline=time.monotonic() + 10,
                    capture_timeout=10,
                )
        finally:
            _close_tls_acceptor(listener, thread, stop, observed)
        temp.cleanup()
        other.cleanup()
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_TRANSPORT)
        self.assertEqual(observed["connections"], 1)
        self.assertEqual(observed["hello_1"], b"\x16")
        self.assertEqual(_guard_threads(), [])

    def test_nonreading_upload_gentle_positive(self) -> None:
        factory, _created = _snbuf_socket_factory(_CLIENT_SNDBUF)
        with mock.patch.object(socket, "socket", factory), _http_server(
            read_mode="normal"
        ) as server:
            status, payload = self._open_http(
                server.server_port, body=_UPLOAD_BODY
            )
        self.assertEqual(status, 200)
        self.assertEqual(payload, b"{}")
        # The ENTIRE permitted payload reached the peer.
        self.assertEqual(_RecordingMain.recorded[0]["body"], _UPLOAD_BODY)
        self.assertEqual(_guard_threads(), [])

    def test_slowreading_upload_gentle_positive(self) -> None:
        # R6/R7 matched producer: genuinely backpressured paced
        # producer (64 KiB chunks, 40 ms apart) over small owned
        # buffers set BEFORE connect/listen (32768 client sndbuf,
        # 32768 listener rcvbuf inherited by the accepted peer):
        # the ACTUAL local write duration is governed by the paced
        # peer reader and completes under the generous budget.
        # The matched short-budget negative of this SAME producer
        # runs under the explicit finite parent boundary in
        # test_supervised_slowreading_upload_short_budget (the
        # in-process blocker duplicate was removed: a regressed
        # deadline must not be able to hang the suite).
        factory, _created = _snbuf_socket_factory(32_768)
        with (
            mock.patch.object(socket, "socket", factory),
            _http_server(
                read_mode="normal",
                read_delay=0.04,
                listener_rcvbuf=32_768,
                accepted_rcvbuf=None,
            ) as server,
        ):
            status, _payload = self._open_http(server.server_port, body=_UPLOAD_BODY)
        self.assertEqual(status, 200)
        self.assertEqual(_RecordingMain.recorded[0]["body"], _UPLOAD_BODY)
        self.assertEqual(_guard_threads(), [])

    def test_cumulative_each_phase_fits_sum_expires(self) -> None:
        # Same finite producer for both budgets: a controlled
        # call-through resolver (1.0 s sleep lower bound plus real
        # spawn/IPC) and a paced upload (0.05 s per <= 64 KiB read)
        # over owned buffers set BEFORE connect/listen: client
        # SO_SNDBUF 32768 before the first connect, listener
        # SO_RCVBUF 32768 before listen (the accepted peer inherits
        # that initial advertised window; setting it on the accepted
        # socket later is not the same window).  With the small owned
        # buffers the kernel cannot absorb the 1.5 MiB body, so the
        # ACTUAL local write duration is genuinely governed by the
        # paced peer reader.  The GENEROUS run first MEASURES the
        # ACTUAL local setup phases of the real call: transparent
        # call-through wrappers around the product's OWN phase
        # functions (the original functions still execute unchanged)
        # time startup+resolver through the resolver return, the
        # bounded connect, and the request write through its local
        # write completion (the request-phase return - local write
        # completion, not peer receipt, which the separate
        # complete-body equality proves).  Each phase is below the
        # 2 s budget and their sum is over it (sleeps are lower
        # bounds, so the sum-over property holds on any machine); the
        # SAME producer under the 2 s budget must then expire mid-
        # write with real accepted/header/body progress.
        self.assertLessEqual(len(_UPLOAD_BODY), 2_000_000)
        temp = tempfile.TemporaryDirectory()
        try:
            script = Path(temp.name) / "resolver.py"
            script.write_text(
                _CALLTHROUGH_CHILD.replace("@ROOT@", str(ROOT)).replace(
                    "@DELAY@", "1.0"
                ),
                encoding="utf-8",
            )
            argv = [sys.executable, "-I", "-S", "-B", str(script)]
            # 1) Generous control: measure the actual local phases.
            marks: dict[str, float] = {}
            with (
                mock.patch.object(
                    upstream_setup, "_resolver_argv", lambda: list(argv)
                ),
                mock.patch.object(
                    upstream_setup,
                    "resolve_addresses",
                    _phase_call_through(
                        upstream_setup.resolve_addresses, marks, "resolve"
                    ),
                ),
                mock.patch.object(
                    upstream_setup,
                    "_connect_phase",
                    _phase_call_through(
                        upstream_setup._connect_phase, marks, "connect"
                    ),
                ),
                mock.patch.object(
                    upstream_setup,
                    "_request_phase",
                    _phase_call_through(
                        upstream_setup._request_phase, marks, "request"
                    ),
                ),
                _http_server(
                    read_mode="normal",
                    read_delay=0.05,
                    listener_rcvbuf=32_768,
                    accepted_rcvbuf=None,
                ) as server,
            ):
                factory, _created = _snbuf_socket_factory(32_768)
                with mock.patch.object(
                    socket, "socket", factory
                ):
                    t0 = time.monotonic()
                    status, _payload = self._open_http(
                        server.server_port,
                        host="localhost",
                        body=_UPLOAD_BODY,
                        deadline=time.monotonic() + 10,
                    )
            self.assertEqual(status, 200)
            phase1 = marks["resolve_end"] - t0
            phase2 = marks["connect_end"] - marks["resolve_end"]
            phase3 = marks["request_end"] - marks["connect_end"]
            self.assertLess(phase1, 2.0)
            self.assertLess(phase2, 2.0)
            self.assertLess(phase3, 2.0)
            self.assertGreater(marks["request_end"] - t0, 2.0)
            # Local write completion is not peer receipt: the ENTIRE
            # permitted payload nevertheless reached the peer.
            self.assertEqual(
                _RecordingMain.recorded[0]["body"], _UPLOAD_BODY
            )
            self.assertIsNotNone(_RecordingMain.first_body_at)
            self.assertIsNotNone(_RecordingMain.last_body_at)
            # 2) Same finite producer under the 2 s budget: the sum
            # of the same phases over the budget loses mid-write,
            # with real accepted/header/body progress observed.
            marks2: dict[str, float] = {}
            with (
                mock.patch.object(
                    upstream_setup, "_resolver_argv", lambda: list(argv)
                ),
                mock.patch.object(
                    upstream_setup,
                    "resolve_addresses",
                    _phase_call_through(
                        upstream_setup.resolve_addresses, marks2, "resolve"
                    ),
                ),
                mock.patch.object(
                    upstream_setup,
                    "_connect_phase",
                    _phase_call_through(
                        upstream_setup._connect_phase, marks2, "connect"
                    ),
                ),
                mock.patch.object(
                    upstream_setup,
                    "_request_phase",
                    _phase_call_through(
                        upstream_setup._request_phase, marks2, "request"
                    ),
                ),
                _http_server(
                    read_mode="normal",
                    read_delay=0.05,
                    listener_rcvbuf=32_768,
                    accepted_rcvbuf=None,
                ) as server,
            ):
                factory2, _created2 = _snbuf_socket_factory(32_768)
                with mock.patch.object(
                    socket, "socket", factory2
                ):
                    started = time.monotonic()
                    connection = None
                    try:
                        with self.assertRaises(
                            upstream_setup.UpstreamSetupError
                        ) as ctx:
                            connection = upstream_setup.open_upstream_connection(
                                scheme="http",
                                host="localhost",
                                port=server.server_port,
                                request_path="/v1/responses",
                                body=_UPLOAD_BODY,
                                headers={"Content-Type": "application/json"},
                                deadline=time.monotonic() + 2.0,
                                capture_timeout=30,
                            )
                    finally:
                        if connection is not None:
                            with suppress(Exception):
                                connection.close()
                    elapsed = time.monotonic() - started
        finally:
            temp.cleanup()
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_DEADLINE)
        self.assertLess(elapsed, 3.5)
        # The local request write never completed under the short
        # budget: the request-phase call-through recorded its entry
        # but never its successful return.
        self.assertIn("request_start", marks2)
        self.assertNotIn("request_end", marks2)
        # Real target-phase progress: the peer accepted the request
        # and a genuine prefix of the body, but not the whole body.
        self.assertEqual(len(_RecordingMain.recorded), 1)
        partial = cast("bytes", _RecordingMain.recorded[0]["body"])
        self.assertGreater(len(partial), 0)
        self.assertLess(len(partial), len(_UPLOAD_BODY))
        self.assertEqual(_guard_threads(), [])


    def test_tls_finite_hold_same_producer_short_budget(self) -> None:
        # R6 matched producer (see the generous-budget counterpart):
        # the acceptor waits one FIXED finite 2 s after observing the
        # ClientHello (never consuming it) before completing the real
        # handshake; the 1 s anchored budget expires inside that
        # hold.  The fixture never closes the blocker before the
        # proxy enforces its timeout: the hold simply ends after the
        # deadline, and the acceptor still serves later connections.
        temp = tempfile.TemporaryDirectory()
        try:
            cert, key = _make_self_signed_cert(Path(temp.name))
        except BaseException:
            temp.cleanup()
            raise
        listener, thread, stop, observed = _tls_acceptor(
            cert, key, stall_delay=2.0
        )
        try:
            port = listener.getsockname()[1]
            started = time.monotonic()
            with mock.patch.dict(
                os.environ, {"SSL_CERT_FILE": str(cert)}
            ), self.assertRaises(
                upstream_setup.UpstreamSetupError
            ) as ctx:
                upstream_setup.open_upstream_connection(
                    scheme="https",
                    host="127.0.0.1",
                    port=port,
                    request_path="/v1/responses",
                    body=_SETUP_BODY,
                    headers={"Content-Type": "application/json"},
                    deadline=time.monotonic() + 1.0,
                    capture_timeout=30,
                )
            elapsed = time.monotonic() - started
        finally:
            _close_tls_acceptor(listener, thread, stop, observed)
        temp.cleanup()
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_DEADLINE)
        self.assertLess(elapsed, 2.5)
        # The real ClientHello was observed before the fixed hold.
        self.assertEqual(observed["connections"], 1)
        self.assertEqual(observed["hello_1"], b"\x16")
        # The handshake never completed under the short budget.
        self.assertNotIn("alpn_1", observed)
        self.assertEqual(_guard_threads(), [])

    def test_tls_finite_hold_same_producer_generous_budget(self) -> None:
        # R6 matched producer: the SAME fixed 2 s hold (identical
        # producer configuration as the short-budget counterpart)
        # completes under the 10 s anchored budget: the real
        # handshake finishes after the hold, ALPN is negotiated and
        # the full request (headers + body) reaches the peer.
        temp = tempfile.TemporaryDirectory()
        try:
            cert, key = _make_self_signed_cert(Path(temp.name))
        except BaseException:
            temp.cleanup()
            raise
        listener, thread, stop, observed = _tls_acceptor(
            cert, key, stall_delay=2.0
        )
        try:
            port = listener.getsockname()[1]
            with mock.patch.dict(
                os.environ, {"SSL_CERT_FILE": str(cert)}
            ):
                connection = upstream_setup.open_upstream_connection(
                    scheme="https",
                    host="127.0.0.1",
                    port=port,
                    request_path="/v1/responses",
                    body=_SETUP_BODY,
                    headers={"Content-Type": "application/json"},
                    deadline=time.monotonic() + 10,
                    capture_timeout=30,
                )
                try:
                    response = connection.getresponse()
                    status = response.status
                    payload = response.read()
                finally:
                    connection.close()
        finally:
            _close_tls_acceptor(listener, thread, stop, observed)
        temp.cleanup()
        self.assertEqual(status, 200)
        self.assertEqual(payload, b'{"ok":true}')
        self.assertEqual(observed["connections"], 1)
        self.assertEqual(observed["hello_1"], b"\x16")
        self.assertEqual(observed["alpn_1"], "http/1.1")
        request = cast("bytes", observed["request_1"])
        self.assertIn(b"POST /v1/responses HTTP/1.1", request)
        self.assertIn(_SETUP_BODY, request)
        self.assertEqual(_guard_threads(), [])

    def test_body_hold_same_producer_short_budget(self) -> None:
        # R6 matched producer (see the generous-budget counterpart):
        # the owned main reads the request headers, then holds the
        # body unread for one FIXED finite 2 s; identical small
        # owned buffers (32768 client sndbuf before connect, 32768
        # listener rcvbuf before listen) keep the kernel from
        # absorbing the 1.5 MiB body.  The 1 s anchored budget
        # expires while the peer holds the body; the later post-hold
        # read then sees the in-flight prefix and the peer-severed
        # connection, so genuine header/body progress exists under
        # the short budget without any fixture premature close.
        stop = threading.Event()
        factory, _created = _snbuf_socket_factory(32_768)
        with (
            mock.patch.object(socket, "socket", factory),
            _http_server(
                stop_event=stop,
                read_mode="normal",
                body_hold=2.0,
                listener_rcvbuf=32_768,
                accepted_rcvbuf=None,
            ) as server,
        ):
            started = time.monotonic()
            connection = None
            try:
                with self.assertRaises(
                    upstream_setup.UpstreamSetupError
                ) as ctx:
                    connection = upstream_setup.open_upstream_connection(
                        scheme="http",
                        host="127.0.0.1",
                        port=server.server_port,
                        request_path="/v1/responses",
                        body=_UPLOAD_BODY,
                        headers={"Content-Type": "application/json"},
                        deadline=time.monotonic() + 1.0,
                        capture_timeout=30,
                    )
            finally:
                if connection is not None:
                    with suppress(Exception):
                        connection.close()
            elapsed = time.monotonic() - started
        self.assertEqual(ctx.exception.reason, upstream_setup.REASON_DEADLINE)
        self.assertLess(elapsed, 2.5)
        # Real progress under the short budget: the peer accepted
        # the request and a genuine (nonempty) body prefix reached
        # it before the deadline severed the connection, but not
        # the whole body.
        self.assertEqual(len(_RecordingMain.recorded), 1)
        partial = cast("bytes", _RecordingMain.recorded[0]["body"])
        self.assertGreater(len(partial), 0)
        self.assertLess(len(partial), len(_UPLOAD_BODY))
        self.assertEqual(_guard_threads(), [])

    def test_body_hold_same_producer_generous_budget(self) -> None:
        # R6 matched producer: the SAME fixed 2 s body hold and the
        # SAME small owned buffers complete under the 10 s anchored
        # budget: the peer reads the whole body after the hold and
        # answers 200 with the full exact body recorded.
        stop = threading.Event()
        factory, _created = _snbuf_socket_factory(32_768)
        with (
            mock.patch.object(socket, "socket", factory),
            _http_server(
                stop_event=stop,
                read_mode="normal",
                body_hold=2.0,
                listener_rcvbuf=32_768,
                accepted_rcvbuf=None,
            ) as server,
        ):
            started = time.monotonic()
            status, _payload = self._open_http(
                server.server_port, body=_UPLOAD_BODY
            )
            elapsed = time.monotonic() - started
        self.assertEqual(status, 200)
        self.assertLess(elapsed, 9.0)
        # The ENTIRE permitted payload reached the peer after the
        # hold.
        self.assertEqual(_RecordingMain.recorded[0]["body"], _UPLOAD_BODY)
        self.assertIsNotNone(_RecordingMain.first_body_at)
        self.assertIsNotNone(_RecordingMain.last_body_at)
        self.assertEqual(_guard_threads(), [])



# Order 022-a requirement 7: the REQUIRED native hanging/slow cases
# run in an owned finite parent-supervised ordinary test process with
# a bounded terminate/kill/reap escape.  The child is a plain stdlib
# scenario script (no AI); a forced escape is FAILED, never a partial
# pass.  The child installs a bounded faulthandler dump so a product
# regression exposes exact Python stacks before the parent deadline.
_HANG_TLS_CHILD = """import faulthandler
import json
import os
import socket
import ssl
import sys
import threading
import time
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
faulthandler.dump_traceback_later(@FAULT@, exit=False)
CERT = "@CERT@"
KEY = "@KEY@"
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("127.0.0.1", 0))
listener.listen(1)
listener.settimeout(0.2)
stop = threading.Event()
state = {"connections": 0, "hello": None, "conn": None}

def loop():
    while not stop.is_set():
        try:
            conn, _addr = listener.accept()
        except socket.timeout:
            continue
        except OSError:
            return
        state["connections"] += 1
        state["conn"] = conn
        conn.settimeout(5.0)
        try:
            state["hello"] = conn.recv(1, socket.MSG_PEEK)
        except OSError:
            pass
        while not stop.is_set():
            time.sleep(0.05)

thread = threading.Thread(target=loop, daemon=False)
thread.start()
port = listener.getsockname()[1]
os.environ["SSL_CERT_FILE"] = CERT
started = time.monotonic()
reason = None
try:
    us.open_upstream_connection(
        scheme="https",
        host="127.0.0.1",
        port=port,
        request_path="/v1/responses",
        body=b'{"model":"m","input":"x","store":false,"stream":false}',
        headers={"Content-Type": "application/json"},
        deadline=time.monotonic() + @BUDGET@,
        capture_timeout=@CAPTURE@,
    )
    reason = "COMPLETED"
except us.UpstreamSetupError as exc:
    reason = exc.reason
elapsed = time.monotonic() - started
stop.set()
conn = state["conn"]
if conn is not None:
    try:
        conn.close()
    except OSError:
        pass
listener.close()
thread.join(5)
result = {
    "reason": reason,
    "elapsed": elapsed,
    "connections": state["connections"],
    "hello": state["hello"].hex() if state["hello"] else None,
    "guard_threads": [
        t.name for t in threading.enumerate()
        if t.name == "concept-setup-guard"
    ],
}
print("RESULT " + json.dumps(result), flush=True)
"""

_HANG_UPLOAD_CHILD = """import faulthandler
import json
import socket
import sys
import threading
import time
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
faulthandler.dump_traceback_later(@FAULT@, exit=False)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 0))
server.listen(1)
server.settimeout(0.2)
stop = threading.Event()
state = {"accepted": 0, "headers": False, "conn": None}

def loop():
    while not stop.is_set():
        try:
            conn, _addr = server.accept()
        except socket.timeout:
            continue
        except OSError:
            return
        state["accepted"] += 1
        state["conn"] = conn
        conn.settimeout(0.5)
        data = b""
        while b"\\r\\n\\r\\n" not in data:
            try:
                chunk = conn.recv(65536)
            except (OSError, socket.timeout):
                break
            if not chunk:
                break
            data += chunk
        if b"\\r\\n\\r\\n" in data:
            state["headers"] = True
        while not stop.is_set():
            time.sleep(0.05)

thread = threading.Thread(target=loop, daemon=False)
thread.start()
port = server.getsockname()[1]
real_socket = us.socket.socket

def factory(family, type=socket.SOCK_STREAM, proto=0, fileno=None):
    sock = real_socket(family, type, proto, fileno)
    if fileno is None:
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 262144)
        except OSError:
            pass
    return sock

us.socket.socket = factory
body = b"0" * @BODYLEN@
started = time.monotonic()
reason = None
try:
    us.open_upstream_connection(
        scheme="http",
        host="127.0.0.1",
        port=port,
        request_path="/v1/responses",
        body=body,
        headers={"Content-Type": "application/json"},
        deadline=time.monotonic() + @BUDGET@,
        capture_timeout=@CAPTURE@,
    )
    reason = "COMPLETED"
except us.UpstreamSetupError as exc:
    reason = exc.reason
elapsed = time.monotonic() - started
stop.set()
conn = state["conn"]
if conn is not None:
    try:
        conn.close()
    except OSError:
        pass
server.close()
thread.join(5)
result = {
    "reason": reason,
    "elapsed": elapsed,
    "accepted": state["accepted"],
    "headers": state["headers"],
    "guard_threads": [
        t.name for t in threading.enumerate()
        if t.name == "concept-setup-guard"
    ],
}
print("RESULT " + json.dumps(result), flush=True)
"""


_HANG_SLOWREAD_CHILD = """import faulthandler
import json
import socket
import sys
import threading
import time
sys.path.insert(0, "@ROOT@")
import upstream_setup as us
faulthandler.dump_traceback_later(@FAULT@, exit=False)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 0))
try:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32768)
except OSError:
    pass
server.listen(1)
server.settimeout(0.2)
stop = threading.Event()
state = {"accepted": 0, "headers": False, "body_len": 0, "conn": None}


def loop():
    while not stop.is_set():
        try:
            conn, _addr = server.accept()
        except socket.timeout:
            continue
        except OSError:
            return
        state["accepted"] += 1
        state["conn"] = conn
        conn.settimeout(2.0)
        data = b""
        while b"\\r\\n\\r\\n" not in data:
            try:
                chunk = conn.recv(65536)
            except (OSError, socket.timeout):
                break
            if not chunk:
                break
            data += chunk
        if b"\\r\\n\\r\\n" in data:
            state["headers"] = True
        head, _, body = data.partition(b"\\r\\n\\r\\n")
        length = 0
        for line in head.split(b"\\r\\n"):
            if line.lower().startswith(b"content-length:"):
                length = int(line.split(b":", 1)[1].strip())
        while len(body) < length and not stop.is_set():
            try:
                chunk = conn.recv(min(65536, length - len(body)))
            except (OSError, socket.timeout):
                break
            if not chunk:
                break
            body += chunk
            time.sleep(@PACING@)
        state["body_len"] = len(body)
        if len(body) == length:
            try:
                conn.sendall(
                    b"HTTP/1.1 200 OK\\r\\n"
                    b"Content-Length: 2\\r\\n"
                    b"Connection: close\\r\\n\\r\\n"
                    b"{}"
                )
            except OSError:
                pass
        try:
            conn.close()
        except OSError:
            pass
        state["conn"] = None
        return


thread = threading.Thread(target=loop, daemon=False)
thread.start()
port = server.getsockname()[1]
real_socket = us.socket.socket


def factory(family, type=socket.SOCK_STREAM, proto=0, fileno=None):
    sock = real_socket(family, type, proto, fileno)
    if fileno is None:
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 32_768)
        except OSError:
            pass
    return sock


us.socket.socket = factory
body = b"0" * @BODYLEN@
started = time.monotonic()
reason = None
completed = False
try:
    connection = us.open_upstream_connection(
        scheme="http",
        host="127.0.0.1",
        port=port,
        request_path="/v1/responses",
        body=body,
        headers={"Content-Type": "application/json"},
        deadline=time.monotonic() + @BUDGET@,
        capture_timeout=@CAPTURE@,
    )
    response = connection.getresponse()
    payload = response.read()
    connection.close()
    completed = payload == b"{}"
    reason = "COMPLETED"
except us.UpstreamSetupError as exc:
    reason = exc.reason
elapsed = time.monotonic() - started
stop.set()
conn = state["conn"]
if conn is not None:
    try:
        conn.close()
    except OSError:
        pass
server.close()
thread.join(5)
result = {
    "reason": reason,
    "completed": completed,
    "elapsed": elapsed,
    "accepted": state["accepted"],
    "headers": state["headers"],
    "body_len": state["body_len"],
    "guard_threads": [
        t.name for t in threading.enumerate()
        if t.name == "concept-setup-guard"
    ],
}
print("RESULT " + json.dumps(result), flush=True)
"""


_RECOVERY_CHILD = """import faulthandler
import json
import socket
import sys
import tempfile
import threading
import time
sys.path.insert(0, "@ROOT@")
import proxy
import upstream_setup as us
from http.server import HTTPServer
from pathlib import Path
from qwen_client import ResponsesReviewer
from tests.test_capture_transport import CLEAN, _BUILD_UNIGRAM
from tests.test_responses_contract import _json_completed, _review_payload
from tests.test_review_batch import (
    _FakeUpstream,
    _contract_body,
    _real_spec,
)
from tests.test_runtime_corpus import _build_db
faulthandler.dump_traceback_later(@FAULT@, exit=False)

# The exact fixed content-free 502 body the handler's stdlib
# send_error(502) path emits on this interpreter (measured, not
# nominal): status line and headers aside, these bytes are the
# complete response body for a setup failure.
FIXED_502_BODY = (
    b'<!DOCTYPE HTML>\\n<html lang="en">\\n    <head>\\n'
    b'        <meta charset="utf-8">\\n'
    b'        <title>Error response</title>\\n'
    b'    </head>\\n'
    b'    <body>\\n'
    b'        <h1>Error response</h1>\\n'
    b'        <p>Error code: 502</p>\\n'
    b'        <p>Message: Bad Gateway.</p>\\n'
    b'        <p>Error code explanation: 502 - Invalid responses from another server/proxy.</p>\\n'
    b'    </body>\\n'
    b'</html>\\n'
)

# Transparent call-throughs: the real product starts/releases the
# owned guards; the observations only record the actual identities,
# the anchored deadline and the actual release outcome.
guard_threads = []
_real_start = threading.Thread.start
def _rec_start(self):
    if getattr(self, "name", None) == "concept-setup-guard":
        guard_threads.append(self)
    return _real_start(self)
deadlines = []
_real_guard_init = us.SetupGuard.__init__
def _rec_guard_init(self, deadline):
    _real_guard_init(self, deadline)
    deadlines.append(deadline)
releases = []
_real_guard_release = us.SetupGuard.release
def _rec_guard_release(self):
    outcome = _real_guard_release(self)
    releases.append(outcome)
    return outcome
threading.Thread.start = _rec_start
us.SetupGuard.__init__ = _rec_guard_init
us.SetupGuard.release = _rec_guard_release
# Actual Thread.join completion call-through: is_alive(False)
# proves ended, not that the caller actually joined.
joined_threads = []
_real_join = threading.Thread.join
def _rec_join(self, timeout=None):
    _real_join(self, timeout)
    joined_threads.append(self)
threading.Thread.join = _rec_join

temp = tempfile.TemporaryDirectory()
main_listener = None
main_thread = None
main_started = False
main_stop = threading.Event()
main_state = {"connections": 0}
review_server = None
review_thread = None
review_started = False
proxy_server = None
proxy_thread = None
proxy_started = False
try:
    db = Path(temp.name) / "recovery-child.sqlite"
    _build_db(db, unigram=_BUILD_UNIGRAM)
    answer = _json_completed(CLEAN)

    # Owned raw main: the FIRST connection is held unread for one
    # fixed finite time (longer than the 1 s setup budget), then
    # drained and answered; later connections are served immediately.
    # Finite producer: nothing here can hang the child.
    main_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_listener.bind(("127.0.0.1", 0))
    try:
        main_listener.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32768)
    except OSError:
        pass
    main_listener.listen(2)
    main_listener.settimeout(0.2)
    main_port = main_listener.getsockname()[1]

    def _main_loop():
        while not main_stop.is_set():
            try:
                conn, _addr = main_listener.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            main_state["connections"] += 1
            first = main_state["connections"] == 1
            try:
                if first:
                    hold_until = time.monotonic() + 1.5
                    while time.monotonic() < hold_until:
                        time.sleep(0.02)
                conn.settimeout(5.0)
                data = b""
                while b"\\r\\n\\r\\n" not in data:
                    try:
                        chunk = conn.recv(65536)
                    except (OSError, socket.timeout):
                        break
                    if not chunk:
                        break
                    data += chunk
                length = 0
                for line in data.split(b"\\r\\n"):
                    if line.lower().startswith(b"content-length:"):
                        length = int(line.split(b":", 1)[1].strip())
                _, _, rest = data.partition(b"\\r\\n\\r\\n")
                while len(rest) < length:
                    try:
                        chunk = conn.recv(min(65536, length - len(rest)))
                    except (OSError, socket.timeout):
                        break
                    if not chunk:
                        break
                    rest += chunk
                head = (
                    "HTTP/1.1 200 OK\\r\\n"
                    "Content-Type: application/json\\r\\n"
                    f"Content-Length: {len(answer)}\\r\\n"
                    "Connection: close\\r\\n\\r\\n"
                ).encode()
                conn.sendall(head + answer)
            except OSError:
                pass
            finally:
                try:
                    conn.close()
                except OSError:
                    pass

    main_thread = threading.Thread(target=_main_loop, daemon=False)
    main_thread.start()
    main_started = True

    # Reachable synthetic review endpoint; the scenario must leave
    # it with zero recorded calls.
    _FakeUpstream.status = 200
    _FakeUpstream.delay = 0.0
    _FakeUpstream.payload = _review_payload(
        [{"id": "t0", "keep": True, "replacement": None, "accepted": False}]
    )
    _FakeUpstream.recorded = []
    review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
    review_thread = threading.Thread(
        target=review_server.serve_forever, daemon=False
    )
    review_thread.start()
    review_started = True

    reviewer = ResponsesReviewer(
        f"http://127.0.0.1:{review_server.server_port}/v1",
        "test-model",
        timeout=5.0,
        api_key="recovery-child-review-key",
    )
    engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
    repairs = []
    _base_repair = engine.repair
    def _rec_repair(text):
        repairs.append(text)
        return _base_repair(text)
    engine.repair = _rec_repair

    proxy_server = proxy.ConceptProxy(
        ("127.0.0.1", 0),
        f"http://127.0.0.1:{main_port}",
        engine,
        setup_timeout=1.0,
    )
    proxy_thread = threading.Thread(
        target=proxy_server.serve_forever, daemon=False
    )
    proxy_thread.start()
    proxy_started = True
    proxy_port = proxy_server.server_port

    # Bounded client send window BEFORE connect: the contract-valid
    # 1,800,053-byte first request (150,000 decoded input
    # codepoints, JSON surrogate-escaped) genuinely stalls on the
    # unread hold over the bounded owned buffers.
    _real_socket = socket.socket
    def _factory(family, type=socket.SOCK_STREAM, proto=0, fileno=None):
        sock = _real_socket(family, type, proto, fileno)
        if fileno is None:
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 32_768)
            except OSError:
                pass
        return sock
    socket.socket = _factory

    import http.client
    def _post(port, body, headers):
        client = http.client.HTTPConnection("127.0.0.1", port, timeout=30)
        try:
            client.request("POST", "/v1/responses", body=body, headers=headers)
            response = client.getresponse()
            return response.status, response.read()
        finally:
            client.close()

    # 1) Failed outgoing setup: the first large connection is held
    # unread past the 1 s anchored setup budget.
    t_entry = time.monotonic()
    a_status, a_payload = _post(
        proxy_port,
        _contract_body(False, input_text="\\U0001F600" * 150_000),
        {"X-Concept-Request-ID": "recovery-child-req-canary"},
    )
    a_elapsed = time.monotonic() - t_entry
    a_body_exact = a_status == 502 and a_payload == FIXED_502_BODY
    a_body_content_free = (
        b"recovery-child-req-canary" not in a_payload
        and b"recovery-child-review-key" not in a_payload
    )
    guard_alive_after_a = bool(guard_threads) and guard_threads[0].is_alive()
    # The exact first guard object (identity, not ident): its
    # actual join completion must be observed BEFORE the later
    # request bytes.
    first_guard = guard_threads[0] if guard_threads else None
    first_guard_joined_before_b = first_guard is not None and any(
        t is first_guard for t in joined_threads
    )
    # The bounded send window is a property of the stalled first
    # request's transport only; the healthy later request runs on
    # the ordinary stdlib socket.
    socket.socket = _real_socket
    # 2) Healthy recovery on the SAME proxy: the anchored first
    # deadline is recorded as already passed BEFORE the later
    # request bytes are written.
    t_before_b = time.monotonic()
    b_status, b_payload = _post(
        proxy_port,
        _contract_body(False, input_text=CLEAN),
        {},
    )
    b_body_exact = b_status == 200 and b_payload == answer
    result = {
        "a_status": a_status,
        "a_body_exact": a_body_exact,
        "a_body_content_free": a_body_content_free,
        "a_elapsed": a_elapsed,
        "b_status": b_status,
        "b_body_exact": b_body_exact,
        "guard_count": len(guard_threads),
        "guard_idents": [g.ident for g in guard_threads],
        "guard_alive_after_a": guard_alive_after_a,
        "deadline_anchor_delta": deadlines[0] - t_entry if deadlines else None,
        "deadline_0": deadlines[0] if deadlines else None,
        "t_before_b": t_before_b,
        "deadline_passed_before_b": bool(deadlines and t_before_b > deadlines[0]),
        "releases": list(releases),
        "first_guard_joined_before_b": first_guard_joined_before_b,
        "all_guards_joined_after_b": bool(guard_threads) and all(
            any(t is g for t in joined_threads) for g in guard_threads
        ),
        "connections": main_state["connections"],
        "repairs": list(repairs),
        "review_calls": len(_FakeUpstream.recorded),
    }
finally:
    # Owned cleanup on every path: shutdown only the serve loops
    # that actually started, then close every created listener;
    # never join a never-started thread.  The flags alone miss a
    # loop whose start raised after the thread actually started
    # (thread ident set, whether still alive or already ended),
    # so the observed ident decides the partial-start path too.
    def _actually_started(flag, thread):
        return bool(flag) or (
            thread is not None and thread.ident is not None
        )
    if _actually_started(proxy_started, proxy_thread):
        try:
            proxy_server.shutdown()
        except Exception:
            pass
        proxy_thread.join(5)
    if proxy_server is not None:
        try:
            proxy_server.server_close()
        except Exception:
            pass
    main_stop.set()
    if main_listener is not None:
        try:
            main_listener.close()
        except OSError:
            pass
    if _actually_started(main_started, main_thread):
        main_thread.join(5)
    if _actually_started(review_started, review_thread):
        try:
            review_server.shutdown()
        except Exception:
            pass
        review_thread.join(5)
    if review_server is not None:
        try:
            review_server.server_close()
        except Exception:
            pass
    temp.cleanup()
print("RESULT " + json.dumps(result), flush=True)
"""


class HangingNativeSupervisedTests(unittest.TestCase):
    """Order 022-a requirement 7: owned finite parent-supervised
    hanging scenarios with terminate/kill/reap escape."""

    def _run_supervised_child(
        self, script: Path, parent_bound: float
    ) -> tuple[int, str, str]:
        proc = subprocess.Popen(
            [sys.executable, "-I", "-B", str(script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            out, err = proc.communicate(timeout=parent_bound)
        except subprocess.TimeoutExpired:
            # Bounded escape: terminate, then kill, then reap.  A
            # forced escape is a FAILED outcome, never a partial pass.
            proc.terminate()
            try:
                out, err = proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                out, err = proc.communicate(timeout=5)
            self.fail(
                "owned supervised test child exceeded the finite "
                f"parent bound {parent_bound}s and was "
                "terminated/killed/reaped: the product deadline did "
                "not bound the setup phase. stderr tail: "
                + err.decode("utf-8", "replace")[-2000:]
            )
        self.assertIsNotNone(proc.returncode)
        return (
            proc.returncode,
            out.decode("utf-8", "replace"),
            err.decode("utf-8", "replace"),
        )

    @staticmethod
    def _result_line(out: str) -> dict[str, object]:
        for line in out.splitlines():
            if line.startswith("RESULT "):
                value = json.loads(line[len("RESULT ") :])
                assert isinstance(value, dict)
                return value
        raise AssertionError("no RESULT line in supervised child output")

    def test_supervised_tls_handshake_stall_long_budget(self) -> None:
        temp = tempfile.TemporaryDirectory()
        try:
            cert, key = _make_self_signed_cert(Path(temp.name))
            script = Path(temp.name) / "hang_tls.py"
            script.write_text(
                _HANG_TLS_CHILD.replace("@ROOT@", str(ROOT))
                .replace("@CERT@", str(cert))
                .replace("@KEY@", str(key))
                .replace("@BUDGET@", "5.0")
                .replace("@CAPTURE@", "30.0")
                .replace("@FAULT@", "15.0"),
                encoding="utf-8",
            )
            rc, out, err = self._run_supervised_child(script, 25.0)
        finally:
            temp.cleanup()
        self.assertEqual(rc, 0, out + err)
        result = self._result_line(out)
        self.assertEqual(result["reason"], "SETUP_DEADLINE")
        self.assertLess(float(cast("float", result["elapsed"])), 8.0)
        self.assertEqual(result["connections"], 1)
        self.assertEqual(result["hello"], "16")
        self.assertEqual(result["guard_threads"], [])

    def test_supervised_nonreading_upload_long_budget(self) -> None:
        temp = tempfile.TemporaryDirectory()
        try:
            script = Path(temp.name) / "hang_upload.py"
            script.write_text(
                _HANG_UPLOAD_CHILD.replace("@ROOT@", str(ROOT))
                .replace("@BODYLEN@", str(len(_UPLOAD_BODY)))
                .replace("@BUDGET@", "5.0")
                .replace("@CAPTURE@", "30.0")
                .replace("@FAULT@", "15.0"),
                encoding="utf-8",
            )
            rc, out, err = self._run_supervised_child(script, 25.0)
        finally:
            temp.cleanup()
        self.assertEqual(rc, 0, out + err)
        result = self._result_line(out)
        self.assertEqual(result["reason"], "SETUP_DEADLINE")
        self.assertLess(float(cast("float", result["elapsed"])), 8.0)
        # The write genuinely reached the peer transport (headers
        # observed) and stalled on the never-reading body.
        self.assertEqual(result["accepted"], 1)
        self.assertEqual(result["headers"], True)
        self.assertEqual(result["guard_threads"], [])
    def test_supervised_slowreading_upload_long_budget(self) -> None:
        # The REQUIRED slow (not stalled) native case under the owned
        # finite parent supervisor: a paced reader with a generous
        # budget COMPLETES - the write drains as the peer paces its
        # reads and the exact response is received - so the bounded
        # terminate/kill/reap escape is available but not needed.
        temp = tempfile.TemporaryDirectory()
        try:
            script = Path(temp.name) / "slowread.py"
            script.write_text(
                _HANG_SLOWREAD_CHILD.replace("@ROOT@", str(ROOT))
                .replace("@BODYLEN@", str(len(_UPLOAD_BODY)))
                .replace("@PACING@", "0.025")
                .replace("@BUDGET@", "20.0")
                .replace("@CAPTURE@", "30.0")
                .replace("@FAULT@", "35.0"),
                encoding="utf-8",
            )
            rc, out, err = self._run_supervised_child(script, 40.0)
        finally:
            temp.cleanup()
        self.assertEqual(rc, 0, out + err)
        result = self._result_line(out)
        self.assertEqual(result["reason"], "COMPLETED")
        self.assertEqual(result["completed"], True)
        self.assertLess(float(cast("float", result["elapsed"])), 15.0)
        self.assertEqual(result["accepted"], 1)
        self.assertEqual(result["headers"], True)
        self.assertEqual(
            int(cast("int", result["body_len"])), len(_UPLOAD_BODY)
        )
        self.assertEqual(result["guard_threads"], [])

    def test_supervised_slowreading_upload_short_budget(self) -> None:
        # The REQUIRED short-budget slow (not stalled) native case
        # under the owned finite parent supervisor: the SAME
        # matched producer as the in-process gentle positive (0.04
        # s per 64 KiB chunk: a ~23 x 40 ms drain lower bound for
        # the 1.5 MiB body, 32768 client sndbuf, 32768 listener
        # rcvbuf) genuinely outlasts the 0.8 s anchored budget -
        # the drain lower bound alone exceeds it on any machine -
        # so the bounded terminate/kill/reap escape is available
        # while the product deadline ends the setup first.
        temp = tempfile.TemporaryDirectory()
        try:
            script = Path(temp.name) / "slowread_short.py"
            script.write_text(
                _HANG_SLOWREAD_CHILD.replace("@ROOT@", str(ROOT))
                .replace("@BODYLEN@", str(len(_UPLOAD_BODY)))
                .replace("@PACING@", "0.04")
                .replace("@BUDGET@", "0.8")
                .replace("@CAPTURE@", "30.0")
                .replace("@FAULT@", "15.0"),
                encoding="utf-8",
            )
            rc, out, err = self._run_supervised_child(script, 20.0)
        finally:
            temp.cleanup()
        self.assertEqual(rc, 0, out + err)
        result = self._result_line(out)
        self.assertEqual(result["reason"], "SETUP_DEADLINE")
        self.assertLess(float(cast("float", result["elapsed"])), 2.0)
        # Real target-phase progress: the peer accepted the request
        # and a genuine body prefix, but not the whole body.
        self.assertEqual(result["accepted"], 1)
        self.assertEqual(result["headers"], True)
        self.assertGreater(int(cast("int", result["body_len"])), 0)
        self.assertLess(
            int(cast("int", result["body_len"])), len(_UPLOAD_BODY)
        )
        self.assertEqual(result["guard_threads"], [])

    def test_supervised_failed_setup_502_then_healthy_recovery_same_proxy(
        self,
    ) -> None:
        # The failure-prone native same-proxy recovery under the
        # owned finite parent supervisor: the real proxy/engine/
        # qualified-Pandoc/SQLite/reviewer stack runs in the child.
        # A contract-valid 1,800,053-byte first upload (150,000
        # decoded input codepoints, JSON surrogate-escaped; both
        # caps respected) is held unread by the owned raw main past
        # the 1 s anchored setup budget over bounded owned buffers.
        # The child proves: the fixed content-free 502 body exactly;
        # the first owned setup guard's actual identity, actual join
        # and actual anchored deadline with the deadline already
        # passed BEFORE the later request bytes; and the SAME proxy
        # serving the later healthy request with zero review work.
        temp = tempfile.TemporaryDirectory()
        try:
            script = Path(temp.name) / "recovery.py"
            script.write_text(
                _RECOVERY_CHILD.replace("@ROOT@", str(ROOT)).replace(
                    "@FAULT@", "20.0"
                ),
                encoding="utf-8",
            )
            rc, out, err = self._run_supervised_child(script, 25.0)
        finally:
            temp.cleanup()
        self.assertEqual(rc, 0, out + err)
        result = self._result_line(out)
        # The genuine outgoing setup failure: exact fixed
        # content-free 502 body, no request/review canary inside.
        self.assertEqual(result["a_status"], 502)
        self.assertIs(result["a_body_exact"], True)
        self.assertIs(result["a_body_content_free"], True)
        self.assertGreaterEqual(
            float(cast("float", result["a_elapsed"])), 0.9
        )
        self.assertLess(float(cast("float", result["a_elapsed"])), 3.0)
        # The SAME proxy then serves the healthy request with the
        # exact unchanged answer.
        self.assertEqual(result["b_status"], 200)
        self.assertIs(result["b_body_exact"], True)
        # Known first-guard identity, actual join before the later
        # request, actual anchored deadline passed before the later
        # request bytes.
        # One owned setup guard per forward on the SAME proxy:
        # both guard identities are observed; the first (stalled)
        # guard was actually joined before the later request
        # bytes, and all guards are joined after the later
        # request.
        self.assertEqual(result["guard_count"], 2)
        idents = cast(list[object], result["guard_idents"])
        self.assertEqual(len(idents), 2)
        self.assertIsNotNone(idents[0])
        self.assertIsNotNone(idents[1])
        self.assertIs(result["guard_alive_after_a"], False)
        # The caller actually joined the exact first guard object
        # (call-through join completion) before the later request
        # bytes; every observed guard's join completed after the
        # later request.  Object identity, never ident equality:
        # the OS may reuse a terminated thread's ident.
        self.assertIs(result["first_guard_joined_before_b"], True)
        self.assertIs(result["all_guards_joined_after_b"], True)
        # The anchored first deadline is the forward entry plus
        # the 1 s budget; the large first request's intake
        # consumed a finite pre-forward interval (measured, not
        # assumed), and the setup phase itself ran exactly the
        # budget before the fixed 502.
        anchor_delta = cast("float", result["deadline_anchor_delta"])
        intake = anchor_delta - 1.0
        self.assertGreaterEqual(intake, 0.0)
        self.assertLess(intake, 1.0)
        setup_elapsed = float(cast("float", result["a_elapsed"])) - intake
        self.assertAlmostEqual(setup_elapsed, 1.0, delta=0.25)
        self.assertIs(result["deadline_passed_before_b"], True)
        # The first setup guard released expired (the setup deadline
        # fired; not a header/body/intake failure); the healthy
        # second setup released unexpired (its success-path and
        # finally releases both observe the unexpired state).
        releases = [bool(r) for r in cast(list[object], result["releases"])]
        self.assertGreaterEqual(len(releases), 2)
        self.assertIs(releases[0], True)
        self.assertTrue(all(r is False for r in releases[1:]))
        # One stalled first and one immediate later connection on
        # the SAME proxy; zero reviewer work; the engine touched
        # only the healthy CLEAN answer.
        self.assertEqual(result["connections"], 2)
        self.assertEqual(result["review_calls"], 0)
        self.assertEqual(result["repairs"], [CLEAN])

# ------------------------------------------------------------------
# Order 022-a requirement 8: the actual constructor / normal main
# default, override and invalid-before-bind, and the actual HTTP
# JSON and delayed-SSE integration through the real stack with
# owned synthetic loopback main/review servers.  Bounded synthetic
# canary evidence only; no general privacy, real-model or
# linguistic-quality certification claim.
# ------------------------------------------------------------------


def _raw_post(
    port: int, body: bytes, headers: dict[str, str]
) -> tuple[int, bytes]:
    """One explicit-header owned loopback POST (the client's own
    Host/link headers are part of the allowlist evidence)."""
    client = http.client.HTTPConnection("127.0.0.1", port, timeout=30)
    try:
        client.request("POST", "/v1/responses", body=body, headers=headers)
        response = client.getresponse()
        payload = response.read()
        return response.status, payload
    finally:
        client.close()


class ConstructorMainTests(unittest.TestCase):
    """Order 022-a requirement 8: the actual constructor and the
    normal main() entry on owned ephemeral loopback binds only
    (never the fixed 18024 service port)."""

    def test_real_constructor_default_override_invalid_before_bind(self) -> None:
        temp = tempfile.TemporaryDirectory()
        try:
            db = Path(temp.name) / "ctor.sqlite"
            # Explicit synthetic key: the constructor-only fixture
            # needs no owner environment credential lookup.
            reviewer = ResponsesReviewer(
                "http://127.0.0.1:9/v1",
                "test-model",
                timeout=5.0,
                api_key="ctor-synthetic-key",
            )
            bound: list[int] = []

            class BindSpy(proxy.ConceptProxy):
                def server_bind(self) -> None:
                    # Observe the real bind ENTRY: for the requested
                    # port 0 this records the requested port, not
                    # the allocated one (the real bind inside
                    # super() updates server_address afterwards).
                    bound.append(self.server_address[1])
                    super().server_bind()

            # Named 30 s default: the real constructor validates
            # and stores the budget; the real bind entry is observed
            # on the owned port 0 and the allocated port is read
            # separately after the real bind.
            default_proxy = BindSpy(
                ("127.0.0.1", 0),
                "http://127.0.0.1:1",
                proxy.RepairEngine(db, reviewer),
            )
            try:
                self.assertEqual(default_proxy.setup_timeout, 30.0)
                self.assertEqual(
                    default_proxy.setup_timeout, MAIN_SETUP_TIMEOUT_SECONDS
                )
                self.assertEqual(bound, [0])
                port = default_proxy.server_address[1]
                self.assertGreater(port, 1024)
                self.assertNotEqual(port, 18024)
            finally:
                default_proxy.server_close()

            # Explicit override: the keyword-only setup_timeout is
            # validated and stored; the same bind-entry observation.
            bound.clear()
            override_proxy = BindSpy(
                ("127.0.0.1", 0),
                "http://127.0.0.1:1",
                proxy.RepairEngine(db, reviewer),
                setup_timeout=7.25,
            )
            try:
                self.assertEqual(override_proxy.setup_timeout, 7.25)
                self.assertEqual(bound, [0])
            finally:
                override_proxy.server_close()

            # Invalid values are rejected BEFORE any bind entry:
            # the explicit baseline distinguishes the invalid calls
            # from the successful bind entries above (the narrow
            # cast is the intentional negative-test typing: the
            # values are deliberately not floats).
            bound.clear()
            for bad in (
                True,
                "abc",
                0,
                -1,
                float("nan"),
                float("inf"),
                1e300,
                10**400,
                threading.TIMEOUT_MAX + 1.0,
            ):
                with self.assertRaises(ValueError):
                    BindSpy(
                        ("127.0.0.1", 0),
                        "http://127.0.0.1:1",
                        proxy.RepairEngine(db, reviewer),
                        setup_timeout=cast(float, bad),
                    )
            self.assertEqual(bound, [])
        finally:
            temp.cleanup()

    def test_normal_main_wires_concept_setup_timeout(self) -> None:
        configured = os.environ.get("CONCEPT_PANDOC", "").strip()
        if not configured:
            raise unittest.SkipTest("qualified CONCEPT_PANDOC not configured")
        temp = tempfile.TemporaryDirectory()
        try:
            db = Path(temp.name) / "main-wire.sqlite"
            _build_db(db, unigram=_BUILD_UNIGRAM)
            seen: dict[str, object] = {}
            constructed: list[proxy.ConceptProxy] = []
            bound_entries: list[int] = []

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
                    setup_timeout: float = MAIN_SETUP_TIMEOUT_SECONDS,
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
                        setup_timeout=setup_timeout,
                    )
                    seen["setup_timeout"] = self.setup_timeout
                    constructed.append(self)

                def server_bind(self) -> None:
                    # Real bind ENTRY observation (requested port 0)
                    # so the invalid cases prove no bind ATTEMPT,
                    # not merely no completed construction.
                    bound_entries.append(self.server_address[1])
                    super().server_bind()

                def serve_forever(self, poll_interval: float = 0.5) -> None:
                    return

            base_env = {
                "CONCEPT_INDEX": str(db),
                "CONCEPT_UPSTREAM_URL": "http://127.0.0.1:1",
                "CONCEPT_REVIEWER_URL": "http://127.0.0.1:9/v1",
                "CONCEPT_PANDOC": configured,
            }
            with mock.patch.object(proxy, "ConceptProxy", Port0Proxy):
                # Unconfigured: the named 30 s constructor default
                # governs (the real constructor validates and sets
                # it); the owned bind is an ephemeral port.
                with mock.patch.dict(os.environ, base_env, clear=True):
                    self.assertEqual(proxy.main(), 0)
                self.assertEqual(seen["setup_timeout"], 30.0)
                self.assertEqual(len(constructed), 1)
                self.assertEqual(bound_entries, [0])
                self.assertGreater(constructed[0].server_address[1], 1024)
                self.assertNotEqual(constructed[0].server_address[1], 18024)

                # Explicit override: setup 7.25 independent of the
                # other axes (they keep their defaults here).
                before_con = len(constructed)
                before_bind = list(bound_entries)
                env = dict(base_env, CONCEPT_SETUP_TIMEOUT="7.25")
                with mock.patch.dict(os.environ, env, clear=True):
                    self.assertEqual(proxy.main(), 0)
                self.assertEqual(seen["setup_timeout"], 7.25)
                self.assertEqual(len(constructed), before_con + 1)
                self.assertEqual(bound_entries, before_bind + [0])

                # Invalid values are rejected before any completed
                # construction AND before any bind attempt (per-case
                # baselines on the real server_bind entry).
                for bad_env in ("abc", "inf", "0", "-1", "1e300"):
                    before_con = len(constructed)
                    before_bind = list(bound_entries)
                    env_bad = dict(base_env, CONCEPT_SETUP_TIMEOUT=bad_env)
                    with (
                        mock.patch.dict(os.environ, env_bad, clear=True),
                        self.assertRaises(ValueError),
                    ):
                        proxy.main()
                    self.assertEqual(len(constructed), before_con)
                    self.assertEqual(bound_entries, before_bind)
        finally:
            # Every known constructed listener closes on ALL paths
            # (no shutdown of an unstarted serve_forever: the stub
            # serve_forever returns immediately and no real fixed
            # 18024 bind is allowed).
            for server in constructed:
                server.server_close()
            temp.cleanup()


class _PacedSseMain(BaseHTTPRequestHandler):
    """Owned finite paced-SSE main producer: a real response-header
    delay, then the whole declared body streamed in small flushed
    frames with real inter-frame gaps (a genuine slow producer, not
    an instant replay).  Every phase is finite, so a regressed clock
    cannot hang the suite."""

    protocol_version = "HTTP/1.1"
    source: bytes = b""
    header_delay: float = 0.0
    frame_gap: float = 0.0
    frame_size: int = 4096
    recorded: list[dict[str, object]] = []
    done_at: float | None = None

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.__class__.recorded.append(
            {
                "path": self.path,
                "headers": dict(self.headers.items()),
                "body": body,
            }
        )
        if self.__class__.header_delay:
            time.sleep(self.__class__.header_delay)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(self.__class__.source)))
        self.end_headers()
        size = self.__class__.frame_size
        source = self.__class__.source
        offset = 0
        while offset < len(source):
            if offset:
                time.sleep(self.__class__.frame_gap)
            self.wfile.write(source[offset : offset + size])
            self.wfile.flush()
            offset += size
        self.__class__.done_at = time.monotonic()

    def log_message(self, *_args: object) -> None:
        return


class _SseSetupHarness:
    """Owned real-stack harness with a short anchored setup budget
    and the paced-SSE main producer: requirement 8 delayed-SSE plus
    requirement 5 clock independence (the later header/body/review
    phases may outlive the released setup clock)."""

    def __init__(
        self,
        setup_timeout: float,
        usage_observer: Callable[[dict[str, object]], None] | None = None,
    ) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.servers: list[HTTPServer] = []
        self.threads: list[threading.Thread] = []
        try:
            self.db = Path(self.temp.name) / "sse-setup.sqlite"
            _build_db(self.db, unigram=_BUILD_UNIGRAM)
            _PacedSseMain.source = _sse_baseline_utf8(USEFUL_018)
            _PacedSseMain.header_delay = 0.0
            _PacedSseMain.frame_gap = 0.0
            _PacedSseMain.frame_size = 4096
            _PacedSseMain.recorded = []
            _PacedSseMain.done_at = None
            _FakeUpstream.status = 200
            _FakeUpstream.delay = 0.0
            _FakeUpstream.payload = b"{}"
            _FakeUpstream.recorded = []
            self.main_server = HTTPServer(("127.0.0.1", 0), _PacedSseMain)
            self.servers.append(self.main_server)
            self.review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
            self.servers.append(self.review_server)
            self.reviewer = ResponsesReviewer(
                f"http://127.0.0.1:{self.review_server.server_port}/v1",
                "test-model",
                timeout=5.0,
                api_key="sse-setup-review-key-synthetic",
            )
            self.engine = proxy.RepairEngine(
                self.db, self.reviewer, pandoc=_real_spec()
            )
            self.proxy_server = proxy.ConceptProxy(
                ("127.0.0.1", 0),
                f"http://127.0.0.1:{self.main_server.server_port}",
                self.engine,
                usage_observer=usage_observer,
                setup_timeout=setup_timeout,
            )
            self.servers.append(self.proxy_server)
        except BaseException:
            # Partial-startup ownership: close every listener that was
            # actually created; no serve loop has started yet.
            for server in self.servers:
                with suppress(OSError):
                    server.server_close()
            self.temp.cleanup()
            raise
        for server in self.servers:
            thread = threading.Thread(
                target=server.serve_forever, daemon=True
            )
            try:
                thread.start()
            except BaseException:
                # Partial-startup ownership: a loop that
                # actually started before the startup
                # failure (thread ident set, whether still
                # alive or already ended) is registered so
                # its server is shut down and the thread is
                # actually joined; a never-started thread
                # (ident is None) is never registered, shut
                # down or joined.
                if thread.ident is not None:
                    self.threads.append(thread)
                self._close_started()
                raise
            self.threads.append(thread)

    def _close_started(self) -> None:
        # Only the serve loops that actually started are shut down
        # (shutdown blocks forever on a never-started loop); every
        # created listener closes and the temp tree is removed.
        started = self.servers[: len(self.threads)]
        for server in started:
            server.shutdown()
        for thread in self.threads:
            thread.join(5)
        for server in self.servers:
            with suppress(OSError):
                server.server_close()
        self.temp.cleanup()

    def close(self) -> None:
        for server in self.servers:
            server.shutdown()
        for thread in self.threads:
            thread.join(5)
        for server in self.servers:
            with suppress(OSError):
                server.server_close()
        self.temp.cleanup()
        alive = [thread for thread in self.threads if thread.is_alive()]
        if alive:
            raise AssertionError(
                "owned sse-setup fixture thread not ended"
            )


class IntegrationTests(unittest.TestCase):
    """Order 022-a requirement 8: the actual HTTP JSON and
    delayed-SSE integration through real ConceptProxy -> real
    RepairEngine (qualified Pandoc, real tiny SQLite) -> real
    ResponsesReviewer with owned synthetic loopback main/review
    servers.  Bounded synthetic canary evidence only."""

    def _assert_useful_review_shape(
        self,
        rrecord: dict[str, object],
        main_canary: str,
        review_key: str,
    ) -> None:
        # Isolated single text-only batch request: the actual
        # recorded review route/headers/body carry the separate
        # review key, the exact request key set, the ordered two
        # targets, the exact bounded output cap, and no main
        # credential in the actual prompt.
        self.assertEqual(rrecord["path"], "/v1/responses")
        rheaders = cast(dict[str, str], rrecord["headers"])
        self.assertEqual(
            rheaders.get("Authorization"), f"Bearer {review_key}"
        )
        self.assertEqual(rheaders.get("Content-Type"), "application/json")
        rval = json.loads(cast(bytes, rrecord["body"]))
        self.assertEqual(
            set(rval),
            {"model", "stream", "store", "max_output_tokens", "input"},
        )
        self.assertEqual(rval["model"], "test-model")
        self.assertIs(rval["stream"], False)
        self.assertIs(rval["store"], False)
        self.assertEqual(rval["max_output_tokens"], 1536)
        rinput = rval["input"]
        self.assertIsInstance(rinput, list)
        self.assertEqual(len(rinput), 1)
        ritem = rinput[0]
        self.assertIsInstance(ritem, dict)
        self.assertEqual(ritem.get("role"), "user")
        rcontent = ritem.get("content")
        self.assertIsInstance(rcontent, list)
        self.assertEqual(len(rcontent), 1)
        rpart = rcontent[0]
        self.assertIsInstance(rpart, dict)
        self.assertEqual(rpart.get("type"), "input_text")
        rprompt = rpart.get("text")
        self.assertIsInstance(rprompt, str)
        # Ordered two targets: t0 before t1 in the actual prompt;
        # the main credential never crosses to the review boundary.
        self.assertLess(rprompt.index("t0"), rprompt.index("t1"))
        self.assertNotIn(main_canary, rprompt)

    def test_chain_useful_two_targets_json(self) -> None:
        # Useful two-target exact repair in the JSON mode preserving
        # Unicode/combining/code/math/HTML/links, with the exact
        # allowlisted forward and the isolated one-review shape/
        # usage.
        usage: list[dict[str, object]] = []
        calls: list[str] = []
        harness = _Harness(usage_observer=usage.append)
        try:
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t1")],
                usage={
                    "input_tokens": 4,
                    "output_tokens": 6,
                    "total_tokens": 10,
                },
            )
            _MainUpstream.content_type = "application/json"
            _MainUpstream.source = _json_completed(USEFUL_018)
            body = _contract_body(False, input_text=USEFUL_018)
            base_repair = harness.engine.repair

            def observed_repair(text: str) -> str:
                calls.append(text)
                return base_repair(text)

            with mock.patch.object(
                harness.engine, "repair", observed_repair
            ):
                status, payload = _raw_post(
                    harness.proxy_server.server_port,
                    body,
                    {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": "Bearer canary-022a-main-key",
                        "Host": "synthetic-client-host.invalid",
                        "Cookie": "session=abc",
                        "X-Concept-Request-ID": "link-canary-022a",
                    },
                )
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(calls, [USEFUL_018])
            self.assertEqual(len(_MainUpstream.recorded), 1)
            record = _MainUpstream.recorded[0]
            # Exact allowlisted forward: the exact body, and only
            # content-type/accept/authorization reach main (never
            # hop-by-hop, the client's Host, ids or cookies).
            self.assertEqual(cast(bytes, record["body"]), body)
            fwd = cast(dict[str, str], record["headers"])
            self.assertEqual(
                fwd.get("Authorization"),
                "Bearer canary-022a-main-key",
            )
            self.assertEqual(fwd.get("Content-Type"), "application/json")
            self.assertEqual(fwd.get("Accept"), "application/json")
            self.assertNotIn("Cookie", fwd)
            self.assertNotIn("X-Concept-Request-ID", fwd)
            self.assertNotEqual(
                fwd.get("Host"), "synthetic-client-host.invalid"
            )
            text = json.loads(payload.decode())[
                "output"
            ][0]["content"][0]["text"]
            self.assertEqual(text, EXPECTED_USEFUL_018)
            # Protected slices preserved exactly in the decoded
            # final composed answer (code, TeX, HTML, link and the
            # NFC-unstable decomposed/combining line).
            for marker in (
                "`presenetliv`",
                "\\(x^2\\)",
                "<b>presenetliv</b>",
                "[zapis](http://example.com/slo)",
                "e\u0301",
            ):
                self.assertIn(marker, text)
            # Raw wire UTF-8 for the protected symbols (a
            # separate loop variable: the wire markers are
            # bytes, the decoded markers above are str).
            for raw_marker in (
                "\u20ac".encode(),
                "\U0001F600".encode(),
                "e\u0301".encode(),
            ):
                self.assertIn(raw_marker, payload)
            self._assert_useful_review_shape(
                _FakeUpstream.recorded[0],
                "canary-022a-main-key",
                "review-key-synthetic",
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

    def test_chain_useful_two_targets_paced_sse_short_setup(self) -> None:
        # Requirement 8 delayed-SSE + requirement 5 clock
        # independence: the anchored setup budget is 1.0 s while the
        # owned finite main producer delays the response headers
        # (1.2 s), then streams the whole SSE body in small flushed
        # frames with real gaps (~1.2 s), and the real reviewer
        # reply is delayed 1.2 s.  Every later phase genuinely
        # outlives the released setup clock; the exchange still
        # completes with the whole main body captured before any
        # engine/review work and the exact useful two-target repair.
        usage: list[dict[str, object]] = []
        harness = _SseSetupHarness(1.0, usage_observer=usage.append)
        try:
            source = _sse_baseline_utf8(USEFUL_018)
            _PacedSseMain.source = source
            _PacedSseMain.header_delay = 1.2
            frames = 24
            _PacedSseMain.frame_size = max(1, len(source) // frames)
            _PacedSseMain.frame_gap = 0.05
            _FakeUpstream.delay = 1.2
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t1")],
                usage={
                    "input_tokens": 4,
                    "output_tokens": 6,
                    "total_tokens": 10,
                },
            )
            calls: list[str] = []
            repair_times: list[float] = []
            review_windows: list[tuple[float, float]] = []
            base_repair = harness.engine.repair

            def observed_repair(text: str) -> str:
                repair_times.append(time.monotonic())
                calls.append(text)
                return base_repair(text)

            base_review = harness.reviewer.review_batch

            def observed_review(
                sentence: str, targets: tuple[BatchTarget, ...]
            ) -> object:
                started = time.monotonic()
                outcome = base_review(sentence, targets)
                review_windows.append((started, time.monotonic()))
                return outcome

            body = _contract_body(True, input_text=USEFUL_018)
            t_entry = time.monotonic()
            with (
                mock.patch.object(harness.engine, "repair", observed_repair),
                mock.patch.object(
                    harness.reviewer, "review_batch", observed_review
                ),
            ):
                status, payload = _raw_post(
                    harness.proxy_server.server_port,
                    body,
                    {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": "Bearer sse-setup-main-canary",
                        "Host": "synthetic-sse-client-host.invalid",
                        "Cookie": "session=abc",
                        "X-Concept-Request-ID": "sse-setup-link-canary",
                    },
                )
            elapsed = time.monotonic() - t_entry
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(calls, [USEFUL_018])
            # The whole main body was captured before engine/review
            # work began: the paced producer's completion precedes
            # the first repair call.
            self.assertIsNotNone(_PacedSseMain.done_at)
            self.assertLess(cast(float, _PacedSseMain.done_at), repair_times[0])
            # The later phases genuinely outlived the 1.0 s anchored
            # setup clock: the review started, the repair began and
            # the whole exchange finished only after that deadline.
            self.assertGreater(review_windows[0][0], t_entry + 1.0)
            self.assertGreater(repair_times[0], t_entry + 1.0)
            self.assertGreater(elapsed, 2.0)
            # The exact useful two-target repair in the SSE mode.
            final = [
                json.loads(block[5:])
                for block in payload.decode().split("\n\n")
                if block.startswith("data:")
            ]
            completed = next(
                e for e in final if e.get("type") == "response.completed"
            )
            text = completed["response"]["output"][0]["content"][0]["text"]
            self.assertEqual(text, EXPECTED_USEFUL_018)
            for marker in (
                "`presenetliv`",
                "\\(x^2\\)",
                "<b>presenetliv</b>",
                "[zapis](http://example.com/slo)",
                "e\u0301",
            ):
                self.assertIn(marker, text)
            for raw_marker in (
                "\u20ac".encode(),
                "\U0001F600".encode(),
                "e\u0301".encode(),
            ):
                self.assertIn(raw_marker, payload)
            # Exact allowlisted forward on the owned paced main.
            self.assertEqual(len(_PacedSseMain.recorded), 1)
            record = _PacedSseMain.recorded[0]
            self.assertEqual(cast(bytes, record["body"]), body)
            fwd = cast(dict[str, str], record["headers"])
            self.assertEqual(
                fwd.get("Authorization"), "Bearer sse-setup-main-canary"
            )
            self.assertEqual(fwd.get("Content-Type"), "application/json")
            self.assertEqual(fwd.get("Accept"), "application/json")
            self.assertNotIn("Cookie", fwd)
            self.assertNotIn("X-Concept-Request-ID", fwd)
            # The proxy's own outbound Host names the owned main
            # (http.client stdlib behavior); the client's Host
            # itself is allowlist-dropped and never forwarded.
            self.assertNotEqual(
                fwd.get("Host"), "synthetic-sse-client-host.invalid"
            )
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self._assert_useful_review_shape(
                _FakeUpstream.recorded[0],
                "sse-setup-main-canary",
                "sse-setup-review-key-synthetic",
            )
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
            _FakeUpstream.delay = 0.0
            _PacedSseMain.header_delay = 0.0
            _PacedSseMain.frame_gap = 0.0
            harness.close()

    def _run_no_suspicion_mode(self, stream: bool) -> None:
        # One mode of the no-suspicion case: the helper's own
        # locals are the closure bindings (no loop-variable
        # capture).
        calls: list[str] = []
        harness = _Harness()
        try:
            if stream:
                _MainUpstream.content_type = "text/event-stream"
                _MainUpstream.source = _sse_baseline_utf8(CLEAN)
            else:
                _MainUpstream.content_type = "application/json"
                _MainUpstream.source = _json_completed(CLEAN)
            base_repair = harness.engine.repair

            def observed_repair(text: str) -> str:
                calls.append(text)
                return base_repair(text)

            with mock.patch.object(
                harness.engine, "repair", observed_repair
            ):
                status, payload = harness.post(
                    _contract_body(stream, input_text=CLEAN)
                )
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(payload, _MainUpstream.source)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(calls, [CLEAN])
        finally:
            harness.close()

    def test_chain_no_suspicion_zero_review_exact_bytes(self) -> None:
        # No suspicion in either mode: the exact unchanged main
        # bytes are forwarded with zero reviewer calls (the engine
        # is reached once and edits nothing).
        for stream in (False, True):
            with self.subTest(stream=stream):
                self._run_no_suspicion_mode(stream)

    def test_chain_completed_original_optional_review_failure(self) -> None:
        # A completed eligible original (two repairable
        # occurrences) with a GENUINE reviewer failure (real
        # optional-repair path): exact byte-identical original,
        # status 200, with the honest one-attempt usage.
        calls: list[str] = []
        usage: list[dict[str, object]] = []
        harness = _Harness(usage_observer=usage.append)
        try:
            source = _json_completed(TEXT)
            _MainUpstream.source = source
            _MainUpstream.content_type = "application/json"
            _FakeUpstream.status = 500
            _FakeUpstream.payload = b'{"error":"synthetic reviewer failure"}'
            base_repair = harness.engine.repair

            def observed_repair(text: str) -> str:
                calls.append(text)
                return base_repair(text)

            with mock.patch.object(
                harness.engine, "repair", observed_repair
            ):
                status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(payload, source)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(calls, [TEXT])
            self.assertEqual(
                usage,
                [{"review_calls": 1, "reviewer_usage": "unknown"}],
            )
        finally:
            _FakeUpstream.status = 200
            harness.close()

    def test_chain_failed_message_status_bypass_zero_work(self) -> None:
        # Separate case from the completed-original fallback: a
        # non-completed message status bypasses raw unchanged with
        # zero repair and zero review.
        calls: list[str] = []
        harness = _Harness()
        try:
            source = _json_completed(TEXT, message_status="failed")
            _MainUpstream.source = source
            _MainUpstream.content_type = "application/json"
            _FakeUpstream.payload = _review_payload([_prop("t0"), _prop("t1")])
            base_repair = harness.engine.repair

            def observed_repair(text: str) -> str:
                calls.append(text)
                return base_repair(text)

            with mock.patch.object(
                harness.engine, "repair", observed_repair
            ):
                status, payload = harness.post(
                    _contract_body(False, input_text=TEXT)
                )
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(payload, source)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(calls, [])
        finally:
            harness.close()

    def _run_non200_passthrough_case(
        self, status_code: int, body: bytes
    ) -> None:
        # One non-200 case: the helper's own locals are the
        # closure bindings (no loop-variable capture).
        calls: list[str] = []
        harness = _Harness()
        try:
            _MainUpstream.status = status_code
            _MainUpstream.content_type = "application/json"
            _MainUpstream.source = body
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t1")]
            )
            base_repair = harness.engine.repair

            def observed_repair(text: str) -> str:
                calls.append(text)
                return base_repair(text)

            with mock.patch.object(
                harness.engine, "repair", observed_repair
            ):
                status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, status_code)
            self.assertEqual(payload, body)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(calls, [])
        finally:
            _MainUpstream.status = 200
            harness.close()

    def test_chain_real_non200_passthrough_exact_bytes_zero_work(self) -> None:
        # Genuine upstream non-200 keeps its status/body and
        # bypasses repair: zero review, zero engine work.
        cases = (
            (404, b'{"error":{"type":"not_found","code":"synthetic-canary-404"}}'),
            (503, b'{"error":{"type":"unavailable","code":"synthetic-canary-503"}}'),
        )
        for status_code, body in cases:
            with self.subTest(status=status_code):
                self._run_non200_passthrough_case(status_code, body)

    def test_canaries_bounded_capture_and_default_tracing_off(self) -> None:
        # Bounded synthetic canary evidence: the main key, request
        # id, actual response text and reviewer key canaries never
        # reach the test process's explicitly bounded stdout/stderr
        # capture during a real request with a genuine reviewer
        # failure; the capture fails on excess (excess would
        # silently discard canaries); default tracing is off (no
        # trace directory).  Not a general privacy certification.
        class _BoundedCapture(io.StringIO):
            limit = 1_000_000
            overflowed = False

            def write(self, s: str) -> int:
                if self.overflowed:
                    return 0
                if len(self.getvalue()) + len(s) > self.limit:
                    self.overflowed = True
                    return 0
                return super().write(s)

        usage: list[dict[str, object]] = []
        harness = _Harness(usage_observer=usage.append)
        try:
            self.assertIsNone(harness.proxy_server.trace_dir)
            source = _json_completed(TEXT)
            _MainUpstream.source = source
            _MainUpstream.content_type = "application/json"
            _FakeUpstream.status = 500
            _FakeUpstream.payload = (
                b'{"error":"canary-022a-reviewer-exception"}'
            )
            out = _BoundedCapture()
            err = _BoundedCapture()
            with (
                contextlib.redirect_stdout(out),
                contextlib.redirect_stderr(err),
            ):
                status, payload = harness.post(
                    _contract_body(False),
                    {
                        "Authorization": "Bearer canary-022a-main-key",
                        "X-Concept-Request-ID": "canary-022a-request-id",
                    },
                )
            self.assertFalse(out.overflowed, "bounded stdout capture exceeded")
            self.assertFalse(err.overflowed, "bounded stderr capture exceeded")
            captured = out.getvalue() + err.getvalue()
            self.assertEqual(status, 200, payload[:200])
            self.assertEqual(payload, source)
            # Genuinely failed optional review: one real attempt,
            # honest unknown usage, byte-identical completed
            # original.
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(
                usage, [{"review_calls": 1, "reviewer_usage": "unknown"}]
            )
            for canary in (
                "canary-022a-main-key",
                "canary-022a-request-id",
                "canary-022a-reviewer-exception",
                TEXT,
                "review-key-synthetic",
            ):
                self.assertNotIn(canary, captured)
            # The request id was allowlist-dropped at main.
            main_headers = cast(
                dict[str, str], _MainUpstream.recorded[0]["headers"]
            )
            self.assertNotIn("X-Concept-Request-ID", main_headers)
        finally:
            _FakeUpstream.status = 200
            harness.close()
