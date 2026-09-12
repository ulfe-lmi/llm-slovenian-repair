from __future__ import annotations

import ast
import copy
import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research.one_substitution import (
    entering_targets,
    mechanical_substitution,
    project_saved_case,
    qualifying_candidates,
)
from research.tools import run_one_substitution as driver

PRIVATE_TEST_ROOT = Path("/home/ubuntu/.local/share/llm-slovenian-repair")


class OneSubstitutionTests(unittest.TestCase):
    def test_saved_call_schema_accepts_stage_kinds_and_exact_flattening(self) -> None:
        first = {"kind": "reviewer", "marker": "first"}
        retry = {"kind": "expression-retry", "marker": "retry"}
        second_first = {"kind": "reviewer", "marker": "second"}
        record = {
            "decisions": [
                {"first": first, "retry": retry},
                {"first": second_first, "retry": None},
            ],
            "calls": [first, retry, second_first],
        }
        self.assertEqual(driver.call_counts(record), {"first": 2, "retry": 1, "total": 3})

    def test_saved_call_schema_rejects_invalid_stages_and_flattening(self) -> None:
        first = {"kind": "reviewer", "marker": "first"}
        retry = {"kind": "expression-retry", "marker": "retry"}
        second_first = {"kind": "reviewer", "marker": "second"}
        decisions = [
            {"first": first, "retry": retry},
            {"first": second_first, "retry": None},
        ]
        valid_calls = [first, retry, second_first]
        invalid_records = {
            "wrong first kind": {
                "decisions": [{"first": {**first, "kind": "expression-retry"}}],
                "calls": [{**first, "kind": "expression-retry"}],
            },
            "wrong retry kind": {
                "decisions": [{"first": first, "retry": {**retry, "kind": "reviewer"}}],
                "calls": [first, {**retry, "kind": "reviewer"}],
            },
            "non-object stage": {
                "decisions": [{"first": [], "retry": None}],
                "calls": [],
            },
            "missing call": {"decisions": decisions, "calls": valid_calls[:-1]},
            "orphan call": {"decisions": decisions, "calls": [*valid_calls, retry]},
            "order mismatch": {"decisions": decisions, "calls": [retry, first, second_first]},
            "content mismatch": {
                "decisions": decisions,
                "calls": [first, retry, {**second_first, "marker": "changed"}],
            },
            "duplicate call": {"decisions": [{"first": first}], "calls": [first, first]},
        }
        for label, record in invalid_records.items():
            with self.subTest(label=label), self.assertRaises(driver.ExperimentError):
                driver.call_counts(record)

    def test_pair_validator_accepts_blank_reference_only_with_exact_status(self) -> None:
        original = "vsi"
        detector = {"candidates": [], "english": []}
        input_sha = driver.hashlib.sha256(original.encode("utf-8")).hexdigest()

        def pair(reference: object, status: object = "SUPPLIED") -> tuple[dict, dict, dict]:
            dataset = {
                "id": "reference-schema",
                "index": 1,
                "input": original,
                "reference": reference,
                "reference_status": status,
            }
            snapshot = {
                "id": "reference-schema",
                "index": 1,
                "input_sha256": input_sha,
                "detector": detector,
            }
            saved = {
                "id": "reference-schema",
                "index": 1,
                "input": original,
                "input_sha256": input_sha,
                "method": "M2",
                "detector": detector,
                "output": original,
                "operational_failure": False,
                "calls": [],
                "decisions": [],
            }
            return dataset, snapshot, saved

        dataset, snapshot, saved = pair(None, "MISSING_BLANK_FIELD")
        driver.validate_pair(dataset, snapshot, saved, "dassle-spelling", 1)

        dataset, snapshot, saved = pair("vse")
        driver.validate_pair(dataset, snapshot, saved, "dassle-spelling", 1)

    def test_pair_validator_rejects_missing_or_wrong_blank_status(self) -> None:
        original = "vsi"
        detector = {"candidates": [], "english": []}
        input_sha = driver.hashlib.sha256(original.encode("utf-8")).hexdigest()

        def pair(
            status: object = "SUPPLIED", *, omit_status: bool = False
        ) -> tuple[dict, dict, dict]:
            dataset = {
                "id": "reference-schema",
                "index": 1,
                "input": original,
                "reference": None,
            }
            if not omit_status:
                dataset["reference_status"] = status
            snapshot = {
                "id": "reference-schema",
                "index": 1,
                "input_sha256": input_sha,
                "detector": detector,
            }
            saved = {
                "id": "reference-schema",
                "index": 1,
                "input": original,
                "input_sha256": input_sha,
                "method": "M2",
                "detector": detector,
                "output": original,
                "operational_failure": False,
                "calls": [],
                "decisions": [],
            }
            return dataset, snapshot, saved

        for label, arguments in (
            ("missing", {"omit_status": True}),
            ("wrong", {"status": "SUPPLIED"}),
        ):
            with self.subTest(label=label), self.assertRaises(driver.ExperimentError):
                driver.validate_pair(
                    *pair(**arguments), "dassle-spelling", 1
                )

    def test_pair_validator_rejects_every_other_non_string_reference(self) -> None:
        original = "vsi"
        detector = {"candidates": [], "english": []}
        input_sha = driver.hashlib.sha256(original.encode("utf-8")).hexdigest()
        for reference in (True, 1, 1.5, ["vse"], {"value": "vse"}):
            dataset = {
                "id": "reference-schema",
                "index": 1,
                "input": original,
                "reference": reference,
                "reference_status": "MISSING_BLANK_FIELD",
            }
            snapshot = {
                "id": "reference-schema",
                "index": 1,
                "input_sha256": input_sha,
                "detector": detector,
            }
            saved = {
                "id": "reference-schema",
                "index": 1,
                "input": original,
                "input_sha256": input_sha,
                "method": "M2",
                "detector": detector,
                "output": original,
                "operational_failure": False,
                "calls": [],
                "decisions": [],
            }
            with self.subTest(reference_type=type(reference).__name__), self.assertRaises(
                driver.ExperimentError
            ):
                driver.validate_pair(dataset, snapshot, saved, "dassle-spelling", 1)

    def test_only_same_length_one_alphabetic_difference_qualifies(self) -> None:
        self.assertEqual(qualifying_candidates("vsi", ["vse"]), ["vse"])
        self.assertEqual(qualifying_candidates("vsi", ["vsi"]), [])
        self.assertEqual(qualifying_candidates("vsi", ["vso", "vse"]), ["vso", "vse"])

    def test_zero_two_difference_insertion_deletion_transposition_reject(self) -> None:
        self.assertEqual(qualifying_candidates("abc", ["abc"]), [])
        self.assertEqual(qualifying_candidates("abc", ["axd"]), [])
        self.assertEqual(qualifying_candidates("abc", ["abcd"]), [])
        self.assertEqual(qualifying_candidates("abc", ["ab"]), [])
        self.assertEqual(qualifying_candidates("abc", ["acb"]), [])

    def test_whitespace_hyphen_apostrophe_and_normalization_are_not_manufactured(self) -> None:
        self.assertEqual(qualifying_candidates("a b", ["a c"]), [])
        self.assertEqual(qualifying_candidates("a-b", ["aab"]), [])
        self.assertEqual(qualifying_candidates("a'b", ["aab"]), [])
        self.assertEqual(qualifying_candidates("z\u030caba", ["žaba"]), [])

    def test_unique_gate_restores_initial_case_and_requires_exact_unigram(self) -> None:
        candidate = {
            "start": 0,
            "end": 7,
            "text": "Vspešni",
            "evidence": {"unigram": {"state": "UNAVAILABLE"}},
        }
        result = mechanical_substitution("Vspešni so tukaj.", candidate, "uspešni", {"uspešni"})
        self.assertTrue(result["accepted"])
        self.assertEqual(result["edit"], [0, 7, "Uspešni"])
        rejected = mechanical_substitution("Vspešni so tukaj.", candidate, "neznani", {"uspešni"})
        self.assertFalse(rejected["accepted"])
        self.assertEqual(rejected["reason"], "replacement-unigram-uncertain")

    def test_english_suppression_precedes_mechanical_stage(self) -> None:
        detector = {
            "candidates": [
                {
                    "start": 0,
                    "end": 3,
                    "text": "vsi",
                    "evidence": {"unigram": {"state": "UNAVAILABLE"}},
                },
                {
                    "start": 4,
                    "end": 7,
                    "text": "abc",
                    "evidence": {"unigram": {"state": "UNAVAILABLE"}},
                },
            ],
            "english": [
                {"review_suppressed": True, "slovene_unigram": {"state": "UNAVAILABLE"}},
                {"review_suppressed": False, "slovene_unigram": {"state": "UNAVAILABLE"}},
            ],
        }
        admitted = entering_targets(detector)
        self.assertEqual([candidate["text"] for candidate, _ in admitted], ["abc"])

    def test_orchestration_skips_lookup_and_mechanics_for_english_suppression(self) -> None:
        original = "vsi so tukaj."
        detector = {
            "candidates": [
                {
                    "start": 0,
                    "end": 3,
                    "text": "vsi",
                    "evidence": {"unigram": {"state": "UNAVAILABLE"}},
                }
            ],
            "english": [{"review_suppressed": True, "slovene_unigram": {"state": "UNAVAILABLE"}}],
        }
        saved = {
            "id": "english",
            "index": 1,
            "input": original,
            "input_sha256": "input",
            "detector": detector,
            "method": "M2",
            "output": original,
            "operational_failure": False,
            "calls": [],
            "decisions": [],
        }
        pair = {
            "dataset": {"id": "english", "index": 1, "input": original, "reference": original},
            "saved": saved,
        }
        with (
            patch.object(
                driver,
                "qualifying_candidates",
                side_effect=AssertionError("lookup must be skipped"),
            ) as lookup,
            patch.object(
                driver,
                "mechanical_substitution",
                side_effect=AssertionError("mechanics must be skipped"),
            ) as mechanics,
        ):
            record = driver.calculate_case("dassle-spelling", pair, set(), {}, "cfg")
        self.assertEqual(record["new"]["output"], original)
        self.assertEqual(record["mechanical"]["lookup_comparisons"], 0)
        lookup.assert_not_called()
        mechanics.assert_not_called()

    def test_orchestration_c_gt_one_uses_saved_fallback_without_selecting_first(self) -> None:
        original = "abc"
        detector = {
            "candidates": [
                {
                    "start": 0,
                    "end": 3,
                    "text": "abc",
                    "evidence": {"unigram": {"state": "UNAVAILABLE"}},
                }
            ],
            "english": [{"review_suppressed": False, "slovene_unigram": {"state": "UNAVAILABLE"}}],
        }
        candidate = detector["candidates"][0]
        saved = {
            "id": "ambiguous",
            "index": 1,
            "input": original,
            "input_sha256": "input",
            "detector": detector,
            "method": "M2",
            "output": "xyz",
            "operational_failure": False,
            "calls": [],
            "decisions": [
                {
                    "candidate": candidate,
                    "first": None,
                    "retry": None,
                    "final_case": {"adjusted_replacement": "xyz"},
                    "final_gate": {"accepted": True},
                }
            ],
        }
        pair = {
            "dataset": {"id": "ambiguous", "index": 1, "input": original, "reference": "xyz"},
            "saved": saved,
        }
        record = driver.calculate_case(
            "dassle-spelling", pair, {"abd", "abe"}, {3: ["abd", "abe"]}, "cfg"
        )
        target = record["mechanical"]["targets"][0]
        self.assertEqual(target["cardinality"], "C>1")
        self.assertEqual(target["candidate_forms"], ["abd", "abe"])
        self.assertFalse(target["accepted"])
        self.assertIsNone(target["gate"])
        self.assertEqual(record["new"]["output"], saved["output"])
        self.assertEqual(record["new"]["edits"], [[0, 3, "xyz"]])
        self.assertEqual(record["new"]["calls"], [])

    def test_projected_mechanical_target_skips_saved_calls(self) -> None:
        original = "Vspešni so tukaj."
        saved = {
            "input": original,
            "output": original,
            "operational_failure": False,
            "calls": [
                {"kind": "reviewer", "operational_failure": False},
                {"kind": "reviewer", "operational_failure": False},
            ],
            "decisions": [
                {
                    "candidate": {"start": 0, "end": 7, "text": "Vspešni"},
                    "first": {"kind": "reviewer", "operational_failure": False},
                    "retry": {"kind": "reviewer", "operational_failure": False},
                    "final_case": {"adjusted_replacement": "Uspešni"},
                    "final_gate": {"accepted": False},
                }
            ],
        }
        result = project_saved_case(original, saved, [[0, 7, "Uspešni"]])
        self.assertEqual(result["output"], "Uspešni so tukaj.")
        self.assertEqual(result["avoided_first_calls"], 1)
        self.assertEqual(result["avoided_retry_calls"], 1)
        self.assertEqual(result["calls"], [])

    def test_zero_and_ambiguous_candidates_use_exact_saved_fallback(self) -> None:
        original = "Vspešni so tukaj."
        saved = {
            "input": original,
            "output": "Uspešni so tukaj.",
            "operational_failure": False,
            "calls": [],
            "decisions": [
                {
                    "candidate": {"start": 0, "end": 7, "text": "Vspešni"},
                    "first": None,
                    "retry": None,
                    "final_case": {"adjusted_replacement": "Uspešni"},
                    "final_gate": {"accepted": True},
                }
            ],
        }
        self.assertEqual(project_saved_case(original, saved, [])["output"], saved["output"])
        self.assertEqual(qualifying_candidates("vsi", ["vso", "vse"]), ["vso", "vse"])
        self.assertEqual(project_saved_case(original, saved, [])["edits"], [[0, 7, "Uspešni"]])

    def test_mechanical_gate_failure_keeps_frozen_fallback(self) -> None:
        candidate = {
            "start": 0,
            "end": 7,
            "text": "Vspešni",
            "evidence": {"unigram": {"state": "UNAVAILABLE"}},
        }
        candidate["start"], candidate["end"], candidate["text"] = 8, 14, "`code`"
        rejected = mechanical_substitution("Vspešni `code`", candidate, "Uspešni", {"uspešni"})
        self.assertFalse(rejected["accepted"])
        self.assertEqual(rejected["reason"], "protected-span")

    def test_source_verification_is_read_only_and_staged_hardening_is_separate(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".one-sub-source-", dir=Path.cwd()) as raw:
            root = Path(raw)
            source = root / "source.json"
            staged = root / "staged.json"
            source.write_bytes(b"source")
            staged.write_bytes(b"source")
            os.chmod(source, 0o755)
            os.chmod(staged, 0o644)
            before = source.stat()
            driver.require_private_file(
                source, expected_size=6, expected_sha=driver.sha256_file(source)
            )
            after = source.stat()
            self.assertEqual(
                (before.st_mode, before.st_ino, before.st_mtime_ns, before.st_size),
                (after.st_mode, after.st_ino, after.st_mtime_ns, after.st_size),
            )
            with patch.object(driver.os, "chmod") as chmod:
                driver.require_private_file(
                    staged, expected_size=6, expected_sha=driver.sha256_file(staged), harden=True
                )
            chmod.assert_called_once_with(staged, 0o600)
            self.assertEqual(staged.read_bytes(), source.read_bytes())

    def test_uv_mapping_namespaces_and_identity_negatives(
        self,
    ) -> None:
        spelling = [{"dataset": {"index": index, "id": str(index)}} for index in range(1, 76)]
        cases = [{"index": 978 + offset, "id": str(offset + 1)} for offset in range(75)]
        positions, mapping = driver.map_uv_cases(list(range(1, 76)), cases, spelling)
        self.assertEqual(positions, set(range(1, 76)))
        self.assertEqual(mapping[0], {"id": "1", "full_dassle_index": 978, "spelling_position": 1})
        self.assertEqual(mapping[-1]["full_dassle_index"], 1052)
        for bad_cases in (
            cases[1:] + [{"index": 1053, "id": "76"}],
            [*cases[:2], cases[1], *cases[3:]],
            [{**cases[0], "id": "wrong"}, *cases[1:]],
        ):
            with self.assertRaises(driver.ExperimentError):
                driver.map_uv_cases(list(range(1, 76)), bad_cases, spelling)

    def test_shifted_reference_attribution_uses_token_edit_keys(self) -> None:
        source = "aa middle bad"
        reference = "long middle good"
        edit = [10, 13, "good"]
        result = driver.attribute_mechanical_edit(source, reference, edit)
        self.assertEqual(result["status"], "exact_reference")
        self.assertNotEqual(reference[edit[0] : edit[1]], edit[2])

    def test_ambiguous_and_multi_edit_attribution_are_not_guessed(self) -> None:
        self.assertEqual(
            driver.attribute_mechanical_edit("a b c", "x b y", [0, 5, "x b y"])["status"],
            "unresolved",
        )
        self.assertEqual(
            driver.attribute_mechanical_edit("bad", "good", [0, 3, "bet"])["status"],
            "non_reference",
        )

    def test_deterministic_bucket_order_is_complete_and_cannot_select_a_tie(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".one-sub-index-", dir=Path.cwd()) as raw:
            index = Path(raw) / "index.sqlite"
            connection = sqlite3.connect(index)
            connection.execute(
                "CREATE TABLE unigram(word TEXT PRIMARY KEY, count INTEGER NOT NULL)"
            )
            connection.executemany(
                "INSERT INTO unigram VALUES (?, ?)", [("vse", 1), ("vso", 2), ("vsi", 3)]
            )
            connection.commit()
            connection.close()
            expected_inputs = dict(driver.EXPECTED_INPUTS)
            with (
                patch.object(
                    driver,
                    "EXPECTED_INPUTS",
                    {
                        **expected_inputs,
                        "index.sqlite": (index.stat().st_size, driver.sha256_file(index)),
                    },
                ),
                patch.object(driver, "EXPECTED_INDEX_ROWS", 3),
            ):
                vocabulary, buckets, _, rows = driver.load_vocabulary(index)
            self.assertEqual(rows, 3)
            self.assertEqual(buckets[3], ["vse", "vsi", "vso"])
            self.assertEqual(set(qualifying_candidates("vsi", buckets[3])), {"vse", "vso"})

    def test_resume_accepts_one_matching_record_and_refuses_identity_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".one-sub-resume-", dir=Path.cwd()) as raw:
            path = Path(raw) / "case.json"
            record = {"configuration_sha256": "cfg", "phase": "phase", "index": 1}
            path.write_text(json.dumps(record), encoding="utf-8")
            pair = {"dataset": {"index": 1}, "saved": {}}
            self.assertEqual(
                driver.load_or_calculate_case(path, "phase", pair, set(), {}, "cfg"), record
            )
            with self.assertRaises(driver.ExperimentError):
                driver.load_or_calculate_case(path, "other", pair, set(), {}, "cfg")

    def test_network_model_entry_points_are_absent_from_the_offline_driver(self) -> None:
        tree = ast.parse(Path(driver.__file__).read_text(encoding="utf-8"))
        imported = {
            alias.name.split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported.update(
            node.module.split(".", 1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.assertTrue(imported.isdisjoint({"socket", "httpx", "requests", "urllib", "openai"}))
        self.assertFalse(
            any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"call", "post", "request"}
                for node in ast.walk(tree)
            )
        )

    def test_public_projection_handles_integer_count_and_refuses_malformed_identity(self) -> None:
        identity = {"size": 1, "sha256": "0" * 64}
        configuration = {
            "implementation_head": "head",
            "source_identity": {
                "dataset_rows": dict(driver.PHASES),
                "paired_rows": driver.FROZEN_CASE_COUNT,
                "m2_record_count": driver.FROZEN_CASE_COUNT,
                "staged_file_identities": {
                    "dataset.jsonl": identity,
                    "m2_record_count": driver.FROZEN_CASE_COUNT,
                },
                "uv_audit_rows": driver.UV_ROWS,
            },
            "baseline_identity": {"validated": True},
            "algorithm": {},
            "unicode": {},
            "call_policy": {},
        }
        public_config, _ = driver.public_projection(configuration, {}, "results", "manifest")
        self.assertEqual(
            public_config["source_identity"],
            {
                "datasets": dict(driver.PHASES),
                "paired_rows": driver.FROZEN_CASE_COUNT,
                "m2_record_count": driver.FROZEN_CASE_COUNT,
                "file_sha256": {"dataset.jsonl": "0" * 64},
                "uv_audit_rows": driver.UV_ROWS,
            },
        )
        malformed = [
            {"dataset.jsonl": "not-an-identity"},
            {"dataset.jsonl": {"sha256": "0" * 64}},
            {"dataset.jsonl": {"size": 1, "sha256": "0" * 64, "extra": True}},
            {"dataset.jsonl": {"size": 1, "sha256": "g" * 64}},
            {"m2_record_count": driver.FROZEN_CASE_COUNT - 1},
        ]
        for staged in malformed:
            with self.subTest(staged=staged), self.assertRaises(driver.ExperimentError):
                bad = copy.deepcopy(configuration)
                bad["source_identity"]["staged_file_identities"] = staged
                driver.public_projection(bad, {}, "results", "manifest")
        bad_count = copy.deepcopy(configuration)
        bad_count["source_identity"]["m2_record_count"] = driver.FROZEN_CASE_COUNT - 1
        with self.assertRaises(driver.ExperimentError):
            driver.public_projection(bad_count, {}, "results", "manifest")

    def test_publication_only_call_graph_excludes_aggregation_and_calculation(self) -> None:
        tree = ast.parse(Path(driver.__file__).read_text(encoding="utf-8"))
        functions = {
            node.name: node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        reachable: set[str] = set()
        pending = ["publication_only"]
        while pending:
            name = pending.pop()
            if name in reachable:
                continue
            reachable.add(name)
            node = functions.get(name)
            if node is None:
                continue
            pending.extend(
                call.func.id
                for call in ast.walk(node)
                if isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id in functions
            )
        for forbidden in (
            "run",
            "aggregate_frozen",
            "aggregate",
            "calculate_case",
            "load_or_calculate_case",
        ):
            self.assertNotIn(forbidden, reachable)

    def test_publication_supplement_derives_exact_introduced_edits_on_synthetic_data(self) -> None:
        def record(index: int, baseline_output: str, new_output: str) -> dict[str, object]:
            source = "a b"
            return {
                "index": index,
                "baseline": {"input": source, "output": baseline_output},
                "new": {"input": source, "output": new_output},
            }

        records = {
            "dassle-spelling": [record(1, "x b", "x y"), record(2, "a b", "a z")],
            "dassle-spelling-preservation": [record(1, "x b", "a b")],
        }
        supplement = driver.derive_publication_supplement(records, {1})
        views = supplement["views"]
        self.assertEqual(views["dassle-spelling/all"]["baseline"], {"introduced_edits": 1})
        self.assertEqual(views["dassle-spelling/all"]["new"], {"introduced_edits": 2})
        self.assertEqual(
            views["dassle-spelling/initial_uv"],
            {"rows": 1, "baseline": {"introduced_edits": 1}, "new": {"introduced_edits": 1}},
        )
        self.assertEqual(
            views["dassle-spelling/without_initial_uv"],
            {"rows": 1, "baseline": {"introduced_edits": 0}, "new": {"introduced_edits": 1}},
        )
        self.assertEqual(
            views["dassle-spelling-preservation/all"],
            {"rows": 1, "baseline": {"introduced_edits": 1}, "new": {"introduced_edits": 0}},
        )

    def test_publication_only_refuses_private_hash_or_link_drift(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix=".one-sub-private-links-", dir=PRIVATE_TEST_ROOT
        ) as raw:
            scratch = Path(raw)
            os.chmod(scratch, 0o700)
            report_path = scratch / "REPORT.md"
            report_path.write_bytes(b"report\n")
            os.chmod(report_path, 0o600)
            results = {
                "schema_version": 1,
                "experiment_id": driver.EXPERIMENT_ID,
                "status": "COMPLETE_OFFLINE_FROZEN_CASE_AGGREGATION_RECOVERY",
                "configuration_sha256": "cfg",
                "calculation_implementation_head": "calc",
                "aggregation_implementation_head": "agg",
                "incident_sha256": {},
                "metrics": {},
            }
            results_path = scratch / "RESULTS.json"
            results_path.write_bytes(driver.canonical_bytes(results))
            os.chmod(results_path, 0o600)
            manifest = {
                "schema_version": 1,
                "experiment_id": driver.EXPERIMENT_ID,
                "status": "COMPLETE_OFFLINE_FROZEN_CASE_AGGREGATION_RECOVERY",
                "input_manifest_sha256": "input",
                "configuration_sha256": "cfg",
                "calculation_implementation_head": "calc",
                "aggregation_implementation_head": "agg",
                "case_identity_manifest_sha256": "case",
                "case_count": driver.FROZEN_CASE_COUNT,
                "incident_sha256": {},
                "private_results_sha256": "wrong-results-link",
                "private_report_sha256": driver.sha256_file(report_path),
            }
            manifest_path = scratch / "MANIFEST.json"
            manifest_path.write_bytes(driver.canonical_bytes(manifest))
            os.chmod(manifest_path, 0o600)
            expected = {
                "results": driver.sha256_file(results_path),
                "report": driver.sha256_file(report_path),
                "manifest": driver.sha256_file(manifest_path),
            }
            with (
                patch.object(driver, "FROZEN_PRIVATE_AGGREGATE_SHA256", expected),
                patch.object(driver, "FROZEN_CALCULATION_HEAD", "calc"),
                patch.object(driver, "FROZEN_AGGREGATION_HEAD", "agg"),
                self.assertRaises(driver.ExperimentError),
            ):
                driver.verify_frozen_aggregate_outputs(scratch, "cfg", "input", "case", {})

    def test_publication_failure_preserves_status_bytes(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix=".one-sub-publication-", dir=PRIVATE_TEST_ROOT
        ) as raw:
            root = Path(raw)
            repo = root / "repo"
            scratch = root / "scratch"
            repo.mkdir()
            scratch.mkdir()
            os.chmod(scratch, 0o700)
            configuration = {
                "implementation_head": "calc",
                "run_id": driver.RUN_ID,
                "source_identity": {
                    "paired_rows": driver.FROZEN_CASE_COUNT,
                    "dataset_rows": dict(driver.PHASES),
                },
            }
            configuration_data = driver.canonical_bytes(configuration)
            (scratch / "CONFIGURATION.json").write_bytes(configuration_data)
            os.chmod(scratch / "CONFIGURATION.json", 0o600)
            status_data = driver.canonical_bytes(
                {
                    "configuration_sha256": driver.hashlib.sha256(configuration_data).hexdigest(),
                    "run_id": driver.RUN_ID,
                    "status": "EXPERIMENTAL_CALCULATION",
                }
            )
            (scratch / "RUN-STATUS.json").write_bytes(status_data)
            os.chmod(scratch / "RUN-STATUS.json", 0o600)
            (scratch / "INPUT-MANIFEST.json").write_bytes(b"input\n")
            os.chmod(scratch / "INPUT-MANIFEST.json", 0o600)
            args = driver.argparse.Namespace(
                repo_root=repo,
                scratch=scratch,
                expected_implementation_head="pub",
                calculation_implementation_head="calc",
            )
            before = (scratch / "RUN-STATUS.json").read_bytes()
            with (
                patch.object(
                    driver,
                    "FROZEN_CONFIGURATION_SHA256",
                    driver.hashlib.sha256(configuration_data).hexdigest(),
                ),
                patch.object(
                    driver,
                    "FROZEN_RUN_STATUS_SHA256",
                    driver.hashlib.sha256(status_data).hexdigest(),
                ),
                patch.object(
                    driver,
                    "FROZEN_INPUT_MANIFEST_SHA256",
                    driver.sha256_file(scratch / "INPUT-MANIFEST.json"),
                ),
                patch.object(driver, "FROZEN_CALCULATION_HEAD", "calc"),
                patch.object(driver, "verify_remote_implementation"),
                patch.object(
                    driver,
                    "verify_committed_implementation",
                    return_value={"implementation_head": "pub"},
                ),
                patch.object(driver, "snapshot_prior_public_artifacts", return_value={}),
                patch.object(
                    driver,
                    "verify_frozen_inputs",
                    return_value={"m2_record_count": driver.FROZEN_CASE_COUNT},
                ),
                patch.object(driver, "verify_frozen_incidents", return_value={}),
                patch.object(
                    driver,
                    "load_pairs",
                    return_value={"dassle-spelling": [], "dassle-spelling-preservation": []},
                ),
                patch.object(driver, "verify_uv_mapping", return_value=(set(), [])),
                patch.object(driver, "frozen_case_manifest", return_value=({}, "case", 0)),
                patch.object(
                    driver,
                    "verify_frozen_aggregate_outputs",
                    return_value={
                        "results": {"aggregation_implementation_head": "agg", "metrics": {}}
                    },
                ),
                patch.object(
                    driver,
                    "derive_publication_supplement",
                    side_effect=driver.ExperimentError("forced publication failure"),
                ),
                self.assertRaises(driver.ExperimentError),
            ):
                driver.publication_only(args)
            self.assertEqual((scratch / "RUN-STATUS.json").read_bytes(), before)

    def test_prior_public_snapshot_is_unchanged_by_reading(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".one-sub-archive-", dir=Path.cwd()) as raw:
            root = Path(raw)
            (root / "research/configs").mkdir(parents=True)
            (root / "research/configs/old.json").write_text("old", encoding="utf-8")
            before = driver.snapshot_prior_public_artifacts(root)
            after = driver.snapshot_prior_public_artifacts(root)
            self.assertEqual(before, after)

    def test_prior_public_snapshot_allows_only_exact_new_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".one-sub-archive-", dir=Path.cwd()) as raw:
            root = Path(raw)
            old = root / "research/configs/old.json"
            old.parent.mkdir(parents=True)
            old.write_text("old", encoding="utf-8")
            before = driver.snapshot_prior_public_artifacts(root)
            for relative in driver.PUBLIC_OUTPUT_PATHS:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("new", encoding="utf-8")
            driver.compare_prior_public_artifacts(
                before, driver.snapshot_prior_public_artifacts(root)
            )

            old.write_text("mutated", encoding="utf-8")
            with self.assertRaises(driver.ExperimentError):
                driver.compare_prior_public_artifacts(
                    before, driver.snapshot_prior_public_artifacts(root)
                )

    def test_prior_public_snapshot_rejects_deletion_and_unexpected_addition(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".one-sub-archive-", dir=Path.cwd()) as raw:
            root = Path(raw)
            old = root / "research/configs/old.json"
            old.parent.mkdir(parents=True)
            old.write_text("old", encoding="utf-8")
            before = driver.snapshot_prior_public_artifacts(root)
            old.unlink()
            with self.assertRaises(driver.ExperimentError):
                driver.compare_prior_public_artifacts(
                    before, driver.snapshot_prior_public_artifacts(root)
                )

        with tempfile.TemporaryDirectory(prefix=".one-sub-archive-", dir=Path.cwd()) as raw:
            root = Path(raw)
            old = root / "research/configs/old.json"
            old.parent.mkdir(parents=True)
            old.write_text("old", encoding="utf-8")
            before = driver.snapshot_prior_public_artifacts(root)
            extra = root / "research/results/unexpected.json"
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text("unexpected", encoding="utf-8")
            with self.assertRaises(driver.ExperimentError):
                driver.compare_prior_public_artifacts(
                    before, driver.snapshot_prior_public_artifacts(root)
                )

    def test_aggregation_only_call_graph_excludes_calculation_entry_points(self) -> None:
        tree = ast.parse(Path(driver.__file__).read_text(encoding="utf-8"))
        functions = {
            node.name: node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        reachable: set[str] = set()
        pending = ["aggregate_frozen"]
        while pending:
            name = pending.pop()
            if name in reachable:
                continue
            reachable.add(name)
            node = functions.get(name)
            if node is None:
                continue
            for call in ast.walk(node):
                if (
                    isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Name)
                    and call.func.id in functions
                ):
                    pending.append(call.func.id)
        self.assertNotIn("run", reachable)
        self.assertNotIn("calculate_case", reachable)
        self.assertNotIn("load_or_calculate_case", reachable)

    def test_frozen_case_manifest_rejects_case_set_or_identity_drift(self) -> None:
        dataset = {"id": "case-1", "index": 1}
        saved = {"id": "case-1", "index": 1, "saved": True}
        pair = {"dataset": dataset, "saved": saved}

        def make_fixture(
            root: Path, variant: str
        ) -> tuple[Path, dict[str, list[dict[str, object]]], str]:
            scratch = root / "scratch"
            cases = scratch / "cases" / "phase"
            cases.mkdir(parents=True)
            os.chmod(scratch, 0o700)
            os.chmod(scratch / "cases", 0o700)
            os.chmod(cases, 0o700)
            record = {
                "schema_version": 1,
                "configuration_sha256": "cfg",
                "phase": "phase",
                "index": 1,
                "id": "case-1",
                "dataset": dataset,
                "baseline": saved,
            }
            data = driver.canonical_bytes(record)
            case_path = cases / "000001.json"
            case_path.write_bytes(data)
            os.chmod(case_path, 0o600)
            if variant == "missing":
                case_path.unlink()
            elif variant == "additional":
                extra = cases / "000002.json"
                extra.write_bytes(data)
                os.chmod(extra, 0o600)
            elif variant == "changed":
                changed = dict(record)
                changed["dataset"] = {"id": "changed", "index": 1}
                case_path.write_bytes(driver.canonical_bytes(changed))
            elif variant == "wrong-config":
                wrong = dict(record)
                wrong["configuration_sha256"] = "wrong"
                case_path.write_bytes(driver.canonical_bytes(wrong))
            digest = driver.hashlib.sha256()
            for path in sorted(scratch.glob("cases/phase/*.json")):
                contents = path.read_bytes()
                digest.update(
                    str(path.relative_to(scratch)).encode("utf-8")
                    + b"\0"
                    + str(len(contents)).encode("ascii")
                    + b"\0"
                    + driver.hashlib.sha256(contents).hexdigest().encode("ascii")
                    + b"\n"
                )
            pairs = {"phase": [pair]}
            return scratch, pairs, digest.hexdigest()

        with tempfile.TemporaryDirectory(
            prefix=".one-sub-case-manifest-", dir=PRIVATE_TEST_ROOT
        ) as raw:
            root = Path(raw)
            for variant in ("missing", "additional", "changed", "wrong-config"):
                with self.subTest(variant=variant):
                    scratch, pairs, digest = make_fixture(root / variant, variant)
                    with (
                        patch.object(driver, "PHASES", {"phase": 1}),
                        patch.object(driver, "FROZEN_CASE_COUNT", 1),
                        patch.object(driver, "FROZEN_CASE_BYTES", 10_000),
                        patch.object(driver, "FROZEN_CASE_IDENTITY_MANIFEST_SHA256", digest),
                        self.assertRaises(driver.ExperimentError),
                    ):
                        driver.frozen_case_manifest(scratch, pairs, "cfg")

    def test_frozen_case_manifest_uses_component_order_for_phase_directories(self) -> None:
        phases = {"a": 1, "a-b": 1}
        pairs: dict[str, list[dict[str, object]]] = {}
        paths: list[Path] = []

        with tempfile.TemporaryDirectory(
            prefix=".one-sub-component-order-", dir=PRIVATE_TEST_ROOT
        ) as raw:
            scratch = Path(raw) / "scratch"
            cases_root = scratch / "cases"
            cases_root.mkdir(parents=True)
            os.chmod(scratch, 0o700)
            os.chmod(cases_root, 0o700)
            for phase in phases:
                phase_dir = cases_root / phase
                phase_dir.mkdir()
                os.chmod(phase_dir, 0o700)
                dataset = {"id": f"{phase}-case", "index": 1}
                saved = {"id": f"{phase}-case", "index": 1, "saved": True}
                pair = {"dataset": dataset, "saved": saved}
                pairs[phase] = [pair]
                record = {
                    "schema_version": 1,
                    "configuration_sha256": "cfg",
                    "phase": phase,
                    "index": 1,
                    "id": dataset["id"],
                    "dataset": dataset,
                    "baseline": saved,
                }
                path = phase_dir / "000001.json"
                path.write_bytes(driver.canonical_bytes(record))
                os.chmod(path, 0o600)
                paths.append(path)

            component_order = sorted(paths)
            relative_string_order = sorted(
                paths, key=lambda path: str(path.relative_to(scratch))
            )
            self.assertNotEqual(component_order, relative_string_order)

            expected = driver.hashlib.sha256()
            for path in component_order:
                contents = path.read_bytes()
                expected.update(
                    str(path.relative_to(scratch)).encode("utf-8")
                    + b"\0"
                    + str(len(contents)).encode("ascii")
                    + b"\0"
                    + driver.hashlib.sha256(contents).hexdigest().encode("ascii")
                    + b"\n"
                )

            with (
                patch.object(driver, "PHASES", phases),
                patch.object(driver, "FROZEN_CASE_COUNT", 2),
                patch.object(
                    driver, "FROZEN_CASE_BYTES", sum(path.stat().st_size for path in paths)
                ),
                patch.object(
                    driver,
                    "FROZEN_CASE_IDENTITY_MANIFEST_SHA256",
                    expected.hexdigest(),
                ),
            ):
                _, observed, total_bytes = driver.frozen_case_manifest(scratch, pairs, "cfg")

            self.assertEqual(total_bytes, sum(path.stat().st_size for path in paths))
            self.assertEqual(observed, expected.hexdigest())

    def test_aggregation_exception_preserves_status_and_creates_no_outputs(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix=".one-sub-aggregation-", dir=PRIVATE_TEST_ROOT
        ) as raw:
            root = Path(raw)
            repo = root / "repo"
            scratch = root / "scratch"
            scratch.mkdir()
            os.chmod(scratch, 0o700)
            (repo / "research").mkdir(parents=True)
            configuration = {
                "implementation_head": "calc",
                "run_id": driver.RUN_ID,
                "source_identity": {
                    "paired_rows": 0,
                    "dataset_rows": {"dassle-spelling": 0, "dassle-spelling-preservation": 0},
                },
                "baseline_identity": {"summary": {}},
            }
            configuration_data = driver.canonical_bytes(configuration)
            configuration_path = scratch / "CONFIGURATION.json"
            configuration_path.write_bytes(configuration_data)
            os.chmod(configuration_path, 0o600)
            configuration_sha = driver.hashlib.sha256(configuration_data).hexdigest()
            status_data = driver.canonical_bytes(
                {
                    "configuration_sha256": configuration_sha,
                    "run_id": driver.RUN_ID,
                    "status": "EXPERIMENTAL_CALCULATION",
                }
            )
            status_path = scratch / "RUN-STATUS.json"
            status_path.write_bytes(status_data)
            os.chmod(status_path, 0o600)
            before_status = status_path.read_bytes()
            args = driver.argparse.Namespace(
                repo_root=repo,
                scratch=scratch,
                expected_implementation_head="agg",
                calculation_implementation_head="calc",
            )
            with (
                patch.object(
                    driver,
                    "PHASES",
                    {"dassle-spelling": 0, "dassle-spelling-preservation": 0},
                ),
                patch.object(driver, "FROZEN_CASE_COUNT", 0),
                patch.object(driver, "FROZEN_CALCULATION_HEAD", "calc"),
                patch.object(driver, "FROZEN_CONFIGURATION_SHA256", configuration_sha),
                patch.object(
                    driver,
                    "FROZEN_RUN_STATUS_SHA256",
                    driver.hashlib.sha256(status_data).hexdigest(),
                ),
                patch.object(
                    driver,
                    "verify_committed_implementation",
                    return_value={"implementation_head": "agg"},
                ),
                patch.object(driver, "verify_frozen_inputs", return_value={}),
                patch.object(driver, "verify_frozen_incidents", return_value={}),
                patch.object(
                    driver,
                    "load_pairs",
                    return_value={"dassle-spelling": [], "dassle-spelling-preservation": []},
                ),
                patch.object(driver, "verify_uv_mapping", return_value=(set(), [])),
                patch.object(
                    driver,
                    "frozen_case_manifest",
                    return_value=(
                        {"dassle-spelling": [], "dassle-spelling-preservation": []},
                        "case",
                        0,
                    ),
                ),
                patch.object(
                    driver, "load_vocabulary", return_value=(set(), {}, 0.0, 0)
                ),
                patch.object(
                    driver,
                    "aggregate",
                    side_effect=driver.ExperimentError("forced aggregate failure"),
                ),
                self.assertRaises(driver.ExperimentError),
            ):
                driver.aggregate_frozen(args)
            self.assertEqual(status_path.read_bytes(), before_status)
            for name in ("RESULTS.json", "REPORT.md", "MANIFEST.json"):
                self.assertFalse((scratch / name).exists(), name)
            for relative in driver.PUBLIC_OUTPUT_PATHS:
                self.assertFalse((repo / relative).exists(), relative)

    def test_aggregation_identity_retains_distinct_calculation_and_aggregation_heads(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix=".one-sub-aggregation-heads-", dir=PRIVATE_TEST_ROOT
        ) as raw:
            root = Path(raw)
            repo = root / "repo"
            scratch = root / "scratch"
            scratch.mkdir()
            os.chmod(scratch, 0o700)
            (scratch / "INPUT-MANIFEST.json").write_bytes(b"manifest\n")
            os.chmod(scratch / "INPUT-MANIFEST.json", 0o600)
            (repo / "research").mkdir(parents=True)
            for relative in ("research/configs", "research/results", "research/reports"):
                (repo / relative).mkdir(parents=True)
            configuration = {
                "implementation_head": "calc",
                "run_id": driver.RUN_ID,
                "source_identity": {
                    "paired_rows": 0,
                    "dataset_rows": {"dassle-spelling": 0, "dassle-spelling-preservation": 0},
                },
                "baseline_identity": {"summary": {}},
            }
            configuration_data = driver.canonical_bytes(configuration)
            (scratch / "CONFIGURATION.json").write_bytes(configuration_data)
            os.chmod(scratch / "CONFIGURATION.json", 0o600)
            configuration_sha = driver.hashlib.sha256(configuration_data).hexdigest()
            status_data = driver.canonical_bytes(
                {
                    "configuration_sha256": configuration_sha,
                    "run_id": driver.RUN_ID,
                    "status": "EXPERIMENTAL_CALCULATION",
                }
            )
            (scratch / "RUN-STATUS.json").write_bytes(status_data)
            os.chmod(scratch / "RUN-STATUS.json", 0o600)
            args = driver.argparse.Namespace(
                repo_root=repo,
                scratch=scratch,
                expected_implementation_head="agg",
                calculation_implementation_head="calc",
            )
            with (
                patch.object(
                    driver,
                    "PHASES",
                    {"dassle-spelling": 0, "dassle-spelling-preservation": 0},
                ),
                patch.object(driver, "FROZEN_CASE_COUNT", 0),
                patch.object(driver, "FROZEN_CALCULATION_HEAD", "calc"),
                patch.object(driver, "FROZEN_CONFIGURATION_SHA256", configuration_sha),
                patch.object(
                    driver,
                    "FROZEN_RUN_STATUS_SHA256",
                    driver.hashlib.sha256(status_data).hexdigest(),
                ),
                patch.object(
                    driver,
                    "verify_committed_implementation",
                    return_value={"implementation_head": "agg"},
                ),
                patch.object(driver, "verify_frozen_inputs", return_value={}),
                patch.object(
                    driver,
                    "verify_frozen_incidents",
                    return_value={"preaggregation_review": "review"},
                ),
                patch.object(
                    driver,
                    "load_pairs",
                    return_value={"dassle-spelling": [], "dassle-spelling-preservation": []},
                ),
                patch.object(driver, "verify_uv_mapping", return_value=(set(), [])),
                patch.object(
                    driver,
                    "frozen_case_manifest",
                    return_value=(
                        {"dassle-spelling": [], "dassle-spelling-preservation": []},
                        "case",
                        0,
                    ),
                ),
                patch.object(
                    driver, "load_vocabulary", return_value=(set(), {}, 0.0, 0)
                ),
                patch.object(driver, "aggregate", return_value={"runtime": {}}),
                patch.object(driver, "public_projection", return_value=({}, {"metrics": {}})),
                patch.object(driver, "render_public_report", return_value="report\n"),
            ):
                result = driver.aggregate_frozen(args)
            self.assertEqual(result["calculation_implementation_head"], "calc")
            self.assertEqual(result["aggregation_implementation_head"], "agg")
            final_status = json.loads((scratch / "RUN-STATUS.json").read_text(encoding="utf-8"))
            self.assertEqual(final_status["calculation_implementation_head"], "calc")
            self.assertEqual(final_status["aggregation_implementation_head"], "agg")

    def test_unresolved_saved_failure_rolls_back_mechanical_edit(self) -> None:
        original = "Vspešni so tukaj."
        saved = {
            "input": original,
            "output": original,
            "operational_failure": True,
            "calls": [
                {"kind": "reviewer", "operational_failure": False},
                {"kind": "reviewer", "operational_failure": True},
            ],
            "decisions": [
                {
                    "candidate": {"start": 0, "end": 7, "text": "Vspešni"},
                    "first": {"kind": "reviewer", "operational_failure": False},
                    "retry": None,
                    "final_case": {"adjusted_replacement": "sta"},
                    "final_gate": {"accepted": False},
                },
                {
                    "candidate": {"start": 8, "end": 10, "text": "so"},
                    "first": {"kind": "reviewer", "operational_failure": True},
                    "retry": None,
                    "final_case": {"adjusted_replacement": "sta"},
                    "final_gate": {"accepted": False},
                },
            ],
        }
        result = project_saved_case(original, saved, [[0, 7, "Uspešni"]])
        self.assertEqual(result["output"], original)
        self.assertTrue(result["operational_failure"])
        self.assertEqual(result["edits"], [])
        self.assertEqual(result["avoided_total_calls"], 1)

    def test_aggregate_view_denominators_exclude_preservation_and_partition_spelling(self) -> None:
        def row(
            phase: str, index: int, status: str | None
        ) -> tuple[dict[str, object], dict[str, object]]:
            dataset = {"id": f"{phase}-{index}", "index": index, "input": "x", "reference": "x"}
            detector = {"english": []}
            saved = {
                "id": dataset["id"],
                "index": index,
                "input": "x",
                "detector": detector,
                "operational_failure": False,
                "calls": [],
                "decisions": [],
            }
            new = {"operational_failure": False, "calls": [], "decisions": [], "edits": []}
            target = []
            if status is not None:
                target.append(
                    {
                        "cardinality": "C=1",
                        "accepted": True,
                        "applied": True,
                        "attribution": {"status": status},
                    }
                )
                new["edits"] = [[0, 1, "y"]]
            record = {
                "dataset": dataset,
                "index": index,
                "baseline": saved,
                "new": new,
                "mechanical": {"targets": target, "lookup_seconds": 0.0, "lookup_comparisons": 1},
                "integrity": {"protected_differences": 0, "outside_span_differences": 0},
            }
            return {"dataset": dataset, "saved": saved}, record

        spelling = [
            row("spelling", 1, "exact_reference")[0],
            row("spelling", 2, "non_reference")[0],
            row("spelling", 3, None)[0],
        ]
        spelling_records = [
            row("spelling", 1, "exact_reference")[1],
            row("spelling", 2, "non_reference")[1],
            row("spelling", 3, None)[1],
        ]
        preservation, preservation_record = row("preservation", 1, "exact_reference")
        with (
            patch.object(driver, "row_metrics", return_value={}),
            patch.object(driver, "summarize", return_value={"gold_edits": 2}),
        ):
            summary = driver.view_summary([spelling[0]], [spelling_records[0]])
            metrics = driver.aggregate(
                {"dassle-spelling": spelling, "dassle-spelling-preservation": [preservation]},
                {
                    "dassle-spelling": spelling_records,
                    "dassle-spelling-preservation": [preservation_record],
                },
                {1},
                0.0,
                3,
            )
        self.assertEqual(summary["rows"], 1)
        self.assertNotIn("baseline", spelling[0])
        spelling_views = metrics["views"]["dassle-spelling"]
        spelling_all = spelling_views["all"]["mechanical"]
        spelling_uv = spelling_views["initial_uv"]["mechanical"]
        spelling_without_uv = spelling_views["without_initial_uv"]["mechanical"]
        for key in (
            "accepted_unique_targets",
            "applied_mechanical_edits",
            "exact_reference_edits",
            "nonreference_edits",
            "unresolved_attribution",
            "rolled_back_by_failure",
            "fallback_edits",
            "reference_defined_applied_mechanical_edits",
            "precision_denominator",
        ):
            self.assertEqual(
                spelling_all.get(key, 0),
                spelling_uv.get(key, 0) + spelling_without_uv.get(key, 0),
                key,
            )
        self.assertEqual(spelling_all["precision"], 0.5)
        self.assertEqual(
            metrics["views"]["dassle-spelling-preservation"]["all"]["mechanical"]["precision"], 1.0
        )


if __name__ == "__main__":
    unittest.main()
