"""The workflow whitespace CLI is tested through disposable Git histories."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "oap/bin/check_whitespace.py"
BASES = (
    "2832fa1e51bdf3641aabbd81feab8ddb64a876da",
    "82ea1e6f4173934fa47bb34ee6a6f78338d3603a",
)
INCIDENT = "oap/orders/007-e-recover-forward-from-an-immutable-invalid-report.md"


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


class WhitespaceVerifier(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="oap-whitespace-fixture-")
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        subprocess.run(
            ["git", "clone", "--shared", "--no-checkout", str(ROOT), str(self.repo)],
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        )
        self.assertEqual(
            git(self.repo, "config", "user.name", "Synthetic OAP fixture").returncode, 0
        )
        self.assertEqual(
            git(self.repo, "config", "user.email", "synthetic@example.invalid").returncode, 0
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, base: str = BASES[0]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "python3",
                "-B",
                str(CLI),
                "--repo-root",
                str(self.repo),
                "--base",
                base,
                "--revision",
                "HEAD",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )

    def read_tree_file(self, path: str) -> bytes:
        result = subprocess.run(
            ["git", "-C", str(self.repo), "show", f"HEAD:{path}"],
            capture_output=True,
            check=True,
            timeout=30,
        )
        return result.stdout

    def commit_tree(self, changes: dict[str, bytes | None], message: str) -> None:
        """Write one complete synthetic tree without sparse-worktree deletions."""

        index = self.root / "synthetic-index"
        env = {**os.environ, "GIT_INDEX_FILE": str(index)}
        parent = subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        ).stdout.strip()
        subprocess.run(
            ["git", "-C", str(self.repo), "read-tree", "HEAD"],
            env=env,
            capture_output=True,
            check=True,
            timeout=30,
        )
        for path, content in changes.items():
            if content is None:
                result = subprocess.run(
                    ["git", "-C", str(self.repo), "update-index", "--remove", "--", path],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                continue
            blob = subprocess.run(
                ["git", "-C", str(self.repo), "hash-object", "-w", "--stdin"],
                input=content,
                env=env,
                capture_output=True,
                check=True,
                timeout=30,
            ).stdout.decode().strip()
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.repo),
                    "update-index",
                    "--add",
                    "--cacheinfo",
                    f"100644,{blob},{path}",
                ],
                env=env,
                capture_output=True,
                check=True,
                timeout=30,
            )
        tree = subprocess.run(
            ["git", "-C", str(self.repo), "write-tree"],
            env=env,
            capture_output=True,
            check=True,
            timeout=30,
        ).stdout.decode().strip()
        commit = subprocess.run(
            ["git", "-C", str(self.repo), "commit-tree", tree, "-p", parent],
            input=(message + "\n").encode(),
            env=env,
            capture_output=True,
            check=True,
            timeout=30,
        ).stdout.decode().strip()
        subprocess.run(
            ["git", "-C", str(self.repo), "update-ref", "HEAD", commit],
            capture_output=True,
            check=True,
            timeout=30,
        )

    def assert_rejected(self, reason: str) -> None:
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(reason, result.stderr)

    def test_exact_incident_set_passes_both_authorized_bases(self) -> None:
        for base in BASES:
            with self.subTest(base=base):
                result = self.run_cli(base)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('"diagnostics": 3', result.stdout)

    def test_mutated_incident_blob_fails(self) -> None:
        self.commit_tree(
            {INCIDENT: self.read_tree_file(INCIDENT) + b"mutated\n"},
            "Synthetic incident mutation",
        )
        self.assert_rejected("INCIDENT_BLOB_MISMATCH")

    def test_deleted_and_readded_incident_fails_history_binding(self) -> None:
        original = self.read_tree_file(INCIDENT)
        self.commit_tree({INCIDENT: None}, "Synthetic incident deletion")
        self.assert_rejected("INCIDENT_BLOB_MISMATCH")
        self.commit_tree({INCIDENT: original}, "Synthetic incident re-addition")
        self.assert_rejected("INCIDENT_INTRODUCTION_MISMATCH")

    def test_extra_whitespace_fails_closed(self) -> None:
        self.commit_tree(
            {"synthetic-extra.txt": b"extra trailing space \n"},
            "Synthetic extra whitespace",
        )
        self.assert_rejected("DIAGNOSTIC_SET_MISMATCH")

    def test_path_line_and_message_drift_fails_closed(self) -> None:
        self.commit_tree(
            {
                INCIDENT: self.read_tree_file(INCIDENT).replace(
                    b"- Decision: NONE\n", b"- Decision: NONE \n", 1
                )
            },
            "Synthetic diagnostic drift",
        )
        self.assert_rejected("INCIDENT_BLOB_MISMATCH")

    def test_unknown_base_and_invalid_revision_fail_closed(self) -> None:
        unknown = self.run_cli("0" * 40)
        self.assertNotEqual(unknown.returncode, 0)
        self.assertIn("BASE_NOT_AUTHORIZED", unknown.stderr)
        invalid = subprocess.run(
            [
                "python3",
                "-B",
                str(CLI),
                "--repo-root",
                str(self.repo),
                "--base",
                BASES[0],
                "--revision",
                "not-a-revision",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("REVISION_INVALID", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
