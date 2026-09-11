"""The campaign's data-free token-coordinate metrics and paired bootstrap."""

from __future__ import annotations

import difflib
import hashlib
import math
import random
import re
import statistics
from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Any

TOKEN = re.compile(r"\w+|[^\w\s]", re.UNICODE)
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
BOOTSTRAP_SEED = 20260909
BOOTSTRAP_REPLICATES = 2000


def tokens(text: str) -> list[tuple[str, int, int]]:
    return [(match.group(), match.start(), match.end()) for match in TOKEN.finditer(text)]


def edits(source: str, target: str | None) -> list[dict[str, Any]]:
    if target is None:
        return []
    left, right = tokens(source), tokens(target)
    matcher = difflib.SequenceMatcher(
        None, [item[0] for item in left], [item[0] for item in right], autojunk=False
    )
    result = []
    for tag, start, end, target_start, target_end in matcher.get_opcodes():
        if tag == "equal":
            continue
        source_start = left[start][1] if start < len(left) else len(source)
        source_end = left[end - 1][2] if end > start else source_start
        result.append(
            {
                "source_token_start": start,
                "source_token_end": end,
                "replacement_tokens": [item[0] for item in right[target_start:target_end]],
                "start": source_start,
                "end": source_end,
                "changed_tokens": max(end - start, target_end - target_start),
            }
        )
    return result


def edit_key(edit: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        edit["source_token_start"],
        edit["source_token_end"],
        tuple(edit["replacement_tokens"]),
    )


def overlap(candidate: Mapping[str, Any], gold: Mapping[str, Any]) -> bool:
    if gold["start"] == gold["end"]:
        return candidate["start"] <= gold["start"] <= candidate["end"]
    return candidate["start"] < gold["end"] and gold["start"] < candidate["end"]


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f05 = 1.25 * precision * recall / (0.25 * precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "F0.5": f05}


def distribution(values: Iterable[float | int | None]) -> dict[str, float | int | None]:
    ordered = sorted(value for value in values if value is not None)
    if not ordered:
        return {"n": 0, "sum": 0, "mean": None, "median": None, "p95": None, "max": None}
    return {
        "n": len(ordered),
        "sum": sum(ordered),
        "mean": statistics.mean(ordered),
        "median": statistics.median(ordered),
        "p95": ordered[math.ceil(0.95 * len(ordered)) - 1],
        "max": ordered[-1],
    }


def row_metrics(example: Mapping[str, Any], result: Mapping[str, Any], method: str) -> dict[str, Any]:
    source = str(result.get("input", example["input"]))
    reference = example.get("reference")
    output = str(result["output"])
    changes, gold = edits(source, output), edits(source, reference)
    observed, expected = {edit_key(item) for item in changes}, {edit_key(item) for item in gold}
    detector = result.get("detector", {})
    candidates = detector.get("candidates", []) if isinstance(detector, dict) else []
    english = detector.get("english", []) if isinstance(detector, dict) else []
    suppressed = [candidate for candidate, policy in zip(candidates, english) if policy["review_suppressed"]]
    actions: Counter[str] = Counter()
    first_rejections = 0
    retries = accepted_retries = failed_retries = 0
    for decision in result.get("decisions", []):
        first = decision.get("first_proposal")
        if first:
            actions["WIDER" if first.needs_wider_edit else "KEEP" if first.keep else "REPLACE"] += 1
        gate = decision.get("first_gate")
        if gate and gate.get("reason") not in ("KEEP", "WIDER", "unigram-exact"):
            first_rejections += 1
        if decision.get("retry_used") and method != "M3":
            retries += 1
            accepted = bool(decision.get("final_gate", {}).get("accepted"))
            accepted_retries += accepted
            failed_retries += not accepted
    calls = result.get("calls", [])
    return {
        "id": example["id"],
        "index": example["index"],
        "category": example.get("category"),
        "problem_type": example.get("problem_type"),
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "source_words": len(WORD.findall(source)),
        "source_tokens": len(tokens(source)),
        "has_reference": reference is not None,
        "has_gold_error": reference is not None and source != reference,
        "operational_failure": bool(result.get("operational_failure", False)),
        "changed": output != source,
        "exact_reference": output == reference if reference is not None else None,
        "unchanged_error": reference is not None and source != reference and output == source,
        "nonreference_change": reference is not None and output != source and output != reference,
        "tp": len(expected & observed),
        "fp": len(observed - expected),
        "fn": len(expected - observed),
        "gold_edits": len(gold),
        "introduced_edits": len(changes),
        "changed_tokens": sum(edit["changed_tokens"] for edit in changes),
        "detector_candidates": len(candidates),
        "detector_gold_overlap": sum(any(overlap(c, g) for c in gold) for g in candidates),
        "english_suppressions": len(suppressed),
        "english_gold_overlap": sum(any(overlap(c, g) for g in gold) for c in suppressed),
        "actions": dict(actions),
        "first_rejections": first_rejections,
        "retry_calls": retries,
        "accepted_retry_edits": accepted_retries,
        "failed_corrective_retries": failed_retries,
        "first_review_calls": sum(call.get("kind") == "reviewer" for call in calls),
        "model_calls": len(calls),
        "http_seconds": sum(call.get("http_seconds") or 0 for call in calls),
        "call_latencies": [call.get("http_seconds") for call in calls],
        "reasoning_tokens": sum(call.get("reasoning_tokens") or 0 for call in calls),
        "output_tokens": sum(call.get("output_tokens") or 0 for call in calls),
        "accepted_edits": len(result.get("edits", [])) if method in ("M2", "M3") else len(changes),
        "wall_seconds": result.get("wall_seconds"),
    }


def summarize(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    values = list(rows)
    references = [row for row in values if row["has_reference"]]
    errors = [row for row in references if row["has_gold_error"]]
    sum_keys = (
        "source_words", "source_tokens", "introduced_edits", "changed_tokens", "detector_candidates",
        "detector_gold_overlap", "english_suppressions", "english_gold_overlap", "first_review_calls",
        "retry_calls", "model_calls", "http_seconds", "reasoning_tokens", "output_tokens", "accepted_edits",
        "accepted_retry_edits", "failed_corrective_retries", "first_rejections",
    )
    result = {key: sum(row[key] for row in values) for key in sum_keys}
    result.update(
        {
            "N": len(values),
            "reference_N": len(references),
            "error_N": len(errors),
            "operational_failures": sum(row["operational_failure"] for row in values),
            "changed_examples": sum(row["changed"] for row in values),
            "unchanged_examples": sum(not row["changed"] for row in values),
            "exact_reference_success": sum(row["exact_reference"] is True for row in references),
            "exact_error_corrections": sum(row["exact_reference"] is True for row in errors),
            "unchanged_errors": sum(row["unchanged_error"] for row in values),
            "nonreference_changes": sum(row["nonreference_change"] for row in values),
            "gold_edits": sum(row["gold_edits"] for row in references),
            "tp": sum(row["tp"] for row in references),
            "fp": sum(row["fp"] for row in references),
            "fn": sum(row["fn"] for row in references),
        }
    )
    result.update(prf(result["tp"], result["fp"], result["fn"]))
    result["exact_reference_rate"] = result["exact_reference_success"] / len(references) if references else None
    result["exact_error_correction_rate"] = result["exact_error_corrections"] / len(errors) if errors else None
    result["preservation_rate"] = result["unchanged_examples"] / len(values) if values else None
    result["detector_span_recall"] = result["detector_gold_overlap"] / result["gold_edits"] if result["gold_edits"] else None
    result["gold_error_fraction_remaining"] = result["fn"] / result["gold_edits"] if result["gold_edits"] else None
    for key in ("introduced_edits", "changed_tokens", "detector_candidates", "english_suppressions", "model_calls", "accepted_edits"):
        result[key + "_per_1000_words"] = 1000 * result[key] / result["source_words"] if result["source_words"] else None
    result["call_latency_seconds"] = distribution(value for row in values for value in row["call_latencies"])
    result["example_wall_seconds"] = distribution(row["wall_seconds"] for row in values)
    result["actions"] = dict(sum((Counter(row["actions"]) for row in values), Counter()))
    return result


def paired_bootstrap(left: Iterable[Mapping[str, Any]], right: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Fixed-seed paired example bootstrap matching the campaign unit of analysis."""
    right_by_id = {row["id"]: row for row in right}
    pairs = [
        (row, right_by_id[row["id"]])
        for row in left
        if row["id"] in right_by_id and row["has_reference"] and right_by_id[row["id"]]["has_reference"]
    ]
    if not pairs:
        return {"N": 0, "status": "NOT_APPLICABLE_NO_REFERENCE"}

    def values(row: Mapping[str, Any]) -> tuple[float, ...]:
        return (row["tp"], row["fp"], row["fn"], int(row["exact_reference"]), int(not row["changed"]))

    def metric(rows: list[tuple[float, ...]]) -> tuple[float, float, float]:
        sums = [sum(row[index] for row in rows) for index in range(5)]
        tp, fp, fn, exact, preserved = sums
        denominator = 1.25 * tp + fp + 0.25 * fn
        f05 = 1.25 * tp / denominator if denominator else 0.0
        return f05, exact / len(pairs), preserved / len(pairs)

    a, b = [values(x) for x, _ in pairs], [values(y) for _, y in pairs]
    point_a, point_b = metric(a), metric(b)
    rng = random.Random(BOOTSTRAP_SEED)
    samples: list[tuple[float, float, float]] = []
    for _ in range(BOOTSTRAP_REPLICATES):
        indices = [rng.randrange(len(pairs)) for _ in pairs]
        samples.append(
            tuple(x - y for x, y in zip(metric([a[i] for i in indices]), metric([b[i] for i in indices])))
        )
    intervals = [
        (
            sorted(sample[index] for sample in samples)[int(0.025 * len(samples))],
            sorted(sample[index] for sample in samples)[int(0.975 * len(samples))],
        )
        for index in range(3)
    ]
    names = ("custom_token_edit_F0.5", "exact_reference_rate", "exact_preservation_rate")
    return {
        "N": len(pairs),
        "seed": BOOTSTRAP_SEED,
        "replicates": BOOTSTRAP_REPLICATES,
        "unit": "one complete benchmark example/document, not individual edits/tokens",
        "metrics": {
            name: {
                "left": point_a[index],
                "right": point_b[index],
                "absolute_delta": point_a[index] - point_b[index],
                "relative_delta": (point_a[index] - point_b[index]) / point_b[index] if point_b[index] else None,
                "ci95": list(intervals[index]),
            }
            for index, name in enumerate(names)
        },
        "official_metric_note": "These CIs describe the custom alignment metric, not official ERRANT/GLEU scores.",
    }
