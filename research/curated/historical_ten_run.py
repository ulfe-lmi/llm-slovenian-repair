"""Faithful ten-run English-preserve driver, parameterized for saved inputs."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import time
from typing import Any

from .english_preserve import classify
from .historical_common import save, sha
from .historical_pipeline import first_body, retry_body
from .historical_transport import Client
from .patching import apply_edits, restore_initial_case
from .review import Proposal
from .gating import check


class PipelineStop(ValueError):
    pass


def prepare(baseline: list[dict[str, Any]], pipeline: Any, english_lookup: Any) -> dict[str, Any]:
    """Copy the historical preparation stage using caller-owned frozen baseline records."""
    selected, delta, bodies, evidence, eligible = {}, {}, {}, {}, 0
    for record in baseline:
        case = record["case"]
        prepared = pipeline.detect(case["text"])
        selected[case["id"]] = prepared["candidates"]
        eligible += prepared["eligible_words"]
        previous = [item["candidate"] for item in record.get("decisions", [])]
        if selected[case["id"]] != previous:
            delta[case["id"]] = {"before": previous, "after": selected[case["id"]]}
        for candidate in selected[case["id"]]:
            key = f"{case['id']}-{candidate['start']}"
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
    edits, no_retry_edits, decisions, english_records, calls = [], [], [], [], []
    for candidate in candidates:
        key = f"{case['id']}-{candidate['start']}"
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
