"""Portable copy of the historical HTTP client and durable capture logic.

The original transport wrote the request, raw bounded response, timing, and
parsed observation before aggregation.  This port keeps that order and accepts
an injected transport for offline tests.  With no injected transport, network
execution requires ``allow_live=True`` and an explicit endpoint/credential env.
"""

from __future__ import annotations

import base64
import hashlib
import http.client
import json
import os
from pathlib import Path
import tempfile
import time
import unicodedata
import urllib.parse
from collections.abc import Callable, Mapping
from typing import Any, Protocol

from .review import Proposal, ReviewerError, parse_expression, parse_proposal

MODEL = "qwen3.8-27b"
GEC_PROMPT = """Correct Slovenian spelling and grammatical errors conservatively.
Preserve the original meaning, register, formatting and content.
Do not rewrite text that is already correct.
Return only the corrected text.

{source}"""
TRANSLATION_PROMPT = """Translate the following text into natural Slovenian.
Preserve meaning and formatting.
Return only the Slovenian translation.

{source}"""
EXPRESSION_RETRY_PROMPT = """Ta slovenski izraz je napačno zapisan ali oblikovan:

{expression}

Predlagaj najverjetnejšo pravilno slovensko obliko istega izraza.
Odgovor lahko vsebuje od 1 do 4 besede.
Vrni samo popravljeni izraz."""
WORD_RETRY_PROMPT = """Ta beseda je napačno zapisana: {word}

Predlagaj pravilno slovensko obliko. Vrni samo popravljeno besedo."""
CONTEXTUAL_RETRY_PROMPT = '''You are correcting one local expression in Slovenian after a failed proposed fix.
Your previous replacement failed the required reference-word-list check. The listed replacement words were not found in that word list.
This time, really fix the selected expression: carefully check spelling, word formation, agreement, and the meaning of the complete sentence. Give an established, natural standard Slovenian word or short equivalent, not another invented or malformed form. Do not merely approve or repeat the rejected replacement.
Change only the original selected span. Preserve the sentence's meaning and register. Do not rewrite anything outside that span. Use at most four words.
The word list is incomplete, so absence alone is not proof that the original expression is wrong. If the original is already appropriate, KEEP it instead of forcing an unnecessary substitution. If a wider edit is necessary, decline the local replacement.
Return JSON only with exactly these fields: {"keep":boolean,"replacement":string|null,"needs_wider_edit":boolean}.
For KEEP use keep=true, replacement=null, needs_wider_edit=false. For a wider edit use keep=true, replacement=null, needs_wider_edit=true. Otherwise return keep=false, a nonempty replacement, and needs_wider_edit=false.
Do not provide explanations or reasoning. Return a genuine corrected proposal, not an ACCEPT/REJECT verdict.
Original sentence, selected target, and rejected attempt:
'''


def text_body(text: str, translation: bool = False, *, model: str = MODEL) -> dict[str, Any]:
    prompt = (TRANSLATION_PROMPT if translation else GEC_PROMPT).format(source=text)
    return {
        "model": model,
        "stream": False,
        "store": False,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
        "include_reasoning": True,
        "reasoning": {"effort": "low"},
    }


def expression_retry_body(expression: str, *, model: str = MODEL) -> dict[str, Any]:
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


def word_retry_body(word: str, *, model: str = MODEL) -> dict[str, Any]:
    if not isinstance(word, str) or not word or any(char.isspace() for char in word):
        raise ReviewerError("word-only input requires one rejected word")
    return {
        "model": model,
        "stream": False,
        "store": False,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": WORD_RETRY_PROMPT.format(word=word)}]}],
        "include_reasoning": True,
        "reasoning": {"effort": "low"},
    }


def parse_text(value: Mapping[str, Any]) -> str:
    texts = [
        part["text"]
        for item in value.get("output", [])
        if isinstance(item, dict) and item.get("type") == "message" and item.get("role") == "assistant"
        for part in item.get("content", [])
        if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str)
    ]
    if len(texts) != 1:
        raise ReviewerError("expected exactly one assistant text field")
    return texts[0]


def _parse_word(value: Mapping[str, Any]) -> Proposal:
    texts = [
        part["text"]
        for item in value.get("output", [])
        if isinstance(item, dict) and item.get("type") == "message" and item.get("role") == "assistant"
        for part in item.get("content", [])
        if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str)
    ]
    if len(texts) != 1 or not texts[0] or len(texts[0]) > 2000 or any(char.isspace() for char in texts[0]):
        raise ReviewerError("expected one unwrapped word; no format repair or retry")
    word = texts[0]
    if not word[0].isalpha() or not (word[-1].isalpha() or unicodedata.category(word[-1]).startswith("M")):
        raise ReviewerError("expected plain word, not JSON or markup")
    if not all(char.isalpha() or unicodedata.category(char).startswith("M") or char in "-'’" for char in word):
        raise ReviewerError("expected plain word characters, not escape sequences or markup")
    return Proposal(False, word, False)


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate response key")
        result[key] = value
    return result


def _thinking_observation(value: Mapping[str, Any], expected_effort: str = "low") -> dict[str, Any]:
    usage = value.get("usage") or {}
    details = usage.get("output_tokens_details") or {}
    tokens = details.get("reasoning_tokens")
    effort = (value.get("reasoning") or {}).get("effort")
    return {"verified": effort == expected_effort and isinstance(tokens, int) and tokens >= 0,
            "reasoning_tokens": tokens, "effort": effort}


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _save(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    if path.exists():
        if path.read_bytes() != encoded:
            raise RuntimeError(f"immutable artifact conflict: {path}")
        return
    fd, temporary = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class ResponseTransport(Protocol):
    def request(self, endpoint: str, body: bytes, headers: Mapping[str, str], timeout: float) -> tuple[int, Mapping[str, str], bytes]: ...


class FakeTransport:
    """Small deterministic transport for the source boundary tests."""

    def __init__(self, payload: Mapping[str, Any], *, status: int = 200):
        self.payload = json.dumps(payload, ensure_ascii=False).encode()
        self.status = status
        self.calls: list[dict[str, Any]] = []

    def request(self, endpoint: str, body: bytes, headers: Mapping[str, str], timeout: float) -> tuple[int, Mapping[str, str], bytes]:
        self.calls.append({"endpoint": endpoint, "body": body, "timeout": timeout})
        return self.status, {"Content-Type": "application/json"}, self.payload


class _HttpTransport:
    def request(self, endpoint: str, body: bytes, headers: Mapping[str, str], timeout: float) -> tuple[int, Mapping[str, str], bytes]:
        url = urllib.parse.urlsplit(endpoint)
        connection = http.client.HTTPConnection(url.hostname, url.port, timeout=timeout)
        try:
            connection.request("POST", (url.path or "/").rstrip("/") + "/responses", body=body, headers=dict(headers))
            response = connection.getresponse()
            return response.status, {"Content-Type": response.getheader("Content-Type") or ""}, response.read(2_000_001)
        finally:
            connection.close()


class Client:
    """Historical one-in-flight client with complete capture and fail-closed parsing."""

    def __init__(
        self,
        *,
        endpoint: str | None = None,
        credential_env: str | None = None,
        timeout: float = 300.0,
        allow_live: bool = False,
        transport: ResponseTransport | None = None,
        reuse: Mapping[str, Mapping[str, str]] | None = None,
        reasoning_effort: str = "low",
    ):
        self.endpoint = endpoint
        self.credential_env = credential_env
        self.timeout = timeout
        self.allow_live = allow_live
        self.transport = transport
        self.reuse = dict(reuse or {})
        self.reasoning_effort = reasoning_effort
        self.network_calls = 0

    def _materialize_reuse(self, path: Path) -> None:
        item = self.reuse.get(str(path))
        if item and not path.exists():
            source = Path(item["source"])
            if _sha(source) != item["sha256"]:
                raise ValueError("reused source hash changed")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(source.read_bytes())

    def call(self, directory: str | Path, body: Mapping[str, Any], kind: str) -> dict[str, Any]:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        request_path, raw_path, observation_path = (directory / name for name in ("request.json", "response.json", "observation.json"))
        for path in (request_path, raw_path, observation_path):
            self._materialize_reuse(path)
        if observation_path.exists():
            observation = json.loads(observation_path.read_text())
            if json.loads(request_path.read_text()) != body:
                raise ValueError("saved request differs")
            return observation
        interrupted = request_path.exists() and not raw_path.exists()
        _save(request_path, body)
        if interrupted:
            raw = {"operational_failure": True, "failure": "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE", "http_seconds": None, "body_base64": None}
        elif not raw_path.exists():
            started = time.monotonic()
            raw: dict[str, Any] = {"operational_failure": False, "started_monotonic": started}
            try:
                if self.transport is None:
                    if not self.allow_live:
                        raise PermissionError("LIVE_EXECUTION_NOT_AUTHORIZED")
                    if not self.endpoint or not self.credential_env or not os.environ.get(self.credential_env):
                        raise PermissionError("explicit endpoint and credential environment are required")
                    transport: ResponseTransport = _HttpTransport()
                    authorization = "Bearer " + os.environ[self.credential_env]
                else:
                    transport = self.transport
                    authorization = ""
                headers = {"Content-Type": "application/json", "Accept": "application/json"}
                if authorization:
                    headers["Authorization"] = authorization
                self.network_calls += 1
                status, response_headers, payload = transport.request(
                    self.endpoint or "fake://offline", json.dumps(body, ensure_ascii=False).encode(), headers, self.timeout
                )
                raw.update(http_status=status, content_type=response_headers.get("Content-Type"), body_base64=base64.b64encode(payload).decode(), response_bytes=len(payload))
                if status != 200 or len(payload) > 2_000_000:
                    raw.update(operational_failure=True, failure="HTTP_STATUS_OR_RESPONSE_BOUND")
            except (OSError, TimeoutError, http.client.HTTPException, PermissionError, ValueError) as exc:
                raw.update(operational_failure=True, failure="TIMEOUT" if isinstance(exc, TimeoutError) else str(exc))
                raw.setdefault("body_base64", None)
            finally:
                raw["http_seconds"] = time.monotonic() - started
                _save(raw_path, raw)
        raw = json.loads(raw_path.read_text())
        observation: dict[str, Any] = {
            "kind": kind, "request_sha256": _sha(request_path), "response_sha256": _sha(raw_path),
            "operational_failure": raw.get("operational_failure", True), "failure": raw.get("failure"),
            "http_seconds": raw.get("http_seconds"), "http_status": raw.get("http_status"),
            "proposal": None, "text": None, "output_tokens": None, "reasoning_tokens": None,
        }
        if not observation["operational_failure"]:
            try:
                value = json.loads(base64.b64decode(raw["body_base64"]), object_pairs_hook=_unique_pairs)
                if value.get("status") != "completed" or value.get("model") != MODEL:
                    raise ValueError("incomplete response or wrong model")
                thinking = _thinking_observation(value, self.reasoning_effort)
                if not thinking["verified"]:
                    raise ValueError("low reasoning not verified")
                observation.update(response_id=value.get("id"), returned_model=value["model"], thinking_observation=thinking,
                                   output_tokens=(value.get("usage") or {}).get("output_tokens"), reasoning_tokens=thinking.get("reasoning_tokens"),
                                   input_tokens=(value.get("usage") or {}).get("input_tokens"))
                if kind == "reviewer":
                    observation["proposal"] = parse_proposal(value)
                    observation["proposal"] = observation["proposal"].__dict__
                elif kind == "expression-retry":
                    observation["proposal"] = parse_expression(value).__dict__
                elif kind == "word-only-retry":
                    observation["proposal"] = _parse_word(value).__dict__
                else:
                    observation["text"] = parse_text(value)
            except (ValueError, KeyError, TypeError, AttributeError, ReviewerError) as exc:
                observation.update(operational_failure=True, failure="PROTOCOL_OR_CONTENT: " + str(exc))
        _save(observation_path, observation)
        return observation


def request_contract() -> dict[str, object]:
    return {
        "client": "Client.call",
        "http": "POST endpoint/responses with JSON body and Authorization from credential_env",
        "capture": "request -> bounded raw response/timing -> parsed observation",
        "timeout_seconds": 300,
        "response_bound_bytes": 2_000_000,
        "retry": "none; request-only interruption becomes durable failure",
        "default_network_calls": 0,
        "live_requires": ["allow_live", "endpoint", "credential_env"],
    }
