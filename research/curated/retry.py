"""Actual retry variants: contextual expression versus later word-only retry."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .gating import check
from .historical_transport import CONTEXTUAL_RETRY_PROMPT, word_retry_body
from .patching import apply_edits
from .review import Proposal, parse_proposal

WORD_ONLY_INSTRUCTION = """Ta beseda je napačno zapisana: {word}

Predlagaj pravilno slovensko obliko. Vrni samo popravljeno besedo."""


def contextual_retry_body(record: dict[str, Any] | str, decision: dict[str, Any] | None = None, *, model: str = "qwen3.8-27b") -> dict[str, Any]:
    """Build the original low-unigram retry body with sentence/target metadata."""
    if isinstance(record, str):
        data = {"rejected_replacement": record}
    else:
        if decision is None:
            raise ValueError("contextual retry requires the saved decision")
        candidate = decision["candidate"]
        gate = decision.get("first_gate", {})
        proposal = decision["proposal"]
        if isinstance(proposal, Proposal):
            replacement = proposal.replacement
        elif isinstance(proposal, Mapping):
            replacement = proposal.get("replacement")
        else:
            raise ValueError("contextual retry proposal must be a saved mapping or Proposal")
        if not isinstance(replacement, str):
            raise ValueError("contextual retry requires the rejected replacement")
        data = {"original_sentence": record["original"], "target": candidate["text"], "target_start": candidate["start"], "target_end": candidate["end"],
                "rejected_replacement": replacement,
                "replacement_words_not_found": [word["key"] for word in gate.get("unigram", {}).get("words", []) if word.get("state") != "EXACT"]}
    import json
    return {"model": model, "stream": False, "store": False,
            "input": [{"role": "user", "content": [{"type": "input_text", "text": CONTEXTUAL_RETRY_PROMPT + json.dumps(data, ensure_ascii=False)}]}],
            "include_reasoning": True, "reasoning": {"effort": "low"}}


def word_only_retry_body(raw_word: str, *, model: str = "qwen3.8-27b") -> dict[str, Any]:
    return word_retry_body(raw_word, model=model)


def proposal_replacement(value: Proposal | Mapping[str, Any]) -> str:
    """Read a raw saved proposal without assuming a dataclass instance."""
    replacement = value.replacement if isinstance(value, Proposal) else value.get("replacement")
    if not isinstance(replacement, str):
        raise ValueError("retry requires a nonempty rejected replacement")
    return replacement


def parse_contextual(response: object) -> Proposal:
    return parse_proposal(response)


def parse_word_only(response: object) -> Proposal:
    from .historical_transport import _parse_word

    return _parse_word(response)


def retry_policy(kind: str, maximum: int) -> dict[str, Any]:
    if kind not in {"word-only", "expression", "contextual"}:
        raise ValueError("unknown retry policy")
    if maximum < 0:
        raise ValueError("retry limit must be non-negative")
    return {"kind": kind, "maximum": maximum, "network_calls": 0, "model_calls": 0,
            "prompt": "word-only" if kind == "word-only" else "contextual-expression"}


def select_retry(first_gate: str, *, kind: str, maximum: int) -> bool:
    retry_policy(kind, maximum)
    return first_gate == "replacement-unigram-uncertain" and maximum > 0


def outcome(record: dict[str, Any], first_gates: dict[str, dict[str, Any]], retries: dict[str, Proposal | dict[str, Any]], lookup: Any) -> dict[str, Any]:
    """Copied word-only outcome program: no context is sent on retry."""
    edits, decisions, without_retry = [], [], []
    for decision in record["decisions"]:
        candidate = decision["candidate"]
        key = f"{record['case']['id']}-{candidate['start']}"
        initial = first_gates[key]
        raw_first = decision["proposal"]
        proposal = raw_first if isinstance(raw_first, Proposal) else Proposal(bool(raw_first["keep"]), raw_first.get("replacement"), bool(raw_first["needs_wider_edit"]))
        final, source = initial, "first-pass"
        if initial["accepted"]:
            without_retry.append((candidate["start"], candidate["end"], proposal.replacement))
        if initial["reason"] == "replacement-unigram-uncertain":
            if key not in retries:
                raise ValueError("missing required single retry")
            retry = retries[key]
            proposal = retry if isinstance(retry, Proposal) else Proposal(bool(retry["keep"]), retry.get("replacement"), bool(retry["needs_wider_edit"]))
            source = "corrective-retry"
            final = check(record["original"], candidate, proposal, lookup)
        if final["accepted"]:
            edits.append((candidate["start"], candidate["end"], proposal.replacement))
        decisions.append({"key": key, "candidate": candidate, "first_proposal": decision["proposal"], "first_gate": initial,
                          "final_proposal": proposal.__dict__, "final_gate": final, "source": source})
    corrected = apply_edits(record["original"], edits)
    case = record["case"]
    gold = record["original"][: case["start"]] + str(case["gold"]) + record["original"][case["end"]:] if case["known_error"] else record["original"]
    return {"case": case, "original": record["original"], "first_pass_corrected": record.get("corrected"),
            "unigram_without_retry_corrected": apply_edits(record["original"], without_retry), "corrected": corrected,
            "edits": edits, "decisions": decisions, "changed": corrected != record["original"], "exact_gold_output": corrected == gold,
            "protected_differences": 0, "outside_edit_differences": 0}
