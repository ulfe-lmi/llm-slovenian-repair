"""Offline replay of the actual detector → policy → review → gate → patch path."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any

from .corpus import Corpus
from .detector import detect, tokenize
from .english_preserve import classify
from .gating import check
from .patching import apply_edits, restore_initial_case
from .protected import protected_intervals
from .review import Proposal, parse_expression, parse_proposal


def _proposal(value: Proposal | Mapping[str, Any] | str, *, retry: bool = False) -> Proposal:
    if isinstance(value, Proposal):
        return value
    if isinstance(value, str):
        value = json.loads(value)
    if isinstance(value, Mapping) and set(value) == {"keep", "replacement", "needs_wider_edit"}:
        return Proposal(bool(value["keep"]), value["replacement"], bool(value["needs_wider_edit"]))
    if retry:
        return parse_expression(value)
    return parse_proposal(value)


def prepare(
    original: str,
    corpus: Corpus,
    english_lookup: Callable[[str], float],
    *,
    mode: str = "local-context",
    threshold: int = 3,
    maximum: int | None = None,
) -> dict[str, Any]:
    """Run the real frozen detector and English eligibility policy."""
    intervals = protected_intervals(original)
    candidates = detect(
        original, corpus, intervals, mode=mode, threshold=threshold, maximum=maximum
    )
    candidate_rows = [candidate.as_dict() for candidate in candidates]
    english = [classify(candidate, english_lookup) for candidate in candidate_rows]
    return {
        "candidates": candidate_rows,
        "english": english,
        "eligible_words": len(tokenize(original, intervals)),
        "protected_intervals": [interval.__dict__ for interval in intervals],
        "detector_mode": mode,
        "threshold": threshold,
        "maximum": maximum,
    }


def replay(
    original: str,
    corpus: Corpus,
    english_lookup: Callable[[str], float],
    proposals: Mapping[str, Proposal | Mapping[str, Any] | str],
    retry_proposals: Mapping[str, Proposal | Mapping[str, Any] | str] | None = None,
    *,
    mode: str = "local-context",
    threshold: int = 3,
    maximum: int | None = None,
    retry_failures: Mapping[str, Mapping[str, Any] | str] | None = None,
) -> dict[str, Any]:
    """Replay saved proposal values with zero model/network calls.

    Keys are ``<start>`` offsets, matching the historical target records. A
    missing proposal is an error rather than an implicit KEEP, so omissions in
    a saved trace cannot be normalized into a successful replay.
    """
    prepared = prepare(
        original,
        corpus,
        english_lookup,
        mode=mode,
        threshold=threshold,
        maximum=maximum,
    )
    retry_proposals = retry_proposals or {}
    retry_failures = retry_failures or {}
    edits: list[tuple[int, int, str]] = []
    decisions: list[dict[str, Any]] = []
    no_retry_edits: list[tuple[int, int, str]] = []
    corrective_failure = False
    for candidate, policy in zip(prepared["candidates"], prepared["english"], strict=True):
        key = str(candidate["start"])
        if policy["review_suppressed"]:
            decisions.append({"key": key, "english": policy, "first_gate": None, "final_gate": None, "retry_used": False})
            continue
        if key not in proposals:
            raise ValueError(f"saved first proposal missing for offset {key}")
        first_raw = _proposal(proposals[key])
        first, first_case = restore_initial_case(candidate["text"], first_raw)
        first_gate = check(original, candidate, first, _lookup(corpus))
        final, final_case, final_gate = first, first_case, first_gate
        retry_used = False
        if first_gate["accepted"]:
            assert isinstance(first.replacement, str)
            no_retry_edits.append((candidate["start"], candidate["end"], first.replacement))
        if first_gate["reason"] == "replacement-unigram-uncertain":
            if key in retry_failures:
                corrective_failure = True
                decisions.append(
                    {
                        "key": key,
                        "candidate": candidate,
                        "english": policy,
                        "first_proposal": first,
                        "first_case": first_case,
                        "first_gate": first_gate,
                        "final_proposal": None,
                        "final_case": None,
                        "final_gate": None,
                        "retry_used": True,
                        "retry_failure": retry_failures[key],
                    }
                )
                continue
            if key not in retry_proposals:
                raise ValueError(f"saved retry proposal missing for offset {key}")
            retry_used = True
            raw_retry = _proposal(retry_proposals[key], retry=True)
            final, final_case = restore_initial_case(candidate["text"], raw_retry)
            final_gate = check(original, candidate, final, _lookup(corpus))
        if final_gate["accepted"]:
            assert isinstance(final.replacement, str)
            edits.append((candidate["start"], candidate["end"], final.replacement))
        decisions.append(
            {
                "key": key,
                "candidate": candidate,
                "english": policy,
                "first_proposal": first,
                "first_case": first_case,
                "first_gate": first_gate,
                "final_proposal": final,
                "final_case": final_case,
                "final_gate": final_gate,
                "retry_used": retry_used,
            }
        )
    output = apply_edits(original, edits)
    no_retry_output = apply_edits(original, no_retry_edits)
    if corrective_failure:
        output = original
        # Candidate edits are diagnostic evidence only after a corrective
        # transport failure.  The public failure contract is fail-closed;
        # callers can inspect the separate pre-failure field if needed.
        public_edits: list[tuple[int, int, str]] = []
    else:
        public_edits = edits
    return {
        "original": original,
        "output": output,
        "no_retry_output": no_retry_output,
        "detector": prepared,
        "decisions": decisions,
        "edits": public_edits,
        "no_retry_edits": no_retry_edits,
        "review_calls": sum(not policy["review_suppressed"] for policy in prepared["english"]),
        "retry_calls": sum(decision["retry_used"] for decision in decisions),
        "operational_failure": corrective_failure,
        "no_retry_operational_failure": False,
        "candidate_edits_before_failure_fallback": edits,
        "first_edits_before_failure_fallback": no_retry_edits,
        "network_calls": 0,
        "model_calls": 0,
    }


def _lookup(corpus: Corpus) -> Callable[[str], dict[str, object]]:
    def lookup(word: str) -> dict[str, object]:
        evidence = corpus.unigram(word)
        return {"key": evidence.key, "state": evidence.state, "count": evidence.count}

    return lookup
