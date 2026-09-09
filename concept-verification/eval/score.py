"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Scoring."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controlled", type=Path, required=True)
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    controlled = json.loads(Path(args.controlled).read_text(encoding="utf-8"))
    workload = json.loads((args.workload / "summary.json").read_text(encoding="utf-8"))
    selected = controlled["settings_evaluated"][-1]
    summary = {
        "decision": "INCONCLUSIVE",
        "config_sha256": controlled.get("config_sha256"),
        "dataset": controlled.get("dataset"),
        "index_sha256": controlled.get("index_sha256"),
        "controlled": {
            "eligible_words": controlled.get("eligible_words"),
            "known_errors": selected.get("known_errors", 0),
            "candidates": selected.get("candidates", 0),
            "candidate_recall": selected.get("candidate_recall", 0),
            "candidate_precision": selected.get("candidate_precision", 0),
            "reviewer_accuracy": "PENDING LIVE REVIEWER",
            "accepted": "PENDING LIVE REVIEWER",
            "correct": "PENDING HUMAN LABELS",
            "harmful": "PENDING HUMAN LABELS",
            "missed": None,
            "protected_changes": 0,
            "end_to_end_recovery": "PENDING LIVE REVIEWER",
        },
        "real_workload": {
            "responses": len(workload.get("responses", [])),
            "completed": sum(
                item.get("status") == "COMPLETED" for item in workload.get("responses", [])
            ),
            "reviewer_calls_per_response": None,
            "proposals": None,
            "accepted_edits": None,
            "percent_changed": None,
            "protected_diffs": "PENDING_HUMAN_REVIEW",
            "raw_detector_reviewer_proxy_latency": "PENDING_AGGREGATE",
            "median_p95_total": "PENDING_AGGREGATE",
            "benefit_harm": "AWAITING_HUMAN_REVIEW",
        },
        "harm": {
            "harmful_per_1000_eligible_words": "PENDING_HUMAN_LABELS",
            "harmful_fraction_accepted": "PENDING_HUMAN_LABELS",
        },
        "ablations": controlled.get("ablation_status", {}),
        "human_review": "AWAITING_HUMAN_REVIEW",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"decision": summary["decision"], "output": str(args.output)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
