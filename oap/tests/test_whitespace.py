"""The workflow whitespace CLI is tested through disposable Git histories."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "oap/bin/check_whitespace.py"
HISTORY_SOURCE_ENV = "OAP_FORWARD_RECOVERY_HISTORY_SOURCE"
BASES = (
    "2832fa1e51bdf3641aabbd81feab8ddb64a876da",
    "82ea1e6f4173934fa47bb34ee6a6f78338d3603a",
)
INCIDENT = "oap/orders/007-e-recover-forward-from-an-immutable-invalid-report.md"
ORDER_A = "oap/orders/027-a-repair-validation.md"
ORDER_031A = "oap/orders/031-a-functional-proxy-audit.md"
ORDER_A_INTRODUCTION = "d572b19c86a555ae3e8a4a8bbb99da5bd39a68ea"
RECOVERY_MERGE = "73f9f3d10cc602781f8a49e22a7dd342165ea8d9"
RECOVERY_PARENT_FIRST = "4e601d31ccce7fa2f7652e67af524bb95c761078"
RECOVERY_PARENT_SECOND = "db20450c3dd4ad93a559613c704a9fac1c625298"
NORMALIZED_BLOB = "6f2690ba42d1c92589491942557b40731c3b2dae"
BASE_D39 = "d39f629dabdb635a3b02fabb6840122cc8d181a2"


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
        source = Path(os.environ.get(HISTORY_SOURCE_ENV, str(ROOT)))
        subprocess.run(
            ["git", "clone", "--shared", "--no-checkout", str(source), str(self.repo)],
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
                self.assertIn('"diagnostics": 5', result.stdout)

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


    def test_trimmed_issued_order_a_fails_blob_binding(self) -> None:
        data = self.read_tree_file(ORDER_A)
        lines = data.split(b"\n")
        self.assertTrue(lines[10].endswith(b" "), "line 11 must carry the pinned space")
        lines[10] = lines[10][:-1]
        trimmed = b"\n".join(lines)
        self.assertNotEqual(trimmed, data)
        self.commit_tree({ORDER_A: trimmed}, "Synthetic issued-order trim")
        self.assert_rejected("INCIDENT_BLOB_MISMATCH")

    def test_deleted_and_readded_issued_order_a_fails_history_binding(self) -> None:
        original = self.read_tree_file(ORDER_A)
        self.commit_tree({ORDER_A: None}, "Synthetic issued-order deletion")
        self.assert_rejected("INCIDENT_BLOB_MISMATCH")
        self.commit_tree(
            {ORDER_A: original}, "Synthetic issued-order re-addition"
        )
        self.assert_rejected("RECOVERY_LINEAGE_MISSING")

    def test_mutated_issued_order_031a_fails_blob_binding(self) -> None:
        self.commit_tree(
            {ORDER_031A: self.read_tree_file(ORDER_031A) + b"mutated\n"},
            "Synthetic 031-a order mutation",
        )
        self.assert_rejected("INCIDENT_BLOB_MISMATCH")

    def test_trimmed_issued_order_031a_fails_blob_binding(self) -> None:
        data = self.read_tree_file(ORDER_031A)
        self.assertTrue(
            data.endswith(b"```\n\n"),
            "the pinned 031-a bytes end with the EOF blank line",
        )
        # Remove exactly the final newline: the line-161 EOF blank
        # line disappears and the issued bytes change.
        trimmed = data[:-1]
        self.assertNotEqual(trimmed, data)
        self.commit_tree({ORDER_031A: trimmed}, "Synthetic 031-a order trim")
        self.assert_rejected("INCIDENT_BLOB_MISMATCH")

    def test_deleted_and_readded_issued_order_031a_fails_history_binding(
        self,
    ) -> None:
        original = self.read_tree_file(ORDER_031A)
        self.commit_tree({ORDER_031A: None}, "Synthetic 031-a order deletion")
        self.assert_rejected("INCIDENT_BLOB_MISMATCH")
        self.commit_tree(
            {ORDER_031A: original}, "Synthetic 031-a order re-addition"
        )
        self.assert_rejected("INCIDENT_INTRODUCTION_MISMATCH")

    def test_missing_recovery_lineage_fails_closed(self) -> None:
        result = git(self.repo, "update-ref", "HEAD", RECOVERY_PARENT_FIRST)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_rejected("RECOVERY_LINEAGE_MISSING")

    def test_extra_recovery_parent_fails_closed(self) -> None:
        graft = git(
            self.repo,
            "replace",
            "--graft",
            RECOVERY_MERGE,
            RECOVERY_PARENT_FIRST,
            RECOVERY_PARENT_SECOND,
            BASE_D39,
        )
        self.assertEqual(graft.returncode, 0, graft.stderr)
        try:
            header = git(
                self.repo, "rev-list", "--parents", "-n", "1", RECOVERY_MERGE
            )
            self.assertEqual(header.returncode, 0, header.stderr)
            self.assertEqual(
                header.stdout.split(),
                [
                    RECOVERY_MERGE,
                    RECOVERY_PARENT_FIRST,
                    RECOVERY_PARENT_SECOND,
                    BASE_D39,
                ],
            )
            self.assert_rejected("RECOVERY_LINEAGE_MISSING")
        finally:
            drop = git(self.repo, "replace", "-d", RECOVERY_MERGE)
            self.assertEqual(drop.returncode, 0, drop.stderr)

    def test_substituted_original_introduction_blob_fails_closed(self) -> None:
        new_tree = self._swap_tree_entry(
            ORDER_A_INTRODUCTION, ORDER_A, NORMALIZED_BLOB
        )
        replacement = self._replacement_commit(ORDER_A_INTRODUCTION, new_tree)
        put = git(self.repo, "replace", ORDER_A_INTRODUCTION, replacement)
        self.assertEqual(put.returncode, 0, put.stderr)
        try:
            self.assert_rejected("RECOVERY_LINEAGE_MISSING")
        finally:
            drop = git(self.repo, "replace", "-d", ORDER_A_INTRODUCTION)
            self.assertEqual(drop.returncode, 0, drop.stderr)

    def _swap_tree_entry(self, commit: str, path: str, new_blob: str) -> str:
        parts = path.split("/")
        root_tree = git(self.repo, "rev-parse", f"{commit}^{{tree}}")
        self.assertEqual(root_tree.returncode, 0, root_tree.stderr)
        tree_shas = [root_tree.stdout.strip()]
        level_entries: list[list[str]] = []
        leaf_mode = "100644"
        for index, name in enumerate(parts):
            listing = git(self.repo, "ls-tree", tree_shas[index])
            self.assertEqual(listing.returncode, 0, listing.stderr)
            lines = listing.stdout.splitlines()
            level_entries.append(lines)
            entry = next(
                (line for line in lines if line.split("\t", 1)[1] == name),
                None,
            )
            if entry is None:
                self.fail(f"missing {name} in {commit} tree for {path}")
            mode, object_type, object_sha = entry.split("\t", 1)[0].split(" ")
            if index < len(parts) - 1:
                self.assertEqual(object_type, "tree", (path, name))
                tree_shas.append(object_sha)
            else:
                self.assertEqual(object_type, "blob", (path, name))
                leaf_mode = mode
        new_child = new_blob
        for index in range(len(parts) - 1, -1, -1):
            rewritten: list[str] = []
            for line in level_entries[index]:
                meta, name = line.split("\t", 1)
                mode, object_type, object_sha = meta.split(" ")
                if (
                    index == len(parts) - 1
                    and name == parts[-1]
                    and object_type == "blob"
                ):
                    rewritten.append(f"{leaf_mode} blob {new_blob}\t{name}")
                elif (
                    index < len(parts) - 1
                    and object_type == "tree"
                    and object_sha == tree_shas[index + 1]
                ):
                    rewritten.append(f"{mode} tree {new_child}\t{name}")
                else:
                    rewritten.append(line)
            mktree = subprocess.run(
                ["git", "-C", str(self.repo), "mktree"],
                input="\n".join(rewritten) + "\n",
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            new_child = mktree.stdout.strip()
        return new_child

    def _replacement_commit(self, commit: str, new_tree: str) -> str:
        header = git(
            self.repo, "log", "-1", "--format=%an%x1f%ae%x1f%aI%x1f%cn%x1f%ce%x1f%cI",
            commit,
        )
        self.assertEqual(header.returncode, 0, header.stderr)
        an, ae, ai, cn, ce, ci = header.stdout.rstrip("\n").split("\x1f")
        parents = (
            git(self.repo, "rev-list", "--parents", "-n", "1", commit).stdout.split()[1:]
        )
        message = git(self.repo, "log", "-1", "--format=%B", commit)
        self.assertEqual(message.returncode, 0, message.stderr)
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": an,
            "GIT_AUTHOR_EMAIL": ae,
            "GIT_AUTHOR_DATE": ai,
            "GIT_COMMITTER_NAME": cn,
            "GIT_COMMITTER_EMAIL": ce,
            "GIT_COMMITTER_DATE": ci,
        }
        result = subprocess.run(
            [
                "git", "-C", str(self.repo), "commit-tree", new_tree,
                *[arg for parent in parents for arg in ("-p", parent)],
            ],
            input=message.stdout,
            env=env,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return result.stdout.strip()


if __name__ == "__main__":
    unittest.main()
