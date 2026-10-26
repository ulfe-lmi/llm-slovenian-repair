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

_ABSENT: object = object()

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
            _MainUpstream.source = raw
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(payload, raw)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
        finally:
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
            _MainUpstream.source = _tc_baseline(TEXT)
            _FakeUpstream.payload = _review_payload([_prop("t1"), _prop("t0")])
            status, payload = harness.post(_contract_body(True))
            self.assertEqual(status, 200)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            self.assertNotIn(b"presenetliv", payload)
            self.assertEqual(payload.count(b"To je tako zapisano, to je tako zapisano."), 4)
        finally:
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
            (
                "final_part_logprobs",
                {
                    "part": {
                        "type": "output_text",
                        "text": TEXT,
                        "content_index": 0,
                        "logprobs": [
                            {
                                "token": "a",
                                "logprob": -0.1,
                                "start_index": 0,
                                "end_index": 1,
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

    def test_sse_delta_logprobs_bypass(self) -> None:
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
        self._sse_bypass(raw)

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


if __name__ == "__main__":
    unittest.main()
