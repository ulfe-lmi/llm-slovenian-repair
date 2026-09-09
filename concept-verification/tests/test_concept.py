"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Focused tests."""

from __future__ import annotations

import http.client
import json
import sqlite3
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from corpus import Corpus, CorpusError  # noqa: E402
from detector import detect  # noqa: E402
from protected import protected_intervals  # noqa: E402
from proxy import ConceptProxy, transform_sse  # noqa: E402
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
            INSERT INTO bigram VALUES ('je tako',20),('tako zapisano',20),('je presenetljiv',20);
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
