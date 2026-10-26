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
from batch_review import BatchProposal, BatchTarget  # noqa: E402
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

    # -- trap negatives ----------------------------------------------------

    def test_nfd_line_abstain(self) -> None:
        text = "ka\u017ef + e\u0301: " + "e\u0301"
        granted, protected = self._protect(text)
        self.assertEqual(granted, ())
        self.assertEqual(protected[0].start, 0)
        self.assertEqual(protected[-1].end, len(text))

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
        pandoc_protection._walk_blocks(doc, cast("list[object]", document["blocks"]))
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
        pandoc_protection._walk_blocks(doc, cast("list[object]", document["blocks"]))
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
            ('je tako',20),('tako zapisano',20),('je presenetljiv',20),('je zapisano',20);
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
    ) -> dict[str, BatchProposal]:
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
    ) -> dict[str, BatchProposal]:
        self.calls += 1
        return {
            target.id: BatchProposal(
                target.id, False, self.replacement, False
            )
            for target in targets
        }


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
                pass

            def __enter__(self) -> _SentinelCorpus:
                opened.append(True)
                return self

            def __exit__(self, *_: object) -> None:
                return None

        engine.begin_request()
        text = "To je presenetliv zapisano."
        with mock.patch.object(self.proxy_module, "Corpus", _SentinelCorpus):
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
                pass

            def __enter__(self) -> _SentinelCorpus:
                opened.append(True)
                return self

            def __exit__(self, *_: object) -> None:
                return None

        document_calls: list[bool] = []

        def _sentinel_document(text: str) -> object:
            document_calls.append(True)
            raise AssertionError("mapper must not be built for oversized input")

        limit = config.PANDOC_MAX_INPUT_BYTES
        oversize = "a" * (limit + 1)
        engine.begin_request()
        with mock.patch.object(
            pandoc_protection, "_Document", _sentinel_document
        ), mock.patch.object(self.proxy_module, "Corpus", _SentinelCorpus):
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
                    def __init__(self, *args: object, **kw: object) -> None:
                        pass

                    def __enter__(self, _opened: list[bool] = opened) -> _SentinelCorpus:
                        _opened.append(True)
                        return self

                    def __exit__(self, *_: object) -> None:
                        return None

                engine.begin_request()
                with mock.patch.object(self.proxy_module, "Corpus", _SentinelCorpus):
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
                    "id": "r",
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
        client.request("POST", "/v1/responses", body=b"{}",
                       headers={"Content-Length": "2"})
        response = client.getresponse()
        result = response.read()
        client.close()
        self.assertEqual(response.status, 200)
        self.assertIn(b"To je tako zapisano.", result)
        self.assertNotIn(b"presenetliv", result)
        self.assertGreaterEqual(reviewer.calls, 1)

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
