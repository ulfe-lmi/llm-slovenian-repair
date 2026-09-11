"""Portable copy of the historical detector/gate/retry/patch bridge."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from .corpus import Corpus
from .english_preserve import classify
from .gating import UnigramIndex, check
from .historical_detector import detect, tokenize
from .historical_transport import expression_retry_body
from .patching import apply_edits, restore_initial_case
from .review import Proposal

MODEL = "qwen3.8-27b"


def reviewer_prompt(sentence: str, target: str, variant: str = "frozen-v1") -> str:
    if variant not in ("frozen-v1", "dev-v2"):
        raise ValueError("unknown prompt variant")
    suffix = (
        " Answer only the required JSON object."
        if variant == "frozen-v1"
        else " Be conservative and answer only as JSON."
    )
    return (
        "You are a narrow Slovenian expression reviewer. Preserve meaning and register. "
        "Review only the marked target; do not rewrite the sentence. "
        'Return exactly {"keep":boolean,"replacement":string|null,"needs_wider_edit":boolean}. '
        f"Sentence: {sentence}\nTarget: {target}{suffix}"
    )


def first_body(text: str, candidate: Mapping[str, Any], *, model: str = MODEL, reasoning_effort: str = "low") -> dict[str, Any]:
    return {
        "model": model,
        "stream": False,
        "store": False,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": reviewer_prompt(text, str(candidate["text"]))}]}],
        "include_reasoning": True,
        "reasoning": {"effort": reasoning_effort},
    }


class Pipeline:
    """The historical bridge: detector -> English policy -> case -> gate -> patch."""

    def __init__(
        self,
        index: str | Path,
        *,
        english_lookup: Callable[[str], float],
        maximum: int | None = None,
        threshold: int = 3,
    ):
        self.maximum = maximum
        self.threshold = threshold
        self.corpus = Corpus(index)
        self.unigrams = UnigramIndex(index)
        self.english_lookup = english_lookup

    def detect(self, text: str) -> dict[str, Any]:
        intervals = __import__("research.curated.protected", fromlist=["protected_intervals"]).protected_intervals(text)
        candidates = [candidate.as_dict() for candidate in detect(text, self.corpus, intervals, mode="local-context", threshold=self.threshold, maximum=self.maximum)]
        policies = [classify(candidate, self.english_lookup) for candidate in candidates]
        return {
            "candidates": candidates,
            "english": policies,
            "eligible_words": len(tokenize(text, intervals)),
            "protected_intervals": [interval.__dict__ for interval in intervals],
            "detector_mode": "local-context",
            "threshold": self.threshold,
            "maximum": self.maximum,
        }

    def gate(self, text: str, candidate: Mapping[str, Any], proposal: Proposal | Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        if not isinstance(proposal, Proposal):
            proposal = Proposal(bool(proposal["keep"]), proposal.get("replacement"), bool(proposal["needs_wider_edit"]))
        adjusted, case = restore_initial_case(str(candidate["text"]), proposal)
        return adjusted.__dict__, case, check(text, dict(candidate), adjusted, self.unigrams.lookup)

    def close(self) -> None:
        self.corpus.close()
        self.unigrams.close()

    def __enter__(self) -> "Pipeline":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def retry_body(raw: str, *, model: str = MODEL) -> dict[str, Any]:
    return expression_retry_body(raw, model=model)


def parse_first(value: object) -> Proposal:
    from .review import parse_proposal

    return parse_proposal(value)


def parse_retry(value: object) -> Proposal:
    from .review import parse_expression

    return parse_expression(value)


def patch(text: str, edits: list[tuple[int, int, str]]) -> str:
    return apply_edits(text, edits)
