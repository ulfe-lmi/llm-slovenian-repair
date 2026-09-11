"""An archived variant must execute its own settings, not the latest campaign.

All text and responses are synthetic. HTTP is replaced outside the client;
socket creation is forbidden. This is not a live experiment or linguistic test.
"""
import argparse
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research.curated.historical import variant_map
from research.curated import historical_transport
from research.tools.replay import _create_fixture_index
from research.tools.reproduce import execute_authorized
from research.curated.retry import outcome


class VariantExecutionFidelity(unittest.TestCase):
    def test_historical_retry_outcome_accepts_saved_first_stage_dictionary(self):
        record = {"case": {"id": "synthetic", "known_error": False}, "original": "zzzx",
                  "decisions": [{"candidate": {"start": 0, "end": 4, "text": "zzzx"},
                                 "proposal": {"keep": False, "replacement": "Abcd", "needs_wider_edit": False}}]}
        gates = {"synthetic-0": {"accepted": True, "reason": "unigram-exact"}}
        result = outcome(record, gates, {}, lambda word: {"state": "EXACT", "key": word, "count": 10})
        self.assertEqual(result["corrected"], "Abcd")

    def test_nonthinking_mechanical_does_not_run_english_or_unigram_campaign(self):
        scratch = Path(os.environ.get("TMPDIR", str(Path.cwd() / ".research-test-scratch")))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            root = Path(directory)
            inputs = root / "inputs"
            inputs.mkdir()
            (inputs / "records.json").write_text(json.dumps([
                {"id": "synthetic", "index": 0, "input": "zzzx"}
            ]))
            # This later policy must have no effect on the earlier mechanical-only variant.
            (inputs / "english.json").write_text(json.dumps({"zzzx": 5.0}))
            index = root / "index.sqlite"
            _create_fixture_index({"unigrams": {"abc": 100}}, index)
            args = argparse.Namespace(input_root=str(inputs), index=str(index),
                                      output_root=str(root / "output"), max_cases=1,
                                      endpoint="http://example.invalid/v1",
                                      credential_env="SYNTHETIC_RESEARCH_CREDENTIAL",
                                      timeout_seconds=300, workers=1,
                                      model="qwen3.8-27b", allow_live=True)
            requests = []

            def fake_request(_self, endpoint, body, headers, timeout):
                request = json.loads(body)
                requests.append(request)
                response = {"model": "qwen3.8-27b", "status": "completed",
                            "reasoning": {"effort": "none"},
                            "usage": {"output_tokens": 4, "output_tokens_details": {"reasoning_tokens": 0}},
                            "output": [{"type": "message", "role": "assistant", "content": [
                                {"type": "output_text", "text": json.dumps({
                                    "keep": False, "replacement": "Abcd", "needs_wider_edit": False
                                })}
                            ]}]}
                return 200, {"Content-Type": "application/json"}, json.dumps(response).encode()

            with patch.dict(os.environ, {"SYNTHETIC_RESEARCH_CREDENTIAL": "synthetic-placeholder"}), \
                    patch.object(historical_transport._HttpTransport, "request", fake_request), \
                    patch("socket.create_connection", side_effect=AssertionError("network forbidden")):
                execute_authorized(args, variant_map()["nonthinking-mechanical"])
            self.assertEqual(len(requests), 1, "An earlier one-target review must not add direct-GEC or corrective calls")
            self.assertEqual(requests[0].get("reasoning"), {"effort": "none"})
            prompt = requests[0]["input"][0]["content"][0]["text"]
            self.assertIn("Target:", prompt)
            outputs = [json.loads(path.read_text()) for path in (root / "output").rglob("*.json")]
            self.assertTrue(any(isinstance(row, dict) and (
                row.get("corrected") == "Abcd" or (row.get("method") == "M2" and row.get("output") == "Abcd")
            ) for row in outputs), "Mechanical-only variant must not apply later English/unigram/case policies")


if __name__ == "__main__":
    unittest.main()
