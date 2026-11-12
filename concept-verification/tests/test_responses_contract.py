"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Actual-HTTP tests of the explicit text Responses contract (order 015-a).

Every HTTP test runs the real production path: real ConceptProxy HTTP ->
real RepairEngine (installed qualified Pandoc plus tiny real SQLite
corpus) -> real ResponsesReviewer HTTP; only the main upstream and the
reviewer HTTP endpoint are synthetic, with different synthetic main/
review keys (order 015-a, requirement 9).  The main() usage-observer
wiring test is a separate mocked configuration unit: it proves entry-
point wiring only, binds no port and runs no live HTTP chain.
"""

from __future__ import annotations

import http.client
import io
import json
import os
import sys
import tempfile
import threading
import unittest
from collections.abc import Callable
from contextlib import redirect_stderr
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import proxy  # noqa: E402
from batch_review import BatchProposal, BatchTarget  # noqa: E402
from pandoc_protection import PandocSpec  # noqa: E402
from qwen_client import ResponsesReviewer  # noqa: E402
from tests.test_review_batch import (  # noqa: E402
    TEXT,
    _build_corpus,
    _contract_body,
    _envelope,
    _FakeUpstream,
    _prop,
    _real_spec,
    _tc_baseline,
    _tc_delta,
    _tc_item_done,
    _tc_part_done,
    _tc_raw,
    _valid_inner,
)

_MAIN_KEY = "main-key-synthetic"
_REVIEW_KEY = "review-key-synthetic"
# All words are in the tiny test lexicon: a valid completed answer with
# zero detector candidates, hence zero review calls (established by
# EngineBatchTests.test_no_candidates_zero_calls).
_CLEAN_ANSWER = "To je tako zapisano, to je tako zapisano."
# A valid aligned two-target keep batch for the two-occurrence TEXT answer:
# order 035-d R3 - one proposal for two targets is an INVALID batch
# (REASON_MISSING_ID) and can mask a failed review round trip, so every
# keep control must align both target ids.
_KEEP_BOTH = [_prop("t0", keep=True, replacement=None), _prop("t1", keep=True, replacement=None)]
# Accepted-edit control: t0 accepted (replacement "tako"), t1 kept.
_EDIT_T0_KEEP_T1 = [_prop("t0", keep=False, replacement="tako"), _prop("t1", keep=True, replacement=None)]
_TEXT_EDITED_T0 = "To je tako zapisano, to je presenetliv zapisano."
# Sentinel for "key omitted" in fixtures (module order matters: the
# matrix value tuple below references it at import time).
_ABSENT: object = object()

# Order 035-d R3 (Root clarification): the eight defined probability
# values for the persisted actual-HTTP value matrix - the key-absent
# case (the module _ABSENT sentinel) plus all seven JSON value shapes.
_LOGPROBS_MATRIX_VALUES: tuple[object, ...] = (
    _ABSENT,
    None,
    [],
    [{"token": "a", "logprob": -1.0, "start_index": 0, "end_index": 1}],
    False,
    0,
    "unexpected-string",
    {"unexpected": "shape"},
)
_MATRIX_USAGE = {"input_tokens": 11, "output_tokens": 22, "total_tokens": 33}
_MATRIX_METADATA = {"echo": "same-name-echo", "logprobs": [{"token": "echo"}]}

_REVIEW_USAGE = {"input_tokens": 5, "output_tokens": 7, "total_tokens": 12}

# Explicit declarations contradicting the completed stateless foreground
# profile (order 015-a, requirements 2, 4 and 5; ARCH13): each alone must
# make an otherwise identical completed envelope abstain raw unchanged
# with zero review calls.
_DECLARATION_NEGATIVES: dict[str, dict[str, object]] = {
    "incomplete_details_non_null": {"incomplete_details": {"reason": "x"}},
    "store_true": {"store": True},
    "previous_response_id": {"previous_response_id": "r1"},
    "conversation": {"conversation": "c1"},
    "background_true": {"background": True},
}
# Pinned unset policy positive control: absent or null values are unset;
# present store/background accept only the exact boolean false.
_DECLARATION_POSITIVE: dict[str, object] = {
    "store": False,
    "background": False,
    "previous_response_id": None,
    "conversation": None,
    "incomplete_details": None,
}


def _keep_only(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
    return {t.id: BatchProposal(t.id, True, None, False) for t in targets}


class _MainUpstream(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    status: int = 200
    content_type: str = "application/json"
    source: bytes = b"{}"
    recorded: list[dict[str, object]] = []

    def do_POST(self) -> None:  # noqa: N802
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.__class__.recorded.append(
            {"path": self.path, "headers": dict(self.headers.items()), "body": body}
        )
        self.send_response(self.status)
        self.send_header("Content-Type", self.content_type)
        self.send_header("Content-Length", str(len(self.__class__.source)))
        self.end_headers()
        self.wfile.write(self.__class__.source)

    def log_message(self, *_args: object) -> None:
        return


def _json_completed(
    answer: str = TEXT,
    *,
    obj: object = "response",
    status: object = "completed",
    error: object = None,
    message_id: str = "m",
    message_status: object = "completed",
    part: dict[str, object] | None = None,
    usage: object = _ABSENT,
    metadata: object = _ABSENT,
    declarations: dict[str, object] | None = None,
) -> bytes:
    part_value = (
        part
        if part is not None
        else {"type": "output_text", "text": answer, "content_index": 0}
    )
    message: dict[str, object] = {
        "type": "message",
        "id": message_id,
        "role": "assistant",
        "output_index": 0,
        "content": [part_value],
    }
    if message_status is not _ABSENT:
        # _ABSENT omits the status key entirely; None writes JSON null.
        message["status"] = message_status
    value: dict[str, object] = {
        "object": obj,
        "id": "r",
        "status": status,
        "output": [message],
    }
    if error is not None:
        value["error"] = error
    if usage is not _ABSENT:
        value["usage"] = usage
    if metadata is not _ABSENT:
        value["metadata"] = metadata
    if declarations is not None:
        value.update(declarations)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()


def _review_payload(
    proposals: list[dict[str, object]], usage: object = _ABSENT
) -> bytes:
    envelope = _envelope(_valid_inner(proposals))
    if usage is not _ABSENT:
        envelope["usage"] = usage
    return json.dumps(envelope, ensure_ascii=False).encode()


class _Harness:
    """One real proxy instance with recording fake main/review upstreams."""

    def __init__(
        self,
        usage_observer: Callable[[dict[str, object]], None] | None = None,
    ) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = b"{}"
        _MainUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = b"{}"
        _FakeUpstream.recorded = []
        self.servers: list[HTTPServer] = []
        self.threads: list[threading.Thread] = []
        self.main_server = HTTPServer(("127.0.0.1", 0), _MainUpstream)
        self.review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        for server in (self.main_server, self.review_server):
            self.servers.append(server)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            self.threads.append(thread)
        reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.review_server.server_port}/v1",
            "test-model",
            timeout=5.0,
            api_key=_REVIEW_KEY,
        )
        self.engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        self.proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{self.main_server.server_port}",
            self.engine,
            usage_observer=usage_observer,
        )
        self.servers.append(self.proxy_server)
        thread = threading.Thread(target=self.proxy_server.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)

    def post(
        self, body: bytes, headers: dict[str, str] | None = None
    ) -> tuple[int, bytes]:
        all_headers = {"Content-Length": str(len(body))}
        if headers:
            all_headers.update(headers)
        client = http.client.HTTPConnection(
            "127.0.0.1", self.proxy_server.server_port, timeout=20
        )
        client.request("POST", "/v1/responses", body=body, headers=all_headers)
        response = client.getresponse()
        payload = response.read()
        client.close()
        return response.status, payload

    def close(self) -> None:
        for server in self.servers:
            server.shutdown()
        for thread in self.threads:
            thread.join(5)
        for server in self.servers:
            server.server_close()
        self.temp.cleanup()


class ContractHttpTests(unittest.TestCase):
    def _expect_400(self, harness: _Harness, raw: bytes, label: str) -> None:
        _MainUpstream.source = _json_completed()
        _FakeUpstream.payload = _review_payload([_prop("t0"), _prop("t1")])
        status, payload = harness.post(raw)
        self.assertEqual(status, 400, label)
        self.assertEqual(
            json.loads(payload),
            {"error": {"type": "invalid_request", "code": label}},
            label,
        )
        # Rejections happen before any upstream or reviewer call.
        self.assertEqual(_MainUpstream.recorded, [], label)
        self.assertEqual(_FakeUpstream.recorded, [], label)

    def _json_bypass(self, **kwargs: object) -> None:
        harness = _Harness()
        try:
            source = _json_completed(**kwargs)  # type: ignore[arg-type]
            _MainUpstream.source = source
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(payload, source)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            harness.close()

    def _json_bypass_source(self, source: bytes) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = source
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(payload, source)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            harness.close()

    def _msg(self, output: str = TEXT) -> dict[str, object]:
        return {
            "type": "message",
            "id": "m",
            "role": "assistant",
            "status": "completed",
            "output_index": 0,
            "content": [{"type": "output_text", "text": output, "content_index": 0}],
        }

    def _sse_completed_event(self, response: dict[str, object]) -> bytes:
        return (
            '{"type":"response.completed","response":' + json.dumps(response) + "}"
        ).encode()

    def _sse_stream(self, completed: bytes) -> bytes:
        return _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            completed,
        )

    def _sse_bypass(self, raw: bytes) -> None:
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(payload, raw)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            harness.close()

    # A1: useful positives (JSON primary path + retained delayed SSE).

    def test_json_useful_positive_two_targets_one_review(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = _json_completed(
                usage={"input_tokens": 7, "output_tokens": 3, "total_tokens": 10}
            )
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(
                _contract_body(False), {"Authorization": f"Bearer {_MAIN_KEY}"}
            )
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            body = json.loads(payload)
            self.assertEqual(
                body["output"][0]["content"][0]["text"],
                "To je tako zapisano, to je tako zapisano.",
            )
            self.assertEqual(body["output"][0]["id"], "m")
            self.assertEqual(
                body["usage"],
                {"input_tokens": 7, "output_tokens": 3, "total_tokens": 10},
            )
        finally:
            harness.close()

    def test_json_protected_span_unchanged(self) -> None:
        harness = _Harness()
        try:
            answer = (
                "To je presenetliv zapisano, [presenetliv](http://x.example) konec."
            )
            _MainUpstream.source = _json_completed(answer=answer)
            # Both detected candidates need proposals: t0 is the prose
            # occurrence (replaced), t1 is "konec" (kept); the protected
            # link label occurrence is not a candidate.
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t1", True, None)]
            )
            status, payload = harness.post(_contract_body(False, input_text=answer))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            body = json.loads(payload)
            self.assertEqual(
                body["output"][0]["content"][0]["text"],
                "To je tako zapisano, [presenetliv](http://x.example) konec.",
            )
        finally:
            harness.close()

    def test_sse_canonical_positive_two_targets_one_review(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = _tc_baseline(TEXT)
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"presenetliv", payload)
            self.assertEqual(payload.count(b"To je tako zapisano, to je tako zapisano."), 4)
        finally:
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            harness.close()

    # A2: unsupported requests fail before main; invalid responses never
    # reach repair; error/capture semantics survive.

    def test_request_rejection_table(self) -> None:
        harness = _Harness()
        try:
            cases: list[tuple[str, bytes]] = [
                ("REQUEST_UNSUPPORTED", b'{"model":"m","input":"hi","store":false,"tools":[]}'),
                ("REQUEST_UNSUPPORTED", b'{"model":"m","input":"hi","store":true}'),
                ("REQUEST_STORE_REQUIRED", b'{"model":"m","input":"hi"}'),
                (
                    "REQUEST_UNSUPPORTED",
                    b'{"model":"m","input":"hi","store":false,"previous_response_id":"r1"}',
                ),
                (
                    "REQUEST_UNSUPPORTED",
                    b'{"model":"m","input":"hi","store":false,"include":["usage"]}',
                ),
                (
                    "REQUEST_UNSUPPORTED",
                    b'{"model":"m","input":"hi","store":false,"logprobs":true}',
                ),
                (
                    "REQUEST_UNSUPPORTED",
                    b'{"model":"m","input":"hi","store":false,"text":{"format":"json_object"}}',
                ),
                ("REQUEST_UNSUPPORTED", b'{"model":"m","input":"hi","store":false,"n":2}'),
                ("REQUEST_UNSUPPORTED", b'{"model":"m","input":"hi","store":false,"banana":1}'),
                (
                    "REQUEST_UNSUPPORTED",
                    b'{"model":"m","input":"hi","store":false,"audio":{"voice":"alloy"}}',
                ),
                ("REQUEST_SCHEMA", b'{"model":"","input":"hi","store":false}'),
                ("REQUEST_SCHEMA", (b'{"model":"' + b"x" * 201 + b'","input":"hi","store":false}')),
                ("REQUEST_SCHEMA", b'{"model":"m","input":"","store":false}'),
                ("REQUEST_SCHEMA", b'{"model":"m","input":[],"store":false}'),
                (
                    "REQUEST_SCHEMA",
                    b'{"model":"m","input":[{"role":"tool","content":"x"}],"store":false}',
                ),
                (
                    "REQUEST_SCHEMA",
                    b'{"model":"m","input":[{"role":[],"content":"x"}],"store":false}',
                ),
                (
                    "REQUEST_SCHEMA",
                    b'{"model":"m","input":[{"role":{},"content":"x"}],"store":false}',
                ),
                (
                    "REQUEST_SCHEMA",
                    b'{"model":"m","input":[{"role":"user","content":[{"type":"input_image","text":"x"}]}],"store":false}',
                ),
                ("REQUEST_SCHEMA", b'{"model":"m","input":"hi","store":false,"temperature":3}'),
                ("REQUEST_SCHEMA", b'{"model":"m","input":"hi","store":false,"top_p":0}'),
                ("REQUEST_SCHEMA", b'{"model":"m","input":"hi","store":false,"top_k":101}'),
                (
                    "REQUEST_SCHEMA",
                    b'{"model":"m","input":"hi","store":false,"max_output_tokens":0}',
                ),
                (
                    "REQUEST_SCHEMA",
                    b'{"model":"m","input":"hi","store":false,"stop":["a","b","c","d","e"]}',
                ),
                (
                    "REQUEST_SCHEMA",
                    b'{"model":"m","input":"hi","store":false,"metadata":{'
                    + b",".join(b'"k%d":"v"' % i for i in range(17))
                    + b"}}",
                ),
                (
                    "REQUEST_SCHEMA",
                    b'{"model":"m","input":"hi","store":false,"temperature":'
                    + str(10**500).encode()
                    + b"}",
                ),
                ("REQUEST_INVALID_NUMBER", b'{"model":"m","input":"hi","store":false,"x":NaN}'),
                ("REQUEST_INVALID_NUMBER", b'{"model":"m","input":"hi","store":false,"x":1e999}'),
                (
                    "REQUEST_INVALID_NUMBER",
                    b'{"model":"m","input":"hi","store":false,"temperature":1e500}',
                ),
                ("REQUEST_DUPLICATE_KEY", b'{"model":"m","model":"m","input":"hi","store":false}'),
                ("REQUEST_INVALID_JSON", b"not json"),
                ("REQUEST_INVALID_JSON", b"null"),
                ("REQUEST_INVALID_JSON", b"\xff\xfe"),
                ("REQUEST_SCHEMA", b"{}"),
                (
                    "REQUEST_UNSUPPORTED",
                    b'{"model":"m","input":"hi","store":false,"conversation":"c1"}',
                ),
                (
                    "REQUEST_UNSUPPORTED",
                    b'{"model":"m","input":"hi","store":false,"background":true}',
                ),
            ]
            for label, raw in cases:
                with self.subTest(label=label):
                    self._expect_400(harness, raw, label)
        finally:
            harness.close()

    def test_request_valid_optional_shapes(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = _json_completed(answer=_CLEAN_ANSWER)
            body = {
                "model": "m",
                "input": [
                    {"role": "system", "content": "Sistem."},
                    {"role": "user", "content": [{"type": "input_text", "text": "Pitaj."}]},
                ],
                "store": False,
                "stream": False,
                "temperature": 1.5,
                "top_p": 0.9,
                "top_k": 0,
                "max_output_tokens": 1,
                "stop": ["a", "b"],
                "metadata": {"k": "v"},
            }
            raw = json.dumps(body, separators=(",", ":")).encode()
            status, payload = harness.post(raw)
            self.assertEqual(status, 200)
            self.assertEqual(len(_MainUpstream.recorded), 1)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(
                json.loads(payload)["output"][0]["content"][0]["text"], _CLEAN_ANSWER
            )
        finally:
            harness.close()

    def test_stored_chaining_rejected_before_main(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = _json_completed(answer=_CLEAN_ANSWER)
            raw = json.dumps(
                {
                    "model": "m",
                    "input": "hi",
                    "store": False,
                    "stream": False,
                    "previous_response_id": "r-123",
                },
                separators=(",", ":"),
            ).encode()
            self._expect_400(harness, raw, "REQUEST_UNSUPPORTED")
        finally:
            harness.close()

    def test_json_response_negatives(self) -> None:
        cases: list[tuple[str, dict[str, object]]] = [
            ("incomplete_response_status", {"status": "in_progress"}),
            ("non_null_error", {"error": {"code": "x"}}),
            ("incomplete_final_message", {"message_status": "in_progress"}),
            (
                "final_part_annotations",
                {
                    "part": {
                        "type": "output_text",
                        "text": TEXT,
                        "content_index": 0,
                        "annotations": [
                            {
                                "type": "url_citation",
                                "url_index": 0,
                                "start_index": 0,
                                "end_index": 3,
                            }
                        ],
                    }
                },
            ),

        ]
        for name, kwargs in cases:
            with self.subTest(case=name):
                self._json_bypass(**kwargs)

    def test_json_final_message_null_status_bypass(self) -> None:
        # message_status=None writes an explicit JSON null status.
        self._json_bypass(message_status=None)

    def test_json_final_message_absent_status_bypass(self) -> None:
        # The status key is actually omitted, not set to null.
        self._json_bypass(message_status=_ABSENT)

    def test_json_unsupported_completed_shapes_bypass(self) -> None:
        def message(**overrides: object) -> dict[str, object]:
            value = self._msg()
            value.update(overrides)
            return value

        def envelope(*items: dict[str, object]) -> bytes:
            return json.dumps(
                {
                    "object": "response",
                    "id": "r",
                    "status": "completed",
                    "output": list(items),
                },
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode()

        absent_status = self._msg()
        del absent_status["status"]
        cases: list[tuple[str, bytes]] = [
            ("unknown_output_item", envelope({"type": "custom", "id": "c"})),
            (
                "tool_output_item",
                envelope(
                    {"type": "function_call", "id": "f", "name": "f", "arguments": "{}"}
                ),
            ),
            (
                "refusal_content_part",
                envelope(message(content=[{"type": "refusal", "refusal": "ne"}])),
            ),
            ("non_string_message_id", envelope(message(id=7))),
            ("empty_message_id", envelope(message(id=""))),
            ("extra_message_items", envelope(self._msg(), dict(self._msg()))),
            (
                "extra_content_parts",
                envelope(
                    message(
                        content=[
                            {"type": "output_text", "text": TEXT, "content_index": 0},
                            {"type": "output_text", "text": "drugo", "content_index": 1},
                        ]
                    )
                ),
            ),
            ("absent_message_status", envelope(absent_status)),
        ]
        for name, source in cases:
            with self.subTest(case=name):
                self._json_bypass_source(source)

    def test_malformed_main_is_main_error(self) -> None:
        cases: list[tuple[str, bytes, bool]] = [
            ("invalid_json", b"not json", False),
            ("invalid_utf8", b"\xff\xfe", False),
            (
                "duplicate_key",
                b'{"object":"response","object":"response","status":"completed","output":[]}',
                False,
            ),
            (
                "nonfinite_nan",
                b'{"object":"response","status":"completed","score":NaN,"output":[]}',
                False,
            ),
            (
                "nonfinite_overflow",
                b'{"object":"response","status":"completed","score":1e999,"output":[]}',
                False,
            ),
            (
                "sse_duplicate_key",
                (
                    b'data: {"type":"response.completed","response":'
                    b'{"object":"response","object":"response",'
                    b'"status":"completed","output":[]}}\n\n'
                ),
                True,
            ),
            (
                "sse_nonfinite",
                (
                    b'data: {"type":"response.completed","response":'
                    b'{"object":"response","status":"completed",'
                    b'"score":NaN,"output":[]}}\n\n'
                ),
                True,
            ),
        ]
        for name, source, stream in cases:
            with self.subTest(case=name):
                harness = _Harness()
                try:
                    _MainUpstream.content_type = (
                        "text/event-stream" if stream else "application/json"
                    )
                    _MainUpstream.source = source
                    _FakeUpstream.payload = _review_payload([_prop("t0")])
                    status, _ = harness.post(_contract_body(stream))
                    self.assertEqual(status, 502)
                    self.assertEqual(len(_FakeUpstream.recorded), 0)
                finally:
                    _MainUpstream.content_type = "application/json"
                    harness.close()

    def test_json_declaration_contradictions_bypass(self) -> None:
        for name, declarations in _DECLARATION_NEGATIVES.items():
            with self.subTest(case=name):
                self._json_bypass(declarations=dict(declarations))

    def test_json_declaration_unset_and_false_flags_repair(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = _json_completed(
                declarations=dict(_DECLARATION_POSITIVE)
            )
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(
                json.loads(payload)["output"][0]["content"][0]["text"],
                "To je tako zapisano, to je tako zapisano.",
            )
        finally:
            harness.close()

    def test_sse_declaration_contradictions_bypass(self) -> None:
        for name, extra in _DECLARATION_NEGATIVES.items():
            with self.subTest(case=name):
                response: dict[str, object] = {
                    "object": "response",
                    "id": "r",
                    "status": "completed",
                    "output": [self._msg()],
                }
                response.update(extra)
                self._sse_bypass(
                    self._sse_stream(self._sse_completed_event(response))
                )

    def test_sse_declaration_unset_and_false_flags_repair(self) -> None:
        harness = _Harness()
        try:
            response: dict[str, object] = {
                "object": "response",
                "id": "r",
                "status": "completed",
                "output": [self._msg()],
            }
            response.update(_DECLARATION_POSITIVE)
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = self._sse_stream(
                self._sse_completed_event(response)
            )
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"presenetliv", payload)
            self.assertEqual(
                payload.count(b"To je tako zapisano, to je tako zapisano."), 4
            )
        finally:
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_json_sse_final_profile_parity(self) -> None:
        # The same final response.output is handled identically by the
        # JSON primary path and the retained delayed SSE path: explicit
        # contradictions to the supported completed profile abstain raw
        # unchanged with zero review calls in both modes (order 015-a,
        # requirements 4 and 5).  The useful positives above are the
        # paired controls (both make one review and change the body).
        text_part: dict[str, object] = {
            "type": "output_text",
            "text": TEXT,
            "content_index": 0,
        }
        reasoning: dict[str, object] = {
            "type": "reasoning",
            "id": "rs",
            "status": "completed",
        }
        cases: list[tuple[str, list[dict[str, object]]]] = [
            (
                "extra_function_call_item",
                [
                    self._msg(),
                    {
                        "type": "function_call",
                        "id": "f",
                        "name": "f",
                        "arguments": "{}",
                    },
                ],
            ),
            ("extra_unknown_item", [self._msg(), {"type": "custom", "id": "c"}]),
            (
                "text_and_refusal_parts",
                [
                    {
                        "type": "message",
                        "id": "m",
                        "role": "assistant",
                        "status": "completed",
                        "output_index": 0,
                        "content": [
                            dict(text_part),
                            {"type": "refusal", "refusal": "ne"},
                        ],
                    }
                ],
            ),
            (
                "incomplete_reasoning",
                [
                    {"type": "reasoning", "id": "rs", "status": "in_progress"},
                    self._msg(),
                ],
            ),
            ("two_reasoning_items", [reasoning, dict(reasoning), self._msg()]),
        ]
        for name, items in cases:
            with self.subTest(case=name):
                response: dict[str, object] = {
                    "object": "response",
                    "id": "r",
                    "status": "completed",
                    "output": [dict(item) for item in items],
                }
                # Delayed SSE mode: valid delta indices, contradicting
                # final output.
                self._sse_bypass(
                    self._sse_stream(self._sse_completed_event(response))
                )
                # JSON mode: the identical final response.output.
                source = json.dumps(
                    response, ensure_ascii=False, separators=(",", ":")
                ).encode()
                self._json_bypass_source(source)

    def test_response_mode_mismatch_is_protocol_error(self) -> None:
        cases = [
            # Each producer source is valid for its upstream content type;
            # the mismatch is declared-mode vs observed-mode, not a
            # capture failure.
            ("application/json", True, b'{"object":"response"}'),
            (
                "text/event-stream",
                False,
                self._sse_stream(self._sse_completed_event({"object": "response"})),
            ),
        ]
        for content_type, stream, source in cases:
            with self.subTest(content_type=content_type, stream=stream):
                harness = _Harness()
                try:
                    _MainUpstream.content_type = content_type
                    _MainUpstream.source = source
                    _FakeUpstream.payload = _review_payload([_prop("t0")])
                    status, payload = harness.post(_contract_body(stream))
                    self.assertEqual(status, 502)
                    self.assertEqual(
                        json.loads(payload),
                        {
                            "error": {
                                "type": "upstream_protocol_error",
                                "code": "RESPONSE_MODE_MISMATCH",
                            }
                        },
                    )
                    self.assertEqual(len(_FakeUpstream.recorded), 0)
                finally:
                    _MainUpstream.content_type = "application/json"
                    harness.close()

    def test_sse_incomplete_response_status_bypass(self) -> None:
        raw = self._sse_stream(
            self._sse_completed_event(
                {"object": "response", "id": "r", "status": "in_progress", "output": [self._msg()]}
            )
        )
        self._sse_bypass(raw)

    def test_sse_non_null_error_bypass(self) -> None:
        raw = self._sse_stream(
            self._sse_completed_event(
                {
                    "object": "response",
                    "id": "r",
                    "status": "completed",
                    "error": {"code": "x"},
                    "output": [self._msg()],
                }
            )
        )
        self._sse_bypass(raw)

    def test_sse_missing_object_bypass(self) -> None:
        raw = self._sse_stream(
            self._sse_completed_event(
                {"id": "r", "status": "completed", "output": [self._msg()]}
            )
        )
        self._sse_bypass(raw)

    def test_sse_delta_logprobs_removed(self) -> None:
        # Order 035-c: logprobs on a delta event is always removed (by
        # presence); the stream is NOT bypassed.  The delivered SSE must
        # carry the identical answer text with the logprobs field absent.
        delta = (
            '{"type":"response.output_text.delta","item_id":"m",'
            '"logprobs":[{"token":"t"}],"delta":'
            + json.dumps(TEXT)
            + "}"
        ).encode()
        raw = _tc_raw(
            delta,
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            self._sse_completed_event(
                {
                    "object": "response",
                    "id": "r",
                    "status": "completed",
                    "output": [self._msg()],
                }
            ),
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(
                [_prop("t0", keep=True, replacement=None)]
            )
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            # logprobs must be absent from the delivered SSE
            self.assertNotIn(b"logprobs", payload)
            # answer text must be preserved
            self.assertIn(TEXT.encode(), payload)
        finally:
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_sse_done_annotations_bypass(self) -> None:
        done = (
            '{"type":"response.output_text.done","item_id":"m","text":'
            + json.dumps(TEXT)
            + ',"annotations":[{"type":"x","start_index":0,"end_index":1}]}'
        ).encode()
        raw = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            done,
            self._sse_completed_event(
                {
                    "object": "response",
                    "id": "r",
                    "status": "completed",
                    "output": [self._msg()],
                }
            ),
        )
        self._sse_bypass(raw)

    # A3: no-edit raw bytes; metadata/usage stay valid.

    def test_json_no_edit_raw_bytes(self) -> None:
        harness = _Harness()
        try:
            source = _json_completed()
            _MainUpstream.source = source
            _FakeUpstream.payload = _review_payload(
                [
                    _prop("t0", keep=True, replacement=None),
                    _prop("t1", keep=True, replacement=None),
                ]
            )
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(payload, source)
        finally:
            harness.close()

    def test_json_metadata_echo_preserved(self) -> None:
        harness = _Harness()
        try:
            echo = {"type": "output_text", "text": TEXT}
            _MainUpstream.source = _json_completed(metadata={"echo": echo})
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            # The preserved echo carries both original occurrences; the
            # repaired answer contributes none.
            self.assertEqual(payload.count(b"presenetliv"), 2)
            body = json.loads(payload)
            self.assertEqual(
                body["output"][0]["content"][0]["text"],
                "To je tako zapisano, to je tako zapisano.",
            )
            self.assertIn(
                (
                    b'"echo":{"type":"output_text",'
                    b'"text":"To je presenetliv zapisano, to je presenetliv'
                    b' zapisano."}'
                ),
                payload,
            )
        finally:
            harness.close()

    def test_json_usage_absent_null_partial_still_eligible(self) -> None:
        for usage in (_ABSENT, None, {"total_tokens": 3}):
            with self.subTest(usage="absent" if usage is _ABSENT else usage):
                harness = _Harness()
                try:
                    _MainUpstream.source = _json_completed(usage=usage)
                    _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
                    status, payload = harness.post(_contract_body(False))
                    self.assertEqual(status, 200)
                    self.assertEqual(len(_FakeUpstream.recorded), 1)
                    body = json.loads(payload)
                    self.assertEqual(
                        body["output"][0]["content"][0]["text"], _CLEAN_ANSWER
                    )
                    if usage is _ABSENT:
                        self.assertNotIn("usage", body)
                    else:
                        self.assertEqual(body["usage"], usage)
                finally:
                    harness.close()

    def test_json_empty_aligned_lists_tolerated(self) -> None:
        harness = _Harness()
        try:
            part = {
                "type": "output_text",
                "text": TEXT,
                "content_index": 0,
                "logprobs": [],
                "annotations": [],
            }
            _MainUpstream.source = _json_completed(part=part)
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"presenetliv", payload)
        finally:
            harness.close()

    def test_invalid_batch_after_valid_first_returns_original(self) -> None:
        # A valid first proposal cannot survive an invalid batch: the whole
        # answer returns the original after exactly one review attempt.
        harness = _Harness()
        try:
            source = _json_completed()
            _MainUpstream.source = source
            _FakeUpstream.payload = _review_payload(
                [_prop("t0"), _prop("t0"), _prop("t1")]
            )
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(payload, source)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
        finally:
            harness.close()

    def test_review_non200_returns_original_without_fabricated_usage(self) -> None:
        records: list[dict[str, object]] = []
        harness = _Harness(usage_observer=records.append)
        try:
            source = _json_completed()
            _MainUpstream.source = source
            _FakeUpstream.status = 500
            _FakeUpstream.payload = b'{"broken": true}'
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(payload, source)
            self.assertEqual(records, [{"review_calls": 1, "reviewer_usage": "unknown"}])
        finally:
            harness.close()

    # A4: independent main/review authentication; client-managed history.

    def test_auth_separation_keys(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = _json_completed()
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, _ = harness.post(
                _contract_body(False),
                {"Authorization": f"Bearer {_MAIN_KEY}", "Accept": "application/json"},
            )
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            main_headers = cast(dict[str, str], _MainUpstream.recorded[0]["headers"])
            self.assertEqual(main_headers.get("Authorization"), f"Bearer {_MAIN_KEY}")
            self.assertEqual(main_headers.get("Accept"), "application/json")
            review_headers = cast(dict[str, str], _FakeUpstream.recorded[0]["headers"])
            self.assertEqual(review_headers.get("Authorization"), f"Bearer {_REVIEW_KEY}")
        finally:
            harness.close()

    def test_missing_main_authorization_no_borrow(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = _json_completed()
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, _ = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            main_headers = cast(dict[str, str], _MainUpstream.recorded[0]["headers"])
            self.assertNotIn("Authorization", main_headers)
            review_headers = cast(dict[str, str], _FakeUpstream.recorded[0]["headers"])
            self.assertEqual(review_headers.get("Authorization"), f"Bearer {_REVIEW_KEY}")
        finally:
            harness.close()

    def test_linkage_headers_not_forwarded(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = _json_completed(answer=_CLEAN_ANSWER)
            status, _ = harness.post(
                _contract_body(False, input_text=_CLEAN_ANSWER),
                {
                    "Cookie": "session=abc",
                    "X-Session-Id": "s1",
                    "X-Concept-Request-ID": "link-canary-015a",
                    "X-Proxy-Control": "bypass",
                },
            )
            self.assertEqual(status, 200)
            main_headers = cast(dict[str, str], _MainUpstream.recorded[0]["headers"])
            for header in (
                "Cookie",
                "X-Session-Id",
                "X-Concept-Request-ID",
                "X-Proxy-Control",
            ):
                self.assertNotIn(header, main_headers)
        finally:
            harness.close()

    def test_two_turn_client_history(self) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = _json_completed()
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            repaired = json.loads(payload)["output"][0]["content"][0]["text"]
            self.assertEqual(repaired, _CLEAN_ANSWER)
            # Turn 2: the client builds the next request using only the
            # final visible repaired assistant text.
            turn2_body = json.dumps(
                {
                    "model": "m",
                    "input": [
                        {
                            "role": "assistant",
                            "content": [{"type": "input_text", "text": repaired}],
                        },
                        {"role": "user", "content": "Nadaljuj."},
                    ],
                    "store": False,
                    "stream": False,
                },
                separators=(",", ":"),
            ).encode()
            _MainUpstream.source = _json_completed(answer=_CLEAN_ANSWER)
            _FakeUpstream.payload = _review_payload([_prop("t0")])
            status, payload = harness.post(turn2_body)
            self.assertEqual(status, 200)
            self.assertEqual(
                json.loads(payload)["output"][0]["content"][0]["text"], _CLEAN_ANSWER
            )
            main_bodies = [
                cast(bytes, record["body"]) for record in _MainUpstream.recorded
            ]
            self.assertEqual(len(main_bodies), 2)
            self.assertEqual(main_bodies[1].count(repaired.encode()), 1)
            combined = b"".join(main_bodies)
            # No extra draft, reviewer prompt or proposals, no linkage.
            self.assertNotIn(b"batch-v1", combined)
            self.assertNotIn(b"BATCH_INSTRUCTION".lower(), combined)
            # The clean turn-2 answer carries zero candidates.
            self.assertEqual(len(_FakeUpstream.recorded), 1)
        finally:
            harness.close()

    # A5: separated actual usage with explicit unknowns, no carryover,
    # observable without raw logs.

    def test_usage_observer_detailed_usage_and_no_carryover(self) -> None:
        records: list[dict[str, object]] = []
        harness = _Harness(usage_observer=records.append)
        try:
            _MainUpstream.source = _json_completed()
            detailed = {
                "input_tokens": 11,
                "input_tokens_details": {"cached_tokens": 0},
                "output_tokens": 5,
                "output_tokens_details": {"reasoning_tokens": 0},
                "total_tokens": 16,
            }
            _FakeUpstream.payload = _review_payload(
                [_prop("t1"), _prop("t0")], usage=detailed
            )
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(
                records,
                [
                    {
                        "review_calls": 1,
                        "reviewer_usage": {
                            "input_tokens": 11,
                            "output_tokens": 5,
                            "total_tokens": 16,
                        },
                    }
                ],
            )
            # Same proxy instance: a valid clean second answer makes zero
            # review calls; the earlier known usage must not carry over.
            _MainUpstream.source = _json_completed(answer=_CLEAN_ANSWER)
            _FakeUpstream.payload = _review_payload([_prop("t0")])
            status, payload = harness.post(
                _contract_body(False, input_text=_CLEAN_ANSWER)
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, _json_completed(answer=_CLEAN_ANSWER))
            self.assertEqual(len(records), 2)
            self.assertEqual(records[1], {"review_calls": 0, "reviewer_usage": "unknown"})
        finally:
            harness.close()

    def test_usage_absent_reviewer_usage_stays_unknown(self) -> None:
        records: list[dict[str, object]] = []
        harness = _Harness(usage_observer=records.append)
        try:
            _MainUpstream.source = _json_completed()
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertNotIn(b"presenetliv", payload)
            self.assertEqual(
                records, [{"review_calls": 1, "reviewer_usage": "unknown"}]
            )
        finally:
            harness.close()

    def test_usage_observer_failure_changes_nothing(self) -> None:
        def boom(record: dict[str, object]) -> None:
            raise RuntimeError("observer down")

        harness = _Harness(usage_observer=boom)
        try:
            _MainUpstream.source = _json_completed()
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertNotIn(b"presenetliv", payload)
        finally:
            harness.close()

    def test_usage_observer_record_is_content_free(self) -> None:
        records: list[dict[str, object]] = []
        harness = _Harness(usage_observer=records.append)
        try:
            _MainUpstream.source = _json_completed()
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, _ = harness.post(
                _contract_body(False),
                {"X-Concept-Request-ID": "canary-client-id-015a"},
            )
            self.assertEqual(status, 200)
            self.assertTrue(records)
            for record in records:
                self.assertEqual(set(record), {"review_calls", "reviewer_usage"})
            self.assertNotIn(b"canary-client-id-015a", json.dumps(records).encode())
        finally:
            harness.close()

    def test_main_wires_stderr_usage_observer(self) -> None:
        captured: dict[str, object] = {}

        class _ProbeReviewer:
            def __init__(self, *args: object, **kwargs: object) -> None:
                captured["timeout"] = kwargs.get("timeout")

        class _ProbeProxy:
            def __init__(self, *args: object, **kwargs: object) -> None:
                captured["usage_observer"] = kwargs.get("usage_observer")
                raise SystemExit("stop before serve_forever")

        env = {
            "CONCEPT_INDEX": "/tmp/unused.sqlite",
            "CONCEPT_REVIEWER_URL": "http://127.0.0.1:9/v1",
            "CONCEPT_USAGE_OBSERVER": "stderr",
        }
        with mock.patch.dict(os.environ, env), mock.patch.object(
            proxy, "resolve_pandoc_spec", lambda: PandocSpec(binary="/bin/true")
        ), mock.patch.object(proxy, "check_pandoc", lambda spec: None), mock.patch.object(
            proxy, "ResponsesReviewer", _ProbeReviewer
        ), mock.patch.object(proxy, "ConceptProxy", _ProbeProxy), self.assertRaises(
            SystemExit
        ):
            proxy.main()
        observer = captured["usage_observer"]
        self.assertTrue(callable(observer))
        buffer = io.StringIO()
        with redirect_stderr(buffer):
            cast(
                Callable[[dict[str, object]], None], observer
            )({"review_calls": 0, "reviewer_usage": "unknown"})
            cast(
                Callable[[dict[str, object]], None], observer
            )(
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 4,
                        "output_tokens": 2,
                        "total_tokens": 6,
                    },
                }
            )
        lines = buffer.getvalue().splitlines()
        self.assertIn("concept-review-usage calls=0 usage=unknown", lines)
        self.assertIn(
            "concept-review-usage calls=1 usage=input=4,output=2,total=6", lines
        )
        # The bounded stderr record is counts-only: no raw text, no ids.
        self.assertNotIn("canary", buffer.getvalue())


class LogprobsRemovalTests(unittest.TestCase):
    """Order 035-c: always-remove defined API logprobs policy tests."""

    def _msg(self, output: str = TEXT) -> dict[str, object]:
        return {
            "type": "message",
            "id": "m",
            "role": "assistant",
            "status": "completed",
            "output_index": 0,
            "content": [{"type": "output_text", "text": output, "content_index": 0}],
        }

    def _sse_completed_event(self, response: dict[str, object]) -> bytes:
        return (
            '{"type":"response.completed","response":' + json.dumps(response, separators=(",", ":")) + "}"
        ).encode()

    def _json_body(self, part_value: dict[str, object]) -> bytes:
        message = {
            "type": "message",
            "id": "m",
            "role": "assistant",
            "status": "completed",
            "output_index": 0,
            "content": [part_value],
        }
        value = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [message],
        }
        return json.dumps(value, separators=(",", ":")).encode()

    def _expected_json_body(self, text: str) -> dict[str, object]:
        # Independent whole-value oracle (order 035-d R3): the exact
        # expected parsed response after removal/repair, built by hand -
        # never derived from the production normalizer.
        return {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {"type": "output_text", "text": text, "content_index": 0}
                    ],
                }
            ],
        }

    def _sse_events(self, payload: bytes) -> list[dict[str, object]]:
        # Parse every data event of a returned SSE body (test streams
        # carry no [DONE] terminator).
        events: list[dict[str, object]] = []
        for block in payload.decode("utf-8").split("\n\n"):
            for line in block.splitlines():
                if line.startswith("data: "):
                    events.append(json.loads(line[6:]))
        return events

    def test_json_logprobs_null_removed(self) -> None:
        # logprobs: null is removed by presence; response succeeds after a
        # valid aligned two-target keep review (order 035-d R3).
        raw = self._json_body(
            {"type": "output_text", "text": TEXT, "content_index": 0, "logprobs": None}
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(json.loads(payload), self._expected_json_body(TEXT))
        finally:
            harness.close()

    def test_json_logprobs_empty_list_removed(self) -> None:
        # logprobs: [] is removed by presence (valid aligned keep batch).
        raw = self._json_body(
            {"type": "output_text", "text": TEXT, "content_index": 0, "logprobs": []}
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(json.loads(payload), self._expected_json_body(TEXT))
        finally:
            harness.close()

    def test_json_logprobs_populated_removed(self) -> None:
        # logprobs: populated list is removed by presence (valid aligned
        # keep batch).
        raw = self._json_body(
            {
                "type": "output_text",
                "text": TEXT,
                "content_index": 0,
                "logprobs": [
                    {"token": "a", "logprob": -0.1, "start_index": 0, "end_index": 1}
                ],
            }
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(json.loads(payload), self._expected_json_body(TEXT))
        finally:
            harness.close()

    def test_json_logprobs_unexpected_type_removed(self) -> None:
        # logprobs: false (unexpected type) is removed by presence (valid
        # aligned keep batch).
        raw = self._json_body(
            {"type": "output_text", "text": TEXT, "content_index": 0, "logprobs": False}
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(json.loads(payload), self._expected_json_body(TEXT))
        finally:
            harness.close()

    def test_json_logprobs_object_removed(self) -> None:
        # logprobs: object (unexpected type) is removed by presence (valid
        # aligned keep batch).
        raw = self._json_body(
            {
                "type": "output_text",
                "text": TEXT,
                "content_index": 0,
                "logprobs": {"unexpected": "shape"},
            }
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(json.loads(payload), self._expected_json_body(TEXT))
        finally:
            harness.close()

    def test_json_logprobs_zero_removed(self) -> None:
        # logprobs: 0 (number) is removed by presence (valid aligned keep
        # batch; whole-value oracle).
        raw = self._json_body(
            {"type": "output_text", "text": TEXT, "content_index": 0, "logprobs": 0}
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(json.loads(payload), self._expected_json_body(TEXT))
        finally:
            harness.close()

    def test_json_logprobs_string_removed(self) -> None:
        # logprobs: string (unexpected type) is removed by presence (valid
        # aligned keep batch; whole-value oracle).
        raw = self._json_body(
            {
                "type": "output_text",
                "text": TEXT,
                "content_index": 0,
                "logprobs": "unexpected-string",
            }
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(json.loads(payload), self._expected_json_body(TEXT))
        finally:
            harness.close()

    def test_json_other_fields_unchanged_after_removal(self) -> None:
        # Removing logprobs must not alter any other field (valid aligned
        # keep batch; whole-value oracle).
        raw = self._json_body(
            {
                "type": "output_text",
                "text": TEXT,
                "content_index": 0,
                "logprobs": [{"token": "a", "logprob": -1.0}],
            }
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            body = json.loads(payload)
            # All other fields preserved
            self.assertEqual(body["object"], "response")
            self.assertEqual(body["id"], "r")
            self.assertEqual(body["status"], "completed")
            msg = body["output"][0]
            self.assertEqual(msg["type"], "message")
            self.assertEqual(msg["id"], "m")
            self.assertEqual(msg["role"], "assistant")
            self.assertEqual(msg["status"], "completed")
            self.assertEqual(msg["output_index"], 0)
            part = msg["content"][0]
            self.assertEqual(part["type"], "output_text")
            self.assertEqual(part["text"], TEXT)
            self.assertEqual(part["content_index"], 0)
            # logprobs absent
            self.assertNotIn("logprobs", part)
            # Whole independent expected value (no extra/missing keys).
            self.assertEqual(body, self._expected_json_body(TEXT))
        finally:
            harness.close()

    def test_json_no_logprobs_no_edit_byte_identical(self) -> None:
        # No logprobs present and no edit (valid aligned keep batch, one
        # review round trip): output is byte-identical to input.
        raw = self._json_body(
            {"type": "output_text", "text": TEXT, "content_index": 0}
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertEqual(payload, raw)
        finally:
            harness.close()

    def test_json_annotations_still_bypass(self) -> None:
        # Non-empty annotations still cause bypass (policy unchanged).
        raw = self._json_body(
            {
                "type": "output_text",
                "text": TEXT,
                "content_index": 0,
                "annotations": [{"type": "url_citation", "url_index": 0, "start_index": 0, "end_index": 3}],
            }
        )
        self._json_bypass_helper(raw)

    def _json_bypass_helper(self, raw: bytes) -> None:
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertEqual(payload, raw)
        finally:
            harness.close()

    def test_sse_content_part_done_logprobs_removed(self) -> None:
        # Order 035-c: logprobs on a content_part.done part is removed
        # (valid aligned two-target keep batch, one review round trip;
        # whole parsed event values asserted, order 035-d R3).
        part_done = (
            '{"type":"response.content_part.done","item_id":"m",'
            '"part":{"type":"output_text","text":'
            + json.dumps(TEXT)
            + ',"logprobs":[{"token":"x"}]}}'
        ).encode()
        raw = _tc_raw(
            _tc_delta("m", TEXT),
            part_done,
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            self._sse_completed_event(
                {"object": "response", "id": "r", "status": "completed", "output": [self._msg()]}
            ),
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {"type": "response.output_text.delta", "item_id": "m", "delta": TEXT},
                    {
                        "type": "response.content_part.done",
                        "item_id": "m",
                        "part": {"type": "output_text", "text": TEXT},
                    },
                    {
                        "type": "response.output_item.done",
                        "item": {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "content": [{"type": "output_text", "text": TEXT}],
                        },
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "output": [self._msg(TEXT)],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_sse_output_item_done_logprobs_removed(self) -> None:
        # Order 035-c: logprobs on an output_item.done content part is
        # removed (valid aligned keep batch; whole parsed event values
        # asserted).
        item_done = (
            '{"type":"response.output_item.done","output_index":0,'
            '"item":{"type":"message","id":"m","role":"assistant",'
            '"content":[{"type":"output_text","text":'
            + json.dumps(TEXT)
            + ',"logprobs":[{"token":"y"}]}]}}'
        ).encode()
        raw = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            item_done,
            self._sse_completed_event(
                {"object": "response", "id": "r", "status": "completed", "output": [self._msg()]}
            ),
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {"type": "response.output_text.delta", "item_id": "m", "delta": TEXT},
                    {
                        "type": "response.content_part.done",
                        "item_id": "m",
                        "part": {"type": "output_text", "text": TEXT},
                    },
                    {
                        "type": "response.output_item.done",
                        "output_index": 0,
                        "item": {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "content": [{"type": "output_text", "text": TEXT}],
                        },
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "output": [self._msg(TEXT)],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_sse_completed_nested_logprobs_removed(self) -> None:
        # Order 035-c: logprobs in the nested response of a completed event
        # is removed (valid aligned keep batch; whole parsed event values
        # asserted).
        completed = (
            '{"type":"response.completed","response":{"object":"response",'
            '"id":"r","status":"completed","output":'
            '[{"type":"message","id":"m","role":"assistant","status":"completed",'
            '"output_index":0,"content":[{"type":"output_text","text":'
            + json.dumps(TEXT)
            + ',"content_index":0,"logprobs":[{"token":"z"}]}]}]}}'
        ).encode()
        raw = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            completed,
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {"type": "response.output_text.delta", "item_id": "m", "delta": TEXT},
                    {
                        "type": "response.content_part.done",
                        "item_id": "m",
                        "part": {"type": "output_text", "text": TEXT},
                    },
                    {
                        "type": "response.output_item.done",
                        "item": {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "content": [{"type": "output_text", "text": TEXT}],
                        },
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "output": [self._msg(TEXT)],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_sse_logprobs_zero_removed(self) -> None:
        # Order 035-d R3: logprobs 0 (number) on a delta event is removed
        # by presence (valid aligned keep batch; whole parsed event values).
        delta = (
            '{"type":"response.output_text.delta","item_id":"m",'
            '"logprobs":0,"delta":' + json.dumps(TEXT) + "}"
        ).encode()
        raw = _tc_raw(
            delta,
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            self._sse_completed_event(
                {"object": "response", "id": "r", "status": "completed", "output": [self._msg()]}
            ),
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {"type": "response.output_text.delta", "item_id": "m", "delta": TEXT},
                    {
                        "type": "response.content_part.done",
                        "item_id": "m",
                        "part": {"type": "output_text", "text": TEXT},
                    },
                    {
                        "type": "response.output_item.done",
                        "item": {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "content": [{"type": "output_text", "text": TEXT}],
                        },
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "output": [self._msg(TEXT)],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_sse_logprobs_string_removed(self) -> None:
        # Order 035-d R3: logprobs string (unexpected type) on a
        # content_part.done part is removed by presence (valid aligned keep
        # batch; whole parsed event values).
        part_done = (
            '{"type":"response.content_part.done","item_id":"m",'
            '"part":{"type":"output_text","text":'
            + json.dumps(TEXT)
            + ',"logprobs":"unexpected-string"}}'
        ).encode()
        raw = _tc_raw(
            _tc_delta("m", TEXT),
            part_done,
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            self._sse_completed_event(
                {"object": "response", "id": "r", "status": "completed", "output": [self._msg()]}
            ),
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {"type": "response.output_text.delta", "item_id": "m", "delta": TEXT},
                    {
                        "type": "response.content_part.done",
                        "item_id": "m",
                        "part": {"type": "output_text", "text": TEXT},
                    },
                    {
                        "type": "response.output_item.done",
                        "item": {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "content": [{"type": "output_text", "text": TEXT}],
                        },
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "output": [self._msg(TEXT)],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_json_clean_zero_review_control(self) -> None:
        # Order 035-d R3: a TRUE clean zero-review control - the answer has
        # zero detector candidates, so the review endpoint is never called;
        # the populated logprobs are still removed and the whole body is
        # exactly the independent expected value (removal independent of
        # repair).
        raw = self._json_body(
            {
                "type": "output_text",
                "text": _CLEAN_ANSWER,
                "content_index": 0,
                "logprobs": [
                    {"token": "a", "logprob": -0.5, "start_index": 0, "end_index": 1}
                ],
            }
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False, _CLEAN_ANSWER))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(
                json.loads(payload), self._expected_json_body(_CLEAN_ANSWER)
            )
        finally:
            harness.close()

    def test_sse_clean_zero_review_control(self) -> None:
        # Order 035-d R3: TRUE clean zero-review control through the real
        # SSE chain - zero detector candidates, zero review calls, logprobs
        # removed from every copy, every parsed event exactly the
        # independent expected value.
        delta = (
            '{"type":"response.output_text.delta","item_id":"m",'
            '"logprobs":[{"token":"a"}],"delta":' + json.dumps(_CLEAN_ANSWER) + "}"
        ).encode()
        part_done = (
            '{"type":"response.content_part.done","item_id":"m",'
            '"part":{"type":"output_text","text":'
            + json.dumps(_CLEAN_ANSWER)
            + ',"logprobs":[{"token":"b"}]}}'
        ).encode()
        item_done = (
            '{"type":"response.output_item.done","item":{"type":"message","id":"m",'
            '"role":"assistant","status":"completed","content":['
            '{"type":"output_text","text":' + json.dumps(_CLEAN_ANSWER)
            + ',"logprobs":[{"token":"c"}]}]}}'
        ).encode()
        completed = (
            '{"type":"response.completed","response":{"object":"response",'
            '"id":"r","status":"completed","output":'
            '[{"type":"message","id":"m","role":"assistant","status":"completed",'
            '"output_index":0,"content":[{"type":"output_text","text":'
            + json.dumps(_CLEAN_ANSWER)
            + ',"content_index":0,"logprobs":[{"token":"d"}]}]}]}}'
        ).encode()
        raw = _tc_raw(delta, part_done, item_done, completed)
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(True, _CLEAN_ANSWER))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {
                        "type": "response.output_text.delta",
                        "item_id": "m",
                        "delta": _CLEAN_ANSWER,
                    },
                    {
                        "type": "response.content_part.done",
                        "item_id": "m",
                        "part": {"type": "output_text", "text": _CLEAN_ANSWER},
                    },
                    {
                        "type": "response.output_item.done",
                        "item": {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "content": [{"type": "output_text", "text": _CLEAN_ANSWER}],
                        },
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "output": [self._msg(_CLEAN_ANSWER)],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_json_accepted_edit_one_review_control(self) -> None:
        # Order 035-d R3: accepted-edit one-review control - valid aligned
        # two-target batch, t0 accepted (replacement "tako"), t1 kept:
        # exactly one review round trip, only the approved span changes,
        # the unapproved occurrence stays exact, logprobs removed, whole
        # body exactly the independent expected value.
        raw = self._json_body(
            {
                "type": "output_text",
                "text": TEXT,
                "content_index": 0,
                "logprobs": [
                    {"token": "a", "logprob": -0.1, "start_index": 0, "end_index": 1}
                ],
            }
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_EDIT_T0_KEEP_T1)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(
                json.loads(payload), self._expected_json_body(_TEXT_EDITED_T0)
            )
        finally:
            harness.close()

    def test_sse_accepted_edit_one_review_control(self) -> None:
        # Order 035-d R3: accepted-edit one-review control through the real
        # SSE chain - t0 accepted, t1 kept: exactly one review round trip,
        # every established consistent copy carries the repaired answer,
        # the unapproved occurrence stays exact in all copies, logprobs
        # removed from every location, all parsed events exactly the
        # independent expected values.
        delta = (
            '{"type":"response.output_text.delta","item_id":"m",'
            '"logprobs":[{"token":"a"}],"delta":' + json.dumps(TEXT) + "}"
        ).encode()
        part_done = (
            '{"type":"response.content_part.done","item_id":"m",'
            '"part":{"type":"output_text","text":'
            + json.dumps(TEXT)
            + ',"logprobs":[{"token":"b"}]}}'
        ).encode()
        item_done = (
            '{"type":"response.output_item.done","item":{"type":"message","id":"m",'
            '"role":"assistant","status":"completed","content":['
            '{"type":"output_text","text":' + json.dumps(TEXT)
            + ',"logprobs":[{"token":"c"}]}]}}'
        ).encode()
        completed = (
            '{"type":"response.completed","response":{"object":"response",'
            '"id":"r","status":"completed","output":'
            '[{"type":"message","id":"m","role":"assistant","status":"completed",'
            '"output_index":0,"content":[{"type":"output_text","text":'
            + json.dumps(TEXT)
            + ',"content_index":0,"logprobs":[{"token":"d"}]}]}]}}'
        ).encode()
        raw = _tc_raw(delta, part_done, item_done, completed)
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_EDIT_T0_KEEP_T1)
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {
                        "type": "response.output_text.delta",
                        "item_id": "m",
                        "delta": _TEXT_EDITED_T0,
                    },
                    {
                        "type": "response.content_part.done",
                        "item_id": "m",
                        "part": {"type": "output_text", "text": _TEXT_EDITED_T0},
                    },
                    {
                        "type": "response.output_item.done",
                        "item": {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "content": [{"type": "output_text", "text": _TEXT_EDITED_T0}],
                        },
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "output": [self._msg(_TEXT_EDITED_T0)],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            harness.close()

    # --- Order 035-d R3 (Root clarification): compact parameterized
    # actual-HTTP value matrix: all eight defined values in JSON/SSE
    # through both the genuine clean zero-review path and the
    # accepted-edit one-review path, with valid aligned two-target
    # proposals, actual usage/IDs/completion and unrelated same-named
    # metadata echo keys preserved, and exact full independent expected
    # parsed values asserted (never the production normalizer as
    # oracle).

    def _matrix_label(self, logprobs: object) -> str:
        return "absent" if logprobs is _ABSENT else repr(logprobs)

    def _matrix_json_body(self, text: str, logprobs: object) -> bytes:
        part: dict[str, object] = {"type": "output_text", "text": text, "content_index": 0}
        if logprobs is not _ABSENT:
            part["logprobs"] = logprobs
        message = {
            "type": "message",
            "id": "m",
            "role": "assistant",
            "status": "completed",
            "output_index": 0,
            "content": [part],
        }
        return json.dumps(
            {
                "object": "response",
                "id": "resp-matrix",
                "status": "completed",
                "created_at": 1700000000,
                "completed_at": 1700000001,
                "error": None,
                "usage": dict(_MATRIX_USAGE),
                "metadata": dict(_MATRIX_METADATA),
                "output": [message],
            },
            separators=(",", ":"),
        ).encode()

    def _expected_matrix_json(self, text: str) -> dict[str, object]:
        # Independent whole-value oracle: the defined logprobs never
        # appear in the output part; usage/IDs/completion and the
        # same-named metadata echo are exact.
        return {
            "object": "response",
            "id": "resp-matrix",
            "status": "completed",
            "created_at": 1700000000,
            "completed_at": 1700000001,
            "error": None,
            "usage": dict(_MATRIX_USAGE),
            "metadata": dict(_MATRIX_METADATA),
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {"type": "output_text", "text": text, "content_index": 0}
                    ],
                }
            ],
        }

    def _matrix_sse_stream(self, text: str, logprobs: object) -> bytes:
        part: dict[str, object] = {"type": "output_text", "text": text}
        if logprobs is not _ABSENT:
            part["logprobs"] = logprobs
        delta: dict[str, object] = {
            "type": "response.output_text.delta",
            "item_id": "m",
            "delta": text,
        }
        if logprobs is not _ABSENT:
            delta["logprobs"] = logprobs
        events = (
            delta,
            {
                "type": "response.content_part.done",
                "item_id": "m",
                "part": dict(part),
            },
            {
                "type": "response.output_item.done",
                "item": {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "content": [dict(part)],
                },
            },
            {
                "type": "response.completed",
                "response": {
                    "object": "response",
                    "id": "resp-matrix",
                    "status": "completed",
                    "created_at": 1700000000,
                    "completed_at": 1700000001,
                    "usage": dict(_MATRIX_USAGE),
                    "metadata": dict(_MATRIX_METADATA),
                    "output": [
                        {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "output_index": 0,
                            "content": [dict(part)],
                        }
                    ],
                },
            },
        )
        return _tc_raw(
            *[json.dumps(event, separators=(",", ":")).encode() for event in events]
        )

    def _expected_matrix_sse(self, text: str) -> list[dict[str, object]]:
        # Independent whole-value oracle for the four established
        # consistent copies: defined logprobs never appear; usage/IDs/
        # completion and the same-named metadata echo are exact.
        part = {"type": "output_text", "text": text}
        return [
            {"type": "response.output_text.delta", "item_id": "m", "delta": text},
            {"type": "response.content_part.done", "item_id": "m", "part": dict(part)},
            {
                "type": "response.output_item.done",
                "item": {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "content": [dict(part)],
                },
            },
            {
                "type": "response.completed",
                "response": {
                    "object": "response",
                    "id": "resp-matrix",
                    "status": "completed",
                    "created_at": 1700000000,
                    "completed_at": 1700000001,
                    "usage": dict(_MATRIX_USAGE),
                    "metadata": dict(_MATRIX_METADATA),
                    "output": [
                        {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "output_index": 0,
                            "content": [dict(part)],
                        }
                    ],
                },
            },
        ]

    def test_json_value_matrix_clean_and_edit(self) -> None:
        # JSON: all eight values x (clean zero-review, accepted-edit
        # one-review) through the real HTTP chain.
        for logprobs in _LOGPROBS_MATRIX_VALUES:
            with self.subTest(value=self._matrix_label(logprobs), mode="clean-zero-review"):
                harness = _Harness()
                try:
                    raw = self._matrix_json_body(_CLEAN_ANSWER, logprobs)
                    _MainUpstream.source = raw
                    _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
                    status, payload = harness.post(_contract_body(False, _CLEAN_ANSWER))
                    self.assertEqual(status, 200)
                    self.assertEqual(len(_FakeUpstream.recorded), 0)
                    if logprobs is _ABSENT:
                        # No removal and no edit: exact raw bytes.
                        self.assertEqual(payload, raw)
                    self.assertEqual(
                        json.loads(payload), self._expected_matrix_json(_CLEAN_ANSWER)
                    )
                finally:
                    harness.close()
            with self.subTest(value=self._matrix_label(logprobs), mode="accepted-edit-one-review"):
                harness = _Harness()
                try:
                    raw = self._matrix_json_body(TEXT, logprobs)
                    _MainUpstream.source = raw
                    _FakeUpstream.payload = _review_payload(_EDIT_T0_KEEP_T1, usage=_REVIEW_USAGE)
                    status, payload = harness.post(_contract_body(False))
                    self.assertEqual(status, 200)
                    self.assertEqual(len(_FakeUpstream.recorded), 1)
                    self.assertEqual(
                        json.loads(payload), self._expected_matrix_json(_TEXT_EDITED_T0)
                    )
                finally:
                    harness.close()

    def test_sse_value_matrix_clean_and_edit(self) -> None:
        # SSE: all eight values x (clean zero-review, accepted-edit
        # one-review) through the real HTTP chain; all four consistent
        # copies asserted as whole parsed events.
        for logprobs in _LOGPROBS_MATRIX_VALUES:
            with self.subTest(value=self._matrix_label(logprobs), mode="clean-zero-review"):
                harness = _Harness()
                try:
                    raw = self._matrix_sse_stream(_CLEAN_ANSWER, logprobs)
                    _MainUpstream.content_type = "text/event-stream"
                    _MainUpstream.source = raw
                    _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
                    status, payload = harness.post(_contract_body(True, _CLEAN_ANSWER))
                    self.assertEqual(status, 200)
                    self.assertEqual(len(_FakeUpstream.recorded), 0)
                    if logprobs is _ABSENT:
                        # No removal and no edit: exact raw bytes.
                        self.assertEqual(payload, raw)
                    self.assertEqual(
                        self._sse_events(payload), self._expected_matrix_sse(_CLEAN_ANSWER)
                    )
                finally:
                    _MainUpstream.content_type = "application/json"
                    harness.close()
            with self.subTest(value=self._matrix_label(logprobs), mode="accepted-edit-one-review"):
                harness = _Harness()
                try:
                    raw = self._matrix_sse_stream(TEXT, logprobs)
                    _MainUpstream.content_type = "text/event-stream"
                    _MainUpstream.source = raw
                    _FakeUpstream.payload = _review_payload(_EDIT_T0_KEEP_T1, usage=_REVIEW_USAGE)
                    status, payload = harness.post(_contract_body(True))
                    self.assertEqual(status, 200)
                    self.assertEqual(len(_FakeUpstream.recorded), 1)
                    self.assertEqual(
                        self._sse_events(payload), self._expected_matrix_sse(_TEXT_EDITED_T0)
                    )
                finally:
                    _MainUpstream.content_type = "application/json"
                    harness.close()

    def test_json_ineligible_envelope_logprobs_still_removed(self) -> None:
        # Even an ineligible envelope (incomplete status) has logprobs removed.
        value = {
            "object": "response",
            "id": "r",
            "status": "in_progress",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "in_progress",
                    "output_index": 0,
                    "content": [
                        {
                            "type": "output_text",
                            "text": TEXT,
                            "content_index": 0,
                            "logprobs": [{"token": "a"}],
                        }
                    ],
                }
            ],
        }
        raw = json.dumps(value, separators=(",", ":")).encode()
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            # No review call (ineligible)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            # But logprobs is still removed from the wire data
            self.assertNotIn(b"logprobs", payload)
            body = json.loads(payload)
            self.assertEqual(body["status"], "in_progress")
            self.assertEqual(body["output"][0]["content"][0]["text"], TEXT)
        finally:
            harness.close()


    def test_json_non200_logprobs_removed(self) -> None:
        # R3: non-200 recognized Responses object has logprobs removed.
        value = {
            "object": "response",
            "id": "r",
            "status": "failed",
            "error": {"code": "server_error"},
            "output": [
                {
                    "type": "message", "id": "m", "role": "assistant",
                    "status": "incomplete", "output_index": 0,
                    "content": [
                        {"type": "output_text", "text": "partial", "content_index": 0,
                         "logprobs": [{"token": "x"}]}
                    ],
                }
            ],
        }
        raw = json.dumps(value, separators=(",", ":")).encode()
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _MainUpstream.status = 503
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 503)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertNotIn(b"logprobs", payload)
            body = json.loads(payload)
            self.assertEqual(body["status"], "failed")
            self.assertEqual(body["error"]["code"], "server_error")
            self.assertEqual(body["output"][0]["content"][0]["text"], "partial")
        finally:
            _MainUpstream.status = 200
            harness.close()

    def test_sse_non200_logprobs_removed(self) -> None:
        # R3: SSE non-200 with well-formed completed snapshot has logprobs removed.
        completed = (
            '{"type":"response.completed","response":{"object":"response",'
            '"id":"r","status":"incomplete","incomplete_details":{"reason":"max_output_tokens"},'
            '"output":'
            '[{"type":"message","id":"m","role":"assistant","status":"incomplete",'
            '"output_index":0,"content":[{"type":"output_text","text":"partial",'
            '"content_index":0,"logprobs":[{"token":"x"}]}]}]}}'
        ).encode()
        raw = _tc_raw(
            _tc_delta("m", "partial"),
            completed,
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _MainUpstream.status = 503
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 503)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertNotIn(b"logprobs", payload)
            self.assertIn(b"partial", payload)
        finally:
            _MainUpstream.status = 200
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_json_lone_surrogate_in_answer(self) -> None:
        # R6: escaped lone surrogate in answer text does not cause 502.
        # \ud800 is a valid JSON escape for a lone surrogate. Zero detector
        # candidates: a true clean zero-review control (order 035-d R3).
        value = {
            "object": "response", "id": "r", "status": "completed",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0,
                 "content": [
                     {"type": "output_text",
                      "text": "abc\ud800def",
                      "content_index": 0,
                      "logprobs": [{"token": "x"}]}
                 ]}
            ],
        }
        # Build raw JSON with the escaped surrogate
        raw = (
            b'{"object":"response","id":"r","status":"completed","output":'
            b'[{"type":"message","id":"m","role":"assistant","status":"completed",'
            b'"output_index":0,"content":[{"type":"output_text","text":"abc\ud800def",'
            b'"content_index":0,"logprobs":[{"token":"x"}]}]}]}'
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertNotIn(b"logprobs", payload)
            # The answer text must be preserved (lone surrogate intact)
            body = json.loads(payload)
            self.assertEqual(body["output"][0]["content"][0]["text"], "abc\ud800def")
            # Whole expected value: removal only, surrogate preserved.
            expected = self._expected_json_body("abc\ud800def")
            self.assertEqual(body, expected)
        finally:
            harness.close()

    def test_json_lone_surrogate_in_metadata(self) -> None:
        # R6: escaped lone surrogate in opaque metadata is preserved
        # (true clean zero-review control: zero-candidate answer; metadata
        # echo never scanned).
        raw = (
            b'{"object":"response","id":"r","status":"completed","metadata":{"k":"x\ud800y"},'
            b'"output":[{"type":"message","id":"m","role":"assistant","status":"completed",'
            b'"output_index":0,"content":[{"type":"output_text","text":"To je tako zapisano, to je tako zapisano.",'
            b'"content_index":0,"logprobs":null}]}]}'
        )
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertNotIn(b"logprobs", payload)
            body = json.loads(payload)
            self.assertEqual(body["metadata"]["k"], "x\ud800y")
            self.assertEqual(body["output"][0]["content"][0]["text"], _CLEAN_ANSWER)
            self.assertEqual(
                body,
                {
                    "object": "response",
                    "id": "r",
                    "status": "completed",
                    "metadata": {"k": "x\ud800y"},
                    "output": [
                        {
                            "type": "message",
                            "id": "m",
                            "role": "assistant",
                            "status": "completed",
                            "output_index": 0,
                            "content": [
                                {"type": "output_text", "text": _CLEAN_ANSWER, "content_index": 0}
                            ],
                        }
                    ],
                },
            )
        finally:
            harness.close()

    def test_sse_output_item_two_parts_logprobs_removed(self) -> None:
        # R3: SSE output_item.done with TWO output_text parts - both lose logprobs.
        item_done = (
            '{"type":"response.output_item.done","output_index":0,'
            '"item":{"type":"message","id":"m","role":"assistant",'
            '"content":['
            '{"type":"output_text","text":' + json.dumps(TEXT) +
            ',"logprobs":[{"token":"a"}]},'
            '{"type":"output_text","text":"second","logprobs":[{"token":"b"}]}'
            ']}}'
        ).encode()
        # This is unrepairable (two content parts), so it bypasses with 0 review.
        # But both logprobs must still be removed.
        raw = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            item_done,
            self._sse_completed_event(
                {"object": "response", "id": "r", "status": "completed",
                 "output": [self._msg()]}
            ),
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(
                [_prop("t0", keep=True, replacement=None)]
            )
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            # Both logprobs removed
            self.assertNotIn(b"logprobs", payload)
        finally:
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_json_metadata_only_not_text_edit(self) -> None:
        # R4: metadata-only change (logprobs removed) is NOT a text edit.
        # The changed flag must be False.
        from proxy import transform_json
        raw = self._json_body(
            {"type": "output_text", "text": TEXT, "content_index": 0,
             "logprobs": [{"token": "x"}]}
        )
        result_bytes, changed = transform_json(raw, lambda t: t)
        # logprobs removed, but no text edit
        self.assertFalse(changed, "metadata-only must not set changed=True")
        self.assertNotIn(b"logprobs", result_bytes)
        body = json.loads(result_bytes)
        self.assertEqual(body["output"][0]["content"][0]["text"], TEXT)

    def test_sse_metadata_only_not_text_edit(self) -> None:
        # R4: SSE metadata-only change is NOT a text edit.
        from proxy import transform_sse
        delta = (
            '{"type":"response.output_text.delta","item_id":"m",'
            '"logprobs":[{"token":"t"}],"delta":' + json.dumps(TEXT) + "}"
        ).encode()
        raw = _tc_raw(
            delta,
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            self._sse_completed_event(
                {"object": "response", "id": "r", "status": "completed",
                 "output": [self._msg()]}
            ),
        )
        result_bytes, changed = transform_sse(raw, lambda t: t)
        self.assertFalse(changed, "metadata-only SSE must not set changed=True")
        self.assertNotIn(b"logprobs", result_bytes)


    def test_non200_json_body_with_stream_true(self) -> None:
        # R3: stream=true request receives application/json 503 body.
        # Normalization selects by ACTUAL content type, not request.stream.
        value = {
            "object": "response", "id": "r", "status": "failed",
            "error": {"code": "overloaded"},
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "incomplete", "output_index": 0,
                 "content": [{"type": "output_text", "text": "x",
                              "content_index": 0, "logprobs": None}]}
            ],
        }
        raw = json.dumps(value, separators=(",", ":")).encode()
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _MainUpstream.status = 503
            _MainUpstream.content_type = "application/json"
            status, payload = harness.post(_contract_body(True))  # stream=True!
            self.assertEqual(status, 503)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            _MainUpstream.status = 200
            _MainUpstream.content_type = "text/event-stream"
            harness.close()

    def test_non200_sse_body_with_stream_false(self) -> None:
        # R3: stream=false request receives text/event-stream 503 body.
        # Normalization selects by ACTUAL content type, not request.stream.
        completed = (
            '{"type":"response.completed","response":{"object":"response",'
            '"id":"r","status":"incomplete",'
            '"output":[{"type":"message","id":"m","role":"assistant",'
            '"status":"incomplete","output_index":0,"content":'
            '[{"type":"output_text","text":"partial","content_index":0,'
            '"logprobs":null}]}]}}'
        ).encode()
        raw = _tc_raw(completed)
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _MainUpstream.status = 503
            _MainUpstream.content_type = "text/event-stream"
            status, payload = harness.post(_contract_body(False))  # stream=False!
            self.assertEqual(status, 503)
            self.assertNotIn(b"logprobs", payload)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            _MainUpstream.status = 200
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_non200_huge_integer_body_preserved(self) -> None:
        # R3: non-200 body with JSON decoder overflow (huge integer) is
        # returned raw unchanged (malformed error-body semantics preserved).
        huge_int = "9" * 4500
        raw = ('{"opaque_integer":' + huge_int + "}").encode()
        harness = _Harness()
        try:
            _MainUpstream.source = raw
            _MainUpstream.status = 503
            _MainUpstream.content_type = "application/json"
            status, payload = harness.post(_contract_body(False))
            self.assertEqual(status, 503)
            self.assertEqual(payload, raw)  # byte-identical
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
            _MainUpstream.status = 200
            harness.close()

    def test_sse_lone_surrogate_in_completed_answer(self) -> None:
        # R6: SSE completed snapshot with escaped lone surrogate in answer
        # text and logprobs:null. Expected 200, surrogate preserved,
        # logprobs gone. Zero detector candidates: clean zero-review
        # control (order 035-d R3).
        completed = (
            b'{"type":"response.completed","response":{"object":"response",'
            b'"id":"r","status":"completed",'
            b'"output":[{"type":"message","id":"m","role":"assistant",'
            b'"status":"completed","output_index":0,"content":'
            b'[{"type":"output_text","text":"abc\ud800def",'
            b'"content_index":0,"logprobs":null}]}]}}'
        )
        raw = _tc_raw(
            _tc_delta("m", "abc\ud800def"),
            completed,
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {
                        "type": "response.output_text.delta",
                        "item_id": "m",
                        "delta": "abc\ud800def",
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "output": [
                                {
                                    "type": "message",
                                    "id": "m",
                                    "role": "assistant",
                                    "status": "completed",
                                    "output_index": 0,
                                    "content": [
                                        {
                                            "type": "output_text",
                                            "text": "abc\ud800def",
                                            "content_index": 0,
                                        }
                                    ],
                                }
                            ],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            harness.close()

    def test_sse_lone_surrogate_in_metadata(self) -> None:
        # R6: SSE completed snapshot with escaped lone surrogate in metadata
        # (true clean zero-review control: zero-candidate answer; metadata
        # echo never scanned).
        completed = (
            b'{"type":"response.completed","response":{"object":"response",'
            b'"id":"r","status":"completed","metadata":{"k":"x\ud800y"},'
            b'"output":[{"type":"message","id":"m","role":"assistant",'
            b'"status":"completed","output_index":0,"content":'
            b'[{"type":"output_text","text":"To je tako zapisano, to je tako zapisano.","content_index":0,'
            b'"logprobs":null}]}]}}'
        )
        raw = _tc_raw(
            _tc_delta("m", _CLEAN_ANSWER),
            completed,
        )
        harness = _Harness()
        try:
            _MainUpstream.content_type = "text/event-stream"
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload(_KEEP_BOTH)
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertNotIn(b"logprobs", payload)
            events = self._sse_events(payload)
            self.assertEqual(
                events,
                [
                    {
                        "type": "response.output_text.delta",
                        "item_id": "m",
                        "delta": _CLEAN_ANSWER,
                    },
                    {
                        "type": "response.completed",
                        "response": {
                            "object": "response",
                            "id": "r",
                            "status": "completed",
                            "metadata": {"k": "x\ud800y"},
                            "output": [
                                {
                                    "type": "message",
                                    "id": "m",
                                    "role": "assistant",
                                    "status": "completed",
                                    "output_index": 0,
                                    "content": [
                                        {
                                            "type": "output_text",
                                            "text": _CLEAN_ANSWER,
                                            "content_index": 0,
                                        }
                                    ],
                                }
                            ],
                        },
                    },
                ],
            )
        finally:
            _MainUpstream.content_type = "application/json"
            harness.close()


if __name__ == "__main__":
    unittest.main()


class LogprobsLocationMatrixTests(unittest.TestCase):
    """Order 035-d R4: compact direct-level typed-location/all-copy
    matrix supplementing the actual-HTTP proofs (same production
    transform/normalize functions, identity repair, no engine/HTTP).
    Every recognized location across the six lifecycle snapshots and the
    four stream event kinds is removed with changed False; every
    unrecognized lookalike and echo is byte-identical; ordinary UTF-8,
    escaped lone surrogates, raw identity and SSE framing semantics are
    preserved."""

    def _snapshot(self, etype: str, status: str, extra: dict[str, object] | None = None) -> bytes:
        response: dict[str, object] = {
            "object": "response",
            "id": "r",
            "status": status,
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {
                            "type": "output_text",
                            "text": TEXT,
                            "content_index": 0,
                            "logprobs": [{"token": "a", "logprob": -1.0}],
                        }
                    ],
                }
            ],
        }
        if extra:
            response.update(extra)
        return _tc_raw(
            json.dumps({"type": etype, "response": response}, separators=(",", ":")).encode()
        )

    def _events(self, payload: bytes) -> list[dict[str, object]]:
        events: list[dict[str, object]] = []
        for block in payload.decode("utf-8").split("\n\n"):
            for line in block.splitlines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        continue
                    events.append(json.loads(data))
        return events

    def test_lifecycle_snapshots_all_removed(self) -> None:
        # All six lifecycle snapshots lose the nested logprobs; every other
        # field (status, error, incomplete_details, ids, text) is preserved
        # and the changed flag stays False.
        from proxy import transform_sse

        cases: list[tuple[str, str, dict[str, object]]] = [
            ("response.created", "created", {}),
            ("response.in_progress", "in_progress", {}),
            ("response.completed", "completed", {}),
            (
                "response.incomplete",
                "incomplete",
                {"incomplete_details": {"reason": "max_output_tokens"}},
            ),
            ("response.failed", "failed", {"error": {"code": "server_error"}}),
            ("response.queued", "queued", {}),
        ]
        for etype, status, extra in cases:
            with self.subTest(lifecycle=etype):
                raw = self._snapshot(etype, status, extra)
                result, changed = transform_sse(raw, lambda t: t)
                self.assertFalse(changed, etype)
                event = self._events(result)[0]
                self.assertEqual(event["type"], etype, etype)
                response = cast(dict[str, object], event["response"])
                self.assertEqual(response["status"], status, etype)
                self.assertEqual(response["id"], "r", etype)
                part = cast(dict[str, object], response["output"][0]["content"][0])  # type: ignore[index]
                self.assertNotIn("logprobs", part, etype)
                self.assertEqual(part["text"], TEXT, etype)
                for key, value in extra.items():
                    self.assertEqual(response[key], value, etype)

    def test_stream_event_locations_removed(self) -> None:
        # delta / output_text.done / content_part.added / content_part.done
        # / output_item.added / output_item.done: each location is removed
        # in an otherwise bypassing stream with changed False.
        from proxy import transform_sse

        fixtures: dict[str, bytes] = {
            "delta": _tc_raw(
                (
                    '{"type":"response.output_text.delta","item_id":"m",'
                    '"logprobs":[{"token":"a"}],"delta":' + json.dumps(TEXT) + "}"
                ).encode()
            ),
            "text_done": _tc_raw(
                (
                    '{"type":"response.output_text.done","item_id":"m",'
                    '"logprobs":[{"token":"a"}],"text":' + json.dumps(TEXT) + "}"
                ).encode()
            ),
            "part_added": _tc_raw(
                (
                    '{"type":"response.content_part.added","item_id":"m",'
                    '"part":{"type":"output_text","text":' + json.dumps(TEXT)
                    + ',"logprobs":[{"token":"a"}]}}'
                ).encode()
            ),
            "part_done": _tc_raw(
                (
                    '{"type":"response.content_part.done","item_id":"m",'
                    '"part":{"type":"output_text","text":' + json.dumps(TEXT)
                    + ',"logprobs":[{"token":"a"}]}}'
                ).encode()
            ),
            "item_added": _tc_raw(
                (
                    '{"type":"response.output_item.added","item":{"type":"message","id":"m",'
                    '"role":"assistant","content":[{"type":"output_text","text":'
                    + json.dumps(TEXT) + ',"logprobs":[{"token":"a"}]}]}}'
                ).encode()
            ),
            "item_done": _tc_raw(
                (
                    '{"type":"response.output_item.done","item":{"type":"message","id":"m",'
                    '"role":"assistant","content":[{"type":"output_text","text":'
                    + json.dumps(TEXT) + ',"logprobs":[{"token":"a"}]}]}}'
                ).encode()
            ),
        }
        for name, raw in fixtures.items():
            with self.subTest(location=name):
                result, changed = transform_sse(raw, lambda t: t)
                self.assertFalse(changed, name)
                self.assertNotIn(b"logprobs", result, name)
                self.assertIn(TEXT.encode(), result, name)

    def test_multiple_messages_and_parts_removed(self) -> None:
        # Otherwise unrepairable responses still lose every recognized
        # logprobs: two JSON message items, and one SSE item with two
        # output_text parts.
        from proxy import transform_json, transform_sse

        value = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m1",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {
                            "type": "output_text",
                            "text": "one",
                            "content_index": 0,
                            "logprobs": [{"token": "a"}],
                        }
                    ],
                },
                {
                    "type": "message",
                    "id": "m2",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 1,
                    "content": [
                        {
                            "type": "output_text",
                            "text": "two",
                            "content_index": 0,
                            "logprobs": [{"token": "b"}],
                        }
                    ],
                },
            ],
        }
        raw = json.dumps(value, separators=(",", ":")).encode()
        result, changed = transform_json(raw, lambda t: t)
        self.assertFalse(changed)
        body = json.loads(result)
        parts = [cast(dict[str, object], m["content"][0]) for m in body["output"]]  # type: ignore[index]
        for part in parts:
            self.assertNotIn("logprobs", part)
        self.assertEqual([part["text"] for part in parts], ["one", "two"])
        self.assertEqual(
            [cast(dict[str, object], m)["id"] for m in body["output"]],  # type: ignore[index]
            ["m1", "m2"],
        )

        item_done = _tc_raw(
            (
                '{"type":"response.output_item.done","item":{"type":"message","id":"m",'
                '"role":"assistant","content":['
                '{"type":"output_text","text":"one","logprobs":[{"token":"a"}]},'
                '{"type":"output_text","text":"two","logprobs":[{"token":"b"}]}'
                "]}}"
            ).encode()
        )
        result_sse, changed_sse = transform_sse(item_done, lambda t: t)
        self.assertFalse(changed_sse)
        self.assertNotIn(b"logprobs", result_sse)
        self.assertIn(b"one", result_sse)
        self.assertIn(b"two", result_sse)

    def test_unknown_and_echo_locations_unchanged(self) -> None:
        # No recognized location -> byte-identical passthrough, changed
        # False: unknown event types, nested lookalikes, reasoning/tool
        # items, refusal and user input_text parts, and the envelope
        # metadata echo are never scanned.
        from proxy import transform_json, transform_sse

        fixtures: dict[str, bytes] = {
            "unknown_event": _tc_raw(
                b'{"type":"response.custom.event","data":{"logprobs":[1]},"delta":"x"}'
            ),
            "nested_lookalike": _tc_raw(
                (
                    '{"type":"response.output_text.delta","item_id":"m","delta":'
                    + json.dumps(TEXT)
                    + ',"data":{"logprobs":[1]}}'
                ).encode()
            ),
            "reasoning_item": _tc_raw(
                b'{"type":"response.output_item.done","item":{"type":"reasoning","id":"r1",'
                b'"status":"completed","summary":[{"type":"summary_text","text":"thinking",'
                b'"logprobs":[1]}]}}'
            ),
            "tool_item": _tc_raw(
                b'{"type":"response.output_item.done","item":{"type":"tool_call","id":"t1",'
                b'"status":"completed","call_id":"c1","arguments":"{}","logprobs":[1]}}'
            ),
            "refusal_part": _tc_raw(
                b'{"type":"response.output_item.done","item":{"type":"message","id":"m",'
                b'"role":"assistant","content":[{"type":"refusal","refusal":"no",'
                b'"logprobs":[1]}]}}'
            ),
            "user_input_part": _tc_raw(
                b'{"type":"response.output_item.done","item":{"type":"message","id":"m",'
                b'"role":"user","content":[{"type":"input_text","text":"echo",'
                b'"logprobs":[1]}]}}'
            ),
        }
        for name, raw in fixtures.items():
            with self.subTest(echo=name):
                result, changed = transform_sse(raw, lambda t: t)
                self.assertFalse(changed, name)
                self.assertEqual(result, raw, name)

        metadata_echo = (
            b'{"object":"response","id":"r","status":"completed",'
            b'"metadata":{"logprobs":[1]},"output":[{"type":"message","id":"m",'
            b'"role":"assistant","status":"completed","output_index":0,'
            b'"content":[{"type":"output_text","text":"plain prose here",'
            b'"content_index":0}]}]}'
        )
        result, changed = transform_json(metadata_echo, lambda t: t)
        self.assertFalse(changed)
        self.assertEqual(result, metadata_echo)

    def test_ordinary_utf8_and_lone_surrogates(self) -> None:
        # Ordinary UTF-8 is preserved exactly (not re-escaped) and escaped
        # lone surrogates decode to actual unpaired values that survive
        # removal (JSON and SSE).  The fixtures decode to real unpaired
        # surrogate code points, never literal backslash text.
        from proxy import transform_json, transform_sse

        utf8_text = "\u010d\u0161teka \u017eivi \u010dlove\u010d"
        value = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {
                            "type": "output_text",
                            "text": utf8_text,
                            "content_index": 0,
                            "logprobs": [{"token": "a"}],
                        }
                    ],
                }
            ],
        }
        raw = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()
        result, changed = transform_json(raw, lambda t: t)
        self.assertFalse(changed)
        body = json.loads(result)
        part = cast(dict[str, object], body["output"][0]["content"][0])  # type: ignore[index]
        self.assertEqual(part["text"], utf8_text)
        self.assertNotIn("logprobs", part)
        self.assertIn(utf8_text.encode("utf-8"), result)

        surr_text = "abc\ud800def"
        surr_value = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {
                            "type": "output_text",
                            "text": surr_text,
                            "content_index": 0,
                            "logprobs": None,
                        }
                    ],
                }
            ],
        }
        raw = json.dumps(surr_value, ensure_ascii=True, separators=(",", ":")).encode()
        result, changed = transform_json(raw, lambda t: t)
        self.assertFalse(changed)
        body = json.loads(result)
        part = cast(dict[str, object], body["output"][0]["content"][0])  # type: ignore[index]
        self.assertEqual(part["text"], surr_text)
        self.assertNotIn("logprobs", part)

        surr_completed = (
            b'{"type":"response.completed","response":{"object":"response",'
            b'"id":"r","status":"completed","output":'
            b'[{"type":"message","id":"m","role":"assistant",'
            b'"status":"completed","output_index":0,"content":'
            b'[{"type":"output_text","text":"abc\ud800def",'
            b'"content_index":0,"logprobs":null}]}]}}'
        )
        raw_sse = _tc_raw(_tc_delta("m", "abc\ud800def"), surr_completed)
        result_sse, changed_sse = transform_sse(raw_sse, lambda t: t)
        self.assertFalse(changed_sse)
        self.assertNotIn(b"logprobs", result_sse)
        events = self._events(result_sse)
        completed = cast(dict[str, object], events[1])
        response = cast(dict[str, object], completed["response"])
        part = cast(dict[str, object], response["output"][0]["content"][0])  # type: ignore[index]
        self.assertEqual(part["text"], surr_text)

    def test_no_field_no_edit_raw_identity(self) -> None:
        # No recognized logprobs field and no edit: exact raw bytes in
        # JSON and in the canonical one-answer SSE stream.
        from proxy import transform_json, transform_sse

        value = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {"type": "output_text", "text": TEXT, "content_index": 0}
                    ],
                }
            ],
        }
        raw = json.dumps(value, separators=(",", ":")).encode()
        result, changed = transform_json(raw, lambda t: t)
        self.assertFalse(changed)
        self.assertEqual(result, raw)

        raw_sse = _tc_baseline(TEXT)
        result_sse, changed_sse = transform_sse(raw_sse, lambda t: t)
        self.assertFalse(changed_sse)
        self.assertEqual(result_sse, raw_sse)

    def test_framing_id_retry_comments_done_preserved(self) -> None:
        # SSE framing semantics: comments, id and retry lines and the
        # [DONE] terminator are preserved byte-for-byte while the
        # recognized delta location is re-rendered without logprobs.
        from proxy import transform_sse

        delta = (
            '{"type":"response.output_text.delta","item_id":"m",'
            '"logprobs":[{"token":"a"}],"delta":' + json.dumps(TEXT) + "}"
        ).encode()
        completed = (
            '{"type":"response.completed","response":{"object":"response",'
            '"id":"r","status":"completed","output":'
            '[{"type":"message","id":"m","role":"assistant",'
            '"status":"completed","output_index":0,"content":'
            '[{"type":"output_text","text":' + json.dumps(TEXT)
            + ',"content_index":0}]}]}}'
        ).encode()
        raw = (
            b": keep-alive comment\n"
            b"id: 42\n"
            b"retry: 3000\n"
            b"data: " + delta + b"\n\n"
            b"data: " + completed + b"\n\n"
            b"data: [DONE]\n\n"
        )
        result, changed = transform_sse(raw, lambda t: t)
        self.assertFalse(changed)
        text = result.decode("utf-8")
        self.assertIn(": keep-alive comment\n", text)
        self.assertIn("id: 42\n", text)
        self.assertIn("retry: 3000\n", text)
        self.assertIn("data: [DONE]\n\n", text)
        self.assertNotIn("logprobs", text)
        self.assertIn(TEXT, text)


if __name__ == "__main__":
    unittest.main()
