"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Protection.

The runnable proxy's structural protection is mandatory Pandoc parsing
(pinned binary, explicit reader profile, validated original coordinates)
plus the established pure residual semantic policy
(``protection_residuals`` / research 008-c residual classes).

Fail closed: there is no regex-only structural fallback.  A missing
binary, a wrong version, a parse failure, a timeout, a malformed AST or an
unprovable global mapping raises ``PandocStartupError``; the caller
(``RepairEngine.repair``) must then return the exact completed original
with zero review calls (order 013-a, requirements 6 and 12).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Interval:
    start: int
    end: int
    reason: str


def protected_intervals(text: str, tool_arguments: tuple[str, ...] = ()) -> list[Interval]:
    """Protected intervals for one completed answer (code-point offsets).

    Mandatory Pandoc structural parse; conservative residual refinement of
    the granted prose.  Raises ``PandocStartupError`` (never returns a
    regex-only result) when the structural parse or mapping cannot be
    proved.
    """
    from pandoc_protection import (
        PandocStartupError,
        compose_protection,
        protect_with_pandoc,
        resolve_pandoc_spec,
    )

    spec = resolve_pandoc_spec()
    outcome = protect_with_pandoc(spec, text)
    if not outcome.ok:
        raise PandocStartupError(outcome.reason or "PANDOC_PROTECTION", outcome.detail)
    return compose_protection(text, outcome, tool_arguments)


def is_protected(start: int, end: int, intervals: list[Interval]) -> bool:
    return any(start < item.end and end > item.start for item in intervals)
