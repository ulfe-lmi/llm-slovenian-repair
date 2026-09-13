"""Actual low-plus-validator second-pass prompt, response protocol and replay."""

from __future__ import annotations

import json
from typing import Any

from .patching import apply_edits
from .review import Proposal, ReviewerError

VALIDATOR_INSTRUCTION = """You are validating one proposed local correction in Slovenian.
The original may already be correct, and the proposed correction may itself be wrong.
ARE YOU REALLY SURE the proposed correction improves the Slovenian in this exact sentence?
Check the replacement's spelling, word formation, grammatical agreement, natural usage, and meaning in the complete sentence. Preserve meaning and register. Do not treat an unfamiliar technical term or a mentioned expression as automatically wrong.
ACCEPT only if the proposed replacement is correct, natural, and a clear local improvement, without requiring changes outside the selected target.
REJECT if the proposed replacement is wrong, changes the intended meaning, or unnecessarily changes an already acceptable original.
Choose UNCERTAIN if you cannot establish a clear local improvement or a wider edit is required.
Do not propose another replacement, rewrite the sentence, or provide reasoning.
Return exactly one JSON object: {"decision":"ACCEPT"} or {"decision":"REJECT"} or {"decision":"UNCERTAIN"}.
Evaluate the following data:
"""


def validator_body(record: dict[str, Any], decision: dict[str, Any], *, model: str = "qwen3.8-27b") -> dict[str, Any]:
    candidate, proposal = decision["candidate"], decision["proposal"]
    data = {"original_sentence": record["original"], "target": candidate["text"], "target_start": candidate["start"], "target_end": candidate["end"],
            "proposed_replacement": proposal["replacement"], "resulting_sentence": apply_edits(record["original"], [(candidate["start"], candidate["end"], proposal["replacement"])])}
    return {"model": model, "stream": False, "store": False,
            "input": [{"role": "user", "content": [{"type": "input_text", "text": VALIDATOR_INSTRUCTION + json.dumps(data, ensure_ascii=False)}]}],
            "include_reasoning": True, "reasoning": {"effort": "low"}}


def parse_validator(response: object) -> str:
    if not isinstance(response, dict) or not isinstance(response.get("output"), list):
        raise ReviewerError("missing validator output")
    texts = [part["text"] for item in response["output"] if isinstance(item, dict) and item.get("type") == "message" and item.get("role") == "assistant"
             for part in item.get("content", []) if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str)]
    if len(texts) != 1 or len(texts[0]) > 2000:
        raise ReviewerError("expected one bounded validator reply")
    def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ReviewerError("duplicate validator schema key")
            value[key] = item
        return value
    try:
        value = json.loads(texts[0], object_pairs_hook=unique_pairs)
    except json.JSONDecodeError as exc:
        raise ReviewerError("invalid validator JSON") from exc
    if not isinstance(value, dict) or set(value) != {"decision"} or value["decision"] not in ("ACCEPT", "REJECT", "UNCERTAIN"):
        raise ReviewerError("invalid validator schema")
    return value["decision"]


def validate_saved_proposal(proposal: dict[str, Any]) -> bool:
    """Compatibility helper for the exact proposal shape, without deciding truth."""
    required = {"keep", "replacement", "needs_wider_edit"}
    if set(proposal) != required or type(proposal["keep"]) is not bool or type(proposal["needs_wider_edit"]) is not bool:
        return False
    if proposal["keep"] or proposal["needs_wider_edit"]:
        return proposal["replacement"] is None
    return isinstance(proposal["replacement"], str) and bool(proposal["replacement"])
