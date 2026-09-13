"""Exact original-coordinate validation and patching from the experiments."""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata

from .protected import Interval, is_protected, protected_intervals
from .review import Proposal


@dataclass(frozen=True)
class Edit:
    start: int
    end: int
    before: str
    replacement: str


def mechanical(original: str, candidate: dict[str, object], proposal: Proposal) -> dict[str, object]:
    """Reproduce the frozen mechanical gate before the unigram gate."""
    start, end = candidate.get("start"), candidate.get("end")
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(original):
        return {"applied": False, "reason": "invalid-span"}
    target = candidate.get("text")
    if not isinstance(target, str) or original[start:end] != target:
        return {"applied": False, "reason": "stale-span"}
    if is_protected(start, end, protected_intervals(original)):
        return {"applied": False, "reason": "protected-span"}
    if proposal.needs_wider_edit:
        return {"applied": False, "reason": "WIDER"}
    if proposal.keep:
        return {"applied": False, "reason": "KEEP"}
    replacement = proposal.replacement
    if not replacement or replacement == target:
        return {"applied": False, "reason": "empty-or-identity"}
    words = replacement.split(" ")
    if replacement != replacement.strip() or not 1 <= len(words) <= 4 or len(replacement) > 80:
        return {"applied": False, "reason": "replacement-bound"}
    if any(unicodedata.category(char).startswith("C") for char in replacement):
        return {"applied": False, "reason": "control-or-format-character"}
    for word in words:
        if not word or not word[0].isalpha() or not (
            word[-1].isalpha() or unicodedata.category(word[-1]).startswith("M")
        ):
            return {"applied": False, "reason": "structural-replacement"}
        if not all(
            char.isalpha() or unicodedata.category(char).startswith("M") or char in "-'’"
            for char in word
        ) or re.search(r"[-'’]{2}", word):
            return {"applied": False, "reason": "structural-replacement"}
    return {"applied": True, "reason": "mechanically-valid", "replacement": replacement}


def restore_initial_case(original_target: str, proposal: Proposal) -> tuple[Proposal, dict[str, object]]:
    """Apply the historical one-character case rule, preserving other letters."""
    adjusted = proposal.replacement
    upper = len(original_target) >= 2 and original_target[0].isupper() and original_target[1].islower()
    lower = bool(original_target) and original_target[0].islower()
    direction = "upper" if upper else "lower" if lower else None
    if direction and not proposal.keep and not proposal.needs_wider_edit and adjusted:
        initial = adjusted[0].upper() if direction == "upper" else adjusted[0].lower()
        adjusted = initial + adjusted[1:]
    return Proposal(proposal.keep, adjusted, proposal.needs_wider_edit), {
        "eligible_original": direction is not None,
        "direction": direction,
        "changed": adjusted != proposal.replacement,
        "raw_replacement": proposal.replacement,
        "adjusted_replacement": adjusted,
    }


def apply_edits(
    original: str, edits: list[Edit | tuple[int, int, str]], intervals: list[Interval] | None = None
) -> str:
    """Apply non-overlapping edits and assert protected slices are unchanged."""
    intervals = protected_intervals(original) if intervals is None else intervals
    normalized = [
        edit
        if isinstance(edit, Edit)
        else Edit(edit[0], edit[1], original[edit[0] : edit[1]], edit[2])
        for edit in edits
    ]
    ordered = sorted(normalized, key=lambda edit: (edit.start, edit.end))
    last_end = 0
    for edit in ordered:
        if not 0 <= edit.start < edit.end <= len(original):
            raise ValueError("edit span is outside original coordinates")
        if edit.start < last_end:
            raise ValueError("overlapping edits are rejected")
        if original[edit.start : edit.end] != edit.before:
            raise ValueError("stale original slice")
        if is_protected(edit.start, edit.end, intervals):
            raise ValueError("edit intersects protected content")
        last_end = edit.end
    result = original
    for edit in reversed(ordered):
        result = result[: edit.start] + edit.replacement + result[edit.end :]
    for interval in intervals:
        if interval.end > len(original):
            continue
        before = original[interval.start : interval.end]
        shift = sum(
            len(edit.replacement) - (edit.end - edit.start)
            for edit in ordered
            if edit.end <= interval.start
        )
        after_start = interval.start + shift
        if result[after_start : after_start + len(before)] != before:
            raise AssertionError("protected slice changed")
    return result
