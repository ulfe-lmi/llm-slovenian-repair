"""Synthetic historical-snapshot contract tests (objective 012, round 012-b).

File-only synthetic Git repositories (empty commits only) prove the
authorized historical review snapshot contract: a normal descendant main is
accepted; tampered order bytes, an unauthorized older snapshot, a foreign
divergent lineage and a future snapshot are rejected.  No network calls; no
dependency on the real repository history (also runs in copied workspaces).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

try:  # package-style run (python -m unittest research.tests.X)
    from research.tests.research_snapshot_contract import (
        SnapshotError,
        validate_historical_snapshot,
    )
except ImportError:  # discover-style run (directory on sys.path)
    from research_snapshot_contract import (
        SnapshotError,
        validate_historical_snapshot,
    )


class HistoricalSnapshotSyntheticTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="research-snapshot-synthetic-")
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.gitconfig = self.root / "gitconfig"
        self.gitconfig.write_bytes(b"[init]\n\tdefaultBranch = main\n")
        self._init()

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)
        self.temp.cleanup()

    # -- synthetic repository helpers ------------------------------------ #
    def _git(self, *args: str) -> str:
        env = dict(os.environ)
        env["GIT_CONFIG_GLOBAL"] = str(self.gitconfig)
        env["GIT_CONFIG_SYSTEM"] = "/dev/null"
        env["GIT_AUTHOR_NAME"] = "Synthetic Snapshot"
        env["GIT_AUTHOR_EMAIL"] = "synthetic@example.invalid"
        env["GIT_COMMITTER_NAME"] = "Synthetic Snapshot"
        env["GIT_COMMITTER_EMAIL"] = "synthetic@example.invalid"
        proc = subprocess.run(
            ["git", "-C", str(self.repo), "-c", "commit.gpgsign=false", *args],
            capture_output=True,
            env=env,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8"))
        return proc.stdout.decode("utf-8").strip()

    def _init(self) -> None:
        self._git("init", "-b", "main")

    def _commit(self, message: str) -> str:
        self._git("commit", "--allow-empty", "-m", message)
        return self._git("rev-parse", "HEAD")

    def _write_order(self, merge_commit: str, frozen_pr_head: str) -> Path:
        meta = {
            "id": "synthetic",
            "merged_tail_recovery": {
                "prior_id": "synthetic-prior",
                "merge_commit": merge_commit,
                "frozen_pr_head": frozen_pr_head,
            },
        }
        body = "# synthetic order\n\n```oap-metadata\n" + json.dumps(meta, indent=1) + "\n```\n"
        path = self.repo / "synthetic-order.md"
        path.write_text(body, encoding="utf-8")
        return path

    def _run(
        self,
        order_path: Path,
        identities: dict,
        *,
        current_main: str | None,
        pinned: str | None = None,
    ):
        # The pinned digest is the ORIGINAL order bytes digest; pass it
        # explicitly when the file has been mutated or removed after pinning.
        if pinned is None:
            pinned = hashlib.sha256(order_path.read_bytes()).hexdigest()
        return validate_historical_snapshot(
            self.repo,
            identities,
            current_main=current_main,
            order_rel=order_path.name,
            pinned_sha256=pinned,
        )

    def _identities(self, main_sha: str, parent: str) -> dict:
        return {
            "main_sha": main_sha,
            "reviewed_branch_head_sha": main_sha,
            "reviewed_branch_head_parent_sha": parent,
        }

    # -- cases ------------------------------------------------------------- #
    def test_accepts_normal_descendant_main(self) -> None:
        a = self._commit("a")
        b = self._commit("b")
        c = self._commit("c")
        order = self._write_order(b, a)
        result = self._run(order, self._identities(b, a), current_main=c)
        self.assertEqual(result["main_sha"], b)
        self.assertEqual(result["current_main"], c)

    def test_accepts_snapshot_equal_to_current_main(self) -> None:
        a = self._commit("a")
        b = self._commit("b")
        order = self._write_order(b, a)
        result = self._run(order, self._identities(b, a), current_main=b)
        self.assertEqual(result["main_sha"], b)

    def test_accepts_binding_only_without_current_main(self) -> None:
        a = self._commit("a")
        b = self._commit("b")
        order = self._write_order(b, a)
        result = self._run(order, self._identities(b, a), current_main=None)
        self.assertEqual(result["current_main"], None)

    def test_rejects_tampered_order_bytes(self) -> None:
        a = self._commit("a")
        b = self._commit("b")
        order = self._write_order(b, a)
        pinned = hashlib.sha256(order.read_bytes()).hexdigest()
        order.write_bytes(order.read_bytes() + b"tampered\n")
        with self.assertRaises(SnapshotError) as caught:
            self._run(order, self._identities(b, a), current_main=b, pinned=pinned)
        self.assertEqual(caught.exception.reason, "SNAPSHOT_ORDER_TAMPERED")

    def test_rejects_missing_order(self) -> None:
        a = self._commit("a")
        b = self._commit("b")
        order = self._write_order(b, a)
        pinned = hashlib.sha256(order.read_bytes()).hexdigest()
        order.unlink()
        with self.assertRaises(SnapshotError) as caught:
            self._run(order, self._identities(b, a), current_main=b, pinned=pinned)
        self.assertEqual(caught.exception.reason, "SNAPSHOT_ORDER_MISSING")

    def test_rejects_unauthorized_older_snapshot(self) -> None:
        a = self._commit("a")
        b = self._commit("b")
        order = self._write_order(b, a)
        # An older lineage member is not the authorized snapshot identity.
        with self.assertRaises(SnapshotError) as caught:
            self._run(order, self._identities(a, a), current_main=b)
        self.assertEqual(caught.exception.reason, "SNAPSHOT_IDENTITY_MISMATCH")

    def test_rejects_foreign_divergent_lineage(self) -> None:
        a = self._commit("a")
        b = self._commit("b")
        c = self._git("rev-parse", "HEAD")
        # Diverge from a: e is on a different lineage than main c.
        self._git("checkout", "-b", "divergent", a)
        e = self._commit("e")
        self._git("checkout", "main")
        order = self._write_order(e, a)
        with self.assertRaises(SnapshotError) as caught:
            self._run(order, self._identities(e, a), current_main=c)
        self.assertEqual(caught.exception.reason, "SNAPSHOT_LINEAGE")

    def test_rejects_future_snapshot_beyond_current_main(self) -> None:
        a = self._commit("a")
        b = self._commit("b")
        c = self._commit("c")
        f = self._commit("f")
        order = self._write_order(f, c)
        # f is a descendant of current main c - a future snapshot is foreign.
        with self.assertRaises(SnapshotError) as caught:
            self._run(order, self._identities(f, c), current_main=c)
        self.assertEqual(caught.exception.reason, "SNAPSHOT_LINEAGE")


if __name__ == "__main__":
    unittest.main()
