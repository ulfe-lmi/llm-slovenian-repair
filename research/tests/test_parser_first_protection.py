"""008-c focused tests: parser-first structural protection (policy v2).

Covers order requirement 7:

- coordinate mapping (exact round trip; mid-sequence rejection; CRLF;
  decomposed Unicode; emoji/surrogate-pair boundaries);
- protocol parsing (tamper negatives -> fail-closed fallback, not crash);
- policy v2 decisions (autolink destination protected; image incl. alt
  protected; strike/sup/sub content exposed; math/HTML/code/metadata
  protected; link label exposed) - requires the pinned helper;
- residual recognizers per class (positive and negative per class: TeX,
  JSON/config, shell, paths, env vars, identifiers, numbers/units, URLs);
- fail-closed fallback (missing helper; corrupted stream; non-zero exit)
  with byte-identical legacy output and recorded reason;
- determinism;
- end-to-end invariants 1-7 on dev documents with a scripted reviewer
  placed at the HTTP boundary (outside the protection boundary under test,
  per S-EVIDENCE-01);
- planted negatives (a deliberately broken coordinate mapping is caught;
  a fail-open path is impossible by construction and asserted).

Mode-agnostic: with the pinned helper present the parser-first path is
exercised; without it (e.g. CI) the fail-closed legacy fallback is
exercised. Both branches assert the invariants that hold by construction.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "research" / "prose-boundary" / "tools"))

import coordinate as C  # noqa: E402  (frozen 008-a coordinate contract)
import end_to_end_invariants as E2E  # noqa: E402

from research.curated import protected as PRO  # noqa: E402
from research.curated import prose_boundary as PB  # noqa: E402

HELPER = PB.find_helper()
DEV_CORPUS = REPO / "research" / "prose-boundary" / "corpus"
FALLBACK_MODE = HELPER is None
SAMPLE = "Besedilo s številkami 42 in potjo /var/log/x."


def _protected_bytes(text: str) -> set[int]:
    result = PB.protection_with_status(text, helper_path=HELPER)
    prot: set[int] = set()
    for s, e, _r in result.intervals:
        prot.update(range(C.cp_to_byte(text, s), C.cp_to_byte(text, e)))
    return prot


def _bytes_of(text: str, sub: str) -> tuple[int, int]:
    data = text.encode("utf-8")
    start = data.find(sub.encode("utf-8"))
    assert start >= 0, f"{sub!r} not found"
    return start, start + len(sub.encode("utf-8"))


def _all_in(text: str, sub: str, prot: set[int], expected_protected: bool) -> None:
    s, e = _bytes_of(text, sub)
    state = all(i in prot for i in range(s, e))
    assert state == expected_protected, (
        f"{sub!r} expected "
        f"{'protected' if expected_protected else 'exposed'}"
    )


class CoordinateMappingTests(unittest.TestCase):
    def test_round_trip_exact(self):
        text = "ačb\U0001F680e\u0301d"
        data = text.encode("utf-8")
        self.assertEqual(len(data), 12)
        self.assertEqual(len(text), 7)
        for pos in range(len(data) + 1):
            if C.on_code_point_boundary(data, pos):
                cp = C.byte_to_cp(data, pos)
                self.assertIsNotNone(cp, pos)
                self.assertEqual(C.cp_to_byte(text, cp), pos, pos)

    def test_mid_sequence_rejected(self):
        text = "ačb\U0001F680e\u0301d"
        data = text.encode("utf-8")
        non_boundaries = {2, 5, 6, 7, 10}
        for pos in range(len(data) + 1):
            if pos in non_boundaries:
                self.assertFalse(C.on_code_point_boundary(data, pos), pos)
                self.assertIsNone(C.byte_to_cp(data, pos), pos)
                self.assertFalse(C.round_trip(text, pos), pos)

    def test_crlf_boundaries(self):
        text = "x\r\ny"
        data = text.encode("utf-8")
        for pos in range(len(data) + 1):
            self.assertTrue(C.on_code_point_boundary(data, pos), pos)
            self.assertEqual(C.cp_to_byte(text, C.byte_to_cp(data, pos)), pos)

    def test_range_checks(self):
        data = "ačb".encode("utf-8")
        self.assertEqual(C.check_range(data, 1, 3), [])
        self.assertTrue(C.check_range(data, 1, 2))  # bisects the 2-byte char
        self.assertTrue(C.check_range(data, 0, 5))  # out of bounds


class ProtocolTamperTests(unittest.TestCase):
    def _line(self, i: int, kind: str, s: int, e: int) -> bytes:
        return json.dumps(
            {"i": i, "k": kind, "s": s, "e": e}, separators=(",", ":")
        ).encode("utf-8")

    def _protocol(self, *lines: bytes) -> bytes:
        return b"\n".join(list(lines) + [b'{"eof":true}']) + b"\n"

    def _expect_fallback(self, raw: bytes, data: bytes, reason: str) -> None:
        with self.assertRaises(PB.ProtectionFallback) as ctx:
            PB.parse_protocol(raw, data)
        self.assertEqual(str(ctx.exception), reason)

    def test_valid_protocol_parses(self):
        raw = self._protocol(
            self._line(0, "S.Para", 0, 2),
            self._line(1, "Text", 0, 2),
            self._line(2, "E.Para", 0, 2),
        )
        events = PB.parse_protocol(raw, b"ab")
        self.assertEqual(events, [("S.Para", 0, 2), ("Text", 0, 2), ("E.Para", 0, 2)])

    def test_bisection_caught(self):
        data = "č".encode("utf-8")
        raw = self._protocol(self._line(0, "Text", 0, 1))
        self._expect_fallback(raw, data, "coordinate-bisection")

    def test_out_of_order_caught(self):
        raw = self._protocol(self._line(1, "Text", 0, 1), self._line(0, "Text", 0, 1))
        self._expect_fallback(raw, b"ab", "protocol-out-of-order")
        raw = self._protocol(self._line(0, "Text", 0, 1), self._line(2, "Text", 0, 1))
        self._expect_fallback(raw, b"ab", "protocol-out-of-order")

    def test_truncation_caught(self):
        raw = self._line(0, "S.Para", 0, 2) + b"\n" + self._line(1, "Text", 0, 2) + b"\n"
        self._expect_fallback(raw, b"ab", "protocol-truncated")

    def test_early_eof_caught(self):
        raw = (
            self._line(0, "S.Para", 0, 2)
            + b"\n" + b'{"eof":true}\n'
            + self._line(1, "Text", 0, 2) + b"\n"
        )
        self._expect_fallback(raw, b"ab", "protocol-early-eof")

    def test_unbalanced_caught(self):
        raw = self._protocol(self._line(0, "S.Para", 0, 2), self._line(1, "Text", 0, 2))
        self._expect_fallback(raw, b"ab", "protocol-unbalanced")

    def test_wrong_end_family_caught(self):
        raw = self._protocol(
            self._line(0, "S.Para", 0, 2),
            self._line(1, "Text", 0, 2),
            self._line(2, "E.Head", 0, 2),
        )
        self._expect_fallback(raw, b"ab", "protocol-unbalanced")

    def test_not_utf8_caught(self):
        self._expect_fallback(b"\xff\xfe", b"ab", "protocol-not-utf8")

    def test_malformed_caught(self):
        self._expect_fallback(b"not json\n", b"ab", "protocol-malformed")
        raw = (json.dumps({"i": 0, "k": "Text", "s": 0}) + "\n").encode("utf-8")
        self._expect_fallback(raw, b"ab", "protocol-malformed")

    def test_out_of_bounds_caught(self):
        raw = self._protocol(self._line(0, "Text", 0, 3))
        self._expect_fallback(raw, b"ab", "coordinate-out-of-bounds")
        raw = self._protocol(self._line(0, "Text", 1, 0))
        self._expect_fallback(raw, b"ab", "coordinate-out-of-bounds")


@unittest.skipUnless(HELPER is not None, "pinned helper unavailable (fallback mode)")
class PolicyV2Tests(unittest.TestCase):
    def test_autolink_destination_protected(self):
        text = "Poglej <https://primer.si/a> zdaj."
        prot = _protected_bytes(text)
        _all_in(text, "https://primer.si/a", prot, True)
        _all_in(text, "Poglej", prot, False)
        _all_in(text, "zdaj", prot, False)

    def test_image_including_alt_protected(self):
        text = "Glej ![alt besedilo](https://primer.si/x.png) konec."
        prot = _protected_bytes(text)
        _all_in(text, "![alt besedilo](https://primer.si/x.png)", prot, True)
        _all_in(text, "Glej", prot, False)
        _all_in(text, "konec", prot, False)

    def test_strike_sup_sub_content_exposed(self):
        # P2 parses ~~strike~~ as S.Strike (a prose container); sup/sub are
        # not parser structures in this profile, so their content is plain
        # prose. All three remain EXPOSED per the frozen policy decision.
        text = "Vrednost a^x^ in x~y~ in ~~prekrsano~~ konec."
        prot = _protected_bytes(text)
        result = PB.protection_with_status(text, helper_path=HELPER)
        self.assertEqual(result.mode, "parser-first")
        _all_in(text, "x~y~", prot, False)
        _all_in(text, "prekrsano", prot, False)
        _all_in(text, "Vrednost", prot, False)

    def test_math_html_code_metadata_protected(self):
        text = (
            "---\ntitle: Naslov\n---\n\n"
            "Matematika $x^2$ tu.\n\n"
            "<div>\nsamo html\n</div>\n\n"
            "Konec.\n\n"
            "```py\nc = 1\n```\n"
        )
        prot = _protected_bytes(text)
        _all_in(text, "title: Naslov", prot, True)
        _all_in(text, "$x^2$", prot, True)
        _all_in(text, "<div>\nsamo html\n</div>", prot, True)
        _all_in(text, "```py\nc = 1\n```", prot, True)
        _all_in(text, "Matematika", prot, False)
        _all_in(text, "Konec", prot, False)

    def test_link_label_exposed_destination_protected(self):
        text = "Glej [oznaka](https://primer.si) konec."
        prot = _protected_bytes(text)
        _all_in(text, "oznaka", prot, False)
        _all_in(text, "https://primer.si", prot, True)
        _all_in(text, "Glej", prot, False)


class ResidualRecognizerTests(unittest.TestCase):
    def _classes(self, text: str) -> set[str]:
        return {c for c, _s, _e in PB.residual_spans(text)}

    def _spans_of(self, text: str, cls: str) -> list[tuple[int, int]]:
        return [(s, e) for c, s, e in PB.residual_spans(text) if c == cls]

    def test_tex_positive_and_negative(self):
        self.assertIn("tex-paren", self._classes("\\((a^2+b^2\\)"))
        self.assertIn("tex-bracket", self._classes("\\[E=mc^2\\]"))
        self.assertIn("tex-env", self._classes("\\begin{align}x&=1\\end{align}"))
        self.assertNotIn("tex-paren", self._classes("brez tex delov"))
        self.assertNotIn("tex-bracket", self._classes("brez tex delov"))
        self.assertNotIn("tex-env", self._classes("brez tex delov"))

    def test_json_config_positive_and_negative(self):
        spans = self._spans_of('{"kljuc": 1, "seznam": [1, 2]}', "bare-json")
        self.assertTrue(spans and spans[0][0] == 0)
        self.assertIn("bare-json", self._classes("[1, 2]"))
        self.assertIn("config", self._classes("a=1\nb=2"))
        self.assertNotIn("bare-json", self._classes("samo ena vrstica"))
        self.assertNotIn("config", self._classes("samo ena vrstica"))

    def test_shell_positive_and_negative(self):
        self.assertIn("shell", self._classes("$ ls -la"))
        self.assertIn("shell", self._classes("python3 main.py"))
        flag = self._spans_of("nastavite --verbose izvoz", "shell")
        self.assertTrue(any("izvoz" in "nastavite --verbose izvoz"[s:e] for s, e in flag))
        self.assertNotIn("shell", self._classes("brez ukazov"))

    def test_paths_positive_and_negative(self):
        spans = self._spans_of("/var/log/sistem.log", "path")
        self.assertTrue(spans and spans[0][0] == 0)
        self.assertIn("path", self._classes("C:\\Users\\up\\desktop"))
        self.assertIn("relative-path", self._classes("relativna/putanjo/t.txt"))
        self.assertNotIn("path", self._classes("nobenih poti tukaj"))
        self.assertNotIn("relative-path", self._classes("nobenih poti tukaj"))

    def test_env_var_positive_and_negative(self):
        self.assertIn("env-var", self._classes("${HOME}"))
        self.assertIn("env-var", self._classes("glej $PATH zdaj"))
        self.assertNotIn("env-var", self._classes("glej $x zdaj"))
        self.assertNotIn("env-var", self._classes("brez spremenljivk"))

    def test_identifier_positive_and_negative(self):
        self.assertIn("identifier", self._classes("ime_spremenljivke"))
        self.assertIn("identifier", self._classes("vrednost123"))
        self.assertNotIn("identifier", self._classes("samo"))

    def test_upper_identifier_positive_and_negative(self):
        self.assertIn("upper-identifier", self._classes("VREDNOST"))
        self.assertNotIn("upper-identifier", self._classes("V"))

    def test_number_positive_and_negative(self):
        spans = self._spans_of("cena 5 $", "number")
        self.assertIn((5, 6), spans)
        self.assertIn("number", self._classes("87,3 %"))
        self.assertIn("number", self._classes("3,14 pi"))
        self.assertNotIn("number", self._classes("bistvo"))

    def test_url_positive_and_negative(self):
        self.assertIn("url", self._classes("glej https://primer.si/a zdaj"))
        self.assertNotIn("url", self._classes("brez naslovov"))

    def test_no_markdown_delimiter_matching(self):
        # The residual layer must not match Markdown structure: emphasis,
        # inline-code markers and bare heading/list/quote content carry no
        # residual spans (delimiters are structural bytes, never candidate
        # prose).
        self.assertEqual(PB.residual_spans("**poudarek** in *naklon* in `kod`"), [])
        self.assertEqual(PB.residual_spans("prvi odstavek\n\ndrugi odstavek\n"), [])


class FailClosedFallbackTests(unittest.TestCase):
    def test_missing_helper_falls_back(self):
        result = PB.protection_with_status(SAMPLE, helper_path="/nonexistent/nope")
        self.assertEqual(result.mode, "legacy-fallback")
        self.assertEqual(result.fallback_reason, "helper-unavailable")
        self.assertEqual(result.intervals, tuple(PB.legacy_protected_intervals(SAMPLE)))

    def test_identity_mismatch_falls_back(self):
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "helper"
            bad.write_bytes(b"definitely not the pinned helper")
            result = PB.protection_with_status(SAMPLE, helper_path=bad)
        self.assertEqual(result.mode, "legacy-fallback")
        self.assertEqual(result.fallback_reason, "helper-identity-mismatch")
        self.assertEqual(result.intervals, tuple(PB.legacy_protected_intervals(SAMPLE)))

    @unittest.skipUnless(HELPER is not None, "pinned helper unavailable")
    def test_corrupted_stream_falls_back(self):
        for payload, reason, data_text in (
            (b"\x00\xff\xfe", "protocol-not-utf8", SAMPLE),
            (b"not json\n", "protocol-malformed", SAMPLE),
            (b'{"i":0,"k":"Text","s":0,"e":1}\n{"eof":true}\n',
             "coordinate-bisection", "\u010drka"),
        ):
            with mock.patch.object(PB, "_run_helper", return_value=payload):
                result = PB.protection_with_status(data_text, helper_path=HELPER)
            self.assertEqual(result.mode, "legacy-fallback", payload)
            self.assertEqual(result.fallback_reason, reason, payload)
            self.assertEqual(
                result.intervals,
                tuple(PB.legacy_protected_intervals(data_text)),
            )

    @unittest.skipUnless(HELPER is not None, "pinned helper unavailable")
    def test_nonzero_exit_falls_back(self):
        with mock.patch.object(
            PB, "_run_helper", side_effect=PB.ProtectionFallback("helper-exit-7")
        ):
            result = PB.protection_with_status(SAMPLE, helper_path=HELPER)
        self.assertEqual(result.mode, "legacy-fallback")
        self.assertEqual(result.fallback_reason, "helper-exit-7")
        self.assertEqual(result.intervals, tuple(PB.legacy_protected_intervals(SAMPLE)))

    def test_byte_identical_legacy_output_url(self):
        text = "Glej https://primer.si/a."
        result = PB.protection_with_status(text, helper_path="/nonexistent/nope")
        self.assertEqual(result.intervals, ((5, 25, "url+path+relative-path"),))

    def test_byte_identical_legacy_output_path(self):
        text = "pot /var/log/x."
        result = PB.protection_with_status(text, helper_path="/nonexistent/nope")
        self.assertEqual(result.intervals, ((4, 15, "path+relative-path"),))

    def test_byte_identical_legacy_output_fence(self):
        text = "A\n```py\nc1\n```\nB"
        result = PB.protection_with_status(text, helper_path="/nonexistent/nope")
        self.assertEqual(result.intervals, ((1, 14, "fenced-code+identifier"),))

    def test_tool_arguments_protected_in_fallback(self):
        text = "abc def"
        result = PB.protection_with_status(
            text, tool_arguments=("def",), helper_path="/nonexistent/nope"
        )
        self.assertIn((4, 7, "tool-argument"), result.intervals)

    def test_fallback_reason_is_a_stable_token(self):
        result = PB.protection_with_status(SAMPLE, helper_path="/nonexistent/nope")
        self.assertRegex(result.fallback_reason or "", r"^[a-z][a-z0-9-]*$")


class DeterminismTests(unittest.TestCase):
    def test_protection_deterministic(self):
        first = PB.protection_with_status(SAMPLE, helper_path=HELPER)
        second = PB.protection_with_status(SAMPLE, helper_path=HELPER)
        self.assertEqual(first.mode, second.mode)
        self.assertEqual(first.fallback_reason, second.fallback_reason)
        self.assertEqual(first.intervals, second.intervals)

    def test_legacy_deterministic(self):
        self.assertEqual(
            PB.legacy_protected_intervals(SAMPLE),
            PB.legacy_protected_intervals(SAMPLE),
        )

    def test_coordinate_mapping_pure(self):
        text = "ačb\U0001F680"
        data = text.encode("utf-8")
        self.assertEqual(
            [C.byte_to_cp(data, p) for p in range(len(data) + 1)],
            [C.byte_to_cp(data, p) for p in range(len(data) + 1)],
        )


class PublicApiTests(unittest.TestCase):
    def test_public_names_and_signatures(self):
        self.assertTrue(hasattr(PRO, "Interval"))
        self.assertTrue(hasattr(PRO, "is_protected"))
        self.assertTrue(hasattr(PRO, "protected_intervals"))
        intervals = PRO.protected_intervals("glej\n```\nkoda\n```\nkonca")
        self.assertTrue(all(isinstance(iv, PRO.Interval) for iv in intervals))
        starts = [iv.start for iv in intervals]
        self.assertEqual(starts, sorted(starts))
        for left, right in zip(intervals, intervals[1:]):
            self.assertLessEqual(left.end, right.start)
        self.assertTrue(PRO.is_protected(intervals[0].start + 1, intervals[0].end, intervals))
        self.assertFalse(PRO.is_protected(0, 1, []))

    def test_protection_result_diagnostics(self):
        result = PRO.protection_result(SAMPLE)
        self.assertIn(result.mode, ("parser-first", "legacy-fallback"))
        if result.mode == "parser-first":
            self.assertIsNone(result.fallback_reason)
        else:
            self.assertIsInstance(result.fallback_reason, str)

    def test_consumers_import_clean(self):
        for name in (
            "research.curated.pipeline",
            "research.curated.detector",
            "research.curated.patching",
            "research.curated.gating",
            "research.curated.historical_detector",
            "research.curated.historical_variants",
            "research.tools.run_one_substitution",
        ):
            __import__(name)


@unittest.skipUnless(
    (DEV_CORPUS / "documents-dev").is_dir(), "committed dev corpus unavailable"
)
class EndToEndInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._scratch = Path(tempfile.mkdtemp(prefix="008c-e2e-test-"))

    @classmethod
    def tearDownClass(cls):
        import shutil

        shutil.rmtree(cls._scratch, ignore_errors=True)

    def test_invariants_1_to_7_on_dev_documents(self):
        report = E2E.run_invariants(
            DEV_CORPUS,
            HELPER,
            replay_count=8,
            seed_count=2,
            corpus_docs=200,
            full_zero_check=False,
            scratch=self._scratch,
        )
        self.assertIn(report["protection_mode"], ("parser-first", "legacy-fallback"))
        self.assertTrue(report["seeded"], "seeded adjacency required")
        for invariant, ok in report["invariants"].items():
            self.assertTrue(ok, invariant)
        self.assertTrue(report["synthetic_zero_eligible"]["ok"])
        self.assertTrue(report["all_pass"])
        for row in report["seeded"]:
            self.assertTrue(row["edit_applied"], row)


class PlantedNegativeTests(unittest.TestCase):
    @unittest.skipUnless(HELPER is not None, "pinned helper unavailable")
    def test_broken_coordinate_mapping_caught(self):
        with mock.patch.object(PB, "byte_to_cp", return_value=None):
            result = PB.protection_with_status("Besedilo z črkami.", helper_path=HELPER)
        self.assertEqual(result.mode, "legacy-fallback")
        self.assertEqual(result.fallback_reason, "coordinate-bisection")
        self.assertEqual(
            result.intervals,
            tuple(PB.legacy_protected_intervals("Besedilo z črkami.")),
        )

    def test_fail_open_impossible(self):
        # Every failure injection must yield the full legacy 008-a
        # protection (never empty, never weaker): the layer has no
        # fail-open path by construction.
        cases: list[tuple[str, PB.ProtectionResult]] = []
        cases.append(
            ("missing-helper", PB.protection_with_status(SAMPLE, helper_path="/nonexistent/nope"))
        )
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "helper"
            bad.write_bytes(b"nope")
            cases.append(("identity-mismatch", PB.protection_with_status(SAMPLE, helper_path=bad)))
        if HELPER is not None:
            with mock.patch.object(PB, "_run_helper", return_value=b"garbage\n"):
                cases.append(
                    ("corrupted-stream", PB.protection_with_status(SAMPLE, helper_path=HELPER))
                )
            with mock.patch.object(PB, "byte_to_cp", return_value=None):
                cases.append(
                    ("broken-mapping", PB.protection_with_status(SAMPLE, helper_path=HELPER))
                )
        for name, result in cases:
            with self.subTest(name=name):
                self.assertEqual(result.mode, "legacy-fallback")
                self.assertEqual(
                    result.intervals, tuple(PB.legacy_protected_intervals(SAMPLE))
                )
                self.assertNotEqual(result.intervals, ())

    @unittest.skipUnless(HELPER is not None, "pinned helper unavailable")
    def test_parser_first_still_protects_structural_content(self):
        text = "glej ```koda```\nkonca"
        result = PB.protection_with_status(text, helper_path=HELPER)
        self.assertEqual(result.mode, "parser-first")
        self.assertNotEqual(result.intervals, ())


if __name__ == "__main__":
    unittest.main()
