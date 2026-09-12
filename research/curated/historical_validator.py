"""Validator-only replay of the low-plus-validator experiment."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .historical_common import save
from .patching import apply_edits, mechanical
from .review import Proposal
from .validation import validator_body


def _proposal(value: Any) -> Proposal:
    if isinstance(value, Proposal):
        return value
    if isinstance(value, Mapping):
        if not {"keep", "replacement", "needs_wider_edit"}.issubset(value):
            raise ValueError("frozen first-stage proposal is incomplete")
        return Proposal(bool(value["keep"]), value.get("replacement"), bool(value["needs_wider_edit"]))
    raise ValueError("validator requires a caller-supplied frozen first-stage proposal")


def _first_stage(record: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    for name in ("first_stage", "first_stage_decisions", "decisions", "frozen_decisions"):
        value = record.get(name)
        if isinstance(value, list) and all(isinstance(item, Mapping) for item in value):
            return value
    raise ValueError("validator input must contain frozen first-stage decisions")


def _original(record: Mapping[str, Any]) -> str:
    for name in ("original", "input", "text"):
        value = record.get(name)
        if isinstance(value, str):
            return value
    raise ValueError("validator input lacks the original sentence")


def _candidate(original: str, decision: Mapping[str, Any]) -> dict[str, Any]:
    raw = decision.get("candidate", decision.get("span"))
    if not isinstance(raw, Mapping):
        raise ValueError("frozen validator decision lacks candidate coordinates")
    value = dict(raw)
    if "text" not in value and isinstance(value.get("start"), int) and isinstance(value.get("end"), int):
        value["text"] = original[value["start"] : value["end"]]
    return value


def _saved_proposal(decision: Mapping[str, Any]) -> Any:
    for name in ("first_proposal", "first_proposal_raw", "proposal", "first"):
        value = decision.get(name)
        if isinstance(value, Mapping) and "proposal" in value and "keep" not in value:
            value = value["proposal"]
        if value is not None:
            return value
    raise ValueError("frozen validator decision lacks first-stage proposal")


def run_validator_records(
    records: list[dict[str, Any]],
    client: Any,
    output_root: str | Path,
    *,
    model: str,
) -> dict[str, Any]:
    """Run only bounded validator calls over caller-owned frozen proposals."""

    root = Path(output_root)
    completed = 0
    validator_calls = 0
    for number, record in enumerate(records, 1):
        original = _original(record)
        edits: list[tuple[int, int, str]] = []
        decisions: list[dict[str, Any]] = []
        calls: list[dict[str, Any]] = []
        for candidate_number, frozen in enumerate(_first_stage(record)):
            candidate = _candidate(original, frozen)
            proposal = _proposal(_saved_proposal(frozen))
            gate = mechanical(original, candidate, proposal)
            if not gate["applied"]:
                decisions.append({"candidate": candidate, "first_proposal": proposal.__dict__, "mechanical_gate": gate, "validator": None})
                continue
            body = validator_body(
                {"original": original},
                {"candidate": candidate, "proposal": proposal.__dict__},
                model=model,
            )
            call = client.call(
                root / "records" / str(record.get("id", number)) / "targets" / f"{candidate_number:02d}" / "validator",
                body,
                "validator",
            )
            validator_calls += 1
            calls.append(call)
            accepted = call.get("validation") == "ACCEPT" and not call.get("operational_failure")
            if accepted:
                replacement = proposal.replacement
                assert isinstance(replacement, str)
                edits.append((int(candidate["start"]), int(candidate["end"]), replacement))
            decisions.append({
                "candidate": candidate,
                "first_proposal": proposal.__dict__,
                "mechanical_gate": gate,
                "validator": call,
                "applied": accepted,
            })
        corrected = apply_edits(original, edits)
        save(
            root / "records" / (str(record.get("id", number)) + ".json"),
            {
                "id": record.get("id", str(number)),
                "variant": "low-plus-validator",
                "original": original,
                "output": corrected,
                "corrected": corrected,
                "decisions": decisions,
                "calls": calls,
                "first_stage_calls_reused": True,
                "first_stage_calls_executed": 0,
                "validator_calls": len(calls),
                "model_calls": client.network_calls,
            },
        )
        completed += 1
    return {
        "executed": True,
        "records": completed,
        "workers": 1,
        "first_stage_calls_reused": True,
        "first_stage_calls_executed": 0,
        "validator_calls": validator_calls,
        "model_calls": client.network_calls,
        "network_calls": client.network_calls,
        "output_root": "caller-supplied",
    }
