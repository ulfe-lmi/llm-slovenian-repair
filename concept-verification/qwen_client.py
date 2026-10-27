"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Reviewer."""

from __future__ import annotations

import http.client
import json
import math
import os
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from batch_review import (
    REASON_HTTP_FAILED,
    REASON_HTTP_NOT_OK,
    REASON_INVALID_ENCODING,
    REASON_PROMPT_OVERSIZE,
    REASON_REQUEST_OVERSIZE,
    BatchError,
    BatchResult,
    BatchTarget,
    build_prompt,
    build_request_body,
    parse_batch_envelope,
    strict_json_object,
)
from config import (
    REVIEW_BATCH_MAX_REQUEST_BYTES,
    REVIEW_BATCH_MAX_RESPONSE_BYTES,
    REVIEWER_HTTP_TIMEOUT_SECONDS,
)
from review_transport import ReviewTransportError, run_review_exchange

# Exact repository-local versioned worker for the owned transport
# child (order 019-a, requirement 2); executed by the running
# interpreter, never resolved by search or shell.
_REVIEW_WORKER_PATH = Path(__file__).resolve().parent / "review_worker.py"


class ReviewerError(ValueError):
    """Reviewer failure; ``reason`` is a fixed label or None for legacy use."""

    def __init__(self, message: str, reason: str | None = None) -> None:
        super().__init__(message)
        self.reason = reason


@dataclass(frozen=True)
class Proposal:
    keep: bool
    replacement: str | None
    needs_wider_edit: bool


def responses_path(path: str) -> str:
    """Return the one Responses endpoint path used by this experiment."""
    base = path.rstrip("/")
    if not base.endswith("/v1"):
        base += "/v1"
    return base + "/responses"


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
        self,
        base_url: str,
        model: str,
        timeout: float = REVIEWER_HTTP_TIMEOUT_SECONDS,
        api_key: str | None = None,
        profile: str | Path | None = None,
    ):
        parsed = urlparse(base_url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("reviewer base URL must be an explicit HTTP URL")
        # Finite positive whole-exchange budget (order 019-a,
        # requirement 1): validated at constructor entry; the value
        # anchors one monotonic deadline at review_batch entry and is
        # independent of CONCEPT_TIMEOUT and CONCEPT_HEADER_TIMEOUT.
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not math.isfinite(float(timeout))
            or timeout <= 0
        ):
            raise ValueError("reviewer timeout must be a finite positive duration")
        self.scheme, self.host = parsed.scheme, parsed.hostname
        self.port = parsed.port
        self.base_path = parsed.path.rstrip("/")
        self.model, self.timeout = model, float(timeout)
        self.api_key = api_key if api_key is not None else os.environ.get("QWEN_API_KEY")
        profile_name = (
            profile if profile is not None else os.environ.get("CONCEPT_REVIEWER_PROFILE")
        )
        if self.api_key is None and profile_name:
            profile_path = Path(profile_name)
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
            connection.request("POST", responses_path(self.base_path), body=body, headers=headers)
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

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> BatchResult:
        """One fresh bounded batch request; the whole batch fails as a unit.

        ``sentence`` is the completed original answer; occurrence context is
        already serialized into the targets, so it is not re-embedded.  Limit
        failures before dispatch carry the pre-dispatch labels so the caller
        can report zero requests.

        Returns the validated ``BatchResult``: id-keyed proposals plus the
        actual reviewer usage reported by the envelope, or explicit unknown
        when absent/invalid (order 015-a, requirement 7).  Main-generation
        usage is never touched here.  The deadline anchored below covers
        worker startup, IPC and the child's actual resolver/connect/
        TLS/upload/status/header/body work plus the result transfer and
        validation here; a late or racing success is a failure and there
        is no automatic retry (order 019-a, requirements 1-2).
        """
        # One finite positive monotonic deadline anchored at entry,
        # before bounded prompt preparation, worker creation and IPC
        # (order 019-a, requirement 1); byte arrival, interim 100,
        # phase transition and process startup never restart it.
        deadline = time.monotonic() + float(self.timeout)
        prompt_text = build_prompt(targets)
        if prompt_text is None:
            raise ReviewerError("review prompt exceeds bound", reason=REASON_PROMPT_OVERSIZE)
        body = build_request_body(self.model, prompt_text)
        if len(body) > REVIEW_BATCH_MAX_REQUEST_BYTES:
            raise ReviewerError("review request exceeds bound", reason=REASON_REQUEST_OVERSIZE)
        try:
            result_status, payload = run_review_exchange(
                scheme=self.scheme,
                host=self.host,
                port=self.port,
                path=responses_path(self.base_path),
                body=body,
                auth=self.api_key,
                deadline=deadline,
                worker_path=_REVIEW_WORKER_PATH,
            )
        except ReviewTransportError as exc:
            raise ReviewerError("review HTTP request failed", reason=REASON_HTTP_FAILED) from exc
        if result_status != 200 or len(payload) > REVIEW_BATCH_MAX_RESPONSE_BYTES:
            raise ReviewerError(
                "review HTTP response was not successful", reason=REASON_HTTP_NOT_OK
            )
        try:
            decoded = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ReviewerError(
                "review response is not valid UTF-8", reason=REASON_INVALID_ENCODING
            ) from exc
        try:
            envelope = strict_json_object(decoded)
        except BatchError as exc:
            raise ReviewerError("review response is not a JSON object", reason=exc.reason) from exc
        try:
            batch_result = parse_batch_envelope(
                envelope, frozenset(target.id for target in targets)
            )
        except BatchError as exc:
            raise ReviewerError(
                "review batch response is not acceptable", reason=exc.reason
            ) from exc
        # The anchored deadline is rechecked after the parent's own
        # result validation, before transferring the result: late or
        # racing parent work is a failure, not a salvage (order 019-a,
        # requirement 1).
        if time.monotonic() >= deadline:
            raise ReviewerError("review HTTP request failed", reason=REASON_HTTP_FAILED)
        return batch_result
