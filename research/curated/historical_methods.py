"""Historical M0/M1/M2/M3 methods with durable failure accounting."""

from __future__ import annotations

import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .corpus import Corpus
from .historical_pipeline import first_body, patch, retry_body
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
) -> dict[str, Any]:
    """M1/direct method; a supplied completion is supported for offline replay."""
    if isinstance(client_or_completion, str) and directory is None:
        return {"output": client_or_completion, "operational_failure": False, "model_calls": 0, "method": "direct"}
    if directory is None:
        raise TypeError("direct requires a capture directory")
    started = time.monotonic()
    call = client_or_completion.call(Path(directory) / "call", text_body(text, translation), "translation" if translation else "direct")
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


def targeted(text: str, pipeline: Any, client: Any, directory: str | Path) -> dict[str, Any]:
    """M2 actual detector/policy/reviewer/gate/retry/patch path."""
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
        first = client.call(target_dir / "first", first_body(text, candidate), "reviewer")
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
            if initial_gate["reason"] == "replacement-unigram-uncertain":
                retry = client.call(target_dir / "retry", retry_body(raw.replacement or ""), "expression-retry")
                calls.append(retry)
                if retry.get("operational_failure"):
                    any_failed = True
                    final_gate = None
                    final_proposal = None
                else:
                    retry_raw = _proposal(retry["proposal"])
                    final_proposal, final_case, final_gate = pipeline.gate(text, candidate, retry_raw)
            if final_gate and final_gate["accepted"]:
                edits.append((candidate["start"], candidate["end"], final_proposal["replacement"]))
        decision = {"candidate": candidate, "english": policy, "policy_preserved": False,
                    "first": first, "retry": retry, "first_adjusted": adjusted,
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
