"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Repair."""

from __future__ import annotations

import re
from dataclasses import dataclass

from corpus import Corpus
from detector import Candidate
from protected import Interval, is_protected
from qwen_client import Proposal


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
) -> Acceptance:
    if is_protected(candidate.start, candidate.end, intervals):
        return Acceptance(False, "protected", None)
    if proposal.keep:
        return Acceptance(False, "reviewer-kept", None)
    replacement = proposal.replacement
    if proposal.needs_wider_edit or not replacement or replacement == candidate.text:
        return Acceptance(False, "wider-or-identity", None)
    if "\n" in replacement or "\r" in replacement or any(ord(char) < 32 for char in replacement):
        return Acceptance(False, "control-or-newline", None)
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
