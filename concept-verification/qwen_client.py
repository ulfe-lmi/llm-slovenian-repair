"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Reviewer."""

from __future__ import annotations

import http.client
import json
import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


class ReviewerError(ValueError):
    pass


@dataclass(frozen=True)
class Proposal:
    keep: bool
    replacement: str | None
    needs_wider_edit: bool


def parse_proposal(response: object) -> Proposal:
    if not isinstance(response, dict):
        raise ReviewerError("response must be an object")
    output = response.get("output")
    if not isinstance(output, list):
        raise ReviewerError("missing output")
    texts: list[str] = []
    for item in output:
        if (
            not isinstance(item, dict)
            or item.get("type") != "message"
            or item.get("role") != "assistant"
        ):
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if (
                isinstance(part, dict)
                and part.get("type") == "output_text"
                and isinstance(part.get("text"), str)
            ):
                texts.append(part["text"])
    if len(texts) != 1 or len(texts[0]) > 2000:
        raise ReviewerError("expected one bounded assistant output_text")
    raw = texts[0].strip()
    if raw.startswith("```") or raw.endswith("```"):
        raise ReviewerError("code-fence prose is rejected")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReviewerError("review output is not JSON") from exc
    if not isinstance(value, dict) or set(value) != {"keep", "replacement", "needs_wider_edit"}:
        raise ReviewerError("review schema keys are not exact")
    if type(value["keep"]) is not bool or type(value["needs_wider_edit"]) is not bool:
        raise ReviewerError("review booleans are not exact")
    replacement = value["replacement"]
    if replacement is not None and not isinstance(replacement, str):
        raise ReviewerError("replacement type is invalid")
    if value["keep"] and replacement is not None:
        raise ReviewerError("keep cannot carry a replacement")
    if value["needs_wider_edit"] and (not value["keep"] or replacement is not None):
        raise ReviewerError("wider edit is contradictory")
    return Proposal(value["keep"], replacement, value["needs_wider_edit"])


def prompt(sentence: str, target: str, variant: str = "frozen-v1") -> str:
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


class ResponsesReviewer:
    def __init__(
        self, base_url: str, model: str, timeout: float = 15.0, api_key: str | None = None
    ):
        parsed = urlparse(base_url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("reviewer base URL must be an explicit HTTP URL")
        self.scheme, self.host = parsed.scheme, parsed.hostname
        self.port = parsed.port
        self.base_path = parsed.path.rstrip("/")
        self.model, self.timeout = model, timeout
        self.api_key = api_key if api_key is not None else os.environ.get("QWEN_API_KEY")
        profile = os.environ.get("CONCEPT_REVIEWER_PROFILE")
        if self.api_key is None and profile:
            profile_path = Path(profile)
            if profile_path.is_symlink() or not profile_path.is_file():
                raise ReviewerError("reviewer profile is not a regular file")
            with profile_path.open("rb") as handle:
                profile_data = tomllib.load(handle)
            provider = profile_data.get("model_providers", {}).get(
                profile_data.get("model_provider", ""), {}
            )
            value = provider.get("experimental_bearer_token")
            if isinstance(value, str) and value:
                self.api_key = value

    def review(self, sentence: str, target: str, variant: str = "frozen-v1") -> Proposal:
        body = json.dumps(
            {
                "model": self.model,
                "stream": False,
                "store": False,
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt(sentence, target, variant)}
                        ],
                    }
                ],
            },
            ensure_ascii=False,
        ).encode()
        connection_class = (
            http.client.HTTPSConnection if self.scheme == "https" else http.client.HTTPConnection
        )
        connection = connection_class(self.host, self.port, timeout=self.timeout)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        try:
            connection.request("POST", f"{self.base_path}/responses", body=body, headers=headers)
            result = connection.getresponse()
            payload = result.read(2_000_001)
        except (OSError, TimeoutError) as exc:
            raise ReviewerError("review HTTP request failed") from exc
        finally:
            connection.close()
        if result.status != 200 or len(payload) > 2_000_000:
            raise ReviewerError("review HTTP response was not successful")
        try:
            return parse_proposal(json.loads(payload.decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReviewerError("review response is not valid JSON") from exc
