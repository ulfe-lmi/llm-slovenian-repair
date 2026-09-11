"""Independent checks of behaviors already present in the frozen experiments.

Synthetic strings/proposals only; no live model answers or benchmark rows.
"""
from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest

from research.curated.corpus import Corpus
from research.curated.methods import no_retry
from research.curated.pipeline import replay
from research.curated.review import parse_proposal
from research.tools.replay import _create_fixture_index


class StrategicReplayFidelity(unittest.TestCase):
    def test_duplicate_proposal_keys_are_not_silently_accepted(self) -> None:
        # The original experiment.parse_reply uses unique_object for inner JSON.
        body = '{"keep":true,"keep":false,"replacement":"beta","needs_wider_edit":false}'
        response = {
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": body}],
                }
            ]
        }
        with self.assertRaises(ValueError):
            parse_proposal(response)

    def test_english_preservation_has_zero_review_and_retry_calls(self) -> None:
        parent = os.environ.get("TMPDIR")
        self.assertTrue(parent, "Use an owned persistent TMPDIR")
        Path(parent).mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="replay-fidelity-", dir=parent) as name:
            index = Path(name) / "fixture.sqlite"
            _create_fixture_index({"unigrams": {"beta": 100}}, index)
            with Corpus(index) as corpus:
                result = replay("alpha", corpus, lambda _: 3.0, {})
        self.assertEqual(result["output"], "alpha")
        self.assertEqual(result["edits"], [])
        self.assertEqual(result["review_calls"], 0)
        self.assertEqual(result["retry_calls"], 0)

    def test_no_retry_retains_first_stage_operational_failure(self) -> None:
        result = no_retry(
            {
                "no_retry_output": "alpha",
                "no_retry_edits": [],
                "no_retry_operational_failure": True,
                "operational_failure": True,
            }
        )
        self.assertTrue(result["operational_failure"])

    def test_retry_only_failure_does_not_invalidate_no_retry(self) -> None:
        result = no_retry(
            {
                "no_retry_output": "beta",
                "no_retry_edits": [(0, 5, "beta")],
                "no_retry_operational_failure": False,
                "operational_failure": True,
            }
        )
        self.assertFalse(result["operational_failure"])
        self.assertEqual(result["output"], "beta")


if __name__ == "__main__":
    unittest.main()
