"""CLI and verifier coverage for the compressed multi-root identity recipe."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from research.tools.replay import verify_manifest


class IntegrityRecipeTests(unittest.TestCase):
    def setUp(self) -> None:
        parent = os.environ.get("TMPDIR")
        self.assertTrue(parent and not parent.startswith("/tmp"))
        self.root = Path(tempfile.mkdtemp(prefix="integrity-recipe-", dir=parent))
        self.private = self.root / "private"
        (self.private / "sample").mkdir(parents=True)
        self.payload = self.private / "sample" / "artifact.bin"
        self.payload.write_bytes(b"synthetic-private-identity")

    def ledger(self, *, relative: str = "artifact.bin", root: str = "experiments/sample/", sha: str | None = None, size: int | None = None, classification: str = "private-only") -> Path:
        raw = self.payload.read_bytes()
        entry = {
            "classification": classification,
            "relative_path": relative,
            "root": root,
            "sha256": sha or hashlib.sha256(raw).hexdigest(),
            "size": len(raw) if size is None else size,
        }
        path = self.root / "ledger.json.gz"
        with gzip.GzipFile(path, "wb", mtime=0) as stream:
            stream.write(json.dumps({"entries": [entry]}).encode())
        return path

    def test_real_compressed_ledger_and_cli_root_mapping(self) -> None:
        ledger = self.ledger()
        self.assertEqual(verify_manifest(ledger, root_map={"experiments/": self.private}), (1, 0))
        command = [
            sys.executable, "-B", "-m", "research.tools.replay", "--manifest", str(ledger),
            "--root-map", f"experiments/={self.private}", "--limit", "1",
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True, env={**os.environ, "TMPDIR": os.environ["TMPDIR"]})
        self.assertEqual(json.loads(result.stdout)["identity_replay"], {"checked": 1, "skipped": 0})

    def test_summary_json_is_rejected(self) -> None:
        summary = self.root / "summary.json"
        summary.write_text(json.dumps({"entries": 1, "full_census": "ledger.json.gz"}))
        with self.assertRaises(ValueError):
            verify_manifest(summary, root_map={"experiments/": self.private})

    def test_mapping_missing_hash_size_traversal_and_symlink_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            verify_manifest(self.ledger(), root_map={"recovery-executions/": self.private})
        with self.assertRaises(ValueError):
            verify_manifest(self.ledger(sha="0" * 64), root_map={"experiments/": self.private})
        with self.assertRaises(ValueError):
            verify_manifest(self.ledger(size=1), root_map={"experiments/": self.private})
        with self.assertRaises(ValueError):
            verify_manifest(self.ledger(relative="../escape"), root_map={"experiments/": self.private})
        link = self.private / "sample" / "link.bin"
        link.symlink_to(self.payload)
        with self.assertRaises(ValueError):
            verify_manifest(self.ledger(relative="link.bin"), root_map={"experiments/": self.private})


if __name__ == "__main__":
    unittest.main()
