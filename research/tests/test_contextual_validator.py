"""Offline contract tests for the 007-i validator boundary."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from research import contextual_validator as protocol
from research.tools import run_contextual_validator as driver


def response(text: str = "USE_CANDIDATE") -> dict[str, object]:
    return {
        "id": "synthetic-response",
        "status": "completed",
        "model": "qwen3.8-27b",
        "reasoning": {"effort": "low"},
        "usage": {
            "input_tokens": 20,
            "output_tokens": 4,
            "output_tokens_details": {"reasoning_tokens": 3},
        },
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": text}],
            }
        ],
    }


class FakeTransport:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.calls: list[tuple[str, bytes, dict[str, str], float]] = []

    def request(self, endpoint: str, body: bytes, headers: dict[str, str], timeout: float) -> tuple[int, dict[str, str], bytes]:
        self.calls.append((endpoint, body, headers, timeout))
        return 200, {"Content-Type": "application/json"}, self.payload


class ContextualValidatorTests(unittest.TestCase):
    def test_prompt_and_request_are_frozen(self) -> None:
        self.assertEqual(protocol.prompt_sha256(), protocol.FROZEN_PROMPT_SHA256)
        body = protocol.request_body("Celoten stavek.", "stari", "novi")
        self.assertEqual(
            set(body), {"model", "stream", "store", "input", "include_reasoning", "reasoning"}
        )
        self.assertEqual(body["model"], "qwen3.8-27b")
        self.assertEqual(body["stream"], False)
        self.assertEqual(body["store"], False)
        self.assertEqual(body["include_reasoning"], True)
        self.assertEqual(body["reasoning"], {"effort": "low"})
        self.assertEqual(body["input"][0]["content"][0]["type"], "input_text")  # type: ignore[index]
        self.assertIn("Celoten stavek.", body["input"][0]["content"][0]["text"])  # type: ignore[index]

    def test_parser_accepts_only_exact_choices_after_outer_whitespace(self) -> None:
        parsed = protocol.parse_response(response("  KEEP_ORIGINAL\n"))
        self.assertEqual(parsed["decision"], "KEEP_ORIGINAL")
        for text in ("USE_CANDIDATE extra", '{"decision":"USE_CANDIDATE"}', ""):
            with self.subTest(text=text), self.assertRaises(protocol.ValidatorError):
                protocol.parse_response(response(text))

    def test_parser_rejects_wrong_model_effort_tokens_and_duplicate_json(self) -> None:
        for changed in (
            {"model": "other"},
            {"reasoning": {"effort": "high"}},
            {"usage": {"input_tokens": 1, "output_tokens": 1, "output_tokens_details": {"reasoning_tokens": -1}}},
        ):
            value = response()
            value.update(changed)
            with self.subTest(changed=changed), self.assertRaises(protocol.ValidatorError):
                protocol.parse_response(value)
        duplicate = b'{"status":"completed","status":"completed"}'
        with self.assertRaises(protocol.ValidatorError):
            protocol.parse_response_bytes(duplicate)

    def test_persistence_is_request_raw_observation_and_never_resamples(self) -> None:
        fake = FakeTransport(response())
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            body = protocol.request_body("Stavek.", "stari", "novi")
            first = protocol.perform_call(root, body, endpoint="fake://endpoint", transport=fake)
            second = protocol.perform_call(root, body, endpoint="fake://endpoint", transport=fake)
            self.assertEqual(first, second)
            self.assertEqual(len(fake.calls), 1)
            self.assertEqual(
                [path.name for path in sorted(root.iterdir())],
                ["observation.json", "raw-response.json", "request.json"],
            )
            self.assertEqual(first["decision"], "USE_CANDIDATE")

    def test_request_without_raw_response_becomes_uncertain_without_transport_call(self) -> None:
        fake = FakeTransport(response())
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            body = protocol.request_body("Stavek.", "stari", "novi")
            protocol.immutable_write(root / "request.json", protocol.canonical_bytes(body))
            observed = protocol.perform_call(root, body, endpoint="fake://endpoint", transport=fake)
            self.assertEqual(observed["failure"], "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE")
            self.assertEqual(len(fake.calls), 0)
            self.assertTrue((root / "raw-response.json").is_file())
            self.assertTrue((root / "observation.json").is_file())

    def test_partitions_are_disjoint_complete_and_stable(self) -> None:
        candidates = [
            {
                "phase": "dassle-spelling" if index % 2 else "dassle-spelling-preservation",
                "case_index": index + 1,
                "target_start": index,
                "target_end": index + 3,
                "target_ordinal": index % 3,
                "candidate": {"start": index, "end": index + 3, "text": "abc"},
                "candidate_form": "abd",
                "mechanical_edit": [index, index + 3, "abd"],
            }
            for index in range(735)
        ]
        left = protocol.partitions(candidates)
        right = protocol.partitions(list(reversed(candidates)))
        left_keys = [protocol.stable_key(item) for worker in left.values() for item in worker]
        right_keys = [protocol.stable_key(item) for worker in right.values() for item in worker]
        self.assertEqual(len(left_keys), 735)
        self.assertEqual(len(set(left_keys)), 735)
        self.assertEqual(sorted(left_keys), sorted(right_keys))
        self.assertTrue(all(len(value) in {91, 92} for value in left.values()))
        for worker, values in left.items():
            self.assertEqual([protocol.stable_key(item) for item in values], [protocol.stable_key(item) for item in protocol.ordered_candidates(candidates)][worker::8])

    def test_candidate_manifest_hash_has_no_selection_heuristic(self) -> None:
        candidate = {
            "phase": "dassle-spelling",
            "case_index": 1,
            "target_start": 0,
            "target_end": 3,
            "target_ordinal": 0,
            "candidate": {"start": 0, "end": 3, "text": "abc"},
            "candidate_form": "abd",
            "mechanical_edit": [0, 3, "abd"],
        }
        manifest, digest = protocol.candidate_manifest([candidate])
        self.assertEqual(len(manifest), 1)
        self.assertEqual(digest, protocol.sha256_bytes(protocol.canonical_bytes(manifest)))
        self.assertEqual(manifest[0]["stable_key"], ["dassle-spelling", 1, 0, 3, 0])

    def test_projection_failure_is_fail_closed_and_different_from_model_failure(self) -> None:
        saved = {
            "id": "case",
            "index": 1,
            "input": "abc",
            "input_sha256": "x",
            "detector": {"candidates": [], "english": []},
            "decisions": [],
            "calls": [],
            "operational_failure": False,
        }
        projected = driver.projection_result(saved, [[0, 1, "x"], [0, 1, "y"]], only=True, scheduled=set())
        self.assertEqual(projected["output"], "abc")
        self.assertEqual(projected["projection_failure"], "DOCUMENT_PATCH_CONFLICT: ValueError")
        self.assertTrue(projected["operational_failure"])


if __name__ == "__main__":
    unittest.main()
