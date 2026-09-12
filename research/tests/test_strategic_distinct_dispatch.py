"""Executable proof for the distinct historical dispatcher families."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research.curated import historical_transport
from research.curated.historical import variant_map
from research.curated.historical_campaign import run_injected
from research.curated.historical_dassle import analyze
from research.curated.historical_pipeline import Pipeline
from research.curated.historical_retry10 import sequence
from research.curated.historical_transport import Client
from research.curated.historical_variants import build_historical_pipeline
from research.tools.replay import _create_fixture_index
from research.tools.reproduce import execute_authorized


def _response(output: str, effort: str = "low") -> dict[str, object]:
    return {
        "model": "qwen3.8-27b",
        "status": "completed",
        "id": "synthetic",
        "reasoning": {"effort": effort},
        "usage": {"output_tokens": 3, "output_tokens_details": {"reasoning_tokens": 1}},
        "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": output}]}],
    }


class PromptTransport:
    def __init__(self, *, effort: str = "low") -> None:
        self.effort = effort
        self.calls: list[dict[str, object]] = []

    def request(self, _endpoint: str, body: bytes, _headers: object, _timeout: float):
        value = json.loads(body)
        self.calls.append(value)
        prompt = value["input"][0]["content"][0]["text"]
        if '"decision"' in prompt:
            output = json.dumps({"decision": "ACCEPT"})
        elif "Ta beseda je napačno zapisana" in prompt:
            output = "beta"
        elif "failed proposed fix" in prompt:
            output = json.dumps({"keep": False, "replacement": "beta", "needs_wider_edit": False})
        elif "napačno zapisan ali oblikovan" in prompt:
            output = "beta"
        elif "Return only the corrected text" in prompt:
            output = "alpha"
        else:
            output = json.dumps({"keep": False, "replacement": "gamma", "needs_wider_edit": False})
        return 200, {"Content-Type": "application/json"}, json.dumps(_response(output, self.effort)).encode()


class SequenceTransport:
    def __init__(self, outputs: list[str]) -> None:
        self.outputs = outputs
        self.calls: list[dict[str, object]] = []

    def request(self, _endpoint: str, body: bytes, _headers: object, _timeout: float):
        value = json.loads(body)
        self.calls.append(value)
        output = self.outputs.pop(0)
        return 200, {"Content-Type": "application/json"}, json.dumps(_response(output)).encode()


class FailingTransport:
    def __init__(self) -> None:
        self.calls = 0

    def request(self, _endpoint: str, _body: bytes, _headers: object, _timeout: float):
        self.calls += 1
        return 503, {"Content-Type": "application/json"}, b"{}"


class DistinctDispatchTests(unittest.TestCase):
    def setUp(self) -> None:
        parent = os.environ.get("TMPDIR")
        self.assertTrue(parent and not parent.startswith("/tmp"))
        self.root = Path(tempfile.mkdtemp(prefix="distinct-dispatch-", dir=parent))
        self.inputs = self.root / "inputs"
        self.inputs.mkdir()
        (self.inputs / "records.json").write_text(json.dumps([{"id": "case", "index": 1, "input": "alpha"}]))
        self.index = self.root / "index.sqlite"
        _create_fixture_index({"unigrams": {"beta": 100}}, self.index)
        self.args = argparse.Namespace(
            input_root=str(self.inputs), index=str(self.index), output_root=str(self.root / "output"),
            max_cases=1, endpoint="http://example.invalid/v1", credential_env="SYNTHETIC_RESEARCH_CREDENTIAL",
            timeout_seconds=30, workers=1, model="qwen3.8-27b", allow_live=True, trials=1, retry_limit=1,
        )

    def run_variant(self, name: str, transport: PromptTransport) -> dict[str, object]:
        with patch.dict(os.environ, {"SYNTHETIC_RESEARCH_CREDENTIAL": "synthetic-placeholder"}), \
                patch.object(historical_transport._HttpTransport, "request", transport.request), \
                patch("socket.create_connection", side_effect=AssertionError("network forbidden")):
            return execute_authorized(self.args, variant_map()[name])

    def test_contextual_retry_uses_early_pipeline_and_real_wire_body(self) -> None:
        transport = PromptTransport()
        result = self.run_variant("low-unigram-retry", transport)
        self.assertEqual(result["network_calls"], 2)
        self.assertEqual(len(transport.calls), 2)
        self.assertIn("Original sentence", transport.calls[1]["input"][0]["content"][0]["text"])
        self.assertFalse((self.inputs / "english.json").exists())

    def test_word_only_retry_has_its_own_parser_and_no_context(self) -> None:
        transport = PromptTransport()
        self.run_variant("low-word-only-retry", transport)
        self.assertEqual(len(transport.calls), 2)
        retry_prompt = transport.calls[1]["input"][0]["content"][0]["text"]
        self.assertIn("Ta beseda", retry_prompt)
        self.assertNotIn("Original sentence", retry_prompt)

    def test_ten_run_records_stopped_trial_and_continues_schedule(self) -> None:
        self.args.output_root = str(self.root / "stopped-ten-run")
        self.args.trials = 2
        transport = FailingTransport()
        with patch.dict(os.environ, {"SYNTHETIC_RESEARCH_CREDENTIAL": "synthetic-placeholder"}), \
                patch.object(historical_transport._HttpTransport, "request", transport.request):
            result = execute_authorized(self.args, variant_map()["ten-run-expression-retry-low"])
        self.assertEqual(result["status"], "COMPLETED_WITH_STOPPED_TRIALS")
        self.assertEqual(result["stopped_trials"], 2)
        self.assertEqual(transport.calls, 2)

    def test_validator_reuses_frozen_first_stage_and_only_calls_validator(self) -> None:
        (self.inputs / "records.json").write_text(json.dumps([{
            "id": "case", "input": "alpha",
            "first_stage": [{"candidate": {"start": 0, "end": 5, "text": "alpha"},
                              "proposal": {"keep": False, "replacement": "beta", "needs_wider_edit": False}}],
        }]))
        transport = PromptTransport()
        self.run_variant("low-plus-validator", transport)
        self.assertEqual(len(transport.calls), 1)
        self.assertIn('"decision"', transport.calls[0]["input"][0]["content"][0]["text"])
        self.assertNotIn("Target:", transport.calls[0]["input"][0]["content"][0]["text"])

    def test_three_ten_run_schedules_have_distinct_trial_receipts(self) -> None:
        for name in ("ten-run-initial-case-low", "ten-run-expression-retry-low", "ten-run-english-preserve-low"):
            with self.subTest(variant=name):
                self.args.output_root = str(self.root / name)
                self.args.trials = 2
                if name == "ten-run-english-preserve-low":
                    (self.inputs / "english.json").write_text(json.dumps({"alpha": 0.0}))
                transport = PromptTransport()
                result = self.run_variant(name, transport)
                self.assertEqual(result["scheduled_trials"], 2)
                self.assertEqual(len(list((Path(self.args.output_root) / "trials").glob("*/records/*/targets/*/first/request.json"))), 2)
                self.assertEqual(result["stopped_trials"], 0)

    def test_retry10_reuses_fixed_first_anchor_until_gate_accepts(self) -> None:
        transport = SequenceTransport([
            json.dumps({"keep": False, "replacement": "gamma", "needs_wider_edit": False}),
            "delta",
            "beta",
        ])
        client = Client(transport=transport)
        pipeline = build_historical_pipeline(self.index, maximum=1)
        try:
            steps, status, edits = sequence(
                "alpha", {"start": 0, "end": 5, "text": "alpha", "evidence": {"unigram": {"state": "UNAVAILABLE"}}},
                pipeline, client, self.root / "retry10", max_retries=10,
            )
        finally:
            pipeline.close()
        self.assertEqual(status, "ACCEPTED")
        self.assertEqual(len(steps), 3)
        self.assertEqual(len(edits), 1)
        self.assertEqual(transport.calls[1]["input"][0]["content"][0]["text"], transport.calls[2]["input"][0]["content"][0]["text"])
        self.assertIn("gamma", transport.calls[1]["input"][0]["content"][0]["text"])

    def test_retry10_stops_at_ten_corrective_calls(self) -> None:
        transport = SequenceTransport([
            json.dumps({"keep": False, "replacement": "gamma", "needs_wider_edit": False}),
            *(["delta"] * 10),
        ])
        client = Client(transport=transport)
        pipeline = build_historical_pipeline(self.index, maximum=1)
        try:
            steps, status, edits = sequence(
                "alpha", {"start": 0, "end": 5, "text": "alpha", "evidence": {"unigram": {"state": "UNAVAILABLE"}}},
                pipeline, client, self.root / "retry10-stopped", max_retries=10,
            )
        finally:
            pipeline.close()
        self.assertEqual(status, "RETRY_LIMIT_REACHED")
        self.assertEqual(len(steps), 11)
        self.assertEqual(edits, [])
        self.assertEqual(len(transport.calls), 11)

    def test_campaign_runner_routes_slobench_phase_and_worker_status(self) -> None:
        transport = PromptTransport()
        def pipeline_factory():
            return Pipeline(self.index, english_lookup=lambda _word: 0.0, maximum=None)
        def client_factory():
            return Client(transport=transport)
        result = run_injected(
            [
                {"benchmark": "dassle", "id": "d", "index": 1, "input": "alpha"},
                {"benchmark": "slobench", "id": "s", "index": 1, "input": "alpha"},
            ],
            output_root=self.root / "campaign", workers=2,
            pipeline_factory=pipeline_factory, client_factory=client_factory,
        )
        self.assertEqual(result["methods"]["dassle"], ["M0", "M1", "M2", "M3"])
        self.assertEqual(result["methods"]["slobench"], ["RAW", "M1", "M2", "M3"])
        self.assertTrue((self.root / "campaign/workers/dassle/0/STATUS.json").is_file())
        self.assertTrue((self.root / "campaign/phase-complete/slobench.json").is_file())

    def test_dassle_analysis_executes_literal_classification(self) -> None:
        result = analyze(
            [{"id": "x", "input": "Vabc", "reference": "Uabc"}],
            [{"id": "x", "input": "Vabc", "reference": "Uabc", "results": {"M1": {"output": "Uabc"}}}],
        )
        self.assertNotEqual(result["status"], "MECHANICAL_AUDIT_DRIVER_SELECTED")
        self.assertEqual(result["literal_pattern_units"].get("uv_initial"), 1)
        self.assertEqual(result["new_model_calls"], 0)

    def test_dassle_cli_dispatch_executes_audit_without_transport(self) -> None:
        transport = PromptTransport()
        result = self.run_variant("dassle-uv-audit", transport)
        self.assertEqual(result["model_calls"], 0)
        self.assertEqual(result["status"], "ANALYZED_LITERAL_EDIT_UNITS")
        self.assertEqual(transport.calls, [])


if __name__ == "__main__":
    unittest.main()
