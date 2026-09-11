"""Curated method boundaries used by the recorded campaign variants."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from .corpus import Corpus
from .pipeline import replay
from .review import Proposal


def identity(text: str) -> dict[str, Any]:
    """M0/RAW control: return the captured text without analysis or calls."""
    return {"output": text, "operational_failure": False, "model_calls": 0, "method": "identity"}


def direct(text: str, captured_completion: str | None, *, translation: bool = False) -> dict[str, Any]:
    """M1/direct method: consume a supplied completion, never issue a call here."""
    if captured_completion is None:
        return {
            "output": text,
            "operational_failure": True,
            "failure": "missing-captured-completion",
            "model_calls": 0,
            "method": "direct-translation" if translation else "direct",
        }
    return {
        "output": captured_completion,
        "operational_failure": False,
        "model_calls": 0,
        "method": "direct-translation" if translation else "direct",
    }


def targeted(
    text: str,
    index: str,
    english_lookup: Callable[[str], float],
    proposals: Mapping[str, Proposal | Mapping[str, Any] | str],
    retry_proposals: Mapping[str, Proposal | Mapping[str, Any] | str] | None = None,
    *,
    maximum: int | None = None,
) -> dict[str, Any]:
    """M2 targeted path using actual detector, policy, gate, and patch functions."""
    with Corpus(index) as corpus:
        result = replay(
            text,
            corpus,
            english_lookup,
            proposals,
            retry_proposals,
            maximum=maximum,
        )
    result["method"] = "targeted"
    return result


def no_retry(full: Mapping[str, Any]) -> dict[str, Any]:
    """M3 ablation derived from M2 first-stage accepted edits, with zero calls."""
    output = full["no_retry_output"]
    return {
        "output": output,
        "operational_failure": bool(full.get("no_retry_operational_failure", False)),
        "model_calls": 0,
        "network_calls": 0,
        "method": "no-retry",
        "derived_from_M2": True,
        "edits": full["no_retry_edits"],
    }
