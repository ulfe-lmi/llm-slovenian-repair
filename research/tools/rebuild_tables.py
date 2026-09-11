#!/usr/bin/env python3
"""Rebuild the committed data-free numeric research table deterministically."""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path


FIELDS = (
    "experiment_id",
    "kind",
    "status",
    "cases",
    "method_records",
    "model_calls",
    "first_calls",
    "retry_calls",
    "review_calls",
    "applied_edits",
    "exact_gold_repairs",
    "missed_gold_errors",
    "changed_controls",
    "unchanged_controls",
    "complete_trials",
    "stopped_trials",
    "distinct_calls",
    "new_model_calls",
    "inherited_calls",
    "verified_checkpoints",
)


def render(registry: Path) -> str:
    records = json.loads(registry.read_text(encoding="utf-8"))
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    for record in records["experiments"]:
        metrics = record.get("metrics", {})
        row = {field: metrics.get(field, "") for field in FIELDS}
        row["experiment_id"] = record["experiment_id"]
        row["kind"] = record["kind"]
        row["status"] = record["status"]
        writer.writerow(row)
    return output.getvalue()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("research/registry/experiments.json"))
    parser.add_argument("--table", type=Path, default=Path("research/tables/experiment-summary.csv"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    expected = render(args.registry)
    if args.check:
        actual = args.table.read_text(encoding="utf-8")
        if actual != expected:
            raise SystemExit("numeric table is stale; run rebuild_tables.py")
        print("numeric table: PASS")
    else:
        print(expected, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
