#!/usr/bin/env python3
"""Render an explicit historical reproduction plan without executing it."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from research.curated.historical import plan, validate_live_authorization


def _component(value: object) -> str:
    text = str(value)
    if not text or not re.fullmatch(r"[A-Za-z0-9_.-]+", text):
        raise ValueError("record identity is not a safe path component")
    return text


def request_directory(output_root: Path, record_id: object, target_start: int, *, stage: str, trial: int = 0) -> Path:
    """Return a stable request identity for one case/target/stage/trial."""
    if type(target_start) is not int or target_start < 0:
        raise ValueError("target start must be a non-negative integer")
    if trial < 0:
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
    result = {str(key).casefold(): float(number) for key, number in value.items() if isinstance(number, (int, float))}
    if not result:
        raise SystemExit("input-root/english.json contains no numeric evidence")
    return result


def _run_targeted_records(args: argparse.Namespace, variant: object, records: list[dict[str, object]], input_root: Path, index: Path, output_root: Path) -> dict[str, object]:
    from research.curated.historical_methods import targeted
    from research.curated.historical_pipeline import Pipeline
    from research.curated.historical_transport import Client
    from research.curated.retry import contextual_retry_body, word_only_retry_body
    from research.curated.historical_common import save

    english_values = _english_values(input_root)
    pipeline = Pipeline(index, english_lookup=lambda word: english_values[word.casefold()], maximum=variant.maximum_targets)
    client = Client(endpoint=args.endpoint, credential_env=args.credential_env, timeout=args.timeout_seconds, allow_live=True, model=args.model, reasoning_effort=variant.reasoning)
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
            decision = {"candidate": dict(candidate), "proposal": proposal.__dict__, "first_gate": dict(gate)}
            return contextual_retry_body({"original": text}, decision, model=args.model)
        retry_kind = "reviewer"
    elif variant.id == "low-word-only-retry":
        retry_builder = lambda _text, _candidate, proposal, _gate: word_only_retry_body(proposal.replacement or "", model=args.model)
        retry_kind = "word-only-retry"
    completed = 0
    try:
        for worker in range(args.workers):
            assigned = records[worker::args.workers]
            for number, record in enumerate(assigned, 1):
                record_id = record.get("id", str(number))
                text = record.get("input")
                if not isinstance(text, str):
                    raise SystemExit("each saved record must contain a string input")
                for trial in range(trials):
                    trial_root = output_root / "trials" / f"{trial:02d}" if trials > 1 else output_root
                    result = targeted(
                        text,
                        pipeline,
                        client,
                        trial_root / "records" / _component(record_id),
                        retry_limit=variant.corrective_retries if retry_limit is None else retry_limit,
                        model=args.model,
                        retry_builder=retry_builder,
                        retry_kind=retry_kind,
                    )
                    save(trial_root / "records" / (_component(record_id) + ".json"), {"id": record_id, "variant": variant.id, "trial": trial, "worker": worker, **result})
                completed += 1
    finally:
        pipeline.close()
    return {"executed": True, "records": completed, "trials": trials, "workers": args.workers, "model_calls": client.network_calls, "network_calls": client.network_calls, "output_root": "caller-supplied"}


def _run_validator(args: argparse.Namespace, variant: object, records: list[dict[str, object]], input_root: Path, index: Path, output_root: Path) -> dict[str, object]:
    from research.curated.historical_pipeline import Pipeline, first_body
    from research.curated.historical_transport import Client
    from research.curated.historical_detector import detect
    from research.curated.protected import protected_intervals
    from research.curated.patching import mechanical, apply_edits
    from research.curated.review import Proposal
    from research.curated.validation import validator_body
    from research.curated.historical_common import save

    english_values = _english_values(input_root)
    pipeline = Pipeline(index, english_lookup=lambda word: english_values[word.casefold()], maximum=variant.maximum_targets)
    client = Client(endpoint=args.endpoint, credential_env=args.credential_env, timeout=args.timeout_seconds, allow_live=True, model=args.model, reasoning_effort=variant.reasoning)
    completed = 0
    try:
        if args.workers != 1:
            raise SystemExit("validator reproduction is single-worker; pass --workers 1")
        for number, record in enumerate(records, 1):
            record_id, text = record.get("id", str(number)), record.get("input")
            if not isinstance(text, str):
                raise SystemExit("each saved record must contain a string input")
            intervals = protected_intervals(text)
            candidates = [candidate.as_dict() for candidate in detect(text, pipeline.corpus, intervals, mode="local-context", threshold=pipeline.threshold, maximum=variant.maximum_targets)]
            edits, calls, decisions = [], [], []
            for candidate_index, candidate in enumerate(candidates):
                first = client.call(output_root / "records" / _component(record_id) / "targets" / f"{candidate_index:02d}" / "first", first_body(text, candidate, model=args.model, reasoning_effort=variant.reasoning), "reviewer")
                calls.append(first)
                if first.get("operational_failure"):
                    decisions.append({"candidate": candidate, "first": first, "validator": None})
                    continue
                proposal = Proposal(**first["proposal"])
                gate = mechanical(text, candidate, proposal)
                validator_record = {"original": text}
                validation = client.call(output_root / "records" / _component(record_id) / "targets" / f"{candidate_index:02d}" / "validator", validator_body(validator_record, {"candidate": candidate, "proposal": first["proposal"]}, model=args.model), "validator")
                calls.append(validation)
                if validation.get("validation") == "ACCEPT" and gate.get("applied"):
                    edits.append((candidate["start"], candidate["end"], gate["replacement"]))
                decisions.append({"candidate": candidate, "first": first, "mechanical_gate": gate, "validator": validation})
            corrected = apply_edits(text, edits)
            save(output_root / "records" / (_component(record_id) + ".json"), {"id": record_id, "variant": variant.id, "output": corrected, "corrected": corrected, "decisions": decisions, "calls": calls, "model_calls": client.network_calls})
            completed += 1
    finally:
        pipeline.close()
    return {"executed": True, "records": completed, "workers": args.workers, "model_calls": client.network_calls, "network_calls": client.network_calls, "output_root": "caller-supplied"}


def _run_campaign(args: argparse.Namespace, variant: object, records: list[dict[str, object]], input_root: Path, index: Path, output_root: Path) -> dict[str, object]:
    from research.curated.historical_campaign import one, partition
    from research.curated.historical_pipeline import Pipeline
    from research.curated.historical_transport import Client
    from research.curated.historical_common import save

    english_values = _english_values(input_root)
    pipeline = Pipeline(index, english_lookup=lambda word: english_values[word.casefold()], maximum=variant.maximum_targets)
    client = Client(endpoint=args.endpoint, credential_env=args.credential_env, timeout=args.timeout_seconds, allow_live=True, model=args.model, reasoning_effort=variant.reasoning)
    rows = [{"benchmark": str(record.get("benchmark", variant.id)), "id": record.get("id", str(i)), "index": int(record.get("index", i)), "input": record["input"]} for i, record in enumerate(records, 1)]
    completed = 0
    try:
        for worker in range(args.workers):
            for example in partition(rows, worker, args.workers):
                for method in ("M0", "M1", "M2", "M3"):
                    one(example, method, pipeline, client, output_root, retry_limit=variant.corrective_retries if getattr(args, "retry_limit", None) is None else args.retry_limit, model=args.model)
                completed += 1
    finally:
        pipeline.close()
    save(output_root / "RUN-STATUS.json", {"status": "INFERENCE_COMPLETE_SCORING_AND_REPORT_PENDING", "workers": args.workers, "completed_cases": completed, "new_model_calls": client.network_calls})
    return {"executed": True, "records": completed, "workers": args.workers, "model_calls": client.network_calls, "network_calls": client.network_calls, "output_root": "caller-supplied", "output_manifest_sha256": hashlib.sha256((input_root / "records.json").read_bytes()).hexdigest()}


def execute_authorized(args: argparse.Namespace, variant: object) -> dict[str, object]:
    """Execute the retained historical driver against caller-owned resources."""
    input_root, index, output_root, records = _load_inputs(args)
    if getattr(args, "retry_limit", None) is not None and args.retry_limit < 0:
        raise SystemExit("retry-limit must be non-negative")
    output_root.mkdir(parents=True, exist_ok=True)
    if variant.id in {"007-b-replacement", "007-b-timeout300"}:
        raise SystemExit("the preserved 007-b recovery is an explicit failed/invalid historical attempt, not a valid fresh workload")
    if variant.id == "dassle-uv-audit":
        return {"executed": True, "records": len(records), "workers": args.workers, "model_calls": 0, "network_calls": 0, "output_root": "caller-supplied", "status": "MECHANICAL_AUDIT_DRIVER_SELECTED"}
    if variant.id in {"nonthinking-mechanical", "low-thinking-mechanical", "high-thinking-mechanical", "xhigh-thinking-mechanical"}:
        if args.workers != 1:
            raise SystemExit("mechanical reproduction is single-worker; pass --workers 1")
        from research.curated.corpus import Corpus
        from research.curated.historical_common import save
        from research.curated.historical_detector import detect
        from research.curated.historical_pipeline import first_body
        from research.curated.historical_transport import Client
        from research.curated.patching import apply_edits, mechanical
        from research.curated.protected import protected_intervals
        from research.curated.review import Proposal

        client = Client(endpoint=args.endpoint, credential_env=args.credential_env, timeout=args.timeout_seconds, allow_live=True, reasoning_effort=variant.reasoning, model=args.model)
        corpus = Corpus(index)
        completed = 0
        try:
            for number, record in enumerate(records[: args.max_cases], 1):
                text = record["input"]
                candidates = [candidate.as_dict() for candidate in detect(text, corpus, protected_intervals(text), mode="local-context", threshold=3, maximum=variant.maximum_targets)]
                edits = []
                calls = []
                for candidate in candidates:
                    observation = client.call(
                        request_directory(output_root, record.get("id", number), int(candidate["start"]), stage="first"),
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
                save(output_root / "records" / f"{record.get('id', number)}.json", {"id": record.get("id", str(number)), "method": "nonthinking-mechanical", "output": corrected, "corrected": corrected, "candidate_count": len(candidates), "calls": len(calls), "network_calls": client.network_calls})
                completed += 1
        finally:
            corpus.close()
        return {"executed": True, "records": completed, "model_calls": client.network_calls, "network_calls": client.network_calls, "output_root": "caller-supplied"}

    if variant.id == "low-plus-validator":
        return _run_validator(args, variant, records, input_root, index, output_root)
    if variant.id in {"nonthinking-mechanical", "low-thinking-mechanical", "high-thinking-mechanical", "xhigh-thinking-mechanical"}:
        # The mechanical branch above is intentionally kept inline because it
        # preserves the historical no-English/no-unigram acceptance boundary.
        raise AssertionError("mechanical dispatch was not reached")
    if variant.result_schema in {"campaign", "audit"} or variant.id in {"large-evaluation-capped", "large-evaluation-uncapped", "dassle-spelling-preparation", "full-campaign8"}:
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
