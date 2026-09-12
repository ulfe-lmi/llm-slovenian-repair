"""Offline, deliberately experimental one-code-point substitution seam.

This module has no network, model, corpus acquisition, or frequency-ranking
boundary.  It operates on caller-supplied detector candidates and a verified
in-memory exact-unigram vocabulary so that the 007-h driver can replay saved
fallback decisions without resampling them.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from .curated.patching import apply_edits, mechanical, restore_initial_case
from .curated.review import Proposal


def _is_word_shaped(value: str) -> bool:
    """Reject whitespace and multiword forms before character comparison."""
    return bool(value) and not any(character.isspace() for character in value)


def qualifying_candidates(lookup_form: str, bucket: Iterable[str]) -> list[str]:
    """Return the complete set of exact-length, one-alphabetic-substitution forms.

    ``lookup_form`` must already be the target's ``casefold`` view.  No Unicode
    normalization, ordering, frequency, context, or language preference is
    applied.  A caller must treat a result of length greater than one as
    ambiguous rather than selecting one member.
    """
    if not _is_word_shaped(lookup_form):
        return []
    result: list[str] = []
    for candidate in bucket:
        if not isinstance(candidate, str) or not _is_word_shaped(candidate):
            continue
        if len(candidate) != len(lookup_form):
            continue
        differences = [
            position
            for position, (left, right) in enumerate(zip(lookup_form, candidate, strict=True))
            if left != right
        ]
        if len(differences) != 1:
            continue
        position = differences[0]
        if not lookup_form[position].isalpha() or not candidate[position].isalpha():
            continue
        result.append(candidate)
    return result


def exact_single_unigram(replacement: str, vocabulary: set[str]) -> bool:
    """Confirm the final casefolded replacement is one exact vocabulary form."""
    return _is_word_shaped(replacement) and replacement.casefold() in vocabulary


def entering_targets(detector: Mapping[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Apply English suppression before admitting exact-unigram absences."""
    candidates = detector.get("candidates")
    english = detector.get("english")
    if not isinstance(candidates, list) or not isinstance(english, list):
        raise ValueError("detector snapshot lacks candidate and English arrays")
    if len(candidates) != len(english):
        raise ValueError("detector candidate and English arrays are misaligned")
    result: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for candidate, policy in zip(candidates, english, strict=True):
        if not isinstance(candidate, dict) or not isinstance(policy, dict):
            raise ValueError("detector candidate or English policy is not an object")
        if policy.get("review_suppressed"):
            continue
        evidence = candidate.get("evidence")
        unigram = evidence.get("unigram") if isinstance(evidence, dict) else None
        policy_unigram = policy.get("slovene_unigram")
        if not isinstance(unigram, dict) or not isinstance(policy_unigram, dict):
            raise ValueError("detector candidate lacks unigram evidence")
        if unigram.get("state") != policy_unigram.get("state"):
            raise ValueError("candidate and English unigram states differ")
        if unigram.get("state") == "UNAVAILABLE":
            result.append((candidate, policy))
    return result


def mechanical_substitution(
    original: str,
    candidate: Mapping[str, Any],
    replacement: str,
    vocabulary: set[str],
) -> dict[str, Any]:
    """Run case restoration, the existing mechanical gate, and exact membership."""
    proposal = Proposal(False, replacement, False)
    target = candidate.get("text")
    if not isinstance(target, str):
        return {"accepted": False, "reason": "invalid-target"}
    adjusted, case = restore_initial_case(target, proposal)
    mechanics = mechanical(original, dict(candidate), adjusted)
    if not mechanics["applied"]:
        return {
            "accepted": False,
            "reason": str(mechanics["reason"]),
            "case": case,
            "mechanical": mechanics,
        }
    final_replacement = adjusted.replacement
    assert isinstance(final_replacement, str)
    exact = exact_single_unigram(final_replacement, vocabulary)
    return {
        "accepted": exact,
        "reason": "accepted" if exact else "replacement-unigram-uncertain",
        "case": case,
        "mechanical": mechanics,
        "unigram": {
            "state": "EXACT" if exact else "UNAVAILABLE",
            "key": final_replacement.casefold(),
        },
        "edit": [candidate["start"], candidate["end"], final_replacement] if exact else None,
    }


def candidate_key(candidate: Mapping[str, Any]) -> tuple[int, int, str]:
    """Return the original-coordinate identity used by saved decisions."""
    start, end, text = candidate.get("start"), candidate.get("end"), candidate.get("text")
    if type(start) is not int or type(end) is not int or not isinstance(text, str):
        raise ValueError("candidate lacks an original-coordinate identity")
    return start, end, text


def _call(value: object) -> bool:
    return isinstance(value, dict)


def saved_accepted_edits(record: Mapping[str, Any]) -> list[list[Any]]:
    """Extract the exact accepted saved decisions before document fallback."""
    edits: list[list[Any]] = []
    decisions = record.get("decisions")
    if not isinstance(decisions, list):
        raise ValueError("saved record lacks decisions")
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ValueError("saved decision is not an object")
        gate = decision.get("final_gate")
        candidate = decision.get("candidate")
        final_case = decision.get("final_case")
        if not isinstance(gate, dict) or not gate.get("accepted"):
            continue
        if not isinstance(candidate, dict) or not isinstance(final_case, dict):
            raise ValueError("accepted saved decision lacks final coordinates")
        start, end, replacement = (
            candidate.get("start"),
            candidate.get("end"),
            final_case.get("adjusted_replacement"),
        )
        if type(start) is not int or type(end) is not int or not isinstance(replacement, str):
            raise ValueError("accepted saved decision has an invalid edit")
        edits.append([start, end, replacement])
    return edits


def _overlaps(left: Sequence[Any], right: Sequence[Any]) -> bool:
    return int(left[0]) < int(right[1]) and int(right[0]) < int(left[1])


def project_saved_case(
    original: str,
    saved: Mapping[str, Any],
    mechanical_edits: Sequence[Sequence[Any]],
) -> dict[str, Any]:
    """Compose mechanical edits with the saved fallback and project call counts.

    Saved first/retry call objects are data.  This function never invokes a
    transport.  A mechanical target removes both its first and retry call, but
    an unresolved operational failure still rolls the entire result back to
    the original text.  If all failing calls were avoided, the successful saved
    edits may be retained alongside the mechanical edits.
    """
    decisions = saved.get("decisions")
    calls = saved.get("calls")
    if not isinstance(decisions, list) or not isinstance(calls, list):
        raise ValueError("saved record lacks decisions or calls")
    mechanical_keys = {
        (int(edit[0]), int(edit[1]), original[int(edit[0]) : int(edit[1])])
        for edit in mechanical_edits
    }
    if len(mechanical_keys) != len(mechanical_edits):
        raise ValueError("duplicate mechanical edit identity")
    decision_keys = {
        candidate_key(decision.get("candidate"))
        for decision in decisions
        if isinstance(decision, dict) and isinstance(decision.get("candidate"), dict)
    }
    if not mechanical_keys <= decision_keys:
        raise ValueError("mechanical edit lacks a saved fallback decision")
    unresolved_decisions: list[dict[str, Any]] = []
    unresolved_calls: list[dict[str, Any]] = []
    unresolved_failure = False
    avoided_first = 0
    avoided_retry = 0
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ValueError("saved decision is not an object")
        candidate = decision.get("candidate")
        if not isinstance(candidate, dict):
            raise ValueError("saved decision lacks candidate")
        key = candidate_key(candidate)
        mechanical_target = key in mechanical_keys
        first = decision.get("first")
        retry = decision.get("retry")
        if mechanical_target:
            avoided_first += int(_call(first))
            avoided_retry += int(_call(retry))
            continue
        unresolved_decisions.append(decision)
        for call in (first, retry):
            if _call(call):
                assert isinstance(call, dict)
                unresolved_calls.append(call)
                unresolved_failure = unresolved_failure or bool(call.get("operational_failure"))

    accepted = saved_accepted_edits(saved)
    fallback_edits = [
        edit
        for edit in accepted
        if not any(_overlaps(edit, mechanical_edit) for mechanical_edit in mechanical_edits)
    ]
    if unresolved_failure:
        output = original
        applied_edits: list[list[Any]] = []
        new_failure = True
    else:
        applied_edits = [*fallback_edits, *[list(edit) for edit in mechanical_edits]]
        output = apply_edits(original, [tuple(edit) for edit in applied_edits])
        new_failure = False
    baseline_failure = bool(saved.get("operational_failure"))
    baseline_failures = sum(
        bool(call.get("operational_failure")) for call in calls if isinstance(call, dict)
    )
    if baseline_failure != bool(baseline_failures):
        raise ValueError("saved operational-failure flag does not match saved calls")
    return {
        "output": output,
        "edits": applied_edits,
        "operational_failure": new_failure,
        "decisions": unresolved_decisions,
        "calls": unresolved_calls,
        "avoided_first_calls": avoided_first,
        "avoided_retry_calls": avoided_retry,
        "avoided_total_calls": avoided_first + avoided_retry,
        "unresolved_operational_failure": unresolved_failure,
        "baseline_failure": baseline_failure,
    }
