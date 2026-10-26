"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Review batch.

Order 014-a acceptance coverage for one bounded occurrence-addressed
reviewer batch in the runnable proxy: target preparation and bounded
context, strict duplicate-key-free parsing at both envelope levels, the
actual ResponsesReviewer transport against an in-process fake upstream
(exact route/body/authorization, timeout, non-200, oversize, encoding,
pre-dispatch limits), the real RepairEngine with real Pandoc and a real
tiny SQLite corpus, whole-batch rejection versus individual evidence
rejection, and the one-answer SSE eligibility guard through an ephemeral
ConceptProxy HTTP round trip.
"""

from __future__ import annotations

import http.client
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable, Mapping, Sequence
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import batch_review  # noqa: E402
from batch_review import (  # noqa: E402
    REASON_DUPLICATE_ID,
    REASON_FAILED,
    REASON_HTTP_FAILED,
    REASON_HTTP_NOT_OK,
    REASON_INVALID_ENCODING,
    REASON_PREP_INVALID,
    REASON_PROMPT_OVERSIZE,
    REASON_REPLACEMENT_OVERSIZE,
    REASON_REQUEST_OVERSIZE,
    BatchProposal,
    BatchTarget,
    build_prompt,
    build_request_body,
    parse_batch_envelope,
    prepare_targets,
    strict_json_object,
)
from config import (  # noqa: E402
    REVIEW_BATCH_CONTEXT_CODEPOINTS,
    REVIEW_BATCH_MAX_ITEMS,
    REVIEW_BATCH_MAX_PROMPT_CODEPOINTS,
    REVIEW_BATCH_MAX_PROPOSAL_JSON_CODEPOINTS,
    REVIEW_BATCH_MAX_RESPONSE_BYTES,
    REVIEW_BATCH_MAX_TARGET_CODEPOINTS,
)
from detector import Candidate, detect  # noqa: E402
from pandoc_protection import PandocSpec  # noqa: E402
from protected import Interval  # noqa: E402
from proxy import RepairEngine, transform_sse  # noqa: E402
from qwen_client import ResponsesReviewer, ReviewerError  # noqa: E402

from corpus import Corpus  # noqa: E402

TEXT = "To je presenetliv zapisano, to je presenetliv zapisano."


def _real_spec() -> PandocSpec:
    configured = os.environ.get("CONCEPT_PANDOC", "").strip()
    binary = configured or shutil.which("pandoc") or "/usr/bin/pandoc"
    return PandocSpec(binary=binary)


def _occurrences(text: str, word: str = "presenetliv") -> tuple[tuple[int, int, str], ...]:
    result: list[tuple[int, int, str]] = []
    start = text.find(word)
    while start != -1:
        result.append((start, start + len(word), word))
        start = text.find(word, start + 1)
    return tuple(result)


def _build_corpus(root: Path) -> Path:
    db = root / "tiny.sqlite"
    connection = sqlite3.connect(db)
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
    return db


def _valid_inner(proposals: list[dict[str, object]]) -> str:
    return json.dumps(
        {"version": "batch-v1", "proposals": proposals},
        ensure_ascii=False,
        separators=(",", ":"),
    )


def _prop(pid: str, keep: bool = False, replacement: str | None = "tako",
          wider: bool = False) -> dict[str, object]:
    return {"id": pid, "keep": keep, "replacement": replacement,
            "needs_wider_edit": wider}


def _envelope(inner: str, *, status: str = "completed", etype: str = "response",
              error: object = None, parts: Sequence[Mapping[str, object]] | None = None,
              items: Sequence[Mapping[str, object]] | None = None) -> dict[str, object]:
    if items is None:
        if parts is None:
            parts = [{"type": "output_text", "text": inner}]
        items = [{"type": "message", "role": "assistant", "content": parts}]
    # The documented Responses object carries ``object`` (the restored
    # historical Qwen envelope has object=response without a type field).
    value: dict[str, object] = {"object": etype, "status": status, "output": items}
    if error is not None:
        value["error"] = error
    return value


class PrepareTargetsTests(unittest.TestCase):
    def test_valid_two_occurrences_keep_order_and_context(self) -> None:
        targets = prepare_targets(TEXT, _occurrences(TEXT), ())
        self.assertIsNotNone(targets)
        targets = cast(tuple[BatchTarget, ...], targets)
        self.assertEqual(len(targets), 2)
        self.assertEqual([t.id for t in targets], ["t0", "t1"])
        self.assertEqual(targets[0].before_target, "To je ")
        self.assertEqual(targets[0].target, "presenetliv")
        self.assertEqual(targets[0].after_target, " zapisano, to je presenetliv zapisano.")
        self.assertEqual(targets[1].before_target, "To je presenetliv zapisano, to je ")
        self.assertEqual(targets[1].after_target, " zapisano.")
        for target in targets:
            self.assertFalse(target.truncated_before)
            self.assertFalse(target.truncated_after)

    def test_context_window_and_truncation_flags(self) -> None:
        filler = "abc " * 300
        text = filler + "presenetliv" + filler + "."
        (start, end, word) = _occurrences(text)[0]
        targets = prepare_targets(text, ((start, end, word),), ())
        targets = cast(tuple[BatchTarget, ...], targets)
        target = targets[0]
        self.assertEqual(len(target.before_target), REVIEW_BATCH_CONTEXT_CODEPOINTS)
        self.assertEqual(len(target.after_target), REVIEW_BATCH_CONTEXT_CODEPOINTS)
        self.assertTrue(target.truncated_before)
        self.assertTrue(target.truncated_after)

    def test_empty_occurrences(self) -> None:
        self.assertEqual(prepare_targets(TEXT, (), ()), ())

    def test_invalid_bounds(self) -> None:
        (start, end, word) = _occurrences(TEXT)[0]
        for bad in ((start - 1, end - 1, word), (start, end + 1, word),
                    (end, start, word), (start, start, word)):
            self.assertIsNone(prepare_targets(TEXT, (bad,), ()))

    def test_stale_slice_is_never_relocated(self) -> None:
        (start, end, _word) = _occurrences(TEXT)[0]
        stale = (start + 1, end + 1, "resenetliv")
        self.assertIsNone(prepare_targets(TEXT, (stale,), ()))

    def test_overlap_and_order_violations(self) -> None:
        (s0, e0, w) = _occurrences(TEXT)[0]
        (s1, e1, _w1) = _occurrences(TEXT)[1]
        self.assertIsNone(prepare_targets(TEXT, ((s0, e0, w), (s0 + 1, e0 + 1, w[:10])), ()))
        self.assertIsNone(prepare_targets(TEXT, ((s1, e1, w), (s0, e0, w)), ()))

    def test_protected_intersection_rejected(self) -> None:
        (start, end, word) = _occurrences(TEXT)[0]
        self.assertIsNone(prepare_targets(TEXT, ((start, end, word),), ((start, start + 2),)))
        self.assertIsNone(prepare_targets(TEXT, ((start, end, word),), ((end - 1, end + 4),)))

    def test_target_oversize_rejected(self) -> None:
        long_word = "x" * (REVIEW_BATCH_MAX_TARGET_CODEPOINTS + 1)
        text = f"To je {long_word} zapisano."
        (start, end, word) = _occurrences(text, long_word)[0]
        self.assertIsNone(prepare_targets(text, ((start, end, word),), ()))

    def test_too_many_targets_rejected(self) -> None:
        word = "presenetliv"
        text = ", ".join(f"To je {word} zapisano" for _ in range(REVIEW_BATCH_MAX_ITEMS + 1)) + "."
        occurrences = _occurrences(text, word)
        self.assertEqual(len(occurrences), REVIEW_BATCH_MAX_ITEMS + 1)
        self.assertIsNone(prepare_targets(text, occurrences, ()))

    def test_grapheme_sensitive_target_rejected(self) -> None:
        text = "To je presenetli\u034fv zapisano."
        start = text.index("presenetli")
        word = "presenetli\u034fv"
        self.assertIsNone(prepare_targets(text, ((start, start + len(word), word),), ()))

    def test_boundary_sensitive_rejected(self) -> None:
        text = "To je presenetliv\u200d zapisano."  # ZWJ directly after target
        start = text.index("presenetliv")
        word = "presenetliv"
        self.assertIsNone(prepare_targets(text, ((start, start + len(word), word),), ()))


class BuildPromptTests(unittest.TestCase):
    def test_prompt_frames_targets_as_json(self) -> None:
        targets = prepare_targets(TEXT, _occurrences(TEXT), ())
        prompt = build_prompt(cast(tuple[BatchTarget, ...], targets))
        self.assertIsNotNone(prompt)
        prompt = cast(str, prompt)
        self.assertLessEqual(len(prompt), REVIEW_BATCH_MAX_PROMPT_CODEPOINTS)
        payload = json.loads(prompt.rsplit("\n", 1)[1])
        self.assertEqual(payload["version"], "batch-v1")
        self.assertEqual(len(payload["targets"]), 2)
        for item in payload["targets"]:
            self.assertEqual(
                set(item),
                {"id", "before_target", "target", "after_target",
                 "truncated_before", "truncated_after"},
            )
        self.assertEqual(payload["targets"][1]["target"], "presenetliv")

    def test_prompt_oversize_returns_none(self) -> None:
        big = BatchTarget("t0", "x" * 10_000, "y", "", True, False)
        self.assertIsNone(build_prompt((big,)))

    def test_request_body_exact_shape(self) -> None:
        prompt = build_prompt(
            (BatchTarget("t0", "a", "b", "c", False, False),)
        )
        body = build_request_body("test-model", cast(str, prompt))
        value = json.loads(body)
        self.assertEqual(
            set(value),
            {"model", "stream", "store", "max_output_tokens", "input"},
        )
        self.assertEqual(value["model"], "test-model")
        self.assertIs(value["stream"], False)
        self.assertIs(value["store"], False)
        self.assertEqual(value["max_output_tokens"], 1536)
        self.assertEqual(value["input"], [
            {"role": "user", "content": [{"type": "input_text", "text": prompt}]}
        ])

    def test_codepoints_and_bytes_are_distinct(self) -> None:
        prompt = build_prompt(
            (BatchTarget("t0", "\U0001F600" * 10, "b", "", True, False),)
        )
        body = build_request_body("m", cast(str, prompt))
        self.assertGreater(len(body), len(cast(str, prompt)))


class StrictParserTests(unittest.TestCase):
    def _envelope_text(self, envelope: dict[str, object]) -> str:
        return json.dumps(envelope, ensure_ascii=False)

    def test_valid_envelope_maps_by_id_in_any_order(self) -> None:
        # Response order deliberately differs from the supplied id order:
        # proposals must map by validated id, never array position.
        inner = _valid_inner([_prop("t1", keep=True, replacement=None), _prop("t0")])
        envelope = _envelope(inner)
        result = parse_batch_envelope(
            strict_json_object(self._envelope_text(envelope)), frozenset({"t0", "t1"})
        )
        self.assertEqual(set(result), {"t0", "t1"})
        self.assertEqual(result["t0"].keep, False)
        self.assertEqual(result["t0"].replacement, "tako")
        self.assertEqual(result["t1"].keep, True)
        self.assertIsNone(result["t1"].replacement)

    def _reject(self, envelope: dict[str, object], expected: str,
                ids: frozenset[str] = frozenset({"t0", "t1"})) -> None:
        with self.assertRaises(batch_review.BatchError) as ctx:
            parse_batch_envelope(strict_json_object(self._envelope_text(envelope)), ids)
        self.assertEqual(ctx.exception.reason, expected)

    def test_not_completed(self) -> None:
        good = _valid_inner([_prop("t0"), _prop("t1")])
        self._reject(_envelope(good, status="failed"), "REVIEW_NOT_COMPLETED")
        self._reject(_envelope(good, etype="message"), "REVIEW_NOT_COMPLETED")
        self._reject(_envelope(good, error={"code": "x"}), "REVIEW_NOT_COMPLETED")

    def test_unsupported_output(self) -> None:
        good = _valid_inner([_prop("t0"), _prop("t1")])
        self._reject(_envelope(good, items=[{"type": "tool", "name": "x"}]),
                     "REVIEW_UNSUPPORTED_OUTPUT")
        self._reject(_envelope(good, items=[{"type": "message", "role": "user",
                     "content": []}]), "REVIEW_UNSUPPORTED_OUTPUT")
        self._reject(_envelope(good, parts=[{"type": "input_text", "text": "x"}]),
                     "REVIEW_UNSUPPORTED_OUTPUT")
        self._reject(_envelope("", items=[{"type": "message", "role": "assistant",
                     "content": "no list"}]), "REVIEW_UNSUPPORTED_OUTPUT")
        self._reject(_envelope("", items=[{"type": "refusal", "content": []}]),
                     "REVIEW_UNSUPPORTED_OUTPUT")

    def test_output_count(self) -> None:
        self._reject(_envelope("", items=[]), "REVIEW_OUTPUT_COUNT")
        two_parts: list[dict[str, object]] = [
            {"type": "output_text", "text": _valid_inner([_prop("t0")])},
            {"type": "output_text", "text": _valid_inner([_prop("t1")])},
        ]
        self._reject(_envelope("", parts=two_parts), "REVIEW_OUTPUT_COUNT")

    def test_output_oversize(self) -> None:
        too_long = "x" * (REVIEW_BATCH_MAX_PROPOSAL_JSON_CODEPOINTS + 1)
        self._reject(_envelope(too_long), "REVIEW_OUTPUT_OVERSIZE")

    def test_inner_schema(self) -> None:
        self._reject(_envelope(json.dumps({"version": "batch-v1"})), "REVIEW_SCHEMA")
        self._reject(
            _envelope(json.dumps({"version": "batch-v1", "proposals": {"id": "t0"}})),
            "REVIEW_SCHEMA",
        )
        self._reject(
            _envelope(json.dumps({"version": "batch-v1", "proposals": "x"})),
            "REVIEW_SCHEMA",
        )
        self._reject(_envelope(json.dumps(
            {"version": "batch-v1", "proposals": ["x"]})), "REVIEW_SCHEMA")
        self._reject(_envelope(json.dumps(
            {"version": "batch-v1", "proposals": [
                {"id": "t0", "keep": False, "replacement": "tako",
                 "needs_wider_edit": False, "extra": 1}]})), "REVIEW_SCHEMA")
        self._reject(_envelope(json.dumps(
            {"version": "batch-v1", "proposals": [
                {"id": "t0", "keep": 1, "replacement": "tako",
                 "needs_wider_edit": False}]})), "REVIEW_SCHEMA")
        self._reject(_envelope(json.dumps(
            {"version": "batch-v1", "proposals": [
                {"id": "t0", "keep": False, "replacement": 5,
                 "needs_wider_edit": False}]})), "REVIEW_SCHEMA")
        self._reject(_envelope(json.dumps(
            {"version": "batch-v1", "proposals": [
                {"id": 0, "keep": False, "replacement": "tako",
                 "needs_wider_edit": False}]})), "REVIEW_SCHEMA")

    def test_version_mismatch(self) -> None:
        self._reject(_envelope(json.dumps(
            {"version": "batch-v2", "proposals": [_prop("t0"), _prop("t1")]})),
            "REVIEW_VERSION")

    def test_unknown_duplicate_missing_id(self) -> None:
        self._reject(_envelope(_valid_inner([_prop("t9"), _prop("t1")])),
                     "REVIEW_UNKNOWN_ID")
        self._reject(_envelope(_valid_inner([_prop("t0"), _prop("t0"), _prop("t1")])),
                     "REVIEW_DUPLICATE_ID", frozenset({"t0", "t1"}))
        self._reject(_envelope(_valid_inner([_prop("t0")])), "REVIEW_MISSING_ID")

    def test_contradictory_states(self) -> None:
        cases = [
            [_prop("t0", keep=True, replacement="tako"), _prop("t1")],
            [_prop("t0"), _prop("t1", wider=True, replacement="tako")],
            [_prop("t0"), _prop("t1", keep=False, wider=True)],
            [_prop("t0", replacement=None), _prop("t1")],
        ]
        for proposals in cases:
            self._reject(_envelope(_valid_inner(proposals)), "REVIEW_SCHEMA")

    def test_replacement_oversize(self) -> None:
        self._reject(_envelope(_valid_inner(
            [_prop("t0", replacement="a b c d e f g h i"), _prop("t1")])),
            REASON_REPLACEMENT_OVERSIZE)
        self._reject(_envelope(_valid_inner(
            [_prop("t0", replacement="x" * 129), _prop("t1")])),
            REASON_REPLACEMENT_OVERSIZE)

    def test_fenced_and_invalid_json(self) -> None:
        with self.assertRaises(batch_review.BatchError) as ctx:
            strict_json_object("```json\n{}\n```")
        self.assertEqual(ctx.exception.reason, "REVIEW_FENCED_OUTPUT")
        with self.assertRaises(batch_review.BatchError) as ctx:
            strict_json_object('{"a":1} trailing')
        self.assertEqual(ctx.exception.reason, "REVIEW_INVALID_JSON")
        with self.assertRaises(batch_review.BatchError) as ctx:
            strict_json_object("[1, 2]")
        self.assertEqual(ctx.exception.reason, "REVIEW_INVALID_JSON")

    def test_duplicate_keys_rejected_at_both_levels(self) -> None:
        outer = (
            '{"type":"response","type":"response","status":"completed",'
            '"output":[{"type":"message","role":"assistant","content":'
            '[{"type":"output_text","text":"'
            + _valid_inner([_prop("t0"), _prop("t1")]).replace('"', '\\"')
            + '"}]}]}'
        )
        with self.assertRaises(batch_review.BatchError) as ctx:
            strict_json_object(outer)
        self.assertEqual(ctx.exception.reason, "REVIEW_DUPLICATE_KEY")
        inner = '{"version":"batch-v1","version":"batch-v1","proposals":[]}'
        with self.assertRaises(batch_review.BatchError) as ctx:
            strict_json_object(inner)
        self.assertEqual(ctx.exception.reason, "REVIEW_DUPLICATE_KEY")

    def test_nonfinite_number_rejected(self) -> None:
        with self.assertRaises(batch_review.BatchError) as ctx:
            strict_json_object('{"version": NaN}')
        self.assertEqual(ctx.exception.reason, "REVIEW_INVALID_NUMBER")

    def test_numeric_overflow_rejected(self) -> None:
        for bad in ('{"a": 1e999}', '{"a": 1e400}'):
            with self.subTest(bad=bad):
                with self.assertRaises(batch_review.BatchError) as ctx:
                    strict_json_object(bad)
                self.assertEqual(ctx.exception.reason, "REVIEW_INVALID_NUMBER")

    def test_empty_replacement_rejected(self) -> None:
        # A structurally valid first proposal cannot survive an invalid
        # second one: the whole batch is rejected.
        self._reject(
            _envelope(_valid_inner([_prop("t0"), _prop("t1", replacement="")])),
            "REVIEW_SCHEMA",
        )
        self._reject(
            _envelope(_valid_inner([_prop("t0", replacement=""), _prop("t1")])),
            "REVIEW_SCHEMA",
        )
        self._reject(
            _envelope(_valid_inner([_prop("t0"), _prop("t1", replacement="   ")])),
            "REVIEW_SCHEMA",
        )

    def test_incomplete_message_marker_rejected(self) -> None:
        good = _valid_inner([_prop("t0"), _prop("t1")])
        items = [
            {
                "type": "message",
                "role": "assistant",
                "status": "incomplete",
                "content": [{"type": "output_text", "text": good}],
            }
        ]
        self._reject(_envelope("", items=items), "REVIEW_NOT_COMPLETED")
        self._reject(
            _envelope("", items=[
                {"type": "message", "role": "assistant", "status": "completed",
                 "content": [{"type": "output_text", "text": good}]},
                {"type": "message", "role": "assistant", "status": "incomplete",
                 "content": []},
            ]),
            "REVIEW_NOT_COMPLETED",
        )


class _FakeUpstream(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    payload: bytes = b"{}"
    status: int = 200
    delay: float = 0.0
    recorded: list[dict[str, object]] = []

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.__class__.recorded.append(
            {"path": self.path, "headers": dict(self.headers.items()), "body": body}
        )
        if self.delay:
            time.sleep(self.delay)
        self.send_response(self.status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(self.payload)))
        self.end_headers()
        self.wfile.write(self.payload)

    def log_message(self, *_args: object) -> None:
        return


class TransportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]
        _FakeUpstream.recorded = []
        _FakeUpstream.payload = b"{}"
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        self.reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.port}/v1", "test-model", timeout=2.0,
            api_key="fake-key",
        )
        self.targets = prepare_targets(TEXT, _occurrences(TEXT), ()) or ()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(5)
        self.temp.cleanup()

    def _done(self) -> dict[str, BatchProposal]:
        _FakeUpstream.payload = json.dumps(
            _envelope(_valid_inner([_prop("t1"), _prop("t0")])),
            ensure_ascii=False,
        ).encode()
        return self.reviewer.review_batch(TEXT, self.targets)

    def test_single_request_exact_route_body_and_reordered_result(self) -> None:
        result = self._done()
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        record = _FakeUpstream.recorded[0]
        self.assertEqual(record["path"], "/v1/responses")
        headers = cast(dict[str, str], record["headers"])
        self.assertEqual(headers.get("Authorization"), "Bearer fake-key")
        self.assertEqual(headers.get("Content-Type"), "application/json")
        value = json.loads(cast(bytes, record["body"]))
        expected_prompt = cast(str, build_prompt(self.targets))
        self.assertEqual(value["input"][0]["content"][0]["text"], expected_prompt)
        self.assertEqual(value["model"], "test-model")
        self.assertIs(value["stream"], False)
        self.assertIs(value["store"], False)
        self.assertEqual(value["max_output_tokens"], 1536)
        self.assertEqual(set(result), {"t0", "t1"})
        self.assertEqual(result["t0"].replacement, "tako")
        self.assertEqual(result["t1"].replacement, "tako")

    def test_non_200_fails_whole_batch(self) -> None:
        _FakeUpstream.status = 500
        _FakeUpstream.payload = b'{"error": "x"}'
        with self.assertRaises(ReviewerError) as ctx:
            self.reviewer.review_batch(TEXT, self.targets)
        self.assertEqual(ctx.exception.reason, REASON_HTTP_NOT_OK)
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_oversized_response_rejected(self) -> None:
        _FakeUpstream.payload = b"x" * (REVIEW_BATCH_MAX_RESPONSE_BYTES + 1)
        with self.assertRaises(ReviewerError) as ctx:
            self.reviewer.review_batch(TEXT, self.targets)
        self.assertEqual(ctx.exception.reason, REASON_HTTP_NOT_OK)

    def test_invalid_utf8_rejected(self) -> None:
        _FakeUpstream.payload = b"\xff\xfe\xfd{}"
        with self.assertRaises(ReviewerError) as ctx:
            self.reviewer.review_batch(TEXT, self.targets)
        self.assertEqual(ctx.exception.reason, REASON_INVALID_ENCODING)

    def test_timeout_rejected(self) -> None:
        _FakeUpstream.delay = 5.0
        self.reviewer.timeout = 1.0
        started = time.monotonic()
        with self.assertRaises(ReviewerError) as ctx:
            self.reviewer.review_batch(TEXT, self.targets)
        self.assertLess(time.monotonic() - started, 4.0)
        self.assertEqual(ctx.exception.reason, REASON_HTTP_FAILED)
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_prompt_oversize_fails_before_dispatch(self) -> None:
        oversized = (BatchTarget("t0", "x" * 10_000, "y", "", True, False),)
        with self.assertRaises(ReviewerError) as ctx:
            self.reviewer.review_batch(TEXT, oversized)
        self.assertEqual(ctx.exception.reason, REASON_PROMPT_OVERSIZE)
        self.assertEqual(_FakeUpstream.recorded, [])

    def test_request_oversize_fails_before_dispatch(self) -> None:
        big = (BatchTarget("t0", "\U0001F600" * 8000, "b", "", True, True),)
        with mock.patch.object(
            batch_review, "REVIEW_BATCH_MAX_PROMPT_CODEPOINTS", 10**9
        ), self.assertRaises(ReviewerError) as ctx:
            self.reviewer.review_batch(TEXT, big)
        self.assertEqual(ctx.exception.reason, REASON_REQUEST_OVERSIZE)
        self.assertEqual(_FakeUpstream.recorded, [])

    def test_outer_duplicate_key_rejected_by_real_transport(self) -> None:
        inner = _valid_inner([_prop("t0"), _prop("t1")]).replace('"', '\\"')
        wrapper = (
            '{"type":"response","type":"response","status":"completed",'
            '"output":[{"type":"message","role":"assistant","content":'
            '[{"type":"output_text","text":"' + inner + '"}]}]}'
        )
        _FakeUpstream.payload = wrapper.encode()
        with self.assertRaises(ReviewerError) as ctx:
            self.reviewer.review_batch(TEXT, self.targets)
        self.assertEqual(ctx.exception.reason, "REVIEW_DUPLICATE_KEY")
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_failure_after_first_valid_item_rejects_whole_batch(self) -> None:
        # First item acceptable, second item a duplicate id: the whole
        # batch must be rejected after exactly one request.
        _FakeUpstream.payload = json.dumps(
            _envelope(_valid_inner([_prop("t0"), _prop("t0"), _prop("t1")])),
            ensure_ascii=False,
        ).encode()
        with self.assertRaises(ReviewerError) as ctx:
            self.reviewer.review_batch(TEXT, self.targets)
        self.assertEqual(ctx.exception.reason, REASON_DUPLICATE_ID)
        self.assertEqual(len(_FakeUpstream.recorded), 1)


Responder = Callable[[str, tuple[BatchTarget, ...]], dict[str, BatchProposal]]


class _ScriptedBatchReviewer:
    def __init__(self, responder: Responder) -> None:
        self.responder = responder
        self.calls = 0
        self.sent: list[tuple[str, tuple[BatchTarget, ...]]] = []

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> dict[str, BatchProposal]:
        self.calls += 1
        self.sent.append((sentence, targets))
        return self.responder(sentence, targets)


def _replace_all(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
    return {t.id: BatchProposal(t.id, False, "tako", False) for t in targets}


class EngineBatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        import proxy

        self.proxy_module = proxy

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _engine(self, reviewer: object) -> RepairEngine:
        return RepairEngine(self.db, reviewer, pandoc=_real_spec())  # type: ignore[arg-type]

    def test_two_targets_one_request_both_accepted(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_all)
        engine = self._engine(reviewer)
        engine.begin_request()
        repaired = engine.repair(TEXT)
        self.assertEqual(repaired, "To je tako zapisano, to je tako zapisano.")
        self.assertEqual(reviewer.calls, 1)
        details = engine.take_details()
        self.assertEqual(len(details), 1)
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(batch, {"calls": 1, "targets": 2, "outcome": "ok", "reason": None})
        acceptance = cast(list[dict[str, object]], details[0]["acceptance"])
        self.assertTrue(all(item["accepted"] for item in acceptance))
        self.assertEqual(cast(list[object], details[0]["replacements"]), ["tako", "tako"])

    def test_repeated_occurrences_get_separate_ids_and_exact_context(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_all)
        engine = self._engine(reviewer)
        repaired = engine.repair(TEXT)
        self.assertEqual(repaired, "To je tako zapisano, to je tako zapisano.")
        sentence, targets = reviewer.sent[0]
        self.assertEqual(sentence, TEXT)
        self.assertEqual([t.id for t in targets], ["t0", "t1"])
        self.assertEqual(targets[0].before_target, "To je ")
        self.assertEqual(targets[1].before_target, "To je presenetliv zapisano, to je ")
        self.assertNotEqual(targets[0].before_target, targets[1].before_target)

    def test_keep_is_noop(self) -> None:
        def responder(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
            result = {t.id: BatchProposal(t.id, False, "tako", False) for t in targets}
            result[targets[1].id] = BatchProposal(targets[1].id, True, None, False)
            return result

        reviewer = _ScriptedBatchReviewer(responder)
        engine = self._engine(reviewer)
        engine.begin_request()
        repaired = engine.repair(TEXT)
        self.assertEqual(repaired, "To je tako zapisano, to je presenetliv zapisano.")
        self.assertEqual(reviewer.calls, 1)
        details = engine.take_details()
        acceptance = cast(list[dict[str, object]], details[0]["acceptance"])
        self.assertTrue(acceptance[0]["accepted"])
        self.assertFalse(acceptance[1]["accepted"])
        self.assertEqual(acceptance[1]["reason"], "reviewer-kept")

    def test_wider_is_noop(self) -> None:
        def responder(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
            result = {t.id: BatchProposal(t.id, False, "tako", False) for t in targets}
            result[targets[1].id] = BatchProposal(targets[1].id, True, None, True)
            return result

        reviewer = _ScriptedBatchReviewer(responder)
        engine = self._engine(reviewer)
        engine.begin_request()
        repaired = engine.repair(TEXT)
        self.assertEqual(repaired, "To je tako zapisano, to je presenetliv zapisano.")
        details = engine.take_details()
        acceptance = cast(list[dict[str, object]], details[0]["acceptance"])
        # Wider proposals must be keep+null-replacement, so the recorded
        # no-op reason is the keep reason; no edit is applied.
        self.assertEqual(acceptance[1]["reason"], "reviewer-kept")

    def test_independent_evidence_rejection(self) -> None:
        def responder(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
            result = {t.id: BatchProposal(t.id, False, "tako", False) for t in targets}
            # "to" is structurally valid but has no local corpus evidence
            # with these neighbors, so current evidence rejects it alone.
            result[targets[1].id] = BatchProposal(targets[1].id, False, "to", False)
            return result

        reviewer = _ScriptedBatchReviewer(responder)
        engine = self._engine(reviewer)
        engine.begin_request()
        repaired = engine.repair(TEXT)
        self.assertEqual(repaired, "To je tako zapisano, to je presenetliv zapisano.")
        details = engine.take_details()
        acceptance = cast(list[dict[str, object]], details[0]["acceptance"])
        self.assertTrue(acceptance[0]["accepted"])
        self.assertFalse(acceptance[1]["accepted"])
        self.assertEqual(acceptance[1]["reason"], "local-evidence-not-stronger")

    def test_no_candidates_zero_calls(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_all)
        engine = self._engine(reviewer)
        engine.begin_request()
        text = "To je zapisano."
        self.assertEqual(engine.repair(text), text)
        self.assertEqual(reviewer.calls, 0)
        details = engine.take_details()
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(batch, {"calls": 0, "targets": 0, "outcome": "skipped", "reason": None})

    def test_schema_failure_returns_exact_original(self) -> None:
        def responder(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
            raise ReviewerError("synthetic failure", reason=REASON_DUPLICATE_ID)

        reviewer = _ScriptedBatchReviewer(responder)
        engine = self._engine(reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(TEXT), TEXT)
        self.assertEqual(reviewer.calls, 1)
        details = engine.take_details()
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(
            batch, {"calls": 1, "targets": 2, "outcome": "failed", "reason": REASON_DUPLICATE_ID}
        )
        decisions = cast(list[dict[str, object]], details[0]["reviewer_decisions"])
        self.assertEqual(len(decisions), 2)
        for decision in decisions:
            self.assertIsNone(decision["proposal"])
            self.assertEqual(decision["failure"], "reviewer-error")

    def test_unlabeled_failure_maps_to_review_failed(self) -> None:
        def responder(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
            raise ReviewerError("synthetic failure")

        reviewer = _ScriptedBatchReviewer(responder)
        engine = self._engine(reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(TEXT), TEXT)
        details = engine.take_details()
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(batch["reason"], REASON_FAILED)
        self.assertEqual(batch["calls"], 1)

    def test_untrusted_exception_never_stringified(self) -> None:
        marker = "SECRETCANDIDATE"

        def responder(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
            raise RuntimeError(marker)

        reviewer = _ScriptedBatchReviewer(responder)
        engine = self._engine(reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(TEXT), TEXT)
        details = engine.take_details()
        rendered = json.dumps(details, ensure_ascii=False, default=str)
        self.assertNotIn(marker, rendered)
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(batch["reason"], REASON_FAILED)

    def test_synthetic_review_reason_maps_to_review_failed(self) -> None:
        marker = "CANARY014"

        def responder(
            sentence: str, targets: tuple[BatchTarget, ...]
        ) -> dict[str, BatchProposal]:
            raise ReviewerError("synthetic failure", reason="REVIEW_" + marker)

        reviewer = _ScriptedBatchReviewer(responder)
        engine = self._engine(reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(TEXT), TEXT)
        details = engine.take_details()
        rendered = json.dumps(details, ensure_ascii=False, default=str)
        self.assertNotIn(marker, rendered)
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(batch["reason"], REASON_FAILED)
        self.assertEqual(batch["calls"], 1)

    def test_request_oversize_records_zero_calls(self) -> None:
        def responder(sentence: str, targets: tuple[BatchTarget, ...]) -> dict[str, BatchProposal]:
            raise ReviewerError("synthetic failure", reason=REASON_REQUEST_OVERSIZE)

        reviewer = _ScriptedBatchReviewer(responder)
        engine = self._engine(reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(TEXT), TEXT)
        details = engine.take_details()
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(
            batch,
            {"calls": 0, "targets": 2, "outcome": "failed", "reason": REASON_REQUEST_OVERSIZE},
        )

    def test_stale_candidate_returns_original_without_calls(self) -> None:
        def stale_detect(text: str, corpus: object, intervals: object,
                         mode: str = "local-context", maximum: int = 4) -> list[Candidate]:
            start = text.index("presenetliv")
            return [Candidate(start, start + 10, "presenetliv", 1.0, {})]

        reviewer = _ScriptedBatchReviewer(_replace_all)
        engine = self._engine(reviewer)
        engine.begin_request()
        with mock.patch.object(self.proxy_module, "detect", stale_detect):
            self.assertEqual(engine.repair(TEXT), TEXT)
        self.assertEqual(reviewer.calls, 0)
        details = engine.take_details()
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(
            batch,
            {"calls": 0, "targets": 1, "outcome": "skipped", "reason": REASON_PREP_INVALID},
        )

    def test_mixed_valid_and_unmatched_candidate_zero_calls(self) -> None:
        # Two valid detected candidates plus one beyond-EOF candidate whose
        # start matches no token: the whole selection is invalid/stale, so
        # the answer returns the completed original with zero calls instead
        # of reviewing the valid subset (order 014-a, requirement 2).
        def mixed_detect(text: str, corpus: Corpus, intervals: list[Interval] | None,
                         mode: str = "local-context", maximum: int = 4) -> list[Candidate]:
            real = detect(text, corpus, intervals, mode=mode, maximum=maximum)
            return [
                *real,
                Candidate(len(text) + 5, len(text) + 16, "presenetliv", 1.0, {}),
            ]

        reviewer = _ScriptedBatchReviewer(_replace_all)
        engine = self._engine(reviewer)
        engine.begin_request()
        with mock.patch.object(self.proxy_module, "detect", mixed_detect):
            self.assertEqual(engine.repair(TEXT), TEXT)
        self.assertEqual(reviewer.calls, 0)
        details = engine.take_details()
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(
            batch,
            {"calls": 0, "targets": 3, "outcome": "skipped", "reason": REASON_PREP_INVALID},
        )

    def test_prompt_oversize_returns_original_without_calls(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_all)
        engine = self._engine(reviewer)
        engine.begin_request()
        with mock.patch.object(self.proxy_module, "build_prompt", lambda targets: None):
            self.assertEqual(engine.repair(TEXT), TEXT)
        self.assertEqual(reviewer.calls, 0)
        details = engine.take_details()
        batch = cast(dict[str, object], details[0]["review_batch"])
        self.assertEqual(
            batch,
            {"calls": 0, "targets": 2, "outcome": "skipped", "reason": REASON_PROMPT_OVERSIZE},
        )


class _CountingRepair:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, value: str) -> str:
        self.calls += 1
        return value.replace("presenetliv", "tako")


def _sse_delta(item_id: str, text: str) -> bytes:
    payload = (
        '{"type":"response.output_text.delta","item_id":"'
        + item_id
        + '","delta":' + json.dumps(text) + '}'
    )
    return f"data: {payload}\n\n".encode()


def _sse_completed(response: Mapping[str, object] | None = None) -> bytes:
    if response is None:
        # A confirming completed envelope for the default single delta
        # answer "m": exactly one assistant output_text at position 0/0
        # (order 014-a, requirement 8).
        response = {
            "id": "r",
            "usage": {"total_tokens": 4},
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
    return (
        'data: {"type":"response.completed","response":'
        + json.dumps(response)
        + "}\n\n"
    ).encode()


class SseGuardTests(unittest.TestCase):
    def test_multi_answer_delta_streams_bypass(self) -> None:
        raw = (
            _sse_delta("m1", "To je presenetliv zapisano.")
            + _sse_delta("m2", "To je presenetliv zapisano.")
            + _sse_completed()
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_single_answer_delta_stream_repairs_once(self) -> None:
        raw = _sse_delta("m", TEXT) + _sse_completed()
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        self.assertIn(b"To je tako zapisano, to je tako zapisano.", result)

    def test_completed_multiple_output_fields_bypass(self) -> None:
        fields = [
            {"type": "output_text", "text": "To je presenetliv zapisano."},
            {"type": "output_text", "text": "Drugo presenetliv besedilo."},
        ]
        raw = _sse_completed(
            {"id": "r", "output": [
                {"type": "message", "role": "assistant", "content": fields}
            ]}
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_metadata_echo_is_never_mutated(self) -> None:
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "id": "m",
                    "content": [{"type": "output_text", "text": answer}],
                }
            ],
            "metadata": {"echo": {"type": "output_text", "text": answer}},
        }
        raw = _sse_delta("m", answer) + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        # The one answer is rewritten in both of its valid SSE positions
        # (the delta event and the validated completed part); only the
        # nested metadata echo with identical text stays byte-identical.
        self.assertEqual(result.count(b"presenetliv"), 1)
        self.assertEqual(result.count(b"tako"), 2)
        self.assertIn(
            b'"metadata":{"echo":{"type":"output_text","text":"To je presenetliv zapisano."}}',
            result,
        )

    def test_delta_plus_two_completed_messages_bypass(self) -> None:
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "id": "m",
                    "content": [{"type": "output_text", "text": answer}],
                },
                {
                    "type": "message",
                    "role": "assistant",
                    "id": "m2",
                    "content": [{"type": "output_text", "text": "Drugo."}],
                },
            ],
        }
        raw = _sse_delta("m", answer) + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_two_content_parts_same_item_bypass(self) -> None:
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "id": "m",
                    "content": [
                        {"type": "output_text", "text": answer},
                        {"type": "output_text", "text": answer},
                    ],
                }
            ],
        }
        raw = _sse_delta("m", answer) + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_completed_item_id_mismatch_bypass(self) -> None:
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "id": "m2",
                    "content": [{"type": "output_text", "text": answer}],
                }
            ],
        }
        raw = _sse_delta("m", answer) + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_completed_single_field_repairs_once(self) -> None:
        raw = _sse_completed(
            {"id": "r", "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": "To je presenetliv zapisano.",
                     "content_index": 0}
                ]}
            ]}
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        self.assertIn(b"tako", result)

    def test_delta_output_index_mismatch_bypass(self) -> None:
        # The stream event declares output_index=1 while the completed
        # message sits at output[0]: contradictory ownership, zero calls.
        answer = "To je presenetliv zapisano."
        delta = (
            'data: {"type":"response.output_text.delta","item_id":"m",'
            '"output_index":1,"content_index":0,"delta":'
            + json.dumps(answer)
            + "}\n\n"
        ).encode()
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = delta + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_delta_content_index_mismatch_bypass(self) -> None:
        # The stream event declares content_index=1 while the completed
        # part sits at content[0]: contradictory ownership, zero calls.
        answer = "To je presenetliv zapisano."
        delta = (
            'data: {"type":"response.output_text.delta","item_id":"m",'
            '"output_index":0,"content_index":1,"delta":'
            + json.dumps(answer)
            + "}\n\n"
        ).encode()
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = delta + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_stream_indices_consistent_repairs_once(self) -> None:
        # Declared stream positions equal to the actual final positions are
        # consistent ownership: the single answer is still reviewed once.
        answer = "To je presenetliv zapisano."
        delta = (
            'data: {"type":"response.output_text.delta","item_id":"m",'
            '"output_index":0,"content_index":0,"delta":'
            + json.dumps(answer)
            + "}\n\n"
        ).encode()
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = delta + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        self.assertIn(b"tako", result)

    def test_no_accepted_edit_preserves_raw_bytes(self) -> None:
        # The review accepts no text edit: the raw SSE bytes are returned
        # exactly, including the completed event JSON encoding.
        raw = _sse_delta("m", TEXT) + _sse_completed()
        calls = {"count": 0}

        def count_identity(value: str) -> str:
            calls["count"] += 1
            return value

        result, changed = transform_sse(raw, count_identity)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(calls["count"], 1)

    def _typed_id_case(self, item_id_json: str, final_message_id: str) -> None:
        # A delta/done event whose item_id is missing, non-string or empty
        # is never coerced to an invented id, even when the completed
        # message declares that coerced value: zero calls, raw bytes.
        answer = "To je presenetliv zapisano."
        delta = (
            'data: {"type":"response.output_text.delta","item_id":'
            + item_id_json
            + ',"delta":' + json.dumps(answer) + "}\n\n"
        ).encode()
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": final_message_id, "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = delta + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_delta_int_item_id_bypass(self) -> None:
        # item_id=7 (int) must not be coerced to "7" and matched.
        self._typed_id_case("7", "7")

    def test_delta_null_item_id_bypass(self) -> None:
        # item_id=null must not be coerced to "None" and matched.
        self._typed_id_case("null", "None")

    def test_delta_missing_item_id_bypass(self) -> None:
        # A missing item_id must not be invented as "__single__".
        answer = "To je presenetliv zapisano."
        delta = (
            'data: {"type":"response.output_text.delta","delta":'
            + json.dumps(answer) + "}\n\n"
        ).encode()
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "__single__", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = delta + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_done_int_item_id_bypass(self) -> None:
        # A done event with a non-string id is answer-related too: the
        # whole stream abstains even though the delta id is valid.
        answer = "To je presenetliv zapisano."
        delta = _sse_delta("m", answer)
        done = (
            b'data: {"type":"response.output_text.done","item_id":7,'
            b'"text":' + json.dumps(answer).encode() + b"}\n\n"
        )
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = delta + done + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_valid_string_ids_delta_and_done_repaired(self) -> None:
        # Valid string ids on both the delta and the done event confirm the
        # single answer: one review call, both events carry the new text.
        answer = "To je presenetliv zapisano."
        delta = _sse_delta("m", answer)
        done = (
            b'data: {"type":"response.output_text.done","item_id":"m",'
            b'"text":' + json.dumps(answer).encode() + b"}\n\n"
        )
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = delta + done + _sse_completed(completed)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        # The delta is re-emitted once with the full repaired text and the
        # done event carries the same text; the answer is not duplicated.
        self.assertEqual(result.count(b"tako"), 3)
        self.assertNotIn(b"presenetliv", result)

    @staticmethod
    def _canonical_stream(answer: str) -> bytes:
        # The canonical one-answer terminal sequence: delta, content_part
        # done, output_item done, and the completed envelope.
        delta = (
            '{"type":"response.output_text.delta","item_id":"m","delta":'
            + json.dumps(answer)
            + "}"
        )
        part_done = (
            '{"type":"response.content_part.done","item_id":"m",'
            '"part":{"type":"output_text","text":' + json.dumps(answer) + "}}"
        )
        item_done = (
            '{"type":"response.output_item.done","item":{"id":"m",'
            '"type":"message","role":"assistant","status":"completed",'
            '"content":[{"type":"output_text","text":' + json.dumps(answer) + '}]}}'
        )
        completed = {
            "id": "r",
            "metadata": {"note": "unchanged"},
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        events = [delta, part_done, item_done,
                  '{"type":"response.completed","response":'
                  + json.dumps(completed) + "}"]
        return "".join("data: " + event + "\n\n" for event in events).encode()

    def test_terminal_copies_follow_repaired_answer(self) -> None:
        # Every known terminal copy of the confirmed answer (content_part
        # done part, output_item done message, completed part) carries the
        # repaired text; unrelated metadata stays byte-identical.
        answer = "To je presenetliv zapisano."
        raw = self._canonical_stream(answer)
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        self.assertNotIn(b"presenetliv", result)
        self.assertEqual(result.count(b"tako zapisano"), 4)
        self.assertIn(b'"metadata":{"note":"unchanged"}', result)

    def test_terminal_copies_not_duplicated_without_edit(self) -> None:
        # No accepted edit: the canonical stream is returned exactly, with
        # no copy injected into events that carried no text.
        answer = "To je presenetliv zapisano."
        raw = self._canonical_stream(answer)
        result, changed = transform_sse(raw, lambda value: value)
        self.assertEqual(result, raw)
        self.assertFalse(changed)

    def test_extra_done_for_other_id_bypass(self) -> None:
        # An answer event for another item id (even without its own delta
        # stream) means several answers: bypass unchanged, zero calls.
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = (
            _sse_delta("m", answer)
            + b'data: {"type":"response.output_text.done","item_id":"other",'
            b'"text":"Drugo."}\n\n'
            + _sse_completed(completed)
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_extra_output_item_message_for_other_id_bypass(self) -> None:
        # A message-typed output-item event for another id is an answer
        # event too: bypass unchanged, zero calls.
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = (
            _sse_delta("m", answer)
            + b'data: {"type":"response.output_item.done","item":{"id":"other",'
            b'"type":"message","role":"assistant","content":[]}}\n\n'
            + _sse_completed(completed)
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_output_item_done_for_non_message_item_ok(self) -> None:
        # A non-message output-item (e.g. tool bookkeeping) is not an
        # answer: the single confirmed answer is still reviewed once.
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {"type": "message", "id": "m", "role": "assistant",
                 "status": "completed", "output_index": 0, "content": [
                    {"type": "output_text", "text": answer, "content_index": 0}
                ]}
            ],
        }
        raw = (
            _sse_delta("m", answer)
            + b'data: {"type":"response.output_item.done","output_index":1,'
            b'"item":{"id":"tool-1","type":"function_call","name":"x"}}\n\n'
            + _sse_completed(completed)
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        self.assertIn(b"tako", result)


class _EphemeralUpstream(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    source: bytes = b""

    def do_POST(self) -> None:  # noqa: N802
        self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(self.__class__.source)))
        self.end_headers()
        self.wfile.write(self.__class__.source)

    def log_message(self, *_args: object) -> None:
        return


_TC_ANSWER = "To je presenetliv zapisano."
_TC_OTHER = "Nekaj drugacnega."


def _tc_raw(*events: bytes) -> bytes:
    return b"".join(b"data: " + event + b"\n\n" for event in events)


def _tc_delta(item_id: str = "m", text: str | None = None) -> bytes:
    return (
        '{"type":"response.output_text.delta","item_id":"'
        + item_id
        + '","delta":' + json.dumps(_TC_ANSWER if text is None else text) + "}"
    ).encode()


def _tc_part_done(
    text: str | None = None, with_id: bool = True, item_id: object = "m"
) -> bytes:
    payload = '{"type":"response.content_part.done"'
    if with_id:
        payload += ',"item_id":' + json.dumps(item_id)
    payload += (
        ',"part":{"type":"output_text","text":'
        + json.dumps(_TC_ANSWER if text is None else text)
        + "}}"
    )
    return payload.encode()


def _tc_item_done(
    parts: list[dict[str, object]] | None = None,
    role: str = "assistant",
    status: object = "completed",
    with_id: bool = True,
    output_index: int | None = None,
) -> bytes:
    item: dict[str, object] = {"type": "message"}
    if with_id:
        item["id"] = "m"
    item["role"] = role
    if status is not None:
        item["status"] = status
    item["content"] = (
        parts
        if parts is not None
        else [{"type": "output_text", "text": _TC_ANSWER}]
    )
    payload = '{"type":"response.output_item.done"'
    if output_index is not None:
        payload += ',"output_index":' + str(output_index)
    payload += ',"item":' + json.dumps(item) + "}"
    return payload.encode()


def _tc_done(text: str | None = None, item_id: object = "m") -> bytes:
    payload = (
        '{"type":"response.output_text.done","item_id":'
        + json.dumps(item_id)
        + ',"text":' + json.dumps(_TC_ANSWER if text is None else text)
        + "}"
    )
    return payload.encode()


def _tc_delta_payload(payload: object, with_field: bool = True) -> bytes:
    payload_json = '{"type":"response.output_text.delta","item_id":"m"'
    if with_field:
        payload_json += ',"delta":' + json.dumps(payload)
    return (payload_json + "}").encode()


def _tc_completed(output: list[dict[str, object]] | None = None) -> bytes:
    if output is None:
        output = [
            {
                "type": "message",
                "id": "m",
                "role": "assistant",
                "status": "completed",
                "output_index": 0,
                "content": [
                    {
                        "type": "output_text",
                        "text": _TC_ANSWER,
                        "content_index": 0,
                    }
                ],
            }
        ]
    return (
        '{"type":"response.completed","response":{"id":"r","output":'
        + json.dumps(output)
        + "}}"
    ).encode()


def _tc_completed_reasoning_then_message(text: str = _TC_ANSWER) -> bytes:
    # Protected non-answer reasoning bookkeeping plus the final answer at a
    # nonzero output_index (order 014-b, requirement 5).  Built with
    # json.dumps so the fixture is valid JSON by construction.
    response = {
        "id": "r",
        "output": [
            {
                "type": "reasoning",
                "id": "rs1",
                "status": "completed",
                "summary": [{"type": "summary_text", "text": "misel"}],
            },
            {
                "type": "message",
                "id": "m",
                "role": "assistant",
                "status": "completed",
                "output_index": 1,
                "content": [
                    {"type": "output_text", "text": text, "content_index": 0}
                ],
            },
        ],
    }
    return (
        '{"type":"response.completed","response":' + json.dumps(response) + "}"
    ).encode()


def _tc_completed_text_event(text: str, output_index: int = 0) -> bytes:
    # Unframed completed event (framed by _tc_raw) whose single final
    # answer copy carries the identical full answer text.  Built with
    # json.dumps so the fixture is valid JSON by construction.
    response = {
        "id": "r",
        "usage": {"total_tokens": 4},
        "output": [
            {
                "type": "message",
                "id": "m",
                "role": "assistant",
                "status": "completed",
                "output_index": output_index,
                "content": [
                    {"type": "output_text", "text": text, "content_index": 0}
                ],
            }
        ],
    }
    return (
        '{"type":"response.completed","response":' + json.dumps(response) + "}"
    ).encode()


def _tc_baseline(text: str = _TC_ANSWER) -> bytes:
    # The unmutated one-answer baseline: the identical full answer text in
    # every copy (delta, terminal part, terminal item, final answer).  Each
    # negative mutates exactly one named ownership/text field.
    return _tc_raw(
        _tc_delta("m", text),
        _tc_part_done(text=text),
        _tc_item_done(parts=[{"type": "output_text", "text": text}]),
        _tc_completed_text_event(text),
    )


class TerminalCopyOwnershipTests(unittest.TestCase):
    """Order 014-b: before any reviewer side effect, every answer-bearing
    terminal representation is validated against the one final assistant
    answer (exact typed id, final positions, part kind / role / status /
    content cardinality and kinds, exact original text, no duplicated
    copies).  Any copy that cannot be proved consistent makes the whole SSE
    ineligible: raw original, zero repair/reviewer calls."""

    def _bypass(self, raw: bytes) -> None:
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertEqual(result, raw)
        self.assertFalse(changed)
        self.assertEqual(repair.calls, 0)

    def test_multi_part_terminal_item_bypass(self) -> None:
        # (a) output_item.done carries two output_text parts: extra answer
        # copy with contradictory text.
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(),
                _tc_item_done(
                    parts=[
                        {"type": "output_text", "text": _TC_ANSWER},
                        {"type": "output_text", "text": _TC_OTHER},
                    ]
                ),
                _tc_completed(),
            )
        )

    def test_conflicting_content_part_text_bypass(self) -> None:
        # (b) content_part.done carries a different text than the final
        # answer.
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(text=_TC_OTHER),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_missing_id_content_part_bypass(self) -> None:
        # (c) content_part.done carries the answer text without any item_id.
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(with_id=False),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_null_id_content_part_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(item_id=None),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_int_id_content_part_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(item_id=7),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_wrong_role_terminal_item_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(),
                _tc_item_done(role="user"),
                _tc_completed(),
            )
        )

    def test_incomplete_status_terminal_item_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(),
                _tc_item_done(status="incomplete"),
                _tc_completed(),
            )
        )

    def test_conflicting_terminal_item_text_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(),
                _tc_item_done(parts=[{"type": "output_text", "text": _TC_OTHER}]),
                _tc_completed(),
            )
        )

    def test_missing_id_message_item_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(),
                _tc_item_done(with_id=False),
                _tc_completed(),
            )
        )

    def test_content_cardinality_mismatch_terminal_item_bypass(self) -> None:
        # A terminal item with an extra part kind beyond the final message
        # content is not a consistent copy.
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(),
                _tc_item_done(
                    parts=[
                        {"type": "output_text", "text": _TC_ANSWER},
                        {"type": "refusal", "content": "x"},
                    ]
                ),
                _tc_completed(),
            )
        )

    def test_wrong_content_index_terminal_part_bypass(self) -> None:
        event = (
            '{"type":"response.content_part.done","item_id":"m",'
            '"output_index":0,"content_index":5,'
            '"part":{"type":"output_text","text":'
            + json.dumps(_TC_ANSWER)
            + "}}"
        ).encode()
        self._bypass(_tc_raw(_tc_delta(), event, _tc_item_done(), _tc_completed()))

    def test_conflicting_output_text_done_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_done(text=_TC_OTHER),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_output_text_done_without_text_bypass(self) -> None:
        # A terminal done event that carries no text cannot be proved
        # consistent with the confirmed answer.
        event = (
            b'{"type":"response.output_text.done","item_id":"m"}'
        )
        self._bypass(_tc_raw(_tc_delta(), event, _tc_item_done(), _tc_completed()))

    def test_duplicate_terminal_part_copies_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_part_done(),
                _tc_part_done(),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_added_placeholders_ownership_validated_and_protected(self) -> None:
        # Initial added events may be empty placeholders: their ownership is
        # validated, their content is protected, and they are never treated
        # as terminal copies.
        part_added = (
            b'{"type":"response.content_part.added","item_id":"m",'
            b'"part":{"type":"output_text","text":""}}'
        )
        item_added = (
            b'{"type":"response.output_item.added","item":{"id":"m",'
            b'"type":"message","role":"assistant","content":[]}}'
        )
        raw = _tc_raw(
            part_added,
            item_added,
            _tc_delta(),
            _tc_part_done(),
            _tc_item_done(),
            _tc_completed(),
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        self.assertIn(
            b'"type":"response.content_part.added","item_id":"m",'
            b'"part":{"type":"output_text","text":""}',
            result,
        )
        self.assertIn(
            b'"type":"response.output_item.added","item":{"id":"m",'
            b'"type":"message","role":"assistant","content":[]}',
            result,
        )

    def test_added_event_other_id_bypass(self) -> None:
        # An added output_text part for another id is an answer event for
        # that id: ambiguous ownership, bypass unchanged.
        part_added = (
            b'{"type":"response.content_part.added","item_id":"other",'
            b'"part":{"type":"output_text","text":""}}'
        )
        self._bypass(
            _tc_raw(part_added, _tc_delta(), _tc_part_done(), _tc_completed())
        )

    def test_added_part_nonempty_conflicting_text_bypass(self) -> None:
        # An added output_text part with non-empty initial content cannot
        # be proved safe: abstain raw unchanged with zero calls, and the
        # protected added content is never rewritten.
        part_added = (
            '{"type":"response.content_part.added","item_id":"m",'
            '"part":{"type":"output_text","text":'
            + json.dumps(_TC_OTHER)
            + "}}"
        ).encode()
        self._bypass(
            _tc_raw(
                part_added,
                _tc_delta(),
                _tc_part_done(),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_added_item_wrong_role_status_bypass(self) -> None:
        # An initial message item for the confirmed id with a wrong role
        # and a non-terminal status marker is not a consistent initial
        # representation: bypass unchanged with zero calls.
        item_added = (
            b'{"type":"response.output_item.added","item":{"id":"m",'
            b'"type":"message","role":"user","status":"in_progress",'
            b'"content":[]}}'
        )
        self._bypass(
            _tc_raw(
                item_added,
                _tc_delta(),
                _tc_part_done(),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_added_placeholders_reasoning_nonzero_index_positive(self) -> None:
        # The valid empty-placeholder positive with protected reasoning and
        # the final message at a nonzero output_index: one repair, added
        # placeholders byte-identical, reasoning untouched.
        part_added = (
            b'{"type":"response.content_part.added","item_id":"m",'
            b'"part":{"type":"output_text","text":""}}'
        )
        item_added = (
            b'{"type":"response.output_item.added","item":{"id":"m",'
            b'"type":"message","role":"assistant","status":"in_progress",'
            b'"content":[]}}'
        )
        raw = _tc_raw(
            part_added,
            item_added,
            _tc_delta(),
            _tc_part_done(),
            _tc_item_done(output_index=1),
            _tc_completed_reasoning_then_message(),
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        self.assertNotIn(b"presenetliv", result)
        self.assertEqual(result.count(b"To je tako zapisano."), 4)
        self.assertIn(
            b'"type":"response.content_part.added","item_id":"m",'
            b'"part":{"type":"output_text","text":""}',
            result,
        )
        self.assertIn(
            b'"type":"response.output_item.added","item":{"id":"m",'
            b'"type":"message","role":"assistant","status":"in_progress",'
            b'"content":[]}',
            result,
        )
        self.assertIn(
            b'"type":"reasoning","id":"rs1","status":"completed",'
            b'"summary":[{"type":"summary_text","text":"misel"}]',
            result,
        )


    def test_reasoning_plus_nonzero_output_index_positive(self) -> None:
        # A valid canonical stream with protected reasoning bookkeeping and
        # the final message at a nonzero output_index is a supported
        # positive: one repair, consistent copies, reasoning untouched.
        raw = _tc_raw(
            _tc_delta(),
            _tc_part_done(),
            _tc_item_done(output_index=1),
            _tc_completed_reasoning_then_message(),
        )
        repair = _CountingRepair()
        result, changed = transform_sse(raw, repair)
        self.assertTrue(changed)
        self.assertEqual(repair.calls, 1)
        self.assertNotIn(b"presenetliv", result)
        self.assertEqual(result.count(b"To je tako zapisano."), 4)
        self.assertIn(
            b'"type":"reasoning","id":"rs1","status":"completed",'
            b'"summary":[{"type":"summary_text","text":"misel"}]',
            result,
        )


    def test_delta_missing_payload_bypass(self) -> None:
        # A same-id delta event with no payload field between the valid
        # string delta and the matching final answer: malformed answer
        # event, stream ineligible, raw unchanged with zero calls.
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_delta_payload(None, with_field=False),
                _tc_part_done(),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_delta_null_payload_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_delta_payload(None),
                _tc_part_done(),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_delta_number_payload_bypass(self) -> None:
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_delta_payload(7),
                _tc_part_done(),
                _tc_item_done(),
                _tc_completed(),
            )
        )

    def test_delta_array_payload_bypass(self) -> None:
        # A truthy array payload must never be rewritten as text: the
        # stream is ineligible before any collection or rendering.
        self._bypass(
            _tc_raw(
                _tc_delta(),
                _tc_delta_payload(["x"]),
                _tc_part_done(),
                _tc_item_done(),
                _tc_completed(),
            )
        )


class SseHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        self.servers: list[HTTPServer] = []
        self.threads: list[threading.Thread] = []

    def tearDown(self) -> None:
        for server in self.servers:
            server.shutdown()
        for thread in self.threads:
            thread.join(5)
        for server in self.servers:
            server.server_close()
        self.temp.cleanup()

    def _round_trip(self, source: bytes, reviewer: _ScriptedBatchReviewer) -> bytes:
        import proxy

        _EphemeralUpstream.source = source
        upstream = HTTPServer(("127.0.0.1", 0), _EphemeralUpstream)
        self.servers.append(upstream)
        thread = threading.Thread(target=upstream.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)
        engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0), f"http://127.0.0.1:{upstream.server_port}", engine
        )
        self.servers.append(proxy_server)
        thread = threading.Thread(target=proxy_server.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)
        client = http.client.HTTPConnection("127.0.0.1", proxy_server.server_port, timeout=15)
        client.request("POST", "/v1/responses", body=b"{}", headers={"Content-Length": "2"})
        response = client.getresponse()
        result = response.read()
        client.close()
        self.assertEqual(response.status, 200)
        return result

    def test_http_two_targets_one_review_round_trip(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_all)
        source = _sse_delta("m", TEXT) + _sse_completed()
        result = self._round_trip(source, reviewer)
        self.assertIn(b"To je tako zapisano, to je tako zapisano.", result)
        self.assertNotIn(b"presenetliv", result)
        self.assertEqual(reviewer.calls, 1)

    def test_http_multi_answer_zero_review_unchanged(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_all)
        source = (
            _sse_delta("m1", "To je presenetliv zapisano.")
            + _sse_delta("m2", "To je presenetliv zapisano.")
            + _sse_completed()
        )
        result = self._round_trip(source, reviewer)
        self.assertEqual(result, source)
        self.assertEqual(reviewer.calls, 0)

    def test_http_two_completed_messages_zero_review_unchanged(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_all)
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "id": "m",
                    "content": [{"type": "output_text", "text": answer}],
                },
                {
                    "type": "message",
                    "role": "assistant",
                    "id": "m2",
                    "content": [{"type": "output_text", "text": "Drugo."}],
                },
            ],
        }
        source = _sse_delta("m", answer) + _sse_completed(completed)
        result = self._round_trip(source, reviewer)
        self.assertEqual(result, source)
        self.assertEqual(reviewer.calls, 0)

    def test_http_metadata_echo_preserved(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_all)
        answer = "To je presenetliv zapisano."
        completed = {
            "id": "r",
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "id": "m",
                    "content": [{"type": "output_text", "text": answer}],
                }
            ],
            "metadata": {"echo": {"type": "output_text", "text": answer}},
        }
        source = _sse_delta("m", answer) + _sse_completed(completed)
        result = self._round_trip(source, reviewer)
        self.assertEqual(reviewer.calls, 1)
        self.assertIn(b"tako", result)
        self.assertEqual(result.count(b"presenetliv"), 1)
        self.assertIn(
            b'"metadata":{"echo":{"type":"output_text","text":"To je presenetliv zapisano."}}',
            result,
        )

    def test_http_no_accepted_edit_preserves_raw_bytes(self) -> None:
        # Keep proposals are no-ops: one review call happens, but the
        # completed answer stays unchanged and the raw SSE bytes are
        # returned exactly through the real proxy (requirement 7).
        def keep_only(
            sentence: str, targets: tuple[BatchTarget, ...]
        ) -> dict[str, BatchProposal]:
            return {t.id: BatchProposal(t.id, True, None, False) for t in targets}

        reviewer = _ScriptedBatchReviewer(keep_only)
        source = _sse_delta("m", TEXT) + _sse_completed()
        result = self._round_trip(source, reviewer)
        self.assertEqual(result, source)
        self.assertEqual(reviewer.calls, 1)

    def test_http_terminal_copies_follow_repaired_answer(self) -> None:
        # The canonical one-answer stream through the real proxy: every
        # terminal copy of the answer carries the repaired text and no
        # original text remains.
        reviewer = _ScriptedBatchReviewer(_replace_all)
        source = SseGuardTests._canonical_stream(TEXT)
        result = self._round_trip(source, reviewer)
        self.assertEqual(reviewer.calls, 1)
        self.assertNotIn(b"presenetliv", result)
        # Four terminal copies (delta, content_part done, output_item done,
        # completed part), each carrying the full repaired answer twice.
        self.assertEqual(result.count(b"To je tako zapisano, to je tako zapisano."), 4)


    def test_http_contradictory_terminal_copies_raw_bytes_unchanged(self) -> None:
        # Baseline with the identical full answer in every copy, mutating
        # only the terminal item (two output_text parts, one conflicting):
        # the whole SSE is ineligible through the real proxy: raw bytes
        # unchanged, zero review calls (order 014-b, requirement 6).
        reviewer = _ScriptedBatchReviewer(_replace_all)
        source = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(
                parts=[
                    {"type": "output_text", "text": TEXT},
                    {"type": "output_text", "text": _TC_OTHER},
                ]
            ),
            _tc_completed_text_event(TEXT),
        )
        result = self._round_trip(source, reviewer)
        self.assertEqual(result, source)
        self.assertEqual(reviewer.calls, 0)

    def test_http_no_edit_canonical_copies_raw_bytes(self) -> None:
        # Keep proposals are no-ops: the unmutated TEXT baseline with the
        # canonical terminal copies is returned byte-identically through
        # the real proxy after one review call.
        def keep_only(
            sentence: str, targets: tuple[BatchTarget, ...]
        ) -> dict[str, BatchProposal]:
            return {t.id: BatchProposal(t.id, True, None, False) for t in targets}

        reviewer = _ScriptedBatchReviewer(keep_only)
        source = _tc_baseline(TEXT)
        result = self._round_trip(source, reviewer)
        self.assertEqual(result, source)
        self.assertEqual(reviewer.calls, 1)


class CompositionChainTests(unittest.TestCase):
    """Full actual chain: real ConceptProxy HTTP -> real RepairEngine with
    real Pandoc and real tiny SQLite -> real ResponsesReviewer -> fake
    reviewer HTTP endpoint (order 014-a, requirement 11).
    """

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        self.review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        self.review_thread = threading.Thread(
            target=self.review_server.serve_forever, daemon=True
        )
        self.review_thread.start()
        self.servers: list[HTTPServer] = []
        self.threads: list[threading.Thread] = []

    def tearDown(self) -> None:
        for server in self.servers:
            server.shutdown()
        self.review_server.shutdown()
        for thread in self.threads:
            thread.join(5)
        self.review_thread.join(5)
        for server in self.servers:
            server.server_close()
        self.review_server.server_close()
        self.temp.cleanup()

    def _chain(self, source: bytes, review_payload: bytes) -> bytes:
        import proxy

        _FakeUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = review_payload
        _EphemeralUpstream.source = source
        upstream = HTTPServer(("127.0.0.1", 0), _EphemeralUpstream)
        self.servers.append(upstream)
        thread = threading.Thread(target=upstream.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)
        reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.review_server.server_port}/v1",
            "test-model",
            timeout=5.0,
            api_key="fake-key",
        )
        engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0), f"http://127.0.0.1:{upstream.server_port}", engine
        )
        self.servers.append(proxy_server)
        thread = threading.Thread(target=proxy_server.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)
        client = http.client.HTTPConnection(
            "127.0.0.1", proxy_server.server_port, timeout=30
        )
        client.request("POST", "/v1/responses", body=b"{}", headers={"Content-Length": "2"})
        response = client.getresponse()
        result = response.read()
        client.close()
        self.assertEqual(response.status, 200)
        return result

    def test_full_chain_two_targets_one_review_request(self) -> None:
        source = _sse_delta("m", TEXT) + _sse_completed()
        payload = json.dumps(
            _envelope(_valid_inner([_prop("t1"), _prop("t0")])), ensure_ascii=False
        ).encode()
        result = self._chain(source, payload)
        self.assertIn(b"To je tako zapisano, to je tako zapisano.", result)
        self.assertNotIn(b"presenetliv", result)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        record = _FakeUpstream.recorded[0]
        self.assertEqual(record["path"], "/v1/responses")
        body = json.loads(cast(bytes, record["body"]))
        self.assertEqual(body["model"], "test-model")
        self.assertIs(body["stream"], False)
        self.assertIs(body["store"], False)
        self.assertEqual(body["max_output_tokens"], 1536)
        self.assertIn("batch-v1", body["input"][0]["content"][0]["text"])

    def test_full_chain_invalid_batch_after_valid_first_returns_original(self) -> None:
        source = _sse_delta("m", TEXT) + _sse_completed()
        payload = json.dumps(
            _envelope(_valid_inner([_prop("t0"), _prop("t0"), _prop("t1")])),
            ensure_ascii=False,
        ).encode()
        result = self._chain(source, payload)
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)


    def _valid_payload(self) -> bytes:
        return json.dumps(
            _envelope(_valid_inner([_prop("t1"), _prop("t0")])), ensure_ascii=False
        ).encode()

    def _reasoning_then_message_completed(self, text: str) -> bytes:
        return _tc_completed_reasoning_then_message(text)

    def _added_placeholder_events(self, text: str) -> tuple[bytes, bytes]:
        part_added = (
            b'{"type":"response.content_part.added","item_id":"m",'
            b'"part":{"type":"output_text","text":""}}'
        )
        item_added = (
            b'{"type":"response.output_item.added","item":{"id":"m",'
            b'"type":"message","role":"assistant","status":"in_progress",'
            b'"content":[]}}'
        )
        return part_added, item_added

    def test_chain_canonical_baseline_one_review_request(self) -> None:
        # The unmutated TEXT baseline: every copy carries the identical
        # full answer, and the full actual chain makes exactly one review
        # request with four consistent repaired copies.
        source = _tc_baseline(TEXT)
        result = self._chain(source, self._valid_payload())
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertNotIn(b"presenetliv", result)
        self.assertEqual(
            result.count(b"To je tako zapisano, to je tako zapisano."), 4
        )

    def test_chain_contradictory_terminal_copies_zero_review_unchanged(self) -> None:
        # Baseline TEXT copies, mutating only the terminal item (two
        # output_text parts, one conflicting): the full actual chain
        # (proxy -> engine/Pandoc/SQLite -> ResponsesReviewer -> fake
        # reviewer HTTP) must bypass with the raw original and zero review
        # HTTP requests (order 014-b, requirement 6).
        source = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(
                parts=[
                    {"type": "output_text", "text": TEXT},
                    {"type": "output_text", "text": _TC_OTHER},
                ]
            ),
            _tc_completed_text_event(TEXT),
        )
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_conflicting_terminal_text_zero_review_unchanged(self) -> None:
        # Baseline TEXT copies, mutating only the terminal part text.
        source = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=_TC_OTHER),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            _tc_completed_text_event(TEXT),
        )
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_missing_id_terminal_copy_zero_review_unchanged(self) -> None:
        # Baseline TEXT copies, mutating only the terminal part ownership
        # (no item_id at all).
        source = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT, with_id=False),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            _tc_completed_text_event(TEXT),
        )
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_reasoning_nonzero_output_index_positive(self) -> None:
        # Protected reasoning bookkeeping plus the final message at a
        # nonzero output_index, with the identical full TEXT answer in
        # every copy: the supported positive keeps working through the
        # full chain (one request, consistent copies, reasoning untouched).
        source = _tc_raw(
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(
                parts=[{"type": "output_text", "text": TEXT}], output_index=1
            ),
            self._reasoning_then_message_completed(TEXT),
        )
        result = self._chain(source, self._valid_payload())
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertNotIn(b"presenetliv", result)
        self.assertIn(b"To je tako zapisano, to je tako zapisano.", result)
        self.assertIn(
            b'"type":"reasoning","id":"rs1","status":"completed",'
            b'"summary":[{"type":"summary_text","text":"misel"}]',
            result,
        )

    def test_chain_added_part_nonempty_conflicting_text_zero_review_unchanged(self) -> None:
        # Baseline TEXT copies plus an added output_text part carrying
        # non-empty conflicting initial content (cannot be proved safe):
        # the full chain bypasses with the raw original and zero review
        # HTTP requests.
        part_added = (
            '{"type":"response.content_part.added","item_id":"m",'
            '"part":{"type":"output_text","text":' + json.dumps(_TC_OTHER) + "}}"
        ).encode()
        source = _tc_raw(
            part_added,
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            _tc_completed_text_event(TEXT),
        )
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_added_item_wrong_role_status_zero_review_unchanged(self) -> None:
        # Baseline TEXT copies plus an initial message item for the
        # confirmed id with a wrong role and a non-terminal status marker:
        # the full chain bypasses with the raw original and zero review
        # HTTP requests.
        item_added = (
            b'{"type":"response.output_item.added","item":{"id":"m",'
            b'"type":"message","role":"user","status":"in_progress",'
            b'"content":[]}}'
        )
        source = _tc_raw(
            item_added,
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            _tc_completed_text_event(TEXT),
        )
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_added_placeholders_reasoning_nonzero_index_positive(self) -> None:
        # Valid empty placeholders plus protected reasoning and the final
        # message at a nonzero output_index, with the identical full TEXT
        # answer in every copy: one review request, consistent repaired
        # copies, protected added placeholders and reasoning byte-identical.
        part_added, item_added = self._added_placeholder_events(TEXT)
        source = _tc_raw(
            part_added,
            item_added,
            _tc_delta("m", TEXT),
            _tc_part_done(text=TEXT),
            _tc_item_done(
                parts=[{"type": "output_text", "text": TEXT}], output_index=1
            ),
            self._reasoning_then_message_completed(TEXT),
        )
        result = self._chain(source, self._valid_payload())
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertNotIn(b"presenetliv", result)
        self.assertIn(b"To je tako zapisano, to je tako zapisano.", result)
        self.assertIn(part_added[6:], result)
        self.assertIn(item_added[6:], result)
        self.assertIn(
            b'"type":"reasoning","id":"rs1","status":"completed",'
            b'"summary":[{"type":"summary_text","text":"misel"}]',
            result,
        )

    def _delta_type_chain_source(self, payload_event: bytes) -> bytes:
        return _tc_raw(
            _tc_delta("m", TEXT),
            payload_event,
            _tc_part_done(text=TEXT),
            _tc_item_done(parts=[{"type": "output_text", "text": TEXT}]),
            _tc_completed_text_event(TEXT),
        )

    def test_chain_delta_missing_payload_zero_review_unchanged(self) -> None:
        source = self._delta_type_chain_source(
            _tc_delta_payload(None, with_field=False)
        )
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_delta_null_payload_zero_review_unchanged(self) -> None:
        source = self._delta_type_chain_source(_tc_delta_payload(None))
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_delta_number_payload_zero_review_unchanged(self) -> None:
        source = self._delta_type_chain_source(_tc_delta_payload(7))
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_delta_array_payload_zero_review_unchanged(self) -> None:
        source = self._delta_type_chain_source(_tc_delta_payload(["x"]))
        result = self._chain(source, self._valid_payload())
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 0)


    def test_chain_remaining_terminal_copy_variants_zero_review_unchanged(self) -> None:
        # One table-driven full-chain negative per remaining named
        # terminal-copy variant (order 014-b, requirement 6).  Every case
        # starts from the valid TEXT baseline and mutates exactly one
        # named ownership field (or adds the one named terminal copy);
        # the full actual chain (proxy -> engine/Pandoc/SQLite ->
        # ResponsesReviewer -> fake reviewer HTTP) must return the raw
        # original bytes with status 200 and zero review HTTP requests.
        parts: list[dict[str, object]] = [{"type": "output_text", "text": TEXT}]
        cases = {
            "null_part_id": _tc_raw(
                _tc_delta("m", TEXT),
                _tc_part_done(text=TEXT, item_id=None),
                _tc_item_done(parts=parts),
                _tc_completed_text_event(TEXT),
            ),
            "number_part_id": _tc_raw(
                _tc_delta("m", TEXT),
                _tc_part_done(text=TEXT, item_id=7),
                _tc_item_done(parts=parts),
                _tc_completed_text_event(TEXT),
            ),
            "other_part_id": _tc_raw(
                _tc_delta("m", TEXT),
                _tc_part_done(text=TEXT, item_id="other"),
                _tc_item_done(parts=parts),
                _tc_completed_text_event(TEXT),
            ),
            "wrong_role_item": _tc_raw(
                _tc_delta("m", TEXT),
                _tc_part_done(text=TEXT),
                _tc_item_done(parts=parts, role="user"),
                _tc_completed_text_event(TEXT),
            ),
            "incomplete_status_item": _tc_raw(
                _tc_delta("m", TEXT),
                _tc_part_done(text=TEXT),
                _tc_item_done(parts=parts, status="incomplete"),
                _tc_completed_text_event(TEXT),
            ),
            "wrong_index_item": _tc_raw(
                _tc_delta("m", TEXT),
                _tc_part_done(text=TEXT),
                _tc_item_done(parts=parts, output_index=1),
                _tc_completed_text_event(TEXT),
            ),
            "conflicting_text_done": _tc_raw(
                _tc_delta("m", TEXT),
                _tc_done(text=_TC_OTHER),
                _tc_part_done(text=TEXT),
                _tc_item_done(parts=parts),
                _tc_completed_text_event(TEXT),
            ),
        }
        for name, source in cases.items():
            with self.subTest(case=name):
                result = self._chain(source, self._valid_payload())
                self.assertEqual(result, source)
                self.assertEqual(len(_FakeUpstream.recorded), 0)

    def test_chain_invalid_batch_after_valid_first_canonical_copies_raw_bytes(self) -> None:
        # The unmutated TEXT baseline (canonical terminal copies) with an
        # invalid second proposal: one review request is made, the batch
        # is rejected as a whole, and the raw original SSE bytes are
        # returned unchanged.
        source = _tc_baseline(TEXT)
        payload = json.dumps(
            _envelope(_valid_inner([_prop("t0"), _prop("t0"), _prop("t1")])),
            ensure_ascii=False,
        ).encode()
        result = self._chain(source, payload)
        self.assertEqual(result, source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)


class ReviewerTimeoutTests(unittest.TestCase):
    def test_reviewer_default_timeout_is_ordered_cap(self) -> None:
        import config

        self.assertEqual(config.REVIEWER_HTTP_TIMEOUT_SECONDS, 15.0)
        reviewer = ResponsesReviewer("http://127.0.0.1:9/v1", "test-model")
        self.assertEqual(reviewer.timeout, 15.0)

    def test_main_wires_ordered_cap_not_capture_timeout(self) -> None:
        import os

        import proxy
        from pandoc_protection import PandocSpec

        captured: dict[str, object] = {}

        class _ProbeReviewer:
            def __init__(
                self,
                base_url: str,
                model: str,
                timeout: float = 15.0,
                api_key: str | None = None,
                profile: object = None,
            ) -> None:
                captured["timeout"] = timeout

        class _ProbeProxy:
            def __init__(self, *args: object, **kwargs: object) -> None:
                raise SystemExit("stop before serve_forever")

        env = {
            "CONCEPT_INDEX": "/tmp/unused.sqlite",
            "CONCEPT_TIMEOUT": "999",
            "CONCEPT_REVIEWER_URL": "http://127.0.0.1:9/v1",
        }
        with mock.patch.dict(os.environ, env), mock.patch.object(
            proxy, "resolve_pandoc_spec", lambda: PandocSpec(binary="/bin/true")
        ), mock.patch.object(proxy, "check_pandoc", lambda spec: None), mock.patch.object(
            proxy, "ResponsesReviewer", _ProbeReviewer
        ), mock.patch.object(proxy, "ConceptProxy", _ProbeProxy), self.assertRaises(
            SystemExit
        ):
            proxy.main()
        self.assertEqual(captured["timeout"], 15.0)


if __name__ == "__main__":
    unittest.main()
