"""Strict, paired contextual validation for the 007-i experiment.

This module contains the data-free protocol boundary used by the private
007-i driver.  It deliberately has no default endpoint, credential lookup, or
network side effect.  Filled sentences, model responses, and the frozen case
records stay in the caller-owned private experiment root.
"""

from __future__ import annotations

import base64
import hashlib
import http.client
import json
import math
import os
import statistics
import time
import urllib.parse
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, Protocol

from .curated.historical_scoring import edit_key, edits
from .curated.patching import apply_edits
from .curated.protected import is_protected, protected_intervals

MODEL = "qwen3.8-27b"
EFFORT = "low"
WORKERS = 8
MAX_RESPONSE_BYTES = 2_000_000
TIMEOUT_SECONDS = 300.0
CHOICES = frozenset({"USE_CANDIDATE", "KEEP_ORIGINAL", "UNCERTAIN"})

# This is copied byte-for-byte from the owner-supplied frozen prompt.  The
# hash is checked before a campaign can be frozen; do not edit or rewrap it.
FROZEN_PROMPT = """You are validating one proposed Slovenian word substitution.

Sentence:
{sentence}

Original word:
{original}

Proposed word:
{candidate}

Would replacing the original word with the proposed word make this
specific sentence better standard Slovenian while preserving its
intended meaning?

Do not propose another word.
Do not rewrite the sentence.
Do not prefer the proposal merely because it is a known dictionary word.
If the original could be an intentional name, term, rare word, foreign
word, or otherwise appropriate in context, keep the original.

Return exactly one of:
USE_CANDIDATE
KEEP_ORIGINAL
UNCERTAIN
"""
FROZEN_PROMPT_SHA256 = "572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d"


class ValidatorError(RuntimeError):
    """Raised when a request, response, or persisted observation is invalid."""


class ResponseTransport(Protocol):
    def request(
        self,
        endpoint: str,
        body: bytes,
        headers: Mapping[str, str],
        timeout: float,
    ) -> tuple[int, Mapping[str, str], bytes]: ...


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode(
        "utf-8"
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidatorError("duplicate JSON key")
        result[key] = value
    return result


def prompt_text(sentence: str, original: str, candidate: str) -> str:
    if not all(isinstance(item, str) for item in (sentence, original, candidate)):
        raise ValidatorError("prompt fields must be strings")
    return FROZEN_PROMPT.format(sentence=sentence, original=original, candidate=candidate)


def prompt_sha256() -> str:
    return sha256_bytes(FROZEN_PROMPT.encode("utf-8"))


def request_body(sentence: str, original: str, candidate: str, *, model: str = MODEL) -> dict[str, Any]:
    if model != MODEL:
        raise ValidatorError("validator model is not frozen")
    return {
        "model": MODEL,
        "stream": False,
        "store": False,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt_text(sentence, original, candidate)}],
            }
        ],
        "include_reasoning": True,
        "reasoning": {"effort": EFFORT},
    }


def parse_response(value: object, *, model: str = MODEL, effort: str = EFFORT) -> dict[str, Any]:
    """Strictly parse the only three accepted validator output choices."""
    if not isinstance(value, Mapping):
        raise ValidatorError("response is not an object")
    if value.get("status") != "completed":
        raise ValidatorError("response is not completed")
    if value.get("model") != model:
        raise ValidatorError("response model mismatch")
    reasoning = value.get("reasoning")
    if not isinstance(reasoning, Mapping) or reasoning.get("effort") != effort:
        raise ValidatorError("response reasoning effort mismatch")
    usage = value.get("usage")
    if not isinstance(usage, Mapping):
        raise ValidatorError("response usage is missing")
    token_details = usage.get("output_tokens_details")
    if not isinstance(token_details, Mapping):
        raise ValidatorError("response reasoning token accounting is missing")
    reasoning_tokens = token_details.get("reasoning_tokens")
    input_tokens = usage.get("input_tokens")
    output_tokens = usage.get("output_tokens")
    if any(type(item) is not int or item < 0 for item in (input_tokens, output_tokens, reasoning_tokens)):
        raise ValidatorError("response token accounting is invalid")
    output = value.get("output")
    if not isinstance(output, list):
        raise ValidatorError("response output is missing")
    texts: list[str] = []
    for item in output:
        if not isinstance(item, Mapping):
            continue
        if item.get("type") != "message" or item.get("role") != "assistant":
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if isinstance(part, Mapping) and part.get("type") == "output_text":
                text = part.get("text")
                if not isinstance(text, str):
                    raise ValidatorError("assistant output text is not a string")
                texts.append(text)
    if len(texts) != 1:
        raise ValidatorError("expected exactly one assistant output-text field")
    decision = texts[0].strip()
    if decision not in CHOICES:
        raise ValidatorError("validator choice is not exact")
    return {
        "decision": decision,
        "returned_model": model,
        "reasoning_effort": effort,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
    }


def parse_response_bytes(payload: bytes, *, model: str = MODEL, effort: str = EFFORT) -> dict[str, Any]:
    if len(payload) > MAX_RESPONSE_BYTES:
        raise ValidatorError("response exceeds byte bound")
    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidatorError("response is not valid UTF-8 JSON") from exc
    return parse_response(value, model=model, effort=effort)


def stable_key(candidate: Mapping[str, Any]) -> tuple[str, int, int, int, int]:
    phase = candidate.get("phase")
    case_index = candidate.get("case_index")
    start = candidate.get("target_start")
    end = candidate.get("target_end")
    ordinal = candidate.get("target_ordinal")
    if (
        not isinstance(phase, str)
        or type(case_index) is not int
        or type(start) is not int
        or type(end) is not int
        or type(ordinal) is not int
    ):
        raise ValidatorError("candidate stable key is malformed")
    return phase, case_index, start, end, ordinal


def candidate_path_id(candidate: Mapping[str, Any]) -> str:
    phase, index, start, end, ordinal = stable_key(candidate)
    if phase not in {"dassle-spelling", "dassle-spelling-preservation"}:
        raise ValidatorError("candidate phase is not allowed")
    return f"{phase}-{index:06d}-t{start:06d}-{end:06d}-{ordinal:03d}"


def ordered_candidates(candidates: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = [dict(candidate) for candidate in candidates]
    result.sort(key=stable_key)
    if len({stable_key(item) for item in result}) != len(result):
        raise ValidatorError("duplicate candidate stable key")
    return result


def partitions(candidates: Sequence[Mapping[str, Any]], workers: int = WORKERS) -> dict[int, list[dict[str, Any]]]:
    if type(workers) is not int or not 1 <= workers <= WORKERS:
        raise ValidatorError("worker count is outside the frozen bound")
    ordered = ordered_candidates(candidates)
    result = {worker: [] for worker in range(workers)}
    for position, candidate in enumerate(ordered):
        result[position % workers].append(dict(candidate))
    return result


def candidate_manifest(candidates: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], str]:
    ordered = ordered_candidates(candidates)
    manifest: list[dict[str, Any]] = []
    for position, candidate in enumerate(ordered):
        manifest.append(
            {
                "manifest_position": position,
                "stable_key": list(stable_key(candidate)),
                "candidate_id": candidate_path_id(candidate),
                "candidate": candidate["candidate"],
                "candidate_form": candidate["candidate_form"],
                "mechanical_edit": candidate["mechanical_edit"],
            }
        )
    return manifest, sha256_bytes(canonical_bytes(manifest))


def _is_json_object(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def immutable_write(path: Path, data: bytes) -> str:
    """Write a private immutable artifact, refusing replacement or symlinks."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink():
        raise ValidatorError(f"refusing symlink artifact: {path.name}")
    if path.exists():
        if not path.is_file() or path.read_bytes() != data:
            raise ValidatorError(f"immutable artifact conflict: {path.name}")
        return sha256_bytes(data)
    temporary = path.with_name("." + path.name + ".pending")
    if temporary.exists() or temporary.is_symlink():
        raise ValidatorError(f"temporary artifact already exists: {temporary.name}")
    temporary.write_bytes(data)
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)
    os.chmod(path, 0o600)
    return sha256_bytes(data)


def immutable_json(path: Path, value: object) -> str:
    return immutable_write(path, canonical_bytes(value))


class _HttpTransport:
    def request(
        self,
        endpoint: str,
        body: bytes,
        headers: Mapping[str, str],
        timeout: float,
    ) -> tuple[int, Mapping[str, str], bytes]:
        url = urllib.parse.urlsplit(endpoint)
        if url.scheme not in {"http", "https"} or not url.hostname:
            raise ValidatorError("endpoint must be an explicit HTTP(S) URL")
        connection_class = http.client.HTTPSConnection if url.scheme == "https" else http.client.HTTPConnection
        connection = connection_class(url.hostname, url.port, timeout=timeout)
        try:
            path = url.path or "/"
            if not path.endswith("/responses"):
                path = path.rstrip("/") + "/responses"
            if url.query:
                path += "?" + url.query
            connection.request("POST", path, body=body, headers=dict(headers))
            response = connection.getresponse()
            return response.status, {"Content-Type": response.getheader("Content-Type") or ""}, response.read(
                MAX_RESPONSE_BYTES + 1
            )
        finally:
            connection.close()


def _safe_raw(value: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value[key] for key in ("http_status", "content_type", "response_bytes", "body_base64", "http_seconds", "failure") if key in value}


def perform_call(
    directory: Path,
    body: Mapping[str, Any],
    *,
    endpoint: str | None = None,
    credential_env: str | None = None,
    transport: ResponseTransport | None = None,
    timeout: float = TIMEOUT_SECONDS,
    max_response_bytes: int = MAX_RESPONSE_BYTES,
) -> dict[str, Any]:
    """Persist request, raw bounded response, then parsed observation exactly once."""
    directory.mkdir(parents=True, exist_ok=True)
    request_path = directory / "request.json"
    raw_path = directory / "raw-response.json"
    observation_path = directory / "observation.json"
    request_existed = request_path.exists()
    request_bytes = canonical_bytes(body)
    immutable_write(request_path, request_bytes)
    request_sha = sha256_bytes(request_bytes)
    if observation_path.exists():
        if not _is_json_object(observation_path) or not raw_path.is_file():
            raise ValidatorError("completed observation lacks immutable raw response")
        observation = json.loads(observation_path.read_text(encoding="utf-8"))
        if not isinstance(observation, dict) or observation.get("request_sha256") != request_sha:
            raise ValidatorError("persisted observation request identity mismatch")
        return observation
    if request_existed and not raw_path.exists():
        return interrupted_observation(directory, body)
    if raw_path.exists():
        if not _is_json_object(raw_path):
            raise ValidatorError("raw response is not a regular file")
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
    else:
        started = time.monotonic()
        raw_data: dict[str, Any] = {"operational_failure": False}
        try:
            if transport is None:
                if endpoint is None or credential_env is None or not os.environ.get(credential_env):
                    raise PermissionError("explicit endpoint and credential environment are required")
                authorization = "Bearer " + os.environ[credential_env]
                actual_transport: ResponseTransport = _HttpTransport()
            else:
                authorization = ""
                actual_transport = transport
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            if authorization:
                headers["Authorization"] = authorization
            status, response_headers, payload = actual_transport.request(
                endpoint or "fake://offline", request_bytes, headers, timeout
            )
            raw_data.update(
                http_status=status,
                content_type=response_headers.get("Content-Type"),
                response_bytes=len(payload),
                body_base64=base64.b64encode(payload).decode("ascii"),
            )
            if status != 200:
                raw_data.update(operational_failure=True, failure="HTTP_STATUS")
            elif len(payload) > max_response_bytes:
                raw_data.update(operational_failure=True, failure="RESPONSE_BOUND")
        except (OSError, TimeoutError, http.client.HTTPException, PermissionError, ValidatorError) as exc:
            raw_data.update(operational_failure=True, failure="TIMEOUT" if isinstance(exc, TimeoutError) else type(exc).__name__)
            raw_data.setdefault("body_base64", None)
        raw_data["http_seconds"] = time.monotonic() - started
        raw = raw_data
        immutable_json(raw_path, raw)
    if not isinstance(raw, dict):
        raise ValidatorError("raw response is not an object")
    observation: dict[str, Any] = {
        "request_sha256": request_sha,
        "response_sha256": sha256_file(raw_path),
        "http_status": raw.get("http_status"),
        "http_seconds": raw.get("http_seconds"),
        "operational_failure": bool(raw.get("operational_failure", True)),
        "failure": raw.get("failure"),
        "decision": None,
        "returned_model": None,
        "reasoning_effort": None,
        "input_tokens": None,
        "output_tokens": None,
        "reasoning_tokens": None,
    }
    if not observation["operational_failure"]:
        encoded = raw.get("body_base64")
        try:
            if not isinstance(encoded, str):
                raise ValidatorError("raw response body is missing")
            parsed = json.loads(base64.b64decode(encoded), object_pairs_hook=_unique_pairs)
            observation.update(parse_response(parsed))
        except (ValueError, TypeError, KeyError, ValidatorError) as exc:
            observation.update(operational_failure=True, failure="PROTOCOL_" + str(exc))
    immutable_json(observation_path, observation)
    return observation


def interrupted_observation(directory: Path, body: Mapping[str, Any]) -> dict[str, Any]:
    """Close a request-only interruption without dispatching or resampling."""
    request_bytes = canonical_bytes(body)
    immutable_write(directory / "request.json", request_bytes)
    raw = {
        "operational_failure": True,
        "failure": "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE",
        "http_seconds": None,
        "http_status": None,
        "response_bytes": 0,
        "body_base64": None,
    }
    immutable_json(directory / "raw-response.json", raw)
    observation = {
        "request_sha256": sha256_bytes(request_bytes),
        "response_sha256": sha256_file(directory / "raw-response.json"),
        "http_status": None,
        "http_seconds": None,
        "operational_failure": True,
        "failure": raw["failure"],
        "decision": None,
        "returned_model": None,
        "reasoning_effort": None,
        "input_tokens": None,
        "output_tokens": None,
        "reasoning_tokens": None,
    }
    immutable_json(directory / "observation.json", observation)
    return observation


def observation_decision(observation: Mapping[str, Any]) -> str | None:
    if observation.get("operational_failure"):
        return None
    decision = observation.get("decision")
    return decision if decision in CHOICES else None


def attribution(source: str, reference: object, edit: Sequence[Any]) -> dict[str, Any]:
    """Use the unchanged token-coordinate scorer for one candidate edit."""
    if not isinstance(reference, str):
        return {"status": "unresolved", "reason": "reference-unavailable"}
    try:
        isolated = edits(source, apply_edits(source, [tuple(edit)]))
        gold = edits(source, reference)
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        return {"status": "unresolved", "reason": "scorer-failure", "detail": str(exc)}
    if len(isolated) != 1:
        return {"status": "unresolved", "reason": "isolated-edit-count", "isolated_edit_count": len(isolated)}
    item = isolated[0]
    if item["start"] != int(edit[0]) or item["end"] != int(edit[1]):
        return {"status": "unresolved", "reason": "isolated-edit-span-incompatible"}
    status = "exact_reference" if edit_key(item) in {edit_key(value) for value in gold} else "non_reference"
    return {"status": status, "reason": "token-edit-key-membership", "isolated_edit_key": list(edit_key(item)), "gold_edit_count": len(gold)}


def integrity(source: str, output: str, allowed_edits: Sequence[Sequence[Any]]) -> dict[str, int]:
    """Prove exact composition and that protected spans were not touched."""
    intervals = protected_intervals(source)
    observed = edits(source, output)
    protected = sum(is_protected(item["start"], item["end"], intervals) for item in observed)
    allowed = {(int(item[0]), int(item[1])) for item in allowed_edits}
    outside = sum(
        (item["start"], item["end"]) not in allowed
        for item in observed
        if not is_protected(item["start"], item["end"], intervals)
    )
    return {"protected_differences": protected, "outside_span_differences": outside}


def distribution(values: Iterable[int | float | None]) -> dict[str, Any]:
    cleaned = sorted(value for value in values if value is not None)
    if not cleaned:
        return {"n": 0, "sum": 0, "mean": None, "median": None, "p95": None, "max": None}
    return {
        "n": len(cleaned),
        "sum": sum(cleaned),
        "mean": statistics.mean(cleaned),
        "median": statistics.median(cleaned),
        "p95": cleaned[max(0, math.ceil(0.95 * len(cleaned)) - 1)],
        "max": cleaned[-1],
    }
