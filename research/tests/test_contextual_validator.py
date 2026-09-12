"""Offline proof surface for the 007-i pre-live correction."""

from __future__ import annotations

import copy
import json
import os
import stat
import tempfile
import threading
import time
import unittest
from pathlib import Path

from research import contextual_validator as protocol
from research.tools import run_contextual_validator as driver


def response(text: str = "USE_CANDIDATE") -> dict[str, object]:
    return {
        "id": "synthetic-response",
        "status": "completed",
        "model": protocol.MODEL,
        "reasoning": {"effort": protocol.EFFORT},
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
    def __init__(self, payload: dict[str, object] | None = None) -> None:
        self.payload = json.dumps(payload or response(), ensure_ascii=False).encode("utf-8")
        self.calls: list[tuple[str, bytes, dict[str, str], float]] = []

    def request(
        self, endpoint: str, body: bytes, headers: dict[str, str], timeout: float
    ) -> tuple[int, dict[str, str], bytes]:
        self.calls.append((endpoint, body, headers, timeout))
        return 200, {"Content-Type": "application/json"}, self.payload


class RaisingTransport(FakeTransport):
    def request(
        self, endpoint: str, body: bytes, headers: dict[str, str], timeout: float
    ) -> tuple[int, dict[str, str], bytes]:
        self.calls.append((endpoint, body, headers, timeout))
        raise TimeoutError("synthetic timeout")


def candidate(
    index: int,
    *,
    phase: str = "dassle-spelling",
    start: int | None = None,
    target: str = "old",
    replacement: str = "new",
) -> dict[str, object]:
    start = index if start is None else start
    return {
        "phase": phase,
        "case_index": index + 1,
        "target_start": start,
        "target_end": start + len(target),
        "target_ordinal": index % 3,
        "candidate": {"start": start, "end": start + len(target), "text": target},
        "candidate_form": "vocabulary-form",
        "mechanical_edit": [start, start + len(target), replacement],
        "sentence": "synthetic sentence",
        "reference": None,
    }


def call(kind: str = "reviewer", *, failed: bool = False) -> dict[str, object]:
    return {"kind": kind, "operational_failure": failed}


def saved_case(source: str = "a b c") -> dict[str, object]:
    def decision(
        start: int, text: str, replacement: str, *, failed: bool = False
    ) -> dict[str, object]:
        return {
            "candidate": {"start": start, "end": start + len(text), "text": text},
            "final_gate": {"accepted": True},
            "final_case": {"adjusted_replacement": replacement},
            "first": call(failed=failed),
            "retry": None,
        }

    decisions = [decision(0, "a", "A"), decision(2, "b", "B")]
    return {
        "id": "case",
        "index": 1,
        "input": source,
        "input_sha256": "synthetic",
        "detector": {"candidates": [], "english": []},
        "decisions": decisions,
        "calls": [decisions[0]["first"], decisions[1]["first"]],
        "output": "A B c",
        "operational_failure": False,
    }


class ContextualValidatorTests(unittest.TestCase):
    def test_prompt_body_uses_exact_gated_replacement_and_no_extra_context(self) -> None:
        item = candidate(0, start=0, target="Stari", replacement="Novi")
        item["candidate_form"] = "vocabulary-form"
        fake = FakeTransport()
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            driver._call_one(root, item, "https://synthetic.invalid/v1", "UNUSED", transport=fake)
            request_path = next((root / "requests").iterdir()) / "request.json"
            body = json.loads(request_path.read_text(encoding="utf-8"))
        self.assertEqual(body, protocol.request_body("synthetic sentence", "Stari", "Novi"))
        prompt = body["input"][0]["content"][0]["text"]
        self.assertEqual(prompt, protocol.prompt_text("synthetic sentence", "Stari", "Novi"))
        self.assertNotIn("vocabulary-form", prompt)

    def test_prompt_hash_and_request_field_set_are_frozen(self) -> None:
        self.assertEqual(protocol.prompt_sha256(), protocol.FROZEN_PROMPT_SHA256)
        body = protocol.request_body("Sentence.", "old", "new")
        self.assertEqual(
            set(body), {"model", "stream", "store", "input", "include_reasoning", "reasoning"}
        )
        self.assertEqual(body["model"], protocol.MODEL)
        self.assertFalse(body["stream"])
        self.assertFalse(body["store"])
        self.assertTrue(body["include_reasoning"])
        self.assertEqual(body["reasoning"], {"effort": "low"})

    def test_parser_accepts_only_exact_choices_and_rejects_extra_fields(self) -> None:
        parsed = protocol.parse_response(response("  KEEP_ORIGINAL\n"))
        self.assertEqual(parsed["decision"], "KEEP_ORIGINAL")
        for text in ("USE_CANDIDATE extra", '{"decision":"USE_CANDIDATE"}', ""):
            with self.subTest(text=text), self.assertRaises(protocol.ValidatorError):
                protocol.parse_response(response(text))
        duplicate_output = response()
        duplicate_output["output"] = [
            *duplicate_output["output"],
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": "KEEP_ORIGINAL"}],
            },
        ]
        with self.assertRaises(protocol.ValidatorError):
            protocol.parse_response(duplicate_output)
        with self.assertRaises(protocol.ValidatorError):
            protocol.parse_response_bytes(b'{"status":"completed","status":"completed"}')

    def test_parser_verifies_model_effort_and_token_accounting(self) -> None:
        for changed in (
            {"model": "other"},
            {"reasoning": {"effort": "high"}},
            {
                "usage": {
                    "input_tokens": 1,
                    "output_tokens": 1,
                    "output_tokens_details": {"reasoning_tokens": -1},
                }
            },
            {"status": "in_progress"},
        ):
            value = response()
            value.update(changed)
            with self.subTest(changed=changed), self.assertRaises(protocol.ValidatorError):
                protocol.parse_response(value)

    def test_integrity_is_exact_original_coordinate_proof(self) -> None:
        source = "aa bb cc"
        allowed = [[0, 2, "XX"], [6, 8, "YY"]]
        exact = protocol.integrity(source, "XX bb YY", allowed)
        self.assertEqual(exact["protected_differences"], 0)
        self.assertEqual(exact["outside_span_differences"], 0)
        self.assertTrue(exact["exact_expected_output"])
        for altered in ("ZZ bb YY", "XX bb ZZ", "XX ZZ YY"):
            with self.subTest(altered=altered):
                self.assertGreater(
                    protocol.integrity(source, altered, allowed)["outside_span_differences"], 0
                )
        url = "keep https://example.test now"
        with self.assertRaises(protocol.ValidatorError):
            protocol.integrity(url, url, [[5, 24, "other.test"]])

    def test_candidate_population_uses_injected_recomputation_seam(self) -> None:
        record = {
            "index": 1,
            "id": "synthetic",
            "baseline": {"input": "Aaa"},
            "dataset": {"reference": None},
            "mechanical": {
                "targets": [
                    {
                        "cardinality": "C=1",
                        "accepted": True,
                        "candidate": {"start": 0, "end": 3, "text": "Aaa"},
                        "candidate_forms": ["abb"],
                        "gate": {"edit": [0, 3, "Abb"]},
                    }
                ]
            },
        }
        seen: list[tuple[str, tuple[str, ...]]] = []

        def injected(lookup: str, bucket: object) -> list[str]:
            seen.append((lookup, tuple(bucket)))  # type: ignore[arg-type]
            return ["abb"]

        population = driver.build_population(
            {"dassle-spelling": [record]},
            {"abb"},
            {3: ["abb"]},
            qualifier=injected,
            expected_counts={"dassle-spelling": 1},
            expected_total=1,
        )
        self.assertEqual(len(population), 1)
        self.assertEqual(seen, [("aaa", ("abb",))])
        self.assertEqual(population[0]["mechanical_edit"], [0, 3, "Abb"])
        changed_detector = copy.deepcopy(record)
        changed_detector["baseline"]["detector"] = {"english": "changed"}
        self.assertEqual(
            driver.build_population(
                {"dassle-spelling": [changed_detector]},
                {"abb"},
                {3: ["abb"]},
                qualifier=lambda _lookup, _bucket: ["abb"],
                expected_counts={"dassle-spelling": 1},
                expected_total=1,
            ),
            population,
        )

    def test_partitions_are_disjoint_complete_deterministic_and_bounded(self) -> None:
        candidates = [candidate(index) for index in range(735)]
        left = protocol.partitions(candidates)
        right = protocol.partitions(list(reversed(candidates)))
        left_keys = [protocol.stable_key(item) for worker in left.values() for item in worker]
        right_keys = [protocol.stable_key(item) for worker in right.values() for item in worker]
        self.assertEqual(len(left_keys), 735)
        self.assertEqual(len(set(left_keys)), 735)
        self.assertEqual(sorted(left_keys), sorted(right_keys))
        self.assertTrue(all(len(value) in {91, 92} for value in left.values()))
        for worker, values in left.items():
            self.assertEqual(
                [protocol.stable_key(item) for item in values],
                [protocol.stable_key(item) for item in protocol.ordered_candidates(candidates)][
                    worker::8
                ],
            )

    def test_persistence_dispatch_failures_and_request_only_unknown_are_terminal(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            body = protocol.request_body("Sentence.", "old", "new")
            failed = RaisingTransport()
            observation = protocol.perform_call(
                root / "failed",
                body,
                endpoint="https://synthetic.invalid",
                transport=failed,
            )
            self.assertTrue(observation["operational_failure"])
            self.assertEqual(observation["dispatch"], "ATTEMPTED")
            self.assertIsNone(observation["http_status"])
            self.assertEqual(len(failed.calls), 1)
            resumed = root / "resumed"
            protocol.immutable_write(resumed / "request.json", protocol.canonical_bytes(body))
            fake = FakeTransport()
            uncertain = protocol.perform_call(
                resumed,
                body,
                endpoint="https://synthetic.invalid",
                transport=fake,
            )
            self.assertEqual(uncertain["failure"], "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE")
            self.assertEqual(uncertain["dispatch"], "UNKNOWN")
            self.assertEqual(len(fake.calls), 0)

    def test_persistence_is_immutable_and_never_resamples(self) -> None:
        fake = FakeTransport()
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            body = protocol.request_body("Sentence.", "old", "new")
            first = protocol.perform_call(
                root, body, endpoint="https://synthetic.invalid", transport=fake
            )
            second = protocol.perform_call(
                root, body, endpoint="https://synthetic.invalid", transport=fake
            )
            self.assertEqual(first, second)
            self.assertEqual(len(fake.calls), 1)
            self.assertEqual(
                [path.name for path in sorted(root.iterdir())],
                ["dispatch.json", "observation.json", "raw-response.json", "request.json"],
            )
            self.assertEqual(first["decision"], "USE_CANDIDATE")

    def test_worker_execution_has_one_call_per_candidate_and_at_most_eight_in_flight(self) -> None:
        class ConcurrentTransport(FakeTransport):
            def __init__(self) -> None:
                super().__init__()
                self._lock = threading.Lock()
                self.active = 0
                self.maximum = 0

            def request(self, endpoint: str, body: bytes, headers: dict[str, str], timeout: float):
                with self._lock:
                    self.active += 1
                    self.maximum = max(self.maximum, self.active)
                time.sleep(0.002)
                with self._lock:
                    self.active -= 1
                return super().request(endpoint, body, headers, timeout)

        fake = ConcurrentTransport()
        population = [candidate(index) for index in range(17)]
        with tempfile.TemporaryDirectory() as raw_root:
            observations, status = driver.execute_validator(
                Path(raw_root),
                population,
                endpoint="https://synthetic.invalid",
                credential_env="UNUSED",
                transport=fake,
            )
        self.assertEqual(len(observations), 17)
        self.assertEqual(status["observation_records"], 17)
        self.assertEqual(status["dispatched_http_requests"], 17)
        self.assertEqual(status["uncertain_deliveries"], 0)
        self.assertLessEqual(fake.maximum, protocol.WORKERS)
        self.assertEqual(len(fake.calls), 17)

    def test_projection_scheduled_target_only_semantics_and_shared_observations(self) -> None:
        saved = saved_case()
        scheduled = {(0, 1, "a"), (2, 3, "b")}
        only = driver.projection_result(saved, [[0, 1, "X"]], only=True, scheduled=scheduled)
        self.assertEqual(only["output"], "X b c")
        self.assertEqual(len(only["decisions"]), 0)
        self.assertEqual(only["calls"], [])
        saved_failure = copy.deepcopy(saved)
        saved_failure["decisions"][0]["first"]["operational_failure"] = True  # type: ignore[index]
        saved_failure["operational_failure"] = True
        avoided = driver.projection_result(
            saved_failure, [[0, 1, "X"]], only=True, scheduled=scheduled
        )
        self.assertEqual(avoided["output"], "X b c")
        self.assertFalse(avoided["operational_failure"])
        unscheduled_failure = copy.deepcopy(saved)
        failure_call = unscheduled_failure["decisions"][1]["first"]
        failure_call["operational_failure"] = True  # type: ignore[index]
        unscheduled_failure["operational_failure"] = True
        failed = driver.projection_result(
            unscheduled_failure,
            [[0, 1, "X"]],
            only=True,
            scheduled={(0, 1, "a")},
        )
        self.assertEqual(failed["output"], "a b c")
        self.assertTrue(failed["operational_failure"])
        compatible = driver.projection_result(
            saved, [[0, 1, "X"]], only=True, scheduled={(0, 1, "a")}
        )
        self.assertEqual(compatible["output"], "X B c")
        conflicting = driver.projection_result(
            saved, [[2, 3, "X"]], only=True, scheduled={(0, 1, "a")}
        )
        self.assertTrue(conflicting["operational_failure"])

    def test_fallback_keeps_saved_failure_for_rejected_scheduled_target(self) -> None:
        saved = saved_case()
        saved["decisions"][0]["first"]["operational_failure"] = True  # type: ignore[index]
        saved["operational_failure"] = True
        fallback = driver.project_saved_case(saved["input"], saved, [])
        self.assertTrue(fallback["operational_failure"])
        self.assertEqual(fallback["output"], saved["input"])
        bypassed = driver.project_saved_case(saved["input"], saved, [[0, 1, "X"]])
        self.assertFalse(bypassed["operational_failure"])
        self.assertEqual(bypassed["output"], "X B c")

    def test_both_projections_share_the_same_validator_observation(self) -> None:
        saved = saved_case()
        case = {
            "phase": "dassle-spelling",
            "index": 1,
            "id": "case",
            "dataset": {"reference": None},
            "baseline": saved,
            "new": copy.deepcopy(saved),
        }
        item = {
            **candidate(0, start=0, target="a", replacement="X"),
            "sentence": saved["input"],
        }
        observation = {
            "decision": "USE_CANDIDATE",
            "operational_failure": False,
            "dispatch": "ATTEMPTED",
            "http_seconds": 0.1,
            "reasoning_tokens": 1,
            "output_tokens": 1,
        }
        record = driver.make_case_result(
            "dassle-spelling",
            case,
            [item],
            {protocol.candidate_path_id(item): observation},
            "config",
        )
        self.assertEqual(record["validated_fallback"]["output"], "X B c")
        self.assertEqual(record["validated_only"]["output"], "X B c")
        self.assertEqual(record["unrestricted_007h"], case["new"])
        self.assertEqual(record["validator_targets"][0]["observation"], observation)

    def test_public_projection_redacts_private_endpoint_profile_path_and_payload(self) -> None:
        configuration = {
            "implementation_head": "implementation",
            "prior_007h_head": "prior",
            "source_identity": {"candidate_manifest_sha256": "candidate", "candidate_count": 735},
            "deployment": {
                "class": "A100-FP8",
                "model": protocol.MODEL,
                "protocol": "Responses non-streaming",
                "profile_sha256": driver.FROZEN_PROFILE_SHA256,
                "endpoint": "https://private.example/v1",
                "profile_path": "/private/profile.toml",
                "credential_env": "PRIVATE_CREDENTIAL",
            },
            "request": {},
            "parser": {},
            "scheduling": {},
            "limits": {},
            "projections": {},
        }
        result = {
            "status": "COMPLETE",
            "private_results_sha256": "results",
            "private_manifest_sha256": "manifest",
            "metrics": {
                "actual_validator_call_records": 735,
                "dispatched_http_requests": 735,
                "uncertain_deliveries": 0,
            },
        }
        public_config, _public_result = driver.public_projection(configuration, result)
        serialized = json.dumps(public_config, sort_keys=True)
        self.assertNotIn("private.example", serialized)
        self.assertNotIn("/private/profile.toml", serialized)
        self.assertNotIn("PRIVATE_CREDENTIAL", serialized)
        self.assertEqual(
            public_config["deployment"]["profile_sha256"], driver.FROZEN_PROFILE_SHA256
        )

    def test_attribution_is_isolated_and_unresolved_is_distinct(self) -> None:
        self.assertEqual(
            protocol.attribution("abc", "xbc", [0, 3, "xbc"])["status"],
            "exact_reference",
        )
        self.assertEqual(
            protocol.attribution("abc", None, [0, 3, "xbc"])["status"],
            "unresolved",
        )

    def test_call_accounting_compares_unequal_baseline_and_007h_counts(self) -> None:
        accounting = driver.call_accounting(
            {"first": 10, "retry": 4, "total": 14},
            {"first": 8, "retry": 1, "total": 9},
            {"first": 3, "retry": 1, "total": 4},
            735,
        )
        self.assertEqual(
            accounting["ordinary_avoided_vs_baseline"],
            {"first": 7, "retry": 3, "total": 10},
        )
        self.assertEqual(
            accounting["ordinary_avoided_vs_007h"],
            {"first": 5, "retry": 0, "total": 5},
        )
        self.assertEqual(accounting["net_projected"], {"first": 3, "retry": 1, "total": 739})
        self.assertEqual(accounting["delta_vs_baseline"], 725)
        self.assertEqual(accounting["delta_vs_007h"], 730)

    def test_global_metrics_count_failures_attempts_and_uncertain_deliveries(self) -> None:
        metrics = driver.observation_metrics(
            [
                {
                    "decision": "USE_CANDIDATE",
                    "operational_failure": False,
                    "dispatch": "ATTEMPTED",
                    "http_seconds": 2.0,
                    "reasoning_tokens": 3,
                    "output_tokens": 4,
                },
                {
                    "decision": None,
                    "operational_failure": True,
                    "failure": "TIMEOUT",
                    "dispatch": "ATTEMPTED",
                    "http_seconds": 5.0,
                    "reasoning_tokens": None,
                    "output_tokens": None,
                },
                {
                    "decision": None,
                    "operational_failure": True,
                    "failure": "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE",
                    "dispatch": "UNKNOWN",
                    "http_seconds": None,
                    "reasoning_tokens": None,
                    "output_tokens": None,
                },
            ]
        )
        self.assertEqual(metrics["observation_count"], 3)
        self.assertEqual(metrics["dispatched_attempts"], 2)
        self.assertEqual(metrics["uncertain_deliveries"], 1)
        self.assertEqual(metrics["failure_counts"]["TIMEOUT"], 1)
        self.assertEqual(metrics["latency_seconds"]["n"], 2)

    def test_missing_live_inputs_stop_before_request_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            with self.assertRaises(protocol.ValidatorError):
                protocol.perform_call(root / "candidate", protocol.request_body("s", "o", "n"))
            self.assertFalse((root / "candidate" / "request.json").exists())

    def test_private_directory_boundaries_reject_symlink_wrong_mode_and_escape(self) -> None:
        fake = FakeTransport()
        body = protocol.request_body("s", "o", "n")
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            wrong = root / "wrong"
            wrong.mkdir(mode=0o755)
            with self.assertRaises(protocol.ValidatorError):
                protocol.perform_call(wrong / "candidate", body, transport=fake, private_root=wrong)
            target = root / "target"
            target.mkdir(mode=0o700)
            symlink_parent = root / "symlink-parent"
            symlink_parent.symlink_to(target, target_is_directory=True)
            with self.assertRaises(protocol.ValidatorError):
                protocol.perform_call(
                    symlink_parent / "candidate", body, transport=fake, private_root=root
                )
            outside = root.parent / (root.name + "-outside")
            outside.mkdir(mode=0o700)
            try:
                with self.assertRaises(protocol.ValidatorError):
                    protocol.perform_call(
                        outside / "candidate", body, transport=fake, private_root=root
                    )
            finally:
                outside.rmdir()

    def test_public_writer_does_not_chmod_repository_directories(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            parent = Path(raw_root) / "research" / "results"
            parent.mkdir(parents=True, mode=0o755)
            before = stat.S_IMODE(parent.stat().st_mode)
            driver.public_immutable_write(parent / "result.json", b"{}\n")
            self.assertEqual(stat.S_IMODE(parent.stat().st_mode), before)

    def test_profile_hash_and_private_deployment_inputs_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            profile = Path(raw_root) / "profile.toml"
            profile.write_text("synthetic\n", encoding="utf-8")
            os.environ["SYNTHETIC_CREDENTIAL"] = "fake-key"
            try:
                with self.assertRaises(driver.ExperimentError):
                    driver.validate_freeze_inputs(
                        "https://synthetic.invalid/v1", profile, "SYNTHETIC_CREDENTIAL"
                    )
            finally:
                os.environ.pop("SYNTHETIC_CREDENTIAL", None)
        with self.assertRaises(driver.ExperimentError):
            driver.validate_freeze_inputs(None, None, None)


if __name__ == "__main__":
    unittest.main()
