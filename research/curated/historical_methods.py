"""Historical M0/M1/M2/M3 methods with durable failure accounting."""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from .corpus import Corpus
from .historical_pipeline import MODEL, first_body, patch, retry_body
from .historical_transport import _save, text_body
from .review import Proposal


def identity(text: str) -> dict[str, Any]:
    """M0/RAW control: return captured text without analysis or calls."""
    return {"output": text, "operational_failure": False, "calls": [], "edits": [], "wall_seconds": 0.0}


def direct(
    text: str,
    client_or_completion: Any,
    directory: str | Path | None = None,
    translation: bool = False,
    *,
    model: str = MODEL,
) -> dict[str, Any]:
    """M1/direct method; a supplied completion is supported for offline replay."""
    if isinstance(client_or_completion, str) and directory is None:
        return {"output": client_or_completion, "operational_failure": False, "model_calls": 0, "method": "direct"}
    if directory is None:
        raise TypeError("direct requires a capture directory")
    started = time.monotonic()
    call = client_or_completion.call(Path(directory) / "call", text_body(text, translation, model=model), "translation" if translation else "direct")
    output = text if call.get("operational_failure") else call.get("text", text)
    return {
        "output": output,
        "operational_failure": bool(call.get("operational_failure")),
        "calls": [call],
        "edits": [],
        "wall_seconds": time.monotonic() - started,
        "failure": call.get("failure"),
        "translation_valid": not call.get("operational_failure") if translation else None,
    }


def _proposal(value: Mapping[str, Any]) -> Proposal:
    return Proposal(bool(value["keep"]), value.get("replacement"), bool(value["needs_wider_edit"]))


def _saved_decisions(record: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """Return caller-owned first-stage decisions without sampling them again."""
    for name in ("first_stage", "first_stage_decisions", "frozen_decisions", "decisions"):
        value = record.get(name)
        if isinstance(value, list) and all(isinstance(item, Mapping) for item in value):
            return value
    raise ValueError("saved-first-stage retry requires frozen first-stage decisions")


def _saved_candidate(original: str, decision: Mapping[str, Any]) -> dict[str, Any]:
    raw = decision.get("candidate", decision.get("span"))
    if not isinstance(raw, Mapping):
        raise ValueError("saved first-stage decision lacks a candidate")
    candidate = dict(raw)
    start, end = candidate.get("start"), candidate.get("end")
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(original):
        raise ValueError("saved candidate coordinates are invalid")
    if candidate.get("text", original[start:end]) != original[start:end]:
        raise ValueError("saved candidate text differs from original coordinates")
    candidate["text"] = original[start:end]
    return candidate


def _saved_first_proposal(decision: Mapping[str, Any]) -> Proposal | None:
    for name in ("first_proposal_raw", "first_proposal", "proposal", "first"):
        value = decision.get(name)
        if isinstance(value, Mapping) and "proposal" in value and "keep" not in value:
            value = value["proposal"]
        if value is not None:
            if not isinstance(value, Mapping):
                raise ValueError("saved first-stage proposal is not an object")
            return _proposal(value)
    return None


def saved_first_stage_retry(
    text: str,
    pipeline: Any,
    client: Any,
    directory: str | Path,
    frozen_decisions: list[Mapping[str, Any]],
    *,
    retry_builder: Callable[[str, Mapping[str, Any], Proposal, Mapping[str, Any]], dict[str, Any]],
    retry_kind: str,
    retry_limit: int = 1,
    model: str = MODEL,
) -> dict[str, Any]:
    """Replay a frozen first stage and call only its authorized correction.

    The first-stage reviewer is deliberately absent from this function.  A
    saved decision is either reused as-is or, when its saved gate is
    unigram-uncertain, receives at most the one historical corrective call.
    """
    if retry_limit not in (0, 1):
        raise ValueError("saved-first-stage retry permits at most one corrective call")
    if not isinstance(frozen_decisions, list) or not all(isinstance(item, Mapping) for item in frozen_decisions):
        raise ValueError("saved-first-stage retry requires a list of frozen decisions")
    started_calls = int(getattr(client, "network_calls", 0))
    edits: list[tuple[int, int, str]] = []
    first_edits: list[tuple[int, int, str]] = []
    decisions: list[dict[str, Any]] = []
    any_failed = False
    first_failed = False
    for index, frozen in enumerate(frozen_decisions):
        candidate = _saved_candidate(text, frozen)
        first_observation = frozen.get("first")
        if isinstance(first_observation, Mapping) and first_observation.get("operational_failure"):
            first_failed = any_failed = True
            decisions.append({"candidate": candidate, "first": dict(first_observation), "retry": None, "first_gate": None, "final_gate": None})
            continue
        first = _saved_first_proposal(frozen)
        if first is None:
            raise ValueError("saved first-stage decision lacks a proposal")
        saved_gate = frozen.get("first_gate", frozen.get("gate"))
        if isinstance(saved_gate, Mapping):
            first_gate = dict(saved_gate)
        else:
            first_gate = pipeline.gate(text, candidate, first)[2]
        final_proposal: Proposal | None = first
        final_gate: dict[str, Any] | None = first_gate
        if first_gate.get("accepted") and isinstance(first.replacement, str):
            first_edits.append((candidate["start"], candidate["end"], first.replacement))
        retry_observation = None
        if first_gate.get("reason") == "replacement-unigram-uncertain" and retry_limit:
            retry_observation = client.call(
                Path(directory) / "targets" / f"{candidate['start']:08d}" / "retry-00",
                retry_builder(text, candidate, first, first_gate),
                retry_kind,
            )
            if retry_observation.get("operational_failure"):
                any_failed = True
                final_proposal = None
                final_gate = None
            else:
                value = retry_observation.get("proposal")
                if not isinstance(value, Mapping):
                    raise ValueError("saved-first-stage corrective response lacks a proposal")
                final_proposal = _proposal(value)
                final_gate = pipeline.gate(text, candidate, final_proposal)[2]
        if final_gate and final_gate.get("accepted") and final_proposal is not None and isinstance(final_proposal.replacement, str):
            edits.append((candidate["start"], candidate["end"], final_proposal.replacement))
        decisions.append({
            "candidate": candidate,
            "first_proposal": first.__dict__,
            "first_gate": first_gate,
            "first": frozen.get("first"),
            "retry": retry_observation,
            "final_proposal": final_proposal.__dict__ if final_proposal is not None else None,
            "final_gate": final_gate,
            "saved_first_stage": True,
            "target_index": index,
        })
    public_edits = [] if any_failed else edits
    new_calls = int(getattr(client, "network_calls", 0)) - started_calls
    return {
        "original": text,
        "output": patch(text, public_edits),
        "no_retry_output": patch(text, [] if first_failed else first_edits),
        "operational_failure": any_failed,
        "no_retry_operational_failure": first_failed,
        "calls": [item["retry"] for item in decisions if item.get("retry") is not None],
        "edits": public_edits,
        "no_retry_edits": [] if first_failed else first_edits,
        "decisions": decisions,
        "first_stage_calls_reused": len(frozen_decisions),
        "first_stage_calls_executed": 0,
        "retry_calls": new_calls,
        "new_corrective_calls": new_calls,
        "network_calls": new_calls,
        "model_calls": new_calls,
        "detector": {"candidates": [item["candidate"] for item in decisions], "maximum": None},
    }


def targeted(
    text: str,
    pipeline: Any,
    client: Any,
    directory: str | Path,
    *,
    retry_limit: int = 1,
    model: str = MODEL,
    retry_builder: Callable[[str, Mapping[str, Any], Proposal, Mapping[str, Any]], dict[str, Any]] | None = None,
    retry_kind: str = "expression-retry",
) -> dict[str, Any]:
    """M2 actual detector/policy/reviewer/gate/retry/patch path."""
    if retry_limit < 0:
        raise ValueError("retry limit must be non-negative")
    started = time.monotonic()
    directory = Path(directory)
    prepared = pipeline.detect(text)
    _save(directory / "detector.json", prepared)
    decisions: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []
    edits: list[tuple[int, int, str]] = []
    first_edits: list[tuple[int, int, str]] = []
    first_failed = False
    any_failed = False
    for index, (candidate, policy) in enumerate(zip(prepared["candidates"], prepared["english"], strict=True)):
        target_dir = directory / "targets" / f"{index:02d}"
        if policy["review_suppressed"]:
            decision = {"candidate": candidate, "english": policy, "policy_preserved": True,
                        "first": None, "retry": None, "first_gate": None, "final_gate": None}
            decisions.append(decision)
            _save(target_dir / "decision.json", decision)
            continue
        first = client.call(target_dir / "first", first_body(text, candidate, model=model), "reviewer")
        calls.append(first)
        retry = None
        initial_gate = None
        final_gate = None
        adjusted = None
        final_proposal = None
        case = None
        final_case = None
        if first.get("operational_failure"):
            first_failed = True
            any_failed = True
        else:
            raw = _proposal(first["proposal"])
            adjusted, case, initial_gate = pipeline.gate(text, candidate, raw)
            final_gate = initial_gate
            final_proposal = adjusted
            final_case = case
            if initial_gate["accepted"]:
                first_edits.append((candidate["start"], candidate["end"], adjusted["replacement"]))
        retries: list[dict[str, Any]] = []
        if initial_gate and initial_gate["reason"] == "replacement-unigram-uncertain":
            for retry_index in range(retry_limit):
                retry_body_value = (
                    retry_builder(text, candidate, raw, initial_gate)
                    if retry_builder is not None
                    else retry_body(raw.replacement or "", model=model)
                )
                retry = client.call(
                    target_dir / f"retry-{retry_index:02d}",
                    retry_body_value,
                    retry_kind,
                )
                retries.append(retry)
                calls.append(retry)
                if retry.get("operational_failure"):
                    any_failed = True
                    final_gate = None
                    final_proposal = None
                    break
                retry_raw = _proposal(retry["proposal"])
                final_proposal, final_case, final_gate = pipeline.gate(text, candidate, retry_raw)
                if final_gate["accepted"] or final_gate["reason"] != "replacement-unigram-uncertain":
                    break
            retry = retries[-1] if retries else None
        if final_gate and final_gate["accepted"]:
            edits.append((candidate["start"], candidate["end"], final_proposal["replacement"]))
        decision = {"candidate": candidate, "english": policy, "policy_preserved": False,
                    "first": first, "retry": retry, "retries": retries, "first_adjusted": adjusted,
                    "first_case": case, "first_gate": initial_gate, "final_gate": final_gate,
                    "final_proposal": final_proposal, "final_case": final_case}
        decisions.append(decision)
        _save(target_dir / "decision.json", decision)
    applied = [] if any_failed else edits
    first_applied = [] if first_failed else first_edits
    return {
        "output": patch(text, applied),
        "no_retry_output": patch(text, first_applied),
        "operational_failure": any_failed,
        "no_retry_operational_failure": first_failed,
        "calls": calls,
        "edits": applied,
        "no_retry_edits": first_applied,
        "candidate_edits_before_failure_fallback": edits,
        "first_edits_before_failure_fallback": first_edits,
        "detector": prepared,
        "decisions": decisions,
        "wall_seconds": time.monotonic() - started,
    }


def no_retry(text: str, full: Mapping[str, Any]) -> dict[str, Any]:
    """M3 ablation derived from the first-stage M2 records, with zero calls."""
    first_calls = [call for call in full["calls"] if call.get("kind") == "reviewer"]
    first_edits = []
    for decision in full["decisions"]:
        gate = decision.get("first_gate")
        if gate and gate.get("accepted"):
            candidate = decision["candidate"]
            first_edits.append((candidate["start"], candidate["end"], decision["first_adjusted"]["replacement"]))
    failed = any(call.get("operational_failure") for call in first_calls)
    output = patch(text, [] if failed else first_edits)
    if output != full["no_retry_output"] or failed != full["no_retry_operational_failure"]:
        raise AssertionError("M3 differs from preserved first-stage result")
    return {"output": output, "operational_failure": failed, "calls": first_calls,
            "edits": [] if failed else first_edits, "detector": full["detector"],
            "decisions": full["decisions"], "derived_from_M2": True,
            "new_model_calls": 0, "wall_seconds": None,
            "incremental_retry_seconds_excluded": sum(call.get("http_seconds") or 0 for call in full["calls"] if call.get("kind") == "expression-retry")}
