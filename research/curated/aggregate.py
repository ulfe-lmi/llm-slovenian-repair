"""Data-free analysis aggregation used by the preserved campaign."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any

from .scoring import paired_bootstrap, row_metrics, summarize


def aggregate(examples: Iterable[Mapping[str, Any]], results: Mapping[str, Iterable[Mapping[str, Any]]]) -> dict[str, Any]:
    """Aggregate M0/M1/M2/M3 rows while retaining category/type breakdowns."""
    examples = list(examples)
    rows: dict[str, list[dict[str, Any]]] = {}
    summaries: dict[str, Any] = {}
    for method, method_results in results.items():
        method_rows = [row_metrics(example, result, method) for example, result in zip(examples, method_results, strict=True)]
        rows[method] = method_rows
        categories: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        types: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in method_rows:
            if row["category"] is not None:
                categories[row["category"]].append(row)
            if row["problem_type"] is not None:
                types[row["problem_type"]].append(row)
        summaries[method] = {
            "end_to_end": summarize(method_rows),
            "by_category": {key: summarize(value) for key, value in categories.items()},
            "by_problem_type": {key: summarize(value) for key, value in types.items()},
        }
    methods = list(rows)
    comparisons = {}
    if "M2" in rows:
        for other in methods:
            if other != "M2":
                comparisons[f"M2_vs_{other}"] = paired_bootstrap(rows["M2"], rows[other])
    return {
        "methods": summaries,
        "paired_bootstrap": comparisons,
        "row_metrics": rows,
        "metric_authority": "Custom deterministic token-span alignment; non-reference change is not semantic harm.",
    }
