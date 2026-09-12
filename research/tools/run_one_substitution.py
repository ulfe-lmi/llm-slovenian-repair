"""Run the single frozen 007-h one-substitution experiment offline.

The command consumes only explicitly supplied private roots.  It verifies and
replays saved M2 records, writes full evidence below the caller's private
scratch root, and emits only data-free aggregate projections into ``research``.
It never imports an HTTP client or calls a model.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import sqlite3
import stat
import subprocess
import time
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from research.curated.historical_common import immutable_bytes, pointer
from research.curated.historical_scoring import edit_key, edits, row_metrics, summarize
from research.curated.patching import apply_edits
from research.curated.protected import is_protected, protected_intervals
from research.one_substitution import (
    candidate_key,
    entering_targets,
    mechanical_substitution,
    project_saved_case,
    qualifying_candidates,
    saved_accepted_edits,
)

EXPERIMENT_ID = "007-h-unique-one-letter-unigram-substitution"
RUN_ID = "007-h"
EXPECTED_INDEX_ROWS = 141_162
UV_ROWS = 75
PHASES = {"dassle-spelling": 1_487, "dassle-spelling-preservation": 1_486}
PUBLIC_ARCHIVE_ROOTS = (
    "research/configs",
    "research/reports",
    "research/results",
    "research/registry",
    "research/tables",
)
PUBLIC_OUTPUT_PATHS = frozenset(
    {
        "research/configs/007-h-unique-one-letter-unigram-substitution.json",
        "research/reports/007-h-unique-one-letter-unigram-substitution.md",
        "research/results/007-h-unique-one-letter-unigram-substitution.json.gz",
    }
)
IMPLEMENTATION_PATHS = (
    "research/one_substitution.py",
    "research/tools/run_one_substitution.py",
    "research/curated/historical_scoring.py",
    "research/curated/patching.py",
)
IMPLEMENTATION_BRANCH = "oap/007-concept-verification"
EXPECTED_INPUTS = {
    "dassle-spelling.jsonl": (
        761_193,
        "045825b73ab42d7acb1fc987d10ec15356c2727eefd7e45dff7e2fc77ad4e9b7",
    ),
    "dassle-spelling-preservation.jsonl": (
        949_922,
        "d77d6942268d5eeb6116eabef0c272e4c2a840991be39142427639c5f9161eff",
    ),
    "detector-spelling.jsonl": (
        1_772_260,
        "d401d58301b2679ca9377cac946daf9574d54528f7d3a867b1b8e8f9bffc1f63",
    ),
    "detector-preservation.jsonl": (
        995_844,
        "6e020b7618630d7c25ae643cb565263c147e8b57ebbc4473391f9256b14b3f69",
    ),
    "baseline-configuration.json": (
        59_764,
        "4c748b8e9711148c008d4157edef209a21531a2412745f230069215d3ddc5d29",
    ),
    "baseline-results.json": (
        21_676_581,
        "3a75c4dac3d77db7c865d363197efc368898c53b8b092abbc14451052354700f",
    ),
    "uv-audit-results.json": (
        140_769,
        "6d6fb695d420e22ceda4664c20286242151acccce57c381e7abd26415e17b153",
    ),
    "index.sqlite": (7_991_296, "f769235b6af3412e65f0875f4d08231c832f60d8630b43a06ab927c2d32c739f"),
}
BASELINE_EXPECTATIONS = {
    "dassle-spelling": {
        "tp": 604,
        "fp": 193,
        "fn": 911,
        "precision": 0.7578419071518193,
        "recall": 0.39867986798679866,
        "first_calls": 2_001,
        "retry_calls": 209,
        "total_calls": 2_210,
        "failures": 40,
    },
    "dassle-spelling-preservation": {
        "first_calls": 920,
        "retry_calls": 92,
        "total_calls": 1_012,
        "failures": 23,
        "changed_cases": 87,
    },
}


class ExperimentError(RuntimeError):
    """Raised when a frozen source or replay boundary cannot be proved."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExperimentError(f"invalid private JSON artifact: {path.name}") from exc


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise ExperimentError(f"invalid private JSONL artifact: {path.name}") from exc
    for line in lines:
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ExperimentError(f"invalid private JSONL row: {path.name}") from exc
        if not isinstance(value, dict):
            raise ExperimentError(f"private JSONL row is not an object: {path.name}")
        result.append(value)
    return result


def require_private_file(
    path: Path,
    *,
    expected_size: int | None = None,
    expected_sha: str | None = None,
    harden: bool = False,
) -> str:
    try:
        info = path.lstat()
    except OSError as exc:
        raise ExperimentError(f"private file is unavailable: {path.name}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise ExperimentError(f"private file is not a regular non-symlink: {path.name}")
    if info.st_uid != os.getuid():
        raise ExperimentError(f"private file ownership mismatch: {path.name}")
    if expected_size is not None and info.st_size != expected_size:
        raise ExperimentError(f"private file size mismatch: {path.name}")
    if harden and info.st_mode & 0o077:
        os.chmod(path, 0o600)
    actual = sha256_file(path)
    if expected_sha is not None and actual != expected_sha:
        raise ExperimentError(f"private file hash mismatch: {path.name}")
    return actual


def require_private_dir(path: Path, *, harden: bool = False) -> None:
    try:
        info = path.lstat()
    except OSError as exc:
        raise ExperimentError(f"private directory is unavailable: {path.name}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise ExperimentError(f"private directory is not a real directory: {path.name}")
    if info.st_uid != os.getuid():
        raise ExperimentError(f"private directory ownership mismatch: {path.name}")
    if harden and info.st_mode & 0o077:
        os.chmod(path, 0o700)


def _git_bytes(repo_root: Path, *arguments: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "--no-optional-locks", *arguments],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ExperimentError("committed implementation identity cannot be read") from exc
    return completed.stdout


def verify_committed_implementation(repo_root: Path, expected_head: str) -> dict[str, Any]:
    """Verify local committed bytes against a caller-verified full remote SHA.

    The caller verifies the remote branch with its own read-only Git command and
    supplies that full SHA. This function intentionally performs no network
    operation; it proves that the local checkout is clean, on the required
    branch, at that SHA, and that each source file is byte-identical to its HEAD
    blob before a configuration can be frozen.
    """
    if len(expected_head) != 40 or any(
        character not in "0123456789abcdef" for character in expected_head
    ):
        raise ExperimentError("implementation head is not a full lowercase commit SHA")
    status = _git_bytes(repo_root, "status", "--porcelain=v1", "--untracked-files=all")
    if status:
        raise ExperimentError("repository is dirty before implementation freeze")
    try:
        branch = (
            _git_bytes(repo_root, "symbolic-ref", "--quiet", "--short", "HEAD")
            .decode("ascii")
            .strip()
        )
        head = _git_bytes(repo_root, "rev-parse", "--verify", "HEAD").decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise ExperimentError("repository identity is not ASCII") from exc
    if branch != IMPLEMENTATION_BRANCH:
        raise ExperimentError("repository is detached or on the wrong branch")
    if head != expected_head:
        raise ExperimentError("local HEAD does not match caller-verified implementation SHA")
    head_blobs: dict[str, Any] = {}
    for relative in IMPLEMENTATION_PATHS:
        local = repo_root / relative
        try:
            local_info = local.lstat()
        except OSError as exc:
            raise ExperimentError(f"implementation file is unavailable: {relative}") from exc
        if stat.S_ISLNK(local_info.st_mode) or not stat.S_ISREG(local_info.st_mode):
            raise ExperimentError(f"implementation file is not a regular non-symlink: {relative}")
        try:
            blob = _git_bytes(repo_root, "rev-parse", f"HEAD:{relative}").decode("ascii").strip()
            head_bytes = _git_bytes(repo_root, "show", f"HEAD:{relative}")
        except UnicodeDecodeError as exc:
            raise ExperimentError(f"HEAD blob identity is not ASCII: {relative}") from exc
        if local.read_bytes() != head_bytes:
            raise ExperimentError(
                f"working implementation bytes do not match HEAD blob: {relative}"
            )
        head_blobs[relative] = {
            "git_blob_sha1": blob,
            "sha256": hashlib.sha256(head_bytes).hexdigest(),
        }
    return {"implementation_head": head, "branch": branch, "head_blobs": head_blobs}


def write_immutable(path: Path, value: object) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    require_private_dir(path.parent, harden=True)
    if path.exists() and path.is_symlink():
        raise ExperimentError(f"refusing symlink artifact: {path.name}")
    data = canonical_bytes(value)
    immutable_bytes(path, data)
    os.chmod(path, 0o600)
    return hashlib.sha256(data).hexdigest()


def write_private_bytes(path: Path, data: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    require_private_dir(path.parent, harden=True)
    if path.exists() and path.is_symlink():
        raise ExperimentError(f"refusing symlink artifact: {path.name}")
    immutable_bytes(path, data)
    os.chmod(path, 0o600)
    return hashlib.sha256(data).hexdigest()


def write_status(path: Path, value: object) -> None:
    """Replace only the mutable private progress pointer."""
    path.parent.mkdir(parents=True, exist_ok=True)
    require_private_dir(path.parent, harden=True)
    if path.is_symlink():
        raise ExperimentError(f"refusing symlink status artifact: {path.name}")
    pointer(path, value)
    os.chmod(path, 0o600)


def verify_staged_inputs(
    scratch: Path, source_root: Path, uv_root: Path, index_source: Path
) -> dict[str, Any]:
    require_private_dir(scratch, harden=True)
    inputs = scratch / "inputs"
    require_private_dir(inputs, harden=True)
    staged = {
        "dassle-spelling.jsonl": inputs / "datasets/dassle-spelling.jsonl",
        "dassle-spelling-preservation.jsonl": inputs
        / "datasets/dassle-spelling-preservation.jsonl",
        "detector-spelling.jsonl": inputs / "detector-snapshots/dassle-spelling.jsonl",
        "detector-preservation.jsonl": inputs
        / "detector-snapshots/dassle-spelling-preservation.jsonl",
        "baseline-configuration.json": inputs / "baseline/CONFIGURATION.json",
        "baseline-results.json": inputs / "baseline/RESULTS.json",
        "uv-audit-results.json": inputs / "uv-audit/RESULTS.json",
        "index.sqlite": inputs / "index/index.sqlite",
    }
    source = {
        "dassle-spelling.jsonl": source_root / "datasets/dassle-spelling.jsonl",
        "dassle-spelling-preservation.jsonl": source_root
        / "datasets/dassle-spelling-preservation.jsonl",
        "detector-spelling.jsonl": source_root / "detector-snapshots/dassle-spelling.jsonl",
        "detector-preservation.jsonl": source_root
        / "detector-snapshots/dassle-spelling-preservation.jsonl",
        "baseline-configuration.json": source_root / "final-20260910/CONFIGURATION.json",
        "baseline-results.json": source_root / "final-20260910/RESULTS.json",
        "uv-audit-results.json": uv_root / "RESULTS.json",
        "index.sqlite": index_source,
    }
    identities: dict[str, Any] = {}
    for name, staged_path in staged.items():
        expected_size, expected_sha = EXPECTED_INPUTS[name]
        staged_sha = require_private_file(
            staged_path, expected_size=expected_size, expected_sha=expected_sha, harden=True
        )
        source_sha = require_private_file(
            source[name], expected_size=expected_size, expected_sha=expected_sha
        )
        if staged_path.read_bytes() != source[name].read_bytes():
            raise ExperimentError(f"staged byte identity mismatch: {name}")
        identities[name] = {"size": expected_size, "sha256": staged_sha}

    for phase, count in PHASES.items():
        source_phase = source_root / "results/A100" / phase
        staged_phase = inputs / "results/A100" / phase
        require_private_dir(staged_phase, harden=True)
        for index in range(1, count + 1):
            serial = f"{index:06d}"
            source_record = source_phase / serial / "M2.json"
            staged_record = staged_phase / serial / "M2.json"
            source_sha = require_private_file(source_record)
            staged_sha = require_private_file(
                staged_record,
                expected_size=source_record.stat().st_size,
                expected_sha=source_sha,
                harden=True,
            )
            if staged_record.read_bytes() != source_record.read_bytes():
                raise ExperimentError(f"staged byte identity mismatch: {phase}/{serial}")
            identities.setdefault("m2_records", {})[f"{phase}/{serial}"] = {
                "size": staged_record.stat().st_size,
                "sha256": staged_sha,
            }
    identities["m2_record_count"] = sum(PHASES.values())
    write_immutable(scratch / "INPUT-MANIFEST.json", identities)
    return identities


def call_counts(record: Mapping[str, Any]) -> dict[str, int]:
    decisions = record.get("decisions")
    calls = record.get("calls")
    if not isinstance(decisions, list) or not isinstance(calls, list):
        raise ExperimentError("saved M2 record lacks call/decision arrays")
    flattened: list[dict[str, Any]] = []
    counts = {"first": 0, "retry": 0}
    expected_kinds = (("first", "reviewer"), ("retry", "expression-retry"))
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ExperimentError("saved M2 decision is not an object")
        for stage, expected_kind in expected_kinds:
            call = decision.get(stage)
            if call is None:
                continue
            if not isinstance(call, dict):
                raise ExperimentError(f"saved M2 {stage} call is not an object")
            if call.get("kind") != expected_kind:
                raise ExperimentError(
                    f"saved M2 {stage} call kind is not {expected_kind}"
                )
            flattened.append(call)
            counts[stage] += 1
    if calls != flattened:
        raise ExperimentError("saved M2 calls do not equal decision-stage flattening")
    return {"first": counts["first"], "retry": counts["retry"], "total": len(flattened)}


def validate_pair(
    dataset: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    saved: Mapping[str, Any],
    phase: str,
    index: int,
) -> None:
    expected_id = dataset.get("id")
    expected_input = dataset.get("input")
    if (
        dataset.get("index") != index
        or snapshot.get("index") != index
        or saved.get("index") != index
    ):
        raise ExperimentError(f"index pairing mismatch: {phase}/{index}")
    if snapshot.get("id") != expected_id or saved.get("id") != expected_id:
        raise ExperimentError(f"ID pairing mismatch: {phase}/{index}")
    reference = dataset.get("reference")
    if not isinstance(expected_input, str) or not (
        isinstance(reference, str)
        or (reference is None and dataset.get("reference_status") == "MISSING_BLANK_FIELD")
    ):
        raise ExperimentError(f"dataset text schema mismatch: {phase}/{index}")
    input_sha = hashlib.sha256(expected_input.encode("utf-8")).hexdigest()
    if snapshot.get("input_sha256") != input_sha or saved.get("input_sha256") != input_sha:
        raise ExperimentError(f"input hash pairing mismatch: {phase}/{index}")
    if saved.get("input") != expected_input or saved.get("method") != "M2":
        raise ExperimentError(f"saved M2 input/method mismatch: {phase}/{index}")
    if saved.get("detector") != snapshot.get("detector"):
        raise ExperimentError(f"detector snapshot mismatch: {phase}/{index}")
    detector = saved.get("detector")
    if not isinstance(detector, dict):
        raise ExperimentError(f"saved detector missing: {phase}/{index}")
    candidates = detector.get("candidates")
    english = detector.get("english")
    if (
        not isinstance(candidates, list)
        or not isinstance(english, list)
        or len(candidates) != len(english)
    ):
        raise ExperimentError(f"detector/English alignment mismatch: {phase}/{index}")
    for candidate, policy in zip(candidates, english, strict=True):
        if not isinstance(candidate, dict) or not isinstance(policy, dict):
            raise ExperimentError(f"detector entry schema mismatch: {phase}/{index}")
        evidence = candidate.get("evidence")
        unigram = evidence.get("unigram") if isinstance(evidence, dict) else None
        policy_unigram = policy.get("slovene_unigram")
        if not isinstance(unigram, dict) or not isinstance(policy_unigram, dict):
            raise ExperimentError(f"detector unigram evidence missing: {phase}/{index}")
        if unigram.get("state") != policy_unigram.get("state"):
            raise ExperimentError(f"detector unigram state mismatch: {phase}/{index}")
    if not isinstance(saved.get("output"), str) or not isinstance(
        saved.get("operational_failure"), bool
    ):
        raise ExperimentError(f"saved M2 result schema mismatch: {phase}/{index}")
    call_counts(saved)
    if saved["operational_failure"] != any(
        bool(call.get("operational_failure")) for call in saved["calls"] if isinstance(call, dict)
    ):
        raise ExperimentError(f"saved failure semantics mismatch: {phase}/{index}")


def load_pairs(scratch: Path) -> dict[str, list[dict[str, Any]]]:
    inputs = scratch / "inputs"
    result: dict[str, list[dict[str, Any]]] = {}
    for phase, count in PHASES.items():
        dataset_path = (
            inputs
            / "datasets"
            / (
                "dassle-spelling.jsonl"
                if phase == "dassle-spelling"
                else "dassle-spelling-preservation.jsonl"
            )
        )
        snapshot_path = (
            inputs
            / "detector-snapshots"
            / (
                "dassle-spelling.jsonl"
                if phase == "dassle-spelling"
                else "dassle-spelling-preservation.jsonl"
            )
        )
        datasets = read_jsonl(dataset_path)
        snapshots = read_jsonl(snapshot_path)
        if len(datasets) != count or len(snapshots) != count:
            raise ExperimentError(f"dataset/snapshot count mismatch: {phase}")
        pairs: list[dict[str, Any]] = []
        for index, (dataset, snapshot) in enumerate(zip(datasets, snapshots, strict=True), 1):
            saved_path = inputs / "results/A100" / phase / f"{index:06d}" / "M2.json"
            saved = read_json(saved_path)
            if not isinstance(saved, dict):
                raise ExperimentError(f"saved M2 is not an object: {phase}/{index}")
            validate_pair(dataset, snapshot, saved, phase, index)
            pairs.append({"dataset": dataset, "snapshot": snapshot, "saved": saved})
        result[phase] = pairs
    if sum(len(rows) for rows in result.values()) != 2_973:
        raise ExperimentError("paired record total is not 2,973")
    return result


def validate_baseline_replay(pairs: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    baseline: dict[str, Any] = {}
    for phase, rows in pairs.items():
        for row in rows:
            saved = row["saved"]
            accepted = saved_accepted_edits(saved)
            if saved["operational_failure"]:
                if saved["output"] != saved["input"]:
                    raise ExperimentError(
                        f"failed baseline did not return original: {phase}/{saved['index']}"
                    )
            else:
                try:
                    reconstructed = apply_edits(saved["input"], [tuple(edit) for edit in accepted])
                except (TypeError, ValueError, AssertionError) as exc:
                    raise ExperimentError(
                        f"baseline accepted edits cannot be patched: {phase}/{saved['index']}"
                    ) from exc
                if reconstructed != saved["output"] or saved.get("edits") != accepted:
                    raise ExperimentError(
                        f"baseline output/edits replay mismatch: {phase}/{saved['index']}"
                    )
        scored = [row_metrics(row["dataset"], row["saved"], "M2") for row in rows]
        summary = summarize(scored)
        counts = {
            key: sum(call_counts(row["saved"])[key] for row in rows)
            for key in ("first", "retry", "total")
        }
        failures = sum(bool(row["saved"]["operational_failure"]) for row in rows)
        expectations = BASELINE_EXPECTATIONS[phase]
        for key in ("tp", "fp", "fn"):
            if key in expectations and summary[key] != expectations[key]:
                raise ExperimentError(f"baseline {phase} {key} mismatch")
        for key in ("precision", "recall"):
            if key in expectations and not math.isclose(
                summary[key], expectations[key], rel_tol=0.0, abs_tol=1e-15
            ):
                raise ExperimentError(f"baseline {phase} {key} mismatch")
        if counts != {
            "first": expectations.get("first_calls", counts["first"]),
            "retry": expectations["retry_calls"],
            "total": expectations["total_calls"],
        }:
            raise ExperimentError(f"baseline {phase} call counts mismatch")
        if failures != expectations["failures"]:
            raise ExperimentError(f"baseline {phase} failure count mismatch")
        if (
            "changed_cases" in expectations
            and summary["changed_examples"] != expectations["changed_cases"]
        ):
            raise ExperimentError(f"baseline {phase} preservation changes mismatch")
        baseline[phase] = {"summary": summary, "calls": counts, "failures": failures}
    return baseline


def map_uv_cases(
    positions: list[Any], cases: list[Any], spelling: list[dict[str, Any]]
) -> tuple[set[int], list[dict[str, Any]]]:
    """Map full-DASSLE audit identities to spelling-subset positions explicitly."""
    if len(positions) != UV_ROWS or len(cases) != UV_ROWS:
        raise ExperimentError("u/v audit identity list is incomplete")
    if any(
        type(position) is not int or not 1 <= position <= len(spelling) for position in positions
    ):
        raise ExperimentError("u/v spelling position is outside spelling rows")
    if len(set(positions)) != UV_ROWS:
        raise ExperimentError("u/v spelling positions are not unique")
    if any(not isinstance(case, dict) for case in cases):
        raise ExperimentError("u/v audit case is not an object")
    ids = [case.get("id") for case in cases]
    full_indices = [case.get("index") for case in cases]
    if len(set(ids)) != UV_ROWS:
        raise ExperimentError("u/v audit case IDs are not unique")
    if len(set(full_indices)) != UV_ROWS:
        raise ExperimentError("u/v full-DASSLE indices are not unique")
    mapping: list[dict[str, Any]] = []
    for case, position in zip(cases, positions, strict=True):
        spelling_row = spelling[position - 1]
        dataset = spelling_row.get("dataset")
        if not isinstance(dataset, dict):
            raise ExperimentError("spelling row lacks dataset identity")
        if case.get("id") != dataset.get("id"):
            raise ExperimentError("u/v audit ID identity does not map exactly")
        if dataset.get("index") != position:
            raise ExperimentError("spelling-subset index is not the mapped position")
        mapping.append(
            {
                "id": case["id"],
                "full_dassle_index": case["index"],
                "spelling_position": position,
            }
        )
    return set(positions), mapping


def verify_uv_mapping(
    scratch: Path, spelling: list[dict[str, Any]]
) -> tuple[set[int], list[dict[str, Any]]]:
    value = read_json(scratch / "inputs/uv-audit/RESULTS.json")
    if not isinstance(value, dict) or value.get("initial_uv_rows") != UV_ROWS:
        raise ExperimentError("u/v audit does not assert 75 rows")
    positions = value.get("spelling_positions_of_uv_rows")
    cases = value.get("initial_uv_cases")
    if not isinstance(positions, list) or not isinstance(cases, list):
        raise ExperimentError("u/v audit identity list is incomplete")
    return map_uv_cases(positions, cases, spelling)


def load_vocabulary(index_path: Path) -> tuple[set[str], dict[int, list[str]], float, int]:
    require_private_file(
        index_path,
        expected_size=EXPECTED_INPUTS["index.sqlite"][0],
        expected_sha=EXPECTED_INPUTS["index.sqlite"][1],
    )
    started = time.perf_counter()
    uri = index_path.as_uri() + "?mode=ro&immutable=1"
    connection = sqlite3.connect(uri, uri=True)
    try:
        rows = connection.execute("SELECT word, count FROM unigram ORDER BY word").fetchall()
    except sqlite3.Error as exc:
        raise ExperimentError("unigram table cannot be read") from exc
    finally:
        connection.close()
    vocabulary: set[str] = set()
    buckets: dict[int, list[str]] = defaultdict(list)
    for word, count in rows:
        if not isinstance(word, str) or not isinstance(count, int):
            raise ExperimentError("unigram row schema mismatch")
        if word in vocabulary:
            raise ExperimentError("unigram vocabulary forms are not unique")
        vocabulary.add(word)
        buckets[len(word)].append(word)
    if len(rows) != EXPECTED_INDEX_ROWS or len(vocabulary) != EXPECTED_INDEX_ROWS:
        raise ExperimentError("unigram row count mismatch")
    if any(bucket != sorted(bucket) for bucket in buckets.values()):
        raise ExperimentError("unigram length buckets are not deterministically ordered")
    return vocabulary, dict(buckets), time.perf_counter() - started, len(rows)


def attribute_mechanical_edit(source: str, reference: object, edit: list[Any]) -> dict[str, Any]:
    """Classify an applied edit by scorer token keys, never reference offsets."""
    if not isinstance(reference, str):
        return {"status": "unresolved", "reason": "reference-unavailable"}
    try:
        isolated_output = apply_edits(source, [tuple(edit)])
        isolated = edits(source, isolated_output)
        gold = edits(source, reference)
    except (TypeError, ValueError, AssertionError) as exc:
        return {"status": "unresolved", "reason": "scorer-failure", "detail": str(exc)}
    if len(isolated) != 1:
        return {
            "status": "unresolved",
            "reason": "isolated-edit-count",
            "isolated_edit_count": len(isolated),
        }
    unit = isolated[0]
    if unit["start"] != int(edit[0]) or unit["end"] != int(edit[1]):
        return {"status": "unresolved", "reason": "isolated-edit-span-incompatible"}
    status = (
        "exact_reference"
        if edit_key(unit) in {edit_key(item) for item in gold}
        else "non_reference"
    )
    return {
        "status": status,
        "reason": "token-edit-key-membership",
        "isolated_edit_key": list(edit_key(unit)),
        "gold_edit_count": len(gold),
    }


def calculate_case(
    phase: str,
    pair: Mapping[str, Any],
    vocabulary: set[str],
    buckets: Mapping[int, list[str]],
    configuration_sha: str,
) -> dict[str, Any]:
    dataset = pair["dataset"]
    saved = pair["saved"]
    detector = saved["detector"]
    admitted = entering_targets(detector)
    mechanical_targets: list[dict[str, Any]] = []
    mechanical_edits: list[list[Any]] = []
    lookup_seconds = 0.0
    for candidate, policy in admitted:
        target_text = candidate.get("text")
        if not isinstance(target_text, str):
            raise ExperimentError(
                f"detector target text is invalid: {phase}/{pair['dataset']['index']}"
            )
        lookup_form = target_text.casefold()
        bucket = buckets.get(len(lookup_form), ())
        started = time.perf_counter()
        candidates = qualifying_candidates(lookup_form, bucket)
        lookup_seconds += time.perf_counter() - started
        detail: dict[str, Any] = {
            "candidate": candidate,
            "english": policy,
            "lookup_form": lookup_form,
            "bucket_size": len(bucket),
            "lookup_comparisons": len(bucket),
            "candidate_count": len(candidates),
            "candidate_forms": candidates,
            "cardinality": "C=0" if not candidates else "C=1" if len(candidates) == 1 else "C>1",
            "gate": None,
            "accepted": False,
        }
        if len(candidates) == 1:
            gate = mechanical_substitution(
                str(saved["input"]), candidate, candidates[0], vocabulary
            )
            detail["gate"] = gate
            detail["accepted"] = bool(gate.get("accepted"))
            if gate.get("accepted"):
                edit = gate.get("edit")
                if not isinstance(edit, list) or len(edit) != 3:
                    raise ExperimentError("accepted mechanical gate lacks edit")
                mechanical_edits.append(edit)
        mechanical_targets.append(detail)
    try:
        projected = project_saved_case(str(saved["input"]), saved, mechanical_edits)
    except (ValueError, KeyError, TypeError) as exc:
        raise ExperimentError(
            f"saved fallback cannot compose: {phase}/{pair['dataset']['index']}"
        ) from exc
    new_result = {
        "id": saved["id"],
        "index": saved["index"],
        "method": "M2",
        "input": saved["input"],
        "input_sha256": saved["input_sha256"],
        "detector": saved["detector"],
        "decisions": projected["decisions"],
        "calls": projected["calls"],
        "edits": projected["edits"],
        "output": projected["output"],
        "operational_failure": projected["operational_failure"],
        "wall_seconds": 0.0,
    }
    for target in mechanical_targets:
        if not target["accepted"]:
            continue
        gate_edit = (target.get("gate") or {}).get("edit")
        target["applied"] = isinstance(gate_edit, list) and any(
            gate_edit == edit for edit in new_result["edits"]
        )
        if target["applied"]:
            target["attribution"] = attribute_mechanical_edit(
                str(saved["input"]), dataset.get("reference"), gate_edit
            )
    approved = {
        candidate_key(decision["candidate"])
        for decision in saved["decisions"]
        if isinstance(decision, dict) and isinstance(decision.get("candidate"), dict)
    }
    for edit in new_result["edits"]:
        if (edit[0], edit[1], str(saved["input"])[edit[0] : edit[1]]) not in approved and not any(
            edit == accepted_edit for accepted_edit in mechanical_edits
        ):
            raise ExperimentError("new edit lies outside approved original-coordinate spans")
    intervals = protected_intervals(str(saved["input"]))
    protected_differences = sum(
        is_protected(int(edit[0]), int(edit[1]), intervals) for edit in new_result["edits"]
    )
    if protected_differences:
        raise ExperimentError("new edit intersects protected content")
    if (
        apply_edits(str(saved["input"]), [tuple(edit) for edit in new_result["edits"]])
        != new_result["output"]
    ):
        raise ExperimentError("new output does not reproduce exact patch composition")
    return {
        "schema_version": 1,
        "configuration_sha256": configuration_sha,
        "phase": phase,
        "index": dataset["index"],
        "id": dataset["id"],
        "dataset": dataset,
        "baseline": saved,
        "mechanical": {
            "targets": mechanical_targets,
            "lookup_seconds": lookup_seconds,
            "lookup_comparisons": sum(
                target["lookup_comparisons"] for target in mechanical_targets
            ),
            "accepted_targets": sum(bool(target["accepted"]) for target in mechanical_targets),
        },
        "new": new_result,
        "integrity": {
            "protected_differences": protected_differences,
            "outside_span_differences": 0,
        },
    }


def load_or_calculate_case(
    path: Path,
    phase: str,
    pair: Mapping[str, Any],
    vocabulary: set[str],
    buckets: Mapping[int, list[str]],
    configuration_sha: str,
) -> dict[str, Any]:
    if path.exists():
        if path.is_symlink():
            raise ExperimentError(f"case record is a symlink: {path.name}")
        record = read_json(path)
        if not isinstance(record, dict) or record.get("configuration_sha256") != configuration_sha:
            raise ExperimentError(
                f"existing case record does not match frozen configuration: {path.name}"
            )
        if record.get("phase") != phase or record.get("index") != pair["dataset"].get("index"):
            raise ExperimentError(f"existing case identity mismatch: {path.name}")
        return record
    record = calculate_case(phase, pair, vocabulary, buckets, configuration_sha)
    write_immutable(path, record)
    return record


def build_configuration(
    scratch: Path,
    input_manifest: Mapping[str, Any],
    baseline: Mapping[str, Any],
    uv_indices: set[int],
    module_sha: str,
    driver_sha: str,
    scorer_sha: str,
    patching_sha: str,
    implementation: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "run_id": RUN_ID,
        "status": "FROZEN_BEFORE_EXPERIMENTAL_CALCULATION",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "implementation_head": implementation["implementation_head"],
        "implementation_branch": implementation["branch"],
        "source_identity": {
            "dataset_rows": {phase: count for phase, count in PHASES.items()},
            "paired_rows": sum(PHASES.values()),
            "staged_file_identities": {
                key: value for key, value in input_manifest.items() if key != "m2_records"
            },
            "m2_record_count": input_manifest["m2_record_count"],
            "uv_audit_rows": len(uv_indices),
            "uv_indices_sha256": hashlib.sha256(
                ("\n".join(str(item) for item in sorted(uv_indices)) + "\n").encode()
            ).hexdigest(),
        },
        "code_identity": {
            "one_substitution_sha256": module_sha,
            "driver_sha256": driver_sha,
            "scorer_sha256": scorer_sha,
            "patching_sha256": patching_sha,
            "head_blobs": implementation["head_blobs"],
        },
        "baseline_identity": {
            "configuration_sha256": EXPECTED_INPUTS["baseline-configuration.json"][1],
            "results_sha256": EXPECTED_INPUTS["baseline-results.json"][1],
            "method": "M2",
            "validated": True,
            "summary": baseline,
        },
        "algorithm": {
            "english_first": "review_suppressed targets bypass before the mechanical stage",
            "entry": "detector-selected candidate with original unigram state exactly UNAVAILABLE",
            "lookup": (
                "target.casefold() against every vocabulary form in the exact Python len bucket"
            ),
            "candidate_rule": (
                "same Unicode code-point length; exactly one difference; both differing "
                "code points alphabetic; all other code points identical"
            ),
            "cardinality": "C=0 falls through; C=1 may continue; C>1 falls through",
            "forbidden_selection": (
                "no frequency, context, u/v, morphology, normalization, sorting, or model tie-break"
            ),
            "case": "existing symmetric initial-case restoration",
            "gates": (
                "existing mechanical gate followed by independent one-word EXACT unigram membership"
            ),
            "patch": "original-coordinate exact patch; document failure remains fail-closed",
            "fallback": (
                "saved first/retry decisions are reused for every unresolved target "
                "without resampling"
            ),
        },
        "unicode": {
            "semantics": "Python string code points",
            "normalization": "none",
            "grapheme_partial_targets": "gate failure/unchanged",
        },
        "call_policy": {
            "live_model_calls": 0,
            "live_network_calls": 0,
            "saved_calls_reused_as_projection": True,
            "mechanical_targets_consume_first_retry_validator_confirmation": False,
        },
        "no_tuning_or_resampling": True,
        "frequency_used_for_selection": False,
        "private_evidence_root": str(scratch),
    }


def safe_score(summary: Mapping[str, Any]) -> dict[str, Any]:
    keys = (
        "N",
        "reference_N",
        "error_N",
        "gold_edits",
        "tp",
        "fp",
        "fn",
        "precision",
        "recall",
        "F0.5",
        "changed_examples",
        "unchanged_examples",
        "exact_reference_success",
        "exact_error_corrections",
        "unchanged_errors",
        "nonreference_changes",
        "operational_failures",
        "detector_candidates",
        "english_suppressions",
        "first_review_calls",
        "retry_calls",
        "model_calls",
        "accepted_edits",
        "accepted_retry_edits",
        "failed_corrective_retries",
        "source_words",
        "source_tokens",
    )
    return {key: summary.get(key) for key in keys}


def view_summary(
    pairs: list[dict[str, Any]], records: list[dict[str, Any]], indices: Iterable[int] | None = None
) -> dict[str, Any]:
    selected = set(indices) if indices is not None else None
    selected_pairs = [
        pair for pair in pairs if selected is None or pair["dataset"].get("index") in selected
    ]
    selected_records = [
        record for record in records if selected is None or record.get("index") in selected
    ]
    baseline_rows = [
        row_metrics(pair["dataset"], pair["baseline"], "M2") for pair in selected_pairs
    ]
    new_rows = [row_metrics(record["dataset"], record["new"], "M2") for record in selected_records]
    return {
        "rows": len(selected_pairs),
        "baseline": safe_score(summarize(baseline_rows)),
        "new": safe_score(summarize(new_rows)),
    }


def aggregate(
    pairs_by_phase: Mapping[str, list[dict[str, Any]]],
    records_by_phase: Mapping[str, list[dict[str, Any]]],
    uv_indices: set[int],
    vocabulary_seconds: float,
    vocabulary_rows: int,
) -> dict[str, Any]:
    def new_call_counts(result: Mapping[str, Any]) -> dict[str, int]:
        decisions = result.get("decisions")
        calls = result.get("calls")
        if not isinstance(decisions, list) or not isinstance(calls, list):
            raise ExperimentError("projected result lacks call/decision arrays")
        return {
            "first": sum(
                isinstance(item, dict) and isinstance(item.get("first"), dict) for item in decisions
            ),
            "retry": sum(
                isinstance(item, dict) and isinstance(item.get("retry"), dict) for item in decisions
            ),
            "total": len(calls),
        }

    def one_view(
        phase: str,
        pairs: list[dict[str, Any]],
        records: list[dict[str, Any]],
        selected_indices: set[int] | None,
        view_name: str,
    ) -> dict[str, Any]:
        selected = [
            (pair, record)
            for pair, record in zip(pairs, records, strict=True)
            if selected_indices is None or pair["dataset"].get("index") in selected_indices
        ]
        selected_pairs = [pair for pair, _ in selected]
        selected_records = [record for _, record in selected]
        baseline_rows = [
            row_metrics(pair["dataset"], pair["baseline"], "M2") for pair in selected_pairs
        ]
        new_rows = [
            row_metrics(record["dataset"], record["new"], "M2") for record in selected_records
        ]
        baseline_score = safe_score(summarize(baseline_rows))
        new_score = safe_score(summarize(new_rows))
        stage: Counter[str] = Counter()
        mechanical: Counter[str] = Counter()
        calls: Counter[str] = Counter()
        failures: Counter[str] = Counter()
        integrity: Counter[str] = Counter()
        for _pair, record in selected:
            saved = record["baseline"]
            new = record["new"]
            base_call = call_counts(saved)
            projected_call = new_call_counts(new)
            for key in ("first", "retry", "total"):
                calls[f"baseline_{key}"] += base_call[key]
                calls[f"projected_{key}"] += projected_call[key]
                calls[f"avoided_{key}"] += base_call[key] - projected_call[key]
            baseline_failed = bool(saved["operational_failure"])
            projected_failed = bool(new["operational_failure"])
            failures["baseline"] += baseline_failed
            failures["projected"] += projected_failed
            failures["avoided"] += baseline_failed and not projected_failed
            failures["introduced"] += not baseline_failed and projected_failed
            integrity["protected_differences"] += record["integrity"]["protected_differences"]
            integrity["outside_span_differences"] += record["integrity"]["outside_span_differences"]
            targets = record["mechanical"]["targets"]
            stage["stage_entering_oov_targets"] += len(targets)
            stage["C=0"] += sum(target["cardinality"] == "C=0" for target in targets)
            stage["C=1"] += sum(target["cardinality"] == "C=1" for target in targets)
            stage["C>1"] += sum(target["cardinality"] == "C>1" for target in targets)
            stage["prior_english_suppressions"] += sum(
                bool(item.get("review_suppressed"))
                for item in saved["detector"].get("english", [])
                if isinstance(item, dict)
            )
            for target in targets:
                if target["cardinality"] == "C=1" and not target["accepted"]:
                    reason = str((target.get("gate") or {}).get("reason"))
                    mechanical[f"unique_rejected_{reason}"] += 1
                if not target["accepted"]:
                    continue
                mechanical["accepted_unique_targets"] += 1
                if not target.get("applied"):
                    mechanical["rolled_back_by_failure"] += 1
                    continue
                mechanical["applied_mechanical_edits"] += 1
                attribution = target.get("attribution", {})
                status = attribution.get("status")
                if status == "exact_reference":
                    mechanical["exact_reference_edits"] += 1
                elif status == "non_reference":
                    mechanical["nonreference_edits"] += 1
                else:
                    mechanical["unresolved_attribution"] += 1
            applied = sum(bool(target.get("applied")) for target in targets)
            mechanical["fallback_edits"] += max(0, len(new["edits"]) - applied)
            mechanical["lookup_comparisons"] += int(
                record["mechanical"].get("lookup_comparisons", 0)
            )
        applied = mechanical["applied_mechanical_edits"]
        resolved = mechanical["exact_reference_edits"] + mechanical["nonreference_edits"]
        mechanical["reference_defined_applied_mechanical_edits"] = resolved
        mechanical["precision_denominator"] = resolved
        mechanical["precision"] = (
            mechanical["exact_reference_edits"] / resolved if resolved else None
        )
        gold_edits = int(new_score["gold_edits"] or 0)
        mechanical["spelling_gold_recall_denominator"] = (
            gold_edits if phase == "dassle-spelling" else None
        )
        mechanical["spelling_gold_recall"] = (
            mechanical["exact_reference_edits"] / gold_edits
            if phase == "dassle-spelling" and gold_edits
            else None
        )
        entering = stage["stage_entering_oov_targets"]
        mechanical["stage_entering_resolvable_fraction"] = (
            mechanical["accepted_unique_targets"] / entering if entering else None
        )
        runtime = {
            "candidate_lookup_seconds": sum(
                float(record["mechanical"]["lookup_seconds"]) for record in selected_records
            ),
            "candidate_lookup_comparisons": mechanical["lookup_comparisons"],
            "reused_model_seconds": sum(
                float(call.get("http_seconds") or 0)
                for record in selected_records
                for call in record["baseline"].get("calls", [])
                if isinstance(call, dict)
            ),
        }
        return {
            "view": view_name,
            "rows": len(selected),
            "baseline": baseline_score,
            "new": new_score,
            "stage": dict(stage),
            "mechanical": dict(mechanical),
            "calls": dict(calls),
            "failures": dict(failures),
            "integrity": dict(integrity),
            "runtime": runtime,
        }

    views: dict[str, Any] = {}
    for phase, pairs in pairs_by_phase.items():
        records = records_by_phase[phase]
        phase_views: dict[str, Any] = {"all": one_view(phase, pairs, records, None, "all")}
        if phase == "dassle-spelling":
            phase_views["initial_uv"] = one_view(phase, pairs, records, uv_indices, "initial_uv")
            phase_views["without_initial_uv"] = one_view(
                phase,
                pairs,
                records,
                set(range(1, len(pairs) + 1)) - uv_indices,
                "without_initial_uv",
            )
        views[phase] = phase_views
    all_views = {
        f"{phase}/{view_name}": view
        for phase, phase_views in views.items()
        for view_name, view in phase_views.items()
    }
    return {
        "views": views,
        "by_view": all_views,
        "integrity": {
            "protected_differences": sum(
                view["integrity"]["protected_differences"]
                for view in (phase["all"] for phase in views.values())
            ),
            "outside_span_differences": sum(
                view["integrity"]["outside_span_differences"]
                for view in (phase["all"] for phase in views.values())
            ),
        },
        "runtime": {
            "vocabulary_load_seconds": vocabulary_seconds,
            "vocabulary_rows": vocabulary_rows,
            "candidate_lookup_seconds": sum(
                float(record["mechanical"]["lookup_seconds"])
                for records in records_by_phase.values()
                for record in records
            ),
            "candidate_lookup_comparisons": sum(
                int(record["mechanical"].get("lookup_comparisons", 0))
                for records in records_by_phase.values()
                for record in records
            ),
            "reused_model_seconds": sum(
                float(call.get("http_seconds") or 0)
                for records in records_by_phase.values()
                for record in records
                for call in record["baseline"].get("calls", [])
                if isinstance(call, dict)
            ),
            "actual_model_calls": 0,
            "actual_network_calls": 0,
        },
    }


def public_projection(
    configuration: Mapping[str, Any],
    metrics: Mapping[str, Any],
    private_results_sha: str,
    private_manifest_sha: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    sources = configuration["source_identity"]["staged_file_identities"]
    public_config = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "status": "COMPLETE_OFFLINE_PAIRED_CALCULATION",
        "implementation_head": configuration["implementation_head"],
        "question": (
            "Can a complete unique one-code-point unigram lane resolve selected Slovene OOV "
            "targets before review while preserving controlled text?"
        ),
        "source_identity": {
            "datasets": configuration["source_identity"]["dataset_rows"],
            "paired_rows": configuration["source_identity"]["paired_rows"],
            "file_sha256": {key: value["sha256"] for key, value in sources.items()},
            "uv_audit_rows": configuration["source_identity"]["uv_audit_rows"],
        },
        "baseline_identity": configuration["baseline_identity"],
        "algorithm": configuration["algorithm"],
        "unicode": configuration["unicode"],
        "call_policy": configuration["call_policy"],
        "no_tuning_or_resampling": True,
        "private_evidence_sha256": {
            "results": private_results_sha,
            "manifest": private_manifest_sha,
        },
    }
    public_result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "status": "COMPLETE_OFFLINE_PAIRED_CALCULATION",
        "implementation_head": configuration["implementation_head"],
        "configuration_sha256": hashlib.sha256(canonical_bytes(public_config)).hexdigest(),
        "private_evidence_sha256": {
            "results": private_results_sha,
            "manifest": private_manifest_sha,
        },
        "metrics": metrics,
        "limitations": [
            (
                "This is one frozen DASSLE spelling/preservation experiment, not a general "
                "Slovenian or production claim."
            ),
            (
                "Supplied reference scoring can penalize valid alternatives; non-reference "
                "edits are not semantic harm labels."
            ),
            (
                "Saved Qwen records are projected for unresolved targets; actual experiment "
                "model and network calls are zero."
            ),
        ],
    }
    return public_config, public_result


def render_public_report(configuration: Mapping[str, Any], result: Mapping[str, Any]) -> str:
    metrics = result["metrics"]
    spelling = metrics["views"]["dassle-spelling"]
    preservation = metrics["views"]["dassle-spelling-preservation"]["all"]

    def view_lines(label: str, view: Mapping[str, Any], *, is_spelling: bool) -> list[str]:
        stage = view["stage"]
        mechanical = view["mechanical"]
        baseline = view["baseline"]
        new = view["new"]
        calls = view["calls"]
        failures = view["failures"]
        lines = [
            f"### {label}",
            f"- Stage-entering OOV / English suppressed: "
            f"{stage.get('stage_entering_oov_targets', 0)} / "
            f"{stage.get('prior_english_suppressions', 0)}",
            f"- C=0 / C=1 / C>1: {stage.get('C=0', 0)} / "
            f"{stage.get('C=1', 0)} / {stage.get('C>1', 0)}",
            f"- Unique accepted / applied / rolled back: "
            f"{mechanical.get('accepted_unique_targets', 0)} / "
            f"{mechanical.get('applied_mechanical_edits', 0)} / "
            f"{mechanical.get('rolled_back_by_failure', 0)}",
            f"- Exact-reference / non-reference / unresolved: "
            f"{mechanical.get('exact_reference_edits', 0)} / "
            f"{mechanical.get('nonreference_edits', 0)} / "
            f"{mechanical.get('unresolved_attribution', 0)}",
            f"- Mechanical precision (denominator "
            f"{mechanical.get('precision_denominator')}): "
            f"{mechanical.get('precision')}",
            f"- Fallback Qwen edits: {mechanical.get('fallback_qwen_edits', 0)}; "
            f"unchanged/unresolved targets: "
            f"{stage.get('unchanged_or_unresolved_targets', 0)}",
            f"- Lookup comparisons: {view['runtime'].get('candidate_lookup_comparisons', 0)}",
            f"- Calls baseline first/retry/total: "
            f"{calls.get('baseline_first', 0)} / {calls.get('baseline_retry', 0)} / "
            f"{calls.get('baseline_total', 0)}",
            f"- Calls projected first/retry/total: "
            f"{calls.get('projected_first', 0)} / {calls.get('projected_retry', 0)} / "
            f"{calls.get('projected_total', 0)}",
            f"- Calls avoided first/retry/total: "
            f"{calls.get('avoided_first', 0)} / {calls.get('avoided_retry', 0)} / "
            f"{calls.get('avoided_total', 0)}",
            f"- Failures baseline/projected/avoided/introduced: "
            f"{failures.get('baseline', 0)} / {failures.get('projected', 0)} / "
            f"{failures.get('avoided', 0)} / {failures.get('introduced', 0)}",
            f"- Score baseline TP/FP/FN: {baseline['tp']} / {baseline['fp']} / {baseline['fn']}",
            f"- Score new TP/FP/FN: {new['tp']} / {new['fp']} / {new['fn']}",
            f"- Score baseline precision/recall/F0.5: "
            f"{baseline['precision']} / {baseline['recall']} / {baseline['F0.5']}",
            f"- Score new precision/recall/F0.5: "
            f"{new['precision']} / {new['recall']} / {new['F0.5']}",
        ]
        if is_spelling:
            lines.insert(
                6,
                f"- Spelling-gold recall (denominator "
                f"{mechanical.get('spelling_gold_recall_denominator')}): "
                f"{mechanical.get('spelling_gold_recall')}",
            )
        else:
            lines.insert(6, "- Spelling-gold recall: n/a for preservation")
        return lines

    lines = [
        "# 007-h unique one-letter unigram substitution",
        "",
        "EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.",
        "",
        "One owner-authorized offline paired calculation over frozen DASSLE data.",
        "English suppression precedes lookup; C>1 falls through; no frequency,",
        "ordering, context, u/v, normalization, or model tie-break is used.",
        "",
        "## Frozen identity",
        "",
        f"- Paired records: {configuration['source_identity']['paired_rows']} "
        "(1,487 spelling; 1,486 preservation).",
        f"- Caller-verified committed implementation: {configuration['implementation_head']}.",
        f"- Baseline configuration: {configuration['baseline_identity']['configuration_sha256']}.",
        f"- Baseline results: {configuration['baseline_identity']['results_sha256']}.",
        f"- Exact unigram rows loaded once: {metrics['runtime']['vocabulary_rows']}.",
        "- Actual experiment model/network calls: 0 / 0.",
        "",
        "## Required views",
        "",
    ]
    lines.extend(view_lines("Spelling all", spelling["all"], is_spelling=True))
    lines.extend(
        view_lines(
            "Initial-u/v (75 frozen identities)",
            spelling["initial_uv"],
            is_spelling=True,
        )
    )
    lines.extend(
        view_lines(
            "Spelling without initial-u/v",
            spelling["without_initial_uv"],
            is_spelling=True,
        )
    )
    lines.extend(view_lines("Preservation all", preservation, is_spelling=False))
    lines.extend(
        [
            "",
            "## Runtime and integrity",
            "",
            f"- Vocabulary load seconds: {metrics['runtime']['vocabulary_load_seconds']}.",
            f"- Candidate lookup seconds: {metrics['runtime']['candidate_lookup_seconds']}.",
            f"- Reused saved model time: {metrics['runtime']['reused_model_seconds']}.",
            f"- Protected/outside-span differences: "
            f"{metrics['integrity']['protected_differences']} / "
            f"{metrics['integrity']['outside_span_differences']}.",
            f"- Preservation changed cases/edits: "
            f"{preservation['new']['changed_examples']} / "
            f"{preservation['new']['introduced_edits']}.",
            "",
            "## Interpretation and stop",
            "",
            "The resolvable fraction, accuracy, call savings, preservation effect,",
            "u/v ablation, and frozen-fallback end-to-end scores are above.",
            "Reference scoring can penalize valid alternatives; non-reference edits",
            "are not semantic harm labels. Results do not authorize integration,",
            "merge, release, deployment, or live inference.",
        ]
    )
    return "\n".join(lines) + "\n"


def snapshot_prior_public_artifacts(repo_root: Path) -> dict[str, str]:
    """Hash existing public archive files so this run can prove they stayed fixed."""
    snapshot: dict[str, str] = {}
    for relative_root in PUBLIC_ARCHIVE_ROOTS:
        root = repo_root / relative_root
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and not path.is_symlink():
                snapshot[str(path.relative_to(repo_root))] = sha256_file(path)
    return snapshot


def compare_prior_public_artifacts(before: Mapping[str, str], after: Mapping[str, str]) -> None:
    """Allow only the three predeclared 007-h public outputs to be added."""
    before_paths = set(before)
    after_paths = set(after)
    changed = sorted(path for path in before_paths & after_paths if before[path] != after[path])
    deleted = sorted(before_paths - after_paths)
    unexpected = sorted(after_paths - before_paths - PUBLIC_OUTPUT_PATHS)
    authorized_preexisting = sorted(before_paths & PUBLIC_OUTPUT_PATHS)
    authorized_missing = sorted(PUBLIC_OUTPUT_PATHS - after_paths)
    if changed or deleted or unexpected or authorized_preexisting or authorized_missing:
        details = {
            "changed": changed,
            "deleted": deleted,
            "unexpected_new": unexpected,
            "authorized_preexisting": authorized_preexisting,
            "authorized_missing": authorized_missing,
        }
        raise ExperimentError(
            "prior public artifact boundary violation: " + json.dumps(details, sort_keys=True)
        )


def run(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    scratch = Path(args.scratch).resolve()
    source_root = Path(args.source_root).resolve()
    uv_root = Path(args.uv_root).resolve()
    index_source = Path(args.index_source).resolve()
    prior_public_snapshot = snapshot_prior_public_artifacts(repo_root)
    implementation = verify_committed_implementation(repo_root, args.expected_implementation_head)
    input_manifest = verify_staged_inputs(scratch, source_root, uv_root, index_source)
    write_status(
        scratch / "RUN-STATUS.json", {"status": "PAIRING_AND_BASELINE_VALIDATION", "run_id": RUN_ID}
    )
    pairs = load_pairs(scratch)
    baseline = validate_baseline_replay(pairs)
    spelling_pairs = pairs["dassle-spelling"]
    uv_indices, uv_mapping = verify_uv_mapping(scratch, spelling_pairs)
    module_path = repo_root / "research/one_substitution.py"
    driver_path = repo_root / "research/tools/run_one_substitution.py"
    scorer_path = repo_root / "research/curated/historical_scoring.py"
    patching_path = repo_root / "research/curated/patching.py"
    configuration = build_configuration(
        scratch,
        input_manifest,
        baseline,
        uv_indices,
        sha256_file(module_path),
        sha256_file(driver_path),
        sha256_file(scorer_path),
        sha256_file(patching_path),
        implementation,
    )
    configuration_path = scratch / "CONFIGURATION.json"
    configuration_sha = write_immutable(configuration_path, configuration)
    if sha256_file(configuration_path) != configuration_sha:
        raise ExperimentError("frozen configuration identity cannot be verified")
    write_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "EXPERIMENTAL_CALCULATION",
            "configuration_sha256": configuration_sha,
            "run_id": RUN_ID,
        },
    )
    vocabulary, buckets, vocabulary_seconds, vocabulary_rows = load_vocabulary(
        scratch / "inputs/index/index.sqlite"
    )
    records_by_phase: dict[str, list[dict[str, Any]]] = {}
    for phase, phase_pairs in pairs.items():
        records: list[dict[str, Any]] = []
        for pair in phase_pairs:
            case_path = scratch / "cases" / phase / f"{pair['dataset']['index']:06d}.json"
            records.append(
                load_or_calculate_case(
                    case_path, phase, pair, vocabulary, buckets, configuration_sha
                )
            )
        records_by_phase[phase] = records
    metrics = aggregate(pairs, records_by_phase, uv_indices, vocabulary_seconds, vocabulary_rows)
    private_results = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "configuration_sha256": configuration_sha,
        "baseline": baseline,
        "uv_mapping": uv_mapping,
        "metrics": metrics,
        "status": "COMPLETE_OFFLINE_PAIRED_CALCULATION",
    }
    private_results_path = scratch / "RESULTS.json"
    private_results_sha = write_immutable(private_results_path, private_results)
    private_report = (
        "# Private 007-h report\n\n"
        + json.dumps(private_results, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n"
    )
    private_report_sha = write_private_bytes(scratch / "REPORT.md", private_report.encode("utf-8"))
    manifest = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "input_manifest_sha256": sha256_file(scratch / "INPUT-MANIFEST.json"),
        "configuration_sha256": configuration_sha,
        "private_results_sha256": private_results_sha,
        "private_report_sha256": private_report_sha,
        "case_count": sum(len(rows) for rows in records_by_phase.values()),
        "case_record_sha256": {
            f"{phase}/{record['index']:06d}": sha256_file(
                scratch / "cases" / phase / f"{record['index']:06d}.json"
            )
            for phase, records in records_by_phase.items()
            for record in records
        },
        "status": "COMPLETE_OFFLINE_PAIRED_CALCULATION",
    }
    private_manifest_sha = write_immutable(scratch / "MANIFEST.json", manifest)
    public_config, public_result = public_projection(
        configuration, metrics, private_results_sha, private_manifest_sha
    )
    public_result["configuration_sha256"] = hashlib.sha256(
        canonical_bytes(public_config)
    ).hexdigest()
    public_config_path = (
        repo_root / "research/configs/007-h-unique-one-letter-unigram-substitution.json"
    )
    public_result_path = (
        repo_root / "research/results/007-h-unique-one-letter-unigram-substitution.json.gz"
    )
    public_report_path = (
        repo_root / "research/reports/007-h-unique-one-letter-unigram-substitution.md"
    )
    immutable_bytes(public_config_path, canonical_bytes(public_config))
    compressed = gzip.compress(canonical_bytes(public_result), mtime=0)
    immutable_bytes(public_result_path, compressed)
    immutable_bytes(
        public_report_path, render_public_report(configuration, public_result).encode("utf-8")
    )
    compare_prior_public_artifacts(
        prior_public_snapshot, snapshot_prior_public_artifacts(repo_root)
    )
    write_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "COMPLETE_OFFLINE_PAIRED_CALCULATION",
            "run_id": RUN_ID,
            "configuration_sha256": configuration_sha,
            "manifest_sha256": private_manifest_sha,
            "private_results_sha256": private_results_sha,
            "actual_model_calls": 0,
            "actual_network_calls": 0,
        },
    )
    return {
        "status": "COMPLETE_OFFLINE_PAIRED_CALCULATION",
        "configuration_sha256": configuration_sha,
        "private_manifest_sha256": private_manifest_sha,
        "private_results_sha256": private_results_sha,
        "public_config_sha256": sha256_file(public_config_path),
        "public_result_sha256": sha256_file(public_result_path),
        "public_report_sha256": sha256_file(public_report_path),
        "paired_rows": sum(PHASES.values()),
        "actual_model_calls": 0,
        "actual_network_calls": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--uv-root", type=Path, required=True)
    parser.add_argument("--index-source", type=Path, required=True)
    parser.add_argument("--expected-implementation-head", required=True)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(run(args), sort_keys=True))
    except ExperimentError as exc:
        print(json.dumps({"status": "FAILED", "reason": str(exc)}, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
