"""008-h focused tests: composition-contract fix and dialect-edge protection.

Covers order 008-h scope items 3-5 (additive file; no existing test file is
modified):

- the single predeclared xml-fragment trigger decision EXTEND (scope item 4):
  the trigger name pattern is widened from ASCII letters to Unicode letters
  with the same shape guards (letter/underscore then letters/digits/hyphens
  plus the existing dot/colon/underscore extensions, same-line closing or
  self-closing or attribute space, never on comparison operators, never on
  an opening bracket followed by digits, never on a lone bracket);
  recognized ASCII dialect names still abstain (v2 parity);
- the builder composition contract (scope item 3b): R1 (a fenced or indented
  code component is never composed on the line immediately after an HTML
  closing-tag line; the inserted blank line is template-owned NEUTRAL and
  recorded in the composition provenance), R2 (structured-keyvalue
  components with list-item-style lines carrying paired emphasis or quoted
  emphasis-like content are not admitted to the v3 pool), R3 (structured-xml
  components with non-ASCII tag letters are not admitted under FALLBACK),
  the label_source split (construction vs oracle-refined) on every labeled
  region, and the no-parser-participation assertion;
- pipeline behaviour with the pinned helper: the exact v2 residual shapes
  (html-closing-tag-adjacent-fence without the separator: the code lines
  after an internal blank line are exposed; with the separator: the fence is
  a genuine code block; keyvalue-list-item-quoted-emphasis: quote plus word
  exposed), the yaml-hash-comment-heading shape (comment text exposed, hash
  marker structural, the no-space negative stays plain prose), and the
  xml-diacritic-tag-name shapes (protected under EXTEND);
- the committed visible dev dialect-edge batch
  (corpus/defect-dev-008h/) is re-validated fail-closed: every PROTECTED
  region fully covered and every POLICY_EXPOSED region fully exposed by the
  live implementation, and the committed census key matches the files.

Mode handling: the recognizer-level and builder-level tests are pure
functions and run everywhere; the pipeline-level tests require the pinned
helper (parser-first path) and are skipped with a recorded reason when it
is unavailable.
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "research" / "prose-boundary" / "tools"))

import prose_boundary_builder as B  # noqa: E402
from research.curated import prose_boundary as PB  # noqa: E402

HELPER = PB.find_helper()
NEEDS_HELPER = HELPER is not None


def _protected_bytes(text: str) -> set[int]:
    result = PB.protection_with_status(text, helper_path=HELPER)
    assert result.mode == "parser-first", result.fallback_reason
    prot: set[int] = set()
    for s, e, _r in result.intervals:
        prot.update(range(PB.cp_to_byte(text, s), PB.cp_to_byte(text, e)))
    return prot


def _fully_protected(text: str, sub: str) -> bool:
    prot = _protected_bytes(text)
    start = len(text[:text.index(sub)].encode("utf-8"))
    end = start + len(sub.encode("utf-8"))
    return all(b in prot for b in range(start, end))


def _fully_exposed(text: str, sub: str) -> bool:
    prot = _protected_bytes(text)
    start = len(text[:text.index(sub)].encode("utf-8"))
    end = start + len(sub.encode("utf-8"))
    return all(b not in prot for b in range(start, end))


# ---------------------------------------------------------------------------
# scope item 4: the EXTEND trigger decision (recognizer level)
# ---------------------------------------------------------------------------
class TestExtendTrigger(unittest.TestCase):
    def test_pattern_is_unicode_widening_with_same_guards(self):
        self.assertEqual(PB.RE_XML_NAME, r"(?!\d)\w[\w.:-]*")

    def test_dialect_pattern_unchanged_ascii(self):
        self.assertEqual(
            PB.RE_XML_DIALECT_NAME.pattern, r"[A-Za-z][A-Za-z0-9-]*")

    def test_diacritic_names_trigger(self):
        for name in ("šumnik", "črtica", "žrno", "šumnik-projekt"):
            self.assertTrue(PB._xml_name_triggers(name), name)

    def test_recognized_ascii_names_still_abstain(self):
        for name in ("div", "stevec", "projekt"):
            self.assertFalse(PB._xml_name_triggers(name), name)

    def test_namespaced_and_period_underscore_still_trigger(self):
        for name in ("xsl:stylesheet", "foo.bar", "a_b", "xsl:žrno"):
            self.assertTrue(PB._xml_name_triggers(name), name)

    def test_paired_diacritic_fragment_protected_in_full(self):
        spans = PB._xml_fragment_spans(
            "in <šumnik beseda>notranjost</šumnik beseda> tam")
        text = "in <šumnik beseda>notranjost</šumnik beseda> tam"
        self.assertEqual(spans, [(3, 44)])
        self.assertEqual(text[3:44],
                         "<šumnik beseda>notranjost</šumnik beseda>")

    def test_self_closing_diacritic(self):
        self.assertEqual(PB._xml_fragment_spans('<črtica x="1"/>'), [(0, 15)])

    def test_unbalanced_diacritic_to_end_of_line(self):
        self.assertEqual(
            PB._xml_fragment_spans("in <žrno a> preostanek"), [(3, 22)])

    def test_standalone_closing_diacritic(self):
        self.assertEqual(PB._xml_fragment_spans("in </šumnik> tam"), [(3, 12)])

    def test_multiline_paired_diacritic(self):
        text = "Naredi <žrno a>\nvsebina bloka\n</žrno a> konec"
        self.assertEqual(PB._xml_fragment_spans(text), [(7, 39)])

    def test_comparison_operator_does_not_fire(self):
        self.assertEqual(PB._xml_fragment_spans("x < 5"), [])
        self.assertEqual(
            PB._xml_fragment_spans("Vrednost < 10 je majhna."), [])

    def test_digit_after_bracket_does_not_fire(self):
        self.assertEqual(PB._xml_fragment_spans("Kolicina <5 je majhna."),
                         [])

    def test_space_after_bracket_does_not_fire(self):
        self.assertEqual(PB._xml_fragment_spans("< črtica"), [])

    def test_lone_bracket_does_not_fire(self):
        self.assertEqual(PB._xml_fragment_spans("Glej levo < stran."), [])

    def test_diacritic_without_closing_bracket_does_not_fire(self):
        self.assertEqual(PB._xml_fragment_spans("Glej <črtica tukaj."), [])

    def test_recognized_html_unchanged(self):
        self.assertEqual(
            PB._xml_fragment_spans('in <div class="a">vsebina</div> tam'), [])
        self.assertEqual(PB._xml_fragment_spans("<stevec>42</stevec>"), [])


# ---------------------------------------------------------------------------
# scope item 3b: builder composition contract
# ---------------------------------------------------------------------------
def _segs(html_frag: str, sep: str, code_frag: str):
    return [
        ("prose line\n", "comp-a", "PROSE", B.CONSTRUCTION),
        ("\n", "template", "NEUTRAL", B.CONSTRUCTION),
        (html_frag, "comp-html", "PROTECTED", B.CONSTRUCTION),
        (sep, "template", "NEUTRAL", B.CONSTRUCTION),
        (code_frag, "comp-code", "PROTECTED", B.CONSTRUCTION),
    ]


class TestBuilderCompositionContract(unittest.TestCase):
    def test_r1_fires_on_exact_v2_adjacency(self):
        out, n = B.apply_r1(_segs("</div>", "\n", "```\nx\n```\n"))
        self.assertEqual(n, 1)
        self.assertEqual(out[4], ("\n", "template", "NEUTRAL",
                                  B.CONSTRUCTION))
        self.assertIn("</div>\n\n```\nx\n```\n",
                      "".join(s[0] for s in out))

    def test_r1_indented_code_variant(self):
        _out, n = B.apply_r1(_segs("</p>", "\n", "    code line\n"))
        self.assertEqual(n, 1)

    def test_r1_not_when_already_separated(self):
        for segs in (_segs("</div>\n", "\n", "```\nx\n```\n"),
                     _segs("</div>", "\n\n", "```\nx\n```\n")):
            _out, n = B.apply_r1(segs)
            self.assertEqual(n, 0)

    def test_r1_not_on_non_closing_tag(self):
        _out, n = B.apply_r1(_segs("<div>", "\n", "```\nx\n```\n"))
        self.assertEqual(n, 0)

    def test_r1_not_when_next_is_prose(self):
        _out, n = B.apply_r1(_segs("</div>", "\n", "prose\n"))
        self.assertEqual(n, 0)

    def test_r2_predicate_excludes_list_item_emphasis(self):
        self.assertTrue(B.r2_keyvalue_list_item_emphasis_excluded(
            'naloge:\n  - **"kratek"** seznam'))
        self.assertTrue(B.r2_keyvalue_list_item_emphasis_excluded(
            'naloge:\n  - *"kratek"* seznam'))
        self.assertTrue(B.r2_keyvalue_list_item_emphasis_excluded(
            "- **poudarek** tu"))
        self.assertFalse(B.r2_keyvalue_list_item_emphasis_excluded(
            "stevec: 42\nnaziv: Besedilo"))
        self.assertFalse(B.r2_keyvalue_list_item_emphasis_excluded(
            "kljuc: vrednost\n- navaden stik"))

    def test_r3_predicate_excludes_diacritic_tags(self):
        self.assertTrue(B.r3_xml_diacritic_tag_excluded("<šumnik>t</šumnik>"))
        self.assertTrue(B.r3_xml_diacritic_tag_excluded('<črtica x="1"/>'))
        self.assertFalse(B.r3_xml_diacritic_tag_excluded(
            "<stevec>42</stevec>"))
        self.assertFalse(B.r3_xml_diacritic_tag_excluded(
            "<div class=\"a\">x</div>"))

    def test_no_parser_participation_assertion(self):
        B.assert_no_parser_participation()

    def test_label_source_on_segment_labelers(self):
        self.assertEqual(B.label_prose("besedilo", "c1"),
                         [("besedilo", "c1", "PROSE", B.CONSTRUCTION)])
        segs = B.label_code_block("x = 1", "c1")
        self.assertEqual(segs[2][3], B.CONSTRUCTION)
        segs = B.generic_label("navadno besedilo", "c1")
        self.assertTrue(segs)
        for _t, _cid, _role, lsrc in segs:
            self.assertIn(lsrc, (B.CONSTRUCTION, B.ORACLE_REFINED))

    def test_compose_returns_r1_count_and_label_source(self):
        pool = {
            "prose-science": [
                {"component_id": "p1", "family": "prose-science",
                 "fragment": "Vrstica o rasti.\n", "category": "prose"},
                {"component_id": "p2", "family": "prose-science",
                 "fragment": "Vrstica o merjenju.\n", "category": "prose"},
            ],
            "prose": [],
            "code": [
                {"component_id": "c1", "family": "code-c",
                 "fragment": "x = 1\n", "category": "code"},
                {"component_id": "c2", "family": "code-c",
                 "fragment": "y = 2\n", "category": "code"},
            ],
            "machine": [
                {"component_id": "m1", "family": "machine-filenames",
                 "fragment": "/abs/path/x.log", "category": "machine"},
                {"component_id": "m2", "family": "machine-filenames",
                 "fragment": "/abs/path/y.log", "category": "machine"},
            ],
        }
        index = {c["component_id"]: c
                 for fam in pool.values() for c in fam}
        rng = random.Random(1234)
        segs, r1_count = B.compose(rng, pool, "T3-prose-fenced-prose", set())
        self.assertIsInstance(r1_count, int)
        for text, _cid, _role, lsrc in segs:
            self.assertIn(lsrc, (B.CONSTRUCTION, B.ORACLE_REFINED))
        # determinism with the same seed
        rng2 = random.Random(1234)
        segs2, r1_count2 = B.compose(rng2, pool, "T3-prose-fenced-prose",
                                     set())
        self.assertEqual(segs, segs2)
        self.assertEqual(r1_count, r1_count2)

    def test_finalize_document_records_r1_provenance(self):
        segs, r1_count = B.apply_r1(_segs("</div>", "\n", "```\nx\n```\n"))
        doc = B.assemble(segs, {}, "T10-randomized")
        document, _label = B.finalize_document(doc, "test-000001", "ab" * 8,
                                               "T10-randomized", r1_count)
        self.assertEqual(
            document["composition_provenance"]["r1_blank_line_insertions"],
            r1_count)
        for region in _label["regions"]:
            self.assertIn(region["label_source"],
                          (B.CONSTRUCTION, B.ORACLE_REFINED))


# ---------------------------------------------------------------------------
# scope items 4-5: pipeline behaviour with the pinned helper
# ---------------------------------------------------------------------------
@unittest.skipUnless(NEEDS_HELPER, "pinned helper unavailable")
class TestDialectEdgePipeline(unittest.TestCase):
    # --- 35 B shape: html-closing-tag-adjacent-fence -----------------------
    def test_35b_shape_without_separator_exposes_code_after_blank(self):
        text = "Pred tem.\n</div>\n```\nline en\n\nline dva\n```\nZa tem.\n"
        prot = _protected_bytes(text)

        def covered(sub: str) -> bool:
            s = len(text[:text.index(sub)].encode("utf-8"))
            e = s + len(sub.encode("utf-8"))
            return all(b in prot for b in range(s, e))

        self.assertTrue(covered("\n</div>\n```\nline en\n\n"))
        self.assertTrue(covered("\n```\nZa tem."))
        s = len(text[:text.index("line dva")].encode("utf-8"))
        e = s + len("line dva".encode("utf-8"))
        self.assertFalse(all(b in prot for b in range(s, e)))

    def test_35b_shape_with_separator_fully_protected(self):
        text = "Pred tem.\n</div>\n\n```\nline en\nline dva\n```\nZa tem.\n"
        self.assertTrue(_fully_protected(text, "line dva"))
        self.assertTrue(_fully_protected(text, "```"))

    def test_indented_code_with_separator_fully_protected(self):
        text = "Pred tem.\n</p>\n\n    koda ena\n    koda dva\nZa tem.\n"
        self.assertTrue(_fully_protected(text, "koda dva"))

    # --- 16 B shape: keyvalue-list-item-quoted-emphasis --------------------
    def test_16b_shape_quotes_and_word_exposed(self):
        text = ('V nastopu so navedene naloge.\nnaloge:\n'
                '  - **"kratek"** seznam\nZaključek sledi.\n')
        self.assertTrue(_fully_exposed(text, '"kratek"'))
        self.assertTrue(_fully_exposed(text, "naloge:"))
        self.assertTrue(_fully_protected(text, "\n  - **"))
        self.assertTrue(_fully_protected(text, "**"))

    def test_16b_shape_emphasis_variant(self):
        text = ('V nastopu so navedene naloge.\nnaloge:\n'
                '  - *"kratek"* seznam\nZaključek sledi.\n')
        self.assertTrue(_fully_exposed(text, '"kratek"'))

    # --- yaml-hash-comment-heading ------------------------------------------
    def test_yaml_hash_comment_text_exposed_marker_protected(self):
        text = ("Pred tem.\n\nstevec: 42\nnaziv: Testna\n# komentar\n"
                "pot: /abs/path/x.log\n\nZa tem.\n")
        self.assertTrue(_fully_exposed(text, "komentar"))
        self.assertTrue(_fully_protected(text, "# "))
        self.assertTrue(_fully_protected(text, "stevec: 42"))
        self.assertTrue(_fully_protected(text, "pot: /abs/path/x.log"))

    def test_yaml_hash_no_space_is_plain_prose(self):
        text = ("Pred tem.\n\nstevec: 42\n#komentar\n"
                "pot: /abs/path/x.log\n\nZa tem.\n")
        self.assertTrue(_fully_exposed(text, "#komentar"))

    # --- xml-diacritic-tag-name (EXTEND -> protected) -----------------------
    def test_xml_diacritic_paired_protected(self):
        text = "V dokumentu je <šumnik beseda>vsebina</šumnik beseda> tam."
        self.assertTrue(_fully_protected(text, "vsebina"))
        self.assertTrue(_fully_protected(text, "<šumnik beseda>"))
        self.assertTrue(_fully_protected(text, "</šumnik beseda>"))

    def test_xml_diacritic_self_closing_protected(self):
        text = 'Uporabimo <črtica x="1"/> v besedilu.'
        self.assertTrue(_fully_protected(text, '<črtica x="1"/>'))

    def test_xml_diacritic_unbalanced_to_end_of_line(self):
        text = "Začetek je <žrno a> in preostanek vrstice."
        self.assertTrue(
            _fully_protected(text, "<žrno a> in preostanek vrstice."))

    def test_xml_diacritic_standalone_close_protected(self):
        text = "Vsebina in </šumnik> na koncu."
        self.assertTrue(_fully_protected(text, "</šumnik>"))

    # --- negative controls ---------------------------------------------------
    def test_diacritic_bracket_without_close_stays_prose(self):
        text = "Glej <črtica tukaj."
        self.assertTrue(_fully_exposed(text, "<črtica tukaj."))

    def test_inequality_brackets_stay_exposed(self):
        text = "Res je, da x < 5 velja."
        self.assertTrue(_fully_exposed(text, "x < "))
        # no xml-fragment span may cover the bracket
        self.assertEqual(
            [reason for _s, _e, reason in
             PB.protection_with_status(text, helper_path=HELPER).intervals
             if "xml-fragment" in reason], [])

    def test_lone_bracket_stays_exposed(self):
        text = "Glej levo < stran."
        self.assertTrue(_fully_exposed(text, "< stran."))

    def test_recognized_html_unchanged(self):
        text = 'Označimo <div class="a">vsebino</div> in <div>šumnik</div>.'
        self.assertTrue(_fully_protected(text, '<div class="a">'))
        self.assertTrue(_fully_protected(text, "<div>"))
        self.assertTrue(_fully_exposed(text, "vsebino"))
        self.assertTrue(_fully_exposed(text, "šumnik"))

    # --- committed dev-edge batch re-validation -----------------------------
    def test_dev_edge_batch_fail_closed(self):
        root = REPO / "research" / "prose-boundary" / "corpus" \
            / "defect-dev-008h"
        docs = sorted((root / "documents").glob("*.json"))
        self.assertEqual(len(docs), 32)
        for p in docs:
            doc = json.loads(p.read_text(encoding="utf-8"))
            label = json.loads(
                (root / "labels" / p.name).read_text(encoding="utf-8"))
            text = doc["document"]
            data = text.encode("utf-8")
            self.assertEqual(hashlib.sha256(data).hexdigest(), doc["sha256"])
            self.assertTrue(all(label["invariants"].values()))
            result = PB.protection_with_status(text, helper_path=HELPER)
            self.assertEqual(result.mode, "parser-first", doc["doc_id"])
            prot: set[int] = set()
            for s, e, _r in result.intervals:
                prot.update(range(PB.cp_to_byte(text, s),
                                  PB.cp_to_byte(text, e)))
            for region in label["regions"]:
                rs = PB.cp_to_byte(text, region["start_cp"])
                re_ = PB.cp_to_byte(text, region["end_cp"])
                span = set(range(rs, re_))
                if region["role"] == "PROTECTED":
                    self.assertEqual(
                        span - prot, set(),
                        f"{doc['doc_id']}: PROTECTED region {region} "
                        f"has uncovered bytes")
                elif region["role"] == "POLICY_EXPOSED":
                    self.assertEqual(
                        span & prot, set(),
                        f"{doc['doc_id']}: POLICY_EXPOSED region {region} "
                        f"has covered bytes")

    def test_dev_edge_batch_census_matches_files(self):
        census = json.loads(
            (REPO / "research" / "prose-boundary" / "corpus" / "manifests"
             / "corpus-census.json").read_text(encoding="utf-8"))
        entry = census["defect_dev_008h"]
        root = REPO / entry["root"]
        for name, spec in entry["documents"]["documents_by_file"].items():
            data = (root / "documents" / name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),
                             spec["sha256"])
        for name, spec in entry["labels"]["labels_by_file"].items():
            data = (root / "labels" / name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),
                             spec["sha256"])


if __name__ == "__main__":
    unittest.main()
