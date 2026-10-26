r"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Residual protection.

The runnable proxy's residual semantic policy reuses the established frozen
research residual recognizers (008-c structural policy v2 classes: url,
path, relative-path, shell, env-var, identifier, upper-identifier, number,
tex-paren, tex-bracket, tex-env, bare-json, config, xml-fragment) from
``research.curated.prose_boundary.residual_spans``.  That function is pure:
the module import performs no helper discovery and no subprocess call, and
this adapter never calls ``protection_with_status``,
``resolve_helper_path`` or ``_run_helper``.

These recognizers refine the prose spans Pandoc has already granted as
structurally safe (order 013-a, requirement 7).  They are not an alternate
structural parser and never replace the mandatory Pandoc parse.

Bounded proxy-side addition: the frozen research policy protects an
unterminated ``\(``/``\[`` opener only when the remainder looks math-like.
An opener with no closing sequence anywhere later is still unproved math,
so ``_unterminated_tex_spans`` conservatively protects from the opener to
the end of its line.  The frozen research module is not modified.
"""

from __future__ import annotations

import sys
from pathlib import Path

from protected import Interval

try:  # pragma: no cover - path bootstrap is environment dependent
    from research.curated.prose_boundary import residual_spans as _research_residual_spans
except ModuleNotFoundError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from research.curated.prose_boundary import residual_spans as _research_residual_spans


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


def residual_intervals(
    text: str, tool_arguments: tuple[str, ...] = ()
) -> list[Interval]:
    """Whole-text residual matches: established research classes, the
    bounded proxy unterminated-Tex addition, and tool arguments."""
    spans = list(_research_residual_spans(text))
    spans.extend(_unterminated_tex_spans(text))
    intervals = [Interval(start, end, cls) for cls, start, end in spans]
    for argument in tool_arguments:
        if not argument:
            continue
        start = 0
        while True:
            start = text.find(argument, start)
            if start < 0:
                break
            intervals.append(Interval(start, start + len(argument), "tool-argument"))
            start += 1
    return _merge(intervals)


def _unterminated_tex_spans(text: str) -> list[tuple[str, int, int]]:
    """Conservative proxy addition: unterminated ``\\(``/``\\[`` openers.

    For each opener with no closing sequence anywhere later in the text,
    the remainder of the opener's line is unproved (the closing delimiter
    may simply be missing), so protect from the opener to the end of the
    line.  This is the proxy's bounded extension of the frozen research
    tex-paren/tex-bracket malformed handling; it never protects past a
    line boundary and never changes the research module.
    """
    BS = chr(92)  # backslash; explicit to keep this source escape-free
    spans: list[tuple[str, int, int]] = []
    for cls, open_char, close_char in (
        ("tex-unterm-paren", "(", ")"),
        ("tex-unterm-bracket", "[", "]"),
    ):
        open_seq = BS + open_char
        close_seq = BS + close_char
        start = 0
        while True:
            pos = text.find(open_seq, start)
            if pos < 0:
                break
            start = pos + 2
            if text.find(close_seq, pos + 2) != -1:
                continue
            line_end = text.find("\n", pos)
            spans.append((cls, pos, len(text) if line_end < 0 else line_end))
    return spans
