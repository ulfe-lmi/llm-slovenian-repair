"""Copied automatic metrics/scorer projections; never semantic labels."""

from __future__ import annotations

import difflib
import hashlib
import math
import re
import statistics
from collections import Counter
from typing import Any

TOKEN = re.compile(r"\w+|[^\w\s]", re.UNICODE)
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def tokens(text: str) -> list[tuple[str, int, int]]:
    return [(match.group(), match.start(), match.end()) for match in TOKEN.finditer(text)]


def edits(source: str, target: str | None) -> list[dict[str, Any]]:
    if target is None:
        return []
    left, right = tokens(source), tokens(target)
    matcher = difflib.SequenceMatcher(None, [item[0] for item in left], [item[0] for item in right], autojunk=False)
    result = []
    for tag, i, j, k, l in matcher.get_opcodes():
        if tag == "equal":
            continue
        start = left[i][1] if i < len(left) else len(source)
        end = left[j - 1][2] if j > i else start
        result.append({"source_token_start": i, "source_token_end": j,
                       "replacement_tokens": [item[0] for item in right[k:l]],
                       "start": start, "end": end, "changed_tokens": max(j - i, l - k)})
    return result


def edit_key(edit: dict[str, Any]) -> tuple[Any, ...]:
    return (edit["source_token_start"], edit["source_token_end"], tuple(edit["replacement_tokens"]))


def overlap(candidate: dict[str, Any], gold: dict[str, Any]) -> bool:
    return candidate["start"] <= gold["start"] <= candidate["end"] if gold["start"] == gold["end"] else candidate["start"] < gold["end"] and gold["start"] < candidate["end"]


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {"precision": precision, "recall": recall, "F0.5": 1.25 * precision * recall / (0.25 * precision + recall) if precision + recall else 0.0}


def distribution(values: Any) -> dict[str, Any]:
    values = sorted(value for value in values if value is not None)
    if not values:
        return {"n": 0, "sum": 0, "mean": None, "median": None, "p95": None, "max": None}
    return {"n": len(values), "sum": sum(values), "mean": statistics.mean(values), "median": statistics.median(values),
            "p95": values[math.ceil(0.95 * len(values)) - 1], "max": values[-1]}


def row_metrics(example: dict[str, Any], result: dict[str, Any], method: str) -> dict[str, Any]:
    source = result.get("input", example["input"])
    reference = example.get("reference")
    output = result["output"]
    changes, gold = edits(source, output), edits(source, reference)
    observed, expected = {edit_key(item) for item in changes}, {edit_key(item) for item in gold}
    candidates = result.get("detector", {}).get("candidates", [])
    english = result.get("detector", {}).get("english", [])
    suppressed = [candidate for candidate, policy in zip(candidates, english, strict=True) if policy["review_suppressed"]]
    actions, retries, retry_accept, retry_fail, first_rejected = Counter(), 0, 0, 0, 0
    for decision in result.get("decisions", []):
        first = decision.get("first")
        if first and not first.get("operational_failure"):
            proposal = first["proposal"]
            actions["WIDER" if proposal["needs_wider_edit"] else "KEEP" if proposal["keep"] else "REPLACE"] += 1
        if decision.get("first_gate") and decision["first_gate"]["reason"] not in ("KEEP", "WIDER", "unigram-exact"):
            first_rejected += 1
        if decision.get("retry") and method != "M3":
            retries += 1
            accepted = bool(decision.get("final_gate") and decision["final_gate"]["accepted"] and not result.get("operational_failure"))
            retry_accept += accepted
            retry_fail += not accepted
    calls = result.get("calls", [])
    tp, fp, fn = len(expected & observed), len(observed - expected), len(expected - observed)
    return {
        "id": example["id"], "index": example.get("index"), "category": example.get("category"), "problem_type": example.get("problem_type"),
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(), "source_words": len(WORD.findall(source)), "source_tokens": len(tokens(source)),
        "has_reference": reference is not None, "has_gold_error": reference is not None and source != reference,
        "operational_failure": result.get("operational_failure", False), "changed": output != source,
        "exact_reference": output == reference if reference is not None else None,
        "unchanged_error": reference is not None and source != reference and output == source,
        "nonreference_change": reference is not None and output != source and output != reference,
        "tp": tp, "fp": fp, "fn": fn, "gold_edits": len(gold), "introduced_edits": len(changes),
        "changed_tokens": sum(item["changed_tokens"] for item in changes), "detector_candidates": len(candidates),
        "detector_gold_overlap": sum(any(overlap(candidate, item) for candidate in candidates) for item in gold),
        "detector_error_example_covered": any(overlap(candidate, item) for candidate in candidates for item in gold),
        "english_suppressions": len(suppressed), "english_gold_overlap": sum(any(overlap(candidate, item) for candidate in suppressed) for item in gold),
        "english_suppressed_error": any(overlap(candidate, item) for candidate in suppressed for item in gold),
        "actions": dict(actions), "first_rejections": first_rejected, "retry_calls": retries,
        "accepted_retry_edits": retry_accept, "failed_corrective_retries": retry_fail,
        "first_review_calls": sum(call.get("kind") == "reviewer" for call in calls), "model_calls": len(calls),
        "http_seconds": sum(call.get("http_seconds") or 0 for call in calls),
        "call_latencies": [call.get("http_seconds") for call in calls],
        "reasoning_tokens": sum(call.get("reasoning_tokens") or 0 for call in calls), "output_tokens": sum(call.get("output_tokens") or 0 for call in calls),
        "accepted_edits": len(result.get("edits", [])) if method in ("M2", "M3") else len(changes), "wall_seconds": result.get("wall_seconds"),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    references = [row for row in rows if row["has_reference"]]
    errors = [row for row in references if row["has_gold_error"]]
    sumkeys = ("source_words", "source_tokens", "introduced_edits", "changed_tokens", "detector_candidates", "detector_gold_overlap", "english_suppressions", "english_gold_overlap", "first_review_calls", "retry_calls", "model_calls", "http_seconds", "reasoning_tokens", "output_tokens", "accepted_edits", "accepted_retry_edits", "failed_corrective_retries", "first_rejections")
    result = {key: sum(row[key] for row in rows) for key in sumkeys}
    result.update({"N": n, "reference_N": len(references), "error_N": len(errors), "operational_failures": sum(row["operational_failure"] for row in rows),
                   "changed_examples": sum(row["changed"] for row in rows), "unchanged_examples": sum(not row["changed"] for row in rows),
                   "exact_reference_success": sum(row["exact_reference"] is True for row in references), "exact_error_corrections": sum(row["exact_reference"] is True for row in errors),
                   "unchanged_errors": sum(row["unchanged_error"] for row in rows), "nonreference_changes": sum(row["nonreference_change"] for row in rows),
                   "detector_error_examples_covered": sum(row["detector_error_example_covered"] for row in errors), "english_suppressed_error_examples": sum(row["english_suppressed_error"] for row in errors),
                   "gold_edits": sum(row["gold_edits"] for row in references), "tp": sum(row["tp"] for row in references), "fp": sum(row["fp"] for row in references), "fn": sum(row["fn"] for row in references)})
    result.update(prf(result["tp"], result["fp"], result["fn"]))
    if not references:
        result.update(precision=None, recall=None, **{"F0.5": None})
    result["exact_reference_rate"] = result["exact_reference_success"] / len(references) if references else None
    result["exact_error_correction_rate"] = result["exact_error_corrections"] / len(errors) if errors else None
    result["preservation_rate"] = result["unchanged_examples"] / n if n else None
    result["detector_span_recall"] = result["detector_gold_overlap"] / result["gold_edits"] if result["gold_edits"] else None
    result["gold_error_fraction_remaining"] = result["fn"] / result["gold_edits"] if result["gold_edits"] else None
    for key in ("introduced_edits", "changed_tokens", "detector_candidates", "english_suppressions", "model_calls", "accepted_edits"):
        result[key + "_per_1000_words"] = 1000 * result[key] / result["source_words"] if result["source_words"] else None
    result["call_latency_seconds"] = distribution(value for row in rows for value in row["call_latencies"])
    result["example_wall_seconds"] = distribution(row["wall_seconds"] for row in rows)
    result["actions"] = dict(sum((Counter(row["actions"]) for row in rows), Counter()))
    return result
