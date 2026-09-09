"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Proxy."""

from __future__ import annotations

import http.client
import json
import os
import select
import time
from collections.abc import Callable
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from corpus import Corpus
from detector import detect, tokenize
from protected import protected_intervals
from qwen_client import ResponsesReviewer
from repair import accept, apply_edits


class ProxyError(ValueError):
    pass


def _events(raw: bytes) -> list[tuple[str, dict[str, object]]]:
    text = raw.decode("utf-8")
    result: list[tuple[str, dict[str, object]]] = []
    for block in text.split("\n\n"):
        if not block.strip():
            continue
        data_lines = [line[5:] for line in block.split("\n") if line.startswith("data:")]
        if not data_lines or "[DONE]" in data_lines:
            continue
        try:
            value = json.loads("\n".join(data_lines))
        except json.JSONDecodeError as exc:
            raise ProxyError("upstream SSE contains malformed JSON") from exc
        if not isinstance(value, dict):
            raise ProxyError("upstream SSE event is not an object")
        result.append((block, value))
    return result


def _bounded_read(response: http.client.HTTPResponse, maximum: int, timeout: float) -> bytes:
    """Read a complete response with both byte and wall-clock bounds."""
    if response.length is not None:
        if response.length > maximum:
            raise ProxyError("upstream response exceeds capture bound")
        return response.read(response.length)
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
            return b"".join(chunks)
        total += len(piece)
        if total > maximum:
            raise ProxyError("upstream response exceeds capture bound")
        chunks.append(piece)


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


def transform_sse(raw: bytes, repair: Callable[[str], str]) -> tuple[bytes, bool]:
    """Repair only assistant output-text events; return raw bytes for no safe text."""
    parsed = _events(raw)
    streams: dict[str, list[str]] = {}
    delta_events: dict[str, list[dict[str, object]]] = {}
    for _, value in parsed:
        if value.get("type") == "response.output_text.delta" and isinstance(
            value.get("delta"), str
        ):
            item_id = str(value.get("item_id", "__single__"))
            streams.setdefault(item_id, []).append(str(value["delta"]))
            delta_events.setdefault(item_id, []).append(value)
    if not streams:
        return raw, False
    repaired: dict[str, str] = {}
    for item_id, parts in streams.items():
        original = "".join(parts)
        changed = repair(original)
        repaired[item_id] = changed
    output: list[str] = []
    used_first: set[str] = set()
    for block, value in parsed:
        event_type = value.get("type")
        item_id = str(value.get("item_id", "__single__"))
        if event_type == "response.output_text.delta" and item_id in repaired:
            value["delta"] = repaired[item_id] if item_id not in used_first else ""
            used_first.add(item_id)
        elif event_type == "response.output_text.done" and item_id in repaired:
            value["text"] = repaired[item_id]
        else:
            for field, old in _nested_output_text(value):
                for candidate in streams:
                    original = "".join(streams[candidate])
                    if old == original:
                        field["text"] = repaired[candidate]
        lines = block.split("\n")
        data_index = next(
            (index for index, line in enumerate(lines) if line.startswith("data:")), None
        )
        if data_index is not None:
            lines[data_index] = "data: " + json.dumps(
                value, ensure_ascii=False, separators=(",", ":")
            )
        output.append("\n".join(lines))
    return ("\n\n".join(output) + "\n\n").encode("utf-8"), True


@dataclass
class RepairEngine:
    index: Path
    reviewer: ResponsesReviewer
    mode: str = "local-context"

    def repair(self, text: str) -> str:
        intervals = protected_intervals(text)
        with Corpus(self.index) as corpus:
            candidates = detect(text, corpus, intervals, mode=self.mode, maximum=4)
            if not candidates:
                return text
            tokens = tokenize(text, intervals)
            edits: list[tuple[int, int, str]] = []
            for candidate in candidates:
                token_index = next(
                    (i for i, token in enumerate(tokens) if token.start == candidate.start), None
                )
                if token_index is None:
                    continue
                left = tokens[token_index - 1].key if token_index else None
                right = tokens[token_index + 1].key if token_index + 1 < len(tokens) else None
                try:
                    proposal = self.reviewer.review(text, candidate.text)
                    decision = accept(
                        text, candidate, proposal, corpus, intervals, left=left, right=right
                    )
                except Exception:
                    continue
                if decision.accepted and decision.replacement is not None:
                    edits.append((candidate.start, candidate.end, decision.replacement))
            return apply_edits(text, edits, intervals) if edits else text


class _Handler(BaseHTTPRequestHandler):
    server_version = "concept-verification/1"

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/responses":
            self.send_error(404)
            return
        owner = self.server
        length = int(self.headers.get("Content-Length", "-1"))
        if length < 0 or length > 2_000_000:
            self.send_error(413)
            return
        body = self.rfile.read(length)
        start = time.monotonic()
        try:
            raw, content_type = owner.forward(body, dict(self.headers))  # type: ignore[attr-defined]
            if content_type.startswith("text/event-stream"):
                try:
                    repaired, _ = transform_sse(raw, owner.engine.repair)  # type: ignore[attr-defined]
                except Exception:
                    complete = any(
                        value.get("type") == "response.completed" for _, value in _events(raw)
                    )
                    if not complete:
                        raise
                    repaired = raw
            else:
                repaired = raw
            self.send_response(200)
            self.send_header("Content-Type", content_type or "text/event-stream")
            self.send_header("Content-Length", str(len(repaired)))
            self.end_headers()
            self.wfile.write(repaired)
            owner.last_latency = time.monotonic() - start  # type: ignore[attr-defined]
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
        self, address: tuple[str, int], upstream: str, engine: RepairEngine, timeout: float = 30.0
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
        self.last_latency = 0.0

    def forward(self, body: bytes, incoming: dict[str, str]) -> tuple[bytes, str]:
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
                "POST", f"{self.upstream.path.rstrip('/')}/v1/responses", body=body, headers=headers
            )
            response = connection.getresponse()
            raw = _bounded_read(response, 8_000_000, self.capture_timeout)
            if response.status != 200:
                raise ProxyError("upstream returned an error")
            return raw, response.getheader("Content-Type", "")
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
    )
    proxy = ConceptProxy(
        ("127.0.0.1", 18024),
        upstream,
        RepairEngine(Path(index), reviewer),
        timeout=float(os.environ.get("CONCEPT_TIMEOUT", "30")),
    )
    proxy.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
