"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Eval runner."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import canonical_bytes, load_json, sha256_file  # noqa: E402
from corpus import Corpus  # noqa: E402
from detector import candidate_summary, detect, tokenize  # noqa: E402
from eval.common import (  # noqa: E402
    aggregate_candidates,
    dataset_identity,
    file_sha256,
    load_cases,
)
from protected import protected_intervals  # noqa: E402
from qwen_client import prompt  # noqa: E402


def _run(
    cases: list[dict[str, object]], corpus: Corpus, mode: str, threshold: int
) -> tuple[dict[str, object], dict[str, list[dict[str, object]]]]:
    by_id: dict[str, list[dict[str, object]]] = {}
    for case in cases:
        candidates = detect(
            str(case["text"]),
            corpus,
            protected_intervals(str(case["text"])),
            mode=mode,
            threshold=threshold,
        )
        by_id[str(case["id"])] = candidate_summary(candidates)
    return aggregate_candidates(cases, by_id), by_id


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE"
    )
    parser.add_argument("--phase", choices=("dev", "heldout"))
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument(
        "--index", type=Path, default=Path("concept-verification/eval/results/index.sqlite")
    )
    parser.add_argument("--results", type=Path)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--frozen", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    config = load_json(args.config)
    dev_path = args.config.parent / "cases/dev.jsonl"
    heldout_path = args.config.parent / "cases/heldout.jsonl"
    if args.freeze:
        if args.output is None:
            raise SystemExit("--freeze requires --output")
        frozen = {
            "version": "concept-v1-frozen",
            "config_sha256": sha256_file(args.config),
            "dev": dataset_identity(dev_path),
            "heldout": dataset_identity(heldout_path),
            "index_sha256": file_sha256(args.index) if args.index.exists() else None,
            "mode": config["selected_mode"],
            "threshold": config["selected_threshold"],
            "prompt_variant": config["selected_prompt_variant"],
            "prompt_template_sha256": hashlib.sha256(
                prompt("{{sentence}}", "{{target}}", str(config["selected_prompt_variant"])).encode(
                    "utf-8"
                )
            ).hexdigest(),
            "threshold_settings": config["threshold_settings"],
            "prompt_variants": config["prompt_variants"],
            "decision_thresholds": config["decision"],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(canonical_bytes(frozen))
        print(
            json.dumps(
                {"frozen": str(args.output), "sha256": file_sha256(args.output)}, sort_keys=True
            )
        )
        return 0
    if args.phase is None or args.results is None:
        raise SystemExit("--phase and --results are required unless --freeze is used")
    cases = load_cases(dev_path if args.phase == "dev" else heldout_path)
    if args.phase == "heldout":
        if args.frozen is None or not args.frozen.exists():
            raise SystemExit("held-out execution requires frozen-experiment.json")
        frozen = load_json(args.frozen)
        if frozen.get("config_sha256") != sha256_file(args.config) or frozen.get(
            "heldout"
        ) != dataset_identity(heldout_path):
            raise SystemExit("frozen identity mismatch; held-out tuning is refused")
        if args.index.exists() and frozen.get("index_sha256") != file_sha256(args.index):
            raise SystemExit("frozen index identity mismatch")
        mode, threshold = str(frozen["mode"]), int(frozen["threshold"])
        settings = [(mode, threshold)]
    else:
        settings = [
            (mode, int(threshold))
            for mode in config["detector_modes"]
            for threshold in config["threshold_settings"]
        ]
        if len(settings) > 8:
            raise SystemExit("development tuning exceeds four thresholds per mode")
    if not args.index.exists():
        raise SystemExit("verified external SQLite index is required")
    summaries: list[dict[str, object]] = []
    selected: dict[str, list[dict[str, object]]] = {}
    with Corpus(args.index) as corpus:
        for mode, threshold in settings:
            summary, candidates = _run(cases, corpus, mode, threshold)
            summary.update({"mode": mode, "threshold": threshold})
            summaries.append(summary)
            if args.phase == "heldout" or (
                mode == config["selected_mode"] and threshold == config["selected_threshold"]
            ):
                selected = candidates
    result = {
        "phase": args.phase,
        "config_sha256": sha256_file(args.config),
        "dataset": dataset_identity(dev_path if args.phase == "dev" else heldout_path),
        "index_sha256": file_sha256(args.index),
        "eligible_words": sum(
            len(tokenize(str(case["text"]), protected_intervals(str(case["text"]))))
            for case in cases
        ),
        "settings_evaluated": summaries,
        "selected_candidates": selected,
        "ablation_status": {
            "raw_qwen": "NOT RUN",
            "detector_only": "MEASURED",
            "reviewer_decisions": "PENDING LIVE REVIEWER",
            "full_pipeline": "PENDING LIVE REVIEWER",
        },
    }
    args.results.mkdir(parents=True, exist_ok=True)
    output = args.results / f"{args.phase}.json"
    output.write_bytes(canonical_bytes(result))
    print(
        json.dumps(
            {"phase": args.phase, "output": str(output), "sha256": file_sha256(output)},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
