"""Copied per-phase analysis/aggregation program with explicit result roots."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from typing import Any

from .historical_bootstrap import paired
from .historical_common import jsonlines, read, result_path, save, sha
from .historical_scoring import edits, overlap, row_metrics, summarize


def phase(root: str | Path, benchmark: str, *, write: bool = True) -> dict[str, Any]:
    root = Path(root)
    config = read(root / "CONFIGURATION.json") if (root / "CONFIGURATION.json").exists() else {"datasets": read(root / "DATASET-ADAPTATION.json")["datasets"]}
    examples = jsonlines(config["datasets"][benchmark]["path"])
    names = ("RAW", "M1", "M2", "M3") if benchmark == "slobench" else ("M0", "M1", "M2", "M3")
    rows, summaries, identities = {}, {}, {}
    suppressed, retries = [], []
    for method in names:
        observed = []
        for example in examples:
            path = result_path(root, benchmark, example["index"], method)
            if not path.exists():
                continue
            result = read(path)
            if result["id"] != example["id"] or result["method"] != method:
                raise ValueError("result identity mismatch")
            observed.append(row_metrics(example, result, method))
            if method == "M2":
                gold = edits(result["input"], example.get("reference"))
                for candidate, policy in zip(result.get("detector", {}).get("candidates", []), result.get("detector", {}).get("english", []), strict=True):
                    if policy["review_suppressed"]:
                        suppressed.append({"id": example["id"], "index": example["index"], **policy, "gold_overlap": any(overlap(candidate, item) for item in gold), "preservation_set": bool(example.get("preservation"))})
                no_path = result_path(root, benchmark, example["index"], "M3")
                if no_path.exists():
                    no_result = read(no_path)
                    full_metric, no_metric = observed[-1], row_metrics(example, no_result, "M3")
                    retry_rows = [call for call in result.get("calls", []) if call.get("kind") == "expression-retry"]
                    retries.append({"id": example["id"], "index": example["index"], "calls": len(retry_rows),
                                    "accepted": full_metric["accepted_retry_edits"], "failed": full_metric["failed_corrective_retries"],
                                    "full_tp": full_metric["tp"], "no_retry_tp": no_metric["tp"], "tp_delta": full_metric["tp"] - no_metric["tp"],
                                    "fp_delta": full_metric["fp"] - no_metric["fp"], "exact_improved": example.get("reference") is not None and result["output"] == example["reference"] and no_result["output"] != example["reference"],
                                    "exact_regressed": example.get("reference") is not None and result["output"] != example["reference"] and no_result["output"] == example["reference"],
                                    "output_changed_by_retry": result["output"] != no_result["output"],
                                    "http_seconds": sum(call.get("http_seconds") or 0 for call in retry_rows),
                                    "reasoning_tokens": sum(call.get("reasoning_tokens") or 0 for call in retry_rows),
                                    "output_tokens": sum(call.get("output_tokens") or 0 for call in retry_rows)})
            identities[str(path)] = sha(path)
        rows[method] = observed
        categories, types = defaultdict(list), defaultdict(list)
        for row in observed:
            if row["category"] is not None:
                categories[row["category"]].append(row)
            if row["problem_type"] is not None:
                types[row["problem_type"]].append(row)
        unique = {}
        for row in observed:
            unique.setdefault(row["source_sha256"], row)
        summaries[method] = {"end_to_end": summarize(observed), "conditional_no_operational_failure": summarize([row for row in observed if not row["operational_failure"]]),
                             "unique_text_first_occurrence": summarize(list(unique.values())), "by_category": {key: summarize(value) for key, value in categories.items()},
                             "by_problem_type": {key: summarize(value) for key, value in types.items()}}
    baseline = "RAW" if benchmark == "slobench" else "M0"
    report = {"benchmark": benchmark, "expected_examples": len(examples), "available_examples": {method: len(rows[method]) for method in names},
              "complete": all(len(rows[method]) == len(examples) for method in names), "methods": summaries,
              "paired_bootstrap": {f"M2_vs_{other}": paired(rows.get("M2", []), rows.get(other, [])) for other in (baseline, "M1", "M3")},
              "english_suppressions": suppressed, "retry_ablation": retries,
              "retry_ablation_totals": {key: sum(row[key] for row in retries) for key in ("calls", "accepted", "failed", "tp_delta", "fp_delta", "exact_improved", "exact_regressed", "output_changed_by_retry", "http_seconds", "reasoning_tokens", "output_tokens")},
              "row_metrics": rows, "result_identities": identities,
              "metric_authority": "Custom deterministic token-span edits from supplied references, not official ERRANT; no-reference fields remain unknown and nonreference change is not a human-labeled harmful edit."}
    if write:
        save(root / "analysis" / (benchmark + ".json"), report)
    return report
