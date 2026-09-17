"""Portable copy of the native eight-worker campaign runner.

The source retains partitioning, resume checks, immutable result storage,
checkpoint markers and fail-closed independent-example handling.  A plan can
be rendered offline; execution is only possible with explicit resources and
``allow_live=True`` in the injected client factory.
"""

from __future__ import annotations

import json
import multiprocessing
import os
import time
import traceback
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .historical_common import jsonlines, pointer, read, safe_component, save, utc
from .historical_methods import direct, identity, no_retry, targeted
from .historical_transport import Client

WORKERS = 8
TERMINAL_WORKER_STATUSES = frozenset({
    "COMPLETE",
    "INDEPENDENT_WORK_COMPLETE_WITH_BLOCKED_EXAMPLES",
    "WORKER_FAILED_BEFORE_COMPLETION",
})


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


def one(
    example: dict[str, Any],
    method: str,
    pipeline: Any,
    client: Client,
    output_root: str | Path,
    *,
    raw: dict[str, Any] | None = None,
    retry_limit: int = FINAL_CAMPAIGN.retry_limit,
    model: str = "qwen3.8-27b",
) -> dict[str, Any]:
    root = Path(output_root)
    benchmark = safe_component(example["benchmark"], label="benchmark identity")
    safe_component(example["id"])
    if type(example["index"]) is not int or example["index"] < 1:
        raise ValueError("campaign record index must be a positive integer")
    method_name = safe_component(method, label="method identity")
    path = root / "results" / "A100" / benchmark / f"{example['index']:06d}" / (method_name + ".json")
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
        value = direct(text, client, work, translation=True, model=model)
    elif method == "M1":
        value = direct(text, client, work, model=model)
    elif method == "M2":
        value = targeted(text, pipeline, client, work, retry_limit=retry_limit, model=model)
    elif method == "M3":
        value = no_retry(text, read(root / "results" / "A100" / benchmark / f"{example['index']:06d}" / "M2.json"))
    else:
        raise ValueError("unknown historical campaign method")
    save(path, stored(example, method, value, text))
    return stored(example, method, value, text)


def offline_campaign_plan() -> dict[str, object]:
    return {"phases": list(FINAL_CAMPAIGN.phases), "workers": FINAL_CAMPAIGN.workers, "methods": list(FINAL_CAMPAIGN.methods),
            "retry_limit": FINAL_CAMPAIGN.retry_limit, "deployment": FINAL_CAMPAIGN.deployment, "remote_scoring": FINAL_CAMPAIGN.remote_scoring,
            "network_calls": 0, "model_calls": 0, "execution": "not started"}


def run_assigned(
    worker: int,
    phase: str,
    rows: list[dict[str, Any]],
    output_root: str | Path,
    pipeline_factory: Callable[[], Any],
    client_factory: Callable[[], Client],
    *,
    retry_limit: int = FINAL_CAMPAIGN.retry_limit,
    model: str = "qwen3.8-27b",
) -> None:
    phase_name = safe_component(phase, label="phase identity")
    if type(worker) is not int or not 0 <= worker < WORKERS:
        raise ValueError("worker outside historical partition range")
    monitor = Path(output_root) / "workers" / phase_name / str(worker)
    monitor.mkdir(parents=True, exist_ok=True)
    pipeline, client = pipeline_factory(), client_factory()
    started, done, blocked = time.monotonic(), 0, []
    def status(state: str, **extra: Any) -> None:
        identity_value = process_identity(os.getpid()) or {"start_ticks": None}
        pointer(monitor / "STATUS.json", {"status": state, "pid": os.getpid(), "process_start_ticks": identity_value["start_ticks"], "worker": worker, "phase": phase, "completed_assigned": done, "assigned": len(rows), "assigned_indices": [row["index"] for row in rows], "blocked_examples": blocked, "new_model_calls": client.network_calls, "seconds": time.monotonic() - started, "utc": utc(), **extra})
    status("RUNNING")
    try:
        for example in rows:
            status("RUNNING", current_index=example["index"], current_id=example["id"])
            try:
                if phase == "slobench":
                    raw = one(example, "RAW", pipeline, client, output_root, retry_limit=retry_limit, model=model)
                    for method in ("M1", "M2", "M3"):
                        one(example, method, pipeline, client, output_root, raw=raw, retry_limit=retry_limit, model=model)
                else:
                    for method in ("M0", "M1", "M2", "M3"):
                        one(example, method, pipeline, client, output_root, retry_limit=retry_limit, model=model)
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


def _worker_entry(
    worker: int,
    phase: str,
    rows: list[dict[str, Any]],
    output_root: str | Path,
    pipeline_factory: Callable[[], Any],
    client_factory: Callable[[], Client],
    retry_limit: int,
    model: str,
) -> None:
    """Process target matching runner8's one-process-per-worker boundary."""
    safe_component(phase, label="phase identity")
    try:
        run_assigned(
            worker,
            phase,
            rows,
            output_root,
            pipeline_factory,
            client_factory,
            retry_limit=retry_limit,
            model=model,
        )
    except BaseException as exc:
        monitor = Path(output_root) / "workers" / phase / str(worker)
        pointer(
            monitor / "STATUS.json",
            {
                "status": "WORKER_FAILED_BEFORE_COMPLETION",
                "pid": os.getpid(),
                "worker": worker,
                "phase": phase,
                "completed_assigned": 0,
                "assigned": len(rows),
                "new_model_calls": 0,
                "failure_type": type(exc).__name__,
            },
        )
        raise


def run(config: dict[str, Any], *, output_root: str | Path, pipeline_factory: Callable[[], Any], client_factory: Callable[[], Client]) -> dict[str, Any]:
    """Sequential historical campaign driver copied from campaign.py."""
    verify_configuration(config)
    schedule = config.get("schedule")
    datasets = config.get("datasets")
    if not isinstance(schedule, list) or not isinstance(datasets, dict):
        raise ValueError("historical campaign configuration lacks a schedule/datasets mapping")
    for scheduled in schedule:
        benchmark = safe_component(scheduled, label="phase identity")
        if benchmark not in datasets or not isinstance(datasets[benchmark], dict) or not isinstance(datasets[benchmark].get("path"), (str, Path)):
            raise ValueError(f"historical campaign dataset is missing for phase: {benchmark}")
    completed: list[str] = []
    client = client_factory()
    pipeline = pipeline_factory()
    try:
        for scheduled in schedule:
            benchmark = safe_component(scheduled, label="phase identity")
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
            pointer(Path(output_root) / "phase-complete" / (safe_component(benchmark, label="phase identity") + ".json"), {"benchmark": benchmark, "examples": len(rows), "new_model_calls": client.network_calls, "utc": utc()})
        status = "INFERENCE_COMPLETE_SCORING_AND_REPORT_PENDING"
    finally:
        pipeline.close()
    pointer(Path(output_root) / "RUN-STATUS.json", {"status": status, "completed_benchmarks": completed, "new_network_calls_this_process": client.network_calls, "utc": utc()})
    return {"status": status, "completed_benchmarks": completed, "new_model_calls": client.network_calls}


def run_injected(
    rows: list[dict[str, Any]],
    *,
    output_root: str | Path,
    workers: int,
    pipeline_factory: Callable[[], Any],
    client_factory: Callable[[], Client],
    retry_limit: int = FINAL_CAMPAIGN.retry_limit,
    model: str = "qwen3.8-27b",
    sequential: bool = False,
) -> dict[str, Any]:
    """Run the owned worker/phase entrypoint over injected private rows.

    This is the caller-owned reproduction seam used by the public CLI.  It
    exercises ``run_assigned`` and its worker status/checkpoint behavior while
    keeping rows and resources outside the repository.
    """
    if not 1 <= workers <= WORKERS:
        raise ValueError("campaign workers must be between 1 and 8")
    if retry_limit < 0:
        raise ValueError("retry limit must be non-negative")
    root = Path(output_root)
    normalized_rows: list[dict[str, Any]] = []
    for row in rows:
        benchmark = safe_component(row.get("benchmark"), label="benchmark identity")
        record_id = safe_component(row.get("id"))
        index = row.get("index")
        if type(index) is not int or index < 1:
            raise ValueError("campaign record index must be a positive integer")
        if not isinstance(row.get("input"), str):
            raise ValueError("campaign row lacks input")
        normalized_rows.append({"benchmark": benchmark, "id": record_id, "index": index, "input": row["input"]})
    phases: dict[str, list[dict[str, Any]]] = {}
    for row in normalized_rows:
        phase = row["benchmark"]
        phases.setdefault(phase, []).append(row)
    worker_statuses: list[dict[str, Any]] = []
    phase_incidents = False
    for phase, phase_rows in phases.items():
        # The historical scheduler assigns rows by stable index, then starts
        # one owned process per worker. SloBench's RAW->M1/M2/M3 branch lives in
        # run_assigned; all other phases use M0/M1/M2/M3 there.
        processes: list[Any] = []
        if sequential:
            for worker in range(workers):
                assigned = partition(phase_rows, worker, workers)
                try:
                    run_assigned(worker, phase, assigned, root, pipeline_factory, client_factory, retry_limit=retry_limit, model=model)
                except BaseException as exc:
                    monitor = root / "workers" / safe_component(phase, label="phase identity") / str(worker)
                    pointer(monitor / "STATUS.json", {
                        "status": "WORKER_FAILED_BEFORE_COMPLETION",
                        "worker": worker,
                        "phase": phase,
                        "completed_assigned": 0,
                        "assigned": len(assigned),
                        "assigned_indices": [row["index"] for row in assigned],
                        "new_model_calls": 0,
                        "failure_type": type(exc).__name__,
                    })
        else:
            context: Any
            try:
                context = multiprocessing.get_context("fork")
            except ValueError:
                context = multiprocessing.get_context("spawn")
            for worker in range(workers):
                assigned = partition(phase_rows, worker, workers)
                process = context.Process(
                    target=_worker_entry,
                    args=(worker, phase, assigned, root, pipeline_factory, client_factory, retry_limit, model),
                )
                process.start()
                processes.append(process)
            for process in processes:
                process.join()
        phase_statuses: list[dict[str, Any]] = []
        for worker in range(workers):
            status_path = root / "workers" / phase / str(worker) / "STATUS.json"
            process: Any = processes[worker] if not sequential else None
            exit_code = getattr(process, "exitcode", 0) if process is not None else 0
            incident: str | None = None
            status: dict[str, Any] | None = None
            if status_path.is_symlink():
                incident = "worker status is a symlink"
            elif status_path.is_file():
                try:
                    value = read(status_path)
                    if isinstance(value, dict):
                        status = value
                    else:
                        incident = "worker status is not an object"
                except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
                    incident = f"worker status is unreadable: {type(exc).__name__}"
            else:
                incident = "worker exited before writing status"
            if status is None:
                status = {}
            if incident is None and status.get("status") not in TERMINAL_WORKER_STATUSES:
                incident = "worker status has no terminal selection"
            if incident is None and status.get("worker") != worker:
                incident = "worker status identity mismatch"
            if incident is None and status.get("phase") != phase:
                incident = "worker status phase mismatch"
            if exit_code not in (0, None):
                incident = incident or f"worker exited with code {exit_code}"
            if incident is not None:
                phase_incidents = True
                previous = status.get("status")
                status = {
                    **status,
                    "status": "WORKER_FAILED_BEFORE_COMPLETION",
                    "worker": worker,
                    "phase": phase,
                    "assigned": len(partition(phase_rows, worker, workers)),
                    "assigned_indices": [row["index"] for row in partition(phase_rows, worker, workers)],
                    "completed_assigned": int(status.get("completed_assigned", 0) or 0),
                    "new_model_calls": int(status.get("new_model_calls", 0) or 0),
                    "exit_code": exit_code,
                    "worker_incident": incident,
                    "previous_status": previous,
                }
                pointer(status_path, status)
            phase_statuses.append(status)
            worker_statuses.append(status)
        if len(phase_statuses) != workers or any(item.get("status") not in TERMINAL_WORKER_STATUSES for item in phase_statuses):
            phase_incidents = True
        pointer(root / "phase-complete" / (phase + ".json"), {
            "phase": phase,
            "examples": len(phase_rows),
            "workers": workers,
            "methods": ["RAW", "M1", "M2", "M3"] if phase == "slobench" else ["M0", "M1", "M2", "M3"],
            "retry_limit": retry_limit,
            "model": model,
            "new_model_calls": sum(int(item.get("new_model_calls", 0)) for item in phase_statuses),
            "status": "COMPLETE" if all(item.get("status") == "COMPLETE" for item in phase_statuses) else "RECORDED_WITH_WORKER_INCIDENTS",
            "utc": utc(),
        })
    result = {
        "status": "RECORDED_WITH_WORKER_INCIDENTS" if phase_incidents else "INFERENCE_COMPLETE_SCORING_AND_REPORT_PENDING",
        "phases": list(phases),
        "workers": workers,
        "methods": {phase: (["RAW", "M1", "M2", "M3"] if phase == "slobench" else ["M0", "M1", "M2", "M3"]) for phase in phases},
        "completed_cases": sum(len(value) for value in phases.values()),
        "worker_statuses": worker_statuses,
        "new_model_calls": sum(int(item.get("new_model_calls", 0)) for item in worker_statuses),
        "network_calls": sum(int(item.get("new_model_calls", 0)) for item in worker_statuses),
        "model_calls": sum(int(item.get("new_model_calls", 0)) for item in worker_statuses),
        "process_scheduler": "sequential-test-seam" if sequential else "multiprocessing-worker-processes",
    }
    pointer(root / "RUN-STATUS.json", result)
    return {"executed": True, "records": result["completed_cases"], "output_root": "caller-supplied", **result}


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
