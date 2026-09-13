"""Focused executable checks for the second 007-f fidelity review."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research.curated import historical_transport
from research.curated.historical import variant_map
from research.curated.historical_campaign import run_injected
from research.curated.historical_common import safe_component
from research.curated.historical_pipeline import Pipeline
from research.curated.historical_retry10 import run_record
from research.curated.historical_ten_run import run_scheduled_trials
from research.curated.historical_transport import Client
from research.curated.historical_validator import run_validator_records
from research.curated.historical_variants import build_historical_pipeline
from research.curated.pipeline import replay
from research.curated.review import Proposal
from research.tools.replay import _create_fixture_index, verify_representative_roots
from research.tools.reproduce import execute_authorized


def _response(output: str) -> dict[str, object]:
    return {
        "model": "qwen3.8-27b",
        "status": "completed",
        "id": "synthetic",
        "reasoning": {"effort": "low"},
        "usage": {"output_tokens": 3, "output_tokens_details": {"reasoning_tokens": 1}},
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": output}],
            }
        ],
    }


class FixedTransport:
    def __init__(self, outputs: list[str]) -> None:
        self.outputs = list(outputs)
        self.calls: list[dict[str, object]] = []

    def request(self, _endpoint: str, body: bytes, _headers: object, _timeout: float):
        request = json.loads(body)
        self.calls.append(request)
        output = self.outputs.pop(0) if self.outputs else "delta"
        return 200, {"Content-Type": "application/json"}, json.dumps(_response(output)).encode()


class AddendumFidelityTests(unittest.TestCase):
    def setUp(self) -> None:
        parent = os.environ.get("TMPDIR")
        self.assertTrue(parent and not parent.startswith("/" + "tmp"))
        self.root = Path(tempfile.mkdtemp(prefix="addendum-fidelity-", dir=parent))
        self.index = self.root / "index.sqlite"
        _create_fixture_index({"unigrams": {"foo": 100, "bar": 100, "beta": 100}}, self.index)

    def args(
        self, records: list[dict[str, object]], *, output: str = "output"
    ) -> argparse.Namespace:
        inputs = self.root / "inputs"
        inputs.mkdir(exist_ok=True)
        (inputs / "records.json").write_text(json.dumps(records))
        return argparse.Namespace(
            input_root=str(inputs),
            index=str(self.index),
            output_root=str(self.root / output),
            max_cases=len(records),
            endpoint="http://example.invalid/v1",
            credential_env="SYNTHETIC_RESEARCH_CREDENTIAL",
            timeout_seconds=30,
            workers=1,
            model="qwen3.8-27b",
            allow_live=True,
            trials=1,
            retry_limit=1,
        )

    def test_raw_and_hyphen_views_select_different_candidates(self) -> None:
        raw = build_historical_pipeline(self.index, maximum=None, detector_view="raw")
        hyphen = build_historical_pipeline(self.index, maximum=None, detector_view="hyphen-space")
        try:
            raw_result = raw.detect("foo-bar")
            hyphen_result = hyphen.detect("foo-bar")
        finally:
            raw.close()
            hyphen.close()
        self.assertEqual([item["text"] for item in raw_result["candidates"]], ["foo-bar"])
        self.assertEqual(hyphen_result["candidates"], [])
        self.assertEqual(raw_result["detector_view"], "raw")
        self.assertEqual(hyphen_result["detector_view"], "hyphen-space")

    def test_both_hyphen_descendants_reach_word_only_retry(self) -> None:
        for variant_id in ("full-hyphen-space-low", "full-hyphen-case-low"):
            with self.subTest(variant=variant_id):
                args = self.args([{"id": "case", "input": "alpha"}], output=variant_id)
                transport = FixedTransport(
                    [
                        json.dumps(
                            {"keep": False, "replacement": "gamma", "needs_wider_edit": False}
                        ),
                        "beta",
                    ]
                )
                with (
                    patch.dict(
                        os.environ, {"SYNTHETIC_RESEARCH_CREDENTIAL": "synthetic-placeholder"}
                    ),
                    patch.object(historical_transport._HttpTransport, "request", transport.request),
                ):
                    result = execute_authorized(args, variant_map()[variant_id])
                self.assertEqual(result["network_calls"], 2)
                self.assertIn("Ta beseda", transport.calls[1]["input"][0]["content"][0]["text"])

    def test_retry10_uses_latest_english_suppression_and_fixed_anchor(self) -> None:
        args = self.args([{"id": "case", "input": "alpha"}], output="retry10-suppressed")
        inputs = Path(args.input_root)
        (inputs / "english.json").write_text(json.dumps({"alpha": 5.0}))
        with patch.dict(os.environ, {"SYNTHETIC_RESEARCH_CREDENTIAL": "synthetic-placeholder"}):
            result = execute_authorized(args, variant_map()["prijigrala-retry10"])
        self.assertEqual(result["model_calls"], 0)
        self.assertEqual(result["status"], "ENGLISH_ATTESTED_PRESERVED")

        (inputs / "english.json").write_text(json.dumps({"alpha": 0.0}))
        args.output_root = str(self.root / "retry10-fixed-anchor")
        transport = FixedTransport(
            [
                json.dumps({"keep": False, "replacement": "gamma", "needs_wider_edit": False}),
                "delta",
                "delta",
            ]
        )
        args.retry_limit = 2
        with (
            patch.dict(os.environ, {"SYNTHETIC_RESEARCH_CREDENTIAL": "synthetic-placeholder"}),
            patch.object(historical_transport._HttpTransport, "request", transport.request),
        ):
            result = execute_authorized(args, variant_map()["prijigrala-retry10"])
        retry_prompts = [call["input"][0]["content"][0]["text"] for call in transport.calls[1:]]
        self.assertEqual(len(transport.calls), 3)
        self.assertEqual(retry_prompts[0], retry_prompts[1])
        self.assertIn("gamma", retry_prompts[0])
        self.assertEqual(result["status"], "RETRY_LIMIT_REACHED")

    def test_configurations_have_one_coherent_request_section(self) -> None:
        configs = Path(__file__).resolve().parents[1] / "configs"
        no_model = {
            "007-b-replacement",
            "007-b-timeout300",
            "dassle-uv-audit",
            "levenshtein-lookup-diagnostic",
            "007-h-unique-one-letter-unigram-substitution",
        }
        for path in configs.glob("*.json"):
            value = json.loads(path.read_text())
            request = value.get("request")
            self.assertIsInstance(request, dict, path.name)
            if value["experiment_id"] in no_model:
                self.assertNotIn("generic_prompt", value)
                self.assertNotIn("retry_prompt", value)
                self.assertNotIn("historical_wire_keys", value)
                self.assertEqual(request.get("model_calls"), 0)
                self.assertNotIn("prompt", request)
                self.assertNotIn("wire_keys", request)
            elif value["experiment_id"] == "low-plus-validator":
                self.assertNotIn("generic_prompt", value)
                self.assertNotIn("retry_prompt", value)
                self.assertIn("validat", request["prompt"].casefold())
                self.assertIn("frozen first-stage", " ".join(request["content"]).casefold())
            elif value["experiment_id"] == "007-j-levenshtein-one-contextual-validator":
                self.assertEqual(
                    request["fields"],
                    ["model", "stream", "store", "input", "include_reasoning", "reasoning"],
                )
                self.assertFalse(request["stream"])
                self.assertFalse(request["store"])
                self.assertTrue(request["include_reasoning"])
                self.assertEqual(request["reasoning_effort"], "low")
            else:
                self.assertEqual(request["wire_keys"], value["historical_wire_keys"])
                self.assertIn("prompt", request)

    def test_original_attempts_use_exact_report_hashes_and_no_wildcards(self) -> None:
        catalog = json.loads(
            (Path(__file__).resolve().parents[1] / "registry/experiments.json").read_text()
        )
        mappings = {item["id"]: item for item in catalog["original_attempt_mappings"]}
        self.assertEqual(
            mappings["007-a-original-attempt"]["source_evidence_sha256"],
            "ac84a66c1d37a80601e0910fd32f4ea547281a787c896f50c8f1630bc188cc19",
        )
        self.assertEqual(
            mappings["007-b-original-attempt"]["source_evidence_sha256"],
            "9f973123e1a89116e17dd408c5a6da29989d6e27680c44a742a95401f2f95a66",
        )
        self.assertNotIn("*", json.dumps(mappings))

    def test_campaign_uses_distinct_processes_and_disjoint_partitions(self) -> None:
        def pipeline_factory():
            return Pipeline(self.index, english_lookup=lambda _word: 0.0, maximum=None)

        def client_factory():
            return Client(
                transport=FixedTransport(
                    [json.dumps({"keep": True, "replacement": None, "needs_wider_edit": False})]
                )
            )

        rows = [
            {"benchmark": "synthetic", "id": f"case-{index}", "index": index, "input": "alpha"}
            for index in range(1, 5)
        ]
        result = run_injected(
            rows,
            output_root=self.root / "campaign",
            workers=2,
            pipeline_factory=pipeline_factory,
            client_factory=client_factory,
        )
        statuses = [item for item in result["worker_statuses"] if item["phase"] == "synthetic"]
        self.assertEqual(len(statuses), 2)
        self.assertEqual(len({item["pid"] for item in statuses}), 2)
        self.assertEqual(
            sorted(statuses[0]["assigned_indices"] + statuses[1]["assigned_indices"]), [1, 2, 3, 4]
        )
        self.assertEqual(result["process_scheduler"], "multiprocessing-worker-processes")

    def test_failed_before_status_is_recorded_as_worker_incident(self) -> None:
        def broken_pipeline_factory():
            raise RuntimeError("synthetic worker setup failure")

        def client_factory():
            return object()

        result = run_injected(
            [{"benchmark": "synthetic", "id": "case", "index": 1, "input": "alpha"}],
            output_root=self.root / "failed-worker",
            workers=1,
            pipeline_factory=broken_pipeline_factory,
            client_factory=client_factory,
        )
        self.assertEqual(result["status"], "RECORDED_WITH_WORKER_INCIDENTS")
        status = json.loads(
            (self.root / "failed-worker/workers/synthetic/0/STATUS.json").read_text()
        )
        self.assertEqual(status["status"], "WORKER_FAILED_BEFORE_COMPLETION")
        self.assertEqual(status["worker_incident"], "worker exited with code 1")

    def test_new_driver_boundaries_reject_unsafe_ids_before_writes(self) -> None:
        with self.assertRaises(ValueError):
            run_validator_records(
                [{"id": "../escape"}], object(), self.root / "validator", model="qwen3.8-27b"
            )
        self.assertFalse((self.root / "validator").exists())
        with self.assertRaises(ValueError):
            run_scheduled_trials(
                [{"id": "", "input": "alpha"}],
                "ten-run-initial-case-low",
                object(),
                object(),
                self.root / "ten",
            )
        self.assertFalse((self.root / "ten").exists())
        with self.assertRaises(ValueError):
            run_record(
                {"id": "../escape", "input": "alpha"}, object(), object(), self.root / "retry10"
            )
        self.assertFalse((self.root / "retry10").exists())
        with self.assertRaises(ValueError):
            safe_component("")
        with self.assertRaises(ValueError):
            safe_component("..")

    def test_representative_root_verification_reports_counts_and_hashes_only(self) -> None:
        first = self.root / "first.bin"
        second = self.root / "second.bin"
        first.write_bytes(b"first")
        second.write_bytes(b"second")
        ledger = self.root / "ledger.json.gz"
        entries = {
            "entries": [
                {
                    "root": "experiments/a",
                    "relative_path": "first.bin",
                    "classification": "private-only",
                    "sha256": hashlib.sha256(b"first").hexdigest(),
                    "size": 5,
                },
                {
                    "root": "recovery/a",
                    "relative_path": "second.bin",
                    "classification": "private-only",
                    "sha256": hashlib.sha256(b"second").hexdigest(),
                    "size": 6,
                },
            ]
        }
        with gzip.GzipFile(ledger, "wb", mtime=0) as handle:
            handle.write(json.dumps(entries).encode())
        receipt = verify_representative_roots(
            ledger,
            root_map={"experiments/a": self.root, "recovery/a": self.root},
        )
        self.assertEqual(receipt["checked"], 2)
        encoded = json.dumps(receipt)
        self.assertNotIn(str(self.root), encoded)
        self.assertNotIn("first.bin", encoded)
        self.assertIn(hashlib.sha256(b"first").hexdigest(), encoded)

    def test_retry_failure_hides_public_edits_but_keeps_m3_first_stage_edits(self) -> None:
        index = self.root / "replay-two.sqlite"
        _create_fixture_index({"unigrams": {"ok": 100}}, index)
        with __import__("research.curated.corpus", fromlist=["Corpus"]).Corpus(index) as corpus:
            result = replay(
                "alpha beta",
                corpus,
                lambda _word: 0.0,
                {"0": Proposal(False, "ok", False), "6": Proposal(False, "gamma", False)},
                retry_failures={"6": {"failure": "TIMEOUT"}},
            )
        self.assertEqual(result["output"], "alpha beta")
        self.assertEqual(result["edits"], [])
        self.assertEqual(result["candidate_edits_before_failure_fallback"], [(0, 5, "ok")])
        self.assertEqual(result["no_retry_output"], "ok beta")
        self.assertEqual(result["no_retry_edits"], [(0, 5, "ok")])


if __name__ == "__main__":
    unittest.main()
