"""Copied checkpoint8 logic without cloud or model side effects."""

from __future__ import annotations

from pathlib import Path
import tarfile
import time
from typing import Any

from .historical_common import immutable_bytes, read, save, sha, utc


def checkpoint_completed_cases(root: str | Path, workspace: str | Path, config: dict[str, Any]) -> dict[str, Any]:
    root, workspace = Path(root), Path(workspace)
    folder = root / "checkpoints"
    folder.mkdir(parents=True, exist_ok=True)
    backed = set()
    for receipt in sorted(folder.glob("*.json")):
        entry = read(receipt)
        if entry.get("kind") == "completed-case-checkpoint":
            backed.update(entry["case_keys"])
    available = []
    for phase in config["schedule"]:
        for index in range(1, config["datasets"][phase]["examples"] + 1):
            key = f"{phase}/{index:06d}"
            directory = root / "results/A100" / key
            names = ("RAW", "M1", "M2", "M3") if phase == "slobench" else ("M0", "M1", "M2", "M3")
            if key not in backed and all((directory / (name + ".json")).is_file() for name in names):
                available.append((key, directory))
    for start in range(0, len(available), 25):
        batch = available[start : start + 25]
        archive = folder / f"cases-{time.time_ns()}.tar.gz"
        with tarfile.open(archive, "x:gz") as output:
            for key, directory in batch:
                output.add(directory, arcname=str(directory.relative_to(root)), filter=lambda info: None if Path(info.name).name.startswith(".") else info)
        entry = {"kind": "completed-case-checkpoint", "utc": utc(), "case_keys": [key for key, _ in batch], "archive": str(archive), "sha256": sha(archive), "new_model_calls": 0, "cloud_sync_asserted": False}
        save(folder / (archive.stem + ".json"), entry)
    return {"completed_cases_archived": len(backed) + len(available), "new_model_calls": 0, "cloud_sync_asserted": False}
