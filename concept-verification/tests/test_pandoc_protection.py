"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Pandoc protection.

Order 013-a acceptance coverage: qualified Pandoc startup and bounded
failure reasons, exact original-span mapping on the actual pinned binary,
fail-closed protected regions, bounded subprocess capture (flood,
early exit, timeout, write-before-read; no FD or process leaks), the
RepairEngine fail-closed boundary (no corpus, no reviewer),
acceptance/patch bounds and grapheme splits, an ephemeral HTTP round trip
through the real proxy with the real Pandoc, and proof that the historical
pulldown helper is never invoked on the proxy path.

Mapping positives and negatives are asserted against the pinned
commonmark_x+sourcepos-smart profile on the selected binary; a missing
dependency fails these tests (never skips).
"""

from __future__ import annotations

import hashlib
import http.client
import json
import os
import selectors as sel
import shutil
import sqlite3
import subprocess as sp
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import pandoc_protection  # noqa: E402
from batch_review import BatchProposal, BatchResult, BatchTarget  # noqa: E402
from detector import Candidate  # noqa: E402
from pandoc_protection import (  # noqa: E402
    PandocSpec,
    PandocStartupError,
    check_pandoc,
    compose_protection,
    parse_document,
    protect_with_pandoc,
    resolve_pandoc_spec,
)
from protected import Interval, protected_intervals  # noqa: E402
from qwen_client import Proposal  # noqa: E402
from repair import accept, apply_edits  # noqa: E402

from corpus import Corpus  # noqa: E402

# Order 033-a, R9/A1: the exact preserved old-baseline repro vectors
# (14 red + 4 controls), extracted as pure owned synthetic data from the
# preserved probe; every input SHA-256 equals the immutable old-byte
# baseline (no customer/evaluation data).  Each row carries independent
# original-source oracles: the required protected range must stay fully
# protected, every non-ordinary target occurrence must not be granted,
# and the ordinary (outside) occurrence must be granted (outside-only).
_OLD_BASELINE_VECTORS: tuple[dict[str, object], ...] = (
    {
        "case": 'R1-slovenian-low-high-double',
        "kind": 'red',
        "input": '„Danes je leppo vreme.“',
        "input_sha256": '2024781effa396266786cc9c05d0e85d880eea3b6ae4d9eac31d4c222a67e2e1',
        "required_protected_range": (1, 22),
        "target_original_ranges": ((10, 15),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R2-slovenian-guillemets',
        "kind": 'red',
        "input": '»Danes je leppo vreme.«',
        "input_sha256": '89eb01b07cef7091dcbda82d3a732b55967d7c2486eeea19bfad38c2110d05b0',
        "required_protected_range": (1, 22),
        "target_original_ranges": ((10, 15),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R3-inward-guillemets',
        "kind": 'red',
        "input": '«Danes je leppo vreme.»',
        "input_sha256": '6afaa2624bd2734e560581cfe09c6f2b2a0bcd7d67fe2dcf72f4599f2140bf90',
        "required_protected_range": (1, 22),
        "target_original_ranges": ((10, 15),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R4-nested-straight-quote',
        "kind": 'red',
        "input": '"Predgovor \'leppo vreme.\' konec."',
        "input_sha256": 'd6ce6e0a9ca1b3ec9ab2050d70af4ed4efe0862d019b459f368dfc755989d708',
        "required_protected_range": (11, 24),
        "target_original_ranges": ((12, 17),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R5-quote-continuing-next-block',
        "kind": 'red',
        "input": '“Prvi odstavek.\n\nDanes je leppo vreme.”',
        "input_sha256": '62924c33adba9b099fbbd30f0fa8da2d7fc3bbd4a6c6af4a9ef5aff093ec0a9e',
        "required_protected_range": (1, 38),
        "target_original_ranges": ((26, 31),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R6-lazy-blockquote-continuation',
        "kind": 'red',
        "input": '> Prvi stavek.\nDanes je leppo vreme.',
        "input_sha256": 'ab78bd9bd8251c968cbafe20eb1bc8a36031bd4e150cc2589a1aa216cd7cdbdf',
        "required_protected_range": (0, 36),
        "target_original_ranges": ((24, 29),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R7-mismatched-html-close',
        "kind": 'red',
        "input": 'Besedilo <b> </i> Danes je leppo vreme.',
        "input_sha256": '4e6e786b14652d5689170461e1f684c586d0d68ba24b92930b7d91ff152a68a6',
        "required_protected_range": (9, 39),
        "target_original_ranges": ((27, 32),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R8-mismatched-then-eventual-close',
        "kind": 'red',
        "input": 'Besedilo <b> </i> Danes je leppo vreme.</b>',
        "input_sha256": 'a1faaceed6f1c03a408156d481c219e62704ec8af917fe4c47d6f5d78de84ce0',
        "required_protected_range": (9, 43),
        "target_original_ranges": ((27, 32),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R9-tag-in-nested-emphasis',
        "kind": 'red',
        "input": 'Besedilo **<b>predgovor** Danes je leppo vreme.',
        "input_sha256": '512cc7c508bba52d9c169c6ce4a339fc390c70dcea9ee126529a3e73c6ae0ceb',
        "required_protected_range": (11, 47),
        "target_original_ranges": ((35, 40),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R10-unclosed-tag-next-block',
        "kind": 'red',
        "input": 'Besedilo <b>predgovor\n\nDanes je leppo vreme.',
        "input_sha256": 'fc1482474428d7349c40110e9aaad12bc874ef67c57a1d303236929c06909e20',
        "required_protected_range": (9, 44),
        "target_original_ranges": ((32, 37),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R11-escaped-in-curly-quote',
        "kind": 'red',
        "input": '“Uvod \\"To je presenetliv zapisano.\\" konec.”',
        "input_sha256": '05a33285600a4dbe817a2b56503ea5ad44ac03edcb968e36b06bf4d961e7a330',
        "required_protected_range": (1, 44),
        "target_original_ranges": ((14, 25),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R12-escaped-in-straight-quote',
        "kind": 'red',
        "input": '"Uvod \\"To je presenetliv zapisano.\\" konec."',
        "input_sha256": 'b1438f06cf7a17ac9710011b0dfe1799ab23d6795cba576c853f55bd232c12b1',
        "required_protected_range": (1, 43),
        "target_original_ranges": ((14, 25),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R13-entity-in-straight-quote',
        "kind": 'red',
        "input": '"Uvod &quot;To je presenetliv zapisano.&quot; konec."',
        "input_sha256": 'ba4999b4e42fe491264e076cf2a2b99d6ffd8cc5184715a9ac1a24066135c91f',
        "required_protected_range": (1, 51),
        "target_original_ranges": ((18, 29),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'R14-duplicate-inside-and-outside',
        "kind": 'red',
        "input": '»Danes je leppo vreme.«\n\nDanes je leppo danes.',
        "input_sha256": 'acd06388966b41ff0ee7682ceee54c471cd17771bae39e2387dc4f5a3f5301a9',
        "required_protected_range": (1, 21),
        "target_original_ranges": ((10, 15), (34, 39),),
        "ordinary_target_occurrence_indices": (1,),
    },
    {
        "case": 'K1-unquoted-reachable',
        "kind": 'reachable',
        "input": 'To je leppo zapisano.',
        "input_sha256": '35c7351158cc7474c0114a4e01b8db88354383ec942907c039cabdf65c8d56bb',
        "required_protected_range": None,
        "target_original_ranges": ((6, 11),),
        "ordinary_target_occurrence_indices": (0,),
    },
    {
        "case": 'K2-zero-call-control',
        "kind": 'zero',
        "input": 'To je lepo vreme.',
        "input_sha256": '28c7d7fa8f8c0fa5394a6be9064594eb08d34dd3556de3770640433092876126',
        "required_protected_range": None,
        "target_original_ranges": (),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'K3-ascii-double-quote-control',
        "kind": 'protected',
        "input": '"To je leppo zapisano."',
        "input_sha256": '366e368e8a4f6836ff385e1b6a05dc660d8f46eb06e5f4f9436dacf39baf81bc',
        "required_protected_range": None,
        "target_original_ranges": ((7, 12),),
        "ordinary_target_occurrence_indices": (),
    },
    {
        "case": 'K4-entity-quote-control',
        "kind": 'protected',
        "input": '&quot;To je presenetliv zapisano.&quot;',
        "input_sha256": 'a3b6857542ca87c93c45a2eee3a0f45c8e8d8890459920e78dba93b1921abde3',
        "required_protected_range": None,
        "target_original_ranges": ((12, 23),),
        "ordinary_target_occurrence_indices": (),
    },
)



def _real_spec() -> PandocSpec:
    configured = os.environ.get("CONCEPT_PANDOC", "").strip()
    binary = configured or shutil.which("pandoc") or "/usr/bin/pandoc"
    return PandocSpec(binary=binary)


def _write_fake(root: Path, name: str, body: str, mode: int = 0o700) -> Path:
    path = root / name
    path.write_text(body, encoding="utf-8")
    path.chmod(mode)
    return path


def _fd_count() -> int:
    return len(os.listdir("/proc/self/fd"))


FAKE_VERSION_BAD = "#!/bin/sh\necho 'pandoc 3.8.0'\n"
FAKE_BAD_EXIT = "#!/bin/sh\nexit 3\n"
FAKE_MALFORMED = (
    "#!/bin/sh\n"
    "if [ \"$1\" = --version ]; then echo 'pandoc 3.7.0.2'; "
    "else printf '%s' 'not json'; fi\n"
)
FAKE_CAPABILITY_BAD = (
    "#!/bin/sh\n"
    "if [ \"$1\" = --version ]; then echo 'pandoc 3.7.0.2'; "
    "else printf '%s' '{\"blocks\":[]}'; fi\n"
)
FAKE_SLEEPER = "#!/bin/sh\nsleep 30\n"


class PandocStartupTests(unittest.TestCase):
    """Qualified startup contract and bounded failure reasons."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_real_binary_is_qualified(self) -> None:
        spec = _real_spec()
        self.assertTrue(
            os.path.isfile(spec.binary), "qualified Pandoc binary is missing"
        )
        check_pandoc(spec)

    def test_resolve_uses_env_var(self) -> None:
        target = self.root / "pandoc-env"
        _write_fake(self.root, "pandoc-env", FAKE_BAD_EXIT)
        with mock.patch.dict(os.environ, {"CONCEPT_PANDOC": str(target)}):
            self.assertEqual(resolve_pandoc_spec().binary, str(target))

    def test_resolve_missing_fails(self) -> None:
        env = {
            "CONCEPT_PANDOC": "",
            "PATH": str(self.root / "empty-path"),
        }
        with mock.patch.dict(os.environ, env, clear=True):
            env["HOME"] = str(self.root)
            with self.assertRaises(PandocStartupError) as ctx:
                resolve_pandoc_spec()
        self.assertEqual(ctx.exception.reason, "PANDOC_NOT_FOUND")

    def test_not_executable(self) -> None:
        target = _write_fake(self.root, "noexec", FAKE_VERSION_BAD, mode=0o600)
        with self.assertRaises(PandocStartupError) as ctx:
            check_pandoc(PandocSpec(binary=str(target)))
        self.assertEqual(ctx.exception.reason, "PANDOC_NOT_EXECUTABLE")

    def test_wrong_version(self) -> None:
        target = _write_fake(self.root, "badver", FAKE_VERSION_BAD)
        with self.assertRaises(PandocStartupError) as ctx:
            check_pandoc(PandocSpec(binary=str(target)))
        self.assertEqual(ctx.exception.reason, "PANDOC_WRONG_VERSION")

    def test_bad_exit(self) -> None:
        target = _write_fake(self.root, "badexit", FAKE_BAD_EXIT)
        with self.assertRaises(PandocStartupError) as ctx:
            check_pandoc(PandocSpec(binary=str(target)))
        self.assertEqual(ctx.exception.reason, "PANDOC_BAD_EXIT")

    def test_malformed_output(self) -> None:
        target = _write_fake(self.root, "malformed", FAKE_MALFORMED)
        with self.assertRaises(PandocStartupError) as ctx:
            parse_document(PandocSpec(binary=str(target)), "Beseda\n")
        self.assertEqual(ctx.exception.reason, "PANDOC_MALFORMED_OUTPUT")

    def test_capability_failure(self) -> None:
        target = _write_fake(self.root, "nocap", FAKE_CAPABILITY_BAD)
        with self.assertRaises(PandocStartupError) as ctx:
            check_pandoc(PandocSpec(binary=str(target)))
        self.assertEqual(ctx.exception.reason, "PANDOC_CAPABILITY")

    def test_startup_timeout(self) -> None:
        target = _write_fake(self.root, "sleeper", FAKE_SLEEPER)
        with self.assertRaises(PandocStartupError) as ctx:
            check_pandoc(PandocSpec(binary=str(target), startup_timeout=1.0))
        self.assertEqual(ctx.exception.reason, "PANDOC_TIMEOUT")

    def test_input_too_large(self) -> None:
        spec = _real_spec()
        with mock.patch.object(pandoc_protection, "PANDOC_MAX_INPUT_BYTES", 10), \
                self.assertRaises(PandocStartupError) as ctx:
            parse_document(spec, "x" * 20)
        self.assertEqual(ctx.exception.reason, "PANDOC_INPUT_TOO_LARGE")

    def test_output_too_large_enforced_immediately(self) -> None:
        fake = self.root / "flood"
        fake.write_text(
            f"#!{sys.executable}\n"
            "import sys\n"
            "sys.stdout.buffer.write(b'x' * 4096)\n"
            "sys.stdout.buffer.flush()\n"
            "sys.exit(0)\n",
            encoding="utf-8",
        )
        fake.chmod(0o700)
        spec = PandocSpec(binary=str(fake))
        fds_before = _fd_count()
        started = time.monotonic()
        with mock.patch.object(pandoc_protection, "PANDOC_MAX_OUTPUT_BYTES", 1024), \
                self.assertRaises(PandocStartupError) as ctx:
            parse_document(spec, "Beseda\n")
        self.assertEqual(ctx.exception.reason, "PANDOC_OUTPUT_TOO_LARGE")
        self.assertLess(time.monotonic() - started, 10.0)
        time.sleep(0.05)
        self.assertEqual(_fd_count(), fds_before)


class BoundedCaptureTests(unittest.TestCase):
    """Bounded streaming capture: no deadlock, bounded cleanup, no leaks."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _spy_popen(self) -> tuple[object, Callable[..., object], dict[str, int]]:
        real_popen = sp.Popen
        captured: dict[str, int] = {}

        def spy(*args: Any, **kwargs: Any) -> object:
            process = real_popen(*args, **kwargs)
            captured["pid"] = process.pid
            return process

        return real_popen, spy, captured

    def test_write_before_read_child_no_deadlock(self) -> None:
        fake = self.root / "wbread"
        fake.write_text(
            f"#!{sys.executable}\n"
            "import sys\n"
            "sys.stdout.buffer.write(b'y' * 200000)\n"
            "sys.stdout.buffer.flush()\n"
            "sys.stdin.read()\n"
            "sys.stdout.buffer.write(b'end')\n"
            "sys.stdout.buffer.flush()\n"
            "sys.exit(0)\n",
            encoding="utf-8",
        )
        fake.chmod(0o700)
        spec = PandocSpec(binary=str(fake), timeout=20.0)
        with mock.patch.object(pandoc_protection, "PANDOC_MAX_OUTPUT_BYTES", 1_000_000):
            started = time.monotonic()
            returncode, stdout = pandoc_protection._run_bounded(
                spec, [str(fake), "-f", "x", "-t", "json"], b"w" * 50000
            )
        elapsed = time.monotonic() - started
        self.assertEqual(returncode, 0)
        self.assertEqual(len(stdout), 200003)
        self.assertTrue(stdout.endswith(b"end"))
        self.assertLess(elapsed, 15.0)

    def test_early_exit_child_no_deadlock(self) -> None:
        fake = self.root / "early"
        fake.write_text(
            f"#!{sys.executable}\nimport sys\nsys.exit(7)\n", encoding="utf-8"
        )
        fake.chmod(0o700)
        spec = PandocSpec(binary=str(fake), timeout=10.0)
        started = time.monotonic()
        returncode, stdout = pandoc_protection._run_bounded(
            spec, [str(fake), "-f", "x", "-t", "json"], b"z" * 50000
        )
        self.assertLess(time.monotonic() - started, 10.0)
        self.assertEqual(returncode, 7)
        self.assertEqual(stdout, b"")

    def test_timeout_kills_group_without_leaks(self) -> None:
        fake = self.root / "slow"
        fake.write_text(
            f"#!{sys.executable}\n"
            "import time\n"
            "time.sleep(30)\n",
            encoding="utf-8",
        )
        fake.chmod(0o700)
        spec = PandocSpec(binary=str(fake), timeout=0.5)
        real_popen, spy, captured = self._spy_popen()
        fds_before = _fd_count()
        with mock.patch.object(sp, "Popen", spy), \
                self.assertRaises(PandocStartupError) as ctx:
            pandoc_protection._run_bounded(
                spec, [str(fake), "-f", "x", "-t", "json"], b""
            )
        self.assertEqual(ctx.exception.reason, "PANDOC_TIMEOUT")
        time.sleep(0.1)
        import os as _os

        with self.assertRaises(ProcessLookupError):
            _os.kill(captured["pid"], 0)
        self.assertEqual(_fd_count(), fds_before)

    def test_flood_bounded_without_leaks(self) -> None:
        fake = self.root / "flood2"
        fake.write_text(
            f"#!{sys.executable}\n"
            "import sys\n"
            "sys.stdout.buffer.write(b'x' * 20000)\n"
            "sys.exit(0)\n",
            encoding="utf-8",
        )
        fake.chmod(0o700)
        spec = PandocSpec(binary=str(fake), timeout=10.0)
        real_popen, spy, captured = self._spy_popen()
        fds_before = _fd_count()
        with mock.patch.object(sp, "Popen", spy), \
                mock.patch.object(pandoc_protection, "PANDOC_MAX_OUTPUT_BYTES", 4096), \
                self.assertRaises(PandocStartupError) as ctx:
            pandoc_protection._run_bounded(
                spec, [str(fake), "-f", "x", "-t", "json"], b""
            )
        self.assertEqual(ctx.exception.reason, "PANDOC_OUTPUT_TOO_LARGE")
        time.sleep(0.1)
        import os as _os

        with self.assertRaises(ProcessLookupError):
            _os.kill(captured["pid"], 0)
        self.assertEqual(_fd_count(), fds_before)

    def test_selector_allocation_failure_cleans_child_and_fds(self) -> None:
        # A real child is launched, then selector allocation fails: the
        # owned child group must be signalled and all pipes closed, while
        # an unrelated sentinel process outside the owned group survives.
        import subprocess as sp

        fake = self.root / "allocfail"
        fake.write_text(
            f"#!{sys.executable}\n"
            "import time\n"
            "time.sleep(30)\n",
            encoding="utf-8",
        )
        fake.chmod(0o700)
        spec = PandocSpec(binary=str(fake), timeout=10.0)
        real_popen, spy, captured = self._spy_popen()
        fds_before = _fd_count()
        sentinel = sp.Popen(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            start_new_session=True,
        )
        try:
            time.sleep(0.2)  # sentinel up before the owned group is signalled
            with mock.patch.object(
                sp, "Popen", spy
            ), mock.patch.object(
                sel,
                "DefaultSelector",
                side_effect=OSError("injected allocation failure"),
            ), self.assertRaises(OSError):
                pandoc_protection._run_bounded(
                    spec, [str(fake), "-f", "x", "-t", "json"], b""
                )
            time.sleep(0.1)
            import os as _os

            with self.assertRaises(ProcessLookupError):
                _os.kill(captured["pid"], 0)
            self.assertIsNone(
                sentinel.poll(), "unrelated sentinel must survive"
            )
            self.assertEqual(_fd_count(), fds_before)
        finally:
            sentinel.kill()
            sentinel.wait(timeout=5)

    def test_timeout_kills_descendant_retaining_pipes(self) -> None:
        # The direct child exits immediately while a descendant retains a
        # pipe: the owned group signal must still reach the descendant,
        # even though the parent already exited (poll() is not None).
        import subprocess as sp

        marker = "orphan-descendant-marker-013a"
        fake = self.root / "orphan"
        fake.write_text(
            f"#!{sys.executable}\n"
            "import subprocess, sys, time\n"
            "subprocess.Popen([sys.executable, '-c',\n"
            f"    'import time; time.sleep(30)  # {marker}'])\n"
            "time.sleep(0.2)\n"
            "sys.exit(0)\n",
            encoding="utf-8",
        )
        fake.chmod(0o700)
        spec = PandocSpec(binary=str(fake), timeout=1.0)
        real_popen, spy, captured = self._spy_popen()
        fds_before = _fd_count()
        with mock.patch.object(
            sp, "Popen", spy
        ), self.assertRaises(PandocStartupError) as ctx:
            pandoc_protection._run_bounded(
                spec, [str(fake), "-f", "x", "-t", "json"], b""
            )
        self.assertEqual(ctx.exception.reason, "PANDOC_TIMEOUT")
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            probe = sp.run(["pgrep", "-f", marker], capture_output=True)
            if probe.returncode != 0:
                break
            time.sleep(0.05)
        self.assertNotEqual(
            probe.returncode, 0, "descendant must not survive group signal"
        )
        self.assertEqual(_fd_count(), fds_before)


class PandocMappingTests(unittest.TestCase):
    """Exact original-span mapping and fail-closed regions (real binary)."""

    spec: PandocSpec

    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = _real_spec()
        check_pandoc(cls.spec)  # missing dependency fails here, never skips

    def _protect(self, text: str) -> tuple[tuple[tuple[int, int], ...], list[Interval]]:
        outcome = protect_with_pandoc(self.spec, text)
        self.assertTrue(outcome.ok, f"{text!r}: {outcome.reason} {outcome.detail}")
        return outcome.granted, compose_protection(text, outcome)

    def _assert_granted(self, text: str, spans: tuple[tuple[int, int], ...]) -> None:
        """Exact granted-set equality for the whole document."""
        granted, _ = self._protect(text)
        self.assertEqual(set(spans), set(granted))

    def _assert_granted_region(
        self, text: str, spans: tuple[tuple[int, int], ...]
    ) -> None:
        """Each intended positive region is fully usable: every point of it
        is granted and no final protected interval overlaps it."""
        granted, protected = self._protect(text)
        for start, end in spans:
            cursor = start
            for granted_start, granted_end in granted:
                if granted_end <= cursor:
                    continue
                if granted_start > cursor:
                    self.fail(
                        f"{text!r}: gap {cursor}..{granted_start} within granted "
                        f"region ({start}, {end}) in {granted}"
                    )
                cursor = max(cursor, granted_end)
                if cursor >= end:
                    break
            self.assertGreaterEqual(
                cursor, end,
                f"{text!r}: region ({start}, {end}) not fully granted: {granted}",
            )
            for interval in protected:
                self.assertFalse(
                    interval.start < end and interval.end > start,
                    f"{text!r}: final protection {interval} overlaps granted "
                    f"region ({start}, {end})",
                )

    def _assert_protected(
        self, text: str, start: int, end: int, patch: bool = False
    ) -> None:
        """Final composed protection: every point of the region must be
        covered by a protected interval (no exposed tokens inside), whether
        the coverage comes from structural denial or the residual policy."""
        _, protected = self._protect(text)
        cursor = start
        for interval in protected:
            if interval.end <= cursor:
                continue
            if interval.start > cursor:
                self.fail(
                    f"{text!r}: gap {cursor}..{interval.start} within protected "
                    f"region ({start}, {end}) in {protected}"
                )
            cursor = max(cursor, interval.end)
            if cursor >= end:
                break
        self.assertGreaterEqual(
            cursor, end, f"{text!r}: region ({start}, {end}) not fully covered"
        )
        if patch:
            # A targeted interior patch must be refused.
            midpoint = (start + end) // 2
            interior = (midpoint, min(end, midpoint + 1), "x")
            with self.assertRaisesRegex(
                ValueError, "edit intersects protected content"
            ):
                apply_edits(text, [interior], protected)

    # -- useful positives -------------------------------------------------

    def test_plain_prose_exact_spans(self) -> None:
        text = "Dobro jutro. To je zapisano.\n"
        self._assert_granted(
            text,
            (
                (0, 5), (5, 6), (6, 11), (11, 12), (12, 13), (13, 15),
                (15, 16), (16, 18), (18, 19), (19, 27), (27, 28),
            ),
        )
        self._assert_protected(text, 28, 29)

    def test_no_final_lf(self) -> None:
        self._assert_granted("Beseda", ((0, 6),))
        self._assert_granted("Beseda kraj", ((0, 6), (6, 7), (7, 11)))

    def test_nfc_slovenian_with_and_without_final_lf(self) -> None:
        text = "To je presenetljivo napisano.\n"
        self._assert_granted(
            text,
            (
                (0, 2), (2, 3), (3, 5), (5, 6),
                (6, 19), (19, 20), (20, 28), (28, 29),
            ),
        )
        self._assert_protected(text, 29, 30)  # the final LF itself
        self._assert_granted(
            "To je presenetljivo napisano.",
            (
                (0, 2), (2, 3), (3, 5), (5, 6),
                (6, 19), (19, 20), (20, 28), (28, 29),
            ),
        )

    def test_tab_glue(self) -> None:
        text = "zacetek\tkonec\n"
        self._assert_granted(text, ((0, 7), (7, 8), (8, 13)))

    def test_crlf(self) -> None:
        text = "prva\r\ndruga\n"
        self._assert_granted(text, ((0, 4), (6, 11)))
        self._assert_protected(text, 4, 6)

    def test_emoji_prefix(self) -> None:
        text = "\U0001F600 Pozdrav iz Ljubljane.\n"
        # The lone emoji is one stable grapheme and stays usable.
        self._assert_granted(
            text,
            (
                (0, 1), (1, 2), (2, 9), (9, 10),
                (10, 12), (12, 13), (13, 22), (22, 23),
            ),
        )
        self._assert_protected(text, 23, 24)

    def test_repeated_words_distinct_spans(self) -> None:
        text = "zapisano zapisano\n"
        self._assert_granted(text, ((0, 8), (8, 9), (9, 17)))

    def test_list_prose(self) -> None:
        text = "- prva\n- druga\n"
        self._assert_granted(text, ((2, 6), (9, 14)))
        self._assert_protected(text, 0, 2)
        self._assert_protected(text, 6, 9)

    def test_emphasis_prose(self) -> None:
        text = "**To je presenetliv zapisano.**\n"
        self._assert_granted(
            text,
            ((2, 4), (4, 5), (5, 7), (7, 8), (8, 19), (19, 20), (20, 28), (28, 29)),
        )
        self._assert_protected(text, 0, 2)
        self._assert_protected(text, 29, 32)

    def test_strikethrough_and_superscript(self) -> None:
        text = "To je ~~stare~~ in x^2^ zapisano.\n"
        self._assert_granted_region(text, ((8, 13),))  # strikethrough interior prose
        self._assert_protected(text, 5, 8)  # ~~ opener
        self._assert_protected(text, 13, 16)  # ~~ closer

    def test_prose_around_code_url_math_link(self) -> None:
        text = "Uporabi `pip install` sedaj.\n"
        self._assert_granted_region(text, ((0, 7),))
        self._assert_protected(text, 8, 21)
        text = "Odpri https://example.com/x sedaj.\n"
        self._assert_protected(text, 6, 27)
        self._assert_granted_region(text, ((28, 33),))
        text = "Formula $x^2$ tu.\n"
        self._assert_protected(text, 7, 14)
        self._assert_granted_region(text, ((0, 7),))
        text = "Glede [besedilo](http://x.y/z) tu.\n"
        self._assert_protected(text, 5, 31)
        self._assert_granted_region(text, ((0, 5),))

    def test_link_image_whole_including_label(self) -> None:
        text = "Glede ![alt besedilo](http://x.y/z.png) tu.\n"
        self._assert_protected(text, 5, 40)
        self._assert_granted_region(text, ((0, 5), (40, 42)))

    def test_table_deflist_metadata_protected(self) -> None:
        table = "| a | b |\n| - | - |\n| 1 | 2 |\n"
        self._assert_protected(table, 0, len(table) - 1)
        deflist = "term\n: definition\n"
        self._assert_protected(deflist, 0, len(deflist) - 1)
        metadata = "---\ntitle: X\n---\nBeseda\n"
        self._assert_protected(metadata, 0, 17)
        self._assert_granted_region(metadata, ((17, 23),))

    def test_header_and_blockquote_lines(self) -> None:
        # Established residual policy: shell-prompt-style lines (#, >, $)
        # are protected in full, including their structural marker.
        header = "# Naslov besedilo\n"
        self._assert_protected(header, 0, len(header))  # residual shell-style line
        blockquote = "> citat besedilo\n"
        self._assert_protected(blockquote, 0, len(blockquote))

    def test_blockquote_structure_denied_in_full(self) -> None:
        # Order 033-a, requirement 5: a complete Pandoc BlockQuote
        # structure - lazy continuation and nesting included - is denied
        # in full at the structural layer, not only by the residual
        # shell-marker policy: nothing inside it is granted.
        lazy = "> Prvi stavek.\nDanes je lepo vreme.\n"
        granted, _ = self._protect(lazy)
        self.assertEqual(granted, ())
        self._assert_protected(lazy, 0, len(lazy) - 1)
        nested = "> prva\n>   gnezdeno\n\npoje\n"
        granted, _ = self._protect(nested)
        self.assertEqual(granted, ((21, 25),))  # only "poje" after the quote
        self._assert_protected(nested, 0, 21)
        # Independent prose after the proved block boundary stays usable
        # with its exact original spans.
        after = "> citat besedilo\n\nTo je presenetliv zapisano.\n"
        granted, protected = self._protect(after)
        second = "To je presenetliv zapisano."
        base = after.index(second)
        self.assertEqual(
            granted,
            (
                (base, base + 2), (base + 2, base + 3),
                (base + 3, base + 5), (base + 5, base + 6),
                (base + 6, base + 17), (base + 17, base + 18),
                (base + 18, base + 26), (base + 26, base + 27),
            ),
        )
        self._assert_protected(after, 0, base)

    def test_quote_families_interior_protected(self) -> None:
        # Order 033-a, requirement 3: the Slovenian low/high pair, both
        # guillemet directions, and the established curly/straight
        # double and single forms each protect their interior; only a
        # proved compatible closer of the same family releases it.
        for text in (
            "\u201epresenetliv zapisano\u201c zunaj.\n",  # low/high double
            "\u201apresenetliv zapisano\u2018 zunaj.\n",  # low/high single
            "\u00abpresenetliv zapisano\u00bb zunaj.\n",  # guillemet inward
            "\u00bbpresenetliv zapisano\u00ab zunaj.\n",  # guillemet outward
            "\u201cpresenetliv zapisano\u201d zunaj.\n",  # curly double
            "\u2018presenetliv zapisano\u2019 zunaj.\n",  # curly single
            '"presenetliv zapisano" zunaj.\n',  # straight double
            "'presenetliv zapisano' zunaj.\n",  # straight single
        ):
            with self.subTest(family=text[0]):
                self._assert_protected(text, 0, 22)
                self._assert_granted_region(text, ((23, 28),))

    def test_lowhigh_single_quote_outside_only(self) -> None:
        # Order 033-a, requirement 3 (R3): the Slovenian low/high single
        # U+201A...U+2018 is a relevant single quotation; its interior is
        # protected and only the exact outside occurrence of the same
        # token is grantable.  Owned synthetic input (root receipt) with
        # independent original-source oracles.
        text = "\u201aTo je presenetliv zapisano.\u2018 To je presenetliv zapisano.\n"
        self._assert_protected(text, 0, 29)  # the proven low/high single extent
        self._assert_granted_region(text, ((36, 47),))  # the outside token only

    def test_old_baseline_exact_vectors_replay(self) -> None:
        # Order 033-a, R9/A1: replay the exact preserved old-baseline repro
        # vectors (14 red + 4 controls) against the corrected mapper with
        # independent original-source oracles.  The input bytes are the
        # immutable old baseline (verified by SHA-256); the baseline's red
        # assertions are NOT rerun (that log stays immutable) - only the
        # protection oracles are asserted: the required protected range
        # stays fully protected, every non-ordinary target occurrence is
        # not granted, and the ordinary (outside) occurrence is granted.
        for vector in _OLD_BASELINE_VECTORS:
            with self.subTest(case=cast("str", vector["case"])):
                text = cast("str", vector["input"])
                self.assertEqual(
                    hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    cast("str", vector["input_sha256"]),
                )
                granted, protected = self._protect(text)
                raw_range = vector["required_protected_range"]
                if raw_range is not None:
                    start, end = cast("tuple[int, int]", raw_range)
                    cursor = start
                    for interval in protected:
                        if interval.end <= cursor:
                            continue
                        if interval.start > cursor:
                            self.fail(
                                f"{vector['case']}: protected gap at {cursor} "
                                f"in {[(iv.start, iv.end) for iv in protected]}"
                            )
                        cursor = max(cursor, interval.end)
                        if cursor >= end:
                            break
                    self.assertGreaterEqual(
                        cursor, end,
                        f"{vector['case']}: required protected range "
                        f"({start}, {end}) not fully covered: "
                        f"{[(iv.start, iv.end) for iv in protected]}",
                    )
                targets = cast(
                    "tuple[tuple[int, int], ...]",
                    vector["target_original_ranges"],
                )
                ordinary = set(
                    cast(
                        "tuple[int, ...]",
                        vector["ordinary_target_occurrence_indices"],
                    )
                )
                for index, (start, end) in enumerate(targets):
                    if index in ordinary:
                        # outside-only oracle: this occurrence is grantable.
                        cursor = start
                        for gs, ge in sorted(granted):
                            if ge <= cursor:
                                continue
                            if gs > cursor:
                                break
                            cursor = max(cursor, ge)
                            if cursor >= end:
                                break
                        self.assertGreaterEqual(
                            cursor, end,
                            f"{vector['case']}: ordinary occurrence "
                            f"({start}, {end}) not granted: {granted}",
                        )
                    else:
                        leaked = [
                            (gs, ge)
                            for gs, ge in granted
                            if gs < end and ge > start
                        ]
                        self.assertEqual(
                            leaked, [],
                            f"{vector['case']}: protected occurrence "
                            f"({start}, {end}) leaked grants: {leaked}",
                        )

    def test_escaped_and_entity_quote_pairs(self) -> None:
        # Order 033-a, requirement 3 and the established accepted-base
        # standalone escaped-quotation control: an escaped or entity
        # pair protects its target, and an in-word entity apostrophe
        # stays ordinary punctuation (inert, never granted).
        escaped = '\\"citat besedilo\\" je zapisano.\n'
        self._assert_protected(escaped, 0, 18)
        self._assert_granted_region(escaped, ((19, 31),))
        entity = "&ldquo;citat besedilo&rdquo; je zapisano.\n"
        self._assert_protected(entity, 0, 28)
        self._assert_granted_region(entity, ((29, 41),))
        in_word = "don&apos;t zapisano.\n"
        self._assert_granted_region(in_word, ((0, 3), (10, 18)))
        self._assert_protected(in_word, 3, 9)  # the &apos; fragment itself

    def test_cross_family_markers_do_not_release_outer(self) -> None:
        # Order 033-a, requirement 3: an escaped or entity inner marker
        # can never release a different (literal) outer quotation, and a
        # literal marker can never release a normalized level; the
        # unproved extent protects fail-closed.
        escaped_inner = '"presenetliv \\"zapisano\\" je" tu.\n'
        self._assert_protected(escaped_inner, 0, 29)
        self._assert_granted_region(escaped_inner, ((30, 33),))
        entity_inner = '&ldquo;presenetliv "zapisano"&rdquo; je.\n'
        self._assert_protected(entity_inner, 0, 36)
        self._assert_granted_region(entity_inner, ((37, 40),))
        # The required complementary direction: a literal outer marker is
        # never released by an entity inner marker, either.
        literal_outer_entity_inner = '"presenetliv &ldquo;zapisano&rdquo; je" tu.\n'
        self._assert_protected(literal_outer_entity_inner, 0, 40)
        self._assert_granted_region(literal_outer_entity_inner, ((40, 43),))

    def test_nested_quotes_across_delimiters(self) -> None:
        # Nesting stays distinct across delimiters: the inner single
        # form releases only its own level, never the outer double.
        text = '"a \'b\' c" je.\n'
        self._assert_protected(text, 0, 9)
        self._assert_granted_region(text, ((10, 13),))

    def test_cross_block_quotation_extent(self) -> None:
        # A quotation whose proved closer sits in a later block denies
        # the source-ordered extent between the proved markers.
        text = 'To je "presenetliv\n\nzapisano" je.\n'
        granted, _ = self._protect(text)
        self.assertEqual(
            set(granted),
            {(0, 2), (2, 3), (3, 5), (30, 32), (32, 33)},
        )
        self._assert_protected(text, 7, 29)

    def test_quoted_footnote_definition_denied_in_full(self) -> None:
        # Order 033-a, requirements 4-5: a footnote definition quoted in
        # a BlockQuote empties the BlockQuote in the pinned reader while
        # the payload is relocated under the later reference; the proven
        # wrapper extent keeps the entire quoted original region denied
        # against the relocated Note candidate grants.  Owned synthetic
        # structural input (root receipt).
        text = "> [^n]: To je presenetliv zapisano.\n\nTo[^n]\n"
        granted, _ = self._protect(text)
        self.assertEqual(granted, ((37, 39),))  # only the outside "To"
        self._assert_protected(text, 0, 36)

    def test_quoted_footnote_definition_lazy_denied_in_full(self) -> None:
        # The unmarked lazy continuation line belongs to the same quoted
        # region and stays denied as well.  Owned synthetic structural
        # input (root receipt).
        text = "> [^n]: To je\npresenetliv zapisano.\n\nTo[^n]\n"
        granted, _ = self._protect(text)
        self.assertEqual(granted, ((37, 39),))  # only the outside "To"
        self._assert_protected(text, 0, 36)

    def test_footnote_relocation_source_order_control(self) -> None:
        # Order 033-a, requirement 4 (recorded source-order control): the
        # relocated definition replayed at its proven physical position
        # neither denies earlier ordinary prose nor promotes the quote
        # region; the definition prose outside any quotation stays
        # usable with its exact original spans.
        text = "To[^n] je zapisano.\n\n[^n]: citatno besedilo\n"
        granted, _ = self._protect(text)
        self.assertEqual(
            set(granted),
            {
                (0, 2), (7, 9), (9, 10), (10, 18), (18, 19),
                (27, 34), (34, 35), (35, 43),
            },
        )
        self._assert_protected(text, 2, 6)  # the reference
        self._assert_protected(text, 21, 27)  # the definition marker

    def test_repeated_footnote_reference_coalesced(self) -> None:
        # Order 033-a, requirement 4: a definition referenced twice
        # duplicates one physical payload in the AST; coalescing replays
        # it exactly once, so ordinary prose around every reference stays
        # usable and the definition prose is granted at its position.
        text = "To[^n] je.\nIn spet[^n] tukaj.\n\n[^n]: citatno besedilo\n"
        granted, _ = self._protect(text)
        self.assertEqual(
            set(granted),
            {
                (0, 2), (7, 9), (9, 10),
                (11, 13), (13, 14), (14, 18), (23, 28), (28, 29),
                (37, 44), (44, 45), (45, 53),
            },
        )
        self._assert_protected(text, 2, 6)
        self._assert_protected(text, 18, 22)
        self._assert_protected(text, 31, 37)

    # -- trap negatives ----------------------------------------------------

    def test_nfd_line_abstain(self) -> None:
        text = "ka\u017ef + e\u0301: " + "e\u0301"
        granted, protected = self._protect(text)
        self.assertEqual(granted, ())
        self.assertEqual(protected[0].start, 0)
        self.assertEqual(protected[-1].end, len(text))

    def test_nfc_unstable_line_unproved_quote_and_html_fail_closed(self) -> None:
        # Order 033-a, R2/R7: a structural context opener whose original
        # line is not NFC-stable must not be placed from the reader's
        # NFC-normalized columns into a guessed original offset.  The
        # unproved extent stays fail-closed, the independent original
        # protected range (including the planted sentence) is denied, and
        # no grant leaks into it.  Owned synthetic inputs (root receipt).
        for text, protected in (
            ("\u0344" * 32 + '"\n\nTo je presenetliv zapisano.\n', (32, 63)),
            ("\u0344" * 32 + " <b>\n\nTo je presenetliv zapisano.\n", (33, 66)),
        ):
            with self.subTest(first=text[32:36]):
                granted, _ = self._protect(text)
                self._assert_protected(text, protected[0], protected[1])
                leaked = [
                    (gs, ge)
                    for gs, ge in granted
                    if gs < protected[1] and ge > protected[0]
                ]
                self.assertEqual(leaked, [])

    def test_bare_cr_protected(self) -> None:
        text = "a\rb\n"
        granted, _ = self._protect(text)
        self.assertEqual(granted, ())

    def test_control_chars_protected(self) -> None:
        for char in ("\x00", "\u2028", "\u2029", "\x85", "\x0c"):
            text = f"ab{char}cd\n"
            granted, _ = self._protect(text)
            self.assertEqual(
                granted, (), f"control char {char!r} leaked a grant: {granted}"
            )

    def test_escapes_and_entities_protected(self) -> None:
        text = "To je \\*zvezda\\* sedaj.\n"
        self._assert_protected(text, 5, 8)  # \* opener fragment
        self._assert_protected(text, 14, 17)  # \* closer fragment
        self._assert_granted_region(text, ((8, 14),))  # the inner word is prose
        entity = "To je &amp; zapisano.\n"
        self._assert_protected(entity, 5, 12)  # &amp; fragment
        self._assert_granted_region(entity, ((12, 20),))

    def test_tex_forms_and_malformed_protected(self) -> None:
        inline = r"\(To je presenetliv zapisano.\)\n"
        # The whole expression, including the closing delimiter, is
        # protected; the fixture's trailing literal backslash-n is ordinary
        # text outside the expression.
        self._assert_protected(inline, 0, 31)
        # Malformed (unterminated) opener with a math-like remainder: the
        # frozen residual policy protects to the end of the text.
        unterminated = r"\(x^2 + y.\n"
        self._assert_protected(unterminated, 0, len(unterminated))
        # The unproved prose form: no closing delimiter anywhere, so the
        # bounded proxy addition protects to the end of the line.
        malformed = r"\(To je presenetliv zapisano.\n"
        self._assert_protected(malformed, 0, len(malformed) - 1)
        bracket = "U \\[0, 1\\] sedaj.\n"
        self._assert_protected(bracket, 3, 11)
        env = "U \\begin{equation} a \\end{equation} sedaj.\n"
        self._assert_protected(env, 2, 35)

    def test_literal_quotes_interior_protected(self) -> None:
        text = 'To je "presenetliv zapisano" zunaj.\n'
        self._assert_protected(text, 7, 27)
        self._assert_granted_region(text, ((29, 34),))
        # Unpaired opener: the remainder of the line stays protected.
        unpaired = 'To je "presenetliv sedaj.\n'
        self._assert_protected(unpaired, 6, 25)
        # In-word apostrophe is ordinary punctuation, not a delimiter.
        apostrophe = "To je don't zapisano.\n"
        self._assert_granted_region(apostrophe, ((12, 20), (10, 11)))

    def test_grapheme_joiner_mark_protected(self) -> None:
        text = "To je presenetliv\u034f zapisano.\n"
        self._assert_protected(text, 6, 18)  # word plus its U+034f joiner
        self._assert_granted_region(text, ((19, 27),))

    def test_zwj_and_modifier_sequences_protected(self) -> None:
        zwj = "a \U0001F468\u200d\U0001F469 b\n"
        self._assert_protected(zwj, 2, 5)
        self._assert_granted_region(zwj, ((0, 1),))
        skin = "\U0001F44d\U0001F3FD dobro\n"
        self._assert_protected(skin, 0, 2)
        self._assert_granted_region(skin, ((3, 8),))
        regional = "z\U0001F1F8\U0001F1EE dobro\n"
        self._assert_protected(regional, 1, 3)
        self._assert_granted_region(regional, ((4, 9),))

    def test_html_fragments(self) -> None:
        full = "<b>To je presenetliv zapisano.</b> zunaj\n"
        self._assert_protected(full, 0, 35)
        self._assert_granted_region(full, ((35, 40),))
        between = "<i>a</i> besedilo <b>b</b>\n"
        self._assert_granted_region(between, ((9, 17),))
        self._assert_protected(between, 0, 9)
        self._assert_protected(between, 17, 27)
        unclosed = "besedilo <b>ok\n"
        self._assert_granted_region(unclosed, ((0, 8),))
        self._assert_protected(unclosed, 12, 14)
        void = "prvi<br>drugi\n"
        self._assert_granted_region(void, ((0, 4), (8, 13)))
        inner = "<b>ponosno</b> besedilo\n"
        self._assert_protected(inner, 3, 10)
        self._assert_granted_region(inner, ((15, 23),))

    def test_html_context_repair(self) -> None:
        # Order 033-a, requirement 6: compound (multi-line) opening tag
        # positions, mismatched and split closers, tags under emphasis,
        # unclosed tags into later blocks, and attribute quotes.
        multiline = 'prvi <div\n    attr="x">\nstavek</div> zunaj\n'
        open_start = multiline.index("<div")
        close_end = multiline.index("</div>") + 5
        self._assert_protected(multiline, open_start, close_end)
        self._assert_granted_region(
            multiline,
            ((0, 4), (multiline.index("zunaj"), multiline.index("zunaj") + 5)),
        )
        crlf = 'prvi <div\r\n    attr="x">\nstavek</div> zunaj\n'
        open_start = crlf.index("<div")
        close_end = crlf.index("</div>") + 5
        self._assert_protected(crlf, open_start, close_end)
        self._assert_granted_region(
            crlf,
            ((0, 4), (crlf.index("zunaj"), crlf.index("zunaj") + 5)),
        )
        # A closer with another identity cannot discharge the opener.
        mismatched = "<b>a</i> b</b> c\n"
        self._assert_protected(mismatched, 0, 13)
        self._assert_granted_region(mismatched, ((15, 16),))
        # A split closer the reader does not recognize as a tag can
        # never release the unmatched opener by raw-string matching.
        split = "<b>a</\nb> c\n"
        granted, _ = self._protect(split)
        self.assertEqual(granted, ())
        self._assert_protected(split, 0, len(split) - 1)
        # An opening tag under emphasis keeps its source-ordered extent.
        emph = "**<b>a</b>** c\n"
        self._assert_protected(emph, 0, 12)
        self._assert_granted_region(emph, ((13, 14),))
        # An unclosed opener denies through the following block.
        into_next = "prvi <b>stavek\n\nzapisano.\n"
        granted, _ = self._protect(into_next)
        self.assertEqual(granted, ((0, 4),))
        self._assert_protected(into_next, 5, len(into_next) - 1)
        # Quotes in tag attributes are machine syntax, not markers.
        attr = '<a href="x">stavek</a> zunaj\n'
        self._assert_protected(attr, 0, 21)
        self._assert_granted_region(attr, ((23, 28),))

    def test_nested_emphasis_in_denied_contexts(self) -> None:
        strong_quote = 'To je "**presenetliv zapisano**" zunaj.\n'
        self._assert_protected(strong_quote, 8, 31)
        self._assert_granted_region(strong_quote, ((33, 38), (38, 39)))
        emph_quote = 'To je "*presenetliv* zapisano" zunaj.\n'
        self._assert_protected(emph_quote, 9, 20)
        self._assert_protected(emph_quote, 22, 30)
        self._assert_granted_region(emph_quote, ((31, 36), (36, 37)))
        strong_html = "<b>**presenetliv zapisano**</b> zunaj\n"
        self._assert_protected(strong_html, 6, 26)
        self._assert_granted_region(strong_html, ((32, 37),))
        # Plain emphasis without a denied context stays usable.
        plain = "To je *presenetliv* zapisano.\n"
        self._assert_granted_region(plain, ((7, 18),))
        self._assert_protected(plain, 5, 7)

    def test_empty_document(self) -> None:
        granted, protected = self._protect("")
        self.assertEqual(granted, ())
        self.assertEqual(protected, [])

    def test_data_pos_collision_unit(self) -> None:
        # Hand-crafted AST: one wrapper Span with two distinct data-pos
        # values defeats provenance for that leaf (no grant).
        document = {
            "pandoc-api-version": [1, 23, 1, 1],
            "meta": {},
            "blocks": [
                {
                    "t": "Div",
                    "c": [
                        ["", [], [["wrapper", "1"], ["data-pos", "1:1-2:1"]]],
                        [
                            {
                                "t": "Para",
                                "c": [
                                    {
                                        "t": "Span",
                                        "c": [
                                            [
                                                "",
                                                [],
                                                [
                                                    ["wrapper", "1"],
                                                    ["data-pos", "1:1-1:7"],
                                                    ["data-pos", "1:1-1:9"],
                                                ],
                                            ],
                                            [{"t": "Str", "c": "Beseda"}],
                                        ],
                                    }
                                ],
                            }
                        ],
                    ],
                }
            ],
        }
        doc = pandoc_protection._Document("Beseda\n")
        pandoc_protection._walk_blocks(doc, cast("list[dict[str, object]]", document["blocks"]))
        self.assertEqual(doc.granted, [])

    def test_user_data_pos_collision_real_markdown(self) -> None:
        # A user data-pos colliding with the generated container position
        # defeats provenance for that container node only.  Leaf provenance
        # is machine-generated, so inner prose keeps its own exact spans.
        text = '::: {.x data-pos="1:9-1:9"}\nBeseda\n:::\n'
        granted, protected = self._protect(text)
        self.assertIn((28, 34), granted)  # Beseda at its exact offsets
        self._assert_protected(text, 0, 28)
        self._assert_protected(text, 34, len(text) - 1)

    def test_header_user_data_pos_collision_real_markdown(self) -> None:
        # Same collision at a Header: the document stays ok and the
        # shell-prompt-style line (#) is protected in full by the
        # established residual policy, regardless of the collision.
        text = '# Naslov {#h data-pos="9:9-9:9"}\n'
        self._protect(text)  # document stays ok
        # Any raw structural grant is contained: the whole line is finally
        # protected by the established residual policy.
        self._assert_protected(text, 0, len(text))

    def test_forged_wrapper_without_position_unit(self) -> None:
        # wrapper="1" without any data-pos is untrusted: no grant.
        document = {
            "pandoc-api-version": [1, 23, 1, 1],
            "meta": {},
            "blocks": [
                {
                    "t": "Div",
                    "c": [
                        ["", [], [["wrapper", "1"], ["data-pos", "1:1-2:1"]]],
                        [
                            {
                                "t": "Para",
                                "c": [
                                    {
                                        "t": "Span",
                                        "c": [
                                            ["", [], [["wrapper", "1"]]],
                                            [{"t": "Str", "c": "Beseda"}],
                                        ],
                                    }
                                ],
                            }
                        ],
                    ],
                }
            ],
        }
        doc = pandoc_protection._Document("Beseda\n")
        pandoc_protection._walk_blocks(doc, cast("list[dict[str, object]]", document["blocks"]))
        self.assertEqual(doc.granted, [])


class ResidualReuseTests(unittest.TestCase):
    def test_residual_reuses_established_research_policy(self) -> None:
        from protection_residuals import residual_intervals

        intervals = residual_intervals(r"Uporabi \(x^2\) in \[0, 1\] sedaj.")
        classes = {cls for item in intervals for cls in item.reason.split("+")}
        self.assertIn("tex-paren", classes)
        self.assertIn("tex-bracket", classes)
        intervals = residual_intervals('Konfig: a = 1 in [1, 2] in <Konfig/>.')
        self.assertTrue(
            any(item.reason in ("bare-json", "config", "number") for item in intervals)
        )
        intervals = residual_intervals("besedilo", tool_arguments=("besedilo",))
        self.assertIn("tool-argument", {item.reason for item in intervals})

    def test_unterminated_tex_proxy_addition(self) -> None:
        from protection_residuals import _unterminated_tex_spans, residual_intervals

        # No closing delimiter anywhere: bounded protection to end of line.
        text = r"\(To je presenetliv zapisano."
        self.assertIn(
            ("tex-unterm-paren", 0, len(text)), _unterminated_tex_spans(text)
        )
        classes = {
            cls for item in residual_intervals(text) for cls in item.reason.split("+")
        }
        self.assertIn("tex-unterm-paren", classes)
        # A closing delimiter anywhere keeps the opener under the frozen rule.
        self.assertEqual(_unterminated_tex_spans(r"\(a\) b"), [])
        self.assertEqual(_unterminated_tex_spans("U \\[0, 1\\] sedaj."), [])


def _build_corpus(root: Path) -> Path:
    db = root / "tiny.sqlite"
    connection = sqlite3.connect(db)
    connection.executescript(
        """
        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE unigram (word TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE bigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE trigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE middle (left_word TEXT, right_word TEXT, middle_word TEXT, count INTEGER,
            PRIMARY KEY(left_word,right_word,middle_word));
        INSERT INTO unigram VALUES
            ('to',100),('je',100),('tako',100),('presenetljiv',50),('zapisano',50);
        INSERT INTO bigram VALUES
            ('je tako',20),('tako zapisano',20),('je presenetljiv',20),('je zapisano',20),
            -- explicit original-context bigram for the typo original: 'je presenetliv' 10
            -- is the EXACT comparable context at factor 2 against candidate 'je tako' 20
            ('je presenetliv',10);
        INSERT INTO trigram VALUES ('to je tako',20),('je tako zapisano',20);
        INSERT INTO middle VALUES ('je','zapisano','tako',20);
        """
    )
    connection.commit()
    connection.close()
    return db


class _ReviewerThatFailsIfCalled:
    def __init__(self) -> None:
        self.calls = 0

    def review(self, sentence: str, target: str, variant: str = "frozen-v1") -> Proposal:
        self.calls += 1
        raise AssertionError("reviewer must not be called")

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> BatchResult:
        self.calls += 1
        raise AssertionError("reviewer must not be called")


class _FakeReviewer:
    def __init__(self, replacement: str = "tako") -> None:
        self.replacement = replacement
        self.calls = 0

    def review(self, sentence: str, target: str, variant: str = "frozen-v1") -> Proposal:
        self.calls += 1
        return Proposal(False, self.replacement, False)

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> BatchResult:
        self.calls += 1
        return BatchResult(
            {
                target.id: BatchProposal(
                    target.id, False, self.replacement, False
                )
                for target in targets
            },
            None,
        )


class EngineBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        import proxy

        self.proxy_module = proxy

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_map_failure_returns_exact_original_before_corpus(self) -> None:
        fake = self.root / "garbage"
        fake.write_text(
            f"#!{sys.executable}\nimport sys\nsys.stdout.write('garbage')\n",
            encoding="utf-8",
        )
        fake.chmod(0o700)
        reviewer = _ReviewerThatFailsIfCalled()
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=PandocSpec(binary=str(fake))
        )
        opened: list[bool] = []

        class _SentinelCorpus:
            def __init__(self, *args: object, **kwargs: object) -> None:
                opened.append(True)

            def close(self) -> None:
                return None

        engine.begin_request()
        text = "To je presenetliv zapisano."
        with mock.patch.object(self.proxy_module, "RuntimeCorpus", _SentinelCorpus):
            repaired = engine.repair(text)
        self.assertEqual(repaired, text)  # byte-exact original
        self.assertEqual(reviewer.calls, 0)
        self.assertEqual(opened, [])  # corpus never opened
        details = engine.take_details()
        self.assertEqual(len(details), 1)
        self.assertEqual(details[0]["original"], text)
        self.assertEqual(details[0]["repaired"], text)
        self.assertEqual(details[0]["candidates"], [])
        self.assertEqual(details[0]["reviewer_decisions"], [])
        self.assertIn("protection_failure", details[0])
        failure = cast("dict[str, object]", details[0]["protection_failure"])
        self.assertIsInstance(failure, dict)
        self.assertEqual(failure["reason"], "PANDOC_MALFORMED_OUTPUT")

    def test_input_too_large_fails_before_mapper_subprocess_and_corpus(self) -> None:
        # Oversized input must fail the declared bound before the per-
        # codepoint mapper is constructed, before the Pandoc subprocess,
        # and before the corpus is opened (requirement 8).
        reviewer = _ReviewerThatFailsIfCalled()
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=PandocSpec(binary=str(self.root / "unused"))
        )
        opened: list[bool] = []

        class _SentinelCorpus:
            def __init__(self, *args: object, **kwargs: object) -> None:
                opened.append(True)

            def close(self) -> None:
                return None

        document_calls: list[bool] = []

        def _sentinel_document(text: str) -> object:
            document_calls.append(True)
            raise AssertionError("mapper must not be built for oversized input")

        limit = config.PANDOC_MAX_INPUT_BYTES
        oversize = "a" * (limit + 1)
        engine.begin_request()
        # Order 025-a, requirement 7: the default finite
        # analysis-eligibility limits (32768 code points / 131072
        # bytes) would bypass this unchanged payload before the
        # original Pandoc preflight, so this test scopes valid
        # analysis limits above it to keep the actual original parser
        # cap under test.  The payload and every assertion are
        # unchanged: this is axis separation, not a default-policy
        # run.
        with mock.patch.object(
            pandoc_protection, "_Document", _sentinel_document
        ), mock.patch.object(self.proxy_module, "RuntimeCorpus", _SentinelCorpus), \
                mock.patch.object(
                    config, "RUNTIME_ANALYSIS_MAX_CODEPOINTS", 2_000_000
                ), mock.patch.object(
                    config, "RUNTIME_ANALYSIS_MAX_UTF8_BYTES", 4_000_000
                ):
            repaired = engine.repair(oversize)
        self.assertEqual(repaired, oversize)  # byte-exact original
        self.assertEqual(reviewer.calls, 0)
        self.assertEqual(opened, [])  # corpus never opened
        self.assertEqual(document_calls, [])  # mapper never constructed
        details = engine.take_details()
        failure = cast("dict[str, object]", details[0]["protection_failure"])
        self.assertIsInstance(failure, dict)
        self.assertEqual(failure["reason"], "PANDOC_INPUT_TOO_LARGE")

    def test_engine_failure_modes_return_exact_original(self) -> None:
        text = "To je presenetliv zapisano."
        bad_json = _write_fake(
            self.root,
            "badjson",
            f"#!{sys.executable}\nimport sys\nsys.stdout.write('{{\"blocks\":{{}}}}')\n",
        )
        bad_exit = _write_fake(self.root, "badexit", "#!/bin/sh\nexit 3\n")
        sleeper = _write_fake(
            self.root,
            "sleeper",
            f"#!{sys.executable}\nimport time\ntime.sleep(30)\n",
        )
        for name, binary, timeout, expected in (
            ("valid-json-invalid-schema", str(bad_json), None, "PANDOC_SCHEMA"),
            ("nonzero-exit", str(bad_exit), None, "PANDOC_BAD_EXIT"),
            ("runtime-timeout", str(sleeper), 1.0, "PANDOC_TIMEOUT"),
        ):
            with self.subTest(mode=name):
                reviewer = _ReviewerThatFailsIfCalled()
                if timeout is None:
                    spec = PandocSpec(binary=binary)
                else:
                    spec = PandocSpec(binary=binary, timeout=timeout)
                engine = self.proxy_module.RepairEngine(
                    self.db, reviewer, pandoc=spec
                )
                opened: list[bool] = []

                class _SentinelCorpus:
                    def __init__(
                        self,
                        *args: object,
                        _opened: list[bool] = opened,
                        **kw: object,
                    ) -> None:
                        _opened.append(True)

                    def close(self) -> None:
                        return None

                engine.begin_request()
                with mock.patch.object(
                    self.proxy_module, "RuntimeCorpus", _SentinelCorpus
                ):
                    repaired = engine.repair(text)
                self.assertEqual(repaired, text)
                self.assertEqual(reviewer.calls, 0)
                self.assertEqual(opened, [])
                details = engine.take_details()
                failure = cast("dict[str, object]", details[0]["protection_failure"])
                self.assertIsInstance(failure, dict)
                self.assertEqual(failure["reason"], expected)

    def test_node_limit_returns_exact_original(self) -> None:
        reviewer = _ReviewerThatFailsIfCalled()
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=_real_spec()
        )
        text = "To je presenetliv zapisano."
        with mock.patch.object(pandoc_protection, "PANDOC_MAX_BLOCKS", 1), \
                mock.patch.object(pandoc_protection, "PANDOC_MAX_INLINES", 1):
            self.assertEqual(engine.repair(text), text)
        self.assertEqual(reviewer.calls, 0)

    def test_missing_binary_fails_closed(self) -> None:
        reviewer = _ReviewerThatFailsIfCalled()
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=PandocSpec(binary=str(self.root / "missing"))
        )
        text = "To je presenetliv zapisano."
        self.assertEqual(engine.repair(text), text)
        self.assertEqual(reviewer.calls, 0)

    def test_success_path_no_candidates(self) -> None:
        reviewer = _ReviewerThatFailsIfCalled()
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=_real_spec()
        )
        text = "To je zapisano."
        self.assertEqual(engine.repair(text), text)
        self.assertEqual(reviewer.calls, 0)

    def test_success_path_accepts_real_repair(self) -> None:
        reviewer = _FakeReviewer("tako")
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=_real_spec()
        )
        repaired = engine.repair("To je presenetliv zapisano.")
        self.assertEqual(repaired, "To je tako zapisano.")
        self.assertGreaterEqual(reviewer.calls, 1)

    def test_lazy_blockquote_zero_calls_byte_identical(self) -> None:
        # Order 033-a, requirement 5: a planted token inside a complete
        # BlockQuote (lazy continuation) is fully protected - zero
        # candidates, zero review calls, the exact completed original.
        reviewer = _ReviewerThatFailsIfCalled()
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=_real_spec()
        )
        engine.begin_request()
        text = "> Prvi stavek.\nDanes je presenetliv zapisano.\n"
        repaired = engine.repair(text)
        self.assertEqual(repaired, text)  # byte-exact original
        self.assertEqual(reviewer.calls, 0)
        details = engine.take_details()
        self.assertEqual(len(details), 1)
        self.assertEqual(details[0]["candidates"], [])

    def test_quoted_footnote_definition_zero_calls_byte_identical(self) -> None:
        # Order 033-a, requirements 4-5 and 8: a target located only
        # inside the quoted footnote definition (relocated Note payload)
        # must cause zero review and a byte-identical original.
        reviewer = _ReviewerThatFailsIfCalled()
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=_real_spec()
        )
        engine.begin_request()
        text = "> [^n]: To je presenetliv zapisano.\n\nTo[^n]\n"
        repaired = engine.repair(text)
        self.assertEqual(repaired, text)  # byte-exact original
        self.assertEqual(reviewer.calls, 0)
        details = engine.take_details()
        self.assertEqual(details[0]["candidates"], [])

    def test_nfc_unstable_line_zero_calls_byte_identical(self) -> None:
        # Order 033-a, R2/R7: a structural context opener on a non-NFC-
        # stable original line leaves its extent unproved; the document
        # fails closed with zero candidates, zero review calls and the
        # byte-exact original, and the independent original protected
        # range (covering the planted sentence) is denied.  Owned synthetic
        # inputs (root receipt).
        reviewer = _ReviewerThatFailsIfCalled()
        for text, protected in (
            ("\u0344" * 32 + '"\n\nTo je presenetliv zapisano.\n', (32, 63)),
            ("\u0344" * 32 + " <b>\n\nTo je presenetliv zapisano.\n", (33, 66)),
        ):
            with self.subTest(first=text[32:36]):
                engine = self.proxy_module.RepairEngine(
                    self.db, reviewer, pandoc=_real_spec()
                )
                engine.begin_request()
                repaired = engine.repair(text)
                self.assertEqual(repaired, text)  # byte-exact original
                details = engine.take_details()
                self.assertEqual(len(details), 1)
                self.assertEqual(details[0]["candidates"], [])
                outcome = protect_with_pandoc(_real_spec(), text)
                prot = compose_protection(text, outcome)
                covers = any(
                    iv.start <= protected[0] and iv.end >= protected[1]
                    for iv in prot
                )
                self.assertTrue(
                    covers, f"protected range {protected} not denied: {prot}"
                )
        self.assertEqual(reviewer.calls, 0)

    def test_same_token_protected_and_outside_only(self) -> None:
        # Order 033-a, requirement 8: when the same token appears
        # protected (inside a proved BlockQuote) and ordinary, only the
        # exact outside occurrence may change.
        reviewer = _FakeReviewer("tako")
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=_real_spec()
        )
        engine.begin_request()
        text = (
            "> To je presenetliv zapisano.\n"
            "> To je presenetliv zapisano.\n"
            "\n"
            "To je presenetliv zapisano.\n"
        )
        repaired = engine.repair(text)
        self.assertEqual(
            repaired,
            (
                "> To je presenetliv zapisano.\n"
                "> To je presenetliv zapisano.\n"
                "\n"
                "To je tako zapisano.\n"
            ),
        )
        self.assertEqual(reviewer.calls, 1)  # one bounded batch

    def test_lowhigh_single_quote_engine_outside_only(self) -> None:
        # Order 033-a, requirement 3 (R3): with the proven low/high single
        # family in place, the engine repairs only the exact outside
        # occurrence in one bounded batch; the protected interior is left
        # byte-exact.  Owned synthetic input (root receipt).
        reviewer = _FakeReviewer("tako")
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=_real_spec()
        )
        engine.begin_request()
        text = "\u201aTo je presenetliv zapisano.\u2018 To je presenetliv zapisano.\n"
        repaired = engine.repair(text)
        self.assertEqual(
            repaired,
            "\u201aTo je presenetliv zapisano.\u2018 To je tako zapisano.\n",
        )
        self.assertEqual(reviewer.calls, 1)  # one bounded batch

    def test_recorded_quoted_repeated_note_source_order(self) -> None:
        # Order 033-a, requirement 4 (R4, recorded source-order control):
        # the earlier ordinary target is repaired in one bounded batch while
        # the later quoted footnote definition stays byte-exact; a future
        # AST-order/double-toggle regression that grants the relocated
        # definition would fail here.  Owned synthetic input (root receipt).
        reviewer = _FakeReviewer("tako")
        engine = self.proxy_module.RepairEngine(
            self.db, reviewer, pandoc=_real_spec()
        )
        engine.begin_request()
        text = (
            'To[^1] je[^1].\n\n'
            'To je presenetliv zapisano.\n\n'
            '[^1]: "To je presenetliv zapisano.\n'
        )
        repaired = engine.repair(text)
        self.assertEqual(
            repaired,
            (
                'To[^1] je[^1].\n\n'
                'To je tako zapisano.\n\n'
                '[^1]: "To je presenetliv zapisano.\n'
            ),
        )
        self.assertEqual(reviewer.calls, 1)  # one bounded batch


class AcceptancePatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _candidate(self, text: str, start: int, end: int) -> Candidate:
        return Candidate(start, end, text[start:end], 1.0,
                         {"unigram": {"state": "UNAVAILABLE"}})

    def test_stale_candidate_bounds(self) -> None:
        text = "To je presenetliv zapisano."
        with Corpus(self.db) as corpus:
            candidate = self._candidate(text, 6, 17)
            stale = Candidate(candidate.start, candidate.end, "other", 1.0, {})
            decision = accept(text, stale, Proposal(False, "tako", False), corpus, [])
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "stale-candidate-bounds")

    def test_invalid_candidate_bounds_rejected(self) -> None:
        text = "To je presenetliv zapisano."
        with Corpus(self.db) as corpus:
            for start, end in ((-1, 5), (6, len(text) + 3), (9, 7)):
                candidate = Candidate(start, end, text[6:7], 1.0, {})
                decision = accept(
                    text, candidate, Proposal(False, "tako", False), corpus, []
                )
                self.assertFalse(decision.accepted)
                self.assertEqual(decision.reason, "stale-candidate-bounds")

    def test_invalid_neighbor_bounds_rejected(self) -> None:
        text = "To je presenetliv zapisano."
        with Corpus(self.db) as corpus:
            candidate = self._candidate(text, 6, 17)
            for bounds in ((-1, 4), (2, len(text) + 2), (4, 2)):
                decision = accept(
                    text,
                    candidate,
                    Proposal(False, "tako", False),
                    corpus,
                    [],
                    left="je",
                    left_bounds=bounds,
                )
                self.assertFalse(decision.accepted)
                self.assertEqual(decision.reason, "stale-neighbor-bounds")

    def test_capitalized_neighbor_key_accepted(self) -> None:
        text = "To je presenetliv zapisano."
        with Corpus(self.db) as corpus:
            candidate = self._candidate(text, 6, 17)
            # Original slice "To" vs tokenizer key "to": bounds valid.
            decision = accept(
                text,
                candidate,
                Proposal(False, "tako", False),
                corpus,
                [],
                left="to",
                left_bounds=(0, 2),
                right="zapisano",
                right_bounds=(18, 26),
            )
        self.assertTrue(decision.accepted, decision.reason)

    def test_barrier_between_neighbor(self) -> None:
        text = "To je `git status` presenetliv zapisano."
        intervals = protected_intervals(text)
        with Corpus(self.db) as corpus:
            start = text.index("presenetliv")
            candidate = self._candidate(text, start, start + len("presenetliv"))
            # The protected code fragment sits strictly between the left
            # neighbor "je" and the candidate.
            left = text.index(" je ") + 1
            right = text.index("zapisano")
            decision = accept(
                text,
                candidate,
                Proposal(False, "tako", False),
                corpus,
                intervals,
                left="je",
                left_bounds=(left, left + 2),
                right="zapisano",
                right_bounds=(right, right + len("zapisano")),
            )
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "barrier-between-neighbor")

    def test_barrier_between_neighbor_right(self) -> None:
        text = "To je presenetliv `git status` zapisano."
        intervals = protected_intervals(text)
        with Corpus(self.db) as corpus:
            start = text.index("presenetliv")
            candidate = self._candidate(text, start, start + len("presenetliv"))
            right = text.index("zapisano")
            decision = accept(
                text,
                candidate,
                Proposal(False, "tako", False),
                corpus,
                intervals,
                left="je",
                left_bounds=(3, 5),
                right="zapisano",
                right_bounds=(right, right + 8),
            )
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "barrier-between-neighbor")

    def test_grapheme_sensitive_replacement_rejected(self) -> None:
        text = "To je presenetliv zapisano."
        with Corpus(self.db) as corpus:
            candidate = self._candidate(text, 6, 17)
            decision = accept(
                text,
                candidate,
                Proposal(False, "ta\u030cko", False),
                corpus,
                [],
            )
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "grapheme-sensitive-replacement")

    def test_apply_edits_split_grapheme_rejected(self) -> None:
        # Composed protection: the word plus its U+034f joiner is one
        # protected interval, so editing the word body up to (but not
        # including) the joiner must be refused.
        text = "To je presenetliv\u034f zapisano."
        intervals = protected_intervals(text)
        with self.assertRaisesRegex(
            ValueError, "edit intersects protected content"
        ):
            apply_edits(text, [(6, 17, "x")], intervals)
        # Guard level: an edit ending exactly before a grapheme-sensitive
        # mark that the given intervals do not cover is still refused.
        with self.assertRaisesRegex(ValueError, "grapheme"):
            apply_edits("ab\u034fc", [(0, 2, "x")], [Interval(2, 5, "p")])

    def test_apply_edits_still_rejects_protected_overlap(self) -> None:
        text = "Dobro `git status` in besedilo."
        intervals = protected_intervals(text)
        with self.assertRaises(ValueError):
            apply_edits(text, [(9, 15, "x")], intervals)
        with self.assertRaises(ValueError):
            apply_edits(text, [(0, 20, "x")], intervals)
        with self.assertRaises(ValueError):
            apply_edits(text, [(100, 110, "x")], intervals)


class ProxyHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        self.servers: list[HTTPServer] = []
        self.forever_servers: list[HTTPServer] = []
        self.threads: list[threading.Thread] = []

    def tearDown(self) -> None:
        for server in self.forever_servers:
            server.shutdown()
        for thread in self.threads:
            thread.join(5)
        for server in self.servers:
            server.server_close()
        self.temp.cleanup()

    def _start_upstream(self, text: str) -> str:
        delta = (
            '{"type":"response.output_text.delta","item_id":"m","delta":'
            + json.dumps(text)
            + "}"
        )
        completed = (
            '{"type":"response.completed","response":'
            + json.dumps(
                {
                    "object": "response",
                    "id": "r",
                    "status": "completed",
                    "usage": {"total_tokens": 4},
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
                                    "text": text,
                                    "content_index": 0,
                                }
                            ],
                        }
                    ],
                }
            )
            + "}"
        )
        source = (
            "data: " + delta + "\n\n"
        ).encode() + ("data: " + completed + "\n\n").encode()

        class Upstream(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(source)))
                self.end_headers()
                self.wfile.write(source)

            def log_message(self, *_args: object) -> None:
                return

        upstream = HTTPServer(("127.0.0.1", 0), Upstream)
        self.servers.append(upstream)
        self.forever_servers.append(upstream)
        thread = threading.Thread(target=upstream.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)
        return f"http://127.0.0.1:{upstream.server_port}"

    def test_ephemeral_http_round_trip_real_pandoc(self) -> None:
        import proxy

        upstream_url = self._start_upstream("To je presenetliv zapisano.")
        reviewer = _FakeReviewer("tako")
        engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0), upstream_url, engine
        )
        self.servers.append(proxy_server)
        thread = threading.Thread(target=proxy_server.handle_request, daemon=True)
        thread.start()
        self.threads.append(thread)
        client = http.client.HTTPConnection("127.0.0.1", proxy_server.server_port,
                                            timeout=10)
        body = b'{"model":"m","input":"hi","store":false,"stream":true}'
        client.request("POST", "/v1/responses", body=body,
                       headers={"Content-Length": str(len(body))})
        response = client.getresponse()
        result = response.read()
        client.close()
        self.assertEqual(response.status, 200)
        self.assertIn(b"To je tako zapisano.", result)
        self.assertNotIn(b"presenetliv", result)
        self.assertGreaterEqual(reviewer.calls, 1)

    def _start_json_upstream(self, text: str) -> tuple[str, bytes]:
        # Owned finite application/json completed upstream (order 033-a,
        # R10): fakes live only at the external main seam; the proxy,
        # engine, Pandoc, detector, acceptance and patcher stay real.
        envelope = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "output_index": 0,
                    "status": "completed",
                    "content": [
                        {
                            "type": "output_text",
                            "text": text,
                            "content_index": 0,
                        }
                    ],
                }
            ],
        }
        # Deliberately NON-canonical upstream bytes (distinct whitespace and
        # a trailing newline): the no-edit path must return these exact
        # envelope bytes, so a reserialization with canonical separators
        # would not be byte-identical and the preservation assertion is
        # meaningful, not trivially satisfied by matching JSON settings.
        source = (
            json.dumps(envelope, ensure_ascii=False, indent=2) + "\n"
        ).encode()

        class JsonUpstream(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(source)))
                self.end_headers()
                self.wfile.write(source)

            def log_message(self, *_args: object) -> None:
                return

        server = HTTPServer(("127.0.0.1", 0), JsonUpstream)
        self.servers.append(server)
        self.forever_servers.append(server)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)
        return f"http://127.0.0.1:{server.server_port}", source

    def _json_round_trip(
        self, upstream_url: str, engine: object
    ) -> bytes:
        import proxy

        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0), upstream_url, cast(proxy.RepairEngine, engine)
        )
        self.servers.append(proxy_server)
        thread = threading.Thread(target=proxy_server.handle_request, daemon=True)
        thread.start()
        self.threads.append(thread)
        client = http.client.HTTPConnection(
            "127.0.0.1", proxy_server.server_port, timeout=10
        )
        body = b'{"model":"m","input":"hi","store":false,"stream":false}'
        client.request(
            "POST",
            "/v1/responses",
            body=body,
            headers={"Content-Length": str(len(body))},
        )
        response = client.getresponse()
        result = response.read()
        client.close()
        self.assertEqual(response.status, 200)
        return result

    def test_http_json_protected_only_exact_body_zero_calls(self) -> None:
        # Order 033-a, R10: with no eligible target left (the only
        # candidate sits inside a proved BlockQuote), the actual
        # JSON/HTTP path returns the exact original upstream body bytes
        # with zero review calls.
        import proxy

        text = "> To je presenetliv zapisano.\n"
        upstream_url, source = self._start_json_upstream(text)
        reviewer = _ReviewerThatFailsIfCalled()
        engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        result = self._json_round_trip(upstream_url, engine)
        self.assertEqual(result, source)  # exact no-edit envelope bytes
        self.assertEqual(reviewer.calls, 0)

    def test_http_json_repeated_protected_outside_only(self) -> None:
        # Order 033-a, R10: the same token protected (BlockQuote) and
        # ordinary: one bounded review batch and the exact outside-only
        # patch in the JSON envelope.
        import proxy

        text = (
            "> To je presenetliv zapisano.\n"
            "\n"
            "To je presenetliv zapisano.\n"
        )
        upstream_url, _ = self._start_json_upstream(text)
        reviewer = _FakeReviewer("tako")
        engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        result = self._json_round_trip(upstream_url, engine)
        envelope = json.loads(result.decode("utf-8"))
        output = cast("list[object]", envelope["output"])
        message = cast("dict[str, object]", output[0])
        content = cast("list[object]", message["content"])
        returned = cast("dict[str, object]", content[0])["text"]
        self.assertEqual(
            returned,
            "> To je presenetliv zapisano.\n\nTo je tako zapisano.\n",
        )
        self.assertEqual(reviewer.calls, 1)  # one bounded batch

    def test_startup_check_before_bind(self) -> None:
        import proxy

        built: list[bool] = []

        class _ProbeProxy(proxy.ConceptProxy):
            def __init__(self, *args: object, **kwargs: object) -> None:
                built.append(True)
                raise AssertionError("proxy must not be built before pandoc check")

        env = {"CONCEPT_PANDOC": str(self.root / "missing"),
               "CONCEPT_INDEX": str(self.db)}
        with mock.patch.dict(os.environ, env), \
                mock.patch.object(proxy, "ConceptProxy", _ProbeProxy), \
                self.assertRaises(SystemExit) as ctx:
            proxy.main()
        self.assertIn("pandoc startup failure", str(ctx.exception))
        self.assertEqual(built, [])


class NoPulldownProofTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_proxy_path_never_invokes_pulldown_helper(self) -> None:
        import research.curated.prose_boundary as pb

        def _boom(*_args: object, **_kwargs: object) -> object:
            raise AssertionError("historical pulldown helper invoked on proxy path")

        spec = _real_spec()
        text = "To je presenetliv zapisano."
        with mock.patch.object(pb, "_run_helper", _boom), \
                mock.patch.object(pb, "find_helper", _boom), \
                mock.patch.object(pb, "resolve_helper_path", _boom):
            intervals = protected_intervals(text)
            self.assertTrue(isinstance(intervals, list))
            import proxy

            engine = proxy.RepairEngine(
                _build_corpus(self.root),
                _ReviewerThatFailsIfCalled(),
                pandoc=spec,
            )
            self.assertEqual(engine.repair(text), text)


if __name__ == "__main__":
    unittest.main()
