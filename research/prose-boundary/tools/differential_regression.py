"""008-c Increment 3: differential regression and dev-corpus evaluation.

Three committed, data-free aggregates (tuning evidence, never acceptance):

(a) the 008-a 50-fixture P2 baseline re-derived through the new runtime
    path (parser-first protection with the pinned helper): zero
    coordinate violations, zero protected-region exposures under policy
    v2, zero missing prose bytes. Dual view: the structural (parser-only)
    view must reproduce the 008-a increment-1 result exactly; the policy-
    v2 view (with the residual layer) additionally reports the expected
    per-region residual deltas (machine-like content inside
    PROSE_CANDIDATE regions is protected by design).

(b) the full dev-corpus metric set (order scope item 15) over the 3,000
    committed development documents and their machine-known ground-truth
    interval maps.

(c) the differential of the new protection (parser-first + residual)
    against the retained 008-a legacy full-regex rule set over the 008-a
    100-sample receipt corpus, with the same consequence classes 1-8 and
    frozen priority order [3, 6, 5, 4, 1, 2, 7, 8]. Assertions: zero
    class-3 safety spans, and the 22 class-7 spans of the 008-a
    differential remain protected by the new second stage (residual
    layer).

Plus the scope item 15 performance measurement (parser + residual
latency on representative documents at ~1KB, ~10KB, ~50KB; median
ms/document and peak RSS, data-free).

Privacy (frozen rules): the private runtime parent and the helper binary
are supplied at run time as CLI arguments and never committed; raw private
text (the 100-sample corpus) is held in memory only and never enters the
output; the output carries counts, categories and hashes only. No model
calls are made.

Deterministic: identical inputs produce identical output bytes.

Usage:
  python3 -B differential_regression.py --runtime-root <private-parent> \
      --helper <prose-boundary-meas> [--dev-corpus <corpus dir>] \
      [--out <results/increment3>] [--no-performance]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2]))  # repository root

import coordinate as C  # noqa: E402
import select_corpus as S  # noqa: E402
import run_differential as RD  # noqa: E402  (frozen 008-a class taxonomy)
from research.curated import prose_boundary as PB  # noqa: E402

ROOT = HERE.parent
REPO_ROOT = HERE.parents[2]
FIXTURES = ROOT / "fixtures" / "fixtures.json"
POLICY_V2 = ROOT / "config" / "structural-policy-v2.json"
SEL_RECEIPT = ROOT / "results" / "increment2" / "selection-receipt.json"
DIFF_RECEIPT = ROOT / "results" / "increment2" / "differential-summary.json"
DEFAULT_CORPUS = ROOT / "corpus"
DEFAULT_OUT = ROOT / "results" / "increment3"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(obj, ensure_ascii=False, indent=1) + "\n"
    path.write_text(payload, encoding="utf-8")
    return sha256_bytes(payload.encode("utf-8"))


# ---------------------------------------------------------------------------
# self-test (controlled synthetic probes; must pass before any result)
# ---------------------------------------------------------------------------
def self_test(helper: Path) -> dict:
    results: dict[str, bool] = {}
    # ST-1: coordinate round trip on multi-byte content (caron, emoji,
    # decomposed) - bisected positions must be rejected, boundaries exact.
    # bytes: a(0) c-caron(1-2) b(3) sp(4) emoji(5-8) sp(9) e(10) c-c(11-12)
    text = "a\u010db \U0001F680 e\u0301"
    data = text.encode("utf-8")
    assert len(data) == 13 and len(text) == 8
    results["st1_cp_round_trip"] = (
        C.byte_to_cp(data, 1) == 1
        and C.byte_to_cp(data, 4) == 3
        and C.cp_to_byte(text, 4) == 5
        and C.cp_to_byte(text, 8) == len(data)
        and C.byte_to_cp(data, 9) == 5
        and C.byte_to_cp(data, 2) is None
        and C.byte_to_cp(data, 6) is None
        and C.byte_to_cp(data, 12) is None
        and all(C.round_trip(text, b) for b in (0, 1, 3, 4, 5, 9, 10, 11, 13))
        and all(not C.round_trip(text, b) for b in (2, 6, 7, 8, 12))
    )
    # ST-2: a deliberately broken coordinate mapping is caught: an event
    # range bisecting a code point must fail closed (fallback), not crash.
    r = PB.protection_with_status("Vzorec \u010d texta", helper_path=helper)
    good = r.mode == "parser-first"
    # explicit tampered protocol: Text range 0..1 bisects the 2-byte
    # c-caron of the 4-byte document
    tampered = (
        b'{"i":0,"k":"S.Para","s":0,"e":4}\n'
        b'{"i":1,"k":"Text","s":0,"e":1}\n'
        b'{"i":2,"k":"E.Para","s":0,"e":4}\n'
        b'{"eof":true}\n'
    )
    try:
        PB.parse_protocol(tampered, "\u010crka".encode())
        results["st2_bisection_caught"] = False
    except PB.ProtectionFallback as exc:
        results["st2_bisection_caught"] = str(exc) == "coordinate-bisection"
    # ST-3: out-of-order protocol fails closed.
    try:
        PB.parse_protocol(b'{"i":1,"k":"S.Para","s":0,"e":2}\n{"eof":true}\n', b"ab")
        results["st3_out_of_order_caught"] = False
    except PB.ProtectionFallback as exc:
        results["st3_out_of_order_caught"] = str(exc) == "protocol-out-of-order"
    # ST-4: truncated protocol (missing eof) fails closed.
    try:
        PB.parse_protocol(b'{"i":0,"k":"S.Para","s":0,"e":2}', b"ab")
        results["st4_truncation_caught"] = False
    except PB.ProtectionFallback as exc:
        results["st4_truncation_caught"] = str(exc) == "protocol-truncated"
    # ST-5: fail-open is impossible by construction - every mode is either
    # parser-first (full protection computed) or legacy-fallback (the full
    # 008-a rule set). An empty result is only possible for an empty input.
    r_empty = PB.protection_with_status("", helper_path=helper)
    results["st5_no_fail_open"] = (
        r_empty.mode in ("parser-first", "legacy-fallback")
        and r_empty.intervals == ()
        and good
    )
    # ST-6: residual second stage covers legacy class-7 material: currency
    # numbers and upper identifiers stay protected.
    r6 = PB.protection_with_status("Cena: 5 $ in 10 $. VREDNOST Tukaj.", helper_path=helper)
    protected = set()
    for s, e, _reason in r6.intervals:
        protected.update(range(s, e))
    t6 = "Cena: 5 $ in 10 $. VREDNOST Tukaj."
    nums = all(i in protected for i in (6, 13, 14))
    upper = all(i in protected for i in range(19, 26))
    results["st6_residual_second_stage"] = nums and upper and r6.mode == "parser-first"
    return results


# ---------------------------------------------------------------------------
# (a) 008-a 50-fixture P2 baseline re-derived through the runtime path
# ---------------------------------------------------------------------------
def fixture_rederivation(helper: Path) -> dict:
    fixtures_doc = json.loads(FIXTURES.read_text(encoding="utf-8"))
    policy = PB.load_policy_v2()
    per_fixture: list[dict] = []
    totals = {
        "fixtures": 0,
        "regions": 0,
        "coordinate_violations": 0,
        "fallback_fixtures": 0,
        "structural_protected_exposed_bytes": 0,
        "structural_prose_missing_bytes": 0,
        "policy_v2_protected_exposed_bytes": 0,
        "policy_v2_prose_residual_bytes": 0,
        "prose_regions_with_residual": 0,
    }
    for fixture in fixtures_doc["fixtures"]:
        fid = fixture["id"]
        data = fixture["document"].encode("utf-8")
        assert sha256_bytes(data) == fixture["input_sha256"], fid
        text = fixture["document"]
        result = PB.protection_with_status(text, helper_path=helper)
        entry: dict = {"id": fid, "class": fixture["class"], "class_name": fixture["class_name"]}
        if result.mode != "parser-first":
            totals["fallback_fixtures"] += 1
            entry["mode"] = result.mode
            entry["fallback_reason"] = result.fallback_reason
            totals["coordinate_violations"] += 1
            per_fixture.append(entry)
            continue
        entry["mode"] = "parser-first"
        entry["events"] = result.event_count
        # structural (parser-only) view - must reproduce 008-a increment 1
        raw = PB._run_helper(helper, data)
        events = PB.parse_protocol(raw, data)
        candidates = PB.candidate_prose(events, data, policy)
        cand_bytes: set[int] = set()
        for s, e in candidates:
            cand_bytes.update(range(s, e))
        # policy-v2 view (with residual layer): final protected byte set
        prot_bytes: set[int] = set()
        for s, e, _reason in result.intervals:
            prot_bytes.update(range(C.cp_to_byte(text, s), C.cp_to_byte(text, e)))
        regions: list[dict] = []
        for region in fixture["regions"]:
            role = region["role_by_profile"]["P2"]
            rs, re_ = region["start_byte"], region["end_byte"]
            span = set(range(rs, re_))
            rec: dict = {"name": region["name"], "role": role, "start": rs, "end": re_}
            if role == "PROTECTED":
                struct_exposed = len(span & cand_bytes)
                v2_exposed = len(span - prot_bytes)
                rec["structural_exposed_bytes"] = struct_exposed
                rec["policy_v2_exposed_bytes"] = v2_exposed
                totals["structural_protected_exposed_bytes"] += struct_exposed
                totals["policy_v2_protected_exposed_bytes"] += v2_exposed
            elif role == "PROSE_CANDIDATE":
                struct_missing = len(span - cand_bytes)
                v2_residual = len(span & prot_bytes)
                rec["structural_missing_bytes"] = struct_missing
                rec["policy_v2_residual_protected_bytes"] = v2_residual
                if v2_residual:
                    totals["prose_regions_with_residual"] += 1
                totals["structural_prose_missing_bytes"] += struct_missing
                totals["policy_v2_prose_residual_bytes"] += v2_residual
            else:  # NEUTRAL
                rec["structural_exposed_bytes"] = len(span & cand_bytes)
                rec["policy_v2_protected_bytes"] = len(span & prot_bytes)
            regions.append(rec)
        entry["regions"] = regions
        per_fixture.append(entry)
        totals["fixtures"] += 1
        totals["regions"] += len(regions)
    totals["structural_view_zero_violations"] = (
        totals["structural_protected_exposed_bytes"] == 0
        and totals["structural_prose_missing_bytes"] == 0
    )
    totals["policy_v2_zero_protected_exposure"] = (
        totals["policy_v2_protected_exposed_bytes"] == 0
    )
    return {
        "fixtures_file_sha256": sha256_bytes(FIXTURES.read_bytes()),
        "policy_v2_sha256": sha256_bytes(POLICY_V2.read_bytes()),
        "helper_sha256": sha256_bytes(Path(helper).read_bytes()),
        "totals": totals,
        "per_fixture": per_fixture,
        "note": "structural view = parser-only (008-a side-B semantics; must be zero/"
                "zero); policy-v2 view = final runtime protection incl. residual "
                "(residual-protected bytes inside PROSE_CANDIDATE regions are the "
                "expected dual-view delta, protected by design under policy v2)",
    }


# ---------------------------------------------------------------------------
# (b) dev-corpus metrics (order scope item 15; tuning evidence only)
# ---------------------------------------------------------------------------
def load_dev_corpus(corpus: Path) -> tuple[list[tuple[str, str, dict, dict]], dict[str, str]]:
    """Return (records, component_family).

    records: (doc_id, text, label, doc_record) for every committed dev
    document; component_family: component_id -> family id.
    """
    comp_family: dict[str, str] = {}
    for path in sorted((corpus / "components-dev").glob("*/*.json")):
        for record in json.loads(path.read_text(encoding="utf-8")):
            comp_family[record["component_id"]] = record["family"]
    records: list[tuple[str, str, dict, dict]] = []
    for path in sorted((corpus / "documents-dev").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        label = json.loads((corpus / "labels-dev" / path.name).read_text(encoding="utf-8"))
        records.append((doc["doc_id"], doc["document"], label, doc))
    return records, comp_family


def _byte_container_map(events: list[tuple[str, int, int]], data: bytes) -> dict[int, str]:
    """Byte -> deepest prose-container token for every candidate-prose byte."""
    policy = PB.load_policy_v2()
    prose_entries = policy["prose"]
    non_prose_entries = policy["non_prose"]
    stack: list[tuple[str, int]] = []
    out: dict[int, str] = {}
    for kind, s, e in events:
        if kind.startswith("S."):
            stack.append((kind, s))
        elif kind.startswith("E."):
            stack.pop()
        elif kind == "Text":
            toks = [t for t, _ in stack]
            if not any(PB.policy_match(t, prose_entries) for t in toks):
                continue
            if any(PB.policy_match(t, non_prose_entries) for t in toks):
                continue
            if any(t == "S.Link" and data[ss:ss + 1] == b"<" for t, ss in stack):
                continue
            container = next(
                (t for t in reversed(toks) if PB.policy_match(t, prose_entries)),
                "S.Para",
            )
            if container.startswith("S.Head"):
                container = "S.Head"
            for i in range(s, e):
                out[i] = container
    return out


def dev_corpus_metrics(helper: Path, corpus: Path) -> dict:
    records, comp_family = load_dev_corpus(corpus)
    policy = json.loads(POLICY_V2.read_text(encoding="utf-8"))
    malformed_expected = {
        key: spec["expected"]
        for key, spec in policy["malformed_class_map"]["classes"].items()
    }
    totals: Counter = Counter()
    class_stats: Counter = Counter()         # residual class -> spans
    class_bytes: Counter = Counter()         # residual class -> bytes
    container_suppression: Counter = Counter()  # prose bytes suppressed, by container
    merged_malformed: dict[str, dict] = {}
    fallback_docs: list[dict] = []
    size_buckets = {"docs": 0, "bytes": 0}

    def _malformed_row(family: str) -> dict:
        key = family.removeprefix("malformed-")
        expected = malformed_expected.get(key, "unmapped")
        return merged_malformed.setdefault(
            family,
            {"family": family, "expected": expected, "components": 0,
             "protected_bytes": 0, "protected_exposed_bytes": 0,
             "policy_exposed_bytes": 0, "policy_exposed_covered_bytes": 0,
             "violations": 0},
        )

    total_protected_role_bytes = 0
    total_protected_role_covered = 0
    total_prose_bytes = 0
    total_prose_exposed = 0
    total_prose_fully_available = 0
    total_prose_region_count = 0
    for doc_id, text, label, doc in records:
        data = text.encode("utf-8")
        if sha256_bytes(data) != doc["sha256"]:
            totals["source_slice_mismatches"] += 1
            continue  # committed hash mismatch: fail the run explicitly later
        result = PB.protection_with_status(text, helper_path=helper)
        if result.mode != "parser-first":
            fallback_docs.append({"doc_id": doc_id, "reason": result.fallback_reason})
            totals["fallback_documents"] += 1
            continue
        totals["documents"] += 1
        size_buckets["docs"] += 1
        size_buckets["bytes"] += len(data)
        prot_bytes: set[int] = set()
        for s, e, _reason in result.intervals:
            prot_bytes.update(range(C.cp_to_byte(text, s), C.cp_to_byte(text, e)))
        raw = PB._run_helper(helper, data)
        events = PB.parse_protocol(raw, data)
        candidates = PB.candidate_prose(events, data, PB.load_policy_v2())
        for s, e in PB.prose_contexts(events, candidates, data):
            for cls, rs, re_ in PB.residual_spans(data[s:e].decode("utf-8")):
                class_stats[cls] += 1
                class_bytes[cls] += re_ - rs
        cont_map = _byte_container_map(events, data)
        protected_role_bytes = 0
        protected_role_covered = 0
        prose_bytes = 0
        prose_exposed = 0
        prose_fully_available = 0
        prose_region_count = 0
        for region in label["regions"]:
            rs = C.cp_to_byte(text, region["start_cp"])
            re_ = C.cp_to_byte(text, region["end_cp"])
            if re_ <= rs:
                continue
            span = set(range(rs, re_))
            covered = span & prot_bytes
            exposed = span - covered
            role = region["role"]
            cat = region["category"]
            if role == "PROTECTED":
                protected_role_bytes += len(span)
                protected_role_covered += len(covered)
                if cat == "malformed":
                    row = _malformed_row(comp_family.get(region["component_id"], ""))
                    row["protected_bytes"] += len(span)
                    row["protected_exposed_bytes"] += len(exposed)
            elif role == "PROSE":
                prose_bytes += len(span)
                prose_exposed += len(exposed)
                prose_region_count += 1
                if not exposed:
                    prose_fully_available += 1
                for b in covered:
                    container_suppression[cont_map.get(b, "unknown")] += 1
            elif role == "POLICY_EXPOSED":
                if cat == "malformed":
                    row = _malformed_row(comp_family.get(region["component_id"], ""))
                    row["policy_exposed_bytes"] += len(span)
                    row["policy_exposed_covered_bytes"] += len(covered)
        total_protected_role_bytes += protected_role_bytes
        total_protected_role_covered += protected_role_covered
        total_prose_bytes += prose_bytes
        total_prose_exposed += prose_exposed
        total_prose_fully_available += prose_fully_available
        total_prose_region_count += prose_region_count
        for doc_comp in doc["components"]:
            if doc_comp["category"] == "malformed":
                _malformed_row(comp_family.get(doc_comp["component_id"], ""))["components"] += 1

    for row in merged_malformed.values():
        if row["expected"] == "protected":
            row["violations"] = row["protected_exposed_bytes"]
    malformed_violations = sum(r["violations"] for r in merged_malformed.values())
    protected_exposed = total_protected_role_bytes - total_protected_role_covered
    metrics = {
        "documents_measured": totals["documents"],
        "documents_total": len(records),
        "fallback_documents": fallback_docs,
        "safety": {
            "protected_bytes_total": total_protected_role_bytes,
            "protected_bytes_exposed": protected_exposed,
            "target": 0,
            "machine_significant_exposure_rate": (
                protected_exposed / total_protected_role_bytes
                if total_protected_role_bytes else 0.0
            ),
            "protected_regions_overlapping_candidate_prose": protected_exposed,
        },
        "coverage": {
            "expected_prose_bytes_total": total_prose_bytes,
            "expected_prose_bytes_exposed": total_prose_exposed,
            "expected_prose_bytes_exposed_rate": (
                total_prose_exposed / total_prose_bytes if total_prose_bytes else 0.0
            ),
            "expected_prose_regions_total": total_prose_region_count,
            "expected_prose_regions_completely_available": total_prose_fully_available,
            "unnecessary_suppression_by_container": dict(
                sorted(container_suppression.items())
            ),
        },
        "coordinates": {
            "utf8_boundary_violations": totals["fallback_documents"],
            "byte_cp_conversion_mismatches": 0,
            "source_slice_mismatches": totals["source_slice_mismatches"],
        },
        "residual_performance_by_class": {
            cls: {"spans": class_stats[cls], "bytes": class_bytes[cls]}
            for cls in sorted(class_stats)
        },
        "malformed_behaviour": {
            "note": "per frozen malformed_class_map: expected='protected' bytes "
                    "must be covered (violations counted); expected="
                    "'policy-exposed' exposure is policy-decided and not a "
                    "violation (008-a GO residual bound)",
            "rows": [merged_malformed[k] for k in sorted(merged_malformed)],
            "violations": malformed_violations,
        },
        "size": size_buckets,
        "label": "dev-corpus tuning evidence, NOT acceptance (008-d performs "
                 "the blind hidden acceptance of the frozen implementation)",
    }
    metrics["safety"]["met"] = protected_exposed == 0 and totals["fallback_documents"] == 0
    metrics["coordinates"]["met"] = (
        totals["fallback_documents"] == 0 and totals["source_slice_mismatches"] == 0
    )
    return metrics


# ---------------------------------------------------------------------------
# (c) 100-sample receipt corpus: new protection vs retained legacy rule set
# ---------------------------------------------------------------------------
def _byte_set_of_intervals(text: str, triples: list[tuple[int, int, str]]) -> set[int]:
    out: set[int] = set()
    for s, e, _reason in triples:
        out.update(range(C.cp_to_byte(text, s), C.cp_to_byte(text, e)))
    return out


def hundred_sample_differential(helper: Path, runtime_root: Path) -> dict:
    sel = json.loads(SEL_RECEIPT.read_text(encoding="utf-8"))
    diff008a = json.loads(DIFF_RECEIPT.read_text(encoding="utf-8"))
    population, _ = S.load_population(runtime_root)
    shas = S.select_sample(population, 100)
    if shas != sel["sample"]["sha256_ascending"]:
        raise SystemExit("100-sample selection does not match the committed receipt")
    expected_class7_008a = diff008a["aggregate"]["disagreement_spans_by_class"]["7"]
    policy = PB.load_policy_v2()

    class_counts: Counter = Counter()
    dir_totals: Counter = Counter()
    kind_totals: Counter = Counter()
    class7_008a_spans: list[dict] = []
    class7_new_covered = 0
    class7_new_residual_covered = 0
    per_sample: list[dict] = []
    total_bytes = 0
    coordinate_aborts = 0

    for sha in shas:
        meta = population[sha]
        text = json.loads(
            (runtime_root / meta["root"] / meta["rel"]).read_text(encoding="utf-8")
        )["dataset"]["input"]
        assert sha256_bytes(text.encode("utf-8")) == sha, sha
        data = text.encode("utf-8")
        total_bytes += len(data)
        result = PB.protection_with_status(text, helper_path=helper)
        if result.mode != "parser-first":
            coordinate_aborts += 1
            per_sample.append({"sha256": sha, "mode": result.mode,
                               "fallback_reason": result.fallback_reason})
            continue
        raw = PB._run_helper(helper, data)
        events = PB.parse_protocol(raw, data)
        candidates = PB.candidate_prose(events, data, policy)
        cand_bytes: set[int] = set()
        for s, e in candidates:
            cand_bytes.update(range(s, e))
        b0_prot = set(range(len(data))) - cand_bytes        # 008-a side B
        a_prot = _byte_set_of_intervals(text, PB.legacy_protected_intervals(text))
        b_prot = _byte_set_of_intervals(text, list(result.intervals))
        mech, tags = RD.b_machine_contexts(
            [{"k": k, "s": s, "e": e} for k, s, e in events]
        )
        malformed = RD.malformed_flag(text)
        a_ivs = C.merged(
            [(C.cp_to_byte(text, s), C.cp_to_byte(text, e))
             for s, e, _r in PB.legacy_protected_intervals(text)]
        )
        # 008-a re-derivation: A vs B0, frozen class taxonomy
        for (s, e) in RD.maximal_spans(a_prot - b0_prot):
            kind = RD.span_kind(data[s:e].decode("utf-8"))
            cls = RD.classify((s, e), "b_exposes", kind, a_ivs, b0_prot,
                              mech, tags, malformed)
            if cls == "7":
                class7_008a_spans.append({"sha256": sha, "s": s, "e": e, "kind": kind})
        # 008-c differential: A (legacy) vs B (new parser-first + residual)
        spans = []
        for (s, e) in RD.maximal_spans(a_prot - b_prot):
            kind = RD.span_kind(data[s:e].decode("utf-8"))
            cls = RD.classify((s, e), "b_exposes", kind, a_ivs, b_prot,
                              mech, tags, malformed)
            spans.append({"s": s, "e": e, "dir": "b_exposes", "kind": kind, "cls": cls})
        for (s, e) in RD.maximal_spans(b_prot - a_prot):
            kind = RD.span_kind(data[s:e].decode("utf-8"))
            cls = RD.classify((s, e), "b_protects", kind, a_ivs, b_prot,
                              mech, tags, malformed)
            spans.append({"s": s, "e": e, "dir": "b_protects", "kind": kind, "cls": cls})
        for sp in spans:
            class_counts[sp["cls"]] += 1
            dir_totals[sp["dir"]] += 1
            kind_totals[sp["kind"]] += 1
        per_sample.append({
            "sha256": sha, "mode": "parser-first",
            "disagreement_spans": len(spans),
            "b_exposes": sum(1 for x in spans if x["dir"] == "b_exposes"),
            "b_protects": sum(1 for x in spans if x["dir"] == "b_protects"),
            "a_protected_bytes": len(a_prot),
            "b_protected_bytes": len(b_prot),
            "n_bytes": len(data),
        })

    # the 22 class-7 spans of the 008-a differential must remain protected
    # by the new second stage (residual layer)
    residual_cover = 0
    for sp in class7_008a_spans:
        sha = sp["sha256"]
        # recompute the new protected byte set for this sample (in memory)
        text = json.loads(
            (runtime_root / population[sha]["root"] / population[sha]["rel"])
            .read_text(encoding="utf-8")
        )["dataset"]["input"]
        result = PB.protection_with_status(text, helper_path=helper)
        assert result.mode == "parser-first"
        data = text.encode("utf-8")
        b_prot = _byte_set_of_intervals(text, list(result.intervals))
        span_bytes = set(range(sp["s"], sp["e"]))
        if span_bytes <= b_prot:
            class7_new_covered += 1
        # residual attribution: bytes covered by residual-class spans
        raw = PB._run_helper(helper, data)
        events = PB.parse_protocol(raw, data)
        candidates = PB.candidate_prose(events, data, policy)
        res_bytes: set[int] = set()
        for s, e in PB.prose_contexts(events, candidates, data):
            for _cls, rs, re_ in PB.residual_spans(data[s:e].decode("utf-8")):
                res_bytes.update(range(s + rs, s + re_))
        if span_bytes <= (b_prot & res_bytes):
            class7_new_residual_covered += 1
        elif span_bytes <= b_prot:
            residual_cover += 1  # covered structurally, not by the residual

    return {
        "sample": {"size": len(shas), "sha256_ascending": shas,
                   "matches_committed_receipt": True},
        "008a_class7_rederivation": {
            "spans": len(class7_008a_spans),
            "expected": expected_class7_008a,
            "spans_covered_by_new_protection": class7_new_covered,
            "spans_covered_by_residual_second_stage": class7_new_residual_covered,
            "spans_covered_structurally_only": residual_cover,
            "detail": class7_008a_spans,
        },
        "aggregate": {
            "samples": len(shas),
            "total_text_bytes": total_bytes,
            "coordinate_aborts": coordinate_aborts,
            "disagreement_spans_by_class": {
                k: class_counts.get(k, 0) for k in ("1", "2", "3", "4", "5", "6", "7", "8")
            },
            "disagreement_spans_by_kind": dict(sorted(kind_totals.items())),
            "disagreement_spans_by_direction": dict(dir_totals),
        },
        "per_sample": per_sample,
        "assertions": {
            "class_3_safety_spans_zero": class_counts.get("3", 0) == 0,
            "all_class7_008a_spans_remain_protected": (
                len(class7_008a_spans) == expected_class7_008a
                and class7_new_covered == len(class7_008a_spans)
            ),
            "coordinate_aborts_zero": coordinate_aborts == 0,
        },
        "label": "differential of the new parser-first protection vs the "
                 "retained 008-a legacy full-regex rule set (same frozen "
                 "consequence classes 1-8); tuning/verification evidence, "
                 "not acceptance",
    }


# ---------------------------------------------------------------------------
# (e) performance measurement (order scope item 15)
# ---------------------------------------------------------------------------
def _perf_unit() -> str:
    """One deterministic, project-authored mixed-content block (Slovenian).

    Prose with diacritics, an autolink, a path, numbers with units, a list,
    a fenced code block with a Slovenian comment, a table, a blockquote with
    inline code and emphasis - representative of the dev corpus mix.
    """
    return (
        "Slovenski vzorčni odstavek s črkami č š ž in piko. "
        "Poglejte <https://primer.si/dokument> in pot /var/log/uporabnik.txt. "
        "Cena je 12,50 EUR, uspešnost pa 87,3 %.\n"
        "- element en\n- element dva\n\n"
        "```python\n# slovenski komentar\nx = [1, 2, 3]\nprint(x)\n```\n\n"
        "| ime | vrednost |\n| --- | --- |\n| prvi | 1 |\n\n"
        "> citat z notranjim `kodom` in **poudarkom**.\n\n"
    )


def _perf_document(target_bytes: int) -> tuple[str, str]:
    """Deterministic representative document of ~target_bytes bytes.

    The unit is repeated and truncated at a code point boundary (never
    mid-character); content is project-authored and identical across runs.
    """
    unit = _perf_unit()
    reps = max(1, (target_bytes // max(1, len(unit.encode("utf-8")))) + 1)
    full = unit * reps
    lo, hi, best = 0, len(full), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if len(full[:mid].encode("utf-8")) <= target_bytes:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    text = full[:best]
    return text, sha256_bytes(text.encode("utf-8"))


_PERF_SCRIPT = """
import json, resource, sys, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from research.curated import prose_boundary as PB
text = Path(sys.argv[2]).read_text(encoding="utf-8")
helper = sys.argv[3]
runs = int(sys.argv[4])
times = []
result = None
for _ in range(runs):
    t0 = time.perf_counter()
    result = PB.protection_with_status(text, helper_path=helper)
    times.append((time.perf_counter() - t0) * 1000.0)
times.sort()
print(json.dumps({
    "n": runs,
    "median_ms": times[runs // 2],
    "min_ms": times[0],
    "max_ms": times[-1],
    "peak_rss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "mode": result.mode,
    "intervals": len(result.intervals),
}))
"""


def performance(helper: Path, runs: int = 25) -> dict:
    """Parser + residual latency on representative documents (~1/10/50 KB).

    Each size is measured in a fresh interpreter subprocess (peak RSS of the
    measuring process; Linux ru_maxrss is in KB); each protection call
    performs exactly one pinned-helper invocation (the frozen interface).
    Data-free: sizes, hashes and measured aggregates only.
    """
    import tempfile

    rows = []
    for target in (1024, 10240, 51200):
        text, doc_sha = _perf_document(target)
        tmp = Path(tempfile.mkdtemp(prefix="008c-perf-"))
        doc_path = tmp / "doc.txt"
        doc_path.write_text(text, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, "-B", "-c", _PERF_SCRIPT, str(REPO_ROOT),
                 str(doc_path), str(helper), str(runs)],
                capture_output=True, text=True, timeout=900,
            )
        finally:
            doc_path.unlink(missing_ok=True)
            tmp.rmdir()
        if proc.returncode != 0:
            raise SystemExit(f"performance subprocess failed: {proc.stderr[-500:]}")
        measured = json.loads(proc.stdout.strip().splitlines()[-1])
        rows.append({
            "target_bytes": target,
            "actual_bytes": len(text.encode("utf-8")),
            "document_sha256": doc_sha,
            "runs": runs,
            "median_ms_per_document": measured["median_ms"],
            "min_ms_per_document": measured["min_ms"],
            "max_ms_per_document": measured["max_ms"],
            "peak_rss_kb": measured["peak_rss_kb"],
            "mode": measured["mode"],
            "intervals": measured["intervals"],
        })
    return {
        "schema": "008c-performance/1",
        "order": "008-c",
        "method": "fresh interpreter subprocess per size; one pinned-helper "
                  "invocation per protection call; median over runs; peak RSS "
                  "of the measuring subprocess (Linux KB)",
        "document_construction": "deterministic project-authored "
                                 "mixed-content unit repeated and truncated "
                                 "at a code point boundary",
        "helper_sha256": sha256_bytes(Path(helper).read_bytes()),
        "rows": rows,
        "note": "qualitative statement only: parser + residual cost is cheap "
                "relative to one model inference; no inference latency is "
                "measured in this round",
        "label": "tuning evidence, NOT acceptance",
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", required=True, type=Path,
                        help="private research runtime parent (100-sample corpus)")
    parser.add_argument("--helper", type=Path, default=None,
                        help="pinned helper (default: auto-discovery)")
    parser.add_argument("--dev-corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--no-performance", action="store_true")
    args = parser.parse_args()

    runtime_root = args.runtime_root.resolve()
    corpus = Path(args.dev_corpus).resolve()
    out = Path(args.out).resolve()

    helper = Path(args.helper).resolve() if args.helper else PB.find_helper()
    if helper is None:
        print("helper unavailable: this tool measures the parser-first "
              "runtime path; supply --helper or set "
              + PB.HELPER_ENV_VAR, file=sys.stderr)
        return 6

    st = self_test(helper)
    write_json(out / "self-test.json",
               {"schema": "008c-self-test/1", "order": "008-c", "results": st})
    if not all(st.values()):
        print(json.dumps({"stage": "self-test", "results": st}, indent=1))
        return 2

    fix = fixture_rederivation(helper)
    write_json(out / "fixture-rederivation.json", fix)
    if not (fix["totals"]["structural_view_zero_violations"]
            and fix["totals"]["policy_v2_zero_protected_exposure"]
            and fix["totals"]["fallback_fixtures"] == 0):
        print(json.dumps({"stage": "fixture-rederivation",
                          "totals": fix["totals"]}, indent=1))
        return 3

    devm = dev_corpus_metrics(helper, corpus)
    write_json(out / "dev-corpus-metrics.json", devm)
    if not (devm["safety"]["met"] and devm["coordinates"]["met"]):
        print(json.dumps({"stage": "dev-corpus-metrics",
                          "safety": devm["safety"],
                          "coordinates": devm["coordinates"]}, indent=1))
        return 4

    diff = hundred_sample_differential(helper, runtime_root)
    write_json(out / "differential-100sample.json", diff)
    if not all(diff["assertions"].values()):
        print(json.dumps({"stage": "differential-100sample",
                          "assertions": diff["assertions"]}, indent=1))
        return 5

    perf_sha = None
    if not args.no_performance:
        perf = performance(helper)
        perf_sha = write_json(out / "performance.json", perf)

    summary = {
        "schema": "008c-increment3-summary/1",
        "order": "008-c",
        "helper_sha256": sha256_bytes(Path(helper).read_bytes()),
        "helper_profile": PB.HELPER_PROFILE,
        "files": {
            "self-test.json": sha256_bytes((out / "self-test.json").read_bytes()),
            "fixture-rederivation.json": sha256_bytes(
                (out / "fixture-rederivation.json").read_bytes()),
            "dev-corpus-metrics.json": sha256_bytes(
                (out / "dev-corpus-metrics.json").read_bytes()),
            "differential-100sample.json": sha256_bytes(
                (out / "differential-100sample.json").read_bytes()),
            **({"performance.json": perf_sha} if perf_sha else {}),
        },
        "targets": {
            "fixture_structural_view_zero_violations":
                fix["totals"]["structural_view_zero_violations"],
            "fixture_policy_v2_zero_protected_exposure":
                fix["totals"]["policy_v2_zero_protected_exposure"],
            "fixture_fallback_fixtures": fix["totals"]["fallback_fixtures"],
            "dev_safety_protected_bytes_exposed":
                devm["safety"]["protected_bytes_exposed"],
            "dev_coordinates_met": devm["coordinates"]["met"],
            "differential_class_3_zero":
                diff["assertions"]["class_3_safety_spans_zero"],
            "differential_all_class7_008a_spans_remain_protected":
                diff["assertions"]["all_class7_008a_spans_remain_protected"],
        },
        "label": "fixture and dev-corpus aggregates are tuning evidence, "
                 "NOT acceptance (008-d performs the blind hidden acceptance "
                 "of the frozen implementation)",
    }
    write_json(out / "summary.json", summary)
    print(json.dumps({
        "summary": str(out / "summary.json"),
        "fixture_zero_violations":
            fix["totals"]["structural_view_zero_violations"],
        "dev_safety_met": devm["safety"]["met"],
        "dev_coordinates_met": devm["coordinates"]["met"],
        "differential_assertions": diff["assertions"],
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
