"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Repair."""

from __future__ import annotations

import re
from dataclasses import dataclass

from detector import Candidate
from pandoc_protection import grapheme_boundary_sensitive, grapheme_sensitive
from protected import Interval, is_protected
from qwen_client import Proposal

from corpus import Corpus


@dataclass(frozen=True)
class Acceptance:
    accepted: bool
    reason: str
    replacement: str | None


def accept(
    text: str,
    candidate: Candidate,
    proposal: Proposal,
    corpus: Corpus,
    intervals: list[Interval],
    *,
    left: str | None = None,
    right: str | None = None,
    left_bounds: tuple[int, int] | None = None,
    right_bounds: tuple[int, int] | None = None,
) -> Acceptance:
    # Stale-coordinate validation (order 013-a, requirement 14): the
    # candidate and its neighbor tokens must still match the exact
    # original slices before any acceptance decision.
    # Bounds are validated before any slicing so negative or oversized
    # coordinates cannot match by Python slice semantics.
    if not 0 <= candidate.start < candidate.end <= len(text):
        return Acceptance(False, "stale-candidate-bounds", None)
    if text[candidate.start : candidate.end] != candidate.text:
        return Acceptance(False, "stale-candidate-bounds", None)
    if (
        left is not None
        and left_bounds is not None
    ):
        if not 0 <= left_bounds[0] < left_bounds[1] <= len(text):
            return Acceptance(False, "stale-neighbor-bounds", None)
        # Neighbor tokens arrive as tokenizer keys (casefolded); compare
        # the original slice under the same convention.
        if text[left_bounds[0] : left_bounds[1]].casefold() != left:
            return Acceptance(False, "stale-neighbor-bounds", None)
    if (
        right is not None
        and right_bounds is not None
    ):
        if not 0 <= right_bounds[0] < right_bounds[1] <= len(text):
            return Acceptance(False, "stale-neighbor-bounds", None)
        if text[right_bounds[0] : right_bounds[1]].casefold() != right:
            return Acceptance(False, "stale-neighbor-bounds", None)
    if is_protected(candidate.start, candidate.end, intervals):
        return Acceptance(False, "protected", None)
    # Context barrier at acceptance: protected content strictly between a
    # neighbor token and the candidate invalidates the adjacency evidence.
    if left_bounds is not None and any(
        left_bounds[1] <= item.start and item.end <= candidate.start for item in intervals
    ):
        return Acceptance(False, "barrier-between-neighbor", None)
    if right_bounds is not None and any(
        candidate.end <= item.start and item.end <= right_bounds[0] for item in intervals
    ):
        return Acceptance(False, "barrier-between-neighbor", None)
    if proposal.keep:
        return Acceptance(False, "reviewer-kept", None)
    replacement = proposal.replacement
    if proposal.needs_wider_edit or not replacement or replacement == candidate.text:
        return Acceptance(False, "wider-or-identity", None)
    if "\n" in replacement or "\r" in replacement or any(ord(char) < 32 for char in replacement):
        return Acceptance(False, "control-or-newline", None)
    # The replacement must be grapheme-stable throughout: a combining mark
    # or joiner anywhere in it (e.g. a mid-word NFD sequence) is unproved.
    if any(grapheme_sensitive(char) for char in replacement):
        return Acceptance(False, "grapheme-sensitive-replacement", None)
    if re.search(r"[`<>\[\]{}]", replacement):
        return Acceptance(False, "markup", None)
    words = replacement.casefold().split()
    if not 1 <= len(words) <= 4 or sum(len(word) for word in words) > 80:
        return Acceptance(False, "replacement-size", None)
    if any(corpus.unigram(word).state != "EXACT" for word in words):
        return Acceptance(False, "replacement-unigram-uncertain", None)
    local_exact = 0
    if left:
        local_exact += corpus.ngram(f"{left} {words[0]}", 2).state == "EXACT"
    if right:
        local_exact += corpus.ngram(f"{words[-1]} {right}", 2).state == "EXACT"
    if left and right:
        local_exact += corpus.ngram(f"{left} {words[0]} {right}", 3).state == "EXACT"
    if local_exact < 1:
        return Acceptance(False, "local-evidence-not-stronger", None)
    return Acceptance(True, "accepted-independent-evidence", replacement)


def apply_edits(text: str, edits: list[tuple[int, int, str]], intervals: list[Interval]) -> str:
    ordered = sorted(edits, key=lambda item: (item[0], item[1]))
    for index, (start, end, _replacement) in enumerate(ordered):
        if not 0 <= start < end <= len(text) or (index and start < ordered[index - 1][1]):
            raise ValueError("overlapping or invalid edit")
        if is_protected(start, end, intervals):
            raise ValueError("edit intersects protected content")
        # An edit must not split a grapheme-sensitive sequence: a
        # grapheme-sensitive character immediately outside the edit whose
        # partner lies inside the edit would be separated.
        if (start > 0 and grapheme_boundary_sensitive(text[start - 1])) or (
            end < len(text) and grapheme_boundary_sensitive(text[end])
        ):
            raise ValueError("edit splits grapheme-sensitive sequence")
    result = text
    for start, end, replacement in reversed(ordered):
        result = result[:start] + replacement + result[end:]
    for interval in intervals:
        if interval.end <= len(text):
            before = text[interval.start : interval.end]
            start_shift = sum(
                len(repl) - (end - start) for start, end, repl in ordered if end <= interval.start
            )
            after_start = interval.start + start_shift
            if result[after_start : after_start + len(before)] != before:
                raise AssertionError("protected slice changed")
    return result
