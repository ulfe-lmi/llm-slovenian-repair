#!/usr/bin/env python3
"""Render or execute the preserved historical reproduction drivers."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from research.curated.historical import plan, validate_live_authorization
from research.curated.historical_common import safe_component


def _component(value: object) -> str:
    return safe_component(value)


def request_directory(output_root: Path, record_id: object, target_start: int, *, stage: str, trial: int = 0) -> Path:
    """Return a stable request identity for one case/target/stage/trial."""
    if type(target_start) is not int or target_start < 0:
        raise ValueError("target start must be a non-negative integer")
    if type(trial) is not int or trial < 0:
        raise ValueError("trial must be non-negative")
    return output_root / "requests" / _component(record_id) / f"target-{target_start:08d}" / _component(stage) / f"trial-{trial:04d}"


def _load_inputs(args: argparse.Namespace) -> tuple[Path, Path, Path, list[dict[str, object]]]:
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
    return input_root, index, output_root, records[: args.max_cases]


def _english_values(input_root: Path) -> dict[str, float]:
    english_path = input_root / "english.json"
    if not english_path.is_file():
        raise SystemExit("this historical variant requires caller-owned numeric English evidence in input-root/english.json")
    value = json.loads(english_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit("input-root/english.json must be an object of numeric frequencies")
    result = {}
    for key, number in value.items():
        if not isinstance(key, str) or type(number) not in (int, float) or not math.isfinite(float(number)):
            raise SystemExit("input-root/english.json must contain finite numeric frequencies")
        result[key.casefold()] = float(number)
    if not result:
        raise SystemExit("input-root/english.json contains no numeric evidence")
    return result


def _client(args: argparse.Namespace, *, reasoning: str):
    from research.curated.historical_transport import Client

    return Client(
        endpoint=args.endpoint,
        credential_env=args.credential_env,
        timeout=args.timeout_seconds,
        allow_live=True,
        model=args.model,
        reasoning_effort=reasoning,
    )


def _early_pipeline(index: Path, variant: object):
    from research.curated.historical_variants import build_historical_pipeline

    hyphen_variants = {
        "full-hyphen-space-low",
        "full-hyphen-case-low",
        "ten-run-initial-case-low",
        "ten-run-expression-retry-low",
    }
    case_rule = "one-way" if variant.id == "full-hyphen-case-low" else "symmetric" if variant.id in {"ten-run-initial-case-low", "ten-run-expression-retry-low"} else "none"
    return build_historical_pipeline(
        index,
        maximum=variant.maximum_targets,
        case_rule=case_rule,
        detector_view="hyphen-space" if variant.id in hyphen_variants else "raw",
    )


def _latest_pipeline(index: Path, variant: object, input_root: Path):
    from research.curated.historical_pipeline import Pipeline

    english_values = _english_values(input_root)

    def lookup(word: str) -> float:
        key = word.casefold()
        if key not in english_values:
            raise SystemExit("caller-owned English evidence is missing for an evaluated target")
        return english_values[key]

    return Pipeline(index, english_lookup=lookup, maximum=variant.maximum_targets)


def _validate_record_ids(records: list[dict[str, object]]) -> None:
    """Reject unsafe IDs before creating any caller-owned output."""
    for number, record in enumerate(records, 1):
        _component(record.get("id", number))


def _run_targeted_records(args: argparse.Namespace, variant: object, records: list[dict[str, object]], input_root: Path, index: Path, output_root: Path) -> dict[str, object]:
    from research.curated.historical_common import save
    from research.curated.historical_methods import targeted
    from research.curated.retry import (
        contextual_retry_body,
        proposal_replacement,
        word_only_retry_body,
    )

    if args.workers != 1:
        raise SystemExit("targeted historical variants are single-worker; pass --workers 1")
    # These variants predate the later English-preservation study.  They use a
    # separate source-family pipeline, so absence of english.json is intentional.
    pipeline = _early_pipeline(index, variant)
    client = _client(args, reasoning=variant.reasoning)
    trials = getattr(args, "trials", 1)
    retry_limit = getattr(args, "retry_limit", None)
    if retry_limit is not None and retry_limit < 0:
        raise SystemExit("retry-limit must be non-negative")
    if variant.id.startswith("ten-run-"):
        if trials < 1 or trials > 10:
            raise SystemExit("ten-run variants require 1 <= trials <= 10")
    else:
        if trials != 1:
            raise SystemExit("--trials is only valid for ten-run historical variants")
        trials = 1
    retry_builder = None
    retry_kind = "expression-retry"
    if variant.id == "low-unigram-retry":
        def retry_builder(text, candidate, proposal, gate):
            proposal_value = proposal.__dict__ if hasattr(proposal, "__dict__") else dict(proposal)
            decision = {"candidate": dict(candidate), "proposal": proposal_value, "first_gate": dict(gate)}
            return contextual_retry_body({"original": text}, decision, model=args.model)
        retry_kind = "reviewer"
    elif variant.id in {"low-word-only-retry", "full-hyphen-space-low", "full-hyphen-case-low"}:
        def retry_builder(_text, _candidate, proposal, _gate):
            return word_only_retry_body(proposal_replacement(proposal), model=args.model)
        retry_kind = "word-only-retry"
    completed = 0
    try:
        for number, record in enumerate(records, 1):
            record_id = _component(record.get("id", number))
            text = record.get("input")
            if not isinstance(text, str):
                raise SystemExit("each saved record must contain a string input")
            for trial in range(trials):
                trial_root = output_root / "trials" / f"{trial:02d}" if trials > 1 else output_root
                result = targeted(
                    text,
                    pipeline,
                    client,
                    trial_root / "records" / record_id,
                    retry_limit=variant.corrective_retries if retry_limit is None else retry_limit,
                    model=args.model,
                    retry_builder=retry_builder,
                    retry_kind=retry_kind,
                )
                save(trial_root / "records" / (record_id + ".json"), {"id": record_id, "variant": variant.id, "trial": trial, "worker": 0, **result})
            completed += 1
    finally:
        pipeline.close()
    return {"executed": True, "records": completed, "trials": trials, "workers": args.workers, "model_calls": client.network_calls, "network_calls": client.network_calls, "output_root": "caller-supplied"}


def _run_saved_first_stage_records(
    args: argparse.Namespace,
    variant: object,
    records: list[dict[str, object]],
    index: Path,
    output_root: Path,
) -> dict[str, object]:
    """Run retry-only studies from caller-owned frozen first-stage decisions."""
    from research.curated.historical_methods import saved_first_stage_retry
    from research.curated.historical_common import save
    from research.curated.retry import contextual_retry_body, proposal_replacement, word_only_retry_body

    if args.workers != 1:
        raise SystemExit("saved-first-stage retry variants are single-worker; pass --workers 1")
    if variant.id not in {"low-unigram-retry", "low-word-only-retry"}:
        raise SystemExit("saved-first-stage retry is only valid for the two retry-only studies")
    pipeline = _early_pipeline(index, variant)
    client = _client(args, reasoning=variant.reasoning)
    if variant.id == "low-unigram-retry":
        def retry_builder(text, candidate, proposal, gate):
            return contextual_retry_body(
                {"original": text},
                {"candidate": dict(candidate), "proposal": proposal.__dict__, "first_gate": dict(gate)},
                model=args.model,
            )

        retry_kind = "reviewer"
    else:
        def retry_builder(_text, _candidate, proposal, _gate):
            return word_only_retry_body(proposal_replacement(proposal), model=args.model)

        retry_kind = "word-only-retry"
    completed = 0
    reused = 0
    try:
        for number, record in enumerate(records, 1):
            record_id = _component(record.get("id", number))
            text = record.get("input", record.get("original"))
            if not isinstance(text, str):
                raise SystemExit("each saved record must contain a string input")
            frozen = next(
                (record.get(name) for name in ("first_stage", "first_stage_decisions", "frozen_decisions", "decisions") if isinstance(record.get(name), list)),
                None,
            )
            if frozen is None:
                raise SystemExit("retry-only live reproduction requires caller-owned frozen first-stage decisions")
            result = saved_first_stage_retry(
                text,
                pipeline,
                client,
                output_root / "records" / record_id,
                frozen,
                retry_builder=retry_builder,
                retry_kind=retry_kind,
                retry_limit=1 if args.retry_limit is None else args.retry_limit,
                model=args.model,
            )
            save(output_root / "records" / (record_id + ".json"), {"id": record_id, "variant": variant.id, **result})
            reused += result["first_stage_calls_reused"]
            completed += 1
    finally:
        pipeline.close()
    return {
        "executed": True,
        "records": completed,
        "workers": 1,
        "first_stage_calls_reused": reused,
        "first_stage_calls_executed": 0,
        "model_calls": client.network_calls,
        "network_calls": client.network_calls,
        "output_root": "caller-supplied",
    }


def _run_validator(args: argparse.Namespace, variant: object, records: list[dict[str, object]], input_root: Path, index: Path, output_root: Path) -> dict[str, object]:
    from research.curated.historical_validator import run_validator_records

    if args.workers != 1:
        raise SystemExit("validator reproduction is single-worker; pass --workers 1")
    client = _client(args, reasoning=variant.reasoning)
    return run_validator_records(records, client, output_root, model=args.model)


def _run_campaign(args: argparse.Namespace, variant: object, records: list[dict[str, object]], input_root: Path, index: Path, output_root: Path) -> dict[str, object]:
    from research.curated.historical_campaign import run_injected

    rows = []
    for i, record in enumerate(records, 1):
        benchmark = safe_component(record.get("benchmark", variant.id), label="benchmark identity")
        record_id = _component(record.get("id", i))
        index_value = record.get("index", i)
        if type(index_value) is not int or index_value < 1:
            raise SystemExit("campaign record index must be a positive integer")
        if not isinstance(record.get("input"), str):
            raise SystemExit("campaign record lacks a string input")
        rows.append({"benchmark": benchmark, "id": record_id, "index": index_value, "input": record["input"]})
    retry_limit = variant.corrective_retries if getattr(args, "retry_limit", None) is None else args.retry_limit
    if retry_limit < 0:
        raise SystemExit("retry-limit must be non-negative")

    def pipeline_factory():
        return _latest_pipeline(index, variant, input_root)

    def client_factory():
        return _client(args, reasoning=variant.reasoning)

    return run_injected(
        rows,
        output_root=output_root,
        workers=args.workers,
        pipeline_factory=pipeline_factory,
        client_factory=client_factory,
        retry_limit=retry_limit,
        model=args.model,
    )


def execute_authorized(args: argparse.Namespace, variant: object) -> dict[str, object]:
    """Execute the retained historical driver against caller-owned resources."""
    input_root, index, output_root, records = _load_inputs(args)
    if getattr(args, "retry_limit", None) is not None and args.retry_limit < 0:
        raise SystemExit("retry-limit must be non-negative")
    _validate_record_ids(records)
    output_root.mkdir(parents=True, exist_ok=True)
    if variant.id in {"007-b-replacement", "007-b-timeout300"}:
        raise SystemExit("the preserved 007-b recovery is an explicit failed/invalid historical attempt, not a valid fresh workload")
    if variant.id == "dassle-uv-audit":
        from research.curated.historical_dassle import run_audit_records

        if args.workers != 1:
            raise SystemExit("DASSLE audit is a single-process mechanical driver; pass --workers 1")
        result = run_audit_records(records)
        from research.curated.historical_common import save

        save(output_root / "AUDIT.json", result)
        return {"executed": True, "records": len(records), "workers": args.workers, "model_calls": 0, "network_calls": 0, "output_root": "caller-supplied", **result}
    if variant.id == "levenshtein-lookup-diagnostic":
        from research.curated.historical_common import save

        if args.workers != 1:
            raise SystemExit("the unavailable lookup diagnostic is single-process; pass --workers 1")
        result = {
            "status": "UNAVAILABLE_INLINE_LEVENSHTEIN_SOURCE",
            "records": len(records),
            "new_model_calls": 0,
            "network_calls": 0,
            "source_identity": "no standalone source hash was preserved",
        }
        save(output_root / "DIAGNOSTIC.json", result)
        return {"executed": True, "workers": args.workers, "model_calls": 0, "output_root": "caller-supplied", **result}
    if variant.id in {"nonthinking-mechanical", "low-thinking-mechanical", "high-thinking-mechanical", "xhigh-thinking-mechanical"}:
        if args.workers != 1:
            raise SystemExit("mechanical reproduction is single-worker; pass --workers 1")
        from research.curated.historical_common import save
        from research.curated.historical_pipeline import first_body
        from research.curated.historical_transport import Client
        from research.curated.patching import apply_edits, mechanical
        from research.curated.review import Proposal

        client = Client(endpoint=args.endpoint, credential_env=args.credential_env, timeout=args.timeout_seconds, allow_live=True, reasoning_effort=variant.reasoning, model=args.model)
        pipeline = _early_pipeline(index, variant)
        completed = 0
        try:
            for number, record in enumerate(records[: args.max_cases], 1):
                text = record.get("input")
                if not isinstance(text, str):
                    raise SystemExit("each saved record must contain a string input")
                record_id = _component(record.get("id", number))
                candidates = pipeline.detect(text)["candidates"]
                edits, calls = [], []
                for candidate in candidates:
                    observation = client.call(
                        request_directory(output_root, record_id, int(candidate["start"]), stage="first"),
                        first_body(text, candidate, model=args.model, reasoning_effort=variant.reasoning),
                        "reviewer",
                    )
                    calls.append(observation)
                    if observation.get("operational_failure"):
                        continue
                    proposal = observation["proposal"]
                    local = Proposal(bool(proposal["keep"]), proposal.get("replacement"), bool(proposal["needs_wider_edit"]))
                    gate = mechanical(text, candidate, local)
                    if gate["applied"]:
                        edits.append((candidate["start"], candidate["end"], local.replacement))
                corrected = apply_edits(text, edits)
                save(output_root / "records" / f"{record_id}.json", {"id": record_id, "variant": variant.id, "method": variant.id, "output": corrected, "corrected": corrected, "candidate_count": len(candidates), "calls": len(calls), "network_calls": client.network_calls})
                completed += 1
        finally:
            pipeline.close()
        return {"executed": True, "records": completed, "model_calls": client.network_calls, "network_calls": client.network_calls, "output_root": "caller-supplied"}

    if variant.id == "low-plus-validator":
        return _run_validator(args, variant, records, input_root, index, output_root)
    if variant.id in {"low-unigram-retry", "low-word-only-retry"} and any(
        isinstance(record.get(name), list)
        for record in records
        for name in ("first_stage", "first_stage_decisions", "frozen_decisions", "decisions")
    ):
        return _run_saved_first_stage_records(args, variant, records, index, output_root)
    if variant.id in {"ten-run-initial-case-low", "ten-run-expression-retry-low", "ten-run-english-preserve-low"}:
        from research.curated.historical_ten_run import run_scheduled_trials

        if args.trials < 1 or args.trials > 10:
            raise SystemExit("ten-run variants require 1 <= trials <= 10")
        if args.workers != 1:
            raise SystemExit("ten-run historical drivers are sequential; pass --workers 1")
        if variant.id == "ten-run-english-preserve-low":
            pipeline = _latest_pipeline(index, variant, input_root)
        else:
            pipeline = _early_pipeline(index, variant)
        client = _client(args, reasoning=variant.reasoning)
        try:
            return run_scheduled_trials(
                records,
                variant.id,
                pipeline,
                client,
                output_root,
                trials=args.trials,
                retry_limit=variant.corrective_retries if args.retry_limit is None else args.retry_limit,
                model=args.model,
            )
        finally:
            pipeline.close()
    if variant.id == "prijigrala-retry10":
        from research.curated.historical_retry10 import run_record

        if args.workers != 1:
            raise SystemExit("retry10 is a single-target sequential driver; pass --workers 1")
        pipeline = _latest_pipeline(index, variant, input_root)
        client = _client(args, reasoning=variant.reasoning)
        try:
            if len(records) != 1:
                raise SystemExit("retry10 requires exactly one caller-selected record")
            result = run_record(
                records[0], pipeline, client, output_root,
                max_retries=variant.corrective_retries if args.retry_limit is None else args.retry_limit,
                model=args.model,
            )
            return {"executed": True, "records": 1, "workers": 1, "model_calls": client.network_calls, "network_calls": client.network_calls, "output_root": "caller-supplied", "status": result["status"], "corrective_calls": result["corrective_calls"]}
        finally:
            pipeline.close()
    if variant.id in {"nonthinking-mechanical", "low-thinking-mechanical", "high-thinking-mechanical", "xhigh-thinking-mechanical"}:
        # The mechanical branch above is intentionally kept inline because it
        # preserves the historical no-English/no-unigram acceptance boundary.
        raise AssertionError("mechanical dispatch was not reached")
    if variant.result_schema in {"campaign"} or variant.id in {"large-evaluation-capped", "large-evaluation-uncapped", "dassle-spelling-preparation", "full-campaign8"}:
        return _run_campaign(args, variant, records, input_root, index, output_root)
    return _run_targeted_records(args, variant, records, input_root, index, output_root)


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
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--retry-limit", type=int)
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
