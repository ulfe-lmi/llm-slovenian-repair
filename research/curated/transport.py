"""Frozen transport shapes and completion parser; no client or network side effect."""

from __future__ import annotations

from typing import Any

from .review import reviewer_body

MODEL = "qwen3.8-27b"


def text_body(text: str, *, translation: bool = False, model: str = MODEL) -> dict[str, Any]:
    prompt = (
        "Translate the following text into natural Slovenian.\n"
        "Preserve meaning and formatting.\n"
        "Return only the Slovenian translation.\n\n{source}"
        if translation
        else "Correct Slovenian spelling and grammatical errors conservatively.\n"
        "Preserve the original meaning, register, formatting and content.\n"
        "Do not rewrite text that is already correct.\n"
        "Return only the corrected text.\n\n{source}"
    )
    return {
        "model": model,
        "stream": False,
        "store": False,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt.format(source=text)}]}],
        "include_reasoning": True,
        "reasoning": {"effort": "low"},
    }


def parse_text(response: dict[str, Any]) -> str:
    output = response.get("output", [])
    texts = [
        part["text"]
        for item in output
        if isinstance(item, dict) and item.get("type") == "message" and item.get("role") == "assistant"
        for part in item.get("content", [])
        if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str)
    ]
    if len(texts) != 1:
        raise ValueError("expected exactly one assistant text field")
    return texts[0]


def targeted_body(sentence: str, target: str, *, model: str = MODEL) -> dict[str, Any]:
    return reviewer_body(sentence, target, model=model)
