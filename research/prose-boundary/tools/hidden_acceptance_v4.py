"""008-i v4 hidden evaluation wrapper (thin, disclosed - order requirement 9).

The committed 008-f harness (tools/hidden_acceptance.py) hardcodes its v1
identity (the v1 manifest path and the v2 policy path as module globals), so
it cannot be pointed at the new sealed v4 set through its existing
parameters. This wrapper IMPORTS the 008-f harness UNMODIFIED (byte-identity
of the harness file is asserted against the committed git blob up front) and
re-points its two module-level identity globals at call time:

  HIDDEN_MANIFEST -> research/prose-boundary/corpus/manifests/hidden-manifest-v4.json
  POLICY_V2       -> research/prose-boundary/config/structural-policy-v5.json
                     (v5 = policy of record; its malformed_class_map is
                     byte-identical to the committed v3 map, which is what
                     the runtime residual layer loads; the re-point only
                     changes the harness' expected-map source)

The v4 set uses the 008-i builder schema (identical to the v3 builder
schema: composition_provenance with the 008-i guard/provenance fields,
label_source split), so this wrapper carries its OWN loader (the frozen
harness loader is NOT reused for loading):
  DOC_KEYS   = frozen keys + composition_provenance (R1/R2/T6 guard +
               provenance record)
  REGION_KEYS = frozen keys + label_source (construction / oracle-refined)
  with vocabulary checks, per-file hash checks against the sealed manifest,
  and the invariant assertions (2,000 documents).

The frozen harness functions run verbatim over the loaded records:
self-test, the full item-15 mashup metrics (safety, coordinates, coverage,
residual performance, malformed behaviour, determinism re-run stability
check), the performance axis, and the frozen 008-c e2e invariants runner
over a hardlink view of the sealed v4 documents.

008-h additions (order requirement 9 + the 008-g D1-4 registration), carried
unchanged in design:

  * label-source split: a second PB.protection_with_status pass per
    document splits every PROTECTED region's bytes by label_source.
    Construction-labeled protected bytes are the HARD safety axis
    (zero tolerance); oracle-refined protected bytes are reported as a
    policy-coverage census with the circularity limitation disclosed
    (the label oracle is the implementation's own residual function).
    The split totals are cross-checked against the raw harness record
    (protected_role_bytes / protected_role_covered; must reconcile
    exactly).

  * malformed policy-exposed row totals are INDEPENDENTLY RECOMPUTED from
    the sealed v4 labels (per family: protected / policy-exposed bytes and
    covered bytes). The frozen harness' merged_malformed aggregation
    carries the known 008-f first-document double-count defect (the first
    contributing document's row is seeded AND added, disclosed in 008-g:
    +7 B on v2). The recomputation asserts
    raw - (recomputed_true + first_document_contribution) == 0 per family
    (delta 0 required) and reports the raw frozen-harness rows, the
    recomputed true values, and the first-document contribution.

Implementation freeze: the exact four-file census (v3+v5) recorded in
experiment-008i.json is asserted against the working tree before any result
is produced.

Hard gate (order requirement 7): the driver refuses to run until the v4
seal state is committed AND strategy-verified; the strategy receipt
identity is recorded (filename + sha256 + size; the receipt must cite the
v4 manifest sha256). No private paths are committed.

Committed outputs (one data-free aggregate per axis, explicitly labelled):
  results/hidden-acceptance-v4/mashup-metrics-v4.json
  results/hidden-acceptance-v4/e2e-invariants-hidden-v4.json

Deterministic: fixed sorted iteration order; the frozen harness' bounded
50-case re-run stability check is carried in the raw output and must be
byte-identical. No model calls of any kind.

Usage:
  python3 -B hidden_acceptance_v4.py --private-root <008i-hidden> \
      --strategy-verification <strategy v4 seal-verification receipt> \
      [--helper <prose-boundary-meas>] [--stability-sample 50] \
      [--skip-e2e] [--skip-performance] [--replay-count N] [--seed-count N]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2]))  # repository root

import hidden_acceptance as HA  # noqa: E402  (frozen 008-f harness, imported unmodified)
from research.curated import prose_boundary as PB  # noqa: E402

ROOT = HERE.parent
REPO_ROOT = HERE.parents[2]
V4_MANIFEST = ROOT / "corpus" / "manifests" / "hidden-manifest-v4.json"
SEAL_VERIFICATION_V4 = ROOT / "corpus" / "manifests" / "seal-verification-v4.json"
POLICY_V5 = ROOT / "config" / "structural-policy-v5.json"
EXPERIMENT_CONFIG = ROOT / "config" / "experiment-008i.json"
HARNESS_FILE = HERE / "hidden_acceptance.py"
DEFAULT_OUT = ROOT / "results" / "hidden-acceptance-v4"

# additive fields of a malformed family row (the frozen harness merges
# these field-wise; "family"/"expected" are non-additive, "violations" is
# derived from protected_exposed_bytes and is not checked independently)
ADDITIVE = ("components", "protected_bytes", "protected_exposed_bytes",
            "policy_exposed_bytes", "policy_exposed_covered_bytes")

# v4 loader key sets: frozen vocabulary + the 008-h additions (schema
# carried unchanged by the 008-i builder)
DOC_KEYS_V4 = HA.DOC_KEYS | {"composition_provenance"}
# the 008-i builder provenance record (three guards + the R1 record):
# R1 (extended to all HTML block-start lines), the display-dollar
# adjacency guard, the T6 clean-URL admission refinement
PROVENANCE_KEYS = {"r1_blank_line_insertions", "r1_contract",
                   "display_dollar_barrier_insertions",
                   "display_dollar_guard_contract",
                   "t6_link_destination_admission"}
REGION_KEYS_V4 = HA.REGION_KEYS | {"label_source"}
LABEL_SOURCE_VOCAB = {"construction", "oracle-refined"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(rel: str) -> str:
    out = subprocess.run(["git", "-C", str(REPO_ROOT), "show", f"HEAD:{rel}"],
                         capture_output=True, check=True).stdout
    return sha256_bytes(out)


def implementation_census() -> dict:
    """The four-file runtime protection census (the 008-i identity:
    v3+v5 policies; identical shape to the committed dev-regression
    implementation_census and to the frozen protection identity in
    experiment-008i.json)."""
    files = {
        "research/curated/prose_boundary.py":
            (REPO_ROOT / "research/curated/prose_boundary.py").read_bytes(),
        "research/curated/protected.py":
            (REPO_ROOT / "research/curated/protected.py").read_bytes(),
        "research/prose-boundary/config/structural-policy-v3.json":
            (REPO_ROOT / "research/prose-boundary/config/structural-policy-v3.json").read_bytes(),
        "research/prose-boundary/config/structural-policy-v5.json":
            (REPO_ROOT / "research/prose-boundary/config/structural-policy-v5.json").read_bytes(),
    }
    return {k: sha256_bytes(v) for k, v in sorted(files.items())}


# ---------------------------------------------------------------------------
# v4 loader (own schema; the frozen harness loader is not reused for loading)
# ---------------------------------------------------------------------------
def load_v4_set(private_root: Path):
    """Sealed v4 set loading with strict v4 schema validation (fail loud,
    no content echo). Mirrors the frozen harness loader with the 008-h/008-i
    additions: composition_provenance on documents, label_source on
    regions, plus vocabulary checks."""
    manifest_bytes = V4_MANIFEST.read_bytes()
    manifest_sha = sha256_bytes(manifest_bytes)
    manifest = json.loads(manifest_bytes)
    if manifest.get("schema") != "008i-hidden-manifest-v4/1":
        raise SystemExit(f"v4 manifest schema mismatch: {manifest.get('schema')!r}")
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
        if set(doc.keys()) != DOC_KEYS_V4:
            raise SystemExit(f"document schema mismatch: {doc_rel}")
        if set(doc["composition_provenance"].keys()) != PROVENANCE_KEYS:
            raise SystemExit(f"composition_provenance schema mismatch: {doc_rel}")
        if not isinstance(doc["composition_provenance"]["r1_blank_line_insertions"], int):
            raise SystemExit(f"r1_blank_line_insertions not an int: {doc_rel}")
        if not isinstance(doc["composition_provenance"]["display_dollar_barrier_insertions"], int):
            raise SystemExit(f"display_dollar_barrier_insertions not an int: {doc_rel}")
        for comp in doc["components"]:
            if set(comp.keys()) != HA.COMP_KEYS:
                raise SystemExit(f"component schema mismatch: {doc_rel}")
        label = json.loads((private_root / doc_rel.replace("documents/", "labels/")).read_text(encoding="utf-8"))
        if set(label.keys()) != HA.LABEL_KEYS:
            raise SystemExit(f"label schema mismatch: {doc_rel}")
        if label["doc_id"] != doc["doc_id"]:
            raise SystemExit(f"doc_id mismatch: {doc_rel}")
        for region in label["regions"]:
            if set(region.keys()) != REGION_KEYS_V4:
                raise SystemExit(f"region schema mismatch: {doc_rel}")
            if region["role"] not in HA.ROLE_VOCAB:
                raise SystemExit(f"region role vocabulary violation: {doc_rel}")
            if region["label_source"] not in LABEL_SOURCE_VOCAB:
                raise SystemExit(f"region label_source vocabulary violation: {doc_rel}")
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


# ---------------------------------------------------------------------------
# 008-h addition 1 (carried): label-source split (second protection pass)
# ---------------------------------------------------------------------------
def label_source_split(records, helper) -> dict:
    """Independent per-document re-run of the frozen implementation's
    protection function. Splits every PROTECTED region's bytes by
    label_source; construction = the hard safety axis (zero tolerance),
    oracle-refined = policy-coverage census (circularity disclosed)."""
    import coordinate as C
    per_doc = []
    totals = {"construction_bytes": 0, "construction_covered": 0,
              "oracle_refined_bytes": 0, "oracle_refined_covered": 0,
              "protected_bytes": 0, "protected_covered": 0,
              "fallback_documents": []}
    for doc_id, text, label, _doc in records:
        result = PB.protection_with_status(text, helper_path=helper)
        if result.mode != "parser-first":
            totals["fallback_documents"].append({"doc_id": doc_id,
                                                 "reason": result.fallback_reason})
            continue
        prot: set[int] = set()
        for s, e, _reason in result.intervals:
            prot.update(range(C.cp_to_byte(text, s), C.cp_to_byte(text, e)))
        row = {"doc_id": doc_id,
               "construction_bytes": 0, "construction_covered": 0,
               "oracle_refined_bytes": 0, "oracle_refined_covered": 0}
        for region in label["regions"]:
            if region["role"] != "PROTECTED":
                continue
            rs = C.cp_to_byte(text, region["start_cp"])
            re_ = C.cp_to_byte(text, region["end_cp"])
            if re_ <= rs:
                continue
            span = range(rs, re_)
            covered = sum(1 for b in span if b in prot)
            key = "construction" if region["label_source"] == "construction" else "oracle_refined"
            row[f"{key}_bytes"] += re_ - rs
            row[f"{key}_covered"] += covered
        per_doc.append(row)
        for k in ("construction_bytes", "construction_covered",
                  "oracle_refined_bytes", "oracle_refined_covered"):
            totals[k] += row[k]
        totals["protected_bytes"] += row["construction_bytes"] + row["oracle_refined_bytes"]
        totals["protected_covered"] += row["construction_covered"] + row["oracle_refined_covered"]
    totals["construction_exposed"] = (totals["construction_bytes"]
                                      - totals["construction_covered"])
    totals["oracle_refined_exposed"] = (totals["oracle_refined_bytes"]
                                        - totals["oracle_refined_covered"])
    totals["document_rows"] = per_doc
    return totals


# ---------------------------------------------------------------------------
# 008-h addition 2 (carried): malformed policy-exposed row recomputation
# ---------------------------------------------------------------------------
def malformed_recomputation(records, comp_family, helper, raw_rows) -> dict:
    """Independently recompute the malformed row totals (protected /
    policy-exposed bytes and covered bytes, per family) from the sealed v4
    labels. The frozen harness' merged_malformed aggregation seeds each
    family's merged row from the FIRST document that contributes to THAT
    FAMILY (setdefault(fam, dict(row)) in record order over the measured,
    non-fallback documents) and then adds that same document's contribution
    again (008-f defect, disclosed in 008-g: +7 B on v2). Therefore, per
    family:
        raw_family == true_family + first_contributing_document_contribution_family
    where the first contributing document is the first non-fallback record
    (sorted doc_id order, the harness' measured order) with a malformed row
    entry for that family (a malformed PROTECTED/POLICY_EXPOSED region or a
    malformed component), NOT the first document of the set. Delta 0 is
    required on the explained residual and no fallback documents are
    permitted; both the raw frozen-harness rows and the recomputed true
    values are reported."""
    import coordinate as C
    true_vals: dict[str, dict] = {}
    first_contrib: dict[str, dict] = {}
    first_contrib_doc: dict[str, str] = {}
    seeded: set[str] = set()
    fallback_documents_skipped: list[dict] = []

    def _zeros(family: str) -> dict:
        return {"family": family, "components": 0, "protected_bytes": 0,
                "protected_exposed_bytes": 0, "policy_exposed_bytes": 0,
                "policy_exposed_covered_bytes": 0}

    for doc_id, text, label, doc in records:
        result = PB.protection_with_status(text, helper_path=helper)
        if result.mode != "parser-first":
            fallback_documents_skipped.append(
                {"doc_id": doc_id, "reason": result.fallback_reason})
            continue
        prot: set[int] = set()
        for s, e, _reason in result.intervals:
            prot.update(range(C.cp_to_byte(text, s), C.cp_to_byte(text, e)))
        # per-document contribution rows, mirroring the frozen harness'
        # evaluate_document malformed_rows construction exactly
        doc_rows: dict[str, dict] = {}

        def _row(family: str) -> dict:
            return doc_rows.setdefault(family, _zeros(family))

        for region in label["regions"]:
            if region["category"] != "malformed":
                continue
            role = region["role"]
            if role not in ("PROTECTED", "POLICY_EXPOSED"):
                continue
            family = comp_family.get(region["component_id"], "") or ""
            rs = C.cp_to_byte(text, region["start_cp"])
            re_ = C.cp_to_byte(text, region["end_cp"])
            if re_ <= rs:
                continue
            covered = sum(1 for b in range(rs, re_) if b in prot)
            n = re_ - rs
            row = _row(family)
            if role == "PROTECTED":
                row["protected_bytes"] += n
                row["protected_exposed_bytes"] += n - covered
            else:
                row["policy_exposed_bytes"] += n
                row["policy_exposed_covered_bytes"] += covered
        for comp in doc["components"]:
            if comp["category"] == "malformed":
                _row(comp_family.get(comp["component_id"]) or "")["components"] += 1

        for fam, contrib in doc_rows.items():
            trow = true_vals.setdefault(fam, _zeros(fam))
            for k in ADDITIVE:
                trow[k] += contrib[k]
            if fam not in seeded:
                seeded.add(fam)
                first_contrib[fam] = dict(contrib)
                first_contrib_doc[fam] = doc_id

    rows_out = []
    explained_delta_ok = True
    for raw_row in raw_rows:
        fam = raw_row["family"]
        true_row = true_vals.get(fam, _zeros(fam))
        first_row = first_contrib.get(fam, _zeros(fam))
        deltas = {}
        for k in ADDITIVE:
            explained = raw_row.get(k, 0) - (true_row[k] + first_row[k])
            deltas[k] = explained
            if explained != 0:
                explained_delta_ok = False
        rows_out.append({
            "family": fam,
            "expected": raw_row["expected"],
            "raw_frozen_harness_row": {k: raw_row[k] for k in ADDITIVE},
            "recomputed_true_from_sealed_labels": {k: true_row[k] for k in ADDITIVE},
            "first_contributing_document_id": first_contrib_doc.get(fam),
            "first_contributing_document_contribution": {k: first_row[k] for k in ADDITIVE},
            "explained_delta_raw_minus_true_minus_first": deltas,
        })
    for fam in sorted(set(true_vals) - {r["family"] for r in raw_rows}):
        rows_out.append({
            "family": fam,
            "expected": "unmapped",
            "raw_frozen_harness_row": None,
            "recomputed_true_from_sealed_labels":
                {k: true_vals[fam][k] for k in ADDITIVE},
            "first_contributing_document_id": first_contrib_doc.get(fam),
            "first_contributing_document_contribution":
                {k: first_contrib.get(fam, _zeros(fam))[k] for k in ADDITIVE},
            "explained_delta_raw_minus_true_minus_first": None,
            "note": "family present in sealed labels but absent from the raw rows",
        })
    return {
        "rule": ("raw_frozen_harness_row - recomputed_true_from_sealed_labels "
                 "- first_contributing_document_contribution == 0 per "
                 "additive field per family (delta 0 required); the residual "
                 "is the known frozen-harness first-contributing-document "
                 "double-count defect (008-f; disclosed in 008-g: +7 B on "
                 "v2); the seed is the first non-fallback record, in sorted "
                 "doc_id order, that contributes to the family; no fallback "
                 "documents are permitted"),
        "delta_0_satisfied": bool(explained_delta_ok
                                  and not fallback_documents_skipped),
        "fallback_documents_skipped": fallback_documents_skipped,
        "rows": rows_out,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--strategy-verification", required=True, type=Path,
                        help="strategy's data-free v4 seal verification receipt "
                             "(workorder in the supervision tree); its identity is "
                             "recorded, no private paths are committed")
    parser.add_argument("--helper", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--stability-sample", type=int, default=50)
    parser.add_argument("--skip-e2e", action="store_true")
    parser.add_argument("--skip-performance", action="store_true")
    parser.add_argument("--replay-count", type=int, default=None,
                        help="default: every v4 hidden document")
    parser.add_argument("--seed-count", type=int, default=20)
    args = parser.parse_args()

    # -- fail-closed pre-run guards -----------------------------------------
    harness_sha = sha256_bytes(HARNESS_FILE.read_bytes())
    harness_blob = git_blob_sha("research/prose-boundary/tools/hidden_acceptance.py")
    if harness_sha != harness_blob:
        raise SystemExit("008-f harness bytes differ from the committed blob; "
                         "the frozen surface is not byte-identical")

    if not V4_MANIFEST.is_file() or not SEAL_VERIFICATION_V4.is_file():
        raise SystemExit("v4 seal state not committed (manifest / seal-verification missing)")
    seal_ver = json.loads(SEAL_VERIFICATION_V4.read_text(encoding="utf-8"))
    if seal_ver.get("status") != "SEALED":
        raise SystemExit(f"committed seal-verification-v4 status is {seal_ver.get('status')!r}")
    if seal_ver.get("schema") != "008i-seal-verification-v4/1":
        raise SystemExit(f"committed seal-verification-v4 schema is {seal_ver.get('schema')!r}")
    v4_manifest_sha = sha256_bytes(V4_MANIFEST.read_bytes())
    if v4_manifest_sha != seal_ver.get("manifest_sha256"):
        raise SystemExit("committed v4 manifest bytes differ from the sealed identity")

    receipt_path = args.strategy_verification
    if not receipt_path.is_file() or receipt_path.stat().st_size == 0:
        raise SystemExit("strategy v4 seal verification receipt missing or empty; "
                         "the evaluation phase is gated on strategy verification")
    receipt_text = receipt_path.read_text(encoding="utf-8", errors="replace")
    receipt = {
        "filename": receipt_path.name,
        "sha256": sha256_bytes(receipt_path.read_bytes()),
        "size": receipt_path.stat().st_size,
        "location": "strategy workorders (supervision tree); path not committed",
        "cites_v4_manifest_sha256": v4_manifest_sha in receipt_text,
    }
    if not receipt["cites_v4_manifest_sha256"]:
        raise SystemExit("strategy receipt does not cite the v4 manifest sha256")
    print("strategy_verification:", json.dumps(receipt))

    exp = json.loads(EXPERIMENT_CONFIG.read_text(encoding="utf-8"))
    census = implementation_census()
    expected_census = exp.get("implementation", {}).get("frozen_census", {})
    if expected_census and expected_census != census:
        raise SystemExit("implementation bytes differ from the frozen protection "
                         "identity recorded in experiment-008i.json")

    # -- re-point the frozen harness identity globals (disclosed) ------------
    HA.HIDDEN_MANIFEST = V4_MANIFEST
    HA.POLICY_V2 = POLICY_V5

    private_root = args.private_root.resolve()
    if not (private_root / "hidden-manifest-seal.json").is_file():
        raise SystemExit("private root lacks the hidden-manifest-seal.json seal copy")
    helper = args.helper.resolve() if args.helper else PB.find_helper()
    if helper is not None:
        os.environ[PB.HELPER_ENV_VAR] = str(helper)

    st = HA.self_test(helper)
    print(json.dumps({"self_test": st}, indent=1))
    if not all(st.values()):
        raise SystemExit("self-test failed; no results written")

    records, comp_family, seal_identity = load_v4_set(private_root)
    print("hidden_set:", json.dumps(seal_identity))

    metrics = HA.mashup_metrics(records, comp_family, helper, args.stability_sample)
    if helper is not None and not args.skip_performance:
        metrics["performance"] = HA.performance(helper)
    raw_metrics_sha = sha256_bytes(
        (json.dumps(metrics, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))

    # -- 008-h additions (independent passes over the sealed set) ------------
    split = label_source_split(records, helper)
    raw_totals = {
        "protected_bytes": metrics["safety"]["protected_bytes_total"],
        "protected_covered": metrics["safety"]["protected_bytes_total"]
                             - metrics["safety"]["protected_bytes_exposed"],
    }
    if (split["protected_bytes"] != raw_totals["protected_bytes"]
            or split["protected_covered"] != raw_totals["protected_covered"]
            or split["fallback_documents"]
            != [{"doc_id": d["doc_id"], "reason": d["reason"]}
                for d in metrics["fallback_documents"]]):
        raise SystemExit("label-source split does not reconcile with the raw "
                         "harness record (totals or fallback documents differ)")
    raw_rows = metrics["malformed_behaviour"]["rows"]
    recomputation = malformed_recomputation(records, comp_family, helper, raw_rows)
    if not recomputation["delta_0_satisfied"]:
        raise SystemExit("malformed recomputation: explained delta != 0 for some "
                         "family (raw - true - first-document contribution)")

    exit_code = 0
    e2e_raw = None
    if not args.skip_e2e:
        scratch = Path(tempfile.mkdtemp(prefix="008i-e2e-"))
        try:
            replay_count = args.replay_count or len(records)
            e2e_raw = HA.e2e_on_hidden(private_root, helper, scratch,
                                       replay_count=replay_count,
                                       seed_count=args.seed_count)
            if not e2e_raw["all_pass"]:
                exit_code = 1
        finally:
            import shutil
            shutil.rmtree(scratch, ignore_errors=True)

    v4_identity = {
        "v4_manifest_sha256": v4_manifest_sha,
        "seal_verification_sha256": sha256_bytes(SEAL_VERIFICATION_V4.read_bytes()),
        "seal_identity": seal_identity,
        "strategy_seal_verification_receipt": receipt,
        "frozen_protection_identity": {
            "experiment_config_sha256": sha256_bytes(EXPERIMENT_CONFIG.read_bytes()),
            "census": census,
            "policy_v3_sha256": census["research/prose-boundary/config/structural-policy-v3.json"],
            "policy_v5_sha256": census["research/prose-boundary/config/structural-policy-v5.json"],
            "helper_sha256": sha256_bytes(Path(helper).read_bytes()) if helper else None,
        },
        "frozen_harness": {
            "file": "research/prose-boundary/tools/hidden_acceptance.py",
            "sha256": harness_sha,
            "committed_blob_sha256": harness_blob,
            "byte_identical": True,
            "identity_globals_repointed": {
                "HIDDEN_MANIFEST": "research/prose-boundary/corpus/manifests/hidden-manifest-v4.json",
                "POLICY_V2": "research/prose-boundary/config/structural-policy-v5.json (policy of record; malformed_class_map byte-identical to the committed v3 map the runtime loads)",
            },
        },
    }

    label_source_block = {
        "label": ("the 008-h D1-4 label-source split over the sealed v4 labels: "
                  "construction-labeled protected bytes = the hard safety axis "
                  "(zero tolerance; the 008-i composition contract - R1 "
                  "extended to all HTML block-start lines, the display-dollar "
                  "adjacency guard, the T6 clean-URL admission - removes the "
                  "ambiguous shapes from the pool, and the D1-5 xml-fragment "
                  "trigger refinement closes the measured class-boundary "
                  "shape, so any construction exposure is a defect); "
                  "oracle-refined protected bytes = policy-coverage census "
                  "(CIRCULARITY LIMITATION DISCLOSED: the label oracle is the "
                  "implementation's own residual function, so this axis "
                  "measures what the policy claims to protect, not independent "
                  "evidence)"),
        "construction_labeled_protected": {
            "bytes_total": split["construction_bytes"],
            "bytes_covered": split["construction_covered"],
            "bytes_exposed": split["construction_exposed"],
            "target": 0,
            "met": split["construction_exposed"] == 0,
        },
        "oracle_refined_protected_census": {
            "bytes_total": split["oracle_refined_bytes"],
            "bytes_covered": split["oracle_refined_covered"],
            "bytes_exposed": split["oracle_refined_exposed"],
            "circularity": "oracle = implementation residual function (disclosed)",
        },
        "cross_check_vs_raw_record": {
            "split_protected_bytes": split["protected_bytes"],
            "raw_protected_bytes": raw_totals["protected_bytes"],
            "split_protected_covered": split["protected_covered"],
            "raw_protected_covered": raw_totals["protected_covered"],
            "reconciled": (split["protected_bytes"] == raw_totals["protected_bytes"]
                           and split["protected_covered"] == raw_totals["protected_covered"]),
        },
    }

    def write_json(path: Path, obj: dict) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(obj, ensure_ascii=False, indent=1) + "\n"
        path.write_text(payload, encoding="utf-8")
        return sha256_bytes(payload.encode("utf-8"))

    metrics_v4 = {
        "schema": "008i-hidden-mashup-metrics-v4/1",
        "order": "008-i",
        "label": ("acceptance evidence over the NEW sealed v4 hidden set: the "
                  "frozen 008-i implementation (frozen at the dev regression "
                  "gate; census above) evaluated through the committed 008-f "
                  "frozen harness, imported UNMODIFIED with its v1 identity "
                  "globals re-pointed to the v4 manifest and the v5 policy of "
                  "record (disclosed thin wrapper); the v4 loader carries the "
                  "008-h/008-i schema additions (composition_provenance, "
                  "label_source) with strict validation"),
        "raw_frozen_harness_output": {
            "label": ("raw frozen-harness output over the v4 set, NOT a "
                      "development-run result: the embedded aggregate "
                      "self-identifies with its 008-c/008-f identity fields "
                      "(frozen harness self-identification, unchanged); the "
                      "implementation actually executed is the 008-i frozen "
                      "implementation whose census is recorded in "
                      "frozen_protection_identity; its malformed_behaviour "
                      "rows carry the known frozen-harness first-document "
                      "double-count (see malformed_policy_exposed_"
                      "recomputation)"),
            "output_sha256": raw_metrics_sha,
            "metrics": metrics,
        },
        "label_source_split": label_source_block,
        "malformed_policy_exposed_recomputation": recomputation,
        "v4_identity": v4_identity,
        "privacy": "counts, categories, rates and hashes only; no case content, no label content, no private paths",
    }
    m4_sha = write_json(args.out / "mashup-metrics-v4.json", metrics_v4)
    print("mashup-metrics-v4.json:", m4_sha)
    print(json.dumps({
        "safety": metrics["safety"],
        "construction_exposed": split["construction_exposed"],
        "oracle_refined_exposed": split["oracle_refined_exposed"],
        "coordinates": metrics["coordinates"],
        "coverage_rate": metrics["coverage"]["expected_prose_bytes_exposed_rate"],
        "malformed_violations": metrics["malformed_behaviour"]["violations"],
        "recomputation_delta_0": recomputation["delta_0_satisfied"],
        "determinism": metrics["determinism"]["re_run_stability_check"],
    }, indent=1))

    if e2e_raw is not None:
        e2e_v4 = {
            "schema": "008i-e2e-invariants-hidden-v4/1",
            "order": "008-i",
            "label": ("acceptance evidence over the NEW sealed v4 hidden set: "
                      "end-to-end preservation invariants 1-7 through the "
                      "actual frozen pipeline entry points (the frozen 008-c "
                      "runner, byte-identical, invoked unmodified)"),
            "raw_frozen_harness_output": {
                "label": ("raw frozen-harness output over the v4 set, NOT a "
                          "development-run result: the embedded wrapper "
                          "self-identifies with its 008-f identity fields "
                          "(frozen harness self-identification, unchanged)"),
                "e2e": e2e_raw,
            },
            "per_invariant": e2e_raw["per_invariant"],
            "all_pass": e2e_raw["all_pass"],
            "v4_identity": v4_identity,
            "privacy": "counts, categories, rates and hashes only; no case content, no label content, no private paths",
        }
        e4_sha = write_json(args.out / "e2e-invariants-hidden-v4.json", e2e_v4)
        print("e2e-invariants-hidden-v4.json:", e4_sha)
        print(json.dumps({"per_invariant": e2e_v4["per_invariant"],
                          "all_pass": e2e_raw["all_pass"]}, indent=1))

    for row in metrics.get("performance", {}).get("rows", []):
        print("  ~%dB: median %.3f ms/doc, peak RSS %d KB, mode %s"
              % (row["target_bytes"], row["median_ms_per_document"],
                 row["peak_rss_kb"], row["mode"]))

    # hard axis: CONSTRUCTION-labeled protected bytes (008-h D1-4); the
    # raw total exposure is reported but the oracle-refined census does not
    # by itself block (circularity disclosed)
    hard_fail = (
        split["construction_exposed"] != 0
        or metrics["coordinates"]["source_slice_mismatches"] != 0
        or metrics["coordinates"]["patch_preservation_violations"] != 0
        or metrics["malformed_behaviour"]["violations"] != 0
        or metrics["determinism"]["re_run_stability_check"]["identical"] is not True
        or metrics["fallback_documents"]
        or not label_source_block["cross_check_vs_raw_record"]["reconciled"]
        or not recomputation["delta_0_satisfied"]
        or (e2e_raw is not None and not e2e_raw["all_pass"])
    )
    if hard_fail:
        exit_code = 1
    print("exit_code:", exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
