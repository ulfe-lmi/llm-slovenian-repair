from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from research.curated.corpus import Evidence
from research.curated.english_preserve import classify
from research.curated.gating import check
from research.curated.historical_detector import detect as hyphen_detect
from research.curated.historical_detector import tokenize as hyphen_tokenize
from research.curated.patching import apply_edits, mechanical, restore_initial_case
from research.curated.pipeline import replay
from research.curated.review import (
    Proposal,
    ReviewerError,
    expression_retry_body,
    parse_expression,
    parse_proposal,
    reviewer_body,
)
from research.tools.publication_guard import export_json, safe_destination, scan_public
from research.tools.replay import replay_fixture


class MemoryCorpus:
    def __init__(self, unigrams: dict[str, int], bigrams: set[str] | None = None, trigrams: set[str] | None = None):
        self.unigrams = unigrams
        self.bigrams = bigrams or set()
        self.trigrams = trigrams or set()

    def unigram(self, word: str) -> Evidence:
        key = word.casefold()
        return Evidence("EXACT", self.unigrams[key], key) if key in self.unigrams else Evidence("UNAVAILABLE", None, key)

    def ngram(self, phrase: str, length: int) -> Evidence:
        key = " ".join(phrase.casefold().split())
        available = self.bigrams if length == 2 else self.trigrams
        return Evidence("EXACT", 1, key) if key in available else Evidence("CENSORED", None, key)

    def alternatives(self, left: str, right: str) -> list[tuple[str, int]]:
        return []


def response(text: str) -> dict[str, object]:
    return {"output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": text}]}]}


class ResearchBoundaryTests(unittest.TestCase):
    def test_actual_hyphen_detector_and_protected_intervals(self) -> None:
        text = "Vspešni foo-bar\n```\nVspešni\n```"
        corpus = MemoryCorpus({"foo": 20, "bar": 20})
        intervals = __import__("research.curated.protected", fromlist=["protected_intervals"]).protected_intervals(text)
        tokens = hyphen_tokenize(text, intervals)
        self.assertEqual([token.text for token in tokens], ["Vspešni", "foo", "bar"])
        candidates = hyphen_detect(text, corpus, intervals, mode="local-context", maximum=None)
        self.assertEqual([candidate.text for candidate in candidates], ["Vspešni"])

    def test_english_policy_only_suppresses_original_unavailable_target(self) -> None:
        unavailable = {"text": "payload", "evidence": {"unigram": {"state": "UNAVAILABLE", "count": None}}}
        preserved = classify(unavailable, lambda _: 3.36)
        self.assertTrue(preserved["review_suppressed"])
        available = {"text": "uspešni", "evidence": {"unigram": {"state": "EXACT", "count": 42}}}
        self.assertFalse(classify(available, lambda _: 4.0)["review_suppressed"])

    def test_review_and_expression_contracts_reject_malformed_content(self) -> None:
        parsed = parse_proposal(response(json.dumps({"keep": False, "replacement": "Uspešni", "needs_wider_edit": False})))
        self.assertEqual(parsed.replacement, "Uspešni")
        self.assertIn('"model": "qwen3.8-27b"', json.dumps(reviewer_body("Vspešni.", "Vspešni"), ensure_ascii=False))
        self.assertEqual(expression_retry_body("slaba oblika")["reasoning"], {"effort": "low"})
        self.assertEqual(parse_expression(response("Uspešni")), Proposal(False, "Uspešni", False))
        with self.assertRaises(ReviewerError):
            parse_proposal(response(json.dumps({"keep": True, "replacement": "ne", "needs_wider_edit": False})))
        with self.assertRaises(ReviewerError):
            parse_expression(response("{\"replacement\":\"Uspešni\"}"))

    def test_unigram_gate_case_restoration_and_exact_patch(self) -> None:
        original = "Vspešni so tukaj."
        candidate = {"start": 0, "end": 7, "text": "Vspešni", "evidence": {"unigram": {"state": "UNAVAILABLE"}}}
        raw = Proposal(False, "Uspešni", False)
        adjusted, case = restore_initial_case(candidate["text"], raw)
        self.assertEqual(adjusted.replacement, "Uspešni")
        self.assertEqual(case["direction"], "upper")
        gate = check(original, candidate, adjusted, lambda word: {"state": "EXACT" if word == "uspešni" else "UNAVAILABLE", "count": 1, "key": word})
        self.assertTrue(gate["accepted"])
        self.assertEqual(apply_edits(original, [(0, 7, "Uspešni")]), "Uspešni so tukaj.")
        self.assertEqual(mechanical(original, candidate, adjusted)["reason"], "mechanically-valid")

    def test_replay_runs_actual_boundaries_with_retry_and_no_calls(self) -> None:
        original = "Vspešni so tukaj."
        corpus = MemoryCorpus({"uspešni": 42, "so": 100, "tukaj": 100})
        result = replay(
            original,
            corpus,
            lambda _: 0.0,
            {"0": Proposal(False, "neattested", False)},
            {"0": Proposal(False, "Uspešni", False)},
        )
        self.assertEqual(result["output"], "Uspešni so tukaj.")
        self.assertEqual(result["retry_calls"], 1)
        self.assertEqual(result["model_calls"], 0)

    def test_replay_fixture_entrypoint_is_offline(self) -> None:
        scratch = os.environ.get("TMPDIR")
        self.assertTrue(scratch and not scratch.startswith("/" + "tmp"))
        fixture = Path("research/fixtures/replay.json")
        result = replay_fixture(fixture, Path(scratch) / "research-test-replay")
        self.assertEqual(result["network_calls"], 0)
        self.assertEqual(result["model_calls"], 0)


class PublicationBoundaryTests(unittest.TestCase):
    def test_guard_schema_export_and_negative_paths(self) -> None:
        scratch = os.environ.get("TMPDIR")
        self.assertTrue(scratch)
        with tempfile.TemporaryDirectory(dir=scratch) as name:
            root = Path(name)
            (root / "tables").mkdir()
            (root / "tables/summary.csv").write_text("experiment_id,status\nsynthetic,COMPLETE\n", encoding="utf-8")
            (root / "safe.json").write_text('{"metric_count": 1}\n', encoding="utf-8")
            self.assertEqual(scan_public(root), [])
            (root / "configs").mkdir()
            (root / "configs/request.json").write_text('{"request": {"mode": "synthetic", "content": ["template"]}}\n', encoding="utf-8")
            self.assertEqual(scan_public(root), [])
            (root / "configs/request.json").write_text('{"request": {"input": "private sentence"}}\n', encoding="utf-8")
            self.assertTrue(any("raw JSON field" in error for error in scan_public(root)))
            (root / "configs/request.json").unlink()
            (root / "bad.json").write_text('{"input": "private sentence"}\n', encoding="utf-8")
            self.assertTrue(any("raw JSON field" in error for error in scan_public(root)))
            (root / "bad.json").unlink()
            with self.assertRaises(ValueError):
                safe_destination(root, Path("../escape.json"))
            (root / "inside").mkdir()
            (root / "outside.json").write_text("{}\n", encoding="utf-8")
            (root / "inside/link").symlink_to(root / "outside.json")
            with self.assertRaises(ValueError):
                safe_destination(root, Path("inside/link/new.json"))
            (root / "new.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                safe_destination(root, Path("new.json"))
            with self.assertRaises(ValueError):
                export_json(root, "export.json", {"input": "forbidden"})
            self.assertFalse((root / "export.json").exists())
            export_json(root, "export.json", {"metric_count": 2})
            self.assertEqual(json.loads((root / "export.json").read_text()), {"metric_count": 2})


if __name__ == "__main__":
    unittest.main()
