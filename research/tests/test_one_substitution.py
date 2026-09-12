from __future__ import annotations

import ast
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


class OneSubstitutionTests(unittest.TestCase):
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
            return {"dataset": dataset, "baseline": saved}, record

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
