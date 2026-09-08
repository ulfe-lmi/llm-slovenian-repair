"""Focused real-history and cache-boundary tests for objective 006-k."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from oap_core import OAPError, check_report_history
from source_cache import CACHE_STATE_INVALID, CACHE_STATE_MISSING, plan


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


class CachePlanner(unittest.TestCase):
    def test_missing_cache_has_zero_network_gets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-plan-") as temporary:
            strategy = Path(temporary) / "strategy"
            strategy.mkdir()
            result = plan(strategy)
            self.assertEqual(result["state"], CACHE_STATE_MISSING)
            self.assertEqual(result["network_get_count"], 0)

    def test_unexpected_cache_file_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cache-invalid-") as temporary:
            strategy = Path(temporary) / "strategy"
            root = strategy / "source-cache/concept-verification/gigafida-2.0-words"
            root.mkdir(parents=True)
            (root / "unexpected").write_bytes(b"fixture")
            result = plan(strategy)
            self.assertEqual(result["state"], CACHE_STATE_INVALID)


if __name__ == "__main__":
    unittest.main()
