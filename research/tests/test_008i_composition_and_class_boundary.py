"""008-i focused tests (order 008-i scope items 3-4, Verification section):
the R1 extension to dialect HTML block-start lines, the display-dollar
adjacency guard, the T6 clean-URL link-destination admission, and the
xml-fragment class-boundary decision D1-5 (branch-aware: the assertions on
the measured non-ASCII-attribute shape assert consistency with the committed
implementation state - PRIMARY refinement or documented-boundary FALLBACK;
this file is committed in the D1-5 decision commit).

Positive:
  - the opening-tag-line + fenced-code composition fires R1 with a NEUTRAL
    barrier and zero exposed protected bytes on the shape fixture;
  - the xml-fragment class fires on the measured non-ASCII-attribute shape
    under the EXTEND branch / is classified per the documented boundary
    under the FALLBACK branch;
  - the display-dollar adjacency fires the guard with the NEUTRAL barrier
    and zero exposed TeX-command bytes on the shape fixture;
  - the T6 clean-URL admission assert passes on clean fragments.
Negative:
  - the 008-g/008-h closing-tag R1 fixtures unchanged (incl. the
    test-pinned bare <div> corner); R2/R3 predicates unchanged;
  - the xml-fragment class still abstains for a dialect-recognized tag
    name with ASCII attributes (v2 parity) and the non-vocabulary-name
    path is byte-identical to 008-h (fires by the name trigger, unchanged);
  - the guard does not fire for a complete display-dollar component not
    adjacent to a malformed opener, nor for a malformed opener not followed
    by a complete component;
  - no new over-suppression on any committed dev fixture (the corpus-level
    negative proof is the dev regression gate; the fail-closed batch
    re-checks are included here).
"""

import hashlib
import json
import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "research" / "prose-boundary" / "tools"))
sys.path.insert(0, str(REPO))

import prose_boundary_builder as B  # noqa: E402
from research.curated import prose_boundary as PB  # noqa: E402

HELPER = PB.find_helper()
NEEDS_HELPER = HELPER is not None
CONSTRUCTION = B.CONSTRUCTION
ORACLE_REFINED = B.ORACLE_REFINED

# D1-5 branch detection (committed implementation state)
D15_REFINED = hasattr(PB, "_tag_non_ascii_attr_name")


def _segs(html_frag, sep, code_frag):
    return [
        ("prose line\n", "comp-a", "PROSE", CONSTRUCTION),
        ("\n", "template", "NEUTRAL", CONSTRUCTION),
        (html_frag, "comp-html", "PROTECTED", CONSTRUCTION),
        (sep, "template", "NEUTRAL", CONSTRUCTION),
        (code_frag, "comp-code", "PROTECTED", CONSTRUCTION),
    ]


def _protected_bytes(text):
    result = PB.protection_with_status(text, helper_path=HELPER)
    assert result.mode == "parser-first", result.fallback_reason
    prot = set()
    for s, e, _r in result.intervals:
        prot.update(range(PB.cp_to_byte(text, s), PB.cp_to_byte(text, e)))
    return prot


def _exposed_chars(text, sub):
    prot = _protected_bytes(text)
    start = len(text[:text.index(sub)].encode("utf-8"))
    out = []
    for ch in sub:
        cb = len(ch.encode("utf-8"))
        if all(b not in prot for b in range(start, start + cb)):
            out.append(ch)
        start += cb
    return "".join(out)


# ---------------------------------------------------------------------------
# scope item 3a: R1 extension to dialect HTML block-start lines
# ---------------------------------------------------------------------------
class TestR1ExtensionPredicates(unittest.TestCase):
    def test_multi_tag_opening_line_fires(self):
        # the v3 S1 shape: a complete multi-tag opening line
        self.assertTrue(B.is_html_block_start_line(
            '<table class="t"><tr><td>celica</td></tr>'))
        self.assertTrue(B.is_html_block_start_line("<ul><li>a</li>"))
        self.assertTrue(B.is_html_block_start_line("<div><span>t</span></div>"))

    def test_incomplete_block_tag_fires(self):
        self.assertTrue(B.is_html_block_start_line("<table"))
        self.assertTrue(B.is_html_block_start_line("<table class=\"x\"> <tr>"))

    def test_closing_tag_with_continuation_fires(self):
        self.assertTrue(B.is_html_block_start_line("</div> <span>t</span>"))

    def test_unterminated_comment_pi_cdata_decl_fire(self):
        self.assertTrue(B.is_html_block_start_line("<!-- komentar"))
        self.assertTrue(B.is_html_block_start_line("<?pi"))
        self.assertTrue(B.is_html_block_start_line("<![CDATA[x"))
        self.assertTrue(B.is_html_block_start_line("<!ENTITY x"))

    def test_terminated_comment_pi_cdata_decl_do_not_fire(self):
        self.assertFalse(B.is_html_block_start_line("<!-- komplet -->"))
        self.assertFalse(B.is_html_block_start_line("<?x ?>"))
        self.assertFalse(B.is_html_block_start_line("<![CDATA[ok]]>"))
        self.assertFalse(B.is_html_block_start_line("<!ENTITY a \"b\">"))

    def test_pre_style_script_textarea_fire(self):
        self.assertTrue(B.is_html_block_start_line("<pre"))
        self.assertTrue(B.is_html_block_start_line("<pre>"))
        self.assertTrue(B.is_html_block_start_line("<script async"))

    def test_bare_single_complete_opening_tag_corner_excluded(self):
        # the 008-h test-pinned corner (test_r1_not_on_non_closing_tag),
        # preserved by the '008-h R1/R2/R3 contract otherwise stay intact'
        # clause of the order; disclosed residual (REPORT-008I.md)
        for line in ("<div>", "<table>", "<table class=\"x\">", "<div/>",
                     "<TABLE>", "<span>", "<prefix>", "<table1>"):
            self.assertFalse(B.is_html_block_start_line(line), line)

    def test_plain_lines_do_not_fire(self):
        self.assertFalse(B.is_html_block_start_line("plain prose line"))
        self.assertFalse(B.is_html_block_start_line("V tabeli je <td> x"))


class TestR1ExtensionComposition(unittest.TestCase):
    def test_multi_tag_line_fence_inserts_barrier(self):
        out, n = B.apply_r1(_segs(
            '<table class="t"><tr><td>celica</td></tr>', "\n",
            "```\ncode en\n\ncode dva\n```\n"))
        self.assertEqual(n, 1)
        text = "".join(s[0] for s in out)
        self.assertIn(
            '<table class="t"><tr><td>celica</td></tr>\n\n```\ncode en\n',
            text)
        self.assertEqual(out[3], ("\n", "template", "NEUTRAL", CONSTRUCTION))

    def test_incomplete_block_tag_line_fence_inserts_barrier(self):
        _out, n = B.apply_r1(_segs("<table", "\n", "```\nx\n```\n"))
        self.assertEqual(n, 1)

    def test_closing_tag_with_continuation_fence_inserts_barrier(self):
        _out, n = B.apply_r1(_segs("</div> <span>t</span>", "\n", "```\nx\n```\n"))
        self.assertEqual(n, 1)

    def test_unterminated_comment_fence_inserts_barrier(self):
        _out, n = B.apply_r1(_segs("<!-- komentar", "\n", "```\nx\n```\n"))
        self.assertEqual(n, 1)

    def test_008g_008h_closing_tag_fixtures_unchanged(self):
        # exact v2 adjacency (frozen fixture re-asserted)
        out, n = B.apply_r1(_segs("</div>", "\n", "```\nx\n```\n"))
        self.assertEqual(n, 1)
        self.assertEqual(out[4], ("\n", "template", "NEUTRAL",
                                  CONSTRUCTION))
        self.assertIn("</div>\n\n```\nx\n```\n", "".join(s[0] for s in out))
        # indented code variant
        _out, n = B.apply_r1(_segs("</p>", "\n", "    code line\n"))
        self.assertEqual(n, 1)
        # already separated
        for segs in (_segs("</div>\n", "\n", "```\nx\n```\n"),
                     _segs("</div>", "\n\n", "```\nx\n```\n")):
            _out, n = B.apply_r1(segs)
            self.assertEqual(n, 0)
        # the test-pinned corner: bare single complete opening tag at EOL
        _out, n = B.apply_r1(_segs("<div>", "\n", "```\nx\n```\n"))
        self.assertEqual(n, 0)
        # next is prose, not a code block
        _out, n = B.apply_r1(_segs("</div>", "\n", "prose\n"))
        self.assertEqual(n, 0)


@unittest.skipUnless(NEEDS_HELPER, "pinned helper unavailable")
class TestR1ShapeFixturePipeline(unittest.TestCase):
    def test_e01_guarded_composition_zero_exposed_protected(self):
        # dev-edge e01 (D008i-A): the guarded composition (R1 barrier
        # present) - every PROTECTED region fully covered
        root = REPO / "research" / "prose-boundary" / "corpus" \
            / "defect-dev-008i"
        doc = json.loads((root / "documents" / "e01.json").read_text())
        label = json.loads((root / "labels" / "e01.json").read_text())
        text = doc["document"]
        data = text.encode("utf-8")
        self.assertEqual(hashlib.sha256(data).hexdigest(), doc["sha256"])
        prot = _protected_bytes(text)
        for region in label["regions"]:
            if region["role"] != "PROTECTED":
                continue
            rs = PB.cp_to_byte(text, region["start_cp"])
            re_ = PB.cp_to_byte(text, region["end_cp"])
            self.assertEqual(set(range(rs, re_)) - prot, set(),
                             f"e01: PROTECTED region {region} uncovered")
        # the code body after the internal blank line is protected
        self.assertEqual(_exposed_chars(text, "return a;"), "")

    def test_e01_raw_no_barrier_rederives_v3_mechanism(self):
        # the raw shape (no barrier) re-derives the v3 139 B mechanism:
        # the fence + first code lines are absorbed into the HTML block
        # (structural, covered); the code after the first internal blank
        # line parses as paragraph text and is exposed
        raw = ('Pred tem.\n'
               '<table class="t"><tr><td>celica</td></tr>\n'
               '```\nint a = 1;\n\nreturn a;\n```\n'
               'Za tem.\n')
        prot = _protected_bytes(raw)
        # fence absorbed (structural)
        i = raw.index("```")
        b = len(raw[:i].encode("utf-8"))
        self.assertTrue(all(x in prot for x in range(b, b + 3)))
        # first code line absorbed
        self.assertEqual(_exposed_chars(raw, "int a = 1;"), "")
        # code after the internal blank line exposed (the v3 mechanism)
        self.assertEqual(_exposed_chars(raw, "return a;"), "return a;")

    def test_e01_compose_guard_invariants_fail_closed(self):
        # a composition that would leave the adjacency unbarred is
        # impossible: the guard and the invariant share the predicate
        fam = {"comp-html": "structured-html", "comp-code": "code-cpp",
               "comp-a": "prose-science"}
        segs = _segs('<table class="t"><tr><td>celica</td></tr>', "\n",
                     "```\ncode en\n\ncode dva\n```\n")
        out, n = B.apply_r1(segs)
        self.assertEqual(n, 1)
        B.assert_composition_invariants(out, fam)
        # hand-removing the barrier must trip the invariant: the inserted
        # blank line sits immediately after the html component in the
        # guarded output (the original separator follows it); value
        # filtering cannot distinguish the two, so remove by position
        idx_html = next(i for i, s in enumerate(out) if s[1] == "comp-html")
        self.assertEqual(out[idx_html + 1],
                         ("\n", "template", "NEUTRAL", CONSTRUCTION))
        bare = out[:idx_html + 1] + out[idx_html + 2:]
        with self.assertRaises(AssertionError):
            B.assert_composition_invariants(bare, fam)


# ---------------------------------------------------------------------------
# scope item 3b: display-dollar adjacency guard
# ---------------------------------------------------------------------------
class TestDisplayDollarGuard(unittest.TestCase):
    def _fam(self):
        return {"p": "prose-science",
                "m": "malformed-incomplete-display-dollar",
                "d": "math-display-dollar"}

    def test_malformed_before_display_opener_fires(self):
        fam = self._fam()
        segs = [
            ("prose pred\n", "p", "PROSE", CONSTRUCTION),
            ("\n", "template", "NEUTRAL", CONSTRUCTION),
            ("$$\nezakljucena vrstica", "m", "POLICY_EXPOSED", CONSTRUCTION),
            ("\n", "template", "NEUTRAL", CONSTRUCTION),
            ("$$\nx = \\frac{a}{b}\n$$", "d", "PROTECTED", CONSTRUCTION),
        ]
        out, n = B.apply_display_dollar_guard(segs, fam)
        self.assertEqual(n, 1)
        text = "".join(s[0] for s in out)
        self.assertIn("zakljucena vrstica\n\n$$\nx = \\frac{a}{b}\n$$",
                      text)
        self.assertEqual(
            B.count_display_dollar_barrier_insertions(out, fam), 1)
        B.assert_composition_invariants(out, fam)

    def test_complete_component_not_adjacent_to_malformed_no_fire(self):
        fam = {"p": "prose-science", "d": "math-display-dollar",
               "d2": "math-display-dollar"}
        segs = [
            ("prose pred\n", "p", "PROSE", CONSTRUCTION),
            ("\n", "template", "NEUTRAL", CONSTRUCTION),
            ("$$\nx = 1\n$$", "d", "PROTECTED", CONSTRUCTION),
            ("\n", "template", "NEUTRAL", CONSTRUCTION),
            ("$$\ny = 2\n$$", "d2", "PROTECTED", CONSTRUCTION),
        ]
        _out, n = B.apply_display_dollar_guard(segs, fam)
        self.assertEqual(n, 0)

    def test_malformed_opener_not_followed_by_complete_component_no_fire(self):
        fam = {"p": "prose-science", "p2": "prose-history",
               "m": "malformed-incomplete-display-dollar"}
        segs = [
            ("prose pred\n", "p", "PROSE", CONSTRUCTION),
            ("\n", "template", "NEUTRAL", CONSTRUCTION),
            ("$$\nezakljucena vrstica", "m", "POLICY_EXPOSED", CONSTRUCTION),
            ("\n", "template", "NEUTRAL", CONSTRUCTION),
            ("navadna vrstica\n", "p2", "PROSE", CONSTRUCTION),
        ]
        _out, n = B.apply_display_dollar_guard(segs, fam)
        self.assertEqual(n, 0)

    def test_already_separated_no_fire(self):
        fam = self._fam()
        segs = [
            ("prose pred\n", "p", "PROSE", CONSTRUCTION),
            ("\n", "template", "NEUTRAL", CONSTRUCTION),
            ("$$\nezakljucena vrstica\n", "m", "POLICY_EXPOSED", CONSTRUCTION),
            ("\n", "template", "NEUTRAL", CONSTRUCTION),
            ("$$\nx = 1\n$$", "d", "PROTECTED", CONSTRUCTION),
        ]
        _out, n = B.apply_display_dollar_guard(segs, fam)
        self.assertEqual(n, 0)


@unittest.skipUnless(NEEDS_HELPER, "pinned helper unavailable")
class TestDisplayDollarShapeFixturePipeline(unittest.TestCase):
    def test_e03_guarded_composition_zero_exposed_protected(self):
        # dev-edge e03 (D008i-C): the guarded composition - the complete
        # component is a proper DisplayMath (body PROTECTED fully covered);
        # the malformed $$ stays policy-exposed (exposed by design)
        root = REPO / "research" / "prose-boundary" / "corpus" \
            / "defect-dev-008i"
        doc = json.loads((root / "documents" / "e03.json").read_text())
        label = json.loads((root / "labels" / "e03.json").read_text())
        text = doc["document"]
        data = text.encode("utf-8")
        self.assertEqual(hashlib.sha256(data).hexdigest(), doc["sha256"])
        prot = _protected_bytes(text)
        for region in label["regions"]:
            rs = PB.cp_to_byte(text, region["start_cp"])
            re_ = PB.cp_to_byte(text, region["end_cp"])
            span = set(range(rs, re_))
            if region["role"] == "PROTECTED":
                self.assertEqual(span - prot, set(),
                                 f"e03: PROTECTED region {region} uncovered")
            elif region["role"] == "POLICY_EXPOSED":
                self.assertEqual(span & prot, set(),
                                 f"e03: POLICY_EXPOSED region {region} "
                                 f"has covered bytes")
        # the TeX body is fully protected (no exposed TeX-command bytes)
        self.assertEqual(_exposed_chars(text, "x = \\frac{a}{b}"), "")

    def test_e03_raw_no_barrier_cross_pairing_exposes_tex_body(self):
        # the raw shape (no barrier) re-derives the v3 26 B mechanism:
        # the malformed opener pairs with the complete component's opener
        # (DisplayMath spans the two $$ lines), the TeX body then parses as
        # paragraph text where the command names and '=' are exposed
        raw = ('Pred tem.\n$$\nezakljucena vrstica\n'
               '$$\nx = \\frac{a}{b}\n$$\nZa tem.\n')
        self.assertEqual(_exposed_chars(raw, "\\frac"), "\\frac")
        self.assertEqual(_exposed_chars(raw, "="), "=")


# ---------------------------------------------------------------------------
# scope item 3c: T6 clean-URL link-destination admission
# ---------------------------------------------------------------------------
class TestT6Admission(unittest.TestCase):
    def test_clean_fragments_pass(self):
        self.assertTrue(B.t6_link_destination_clean(
            "https://example.com/path?q=1"))
        self.assertTrue(B.t6_link_destination_clean("http://a.si/x"))
        self.assertTrue(B.t6_link_destination_clean(
            "https://primer.si/dokumenti"))

    def test_non_clean_fragments_rejected(self):
        self.assertFalse(B.t6_link_destination_clean(
            "https://example.com/x https://y.si"))
        self.assertFalse(B.t6_link_destination_clean("/rel/path"))
        self.assertFalse(B.t6_link_destination_clean("https://ex<a>.com/x"))
        self.assertFalse(B.t6_link_destination_clean(""))

    def _pool(self, urls):
        return {
            "prose-science": [
                {"component_id": f"p{i}", "family": "prose-science",
                 "fragment": "Vrstica o rasti in merjenju.\n",
                 "category": "prose"} for i in range(4)
            ],
            "machine-urls": [
                {"component_id": f"u{i}", "family": "machine-urls",
                 "fragment": u, "category": "machine"}
                for i, u in enumerate(urls)
            ],
        }

    def test_t6_composes_clean_destination(self):
        pool = self._pool(["https://example.com/dokument"])
        fmap = {c["component_id"]: c["family"]
                for fam in pool.values() for c in fam}
        segs, _r1 = B.compose(random.Random(1), pool,
                              "T6-prose-link-prose", set(), fmap)
        text = "".join(s[0] for s in segs)
        self.assertIn("](https://example.com/dokument)", text)

    def test_t6_refuses_non_clean_destination(self):
        pool = self._pool(["https://example.com/x https://y.si",
                           "https://a.si/relativna pot"])
        with self.assertRaises(LookupError):
            B.compose(random.Random(1), pool, "T6-prose-link-prose", set(),
                      {c["component_id"]: c["family"]
                       for fam in pool.values() for c in fam})

    @unittest.skipUnless(NEEDS_HELPER, "pinned helper unavailable")
    def test_e04_neutral_split_labels_zero_exposed_protected(self):
        # dev-edge e04 (D008i-D): the T6 non-clean-destination observation
        # with NEUTRAL-split labels - machine URL tokens PROTECTED oracle-
        # refined (residual url class), inter-token space NEUTRAL, no
        # whole-region PROTECTED
        root = REPO / "research" / "prose-boundary" / "corpus" \
            / "defect-dev-008i"
        doc = json.loads((root / "documents" / "e04.json").read_text())
        label = json.loads((root / "labels" / "e04.json").read_text())
        text = doc["document"]
        data = text.encode("utf-8")
        self.assertEqual(hashlib.sha256(data).hexdigest(), doc["sha256"])
        prot = _protected_bytes(text)
        for region in label["regions"]:
            rs = PB.cp_to_byte(text, region["start_cp"])
            re_ = PB.cp_to_byte(text, region["end_cp"])
            span = set(range(rs, re_))
            if region["role"] == "PROTECTED":
                self.assertEqual(span - prot, set(),
                                 f"e04: PROTECTED region {region} uncovered")
        self.assertEqual(_exposed_chars(
            text, "https://primer.si/dokumenti"), "")
        self.assertEqual(_exposed_chars(text, "https://primer.si/tabela"), "")


# ---------------------------------------------------------------------------
# scope item 4: D1-5 xml-fragment class boundary (branch-aware)
# ---------------------------------------------------------------------------
@unittest.skipUnless(NEEDS_HELPER, "pinned helper unavailable")
class TestXmlFragmentClassBoundary(unittest.TestCase):
    def test_measured_shape_primary_refinement(self):
        # dialect-vocabulary name + non-ASCII attribute name: the tag as a
        # whole fails inline recognition solely because of the attribute
        if D15_REFINED:
            # PRIMARY: the class fires; the tag token is protected in full
            text = ('V tabeli je <table><tr><td \u0161irina="2" '
                    'id="celica1">celica</td></tr></table> vsebine.\n')
            prot = _protected_bytes(text)
            tag = '<td \u0161irina="2" id="celica1">'
            self.assertEqual(_exposed_chars(text, tag), "",
                             "PRIMARY: the measured tag token must be "
                             "fully protected")
        else:
            # FALLBACK: the class abstains (documented boundary); the tag
            # token bytes are candidate prose; the interior machine tokens
            # are covered by their own classes
            text = ('V tabeli je <table><tr><td \u0161irina="2" '
                    'id="celica1">celica</td></tr></table> vsebine.\n')
            self.assertEqual(_exposed_chars(text, "2"), "",
                             "FALLBACK: interior number stays class-covered")
            self.assertEqual(_exposed_chars(text, "celica1"), "",
                             "FALLBACK: interior identifier stays "
                             "class-covered")
            # the tag delimiters/name/attribute-name bytes are exposed
            # (the measured boundary)
            self.assertEqual(_exposed_chars(text, "<td "), "<td ",
                             "FALLBACK: the tag token bytes must stay "
                             "exposed (documented class boundary)")

    def test_e02_dev_edge_branch_consistent(self):
        # the committed dev-edge e02 labels must be consistent with the
        # committed implementation state (fail-closed)
        root = REPO / "research" / "prose-boundary" / "corpus" \
            / "defect-dev-008i"
        doc = json.loads((root / "documents" / "e02.json").read_text())
        label = json.loads((root / "labels" / "e02.json").read_text())
        text = doc["document"]
        data = text.encode("utf-8")
        self.assertEqual(hashlib.sha256(data).hexdigest(), doc["sha256"])
        prot = _protected_bytes(text)
        for region in label["regions"]:
            rs = PB.cp_to_byte(text, region["start_cp"])
            re_ = PB.cp_to_byte(text, region["end_cp"])
            span = set(range(rs, re_))
            if region["role"] == "PROTECTED":
                self.assertEqual(span - prot, set(),
                                 f"e02: PROTECTED region {region} uncovered")
            elif region["role"] == "POLICY_EXPOSED":
                self.assertEqual(span & prot, set(),
                                 f"e02: POLICY_EXPOSED region {region} has "
                                 f"covered bytes")

    def test_recognized_name_ascii_attrs_still_abstain(self):
        # v2 parity: a dialect-recognized tag name with ASCII attributes is
        # recognised inline (structural) - the class abstains
        self.assertEqual(
            PB._xml_fragment_spans('<div class="a">vsebina</div>'), [])
        self.assertEqual(
            PB._xml_fragment_spans("<table><tr><td>x</td></tr></table>"), [])

    def test_non_vocabulary_name_path_unchanged_008h(self):
        # non-vocabulary (diacritic) names fire by the name trigger, with
        # or without non-ASCII attributes - byte-identical to 008-h
        # (pair protected in full)
        self.assertEqual(
            PB._xml_fragment_spans("<\u017eumnik a>b</\u017eumnik>"),
            [(0, len("<\u017eumnik a>b</\u017eumnik>"))])
        self.assertEqual(
            PB._xml_fragment_spans("<\u017eumnik \u0161irina=\"1\">b"
                                   "</\u017eumnik>"),
            [(0, len("<\u017eumnik \u0161irina=\"1\">b</\u017eumnik>"))])
        # a non-vocabulary ASCII shape name (period/underscore) still fires
        self.assertEqual(
            PB._xml_fragment_spans("<a.b>x</a.b>"),
            [(0, len("<a.b>x</a.b>"))])

    def test_comparison_and_bracket_guards_unchanged(self):
        self.assertEqual(PB._xml_fragment_spans("x < 5 in vrstici"), [])
        self.assertEqual(PB._xml_fragment_spans("<5"), [])
        self.assertEqual(PB._xml_fragment_spans("sam < kot pred"), [])


# ---------------------------------------------------------------------------
# R2/R3 predicates unchanged (008-h contract)
# ---------------------------------------------------------------------------
class TestAdmissionPredicatesUnchanged(unittest.TestCase):
    def test_r2_unchanged(self):
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

    def test_r3_unchanged(self):
        self.assertTrue(B.r3_xml_diacritic_tag_excluded("<\u0161umnik>t</\u0161umnik>"))
        self.assertTrue(B.r3_xml_diacritic_tag_excluded(
            '<\u010drtica x="1"/>'))
        self.assertFalse(B.r3_xml_diacritic_tag_excluded(
            "<stevec>42</stevec>"))
        self.assertFalse(B.r3_xml_diacritic_tag_excluded(
            '<div class="a">x</div>'))


# ---------------------------------------------------------------------------
# no new over-suppression on committed dev fixtures (corpus-level proof is
# the dev regression gate; the batch fail-closed re-check is included)
# ---------------------------------------------------------------------------
@unittest.skipUnless(NEEDS_HELPER, "pinned helper unavailable")
class TestCommittedDevEdgeFailClosed(unittest.TestCase):
    def _fail_closed(self, root, n_docs):
        docs = sorted((root / "documents").glob("*.json"))
        self.assertEqual(len(docs), n_docs)
        for p in docs:
            doc = json.loads(p.read_text(encoding="utf-8"))
            label = json.loads((root / "labels" / p.name).read_text(
                encoding="utf-8"))
            text = doc["document"]
            data = text.encode("utf-8")
            self.assertEqual(hashlib.sha256(data).hexdigest(), doc["sha256"])
            self.assertTrue(all(label["invariants"].values()))
            result = PB.protection_with_status(text, helper_path=HELPER)
            self.assertEqual(result.mode, "parser-first", doc["doc_id"])
            prot = set()
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

    def test_008g_batch_fail_closed_unchanged(self):
        self._fail_closed(REPO / "research" / "prose-boundary" / "corpus"
                          / "defect-dev-008g", 50)

    def test_008h_batch_fail_closed_unchanged(self):
        self._fail_closed(REPO / "research" / "prose-boundary" / "corpus"
                          / "defect-dev-008h", 32)

    def test_008i_batch_fail_closed(self):
        # e01/e03/e04 under every implementation state; e02 consistent
        # with the committed D1-5 branch (see TestXmlFragmentClassBoundary)
        self._fail_closed(REPO / "research" / "prose-boundary" / "corpus"
                          / "defect-dev-008i", 4)

    def test_008i_census_matches_files(self):
        census = json.loads(
            (REPO / "research" / "prose-boundary" / "corpus" / "manifests"
             / "corpus-census.json").read_text(encoding="utf-8"))
        entry = census["defect_dev_008i"]
        root = REPO / entry["root"]
        for name, spec in entry["documents"]["documents_by_file"].items():
            data = (root / "documents" / name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),
                             spec["sha256"])


if __name__ == "__main__":
    unittest.main()
