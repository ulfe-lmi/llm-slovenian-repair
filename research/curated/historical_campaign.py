"""Portable copy of the native eight-worker campaign runner.

The source retains partitioning, resume checks, immutable result storage,
checkpoint markers and fail-closed independent-example handling.  A plan can
be rendered offline; execution is only possible with explicit resources and
``allow_live=True`` in the injected client factory.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing
import os
from pathlib import Path
import time
import traceback
from dataclasses import dataclass
from typing import Any, Callable

from .historical_common import jsonlines, pointer, read, save, sha, utc
from .historical_methods import direct, identity, no_retry, targeted
from .historical_transport import Client

WORKERS = 8


@dataclass(frozen=True)
class CampaignContract:
    phases: tuple[str, ...]
    workers: int
    methods: tuple[str, ...]
    retry_limit: int
    deployment: str
    remote_scoring: str


FINAL_CAMPAIGN = CampaignContract(
    phases=("dassle", "dassle-preservation", "multigec-dev", "multigec-dev-preservation", "multigec-test", "multigec-train", "slobench", "solar-canonical", "solar-canonical-preservation"),
    workers=8,
    methods=("RAW", "M0", "M1", "M2", "M3"),
    retry_limit=1,
    deployment="A100_FP8_ONLY",
    remote_scoring="PENDING_ACCESS",
)


def inherited_records(reuse_path: str | Path | None) -> dict[str, dict[str, Any]]:
    """Load the native read-only request reuse map without resolving private defaults."""
    if reuse_path is None or not Path(reuse_path).is_file():
        return {}
    value = read(reuse_path)
    return {item["destination"]: item for item in value.get("copied", []) if isinstance(item, dict) and "destination" in item}


def partition(rows: list[dict[str, Any]], worker: int, workers: int = WORKERS) -> list[dict[str, Any]]:
    if not 0 <= worker < workers:
        raise ValueError("worker outside historical partition range")
    return [row for row in rows if (row["index"] - 1) % workers == worker]


def process_identity(pid: int) -> dict[str, str] | None:
    try:
        parts = (Path(f"/proc/{pid}/stat").read_text().split(") ", 1)[1]).split()
        return {"state": parts[0], "start_ticks": parts[19]}
    except FileNotFoundError:
        return None


def stored(example: dict[str, Any], method: str, value: dict[str, Any], input_text: str | None = None) -> dict[str, Any]:
    import hashlib
    text = example["input"] if input_text is None else input_text
    return {"benchmark": example["benchmark"], "id": example["id"], "index": example["index"], "method": method,
            "input": text, "input_sha256": hashlib.sha256(text.encode()).hexdigest(), **value}


def one(example: dict[str, Any], method: str, pipeline: Any, client: Client, output_root: str | Path, *, raw: dict[str, Any] | None = None) -> dict[str, Any]:
    root = Path(output_root)
    path = root / "results" / "A100" / example["benchmark"] / f"{example['index']:06d}" / (method + ".json")
    text = example["input"] if raw is None else raw["output"]
    if path.exists():
        result = read(path)
        import hashlib
        if result.get("input_sha256") != hashlib.sha256(text.encode()).hexdigest() or result.get("method") != method or result.get("id") != example["id"]:
            raise AssertionError("saved campaign result identity changed")
        return result
    work = path.parent / method
    if raw is not None and raw.get("operational_failure"):
        value = {"output": text, "operational_failure": True, "failure": "BASE_TRANSLATION_FAILED", "calls": [], "edits": [], "wall_seconds": 0, "blocked_dependency": True}
    elif method == "M0":
        value = identity(text)
    elif method == "RAW":
        value = direct(text, client, work, translation=True)
    elif method == "M1":
        value = direct(text, client, work)
    elif method == "M2":
        value = targeted(text, pipeline, client, work)
    elif method == "M3":
        value = no_retry(text, read(root / "results" / "A100" / example["benchmark"] / f"{example['index']:06d}" / "M2.json"))
    else:
        raise ValueError("unknown historical campaign method")
    save(path, stored(example, method, value, text))
    return stored(example, method, value, text)


def offline_campaign_plan() -> dict[str, object]:
    return {"phases": list(FINAL_CAMPAIGN.phases), "workers": FINAL_CAMPAIGN.workers, "methods": list(FINAL_CAMPAIGN.methods),
            "retry_limit": FINAL_CAMPAIGN.retry_limit, "deployment": FINAL_CAMPAIGN.deployment, "remote_scoring": FINAL_CAMPAIGN.remote_scoring,
            "network_calls": 0, "model_calls": 0, "execution": "not started"}


def run_assigned(worker: int, phase: str, rows: list[dict[str, Any]], output_root: str | Path, pipeline_factory: Callable[[], Any], client_factory: Callable[[], Client]) -> None:
    monitor = Path(output_root) / "workers" / phase / str(worker)
    monitor.mkdir(parents=True, exist_ok=True)
    pipeline, client = pipeline_factory(), client_factory()
    started, done, blocked = time.monotonic(), 0, []
    def status(state: str, **extra: Any) -> None:
        identity_value = process_identity(os.getpid()) or {"start_ticks": None}
        pointer(monitor / "STATUS.json", {"status": state, "pid": os.getpid(), "process_start_ticks": identity_value["start_ticks"], "worker": worker, "phase": phase, "completed_assigned": done, "assigned": len(rows), "blocked_examples": blocked, "new_model_calls": client.network_calls, "seconds": time.monotonic() - started, "utc": utc(), **extra})
    status("RUNNING")
    try:
        for example in rows:
            status("RUNNING", current_index=example["index"], current_id=example["id"])
            try:
                if phase == "slobench":
                    raw = one(example, "RAW", pipeline, client, output_root)
                    for method in ("M1", "M2", "M3"):
                        one(example, method, pipeline, client, output_root, raw=raw)
                else:
                    for method in ("M0", "M1", "M2", "M3"):
                        one(example, method, pipeline, client, output_root)
            except Exception:
                incident = monitor / f"INCIDENT-{example['index']}-{time.time_ns()}.json"
                save(incident, {"utc": utc(), "phase": phase, "id": example["id"], "index": example["index"], "traceback": traceback.format_exc(), "worker": worker, "requires_separate_reconciliation": True})
                blocked.append({"id": example["id"], "index": example["index"], "incident": str(incident)})
            else:
                done += 1
            status("RUNNING", last_attempted_index=example["index"])
        status("COMPLETE" if not blocked else "INDEPENDENT_WORK_COMPLETE_WITH_BLOCKED_EXAMPLES")
    finally:
        pipeline.close()


def run(config: dict[str, Any], *, output_root: str | Path, pipeline_factory: Callable[[], Any], client_factory: Callable[[], Client]) -> dict[str, Any]:
    """Sequential historical campaign driver copied from campaign.py."""
    verify_configuration(config)
    completed: list[str] = []
    client = client_factory()
    pipeline = pipeline_factory()
    try:
        for benchmark in config["schedule"]:
            rows = jsonlines(config["datasets"][benchmark]["path"])
            for example in rows:
                if benchmark == "slobench":
                    raw = one(example, "RAW", pipeline, client, output_root)
                    for method in ("M1", "M2", "M3"):
                        one(example, method, pipeline, client, output_root, raw=raw)
                else:
                    for method in ("M0", "M1", "M2", "M3"):
                        one(example, method, pipeline, client, output_root)
            completed.append(benchmark)
            pointer(Path(output_root) / "phase-complete" / (benchmark + ".json"), {"benchmark": benchmark, "examples": len(rows), "new_model_calls": client.network_calls, "utc": utc()})
        status = "INFERENCE_COMPLETE_SCORING_AND_REPORT_PENDING"
    finally:
        pipeline.close()
    pointer(Path(output_root) / "RUN-STATUS.json", {"status": status, "completed_benchmarks": completed, "new_network_calls_this_process": client.network_calls, "utc": utc()})
    return {"status": status, "completed_benchmarks": completed, "new_model_calls": client.network_calls}


def refuse_live_default(*, allow_live: bool = False) -> None:
    if allow_live:
        raise PermissionError("campaign execution requires an explicit endpoint, input, output and bounded client authorization")


def verify_configuration(config: dict[str, Any]) -> dict[str, Any]:
    if config.get("concurrency", {}).get("requests_in_flight") != WORKERS or config.get("deployment", {}).get("model") != "qwen3.8-27b":
        raise ValueError("historical campaign configuration identity mismatch")
    if config.get("reasoning_effort") != "low" or config.get("english_threshold") != 3.0:
        raise ValueError("historical reasoning/English setting mismatch")
    if config.get("detector", {}).get("maximum", "missing") is not None or config.get("detector", {}).get("hidden_ceiling", "missing") is not None:
        raise ValueError("uncapped campaign detector was capped")
    return config
