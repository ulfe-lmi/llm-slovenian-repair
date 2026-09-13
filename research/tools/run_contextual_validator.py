"""Run the owner-authorized 007-i contextual validator experiment.

Preparation copies only the frozen 007-h inputs into an explicitly supplied
native private root.  Live execution is opt-in and uses no default endpoint.
Every request, bounded raw response, and parsed observation is immutable; the
two projections are aggregated only from those same observations.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import shutil
import stat
import subprocess
import time
import urllib.parse
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
FROZEN_LIVE_HEAD = "e85600ffd91164440166ee33a20c3b84af50bfe6"
FROZEN_LIVE_CONFIGURATION_SHA256 = (
    "0cbc4738f23bed247fac6a3cd2203086956329eea9ca23ffb8bf8e1351165d21"
)
FROZEN_REQUEST_TREE_FILE_COUNT = 2_940
FROZEN_REQUEST_TREE_TOTAL_BYTES = 4_651_774
FROZEN_REQUEST_TREE_MANIFEST_SHA256 = (
    "d46b47754e2ba158ea099bfe556a84164e534610233426819d9114a455aea945"
)
FROZEN_CANDIDATE_MANIFEST_SHA256 = (
    "70544b1dec158f1e72cfaae8fb2547d9ba6ea22c3cd7934e0b7341bce8617854"
)


class ExperimentError(RuntimeError):
    """Raised when a frozen input, protocol, or publication boundary fails."""


def canonical_bytes(value: object) -> bytes:
    return protocol.canonical_bytes(value)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return protocol.sha256_file(path)


def request_tree_identity(request_root: Path) -> dict[str, Any]:
    """Hash every persisted request artifact using deterministic sha256sum lines."""
    require_owned_dir(request_root)
    files: list[tuple[str, int, str]] = []
    for path in sorted(
        request_root.rglob("*"), key=lambda item: item.relative_to(request_root).as_posix()
    ):
        if path.is_symlink():
            raise ExperimentError(f"request tree contains symlink: {path.name}")
        if path.is_dir():
            require_owned_dir(path)
            continue
        if not path.is_file():
            raise ExperimentError(f"request tree contains unsupported type: {path.name}")
        require_private_file(path)
        relative = path.relative_to(request_root).as_posix()
        files.append((relative, path.stat().st_size, sha256_file(path)))
    manifest = "".join(f"{digest}  ./{relative}\n" for relative, _, digest in files)
    return {
        "file_count": len(files),
        "total_bytes": sum(size for _, size, _ in files),
        "sha256sum_manifest_sha256": sha256_bytes(manifest.encode("utf-8")),
    }


def verify_frozen_request_tree(request_root: Path) -> dict[str, Any]:
    identity = request_tree_identity(request_root)
    if identity != {
        "file_count": FROZEN_REQUEST_TREE_FILE_COUNT,
        "total_bytes": FROZEN_REQUEST_TREE_TOTAL_BYTES,
        "sha256sum_manifest_sha256": FROZEN_REQUEST_TREE_MANIFEST_SHA256,
    }:
        raise ExperimentError("frozen request tree identity changed")
    return identity


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
        raise ExperimentError(f"private directory mode mismatch: {path.name}")


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


def require_private_file(path: Path, *, expected_sha: str | None = None) -> None:
    require_owned_file(path, expected_sha=expected_sha)
    try:
        mode = stat.S_IMODE(path.stat().st_mode)
    except OSError as exc:
        raise ExperimentError(f"private file is unavailable: {path.name}") from exc
    if mode != 0o600:
        raise ExperimentError(f"private file mode mismatch: {path.name}")


def immutable_write(path: Path, data: bytes) -> str:
    """Write a private immutable artifact with strict directory/file modes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    require_owned_dir(path.parent)
    if path.is_symlink():
        raise ExperimentError(f"refusing symlink artifact: {path.name}")
    if path.exists():
        require_private_file(path)
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
    require_private_file(path)
    return sha256_bytes(data)


def immutable_json(path: Path, value: object) -> str:
    return immutable_write(path, canonical_bytes(value))


def public_immutable_write(path: Path, data: bytes) -> str:
    """Write a public repository artifact without changing repository modes."""
    if path.is_symlink():
        raise ExperimentError(f"refusing symlink public artifact: {path.name}")
    if path.exists():
        if not path.is_file() or path.read_bytes() != data:
            raise ExperimentError(f"public artifact conflict: {path.name}")
        return sha256_bytes(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name("." + path.name + ".public")
    if temporary.exists() or temporary.is_symlink():
        raise ExperimentError(f"public temporary artifact collision: {temporary.name}")
    temporary.write_bytes(data)
    os.chmod(temporary, 0o644)
    os.replace(temporary, path)
    return sha256_bytes(data)


def mutable_status(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    require_owned_dir(path.parent)
    if path.is_symlink():
        raise ExperimentError(f"refusing symlink status: {path.name}")
    if path.exists():
        require_private_file(path)
    temporary = path.with_name("." + path.name + ".pointer")
    temporary.write_bytes(canonical_bytes(value))
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)
    os.chmod(path, 0o600)
    require_private_file(path)


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
    destination.mkdir(parents=True, exist_ok=True, mode=0o700)
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
    scratch.mkdir(parents=True, exist_ok=True, mode=0o700)
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


def profile_identity(profile_path: Path) -> dict[str, str]:
    """Freeze the private profile path and verify the owner-supplied profile hash."""
    require_owned_file(profile_path)
    actual_sha = sha256_file(profile_path)
    if actual_sha != FROZEN_PROFILE_SHA256:
        raise ExperimentError("A100 profile SHA-256 does not match the frozen profile")
    return {"path": str(profile_path), "sha256": actual_sha}


def validate_freeze_inputs(
    endpoint: str | None,
    profile_path: Path | None,
    credential_env: str | None,
) -> dict[str, Any]:
    """Validate all explicit private deployment inputs before preparation/live work."""
    if not endpoint or not profile_path or not credential_env:
        raise ExperimentError(
            "explicit endpoint, profile path, and credential environment are required"
        )
    parsed = urllib.parse.urlsplit(endpoint)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        raise ExperimentError("endpoint must be an explicit credential-free HTTP(S) URL")
    if not credential_env.replace("_", "a").isalnum() or credential_env[0].isdigit():
        raise ExperimentError("credential environment name is malformed")
    if not os.environ.get(credential_env):
        raise ExperimentError("credential environment value is missing")
    identity = profile_identity(profile_path.absolute())
    return {"endpoint": endpoint, "profile": identity, "credential_env": credential_env}


def load_frozen_state(
    scratch: Path,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any], set[int], dict[str, Any], str]:
    prior.verify_frozen_inputs(scratch)
    pairs = prior.load_pairs(scratch)
    baseline = prior.validate_baseline_replay(pairs)
    uv_indices, _uv_mapping = prior.verify_uv_mapping(scratch, pairs["dassle-spelling"])
    frozen_records, case_digest, total_bytes = prior.frozen_case_manifest(
        scratch, pairs, prior.FROZEN_CONFIGURATION_SHA256
    )
    for phase_records in frozen_records.values():
        for case in phase_records:
            unrestricted = case.get("new")
            if not isinstance(unrestricted, dict):
                raise ExperimentError("007-h unrestricted case result is missing")
            if unrestricted.get("input") != case["baseline"].get("input"):
                raise ExperimentError("007-h unrestricted input identity changed")
            if not isinstance(unrestricted.get("output"), str) or not isinstance(
                unrestricted.get("operational_failure"), bool
            ):
                raise ExperimentError("007-h unrestricted result schema is invalid")
            try:
                prior.call_counts(unrestricted)
            except ExperimentError as exc:
                raise ExperimentError("007-h unrestricted call identity is invalid") from exc
    if case_digest != FROZEN_7H_CASE_MANIFEST or total_bytes != prior.FROZEN_CASE_BYTES:
        raise ExperimentError("007-h case identity does not match the frozen order")
    if sum(len(rows) for rows in pairs.values()) != 2_973:
        raise ExperimentError("007-h population is not 2,973 rows")
    return pairs, baseline, uv_indices, frozen_records, case_digest


def build_population(
    records_by_phase: dict[str, list[dict[str, Any]]],
    vocabulary: set[str],
    buckets: dict[int, list[str]],
    *,
    qualifier=qualifying_candidates,
    expected_counts: dict[str, int] | None = None,
    expected_total: int | None = None,
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
                if (
                    not isinstance(candidate, dict)
                    or not isinstance(forms, list)
                    or len(forms) != 1
                    or not isinstance(forms[0], str)
                ):
                    raise ExperimentError("007-h unique target schema is invalid")
                start, end, text = (
                    candidate.get("start"),
                    candidate.get("end"),
                    candidate.get("text"),
                )
                if type(start) is not int or type(end) is not int or not isinstance(text, str):
                    raise ExperimentError("007-h candidate coordinates are invalid")
                if baseline["input"][start:end] != text:
                    raise ExperimentError("007-h candidate coordinate is stale")
                lookup_form = text.casefold()
                actual = qualifier(lookup_form, buckets.get(len(lookup_form), ()))
                if actual != forms:
                    raise ExperimentError("007-h candidate-generation drift")
                if len(actual) != 1:
                    raise ExperimentError("007-h unique candidate cardinality drift")
                recomputed = mechanical_substitution(
                    baseline["input"], candidate, actual[0], vocabulary
                )
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
    expected_counts = EXPECTED_CANDIDATES if expected_counts is None else expected_counts
    expected_total = EXPECTED_TOTAL if expected_total is None else expected_total
    if dict(counts) != expected_counts or len(population) != expected_total:
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
    deployment: dict[str, Any],
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
            "uv_indices_sha256": sha256_bytes(
                ("\n".join(str(item) for item in sorted(uv_indices)) + "\n").encode()
            ),
        },
        "prior_007h_identity": {
            "implementation_head": FROZEN_7H_IMPLEMENTATION_HEAD,
            "configuration_sha256": FROZEN_7H_CONFIGURATION,
            "case_identity_manifest_sha256": FROZEN_7H_CASE_MANIFEST,
            "baseline": baseline,
        },
        "code_identity": {"sha256": code_paths, "head_blobs": implementation["head_blobs"]},
        "prompt": {
            "sha256": FROZEN_PROMPT_SHA256,
            "template": "owner-supplied 007-i validator prompt",
        },
        "deployment": {
            "class": "A100-FP8",
            "model": MODEL,
            "profile_sha256": FROZEN_PROFILE_SHA256,
            "endpoint": deployment["endpoint"],
            "profile_path": deployment["profile"]["path"],
            "credential_env": deployment["credential_env"],
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
            "partition_key": [
                "phase",
                "case_index",
                "target_start",
                "target_end",
                "target_ordinal",
            ],
            "partition": "stable ordered position modulo worker count",
            "in_flight_per_worker": 1,
            "maximum_in_flight": WORKERS,
            "scheduled_candidates": len(population),
        },
        "limits": {
            "timeout_seconds": protocol.TIMEOUT_SECONDS,
            "response_bound_bytes": protocol.MAX_RESPONSE_BYTES,
            "attempts_per_candidate": 1,
            "resampling": False,
        },
        "persistence": {
            "order": ["request bytes", "bounded raw response/timing", "parsed observation"],
            "interrupted_request": "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE",
            "immutable_completed_observations": True,
        },
        "projections": {
            "validated_fallback": (
                "USE_CANDIDATE mechanical edit; every other decision uses "
                "saved 007-h baseline fallback"
            ),
            "validated_only": (
                "USE_CANDIDATE mechanical edit; every other decision leaves original target"
            ),
            "shared_observation": True,
            "baseline_calls_resampled": False,
        },
        "scorer": {
            "implementation_head": FROZEN_7H_IMPLEMENTATION_HEAD,
            "attribution": "unchanged token-coordinate 007-h scorer",
        },
        "privacy": {
            "public": "aggregate metrics, hashes, limitations only",
            "private": (
                "filled prompts, sentences, targets, responses, credentials and "
                "endpoint/profile values"
            ),
        },
        "no_tuning_or_resampling": True,
        "private_evidence_root": str(scratch),
    }


def prepare(
    repo_root: Path,
    scratch: Path,
    source_root: Path,
    expected_head: str,
    *,
    endpoint: str,
    profile_path: Path,
    credential_env: str,
) -> dict[str, Any]:
    deployment = validate_freeze_inputs(endpoint, profile_path, credential_env)
    if protocol.prompt_sha256() != FROZEN_PROMPT_SHA256:
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
        repo_root,
        scratch,
        implementation,
        case_digest,
        baseline,
        uv_indices,
        population,
        candidate_digest,
        deployment,
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
    return {
        "configuration": configuration,
        "configuration_sha256": configuration_sha,
        "population": population,
        "pairs": pairs,
        "baseline": baseline,
        "uv_indices": uv_indices,
        "case_records": frozen_records,
        "candidate_manifest_sha256": candidate_digest,
    }


def load_prepared(
    scratch: Path,
    expected_head: str | None = None,
    *,
    endpoint: str | None = None,
    profile_path: Path | None = None,
    credential_env: str | None = None,
) -> dict[str, Any]:
    require_owned_dir(scratch)
    require_private_file(scratch / "CONFIGURATION.json")
    configuration = read_json(scratch / "CONFIGURATION.json")
    if not isinstance(configuration, dict) or configuration.get("experiment_id") != EXPERIMENT_ID:
        raise ExperimentError("prepared configuration identity mismatch")
    if expected_head and configuration.get("implementation_head") != expected_head:
        raise ExperimentError("prepared implementation head mismatch")
    deployment = configuration.get("deployment")
    if not isinstance(deployment, dict):
        raise ExperimentError("prepared deployment identity is missing")
    supplied = validate_freeze_inputs(endpoint, profile_path, credential_env)
    if (
        deployment.get("endpoint") != supplied["endpoint"]
        or deployment.get("profile_path") != supplied["profile"]["path"]
        or deployment.get("profile_sha256") != supplied["profile"]["sha256"]
        or deployment.get("credential_env") != supplied["credential_env"]
    ):
        raise ExperimentError("prepared deployment identity does not match explicit resume inputs")
    require_private_file(scratch / "CANDIDATE-MANIFEST.json")
    require_private_file(scratch / "CANDIDATES.json")
    manifest = read_json(scratch / "CANDIDATE-MANIFEST.json")
    population = read_json(scratch / "CANDIDATES.json")
    if not isinstance(manifest, list) or not isinstance(population, list):
        raise ExperimentError("prepared candidate manifest is malformed")
    recomputed_manifest, recomputed_digest = protocol.candidate_manifest(population)
    if (
        recomputed_digest != configuration["source_identity"]["candidate_manifest_sha256"]
        or manifest != recomputed_manifest
    ):
        raise ExperimentError("prepared candidate manifest hash mismatch")
    pairs, baseline, uv_indices, case_records, case_digest = load_frozen_state(scratch)
    if case_digest != configuration["source_identity"]["case_identity_manifest_sha256"]:
        raise ExperimentError("prepared case identity mismatch")
    return {
        "configuration": configuration,
        "configuration_sha256": sha256_file(scratch / "CONFIGURATION.json"),
        "population": protocol.ordered_candidates(population),
        "pairs": pairs,
        "baseline": baseline,
        "uv_indices": uv_indices,
        "case_records": case_records,
        "candidate_manifest": manifest,
    }


def verify_aggregation_head(
    repo_root: Path, live_head: str, aggregation_head: str
) -> dict[str, str]:
    """Require a distinct, clean local branch head for offline aggregation."""
    if live_head != FROZEN_LIVE_HEAD:
        raise ExperimentError("frozen live implementation head mismatch")
    if (
        len(aggregation_head) != 40
        or aggregation_head != aggregation_head.lower()
        or any(character not in "0123456789abcdef" for character in aggregation_head)
    ):
        raise ExperimentError("aggregation head must be a full lowercase commit SHA")
    try:
        current_head = subprocess.run(
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
        raise ExperimentError("aggregation Git identity cannot be read") from exc
    if current_head != aggregation_head:
        raise ExperimentError("aggregation head is not the current branch head")
    if current_head == live_head:
        raise ExperimentError("aggregation head must differ from frozen live head")
    if branch != "oap/007-concept-verification":
        raise ExperimentError("aggregation branch is not the active objective branch")
    if status:
        raise ExperimentError("aggregation branch must be clean")
    return {
        "live_implementation_head": live_head,
        "aggregation_implementation_head": aggregation_head,
        "implementation_branch": branch,
        "working_tree": "clean",
    }


def load_aggregation_prepared(scratch: Path, expected_live_head: str) -> dict[str, Any]:
    """Load frozen inputs for recovery without validating or touching live inputs."""
    require_owned_dir(scratch)
    require_private_file(scratch / "CONFIGURATION.json")
    configuration = read_json(scratch / "CONFIGURATION.json")
    if not isinstance(configuration, dict) or configuration.get("experiment_id") != EXPERIMENT_ID:
        raise ExperimentError("prepared configuration identity mismatch")
    if expected_live_head != FROZEN_LIVE_HEAD:
        raise ExperimentError("recovery live head is not the frozen live head")
    if configuration.get("implementation_head") != expected_live_head:
        raise ExperimentError("frozen configuration live head mismatch")
    if sha256_file(scratch / "CONFIGURATION.json") != FROZEN_LIVE_CONFIGURATION_SHA256:
        raise ExperimentError("frozen configuration bytes changed")
    if configuration.get("status") != "FROZEN_BEFORE_LIVE_EXECUTION":
        raise ExperimentError("frozen configuration status changed")
    require_private_file(scratch / "CANDIDATE-MANIFEST.json")
    require_private_file(scratch / "CANDIDATES.json")
    manifest = read_json(scratch / "CANDIDATE-MANIFEST.json")
    population = read_json(scratch / "CANDIDATES.json")
    if not isinstance(manifest, list) or not isinstance(population, list):
        raise ExperimentError("prepared candidate manifest is malformed")
    recomputed_manifest, recomputed_digest = protocol.candidate_manifest(population)
    if (
        recomputed_digest != configuration["source_identity"]["candidate_manifest_sha256"]
        or manifest != recomputed_manifest
        or len(population) != EXPECTED_TOTAL
    ):
        raise ExperimentError("prepared candidate manifest hash mismatch")
    pairs, baseline, uv_indices, case_records, case_digest = load_frozen_state(scratch)
    if case_digest != configuration["source_identity"]["case_identity_manifest_sha256"]:
        raise ExperimentError("prepared case identity mismatch")
    require_private_file(scratch / "RUN-STATUS.json")
    status = read_json(scratch / "RUN-STATUS.json")
    if (
        not isinstance(status, dict)
        or status.get("status") != "VALIDATOR_OBSERVATIONS_COMPLETE"
        or status.get("scheduled_candidates") != EXPECTED_TOTAL
        or status.get("observation_records") != EXPECTED_TOTAL
        or status.get("dispatched_http_requests") != EXPECTED_TOTAL
        or status.get("uncertain_deliveries") != 0
    ):
        raise ExperimentError("validator observations are not in the frozen complete state")
    for name in ("CASE-RESULTS.json", "RESULTS.json", "MANIFEST.json", "REPORT.md"):
        if (scratch / name).exists() or (scratch / name).is_symlink():
            raise ExperimentError(f"private aggregate output already exists: {name}")
    return {
        "configuration": configuration,
        "configuration_sha256": FROZEN_LIVE_CONFIGURATION_SHA256,
        "population": protocol.ordered_candidates(population),
        "pairs": pairs,
        "baseline": baseline,
        "uv_indices": uv_indices,
        "case_records": case_records,
        "candidate_manifest": manifest,
        "worker_status": status,
    }


def load_completed_observations(
    scratch: Path, population: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Read completed observations and prove each request record is unchanged."""
    request_root = scratch / "requests"
    require_owned_dir(request_root)
    expected_ids = {protocol.candidate_path_id(candidate) for candidate in population}
    actual_dirs: set[str] = set()
    for path in request_root.iterdir():
        if path.is_symlink() or not path.is_dir():
            raise ExperimentError("request tree contains an unexpected entry")
        require_owned_dir(path)
        actual_dirs.add(path.name)
    if actual_dirs != expected_ids:
        raise ExperimentError("persisted request directories do not match candidates")
    observations: dict[str, dict[str, Any]] = {}
    for candidate in population:
        candidate_id = protocol.candidate_path_id(candidate)
        directory = request_root / candidate_id
        expected_names = {"request.json", "dispatch.json", "raw-response.json", "observation.json"}
        names = {path.name for path in directory.iterdir()}
        if names != expected_names:
            raise ExperimentError(f"persisted observation file set is invalid: {candidate_id}")
        for name in expected_names:
            require_private_file(directory / name)
        body = protocol.request_body(
            candidate["sentence"], candidate["candidate"]["text"], candidate["mechanical_edit"][2]
        )
        request_bytes = canonical_bytes(body)
        request_path = directory / "request.json"
        if request_path.read_bytes() != request_bytes:
            raise ExperimentError(f"persisted request bytes changed: {candidate_id}")
        dispatch = read_json(directory / "dispatch.json")
        raw = read_json(directory / "raw-response.json")
        observation = read_json(directory / "observation.json")
        if not all(
            isinstance(value, dict) for value in (dispatch, raw, observation)
        ):
            raise ExperimentError(f"persisted observation JSON is malformed: {candidate_id}")
        if (
            dispatch.get("dispatch") != "ATTEMPTED"
            or raw.get("dispatch") != "ATTEMPTED"
            or observation.get("dispatch") != "ATTEMPTED"
            or observation.get("request_sha256") != sha256_bytes(request_bytes)
            or observation.get("response_sha256") != sha256_file(directory / "raw-response.json")
        ):
            raise ExperimentError(f"persisted observation identity is invalid: {candidate_id}")
        observations[candidate_id] = observation
    if len(observations) != EXPECTED_TOTAL:
        raise ExperimentError("persisted observation count is not 735")
    return observations


def write_aggregation_incident(scratch: Path) -> str:
    incident = {
        "schema_version": 1,
        "run_id": RUN_ID,
        "status": "AGGREGATION_EVALUATION_ORDER_FAILURE",
        "stage": "make_views",
        "exception_class": "KeyError",
        "exception_message": "valid_response_count",
        "live_implementation_head": FROZEN_LIVE_HEAD,
        "configuration_sha256": FROZEN_LIVE_CONFIGURATION_SHA256,
        "candidate_manifest_sha256": FROZEN_CANDIDATE_MANIFEST_SHA256,
        "request_tree": {
            "file_count": FROZEN_REQUEST_TREE_FILE_COUNT,
            "total_bytes": FROZEN_REQUEST_TREE_TOTAL_BYTES,
            "sha256sum_manifest_sha256": FROZEN_REQUEST_TREE_MANIFEST_SHA256,
        },
        "scheduled_candidates": EXPECTED_TOTAL,
        "existing_observation_records": EXPECTED_TOTAL,
        "existing_dispatch_records": EXPECTED_TOTAL,
        "additional_model_calls": 0,
        "additional_network_calls": 0,
        "private_aggregate_outputs_present": False,
        "public_outputs_present": False,
        "raw_text_or_traceback_persisted": False,
    }
    return immutable_json(scratch / "INCIDENT.json", incident)


def _candidate_observation_path(scratch: Path, candidate: dict[str, Any]) -> Path:
    return scratch / "requests" / protocol.candidate_path_id(candidate)


def _call_one(
    scratch: Path,
    candidate: dict[str, Any],
    endpoint: str | None,
    credential_env: str | None,
    *,
    transport: protocol.ResponseTransport | None = None,
) -> dict[str, Any]:
    directory = _candidate_observation_path(scratch, candidate)
    edit = candidate.get("mechanical_edit")
    if not isinstance(edit, list) or len(edit) != 3 or not isinstance(edit[2], str):
        raise ExperimentError("candidate mechanical edit lacks its gated replacement")
    body = protocol.request_body(candidate["sentence"], candidate["candidate"]["text"], edit[2])
    return protocol.perform_call(
        directory,
        body,
        endpoint=endpoint,
        credential_env=credential_env,
        transport=transport,
        timeout=protocol.TIMEOUT_SECONDS,
        max_response_bytes=protocol.MAX_RESPONSE_BYTES,
        private_root=scratch,
    )


def execute_validator(
    scratch: Path,
    population: list[dict[str, Any]],
    *,
    endpoint: str | None,
    credential_env: str | None,
    transport: protocol.ResponseTransport | None = None,
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
            observation = _call_one(
                scratch,
                candidate,
                endpoint,
                credential_env,
                transport=transport,
            )
            local[protocol.candidate_path_id(candidate)] = observation
            dispatched += int(observation.get("dispatch") == "ATTEMPTED")
            failures += int(bool(observation.get("operational_failure")))
        return (
            worker_id,
            local,
            {
                "worker": worker_id,
                "assigned": len(partitions[worker_id]),
                "completed": len(local),
                "dispatched_http": dispatched,
                "failures": failures,
                "seconds": time.monotonic() - started,
            },
        )

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
        "uncertain_deliveries": sum(
            1 for observation in observations.values() if observation.get("dispatch") == "UNKNOWN"
        ),
        "protocol_or_operational_failures": sum(
            item["failures"] for item in worker_status.values()
        ),
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


def _accepted_saved_edit(decision: dict[str, Any]) -> list[Any] | None:
    gate = decision.get("final_gate")
    candidate = decision.get("candidate")
    final_case = decision.get("final_case")
    if not isinstance(gate, dict) or not gate.get("accepted"):
        return None
    if not isinstance(candidate, dict) or not isinstance(final_case, dict):
        raise ExperimentError("accepted saved decision lacks its exact edit")
    start = candidate.get("start")
    end = candidate.get("end")
    replacement = final_case.get("adjusted_replacement")
    if type(start) is not int or type(end) is not int or not isinstance(replacement, str):
        raise ExperimentError("accepted saved decision has an invalid edit")
    return [start, end, replacement]


def _call_array(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for decision in decisions:
        for name in ("first", "retry"):
            call = decision.get(name)
            if isinstance(call, dict):
                calls.append(call)
    return calls


def projected_call_counts(results: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"first": 0, "retry": 0, "total": 0}
    for result in results:
        decisions = result.get("decisions", [])
        call_list = result.get("calls", [])
        if not isinstance(decisions, list) or not isinstance(call_list, list):
            raise ExperimentError("projected result lacks call/decision arrays")
        counts["first"] += sum(
            isinstance(item, dict) and isinstance(item.get("first"), dict) for item in decisions
        )
        counts["retry"] += sum(
            isinstance(item, dict) and isinstance(item.get("retry"), dict) for item in decisions
        )
        counts["total"] += len(call_list)
    return counts


def call_accounting(
    baseline_calls: dict[str, int],
    unrestricted_calls: dict[str, int],
    projected_calls: dict[str, int],
    validator_added: int,
) -> dict[str, Any]:
    net = {
        "first": projected_calls["first"],
        "retry": projected_calls["retry"],
        "total": projected_calls["total"] + validator_added,
    }
    return {
        "baseline": baseline_calls,
        "unrestricted_007h": unrestricted_calls,
        "projected_ordinary": projected_calls,
        "ordinary_avoided_vs_baseline": {
            key: baseline_calls[key] - projected_calls[key] for key in ("first", "retry", "total")
        },
        "ordinary_avoided_vs_007h": {
            key: unrestricted_calls[key] - projected_calls[key]
            for key in ("first", "retry", "total")
        },
        "validator_calls_added": validator_added,
        "net_projected": net,
        "delta_vs_baseline": net["total"] - baseline_calls["total"],
        "delta_vs_007h": net["total"] - unrestricted_calls["total"],
    }


def observation_metrics(observations: list[dict[str, Any]]) -> dict[str, Any]:
    decisions: Counter[str] = Counter()
    failures: Counter[str] = Counter()
    latencies: list[float] = []
    reasoning: list[int] = []
    output_tokens: list[int] = []
    dispatched = 0
    uncertain = 0
    for observation in observations:
        decision = observation.get("decision")
        if decision in protocol.CHOICES:
            decisions[str(decision)] += 1
        if observation.get("operational_failure"):
            failures[str(observation.get("failure") or "UNKNOWN_FAILURE")] += 1
        if observation.get("http_seconds") is not None:
            latencies.append(float(observation["http_seconds"]))
        if observation.get("reasoning_tokens") is not None:
            reasoning.append(int(observation["reasoning_tokens"]))
        if observation.get("output_tokens") is not None:
            output_tokens.append(int(observation["output_tokens"]))
        dispatched += int(observation.get("dispatch") == "ATTEMPTED")
        uncertain += int(observation.get("dispatch") == "UNKNOWN")
    return {
        "observation_count": len(observations),
        "decision_counts": dict(decisions),
        "failure_counts": dict(failures),
        "latency_seconds": protocol.distribution(latencies),
        "reasoning_tokens": protocol.distribution(reasoning),
        "output_tokens": protocol.distribution(output_tokens),
        "dispatched_attempts": dispatched,
        "uncertain_deliveries": uncertain,
    }


def projection_result(
    saved: dict[str, Any],
    edits_to_apply: list[list[Any]],
    *,
    only: bool,
    scheduled: set[tuple[int, int, str]],
) -> dict[str, Any]:
    """Project exact original-coordinate edits without invoking a baseline call."""
    source = saved["input"]
    decisions: list[dict[str, Any]] = []
    for decision in saved.get("decisions", []):
        if not isinstance(decision, dict):
            raise ExperimentError("saved decision is not an object")
        key = saved_decision_key(decision)
        if only and key in scheduled:
            continue
        decisions.append(decision)
    calls = _call_array(decisions)
    saved_edits: list[list[Any]] = []
    if only:
        saved_edits = [
            edit for decision in decisions if (edit := _accepted_saved_edit(decision)) is not None
        ]
        retained_failure = any(bool(call.get("operational_failure")) for call in calls)
    else:
        retained_failure = False
    try:
        projected_edits = [*saved_edits, *edits_to_apply] if only else list(edits_to_apply)
        if retained_failure:
            output = source
            projected_edits = []
            projection_failure = "SAVED_FALLBACK_OPERATIONAL_FAILURE"
        else:
            output = apply_edits(source, [tuple(edit) for edit in projected_edits])
            projection_failure = None
    except (AssertionError, TypeError, ValueError) as exc:
        output = source
        projected_edits = []
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
        "edits": projected_edits,
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
        attribution = protocol.attribution(
            sentence, case["dataset"].get("reference"), candidate["mechanical_edit"]
        )
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
        fallback_projection["projection_failure"] = (
            "SAVED_FALLBACK_COMPOSITION: " + type(exc).__name__
        )
        fallback_projection["operational_failure"] = True
    only_projection = projection_result(saved, only_edits, only=True, scheduled=scheduled)
    for target in validator_targets:
        target["applied_fallback"] = (
            target["decision"] == "USE_CANDIDATE"
            and target["mechanical_edit"] in fallback_projection["edits"]
        )
        target["applied_only"] = (
            target["decision"] == "USE_CANDIDATE"
            and target["mechanical_edit"] in only_projection["edits"]
        )
        if target["decision"] == "USE_CANDIDATE" and not target["applied_fallback"]:
            target["fallback_rollback"] = fallback_projection.get("projection_failure") or bool(
                fallback_projection.get("operational_failure")
            )
        if target["decision"] == "USE_CANDIDATE" and not target["applied_only"]:
            target["only_rollback"] = only_projection.get("projection_failure")
    fallback_integrity = protocol.integrity(
        sentence, fallback_projection["output"], fallback_projection["edits"]
    )
    only_integrity = protocol.integrity(
        sentence, only_projection["output"], only_projection["edits"]
    )
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "configuration_sha256": configuration_sha,
        "phase": phase,
        "index": case["index"],
        "id": case["id"],
        "dataset": case["dataset"],
        "baseline": saved,
        "unrestricted_007h": case["new"],
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
    by_case = {
        (record["phase"], record["index"]): record for rows in records.values() for record in rows
    }
    views: dict[str, Any] = {}
    selection_names = {
        "all": None,
        "initial_uv": uv_indices,
        "without_initial_uv": set(range(1, PHASES["dassle-spelling"] + 1)) - uv_indices,
    }

    def one(phase: str, selected: set[int] | None) -> dict[str, Any]:
        pairs_selected = [
            pair
            for pair in pairs[phase]
            if selected is None or pair["dataset"]["index"] in selected
        ]
        record_selected = [by_case[(phase, pair["dataset"]["index"])] for pair in pairs_selected]
        candidate_selected = [
            item
            for item in population
            if item["phase"] == phase and (selected is None or item["case_index"] in selected)
        ]
        baseline_rows = [
            row_metrics(pair["dataset"], pair["saved"], "M2") for pair in pairs_selected
        ]
        unrestricted_rows = [
            row_metrics(record["dataset"], record["unrestricted_007h"], "M2")
            for record in record_selected
        ]
        fallback_rows = [
            row_metrics(record["dataset"], record["validated_fallback"], "M2")
            for record in record_selected
        ]
        only_rows = [
            row_metrics(record["dataset"], record["validated_only"], "M2")
            for record in record_selected
        ]
        outcome: Counter[str] = Counter()
        attribution_counts: Counter[str] = Counter()
        attribution_by_decision: dict[str, Counter[str]] = {
            key: Counter() for key in ("USE_CANDIDATE", "KEEP_ORIGINAL", "UNCERTAIN", "FAILURE")
        }
        selected_observations: list[dict[str, Any]] = []
        for candidate in candidate_selected:
            target = next(
                item
                for item in by_case[(candidate["phase"], candidate["case_index"])][
                    "validator_targets"
                ]
                if item["candidate_id"] == protocol.candidate_path_id(candidate)
            )
            decision = target["decision"] or "FAILURE"
            outcome[decision] += 1
            status = target["attribution"]["status"]
            attribution_counts[status] += 1
            attribution_by_decision[decision][status] += 1
            selected_observations.append(target["observation"])
        validator = observation_metrics(selected_observations)
        valid_response_count = sum(
            outcome[key] for key in ("USE_CANDIDATE", "KEEP_ORIGINAL", "UNCERTAIN")
        )
        validator.update(
            {
                "decision_counts": dict(outcome),
                "valid_response_count": valid_response_count,
                "unconditional_acceptance_rate": (
                    outcome["USE_CANDIDATE"] / len(candidate_selected)
                    if candidate_selected
                    else None
                ),
                "valid_response_acceptance_rate": (
                    outcome["USE_CANDIDATE"] / valid_response_count
                    if valid_response_count
                    else None
                ),
                "attribution": dict(attribution_counts),
                "attribution_by_decision": {
                    key: dict(value) for key, value in attribution_by_decision.items()
                },
                "known_good_reference_exact_sensitivity": {
                    "numerator": attribution_by_decision["USE_CANDIDATE"]["exact_reference"],
                    "denominator": attribution_counts["exact_reference"],
                    "value": (
                        attribution_by_decision["USE_CANDIDATE"]["exact_reference"]
                        / attribution_counts["exact_reference"]
                        if attribution_counts["exact_reference"]
                        else None
                    ),
                },
                "preservation_candidate_rejection_rate": {
                    "numerator": (
                        len(candidate_selected) - outcome["USE_CANDIDATE"]
                        if phase == "dassle-spelling-preservation"
                        else None
                    ),
                    "denominator": (
                        len(candidate_selected) if phase == "dassle-spelling-preservation" else None
                    ),
                    "value": (
                        (len(candidate_selected) - outcome["USE_CANDIDATE"])
                        / len(candidate_selected)
                        if phase == "dassle-spelling-preservation" and candidate_selected
                        else None
                    ),
                },
            }
        )
        baseline_calls = projected_call_counts([pair["saved"] for pair in pairs_selected])
        unrestricted_calls = projected_call_counts(
            [record["unrestricted_007h"] for record in record_selected]
        )
        fallback_calls = projected_call_counts(
            [record["validated_fallback"] for record in record_selected]
        )
        only_calls = projected_call_counts([record["validated_only"] for record in record_selected])
        integrity = {
            view_name: {
                "protected_differences": sum(
                    record["integrity"][view_name]["protected_differences"]
                    for record in record_selected
                ),
                "outside_span_differences": sum(
                    record["integrity"][view_name]["outside_span_differences"]
                    for record in record_selected
                ),
                "exact_expected_output_failures": sum(
                    not record["integrity"][view_name]["exact_expected_output"]
                    for record in record_selected
                ),
            }
            for view_name in ("validated_fallback", "validated_only")
        }
        return {
            "rows": len(pairs_selected),
            "scheduled_candidates": len(candidate_selected),
            "validator": validator,
            "baseline": summarize(baseline_rows),
            "unrestricted_007h": summarize(unrestricted_rows),
            "validated_fallback": summarize(fallback_rows),
            "validated_only": summarize(only_rows),
            "call_accounting": {
                "validated_fallback": call_accounting(
                    baseline_calls, unrestricted_calls, fallback_calls, len(candidate_selected)
                ),
                "validated_only": call_accounting(
                    baseline_calls, unrestricted_calls, only_calls, len(candidate_selected)
                ),
            },
            "integrity": integrity,
            "preservation_changed": {
                "validated_fallback_cases": sum(row["changed"] for row in fallback_rows),
                "validated_fallback_edit_units": sum(
                    row["introduced_edits"] for row in fallback_rows
                ),
                "validated_only_cases": sum(row["changed"] for row in only_rows),
                "validated_only_edit_units": sum(row["introduced_edits"] for row in only_rows),
            }
            if phase == "dassle-spelling-preservation"
            else None,
        }

    for phase in PHASES:
        phase_views = {"all": one(phase, None)}
        if phase == "dassle-spelling":
            phase_views["initial_uv"] = one(phase, uv_indices)
            phase_views["without_initial_uv"] = one(phase, selection_names["without_initial_uv"])
        views[phase] = phase_views
    all_observations = list(observations.values())
    global_validator = observation_metrics(all_observations)
    return {
        "views": views,
        "global_validator": global_validator,
        "worker_runtime": worker_status,
        "actual_validator_call_records": len(observations),
        "dispatched_http_requests": global_validator["dispatched_attempts"],
        "uncertain_deliveries": global_validator["uncertain_deliveries"],
    }


def aggregate(
    scratch: Path,
    prepared: dict[str, Any],
    observations: dict[str, dict[str, Any]],
    worker_status: dict[str, Any],
    *,
    aggregation_recovery: dict[str, Any] | None = None,
) -> dict[str, Any]:
    configuration_sha = prepared["configuration_sha256"]
    records: dict[str, list[dict[str, Any]]] = {}
    candidates_by_case: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for candidate in prepared["population"]:
        candidates_by_case.setdefault((candidate["phase"], candidate["case_index"]), []).append(
            candidate
        )
    for phase, cases in prepared["case_records"].items():
        records[phase] = []
        for case in cases:
            case_candidates = candidates_by_case.get((phase, case["index"]), [])
            records[phase].append(
                make_case_result(phase, case, case_candidates, observations, configuration_sha)
            )
    metrics = make_views(
        prepared["pairs"],
        records,
        prepared["population"],
        observations,
        prepared["uv_indices"],
        worker_status,
    )
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "configuration_sha256": configuration_sha,
        "candidate_manifest_sha256": prepared["configuration"]["source_identity"][
            "candidate_manifest_sha256"
        ],
        "case_identity_manifest_sha256": prepared["configuration"]["source_identity"][
            "case_identity_manifest_sha256"
        ],
        "metrics": metrics,
        "status": (
            "COMPLETE"
            if len(observations) == EXPECTED_TOTAL
            else "PARTIAL_SYSTEMIC_VALIDATOR_FAILURE"
        ),
    }
    if aggregation_recovery is not None:
        result["aggregation_recovery"] = aggregation_recovery
    immutable_json(scratch / "CASE-RESULTS.json", records)
    private_results_sha = immutable_json(scratch / "RESULTS.json", result)
    private_manifest = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "configuration_sha256": configuration_sha,
        "candidate_manifest_sha256": result["candidate_manifest_sha256"],
        "case_identity_manifest_sha256": result["case_identity_manifest_sha256"],
        "aggregation_recovery": aggregation_recovery,
        "case_count": 2_973,
        "candidate_count": EXPECTED_TOTAL,
        "private_results_sha256": private_results_sha,
        "request_record_count": len(observations),
        "status": result["status"],
    }
    private_manifest_sha = immutable_json(scratch / "MANIFEST.json", private_manifest)
    private_report = (
        "# Private 007-i report\n\n"
        + json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n"
    )
    private_report_sha = immutable_write(scratch / "REPORT.md", private_report.encode("utf-8"))
    mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": result["status"],
            "run_id": RUN_ID,
            "configuration_sha256": configuration_sha,
            "candidate_manifest_sha256": result["candidate_manifest_sha256"],
            "private_results_sha256": private_results_sha,
            "private_manifest_sha256": private_manifest_sha,
            "scheduled_candidates": EXPECTED_TOTAL,
            "observation_records": len(observations),
            "dispatched_http_requests": worker_status.get("dispatched_http_requests", 0),
            "aggregation_recovery": aggregation_recovery,
        },
    )
    result["private_results_sha256"] = private_results_sha
    result["private_manifest_sha256"] = private_manifest_sha
    result["private_report_sha256"] = private_report_sha
    return result


def aggregate_from_completed_observations(
    scratch: Path,
    prepared: dict[str, Any],
    aggregation_recovery: dict[str, Any],
    *,
    transport: protocol.ResponseTransport | None = None,
) -> dict[str, Any]:
    """Aggregate persisted observations without crossing the transport boundary."""
    before = verify_frozen_request_tree(scratch / "requests")
    observations = load_completed_observations(scratch, prepared["population"])
    aggregation_recovery["request_tree_before"] = before
    aggregation_recovery["request_tree_after"] = before
    # The optional transport is an injected fail-if-called test seam.  Recovery
    # intentionally never passes it to a request function.
    del transport
    result = aggregate(
        scratch,
        prepared,
        observations,
        prepared["worker_status"],
        aggregation_recovery=aggregation_recovery,
    )
    after = verify_frozen_request_tree(scratch / "requests")
    if after != before:
        raise ExperimentError("request tree changed during aggregation")
    return result


def recover_aggregation(
    repo_root: Path,
    scratch: Path,
    *,
    expected_live_head: str,
    aggregation_head: str,
    transport: protocol.ResponseTransport | None = None,
) -> dict[str, Any]:
    """Recover the interrupted aggregation from the immutable live evidence."""
    git_identity = verify_aggregation_head(repo_root, expected_live_head, aggregation_head)
    prepared = load_aggregation_prepared(scratch, expected_live_head)
    incident_sha = write_aggregation_incident(scratch)
    recovery = {
        **git_identity,
        "mode": "POST_LIVE_ZERO_DISPATCH_AGGREGATION",
        "frozen_configuration_sha256": FROZEN_LIVE_CONFIGURATION_SHA256,
        "incident_sha256": incident_sha,
        "scheduled_candidates": EXPECTED_TOTAL,
        "existing_observation_records": EXPECTED_TOTAL,
        "existing_dispatch_records": EXPECTED_TOTAL,
        "additional_model_calls": 0,
        "additional_network_calls": 0,
        "transport_dispatches_during_aggregation": 0,
        "request_tree_unchanged": True,
        "resampling": False,
    }
    return aggregate_from_completed_observations(
        scratch, prepared, recovery, transport=transport
    )


def public_projection(
    configuration: dict[str, Any], result: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    deployment = configuration.get("deployment", {})
    aggregation_recovery = result.get("aggregation_recovery")
    request = copy.deepcopy(configuration["request"])
    request["wire_keys"] = list(request.get("fields", []))
    request["prompt"] = "owner-supplied frozen 007-i prompt"
    public_config = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "status": result["status"],
        "live_implementation_head": configuration["implementation_head"],
        "aggregation_implementation_head": (
            aggregation_recovery["aggregation_implementation_head"]
            if isinstance(aggregation_recovery, dict)
            else None
        ),
        "implementation_head": configuration["implementation_head"],
        "historical_wire_keys": request["wire_keys"],
        "prior_007h_head": configuration["prior_007h_head"],
        "question": (
            "Can one frozen contextual Qwen validator improve unique one-letter "
            "candidate selection without resampling baseline responses?"
        ),
        "source_identity": dict(configuration["source_identity"]),
        "prompt": {
            "sha256": FROZEN_PROMPT_SHA256,
            "template": "owner-supplied frozen 007-i prompt",
        },
        "deployment": {
            "class": deployment.get("class", "A100-FP8"),
            "model": deployment.get("model", MODEL),
            "protocol": deployment.get("protocol", "Responses non-streaming"),
            "profile_sha256": deployment.get("profile_sha256", FROZEN_PROFILE_SHA256),
            "endpoint": "private endpoint identity omitted",
            "profile_path": "private profile path omitted",
        },
        "request": request,
        "parser": configuration["parser"],
        "scheduling": configuration["scheduling"],
        "limits": configuration["limits"],
        "projections": configuration["projections"],
        "actual": {
            "scheduled_candidates": EXPECTED_TOTAL,
            "validator_observations": result["metrics"]["actual_validator_call_records"],
            "dispatched_attempts": result["metrics"].get("dispatched_http_requests", 0),
            "uncertain_deliveries": result["metrics"].get("uncertain_deliveries", 0),
        },
        "private_evidence_sha256": {
            "results": result["private_results_sha256"],
            "manifest": result["private_manifest_sha256"],
        },
    }
    if isinstance(aggregation_recovery, dict):
        public_config["aggregation_recovery"] = {
            "mode": aggregation_recovery["mode"],
            "live_implementation_head": aggregation_recovery["live_implementation_head"],
            "aggregation_implementation_head": aggregation_recovery[
                "aggregation_implementation_head"
            ],
            "frozen_configuration_sha256": aggregation_recovery[
                "frozen_configuration_sha256"
            ],
            "incident_sha256": aggregation_recovery["incident_sha256"],
            "scheduled_candidates": aggregation_recovery["scheduled_candidates"],
            "existing_observation_records": aggregation_recovery[
                "existing_observation_records"
            ],
            "existing_dispatch_records": aggregation_recovery["existing_dispatch_records"],
            "additional_model_calls": aggregation_recovery["additional_model_calls"],
            "additional_network_calls": aggregation_recovery["additional_network_calls"],
            "transport_dispatches_during_aggregation": aggregation_recovery[
                "transport_dispatches_during_aggregation"
            ],
            "request_tree_before": aggregation_recovery["request_tree_before"],
            "request_tree_after": aggregation_recovery["request_tree_after"],
            "request_tree_unchanged": aggregation_recovery["request_tree_unchanged"],
            "resampling": aggregation_recovery["resampling"],
        }
    public_result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "status": result["status"],
        "live_implementation_head": configuration["implementation_head"],
        "aggregation_implementation_head": public_config["aggregation_implementation_head"],
        "implementation_head": configuration["implementation_head"],
        "configuration_sha256": sha256_bytes(canonical_bytes(public_config)),
        "private_evidence_sha256": public_config["private_evidence_sha256"],
        "metrics": result["metrics"],
        "limitations": [
            (
                "This is an owner-authorized frozen experiment, not a product or "
                "linguistic acceptance claim."
            ),
            (
                "Reference-token attribution is mechanical and non-reference edits "
                "are not semantic harm labels."
            ),
            (
                "Validator failures and UNCERTAIN conservatively reject candidates; "
                "no validator retry or baseline resampling occurs."
            ),
            "Live service availability and inherited repository checks remain separate evidence.",
        ],
    }
    if "aggregation_recovery" in public_config:
        public_result["aggregation_recovery"] = public_config["aggregation_recovery"]
    return public_config, public_result


def public_report(result: dict[str, Any], public_config: dict[str, Any]) -> str:
    def call_triplet(counts: dict[str, int]) -> str:
        return f"{counts['first']}/{counts['retry']}/{counts['total']}"

    lines = [
        "# 007-i contextual validator",
        "",
        "EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.",
        "",
        "One owner-authorized paired contextual validator experiment over frozen 007-h candidates.",
        (
            "No baseline response was resampled; both projections consume the same "
            "validator observation."
        ),
        "",
        "## Frozen identity",
        "",
        f"- Scheduled unique candidates: {EXPECTED_TOTAL} (571 spelling; 164 preservation).",
        f"- Frozen live implementation head: {public_config['live_implementation_head']}.",
        f"- Aggregation implementation head: {public_config['aggregation_implementation_head']}.",
        "- Candidate manifest SHA-256: "
        f"{public_config['source_identity']['candidate_manifest_sha256']}.",
        f"- Prompt SHA-256: {FROZEN_PROMPT_SHA256}.",
        "- Immutable validator observations / dispatched attempts / uncertain deliveries: "
        f"{result['metrics']['actual_validator_call_records']} / "
        f"{result['metrics'].get('dispatched_http_requests', 0)} / "
        f"{result['metrics'].get('uncertain_deliveries', 0)}.",
        "",
    ]
    recovery = public_config.get("aggregation_recovery")
    if isinstance(recovery, dict):
        lines += [
            "## Aggregation recovery",
            "",
            "- The deterministic aggregation incident was a KeyError for the derived "
            "`valid_response_count` field inside `make_views`; no raw traceback or "
            "private payload was published.",
            "- Existing observation records / dispatch records: "
            f"{recovery['existing_observation_records']} / "
            f"{recovery['existing_dispatch_records']}; additional model/network calls: "
            f"{recovery['additional_model_calls']} / {recovery['additional_network_calls']}.",
            "- Request-tree identity before and after: "
            f"{recovery['request_tree_before']['file_count']} files, "
            f"{recovery['request_tree_before']['total_bytes']} bytes, "
            f"{recovery['request_tree_before']['sha256sum_manifest_sha256']} / "
            f"{recovery['request_tree_after']['sha256sum_manifest_sha256']}; unchanged: "
            f"{recovery['request_tree_unchanged']}.",
            f"- Incident identity SHA-256: {recovery['incident_sha256']}.",
            "",
        ]
    lines += [
        "## Required views",
        "",
    ]
    for phase, phase_views in result["metrics"]["views"].items():
        for name, view in phase_views.items():
            validator = view["validator"]
            accepted = validator["attribution_by_decision"]["USE_CANDIDATE"]
            rejected = {
                status: sum(
                    validator["attribution_by_decision"][key].get(status, 0)
                    for key in ("KEEP_ORIGINAL", "UNCERTAIN", "FAILURE")
                )
                for status in ("exact_reference", "non_reference", "unresolved")
            }
            fallback_accounting = view["call_accounting"]["validated_fallback"]
            only_accounting = view["call_accounting"]["validated_only"]
            decision_counts = validator["decision_counts"]
            sensitivity = validator["known_good_reference_exact_sensitivity"]
            baseline_score = view["baseline"]
            fallback_score = view["validated_fallback"]
            only_score = view["validated_only"]
            fallback_integrity = view["integrity"]["validated_fallback"]
            only_integrity = view["integrity"]["validated_only"]
            lines += [
                f"### {phase} / {name}",
                f"- Rows / scheduled candidates: {view['rows']} / {view['scheduled_candidates']}.",
                "- Validator decisions USE / KEEP / UNCERTAIN / FAILURE: "
                f"{decision_counts.get('USE_CANDIDATE', 0)} / "
                f"{decision_counts.get('KEEP_ORIGINAL', 0)} / "
                f"{decision_counts.get('UNCERTAIN', 0)} / "
                f"{decision_counts.get('FAILURE', 0)}.",
                "- Attribution accepted exact-reference / non-reference / unresolved: "
                f"{accepted.get('exact_reference', 0)} / "
                f"{accepted.get('non_reference', 0)} / {accepted.get('unresolved', 0)}.",
                "- Attribution rejected exact-reference / non-reference / unresolved: "
                f"{rejected['exact_reference']} / {rejected['non_reference']} / "
                f"{rejected['unresolved']}.",
                "- Unconditional / valid-response acceptance: "
                f"{validator['unconditional_acceptance_rate']} / "
                f"{validator['valid_response_acceptance_rate']}.",
                "- Reference-exact sensitivity (numerator / denominator): "
                f"{sensitivity['numerator']} / {sensitivity['denominator']} = "
                f"{sensitivity['value']}.",
                f"- Baseline TP/FP/FN: {baseline_score['tp']} / "
                f"{baseline_score['fp']} / {baseline_score['fn']}.",
                f"- VALIDATED+FALLBACK TP/FP/FN: {fallback_score['tp']} / "
                f"{fallback_score['fp']} / {fallback_score['fn']}.",
                f"- VALIDATED-ONLY TP/FP/FN: {only_score['tp']} / "
                f"{only_score['fp']} / {only_score['fn']}.",
                "- Baseline / fallback / only precision: "
                f"{baseline_score['precision']} / {fallback_score['precision']} / "
                f"{only_score['precision']}.",
                "- Baseline / fallback / only recall: "
                f"{baseline_score['recall']} / {fallback_score['recall']} / "
                f"{only_score['recall']}.",
                "- Baseline / fallback / only F0.5: "
                f"{view['baseline']['F0.5']} / {view['validated_fallback']['F0.5']} / "
                f"{view['validated_only']['F0.5']}.",
                "- Fallback calls baseline / unrestricted-007h / avoided-baseline / "
                "avoided-007h / validator-added / net "
                "(first/retry/total): "
                f"{call_triplet(fallback_accounting['baseline'])} / "
                f"{call_triplet(fallback_accounting['unrestricted_007h'])} / "
                f"{call_triplet(fallback_accounting['ordinary_avoided_vs_baseline'])} / "
                f"{call_triplet(fallback_accounting['ordinary_avoided_vs_007h'])} / "
                f"{fallback_accounting['validator_calls_added']} / "
                f"{call_triplet(fallback_accounting['net_projected'])}.",
                "- Only calls baseline / unrestricted-007h / avoided-baseline / "
                "avoided-007h / validator-added / net (first/retry/total): "
                f"{call_triplet(only_accounting['baseline'])} / "
                f"{call_triplet(only_accounting['unrestricted_007h'])} / "
                f"{call_triplet(only_accounting['ordinary_avoided_vs_baseline'])} / "
                f"{call_triplet(only_accounting['ordinary_avoided_vs_007h'])} / "
                f"{only_accounting['validator_calls_added']} / "
                f"{call_triplet(only_accounting['net_projected'])}.",
                "- Protected/outside differences fallback: "
                f"{fallback_integrity['protected_differences']} / "
                f"{fallback_integrity['outside_span_differences']}.",
                "- Protected/outside differences only: "
                f"{only_integrity['protected_differences']} / "
                f"{only_integrity['outside_span_differences']}.",
                "",
            ]
            if phase == "dassle-spelling-preservation":
                changed = view["preservation_changed"]
                lines.append(
                    "- Preservation changed cases/edit units fallback and only: "
                    f"{changed['validated_fallback_cases']} / "
                    f"{changed['validated_fallback_edit_units']} and "
                    f"{changed['validated_only_cases']} / {changed['validated_only_edit_units']}."
                )
                lines.append("")
    global_metrics = result["metrics"]["global_validator"]
    lines += [
        "## Runtime and limitations",
        "",
        "- Global validator observations/decisions/failures: "
        f"{global_metrics['observation_count']} / {global_metrics['decision_counts']} / "
        f"{global_metrics['failure_counts']}.",
        "- Global dispatched attempts / uncertain deliveries: "
        f"{global_metrics['dispatched_attempts']} / "
        f"{global_metrics['uncertain_deliveries']}.",
        "- Global latency seconds (n / median / p95 / max): "
        f"{global_metrics['latency_seconds']['n']} / "
        f"{global_metrics['latency_seconds']['median']} / "
        f"{global_metrics['latency_seconds']['p95']} / "
        f"{global_metrics['latency_seconds']['max']}.",
        f"- Worker count: {WORKERS}; at most one in-flight call per worker.",
        (
            "- The validator is a strict binary choice protocol. Extra text, malformed "
            "JSON, wrong model/effort, incomplete status, missing token accounting, "
            "timeout, or transport failure is a distinct conservative failure."
        ),
        (
            "- Reference scoring can penalize valid alternatives. Non-reference changes "
            "are not semantic harm labels."
        ),
        (
            "- This result does not authorize integration, merge, release, deployment, "
            "or product linguistic acceptance."
        ),
    ]
    return "\n".join(lines) + "\n"


def write_public(
    repo_root: Path, configuration: dict[str, Any], result: dict[str, Any]
) -> dict[str, str]:
    public_config, public_result = public_projection(configuration, result)
    paths = {
        "config": repo_root / "research/configs/007-i-contextual-validator.json",
        "result": repo_root / "research/results/007-i-contextual-validator.json.gz",
        "report": repo_root / "research/reports/007-i-contextual-validator.md",
    }
    public_immutable_write(paths["config"], canonical_bytes(public_config))
    public_immutable_write(paths["result"], gzip.compress(canonical_bytes(public_result), mtime=0))
    public_immutable_write(paths["report"], public_report(result, public_config).encode("utf-8"))
    return {key: sha256_file(path) for key, path in paths.items()}


def run(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    scratch = Path(args.scratch).absolute()
    profile_path = Path(args.profile_path).absolute() if args.profile_path else None
    if args.recover_aggregation:
        if args.prepare_only:
            raise ExperimentError("aggregation recovery cannot be prepare-only")
        if not args.aggregation_head:
            raise ExperimentError("aggregation recovery requires --aggregation-head")
        result = recover_aggregation(
            repo_root,
            scratch,
            expected_live_head=args.expected_implementation_head,
            aggregation_head=args.aggregation_head,
        )
        require_private_file(scratch / "CONFIGURATION.json")
        configuration = read_json(scratch / "CONFIGURATION.json")
        if not isinstance(configuration, dict):
            raise ExperimentError("frozen configuration is not an object")
        paths = write_public(repo_root, configuration, result)
        return {
            "status": result["status"],
            "configuration_sha256": sha256_file(scratch / "CONFIGURATION.json"),
            "private_results_sha256": result["private_results_sha256"],
            "private_manifest_sha256": result["private_manifest_sha256"],
            "private_report_sha256": result["private_report_sha256"],
            "public": paths,
            "scheduled_candidates": EXPECTED_TOTAL,
            "actual_model_calls": result["metrics"]["actual_validator_call_records"],
            "actual_network_calls": result["metrics"].get("dispatched_http_requests", 0),
            "additional_model_calls": result["aggregation_recovery"]["additional_model_calls"],
            "additional_network_calls": result["aggregation_recovery"]["additional_network_calls"],
        }
    if args.aggregation_head:
        raise ExperimentError("--aggregation-head requires --recover-aggregation")
    has_configuration = (scratch / "CONFIGURATION.json").exists()
    if args.prepare_only and has_configuration:
        prepared = load_prepared(
            scratch,
            args.expected_implementation_head,
            endpoint=args.endpoint,
            profile_path=profile_path,
            credential_env=args.credential_env,
        )
    elif not has_configuration:
        if not args.source_root:
            raise ExperimentError("initial preparation requires the frozen 007-h source root")
        prepared = prepare(
            repo_root,
            scratch,
            Path(args.source_root).absolute(),
            args.expected_implementation_head,
            endpoint=args.endpoint,
            profile_path=profile_path,
            credential_env=args.credential_env,
        )
    else:
        prepared = load_prepared(
            scratch,
            args.expected_implementation_head,
            endpoint=args.endpoint,
            profile_path=profile_path,
            credential_env=args.credential_env,
        )
    if args.prepare_only:
        return {
            "status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "configuration_sha256": prepared["configuration_sha256"],
            "candidate_manifest_sha256": prepared["candidate_manifest_sha256"],
            "scheduled_candidates": EXPECTED_TOTAL,
            "actual_model_calls": 0,
            "actual_network_calls": 0,
        }
    existing_status = (
        read_json(scratch / "RUN-STATUS.json") if (scratch / "RUN-STATUS.json").exists() else {}
    )
    if (
        existing_status.get("status") in {"COMPLETE", "PARTIAL_SYSTEMIC_VALIDATOR_FAILURE"}
        and (scratch / "RESULTS.json").exists()
    ):
        result = read_json(scratch / "RESULTS.json")
        paths = write_public(repo_root, prepared["configuration"], result)
        return {
            "status": result["status"],
            "configuration_sha256": prepared["configuration_sha256"],
            "private_results_sha256": result.get("private_results_sha256"),
            "private_manifest_sha256": result.get("private_manifest_sha256"),
            "public": paths,
            "actual_model_calls": result["metrics"]["actual_validator_call_records"],
            "actual_network_calls": result["metrics"].get("dispatched_http_requests", 0),
        }
    observations, worker_status = execute_validator(
        scratch,
        prepared["population"],
        endpoint=args.endpoint,
        credential_env=args.credential_env,
    )
    result = aggregate(scratch, prepared, observations, worker_status)
    paths = write_public(repo_root, prepared["configuration"], result)
    return {
        "status": result["status"],
        "configuration_sha256": prepared["configuration_sha256"],
        "private_results_sha256": result["private_results_sha256"],
        "private_manifest_sha256": result["private_manifest_sha256"],
        "public": paths,
        "scheduled_candidates": EXPECTED_TOTAL,
        "actual_model_calls": result["metrics"]["actual_validator_call_records"],
        "actual_network_calls": result["metrics"].get("dispatched_http_requests", 0),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--expected-implementation-head", required=True)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--endpoint")
    parser.add_argument("--credential-env")
    parser.add_argument("--profile", "--profile-path", dest="profile_path")
    parser.add_argument("--recover-aggregation", action="store_true")
    parser.add_argument("--aggregation-head")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(run(args), sort_keys=True))
    except (ExperimentError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "reason": str(exc)}, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
