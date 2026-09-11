"""Frozen contextual-review and expression-retry request/response boundaries.

The functions are deliberately transport-free. Historical experiments supplied
the injected response; this module validates that response exactly and never
performs a network call.
"""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass
from typing import Any


class ReviewerError(ValueError):
    """A response cannot be used as a frozen local proposal."""


@dataclass(frozen=True)
class Proposal:
    keep: bool
    replacement: str | None
    needs_wider_edit: bool


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReviewerError("duplicate review schema key")
        result[key] = value
    return result


TARGETED_PROMPT = (
    "You are a narrow Slovenian expression reviewer. Preserve meaning and register. "
    "Review only the marked target; do not rewrite the sentence. "
    'Return exactly {{"keep":boolean,"replacement":string|null,"needs_wider_edit":boolean}}. '
    "Sentence: {sentence}\nTarget: {target} Answer only the required JSON object."
)

EXPRESSION_RETRY_PROMPT = """Ta slovenski izraz je napačno zapisan ali oblikovan:

{expression}

Predlagaj najverjetnejšo pravilno slovensko obliko istega izraza.
Odgovor lahko vsebuje od 1 do 4 besede.
Vrni samo popravljeni izraz."""


def _assistant_texts(response: object) -> list[str]:
    if not isinstance(response, dict) or not isinstance(response.get("output"), list):
        raise ReviewerError("missing output")
    texts: list[str] = []
    for item in response["output"]:
        if not isinstance(item, dict) or item.get("type") != "message" or item.get("role") != "assistant":
            continue
        content = item.get("content")
        if not isinstance(content, list):
            raise ReviewerError("assistant content is not a list")
        for part in content:
            if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str):
                texts.append(part["text"])
    return texts


def parse_proposal(response: object) -> Proposal:
    """Parse the actual three-field JSON proposal; reject the whole response."""
    texts = _assistant_texts(response)
    if len(texts) != 1 or len(texts[0]) > 2000:
        raise ReviewerError("expected one bounded assistant output_text")
    try:
        value = json.loads(texts[0].strip(), object_pairs_hook=_unique_pairs)
    except json.JSONDecodeError as exc:
        raise ReviewerError("review output is not JSON") from exc
    if not isinstance(value, dict) or set(value) != {"keep", "replacement", "needs_wider_edit"}:
        raise ReviewerError("review schema keys are not exact")
    keep, replacement, wider = value["keep"], value["replacement"], value["needs_wider_edit"]
    if type(keep) is not bool or type(wider) is not bool:
        raise ReviewerError("review booleans are not exact")
    if replacement is not None and not isinstance(replacement, str):
        raise ReviewerError("replacement type is invalid")
    if (keep and replacement is not None) or (wider and (not keep or replacement is not None)):
        raise ReviewerError("contradictory review proposal")
    if not keep and (replacement is None or not replacement.strip()):
        raise ReviewerError("empty replacement")
    return Proposal(keep, replacement, wider)


def reviewer_prompt(sentence: str, target: str) -> str:
    return TARGETED_PROMPT.format(sentence=sentence, target=target)


def reviewer_body(sentence: str, target: str, *, model: str = "qwen3.8-27b") -> dict[str, Any]:
    return {
        "model": model,
        "stream": False,
        "store": False,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": reviewer_prompt(sentence, target)}]}],
        "include_reasoning": True,
        "reasoning": {"effort": "low"},
    }


def expression_retry_body(expression: str, *, model: str = "qwen3.8-27b") -> dict[str, Any]:
    if not isinstance(expression, str) or not 1 <= len(expression.split()) <= 4 or len(expression) > 80:
        raise ReviewerError("rejected expression must contain 1–4 words within 80 code points")
    return {
        "model": model,
        "stream": False,
        "store": False,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": EXPRESSION_RETRY_PROMPT.format(expression=expression)}]}],
        "include_reasoning": True,
        "reasoning": {"effort": "low"},
    }


def parse_expression(response: object) -> Proposal:
    texts = _assistant_texts(response)
    if len(texts) != 1:
        raise ReviewerError("expected exactly one corrected expression")
    expression = texts[0].strip(" \t\r\n")
    words = expression.split()
    if not 1 <= len(words) <= 4 or len(expression) > 80:
        raise ReviewerError("corrected expression exceeds the frozen bound")
    if any(unicodedata.category(char).startswith("C") for char in expression):
        raise ReviewerError("control or format character in corrected expression")
    if not all(char.isalpha() or unicodedata.category(char).startswith("M") or char in " -'’" for char in expression):
        raise ReviewerError("unsupported character in corrected expression")
    for word in words:
        if not word[0].isalpha() or not (word[-1].isalpha() or unicodedata.category(word[-1]).startswith("M")):
            raise ReviewerError("corrected expression must contain plain words")
    return Proposal(False, expression, False)
