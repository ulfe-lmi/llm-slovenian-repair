"""Run the owner-authorized 007-i contextual validator experiment.

Preparation copies only the frozen 007-h inputs into an explicitly supplied
native private root.  Live execution is opt-in and uses no default endpoint.
Every request, bounded raw response, and parsed observation is immutable; the
two projections are aggregated only from those same observations.
"""

from __future__ import annotations

import argparse
import base64
import copy
import gzip
import hashlib
import json
import os
import shutil
import statistics
import stat
import subprocess
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from research import contextual_validator as protocol
from research.curated.historical_scoring import row_metrics, summarize
from research.curated.patching import apply_edits
from research.one_substitution import (
    candidate_key,
    mechanical_substitution,
    project_saved_case,
    qualifying_candidates,
)
from research.tools import run_one_substitution as prior

RUN_ID = "007-i"
EXPERIMENT_ID = "007-i-contextual-validator"
PHASES = {"dassle-spelling": 1_487, "dassle-spelling-preservation": 1_486}
EXPECTED_CANDIDATES = {"dassle-spelling": 571, "dassle-spelling-preservation": 164}
EXPECTED_TOTAL = 735
FROZEN_7H_HEAD = "e916a2d9cafd171fbb71bfc70ac2c21222118f6e"
FROZEN_7H_IMPLEMENTATION_HEAD = "65ba55ef3ff84bda4202190e589d45721409287b"
FROZEN_7H_CONFIGURATION = "10657c4a2a2c53cc6bea9fab4164671dae0196d5c442275da1fb33c0326d27ee"
FROZEN_7H_CASE_MANIFEST = "4490d7c1e14b28369217d06915bc1fce936160108de615f22f59032a803a46ef"
FROZEN_PROFILE_SHA256 = "c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60"
FROZEN_PROMPT_SHA256 = protocol.FROZEN_PROMPT_SHA256
MODEL = protocol.MODEL
WORKERS = protocol.WORKERS


class ExperimentError(RuntimeError):
    """Raised when a frozen input, protocol, or publication boundary fails."""


def canonical_bytes(value: object) -> bytes:
    return protocol.canonical_bytes(value)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return protocol.sha256_file(path)


def read_json(path: Path) -> Any:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExperimentError(f"invalid private JSON artifact: {path.name}") from exc
    return value


def require_owned_dir(path: Path, *, mode: int = 0o700) -> None:
    try:
        info = path.lstat()
    except OSError as exc:
        raise ExperimentError(f"private directory is unavailable: {path}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise ExperimentError(f"private path is not a real directory: {path.name}")
    if info.st_uid != os.getuid():
        raise ExperimentError(f"private directory ownership mismatch: {path.name}")
    if stat.S_IMODE(info.st_mode) != mode:
        os.chmod(path, mode)


def require_owned_file(path: Path, *, expected_sha: str | None = None) -> None:
    try:
        info = path.lstat()
    except OSError as exc:
        raise ExperimentError(f"private file is unavailable: {path.name}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise ExperimentError(f"private file is not a regular file: {path.name}")
    if info.st_uid != os.getuid():
        raise ExperimentError(f"private file ownership mismatch: {path.name}")
    if expected_sha is not None and sha256_file(path) != expected_sha:
        raise ExperimentError(f"private file hash mismatch: {path.name}")


def immutable_write(path: Path, data: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    require_owned_dir(path.parent)
    if path.exists():
        require_owned_file(path)
        if path.read_bytes() != data:
            raise ExperimentError(f"immutable artifact conflict: {path.name}")
        return sha256_bytes(data)
    temporary = path.with_name("." + path.name + ".pending")
    if temporary.exists() or temporary.is_symlink():
        raise ExperimentError(f"temporary artifact collision: {temporary.name}")
    temporary.write_bytes(data)
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)
    os.chmod(path, 0o600)
    return sha256_bytes(data)


def immutable_json(path: Path, value: object) -> str:
    return immutable_write(path, canonical_bytes(value))


def mutable_status(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    require_owned_dir(path.parent)
    if path.exists() and path.is_symlink():
        raise ExperimentError(f"refusing symlink status: {path.name}")
    temporary = path.with_name("." + path.name + ".pointer")
    temporary.write_bytes(canonical_bytes(value))
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)
    os.chmod(path, 0o600)


def copy_file_exact(source: Path, destination: Path) -> None:
    require_owned_file(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    require_owned_dir(destination.parent)
    if destination.exists():
        require_owned_file(destination, expected_sha=sha256_file(source))
        return
    temporary = destination.with_name("." + destination.name + ".copy")
    if temporary.exists() or temporary.is_symlink():
        raise ExperimentError(f"copy temporary collision: {temporary.name}")
    shutil.copyfile(source, temporary)
    os.chmod(temporary, 0o600)
    os.replace(temporary, destination)
    os.chmod(destination, 0o600)


def copy_tree_exact(source: Path, destination: Path) -> None:
    require_owned_dir(source)
    destination.mkdir(parents=True, exist_ok=True)
    require_owned_dir(destination)
    for entry in sorted(source.iterdir(), key=lambda item: item.name):
        target = destination / entry.name
        if entry.is_symlink():
            raise ExperimentError(f"source tree contains symlink: {entry.name}")
        if entry.is_dir():
            copy_tree_exact(entry, target)
        elif entry.is_file():
            copy_file_exact(entry, target)
        else:
            raise ExperimentError(f"source tree contains unsupported type: {entry.name}")


def stage_frozen_inputs(source_root: Path, scratch: Path) -> None:
    """Copy only the 007-h inputs/cases/manifests; never alter their source."""
    require_owned_dir(source_root)
    scratch.mkdir(parents=True, exist_ok=True)
    require_owned_dir(scratch)
    for name in ("inputs", "cases"):
        source = source_root / name
        if not source.is_dir() or source.is_symlink():
            raise ExperimentError(f"007-h source subtree is unavailable: {name}")
        copy_tree_exact(source, scratch / name)
    copy_file_exact(source_root / "INPUT-MANIFEST.json", scratch / "INPUT-MANIFEST.json")


def source_and_code_identity(repo_root: Path, expected_head: str) -> dict[str, Any]:
    try:
        head = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--verify", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        branch = subprocess.run(
            ["git", "-C", str(repo_root), "symbolic-ref", "--quiet", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain=v1", "--untracked-files=all"],
            check=True,
            capture_output=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ExperimentError("implementation Git identity cannot be read") from exc
    if head != expected_head or branch != "oap/007-concept-verification" or status:
        raise ExperimentError("implementation must be clean at the expected branch head")
    paths = (
        "research/contextual_validator.py",
        "research/tools/run_contextual_validator.py",
        "research/one_substitution.py",
        "research/curated/historical_scoring.py",
        "research/curated/patching.py",
    )
    blobs: dict[str, Any] = {}
    for relative in paths:
        path = repo_root / relative
        require_owned_file(path)
        try:
            blob = subprocess.run(
                ["git", "-C", str(repo_root), "show", f"HEAD:{relative}"],
                check=True,
                capture_output=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError) as exc:
            raise ExperimentError(f"implementation blob is unavailable: {relative}") from exc
        if path.read_bytes() != blob:
            raise ExperimentError(f"implementation bytes differ from HEAD: {relative}")
        blobs[relative] = {"sha256": sha256_bytes(blob)}
    return {"implementation_head": head, "branch": branch, "head_blobs": blobs}


def load_frozen_state(scratch: Path) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any], set[int], dict[str, Any], str]:
    prior.verify_frozen_inputs(scratch)
    pairs = prior.load_pairs(scratch)
    baseline = prior.validate_baseline_replay(pairs)
    uv_indices, uv_mapping = prior.verify_uv_mapping(scratch, pairs["dassle-spelling"])
    frozen_records, case_digest, total_bytes = prior.frozen_case_manifest(
        scratch, pairs, prior.FROZEN_CONFIGURATION_SHA256
    )
    if case_digest != FROZEN_7H_CASE_MANIFEST or total_bytes != prior.FROZEN_CASE_BYTES:
        raise ExperimentError("007-h case identity does not match the frozen order")
    if sum(len(rows) for rows in pairs.values()) != 2_973:
        raise ExperimentError("007-h population is not 2,973 rows")
    return pairs, baseline, uv_indices, frozen_records, case_digest


def build_population(
    records_by_phase: dict[str, list[dict[str, Any]]],
    vocabulary: set[str],
    buckets: dict[int, list[str]],
) -> list[dict[str, Any]]:
    population: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for phase, records in records_by_phase.items():
        for case in records:
            baseline = case["baseline"]
            targets = case["mechanical"].get("targets")
            if not isinstance(targets, list):
                raise ExperimentError("007-h case lacks mechanical targets")
            for ordinal, target in enumerate(targets):
                if not isinstance(target, dict):
                    raise ExperimentError("007-h mechanical target is not an object")
                if not (target.get("cardinality") == "C=1" and target.get("accepted") is True):
                    continue
                candidate = target.get("candidate")
                forms = target.get("candidate_forms")
                gate = target.get("gate")
                if not isinstance(candidate, dict) or not isinstance(forms, list) or len(forms) != 1 or not isinstance(forms[0], str):
                    raise ExperimentError("007-h unique target schema is invalid")
                start, end, text = candidate.get("start"), candidate.get("end"), candidate.get("text")
                if type(start) is not int or type(end) is not int or not isinstance(text, str):
                    raise ExperimentError("007-h candidate coordinates are invalid")
                if baseline["input"][start:end] != text:
                    raise ExperimentError("007-h candidate coordinate is stale")
                lookup_form = text.casefold()
                actual = qualifying_candidates(lookup_form, buckets.get(len(lookup_form), ()))
                if actual != forms:
                    raise ExperimentError("007-h candidate-generation drift")
                if len(actual) != 1:
                    raise ExperimentError("007-h unique candidate cardinality drift")
                recomputed = mechanical_substitution(baseline["input"], candidate, actual[0], vocabulary)
                edit = recomputed.get("edit")
                if not recomputed.get("accepted") or not isinstance(edit, list) or gate is None:
                    raise ExperimentError("007-h mechanical gate drift")
                if gate.get("edit") != edit:
                    raise ExperimentError("007-h accepted edit identity drift")
                population.append(
                    {
                        "phase": phase,
                        "case_index": int(case["index"]),
                        "case_id": case["id"],
                        "target_ordinal": ordinal,
                        "target_start": start,
                        "target_end": end,
                        "candidate": copy.deepcopy(candidate),
                        "candidate_form": actual[0],
                        "mechanical_edit": copy.deepcopy(edit),
                        "sentence": baseline["input"],
                        "reference": case["dataset"].get("reference"),
                    }
                )
                counts[phase] += 1
    if dict(counts) != EXPECTED_CANDIDATES or len(population) != EXPECTED_TOTAL:
        raise ExperimentError(f"007-h candidate population mismatch: {dict(counts)}")
    return protocol.ordered_candidates(population)


def private_manifest(population: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], str]:
    manifest, digest = protocol.candidate_manifest(population)
    return manifest, digest


def build_configuration(
    repo_root: Path,
    scratch: Path,
    implementation: dict[str, Any],
    case_digest: str,
    baseline: dict[str, Any],
    uv_indices: set[int],
    population: list[dict[str, Any]],
    candidate_digest: str,
) -> dict[str, Any]:
    code_paths = {
        name: sha256_file(repo_root / name)
        for name in (
            "research/contextual_validator.py",
            "research/tools/run_contextual_validator.py",
            "research/one_substitution.py",
            "research/curated/historical_scoring.py",
            "research/curated/patching.py",
        )
    }
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "run_id": RUN_ID,
        "status": "FROZEN_BEFORE_LIVE_EXECUTION",
        "implementation_head": implementation["implementation_head"],
        "implementation_branch": implementation["branch"],
        "prior_007h_head": FROZEN_7H_HEAD,
        "source_identity": {
            "dataset_rows": PHASES,
            "paired_rows": 2_973,
            "case_identity_manifest_sha256": case_digest,
            "input_manifest_sha256": sha256_file(scratch / "INPUT-MANIFEST.json"),
            "candidate_manifest_sha256": candidate_digest,
            "candidate_count": len(population),
            "candidate_counts": EXPECTED_CANDIDATES,
            "uv_audit_rows": len(uv_indices),
            "uv_indices_sha256": sha256_bytes(("\n".join(str(item) for item in sorted(uv_indices)) + "\n").encode()),
        },
        "prior_007h_identity": {
            "implementation_head": FROZEN_7H_IMPLEMENTATION_HEAD,
            "configuration_sha256": FROZEN_7H_CONFIGURATION,
            "case_identity_manifest_sha256": FROZEN_7H_CASE_MANIFEST,
            "baseline": baseline,
        },
        "code_identity": {"sha256": code_paths, "head_blobs": implementation["head_blobs"]},
        "prompt": {"sha256": FROZEN_PROMPT_SHA256, "template": "owner-supplied 007-i validator prompt"},
        "deployment": {
            "class": "A100-FP8",
            "model": MODEL,
            "profile_sha256": FROZEN_PROFILE_SHA256,
            "endpoint": "private Responses endpoint",
            "protocol": "Responses non-streaming",
        },
        "request": {
            "fields": ["model", "stream", "store", "input", "include_reasoning", "reasoning"],
            "stream": False,
            "store": False,
            "include_reasoning": True,
            "reasoning_effort": "low",
            "serializer": "canonical UTF-8 JSON with one final LF",
        },
        "parser": {
            "status": "completed",
            "assistant_output_text_fields": 1,
            "choices": sorted(protocol.CHOICES),
            "surrounding_whitespace_only": True,
            "duplicate_json_keys": "reject",
            "token_accounting": "input/output/reasoning nonnegative integers",
        },
        "scheduling": {
            "workers": WORKERS,
            "partition_key": ["phase", "case_index", "target_start", "target_end", "target_ordinal"],
            "partition": "stable ordered position modulo worker count",
            "in_flight_per_worker": 1,
            "maximum_in_flight": WORKERS,
            "scheduled_candidates": len(population),
        },
        "limits": {"timeout_seconds": protocol.TIMEOUT_SECONDS, "response_bound_bytes": protocol.MAX_RESPONSE_BYTES, "attempts_per_candidate": 1, "resampling": False},
        "persistence": {"order": ["request bytes", "bounded raw response/timing", "parsed observation"], "interrupted_request": "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE", "immutable_completed_observations": True},
        "projections": {
            "validated_fallback": "USE_CANDIDATE mechanical edit; every other decision uses saved 007-h baseline fallback",
            "validated_only": "USE_CANDIDATE mechanical edit; every other decision leaves original target",
            "shared_observation": True,
            "baseline_calls_resampled": False,
        },
        "scorer": {"implementation_head": FROZEN_7H_IMPLEMENTATION_HEAD, "attribution": "unchanged token-coordinate 007-h scorer"},
        "privacy": {"public": "aggregate metrics, hashes, limitations only", "private": "filled prompts, sentences, targets, responses, credentials and endpoint/profile values"},
        "no_tuning_or_resampling": True,
        "private_evidence_root": str(scratch),
    }


def prepare(
    repo_root: Path,
    scratch: Path,
    source_root: Path,
    expected_head: str,
) -> dict[str, Any]:
    if prompt_sha256 := protocol.prompt_sha256():
        if prompt_sha256 != FROZEN_PROMPT_SHA256:
            raise ExperimentError("frozen prompt hash mismatch")
    stage_frozen_inputs(source_root, scratch)
    implementation = source_and_code_identity(repo_root, expected_head)
    pairs, baseline, uv_indices, frozen_records, case_digest = load_frozen_state(scratch)
    vocabulary, buckets, _vocabulary_seconds, _vocabulary_rows = prior.load_vocabulary(
        scratch / "inputs/index/index.sqlite"
    )
    population = build_population(frozen_records, vocabulary, buckets)
    manifest, candidate_digest = private_manifest(population)
    immutable_json(scratch / "CANDIDATE-MANIFEST.json", manifest)
    immutable_json(scratch / "CANDIDATES.json", population)
    configuration = build_configuration(
        repo_root, scratch, implementation, case_digest, baseline, uv_indices, population, candidate_digest
    )
    configuration_sha = immutable_json(scratch / "CONFIGURATION.json", configuration)
    if sha256_file(scratch / "CONFIGURATION.json") != configuration_sha:
        raise ExperimentError("configuration hash cannot be verified")
    mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "run_id": RUN_ID,
            "configuration_sha256": configuration_sha,
            "candidate_manifest_sha256": candidate_digest,
            "scheduled_candidates": EXPECTED_TOTAL,
            "actual_validator_call_records": 0,
        },
    )
    return {"configuration": configuration, "configuration_sha256": configuration_sha, "population": population, "pairs": pairs, "baseline": baseline, "uv_indices": uv_indices, "case_records": frozen_records, "candidate_manifest_sha256": candidate_digest}


def load_prepared(scratch: Path, expected_head: str | None = None) -> dict[str, Any]:
    configuration = read_json(scratch / "CONFIGURATION.json")
    if not isinstance(configuration, dict) or configuration.get("experiment_id") != EXPERIMENT_ID:
        raise ExperimentError("prepared configuration identity mismatch")
    if expected_head and configuration.get("implementation_head") != expected_head:
        raise ExperimentError("prepared implementation head mismatch")
    require_owned_file(scratch / "CONFIGURATION.json")
    manifest = read_json(scratch / "CANDIDATE-MANIFEST.json")
    population = read_json(scratch / "CANDIDATES.json")
    if not isinstance(manifest, list) or not isinstance(population, list):
        raise ExperimentError("prepared candidate manifest is malformed")
    if protocol.candidate_manifest(population)[1] != configuration["source_identity"]["candidate_manifest_sha256"]:
        raise ExperimentError("prepared candidate manifest hash mismatch")
    pairs, baseline, uv_indices, case_records, case_digest = load_frozen_state(scratch)
    if case_digest != configuration["source_identity"]["case_identity_manifest_sha256"]:
        raise ExperimentError("prepared case identity mismatch")
    return {"configuration": configuration, "configuration_sha256": sha256_file(scratch / "CONFIGURATION.json"), "population": protocol.ordered_candidates(population), "pairs": pairs, "baseline": baseline, "uv_indices": uv_indices, "case_records": case_records, "candidate_manifest": manifest}


def _candidate_observation_path(scratch: Path, candidate: dict[str, Any]) -> Path:
    return scratch / "requests" / protocol.candidate_path_id(candidate)


def _call_one(scratch: Path, candidate: dict[str, Any], endpoint: str | None, credential_env: str | None) -> dict[str, Any]:
    directory = _candidate_observation_path(scratch, candidate)
    body = protocol.request_body(candidate["sentence"], candidate["candidate"]["text"], candidate["candidate_form"])
    return protocol.perform_call(
        directory,
        body,
        endpoint=endpoint,
        credential_env=credential_env,
        timeout=protocol.TIMEOUT_SECONDS,
        max_response_bytes=protocol.MAX_RESPONSE_BYTES,
    )


def execute_validator(
    scratch: Path,
    population: list[dict[str, Any]],
    *,
    endpoint: str | None,
    credential_env: str | None,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    partitions = protocol.partitions(population)
    observations: dict[str, dict[str, Any]] = {}
    worker_status: dict[int, dict[str, Any]] = {}

    def worker(worker_id: int) -> tuple[int, dict[str, dict[str, Any]], dict[str, Any]]:
        started = time.monotonic()
        local: dict[str, dict[str, Any]] = {}
        dispatched = 0
        failures = 0
        for candidate in partitions[worker_id]:
            path = _candidate_observation_path(scratch, candidate)
            before = (path / "request.json").exists()
            observation = _call_one(scratch, candidate, endpoint, credential_env)
            local[protocol.candidate_path_id(candidate)] = observation
            dispatched += int(not before and bool(observation.get("http_status")))
            failures += int(bool(observation.get("operational_failure")))
        return worker_id, local, {"worker": worker_id, "assigned": len(partitions[worker_id]), "completed": len(local), "dispatched_http": dispatched, "failures": failures, "seconds": time.monotonic() - started}

    with ThreadPoolExecutor(max_workers=WORKERS, thread_name_prefix="oap-007-i") as pool:
        futures = [pool.submit(worker, worker_id) for worker_id in range(WORKERS)]
        for future in futures:
            worker_id, local, status = future.result()
            observations.update(local)
            worker_status[worker_id] = status
    if set(observations) != {protocol.candidate_path_id(item) for item in population}:
        raise ExperimentError("validator observation set is incomplete")
    status = {
        "status": "VALIDATOR_OBSERVATIONS_COMPLETE",
        "scheduled_candidates": len(population),
        "observation_records": len(observations),
        "dispatched_http_requests": sum(item["dispatched_http"] for item in worker_status.values()),
        "protocol_or_operational_failures": sum(item["failures"] for item in worker_status.values()),
        "workers": WORKERS,
        "worker_runtime": worker_status,
    }
    mutable_status(scratch / "RUN-STATUS.json", status)
    immutable_json(scratch / "WORKER-RESULT.json", status)
    return observations, status


def saved_decision_key(decision: Any) -> tuple[int, int, str] | None:
    if isinstance(decision, dict) and isinstance(decision.get("candidate"), dict):
        return candidate_key(decision["candidate"])
    return None


def projection_result(saved: dict[str, Any], edits_to_apply: list[list[Any]], *, only: bool, scheduled: set[tuple[int, int, str]]) -> dict[str, Any]:
    source = saved["input"]
    decisions = []
    calls = []
    for decision in saved.get("decisions", []):
        key = saved_decision_key(decision)
        if only and key in scheduled:
            continue
        decisions.append(decision)
        for name in ("first", "retry"):
            call = decision.get(name)
            if isinstance(call, dict):
                calls.append(call)
    try:
        output = apply_edits(source, [tuple(edit) for edit in edits_to_apply])
        projection_failure = None
    except (AssertionError, TypeError, ValueError) as exc:
        output = source
        edits_to_apply = []
        projection_failure = "DOCUMENT_PATCH_CONFLICT: " + type(exc).__name__
    return {
        "id": saved["id"],
        "index": saved["index"],
        "method": "M2",
        "input": source,
        "input_sha256": saved["input_sha256"],
        "detector": saved["detector"],
        "decisions": decisions,
        "calls": calls,
        "edits": edits_to_apply,
        "output": output,
        "operational_failure": bool(projection_failure),
        "projection_failure": projection_failure,
        "wall_seconds": 0.0,
    }


def make_case_result(
    phase: str,
    case: dict[str, Any],
    candidates: list[dict[str, Any]],
    observations: dict[str, dict[str, Any]],
    configuration_sha: str,
) -> dict[str, Any]:
    saved = case["baseline"]
    sentence = saved["input"]
    scheduled = {candidate_key(item["candidate"]) for item in candidates}
    validator_targets: list[dict[str, Any]] = []
    fallback_edits: list[list[Any]] = []
    only_edits: list[list[Any]] = []
    for candidate in candidates:
        candidate_id = protocol.candidate_path_id(candidate)
        observation = observations[candidate_id]
        decision = protocol.observation_decision(observation)
        attribution = protocol.attribution(sentence, case["dataset"].get("reference"), candidate["mechanical_edit"])
        if decision == "USE_CANDIDATE":
            fallback_edits.append(copy.deepcopy(candidate["mechanical_edit"]))
            only_edits.append(copy.deepcopy(candidate["mechanical_edit"]))
        validator_targets.append(
            {
                "candidate_id": candidate_id,
                "stable_key": list(protocol.stable_key(candidate)),
                "candidate": candidate["candidate"],
                "candidate_form": candidate["candidate_form"],
                "mechanical_edit": candidate["mechanical_edit"],
                "observation": observation,
                "decision": decision,
                "attribution": attribution,
            }
        )
    try:
        fallback = project_saved_case(sentence, saved, fallback_edits)
        fallback_projection = {
            **saved,
            "decisions": fallback["decisions"],
            "calls": fallback["calls"],
            "edits": fallback["edits"],
            "output": fallback["output"],
            "operational_failure": fallback["operational_failure"],
            "wall_seconds": 0.0,
        }
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        fallback_projection = projection_result(saved, [], only=False, scheduled=scheduled)
        fallback_projection["projection_failure"] = "SAVED_FALLBACK_COMPOSITION: " + type(exc).__name__
        fallback_projection["operational_failure"] = True
    only_projection = projection_result(saved, only_edits, only=True, scheduled=scheduled)
    for target in validator_targets:
        target["applied_fallback"] = target["decision"] == "USE_CANDIDATE" and target["mechanical_edit"] in fallback_projection["edits"]
        target["applied_only"] = target["decision"] == "USE_CANDIDATE" and target["mechanical_edit"] in only_projection["edits"]
        if target["decision"] == "USE_CANDIDATE" and not target["applied_fallback"]:
            target["fallback_rollback"] = fallback_projection.get("projection_failure") or bool(fallback_projection.get("operational_failure"))
        if target["decision"] == "USE_CANDIDATE" and not target["applied_only"]:
            target["only_rollback"] = only_projection.get("projection_failure")
    fallback_integrity = protocol.integrity(sentence, fallback_projection["output"], fallback_projection["edits"])
    only_integrity = protocol.integrity(sentence, only_projection["output"], only_projection["edits"])
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "configuration_sha256": configuration_sha,
        "phase": phase,
        "index": case["index"],
        "id": case["id"],
        "dataset": case["dataset"],
        "baseline": saved,
        "validator_targets": validator_targets,
        "validated_fallback": fallback_projection,
        "validated_only": only_projection,
        "integrity": {"validated_fallback": fallback_integrity, "validated_only": only_integrity},
    }


def make_views(
    pairs: dict[str, list[dict[str, Any]]],
    records: dict[str, list[dict[str, Any]]],
    population: list[dict[str, Any]],
    observations: dict[str, dict[str, Any]],
    uv_indices: set[int],
    worker_status: dict[str, Any],
) -> dict[str, Any]:
    by_case = {(record["phase"], record["index"]): record for rows in records.values() for record in rows}
    candidates_by_case: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for candidate in population:
        candidates_by_case.setdefault((candidate["phase"], candidate["case_index"]), []).append(candidate)
    views: dict[str, Any] = {}
    selection_names = {"all": None, "initial_uv": uv_indices, "without_initial_uv": set(range(1, PHASES["dassle-spelling"] + 1)) - uv_indices}

    def one(phase: str, selection_name: str, selected: set[int] | None) -> dict[str, Any]:
        pairs_selected = [pair for pair in pairs[phase] if selected is None or pair["dataset"]["index"] in selected]
        record_selected = [by_case[(phase, pair["dataset"]["index"])] for pair in pairs_selected]
        candidate_selected = [item for item in population if item["phase"] == phase and (selected is None or item["case_index"] in selected)]
        baseline_rows = [row_metrics(pair["dataset"], pair["saved"], "M2") for pair in pairs_selected]
        fallback_rows = [row_metrics(record["dataset"], record["validated_fallback"], "M2") for record in record_selected]
        only_rows = [row_metrics(record["dataset"], record["validated_only"], "M2") for record in record_selected]
        unrestricted_rows = [row_metrics(record["dataset"], record["baseline"], "M2") for record in record_selected]
        outcome = Counter()
        attribution_counts: Counter[str] = Counter()
        attribution_by_decision: dict[str, Counter[str]] = {key: Counter() for key in ("USE_CANDIDATE", "KEEP_ORIGINAL", "UNCERTAIN", "FAILURE")}
        latencies: list[float] = []
        reasoning: list[int] = []
        output_tokens: list[int] = []
        for candidate in candidate_selected:
            target = next(item for item in by_case[(candidate["phase"], candidate["case_index"])] ["validator_targets"] if item["candidate_id"] == protocol.candidate_path_id(candidate))
            decision = target["decision"] or "FAILURE"
            outcome[decision] += 1
            status = target["attribution"]["status"]
            attribution_counts[status] += 1
            attribution_by_decision[decision][status] += 1
            observation = target["observation"]
            if observation.get("http_seconds") is not None:
                latencies.append(float(observation["http_seconds"]))
            if observation.get("reasoning_tokens") is not None:
                reasoning.append(int(observation["reasoning_tokens"]))
            if observation.get("output_tokens") is not None:
                output_tokens.append(int(observation["output_tokens"]))
        def calls(results: list[dict[str, Any]]) -> dict[str, int]:
            return {"first": sum(sum(item.get("kind") == "reviewer" for item in result.get("calls", [])) for result in results), "retry": sum(sum(item.get("kind") == "expression-retry" for item in result.get("calls", [])) for result in results), "total": sum(len(result.get("calls", [])) for result in results)}
        base_calls, fallback_calls, only_calls = calls([pair["saved"] for pair in pairs_selected]), calls([record["validated_fallback"] for record in record_selected]), calls([record["validated_only"] for record in record_selected])
        def accounting(projected: dict[str, int]) -> dict[str, Any]:
            added = len(candidate_selected)
            return {"baseline": base_calls, "projected_baseline": projected, "ordinary_avoided": {key: base_calls[key] - projected[key] for key in ("first", "retry", "total")}, "validator_calls_added": added, "projected_total_with_validator": projected["total"] + added, "delta_vs_baseline": projected["total"] + added - base_calls["total"], "delta_vs_007h": projected["total"] + added - base_calls["total"]}
        exact_total = attribution_counts["exact_reference"]
        use_exact = attribution_by_decision["USE_CANDIDATE"]["exact_reference"]
        valid_responses = sum(outcome[key] for key in ("USE_CANDIDATE", "KEEP_ORIGINAL", "UNCERTAIN"))
        preserved_rejections = len(candidate_selected) - outcome["USE_CANDIDATE"] if phase == "dassle-spelling-preservation" else None
        return {
            "rows": len(pairs_selected),
            "scheduled_candidates": len(candidate_selected),
            "validator": {"decision_counts": dict(outcome), "valid_response_count": valid_responses, "unconditional_acceptance_rate": outcome["USE_CANDIDATE"] / len(candidate_selected) if candidate_selected else None, "valid_response_acceptance_rate": outcome["USE_CANDIDATE"] / valid_responses if valid_responses else None, "attribution": dict(attribution_counts), "attribution_by_decision": {key: dict(value) for key, value in attribution_by_decision.items()}, "known_good_reference_exact_sensitivity": {"numerator": use_exact, "denominator": exact_total, "value": use_exact / exact_total if exact_total else None}, "preservation_candidate_rejection_rate": {"numerator": preserved_rejections, "denominator": len(candidate_selected), "value": preserved_rejections / len(candidate_selected) if preserved_rejections is not None and candidate_selected else None}},
            "baseline": summarize(baseline_rows),
            "unrestricted_007h": summarize(unrestricted_rows),
            "validated_fallback": summarize(fallback_rows),
            "validated_only": summarize(only_rows),
            "call_accounting": {"validated_fallback": accounting(fallback_calls), "validated_only": accounting(only_calls)},
            "integrity": {"validated_fallback": {"protected_differences": sum(record["integrity"]["validated_fallback"]["protected_differences"] for record in record_selected), "outside_span_differences": sum(record["integrity"]["validated_fallback"]["outside_span_differences"] for record in record_selected)}, "validated_only": {"protected_differences": sum(record["integrity"]["validated_only"]["protected_differences"] for record in record_selected), "outside_span_differences": sum(record["integrity"]["validated_only"]["outside_span_differences"] for record in record_selected)}},
            "preservation_changed": {"validated_fallback_cases": sum(row["changed"] for row in fallback_rows), "validated_fallback_edit_units": sum(row["introduced_edits"] for row in fallback_rows), "validated_only_cases": sum(row["changed"] for row in only_rows), "validated_only_edit_units": sum(row["introduced_edits"] for row in only_rows)} if phase == "dassle-spelling-preservation" else None,
            "validator_latency_seconds": protocol.distribution(latencies),
            "reasoning_tokens": protocol.distribution(reasoning),
            "output_tokens": protocol.distribution(output_tokens),
        }

    for phase in PHASES:
        phase_views = {"all": one(phase, "all", None)}
        if phase == "dassle-spelling":
            phase_views["initial_uv"] = one(phase, "initial_uv", uv_indices)
            phase_views["without_initial_uv"] = one(phase, "without_initial_uv", selection_names["without_initial_uv"])
        views[phase] = phase_views
    return {"views": views, "worker_runtime": worker_status, "actual_validator_call_records": len(population), "dispatched_http_requests": worker_status.get("dispatched_http_requests", 0)}


def aggregate(
    scratch: Path,
    prepared: dict[str, Any],
    observations: dict[str, dict[str, Any]],
    worker_status: dict[str, Any],
) -> dict[str, Any]:
    configuration_sha = prepared["configuration_sha256"]
    records: dict[str, list[dict[str, Any]]] = {}
    candidates_by_case: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for candidate in prepared["population"]:
        candidates_by_case.setdefault((candidate["phase"], candidate["case_index"]), []).append(candidate)
    for phase, cases in prepared["case_records"].items():
        records[phase] = []
        for case in cases:
            case_candidates = candidates_by_case.get((phase, case["index"]), [])
            records[phase].append(make_case_result(phase, case, case_candidates, observations, configuration_sha))
    metrics = make_views(prepared["pairs"], records, prepared["population"], observations, prepared["uv_indices"], worker_status)
    result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "configuration_sha256": configuration_sha, "candidate_manifest_sha256": prepared["configuration"]["source_identity"]["candidate_manifest_sha256"], "case_identity_manifest_sha256": prepared["configuration"]["source_identity"]["case_identity_manifest_sha256"], "metrics": metrics, "status": "COMPLETE" if worker_status.get("dispatched_http_requests", 0) == EXPECTED_TOTAL else "PARTIAL_SYSTEMIC_VALIDATOR_FAILURE"}
    immutable_json(scratch / "CASE-RESULTS.json", records)
    private_results_sha = immutable_json(scratch / "RESULTS.json", result)
    private_manifest = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "configuration_sha256": configuration_sha,
        "candidate_manifest_sha256": result["candidate_manifest_sha256"],
        "case_identity_manifest_sha256": result["case_identity_manifest_sha256"],
        "case_count": 2_973,
        "candidate_count": EXPECTED_TOTAL,
        "private_results_sha256": private_results_sha,
        "request_record_count": len(observations),
        "status": result["status"],
    }
    private_manifest_sha = immutable_json(scratch / "MANIFEST.json", private_manifest)
    private_report = "# Private 007-i report\n\n" + json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    private_report_sha = immutable_write(scratch / "REPORT.md", private_report.encode("utf-8"))
    mutable_status(scratch / "RUN-STATUS.json", {"status": result["status"], "run_id": RUN_ID, "configuration_sha256": configuration_sha, "candidate_manifest_sha256": result["candidate_manifest_sha256"], "private_results_sha256": private_results_sha, "private_manifest_sha256": private_manifest_sha, "scheduled_candidates": EXPECTED_TOTAL, "observation_records": len(observations), "dispatched_http_requests": worker_status.get("dispatched_http_requests", 0)})
    result["private_results_sha256"] = private_results_sha
    result["private_manifest_sha256"] = private_manifest_sha
    result["private_report_sha256"] = private_report_sha
    return result


def public_projection(configuration: dict[str, Any], result: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    public_config = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "status": result["status"],
        "implementation_head": configuration["implementation_head"],
        "prior_007h_head": configuration["prior_007h_head"],
        "question": "Can one frozen contextual Qwen validator improve unique one-letter candidate selection without resampling baseline responses?",
        "source_identity": {key: value for key, value in configuration["source_identity"].items() if key != "uv_indices_sha256" or True},
        "prompt": {"sha256": FROZEN_PROMPT_SHA256, "template": "owner-supplied frozen 007-i prompt"},
        "deployment": {"class": "A100-FP8", "model": MODEL, "protocol": "Responses non-streaming", "profile_sha256": FROZEN_PROFILE_SHA256, "endpoint": "private endpoint identity omitted"},
        "request": configuration["request"],
        "parser": configuration["parser"],
        "scheduling": configuration["scheduling"],
        "limits": configuration["limits"],
        "projections": configuration["projections"],
        "actual": {"scheduled_candidates": EXPECTED_TOTAL, "validator_call_records": result["metrics"]["actual_validator_call_records"], "dispatched_http_requests": result["metrics"].get("dispatched_http_requests", 0)},
        "private_evidence_sha256": {"results": result["private_results_sha256"], "manifest": result["private_manifest_sha256"]},
    }
    public_result = {"schema_version": 1, "experiment_id": EXPERIMENT_ID, "status": result["status"], "implementation_head": configuration["implementation_head"], "configuration_sha256": sha256_bytes(canonical_bytes(public_config)), "private_evidence_sha256": public_config["private_evidence_sha256"], "metrics": result["metrics"], "limitations": ["This is an owner-authorized frozen experiment, not a product or linguistic acceptance claim.", "Reference-token attribution is mechanical and non-reference edits are not semantic harm labels.", "Validator failures and UNCERTAIN conservatively reject candidates; no validator retry or baseline resampling occurs.", "Live service availability and inherited repository checks remain separate evidence."]}
    return public_config, public_result


def public_report(result: dict[str, Any], public_config: dict[str, Any]) -> str:
    lines = [
        "# 007-i contextual validator",
        "",
        "EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.",
        "",
        "One owner-authorized paired contextual validator experiment over frozen 007-h candidates.",
        "No baseline response was resampled; both projections consume the same validator observation.",
        "",
        "## Frozen identity",
        "",
        f"- Scheduled unique candidates: {EXPECTED_TOTAL} (571 spelling; 164 preservation).",
        f"- Implementation head: {public_config['implementation_head']}.",
        f"- Candidate manifest SHA-256: {public_config['source_identity']['candidate_manifest_sha256']}.",
        f"- Prompt SHA-256: {FROZEN_PROMPT_SHA256}.",
        f"- Actual validator call records / dispatched HTTP requests: {result['metrics']['actual_validator_call_records']} / {result['metrics'].get('dispatched_http_requests', 0)}.",
        "",
        "## Required views",
        "",
    ]
    for phase, phase_views in result["metrics"]["views"].items():
        for name, view in phase_views.items():
            validator = view["validator"]
            lines += [
                f"### {phase} / {name}",
                f"- Rows / scheduled candidates: {view['rows']} / {view['scheduled_candidates']}.",
                f"- Validator decisions USE / KEEP / UNCERTAIN / FAILURE: {validator['decision_counts'].get('USE_CANDIDATE', 0)} / {validator['decision_counts'].get('KEEP_ORIGINAL', 0)} / {validator['decision_counts'].get('UNCERTAIN', 0)} / {validator['decision_counts'].get('FAILURE', 0)}.",
                f"- Unconditional / valid-response acceptance: {validator['unconditional_acceptance_rate']} / {validator['valid_response_acceptance_rate']}.",
                f"- Reference-exact sensitivity (numerator / denominator): {validator['known_good_reference_exact_sensitivity']['numerator']} / {validator['known_good_reference_exact_sensitivity']['denominator']} = {validator['known_good_reference_exact_sensitivity']['value']}.",
                f"- Baseline TP/FP/FN: {view['baseline']['tp']} / {view['baseline']['fp']} / {view['baseline']['fn']}.",
                f"- VALIDATED+FALLBACK TP/FP/FN: {view['validated_fallback']['tp']} / {view['validated_fallback']['fp']} / {view['validated_fallback']['fn']}.",
                f"- VALIDATED-ONLY TP/FP/FN: {view['validated_only']['tp']} / {view['validated_only']['fp']} / {view['validated_only']['fn']}.",
                f"- Baseline / fallback / only precision: {view['baseline']['precision']} / {view['validated_fallback']['precision']} / {view['validated_only']['precision']}.",
                f"- Baseline / fallback / only recall: {view['baseline']['recall']} / {view['validated_fallback']['recall']} / {view['validated_only']['recall']}.",
                f"- Fallback call accounting (baseline, retained, validator-added, net): {view['call_accounting']['validated_fallback']['baseline']['total']} / {view['call_accounting']['validated_fallback']['projected_baseline']['total']} / {view['call_accounting']['validated_fallback']['validator_calls_added']} / {view['call_accounting']['validated_fallback']['projected_total_with_validator']}.",
                f"- Only call accounting (baseline, retained, validator-added, net): {view['call_accounting']['validated_only']['baseline']['total']} / {view['call_accounting']['validated_only']['projected_baseline']['total']} / {view['call_accounting']['validated_only']['validator_calls_added']} / {view['call_accounting']['validated_only']['projected_total_with_validator']}.",
                f"- Protected/outside differences fallback: {view['integrity']['validated_fallback']['protected_differences']} / {view['integrity']['validated_fallback']['outside_span_differences']}.",
                f"- Protected/outside differences only: {view['integrity']['validated_only']['protected_differences']} / {view['integrity']['validated_only']['outside_span_differences']}.",
                "",
            ]
    lines += [
        "## Runtime and limitations",
        "",
        f"- Validator latency seconds (n / median / p95 / max): {result['metrics']['views']['dassle-spelling']['all']['validator_latency_seconds']['n']} / {result['metrics']['views']['dassle-spelling']['all']['validator_latency_seconds']['median']} / {result['metrics']['views']['dassle-spelling']['all']['validator_latency_seconds']['p95']} / {result['metrics']['views']['dassle-spelling']['all']['validator_latency_seconds']['max']}.",
        f"- Worker count: {WORKERS}; at most one in-flight call per worker.",
        "- The validator is a strict binary choice protocol. Extra text, malformed JSON, wrong model/effort, incomplete status, missing token accounting, timeout, or transport failure is a distinct conservative failure.",
        "- Reference scoring can penalize valid alternatives. Non-reference changes are not semantic harm labels.",
        "- This result does not authorize integration, merge, release, deployment, or product linguistic acceptance.",
    ]
    return "\n".join(lines) + "\n"


def write_public(repo_root: Path, configuration: dict[str, Any], result: dict[str, Any]) -> dict[str, str]:
    public_config, public_result = public_projection(configuration, result)
    paths = {
        "config": repo_root / "research/configs/007-i-contextual-validator.json",
        "result": repo_root / "research/results/007-i-contextual-validator.json.gz",
        "report": repo_root / "research/reports/007-i-contextual-validator.md",
    }
    immutable_write(paths["config"], canonical_bytes(public_config))
    immutable_write(paths["result"], gzip.compress(canonical_bytes(public_result), mtime=0))
    immutable_write(paths["report"], public_report(result, public_config).encode("utf-8"))
    return {key: sha256_file(path) for key, path in paths.items()}


def run(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    scratch = Path(args.scratch).resolve()
    if args.prepare_only or not (scratch / "CONFIGURATION.json").exists():
        if not args.source_root:
            raise ExperimentError("initial preparation requires the frozen 007-h source root")
        prepared = prepare(repo_root, scratch, Path(args.source_root).resolve(), args.expected_implementation_head)
    else:
        prepared = load_prepared(scratch, args.expected_implementation_head)
    if args.prepare_only:
        return {"status": "FROZEN_BEFORE_LIVE_EXECUTION", "configuration_sha256": prepared["configuration_sha256"], "candidate_manifest_sha256": prepared["candidate_manifest_sha256"], "scheduled_candidates": EXPECTED_TOTAL, "actual_model_calls": 0, "actual_network_calls": 0}
    existing_status = read_json(scratch / "RUN-STATUS.json") if (scratch / "RUN-STATUS.json").exists() else {}
    if existing_status.get("status") in {"COMPLETE", "PARTIAL_SYSTEMIC_VALIDATOR_FAILURE"} and (scratch / "RESULTS.json").exists():
        result = read_json(scratch / "RESULTS.json")
        paths = write_public(repo_root, prepared["configuration"], result)
        return {"status": result["status"], "configuration_sha256": prepared["configuration_sha256"], "private_results_sha256": result.get("private_results_sha256"), "private_manifest_sha256": result.get("private_manifest_sha256"), "public": paths, "actual_model_calls": result["metrics"]["actual_validator_call_records"], "actual_network_calls": result["metrics"].get("dispatched_http_requests", 0)}
    observations, worker_status = execute_validator(scratch, prepared["population"], endpoint=args.endpoint, credential_env=args.credential_env)
    result = aggregate(scratch, prepared, observations, worker_status)
    paths = write_public(repo_root, prepared["configuration"], result)
    return {"status": result["status"], "configuration_sha256": prepared["configuration_sha256"], "private_results_sha256": result["private_results_sha256"], "private_manifest_sha256": result["private_manifest_sha256"], "public": paths, "scheduled_candidates": EXPECTED_TOTAL, "actual_model_calls": result["metrics"]["actual_validator_call_records"], "actual_network_calls": result["metrics"].get("dispatched_http_requests", 0)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--expected-implementation-head", required=True)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--endpoint")
    parser.add_argument("--credential-env")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(run(args), sort_keys=True))
    except (ExperimentError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "reason": str(exc)}, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
