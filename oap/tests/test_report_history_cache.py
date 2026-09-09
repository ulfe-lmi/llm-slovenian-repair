"""Focused real-history and cache-boundary tests for objective 006-k."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
import json
from pathlib import Path
from unittest.mock import patch
import hashlib

import acquisition_history
import source_cache
from oap_core import OAPError, check_report_history


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


class ReportHistoryGuard(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="oap-history-cache-")
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        run_git(self.repo, "init", "-b", "main")
        run_git(self.repo, "config", "user.name", "Synthetic history test")
        run_git(self.repo, "config", "user.email", "synthetic@example.invalid")
        (self.repo / "oap/reports").mkdir(parents=True)
        (self.repo / "implementation.txt").write_text("implementation\n")
        run_git(self.repo, "add", ".")
        run_git(self.repo, "commit", "-m", "implementation")
        self.implementation = run_git(self.repo, "rev-parse", "HEAD")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_report(self, name: str, implementation: str | None = None) -> Path:
        path = self.repo / "oap/reports" / name
        head = implementation or self.implementation
        path.write_text(
            "# synthetic\n\n```oap-report\n"
            f'{{"implementation_head":"{head}"}}\n'
            "```\n"
        )
        return path

    def commit(self, message: str) -> str:
        run_git(self.repo, "add", ".")
        run_git(self.repo, "commit", "-m", message)
        return run_git(self.repo, "rev-parse", "HEAD")

    def test_add_once_path_only_actual_parent_passes(self) -> None:
        self.write_report("000-a-synthetic.md")
        head = self.commit("publish report")
        result = check_report_history(self.repo, head)
        self.assertEqual(result["report_count"], 1)

    def test_modify_published_report_fails(self) -> None:
        path = self.write_report("000-a-synthetic.md")
        self.commit("publish report")
        path.write_text(path.read_text() + "changed\n")
        head = self.commit("modify report")
        with self.assertRaises(OAPError) as caught:
            check_report_history(self.repo, head)
        self.assertEqual(caught.exception.code, "REPORT_HISTORY_MUTATION")

    def test_implementation_head_change_after_publication_fails(self) -> None:
        path = self.write_report("000-a-synthetic.md")
        self.commit("publish report")
        path.write_text(path.read_text().replace(self.implementation, "0" * 40))
        head = self.commit("change implementation head")
        with self.assertRaises(OAPError) as caught:
            check_report_history(self.repo, head)
        self.assertEqual(caught.exception.code, "REPORT_HISTORY_MUTATION")

    def test_invalid_report_repair_at_same_path_fails(self) -> None:
        path = self.write_report("000-a-synthetic.md", implementation="0" * 40)
        self.commit("publish invalid report")
        path.write_text(path.read_text().replace("0" * 40, self.implementation))
        head = self.commit("repair report in place")
        with self.assertRaises(OAPError) as caught:
            check_report_history(self.repo, head)
        self.assertEqual(caught.exception.code, "REPORT_HISTORY_MUTATION")

    def test_manifest_added_exception_fails(self) -> None:
        self.write_report("000-a-synthetic.md")
        self.commit("publish report")
        (self.repo / "oap/REPORT-HISTORY-INCIDENTS.json").write_text(
            '{"schema_version":1,"scope":"oap/reports","incidents":[]}\n'
        )
        head = self.commit("add manifest exception")
        with self.assertRaises(OAPError) as caught:
            check_report_history(self.repo, head)
        self.assertEqual(caught.exception.code, "REPORT_HISTORY_MANIFEST_MISMATCH")

    def test_delete_recreate_fails(self) -> None:
        path = self.write_report("000-a-synthetic.md")
        self.commit("publish report")
        path.unlink()
        self.commit("delete report")
        self.write_report("000-a-synthetic.md")
        head = self.commit("recreate report")
        with self.assertRaises(OAPError) as caught:
            check_report_history(self.repo, head)
        self.assertEqual(caught.exception.code, "REPORT_HISTORY_MUTATION")

    def test_new_corrective_suffix_has_new_immutable_path(self) -> None:
        self.write_report("000-a-synthetic.md")
        self.commit("publish first report")
        (self.repo / "implementation.txt").write_text("corrective implementation\n")
        self.commit("corrective implementation")
        self.implementation = run_git(self.repo, "rev-parse", "HEAD")
        self.write_report("000-b-synthetic.md")
        head = self.commit("publish corrective suffix")
        self.assertEqual(check_report_history(self.repo, head)["report_count"], 2)

    def test_real_history_has_only_two_frozen_incidents_and_third_touch_fails(self) -> None:
        source = Path(__file__).resolve().parents[2]
        if not (source / ".git").exists():
            self.skipTest("the owned baseline mirror has no Git history")
        result = check_report_history(source, "HEAD")
        self.assertEqual(
            {item["path"] for item in result["known_incidents"]},
            {
                "oap/reports/006-a-unigram-lexicon-importer.md",
                "oap/reports/006-c-support-observed-terminal-tab-and-complete-smoke.md",
            },
        )
        with tempfile.TemporaryDirectory(prefix="oap-real-history-") as temporary:
            clone = Path(temporary) / "repo"
            subprocess.run(
                ["git", "clone", "--no-local", str(source), str(clone)],
                check=True,
                capture_output=True,
            )
            run_git(clone, "config", "user.name", "Synthetic history test")
            run_git(clone, "config", "user.email", "synthetic@example.invalid")
            report = clone / "oap/reports/006-a-unigram-lexicon-importer.md"
            report.write_text(report.read_text() + "third touch\n")
            run_git(clone, "add", str(report.relative_to(clone)))
            run_git(clone, "commit", "-m", "third touch")
            with self.assertRaises(OAPError) as caught:
                check_report_history(clone, "HEAD")
            self.assertEqual(caught.exception.code, "REPORT_HISTORY_INCIDENT_SEQUENCE")


class CachePlanner(unittest.TestCase):
    @staticmethod
    def _fixture(strategy: Path, data: bytes) -> tuple[Path, dict[str, object]]:
        root = strategy / "source-cache/concept-verification/gigafida-2.0-words"
        root.mkdir(parents=True)
        part = root / source_cache.PART_NAME
        part.write_bytes(data)
        expected: dict[str, object] = {
            "EXPECTED_SIZE": len(data),
            "EXPECTED_MD5": hashlib.md5(data, usedforsecurity=False).hexdigest(),
            "EXPECTED_SHA256": hashlib.sha256(data).hexdigest(),
            "EXPECTED_GENERATION": hashlib.sha256(data).hexdigest(),
        }
        expected["evidence"] = source_cache.verify_source_artifact.ArtifactVerification(
            source_id=source_cache.SOURCE_ID,
            byte_size=len(data),
            md5=expected["EXPECTED_MD5"],  # type: ignore[arg-type]
            sha256=expected["EXPECTED_SHA256"],  # type: ignore[arg-type]
            member_count=1,
            total_uncompressed_size=len(data),
        )
        return root, expected

    def _promote(self, strategy: Path, data: bytes = b"synthetic archive bytes") -> Path:
        root, values = self._fixture(strategy, data)
        with patch.multiple(
            source_cache,
            EXPECTED_SIZE=values["EXPECTED_SIZE"],
            EXPECTED_MD5=values["EXPECTED_MD5"],
            EXPECTED_SHA256=values["EXPECTED_SHA256"],
            EXPECTED_GENERATION=values["EXPECTED_GENERATION"],
        ), patch.object(
            source_cache.verify_source_artifact,
            "verify_artifact",
            return_value=values["evidence"],
        ):
            result = source_cache.promote(strategy)
            self.assertEqual(result["state"], source_cache.CACHE_STATE_VERIFIED)
        return root

    def test_missing_cache_has_zero_network_gets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-plan-") as temporary:
            strategy = Path(temporary) / "strategy"
            strategy.mkdir()
            result = source_cache.plan(strategy)
            self.assertEqual(result["state"], source_cache.CACHE_STATE_MISSING)
            self.assertEqual(result["network_get_count"], 0)

    def test_unexpected_cache_file_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-invalid-") as temporary:
            strategy = Path(temporary) / "strategy"
            root = strategy / "source-cache/concept-verification/gigafida-2.0-words"
            root.mkdir(parents=True)
            (root / "unexpected").write_bytes(b"fixture")
            result = source_cache.plan(strategy)
            self.assertEqual(result["state"], source_cache.CACHE_STATE_INVALID)

    def test_promotion_uses_one_atomic_rename_and_never_hardlinks(self) -> None:
        data = b"synthetic archive bytes"
        with tempfile.TemporaryDirectory(prefix="cache-promote-") as temporary:
            strategy = Path(temporary) / "strategy"
            root, values = self._fixture(strategy, data)
            part = root / source_cache.PART_NAME
            expected = {key: value for key, value in values.items() if key != "evidence"}
            with patch.multiple(source_cache, **expected), patch.object(
                source_cache.verify_source_artifact,
                "verify_artifact",
                return_value=values["evidence"],
            ), patch.object(source_cache.os, "link") as link, patch.object(
                source_cache.os, "replace", wraps=source_cache.os.replace
            ) as replace:
                result = source_cache.promote(strategy)
                self.assertEqual(result["state"], source_cache.CACHE_STATE_VERIFIED)
                self.assertEqual(
                    source_cache.inspect(strategy)["state"], source_cache.CACHE_STATE_VERIFIED
                )
                link.assert_not_called()
                replace.assert_called_once_with(part, root / source_cache.FINAL_NAME)
            self.assertTrue((root / source_cache.FINAL_NAME).is_file())
            self.assertFalse(part.exists())

    def test_rename_failure_cleans_only_fixed_artifacts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-rename-failure-") as temporary:
            strategy = Path(temporary) / "strategy"
            root, values = self._fixture(strategy, b"rename failure")
            expected = {key: value for key, value in values.items() if key != "evidence"}
            with patch.multiple(source_cache, **expected), patch.object(
                source_cache.verify_source_artifact,
                "verify_artifact",
                return_value=values["evidence"],
            ), patch.object(source_cache.os, "replace", side_effect=OSError("synthetic rename")):
                with self.assertRaises(source_cache.CacheError) as caught:
                    source_cache.promote(strategy)
            self.assertEqual(caught.exception.reason, "CACHE_PROMOTION_FAILED")
            self.assertEqual(list(root.iterdir()), [])

    def test_post_rename_verification_failure_cleans_final(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-post-verify-") as temporary:
            strategy = Path(temporary) / "strategy"
            root, values = self._fixture(strategy, b"post verify failure")
            expected = {key: value for key, value in values.items() if key != "evidence"}
            failure = source_cache.verify_source_artifact.ArtifactVerificationError("fixture")
            with patch.multiple(source_cache, **expected), patch.object(
                source_cache.verify_source_artifact,
                "verify_artifact",
                side_effect=[values["evidence"], failure],
            ):
                with self.assertRaises(source_cache.CacheError) as caught:
                    source_cache.promote(strategy)
            self.assertEqual(caught.exception.reason, "CACHE_VERIFIER_FAILED")
            self.assertEqual(list(root.iterdir()), [])

    def test_metadata_failure_cleans_final(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-metadata-failure-") as temporary:
            strategy = Path(temporary) / "strategy"
            root, values = self._fixture(strategy, b"metadata failure")
            expected = {key: value for key, value in values.items() if key != "evidence"}
            with patch.multiple(source_cache, **expected), patch.object(
                source_cache.verify_source_artifact,
                "verify_artifact",
                return_value=values["evidence"],
            ), patch.object(
                source_cache, "_write_exclusive", side_effect=source_cache.CacheError("fixture")
            ):
                with self.assertRaises(source_cache.CacheError):
                    source_cache.promote(strategy)
            self.assertEqual(list(root.iterdir()), [])

    def test_corrupt_archive_and_metadata_are_invalid(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-corrupt-") as temporary:
            strategy = Path(temporary) / "strategy"
            root = self._promote(strategy, b"corruptible")
            final = root / source_cache.FINAL_NAME
            final.chmod(0o600)
            final.write_bytes(b"corrupt archive")
            expected = {
                "EXPECTED_SIZE": 11,
                "EXPECTED_MD5": hashlib.md5(b"corruptible", usedforsecurity=False).hexdigest(),
                "EXPECTED_SHA256": hashlib.sha256(b"corruptible").hexdigest(),
                "EXPECTED_GENERATION": hashlib.sha256(b"corruptible").hexdigest(),
            }
            with patch.multiple(source_cache, **expected), patch.object(
                source_cache.verify_source_artifact,
                "verify_artifact",
                side_effect=AssertionError("digest must fail before verifier"),
            ):
                state = source_cache.inspect(strategy)
            self.assertEqual(state["state"], source_cache.CACHE_STATE_INVALID)
            self.assertEqual(state["reason"], "CACHE_DIGEST_MISMATCH")

            metadata = root / source_cache.METADATA_NAME
            with patch.multiple(source_cache, **expected), patch.object(
                source_cache.verify_source_artifact, "verify_artifact", return_value=None
            ):
                metadata.write_text(metadata.read_text().replace('"byte_size": 11', '"byte_size": 12'))
                self.assertEqual(source_cache.inspect(strategy)["state"], source_cache.CACHE_STATE_INVALID)

    def test_duplicate_metadata_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-duplicate-") as temporary:
            strategy = Path(temporary) / "strategy"
            root = self._promote(strategy)
            metadata = root / source_cache.METADATA_NAME
            metadata.write_text('{"schema_version":1,"schema_version":1}\n')
            state = source_cache.inspect(strategy)
            self.assertEqual(state["state"], source_cache.CACHE_STATE_INVALID)
            self.assertEqual(state["reason"], "CACHE_METADATA_DUPLICATE_KEY")

    def test_symlink_hardlink_and_nonregular_are_rejected(self) -> None:
        for name, setup, reason in (
            (
                "symlink",
                lambda root: (root / source_cache.FINAL_NAME).symlink_to("target"),
                "CACHE_SYMLINK",
            ),
            (
                "nonregular",
                lambda root: (root / source_cache.FINAL_NAME).mkdir(),
                "CACHE_WRONG_TYPE",
            ),
        ):
            with tempfile.TemporaryDirectory(prefix=f"cache-{name}-") as temporary:
                strategy = Path(temporary) / "strategy"
                root = strategy / "source-cache/concept-verification/gigafida-2.0-words"
                root.mkdir(parents=True)
                setup(root)
                state = source_cache.inspect(strategy)
                self.assertEqual(state["state"], source_cache.CACHE_STATE_INVALID)
                self.assertEqual(state["reason"], reason)
        with tempfile.TemporaryDirectory(prefix="cache-hardlink-") as temporary:
            strategy = Path(temporary) / "strategy"
            root = strategy / "source-cache/concept-verification/gigafida-2.0-words"
            root.mkdir(parents=True)
            (root / "other").write_bytes(b"hardlink")
            (root / source_cache.FINAL_NAME).hardlink_to(root / "other")
            state = source_cache.inspect(strategy)
            self.assertEqual(state["state"], source_cache.CACHE_STATE_INVALID)
            self.assertEqual(state["reason"], "CACHE_HARDLINK")

    def test_wrong_owner_wrong_root_overwrite_and_lifecycle_gates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-owner-") as temporary:
            strategy = Path(temporary) / "strategy"
            root = self._promote(strategy)
            with patch.object(source_cache, "_ubuntu_uid", return_value=-1):
                with self.assertRaises(source_cache.CacheError) as caught:
                    source_cache.inspect(strategy)
            self.assertEqual(caught.exception.reason, "CACHE_WRONG_OWNER")
            sibling = Path(temporary) / "wrong-root/source-cache/concept-verification/gigafida-2.0-words"
            sibling.mkdir(parents=True)
            (sibling / source_cache.FINAL_NAME).write_bytes(b"not discovered")
            expected = {
                "EXPECTED_SIZE": 23,
                "EXPECTED_MD5": hashlib.md5(b"synthetic archive bytes", usedforsecurity=False).hexdigest(),
                "EXPECTED_SHA256": hashlib.sha256(b"synthetic archive bytes").hexdigest(),
                "EXPECTED_GENERATION": hashlib.sha256(b"synthetic archive bytes").hexdigest(),
            }
            evidence = source_cache.verify_source_artifact.ArtifactVerification(
                source_id=source_cache.SOURCE_ID,
                byte_size=23,
                md5=expected["EXPECTED_MD5"],  # type: ignore[arg-type]
                sha256=expected["EXPECTED_SHA256"],  # type: ignore[arg-type]
                member_count=1,
                total_uncompressed_size=23,
            )
            with patch.multiple(source_cache, **expected), patch.object(
                source_cache.verify_source_artifact, "verify_artifact", return_value=evidence
            ):
                self.assertEqual(source_cache.plan(strategy)["state"], source_cache.CACHE_STATE_VERIFIED)
            with self.assertRaises(source_cache.CacheError) as caught:
                source_cache.cleanup(strategy, lifecycle="not-complete")
            self.assertEqual(caught.exception.reason, "CACHE_CLEANUP_GATE")
            source_cache.cleanup(strategy, lifecycle="abandoned")
            self.assertFalse(root.exists())

        with tempfile.TemporaryDirectory(prefix="cache-overwrite-") as temporary:
            strategy = Path(temporary) / "strategy"
            root, values = self._fixture(strategy, b"overwrite")
            (root / source_cache.FINAL_NAME).write_bytes(b"existing")
            expected = {key: value for key, value in values.items() if key != "evidence"}
            with patch.multiple(source_cache, **expected), patch.object(
                source_cache.verify_source_artifact,
                "verify_artifact",
                return_value=values["evidence"],
            ):
                with self.assertRaises(source_cache.CacheError) as caught:
                    source_cache.promote(strategy)
            self.assertEqual(caught.exception.reason, "CACHE_FINAL_EXISTS")


class AcquisitionHistory(unittest.TestCase):
    def test_current_generation_is_monotonic_and_prior_receipt_is_untouched(self) -> None:
        root = Path(__file__).resolve().parents[2]
        prior = (root / "resources/source-acquisitions/gigafida-2.0-words-006-k.json").read_bytes()
        result = acquisition_history.validate_acquisition_history(root, revision="HEAD")
        self.assertEqual(result["legacy_cumulative_get_count"], 12)
        self.assertEqual(result["current_cumulative_get_count"], 14)
        self.assertEqual(result["current_network_get_count"], 2)
        self.assertEqual(
            (root / "resources/source-acquisitions/gigafida-2.0-words-006-k.json").read_bytes(),
            prior,
        )

    def test_accidental_refetch_after_verified_generation_is_rejected(self) -> None:
        root = Path(__file__).resolve().parents[2]
        receipt = json.loads(
            (root / "resources/source-acquisitions/gigafida-2.0-words-006-l.json").read_text()
        )
        receipt.update(
            {
                "receipt_id": "gigafida-2.0-words-006-m",
                "status": "ESTABLISHED_VERIFIED",
                "network_get_count": 1,
                "cumulative_observed_objective_get_count": 15,
                "prior_validation": "VERIFIED_REUSABLE_REUSE",
                "prior_receipt_id": "gigafida-2.0-words-006-l",
                "prior_cache_state": "VERIFIED_REUSABLE",
                "invalidation_deletion_reason": None,
            }
        )
        with self.assertRaises(acquisition_history.AcquisitionHistoryError) as caught:
            acquisition_history._active_cache_receipt(
                receipt,
                "m",
                14,
                previous_receipt="gigafida-2.0-words-006-l",
                previous_state="VERIFIED_REUSABLE",
                previous_generation=acquisition_history.ARCHIVE_SHA256,
            )
        self.assertEqual(caught.exception.reason, "ACQUISITION_CACHE_STATE")


if __name__ == "__main__":
    unittest.main()
