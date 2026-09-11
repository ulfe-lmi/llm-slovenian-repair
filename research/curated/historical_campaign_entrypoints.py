"""Copied prepare8/launch8 entrypoint checks with no default execution."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
from typing import Any

from .historical_campaign import verify_configuration
from .historical_campaign_storage import Storage
from .historical_common import save, utc


def verify(config: dict[str, Any], *, source: Storage | None = None) -> dict[str, Any]:
    """Validate configuration/frozen resource identities without starting workers."""
    verify_configuration(config)
    if source is not None:
        for path, expected in config.get("runtime_guard_files", {}).items():
            if source.source_sha(path) != expected:
                raise ValueError(f"runtime guard identity changed: {path}")
    return config


def prepare(config_path: str | Path, *, source: Storage, output_root: str | Path) -> dict[str, Any]:
    config = verify(source.source_read(config_path), source=source)
    result = {"status": "PREPARED_NO_NEW_MODEL_CALLS", "new_model_calls": 0, "schedule": config.get("schedule", []), "output_root": str(output_root)}
    save(Path(output_root) / "PREPARATION.json", result)
    return result


def launch_plan(*, root: str | Path, workers: int = 8, endpoint: str, credential_env: str, output_root: str | Path, max_cases: int, timeout_seconds: int) -> dict[str, Any]:
    if not endpoint or not credential_env or not output_root or workers < 1 or workers > 8 or max_cases < 1 or timeout_seconds < 1:
        raise ValueError("explicit endpoint, credential reference, output root and bounded resources required")
    return {"root": str(root), "workers": workers, "endpoint": endpoint, "credential_env": credential_env, "output_root": str(output_root), "max_cases": max_cases, "timeout_seconds": timeout_seconds, "started": False, "new_model_calls": 0}
