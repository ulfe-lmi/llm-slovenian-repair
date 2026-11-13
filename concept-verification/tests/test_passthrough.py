"""Real HTTP relay tests; synthetic upstreams, real repair and transport."""

from __future__ import annotations

import http.client
import json
import os
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import proxy  # noqa: E402
from qwen_client import ResponsesReviewer  # noqa: E402
from tests.test_responses_contract import (  # noqa: E402
    _CLEAN_ANSWER,
    _EDIT_T0_KEEP_T1,
    _TEXT_EDITED_T0,
    _json_completed,
    _review_payload,
)
from tests.test_review_batch import (  # noqa: E402
    TEXT,
    _build_corpus,
    _FakeUpstream,
    _real_spec,
    _tc_baseline,
)


class Upstream(BaseHTTPRequestHandler):
    source = b"upstream body\x00\xff"
    status = 200
    content_type = "application/octet-stream"
    recorded: list[tuple[str, str, bytes, list[tuple[str, str]]]] = []
    stream_gate = None

    def relay(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        type(self).recorded.append((self.command, self.path, body, list(self.headers.items())))
        self.send_response(self.status)
        self.send_header("Content-Type", self.content_type)
        self.send_header("Content-Length", str(len(self.source)))
        self.send_header("X-Upstream", "preserved")
        self.send_header("ETag", '"original"')
        self.send_header("Set-Cookie", "one=1")
        self.send_header("Set-Cookie", "two=2")
        self.send_header("Connection", "close, X-Hop")
        self.send_header("X-Hop", "removed")
        self.end_headers()
        if self.command != "HEAD":
            if self.stream_gate is not None:
                self.wfile.write(self.source[:5])
                self.wfile.flush()
                self.stream_gate.wait(5)
                self.wfile.write(self.source[5:])
            else:
                self.wfile.write(self.source)

    do_GET = do_HEAD = do_POST = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = relay

    def log_message(self, *_args):
        pass


class PassthroughTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        Upstream.source = b"upstream body\x00\xff"
        Upstream.status = 200
        Upstream.content_type = "application/octet-stream"
        Upstream.recorded = []
        Upstream.stream_gate = None
        _FakeUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = _review_payload(_EDIT_T0_KEEP_T1)
        self.main = ThreadingHTTPServer(("127.0.0.1", 0), Upstream)
        self.review = ThreadingHTTPServer(("127.0.0.1", 0), _FakeUpstream)
        reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.review.server_port}/v1",
            "synthetic",
            api_key="review-key",
        )
        engine = proxy.RepairEngine(
            _build_corpus(Path(self.temp.name)), reviewer, pandoc=_real_spec()
        )
        self.proxy = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{self.main.server_port}/v1",
            engine,
            passthrough_mode=True,
        )
        self.servers = [self.proxy, self.main, self.review]
        self.threads = []
        for server in self.servers:
            thread = threading.Thread(target=server.serve_forever)
            thread.start()
            self.threads.append(thread)

    def tearDown(self):
        for server in self.servers:
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join(5)
            self.assertFalse(thread.is_alive())
        self.temp.cleanup()

    def request(self, method="POST", path="/v1/responses", body=None, headers=None, **kwargs):
        client = http.client.HTTPConnection("127.0.0.1", self.proxy.server_port, timeout=10)
        client.request(method, path, body=body, headers=headers or {}, **kwargs)
        response = client.getresponse()
        result = response.status, response.read(), response.getheaders()
        client.close()
        return result

    def candidate(self, **extra):
        return json.dumps(
            {"model": "synthetic", "store": False, "input": "Pozdrav.", **extra}
        ).encode()

    def assert_no_review(self):
        self.assertEqual(_FakeUpstream.recorded, [])

    def test_routes_methods_binary_and_metadata_survive(self):
        for method, path in [
            ("GET", "/v1/models?extra=1"),
            ("GET", "/health"),
            ("DELETE", "/v1/responses/r1"),
            ("OPTIONS", "/v1/models"),
            ("PUT", "/custom"),
            ("PATCH", "/custom"),
        ]:
            with self.subTest(method=method, path=path):
                status, body, headers = self.request(method, path)
                self.assertEqual((status, body), (200, Upstream.source))
                self.assertEqual(Upstream.recorded[-1][:2], (method, path))
                self.assertIn(("ETag", '"original"'), headers)
                self.assertEqual([v for k, v in headers if k == "Set-Cookie"], ["one=1", "two=2"])
                self.assertNotIn("X-Hop", dict(headers))
        self.assert_no_review()

    def test_head_preserves_length_without_body(self):
        status, body, headers = self.request("HEAD", "/v1/models")
        self.assertEqual((status, body), (200, b""))
        self.assertEqual(dict(headers)["Content-Length"], str(len(Upstream.source)))

    def test_transparent_proxy_can_bind_all_ipv4_interfaces(self):
        server = proxy.ConceptProxy(
            ("0.0.0.0", 0),
            f"http://127.0.0.1:{self.main.server_port}/v1",
            self.proxy.engine,
            passthrough_mode=True,
        )
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        client = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=2)
        try:
            self.assertEqual(server.server_address[0], "0.0.0.0")
            client.request("GET", "/v1/models")
            response = client.getresponse()
            self.assertEqual((response.status, response.read()), (200, Upstream.source))
        finally:
            client.close()
            server.shutdown()
            server.server_close()
            thread.join(5)
        self.assertFalse(thread.is_alive())

    def test_other_traffic_streams_before_upstream_completion(self):
        gate = threading.Event()
        Upstream.stream_gate = gate
        client = http.client.HTTPConnection("127.0.0.1", self.proxy.server_port, timeout=2)
        try:
            client.request("GET", "/custom-stream")
            response = client.getresponse()
            self.assertEqual(response.read(5), Upstream.source[:5])
            self.assertFalse(gate.is_set())
            gate.set()
            self.assertEqual(response.read(), Upstream.source[5:])
        finally:
            gate.set()
            client.close()
        self.assert_no_review()

    def test_buffered_body_timeout_returns_error_and_releases_request(self):
        gate = threading.Event()
        Upstream.stream_gate = gate
        Upstream.content_type = "application/json"
        Upstream.source = _json_completed(TEXT)
        self.proxy.capture_timeout = 0.15
        try:
            self.assertEqual(self.request(body=self.candidate())[0], 502)
            self.assertEqual(self.request("HEAD", "/health")[0], 200)
            self.assertFalse(gate.is_set())
        finally:
            gate.set()
        self.assert_no_review()

    def test_stream_disconnect_releases_slot_before_upstream_finishes(self):
        gate = threading.Event()
        Upstream.stream_gate = gate
        client = http.client.HTTPConnection("127.0.0.1", self.proxy.server_port, timeout=2)
        try:
            client.request("GET", "/blocked-stream")
            response = client.getresponse()
            self.assertEqual(response.read(5), Upstream.source[:5])
            response.close()
            client.close()
            self.assertEqual(self.request("HEAD", "/health")[0], 200)
            self.assertFalse(gate.is_set())
        finally:
            gate.set()
            client.close()
        self.assert_no_review()

    def test_repeated_request_headers_survive(self):
        client = http.client.HTTPConnection("127.0.0.1", self.proxy.server_port, timeout=2)
        try:
            client.putrequest("GET", "/v1/models")
            client.putheader("X-Vendor", "one")
            client.putheader("X-Vendor", "two")
            client.endheaders()
            response = client.getresponse()
            response.read()
            self.assertEqual(response.status, 200)
        finally:
            client.close()
        self.assertEqual(
            [v for k, v in Upstream.recorded[-1][3] if k == "X-Vendor"], ["one", "two"]
        )

    def test_tools_images_and_vendor_fields_arrive_unchanged(self):
        body = self.candidate(
            tools=[{"type": "function", "name": "read_file"}],
            input=[
                {"role": "user", "content": [{"type": "input_image", "image_url": "synthetic"}]}
            ],
            future_vendor_option={"value": True},
        )
        status, result, _ = self.request(
            body=body,
            headers={
                "Authorization": "Bearer caller-key",
                "X-Vendor": "preserve",
                "Connection": "close, X-Internal",
                "X-Internal": "remove",
            },
        )
        self.assertEqual((status, result), (200, Upstream.source))
        self.assertEqual(Upstream.recorded[-1][2], body)
        forwarded = dict(Upstream.recorded[-1][3])
        self.assertEqual(forwarded["Authorization"], "Bearer caller-key")
        self.assertEqual(forwarded["X-Vendor"], "preserve")
        self.assertNotIn("X-Internal", forwarded)
        self.assert_no_review()

    def test_tool_response_is_byte_identical(self):
        Upstream.content_type = "application/json"
        Upstream.source = (
            b'{ "object":"response", "status":"completed", "output":'
            b'[{"type":"function_call","name":"f","arguments":"{}"}]} '
        )
        self.assertEqual(self.request(body=self.candidate(tools=[]))[:2], (200, Upstream.source))
        self.assert_no_review()

    def test_plain_final_answer_with_tools_is_actually_repaired(self):
        Upstream.content_type = "application/json"
        Upstream.source = _json_completed(TEXT)
        status, body, headers = self.request(
            body=self.candidate(tools=[{"type": "function", "name": "f"}])
        )
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["output"][0]["content"][0]["text"], _TEXT_EDITED_T0)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertNotIn("ETag", dict(headers))

    def test_structured_and_stored_requests_bypass_repair(self):
        Upstream.content_type = "application/json"
        Upstream.source = _json_completed(TEXT)
        for extra in [
            {"text": {"format": {"type": "json_schema"}}},
            {"store": True},
            {"previous_response_id": "r1"},
            {"background": True},
            {"response_format": {"type": "json_object"}},
        ]:
            with self.subTest(extra=extra):
                self.assertEqual(
                    self.request(body=self.candidate(**extra))[:2], (200, Upstream.source)
                )
        self.assert_no_review()

    def test_explicit_trace_setting_still_records_the_repaired_text(self):
        trace_dir = Path(self.temp.name) / "traces"
        trace_dir.mkdir()
        self.proxy.trace_dir = trace_dir
        Upstream.content_type = "application/json"
        Upstream.source = _json_completed(TEXT)
        self.assertEqual(self.request(body=self.candidate())[0], 200)
        traces = list(trace_dir.glob("*.json"))
        self.assertEqual(len(traces), 1)
        record = json.loads(traces[0].read_text())
        self.assertEqual(record["original"], TEXT)
        self.assertEqual(record["repaired"], _TEXT_EDITED_T0)

    def test_upstream_errors_are_opaque_with_headers(self):
        Upstream.content_type = "application/json"
        Upstream.source = b'{"error":"invalid", "logprobs":42}'
        for status in [400, 401, 404, 429, 500, 503]:
            Upstream.status = status
            self.assertEqual(self.request(body=b"invalid JSON")[:2], (status, Upstream.source))
        self.assert_no_review()

    def test_malformed_candidate_response_is_passed_unchanged(self):
        Upstream.content_type = "application/json"
        Upstream.source = b"\xffnot-json"
        self.assertEqual(self.request(body=self.candidate())[:2], (200, Upstream.source))
        self.assert_no_review()

    def test_chunked_upload_is_forwarded_with_identical_payload(self):
        chunks = [b"first", b"\x00\xffsecond"]
        self.assertEqual(
            self.request(path="/v1/chat/completions", body=iter(chunks), encode_chunked=True)[:2],
            (200, Upstream.source),
        )
        self.assertEqual(Upstream.recorded[-1][2], b"".join(chunks))
        self.assert_no_review()

    def test_oversized_repair_capture_falls_back_to_passthrough(self):
        Upstream.content_type = "application/json"
        Upstream.source = _json_completed(TEXT)
        with mock.patch.object(proxy, "MAIN_BODY_MAX_BYTES", 16):
            self.assertEqual(self.request(body=self.candidate())[:2], (200, Upstream.source))
        self.assert_no_review()

    def test_clean_answer_is_unchanged_without_review(self):
        Upstream.content_type = "application/json"
        Upstream.source = _json_completed(_CLEAN_ANSWER)
        self.assertEqual(self.request(body=self.candidate())[:2], (200, Upstream.source))
        self.assert_no_review()

    def test_streaming_final_answer_is_repaired_consistently(self):
        Upstream.content_type = "text/event-stream"
        Upstream.source = _tc_baseline(TEXT)
        status, body, _ = self.request(body=self.candidate(stream=True, tools=[]))
        self.assertEqual(status, 200)
        self.assertIn(_TEXT_EDITED_T0.encode(), body)
        self.assertNotIn(TEXT.encode(), body)
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_streaming_tool_events_are_unchanged(self):
        Upstream.content_type = "text/event-stream"
        Upstream.source = (
            b'data: {"type":"response.function_call_arguments.delta","delta":"{}"}\n\n'
            b"data: [DONE]\n\n"
        )
        self.assertEqual(self.request(body=self.candidate(stream=True))[:2], (200, Upstream.source))
        self.assert_no_review()

    def test_ambiguous_framing_never_reaches_upstream(self):
        status, _, _ = self.request(
            body=b"x", headers={"Content-Length": "1", "Transfer-Encoding": "chunked"}
        )
        self.assertEqual(status, 400)
        self.assertEqual(Upstream.recorded, [])


class LauncherSettingsTests(unittest.TestCase):
    def run_launcher(self, settings):
        environment = {"CONCEPT_INDEX": "/synthetic/index.sqlite", **settings}
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(proxy, "resolve_pandoc_spec", return_value=_real_spec()),
            mock.patch.object(proxy, "check_pandoc"),
            mock.patch.object(proxy, "ConceptProxy") as factory,
        ):
            self.assertEqual(proxy.main(), 0)
        factory.return_value.serve_forever.assert_called_once()
        factory.return_value.server_close.assert_called_once()
        return factory.call_args

    def test_normal_launcher_selects_requested_port_and_transparent_handler(self):
        selected = self.run_launcher({"CONCEPT_PORT": "18023"})
        self.assertEqual(selected.args[0], ("127.0.0.1", 18023))
        self.assertIs(selected.kwargs["passthrough_mode"], True)

    def test_launcher_can_select_all_ipv4_interfaces(self):
        selected = self.run_launcher({"CONCEPT_HOST": "0.0.0.0", "CONCEPT_PORT": "18023"})
        self.assertEqual(selected.args[0], ("0.0.0.0", 18023))
        self.assertIs(selected.kwargs["passthrough_mode"], True)

    def test_strict_mode_remains_available(self):
        selected = self.run_launcher({"CONCEPT_PASSTHROUGH": "0"})
        self.assertEqual(selected.args[0], ("127.0.0.1", 18024))
        self.assertIs(selected.kwargs["passthrough_mode"], False)

    def test_invalid_listener_settings_never_construct_a_listener(self):
        for setting, values in [
            ("CONCEPT_PORT", ["0", "-1", "65536", "bad", ""]),
            ("CONCEPT_HOST", ["", "not-an-address", "256.0.0.1", "::1"]),
            ("CONCEPT_PASSTHROUGH", ["true", "2", ""]),
        ]:
            for value in values:
                with (
                    self.subTest(setting=setting, value=value),
                    mock.patch.dict(os.environ, {setting: value}, clear=True),
                    mock.patch.object(proxy, "ConceptProxy") as factory,
                    self.assertRaises(ValueError),
                ):
                    proxy.main()
                factory.assert_not_called()


if __name__ == "__main__":
    unittest.main()
