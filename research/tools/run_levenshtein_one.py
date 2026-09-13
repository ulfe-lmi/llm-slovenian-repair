"""Run the bounded 007-j standard-Levenshtein-one experiment.

The driver freezes the 007-i private inputs, enumerates the complete
distance-one union, reuses only byte-identical substitution observations, and
dispatches the new insertion/deletion population through the unchanged
validator protocol.  Model payloads and row-level evidence stay in the
caller-supplied native private root.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import json
import os
import stat
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from research import contextual_validator as protocol
from research import levenshtein_one as distance_one
from research.tools import run_contextual_validator as validator_driver
from research.tools import run_one_substitution as baseline_driver

RUN_ID = "007-j"
EXPERIMENT_ID = "007-j-levenshtein-one-contextual-validator"
PHASES = {"dassle-spelling": 1_487, "dassle-spelling-preservation": 1_486}
EXPECTED_ENTERING = {"dassle-spelling": 2_001, "dassle-spelling-preservation": 920}
EXPECTED_CANDIDATES = {"dassle-spelling": 826, "dassle-spelling-preservation": 209}
EXPECTED_OPERATIONS = {"SUBSTITUTION": 542, "INSERTION": 172, "DELETION": 321}
EXPECTED_REUSED = 542
EXPECTED_FRESH = 493
EXPECTED_TOTAL = EXPECTED_REUSED + EXPECTED_FRESH
EXPECTED_PRIOR_CONFIG = "0cbc4738f23bed247fac6a3cd2203086956329eea9ca23ffb8bf8e1351165d21"
EXPECTED_PRIOR_CANDIDATES = "70544b1dec158f1e72cfaae8fb2547d9ba6ea22c3cd7934e0b7341bce8617854"
EXPECTED_PRIOR_RESULTS = "913572ae5d16ba29ab8afd6ea59a1dc3f03de90d40136891ea1637eba16f92f9"
EXPECTED_PRIOR_MANIFEST = "04f66e96d4feddaea520c1ccb27724dc5417b4f6535bbe85a5c6cac904395cb0"
EXPECTED_PRIOR_CASES = "4490d7c1e14b28369217d06915bc1fce936160108de615f22f59032a803a46ef"
EXPECTED_PRIOR_REQUEST_TREE = "d46b47754e2ba158ea099bfe556a84164e534610233426819d9114a455aea945"
EXPECTED_PROFILE = "c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60"
EXPECTED_PROMPT = protocol.FROZEN_PROMPT_SHA256
EXPECTED_IMPLEMENTATION_BASE = "a4d3592e25a792dd3f8d65a729c54a08032a88e3"
NATIVE_RUNTIME_PARENT = Path("/").joinpath(
    "home",
    "ubuntu",
    ".local",
    "share",
    "llm-slovenian-repair",
    "research-runtime-20260911.YJemoq",
)
SCRATCH_NAME_PREFIX = EXPERIMENT_ID + "-recovery."
EXPECTED_REQUEST_FIELDS = [
    "model",
    "stream",
    "store",
    "input",
    "include_reasoning",
    "reasoning",
]
EXPECTED_PARSER = {
    "status": "completed",
    "assistant_output_text_fields": 1,
    "choices": sorted(protocol.CHOICES),
    "surrounding_whitespace_only": True,
    "duplicate_json_keys": "reject",
    "token_accounting": "input/output/reasoning nonnegative integers",
}

TRANSITION_EXPECTED = {
    "dassle-spelling": {
        "C=0 -> C=0": 524,
        "C=0 -> C=1": 403,
        "C=0 -> C>1": 84,
        "C=1 -> same unique candidate": 423,
        "C=1 -> different unique candidate": 0,
        "C=1 -> C>1": 148,
        "C>1 -> C=1": 0,
        "C>1 -> C>1": 419,
    },
    "dassle-spelling-preservation": {
        "C=0 -> C=0": 480,
        "C=0 -> C=1": 90,
        "C=0 -> C>1": 18,
        "C=1 -> same unique candidate": 119,
        "C=1 -> different unique candidate": 0,
        "C=1 -> C>1": 45,
        "C>1 -> C=1": 0,
        "C>1 -> C>1": 168,
    },
}


class ExperimentError(RuntimeError):
    """Raised when a frozen boundary or durable identity cannot be proved."""


def canonical_bytes(value: object) -> bytes:
    return protocol.canonical_bytes(value)


def sha256_bytes(value: bytes) -> str:
    return protocol.sha256_bytes(value)


def sha256_file(path: Path) -> str:
    return protocol.sha256_file(path)


def read_json(path: Path) -> Any:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExperimentError(f"invalid private JSON artifact: {path.name}") from exc
    return value


def require_private_dir(path: Path) -> None:
    try:
        info = path.lstat()
    except OSError as exc:
        raise ExperimentError(f"private directory is unavailable: {path}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise ExperimentError(f"private path is not a real directory: {path.name}")
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
        raise ExperimentError(f"private directory ownership/mode mismatch: {path.name}")


def require_private_file(path: Path, expected_sha: str | None = None) -> None:
    try:
        info = path.lstat()
    except OSError as exc:
        raise ExperimentError(f"private file is unavailable: {path.name}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise ExperimentError(f"private path is not a regular file: {path.name}")
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
        raise ExperimentError(f"private file ownership/mode mismatch: {path.name}")
    if expected_sha is not None and sha256_file(path) != expected_sha:
        raise ExperimentError(f"private file hash mismatch: {path.name}")


def immutable_write(path: Path, data: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    require_private_dir(path.parent)
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


def mutable_status(path: Path, value: object) -> None:
    immutable_write(path.with_name("." + path.name + ".status"), canonical_bytes(value))
    os.replace(path.with_name("." + path.name + ".status"), path)
    os.chmod(path, 0o600)
    require_private_file(path)


def source_root_identity(source_root: Path) -> dict[str, str]:
    require_private_dir(source_root)
    for name in ("CONFIGURATION.json", "CANDIDATE-MANIFEST.json", "RESULTS.json", "MANIFEST.json"):
        require_private_file(source_root / name)
    expected = {
        "CONFIGURATION.json": EXPECTED_PRIOR_CONFIG,
        "CANDIDATE-MANIFEST.json": EXPECTED_PRIOR_CANDIDATES,
        "RESULTS.json": EXPECTED_PRIOR_RESULTS,
        "MANIFEST.json": EXPECTED_PRIOR_MANIFEST,
    }
    for name, digest in expected.items():
        require_private_file(source_root / name, digest)
    identity = validator_driver.verify_frozen_request_tree(source_root / "requests")
    if identity["sha256sum_manifest_sha256"] != EXPECTED_PRIOR_REQUEST_TREE:
        raise ExperimentError("007-i request-tree identity changed")
    return {**expected, "request_tree": identity["sha256sum_manifest_sha256"]}


def ensure_scratch(scratch: Path) -> None:
    scratch = scratch.absolute()
    if scratch.parent != NATIVE_RUNTIME_PARENT:
        raise ExperimentError(
            "007-j private root must be directly beneath the native runtime parent"
        )
    require_private_dir(NATIVE_RUNTIME_PARENT)
    if not scratch.name.startswith(SCRATCH_NAME_PREFIX):
        raise ExperimentError("007-j private root name is not a unique recovery root")
    if scratch.exists() or scratch.is_symlink():
        require_private_dir(scratch)
        return
    require_private_dir(scratch.parent)
    scratch.mkdir(mode=0o700)
    require_private_dir(scratch)


def stage_inputs(source_root: Path, scratch: Path) -> None:
    """Copy only the frozen 007-i input/case trees into the new private root."""
    validator_driver.stage_frozen_inputs(source_root, scratch)


def _cardinality(count: int) -> str:
    return "C=0" if count == 0 else "C=1" if count == 1 else "C>1"


def _case_path(root: Path, phase: str, index: int) -> Path:
    return root / "cases" / phase / f"{index:06d}.json"


def is_english_review_suppressed(target: dict[str, Any]) -> bool:
    """Return the frozen English-policy suppression decision for a target."""
    english = target.get("english")
    if not isinstance(english, dict) or type(english.get("review_suppressed")) is not bool:
        raise ExperimentError("frozen target lacks the English suppression decision")
    return english["review_suppressed"]


def build_population(
    records: dict[str, list[dict[str, Any]]],
    vocabulary: set[str],
    buckets: dict[int, list[str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    population: list[dict[str, Any]] = []
    transitions: dict[str, Counter[str]] = {
        phase: Counter({key: 0 for key in TRANSITION_EXPECTED[phase]}) for phase in PHASES
    }
    operation_counts: dict[str, Counter[str]] = {phase: Counter() for phase in PHASES}
    entering_counts: Counter[str] = Counter()
    lookup_seconds = 0.0
    deletion_index = distance_one.build_deletion_signature_index(vocabulary)
    for phase, cases in records.items():
        for case in cases:
            baseline = case.get("baseline")
            targets = case.get("mechanical", {}).get("targets")
            if not isinstance(baseline, dict) or not isinstance(targets, list):
                raise ExperimentError("007-i case lacks frozen baseline targets")
            for ordinal, target in enumerate(targets):
                if not isinstance(target, dict):
                    raise ExperimentError("frozen target is not an object")
                candidate = target.get("candidate")
                if not isinstance(candidate, dict):
                    raise ExperimentError("frozen target lacks candidate/English policy")
                if is_english_review_suppressed(target):
                    continue
                entering_counts[phase] += 1
                start, end, text = (
                    candidate.get("start"),
                    candidate.get("end"),
                    candidate.get("text"),
                )
                if type(start) is not int or type(end) is not int or not isinstance(text, str):
                    raise ExperimentError("frozen target coordinates are invalid")
                original = baseline.get("input")
                if not isinstance(original, str) or original[start:end] != text:
                    raise ExperimentError("frozen target slice is stale")
                lookup = text.casefold()
                all_one_edit_forms = distance_one.distance_one_candidates(
                    lookup, vocabulary, deletion_index=deletion_index
                )
                old_forms = []
                for item in all_one_edit_forms:
                    if item["operation"] != distance_one.SUBSTITUTION:
                        continue
                    differences = [
                        position
                        for position, (left, right) in enumerate(
                            zip(lookup, item["text"], strict=True)
                        )
                        if left != right
                    ]
                    if (
                        len(differences) == 1
                        and lookup[differences[0]].isalpha()
                        and item["text"][differences[0]].isalpha()
                    ):
                        old_forms.append(item["text"])
                frozen_old_forms = target.get("candidate_forms")
                if not isinstance(frozen_old_forms, list) or set(old_forms) != set(
                    frozen_old_forms
                ):
                    raise ExperimentError("007-i substitution identity drift")
                old_cardinality = _cardinality(len(old_forms))
                started = time.monotonic()
                new_forms = distance_one.distance_one_candidates(
                    lookup, vocabulary, deletion_index=deletion_index
                )
                lookup_seconds += time.monotonic() - started
                new_cardinality = _cardinality(len(new_forms))
                if old_cardinality == "C=1" and new_cardinality == "C=1":
                    transition = (
                        "C=1 -> same unique candidate"
                        if old_forms[0] == new_forms[0]["text"]
                        else "C=1 -> different unique candidate"
                    )
                else:
                    transition = f"{old_cardinality} -> {new_cardinality}"
                transitions[phase][transition] += 1
                if len(new_forms) != 1:
                    continue
                new_form = new_forms[0]
                gate = baseline_driver.mechanical_substitution(
                    original, candidate, new_form["text"], vocabulary
                )
                if not gate.get("accepted") or not isinstance(gate.get("edit"), list):
                    raise ExperimentError("new unique candidate failed unchanged mechanical gate")
                edit = gate["edit"]
                population.append(
                    {
                        "phase": phase,
                        "case_index": int(case["index"]),
                        "case_id": case["id"],
                        "target_ordinal": ordinal,
                        "target_start": start,
                        "target_end": end,
                        "candidate": copy.deepcopy(candidate),
                        "candidate_form": new_form["text"],
                        "operation": new_form["operation"],
                        "mechanical_edit": copy.deepcopy(edit),
                        "sentence": original,
                        "reference": case["dataset"].get("reference"),
                    }
                )
                operation_counts[phase][new_form["operation"]] += 1
    if dict(entering_counts) != EXPECTED_ENTERING:
        raise ExperimentError(f"entering population mismatch: {dict(entering_counts)}")
    if {phase: dict(values) for phase, values in transitions.items()} != TRANSITION_EXPECTED:
        raise ExperimentError("candidate transition matrix mismatch")
    if {
        phase: len([item for item in population if item["phase"] == phase]) for phase in PHASES
    } != EXPECTED_CANDIDATES:
        raise ExperimentError("new unique candidate population mismatch")
    if Counter(item["operation"] for item in population) != Counter(EXPECTED_OPERATIONS):
        raise ExperimentError("new operation population mismatch")
    return protocol.ordered_candidates(population), {
        "entering_targets": dict(entering_counts),
        "transition_matrix": {phase: dict(values) for phase, values in transitions.items()},
        "operation_counts": {phase: dict(values) for phase, values in operation_counts.items()},
        "lookup_seconds": lookup_seconds,
        "vocabulary_forms": len(vocabulary),
    }


def prior_population_and_observations(
    source_root: Path,
    records: dict[str, list[dict[str, Any]]],
    vocabulary: set[str],
    buckets: dict[int, list[str]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    old_population = validator_driver.build_population(records, vocabulary, buckets)
    manifest, digest = validator_driver.private_manifest(old_population)
    if digest != EXPECTED_PRIOR_CANDIDATES:
        raise ExperimentError("007-i candidate manifest identity changed")
    old_observations = validator_driver.load_completed_observations(source_root, old_population)
    return (
        old_population,
        old_observations,
        {"candidate_manifest_sha256": digest, "manifest": manifest},
    )


def reuse_observations(
    source_root: Path,
    scratch: Path,
    population: list[dict[str, Any]],
    old_population: list[dict[str, Any]],
    old_observations: dict[str, dict[str, Any]],
    old_configuration: dict[str, Any],
    deployment: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    old_by_id = {protocol.candidate_path_id(item): item for item in old_population}
    reused: dict[str, dict[str, Any]] = {}
    reuse_records: list[dict[str, Any]] = []
    fresh: list[dict[str, Any]] = []
    source_case_hashes: dict[tuple[str, int], str] = {}
    for item in population:
        candidate_id = protocol.candidate_path_id(item)
        old_item = old_by_id.get(candidate_id)
        body = protocol.request_body(
            item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
        )
        request_bytes = canonical_bytes(body)
        old_request = source_root / "requests" / candidate_id / "request.json"
        old_raw = source_root / "requests" / candidate_id / "raw-response.json"
        old_observation = old_observations.get(candidate_id)
        old_request_bytes = old_request.read_bytes() if old_request.is_file() else None
        old_raw_sha256 = sha256_file(old_raw) if old_raw.is_file() else None
        reason = reuse_identity_reason(
            item,
            old_item,
            request_bytes,
            old_request_bytes,
            old_observation,
            old_raw_sha256,
            old_configuration,
            deployment,
        )
        if reason is None:
            target_key = (item["phase"], item["case_index"])
            if target_key not in source_case_hashes:
                source_case_hashes[target_key] = sha256_file(
                    _case_path(source_root, item["phase"], item["case_index"])
                )
            target_dir = scratch / "requests" / candidate_id
            validator_driver.copy_tree_exact(old_request.parent, target_dir)
            reused[candidate_id] = old_observation  # type: ignore[assignment]
            reuse_records.append(
                {
                    "candidate_id": candidate_id,
                    "stable_key": list(protocol.stable_key(item)),
                    "source_case_sha256": source_case_hashes[target_key],
                    "request_sha256": sha256_bytes(request_bytes),
                    "raw_response_sha256": sha256_file(old_raw),
                    "observation_sha256": sha256_file(old_request.parent / "observation.json"),
                    "source": "007-i immutable request/raw/observation",
                    "dispatch_added": False,
                }
            )
        else:
            fresh.append(item)
    if len(reused) != EXPECTED_REUSED or len(fresh) != EXPECTED_FRESH:
        raise ExperimentError(f"reuse/fresh population mismatch: {len(reused)}/{len(fresh)}")
    return reused, reuse_records, fresh


def reuse_identity_reason(
    item: dict[str, Any],
    old_item: dict[str, Any] | None,
    request_bytes: bytes,
    old_request_bytes: bytes | None,
    old_observation: dict[str, Any] | None,
    old_raw_sha256: str | None,
    old_configuration: dict[str, Any],
    deployment: dict[str, Any],
) -> str | None:
    """Return a safe reason when an observation cannot be reused exactly."""
    if old_item is None:
        return "missing-source-candidate"
    if item.get("operation") != "SUBSTITUTION":
        return "operation-is-not-substitution"
    for key in (
        "phase",
        "case_index",
        "case_id",
        "target_ordinal",
        "target_start",
        "target_end",
        "candidate",
        "candidate_form",
        "mechanical_edit",
        "sentence",
    ):
        if old_item.get(key) != item.get(key):
            return "source-candidate-identity-mismatch"
    if old_request_bytes != request_bytes:
        return "request-bytes-mismatch"
    if not isinstance(old_observation, dict):
        return "missing-source-observation"
    if old_observation.get("request_sha256") != sha256_bytes(request_bytes):
        return "observation-request-hash-mismatch"
    if old_raw_sha256 is None or old_observation.get("response_sha256") != old_raw_sha256:
        return "observation-response-hash-mismatch"
    if old_configuration.get("prompt", {}).get("sha256") != EXPECTED_PROMPT:
        return "prompt-identity-mismatch"
    old_deployment = old_configuration.get("deployment")
    if not isinstance(old_deployment, dict):
        return "deployment-identity-mismatch"
    for key in ("model", "profile_sha256", "profile_path", "endpoint", "protocol"):
        if old_deployment.get(key) != deployment.get(key):
            return "deployment-identity-mismatch"
    old_request = old_configuration.get("request")
    if (
        not isinstance(old_request, dict)
        or old_request.get("fields") != EXPECTED_REQUEST_FIELDS
        or old_request.get("stream") is not False
        or old_request.get("store") is not False
        or old_request.get("include_reasoning") is not True
        or old_request.get("reasoning_effort") != protocol.EFFORT
    ):
        return "request-policy-identity-mismatch"
    if old_configuration.get("parser") != EXPECTED_PARSER:
        return "parser-identity-mismatch"
    old_limits = old_configuration.get("limits")
    if (
        not isinstance(old_limits, dict)
        or old_limits.get("timeout_seconds") != protocol.TIMEOUT_SECONDS
        or old_limits.get("response_bound_bytes") != protocol.MAX_RESPONSE_BYTES
        or old_limits.get("attempts_per_candidate") != 1
        or old_limits.get("resampling") is not False
    ):
        return "limit-identity-mismatch"
    return None


def deployment_from_inputs(
    source_configuration: dict[str, Any],
    endpoint: str | None,
    profile_path: Path | None,
    credential_env: str | None,
) -> dict[str, Any]:
    source_deployment = source_configuration.get("deployment", {})
    actual_endpoint = endpoint or source_deployment.get("endpoint")
    actual_profile = profile_path or Path(str(source_deployment.get("profile_path", "")))
    actual_credential = credential_env or source_deployment.get("credential_env")
    if not isinstance(actual_endpoint, str) or not actual_endpoint:
        raise ExperimentError("frozen endpoint identity is unavailable")
    require_private_file(actual_profile, EXPECTED_PROFILE)
    if not isinstance(actual_credential, str) or not actual_credential:
        raise ExperimentError("frozen credential environment identity is unavailable")
    return {
        "class": "A100-FP8",
        "model": protocol.MODEL,
        "endpoint": actual_endpoint,
        "profile_path": str(actual_profile),
        "profile_sha256": EXPECTED_PROFILE,
        "credential_env": actual_credential,
        "protocol": "Responses non-streaming",
    }


def build_configuration(
    repo_root: Path,
    scratch: Path,
    expected_head: str,
    source_configuration: dict[str, Any],
    source_identity: dict[str, Any],
    population: list[dict[str, Any]],
    population_digest: str,
    analysis: dict[str, Any],
    reuse_records: list[dict[str, Any]],
    fresh: list[dict[str, Any]],
    deployment: dict[str, Any],
) -> dict[str, Any]:
    original_identity = validator_driver.source_and_code_identity(repo_root, expected_head)
    code_paths = {
        name: sha256_file(repo_root / name)
        for name in (
            "research/levenshtein_one.py",
            "research/tools/run_levenshtein_one.py",
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
        "implementation_head": expected_head,
        "implementation_branch": original_identity["branch"],
        "prior_007i_identity": {
            "configuration_sha256": EXPECTED_PRIOR_CONFIG,
            "candidate_manifest_sha256": EXPECTED_PRIOR_CANDIDATES,
            "results_sha256": EXPECTED_PRIOR_RESULTS,
            "manifest_sha256": EXPECTED_PRIOR_MANIFEST,
            "case_identity_manifest_sha256": EXPECTED_PRIOR_CASES,
            "request_tree_sha256": EXPECTED_PRIOR_REQUEST_TREE,
            "model": protocol.MODEL,
            "prompt_sha256": EXPECTED_PROMPT,
            "profile_sha256": EXPECTED_PROFILE,
        },
        "source_identity": {
            **source_identity,
            "dataset_rows": PHASES,
            "paired_rows": sum(PHASES.values()),
            "candidate_manifest_sha256": population_digest,
            "candidate_count": len(population),
            "candidate_counts": EXPECTED_CANDIDATES,
            "reused_observations": len(reuse_records),
            "fresh_candidate_count": len(fresh),
            "fresh_call_budget": EXPECTED_FRESH,
            "operation_counts": analysis["operation_counts"],
            "entering_targets": analysis["entering_targets"],
            "transition_matrix": analysis["transition_matrix"],
            "vocabulary_forms": analysis["vocabulary_forms"],
            "runtime": {
                "candidate_search_seconds": analysis["lookup_seconds"],
                "vocabulary_loading_seconds": analysis["vocabulary_load_seconds"],
                "vocabulary_rows": analysis["vocabulary_rows"],
            },
        },
        "code_identity": {"sha256": code_paths, "head_blobs": original_identity["head_blobs"]},
        "candidate_rule": {
            "distance": "standard unit-cost Levenshtein over Python Unicode code points",
            "identity": "distance zero excluded",
            "accepted": "complete deduplicated vocabulary union at distance one only",
            "operations": ["SUBSTITUTION", "INSERTION", "DELETION"],
            "normalization": "none",
            "transposition": "distance two and excluded",
            "ranking": "none",
        },
        "old_candidate_identity": {
            "rule": "007-i/007-h alphabetic one-substitution recomputation only",
            "source_configuration_sha256": source_configuration.get("prior_007h_head"),
            "candidate_manifest_sha256": EXPECTED_PRIOR_CANDIDATES,
            "transition_assertion": True,
        },
        "prompt": {
            "sha256": EXPECTED_PROMPT,
            "template": "owner-supplied frozen 007-i validator prompt",
        },
        "deployment": deployment,
        "request": {
            "fields": EXPECTED_REQUEST_FIELDS,
            "stream": False,
            "store": False,
            "include_reasoning": True,
            "reasoning_effort": protocol.EFFORT,
            "serializer": "canonical UTF-8 JSON with one final LF",
        },
        "parser": EXPECTED_PARSER,
        "scheduling": {
            "workers": protocol.WORKERS,
            "partition_key": [
                "phase",
                "case_index",
                "target_start",
                "target_end",
                "target_ordinal",
            ],
            "partition": "stable ordered position modulo worker count",
            "in_flight_per_worker": 1,
            "maximum_in_flight": protocol.WORKERS,
            "scheduled_new_calls": len(fresh),
        },
        "limits": {
            "timeout_seconds": protocol.TIMEOUT_SECONDS,
            "response_bound_bytes": protocol.MAX_RESPONSE_BYTES,
            "attempts_per_candidate": 1,
            "resampling": False,
            "new_call_budget": EXPECTED_FRESH,
        },
        "persistence": {
            "order": [
                "request bytes",
                "dispatch marker",
                "bounded raw response/timing",
                "parsed observation",
            ],
            "interrupted_request": "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE",
            "immutable_completed_observations": True,
            "reuse_records": "exact source/case/request/prompt/deployment identity required",
        },
        "reuse": {
            "policy": "exact identity only; target text or candidate alone is insufficient",
            "count": len(reuse_records),
            "fresh_count": len(fresh),
            "reuse_manifest_sha256": sha256_bytes(canonical_bytes(reuse_records)),
        },
        "projections": {
            "validated_fallback": (
                "USE_CANDIDATE supplied mechanical edit; all other choices use "
                "007-i baseline fallback"
            ),
            "validated_only": (
                "USE_CANDIDATE supplied mechanical edit; all other choices leave original target"
            ),
            "baseline_calls_resampled": False,
            "shared_observation": True,
        },
        "scorer": {
            "implementation_head": source_configuration.get("prior_007h_head"),
            "attribution": "unchanged 007-i scorer",
        },
        "privacy": {
            "public": "aggregate metrics, hashes, transition and operation counts only",
            "private": (
                "sentences, targets, candidates, prompts, responses, endpoint/profile "
                "and credentials"
            ),
        },
        "no_tuning_or_resampling": True,
        "private_evidence_root": str(scratch),
    }


def persist_preparation(
    scratch: Path,
    configuration: dict[str, Any],
    population: list[dict[str, Any]],
    candidate_manifest: list[dict[str, Any]],
    fresh: list[dict[str, Any]],
    reuse_records: list[dict[str, Any]],
) -> dict[str, Any]:
    immutable_json(scratch / "CANDIDATES.json", population)
    immutable_json(scratch / "CANDIDATE-MANIFEST.json", candidate_manifest)
    immutable_json(scratch / "FRESH-CALL-MANIFEST.json", fresh)
    immutable_json(scratch / "REUSE-RECORDS.json", reuse_records)
    configuration_sha = immutable_json(scratch / "CONFIGURATION.json", configuration)
    immutable_json(
        scratch / "RUN-STATUS.json",
        {
            "status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "run_id": RUN_ID,
            "configuration_sha256": configuration_sha,
            "candidate_manifest_sha256": configuration["source_identity"][
                "candidate_manifest_sha256"
            ],
            "scheduled_candidates": len(population),
            "reused_observations": len(reuse_records),
            "fresh_candidates": len(fresh),
            "dispatched_http_requests": 0,
        },
    )
    return {
        "configuration_sha256": configuration_sha,
        "candidate_manifest_sha256": configuration["source_identity"]["candidate_manifest_sha256"],
    }


def load_prepared(scratch: Path) -> dict[str, Any]:
    require_private_dir(scratch)
    for name in (
        "CONFIGURATION.json",
        "CANDIDATES.json",
        "CANDIDATE-MANIFEST.json",
        "FRESH-CALL-MANIFEST.json",
        "REUSE-RECORDS.json",
    ):
        require_private_file(scratch / name)
    configuration = read_json(scratch / "CONFIGURATION.json")
    population = read_json(scratch / "CANDIDATES.json")
    manifest = read_json(scratch / "CANDIDATE-MANIFEST.json")
    fresh = read_json(scratch / "FRESH-CALL-MANIFEST.json")
    reuse_records = read_json(scratch / "REUSE-RECORDS.json")
    if not isinstance(configuration, dict) or not all(
        isinstance(value, list) for value in (population, manifest, fresh, reuse_records)
    ):
        raise ExperimentError("prepared private artifacts are malformed")
    recomputed, digest = protocol.candidate_manifest(population)
    if (
        recomputed != manifest
        or digest != configuration["source_identity"]["candidate_manifest_sha256"]
    ):
        raise ExperimentError("prepared candidate manifest mismatch")
    return {
        "configuration": configuration,
        "configuration_sha256": sha256_file(scratch / "CONFIGURATION.json"),
        "population": protocol.ordered_candidates(population),
        "candidate_manifest": manifest,
        "fresh": protocol.ordered_candidates(fresh),
        "reuse_records": reuse_records,
    }


def execute_fresh(
    scratch: Path,
    fresh: list[dict[str, Any]],
    endpoint: str,
    credential_env: str,
    *,
    transport: protocol.ResponseTransport | None = None,
) -> dict[int, dict[str, Any]]:
    if transport is None and not os.environ.get(credential_env):
        raise ExperimentError("LIVE_CREDENTIAL_MISSING")
    partitions = protocol.partitions(fresh)
    statuses: dict[int, dict[str, Any]] = {}

    def worker(worker_id: int) -> tuple[int, dict[str, Any]]:
        started = time.monotonic()
        observations = 0
        dispatched = 0
        failures = 0
        for item in partitions[worker_id]:
            observation = validator_driver._call_one(
                scratch, item, endpoint, credential_env, transport=transport
            )
            observations += 1
            dispatched += int(observation.get("dispatch") == "ATTEMPTED")
            failures += int(bool(observation.get("operational_failure")))
        return worker_id, {
            "worker": worker_id,
            "assigned": len(partitions[worker_id]),
            "completed": observations,
            "dispatched_http": dispatched,
            "failures": failures,
            "seconds": time.monotonic() - started,
        }

    with ThreadPoolExecutor(max_workers=protocol.WORKERS, thread_name_prefix="oap-007-j") as pool:
        futures = [pool.submit(worker, worker_id) for worker_id in range(protocol.WORKERS)]
        for future in futures:
            worker_id, status = future.result()
            statuses[worker_id] = status
    if sum(value["completed"] for value in statuses.values()) != len(fresh):
        raise ExperimentError("fresh observation set is incomplete")
    mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "VALIDATOR_OBSERVATIONS_COMPLETE",
            "run_id": RUN_ID,
            "scheduled_candidates": len(fresh),
            "observation_records": len(fresh),
            "dispatched_http_requests": sum(
                value["dispatched_http"] for value in statuses.values()
            ),
            "protocol_or_operational_failures": sum(
                value["failures"] for value in statuses.values()
            ),
            "workers": protocol.WORKERS,
            "worker_runtime": statuses,
        },
    )
    worker_result = scratch / "WORKER-RESULT.json"
    if worker_result.exists() or worker_result.is_symlink():
        require_private_file(worker_result)
        previous = read_json(worker_result)
        if not isinstance(previous, dict):
            raise ExperimentError("persisted worker result is malformed")
        for worker_id, current in statuses.items():
            old = previous.get(str(worker_id), previous.get(worker_id))
            if not isinstance(old, dict) or any(
                old.get(key) != current.get(key)
                for key in ("worker", "assigned", "completed", "dispatched_http", "failures")
            ):
                raise ExperimentError("persisted worker assignment/result identity changed")
    else:
        immutable_json(worker_result, statuses)
    return statuses


def load_fresh_observations(
    scratch: Path, fresh: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    observations: dict[str, dict[str, Any]] = {}
    for item in fresh:
        candidate_id = protocol.candidate_path_id(item)
        path = scratch / "requests" / candidate_id / "observation.json"
        require_private_file(path)
        value = read_json(path)
        if not isinstance(value, dict):
            raise ExperimentError("fresh observation is not an object")
        observations[candidate_id] = value
    if len(observations) != len(fresh):
        raise ExperimentError("fresh observation count mismatch")
    return observations


def complete_result(
    scratch: Path,
    prepared: dict[str, Any],
    source_root: Path,
    records: dict[str, list[dict[str, Any]]],
    pairs: dict[str, list[dict[str, Any]]],
    uv_indices: set[int],
    observations: dict[str, dict[str, Any]],
    worker_status: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    if len(observations) != EXPECTED_TOTAL:
        raise ExperimentError("complete aggregation requires all reused and fresh observations")
    by_case: dict[str, list[dict[str, Any]]] = {phase: [] for phase in PHASES}
    candidates_by_case: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for item in prepared["population"]:
        candidates_by_case.setdefault((item["phase"], item["case_index"]), []).append(item)
    for phase, cases in records.items():
        for case in cases:
            value = validator_driver.make_case_result(
                phase,
                case,
                candidates_by_case.get((phase, case["index"]), []),
                observations,
                prepared["configuration_sha256"],
            )
            value["experiment_id"] = EXPERIMENT_ID
            by_case[phase].append(value)
    metrics = validator_driver.make_views(
        pairs,
        by_case,
        prepared["population"],
        observations,
        uv_indices,
        worker_status,
    )
    reuse_ids = {record["candidate_id"] for record in prepared["reuse_records"]}
    for phase_records in by_case.values():
        for record in phase_records:
            for target in record["validator_targets"]:
                target["observation_source"] = (
                    "reuse" if target["candidate_id"] in reuse_ids else "fresh"
                )
    update_view_call_accounting(metrics, prepared["population"], reuse_ids, uv_indices)
    metrics["candidate_analysis"] = candidate_analysis(by_case, prepared["population"])
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "configuration_sha256": prepared["configuration_sha256"],
        "candidate_manifest_sha256": prepared["configuration"]["source_identity"][
            "candidate_manifest_sha256"
        ],
        "case_identity_manifest_sha256": EXPECTED_PRIOR_CASES,
        "status": "COMPLETE",
        "metrics": metrics,
        "reuse": {
            "observations": EXPECTED_REUSED,
            "fresh_calls": EXPECTED_FRESH,
            "total_observations": EXPECTED_TOTAL,
        },
        "source_root": str(source_root),
    }
    immutable_json(scratch / "CASE-RESULTS.json", by_case)
    result_sha = immutable_json(scratch / "RESULTS.json", result)
    manifest_sha = immutable_json(
        scratch / "MANIFEST.json",
        {
            "schema_version": 1,
            "experiment_id": EXPERIMENT_ID,
            "configuration_sha256": prepared["configuration_sha256"],
            "candidate_manifest_sha256": result["candidate_manifest_sha256"],
            "case_identity_manifest_sha256": EXPECTED_PRIOR_CASES,
            "case_count": sum(PHASES.values()),
            "candidate_count": EXPECTED_TOTAL,
            "reused_observations": EXPECTED_REUSED,
            "fresh_calls": EXPECTED_FRESH,
            "private_results_sha256": result_sha,
            "status": result["status"],
        },
    )
    report_sha = immutable_write(
        scratch / "REPORT.md",
        (
            "# Private 007-j report\n\n"
            + json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
            + "\n"
        ).encode("utf-8"),
    )
    for path in (
        scratch / "CASE-RESULTS.json",
        scratch / "RESULTS.json",
        scratch / "MANIFEST.json",
        scratch / "REPORT.md",
    ):
        require_private_file(path)
    mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "COMPLETE",
            "run_id": RUN_ID,
            "configuration_sha256": prepared["configuration_sha256"],
            "candidate_manifest_sha256": result["candidate_manifest_sha256"],
            "reused_observations": EXPECTED_REUSED,
            "fresh_candidates": EXPECTED_FRESH,
            "observation_records": len(observations),
            "scheduled_candidates": EXPECTED_TOTAL,
            "dispatched_http_requests": metrics["dispatched_http_requests"],
            "uncertain_deliveries": metrics["uncertain_deliveries"],
            "aggregate_artifacts_verified": True,
            "private_results_sha256": result_sha,
            "private_manifest_sha256": manifest_sha,
            "private_report_sha256": report_sha,
        },
    )
    result.update(
        {
            "private_results_sha256": result_sha,
            "private_manifest_sha256": manifest_sha,
            "private_report_sha256": report_sha,
        }
    )
    return result


def _empty_candidate_bucket() -> dict[str, Any]:
    return {
        "unique": 0,
        "attribution": {"exact_reference": 0, "non_reference": 0, "unresolved": 0},
        "validator": {
            "USE_CANDIDATE": 0,
            "KEEP_ORIGINAL": 0,
            "UNCERTAIN": 0,
            "FAILURE": 0,
        },
        "accepted": {"exact_reference": 0, "non_reference": 0, "unresolved": 0},
        "rejected": {"exact_reference": 0, "non_reference": 0, "unresolved": 0},
        "unresolved_attribution": 0,
        "final_tp_fp_fn": {"TP": 0, "FP": 0, "FN": 0},
        "final_unresolved": 0,
        "reference_precision_among_accepted": {
            "numerator": 0,
            "denominator": 0,
            "value": None,
        },
    }


def _add_candidate_to_bucket(bucket: dict[str, Any], target: dict[str, Any]) -> None:
    bucket["unique"] += 1
    attribution = target.get("attribution", {}).get("status")
    attribution = (
        attribution if attribution in {"exact_reference", "non_reference"} else "unresolved"
    )
    bucket["attribution"][attribution] += 1
    if attribution == "unresolved":
        bucket["unresolved_attribution"] += 1
    decision = target.get("decision") or "FAILURE"
    if decision not in bucket["validator"]:
        decision = "FAILURE"
    bucket["validator"][decision] += 1
    disposition = "accepted" if decision == "USE_CANDIDATE" else "rejected"
    bucket[disposition][attribution] += 1
    applied = target.get("applied_fallback") is True
    if applied and attribution == "exact_reference":
        bucket["final_tp_fp_fn"]["TP"] += 1
    elif applied and attribution == "non_reference":
        bucket["final_tp_fp_fn"]["FP"] += 1
    elif not applied and attribution == "exact_reference":
        bucket["final_tp_fp_fn"]["FN"] += 1
    elif applied:
        bucket["final_unresolved"] += 1
    accepted_exact = bucket["accepted"]["exact_reference"]
    accepted_non_reference = bucket["accepted"]["non_reference"]
    denominator = accepted_exact + accepted_non_reference
    bucket["reference_precision_among_accepted"] = {
        "numerator": accepted_exact,
        "denominator": denominator,
        "value": accepted_exact / denominator if denominator else None,
    }


def candidate_analysis(
    by_case: dict[str, list[dict[str, Any]]], population: list[dict[str, Any]]
) -> dict[str, Any]:
    """Aggregate only data-free operation and validator outcome counts."""
    targets: dict[str, dict[str, Any]] = {}
    for records in by_case.values():
        for record in records:
            for target in record["validator_targets"]:
                targets[target["candidate_id"]] = target
    result: dict[str, Any] = {"all_unique": {}, "new_or_changed": {}}
    for scope in result:
        result[scope] = {
            operation: _empty_candidate_bucket() for operation in distance_one.OPERATIONS
        }
    for item in population:
        candidate_id = protocol.candidate_path_id(item)
        target = targets.get(candidate_id)
        if target is None:
            raise ExperimentError("candidate analysis lacks a validator target")
        operation = item["operation"]
        _add_candidate_to_bucket(result["all_unique"][operation], target)
        if target.get("observation_source") == "fresh":
            _add_candidate_to_bucket(result["new_or_changed"][operation], target)
    return result


def update_view_call_accounting(
    metrics: dict[str, Any],
    population: list[dict[str, Any]],
    reuse_ids: set[str],
    uv_indices: set[int],
) -> None:
    """Replace aggregate-wide subtraction with exact identities per view."""
    for phase, phase_views in metrics["views"].items():
        for view_name, view in phase_views.items():
            selected_ids = {
                protocol.candidate_path_id(item)
                for item in population
                if item["phase"] == phase
                and (
                    view_name == "all"
                    or (view_name == "initial_uv" and item["case_index"] in uv_indices)
                    or (view_name == "without_initial_uv" and item["case_index"] not in uv_indices)
                )
            }
            reused = len(selected_ids & reuse_ids)
            fresh = len(selected_ids - reuse_ids)
            total = len(selected_ids)
            if total != view["scheduled_candidates"]:
                raise ExperimentError("view candidate identity count mismatch")
            for accounting in view["call_accounting"].values():
                ordinary_total = accounting["projected_ordinary"]["total"]
                accounting["validator_observations"] = total
                accounting["validator_calls_reused"] = reused
                accounting["validator_calls_added"] = fresh
                accounting["validator_calls_total"] = total
                accounting["net_projected"]["total"] = ordinary_total + total
                accounting["net_projected"]["validator_observations"] = total
                accounting["delta_vs_baseline"] = (
                    accounting["net_projected"]["total"] - accounting["baseline"]["total"]
                )
                accounting["delta_vs_007h"] = (
                    accounting["net_projected"]["total"] - accounting["unrestricted_007h"]["total"]
                )


def blocked_result(scratch: Path, prepared: dict[str, Any], reason: str) -> dict[str, Any]:
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "configuration_sha256": prepared["configuration_sha256"],
        "candidate_manifest_sha256": prepared["configuration"]["source_identity"][
            "candidate_manifest_sha256"
        ],
        "case_identity_manifest_sha256": EXPECTED_PRIOR_CASES,
        "status": "BLOCKED",
        "blocker": reason,
        "offline": {
            "transition_matrix": prepared["configuration"]["source_identity"]["transition_matrix"],
            "operation_counts": prepared["configuration"]["source_identity"]["operation_counts"],
            "entering_targets": prepared["configuration"]["source_identity"]["entering_targets"],
            "candidate_count": EXPECTED_TOTAL,
            "reused_observations": EXPECTED_REUSED,
            "fresh_candidates_without_dispatch": EXPECTED_FRESH,
            "dispatched_http_requests": 0,
            "scientific_projections": "NOT RUN: fresh validator population is not observed",
        },
    }
    result_sha = immutable_json(scratch / "RESULTS.json", result)
    manifest_sha = immutable_json(
        scratch / "MANIFEST.json",
        {
            "schema_version": 1,
            "experiment_id": EXPERIMENT_ID,
            "configuration_sha256": prepared["configuration_sha256"],
            "candidate_manifest_sha256": result["candidate_manifest_sha256"],
            "case_identity_manifest_sha256": EXPECTED_PRIOR_CASES,
            "candidate_count": EXPECTED_TOTAL,
            "reused_observations": EXPECTED_REUSED,
            "fresh_calls": 0,
            "status": "BLOCKED",
            "blocker": reason,
            "private_results_sha256": result_sha,
        },
    )
    report_sha = immutable_write(
        scratch / "REPORT.md",
        (
            "# Private 007-j report\n\n"
            + json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
            + "\n"
        ).encode("utf-8"),
    )
    mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "BLOCKED",
            "run_id": RUN_ID,
            "blocker": reason,
            "configuration_sha256": prepared["configuration_sha256"],
            "reused_observations": EXPECTED_REUSED,
            "fresh_candidates": EXPECTED_FRESH,
            "dispatched_http_requests": 0,
        },
    )
    result.update(
        {
            "private_results_sha256": result_sha,
            "private_manifest_sha256": manifest_sha,
            "private_report_sha256": report_sha,
        }
    )
    return result


def public_projection(
    configuration: dict[str, Any], result: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    identity = configuration["source_identity"]
    result_metrics = result.get("metrics")
    public_configuration = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "run_id": RUN_ID,
        "status": result["status"],
        "implementation_head": configuration["implementation_head"],
        "implementation_branch": configuration["implementation_branch"],
        "prior_007i_identity": configuration["prior_007i_identity"],
        "source_identity": {
            "dataset_rows": identity["dataset_rows"],
            "paired_rows": identity["paired_rows"],
            "candidate_count": identity["candidate_count"],
            "candidate_counts": identity["candidate_counts"],
            "reused_observations": identity["reused_observations"],
            "fresh_call_budget": identity["fresh_call_budget"],
            "entering_targets": identity["entering_targets"],
            "transition_matrix": identity["transition_matrix"],
            "operation_counts": identity["operation_counts"],
            "vocabulary_forms": identity["vocabulary_forms"],
            "runtime": identity.get("runtime"),
            "case_identity_manifest_sha256": identity["case_identity_manifest_sha256"],
            "candidate_manifest_sha256": identity["candidate_manifest_sha256"],
        },
        "candidate_rule": configuration["candidate_rule"],
        "prompt": {
            "sha256": EXPECTED_PROMPT,
            "template": "owner-supplied frozen 007-i validator prompt",
        },
        "deployment": {
            "class": "A100-FP8",
            "model": protocol.MODEL,
            "protocol": "Responses non-streaming",
            "profile_sha256": EXPECTED_PROFILE,
            "endpoint": "private endpoint identity omitted",
            "profile_path": "private profile path omitted",
        },
        "request": configuration["request"],
        "parser": configuration["parser"],
        "scheduling": configuration["scheduling"],
        "limits": configuration["limits"],
        "reuse": {
            "policy": configuration["reuse"]["policy"],
            "count": EXPECTED_REUSED,
            "fresh_count": EXPECTED_FRESH,
            "fresh_dispatches": result.get("reuse", {}).get(
                "fresh_calls", result.get("offline", {}).get("dispatched_http_requests", 0)
            ),
        },
        "privacy": configuration["privacy"]["public"],
    }
    public_configuration["configuration_sha256"] = sha256_bytes(
        canonical_bytes(public_configuration)
    )
    public_result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "status": result["status"],
        "implementation_head": configuration["implementation_head"],
        "configuration_sha256": public_configuration["configuration_sha256"],
        "candidate_manifest_sha256": identity["candidate_manifest_sha256"],
        "source_identity": public_configuration["source_identity"],
        "transition_matrix": identity["transition_matrix"],
        "operation_counts": identity["operation_counts"],
        "reuse": public_configuration["reuse"],
        "candidate_analysis": result_metrics.get("candidate_analysis")
        if isinstance(result_metrics, dict)
        else None,
        "metrics": result.get("metrics"),
        "offline": result.get("offline"),
        "blocker": result.get("blocker"),
        "private_evidence_sha256": {
            key: result[key]
            for key in (
                "private_results_sha256",
                "private_manifest_sha256",
                "private_report_sha256",
            )
            if key in result
        },
        "limitations": [
            (
                "This is an owner-authorized bounded research experiment, not product "
                "or linguistic acceptance."
            ),
            (
                "Standard Levenshtein distance is mechanical candidate generation; it "
                "does not establish semantic correctness."
            ),
            "Non-reference status is not a semantic-harm label.",
            "No merge, release, deployment, or production integration is authorized.",
        ],
    }
    return public_configuration, public_result


def public_report(configuration: dict[str, Any], result: dict[str, Any]) -> str:
    identity = configuration["source_identity"]
    lines = [
        "# 007-j standard Levenshtein-one contextual validation",
        "",
        "EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.",
        "",
        (
            "The sole variable is complete standard unit-cost Levenshtein distance-one "
            "candidate generation over the frozen 007-i vocabulary; validator and "
            "fallback identities remain unchanged."
        ),
        "",
        "## Frozen identity",
        "",
        f"- Status: {result['status']}.",
        (
            f"- Candidate population: {identity['candidate_count']} "
            f"({identity['candidate_counts']['dassle-spelling']} spelling; "
            f"{identity['candidate_counts']['dassle-spelling-preservation']} preservation)."
        ),
        f"- Reused observations / fresh-call budget: {EXPECTED_REUSED} / {EXPECTED_FRESH}.",
        f"- Candidate manifest SHA-256: {identity['candidate_manifest_sha256']}.",
        f"- Prompt SHA-256: {EXPECTED_PROMPT}.",
        "",
        "## Transition matrix",
        "",
    ]
    for phase in PHASES:
        lines.append(f"### {phase}")
        for transition, count in identity["transition_matrix"][phase].items():
            lines.append(f"- {transition}: {count}.")
        lines.append("")
    lines += ["## Operation counts", ""]
    for phase in PHASES:
        counts = identity["operation_counts"][phase]
        lines.append(
            f"- {phase}: SUBSTITUTION {counts.get('SUBSTITUTION', 0)}; "
            f"INSERTION {counts.get('INSERTION', 0)}; "
            f"DELETION {counts.get('DELETION', 0)}."
        )
    if result["status"] == "BLOCKED":
        lines += [
            "",
            "## Scientific execution",
            "",
            f"- Blocker: `{result.get('blocker', 'unspecified')}`.",
            "- Fresh validator calls: 0; no fresh candidate was dispatched or resampled.",
            "- Scientific projections and 007-i deltas: NOT RUN; fresh observations are required.",
        ]
    else:
        result_metrics = result.get("metrics")
        analysis = (
            result_metrics.get("candidate_analysis", {}) if isinstance(result_metrics, dict) else {}
        )
        lines += [
            "",
            "## Scientific execution",
            "",
            (
                f"- Reused observations / fresh calls / total observations: "
                f"{EXPECTED_REUSED} / {EXPECTED_FRESH} / {EXPECTED_TOTAL}."
            ),
            (
                "- Operation-level, four-population, fallback, scorer, runtime, and "
                "integrity metrics are retained in the data-free aggregate result."
            ),
        ]
        for scope in ("all_unique", "new_or_changed"):
            lines += ["", f"### {scope.replace('_', ' ').title()} candidate outcomes", ""]
            for operation in ("SUBSTITUTION", "INSERTION", "DELETION"):
                bucket = analysis.get(scope, {}).get(operation, {})
                validator = bucket.get("validator", {})
                accepted = bucket.get("accepted", {})
                rejected = bucket.get("rejected", {})
                final = bucket.get("final_tp_fp_fn", {})
                precision = bucket.get("reference_precision_among_accepted", {})
                lines.append(
                    f"- {operation}: unique {bucket.get('unique', 0)}; "
                    "exact/non-reference/unresolved "
                    f"{bucket.get('attribution', {}).get('exact_reference', 0)}/"
                    f"{bucket.get('attribution', {}).get('non_reference', 0)}/"
                    f"{bucket.get('attribution', {}).get('unresolved', 0)}; "
                    f"USE/KEEP/UNCERTAIN/FAILURE "
                    f"{validator.get('USE_CANDIDATE', 0)}/{validator.get('KEEP_ORIGINAL', 0)}/"
                    f"{validator.get('UNCERTAIN', 0)}/{validator.get('FAILURE', 0)}; "
                    f"accepted exact/non-reference/unresolved "
                    f"{accepted.get('exact_reference', 0)}/{accepted.get('non_reference', 0)}/"
                    f"{accepted.get('unresolved', 0)}; rejected "
                    f"{rejected.get('exact_reference', 0)}/{rejected.get('non_reference', 0)}/"
                    f"{rejected.get('unresolved', 0)}; TP/FP/FN "
                    f"{final.get('TP', 0)}/{final.get('FP', 0)}/{final.get('FN', 0)}; "
                    f"reference precision {precision.get('value')} "
                    f"({precision.get('numerator', 0)}/"
                    f"{precision.get('denominator', 0)})."
                )
        runtime = identity.get("runtime", {})
        lines += [
            "",
            "### Runtime accounting",
            "",
            (
                f"- Candidate search seconds: {runtime.get('candidate_search_seconds')}; "
                f"vocabulary loading seconds: {runtime.get('vocabulary_loading_seconds')}; "
                f"vocabulary rows: {runtime.get('vocabulary_rows')}."
            ),
        ]
    lines += [
        "",
        "## Boundaries",
        "",
        (
            "- Reuse requires exact source-row, coordinate, sentence, candidate, request, "
            "prompt, deployment, parser, and persisted-response identity; reuse by text "
            "alone is rejected."
        ),
        "- C=0 and C>1 candidates use the unchanged baseline path; only C=1 reaches validation.",
        "- No baseline response is resampled. PR #8 remains open and unmerged.",
        (
            "- This report does not authorize integration, merge, release, deployment, "
            "or product linguistic acceptance."
        ),
    ]
    return "\n".join(lines) + "\n"


def write_public(
    repo_root: Path, configuration: dict[str, Any], result: dict[str, Any]
) -> dict[str, str]:
    public_configuration, public_result = public_projection(configuration, result)
    paths = {
        "config": repo_root / "research/configs/007-j-levenshtein-one-contextual-validator.json",
        "result": repo_root / "research/results/007-j-levenshtein-one-contextual-validator.json.gz",
        "report": repo_root / "research/reports/007-j-levenshtein-one-contextual-validator.md",
    }
    validator_driver.public_immutable_write(paths["config"], canonical_bytes(public_configuration))
    validator_driver.public_immutable_write(
        paths["result"], gzip.compress(canonical_bytes(public_result), mtime=0)
    )
    validator_driver.public_immutable_write(
        paths["report"], public_report(configuration, result).encode("utf-8")
    )
    return {key: sha256_file(path) for key, path in paths.items()}


def prepare(
    repo_root: Path,
    scratch: Path,
    source_root: Path,
    expected_head: str,
    endpoint: str | None,
    profile_path: Path | None,
    credential_env: str | None,
) -> dict[str, Any]:
    source_identity = source_root_identity(source_root)
    ensure_scratch(scratch)
    stage_inputs(source_root, scratch)
    pairs, _baseline, uv_indices, records, case_digest = validator_driver.load_frozen_state(scratch)
    if case_digest != EXPECTED_PRIOR_CASES:
        raise ExperimentError("staged 007-i case identity mismatch")
    vocabulary, buckets, vocabulary_seconds, vocabulary_rows = baseline_driver.load_vocabulary(
        scratch / "inputs/index/index.sqlite"
    )
    old_population, old_observations, old_manifest = prior_population_and_observations(
        source_root, records, vocabulary, buckets
    )
    population, analysis = build_population(records, vocabulary, buckets)
    candidate_manifest, population_digest = protocol.candidate_manifest(population)
    old_configuration = read_json(source_root / "CONFIGURATION.json")
    if not isinstance(old_configuration, dict):
        raise ExperimentError("007-i configuration is not an object")
    deployment = deployment_from_inputs(old_configuration, endpoint, profile_path, credential_env)
    reused, reuse_records, fresh = reuse_observations(
        source_root,
        scratch,
        population,
        old_population,
        old_observations,
        old_configuration,
        deployment,
    )
    analysis["vocabulary_load_seconds"] = vocabulary_seconds
    analysis["vocabulary_rows"] = vocabulary_rows
    configuration = build_configuration(
        repo_root,
        scratch,
        expected_head,
        old_configuration,
        {
            **source_identity,
            "case_identity_manifest_sha256": case_digest,
            "old_candidate_manifest_sha256": old_manifest["candidate_manifest_sha256"],
        },
        population,
        population_digest,
        analysis,
        reuse_records,
        fresh,
        deployment,
    )
    persisted = persist_preparation(
        scratch, configuration, population, candidate_manifest, fresh, reuse_records
    )
    return {
        "configuration": configuration,
        "configuration_sha256": persisted["configuration_sha256"],
        "population": population,
        "fresh": fresh,
        "reused": reused,
        "reuse_records": reuse_records,
        "pairs": pairs,
        "records": records,
        "uv_indices": uv_indices,
        "source_root": source_root,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    scratch = Path(args.scratch).absolute()
    ensure_scratch(scratch)
    source_root = Path(args.source_root).absolute() if args.source_root else None
    if (scratch / "CONFIGURATION.json").exists():
        prepared = load_prepared(scratch)
        source_root = source_root or Path(str(read_json(scratch / "SOURCE.json")["source_root"]))
        source_root_identity(source_root)
        # A prepared root is safe to resume only with its original frozen
        # inputs.  Load the paired state from the staged copy.
        pairs, _baseline, uv_indices, records, case_digest = validator_driver.load_frozen_state(
            scratch
        )
        prepared.update(
            {
                "pairs": pairs,
                "records": records,
                "uv_indices": uv_indices,
                "source_root": source_root,
            }
        )
        reused = {}
        for item in prepared["population"]:
            candidate_id = protocol.candidate_path_id(item)
            if candidate_id in {record["candidate_id"] for record in prepared["reuse_records"]}:
                reused[candidate_id] = read_json(
                    scratch / "requests" / candidate_id / "observation.json"
                )
        prepared["reused"] = reused
    else:
        if source_root is None:
            raise ExperimentError("initial preparation requires the frozen 007-i source root")
        prepared = prepare(
            repo_root,
            scratch,
            source_root,
            args.expected_implementation_head,
            args.endpoint,
            Path(args.profile_path).absolute() if args.profile_path else None,
            args.credential_env,
        )
        immutable_json(scratch / "SOURCE.json", {"source_root": str(source_root)})
    if args.prepare_only:
        return {
            "status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "configuration_sha256": prepared["configuration_sha256"],
            "candidate_manifest_sha256": prepared["configuration"]["source_identity"][
                "candidate_manifest_sha256"
            ],
            "reused_observations": EXPECTED_REUSED,
            "fresh_candidates": EXPECTED_FRESH,
            "fresh_calls": 0,
        }
    configuration = prepared["configuration"]
    existing = read_json(scratch / "RESULTS.json") if (scratch / "RESULTS.json").exists() else None
    if isinstance(existing, dict) and existing.get("status") in {"COMPLETE", "BLOCKED"}:
        result = existing
        public = write_public(repo_root, configuration, result)
        return {
            "status": result["status"],
            "public": public,
            "configuration_sha256": prepared["configuration_sha256"],
        }
    deployment = configuration["deployment"]
    try:
        worker_status = execute_fresh(
            scratch, prepared["fresh"], deployment["endpoint"], deployment["credential_env"]
        )
    except ExperimentError as exc:
        if str(exc) != "LIVE_CREDENTIAL_MISSING":
            raise
        result = blocked_result(scratch, prepared, str(exc))
        public = write_public(repo_root, configuration, result)
        return {
            "status": result["status"],
            "blocker": str(exc),
            "public": public,
            "configuration_sha256": prepared["configuration_sha256"],
        }
    fresh_observations = load_fresh_observations(scratch, prepared["fresh"])
    observations = {**prepared["reused"], **fresh_observations}
    result = complete_result(
        scratch,
        prepared,
        source_root,
        prepared["records"],
        prepared["pairs"],
        prepared["uv_indices"],
        observations,
        worker_status,
    )
    public = write_public(repo_root, configuration, result)
    return {
        "status": result["status"],
        "public": public,
        "configuration_sha256": prepared["configuration_sha256"],
        "fresh_calls": EXPECTED_FRESH,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--expected-implementation-head", required=True)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--endpoint")
    parser.add_argument("--profile", "--profile-path", dest="profile_path")
    parser.add_argument("--credential-env")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(run(args), ensure_ascii=False, sort_keys=True))
    except (ExperimentError, OSError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "reason": str(exc)}, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
