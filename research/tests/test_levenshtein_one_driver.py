from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research import contextual_validator as protocol
from research.tools import run_levenshtein_one as driver


def candidate(
    index: int,
    *,
    operation: str = driver.distance_one.SUBSTITUTION,
    target: str = "old",
    replacement: str = "new",
) -> dict[str, object]:
    start = index
    return {
        "phase": "dassle-spelling",
        "case_index": index + 1,
        "case_id": f"case-{index}",
        "target_ordinal": 0,
        "target_start": start,
        "target_end": start + len(target),
        "candidate": {"start": start, "end": start + len(target), "text": target},
        "candidate_form": replacement,
        "operation": operation,
        "mechanical_edit": [start, start + len(target), replacement],
        "sentence": "synthetic sentence",
        "reference": None,
    }


def validator_response(choice: str = "KEEP_ORIGINAL") -> dict[str, object]:
    return {
        "status": "completed",
        "model": protocol.MODEL,
        "reasoning": {"effort": protocol.EFFORT},
        "usage": {
            "input_tokens": 1,
            "output_tokens": 1,
            "output_tokens_details": {"reasoning_tokens": 1},
        },
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": choice}],
            }
        ],
    }


class FakeTransport:
    def __init__(self, choice: str = "KEEP_ORIGINAL") -> None:
        self.payload = json.dumps(validator_response(choice)).encode("utf-8")
        self.calls = 0

    def request(
        self, endpoint: str, body: bytes, headers: dict[str, str], timeout: float
    ) -> tuple[int, dict[str, str], bytes]:
        del endpoint, body, headers, timeout
        self.calls += 1
        return 200, {"Content-Type": "application/json"}, self.payload


def reuse_fixture() -> tuple[
    dict[str, object], dict[str, object], bytes, dict[str, object], dict[str, object]
]:
    item = candidate(1, target="old", replacement="new")
    old_item = copy.deepcopy(item)
    request_bytes = b"frozen request bytes"
    deployment = {
        "model": protocol.MODEL,
        "profile_sha256": driver.EXPECTED_PROFILE,
        "profile_path": "/private/profile.toml",
        "endpoint": "https://private.invalid/v1",
        "protocol": "Responses non-streaming",
    }
    configuration = {
        "prompt": {"sha256": driver.EXPECTED_PROMPT},
        "deployment": deployment,
        "request": {
            "fields": driver.EXPECTED_REQUEST_FIELDS,
            "stream": False,
            "store": False,
            "include_reasoning": True,
            "reasoning_effort": protocol.EFFORT,
        },
        "parser": copy.deepcopy(driver.EXPECTED_PARSER),
        "limits": {
            "timeout_seconds": protocol.TIMEOUT_SECONDS,
            "response_bound_bytes": protocol.MAX_RESPONSE_BYTES,
            "attempts_per_candidate": 1,
            "resampling": False,
        },
    }
    return item, old_item, request_bytes, configuration, deployment


def saved_case() -> dict[str, object]:
    source_candidate = {"start": 0, "end": 1, "text": "a"}
    return {
        "id": "saved-case",
        "index": 1,
        "input": "a B c",
        "input_sha256": hashlib.sha256(b"a B c").hexdigest(),
        "detector": {"candidates": [], "english": []},
        "decisions": [
            {
                "candidate": source_candidate,
                "first": None,
                "retry": None,
                "final_gate": {"accepted": False},
            }
        ],
        "calls": [],
        "output": "a B c",
        "edits": [],
        "operational_failure": False,
    }


class LevenshteinOneDriverTests(unittest.TestCase):
    def test_native_root_is_direct_and_named_recovery_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=driver.NATIVE_RUNTIME_PARENT) as raw_root:
            native = Path(raw_root) / "native"
            native.mkdir(mode=0o700)
            os.chmod(native, 0o700)
            with patch.object(driver, "NATIVE_RUNTIME_PARENT", native):
                with self.assertRaisesRegex(driver.ExperimentError, "native runtime parent"):
                    driver.ensure_scratch(native.parent / "007-j-recovery.outside")
                with self.assertRaisesRegex(driver.ExperimentError, "unique recovery root"):
                    driver.ensure_scratch(native / "arbitrary")
                scratch = native / (driver.SCRATCH_NAME_PREFIX + "synthetic")
                driver.ensure_scratch(scratch)
                self.assertEqual(scratch.stat().st_mode & 0o777, 0o700)

    def test_english_suppression_is_applied_before_candidate_generation(self) -> None:
        self.assertTrue(
            driver.is_english_review_suppressed({"english": {"review_suppressed": True}})
        )
        self.assertFalse(
            driver.is_english_review_suppressed({"english": {"review_suppressed": False}})
        )

    def test_reuse_requires_source_request_profile_parser_and_response_identity(self) -> None:
        item, old_item, request_bytes, configuration, deployment = reuse_fixture()
        observation = {
            "request_sha256": driver.sha256_bytes(request_bytes),
            "response_sha256": "raw-response-hash",
        }
        self.assertIsNone(
            driver.reuse_identity_reason(
                item,
                old_item,
                request_bytes,
                request_bytes,
                observation,
                "raw-response-hash",
                configuration,
                deployment,
            )
        )
        mutations = (
            ("candidate", lambda value: value["candidate"]["candidate"].update(text="changed")),
            ("request", lambda value: value.update(request_bytes=b"changed request")),
            (
                "profile",
                lambda value: value["deployment"].update(profile_sha256="changed-profile"),
            ),
            ("parser", lambda value: value["parser"]["parser"].update(status="changed")),
        )
        for name, mutate in mutations:
            with self.subTest(identity=name):
                changed_item = copy.deepcopy(item)
                changed_configuration = copy.deepcopy(configuration)
                changed_deployment = copy.deepcopy(deployment)
                changed_request = request_bytes
                values = {
                    "candidate": changed_item,
                    "request_bytes": changed_request,
                    "deployment": changed_deployment,
                    "parser": changed_configuration,
                }
                mutate(values)
                changed_request = values["request_bytes"]
                self.assertIsNotNone(
                    driver.reuse_identity_reason(
                        changed_item,
                        old_item,
                        changed_request,
                        request_bytes,
                        observation,
                        "raw-response-hash",
                        changed_configuration,
                        changed_deployment,
                    )
                )
        self.assertEqual(
            driver.reuse_identity_reason(
                item,
                old_item,
                request_bytes,
                request_bytes,
                observation,
                "raw-response-hash",
                configuration,
                {**deployment, "model": "other"},
            ),
            "deployment-identity-mismatch",
        )
        self.assertEqual(
            driver.reuse_identity_reason(
                {**item, "operation": driver.distance_one.INSERTION},
                old_item,
                request_bytes,
                request_bytes,
                observation,
                "raw-response-hash",
                configuration,
                deployment,
            ),
            "operation-is-not-substitution",
        )

    def test_keep_uncertain_failure_fallback_and_use_only_supplied_candidate(self) -> None:
        saved = saved_case()
        case = {
            "phase": "dassle-spelling",
            "index": 1,
            "id": "saved-case",
            "dataset": {"reference": "X B c"},
            "baseline": saved,
            "new": copy.deepcopy(saved),
        }
        item = candidate(0, target="a", replacement="X")
        item["sentence"] = saved["input"]
        for choice in ("KEEP_ORIGINAL", "UNCERTAIN", None):
            observation = {
                "decision": choice,
                "operational_failure": choice is None,
                "dispatch": "ATTEMPTED",
            }
            record = driver.validator_driver.make_case_result(
                "dassle-spelling",
                case,
                [item],
                {protocol.candidate_path_id(item): observation},
                "configuration",
            )
            self.assertEqual(record["validated_fallback"]["output"], saved["input"])
            self.assertEqual(record["validated_only"]["output"], saved["input"])
        use_record = driver.validator_driver.make_case_result(
            "dassle-spelling",
            case,
            [item],
            {
                protocol.candidate_path_id(item): {
                    "decision": "USE_CANDIDATE",
                    "operational_failure": False,
                    "dispatch": "ATTEMPTED",
                }
            },
            "configuration",
        )
        self.assertEqual(use_record["validated_fallback"]["output"], "X B c")
        self.assertEqual(use_record["validated_only"]["output"], "X B c")
        self.assertEqual(use_record["validated_fallback"]["edits"], [[0, 1, "X"]])

    def test_worker_partition_persistence_resume_and_uncertain_delivery(self) -> None:
        values = [candidate(index) for index in range(9)]
        with tempfile.TemporaryDirectory(dir=driver.NATIVE_RUNTIME_PARENT) as raw_root:
            root = Path(raw_root)
            transport = FakeTransport()
            first = driver.execute_fresh(
                root, values, "https://synthetic.invalid", "MISSING", transport=transport
            )
            self.assertEqual(sum(item["completed"] for item in first.values()), 9)
            self.assertEqual(sum(item["dispatched_http"] for item in first.values()), 9)
            self.assertEqual(transport.calls, 9)
            driver.execute_fresh(
                root,
                list(reversed(values)),
                "https://synthetic.invalid",
                "MISSING",
                transport=transport,
            )
            self.assertEqual(transport.calls, 9)
        with tempfile.TemporaryDirectory(dir=driver.NATIVE_RUNTIME_PARENT) as raw_root:
            root = Path(raw_root)
            item = candidate(0)
            directory = root / "requests" / protocol.candidate_path_id(item)
            directory.parent.mkdir(mode=0o700)
            os.chmod(directory.parent, 0o700)
            directory.mkdir(mode=0o700)
            os.chmod(directory, 0o700)
            body = protocol.request_body(
                item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
            )
            protocol.immutable_write(directory / "request.json", protocol.canonical_bytes(body))
            transport = FakeTransport()
            status = driver.execute_fresh(
                root, [item], "https://synthetic.invalid", "MISSING", transport=transport
            )
            self.assertEqual(transport.calls, 0)
            self.assertEqual(status[0]["failures"], 1)
            self.assertEqual(
                json.loads((directory / "observation.json").read_text())["failure"],
                "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE",
            )

    def test_default_execution_stops_before_network_and_protected_integrity_is_exact(self) -> None:
        with (
            tempfile.TemporaryDirectory(dir=driver.NATIVE_RUNTIME_PARENT) as raw_root,
            patch.dict(os.environ, {}, clear=True),
            self.assertRaisesRegex(driver.ExperimentError, "LIVE_CREDENTIAL_MISSING"),
        ):
            driver.execute_fresh(
                Path(raw_root), [candidate(0)], "https://synthetic.invalid", "MISSING"
            )
        source = "see https://example.test and a"
        start = source.rfind("a")
        exact = protocol.integrity(source, source[:start] + "X", [[start, start + 1, "X"]])
        self.assertEqual(exact["protected_differences"], 0)
        self.assertEqual(exact["outside_span_differences"], 0)
        altered = source[:4] + "https://changed.test" + source[24:]
        self.assertGreater(
            protocol.integrity(source, altered[:start] + "X", [[start, start + 1, "X"]])[
                "outside_span_differences"
            ],
            0,
        )
        with self.assertRaises(protocol.ValidatorError):
            protocol.integrity(source, source, [[4, 24, "changed"]])

    def test_operation_analysis_and_view_accounting_use_actual_candidate_identities(self) -> None:
        population = [
            candidate(0, operation=driver.distance_one.SUBSTITUTION),
            candidate(1, operation=driver.distance_one.INSERTION),
            candidate(2, operation=driver.distance_one.DELETION),
        ]
        targets = []
        for index, item in enumerate(population):
            targets.append(
                {
                    "candidate_id": protocol.candidate_path_id(item),
                    "attribution": {"status": "exact_reference" if index == 0 else "non_reference"},
                    "decision": "USE_CANDIDATE" if index != 2 else "KEEP_ORIGINAL",
                    "applied_fallback": index == 0,
                    "observation_source": "reuse" if index == 0 else "fresh",
                }
            )
        analysis = driver.candidate_analysis(
            {"dassle-spelling": [{"validator_targets": targets}]}, population
        )
        self.assertEqual(analysis["all_unique"][driver.distance_one.INSERTION]["unique"], 1)
        self.assertEqual(
            analysis["all_unique"][driver.distance_one.SUBSTITUTION]["final_tp_fp_fn"]["TP"], 1
        )
        self.assertEqual(
            analysis["all_unique"][driver.distance_one.DELETION]["rejected"]["non_reference"], 1
        )
        self.assertEqual(analysis["new_or_changed"][driver.distance_one.SUBSTITUTION]["unique"], 0)
        self.assertEqual(analysis["new_or_changed"][driver.distance_one.INSERTION]["unique"], 1)

        def accounting() -> dict[str, object]:
            return {
                "projected_ordinary": {"total": 10},
                "baseline": {"total": 10},
                "unrestricted_007h": {"total": 9},
                "net_projected": {"total": 13},
            }

        metrics = {
            "views": {
                "dassle-spelling": {
                    "all": {
                        "scheduled_candidates": 3,
                        "call_accounting": {"fallback": accounting()},
                    },
                    "initial_uv": {
                        "scheduled_candidates": 1,
                        "call_accounting": {"fallback": accounting()},
                    },
                    "without_initial_uv": {
                        "scheduled_candidates": 2,
                        "call_accounting": {"fallback": accounting()},
                    },
                }
            }
        }
        driver.update_view_call_accounting(
            metrics,
            population,
            {protocol.candidate_path_id(population[0])},
            {1},
        )
        all_accounting = metrics["views"]["dassle-spelling"]["all"]["call_accounting"]["fallback"]
        self.assertEqual(all_accounting["validator_calls_reused"], 1)
        self.assertEqual(all_accounting["validator_calls_added"], 2)
        self.assertEqual(all_accounting["net_projected"]["total"], 13)
        uv_accounting = metrics["views"]["dassle-spelling"]["initial_uv"]["call_accounting"][
            "fallback"
        ]
        self.assertEqual(uv_accounting["validator_calls_reused"], 1)
        self.assertEqual(uv_accounting["validator_calls_added"], 0)


if __name__ == "__main__":
    unittest.main()
