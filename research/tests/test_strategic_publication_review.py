"""Independent acceptance regressions for OAP007-c requirements 11 and 16.

These exercise the publication CLI, not a substitute implementation. Every
text/key is synthetic; no experimental dataset or real credential is embedded.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class StrategicPublicationReview(unittest.TestCase):
    def setUp(self) -> None:
        parent = os.environ.get("TMPDIR")
        if not parent:
            self.fail("Set TMPDIR to an owned persistent scratch directory")
        Path(parent).mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="publication-review-", dir=parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.public = self.root / "public"
        self.public.mkdir()

    def cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", "-m", "research.tools.publication_guard", *args],
            cwd=Path(__file__).resolve().parents[2],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

    def payload(self, value: object) -> Path:
        path = self.root / "export-source.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_numeric_export_is_allowed(self) -> None:
        source = self.payload({"cases": 7, "tp": 2, "fp": 1, "fn": 5})
        result = self.cli("--root", str(self.public), "--export-json", "metrics.json", str(source))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.public / "metrics.json").read_text()), json.loads(source.read_text()))

    def test_raw_key_field_is_rejected_before_write(self) -> None:
        source = self.payload({"api_key": "sk-" + "C" * 48})
        result = self.cli("--root", str(self.public), "--export-json", "config.json", str(source))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.public / "config.json").exists())

    def test_forbidden_dataset_field_is_rejected_before_write(self) -> None:
        source = self.payload({"dataset_row": "SYNTHETIC_CANARY_NOT_REAL_DATA"})
        result = self.cli("--root", str(self.public), "--export-json", "record.json", str(source))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.public / "record.json").exists())

    def test_internal_symlink_component_is_rejected(self) -> None:
        (self.public / "real").mkdir()
        (self.public / "alias").symlink_to("real", target_is_directory=True)
        source = self.payload({"cases": 3})
        result = self.cli("--root", str(self.public), "--export-json", "alias/metrics.json", str(source))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.public / "real" / "metrics.json").exists())

    def test_existing_file_is_not_overwritten(self) -> None:
        original = b'{"cases": 1}\n'
        destination = self.public / "metrics.json"
        destination.write_bytes(original)
        source = self.payload({"cases": 2})
        result = self.cli("--root", str(self.public), "--export-json", "metrics.json", str(source))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(destination.read_bytes(), original)

    def short_overlap(self, suffix: str) -> None:
        private = self.root / "prepared"
        private.mkdir()
        canary = "synthetic cobalt lantern sample sentence"
        source = private / ("source" + suffix)
        if suffix == ".jsonl":
            source.write_text(json.dumps({"id": "synthetic", "input": canary, "reference": canary}) + "\n")
        else:
            source.write_text(canary)
        text = ("Ordinary explanatory context. " * 20) + canary + (" More explanatory context. " * 20)
        (self.public / "README.md").write_text(text)
        result = self.cli("--root", str(self.public), "--private-root", str(private))
        self.assertNotEqual(result.returncode, 0, "Short private text embedded in a longer public document was missed")

    def test_short_text_embedded_in_long_document_is_detected(self) -> None:
        self.short_overlap(".txt")

    def test_short_jsonl_field_embedded_in_long_document_is_detected(self) -> None:
        self.short_overlap(".jsonl")

    def test_staged_tree_is_checked_instead_of_clean_worktree(self) -> None:
        repo = self.root / "fixture-repo"
        repo.mkdir()
        subprocess.run(["git", "init", "--quiet", str(repo)], check=True, capture_output=True)
        folder = repo / "research"
        folder.mkdir()
        file = folder / "record.json"
        file.write_text(json.dumps({"dataset_row": "SYNTHETIC_CANARY"}))
        subprocess.run(["git", "-C", str(repo), "add", "research/record.json"], check=True, capture_output=True)
        file.write_text(json.dumps({"cases": 1}))
        staged = self.root / "staged"
        staged.mkdir()
        subprocess.run(
            ["git", "-C", str(repo), "checkout-index", "--all", "--prefix=" + str(staged) + os.sep],
            check=True,
            capture_output=True,
        )
        result = self.cli("--root", str(folder), "--staged-tree", str(staged / "research"))
        self.assertNotEqual(result.returncode, 0)

    def test_index_scan_ignores_worktree_venv_but_catches_staged_leak(self) -> None:
        repo = self.root / "index-fixture-repo"
        repo.mkdir()
        subprocess.run(["git", "init", "--quiet", str(repo)], check=True, capture_output=True)
        (repo / ".gitignore").write_text(".venv/\n", encoding="utf-8")
        (repo / "research").mkdir()
        (repo / "research" / "safe.md").write_text("safe numeric note\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", ".gitignore", "research/safe.md"], check=True, capture_output=True)
        external = self.root / "external-venv"
        external.mkdir()
        (external / "lib64").mkdir()
        (repo / ".venv").symlink_to(external, target_is_directory=True)
        (repo / "research" / "leak.json").write_text(json.dumps({"dataset_row": "SYNTHETIC_CANARY"}), encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "research/leak.json"], check=True, capture_output=True)

        result = self.cli("--staged-tree", str(repo))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("raw JSON field", result.stderr)
        self.assertNotIn("lib64", result.stderr)

    def test_index_scan_success_count_ignores_worktree_venv(self) -> None:
        repo = self.root / "index-success-fixture-repo"
        repo.mkdir()
        subprocess.run(["git", "init", "--quiet", str(repo)], check=True, capture_output=True)
        (repo / ".gitignore").write_text(".venv/\n", encoding="utf-8")
        (repo / "research").mkdir()
        (repo / "research" / "safe.md").write_text("safe numeric note\n", encoding="utf-8")
        subprocess.run(
            ["git", "-C", str(repo), "add", ".gitignore", "research/safe.md"],
            check=True,
            capture_output=True,
        )
        external = self.root / "success-external-venv"
        (external / "lib64").mkdir(parents=True)
        (repo / ".venv").symlink_to(external, target_is_directory=True)

        result = self.cli("--staged-tree", str(repo))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("publication guard: PASS (1 files)", result.stdout)


if __name__ == "__main__":
    unittest.main()
