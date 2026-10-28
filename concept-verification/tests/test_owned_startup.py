"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.
Owned Pandoc/reviewer partial-startup cleanup (order 023-a).

Bounded ownership proofs at the actual product boundary: the real
``protect_with_pandoc`` (qualified installed 3.7.0.2 binary, real
CPython ``Popen``) and the real ``run_review_exchange`` (production
``review_worker.py``, owned loopback main).  Controlled real
call-through fault seams at ``subprocess.Popen._execute_child`` and
``os.pipe`` cover: caller interruption before child creation
(never-created), after actual child creation with the child
scheduler-held (SIGSTOP) or already ended, second-pipe allocation
KeyboardInterrupt/MemoryError/OSError, and process-object allocation
failure itself.  Every case proves ownership, reaping and FD cleanup
BEFORE test cleanup: the known owned child is actually wait/reaped
before product return, the exact owned descriptors are closed, the
original nonordinary exception identity is preserved, ordinary
failures keep their fixed labels, and a known unrelated sentinel
child of the test process remains untouched (no ``waitpid(-1)``, no
global group signal).  The potentially-hanging native held-child
cases run under a finite owned parent supervisor of an isolated
process group; the Pandoc child's own session escapes that group, so
the supervised script's own fail-safe finally owns the exact captured
child and the parent additionally verifies the exact known identity
is gone after a forced escape.  A forced escape is a FAILED outcome,
never a pass.

Controlled fault evidence only: no claim of spontaneous native
failure, completed linguistic qualification, live-model or
deployment behavior.  The qualified Pandoc binary comes from
``CONCEPT_PANDOC`` (no PATH discovery or fallback); required cases
do not skip.
"""

from __future__ import annotations

import contextlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandoc_protection as pp  # noqa: E402
import review_transport as rt  # noqa: E402
from batch_review import REASON_HTTP_FAILED  # noqa: E402

WORKER = ROOT / "review_worker.py"
PARENT_BOUND_SECONDS = 30.0
_HELD_CHILD_OBSERVE_SECONDS = 5.0
_HEALTHY_BODY = "Beseda in *poudar* zapis."
_HEALTHY_PAYLOAD = b'{"ok": true}'


def _qualified_binary() -> str:
    configured = os.environ.get("CONCEPT_PANDOC", "").strip()
    if not configured:
        raise AssertionError(
            "CONCEPT_PANDOC must name the qualified installed Pandoc "
            "binary; no PATH discovery or fallback (order 023-a)"
        )
    return configured


def _spec() -> pp.PandocSpec:
    return pp.PandocSpec(binary=_qualified_binary())


def _fds() -> set[int]:
    return {int(name) for name in os.listdir("/proc/self/fd")}


def _proc_state(pid: int) -> str | None:
    try:
        return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
    except (FileNotFoundError, ProcessLookupError):
        return None


def _waitid_observed(pid: int) -> os.waitid_result | None:
    """Observe a known child's exit WITHOUT detaching it
    (WNOWAIT|WNOHANG): it returns the wait status while the child is
    still an unreaped zombie of this process, returns None while the
    child is still dying, and raises ChildProcessError when the child
    is already reaped (or not ours)."""
    return os.waitid(os.P_PID, pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)


class _Sentinel:
    """A known unrelated owned child of THIS test process.  It runs a
    trivial real child that exits on its own and stays an unreaped
    zombie for the duration of the test.  A product boundary that
    reaped globally (``waitpid(-1)``) or signalled a wrong group
    would detach or kill it; the test reaps it only in its own
    finally, after every observation."""

    def __init__(self) -> None:
        self.proc: subprocess.Popen[bytes] = subprocess.Popen(
            [sys.executable, "-B", "-c", "pass"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        until = time.monotonic() + _HELD_CHILD_OBSERVE_SECONDS
        while _proc_state(self.proc.pid) != "Z" and time.monotonic() < until:
            time.sleep(0.005)
        if _proc_state(self.proc.pid) != "Z":
            with contextlib.suppress(OSError):
                self.proc.kill()
            self.proc.wait(timeout=5)
            raise AssertionError("sentinel child did not become a zombie in bound")

    def assert_untouched(self) -> None:
        try:
            observed = _waitid_observed(self.proc.pid)
        except ChildProcessError:
            raise AssertionError(
                "sentinel child was reaped across the product boundary: "
                "a global wait (waitpid(-1)) or wrong-group signal leaked "
                "into unrelated owned children"
            ) from None
        if observed is None:
            raise AssertionError("sentinel child did not exit on its own")
        if observed[0] != self.proc.pid or observed[4] != os.CLD_EXITED or observed[3] != 0:
            raise AssertionError("sentinel child status altered by product boundary")

    def reap(self) -> None:
        # Reap this test's own known child; a later Popen.__del__ on
        # the already-reaped instance is a documented no-op.
        with contextlib.suppress(ChildProcessError):
            os.waitpid(self.proc.pid, 0)


class _OwnedBoundaryBase(unittest.TestCase):
    def _assert_fd_closed(self, fd: int) -> None:
        with self.assertRaises(OSError):
            os.fstat(fd)

    def _assert_no_new_fds(self, before: set[int]) -> None:
        self.assertTrue(before.issuperset(_fds()))

    def _patch_execute(
        self,
        captured: dict[str, object],
        *,
        pre_fault: type[BaseException] | None = None,
        post_create: str = "none",
    ) -> mock._patch[object]:
        """Temporary controlled call-through seam on the real
        ``Popen._execute_child``: the real child creation always runs
        first (except the pre-fork mode), then the exact known child
        is held (SIGSTOP), ended (SIGKILL, exit observed without
        reaping) or left running, and the controlled fault is raised
        before the constructor returns.  The owning instance is
        captured for the test's own failure-safe reap."""
        real_execute = getattr(subprocess.Popen, "_execute_child")  # noqa: B009
        flexible_execute = cast("Callable[..., None]", real_execute)

        def fault_execute(
            self_p: subprocess.Popen[bytes], *args: object, **kwargs: object
        ) -> None:
            previous = captured.get("calls", 0)
            assert isinstance(previous, int)
            captured["calls"] = previous + 1
            if pre_fault is not None:
                captured["proc"] = self_p
                captured["pid"] = None
                raise pre_fault("controlled pre-fork start interruption")
            flexible_execute(self_p, *args, **kwargs)
            pid = self_p.pid
            captured["proc"] = self_p
            captured["pid"] = pid
            if post_create == "stop":
                os.kill(pid, signal.SIGSTOP)
                until = time.monotonic() + _HELD_CHILD_OBSERVE_SECONDS
                while (
                    _proc_state(pid) != "T"
                    and time.monotonic() < until
                ):
                    time.sleep(0.005)
                if _proc_state(pid) != "T":
                    raise AssertionError(
                        "controlled held-child state not established"
                    )
                captured["state"] = "T"
                raise KeyboardInterrupt("controlled post-create start interruption")
            if post_create == "end":
                os.kill(pid, signal.SIGKILL)
                until = time.monotonic() + _HELD_CHILD_OBSERVE_SECONDS
                while time.monotonic() < until:
                    if _waitid_observed(pid) is not None:
                        break
                    time.sleep(0.005)
                else:
                    raise AssertionError(
                        "ended child exit not observed within bound"
                    )
                captured["state"] = "ended"
                raise KeyboardInterrupt("controlled post-create start interruption")
            if post_create != "none":
                raise AssertionError("unknown post_create mode")

        return mock.patch.object(
            subprocess.Popen, "_execute_child", fault_execute
        )

    def _patch_pipe(
        self,
        pairs: list[tuple[int, int]],
        second_fault: Callable[[str], BaseException] | None = None,
    ) -> mock._patch[object]:
        real_pipe = os.pipe
        calls = [0]

        def flaky_pipe() -> tuple[int, int]:
            calls[0] += 1
            if calls[0] == 2 and second_fault is not None:
                raise second_fault(
                    "controlled second-pipe allocation failure"
                )
            pair = real_pipe()
            pairs.append(pair)
            return pair

        return mock.patch.object(os, "pipe", flaky_pipe)

    def _fail_safe_reap_known_child(self, captured: dict[str, object]) -> None:
        """Failure-safe cleanup of this test's known real child: when
        the actual Popen instance retained at construction still
        reports a live child, resume, terminate, SIGKILL-escalate,
        and actually wait it with a bounded timeout; an already
        ended/reaped child is a no-op.  It signals only the exact
        known object (no global waitpid, no pid-recycling risk), and
        it never converts a failing product assertion into a pass:
        assertions run before this cleanup, which only prevents an
        orphaned known child."""
        proc = captured.get("proc")
        if not isinstance(proc, subprocess.Popen):
            return
        if getattr(proc, "pid", None) is None:
            # Never-created pre-allocated instance: nothing to signal
            # or wait; poll/wait would raise on the unset pid.
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


def _fault_popen(fault: type[BaseException]) -> type[subprocess.Popen[bytes]]:
    """Temporary local subclass (module-bound, never a global class-
    slot mutation) whose ``__new__`` raises the controlled fault, so
    process-object allocation itself fails before any child can be
    created (order 023-a, requirement 6)."""

    class _FaultPopen(subprocess.Popen[bytes]):
        _fault: type[BaseException] = fault

        def __new__(cls, *args: object, **kwargs: object) -> _FaultPopen:
            raise cls._fault("controlled process-object allocation failure")

    return _FaultPopen


class PandocStartInterruptionTests(_OwnedBoundaryBase):
    """Order 023-a requirement 2/5: the real protect_with_pandoc
    boundary owns the exact Pandoc process object before the
    fallible constructor can create a child, on every
    never-created/created-held/created-ended/allocation-failure
    state, with the qualified real binary."""

    def test_prefork_interrupt_never_created_sentinel_untouched(self) -> None:
        captured: dict[str, object] = {}
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_execute(
                captured, pre_fault=KeyboardInterrupt
            ), self.assertRaises(KeyboardInterrupt) as ctx:
                pp.protect_with_pandoc(_spec(), "Beseda.")
            self.assertIn("controlled pre-fork", str(ctx.exception))
            proc = captured["proc"]
            assert isinstance(proc, subprocess.Popen)
            self.assertIsNone(proc.pid)
            self.assertEqual(captured["calls"], 1)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            self._fail_safe_reap_known_child(captured)
            sentinel.reap()

    def test_held_child_reaped_before_return(self) -> None:
        captured: dict[str, object] = {}
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_execute(
                captured, post_create="stop"
            ), self.assertRaises(KeyboardInterrupt) as ctx:
                pp.protect_with_pandoc(_spec(), "Beseda.")
            self.assertIn("controlled post-create", str(ctx.exception))
            pid = captured["pid"]
            assert isinstance(pid, int)
            proc = captured["proc"]
            assert isinstance(proc, subprocess.Popen)
            self.assertEqual(captured["state"], "T")
            # The product must have terminated/killed and actually
            # wait/reaped the exact known held child BEFORE return:
            # a WNOHANG probe now finds no child at all.
            with self.assertRaises(ChildProcessError):
                os.waitpid(pid, os.WNOHANG)
            self.assertEqual(proc.returncode, -9)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            self._fail_safe_reap_known_child(captured)
            sentinel.reap()

    def test_ended_child_reaped_before_return(self) -> None:
        captured: dict[str, object] = {}
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_execute(
                captured, post_create="end"
            ), self.assertRaises(KeyboardInterrupt) as ctx:
                pp.protect_with_pandoc(_spec(), "Beseda.")
            self.assertIn("controlled post-create", str(ctx.exception))
            pid = captured["pid"]
            assert isinstance(pid, int)
            proc = captured["proc"]
            assert isinstance(proc, subprocess.Popen)
            self.assertEqual(captured["state"], "ended")
            with self.assertRaises(ChildProcessError):
                os.waitpid(pid, os.WNOHANG)
            # The exact child's actual SIGKILL exit status, not a
            # fabricated one: reaping the already-ended child must
            # report how it really died.
            self.assertEqual(proc.returncode, -9)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            self._fail_safe_reap_known_child(captured)
            sentinel.reap()

    def test_preallocation_failure_preserves_control(self) -> None:
        for fault in (MemoryError, KeyboardInterrupt):
            with self.subTest(fault=fault.__name__):
                sentinel = _Sentinel()
                before = _fds()
                try:
                    with mock.patch.object(
                        subprocess, "Popen", _fault_popen(fault)
                    ), self.assertRaises(fault) as ctx:
                        pp.protect_with_pandoc(_spec(), "Beseda.")
                    self.assertIn(
                        "controlled process-object allocation", str(ctx.exception)
                    )
                    sentinel.assert_untouched()
                    self._assert_no_new_fds(before)
                finally:
                    sentinel.reap()

    def test_ordinary_not_found_then_healthy_subsequent(self) -> None:
        missing = pp.PandocSpec(binary=str(ROOT / "no-such-pandoc-023"))
        # Fail-closed at the real caller boundary: the startup failure
        # is converted to a non-ok outcome with the fixed reason; the
        # raising boundary (parse_document/check_pandoc) keeps
        # PandocStartupError, which this boundary consumes.
        outcome = pp.protect_with_pandoc(missing, "Beseda.")
        self.assertFalse(outcome.ok)
        self.assertEqual(outcome.reason, pp.REASON_NOT_FOUND)
        self.assertEqual(outcome.granted, ())
        # Healthy subsequent invocation through the same real caller
        # boundary with the qualified binary: the actual version and
        # capability checks run before any parse, and exact original
        # prose spans are granted.
        spec = _spec()
        pp.check_pandoc(spec)
        outcome = pp.protect_with_pandoc(spec, _HEALTHY_BODY)
        self.assertTrue(outcome.ok)
        self.assertIsNone(outcome.reason)
        self.assertGreaterEqual(len(outcome.granted), 1)
        text_len = len(_HEALTHY_BODY)
        for start, end in outcome.granted:
            self.assertGreaterEqual(start, 0)
            self.assertLessEqual(end, text_len)
            self.assertGreater(end, start)


class ReviewerStartInterruptionTests(_OwnedBoundaryBase):
    """Order 023-a requirement 3/5: the real run_review_exchange
    boundary owns each pipe as it is created and the exact process
    object before the fallible start, on every
    allocation-failure/never-created/created-held/created-ended
    state, with the production worker and an owned loopback main."""

    def setUp(self) -> None:
        self.server: ThreadingHTTPServer | None = None
        self.thread: threading.Thread | None = None

    def tearDown(self) -> None:
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
        if self.thread is not None:
            self.thread.join(5)
            self.assertFalse(self.thread.is_alive())

    def _start_main(self) -> int:
        _RecordingMain.requests = []
        _RecordingMain.payload = _HEALTHY_PAYLOAD
        assert self.server is None
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _RecordingMain)
        self.thread = threading.Thread(
            target=self.server.serve_forever, daemon=True
        )
        self.thread.start()
        return self.server.server_address[1]

    def _exchange(
        self,
        port: int,
        *,
        worker: Path | None = None,
        budget: float = 30.0,
        body: bytes = b"x",
        auth: str | None = None,
    ) -> tuple[int, bytes]:
        return rt.run_review_exchange(
            scheme="http",
            host="127.0.0.1",
            port=port,
            path="/v1/responses",
            body=body,
            auth=auth,
            deadline=time.monotonic() + budget,
            worker_path=worker if worker is not None else WORKER,
        )

    def _assert_all_owned_fds_closed(
        self,
        pairs: list[tuple[int, int]],
        *,
        product_pairs: int,
    ) -> None:
        # The first product_pairs pairs are the product's owned
        # request/response pipes.  A fault injected after the real
        # child creation additionally records CPython's internal
        # error-reporting pipe, which the interpreter itself closes
        # before the seam raises.  Every recorded descriptor must be
        # closed before product return.
        self.assertGreaterEqual(len(pairs), product_pairs)
        self.assertLessEqual(len(pairs), product_pairs + 1)
        for read_fd, write_fd in pairs:
            self._assert_fd_closed(read_fd)
            self._assert_fd_closed(write_fd)

    def test_second_pipe_keyboard_interrupt(self) -> None:
        self._second_pipe_fault(KeyboardInterrupt)

    def test_second_pipe_memory_error(self) -> None:
        self._second_pipe_fault(MemoryError)

    def _second_pipe_fault(self, fault: type[BaseException]) -> None:
        port = self._start_main()
        captured: dict[str, object] = {}
        pairs: list[tuple[int, int]] = []
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_pipe(pairs, fault), self._patch_execute(
                captured
            ), self.assertRaises(fault) as ctx:
                self._exchange(port)
            self.assertIn("controlled second-pipe", str(ctx.exception))
            # Only the first pipe was allocated; the fault landed on
            # the second allocation: both already-owned descriptors
            # are closed before return and no child exists.
            self.assertEqual(len(pairs), 1)
            self._assert_fd_closed(pairs[0][0])
            self._assert_fd_closed(pairs[0][1])
            self.assertEqual(captured.get("calls", 0), 0)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            sentinel.reap()

    def test_second_pipe_oserror_keeps_fixed_label(self) -> None:
        port = self._start_main()
        captured: dict[str, object] = {}
        pairs: list[tuple[int, int]] = []
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_pipe(
                pairs, lambda message: OSError(24, "EMFILE")
            ), self._patch_execute(captured), self.assertRaises(rt.ReviewTransportError) as ctx:
                self._exchange(port)
            self.assertEqual(ctx.exception.reason, REASON_HTTP_FAILED)
            cause = ctx.exception.__cause__
            assert isinstance(cause, OSError)
            self.assertEqual(cause.errno, 24)
            self.assertEqual(len(pairs), 1)
            self._assert_fd_closed(pairs[0][0])
            self._assert_fd_closed(pairs[0][1])
            self.assertEqual(captured.get("calls", 0), 0)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            sentinel.reap()

    def test_prefork_interrupt_closes_all_owned_fds(self) -> None:
        port = self._start_main()
        captured: dict[str, object] = {}
        pairs: list[tuple[int, int]] = []
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_pipe(pairs), self._patch_execute(
                captured, pre_fault=KeyboardInterrupt
            ), self.assertRaises(KeyboardInterrupt) as ctx:
                self._exchange(port)
            self.assertIn("controlled pre-fork", str(ctx.exception))
            self._assert_all_owned_fds_closed(pairs, product_pairs=2)
            proc = captured["proc"]
            assert isinstance(proc, subprocess.Popen)
            self.assertIsNone(proc.pid)
            self.assertEqual(captured["calls"], 1)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            self._fail_safe_reap_known_child(captured)
            sentinel.reap()

    def test_held_child_reaped_before_return(self) -> None:
        port = self._start_main()
        captured: dict[str, object] = {}
        pairs: list[tuple[int, int]] = []
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_pipe(pairs), self._patch_execute(
                captured, post_create="stop"
            ), self.assertRaises(KeyboardInterrupt) as ctx:
                self._exchange(port)
            self.assertIn("controlled post-create", str(ctx.exception))
            pid = captured["pid"]
            assert isinstance(pid, int)
            proc = captured["proc"]
            assert isinstance(proc, subprocess.Popen)
            self.assertEqual(captured["state"], "T")
            with self.assertRaises(ChildProcessError):
                os.waitpid(pid, os.WNOHANG)
            self.assertEqual(proc.returncode, -9)
            self._assert_all_owned_fds_closed(pairs, product_pairs=2)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            self._fail_safe_reap_known_child(captured)
            sentinel.reap()

    def test_ended_child_reaped_before_return(self) -> None:
        port = self._start_main()
        captured: dict[str, object] = {}
        pairs: list[tuple[int, int]] = []
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_pipe(pairs), self._patch_execute(
                captured, post_create="end"
            ), self.assertRaises(KeyboardInterrupt) as ctx:
                self._exchange(port)
            self.assertIn("controlled post-create", str(ctx.exception))
            pid = captured["pid"]
            assert isinstance(pid, int)
            proc = captured["proc"]
            assert isinstance(proc, subprocess.Popen)
            self.assertEqual(captured["state"], "ended")
            with self.assertRaises(ChildProcessError):
                os.waitpid(pid, os.WNOHANG)
            self.assertEqual(proc.returncode, -9)
            self._assert_all_owned_fds_closed(pairs, product_pairs=2)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            self._fail_safe_reap_known_child(captured)
            sentinel.reap()

    def test_preallocation_failure_preserves_control(self) -> None:
        port = self._start_main()
        for fault in (MemoryError, KeyboardInterrupt):
            with self.subTest(fault=fault.__name__):
                pairs: list[tuple[int, int]] = []
                sentinel = _Sentinel()
                before = _fds()
                try:
                    with self._patch_pipe(pairs), mock.patch.object(
                        subprocess, "Popen", _fault_popen(fault)
                    ), self.assertRaises(fault) as ctx:
                        self._exchange(port)
                    self.assertIn(
                        "controlled process-object allocation", str(ctx.exception)
                    )
                    self._assert_all_owned_fds_closed(pairs, product_pairs=2)
                    sentinel.assert_untouched()
                    self._assert_no_new_fds(before)
                finally:
                    sentinel.reap()

    def test_ordinary_worker_failure_then_healthy_subsequent(self) -> None:
        port = self._start_main()
        with self.assertRaises(rt.ReviewTransportError) as ctx:
            self._exchange(
                port, worker=ROOT / "no-such-review-worker-023.py"
            )
        self.assertEqual(ctx.exception.reason, REASON_HTTP_FAILED)
        # Healthy subsequent invocation at the same real boundary:
        # the production worker and the owned loopback main complete
        # the exchange and the exact payload is transferred.
        status, payload = self._exchange(port)
        self.assertEqual(status, 200)
        self.assertEqual(payload, _HEALTHY_PAYLOAD)
        self.assertEqual(len(_RecordingMain.requests), 1)
        self.assertEqual(_RecordingMain.requests[0]["path"], "/v1/responses")

    def test_healthy_review_boundary(self) -> None:
        port = self._start_main()
        status, payload = self._exchange(port)
        self.assertEqual(status, 200)
        self.assertEqual(payload, _HEALTHY_PAYLOAD)
        self.assertEqual(len(_RecordingMain.requests), 1)


class _RecordingMain(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    payload: bytes = _HEALTHY_PAYLOAD
    requests: list[dict[str, object]] = []

    def do_POST(self) -> None:  # noqa: N802
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.__class__.requests.append(
            {
                "path": self.path,
                "body": body,
                "auth": self.headers.get("Authorization"),
            }
        )
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(self.__class__.payload)))
        self.end_headers()
        self.wfile.write(self.__class__.payload)

    def log_message(self, *_args: object) -> None:
        return


class NativeSupervisedHeldChildTests(_OwnedBoundaryBase):
    """Order 023-a requirement 6: the potentially-hanging native
    held-child scenarios run as isolated script processes under a
    finite owned parent supervisor of an exact process group.  The
    script owns the real product boundary (real binary/worker, real
    argv/env), writes the exact known child pid for parent
    verification, and carries its own fail-safe finally that
    terminates/kills/reaps ONLY the exact captured child — including
    the Pandoc child whose owned session escapes the script's
    process group.  A forced parent escape is a FAILED outcome,
    never a pass."""

    _SCRIPT = '''import contextlib
import json
import os
import pathlib
import signal
import subprocess
import sys
import time

sys.path.insert(0, "@ROOT@")
import pandoc_protection as pp  # noqa: E402
import review_transport as rt  # noqa: E402

case = sys.argv[1]
workdir = sys.argv[2]
port = int(sys.argv[3])
captured = {}
real_execute = subprocess.Popen._execute_child


def fault_execute(self, *args, **kwargs):
    real_execute(self, *args, **kwargs)
    pid = self.pid
    captured["pid"] = pid
    captured["proc"] = self
    with open(os.path.join(workdir, "child-pid"), "w") as f:
        f.write(str(pid))
    os.kill(pid, signal.SIGSTOP)
    time.sleep(0.05)
    state = open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[0]
    captured["state"] = state
    raise KeyboardInterrupt("controlled start interruption")


subprocess.Popen._execute_child = fault_execute
result = {"ok": False}
try:
    if case == "pandoc":
        spec = pp.PandocSpec(binary=os.environ["CONCEPT_PANDOC"])
        pp.protect_with_pandoc(spec, "Beseda.")
        result["why"] = "no-interrupt"
    else:
        rt.run_review_exchange(
            scheme="http",
            host="127.0.0.1",
            port=port,
            path="/v1/responses",
            body=b"x",
            auth=None,
            deadline=time.monotonic() + 20,
            worker_path=pathlib.Path("@WORKER@"),
        )
        result["why"] = "no-interrupt"
    print("RESULT " + json.dumps(result))
    sys.exit(2)
except KeyboardInterrupt as exc:
    result["ok"] = "controlled start interruption" in str(exc)
    pid = captured.get("pid")
    if isinstance(pid, int):
        try:
            os.waitpid(pid, os.WNOHANG)
            result["reaped"] = False
            result["why"] = "child-not-reaped"
        except ChildProcessError:
            result["reaped"] = True
    result["state"] = captured.get("state")
    print("RESULT " + json.dumps(result))
    sys.exit(0 if result.get("ok") and result.get("reaped") else 4)
finally:
    # Script-side failure-safe cleanup of the exact captured child
    # AFTER every observation: on a product regression the stopped
    # child must not outlive this process; the failed rc above is
    # kept, never converted into a pass by the cleanup.  This is
    # what covers the Pandoc child, whose owned session escapes the
    # script's process group.
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
'''

    def _write_script(self, temp: str) -> Path:
        script = Path(temp) / "held_child_supervisor.py"
        script.write_text(
            self._SCRIPT.replace("@ROOT@", str(ROOT)).replace(
                "@WORKER@", str(WORKER)
            )
        )
        script.chmod(0o700)
        return script

    def _run_supervised_tree(
        self,
        script: Path,
        case: str,
        port: int,
        workdir: Path,
    ) -> tuple[int, str, str]:
        """Finite owned parent supervision of the exact owned
        process group, plus exact-identity verification of the known
        native child after any forced escape (that child may sit in
        its own session outside the group).  Every outcome — natural
        exit, nonzero exit, forced escape, unexpected exception —
        leaves no owned child alive and reaps/cleans what it can."""
        proc = subprocess.Popen(
            [
                sys.executable,
                "-I",
                "-B",
                str(script),
                case,
                str(workdir),
                str(port),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            timed_out = False
            try:
                out, err = proc.communicate(timeout=PARENT_BOUND_SECONDS)
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
            # Exact known identity: the registered native child may
            # have escaped the group (owned session).  The parent is
            # not its parent, so it cannot waitpid it; it resumes and
            # SIGKILLs the exact known pid and verifies death by
            # bounded /proc observation (the subreaper/init reaps it).
            known: int | None = None
            pid_file = workdir / "child-pid"
            if pid_file.exists():
                known = int(pid_file.read_text())
                if _proc_state(known) is not None:
                    with contextlib.suppress(OSError):
                        os.kill(known, signal.SIGCONT)
                    with contextlib.suppress(OSError):
                        os.kill(known, signal.SIGKILL)
                    until = time.monotonic() + _HELD_CHILD_OBSERVE_SECONDS
                    while (
                        _proc_state(known) is not None
                        and time.monotonic() < until
                    ):
                        time.sleep(0.01)
            if timed_out:
                with contextlib.suppress(OSError):
                    os.killpg(proc.pid, signal.SIGKILL)
                with contextlib.suppress(subprocess.TimeoutExpired):
                    proc.wait(timeout=10)
                self.fail(
                    "owned supervised start-interruption tree exceeded "
                    f"the finite parent bound {PARENT_BOUND_SECONDS}s and "
                    "was terminated/killed/reaped: the product did not "
                    "reap the held child. stderr tail: "
                    + err.decode("utf-8", "replace")[-2000:]
                )
            self.assertIsNotNone(proc.returncode)
            self.assertIsNone(_proc_state(known) if known is not None else None)
            return (
                proc.returncode,
                out.decode("utf-8", "replace"),
                err.decode("utf-8", "replace"),
            )
        finally:
            if proc.poll() is None:
                with contextlib.suppress(OSError):
                    os.killpg(proc.pid, signal.SIGKILL)
                with contextlib.suppress(subprocess.TimeoutExpired):
                    proc.wait(timeout=10)

    def _assert_result(self, rc: int, out: str, err: str) -> None:
        self.assertEqual(rc, 0, err[-2000:])
        lines = out.splitlines()
        result_line = next(
            (line for line in lines if line.startswith("RESULT ")), None
        )
        assert result_line is not None
        payload = json.loads(result_line[len("RESULT "):])
        self.assertIs(payload.get("ok"), True)
        self.assertTrue(payload.get("reaped") is True)
        self.assertEqual(payload.get("state"), "T")

    def test_pandoc_held_child_under_finite_supervised_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp)
            workdir.chmod(0o700)
            script = self._write_script(temp)
            rc, out, err = self._run_supervised_tree(
                script, "pandoc", 0, workdir
            )
            self._assert_result(rc, out, err)

    def test_reviewer_held_child_under_finite_supervised_tree(self) -> None:
        server: ThreadingHTTPServer | None = None
        thread: threading.Thread | None = None
        try:
            _RecordingMain.requests = []
            _RecordingMain.payload = _HEALTHY_PAYLOAD
            server = ThreadingHTTPServer(("127.0.0.1", 0), _RecordingMain)
            thread = threading.Thread(
                target=server.serve_forever, daemon=True
            )
            thread.start()
            with tempfile.TemporaryDirectory() as temp:
                workdir = Path(temp)
                workdir.chmod(0o700)
                script = self._write_script(temp)
                rc, out, err = self._run_supervised_tree(
                    script, "review", server.server_address[1], workdir
                )
                self._assert_result(rc, out, err)
        finally:
            if server is not None:
                server.shutdown()
                server.server_close()
            if thread is not None:
                thread.join(5)
                self.assertFalse(thread.is_alive())


if __name__ == "__main__":
    unittest.main()
