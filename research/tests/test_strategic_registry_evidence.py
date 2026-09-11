"""The catalog must not erase evidence of an executed/interrupted campaign."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from research.tools.build_public_registry import experiment_records


class StrategicRegistryEvidence(unittest.TestCase):
    def test_execution_receipt_is_not_labelled_before_inference(self) -> None:
        parent = os.environ.get("TMPDIR")
        self.assertTrue(parent, "Use an owned persistent TMPDIR")
        Path(parent).mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="registry-evidence-", dir=parent) as name:
            home = Path(name)
            root = home / "experiments" / "large-evaluation-20260909.ZowPyK"
            root.mkdir(parents=True)
            (root / "CONFIGURATION.json").write_text(
                json.dumps({"status": "FROZEN_BEFORE_BENCHMARK_INFERENCE"})
            )
            (root / "RUN-STATUS.json").write_text(
                json.dumps(
                    {
                        "status": "RUNNING",
                        "phase": "multigec-dev",
                        "completed_examples_in_phase": 1,
                        "new_network_calls_this_process": 7,
                    }
                )
            )
            records = experiment_records(home)
        record = next(r for r in records if r["experiment_id"] == "large-evaluation-capped")
        self.assertNotEqual(record["status"], "FROZEN_BEFORE_BENCHMARK_INFERENCE")
        self.assertNotEqual(record["status"], "NOT_EXECUTED")


if __name__ == "__main__":
    unittest.main()
