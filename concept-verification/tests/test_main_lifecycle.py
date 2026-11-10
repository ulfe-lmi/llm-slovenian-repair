"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Main lifecycle.

Order 031-b, requirement 5: bounded owned-child proofs of the ACTUAL
``proxy.main()`` entry point (order 031-b, requirements 2-4).

Scenarios:
- normal serve completion, failed serve, a primary nonordinary control
  followed by a cleanup control, and cleanup failure with an absent or
  ordinary primary (the control-selection rule of order 031-b,
  requirement 3);
- first-nonordinary identity over LATER nonordinary cleanup:
  MemoryError and SystemExit primaries keep their EXACT object
  identity when the cleanup itself raises a nonordinary control
  (order 031-b, requirement 3: "including MemoryError");
- native SIGINT driving the actual ``main()``, constructor, admission
  and qualified Pandoc, proving natural process exit within a finite
  bound and ACTUAL owned thread/listener cleanup - a raised exception
  alone is insufficient and a forced kill cannot establish PASS;
- the reviewer-only ``CONCEPT_REVIEWER_TIMEOUT`` operator setting:
  absent (default 15), explicitly 45, and invalid (nonnumeric, empty,
  nonpositive, NaN, infinity) rejected before listener creation, while
  the main intake/setup/header/body/delivery budgets retain their
  independent values (order 031-b, requirement 4).

The fixture changes ONLY the hardcoded bind address to OS-assigned
loopback port 0 and observes the real serve entry; it never replaces
the owning close, the admission lifecycle or the handler.  The fixture
class is installed as the entry point's ConceptProxy name before
``main()`` runs, so the real main() wiring (env settings, pandoc
gate, reviewer construction, budgets) is exactly what is exercised.
Every scenario runs with exact Popen ownership and actual reap, a
sanitized child environment, empty auth and no profile, bounded
startup, readiness, IO and cleanup on every path (both pipes drained
under the bound; the child is guaranteed killed and reaped on any
failure path).  No HTTP or model requests are sent and no fixed port
is touched (the fixed 18024 is never bound by these diagnostics).
Root's earlier failure evidence and its counterfactual wrapper are
preserved as historical evidence only: this module exercises the
implemented product bytes.

Observed qualified-Python exit semantics (asserted, not assumed):
an unhandled KeyboardInterrupt exits by SIGINT (Popen returncode -2,
shell 128+2=130); an unhandled MemoryError exits 1; SystemExit(code)
exits with that code; ordinary unhandled exceptions exit 1; a normal
main() return exits 0.
"""

from __future__ import annotations

import contextlib
import os
import select
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Finite per-scenario bounds: a child that exceeds them is killed and
# the scenario FAILS (a forced kill cannot establish PASS).
CHILD_TOTAL_BUDGET_SECONDS = 30.0
STDERR_CAPTURE_CAP_BYTES = 1 << 20

#: Scenarios whose serve_forever completes normally through the
#: native-contract shutdown() from the fixture observer thread
#: (bounded real-accept proof before the shutdown).
NORMAL_SCENARIOS = frozenset(
    {
        "normal",
        "timeout_absent",
        "timeout_45",
        "no_primary_cleanup_fail",
    }
)

#: scenario -> (expected Popen returncode, expected raised type name or
#: None, expect SERVE_ENTRY, expect BOUND listener line, expect exact
#: first-pending identity proof line).
EXPECTATIONS: dict[str, tuple[int, str | None, bool, bool, bool]] = {
    "normal": (0, None, True, True, False),
    "serve_error": (1, "OSError", True, True, True),
    "control_cleanup": (-2, "KeyboardInterrupt", True, True, True),
    "memory_error_primary": (1, "MemoryError", True, True, True),
    "system_exit_primary": (3, "SystemExit", True, True, True),
    "no_primary_cleanup_fail": (1, "ValueError", True, True, False),
    "ordinary_primary_cleanup_nonordinary": (
        -2,
        "KeyboardInterrupt",
        True,
        True,
        False,
    ),
    "ordinary_primary_cleanup_ordinary": (1, "ValueError", True, True, False),
    "sigint": (-2, "KeyboardInterrupt", True, True, False),
    "timeout_absent": (0, None, True, True, False),
    "timeout_45": (0, None, True, True, False),
    "timeout_nonnumeric": (1, "ValueError", False, False, False),
    "timeout_empty": (1, "ValueError", False, False, False),
    "timeout_zero": (1, "ValueError", False, False, False),
    "timeout_negative": (1, "ValueError", False, False, False),
    "timeout_nan": (1, "ValueError", False, False, False),
    "timeout_infinite": (1, "ValueError", False, False, False),
}

INVALID_TIMEOUT_VALUES = {
    "timeout_nonnumeric": "abc",
    "timeout_empty": "",
    "timeout_zero": "0",
    "timeout_negative": "-5",
    "timeout_nan": "nan",
    "timeout_infinite": "inf",
}

CHILD_SCRIPT = r'''
import os
import signal
import socket
import sys
import threading
import time

SCENARIO = os.environ["OAP_031B_SCENARIO"]
sys.path.insert(0, sys.argv[1])
import proxy  # noqa: E402

INSTANCES = []
PENDING_OBJECT = None
CLEANUP_CONTROLS = {
    "control_cleanup": ValueError("synthetic cleanup failure"),
    "memory_error_primary": SystemExit(3),
    "system_exit_primary": KeyboardInterrupt("synthetic cleanup control"),
    "no_primary_cleanup_fail": ValueError("synthetic cleanup failure"),
    "ordinary_primary_cleanup_nonordinary":
        KeyboardInterrupt("synthetic cleanup control"),
    "ordinary_primary_cleanup_ordinary":
        RuntimeError("synthetic ordinary cleanup failure"),
}


def _say(line):
    print(line, flush=True)


class FixtureProxy(proxy.ConceptProxy):
    def __init__(self, address, *args, **kwargs):
        engine = args[1] if len(args) > 1 else kwargs.get("engine")
        reviewer = getattr(engine, "reviewer", None)
        if reviewer is not None:
            # Before any bind allocation: the exact reviewer budget
            # the real main() selected.
            _say("REVIEWER_TIMEOUT %s" % (reviewer.timeout,))
        INSTANCES.append(self)
        # The only fixture address change: the hardcoded bind address
        # becomes OS-assigned loopback port 0.
        super().__init__(("127.0.0.1", 0), *args, **kwargs)
        _say(
            "BUDGETS header=%s client=%s delivery=%s setup=%s capture=%s"
            % (
                self.header_timeout,
                self.client_timeout,
                self.delivery_timeout,
                self.setup_timeout,
                self.capture_timeout,
            )
        )
        _say("BOUND %s" % (self.server_address[1],))

    def serve_forever(self, poll_interval=0.5):
        global PENDING_OBJECT
        _say("SERVE_ENTRY")
        if SCENARIO in ("normal", "timeout_absent", "timeout_45",
                        "no_primary_cleanup_fail"):
            observer = threading.Thread(
                target=self._observe_and_stop, daemon=True
            )
            observer.start()
            super().serve_forever(poll_interval)
            return
        if SCENARIO == "sigint":
            def _signal_self():
                # Let the real accept loop reach its select wait, then
                # send the native SIGINT to this exact process.
                time.sleep(0.5)
                _say("SIGINT_SENT")
                os.kill(os.getpid(), signal.SIGINT)

            signaller = threading.Thread(target=_signal_self, daemon=True)
            signaller.start()
            super().serve_forever(poll_interval)
            return
        if SCENARIO == "control_cleanup":
            PENDING_OBJECT = KeyboardInterrupt("synthetic primary control")
        elif SCENARIO == "memory_error_primary":
            PENDING_OBJECT = MemoryError("synthetic primary control")
        elif SCENARIO == "system_exit_primary":
            PENDING_OBJECT = SystemExit(3)
        elif SCENARIO == "serve_error":
            PENDING_OBJECT = OSError("synthetic serve failure")
        elif SCENARIO in (
            "ordinary_primary_cleanup_nonordinary",
            "ordinary_primary_cleanup_ordinary",
        ):
            PENDING_OBJECT = ValueError("synthetic ordinary primary")
        else:
            raise AssertionError("unknown scenario %r" % (SCENARIO,))
        raise PENDING_OBJECT

    def _observe_and_stop(self):
        # Bounded real-accept proof through the actual accepting loop
        # and admission path, then the native-contract shutdown() from
        # this different thread.
        probe = None
        try:
            probe = socket.create_connection(
                ("127.0.0.1", self.server_address[1]), timeout=2.0
            )
        except OSError:
            _say("ACCEPTED 0")
            return
        deadline = time.monotonic() + 5.0
        admitted = 0
        while time.monotonic() < deadline:
            admitted = self._admission.pending_count()
            if admitted >= 1:
                break
            time.sleep(0.01)
        _say("ACCEPTED %d" % (admitted,))
        probe.close()
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self._admission.pending_count() == 0:
                break
            time.sleep(0.01)
        _say("DRAINED %d" % (self._admission.pending_count(),))
        self.shutdown()

    def server_close(self):
        # The real owning close (admission stop + exact joins +
        # listener close) runs fully and independently; the fixture
        # may only report a scenario cleanup fault AFTER the actual
        # cleanup, simulating a cleanup failure for control selection.
        super().server_close()
        control = CLEANUP_CONTROLS.get(SCENARIO)
        if control is not None:
            raise control


# Install the fixture as the entry point's ConceptProxy name BEFORE
# main() runs: main() resolves that module global at call time, so the
# real main() wiring (env, pandoc gate, reviewer, budgets, close) is
# unchanged and only the bind address becomes OS-assigned.
proxy.ConceptProxy = FixtureProxy

MAIN_EXC = None
try:
    rc = proxy.main()
except BaseException as exc:
    MAIN_EXC = exc
    _say("MAIN_RAISED %s" % (type(exc).__name__,))
    raise
else:
    _say("MAIN_RETURN %s" % (rc,))
finally:
    if INSTANCES:
        fixture = INSTANCES[0]
        nondaemon = [t for t in threading.enumerate() if not t.daemon]
        try:
            listener_closed = fixture.socket.fileno() == -1
        except Exception:
            listener_closed = False
        _say(
            "CLEANUP nondaemon=%d listener_closed=%d"
            % (len(nondaemon), 1 if listener_closed else 0)
        )
    if MAIN_EXC is not None and PENDING_OBJECT is not None:
        _say("IDENTITY %d" % (1 if MAIN_EXC is PENDING_OBJECT else 0))
'''


class MainLifecycleTests(unittest.TestCase):
    """Bounded owned-child runs of the actual main() entry point."""

    def setUp(self) -> None:
        pandoc = os.environ.get("CONCEPT_PANDOC", "").strip()
        self.assertTrue(
            pandoc,
            "CONCEPT_PANDOC must name the qualified installed Pandoc "
            "3.7.0.2 binary (bounded setup requirement, no PATH "
            "discovery)",
        )
        self.pandoc = pandoc
        self.scratch = tempfile.TemporaryDirectory(
            prefix="oap-main-lifecycle-"
        )
        self.base = Path(self.scratch.name)
        (self.base / "home").mkdir(mode=0o700)
        (self.base / "pycache").mkdir(mode=0o700)
        self.script = self.base / "child_main_lifecycle.py"
        self.script.write_text(CHILD_SCRIPT)
        self.script.chmod(0o600)

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def _child_env(self, scenario: str) -> dict[str, str]:
        env = {
            "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
            "HOME": str(self.base / "home"),
            "TMPDIR": str(self.base),
            "PYTHONPYCACHEPREFIX": str(self.base / "pycache"),
            # Nonempty as required by main(); these scenarios never
            # open the index (no request traffic by design).
            "CONCEPT_INDEX": os.environ.get(
                "CONCEPT_INDEX", str(self.base / "index.sqlite")
            ),
            "CONCEPT_PANDOC": self.pandoc,
            # Discard port; no connection is ever made to it.
            "CONCEPT_UPSTREAM_URL": "http://127.0.0.1:9",
            # Empty auth and no profile in the diagnostic child.
            "QWEN_API_KEY": "",
            "OAP_031B_SCENARIO": scenario,
        }
        if scenario == "timeout_45":
            env["CONCEPT_REVIEWER_TIMEOUT"] = "45"
        elif scenario in INVALID_TIMEOUT_VALUES:
            env["CONCEPT_REVIEWER_TIMEOUT"] = INVALID_TIMEOUT_VALUES[scenario]
        return env

    def _run_child(self, scenario: str) -> tuple[list[str], int, bytes]:
        """Run one bounded owned child; both pipes drained with
        deadline-bounded ``os.read`` on the raw ready file
        descriptors (select-ready never triggers a buffered read,
        which could block past the bound on an incomplete record);
        the child is guaranteed killed and reaped on every failure
        path (a forced kill cannot establish PASS)."""
        total_deadline = time.monotonic() + CHILD_TOTAL_BUDGET_SECONDS
        process: subprocess.Popen[bytes] | None = None
        try:
            process = subprocess.Popen(
                [sys.executable, "-B", str(self.script), str(ROOT)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self._child_env(scenario),
                cwd=str(ROOT),
            )
            assert process.stdout is not None
            assert process.stderr is not None
            stdout_fd = process.stdout.fileno()
            stderr_fd = process.stderr.fileno()
            stdout_buf = bytearray()
            stderr_bytes = bytearray()
            lines: list[str] = []
            stdout_open = True
            stderr_open = True

            def drain_line_buffer() -> None:
                while True:
                    idx = stdout_buf.find(b"\n")
                    if idx < 0:
                        return
                    line = (
                        bytes(stdout_buf[:idx]).decode("utf-8", "replace")
                    )
                    del stdout_buf[: idx + 1]
                    if line:
                        lines.append(line)

            while stdout_open or stderr_open:
                remaining = total_deadline - time.monotonic()
                if remaining <= 0:
                    self.fail(
                        f"child for scenario {scenario} exceeded the "
                        "finite bound before both pipes drained (the "
                        "child is killed; a forced kill cannot "
                        "establish PASS)"
                    )
                fds: list[int] = []
                if stdout_open:
                    fds.append(stdout_fd)
                if stderr_open:
                    fds.append(stderr_fd)
                ready, _, _ = select.select(fds, [], [], remaining)
                for fd in ready:
                    if fd == stdout_fd:
                        chunk = os.read(stdout_fd, 65536)
                        if not chunk:
                            stdout_open = False
                        else:
                            stdout_buf.extend(chunk)
                            drain_line_buffer()
                    elif fd == stderr_fd:
                        chunk = os.read(stderr_fd, 65536)
                        if not chunk:
                            stderr_open = False
                        else:
                            room = STDERR_CAPTURE_CAP_BYTES - len(
                                stderr_bytes
                            )
                            if room > 0:
                                stderr_bytes.extend(chunk[:room])
            try:
                returncode = process.wait(
                    timeout=max(0.0, total_deadline - time.monotonic())
                )
            except subprocess.TimeoutExpired:
                self.fail(
                    f"child for scenario {scenario} exceeded the "
                    "finite bound before reaping (the child is "
                    "killed; a forced kill cannot establish PASS)"
                )
            return lines, returncode, bytes(stderr_bytes)
        finally:
            if process is not None:
                if process.poll() is None:
                    process.kill()
                    with contextlib.suppress(
                        subprocess.TimeoutExpired, OSError
                    ):
                        process.wait(timeout=5.0)
                if process.stdout is not None:
                    with contextlib.suppress(OSError):
                        process.stdout.close()
                if process.stderr is not None:
                    with contextlib.suppress(OSError):
                        process.stderr.close()

    def _lines_by_prefix(self, lines: list[str], prefix: str) -> list[str]:
        return [line for line in lines if line.startswith(prefix)]

    def _assert_cleanup_report(self, lines: list[str]) -> None:
        cleanup = self._lines_by_prefix(lines, "CLEANUP")
        self.assertEqual(len(cleanup), 1, "\n".join(lines))
        self.assertIn("nondaemon=1", cleanup[0])
        self.assertIn("listener_closed=1", cleanup[0])

    def _assert_scenario(
        self,
        scenario: str,
        expect_reviewer_timeout: str | None = None,
    ) -> list[str]:
        lines, returncode, _ = self._run_child(scenario)
        expected = EXPECTATIONS[scenario]
        self.assertEqual(returncode, expected[0], "\n".join(lines))
        raised = self._lines_by_prefix(lines, "MAIN_RAISED")
        returned = self._lines_by_prefix(lines, "MAIN_RETURN")
        if expected[1] is None:
            self.assertEqual(len(returned), 1, "\n".join(lines))
            self.assertEqual(len(raised), 0, "\n".join(lines))
        else:
            self.assertEqual(
                raised, [f"MAIN_RAISED {expected[1]}"], "\n".join(lines)
            )
            self.assertEqual(len(returned), 0, "\n".join(lines))
        entries = self._lines_by_prefix(lines, "SERVE_ENTRY")
        bounds = self._lines_by_prefix(lines, "BOUND")
        self.assertEqual(
            len(entries), 1 if expected[2] else 0, "\n".join(lines)
        )
        self.assertEqual(
            len(bounds), 1 if expected[3] else 0, "\n".join(lines)
        )
        if expected[3]:
            port = int(bounds[0].split()[1])
            self.assertTrue(0 < port < 65536)
        if scenario in NORMAL_SCENARIOS:
            accepted = self._lines_by_prefix(lines, "ACCEPTED")
            drained = self._lines_by_prefix(lines, "DRAINED")
            self.assertEqual(accepted, ["ACCEPTED 1"], "\n".join(lines))
            self.assertEqual(drained, ["DRAINED 0"], "\n".join(lines))
        if expect_reviewer_timeout is not None:
            timeouts = self._lines_by_prefix(lines, "REVIEWER_TIMEOUT")
            self.assertEqual(
                timeouts, [f"REVIEWER_TIMEOUT {expect_reviewer_timeout}"]
            )
            # Fixed before listener creation.
            self.assertLess(
                lines.index(
                    next(
                        entry
                        for entry in lines
                        if entry.startswith("REVIEWER_TIMEOUT")
                    )
                ),
                lines.index(
                    next(entry for entry in lines if entry.startswith("BOUND"))
                ),
                "the reviewer setting must be fixed before listener "
                "creation",
            )
        if expected[4]:
            self.assertEqual(
                self._lines_by_prefix(lines, "IDENTITY"), ["IDENTITY 1"]
            )
        if expected[2]:
            self._assert_cleanup_report(lines)
        self.assertNotIn("AssertionError", "\n".join(raised))
        return lines

    def test_normal_serve_completion(self) -> None:
        self._assert_scenario("normal")

    def test_failed_serve_propagates_ordinary_error(self) -> None:
        self._assert_scenario("serve_error")

    def test_nonordinary_primary_keeps_identity_over_cleanup_failure(
        self,
    ) -> None:
        # Keyboard-interrupt primary + ordinary cleanup failure: the
        # EXACT first pending control object propagates (identity,
        # not merely type).
        self._assert_scenario("control_cleanup")

    def test_memory_error_primary_keeps_identity_over_nonordinary_cleanup(
        self,
    ) -> None:
        # MemoryError primary (explicitly nonordinary per R3) with a
        # LATER nonordinary cleanup control (SystemExit): the first
        # pending nonordinary object still wins with exact identity.
        self._assert_scenario("memory_error_primary")

    def test_system_exit_primary_keeps_identity_over_nonordinary_cleanup(
        self,
    ) -> None:
        # SystemExit(3) primary with a LATER nonordinary cleanup
        # control (KeyboardInterrupt): the first pending nonordinary
        # object wins with exact identity and its exit code.
        self._assert_scenario("system_exit_primary")

    def test_cleanup_failure_without_primary_propagates(self) -> None:
        self._assert_scenario("no_primary_cleanup_fail")

    def test_ordinary_primary_does_not_suppress_nonordinary_cleanup(
        self,
    ) -> None:
        self._assert_scenario("ordinary_primary_cleanup_nonordinary")

    def test_ordinary_primary_precedes_ordinary_cleanup(self) -> None:
        self._assert_scenario("ordinary_primary_cleanup_ordinary")

    def test_native_sigint_exits_naturally_with_owned_cleanup(self) -> None:
        lines, returncode, _ = self._run_child("sigint")
        expected = EXPECTATIONS["sigint"]
        # Natural process exit BY the unhandled control (SIGINT,
        # Popen returncode -2 / shell 128+2=130), within the finite
        # bound, without a force-kill.
        self.assertEqual(returncode, expected[0], "\n".join(lines))
        self.assertEqual(
            self._lines_by_prefix(lines, "MAIN_RAISED"),
            ["MAIN_RAISED KeyboardInterrupt"],
            "\n".join(lines),
        )
        self.assertEqual(
            self._lines_by_prefix(lines, "SIGINT_SENT"), ["SIGINT_SENT"]
        )
        self.assertLess(
            lines.index("SIGINT_SENT"),
            lines.index(
                next(entry for entry in lines if entry.startswith("MAIN_RAISED"))
            ),
        )
        self._assert_cleanup_report(lines)

    def test_reviewer_timeout_absent_keeps_default_15(self) -> None:
        lines = self._assert_scenario(
            "timeout_absent", expect_reviewer_timeout="15.0"
        )
        self.assertEqual(
            self._lines_by_prefix(lines, "BUDGETS"),
            [
                "BUDGETS header=30.0 client=30.0 delivery=30.0 "
                "setup=30.0 capture=30.0"
            ],
        )

    def test_reviewer_timeout_explicit_45_only_changes_reviewer(self) -> None:
        lines = self._assert_scenario(
            "timeout_45", expect_reviewer_timeout="45.0"
        )
        self.assertEqual(
            self._lines_by_prefix(lines, "BUDGETS"),
            [
                "BUDGETS header=30.0 client=30.0 delivery=30.0 "
                "setup=30.0 capture=30.0"
            ],
            "only the reviewer budget may change; the independent "
            "intake/setup/header/body/delivery budgets retain their "
            "own values",
        )

    def test_invalid_reviewer_timeout_rejected_before_listener(self) -> None:
        for scenario in (
            "timeout_nonnumeric",
            "timeout_empty",
            "timeout_zero",
            "timeout_negative",
            "timeout_nan",
            "timeout_infinite",
        ):
            with self.subTest(scenario=scenario):
                self._assert_scenario(scenario)


if __name__ == "__main__":
    unittest.main()
