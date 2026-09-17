"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Protection."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Interval:
    start: int
    end: int
    reason: str


_URL = re.compile(r"https?://[^\s<>]+", re.IGNORECASE)
_PATH = re.compile(r"(?<!\w)(?:\.?/|~/|[A-Za-z]:[\\/])[^\s`<>]+")
_RELATIVE_PATH = re.compile(r"(?<!\w)[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+(?!\w)")
_NUMBER = re.compile(r"(?<!\w)[+-]?(?:\d+(?:[.,]\d+)?)(?:\s?(?:%|[A-Za-z]{1,8}))?(?!\w)")
_IDENTIFIER = re.compile(
    r"(?<!\w)(?=[A-Za-z_]*\d|[A-Za-z_]*_[A-Za-z_])[A-Za-z_][A-Za-z0-9_]*(?!\w)"
)
_UPPER_IDENTIFIER = re.compile(r"(?<!\w)[A-Z][A-Z0-9_]{1,}(?!\w)")
_JSON_XML = re.compile(r"(?:\{[^\n{}]{0,2000}\}|\[[^\n\[\]]{0,2000}\]|<[/!?]?[A-Za-z][^>]*>)")
_SHELL = re.compile(
    r"(?m)^\s*(?:[$#>]\s+|(?:sudo\s+)?(?:python|python3|uv|git|curl|npm|pip|pytest|ruff|mypy)\s+)\S[^\n]*$"
)
_FENCE = re.compile(r"(?s)(?:^|\n)(```+|~~~+)[^\n]*\n.*?\n\1(?=\s|$)")
_INLINE = re.compile(r"(?<!`)`[^`\n]+`(?!`)")
_LINK = re.compile(r"!?(?:\[[^\]\n]*\]\([^\)\n]*\)|<https?://[^>]+>)")


def _add(intervals: list[Interval], match: re.Match[str], reason: str) -> None:
    intervals.append(Interval(match.start(), match.end(), reason))


def _merge(intervals: list[Interval]) -> list[Interval]:
    if not intervals:
        return []
    ordered = sorted(intervals)
    merged: list[Interval] = [ordered[0]]
    for current in ordered[1:]:
        previous = merged[-1]
        if current.start <= previous.end:
            merged[-1] = Interval(
                previous.start,
                max(previous.end, current.end),
                previous.reason + "+" + current.reason,
            )
        else:
            merged.append(current)
    return merged


def protected_intervals(text: str, tool_arguments: tuple[str, ...] = ()) -> list[Interval]:
    intervals: list[Interval] = []
    for expression, reason in (
        (_FENCE, "fenced-code"),
        (_INLINE, "inline-code"),
        (_LINK, "markdown-link"),
        (_URL, "url"),
        (_PATH, "path"),
        (_RELATIVE_PATH, "relative-path"),
        (_SHELL, "shell"),
        (_NUMBER, "number"),
        (_IDENTIFIER, "identifier"),
        (_UPPER_IDENTIFIER, "upper-identifier"),
        (_JSON_XML, "structured"),
    ):
        intervals.extend(
            Interval(match.start(), match.end(), reason) for match in expression.finditer(text)
        )
    for argument in tool_arguments:
        if not argument:
            continue
        start = 0
        while True:
            start = text.find(argument, start)
            if start < 0:
                break
            intervals.append(Interval(start, start + len(argument), "tool-argument"))
            start += len(argument)
    return _merge(intervals)


def is_protected(start: int, end: int, intervals: list[Interval]) -> bool:
    return any(start < item.end and end > item.start for item in intervals)
