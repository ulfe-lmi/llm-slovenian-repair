"""Synthetic proof that copied historical sources execute offline."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from research.curated.historical_methods import no_retry, targeted
from research.curated.historical_pipeline import Pipeline
from research.curated.historical_transport import Client, FakeTransport, text_body
from research.tools.replay import _create_fixture_index, replay_saved_record


def response(text: str) -> dict[str, object]:
    return {
        "model": "qwen3.8-27b",
        "status": "completed",
        "id": "synthetic",
        "reasoning": {"effort": "low"},
        "usage": {"output_tokens": 3, "output_tokens_details": {"reasoning_tokens": 1}},
        "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": text}]}],
    }


class HistoricalExecutableSources(unittest.TestCase):
    def scratch(self) -> Path:
        parent = os.environ.get("TMPDIR")
        self.assertTrue(parent)
        return Path(tempfile.mkdtemp(prefix="historical-executable-", dir=parent))

    def test_fake_transport_runs_detector_gate_patch_and_m3_without_network(self) -> None:
        root = self.scratch()
        index = root / "index.sqlite"
        _create_fixture_index({"unigrams": {"beta": 100}}, index)
        fake = FakeTransport(response('{"keep":false,"replacement":"beta","needs_wider_edit":false}'))
        client = Client(transport=fake)
        pipeline = Pipeline(index, english_lookup=lambda _: 0.0, maximum=None)
        try:
            result = targeted("alpha", pipeline, client, root / "run")
            ablation = no_retry("alpha", result)
        finally:
            pipeline.close()
        self.assertEqual(result["output"], "beta")
        self.assertEqual(ablation["output"], "beta")
        self.assertEqual(len(fake.calls), 1)
        self.assertEqual(client.network_calls, 1)
        self.assertEqual(json.loads((root / "run" / "targets" / "00" / "decision.json").read_text())["final_gate"]["reason"], "unigram-exact")

    def test_campaign_input_decisions_saved_replay_is_fail_closed_and_zero_call(self) -> None:
        root = self.scratch()
        index = root / "index.sqlite"
        _create_fixture_index({"unigrams": {"beta": 100}}, index)
        record = {
            "input": "alpha",
            "detector": {"maximum": None},
            "english_evidence": [{"casefolded_target": "alpha", "english_frequency": 0.0}],
            "decisions": [{"candidate": {"start": 0, "end": 5, "text": "alpha"}, "first_proposal": {"keep": False, "replacement": "beta", "needs_wider_edit": False}}],
            "output": "beta",
        }
        receipt = replay_saved_record(record, index, record_name="campaign-synthetic")
        self.assertEqual(receipt["schema"], "campaign-input-decisions")
        self.assertEqual(receipt["output_sha256"], __import__("hashlib").sha256(b"beta").hexdigest())
        self.assertEqual(receipt["network_calls"], 0)
        self.assertEqual(receipt["model_calls"], 0)


if __name__ == "__main__":
    unittest.main()
