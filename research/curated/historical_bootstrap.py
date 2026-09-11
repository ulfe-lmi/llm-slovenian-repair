"""Copied fixed-seed paired example/document bootstrap algorithm."""

from __future__ import annotations

import random
from typing import Any

SEED = 20260909
REPLICATES = 2000


def _metric(rows: list[dict[str, Any]]) -> tuple[float, float, float]:
    tp = sum(row["tp"] for row in rows)
    fp = sum(row["fp"] for row in rows)
    fn = sum(row["fn"] for row in rows)
    denominator = 1.25 * tp + fp + 0.25 * fn
    f05 = 1.25 * tp / denominator if denominator else 0.0
    return f05, sum(row["exact_reference"] for row in rows) / len(rows), sum(not row["changed"] for row in rows) / len(rows)


def paired(left: list[dict[str, Any]], right: list[dict[str, Any]], *, seed: int = SEED, replicates: int = REPLICATES) -> dict[str, Any]:
    right_by_id = {row["id"]: row for row in right}
    pairs = [(row, right_by_id[row["id"]]) for row in left if row["id"] in right_by_id and row["has_reference"] and right_by_id[row["id"]]["has_reference"]]
    if not pairs:
        return {"N": 0, "status": "NOT_APPLICABLE_NO_REFERENCE"}
    left_rows, right_rows = [pair[0] for pair in pairs], [pair[1] for pair in pairs]
    point_left, point_right = _metric(left_rows), _metric(right_rows)
    rng = random.Random(seed)
    samples: list[tuple[float, float, float]] = []
    for _ in range(replicates):
        indices = [rng.randrange(len(pairs)) for _ in pairs]
        samples.append(tuple(a - b for a, b in zip(_metric([left_rows[i] for i in indices]), _metric([right_rows[i] for i in indices]), strict=True)))
    metrics = []
    for index, key in enumerate(("custom_token_edit_F0.5", "exact_reference_rate", "exact_preservation_rate")):
        values = sorted(sample[index] for sample in samples)
        low = values[max(0, int(0.025 * len(values)))]
        high = values[min(len(values) - 1, int(0.975 * len(values)))]
        delta = point_left[index] - point_right[index]
        metrics.append((key, {"left": point_left[index], "right": point_right[index], "absolute_delta": delta,
                              "relative_delta": delta / point_right[index] if point_right[index] else None, "ci95": [low, high]}))
    return {"N": len(pairs), "seed": seed, "replicates": replicates,
            "unit": "one complete benchmark example/document, not individual edits/tokens",
            "metrics": dict(metrics),
            "official_metric_note": "These CIs describe the explicitly custom edit-alignment metric, not the official ERRANT/GLEU scores."}
