"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.
Owned Pandoc/reviewer partial-startup cleanup (order 023-a).

Bounded ownership proofs at the actual product boundary: the real
``protect_with_pandoc`` (qualified installed 3.7.0.2 binary, real
CPython ``Popen``) and the real ``run_review_exchange`` (production
``review_worker.py``, owned loopback main).  Controlled real
call-through fault seams at ``subprocess.Popen._execute_child``,
``os.pipe`` and ``_make_pipe_nonblocking`` cover: caller
interruption before child creation (never-created), after actual
child creation with the child scheduler-held (SIGSTOP) or already
ended, first-pipe registration-gap and second-pipe allocation
KeyboardInterrupt/MemoryError with exact injected-exception
identity, second-pipe and nonblocking fcntl setup OSError with the
fixed label, and process-object allocation failure itself.  Every
case proves ownership, reaping and FD cleanup
BEFORE test cleanup: the known owned child is actually wait/reaped
before product return, the exact owned descriptors are closed, the
original nonordinary exception identity is preserved, ordinary
failures keep their fixed labels, and a known unrelated sentinel
child of the test process remains untouched (no ``waitpid(-1)``, no
global group signal).  The potentially-hanging native held-child
cases run under a finite owned parent supervisor of an isolated
process group: the script registers EVERY known owned fixture
child - the product child and the script's own unrelated sentinel,
each with exact PID plus /proc start identity - BEFORE the
controlled fault, the test process installs the per-process child
subreaper, and the supervisor actually waits/reaps the complete
registered owned set on every outer exit path - natural exit,
forced timeout escape and unexpected exception - never touching a
recycled PID, with product-child reap attribution kept separate
from the fixture-sentinel cleanup; the optional observed metadata
never gates the cleanup; supervisor self-proof fixtures with
declared fixture faults exercise the timeout and unexpected-
exception cleanup paths, including on the actual held script, and
a forced escape is a FAILED outcome, never a pass.

Controlled fault evidence only: no claim of spontaneous native
failure, completed linguistic qualification, live-model or
deployment behavior.  The qualified Pandoc binary comes from
``CONCEPT_PANDOC`` (no PATH discovery or fallback); required cases
do not skip.
"""

from __future__ import annotations

import contextlib
import ctypes
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


def _proc_start_ticks(pid: int) -> int | None:
    """The /proc start identity (stat field 22) of a known PID, or
    None when the PID does not exist: the durable identity half of
    exact-child verification (a recycled PID shows a different start
    identity or is absent)."""
    try:
        parts = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return int(parts[19])
    except (FileNotFoundError, ProcessLookupError, ValueError, IndexError):
        return None


_SUBREAPER_INSTALLED = False


def _ensure_child_subreaper() -> None:
    """Install PR_SET_CHILD_SUBREAPER on THIS test process exactly
    once, so an orphaned registered grandchild (for example the
    new-session child of a killed supervisor script) is adopted here
    and can be actually wait/reaped by the exact PID.  Per-process
    Linux containment only: no process scans, no global reaping, no
    signal broadcast (order 023-a, requirement 6)."""
    global _SUBREAPER_INSTALLED
    if _SUBREAPER_INSTALLED:
        return
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), "PR_SET_CHILD_SUBREAPER failed")
    _SUBREAPER_INSTALLED = True


def _reap_exact_owned_pid(pid: int, start_ticks: int) -> dict[str, object]:
    """Bounded exact-identity cleanup/reap of one registered owned
    child.  Only the exact registered PID is considered, verified
    against its /proc start identity so a recycled PID can never be
    touched; the test process is the per-process child subreaper, so
    a still-alive registered child is actually wait/reaped here.
    Returns an observation record; it only prevents an orphaned known
    child and never converts a failing outcome into a pass."""
    record: dict[str, object] = {"pid": pid}
    current = _proc_start_ticks(pid)
    if current is None:
        # PID absent: the known child already exited and was reaped
        # (by the product or the script's own cleanup) before this.
        record["pid_gone"] = True
        record["reaped_by_supervisor"] = False
        return record
    if current != start_ticks:
        # PID recycled to an unrelated process: never touch it.
        record["pid_recycled"] = True
        record["reaped_by_supervisor"] = False
        return record
    with contextlib.suppress(ProcessLookupError):
        os.kill(pid, signal.SIGCONT)
    with contextlib.suppress(ProcessLookupError):
        os.kill(pid, signal.SIGKILL)
    try:
        waited, status = os.waitpid(pid, 0)
    except ChildProcessError:
        record["pid_gone"] = True
        record["reaped_by_supervisor"] = False
        return record
    record["reaped_by_supervisor"] = waited == pid
    record["waited_pid"] = waited
    record["wait_status"] = status
    return record


def _reap_registered_child(
    workdir: Path,
) -> tuple[dict[str, object], dict[str, object] | None]:
    """Clean/reap EVERY registered owned fixture child (the product
    child and the script's unrelated sentinel) by exact PID + /proc
    start identity on every outer outcome.  A flat single-entry
    registry ({"pid", "start_ticks"}) is accepted as a product-only
    registration.  Returns (product_record, sentinel_record); the
    product record is {"registered": False} when nothing was
    registered.  No process scans, no waitpid(-1), no action on
    recycled or unowned PIDs."""
    path = workdir / "registered-child.json"
    if not path.exists():
        return ({"registered": False}, None)
    known = json.loads(path.read_text())
    if isinstance(known, dict) and isinstance(known.get("entries"), list):
        entries = [
            entry for entry in known["entries"]
            if isinstance(entry, dict)
        ]
    else:
        entries = [{"role": "product", **known}]
    product: dict[str, object] = {"registered": False}
    sentinel: dict[str, object] | None = None
    for entry in entries:
        record = _reap_exact_owned_pid(int(entry["pid"]), int(entry["start_ticks"]))
        if entry.get("role") == "sentinel":
            sentinel = record
        else:
            product = record
    return (product, sentinel)


HELD_CHILD_SCRIPT = '''import contextlib
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
    parts = open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()
    entry = {
        "role": "product",
        "pid": pid,
        "start_ticks": int(parts[19]),
        "pgid": os.getpgid(pid),
        "argv": list(self.args),
    }
    reg_path = os.path.join(workdir, "registered-child.json")
    try:
        entries = json.loads(open(reg_path).read()).get("entries", [])
    except (FileNotFoundError, ValueError):
        entries = []
    entries.append(entry)
    with open(reg_path, "w") as f:
        json.dump({"entries": entries}, f)
    os.kill(pid, signal.SIGSTOP)
    time.sleep(0.05)
    state = open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[0]
    captured["state"] = state
    if case.endswith("-stall"):
        # Declared fixture fault: a stalled cleanup that never
        # returns, forcing the supervisor's bounded timeout.
        time.sleep(300)
    raise KeyboardInterrupt("controlled post-create start interruption")


def proc_state(pid):
    try:
        return pathlib.Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
    except (FileNotFoundError, ProcessLookupError):
        return None


def fds():
    return {int(name) for name in os.listdir("/proc/self/fd")}


# A known unrelated owned child of THIS process (the process that runs
# the product boundary): it exits on its own and stays an unreaped
# zombie; a product global wait or wrong-group signal would detach or
# kill it.  Created BEFORE the controlled start seam is installed, so
# the sentinel spawn itself is a plain real start.
sentinel = subprocess.Popen(
    [sys.executable, "-B", "-c", "pass"],
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
sentinel_pid = sentinel.pid
until = time.monotonic() + 5.0
while proc_state(sentinel_pid) != "Z" and time.monotonic() < until:
    time.sleep(0.005)
if proc_state(sentinel_pid) != "Z":
    print("RESULT " + json.dumps({"ok": False, "why": "sentinel-not-zombie"}))
    sys.exit(5)

# Register the sentinel (the script's own unrelated owned child) with
# exact PID + start identity BEFORE the controlled fault, so the
# parent supervisor can clean/reap every owned fixture child on every
# outer outcome.
s_parts = (
    pathlib.Path(f"/proc/{sentinel_pid}/stat")
    .read_text()
    .rsplit(")", 1)[1]
    .split()
)
sentinel_entry = {
    "role": "sentinel",
    "pid": sentinel_pid,
    "start_ticks": int(s_parts[19]),
}
with open(os.path.join(workdir, "registered-child.json"), "w") as f:
    json.dump({"entries": [sentinel_entry]}, f)

subprocess.Popen._execute_child = fault_execute
before = fds()
result = {"ok": False}
try:
    if case.startswith("pandoc"):
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
    result["interrupt_message_ok"] = (
        "controlled post-create start interruption" in str(exc)
    )
    result["state"] = captured.get("state")
    pid = captured.get("pid")
    if isinstance(pid, int):
        # The product must have terminated/killed and actually
        # wait/reaped the exact known held child BEFORE return: a
        # WNOHANG probe now finds no child at all.
        try:
            os.waitpid(pid, os.WNOHANG)
            result["reaped"] = False
            result["why"] = "child-not-reaped"
        except ChildProcessError:
            result["reaped"] = True
        result["returncode"] = captured["proc"].returncode
    # Sentinel untouched: still an unreaped zombie of this process
    # with its own clean exit status.
    try:
        observed = os.waitid(
            os.P_PID, sentinel_pid, os.WEXITED | os.WNOHANG | os.WNOWAIT
        )
        result["sentinel_untouched"] = (
            observed is not None
            and observed[0] == sentinel_pid
            and observed[4] == os.CLD_EXITED
            and observed[3] == 0
        )
    except ChildProcessError:
        result["sentinel_untouched"] = False
    # No owned descriptor survives the product return.
    result["no_new_fds"] = before.issuperset(fds())
    result["ok"] = (
        result.get("interrupt_message_ok") is True
        and result.get("state") == "T"
        and result.get("reaped") is True
        and result.get("returncode") == -9
        and result.get("sentinel_untouched") is True
        and result.get("no_new_fds") is True
    )
    print("RESULT " + json.dumps(result))
    sys.exit(0 if result["ok"] else 4)
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
    # Reap the script's own sentinel child, after every observation.
    with contextlib.suppress(ChildProcessError):
        os.waitpid(sentinel_pid, 0)
'''


def write_held_child_script(temp: str) -> Path:
    script = Path(temp) / "held_child_supervisor.py"
    script.write_text(
        HELD_CHILD_SCRIPT.replace("@ROOT@", str(ROOT)).replace(
            "@WORKER@", str(WORKER)
        )
    )
    script.chmod(0o700)
    return script


def run_supervised_tree(
    script: Path,
    case: str,
    port: int,
    workdir: Path,
    *,
    bound: float = PARENT_BOUND_SECONDS,
    observed: dict[str, object] | None = None,
) -> tuple[int, str, str]:
    """Finite owned parent supervision of the exact owned process
    group, plus exact-identity reap of the complete registered
    owned set (the product child and the script's sentinel).
    The test process is the per-process child subreaper, so on
    EVERY outer exit path - natural exit, nonzero exit, forced
    timeout escape, unexpected exception - every exact registered
    child (verified by PID and /proc start identity; a recycled
    PID is never touched) is actually wait/reaped here, the script
    group is killed, and the script is actually waited.  The exact
    cleanup is unconditional; the optional ``observed`` mapping
    only carries the resulting metadata and never gates it.  A
    forced escape is a FAILED outcome for the supervised case,
    never a pass."""
    _ensure_child_subreaper()
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
    if observed is not None:
        observed["script_pid"] = proc.pid
    timed_out = False
    out = b""
    err = b""

    def _close_script_pipes() -> None:
        for stream in (proc.stdout, proc.stderr):
            if stream is not None:
                with contextlib.suppress(OSError):
                    stream.close()

    try:
        try:
            out, err = proc.communicate(timeout=bound)
        except subprocess.TimeoutExpired:
            timed_out = True
            # Bounded forced escape: SIGKILL the exact group
            # directly (a SIGTERM stage cannot guarantee the
            # script's Python finally runs) and wait the script.
            with contextlib.suppress(OSError):
                os.killpg(proc.pid, signal.SIGKILL)
            out, err = proc.communicate(timeout=5)
    except BaseException:
        # Unexpected-exception path: kill the exact group, wait the
        # script, close its pipes, actually reap the exact registered
        # child, then re-raise the original exception (test failure).
        with contextlib.suppress(OSError):
            os.killpg(proc.pid, signal.SIGKILL)
        with contextlib.suppress(subprocess.TimeoutExpired):
            proc.wait(timeout=5)
        _close_script_pipes()
        product_record, sentinel_record = _reap_registered_child(workdir)
        if observed is not None:
            observed["script_exit"] = proc.returncode
            observed["child"] = product_record
            if sentinel_record is not None:
                observed["sentinel"] = sentinel_record
        raise
    finally:
        if proc.poll() is None:
            with contextlib.suppress(OSError):
                os.killpg(proc.pid, signal.SIGKILL)
            with contextlib.suppress(subprocess.TimeoutExpired):
                proc.wait(timeout=10)
            _close_script_pipes()
    product_record, sentinel_record = _reap_registered_child(workdir)
    if observed is not None:
        observed["script_exit"] = proc.returncode
        observed["child"] = product_record
        if sentinel_record is not None:
            observed["sentinel"] = sentinel_record
    assert proc.returncode is not None
    if timed_out:
        raise AssertionError(
            "owned supervised start-interruption tree exceeded "
            f"the finite parent bound {bound}s and was "
            "terminated/killed/reaped: the supervised case did "
            "not finish in bound. stderr tail: "
            + err.decode("utf-8", "replace")[-2000:]
        )
    return (
        proc.returncode,
        out.decode("utf-8", "replace"),
        err.decode("utf-8", "replace"),
    )


def check_held_child_result(
    test_case: unittest.TestCase,
    rc: int,
    out: str,
    err: str,
    observed: dict[str, object],
) -> None:
    """The preserved direct held-child assertion set (exception
    message, held state, reap before return, exact exit status,
    sentinel untouched, no new FD - all observed inside the
    supervised script BEFORE its cleanup) plus supervisor
    attribution: the product reaped the held child itself; the
    supervisor found the known child no longer present (or the PID
    already recycled) and had nothing to reap; the registered
    sentinel is either already reaped by the script's own finally
    (exact identity gone) or reaped by the supervisor with the
    sentinel's own clean exit status, never a fabricated
    SIGKILL."""
    test_case.assertEqual(rc, 0, err[-2000:])
    lines = out.splitlines()
    result_line = next(
        (line for line in lines if line.startswith("RESULT ")), None
    )
    assert result_line is not None
    payload = json.loads(result_line[len("RESULT "):])
    test_case.assertIs(payload.get("interrupt_message_ok"), True)
    test_case.assertEqual(payload.get("state"), "T")
    test_case.assertTrue(payload.get("reaped") is True)
    test_case.assertEqual(payload.get("returncode"), -9)
    test_case.assertTrue(payload.get("sentinel_untouched") is True)
    test_case.assertTrue(payload.get("no_new_fds") is True)
    child = observed.get("child")
    test_case.assertIsInstance(child, dict)
    assert isinstance(child, dict)
    test_case.assertIs(child.get("reaped_by_supervisor"), False)
    test_case.assertTrue(
        child.get("pid_gone") is True or child.get("pid_recycled") is True
    )
    test_case.assertNotIn("wait_status", child)
    # The script's own unrelated sentinel: either already reaped by
    # the script's finally before return (exact identity gone) or
    # actually reaped by the supervisor with the sentinel's own
    # clean exit status - never a fabricated SIGKILL status.
    sentinel = observed.get("sentinel")
    test_case.assertIsInstance(sentinel, dict)
    assert isinstance(sentinel, dict)
    if sentinel.get("reaped_by_supervisor") is True:
        status = sentinel.get("wait_status")
        test_case.assertIsInstance(status, int)
        assert isinstance(status, int)
        test_case.assertTrue(os.WIFEXITED(status))
        test_case.assertEqual(os.WEXITSTATUS(status), 0)
        spid = sentinel.get("pid")
        test_case.assertIsInstance(spid, int)
        assert isinstance(spid, int)
        test_case.assertIsNone(_proc_start_ticks(spid))
    else:
        test_case.assertTrue(
            sentinel.get("pid_gone") is True
            or sentinel.get("pid_recycled") is True
        )


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
        second_fault: BaseException | Callable[[str], BaseException] | None = None,
        after_first_fault: BaseException | None = None,
    ) -> mock._patch[object]:
        real_pipe = os.pipe
        calls = [0]

        def flaky_pipe() -> tuple[int, int]:
            calls[0] += 1
            if calls[0] == 2:
                if after_first_fault is not None:
                    # The first pipe is created and assigned to the
                    # product locals; the fault lands before the
                    # second allocation, at the exact registration
                    # gap after first creation.
                    raise after_first_fault
                if second_fault is not None:
                    if isinstance(second_fault, BaseException):
                        raise second_fault
                    raise second_fault(
                        "controlled second-pipe allocation failure"
                    )
            pair = real_pipe()
            pairs.append(pair)
            return pair

        return mock.patch.object(os, "pipe", flaky_pipe)

    def _patch_nonblocking(
        self, fault: BaseException
    ) -> mock._patch[object]:
        """Temporary controlled call-through seam on the real
        ``_make_pipe_nonblocking``: the first (request-write) setup
        runs for real, then the second (response-read) setup raises
        the exact injected instance after BOTH owned pipes exist,
        covering an actual fcntl setup failure (order 023-a,
        requirement 5)."""
        real_setup = rt._make_pipe_nonblocking
        calls = [0]

        def fault_setup(fd: int) -> None:
            calls[0] += 1
            if calls[0] >= 2:
                raise fault
            real_setup(fd)

        return mock.patch.object(rt, "_make_pipe_nonblocking", fault_setup)

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
        # Finite owned parent supervision of the direct held-child
        # case: the real product boundary runs inside an isolated
        # script under the supervisor, so a product regression that
        # fails to terminate/reap the held child is contained and
        # reaped by exact identity - never a pytest hang.  The
        # preserved assertion set (exception message, held state,
        # reap before return, exact exit status, sentinel untouched,
        # no new FD) is observed inside the script before its
        # cleanup and checked here.
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp)
            workdir.chmod(0o700)
            script = write_held_child_script(temp)
            observed: dict[str, object] = {}
            rc, out, err = run_supervised_tree(
                script, "pandoc", 0, workdir, observed=observed
            )
            check_held_child_result(self, rc, out, err, observed)

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
        instance = fault("controlled second-pipe allocation failure")
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_pipe(
                pairs, second_fault=instance
            ), self._patch_execute(captured), self.assertRaises(fault) as ctx:
                self._exchange(port)
            # The exact injected instance object survives the product
            # cleanup and returns to the caller: identity, not merely
            # type or message.
            self.assertIs(ctx.exception, instance)
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
        instance = OSError(24, "EMFILE")
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_pipe(
                pairs, second_fault=instance
            ), self._patch_execute(captured), self.assertRaises(
                rt.ReviewTransportError
            ) as ctx:
                self._exchange(port)
            # Ordinary allocation failure keeps the fixed transport
            # label and preserves the exact original cause object.
            self.assertEqual(ctx.exception.reason, REASON_HTTP_FAILED)
            self.assertIs(ctx.exception.__cause__, instance)
            self.assertEqual(instance.errno, 24)
            self.assertEqual(len(pairs), 1)
            self._assert_fd_closed(pairs[0][0])
            self._assert_fd_closed(pairs[0][1])
            self.assertEqual(captured.get("calls", 0), 0)
            sentinel.assert_untouched()
            self._assert_no_new_fds(before)
        finally:
            sentinel.reap()

    def test_first_pipe_registration_gap_identity(self) -> None:
        # The fault lands AFTER the first pipe is created and
        # recorded and BEFORE the second allocation - the exact
        # registration-gap boundary: both first-pipe descriptors are
        # closed before return with the exact exception identity,
        # and no child was started.
        port = self._start_main()
        for fault_type in (KeyboardInterrupt, MemoryError):
            with self.subTest(fault=fault_type.__name__):
                captured: dict[str, object] = {}
                pairs: list[tuple[int, int]] = []
                instance = fault_type(
                    "controlled first-pipe registration gap"
                )
                sentinel = _Sentinel()
                before = _fds()
                try:
                    with self._patch_pipe(
                        pairs, after_first_fault=instance
                    ), self._patch_execute(captured), self.assertRaises(
                        fault_type
                    ) as ctx:
                        self._exchange(port)
                    self.assertIs(ctx.exception, instance)
                    self.assertEqual(len(pairs), 1)
                    self._assert_fd_closed(pairs[0][0])
                    self._assert_fd_closed(pairs[0][1])
                    self.assertEqual(captured.get("calls", 0), 0)
                    sentinel.assert_untouched()
                    self._assert_no_new_fds(before)
                finally:
                    sentinel.reap()

    def test_nonblocking_setup_identity_and_closure(self) -> None:
        # An actual fcntl setup failure with BOTH owned pipes already
        # created: all four descriptors are closed before return, no
        # child is started, and the exact nonordinary exception
        # identity is preserved.
        port = self._start_main()
        for fault_type in (KeyboardInterrupt, MemoryError):
            with self.subTest(fault=fault_type.__name__):
                captured: dict[str, object] = {}
                pairs: list[tuple[int, int]] = []
                instance = fault_type(
                    "controlled nonblocking setup failure"
                )
                sentinel = _Sentinel()
                before = _fds()
                try:
                    with self._patch_pipe(pairs), self._patch_nonblocking(
                        instance
                    ), self._patch_execute(captured), self.assertRaises(
                        fault_type
                    ) as ctx:
                        self._exchange(port)
                    self.assertIs(ctx.exception, instance)
                    self.assertEqual(len(pairs), 2)
                    self._assert_all_owned_fds_closed(
                        pairs, product_pairs=2
                    )
                    self.assertEqual(captured.get("calls", 0), 0)
                    sentinel.assert_untouched()
                    self._assert_no_new_fds(before)
                finally:
                    sentinel.reap()

    def test_nonblocking_setup_oserror_keeps_fixed_label(self) -> None:
        # Ordinary fcntl setup failure with both pipes created keeps
        # the fixed transport label and the exact original cause.
        port = self._start_main()
        captured: dict[str, object] = {}
        pairs: list[tuple[int, int]] = []
        instance = OSError(22, "EINVAL")
        sentinel = _Sentinel()
        before = _fds()
        try:
            with self._patch_pipe(pairs), self._patch_nonblocking(
                instance
            ), self._patch_execute(captured), self.assertRaises(
                rt.ReviewTransportError
            ) as ctx:
                self._exchange(port)
            self.assertEqual(ctx.exception.reason, REASON_HTTP_FAILED)
            self.assertIs(ctx.exception.__cause__, instance)
            self.assertEqual(instance.errno, 22)
            self.assertEqual(len(pairs), 2)
            self._assert_all_owned_fds_closed(pairs, product_pairs=2)
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
        # Finite owned parent supervision of the direct held-child
        # case: the real product boundary (production worker, owned
        # loopback main) runs inside an isolated script under the
        # supervisor, so a product regression that fails to
        # terminate/reap the held child is contained and reaped by
        # exact identity - never a pytest hang.  The preserved
        # assertion set (exception message, held state, reap before
        # return, exact exit status, sentinel untouched, no new FD
        # including the four owned pipe descriptors) is observed
        # inside the script before its cleanup and checked here.
        port = self._start_main()
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp)
            workdir.chmod(0o700)
            script = write_held_child_script(temp)
            observed: dict[str, object] = {}
            rc, out, err = run_supervised_tree(
                script, "review", port, workdir, observed=observed
            )
            check_held_child_result(self, rc, out, err, observed)

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
    argv/env), registers EVERY known owned fixture child (the
    product child and the script's own unrelated sentinel, each
    with exact PID plus /proc start identity) BEFORE the controlled
    fault, and carries its own fail-safe finally that terminates/
    kills/reaps ONLY the exact captured child and reaps its own
    sentinel after every observation.  The test process installs
    the per-process child subreaper, so on EVERY outer exit path -
    natural exit, forced timeout escape and unexpected exception -
    the supervisor actually waits/reaps the complete registered
    owned set (verified by start identity; a recycled PID is never
    touched), which covers the Pandoc child whose owned session
    escapes the script's process group and the sentinel orphaned
    by the forced escape.  Supervisor self-proof fixtures use declared
    fixture faults and prove containment only, never product
    behavior; a forced escape is a FAILED outcome, never a pass."""

    _HOLD_SCRIPT = '''import json
import os
import pathlib
import signal
import subprocess
import sys
import time

workdir = sys.argv[2]
# Declared fixture faults: an unrelated sentinel child of this script
# plus a held child in its OWN session (the same group-escape
# property as the Pandoc child) that the script never releases - a
# stand-in for a hung product, used only to prove the supervisor's
# bounded cleanup paths (supervisor self-proof, never product
# evidence).
def proc_state(pid):
    try:
        return pathlib.Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
    except (FileNotFoundError, ProcessLookupError):
        return None

sentinel = subprocess.Popen(
    [sys.executable, "-B", "-c", "pass"],
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
until = time.monotonic() + 5.0
while proc_state(sentinel.pid) != "Z" and time.monotonic() < until:
    time.sleep(0.005)
sentinel_entry = {
    "role": "sentinel",
    "pid": sentinel.pid,
    "start_ticks": int(
        pathlib.Path(f"/proc/{sentinel.pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    ),
}
pathlib.Path(workdir, "registered-child.json").write_text(
    json.dumps({"entries": [sentinel_entry]})
)
child = subprocess.Popen(
    [sys.executable, "-B", "-c", "import time; time.sleep(300)"],
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True,
)
child_entry = {
    "role": "product",
    "pid": child.pid,
    "start_ticks": int(
        pathlib.Path(f"/proc/{child.pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    ),
    "pgid": os.getpgid(child.pid),
    "argv": list(child.args),
}
registry = json.loads(
    pathlib.Path(workdir, "registered-child.json").read_text()
)
registry["entries"].append(child_entry)
pathlib.Path(workdir, "registered-child.json").write_text(json.dumps(registry))
os.kill(child.pid, signal.SIGSTOP)
time.sleep(300)
'''

    def _write_hold_script(self, temp: str) -> Path:
        script = Path(temp) / "holding_fixture.py"
        script.write_text(self._HOLD_SCRIPT)
        script.chmod(0o700)
        return script

    def _wait_for_registration(
        self, workdir: Path, bound: float = 10.0
    ) -> None:
        # Wait for the COMPLETE registered owned set (sentinel plus
        # product child) before the controlled parent-side fault
        # fires, so the fixture itself has no registration/cleanup
        # race: the cleanup path always observes the full registry.
        until = time.monotonic() + bound
        while True:
            path = workdir / "registered-child.json"
            roles: set[str] = set()
            if path.exists():
                with contextlib.suppress(ValueError):
                    entries = json.loads(path.read_text()).get(
                        "entries", []
                    )
                    roles = {
                        str(entry.get("role"))
                        for entry in entries
                        if isinstance(entry, dict)
                    }
            if "sentinel" in roles and "product" in roles:
                return
            if time.monotonic() >= until:
                raise AssertionError(
                    "holding fixture did not register the complete "
                    "owned set in bound"
                )
            time.sleep(0.01)

    def _assert_supervisor_reaped(self, observed: dict[str, object]) -> None:
        # The supervisor actually wait/reaped the exact registered
        # child (SIGKILL exit status observed), the script was
        # actually waited, and the exact identity is now gone.
        self.assertIsNotNone(observed.get("script_exit"))
        child = observed.get("child")
        self.assertIsInstance(child, dict)
        assert isinstance(child, dict)
        self.assertIs(child.get("reaped_by_supervisor"), True)
        self.assertEqual(child.get("waited_pid"), child.get("pid"))
        status = child.get("wait_status")
        self.assertIsInstance(status, int)
        assert isinstance(status, int)
        self.assertTrue(os.WIFSIGNALED(status))
        self.assertEqual(os.WTERMSIG(status), signal.SIGKILL)
        pid = child.get("pid")
        self.assertIsInstance(pid, int)
        assert isinstance(pid, int)
        self.assertIsNone(_proc_start_ticks(pid))
        # The complete owned set includes the script's own
        # sentinel: after the forced escape the script's finally
        # cannot run, so the supervisor itself must have actually
        # wait/reaped the exact registered sentinel with its own
        # clean exit status, exact identity gone.
        sentinel = observed.get("sentinel")
        self.assertIsInstance(sentinel, dict)
        assert isinstance(sentinel, dict)
        self.assertIs(sentinel.get("reaped_by_supervisor"), True)
        self.assertEqual(
            sentinel.get("waited_pid"), sentinel.get("pid")
        )
        sstatus = sentinel.get("wait_status")
        self.assertIsInstance(sstatus, int)
        assert isinstance(sstatus, int)
        self.assertTrue(os.WIFEXITED(sstatus))
        self.assertEqual(os.WEXITSTATUS(sstatus), 0)
        spid = sentinel.get("pid")
        self.assertIsInstance(spid, int)
        assert isinstance(spid, int)
        self.assertIsNone(_proc_start_ticks(spid))

    def _assert_registry_identities_gone(
        self, workdir: Path
    ) -> None:
        # Metadata-independent cleanup check: read the actual
        # two-child registry and verify that BOTH registered exact
        # identities (sentinel + product child) are gone or
        # identity-recycled BEFORE test cleanup - no live or zombie
        # child with a registered identity may remain, regardless of
        # whether observation metadata was passed.
        path = workdir / "registered-child.json"
        self.assertTrue(path.exists())
        known = json.loads(path.read_text())
        entries = known["entries"]
        self.assertEqual(
            sorted(entry["role"] for entry in entries),
            ["product", "sentinel"],
        )
        for entry in entries:
            ticks = _proc_start_ticks(int(entry["pid"]))
            self.assertTrue(
                ticks is None or ticks != int(entry["start_ticks"]),
                f"registered {entry['role']} child identity "
                "still present",
            )

    def test_pandoc_held_child_under_finite_supervised_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp)
            workdir.chmod(0o700)
            script = write_held_child_script(temp)
            observed: dict[str, object] = {}
            rc, out, err = run_supervised_tree(
                script, "pandoc", 0, workdir, observed=observed
            )
            check_held_child_result(self, rc, out, err, observed)

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
                script = write_held_child_script(temp)
                observed: dict[str, object] = {}
                rc, out, err = run_supervised_tree(
                    script,
                    "review",
                    server.server_address[1],
                    workdir,
                    observed=observed,
                )
                check_held_child_result(self, rc, out, err, observed)
        finally:
            if server is not None:
                server.shutdown()
                server.server_close()
            if thread is not None:
                thread.join(5)
                self.assertFalse(thread.is_alive())

    def test_supervisor_natural_no_child_path(self) -> None:
        # Natural healthy no-child path: the script exits in bound
        # and registers nothing; the supervisor returns the exact
        # exit status with nothing to reap.
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp)
            workdir.chmod(0o700)
            script = Path(temp) / "no_child.py"
            script.write_text("import sys\nsys.exit(0)\n")
            script.chmod(0o700)
            observed: dict[str, object] = {}
            rc, _out, _err = run_supervised_tree(
                script, "none", 0, workdir, observed=observed
            )
            self.assertEqual(rc, 0)
            self.assertEqual(observed.get("child"), {"registered": False})
            self.assertIsNone(observed.get("sentinel"))
            self.assertEqual(observed.get("script_exit"), 0)

    def test_supervisor_timeout_reaps_exact_registered_child(self) -> None:
        # Supervisor SELF-proof of the timeout cleanup path: the hang
        # is a declared fixture fault (the holding script never
        # returns), so this proves the bounded forced escape and the
        # exact-identity actual reap, NOT product behavior.  Both
        # observation modes: with metadata (attribution asserted via
        # the reported records) and with the default observed=None
        # (cleanup must not depend on metadata; the assertion reads
        # the actual two-child registry instead).
        for mode in ("metadata", "default-none"):
            with self.subTest(observed=mode), tempfile.TemporaryDirectory() as temp:
                workdir = Path(temp)
                workdir.chmod(0o700)
                script = self._write_hold_script(temp)
                observed: dict[str, object] | None = (
                    {} if mode == "metadata" else None
                )
                with self.assertRaises(AssertionError) as ctx:
                    run_supervised_tree(
                        script,
                        "hold",
                        0,
                        workdir,
                        bound=8.0,
                        observed=observed,
                    )
                self.assertIn("finite parent bound", str(ctx.exception))
                if observed is not None:
                    self._assert_supervisor_reaped(observed)
                self._assert_registry_identities_gone(workdir)

    def test_supervisor_timeout_held_script_reaps_complete_owned_set(
        self,
    ) -> None:
        # Supervisor SELF-proof on the ACTUAL held script: its
        # declared fixture fault (pandoc-stall: the seam holds the
        # real Pandoc child, then the script stalls instead of
        # interrupting) forces the bounded timeout.  The COMPLETE
        # registered owned set - the real Pandoc child and the
        # script's own unrelated sentinel - must be actually
        # wait/reaped with the exact statuses (SIGKILL for the
        # stopped product child; the sentinel's own clean exit) and
        # both exact identities gone.  Both observation modes:
        # metadata attribution and default observed=None with the
        # registry identity check.  Containment only: the stall is
        # a fixture stand-in, never product evidence.
        for mode in ("metadata", "default-none"):
            with self.subTest(observed=mode), tempfile.TemporaryDirectory() as temp:
                workdir = Path(temp)
                workdir.chmod(0o700)
                script = write_held_child_script(temp)
                observed: dict[str, object] | None = (
                    {} if mode == "metadata" else None
                )
                with self.assertRaises(AssertionError) as ctx:
                    run_supervised_tree(
                        script,
                        "pandoc-stall",
                        0,
                        workdir,
                        bound=8.0,
                        observed=observed,
                    )
                self.assertIn("finite parent bound", str(ctx.exception))
                if observed is not None:
                    self.assertEqual(observed.get("script_exit"), -9)
                    self._assert_supervisor_reaped(observed)
                self._assert_registry_identities_gone(workdir)

    def test_supervisor_unexpected_exception_reaps_exact_registered_child(
        self,
    ) -> None:
        # Supervisor SELF-proof of the unexpected-exception cleanup
        # path: a declared fixture fault makes the parent's own
        # communicate raise after the exact child is registered; the
        # supervisor must kill the group, wait the script, actually
        # reap the exact registered child and re-raise the original
        # exception.  Containment only, never product evidence.
        #  Both observation modes: metadata (attribution via the
        # reported records) and default observed=None (cleanup must
        # not depend on metadata; registry identity check instead).
        for mode in ("metadata", "default-none"):
            with self.subTest(observed=mode), tempfile.TemporaryDirectory() as temp:
                workdir = Path(temp)
                workdir.chmod(0o700)
                script = self._write_hold_script(temp)
                instance = RuntimeError(
                    "controlled parent-side communicate fault"
                )
                observed: dict[str, object] | None = (
                    {} if mode == "metadata" else None
                )

                def faulted_communicate(
                    self_p: subprocess.Popen[bytes],
                    *args: object,
                    workdir: Path = workdir,
                    instance: RuntimeError = instance,
                    **kwargs: object,
                ) -> tuple[bytes, bytes]:
                    self._wait_for_registration(workdir)
                    raise instance

                with mock.patch.object(
                    subprocess.Popen, "communicate",
                    faulted_communicate,
                ), self.assertRaises(RuntimeError) as ctx:
                    run_supervised_tree(
                        script, "hold", 0, workdir,
                        observed=observed,
                    )
                self.assertIs(ctx.exception, instance)
                if observed is not None:
                    self._assert_supervisor_reaped(observed)
                self._assert_registry_identities_gone(workdir)


if __name__ == "__main__":
    unittest.main()
