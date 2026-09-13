"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Scoring."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from statistics import median
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from detector import tokenize  # noqa: E402
from protected import protected_intervals  # noqa: E402


def _number(value: object) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _p95(values: list[float]) -> float | None:
    if not values:
        return None
    return values[max(0, math.ceil(len(values) * 0.95) - 1)]


def _traces(workload: dict[str, Any], trace_root: Path | None) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for item in workload.get("responses", []):
        if not isinstance(item, dict) or item.get("status") != "COMPLETED":
            continue
        for path_value in item.get("trace_files", []):
            if not isinstance(path_value, str):
                continue
            path = Path(path_value)
            if trace_root is not None and not path.is_absolute():
                path = trace_root / path
            if path.is_symlink() or not path.is_file():
                continue
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                values.append(value)
    return values


def _workload_metrics(workload: dict[str, Any], traces: list[dict[str, Any]]) -> dict[str, Any]:
    completed = sum(item.get("status") == "COMPLETED" for item in workload.get("responses", []))
    eligible_words = sum(
        len(tokenize(str(trace["original"]), protected_intervals(str(trace["original"]))))
        for trace in traces
        if isinstance(trace.get("original"), str)
    )
    candidates = sum(len(trace.get("candidates", [])) for trace in traces)
    calls = sum(len(trace.get("reviewer_decisions", [])) for trace in traces)
    proposals = sum(
        sum(
            isinstance(decision, dict)
            and isinstance(decision.get("proposal"), dict)
            and decision["proposal"].get("keep") is False
            and isinstance(decision["proposal"].get("replacement"), str)
            and bool(decision["proposal"].get("replacement"))
            for decision in trace.get("reviewer_decisions", [])
        )
        for trace in traces
    )
    accepted = sum(
        sum(
            isinstance(decision, dict)
            and isinstance(decision.get("acceptance"), dict)
            and decision["acceptance"].get("accepted") is True
            for decision in trace.get("reviewer_decisions", [])
        )
        for trace in traces
    )
    changed = sum(
        isinstance(trace.get("original"), str)
        and isinstance(trace.get("repaired"), str)
        and trace["original"] != trace["repaired"]
        for trace in traces
    )
    protected = sum(int(trace.get("protected_difference_count", 0)) for trace in traces)
    timings = [
        trace.get("timings", {}) for trace in traces if isinstance(trace.get("timings"), dict)
    ]
    latency_names = ("raw_seconds", "detector_seconds", "reviewer_seconds", "proxy_seconds")
    latency: dict[str, list[float]] = {}
    for name in latency_names:
        latency[name] = [
            float(value[name]) for value in timings if isinstance(value.get(name), (int, float))
        ]
    total = sorted(latency["proxy_seconds"])
    return {
        "responses_attempted": int(
            workload.get("responses_attempted", len(workload.get("responses", [])))
        ),
        "responses_completed": completed,
        "eligible_words": eligible_words,
        "candidates": candidates,
        "candidates_per_1000_eligible_words": candidates / eligible_words * 1000
        if eligible_words
        else 0.0,
        "reviewer_calls": calls,
        "reviewer_calls_per_response": calls / completed if completed else None,
        "proposals": proposals,
        "accepted_edits": accepted,
        "percent_changed": changed / completed * 100 if completed else 0.0,
        "protected_differences": protected,
        "latency_seconds": latency,
        "median_total_seconds": median(total) if total else None,
        "p95_total_seconds": _p95(total),
        "human_benefit_harm": "AWAITING_HUMAN_REVIEW",
    }


def _controlled_gate(controlled: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    metrics = controlled.get("controlled_metrics")
    if not isinstance(metrics, dict):
        settings = controlled.get("settings_evaluated")
        metrics = settings[-1] if isinstance(settings, list) and settings else {}
    correct = _number(metrics.get("exact_gold_correct_repairs"))
    harmful = _number(metrics.get("harmful_edits"))
    accepted = _number(metrics.get("accepted_edits"))
    recovery = _number(metrics.get("end_to_end_recovery"))
    precision = (
        correct / (correct + harmful)
        if correct is not None and harmful is not None and correct + harmful
        else None
    )
    harmful_fraction = harmful / accepted if harmful is not None and accepted else None
    protected = metrics.get("protected_changes")
    thresholds = controlled.get("decision_thresholds", {})
    if not isinstance(thresholds, dict):
        thresholds = {}
    required = {
        "beneficial_precision": float(thresholds.get("beneficial_precision_reference", 0.8)),
        "harmful_fraction": float(thresholds.get("harmful_fraction_reference", 0.05)),
        "recovery": float(thresholds.get("recovery_reference", 0.3)),
        "protected_changes": int(thresholds.get("protected_changes_required", 0)),
    }
    observed = {
        "beneficial_precision": precision,
        "harmful_fraction": harmful_fraction,
        "recovery": recovery,
        "protected_changes": protected,
    }
    missing = [name for name, value in observed.items() if value is None]
    failures = []
    if precision is not None and precision < required["beneficial_precision"]:
        failures.append("beneficial_precision_below_reference")
    if harmful_fraction is not None and harmful_fraction > required["harmful_fraction"]:
        failures.append("harmful_fraction_above_reference")
    if recovery is not None and recovery < required["recovery"]:
        failures.append("recovery_below_reference")
    if protected is not None and protected != required["protected_changes"]:
        failures.append("protected_changes_nonzero")
    if missing:
        decision = "INCONCLUSIVE"
    elif failures:
        decision = "NO-GO"
    else:
        decision = "AUTOMATICALLY_PROMISING, AWAITING_HUMAN_REVIEW"
    return decision, {
        "required": required,
        "observed": observed,
        "missing": missing,
        "failures": failures,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controlled", type=Path, required=True)
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--traces", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    controlled = json.loads(args.controlled.read_text(encoding="utf-8"))
    workload = json.loads((args.workload / "summary.json").read_text(encoding="utf-8"))
    if not isinstance(controlled, dict) or not isinstance(workload, dict):
        raise SystemExit("evaluation inputs must be JSON objects")
    traces = _traces(workload, args.traces)
    workload_metrics = _workload_metrics(workload, traces)
    decision, gate = _controlled_gate(controlled)
    controlled_metrics = controlled.get("controlled_metrics", {})
    if not isinstance(controlled_metrics, dict):
        controlled_metrics = {}
    summary = {
        "decision": decision,
        "gate": gate,
        "config_sha256": controlled.get("config_sha256"),
        "dataset": controlled.get("dataset"),
        "index_sha256": controlled.get("index_sha256"),
        "controlled": controlled_metrics,
        "real_workload": workload_metrics,
        "harm": {
            "harmful_per_1000_eligible_words": "PENDING_HUMAN_LABELS",
            "harmful_fraction_accepted": "PENDING_HUMAN_LABELS",
        },
        "ablations": controlled.get("ablations", controlled.get("ablation_status", {})),
        "human_review": "AWAITING_HUMAN_REVIEW",
        "automatic_quality_is_not_human_quality": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"decision": decision, "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
