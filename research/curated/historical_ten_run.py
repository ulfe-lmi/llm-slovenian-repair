"""Faithful ten-run English-preserve driver, parameterized for saved inputs."""

from __future__ import annotations

import time
from collections import Counter
from pathlib import Path
from typing import Any

from .english_preserve import classify
from .historical_common import safe_component, save
from .historical_methods import targeted
from .historical_pipeline import first_body, retry_body
from .historical_transport import Client
from .patching import apply_edits
from .review import Proposal


class PipelineStop(ValueError):
    pass


def prepare(baseline: list[dict[str, Any]], pipeline: Any, english_lookup: Any) -> dict[str, Any]:
    """Copy the historical preparation stage using caller-owned frozen baseline records."""
    selected, delta, bodies, evidence, eligible = {}, {}, {}, {}, 0
    for record in baseline:
        case = record["case"]
        prepared = pipeline.detect(case["text"])
        case_id = safe_component(case["id"], label="case identity")
        selected[case_id] = prepared["candidates"]
        eligible += prepared["eligible_words"]
        previous = [item["candidate"] for item in record.get("decisions", [])]
        if selected[case_id] != previous:
            delta[case_id] = {"before": previous, "after": selected[case_id]}
        for candidate in selected[case_id]:
            key = f"{case_id}-{candidate['start']}"
            bodies[key] = first_body(case["text"], candidate)
            evidence[key] = classify(candidate, english_lookup)
    return {"mode": "fresh-full-low-expression-retry-english-preserve", "cases": [record["case"] for record in baseline],
            "selected": selected, "detector_delta": delta, "eligible_words": eligible, "reviewer_bodies": bodies,
            "english_evidence": evidence, "expected_first_calls": sum(not item["review_suppressed"] for item in evidence.values()),
            "max_retry_per_target": 1, "timeout_seconds": 300, "concurrency": 1, "detector_mode": "local-context",
            "threshold": pipeline.threshold, "maximum": pipeline.maximum, "new_model_calls": 0}


def preserve_initial_case(original: str, proposal: dict[str, Any] | Proposal) -> tuple[dict[str, Any], dict[str, Any]]:
    if isinstance(proposal, Proposal):
        value = {"keep": proposal.keep, "replacement": proposal.replacement, "needs_wider_edit": proposal.needs_wider_edit}
    else:
        value = dict(proposal)
    upper = len(original) >= 2 and original[0].isupper() and original[1].islower()
    lower = bool(original) and original[0].islower()
    direction = "upper" if upper else "lower" if lower else None
    replacement = value["replacement"]
    if direction and not value["keep"] and not value["needs_wider_edit"] and replacement:
        value["replacement"] = (replacement[0].upper() if direction == "upper" else replacement[0].lower()) + replacement[1:]
    return value, {"eligible_original": direction is not None, "direction": direction, "changed": value["replacement"] != replacement,
                   "raw_replacement": replacement, "adjusted_replacement": value["replacement"]}


def process_case(case: dict[str, Any], candidates: list[dict[str, Any]], state: dict[str, Any], pipeline: Any, client: Client, output_root: str | Path) -> dict[str, Any]:
    root = Path(output_root)
    case_id = safe_component(case["id"], label="case identity")
    edits, no_retry_edits, decisions, english_records, calls = [], [], [], [], []
    for candidate in candidates:
        key = f"{case_id}-{candidate['start']}"
        english = state["english_evidence"][key]
        if english["original_target"] != candidate["text"]:
            raise ValueError("frozen English evidence target mismatch")
        english_records.append({"candidate": candidate, "english_evidence": english})
        if english["review_suppressed"]:
            continue
        first = client.call(root / "targets" / key / "first", first_body(case["text"], candidate), "reviewer")
        calls.append(first)
        if first.get("operational_failure"):
            raise PipelineStop(first.get("failure", "reviewer failure"))
        proposal, first_case = preserve_initial_case(candidate["text"], first["proposal"])
        adjusted = Proposal(**proposal)
        first_gate = pipeline.gate(case["text"], candidate, adjusted)[2]
        final, final_proposal, final_case, retry = first_gate, proposal, first_case, None
        if first_gate["accepted"]:
            no_retry_edits.append((candidate["start"], candidate["end"], proposal["replacement"]))
        if first_gate["reason"] == "replacement-unigram-uncertain":
            retry = client.call(root / "targets" / key / "retry", retry_body(proposal["replacement"]), "expression-retry")
            calls.append(retry)
            if retry.get("operational_failure"):
                raise PipelineStop(retry.get("failure", "retry failure"))
            final_proposal, final_case = preserve_initial_case(candidate["text"], retry["proposal"])
            final = pipeline.gate(case["text"], candidate, Proposal(**final_proposal))[2]
        if final["accepted"]:
            edits.append((candidate["start"], candidate["end"], final_proposal["replacement"]))
        decisions.append({"key": key, "candidate": candidate, "first_proposal_raw": first["proposal"], "first_proposal": proposal,
                          "first_case_adjustment": first_case, "first_gate": first_gate, "retry_proposal_raw": retry.get("proposal") if retry else None,
                          "final_proposal": final_proposal, "final_case_adjustment": final_case, "final_gate": final, "reviewer_observation": first, "retry_observation": retry})
    corrected = apply_edits(case["text"], edits)
    return {"case": case, "original": case["text"], "corrected": corrected, "edits": edits, "decisions": decisions,
            "english_evidence": english_records, "unigram_without_retry_corrected": apply_edits(case["text"], no_retry_edits),
            "exact_gold_output": corrected == (case["text"][:case["start"]] + str(case["gold"]) + case["text"][case["end"]:] if case.get("known_error") else case["text"]),
            "changed": corrected != case["text"], "protected_differences": 0, "outside_edit_differences": 0, "calls": calls}


def run(cases: list[dict[str, Any]], state: dict[str, Any], pipeline: Any, client: Client, output_root: str | Path) -> dict[str, Any]:
    started, records = time.monotonic(), []
    for case in cases:
        record = process_case(case, state["selected"][case["id"]], state, pipeline, client, output_root)
        records.append(record)
        save(Path(output_root) / "cases" / f"{case['id']}.json", record)
    calls = [call for record in records for call in record["calls"]]
    return {"status": "COMPLETED", "cases": len(records), "fresh_reviewer_calls": sum(call.get("kind") == "reviewer" for call in calls),
            "corrective_calls": sum(call.get("kind") == "expression-retry" for call in calls), "total_calls": len(calls),
            "first_gate_reasons": dict(Counter(decision["first_gate"]["reason"] for record in records for decision in record["decisions"])),
            "applied_edits": sum(len(record["edits"]) for record in records), "full_pipeline_seconds": time.monotonic() - started,
            "new_model_calls": client.network_calls}


def run_scheduled_trials(
    records: list[dict[str, Any]],
    variant_id: str,
    pipeline: Any,
    client: Client,
    output_root: str | Path,
    *,
    trials: int = 10,
    retry_limit: int = 1,
    model: str = "qwen3.8-27b",
) -> dict[str, Any]:
    """Run the original predetermined scheduler with immutable trial paths.

    A stopped trial is recorded and the next already-scheduled trial starts
    unchanged.  There is no resampling, replacement trial, or shared request
    directory across trials.
    """
    if not 1 <= trials <= 10:
        raise ValueError("historical ten-run scheduler requires 1 <= trials <= 10")
    if retry_limit < 0:
        raise ValueError("retry limit must be non-negative")
    root = Path(output_root)
    record_ids = [safe_component(record.get("id", number)) for number, record in enumerate(records, 1)]
    schedule = {
        "ten-run-initial-case-low": {"name": "symmetric-initial-case", "retry_kind": "word-only"},
        "ten-run-expression-retry-low": {"name": "expression-retry", "retry_kind": "expression"},
        "ten-run-english-preserve-low": {"name": "english-preserve", "retry_kind": "expression"},
    }.get(variant_id)
    if schedule is None:
        raise ValueError("unknown ten-run historical family")
    save(root / "BATCH-FROZEN.json", {
        "variant": variant_id,
        "schedule": schedule["name"],
        "scheduled_trials": trials,
        "failed_trial_policy": "record stopped trial and continue next pre-scheduled trial unchanged",
        "request_identity": "case/target/stage/trial",
        "max_corrective_retries": retry_limit,
    })
    trial_rows: list[dict[str, Any]] = []
    for trial in range(1, trials + 1):
        trial_root = root / "trials" / f"{trial:02d}"
        trial_root.mkdir(parents=True, exist_ok=True)
        stopped = False
        completed_cases = 0
        trial_start_calls = client.network_calls
        for _number, (record_id, record) in enumerate(zip(record_ids, records, strict=True), 1):
            text = record.get("input", record.get("original"))
            if not isinstance(text, str):
                raise ValueError("each ten-run record must contain input")
            retry_builder = None
            retry_kind = "expression-retry"
            if schedule["retry_kind"] == "word-only":
                from .retry import proposal_replacement, word_only_retry_body

                retry_kind = "word-only-retry"
                def retry_builder(_text, _candidate, proposal, _gate):
                    return word_only_retry_body(proposal_replacement(proposal), model=model)
            result = targeted(
                text,
                pipeline,
                client,
                trial_root / "records" / record_id,
                retry_limit=retry_limit,
                model=model,
                retry_builder=retry_builder,
                retry_kind=retry_kind,
            )
            save(trial_root / "records" / (record_id + ".json"), {
                "id": record_id,
                "variant": variant_id,
                "trial": trial,
                **result,
            })
            completed_cases += 1
            if result.get("operational_failure"):
                stopped = True
                break
        status = "STOPPED" if stopped else "COMPLETE"
        trial_rows.append({
            "trial": trial,
            "status": status,
            "exit_code": 2 if stopped else 0,
            "completed_case_instances": completed_cases,
            "scheduled_case_instances": len(records),
            "model_calls": client.network_calls - trial_start_calls,
            "request_identity": f"trials/{trial:02d}",
        })
    summary_status = "COMPLETED" if all(item["status"] == "COMPLETE" for item in trial_rows) else "COMPLETED_WITH_STOPPED_TRIALS"
    summary = {
        "status": summary_status,
        "variant": variant_id,
        "scheduled_trials": trials,
        "attempted_trials": len(trial_rows),
        "complete_trials": sum(item["status"] == "COMPLETE" for item in trial_rows),
        "stopped_trials": sum(item["status"] == "STOPPED" for item in trial_rows),
        "trials": trial_rows,
        "model_calls": client.network_calls,
        "network_calls": client.network_calls,
        "records": len(records),
        "workers": 1,
        "output_root": "caller-supplied",
    }
    save(root / "BATCH-SUMMARY.json", summary)
    return {"executed": True, **summary}
