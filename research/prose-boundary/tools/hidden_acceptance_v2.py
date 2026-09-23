"""008-g v2 hidden evaluation wrapper (thin, disclosed - order requirement 6).

The committed 008-f harness (tools/hidden_acceptance.py) hardcodes its v1
identity (the v1 manifest path and the v2 policy path as module globals), so
it cannot be pointed at the new sealed v2 set through its existing
parameters. This wrapper IMPORTS the 008-f harness UNMODIFIED (byte-identity
of the harness file is asserted against the committed git blob up front) and
re-points its two module-level identity globals at call time:

  HIDDEN_MANIFEST -> research/prose-boundary/corpus/manifests/hidden-manifest-v2.json
  POLICY_V2       -> research/prose-boundary/config/structural-policy-v3.json

Everything else runs through the frozen harness functions verbatim
(self-test, sealed-set loading with strict schema validation and per-file
hash checks, the full item-15 mashup metrics, the performance axis, and the
frozen 008-c e2e invariants runner over a hardlink view of the sealed v2
documents). The implementation under test is the fixed v3 implementation
frozen at the dev regression gate; its byte census is asserted against the
committed experiment-008g.json (the new frozen protection identity).

Hard gate (order requirement 2): the driver refuses to run until the v2 seal
state is committed AND strategy-verified; the strategy receipt identity is
recorded (filename + sha256 + size; the receipt must cite the v2 manifest
sha256). No private paths are committed.

Committed outputs (one data-free aggregate per axis, explicitly labelled):
  results/hidden-acceptance-v2/mashup-metrics-v2.json
  results/hidden-acceptance-v2/e2e-invariants-hidden-v2.json

Deterministic: fixed sorted iteration order; the frozen harness's bounded
50-case re-run stability check is recomputed independently and must be
byte-identical. No model calls of any kind.

Usage:
  python3 -B hidden_acceptance_v2.py --private-root <008g-hidden> \
      --strategy-verification <strategy seal-verification receipt> \
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
V2_MANIFEST = ROOT / "corpus" / "manifests" / "hidden-manifest-v2.json"
SEAL_VERIFICATION = ROOT / "corpus" / "manifests" / "seal-verification-v2.json"
POLICY_V3 = ROOT / "config" / "structural-policy-v3.json"
EXPERIMENT_CONFIG = ROOT / "config" / "experiment-008g.json"
HARNESS_FILE = HERE / "hidden_acceptance.py"
DEFAULT_OUT = ROOT / "results" / "hidden-acceptance-v2"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(rel: str) -> str:
    out = subprocess.run(["git", "-C", str(REPO_ROOT), "show", f"HEAD:{rel}"],
                         capture_output=True, check=True).stdout
    return sha256_bytes(out)


def implementation_census() -> dict:
    files = {
        "research/curated/prose_boundary.py":
            (REPO_ROOT / "research/curated/prose_boundary.py").read_bytes(),
        "research/curated/protected.py":
            (REPO_ROOT / "research/curated/protected.py").read_bytes(),
        "research/prose-boundary/config/structural-policy-v3.json":
            (REPO_ROOT / "research/prose-boundary/config/structural-policy-v3.json").read_bytes(),
    }
    return {k: sha256_bytes(v) for k, v in sorted(files.items())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--strategy-verification", required=True, type=Path,
                        help="strategy's data-free v2 seal verification receipt "
                             "(workorder in the supervision tree); its identity is "
                             "recorded, no private paths are committed")
    parser.add_argument("--helper", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--stability-sample", type=int, default=50)
    parser.add_argument("--skip-e2e", action="store_true")
    parser.add_argument("--skip-performance", action="store_true")
    parser.add_argument("--replay-count", type=int, default=None,
                        help="default: every v2 hidden document")
    parser.add_argument("--seed-count", type=int, default=20)
    args = parser.parse_args()

    # -- fail-closed pre-run guards -----------------------------------------
    harness_sha = sha256_bytes(HARNESS_FILE.read_bytes())
    harness_blob = git_blob_sha("research/prose-boundary/tools/hidden_acceptance.py")
    if harness_sha != harness_blob:
        raise SystemExit("008-f harness bytes differ from the committed blob; "
                         "the frozen surface is not byte-identical")

    if not V2_MANIFEST.is_file() or not SEAL_VERIFICATION.is_file():
        raise SystemExit("v2 seal state not committed (manifest / seal-verification missing)")
    seal_ver = json.loads(SEAL_VERIFICATION.read_text(encoding="utf-8"))
    if seal_ver.get("status") != "SEALED":
        raise SystemExit(f"committed seal-verification-v2 status is {seal_ver.get('status')!r}")
    v2_manifest_sha = sha256_bytes(V2_MANIFEST.read_bytes())
    if v2_manifest_sha != seal_ver.get("manifest_sha256"):
        raise SystemExit("committed v2 manifest bytes differ from the sealed identity")

    receipt_path = args.strategy_verification
    if not receipt_path.is_file() or receipt_path.stat().st_size == 0:
        raise SystemExit("strategy v2 seal verification receipt missing or empty; "
                         "the evaluation phase is gated on strategy verification")
    receipt_text = receipt_path.read_text(encoding="utf-8", errors="replace")
    receipt = {
        "filename": receipt_path.name,
        "sha256": sha256_bytes(receipt_path.read_bytes()),
        "size": receipt_path.stat().st_size,
        "location": "strategy workorders (supervision tree); path not committed",
        "cites_v2_manifest_sha256": v2_manifest_sha in receipt_text,
    }
    if not receipt["cites_v2_manifest_sha256"]:
        raise SystemExit("strategy receipt does not cite the v2 manifest sha256")
    print("strategy_verification:", json.dumps(receipt))

    exp = json.loads(EXPERIMENT_CONFIG.read_text(encoding="utf-8"))
    census = implementation_census()
    expected_census = exp.get("implementation", {}).get("frozen_census", {})
    if expected_census and expected_census != census:
        raise SystemExit("implementation bytes differ from the frozen protection "
                         "identity recorded in experiment-008g.json")

    # -- re-point the frozen harness identity globals (disclosed) ------------
    HA.HIDDEN_MANIFEST = V2_MANIFEST
    HA.POLICY_V2 = POLICY_V3

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

    records, comp_family, seal_identity = HA.load_hidden_set(private_root)
    print("hidden_set:", json.dumps(seal_identity))

    metrics = HA.mashup_metrics(records, comp_family, helper, args.stability_sample)
    if helper is not None and not args.skip_performance:
        metrics["performance"] = HA.performance(helper)
    raw_metrics_sha = sha256_bytes(
        (json.dumps(metrics, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))

    exit_code = 0
    e2e_raw = None
    if not args.skip_e2e:
        scratch = Path(tempfile.mkdtemp(prefix="008g-e2e-"))
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

    v2_identity = {
        "v2_manifest_sha256": v2_manifest_sha,
        "seal_verification_sha256": sha256_bytes(SEAL_VERIFICATION.read_bytes()),
        "seal_identity": seal_identity,
        "strategy_seal_verification_receipt": receipt,
        "frozen_protection_identity": {
            "experiment_config_sha256": sha256_bytes(EXPERIMENT_CONFIG.read_bytes()),
            "census": census,
            "policy_v3_sha256": census["research/prose-boundary/config/structural-policy-v3.json"],
            "helper_sha256": sha256_bytes(Path(helper).read_bytes()) if helper else None,
        },
        "frozen_harness": {
            "file": "research/prose-boundary/tools/hidden_acceptance.py",
            "sha256": harness_sha,
            "committed_blob_sha256": harness_blob,
            "byte_identical": True,
        },
    }

    def write_json(path: Path, obj: dict) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(obj, ensure_ascii=False, indent=1) + "\n"
        path.write_text(payload, encoding="utf-8")
        return sha256_bytes(payload.encode("utf-8"))

    metrics_v2 = {
        "schema": "008g-hidden-mashup-metrics-v2/1",
        "order": "008-g",
        "label": ("acceptance evidence over the NEW sealed v2 hidden set: the fixed v3 "
                  "implementation (frozen at the dev regression gate; census above) "
                  "evaluated through the committed 008-f frozen harness, imported "
                  "UNMODIFIED with its v1 identity globals re-pointed to the v2 manifest "
                  "and the v3 policy (disclosed thin wrapper)"),
        "raw_frozen_harness_output": {
            "label": ("raw frozen-harness output over the v2 set, NOT a development-run "
                      "result: the embedded aggregate self-identifies with its 008-c "
                      "identity fields (frozen harness self-identification, unchanged); "
                      "the implementation actually executed is the v3 fixed "
                      "implementation whose census is recorded in frozen_protection_identity"),
            "output_sha256": raw_metrics_sha,
            "metrics": metrics,
        },
        "v2_identity": v2_identity,
        "privacy": "counts, categories, rates and hashes only; no case content, no label content, no private paths",
    }
    m2_sha = write_json(args.out / "mashup-metrics-v2.json", metrics_v2)
    print("mashup-metrics-v2.json:", m2_sha)
    print(json.dumps({
        "safety": metrics["safety"],
        "coordinates": metrics["coordinates"],
        "coverage_rate": metrics["coverage"]["expected_prose_bytes_exposed_rate"],
        "malformed_violations": metrics["malformed_behaviour"]["violations"],
        "determinism": metrics["determinism"]["re_run_stability_check"],
    }, indent=1))

    if e2e_raw is not None:
        e2e_v2 = {
            "schema": "008g-e2e-invariants-hidden-v2/1",
            "order": "008-g",
            "label": ("acceptance evidence over the NEW sealed v2 hidden set: end-to-end "
                      "preservation invariants 1-7 through the actual frozen pipeline "
                      "entry points (the frozen 008-c runner, byte-identical, invoked "
                      "unmodified)"),
            "raw_frozen_harness_output": {
                "label": ("raw frozen-harness output over the v2 set, NOT a development-run "
                          "result: the embedded wrapper self-identifies with its 008-f "
                          "identity fields (frozen harness self-identification, unchanged)"),
                "e2e": e2e_raw,
            },
            "per_invariant": e2e_raw["per_invariant"],
            "all_pass": e2e_raw["all_pass"],
            "v2_identity": v2_identity,
            "privacy": "counts, categories, rates and hashes only; no case content, no label content, no private paths",
        }
        e2_sha = write_json(args.out / "e2e-invariants-hidden-v2.json", e2e_v2)
        print("e2e-invariants-hidden-v2.json:", e2_sha)
        print(json.dumps({"per_invariant": e2e_v2["per_invariant"],
                          "all_pass": e2e_raw["all_pass"]}, indent=1))

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
        or (e2e_raw is not None and not e2e_raw["all_pass"])
    )
    if hard_fail:
        exit_code = 1
    print("exit_code:", exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
