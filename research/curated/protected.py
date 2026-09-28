"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Protection.

008-c rework (parser-first structural protection, structural policy v2):

- Markdown-syntax rules (fenced code, inline code, Markdown links) are no
  longer regex rules: they are parser-derived intervals from the pinned
  pulldown-cmark 0.13.4 structural helper (frozen 008-c interface
  decision), with the narrow residual semantic layer running only on
  parser-approved candidate-prose spans. All of this lives in
  ``research.curated.prose_boundary`` (single implementation source).
- The 008-a full-regex rule set is retained in
  ``research.curated.prose_boundary`` (the ``LEGACY_*`` rules and
  ``legacy_protected_intervals``, clearly marked) and is used ONLY as the
  documented fail-closed fallback when the pinned helper is unavailable or
  untrustworthy (identity mismatch, non-zero exit, timeout, malformed or
  truncated protocol, coordinate-contract violation). The protection layer
  never fails open.
- Public surface for all consumers (pipeline, detector, historical
  detector, patching, contextual validator): ``Interval``,
  ``is_protected``, ``protected_intervals`` — unchanged signatures,
  code-point coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass

from .prose_boundary import (
    ProtectionResult,
    legacy_protected_intervals,
    protection_with_status,
)


@dataclass(frozen=True, order=True)
class Interval:
    start: int
    end: int
    reason: str


def protection_result(
    text: str, tool_arguments: tuple[str, ...] = ()
) -> ProtectionResult:
    """Protection with mode/fallback diagnostics (parser-first or the
    fail-closed legacy fallback; never unprotected)."""
    return protection_with_status(text, tuple(tool_arguments))


def protected_intervals(
    text: str, tool_arguments: tuple[str, ...] = ()
) -> list[Interval]:
    """Protected intervals (code-point coordinates, merged) for ``text``.

    Parser-first per frozen structural policy v2 when the pinned helper is
    available and trustworthy; otherwise the retained 008-a full-regex
    rule set (byte-identical output), with the fallback reason recorded in
    :func:`protection_result`.
    """
    result = protection_with_status(text, tuple(tool_arguments))
    return [Interval(start, end, reason) for start, end, reason in result.intervals]


def is_protected(start: int, end: int, intervals: list[Interval]) -> bool:
    return any(start < item.end and end > item.start for item in intervals)
