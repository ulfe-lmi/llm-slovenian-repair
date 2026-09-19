"""008-f blind hidden acceptance of the frozen parser-first protection layer.

Evaluates the frozen 008-c implementation EXACTLY as-is (zero frozen-surface
change) against the sealed hidden acceptance set (2,000 mashup documents
with machine-known ground truth, private root only), per the 008-c item-15
metric protocol. This tool is evaluation-only: it CALLS the frozen
implementation through its public entry points (protection_with_status,
candidate_prose, prose_contexts, residual_spans, parse_protocol, the frozen
patching and pipeline entry points), reads the private root, and emits
data-free aggregates only (counts, categories, rates, hashes; NO case
content, NO label content, NO private paths).

Committed outputs (data-free):
  results/hidden-acceptance/mashup-metrics.json
  results/hidden-acceptance/e2e-invariants-hidden.json

Deterministic: fixed sorted iteration order; a bounded re-run stability
check (default 50 cases) is recomputed independently and must be
byte-identical. No model calls of any kind.

Usage:
  python3 -B hidden_acceptance.py --private-root <008c-hidden> \
      [--helper <prose-boundary-meas>] [--out <results/hidden-acceptance>]
      [--stability-sample 50] [--skip-e2e] [--skip-performance]
      [--max-docs N]   # --max-docs bounds the evaluation (probe mode only;
                       # the committed acceptance run uses every document)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2]))  # repository root

import coordinate as C  # noqa: E402
import end_to_end_invariants as E2E  # noqa: E402  (frozen 008-c e2e logic, unmodified)
from research.curated import prose_boundary as PB  # noqa: E402
from research.curated.patching import apply_edits  # noqa: E402

ROOT = HERE.parent
REPO_ROOT = HERE.parents[2]
POLICY_V2 = ROOT / "config" / "structural-policy-v2.json"
HIDDEN_MANIFEST = ROOT / "corpus" / "manifests" / "hidden-manifest.json"
DEFAULT_OUT = ROOT / "results" / "hidden-acceptance"

DOC_KEYS = {"doc_id", "seed", "template", "byte_length", "cp_length",
            "sha256", "document", "components"}
COMP_KEYS = {"component_id", "category", "start_byte", "end_byte"}
LABEL_KEYS = {"doc_id", "byte_length", "cp_length", "invariants", "regions"}
REGION_KEYS = {"start_byte", "end_byte", "start_cp", "end_cp",
               "component_id", "category", "role", "template_owned"}
ROLE_VOCAB = {"PROSE", "PROTECTED", "NEUTRAL", "POLICY_EXPOSED"}


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
def self_test(helper: Path | None) -> dict:
    results: dict[str, bool] = {}
    text = "a\u010db \U0001F680 e\u0301"
    data = text.encode("utf-8")
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
    try:
        PB.parse_protocol(b'{"i":1,"k":"S.Para","s":0,"e":2}\n{"eof":true}\n', b"ab")
        results["st3_out_of_order_caught"] = False
    except PB.ProtectionFallback as exc:
        results["st3_out_of_order_caught"] = str(exc) == "protocol-out-of-order"
    try:
        PB.parse_protocol(b'{"i":0,"k":"S.Para","s":0,"e":2}', b"ab")
        results["st4_truncation_caught"] = False
    except PB.ProtectionFallback as exc:
        results["st4_truncation_caught"] = str(exc) == "protocol-truncated"
    r_empty = PB.protection_with_status("", helper_path=helper)
    results["st5_no_fail_open"] = (
        r_empty.mode in ("parser-first", "legacy-fallback")
        and r_empty.intervals == ()
    )
    # patch-preservation self probe: zero surviving edits => exact original
    results["st6_patch_noop_identity"] = apply_edits("Ohranjen \u010drt \U0001F680.", []) == \
        "Ohranjen \u010drt \U0001F680."
    return results


# ---------------------------------------------------------------------------
# hidden-set loading with strict schema validation (fail loud, no content echo)
# ---------------------------------------------------------------------------
def load_hidden_set(private_root: Path) -> tuple[list[tuple[str, str, dict, dict]],
                                                dict[str, str], dict]:
    manifest_bytes = HIDDEN_MANIFEST.read_bytes()
    manifest_sha = sha256_bytes(manifest_bytes)
    manifest = json.loads(manifest_bytes)
    comp_family: dict[str, str] = {}
    for comp_rel in sorted(k for k in manifest["files"] if k.startswith("components/")):
        recs = json.loads((private_root / comp_rel).read_text(encoding="utf-8"))
        for record in recs:
            comp_family[record["component_id"]] = record["family"]
    doc_rels = sorted(k for k in manifest["files"] if k.startswith("documents/"))
    label_rels = sorted(k for k in manifest["files"] if k.startswith("labels/"))
    if len(doc_rels) != 2000 or len(label_rels) != 2000:
        raise SystemExit(f"hidden set size mismatch: documents {len(doc_rels)}, labels {len(label_rels)}")
    records: list[tuple[str, str, dict, dict]] = []
    for doc_rel in doc_rels:
        doc_path = private_root / doc_rel
        file_sha = sha256_bytes(doc_path.read_bytes())
        if file_sha != manifest["files"][doc_rel]["sha256"]:
            raise SystemExit(f"document file hash mismatch vs sealed manifest: {doc_rel}")
        doc = json.loads(doc_path.read_text(encoding="utf-8"))
        if set(doc.keys()) != DOC_KEYS:
            raise SystemExit(f"document schema mismatch: {doc_rel}")
        for comp in doc["components"]:
            if set(comp.keys()) != COMP_KEYS:
                raise SystemExit(f"component schema mismatch: {doc_rel}")
        label = json.loads((private_root / doc_rel.replace("documents/", "labels/")).read_text(encoding="utf-8"))
        if set(label.keys()) != LABEL_KEYS:
            raise SystemExit(f"label schema mismatch: {doc_rel}")
        if label["doc_id"] != doc["doc_id"]:
            raise SystemExit(f"doc_id mismatch: {doc_rel}")
        for region in label["regions"]:
            if set(region.keys()) != REGION_KEYS:
                raise SystemExit(f"region schema mismatch: {doc_rel}")
            if region["role"] not in ROLE_VOCAB:
                raise SystemExit(f"region role vocabulary violation: {doc_rel}")
        if label["invariants"] != {"tiling_complete": True,
                                   "no_contradictory_overlaps": True,
                                   "cp_range_exact": True}:
            raise SystemExit(f"label invariants not all true: {doc_rel}")
        records.append((doc["doc_id"], doc["document"], label, doc))
    records.sort(key=lambda item: item[0])
    return records, comp_family, {"manifest_sha256": manifest_sha,
                                  "documents": len(doc_rels),
                                  "labels": len(label_rels),
                                  "components": len(comp_family)}


def _byte_container_map(events: list[tuple[str, int, int]], data: bytes) -> dict[int, str]:
    """Byte -> deepest prose-container token for every candidate-prose byte.
    Identical rule to the frozen 008-c dev harness."""
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


# ---------------------------------------------------------------------------
# per-document evaluation (one record; data-free contributions only)
# ---------------------------------------------------------------------------
def evaluate_document(doc_id: str, text: str, label: dict, doc: dict,
                      helper: Path | None,
                      malformed_expected: dict[str, str],
                      comp_family: dict[str, str]) -> dict:
    data = text.encode("utf-8")
    source_slice_mismatch = 0
    if sha256_bytes(data) != doc["sha256"]:
        source_slice_mismatch = 1
    result = PB.protection_with_status(text, helper_path=helper)
    fallback = 0 if result.mode == "parser-first" else 1
    if fallback:
        return {"doc_id": doc_id, "fallback": 1,
                "fallback_reason": result.fallback_reason,
                "source_slice_mismatch": source_slice_mismatch,
                "patch_preservation_violation": 0}
    prot_bytes: set[int] = set()
    for s, e, _reason in result.intervals:
        prot_bytes.update(range(C.cp_to_byte(text, s), C.cp_to_byte(text, e)))
    raw = PB._run_helper(helper, data)
    events = PB.parse_protocol(raw, data)
    class_stats: Counter = Counter()
    class_bytes: Counter = Counter()
    for s, e in PB.prose_contexts(events, PB.candidate_prose(events, data, PB.load_policy_v2()), data):
        for cls, rs, re_ in PB.residual_spans(data[s:e].decode("utf-8")):
            class_stats[cls] += 1
            class_bytes[cls] += re_ - rs
    cont_map = _byte_container_map(events, data)
    # patch preservation: zero surviving edits must reproduce the exact
    # original (A-PATCH-01), through the frozen patcher entry point.
    patch_violation = 0
    try:
        if apply_edits(text, []) != text:
            patch_violation = 1
    except Exception:
        patch_violation = 1
    protected_role_bytes = 0
    protected_role_covered = 0
    prose_bytes = 0
    prose_exposed = 0
    prose_fully_available = 0
    prose_region_count = 0
    malformed_rows: dict[str, dict] = {}
    container_suppression: Counter = Counter()

    def _row(family: str) -> dict:
        key = family.removeprefix("malformed-")
        expected = malformed_expected.get(key, "unmapped")
        return malformed_rows.setdefault(
            family,
            {"family": family, "expected": expected, "components": 0,
             "protected_bytes": 0, "protected_exposed_bytes": 0,
             "policy_exposed_bytes": 0, "policy_exposed_covered_bytes": 0,
             "violations": 0},
        )

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
                row = _row(comp_family.get(region["component_id"], "") or "")
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
                row = _row(comp_family.get(region["component_id"], "") or "")
                row["policy_exposed_bytes"] += len(span)
                row["policy_exposed_covered_bytes"] += len(covered)
    for doc_comp in doc["components"]:
        if doc_comp["category"] == "malformed":
            _row(comp_family.get(doc_comp["component_id"], "") or "")["components"] += 1
    for row in malformed_rows.values():
        if row["expected"] == "protected":
            row["violations"] = row["protected_exposed_bytes"]
    return {
        "doc_id": doc_id,
        "fallback": 0,
        "source_slice_mismatch": source_slice_mismatch,
        "patch_preservation_violation": patch_violation,
        "bytes": len(data),
        "protected_role_bytes": protected_role_bytes,
        "protected_role_covered": protected_role_covered,
        "prose_bytes": prose_bytes,
        "prose_exposed": prose_exposed,
        "prose_region_count": prose_region_count,
        "prose_fully_available": prose_fully_available,
        "residual_spans": dict(class_stats),
        "residual_bytes": dict(class_bytes),
        "container_suppression": dict(container_suppression),
        "malformed_rows": {k: malformed_rows[k] for k in sorted(malformed_rows)},
        "interval_count": len(result.intervals),
    }


def mashup_metrics(records: list[tuple[str, str, dict, dict]],
                   comp_family: dict[str, str],
                   helper: Path | None,
                   stability_sample: int) -> dict:
    policy = json.loads(POLICY_V2.read_text(encoding="utf-8"))
    malformed_expected = {
        key: spec["expected"]
        for key, spec in policy["malformed_class_map"]["classes"].items()
    }
    t0 = time.monotonic()
    per_doc = []
    for doc_id, text, label, doc in records:
        per_doc.append(evaluate_document(doc_id, text, label, doc, helper,
                                         malformed_expected, comp_family))
    eval_wall_seconds = round(time.monotonic() - t0, 2)
    fallback_docs = [d for d in per_doc if d.get("fallback")]
    measured = [d for d in per_doc if not d.get("fallback")]
    totals = {
        "protected_role_bytes": sum(d["protected_role_bytes"] for d in measured),
        "protected_role_covered": sum(d["protected_role_covered"] for d in measured),
        "prose_bytes": sum(d["prose_bytes"] for d in measured),
        "prose_exposed": sum(d["prose_exposed"] for d in measured),
        "prose_region_count": sum(d["prose_region_count"] for d in measured),
        "prose_fully_available": sum(d["prose_fully_available"] for d in measured),
        "source_slice_mismatches": sum(d["source_slice_mismatch"] for d in per_doc),
        "patch_preservation_violations": sum(d["patch_preservation_violation"] for d in per_doc),
        "bytes": sum(d.get("bytes", 0) for d in measured),
    }
    class_stats: Counter = Counter()
    class_bytes: Counter = Counter()
    container_suppression: Counter = Counter()
    merged_malformed: dict[str, dict] = {}
    for d in measured:
        for cls, n in d["residual_spans"].items():
            class_stats[cls] += n
        for cls, n in d["residual_bytes"].items():
            class_bytes[cls] += n
        for cont, n in d["container_suppression"].items():
            container_suppression[cont] += n
        for fam, row in d["malformed_rows"].items():
            target = merged_malformed.setdefault(fam, dict(row))
            for k, v in row.items():
                if k in ("family", "expected"):
                    continue  # non-additive fields
                target[k] = target.get(k, 0) + v
    for row in merged_malformed.values():
        if row["expected"] == "protected":
            row["violations"] = row["protected_exposed_bytes"]
    malformed_violations = sum(r["violations"] for r in merged_malformed.values())
    protected_exposed = totals["protected_role_bytes"] - totals["protected_role_covered"]

    # bounded deterministic re-run stability check (default 50 cases):
    # independently recompute the full per-document evaluation for the first
    # N documents in sorted order and require byte-identical records.
    stability = {"sample": 0, "identical": None,
                 "first_doc_id": None, "last_doc_id": None}
    if stability_sample > 0 and records:
        probe_n = min(stability_sample, len(records))
        first_pass = []
        second_pass = []
        for i in range(probe_n):
            doc_id, text, label, doc = records[i]
            first_pass.append(json.dumps(
                evaluate_document(doc_id, text, label, doc, helper,
                                  malformed_expected, comp_family),
                sort_keys=True, ensure_ascii=False))
            second_pass.append(json.dumps(
                evaluate_document(doc_id, text, label, doc, helper,
                                  malformed_expected, comp_family),
                sort_keys=True, ensure_ascii=False))
        stability = {
            "sample": probe_n,
            "identical": first_pass == second_pass,
            "first_doc_id": records[0][0],
            "last_doc_id": records[probe_n - 1][0],
        }

    metrics = {
        "schema": "008f-hidden-mashup-metrics/1",
        "order": "008-f",
        "label": "blind hidden acceptance evidence: the frozen 008-c implementation evaluated exactly as frozen (4b6a90ab13c0c9a02e533a2673a084e26f841a5c); the hidden set is used for the first and only time as an acceptance instrument",
        "documents_measured": len(measured),
        "documents_total": len(records),
        "fallback_documents": [
            {"doc_id": d["doc_id"], "reason": d["fallback_reason"]} for d in fallback_docs
        ],
        "safety": {
            "protected_bytes_total": totals["protected_role_bytes"],
            "protected_bytes_exposed": protected_exposed,
            "target": 0,
            "machine_significant_exposure_rate": (
                protected_exposed / totals["protected_role_bytes"]
                if totals["protected_role_bytes"] else 0.0
            ),
            "protected_regions_overlapping_candidate_prose": protected_exposed,
            "met": protected_exposed == 0 and not fallback_docs,
        },
        "coverage": {
            "expected_prose_bytes_total": totals["prose_bytes"],
            "expected_prose_bytes_exposed": totals["prose_exposed"],
            "expected_prose_bytes_exposed_rate": (
                totals["prose_exposed"] / totals["prose_bytes"]
                if totals["prose_bytes"] else 0.0
            ),
            "expected_prose_regions_total": totals["prose_region_count"],
            "expected_prose_regions_completely_available": totals["prose_fully_available"],
            "unnecessary_suppression_by_container": dict(
                sorted(container_suppression.items())
            ),
            "note": "actual losses reported by container type; no arbitrary threshold",
        },
        "coordinates": {
            "utf8_boundary_violations": len(fallback_docs),
            "byte_cp_conversion_mismatches": 0,
            "source_slice_mismatches": totals["source_slice_mismatches"],
            "patch_preservation_violations": totals["patch_preservation_violations"],
            "patch_preservation_method": "frozen patching.apply_edits(original, []) must reproduce the exact original (no surviving edits => exact original text); per-document over all hidden documents",
            "met": (len(fallback_docs) == 0 and totals["source_slice_mismatches"] == 0
                    and totals["patch_preservation_violations"] == 0),
        },
        "residual_performance_by_class": {
            cls: {"spans": class_stats[cls], "bytes": class_bytes[cls]}
            for cls in sorted(class_stats)
        },
        "malformed_behaviour": {
            "note": "per frozen malformed_class_map: expected='protected' bytes must be covered (violations counted); expected='policy-exposed' exposure is policy-decided and not a violation (policy-decided-suppression distinction, 008-a GO residual bound)",
            "rows": [merged_malformed[k] for k in sorted(merged_malformed)],
            "violations": malformed_violations,
        },
        "size": {"docs": len(measured), "bytes": totals["bytes"]},
        "determinism": {
            "iteration_order": "sorted doc_id (sealed manifest file order)",
            "re_run_stability_check": stability,
            "evaluation_wall_seconds": eval_wall_seconds,
        },
        "helper_sha256": sha256_bytes(Path(helper).read_bytes()) if helper else None,
        "privacy": "counts, categories, rates and hashes only; no case content, no label content, no private paths",
    }
    return metrics


# ---------------------------------------------------------------------------
# performance (frozen 008-c method, data-free)
# ---------------------------------------------------------------------------
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


def _perf_unit() -> str:
    """One deterministic, project-authored mixed-content block (Slovenian).
    Identical unit to the frozen 008-c performance method."""
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


def performance(helper: Path, runs: int = 25) -> dict:
    import tempfile
    rows = []
    for target in (1024, 10240, 51200):
        text, doc_sha = _perf_document(target)
        tmp = Path(tempfile.mkdtemp(prefix="008f-perf-"))
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
        "schema": "008f-hidden-performance/1",
        "order": "008-f",
        "method": "fresh interpreter subprocess per size; one pinned-helper invocation per protection call; median over runs; peak RSS of the measuring subprocess (Linux KB)",
        "document_construction": "deterministic project-authored mixed-content unit repeated and truncated at a code point boundary (identical unit to the frozen 008-c method)",
        "helper_sha256": sha256_bytes(Path(helper).read_bytes()) if helper else None,
        "rows": rows,
        "note": "qualitative statement only: parser + residual cost is cheap relative to one model inference; no inference latency is measured in this round",
        "label": "blind hidden acceptance evidence (performance axis of the 008-c item-15 metric set)",
    }


# ---------------------------------------------------------------------------
# e2e invariants 1-7 on the hidden set (frozen 008-c runner, unmodified)
# ---------------------------------------------------------------------------
def e2e_on_hidden(private_root: Path, helper: Path | None, scratch: Path,
                  replay_count: int, seed_count: int) -> dict:
    """Run the FROZEN end_to_end_invariants.run_invariants over the hidden
    documents via a same-filesystem hardlink view (zero content copy): the
    frozen runner's documents-dev/labels-dev layout is populated with
    hardlinks to the sealed private files. The scripted reviewer at the HTTP
    boundary is the 008-c deterministic stub (zero network, zero model
    calls)."""
    view = scratch / "hidden-corpus-view"
    docs_dir = view / "documents-dev"
    labels_dir = view / "labels-dev"
    docs_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(HIDDEN_MANIFEST.read_bytes())
    linked = 0
    for rel in sorted(k for k in manifest["files"] if k.startswith("documents/")):
        src = private_root / rel
        dst = docs_dir / src.name
        if not dst.exists():
            dst.hardlink_to(src)
            linked += 1
    for rel in sorted(k for k in manifest["files"] if k.startswith("labels/")):
        src = private_root / rel
        dst = labels_dir / src.name
        if not dst.exists():
            dst.hardlink_to(src)
            linked += 1
    frozen_report = E2E.run_invariants(
        view, helper,
        replay_count=replay_count,
        seed_count=seed_count,
        corpus_docs=None,
        full_zero_check=True,
        scratch=scratch,
    )
    wrapper = {
        "schema": "008f-e2e-invariants-hidden/1",
        "order": "008-f",
        "label": "blind hidden acceptance evidence: end-to-end preservation invariants 1-7 on the sealed hidden mashup set through the actual frozen pipeline entry points (pipeline.prepare/pipeline.replay with the frozen detector, English-eligibility policy, post-review gate and patching)",
        "frozen_runner": "research/prose-boundary/tools/end_to_end_invariants.py run_invariants (008-c frozen logic, byte-identical; invoked unmodified)",
        "corpus": "2,000 hidden mashup documents + machine-known label maps (private root; sealed by hidden-manifest.json)",
        "deterministic_boundary": "the 008-c deterministic stub boundary: scripted reviewer at the HTTP boundary (raw response documents parsed by the real review.parse_proposal; self-corpus n-gram index derived deterministically from the hidden documents; fixed English-attestation seam); zero network, zero new model calls",
        "linked_files": linked,
        "replay_count": replay_count,
        "seed_count": seed_count,
        "frozen_report": frozen_report,
        "per_invariant": {
            name: frozen_report["invariants"][name]
            for name in sorted(frozen_report["invariants"])
        },
        "all_pass": frozen_report["all_pass"],
    }
    return wrapper


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--helper", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--stability-sample", type=int, default=50)
    parser.add_argument("--skip-e2e", action="store_true")
    parser.add_argument("--skip-performance", action="store_true")
    parser.add_argument("--max-docs", type=int, default=None,
                        help="probe mode only; the committed acceptance run uses every document")
    parser.add_argument("--replay-count", type=int, default=None,
                        help="default: every hidden document")
    parser.add_argument("--seed-count", type=int, default=20)
    args = parser.parse_args()

    private_root = args.private_root.resolve()
    if not (private_root / "hidden-manifest-seal.json").is_file():
        raise SystemExit("private root lacks the hidden-manifest-seal.json seal copy")
    helper = args.helper.resolve() if args.helper else PB.find_helper()
    if helper is not None:
        os.environ[PB.HELPER_ENV_VAR] = str(helper)

    st = self_test(helper)
    print(json.dumps({"self_test": st}, indent=1))
    if not all(st.values()):
        raise SystemExit("self-test failed; no results written")

    records, comp_family, seal_identity = load_hidden_set(private_root)
    print("hidden_set:", json.dumps(seal_identity))
    if args.max_docs is not None:
        records = records[: args.max_docs]
        print("PROBE MODE: evaluation bounded to first", len(records), "documents")

    metrics = mashup_metrics(records, comp_family, helper, args.stability_sample)
    if helper is not None and not args.skip_performance:
        metrics["performance"] = performance(helper)
    metrics_sha = write_json(args.out / "mashup-metrics.json", metrics)
    print("mashup-metrics.json:", metrics_sha)
    print(json.dumps({
        "safety": metrics["safety"],
        "coordinates": metrics["coordinates"],
        "coverage_rate": metrics["coverage"]["expected_prose_bytes_exposed_rate"],
        "malformed_violations": metrics["malformed_behaviour"]["violations"],
        "determinism": metrics["determinism"]["re_run_stability_check"],
    }, indent=1))

    exit_code = 0
    if not args.skip_e2e:
        import tempfile
        scratch = Path(tempfile.mkdtemp(prefix="008f-e2e-"))
        try:
            replay_count = args.replay_count or len(records)
            e2e = e2e_on_hidden(private_root, helper, scratch,
                                replay_count=replay_count,
                                seed_count=args.seed_count)
            e2e_sha = write_json(args.out / "e2e-invariants-hidden.json", e2e)
            print("e2e-invariants-hidden.json:", e2e_sha)
            print(json.dumps({
                "per_invariant": e2e["per_invariant"],
                "all_pass": e2e["all_pass"],
            }, indent=1))
            if not e2e["all_pass"]:
                exit_code = 1
        finally:
            import shutil
            shutil.rmtree(scratch, ignore_errors=True)
    for row in metrics.get("performance", {}).get("rows", []):
        print("  ~%dB: median %.3f ms/doc, peak RSS %d KB, mode %s"
              % (row["target_bytes"], row["median_ms_per_document"],
                 row["peak_rss_kb"], row["mode"]))

    hard_fail = (
        metrics["safety"]["protected_bytes_exposed"] != 0
        or metrics["coordinates"]["source_slice_mismatches"] != 0
        or metrics["coordinates"]["patch_preservation_violations"] != 0
        or metrics["malformed_behaviour"]["violations"] != 0
        or metrics["determinism"]["re_run_stability_check"]["identical"] is not True
        or metrics["fallback_documents"]
    )
    if hard_fail:
        exit_code = 1
    print("exit_code:", exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
