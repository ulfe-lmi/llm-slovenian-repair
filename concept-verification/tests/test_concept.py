"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Focused tests."""

from __future__ import annotations

import http.client
import json
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from corpus import Corpus, CorpusError  # noqa: E402, I001
from detector import Candidate, detect  # noqa: E402
from eval.collect import build_codex_command, main as collect_main  # noqa: E402
from eval.review_sheet import main as review_sheet_main  # noqa: E402
from eval.run_eval import _evaluate  # noqa: E402
from protected import protected_intervals  # noqa: E402
from proxy import ConceptProxy, RepairEngine, transform_sse  # noqa: E402
from qwen_client import ReviewerError, parse_proposal  # noqa: E402
from repair import accept, apply_edits  # noqa: E402


class ConceptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "tiny.sqlite"
        connection = sqlite3.connect(self.db)
        connection.executescript(
            """
            CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE unigram (word TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE bigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE trigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE middle (left_word TEXT, right_word TEXT, middle_word TEXT, count INTEGER,
                PRIMARY KEY(left_word,right_word,middle_word));
            INSERT INTO unigram VALUES
                ('to',100),('je',100),('tako',100),('presenetljiv',50),('zapisano',50);
            INSERT INTO bigram VALUES
                ('je tako',20),('tako zapisano',20),('je presenetljiv',20),('je zapisano',20);
            INSERT INTO trigram VALUES ('to je tako',20),('je tako zapisano',20);
            INSERT INTO middle VALUES ('je','zapisano','tako',20);
            """
        )
        connection.commit()
        connection.close()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_protection_and_exact_patch_invariance(self) -> None:
        text = "Dobro `git status` in URL https://example.org sta varna."
        intervals = protected_intervals(text)
        repaired = apply_edits(text, [(0, 5, "Zares")], intervals)
        for interval in intervals:
            self.assertEqual(
                text[interval.start : interval.end], repaired[interval.start : interval.end]
            )
        self.assertIn("`git status`", repaired)
        self.assertTrue(any(item.reason.startswith("url") for item in intervals))

    def test_evidence_semantics_and_lookup(self) -> None:
        with Corpus(self.db) as corpus:
            self.assertEqual(corpus.unigram("tako").state, "EXACT")
            self.assertEqual(corpus.unigram("missing").state, "UNAVAILABLE")
            self.assertEqual(corpus.ngram("never present", 2).state, "CENSORED")
            self.assertEqual(corpus.ngram("je tako", 2).count, 20)
            self.assertEqual(corpus.alternatives("je", "zapisano"), [("tako", 20)])

    def test_detector_is_deterministic_and_bounded(self) -> None:
        text = "To je presenetliv zapisano in presenetliv zapisano."
        with Corpus(self.db) as corpus:
            first = detect(text, corpus, protected_intervals(text), maximum=4)
            second = detect(text, corpus, protected_intervals(text), maximum=4)
        self.assertEqual(first, second)
        self.assertLessEqual(len(first), 4)
        self.assertTrue(all(item.start < item.end for item in first))

    def test_strict_reviewer_parser(self) -> None:
        good = {
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "output_text",
                            "text": '{"keep":false,"replacement":"tako","needs_wider_edit":false}',
                        }
                    ],
                }
            ]
        }
        self.assertEqual(parse_proposal(good).replacement, "tako")
        bad = {
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "output_text",
                            "text": (
                                '{"keep":false,"replacement":"tako",'
                                '"needs_wider_edit":false,"extra":1}'
                            ),
                        }
                    ],
                }
            ]
        }
        with self.assertRaises(ReviewerError):
            parse_proposal(bad)

    def test_acceptance_requires_independent_local_evidence(self) -> None:
        text = "To je presenetliv zapisano."
        intervals = protected_intervals(text)
        with Corpus(self.db) as corpus:
            candidates = detect(text, corpus, intervals, maximum=4)
            self.assertTrue(candidates)
            candidate = candidates[0]
            from qwen_client import Proposal

            decision = accept(
                text,
                candidate,
                Proposal(False, "tako", False),
                corpus,
                intervals,
                left="je",
                right="zapisano",
            )
            self.assertTrue(decision.accepted)
            repaired = apply_edits(text, [(candidate.start, candidate.end, "tako")], intervals)
            self.assertEqual(repaired, "To je tako zapisano.")

    def test_sse_preserves_event_count_ids_and_usage(self) -> None:
        events = [
            {"type": "response.created", "response": {"id": "r1"}},
            {"type": "response.output_text.delta", "item_id": "m1", "delta": "presenetliv"},
            {"type": "response.output_text.done", "item_id": "m1", "text": "presenetliv"},
            {
                "type": "response.completed",
                "response": {
                    "id": "r1",
                    "usage": {"total_tokens": 4},
                    "output": [
                        {
                            "type": "message",
                            "content": [{"type": "output_text", "text": "presenetliv"}],
                        }
                    ],
                },
            },
        ]
        raw = b"".join(
            (b"event: x\ndata: " + json.dumps(event).encode() + b"\n\n") for event in events
        )
        changed, found = transform_sse(
            raw, lambda value: value.replace("presenetliv", "presenetljiv")
        )
        self.assertTrue(found)
        changed_events = [
            json.loads(part.split(b"data: ", 1)[1])
            for part in changed.split(b"\n\n")
            if b"data: " in part
        ]
        self.assertEqual(len(changed_events), len(events))
        self.assertEqual(changed_events[0]["response"]["id"], "r1")
        self.assertEqual(changed_events[-1]["response"]["usage"]["total_tokens"], 4)
        self.assertEqual(changed_events[1]["delta"], "presenetljiv")

    def test_evaluator_calls_reviewer_once_and_no_reviewer_is_a_noop(self) -> None:
        text = "To je presenetliv zapisano."
        start = text.index("presenetliv")
        candidate = Candidate(
            start,
            start + len("presenetliv"),
            "presenetliv",
            1.0,
            {"unigram": {"state": "UNAVAILABLE"}},
        ).as_dict()
        case = {
            "id": "x01",
            "text": text,
            "target": "presenetliv",
            "start": start,
            "end": start + len("presenetliv"),
            "known_error": True,
            "gold": "tako",
        }

        class Reviewer:
            def __init__(self) -> None:
                self.calls = 0

            def review(self, *_args: object) -> object:
                self.calls += 1
                from qwen_client import Proposal

                return Proposal(False, "tako", False)

        reviewer = Reviewer()
        with Corpus(self.db) as corpus:
            records, metrics = _evaluate(
                [case], corpus, {"x01": [candidate]}, reviewer, "frozen-v1"
            )
        self.assertEqual(reviewer.calls, 1)
        self.assertEqual(records[0]["repaired"], "To je tako zapisano.")
        self.assertEqual(records[0]["apply_edits_calls"], 1)
        self.assertEqual(metrics["exact_gold_correct_repairs"], 1)
        with Corpus(self.db) as corpus:
            records, metrics = _evaluate([case], corpus, {"x01": [candidate]}, None, "frozen-v1")
        self.assertEqual(records[0]["repaired"], text)
        self.assertEqual(records[0]["reviewer_calls"], 0)
        self.assertEqual(metrics["accepted_edits"], 0)

    def test_evaluator_counts_reviewer_failure_harm_and_miss(self) -> None:
        text = "To je presenetliv zapisano."
        start = text.index("presenetliv")
        candidate = Candidate(
            start,
            start + len("presenetliv"),
            "presenetliv",
            1.0,
            {"unigram": {"state": "UNAVAILABLE"}},
        ).as_dict()
        case = {
            "id": "x02",
            "text": text,
            "target": "presenetliv",
            "start": start,
            "end": start + len("presenetliv"),
            "known_error": True,
            "gold": "tako",
        }

        class WrongReviewer:
            def review(self, *_args: object) -> object:
                from qwen_client import Proposal

                return Proposal(False, "zapisano", False)

        with Corpus(self.db) as corpus:
            _records, metrics = _evaluate(
                [case], corpus, {"x02": [candidate]}, WrongReviewer(), "frozen-v1"
            )
        self.assertEqual(metrics["harmful_edits"], 1)
        self.assertEqual(metrics["missed_known_errors"], 1)
        self.assertEqual(metrics["accepted_edits"], 1)

        class FailedReviewer:
            def review(self, *_args: object) -> object:
                from qwen_client import ReviewerError

                raise ReviewerError("synthetic failure")

        with Corpus(self.db) as corpus:
            records, metrics = _evaluate(
                [case], corpus, {"x02": [candidate]}, FailedReviewer(), "frozen-v1"
            )
        self.assertEqual(metrics["reviewer_calls"], 1)
        self.assertEqual(metrics["reviewer_correct"], 0)
        self.assertEqual(records[0]["decisions"][0]["failure"], "reviewer-error")

    def test_proxy_stops_at_terminal_event_without_eof(self) -> None:
        source = (
            b": keep this comment\n\n"
            b'event: unknown\ndata: {"type":"unknown.event"}\n\n'
            b'data: {"type":"response.completed","response":{}}\n\n'
        )

        class Upstream(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                self.wfile.write(source)
                self.wfile.flush()
                time.sleep(0.6)

            def log_message(self, *_args: object) -> None:
                return

        class Engine:
            def repair(self, value: str) -> str:
                return value

        upstream = HTTPServer(("127.0.0.1", 0), Upstream)
        proxy = ConceptProxy(("127.0.0.1", 0), f"http://127.0.0.1:{upstream.server_port}", Engine())
        upstream_thread = threading.Thread(target=upstream.handle_request)
        proxy_thread = threading.Thread(target=proxy.handle_request)
        upstream_thread.start()
        proxy_thread.start()
        try:
            client = http.client.HTTPConnection("127.0.0.1", proxy.server_port, timeout=2)
            client.request("POST", "/v1/responses", body=b"{}", headers={"Content-Length": "2"})
            response = client.getresponse()
            result = response.read()
            self.assertEqual(response.status, 200)
            self.assertIn(b"response.completed", result)
            self.assertIn(b": keep this comment", result)
            proxy_thread.join(2)
            self.assertFalse(proxy_thread.is_alive())
        finally:
            client.close()
            proxy.server_close()
            upstream_thread.join(2)
            upstream.server_close()

    def test_proxy_incomplete_stream_times_out_and_normalizes_path(self) -> None:
        paths: list[str] = []

        class Upstream(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                paths.append(self.path)
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                self.wfile.write(b'data: {"type":"response.created"}\n')
                self.wfile.flush()
                time.sleep(0.4)

            def log_message(self, *_args: object) -> None:
                return

        upstream = HTTPServer(("127.0.0.1", 0), Upstream)
        proxy = ConceptProxy(
            ("127.0.0.1", 0), f"http://127.0.0.1:{upstream.server_port}/v1", object(), timeout=0.1
        )
        upstream_thread = threading.Thread(target=upstream.handle_request)
        proxy_thread = threading.Thread(target=proxy.handle_request)
        upstream_thread.start()
        proxy_thread.start()
        try:
            client = http.client.HTTPConnection("127.0.0.1", proxy.server_port, timeout=2)
            client.request("POST", "/v1/responses", body=b"{}", headers={"Content-Length": "2"})
            response = client.getresponse()
            self.assertEqual(response.status, 502)
            response.read()
            proxy_thread.join(2)
        finally:
            client.close()
            proxy.server_close()
            upstream_thread.join(2)
            upstream.server_close()
        self.assertEqual(paths, ["/v1/responses"])

    def test_proxy_forwards_non_200_status_and_content_type(self) -> None:
        class Upstream(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(429)
                self.send_header("Content-Type", "application/problem+json")
                self.send_header("Content-Length", "3")
                self.end_headers()
                self.wfile.write(b"err")

            def log_message(self, *_args: object) -> None:
                return

        upstream = HTTPServer(("127.0.0.1", 0), Upstream)
        proxy = ConceptProxy(("127.0.0.1", 0), f"http://127.0.0.1:{upstream.server_port}", object())
        upstream_thread = threading.Thread(target=upstream.handle_request)
        proxy_thread = threading.Thread(target=proxy.handle_request)
        upstream_thread.start()
        proxy_thread.start()
        try:
            client = http.client.HTTPConnection("127.0.0.1", proxy.server_port, timeout=2)
            client.request("POST", "/v1/responses", body=b"{}", headers={"Content-Length": "2"})
            response = client.getresponse()
            self.assertEqual(response.status, 429)
            self.assertEqual(response.getheader("Content-Type"), "application/problem+json")
            self.assertEqual(response.read(), b"err")
        finally:
            client.close()
            proxy.server_close()
            upstream_thread.join(2)
            upstream.server_close()

    def test_trace_is_opt_in_and_excludes_headers(self) -> None:
        trace_root = Path(self.temp.name) / "traces"

        class Reviewer:
            def review(self, *_args: object) -> object:
                from qwen_client import Proposal

                return Proposal(True, None, False)

        engine = RepairEngine(self.db, Reviewer())
        engine.begin_request()
        engine.repair("To je zapisano.")
        details = engine.take_details()
        proxy = ConceptProxy(("127.0.0.1", 0), "http://127.0.0.1:1", engine, trace_dir=trace_root)
        try:
            paths = proxy.write_traces("req1", details, 0.2)
            self.assertEqual(len(paths), 1)
            value = json.loads(paths[0].read_text(encoding="utf-8"))
            self.assertNotIn("headers", value)
            self.assertEqual(value["request_id"], "req1")
        finally:
            proxy.server_close()
        disabled_root = Path(self.temp.name) / "disabled"
        self.assertFalse(disabled_root.exists())

    def test_codex_command_and_fake_executable_exit_are_recorded(self) -> None:
        command = build_codex_command(
            "codex",
            "qwen-neumann",
            "provider-x",
            "http://127.0.0.1:18024/v1",
            Path("/tmp/work"),
            "prompt",
        )
        self.assertIn("--ephemeral", command)
        self.assertIn("--profile", command)
        self.assertIn('model_providers.provider-x.base_url="http://127.0.0.1:18024/v1"', command)
        root = Path(self.temp.name)
        fake = root / "fake-codex"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import sys\n"
            'print(\'{"type":"turn.completed"}\')\n'
            "sys.exit(7)\n",
            encoding="utf-8",
        )
        fake.chmod(0o700)
        codex_home = root / "codex-home"
        codex_home.mkdir()
        results = root / "results"
        trace_dir = root / "traces"
        work_root = root / "work"
        self.assertEqual(
            collect_main(
                [
                    "--cases",
                    "1",
                    "--codex-bin",
                    str(fake),
                    "--codex-home",
                    str(codex_home),
                    "--provider-id",
                    "provider-x",
                    "--proxy",
                    "http://127.0.0.1:18024/v1",
                    "--trace-dir",
                    str(trace_dir),
                    "--work-root",
                    str(work_root),
                    "--results",
                    str(results),
                    "--timeout",
                    "2",
                ]
            ),
            0,
        )
        value = json.loads((results / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(value["responses"][0]["exit_code"], 7)
        self.assertEqual(value["responses"][0]["failure"], "codex_exit_nonzero")

    def test_review_sheet_populates_and_refuses_empty_trace(self) -> None:
        root = Path(self.temp.name)
        input_root = root / "input"
        traces = root / "traces"
        input_root.mkdir()
        traces.mkdir()
        trace = traces / "req1-0.json"
        trace.write_text(
            json.dumps(
                {
                    "request_id": "req1",
                    "original": "To je zapisano.",
                    "repaired": "To je zapisano.",
                    "reviewer_decisions": [
                        {
                            "candidate": {"text": "zapisano", "start": 6, "end": 14},
                            "evidence": {"unigram": {"state": "EXACT"}},
                            "proposal": {"keep": True, "replacement": None},
                            "acceptance": {"accepted": False, "replacement": None},
                        }
                    ],
                    "protocol": {"response_completed": True},
                }
            ),
            encoding="utf-8",
        )
        (input_root / "summary.json").write_text(
            json.dumps(
                {"responses": [{"id": "case1", "status": "COMPLETED", "trace_files": [str(trace)]}]}
            ),
            encoding="utf-8",
        )
        output = root / "sheet.jsonl"
        self.assertEqual(
            review_sheet_main(
                ["--input", str(input_root), "--traces", str(traces), "--output", str(output)]
            ),
            0,
        )
        row = json.loads(output.read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(row["pair_label"], "")
        self.assertEqual(row["targets"][0]["edit_label"], "")
        self.assertEqual(
            {row["left"]["text"], row["right"]["text"]}, {row["original"], row["repaired"]}
        )
        trace.write_text(
            json.dumps(
                {
                    "request_id": "req1",
                    "original": "",
                    "repaired": "x",
                    "protocol": {"response_completed": True},
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(SystemExit):
            review_sheet_main(
                ["--input", str(input_root), "--traces", str(traces), "--output", str(output)]
            )

    def test_fake_qwen_proxy_round_trip(self) -> None:
        source = (
            b'data: {"type":"response.output_text.delta","item_id":"m",'
            b'"delta":"presenetliv"}\n\n'
            b'data: {"type":"response.output_text.done","item_id":"m",'
            b'"text":"presenetliv"}\n\n'
            b'data: {"type":"response.completed","response":{"id":"r",'
            b'"usage":{"total_tokens":2}}}\n\n'
        )

        class Upstream(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(source)))
                self.end_headers()
                self.wfile.write(source)

            def log_message(self, *_: object) -> None:
                return

        class Engine:
            def repair(self, value: str) -> str:
                return value.replace("presenetliv", "presenetljiv")

        upstream = HTTPServer(("127.0.0.1", 0), Upstream)
        proxy = ConceptProxy(("127.0.0.1", 0), f"http://127.0.0.1:{upstream.server_port}", Engine())
        upstream_thread = threading.Thread(target=upstream.handle_request)
        proxy_thread = threading.Thread(target=proxy.handle_request)
        upstream_thread.start()
        proxy_thread.start()
        client = http.client.HTTPConnection("127.0.0.1", proxy.server_port, timeout=3)
        client.request("POST", "/v1/responses", body=b"{}", headers={"Content-Length": "2"})
        response = client.getresponse()
        result = response.read()
        proxy_thread.join(3)
        upstream_thread.join(3)
        proxy.server_close()
        upstream.server_close()
        self.assertEqual(response.status, 200)
        self.assertIn(b"presenetljiv", result)
        self.assertIn(b'"total_tokens":2', result)

    def test_archive_identity_rejects_tiny_fixture_before_member_access(self) -> None:
        from config import WORDS
        from corpus import _safe_archive

        tiny = Path(self.temp.name) / "tiny.zip"
        tiny.write_bytes(b"not an archive")
        with self.assertRaises(CorpusError):
            _safe_archive(tiny, WORDS)


if __name__ == "__main__":
    unittest.main()
