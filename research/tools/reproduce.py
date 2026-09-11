#!/usr/bin/env python3
"""Render an explicit historical reproduction plan without executing it."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from research.curated.historical import plan, validate_live_authorization


def execute_authorized(args: argparse.Namespace, variant: object) -> dict[str, object]:
    """Execute the retained driver against caller-owned records after opt-in."""
    input_root = Path(args.input_root)
    index = Path(args.index)
    output_root = Path(args.output_root)
    records_path = input_root / "records.json"
    if not input_root.is_dir() or not index.is_file() or not records_path.is_file():
        raise SystemExit("live execution requires input-root/records.json and a regular index file")
    records = json.loads(records_path.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not all(isinstance(row, dict) for row in records):
        raise SystemExit("input-root/records.json must be a list of record objects")
    if args.max_cases < 1 or args.max_cases > len(records):
        raise SystemExit("live execution requires 1 <= max-cases <= saved record count")
    from research.curated.historical_campaign import one
    from research.curated.historical_pipeline import Pipeline
    from research.curated.historical_transport import Client

    output_root.mkdir(parents=True, exist_ok=True)
    if variant.id in {"nonthinking-mechanical", "low-thinking-mechanical", "high-thinking-mechanical", "xhigh-thinking-mechanical"}:
        from research.curated.corpus import Corpus
        from research.curated.historical_common import save
        from research.curated.historical_detector import detect
        from research.curated.historical_pipeline import first_body
        from research.curated.historical_transport import Client
        from research.curated.patching import apply_edits, mechanical
        from research.curated.protected import protected_intervals
        from research.curated.review import Proposal

        client = Client(endpoint=args.endpoint, credential_env=args.credential_env, timeout=args.timeout_seconds, allow_live=True, reasoning_effort=variant.reasoning)
        corpus = Corpus(index)
        completed = 0
        try:
            for number, record in enumerate(records[: args.max_cases], 1):
                text = record["input"]
                candidates = [candidate.as_dict() for candidate in detect(text, corpus, protected_intervals(text), mode="local-context", threshold=3, maximum=variant.maximum_targets)]
                edits = []
                calls = []
                for candidate in candidates:
                    observation = client.call(output_root / "requests" / str(record.get("id", number)), first_body(text, candidate, reasoning_effort=variant.reasoning), "reviewer")
                    calls.append(observation)
                    if observation.get("operational_failure"):
                        continue
                    proposal = observation["proposal"]
                    local = Proposal(bool(proposal["keep"]), proposal.get("replacement"), bool(proposal["needs_wider_edit"]))
                    gate = mechanical(text, candidate, local)
                    if gate["applied"]:
                        edits.append((candidate["start"], candidate["end"], local.replacement))
                corrected = apply_edits(text, edits)
                save(output_root / "records" / f"{record.get('id', number)}.json", {"id": record.get("id", str(number)), "method": "nonthinking-mechanical", "output": corrected, "corrected": corrected, "candidate_count": len(candidates), "calls": len(calls), "network_calls": client.network_calls})
                completed += 1
        finally:
            corpus.close()
        return {"executed": True, "records": completed, "model_calls": client.network_calls, "network_calls": client.network_calls, "output_root": "caller-supplied"}

    english_values = {}
    english_path = input_root / "english.json"
    if english_path.is_file():
        value = json.loads(english_path.read_text(encoding="utf-8"))
        if isinstance(value, dict):
            english_values = {str(key).casefold(): float(number) for key, number in value.items() if isinstance(number, (int, float))}
    if not english_values:
        raise SystemExit("live execution requires caller-owned numeric English evidence in input-root/english.json")
    pipeline = Pipeline(index, english_lookup=lambda word: english_values[word.casefold()], maximum=variant.maximum_targets)
    client = Client(endpoint=args.endpoint, credential_env=args.credential_env, timeout=args.timeout_seconds, allow_live=True)
    completed = 0
    try:
        for number, record in enumerate(records[: args.max_cases], 1):
            example = {"benchmark": record.get("benchmark", variant.id), "id": record.get("id", str(number)), "index": int(record.get("index", number)), "input": record["input"]}
            for method in ("M0", "M1", "M2", "M3"):
                one(example, method, pipeline, client, output_root)
            completed += 1
    finally:
        pipeline.close()
    return {"executed": True, "records": completed, "model_calls": client.network_calls, "network_calls": client.network_calls,
            "output_root": "caller-supplied", "output_manifest_sha256": hashlib.sha256(records_path.read_bytes()).hexdigest()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--index", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--credential-env", required=True)
    parser.add_argument("--endpoint")
    parser.add_argument("--model")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args(argv)
    validate_live_authorization(
        allow_live=args.allow_live,
        endpoint=args.endpoint,
        model=args.model,
        credential_env=args.credential_env,
        input_root=args.input_root,
        index_path=args.index,
        output_root=args.output_root,
        workers=args.workers,
        max_cases=args.max_cases,
        timeout_seconds=args.timeout_seconds,
    )
    variant = plan(args.variant)["variant"]
    result = plan(args.variant)
    result["requested_resources"] = {
        "input_root": "provided-by-caller",
        "index": "provided-by-caller",
        "output_root": "provided-by-caller",
        "credential_reference": args.credential_env,
    }
    if args.allow_live:
        result["execution"] = execute_authorized(args, type("Variant", (), variant)())
        result["executed"] = True
        result["network_calls"] = result["execution"]["network_calls"]
        result["model_calls"] = result["execution"]["model_calls"]
    else:
        result["executed"] = False
        result["network_calls"] = 0
        result["model_calls"] = 0
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
