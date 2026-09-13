"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Proxy."""

from __future__ import annotations

import http.client
import json
import os
import re
import select
import tempfile
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import cast
from urllib.parse import urlparse

from config import canonical_bytes
from corpus import Corpus
from detector import detect, tokenize
from protected import protected_intervals
from qwen_client import ResponsesReviewer, responses_path
from repair import accept, apply_edits


class ProxyError(ValueError):
    pass


def _split_sse(raw: bytes) -> list[tuple[str, str]]:
    text = raw.decode("utf-8")
    result: list[tuple[str, str]] = []
    cursor = 0
    for match in re.finditer(r"\r\n\r\n|\n\n", text):
        result.append((text[cursor : match.start()], match.group(0)))
        cursor = match.end()
    if cursor < len(text):
        result.append((text[cursor:], ""))
    return result


def _event(block: str) -> dict[str, object] | None:
    data_lines = [line[5:] for line in block.splitlines() if line.startswith("data:")]
    if not data_lines or "".join(data_lines).strip() == "[DONE]":
        return None
    try:
        value = json.loads("\n".join(data_lines))
    except json.JSONDecodeError as exc:
        raise ProxyError("upstream SSE contains malformed JSON") from exc
    if not isinstance(value, dict):
        raise ProxyError("upstream SSE event is not an object")
    return value


def _events(raw: bytes) -> list[tuple[str, dict[str, object]]]:
    result: list[tuple[str, dict[str, object]]] = []
    for block, _delimiter in _split_sse(raw):
        value = _event(block)
        if value is not None:
            result.append((block, value))
    return result


def _complete_prefix(raw: bytes) -> bytes | None:
    """Return bytes through a delimited response.completed event, if present."""
    text = raw.decode("utf-8")
    cursor = 0
    for match in re.finditer(r"\r\n\r\n|\n\n", text):
        block = text[cursor : match.start()]
        value = _event(block)
        cursor = match.end()
        if value is not None and value.get("type") == "response.completed":
            return text[:cursor].encode("utf-8")
    return None


def _bounded_read(
    response: http.client.HTTPResponse,
    maximum: int,
    timeout: float,
    *,
    require_complete_sse: bool = False,
) -> bytes:
    """Read within byte/time limits, stopping at a complete SSE event."""
    if response.length is not None:
        if response.length > maximum:
            raise ProxyError("upstream response exceeds capture bound")
        raw = response.read(response.length)
        if require_complete_sse and _complete_prefix(raw) is None:
            raise ProxyError("upstream SSE is incomplete")
        return raw
    raw_socket = getattr(getattr(response, "fp", None), "raw", None)
    raw_socket = getattr(raw_socket, "_sock", None)
    if raw_socket is None:
        raise ProxyError("upstream socket boundary is unavailable")
    chunks: list[bytes] = []
    total = 0
    deadline = time.monotonic() + timeout
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ProxyError("upstream capture timeout")
        ready, _, _ = select.select([raw_socket], [], [], min(remaining, 0.5))
        if not ready:
            continue
        piece = response.read1(min(65536, maximum - total + 1))
        if not piece:
            raw = b"".join(chunks)
            if require_complete_sse:
                raise ProxyError("upstream SSE is incomplete")
            return raw
        total += len(piece)
        if total > maximum:
            raise ProxyError("upstream response exceeds capture bound")
        chunks.append(piece)
        raw = b"".join(chunks)
        if require_complete_sse:
            complete = _complete_prefix(raw)
            if complete is not None:
                return complete


def _nested_output_text(value: object) -> list[tuple[dict[str, object], str]]:
    found: list[tuple[dict[str, object], str]] = []
    if isinstance(value, dict):
        if value.get("type") == "output_text" and isinstance(value.get("text"), str):
            found.append((value, str(value["text"])))
        for child in value.values():
            found.extend(_nested_output_text(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_nested_output_text(child))
    return found


def _assistant_output_texts(value: dict[str, object]) -> list[dict[str, object]]:
    response = value.get("response")
    if not isinstance(response, dict) or not isinstance(response.get("output"), list):
        return []
    fields: list[dict[str, object]] = []
    for item in response["output"]:
        if (
            not isinstance(item, dict)
            or item.get("type") != "message"
            or item.get("role") != "assistant"
        ):
            continue
        content = item.get("content")
        if isinstance(content, list):
            fields.extend(
                part
                for part in content
                if isinstance(part, dict) and part.get("type") == "output_text"
            )
    return [field for field in fields if isinstance(field.get("text"), str)]


def _render_event(block: str, value: dict[str, object]) -> str:
    lines = block.splitlines()
    data_index = next((index for index, line in enumerate(lines) if line.startswith("data:")), None)
    if data_index is None:
        return block
    lines[data_index] = "data: " + json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    lines = [
        line
        for index, line in enumerate(lines)
        if index == data_index or not line.startswith("data:")
    ]
    return "\n".join(lines)


def transform_sse(raw: bytes, repair: Callable[[str], str]) -> tuple[bytes, bool]:
    """Repair only assistant output text while retaining every SSE block."""
    blocks = _split_sse(raw)
    parsed: list[dict[str, object] | None] = [_event(block) for block, _ in blocks]
    streams: dict[str, list[str]] = {}
    for value in parsed:
        if value is not None and value.get("type") == "response.output_text.delta":
            delta = value.get("delta")
            if isinstance(delta, str):
                item_id = str(value.get("item_id", "__single__"))
                streams.setdefault(item_id, []).append(delta)
    repaired: dict[str, str] = {}
    for item_id, parts in streams.items():
        repaired[item_id] = repair("".join(parts))
    direct_repaired: list[tuple[dict[str, object], str]] = []
    if not streams:
        for value in parsed:
            if value is not None and value.get("type") == "response.completed":
                for field in _assistant_output_texts(value):
                    original = str(field["text"])
                    changed = repair(original)
                    field["text"] = changed
                    direct_repaired.append((field, original))
    if not streams and not direct_repaired:
        return raw, False
    output: list[str] = []
    used_first: set[str] = set()
    for (block, delimiter), value in zip(blocks, parsed, strict=True):
        if value is not None:
            event_type = value.get("type")
            item_id = str(value.get("item_id", "__single__"))
            if event_type == "response.output_text.delta" and item_id in repaired:
                value["delta"] = repaired[item_id] if item_id not in used_first else ""
                used_first.add(item_id)
            elif event_type == "response.output_text.done" and item_id in repaired:
                value["text"] = repaired[item_id]
            else:
                for field, old in _nested_output_text(value):
                    for item_id, parts in streams.items():
                        if old == "".join(parts):
                            field["text"] = repaired[item_id]
            if event_type == "response.completed" and direct_repaired:
                # Direct fields were mutated above; this branch preserves their event.
                pass
            if event_type in {
                "response.output_text.delta",
                "response.output_text.done",
                "response.completed",
            } or any(
                old == "".join(streams[item_id])
                for _field, old in _nested_output_text(value)
                for item_id in streams
            ):
                block = _render_event(block, value)
        output.append(block + delimiter)
    return "".join(output).encode("utf-8"), True


@dataclass(frozen=True)
class Forwarded:
    status: int
    body: bytes
    content_type: str


@dataclass
class RepairEngine:
    index: Path
    reviewer: ResponsesReviewer
    mode: str = "local-context"
    _details: list[dict[str, object]] | None = None

    def begin_request(self) -> None:
        self._details = []

    def take_details(self) -> list[dict[str, object]]:
        details = self._details or []
        self._details = None
        return details

    def repair(self, text: str) -> str:
        raw_started = time.monotonic()
        intervals = protected_intervals(text)
        with Corpus(self.index) as corpus:
            detector_started = time.monotonic()
            candidates = detect(text, corpus, intervals, mode=self.mode, maximum=4)
            detector_seconds = time.monotonic() - detector_started
            tokens = tokenize(text, intervals)
            decisions: list[dict[str, object]] = []
            edits: list[tuple[int, int, str]] = []
            reviewer_seconds = 0.0
            for candidate in candidates:
                token_index = next(
                    (i for i, token in enumerate(tokens) if token.start == candidate.start), None
                )
                if token_index is None:
                    continue
                left = tokens[token_index - 1].key if token_index else None
                right = tokens[token_index + 1].key if token_index + 1 < len(tokens) else None
                review_started = time.monotonic()
                proposal: dict[str, object] | None = None
                acceptance: dict[str, object] = {
                    "accepted": False,
                    "reason": "reviewer-error",
                    "replacement": None,
                }
                failure: str | None = None
                try:
                    value = self.reviewer.review(text, candidate.text)
                    proposal = {
                        "keep": value.keep,
                        "replacement": value.replacement,
                        "needs_wider_edit": value.needs_wider_edit,
                    }
                    decision = accept(
                        text, candidate, value, corpus, intervals, left=left, right=right
                    )
                    acceptance = {
                        "accepted": decision.accepted,
                        "reason": decision.reason,
                        "replacement": decision.replacement,
                    }
                except Exception:
                    failure = "reviewer-error"
                reviewer_seconds += time.monotonic() - review_started
                decisions.append(
                    {
                        "candidate": candidate.as_dict(),
                        "evidence": candidate.evidence,
                        "neighbors": {"left": left, "right": right},
                        "proposal": proposal,
                        "acceptance": acceptance,
                        "failure": failure,
                        "timing_seconds": round(time.monotonic() - review_started, 6),
                    }
                )
                if acceptance["accepted"] and isinstance(acceptance["replacement"], str):
                    edits.append((candidate.start, candidate.end, acceptance["replacement"]))
            repaired = apply_edits(text, edits, intervals) if edits else text
            protected_changes = 0
            for interval in intervals:
                shift = sum(
                    len(replacement) - (end - start)
                    for start, end, replacement in edits
                    if end <= interval.start
                )
                start = interval.start + shift
                if (
                    repaired[start : start + interval.end - interval.start]
                    != text[interval.start : interval.end]
                ):
                    protected_changes += 1
        if self._details is not None:
            self._details.append(
                {
                    "original": text,
                    "repaired": repaired,
                    "candidates": [candidate.as_dict() for candidate in candidates],
                    "corpus_summaries": [candidate.evidence for candidate in candidates],
                    "reviewer_decisions": decisions,
                    "acceptance": [item["acceptance"] for item in decisions],
                    "replacements": [item[2] for item in edits],
                    "timings": {
                        "raw_seconds": 0.0,
                        "detector_seconds": round(detector_seconds, 6),
                        "reviewer_seconds": round(reviewer_seconds, 6),
                        "repair_seconds": round(time.monotonic() - raw_started, 6),
                    },
                    "protected_difference_count": protected_changes,
                }
            )
        return repaired


class _Handler(BaseHTTPRequestHandler):
    server_version = "concept-verification/1"

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/responses":
            self.send_error(404)
            return
        owner = cast(ConceptProxy, self.server)
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            length = -1
        if length < 0 or length > 2_000_000:
            self.send_error(413)
            return
        body = self.rfile.read(length)
        request_id = self.headers.get("X-Concept-Request-ID", "")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", request_id):
            request_id = uuid.uuid4().hex
        started = time.monotonic()
        try:
            if hasattr(owner.engine, "begin_request"):
                owner.engine.begin_request()
            forwarded = owner.forward(body, dict(self.headers))
            raw_seconds = time.monotonic() - started
            repaired = forwarded.body
            if forwarded.status == 200 and forwarded.content_type.lower().startswith(
                "text/event-stream"
            ):
                repaired, _ = transform_sse(forwarded.body, owner.engine.repair)
                if hasattr(owner.engine, "take_details") and hasattr(owner, "write_traces"):
                    details = owner.engine.take_details()
                    owner.write_traces(
                        request_id,
                        details,
                        time.monotonic() - started,
                        raw_seconds,
                    )
            self.send_response(forwarded.status)
            self.send_header("Content-Type", forwarded.content_type or "application/octet-stream")
            self.send_header("Content-Length", str(len(repaired)))
            self.end_headers()
            self.wfile.write(repaired)
        except BrokenPipeError:
            return
        except Exception:
            try:
                self.send_error(502)
            except BrokenPipeError:
                return

    def log_message(self, *_: object) -> None:
        return


class ConceptProxy(HTTPServer):
    def __init__(
        self,
        address: tuple[str, int],
        upstream: str,
        engine: RepairEngine,
        timeout: float = 30.0,
        trace_dir: Path | None = None,
    ):
        if address[0] != "127.0.0.1":
            raise ValueError("proxy must bind to loopback")
        super().__init__(address, _Handler)
        parsed = urlparse(upstream)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("upstream must be an explicit HTTP URL")
        self.upstream = parsed
        self.engine = engine
        self.capture_timeout = timeout
        self.trace_dir = trace_dir
        if trace_dir is not None and trace_dir.exists() and trace_dir.is_symlink():
            raise ValueError("trace directory must not be a symlink")
        if trace_dir is not None:
            trace_dir.mkdir(parents=True, exist_ok=True)

    def write_traces(
        self,
        request_id: str,
        details: list[dict[str, object]],
        proxy_seconds: float,
        raw_seconds: float = 0.0,
    ) -> list[Path]:
        if self.trace_dir is None:
            return []
        paths: list[Path] = []
        for index, detail in enumerate(details):
            detail_timings = detail.get("timings")
            timings: dict[str, object] = {}
            if isinstance(detail_timings, dict):
                timings.update(detail_timings)
            value = {
                "request_id": request_id,
                "message_index": index,
                "original": detail["original"],
                "repaired": detail["repaired"],
                "candidates": detail["candidates"],
                "corpus_summaries": detail["corpus_summaries"],
                "reviewer_decisions": detail["reviewer_decisions"],
                "acceptance": detail["acceptance"],
                "replacements": detail["replacements"],
                "timings": {
                    **timings,
                    "raw_seconds": round(raw_seconds, 6),
                    "proxy_seconds": round(proxy_seconds, 6),
                },
                "protected_difference_count": detail["protected_difference_count"],
                "protocol": {"response_completed": True, "valid": True},
            }
            target = self.trace_dir / f"{request_id}-{index}.json"
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=".trace-", suffix=".tmp", dir=self.trace_dir, delete=False
            ) as handle:
                temporary = Path(handle.name)
                handle.write(canonical_bytes(value))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
            paths.append(target)
        return paths

    def forward(self, body: bytes, incoming: dict[str, str]) -> Forwarded:
        cls = (
            http.client.HTTPSConnection
            if self.upstream.scheme == "https"
            else http.client.HTTPConnection
        )
        host = self.upstream.hostname
        if host is None:
            raise ProxyError("upstream hostname is missing")
        connection = cls(host, self.upstream.port, timeout=self.capture_timeout)
        headers = {
            key: value
            for key, value in incoming.items()
            if key.lower() not in {"host", "content-length"}
        }
        reviewer = getattr(self.engine, "reviewer", None)
        api_key = getattr(reviewer, "api_key", None)
        if not any(key.lower() == "authorization" for key in headers) and api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        headers["Content-Length"] = str(len(body))
        try:
            connection.request(
                "POST", responses_path(self.upstream.path), body=body, headers=headers
            )
            response = connection.getresponse()
            content_type = response.getheader("Content-Type", "")
            raw = _bounded_read(
                response,
                8_000_000,
                self.capture_timeout,
                require_complete_sse=response.status == 200
                and content_type.lower().startswith("text/event-stream"),
            )
            return Forwarded(response.status, raw, content_type)
        finally:
            connection.close()


def main() -> int:
    upstream = os.environ.get("CONCEPT_UPSTREAM_URL", "http://127.0.0.1:8001")
    index = os.environ.get("CONCEPT_INDEX")
    if not index:
        raise SystemExit("CONCEPT_INDEX is required")
    reviewer = ResponsesReviewer(
        os.environ.get("CONCEPT_REVIEWER_URL", "http://127.0.0.1:8001/v1"),
        os.environ.get("CONCEPT_REVIEWER_MODEL", "Qwen3.8-27B"),
        timeout=float(os.environ.get("CONCEPT_TIMEOUT", "30")),
        profile=os.environ.get("CONCEPT_REVIEWER_PROFILE"),
    )
    trace_value = os.environ.get("CONCEPT_TRACE_DIR")
    proxy = ConceptProxy(
        ("127.0.0.1", 18024),
        upstream,
        RepairEngine(Path(index), reviewer),
        timeout=float(os.environ.get("CONCEPT_TIMEOUT", "30")),
        trace_dir=Path(trace_value) if trace_value else None,
    )
    proxy.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
