"""The preserved one-target retry-limit-ten driver."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .historical_common import safe_component, save
from .historical_pipeline import first_body, retry_body
from .patching import apply_edits


def sequence(
    text: str,
    candidate: dict[str, Any],
    pipeline: Any,
    client: Any,
    directory: str | Path,
    *,
    max_retries: int = 10,
    model: str = "qwen3.8-27b",
) -> tuple[list[dict[str, Any]], str, list[tuple[int, int, str]]]:
    if not 0 <= max_retries <= 10:
        raise ValueError("historical retry10 limit must be between 0 and 10")
    root = Path(directory)
    steps: list[dict[str, Any]] = []

    first = client.call(root / "first", first_body(text, candidate, model=model), "reviewer")

    def add_step(number: int, call: dict[str, Any]) -> dict[str, Any]:
        item: dict[str, Any] = {
            "stage": "first-contextual" if number == 0 else "context-free-retry",
            "attempt": number,
            "call": call,
        }
        if not call.get("operational_failure"):
            adjusted, case, gate = pipeline.gate(text, candidate, call["proposal"])
            item.update(adjusted=adjusted, case=case, gate=gate)
        steps.append(item)
        save(root / f"step-{number:02d}.json", item)
        return item

    current = add_step(0, first)
    if first.get("operational_failure"):
        return steps, "OPERATIONAL_FAILURE", []
    anchor = first["proposal"].get("replacement")
    if not isinstance(anchor, str):
        return steps, current["gate"]["reason"], []
    for attempt in range(1, max_retries + 1):
        gate = current["gate"]
        if gate["accepted"]:
            return steps, "ACCEPTED", [(candidate["start"], candidate["end"], current["adjusted"]["replacement"])]
        if gate["reason"] != "replacement-unigram-uncertain":
            return steps, str(gate["reason"]), []
        call = client.call(root / f"retry-{attempt:02d}", retry_body(anchor, model=model), "expression-retry")
        current = add_step(attempt, call)
        if call.get("operational_failure"):
            return steps, "OPERATIONAL_FAILURE", []
    if current.get("gate", {}).get("accepted"):
        return steps, "ACCEPTED", [(candidate["start"], candidate["end"], current["adjusted"]["replacement"])]
    return steps, "RETRY_LIMIT_REACHED", []


def run_record(
    record: dict[str, Any],
    pipeline: Any,
    client: Any,
    output_root: str | Path,
    *,
    max_retries: int = 10,
    model: str = "qwen3.8-27b",
) -> dict[str, Any]:
    record_id = safe_component(record.get("id", "case"))
    original = record.get("input", record.get("original"))
    if not isinstance(original, str):
        raise ValueError("retry10 record lacks input")
    prepared = pipeline.detect(original)
    candidates = prepared.get("candidates")
    policies = prepared.get("english")
    if not isinstance(candidates, list) or not isinstance(policies, list) or len(candidates) != len(policies):
        raise ValueError("retry10 requires the latest pipeline's English policy")
    candidate = record.get("candidate")
    if not isinstance(candidate, dict):
        if len(candidates) != 1:
            raise ValueError("retry10 requires one caller-selected target")
        candidate = candidates[0]
    else:
        matches = [item for item in candidates if item.get("start") == candidate.get("start") and item.get("end") == candidate.get("end") and item.get("text") == candidate.get("text")]
        if len(matches) != 1:
            raise ValueError("retry10 candidate is not one detected caller-selected target")
        candidate = matches[0]
    policy = next(
        (
            policy_value
            for candidate_value, policy_value in zip(candidates, policies, strict=True)
            if candidate_value == candidate
        ),
        None,
    )
    if not isinstance(policy, dict):
        raise ValueError("retry10 English policy does not match the selected target")
    record_root = Path(output_root) / "records" / record_id
    if policy.get("review_suppressed"):
        result = {
            "id": record_id,
            "variant": "prijigrala-retry10",
            "status": "ENGLISH_ATTESTED_PRESERVED",
            "input": original,
            "output": original,
            "steps": [],
            "applied_edits": [],
            "model_calls": client.network_calls,
            "corrective_calls": 0,
            "fixed_retry_anchor": True,
            "english_policy": policy,
        }
        save(Path(output_root) / "records" / (record_id + ".json"), result)
        return result
    steps, status, edits = sequence(original, candidate, pipeline, client, record_root, max_retries=max_retries, model=model)
    output = apply_edits(original, edits)
    result = {
        "id": record_id,
        "variant": "prijigrala-retry10",
        "status": status,
        "input": original,
        "output": output,
        "steps": steps,
        "applied_edits": edits,
        "model_calls": client.network_calls,
        "corrective_calls": max(0, len(steps) - 1),
        "fixed_retry_anchor": True,
        "english_policy": policy,
    }
    save(Path(output_root) / "records" / (record_id + ".json"), result)
    return result
