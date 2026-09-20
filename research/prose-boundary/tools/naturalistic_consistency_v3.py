"""008-h requirement 8: naturalistic consistency re-run (committed
deterministic driver; data-free aggregate under results/hidden-acceptance-v3/).

With the frozen 008-h implementation, re-runs the protection output on the
70 naturalistic responses (private root, read through the disclosed
adjudication loading only) against the EXISTING completed v2 labels (frozen
adjudication outputs - no re-adjudication except the narrow predeclared
label-correction path of scope item 8, which is agent-level and, if used,
recorded separately in the aggregate with rationale).

Span rule (carried from 008-g, disclosed): a line range maps to the
code-point span from the start of its first line to the end of its last line
in the CRLF-normalized view (including the trailing newline of the last line
when present), mapped to original-view code points (identity when no CRLF).
Exposed bytes = span bytes not covered by a protection interval.

008-h addition (the 008-g D1-4 registration): every exposed range carries
exactly one resolution kind:
  CLOSED-RESIDUAL                 - covered by a bounded residual
                                    extension/trigger implemented in this
                                    round (named categories, strict trigger,
                                    negative controls); class reference
                                    recorded;
  DOCUMENTED-DIALECT-LIMITATION   - a v4 policy class documents the shape
                                    rule with measured evidence and
                                    justification (only where no bounded
                                    recognizer within the named categories is
                                    viable, with the reason recorded);
                                    class reference recorded;
  AMBIGUOUS                       - explicitly AMBIGUOUS-labeled range after
                                    reconciliation;
  UNRESOLVED                      - any other (a material contradiction
                                    capping the verdict at CONDITIONAL and
                                    named as remaining scope).
The resolution map for the 15 exposed ranges of the 008-g naturalistic
consistency aggregate is embedded below (data-free: case ID + line range ->
kind + class reference); any exposed range outside the map is reported
UNRESOLVED (fail-closed). The map is informed by - and does not predetermine
- the committed shape analysis (shape-analysis-008h.json).

Materiality (008-g rule, carried for continuity): a range with exposed
bytes >= 50 is a material range; a case with any material range or >= 5
exposed ranges of any size is a material case. Verdict condition (vii)
requires: no UNRESOLVED material range, and each 008-g material case carries
a resolution kind on every exposed range.

The 008-g deterministic attribution heuristic (parser-dialect /
label-ambiguity / residual-class-gap) is carried unchanged for continuity.

Usage (private roots are invocation arguments; no private paths in \nthis committed file):\n  python3 -B naturalistic_consistency_v3.py \\\n      --v1-private-root <008c-hidden> --v2-private-root <008g-hidden> \\\n      [--helper <prose-boundary-meas>]\n\nNo model calls of any kind; private-root reads are harness-mediated
(load_hidden_cases) and produce a data-free aggregate (counts, case IDs,
line/byte references; no response content, no private paths).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOLS = Path(__file__).resolve().parent
OUT = REPO / "research/prose-boundary/results/hidden-acceptance-v3/naturalistic-consistency-v3.json"
MATERIAL_BYTES = 50
MATERIAL_RANGES_PER_CASE = 5

sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(REPO))

import coordinate as C  # noqa: E402
import naturalistic_adjudication as NA  # noqa: E402
import naturalistic_adjudication_v2 as NA2  # noqa: E402  (line views)
from research.curated import prose_boundary as PB  # noqa: E402

DDL = "DOCUMENTED-DIALECT-LIMITATION"
CR = "CLOSED-RESIDUAL"
AMBIGUOUS = "AMBIGUOUS"
UNRESOLVED = "UNRESOLVED"

# The 15 exposed ranges of the 008-g naturalistic consistency aggregate
# (committed, data-free) resolved per D1-4. Class references point at the
# committed structural-policy-v4.json policy-exposed dialect-ambiguity
# classes. Keyed by (case_id, (start_line, end_line)).
RESOLUTION_MAP: dict[tuple[str, tuple[int, int]], tuple[str, str, str]] = {
    ("nat-algorithm-python-hidden-03", (20, 23)): (
        DDL, "markdown-table-dialect-boundary",
        "recognized Markdown table: cell/head text is candidate prose in the dialect"),
    ("nat-comparison-table-hidden-02", (3, 4)): (
        DDL, "markdown-table-dialect-boundary",
        "recognized Markdown table (same shape)"),
    ("nat-comparison-table-hidden-04", (3, 4)): (
        DDL, "markdown-table-dialect-boundary",
        "recognized Markdown table (same shape)"),
    ("nat-glossary-entry-hidden-03", (18, 20)): (
        DDL, "markdown-table-dialect-boundary",
        "table-like lines the dialect does not recognize as a table: plain prose; a table-shape recognizer would reparse Markdown structure (excluded)"),
    ("nat-math-answer-hidden-04", (3, 7)): (
        DDL, "markdown-table-dialect-boundary",
        "recognized Markdown table (same shape)"),
    ("nat-qa-answer-hidden-05", (5, 6)): (
        DDL, "markdown-table-dialect-boundary",
        "recognized Markdown table (same shape)"),
    ("nat-table-equations-hidden-02", (3, 4)): (
        DDL, "markdown-table-dialect-boundary",
        "recognized Markdown table (same shape)"),
    ("nat-table-equations-hidden-03", (3, 7)): (
        DDL, "markdown-table-dialect-boundary",
        "recognized Markdown table (same shape)"),
    ("nat-json-config-hidden-01", (26, 34)): (
        DDL, "markdown-table-dialect-boundary",
        "recognized Markdown table (same shape)"),
    ("nat-json-config-hidden-01", (37, 40)): (
        DDL, "list-item-candidate-prose",
        "list item content is candidate prose; machine-like tokens inside the item are protected only where a bounded residual class fires"),
    ("nat-qa-answer-hidden-04", (10, 13)): (
        DDL, "list-item-candidate-prose",
        "list item content (same shape)"),
    ("nat-qa-answer-hidden-03", (15, 21)): (
        DDL, "indented-code-lazy-continuation",
        "the dialect reads the indented lines as lazy paragraph continuation (not an indented code block); code intent is a composition decision"),
    ("nat-changelog-hidden-03", (3, 3)): (
        DDL, "residual-token-line-glue",
        "the bounded residual classes protect the machine tokens; the line's glue bytes remain candidate prose"),
    ("nat-changelog-hidden-03", (10, 10)): (
        DDL, "residual-token-line-glue",
        "residual-token line glue (same shape)"),
    ("nat-glossary-entry-hidden-02", (26, 26)): (
        DDL, "residual-token-line-glue",
        "residual-token line glue (same shape)"),
}
MATERIAL_CASE_IDS_008G = [
    "nat-glossary-entry-hidden-03", "nat-json-config-hidden-01",
    "nat-math-answer-hidden-04", "nat-qa-answer-hidden-04",
    "nat-table-equations-hidden-03",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v1-private-root", required=True, type=Path,
                        help="v1 private root (008c-hidden); the fixed "
                             "70-case naturalistic population")
    parser.add_argument("--v2-private-root", required=True, type=Path,
                        help="v2 private root (008g-hidden); the frozen "
                             "completed labels")
    parser.add_argument("--helper", type=Path, default=None,
                        help="pinned helper (default: PB.find_helper() "
                             "discovery, sha256-verified)")
    args = parser.parse_args()
    v1_root = args.v1_private_root.resolve()
    v2_root = args.v2_private_root.resolve()
    helper = args.helper.resolve() if args.helper else PB.find_helper()
    if helper is None:
        print("pinned helper unavailable (fail-closed)")
        return 1
    cases = NA.load_hidden_cases(v1_root)
    cases.sort(key=lambda c: c["case_id"])
    per_case = []
    material_case_ids = []
    material_range_count = 0
    unresolved_material = []
    attr_counter: Counter = Counter()
    resolution_counter: Counter = Counter()
    label_corrections: list[dict] = []  # populated only via the narrow predeclared path (agent-level)

    for case in cases:
        cid = case["case_id"]
        label_path = v2_root / "annotations" / f"{cid}.json"
        if not label_path.is_file():
            print("missing label for", cid)
            return 1
        label = json.loads(label_path.read_text(encoding="utf-8"))
        if label.get("status") != "LABELED":
            per_case.append({"case_id": cid, "status": label.get("status"),
                             "material": False, "ranges_checked": 0,
                             "max_exposed_bytes": 0, "exposed_ranges_any_size": 0,
                             "exposed_ranges": []})
            continue
        fragment = case["fragment"]
        lines, crlf = NA2.numbered_view(fragment)
        n = len(lines)
        result = PB.protection_with_status(fragment, helper_path=helper)
        if result.mode != "parser-first":
            print("fallback for", cid, result.fallback_reason)
            return 1
        prot: set[int] = set()
        for s, e, _ in result.intervals:
            prot.update(range(C.cp_to_byte(fragment, s), C.cp_to_byte(fragment, e)))

        starts = []
        off = 0
        for i, ln in enumerate(lines):
            starts.append(off)
            off += len(ln) + (1 if i < n - 1 else 0)

        case_ranges = []
        for r in label["reconciliation"]["final_ranges"]:
            cat = r["category"]
            if cat not in ("STRUCTURAL_PROTECT", "MACHINE_SIGNIFICANT_RESIDUAL"):
                continue
            s_line = r["start_line"] - 1
            e_line = r["end_line"] - 1
            cs = starts[s_line]
            ce = starts[e_line] + len(lines[e_line]) + (1 if e_line < n - 1 else 0)
            bs, be = C.cp_to_byte(fragment, cs), C.cp_to_byte(fragment, ce)
            span = set(range(bs, be))
            exposed = len(span - prot)
            entry = {"line_range": [r["start_line"], r["end_line"]],
                     "category": cat,
                     "span_bytes": len(span), "exposed_bytes": exposed,
                     "material_range": exposed >= MATERIAL_BYTES}
            if exposed > 0:
                key = (cid, (r["start_line"], r["end_line"]))
                if key in RESOLUTION_MAP:
                    kind, cls, note = RESOLUTION_MAP[key]
                else:
                    kind, cls, note = (UNRESOLVED, None,
                                       "exposed range outside the embedded D1-4 "
                                       "resolution map (fail-closed)")
                entry["resolution"] = {"kind": kind,
                                       "class_reference": cls,
                                       "note": note}
                resolution_counter[kind] += 1
                if kind == UNRESOLVED and entry["material_range"]:
                    unresolved_material.append({"case_id": cid,
                                                "line_range": [r["start_line"], r["end_line"]],
                                                "exposed_bytes": exposed})
            case_ranges.append(entry)
            if entry["material_range"]:
                material_range_count += 1

        any_size = [x for x in case_ranges if x["exposed_bytes"] > 0]
        material = (max((x["exposed_bytes"] for x in case_ranges), default=0) >= MATERIAL_BYTES
                    or len(any_size) >= MATERIAL_RANGES_PER_CASE)
        if material:
            material_case_ids.append(cid)

        # attribution (carried 008-g deterministic heuristic, data-free)
        final_arr = label["reconciliation"]["final_line_array"]
        norm_map = NA2.crlf_map(fragment) if crlf else None

        def _to_orig(k: int) -> int:
            return norm_map[k] if norm_map is not None else k

        def _prose_words(text: str) -> int:
            return sum(1 for w in text.split() if len(w) >= 4
                       and any(ch.isalpha() for ch in w))

        attrs = Counter()
        for x in any_size:
            s_l, e_l = x["line_range"]
            if x["category"] == "STRUCTURAL_PROTECT":
                attrs["parser-dialect"] += 1
                continue
            adjacent_soft = any(
                final_arr[i - 1] in ("AMBIGUOUS", "GENUINE_PROSE")
                for i in range(s_l - 2, e_l + 1) if 0 <= i < n)
            range_text = fragment[
                C.cp_to_byte(fragment, _to_orig(starts[s_l - 1])):
                C.cp_to_byte(fragment, _to_orig(starts[e_l - 1] + len(lines[e_l - 1])))]
            if adjacent_soft or _prose_words(range_text) >= 2:
                attrs["label-ambiguity"] += 1
            else:
                attrs["residual-class-gap"] += 1
        per_case.append({
            "case_id": cid, "status": "LABELED",
            "ranges_checked": len(case_ranges),
            "exposed_ranges_any_size": len(any_size),
            "max_exposed_bytes": max((x["exposed_bytes"] for x in case_ranges), default=0),
            "material": material,
            "exposed_ranges": case_ranges,
            "attribution": dict(attrs),
        })
        attr_counter.update(attrs)

    impl_sha = hashlib.sha256(
        (REPO / "research/curated/prose_boundary.py").read_bytes()).hexdigest()
    out = {
        "schema": "008h-naturalistic-consistency-v3/1",
        "order": "008-h",
        "label": ("naturalistic consistency re-run (order requirement 8): the "
                  "frozen 008-h implementation's protection output on the 70 "
                  "naturalistic responses compared against the EXISTING "
                  "completed v2 labels (fixed population, no re-adjudication "
                  "except the narrow predeclared label-correction path); "
                  "data-free aggregate (counts, case IDs, line/byte "
                  "references only; no response content, no private paths)"),
        "span_rule": ("a line range maps to the code-point span from the start "
                      "of its first line to the end of its last line in the "
                      "CRLF-normalized view (including the trailing newline of "
                      "the last line when present), mapped to original-view "
                      "code points (identity when no CRLF); exposed bytes = "
                      "span bytes not covered by a protection interval"),
        "materiality_predeclared": {
            "single_range_exposed_bytes": MATERIAL_BYTES,
            "exposed_ranges_per_case": MATERIAL_RANGES_PER_CASE,
            "rule": "008-g rule carried for continuity: a range with exposed bytes >= 50 is material; a case with any material range or >= 5 exposed ranges of any size is material. Verdict condition (vii) operates on material RANGES: none may be UNRESOLVED",
        },
        "resolution_taxonomy": ("CLOSED-RESIDUAL / DOCUMENTED-DIALECT-LIMITATION "
                                "/ AMBIGUOUS / UNRESOLVED (008-h D1-4); class "
                                "reference recorded for the first two kinds"),
        "cases_total": len(cases),
        "material_contradictions_008g_rule": len(material_case_ids),
        "material_case_ids": material_case_ids,
        "material_case_ids_008g": MATERIAL_CASE_IDS_008G,
        "material_ranges_total": material_range_count,
        "resolution_total": dict(resolution_counter),
        "unresolved_material_ranges": unresolved_material,
        "verdict_condition_vii": {
            "no_unresolved_material_range": not unresolved_material,
            "material_cases_all_resolved": all(
                all(x.get("resolution", {}).get("kind") != UNRESOLVED
                    for x in pc["exposed_ranges"] if x["exposed_bytes"] > 0)
                for pc in per_case if pc["case_id"] in MATERIAL_CASE_IDS_008G
            ),
        },
        "label_corrections": label_corrections,
        "label_corrections_note": ("empty: the re-run revealed no frozen label "
                                   "factually wrong about the source text, so "
                                   "the narrow predeclared re-adjudication path "
                                   "(at most 5 cases, frozen guide, committed "
                                   "008-g v2 instrument) was not triggered"),
        "per_case": per_case,
        "attribution_total": dict(attr_counter),
        "implementation_identity": {
            "research/curated/prose_boundary.py": impl_sha,
            "helper_sha256": hashlib.sha256(helper.read_bytes()).hexdigest(),
            "note": "the frozen 008-h implementation (frozen protection identity recorded in experiment-008h.json)",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    OUT.write_text(payload, encoding="utf-8")
    print(json.dumps({"material_contradictions": len(material_case_ids),
                      "material_case_ids": material_case_ids,
                      "resolution_total": dict(resolution_counter),
                      "unresolved_material": len(unresolved_material),
                      "out": str(OUT),
                      "out_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest()}))
    return 0 if not unresolved_material else 1


if __name__ == "__main__":
    sys.exit(main())
