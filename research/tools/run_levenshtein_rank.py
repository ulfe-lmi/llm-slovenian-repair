"""Run the 007-m CPU ranking census over the exact frozen 007-j C>1 population.

Increment 1 is offline: it verifies the completed 007-j private root, the
frozen 007-i cases and the read-only SQLite index schema (mechanically
confirming unigram/bigram/trigram evidence), re-enumerates the complete
distance-one union with the frozen 007-j generator semantics, ranks every
C>1 candidate with the predeclared lexicographic tuple, abstains on exact
top-score ties, and persists private machine-readable census evidence.  Gold
is used only after ranking, for the reference headroom projection.  No model
calls, no acquisition, and no new index structure.

Increment 2 harness revision: the failed-instrument root ffdf13 (frozen at
88ca4dfe, preserved unchanged as evidence) could not complete its own live
resume because the resume verifier rejected the canonical interrupted
finalization file set (request + dispatch marker + raw/observation UNKNOWN).
This revision accepts that state as a distinguishable uncertain delivery and
adds a cross-root adoption harness: completed C>1 observations are copied
under exact request/raw/observation/profile/prompt/parser identity,
request-only interruptions are carried to conservative uncertain observations
without calls, and only the never-dispatched requests are scheduled fresh.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import json
import math
import os
import sqlite3
import statistics
import subprocess
import time
from collections import Counter
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from research import contextual_validator as protocol
from research import levenshtein_one as distance_one
from research import levenshtein_rank as rank
from research.one_substitution import mechanical_substitution
from research.tools import run_contextual_validator as validator_driver
from research.tools import run_levenshtein_one as prior_j
from research.tools import run_one_substitution as baseline_driver

RUN_ID = "007-m"
EXPERIMENT_ID = "007-m-rank-ambiguous-levenshtein-candidates"
PHASES = prior_j.PHASES
BRANCH = "oap/007-concept-verification"
NATIVE_RUNTIME_PARENT = prior_j.NATIVE_RUNTIME_PARENT
SCRATCH_NAME_PREFIX = EXPERIMENT_ID + "-recovery."

# Frozen completed 007-j root identities (self-consistent with its RUN-STATUS).
EXPECTED_007J_CONFIGURATION = "7375ac89aab6376b90b08c300ddab871fded9c86b73ea23022a3438bf0f677ef"
EXPECTED_007J_CANDIDATE_MANIFEST = (
    "acabcf1b33c38a949c80e81773b8ff3c355386daf768404791aaaed111f1df41"
)
EXPECTED_007J_RESULTS = "947f67f08f9a6d3fc76e417542a0043f0a7bb64bc6a14e81e49f8a2f5843da84"

# Predeclared expected scale from frozen 007-j: verified, never assumed.
EXPECTED_C_GT_1 = {"dassle-spelling": 651, "dassle-spelling-preservation": 231}
EXPECTED_C_GT_1_TOTAL = 882

# Frozen 007-j validated_fallback tp/fn per census slice: paired baseline.
EXPECTED_SLICE_BASELINE: dict[str, tuple[int, int]] = {
    "spelling-all": (822, 693),
    "spelling-initial-uv": (42, 33),
    "spelling-without-initial-uv": (780, 660),
    "preservation-all": (0, 0),
}
SLICE_VIEW = {
    "spelling-all": ("dassle-spelling", "all"),
    "spelling-initial-uv": ("dassle-spelling", "initial_uv"),
    "spelling-without-initial-uv": ("dassle-spelling", "without_initial_uv"),
    "preservation-all": ("dassle-spelling-preservation", "all"),
}

EXPECTED_INDEX_COLUMNS = {
    "meta": ("key", "value"),
    "unigram": ("word", "count"),
    "bigram": ("phrase", "count"),
    "trigram": ("phrase", "count"),
    "middle": ("left_word", "right_word", "middle_word", "count"),
}
EXPECTED_INDEX_ROWS = {"unigram": 141_162, "bigram": 37_720, "trigram": 10_930, "middle": 10_930}
EXPECTED_INDEX_META = {"unigram_absence": "UNAVAILABLE", "ngram_absence": "CENSORED"}

# Worktree changes permitted while increment 1 runs: the strategy-published
# 007-m order plus this increment's own new files (untracked only).
EXPECTED_STRATEGY_FILES = frozenset({"oap/orders/007-m-rank-ambiguous-levenshtein-candidates.md"})
NEW_007M_FILES = frozenset(
    {
        "research/levenshtein_rank.py",
        "research/tools/run_levenshtein_rank.py",
        "research/tests/test_levenshtein_rank.py",
    }
)

TOP_K = rank.TOP_K

# First 007-m census root (scalar display-order rank defect).  It is immutable
# diagnostic evidence, superseded for headroom reporting by this run's root.
SUPERSEDED_CENSUS_ROOT = "007-m-rank-ambiguous-levenshtein-candidates-recovery.e6ca66"

# Increment 2 frozen identities: the accepted census root, the 007-j C=1
# observation evidence, and the strategy-accepted live profile hash.
DISPATCH_POLICY = "at most one CPU-selected candidate per C>1 target; tied tops select nothing"

EXPECTED_007J_CANDIDATES = "db8add38f4e74a657af416b47c4dee59b6fd598ee14f30aea58687b0adbcfacd"
EXPECTED_007J_CASE_RESULTS = "7aa79d0fb7bf904fc8403ab7800ff27dd763d9e73018d81dd06e8d3c0450ef10"
EXPECTED_007J_REUSE_RECORDS = "87cbaa24ea8400738b95010d173d7aa238b9f6e59ddde4c5f5e9bb6f9ecb8aaa"
EXPECTED_007J_C1_TOTAL = 1_035
EXPECTED_007J_C1_COUNTS = {"dassle-spelling": 826, "dassle-spelling-preservation": 209}
EXPECTED_007J_REQUEST_TREE = {
    "file_count": 4_140,
    "total_bytes": 6_486_683,
    "sha256sum_manifest_sha256": (
        "feb785a76b2e4d83bcb01ce532d89e9e6d47cdcdcb45e2b0880453dd11fcb55b"
    ),
}
EXPECTED_CENSUS_ROOT = "007-m-rank-ambiguous-levenshtein-candidates-recovery.97f59c"
EXPECTED_CENSUS_SHA = {
    "RANK-POPULATION.json": ("a2440f25a21da6d41d0b174a573e336c019e531fb07d468a87cbee22ca74b28a"),
    "DISPATCH-MANIFEST.json": ("eebdb900fd8641fd6d26b569407d721ee8007a4052eaa6d5026f85793babb66c"),
    "RANK-AGGREGATE.json": ("d20d7039e2cd2be63454ac87b38d44a8f7c09d48be7c33d7fdc8a0e6a5c270bb"),
    "SOURCE.json": "6c24b2bb7ab50e94b995840778c5d8fde4e0d77317b5a6132aa4fbf0346ca833",
    "INDEX-SCHEMA.json": ("c95da28ea8f57b2036c884b5b268bf18398417219c4297b2b08999b1ad029f56"),
    "RUN-STATUS.json": "9f3a13762c2bac607f271daf762640dab563baf5663e874f6534a37662d9ce83",
    "CENSUS-SUMMARY.json": ("5fc32cb8d123a224eac1f1ebcbaefa7f2d90d5114a9b4556b62f654e42342030"),
    "INPUT-MANIFEST.json": ("b00a1b8dcd8c4cdf4b181601892a094824af7a3268a4785d56149a05807fa399"),
}
# Strategy-accepted drift decision: the live profile is semantically verified
# as the same endpoint, model and Responses protocol with the request itself
# freezing low reasoning, but its bytes differ from the frozen 007-j profile.
EXPECTED_007M_PROFILE_SHA256 = "0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e"
C_GT_1_REUSE_DISABLED = "frozen-profile-identity-mismatch-reuse-disabled-by-strategy"

# Failed-instrument root, preserved unchanged as evidence.  Its frozen
# verifier (88ca4dfe) rejected the canonical interrupted-finalization file
# set, so it cannot complete its own live resume.  The adoption harness binds
# this exact identity; nothing in that root is ever resampled.
EXPECTED_FAILED_ROOT = "007-m-rank-ambiguous-levenshtein-candidates-recovery.ffdf13"
EXPECTED_FAILED_ROOT_CONFIGURATION = (
    "2852655e7ed8cc268f5166195c36a174484ef3f498b8df849873c764eb1d14a5"
)
EXPECTED_FAILED_ROOT_HEAD = "88ca4dfe19740aa21156457d42966661f67902ea"
EXPECTED_FAILED_ROOT_RUN_STATUS = (
    "f815f59fae53827a9cba672a78c7e5ce104c5ff3ffc25333392ab88eef624061"
)
EXPECTED_FAILED_ROOT_REQUEST_TREE = {
    "file_count": 4_940,
    "total_bytes": 7_725_994,
    "sha256sum_manifest_sha256": (
        "3866111815e7e81d2bfbb1c5075fa94c24439bdc9cd5a8a893d47811ea50f26e"
    ),
}
EXPECTED_ADOPTED_COMPLETED_ATTEMPTED = 188
EXPECTED_ADOPTED_COMPLETED_UNCERTAIN = 8
EXPECTED_ADOPTED_REQUEST_ONLY = 8
EXPECTED_ADOPTED_FRESH = 678
EXPECTED_ADOPTED_FRESH_COUNTS = {
    "dassle-spelling": 447,
    "dassle-spelling-preservation": 231,
}

# Second failed-instrument root, preserved unchanged as evidence.  All 882
# C>1 observations and the 1035 C=1 observations completed and persisted
# under 92bee3a (678 fresh calls, zero resampling); only the 007-j replay
# identity gate blocked its aggregation because it compared in-memory
# tuple-typed attribution fields against the JSON-normalized persisted rows.
EXPECTED_SECOND_FAILED_ROOT = (
    "007-m-rank-ambiguous-levenshtein-candidates-recovery.090ea8"
)
EXPECTED_SECOND_FAILED_ROOT_CONFIGURATION = (
    "6b841ec1765059d462ff9f5761549aa0b3b7687005d5304299ea8bed8eddd816"
)
EXPECTED_SECOND_FAILED_ROOT_HEAD = "92bee3a214aa50ef3921f54488545a57d9a95000"
EXPECTED_SECOND_FAILED_ROOT_RUN_STATUS = (
    "f071c164926404abb42b64b22434fe839e5e47e68aa77ede1b6993eff115cd82"
)
EXPECTED_SECOND_FAILED_ROOT_REQUEST_TREE = {
    "file_count": 7_668,
    "total_bytes": 12_140_924,
    "sha256sum_manifest_sha256": (
        "6e287f3c835285d5a31132f42c31878dc91099dc91783debb9900123c033b449"
    ),
}
EXPECTED_SECOND_ADOPTED_COMPLETED_ATTEMPTED = 866
EXPECTED_SECOND_ADOPTED_COMPLETED_UNCERTAIN = 16
EXPECTED_SECOND_ADOPTED_REQUEST_ONLY = 0
EXPECTED_SECOND_ADOPTED_FRESH = 0
EXPECTED_SECOND_ADOPTED_FRESH_COUNTS = {
    "dassle-spelling": 0,
    "dassle-spelling-preservation": 0,
}

LIVE_CODE_FILES = (
    "research/levenshtein_rank.py",
    "research/tools/run_levenshtein_rank.py",
    "research/tests/test_levenshtein_rank.py",
)
SOURCE_007J_EVIDENCE = {
    "CANDIDATES.json": EXPECTED_007J_CANDIDATES,
    "CASE-RESULTS.json": EXPECTED_007J_CASE_RESULTS,
    "RESULTS.json": EXPECTED_007J_RESULTS,
    "REUSE-RECORDS.json": EXPECTED_007J_REUSE_RECORDS,
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
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExperimentError(f"invalid private JSON artifact: {path.name}") from exc


def json_normalized_equal(left: object, right: object) -> bool:
    """Compare values the way the frozen persistence layer stores them.

    Canonical JSON round-trips in-memory tuples to JSON arrays, so this
    comparison is byte-faithful to what immutable_json persisted.
    """
    return canonical_bytes(left) == canonical_bytes(right)


def _git(repo_root: Path, *arguments: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ExperimentError("implementation Git identity cannot be read") from exc
    return completed.stdout


def verify_implementation_identity(repo_root: Path, expected_head: str) -> dict[str, Any]:
    """Prove the branch head and the exact permitted worktree state."""
    head = _git(repo_root, "rev-parse", "--verify", "HEAD").strip()
    branch = _git(repo_root, "symbolic-ref", "--quiet", "--short", "HEAD").strip()
    status = _git(repo_root, "status", "--porcelain=v1", "--untracked-files=all")
    if head != expected_head:
        raise ExperimentError("implementation head is not the expected report head")
    if branch != BRANCH:
        raise ExperimentError("implementation branch is not the objective branch")
    for line in status.splitlines():
        if not line:
            continue
        code, path = line[:2], line[3:]
        if code == "??":
            if path not in EXPECTED_STRATEGY_FILES | NEW_007M_FILES:
                raise ExperimentError(f"unexpected untracked worktree file: {path}")
        else:
            raise ExperimentError(f"unexpected tracked worktree change: {code} {path}")
    return {"implementation_head": head, "branch": branch}


def ensure_scratch(scratch: Path) -> None:
    scratch = scratch.absolute()
    if scratch.parent != NATIVE_RUNTIME_PARENT:
        raise ExperimentError(
            "007-m private root must be directly beneath the native runtime parent"
        )
    validator_driver.require_owned_dir(NATIVE_RUNTIME_PARENT)
    if not scratch.name.startswith(SCRATCH_NAME_PREFIX):
        raise ExperimentError("007-m private root name is not a unique recovery root")
    if scratch.exists() or scratch.is_symlink():
        validator_driver.require_owned_dir(scratch)
        return
    scratch.mkdir(mode=0o700)
    validator_driver.require_owned_dir(scratch)


def verify_source_root(source_root: Path) -> dict[str, Any]:
    """Verify the completed frozen 007-j root before reading any of its trees."""
    validator_driver.require_owned_dir(source_root)
    expected = {
        "CONFIGURATION.json": EXPECTED_007J_CONFIGURATION,
        "CANDIDATE-MANIFEST.json": EXPECTED_007J_CANDIDATE_MANIFEST,
        "RESULTS.json": EXPECTED_007J_RESULTS,
    }
    for name in (*expected, "RUN-STATUS.json", "INPUT-MANIFEST.json"):
        validator_driver.require_private_file(source_root / name)
    for name, digest in expected.items():
        validator_driver.require_private_file(source_root / name, expected_sha=digest)
    status = read_json(source_root / "RUN-STATUS.json")
    if (
        not isinstance(status, dict)
        or status.get("status") != "COMPLETE"
        or status.get("run_id") != "007-j"
        or status.get("configuration_sha256") != EXPECTED_007J_CONFIGURATION
        or status.get("candidate_manifest_sha256") != EXPECTED_007J_CANDIDATE_MANIFEST
        or status.get("private_results_sha256") != EXPECTED_007J_RESULTS
    ):
        raise ExperimentError("007-j source run status is not the completed identity")
    _check_007j_configuration(read_json(source_root / "CONFIGURATION.json"))
    _check_007j_baseline(read_json(source_root / "RESULTS.json"))
    for name in ("inputs", "cases"):
        validator_driver.require_owned_dir(source_root / name)
    return {
        "source_root": str(source_root),
        "source_experiment": "007-j-levenshtein-one-contextual-validator",
        "configuration_sha256": EXPECTED_007J_CONFIGURATION,
        "candidate_manifest_sha256": EXPECTED_007J_CANDIDATE_MANIFEST,
        "results_sha256": EXPECTED_007J_RESULTS,
    }


def _check_007j_configuration(configuration: Any) -> None:
    if not isinstance(configuration, dict):
        raise ExperimentError("007-j configuration is not an object")
    identity = configuration.get("source_identity")
    if not isinstance(identity, dict):
        raise ExperimentError("007-j configuration lacks source identity")
    checks = [
        configuration.get("experiment_id") == "007-j-levenshtein-one-contextual-validator",
        configuration.get("run_id") == "007-j",
        configuration.get("status") == "FROZEN_BEFORE_LIVE_EXECUTION",
        identity.get("candidate_manifest_sha256") == EXPECTED_007J_CANDIDATE_MANIFEST,
        identity.get("candidate_counts") == prior_j.EXPECTED_CANDIDATES,
        identity.get("transition_matrix") == prior_j.TRANSITION_EXPECTED,
        identity.get("entering_targets") == prior_j.EXPECTED_ENTERING,
        (configuration.get("prompt") or {}).get("sha256") == protocol.FROZEN_PROMPT_SHA256,
        (configuration.get("deployment") or {}).get("model") == protocol.MODEL,
        (configuration.get("deployment") or {}).get("profile_sha256") == prior_j.EXPECTED_PROFILE,
        (configuration.get("prior_007i_identity") or {}).get("configuration_sha256")
        == prior_j.EXPECTED_PRIOR_CONFIG,
    ]
    if not all(checks):
        raise ExperimentError("007-j configuration identity fields drifted")


def _check_007j_baseline(results: Any) -> None:
    if not isinstance(results, dict):
        raise ExperimentError("007-j results are not an object")
    views = (results.get("metrics") or {}).get("views")
    if not isinstance(views, dict):
        raise ExperimentError("007-j results lack metrics views")
    for slice_name, (tp, fn) in EXPECTED_SLICE_BASELINE.items():
        phase, view = SLICE_VIEW[slice_name]
        fallback = ((views.get(phase) or {}).get(view) or {}).get("validated_fallback")
        if not isinstance(fallback, dict) or fallback.get("tp") != tp or fallback.get("fn") != fn:
            raise ExperimentError(f"007-j baseline tp/fn drifted for {slice_name}")


class IndexQueries:
    """Read-only frozen-index evidence queries with the frozen absence contract.

    Unigram absence is UNAVAILABLE; bigram/trigram absence is CENSORED because
    the index is truncated near 2 per million with an unknown denominator.
    """

    def __init__(self, path: Path) -> None:
        validator_driver.require_private_file(path)
        try:
            self.connection = sqlite3.connect(path.as_uri() + "?mode=ro&immutable=1", uri=True)
        except sqlite3.Error as exc:
            raise ExperimentError("frozen index cannot be opened read-only") from exc

    def close(self) -> None:
        try:
            self.connection.close()
        except sqlite3.Error as exc:
            raise ExperimentError("frozen index cannot be closed") from exc

    def unigram(self, word: str) -> tuple[str, int | None]:
        row = self.connection.execute(
            "SELECT count FROM unigram WHERE word=?", (word.casefold(),)
        ).fetchone()
        return (rank.EXACT, int(row[0])) if row else (rank.UNAVAILABLE, None)

    def ngram(self, phrase: str, length: int) -> tuple[str, int | None]:
        if length not in (2, 3):
            raise ExperimentError("ngram query length is outside the frozen contract")
        table = "bigram" if length == 2 else "trigram"
        key = " ".join(part.casefold() for part in phrase.split())
        row = self.connection.execute(
            f"SELECT count FROM {table} WHERE phrase=?", (key,)
        ).fetchone()
        return (rank.EXACT, int(row[0])) if row else (rank.CENSORED, None)


def verify_index_schema(index: IndexQueries) -> dict[str, Any]:
    """Mechanically confirm unigram/bigram/trigram evidence in the frozen schema."""
    try:
        rows = index.connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    except sqlite3.Error as exc:
        raise ExperimentError("frozen index schema cannot be read") from exc
    names = {row[0] for row in rows}
    if names != set(EXPECTED_INDEX_COLUMNS):
        raise ExperimentError(f"frozen index table set drifted: {sorted(names)}")
    tables: dict[str, Any] = {}
    for name, columns in EXPECTED_INDEX_COLUMNS.items():
        try:
            info = index.connection.execute(f"PRAGMA table_info({name})").fetchall()
        except sqlite3.Error as exc:
            raise ExperimentError(f"frozen index {name} schema cannot be read") from exc
        actual = tuple(row[1] for row in info)
        if actual != columns:
            raise ExperimentError(f"frozen index {name} columns drifted")
        count: int | None = None
        if name in EXPECTED_INDEX_ROWS:
            count = index.connection.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
            if count != EXPECTED_INDEX_ROWS[name]:
                raise ExperimentError(f"frozen index {name} row count drifted")
        tables[name] = {"columns": list(columns), "row_count": count}
    meta: dict[str, str] = {}
    try:
        meta = {
            row[0]: row[1]
            for row in index.connection.execute("SELECT key, value FROM meta").fetchall()
        }
    except sqlite3.Error as exc:
        raise ExperimentError("frozen index meta cannot be read") from exc
    for key, expected in EXPECTED_INDEX_META.items():
        if meta.get(key) != expected:
            raise ExperimentError(f"frozen index meta contract drifted for {key}")
    return {"tables": tables, "meta": {key: meta[key] for key in sorted(meta)}}


def _cardinality(count: int) -> str:
    return "C=0" if count == 0 else "C=1" if count == 1 else "C>1"


def verify_007j_c1_identity(
    records: dict[str, list[dict[str, Any]]],
    vocabulary: set[str],
    deletion_index: Mapping[str, Any],
) -> tuple[str, list[dict[str, Any]]]:
    """Re-run the frozen 007-j builder and require its exact candidate manifest."""
    population, _analysis = prior_j.build_population(records, vocabulary, deletion_index)
    _manifest, digest = protocol.candidate_manifest(population)
    if digest != EXPECTED_007J_CANDIDATE_MANIFEST:
        raise ExperimentError(f"007-j C=1 candidate identity drift: {digest}")
    return digest, population


def build_c_gt_1_population(
    records: dict[str, list[dict[str, Any]]],
    vocabulary: set[str],
    deletion_index: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Recompute the frozen 007-j enumeration and keep the complete C>1 sets.

    Admission, drift checks, and the frozen 007-j transition matrix are the
    exact 007-j semantics; only the retained population differs (complete C>1
    candidate unions instead of the new unique candidates).
    """
    population: list[dict[str, Any]] = []
    transitions: dict[str, Counter[str]] = {
        phase: Counter({key: 0 for key in prior_j.TRANSITION_EXPECTED[phase]}) for phase in PHASES
    }
    c0_counts: Counter[str] = Counter()
    entering: Counter[str] = Counter()
    lookup_seconds = 0.0
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
                if prior_j.is_english_review_suppressed(target):
                    continue
                entering[phase] += 1
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
                started = time.monotonic()
                all_forms = distance_one.distance_one_candidates(
                    lookup, vocabulary, deletion_index=deletion_index
                )
                lookup_seconds += time.monotonic() - started
                old_forms: list[str] = []
                for item in all_forms:
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
                new_cardinality = _cardinality(len(all_forms))
                if old_cardinality == "C=1" and new_cardinality == "C=1":
                    transition = (
                        "C=1 -> same unique candidate"
                        if old_forms[0] == all_forms[0]["text"]
                        else "C=1 -> different unique candidate"
                    )
                else:
                    transition = f"{old_cardinality} -> {new_cardinality}"
                transitions[phase][transition] += 1
                if new_cardinality != "C>1":
                    if new_cardinality == "C=0":
                        c0_counts[phase] += 1
                    continue
                population.append(
                    {
                        "phase": phase,
                        "case_index": int(case["index"]),
                        "case_id": case["id"],
                        "target_ordinal": ordinal,
                        "target_start": start,
                        "target_end": end,
                        "candidate": copy.deepcopy(candidate),
                        "transition": transition,
                        "cardinality": new_cardinality,
                        "sentence": original,
                        "reference": case["dataset"].get("reference"),
                        "candidates": copy.deepcopy(all_forms),
                    }
                )
    if dict(entering) != prior_j.EXPECTED_ENTERING:
        raise ExperimentError(f"entering population mismatch: {dict(entering)}")
    observed_transitions = {phase: dict(values) for phase, values in transitions.items()}
    if observed_transitions != prior_j.TRANSITION_EXPECTED:
        raise ExperimentError(f"candidate transition matrix mismatch: {observed_transitions}")
    c_gt_1_counts = {
        phase: sum(1 for item in population if item["phase"] == phase) for phase in PHASES
    }
    if c_gt_1_counts != EXPECTED_C_GT_1 or len(population) != EXPECTED_C_GT_1_TOTAL:
        raise ExperimentError(
            "C>1 population mismatch: observed "
            f"{c_gt_1_counts} total {len(population)}, expected "
            f"{EXPECTED_C_GT_1} total {EXPECTED_C_GT_1_TOTAL}"
        )
    analysis = {
        "entering_targets": dict(entering),
        "transition_matrix": observed_transitions,
        "c0_counts": dict(c0_counts),
        "c_gt_1_counts": c_gt_1_counts,
        "lookup_seconds": lookup_seconds,
    }
    return protocol.ordered_candidates(population), analysis


def _mechanical_edit(
    sentence: str,
    candidate: Mapping[str, Any],
    form: str,
    vocabulary: set[str],
) -> list[Any] | None:
    gate = mechanical_substitution(sentence, dict(candidate), form, vocabulary)
    if not gate.get("accepted"):
        return None
    edit = gate.get("edit")
    return edit if isinstance(edit, list) else None


def _reference_headroom(
    item: dict[str, Any],
    ranking: rank.TargetRanking,
    vocabulary: set[str],
) -> dict[str, Any]:
    """Post-ranking gold analysis only: presence, interval, coverage, units.

    The reference rank persists the tie-aware interval of the best score
    group containing an exact-reference candidate; no candidate inside a tie
    is chosen and no scalar rank is fabricated from display order.  For each
    k, ``certain`` means the whole group is within top-k (rank_max <= k) and
    ``possible`` means the best member of the group could be within top-k
    (rank_min <= k); a straddling group is never collapsed into a rank.
    """
    reference = item["reference"]
    if not isinstance(reference, str):
        return {
            "present": False,
            "rank_interval": None,
            "top_k": {str(k): {"certain": False, "possible": False} for k in TOP_K},
            "oracle_gold_units": 0,
            "reference_candidates": 0,
        }
    sentence = item["sentence"]
    candidate = item["candidate"]
    intervals = ranking.rank_intervals
    reference_intervals: list[rank.RankInterval] = []
    for score in ranking.rank_order:
        edit = _mechanical_edit(sentence, candidate, score.text, vocabulary)
        if edit is None:
            continue
        attribution = protocol.attribution(sentence, reference, edit)
        if attribution.get("status") == "exact_reference":
            reference_intervals.append(intervals[score.text])
    present = bool(reference_intervals)
    best = (
        min(reference_intervals, key=lambda value: (value.rank_min, value.rank_max))
        if present
        else None
    )
    return {
        "present": present,
        "rank_interval": best.as_dict() if best is not None else None,
        "top_k": {
            str(k): {
                "certain": best is not None and best.rank_max <= k,
                "possible": best is not None and best.rank_min <= k,
            }
            for k in TOP_K
        },
        "oracle_gold_units": 1 if present else 0,
        "reference_candidates": len(reference_intervals),
    }


def _dispatch_payload(
    item: dict[str, Any],
    ranking: rank.TargetRanking,
    vocabulary: set[str],
) -> dict[str, Any] | None:
    """Build the at-most-one candidate payload a later dispatch may receive."""
    if ranking.tied or ranking.top is None:
        return None
    sentence = item["sentence"]
    candidate = item["candidate"]
    edit = _mechanical_edit(sentence, candidate, ranking.top.text, vocabulary)
    if edit is None:
        return {
            "selected": False,
            "reason": "mechanical-gate-rejected",
            "candidate_form": ranking.top.text,
        }
    prompt = protocol.prompt_text(sentence, str(candidate["text"]), ranking.top.text)
    return {
        "selected": True,
        "phase": item["phase"],
        "case_index": item["case_index"],
        "case_id": item["case_id"],
        "target_ordinal": item["target_ordinal"],
        "target_start": item["target_start"],
        "target_end": item["target_end"],
        "candidate": copy.deepcopy(candidate),
        "candidate_form": ranking.top.text,
        "operation": ranking.top.operation,
        "mechanical_edit": copy.deepcopy(edit),
        "sentence": sentence,
        "score": list(ranking.top.score),
        "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
    }


def _median(values: list[int]) -> int | float | None:
    return statistics.median(values) if values else None


def _percentile(values: list[int], q: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, math.ceil(q * len(ordered)) - 1)]


def _slice_aggregate(
    records: list[dict[str, Any]],
    predicate: Any,
) -> dict[str, Any]:
    slice_records = [record for record in records if predicate(record)]
    set_sizes = [record["set_size"] for record in slice_records]
    operations: Counter[str] = Counter()
    unique_top = tied_top = 0
    reference_present = reference_absent = 0
    rank_mins: list[int] = []
    rank_maxs: list[int] = []
    top_k_certain = {str(k): 0 for k in TOP_K}
    top_k_possible = {str(k): 0 for k in TOP_K}
    lower_tie_groups = 0
    reference_group_tied = 0
    oracle_units = 0
    dispatchable = 0
    for record in slice_records:
        for entry in record["ranking"]["candidates"]:
            operations[str(entry["operation"])] += 1
        ranking = record["ranking"]
        if ranking["tied"]:
            tied_top += 1
        else:
            unique_top += 1
            dispatch = record["dispatch"]
            if isinstance(dispatch, dict) and dispatch.get("selected") is True:
                dispatchable += 1
        lower_tie_groups += sum(1 for group in ranking["tie_groups"] if not group["top_group"])
        headroom = record["reference_headroom"]
        if headroom["present"]:
            reference_present += 1
            interval = headroom["rank_interval"]
            rank_mins.append(interval["min"])
            rank_maxs.append(interval["max"])
            if interval["max"] > interval["min"]:
                reference_group_tied += 1
            for k in TOP_K:
                top_k_state = headroom["top_k"][str(k)]
                if top_k_state["certain"]:
                    top_k_certain[str(k)] += 1
                if top_k_state["possible"]:
                    top_k_possible[str(k)] += 1
        else:
            reference_absent += 1
        oracle_units += headroom["oracle_gold_units"]
    target_count = len(slice_records)
    return {
        "target_count": target_count,
        "total_candidate_pairs": sum(set_sizes),
        "set_size": {
            "min": min(set_sizes) if set_sizes else None,
            "median": _median(set_sizes),
            "p90": _percentile(set_sizes, 0.90),
            "p95": _percentile(set_sizes, 0.95),
            "p99": _percentile(set_sizes, 0.99),
            "max": max(set_sizes) if set_sizes else None,
        },
        "operation_composition": {
            operation: operations[operation] for operation in sorted(operations)
        },
        "unique_top": unique_top,
        "tied_top": tied_top,
        "unique_top_rate": unique_top / target_count if target_count else None,
        "tied_top_rate": tied_top / target_count if target_count else None,
        "reference_present": reference_present,
        "reference_absent": reference_absent,
        "reference_rank": {
            "rank_min": {
                "min": min(rank_mins) if rank_mins else None,
                "median": _median(rank_mins),
                "p95": _percentile(rank_mins, 0.95),
                "max": max(rank_mins) if rank_mins else None,
            },
            "rank_max": {
                "min": min(rank_maxs) if rank_maxs else None,
                "median": _median(rank_maxs),
                "p95": _percentile(rank_maxs, 0.95),
                "max": max(rank_maxs) if rank_maxs else None,
            },
        },
        "top_k_coverage": {
            str(k): {
                "certain": {
                    "count": top_k_certain[str(k)],
                    "rate_among_present": (
                        top_k_certain[str(k)] / reference_present if reference_present else None
                    ),
                },
                "possible": {
                    "count": top_k_possible[str(k)],
                    "rate_among_present": (
                        top_k_possible[str(k)] / reference_present if reference_present else None
                    ),
                },
                "straddling": top_k_possible[str(k)] - top_k_certain[str(k)],
            }
            for k in TOP_K
        },
        "lower_tie_groups": lower_tie_groups,
        "reference_group_tied": reference_group_tied,
        "oracle_gold_units": oracle_units,
        "dispatchable_unique_tops": dispatchable,
    }


def _recall_ceiling(baseline: tuple[int, int] | None, oracle_units: int) -> dict[str, Any]:
    if baseline is None:
        return {
            "frozen_tp": None,
            "frozen_fn": None,
            "frozen_recall": None,
            "ceiling": None,
            "numerator": None,
            "denominator": None,
        }
    tp, fn = baseline
    denominator = tp + fn
    numerator = tp + oracle_units
    return {
        "frozen_tp": tp,
        "frozen_fn": fn,
        "frozen_recall": tp / denominator if denominator else None,
        "ceiling": numerator / denominator if denominator else None,
        "numerator": numerator if denominator else None,
        "denominator": denominator,
    }


def census_population(
    population: list[dict[str, Any]],
    index: IndexQueries,
    vocabulary: set[str],
    uv_indices: set[int],
    slice_baseline: Mapping[str, tuple[int, int]] | None = None,
) -> dict[str, Any]:
    """Rank the complete C>1 population and aggregate the census.

    Gold is used strictly after ranking, only for the reference headroom
    projection; it cannot affect any score, rank, or selection.
    """
    slice_baseline = dict(EXPECTED_SLICE_BASELINE if slice_baseline is None else slice_baseline)
    records: list[dict[str, Any]] = []
    dispatch_pairs: list[tuple[rank.TargetRanking, dict[str, Any]]] = []
    ranking_seconds = 0.0
    headroom_seconds = 0.0
    for item in population:
        candidate = item["candidate"]
        lookup = str(candidate["text"]).casefold()
        started = time.perf_counter()
        context = rank.extract_context(candidate.get("evidence") or {}, lookup)
        ranking = rank.rank_candidates(item["candidates"], context, index.unigram, index.ngram)
        ranking_seconds += time.perf_counter() - started
        started = time.perf_counter()
        headroom = _reference_headroom(item, ranking, vocabulary)
        payload = _dispatch_payload(item, ranking, vocabulary)
        headroom_seconds += time.perf_counter() - started
        if isinstance(payload, dict) and payload.get("selected") is True:
            dispatch_pairs.append((ranking, payload))
        records.append(
            {
                "phase": item["phase"],
                "case_index": item["case_index"],
                "case_id": item["case_id"],
                "target_ordinal": item["target_ordinal"],
                "target_start": item["target_start"],
                "target_end": item["target_end"],
                "transition": item["transition"],
                "set_size": len(item["candidates"]),
                "target_text": candidate["text"],
                "sentence": item["sentence"],
                "gold_sentence": item["reference"],
                "context": {
                    "left_word": context.left_word,
                    "right_word": context.right_word,
                },
                "ranking": ranking.to_dict(),
                "reference_headroom": headroom,
                "dispatch": payload,
            }
        )
    dispatch = rank.select_for_dispatch(dispatch_pairs)
    slice_selectors = {
        "spelling-all": lambda item: item["phase"] == "dassle-spelling",
        "spelling-initial-uv": lambda item: (
            item["phase"] == "dassle-spelling" and item["case_index"] in uv_indices
        ),
        "spelling-without-initial-uv": lambda item: (
            item["phase"] == "dassle-spelling" and item["case_index"] not in uv_indices
        ),
        "preservation-all": lambda item: item["phase"] == "dassle-spelling-preservation",
    }
    slices: dict[str, Any] = {}
    for name in (
        "spelling-all",
        "spelling-initial-uv",
        "spelling-without-initial-uv",
        "preservation-all",
    ):
        aggregate = _slice_aggregate(records, slice_selectors[name])
        aggregate["baseline"] = _recall_ceiling(
            slice_baseline.get(name), aggregate["oracle_gold_units"]
        )
        slices[name] = aggregate
    totals = _slice_aggregate(records, lambda item: True)
    totals["baseline"] = None
    return {
        "records": records,
        "dispatch": dispatch,
        "slices": slices,
        "totals": totals,
        "ranking_seconds": ranking_seconds,
        "headroom_seconds": headroom_seconds,
    }


def public_projection(
    identity: dict[str, Any],
    schema: dict[str, Any],
    analysis: dict[str, Any],
    census: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build the data-free public configuration and aggregate result."""
    public_configuration = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "run_id": RUN_ID,
        "status": "CPU_CENSUS_COMPLETE",
        "implementation_head": identity["implementation_head"],
        "implementation_branch": identity["branch"],
        "frozen_source_identity": {
            "source_experiment": "007-j-levenshtein-one-contextual-validator",
            "source_configuration_sha256": identity.get("configuration_sha256"),
            "source_candidate_manifest_sha256": identity.get("candidate_manifest_sha256"),
            "source_results_sha256": identity.get("results_sha256"),
            "case_identity_manifest_sha256": prior_j.EXPECTED_PRIOR_CASES,
        },
        "index_schema": schema,
        "ranking_rule": {
            "order": "lexicographic descending",
            "tuple": [
                "trigram_exact_flag",
                "trigram_exact_count",
                "exact_bigram_side_count",
                "sum_of_exact_bigram_counts",
                "unigram_exact_count",
            ],
            "substitution": (
                "hypothetical candidate into the frozen immediate left/right context only"
            ),
            "evidence_states": ["EXACT", "CENSORED", "UNAVAILABLE"],
            "absence_contract": dict(EXPECTED_INDEX_META),
            "placeholder_semantics": (
                "numeric placeholders after exactness flags are comparison machinery "
                "only; missing or censored evidence is never reported as zero"
            ),
            "tie_policy": (
                "exact top-score tie selects nothing; no validator call; original retained"
            ),
            "rank_reporting": (
                "tie-aware competition intervals [rank_min, rank_max]; no scalar "
                "rank is derived from display order and no candidate inside a "
                "tie is chosen"
            ),
            "top_k_reporting": (
                "certain = reference rank_max <= k; possible = reference "
                "rank_min <= k, among present references"
            ),
            "non_scored_fields": ["operation", "candidate_text_order"],
            "gold": (
                "structurally absent from ranking and score inputs; post-ranking "
                "headroom analysis only"
            ),
        },
        "population": {
            "expected": {**EXPECTED_C_GT_1, "total": EXPECTED_C_GT_1_TOTAL},
            "observed": {
                **analysis["c_gt_1_counts"],
                "total": sum(analysis["c_gt_1_counts"].values()),
            },
            "c0_counts": analysis["c0_counts"],
            "entering_targets": analysis["entering_targets"],
            "transition_matrix": analysis["transition_matrix"],
        },
        "baseline": {
            slice_name: {"frozen_tp": tp, "frozen_fn": fn}
            for slice_name, (tp, fn) in EXPECTED_SLICE_BASELINE.items()
        },
        "privacy": {
            "public": "aggregate census metrics, hashes, and frozen identities only",
            "private": (
                "sentences, targets, candidates, gold, prompts, and row-level "
                "evidence remain in the private native root"
            ),
        },
        "no_model_calls": True,
    }
    public_configuration["configuration_sha256"] = sha256_bytes(
        canonical_bytes(public_configuration)
    )
    public_result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "run_id": RUN_ID,
        "status": "CPU_CENSUS_COMPLETE",
        "implementation_head": identity["implementation_head"],
        "configuration_sha256": public_configuration["configuration_sha256"],
        "slices": census["slices"],
        "totals": census["totals"],
        "runtime": census["runtime"],
        "private_evidence_sha256": census.get("private_sha256"),
        "limitations": [
            (
                "Same-sample exploratory census on the frozen 007-j C>1 population; "
                "not held-out confirmation."
            ),
            "Gold is post-ranking analysis only and cannot affect selection.",
            ("No model calls were made; validator dispatch is a later supervised increment."),
            "No merge, release, deployment, or product linguistic acceptance is authorized.",
        ],
    }
    return public_configuration, public_result


def write_public(
    repo_root: Path, public_configuration: dict[str, Any], public_result: dict[str, Any]
) -> dict[str, str]:
    paths = {
        "config": repo_root / "research" / "configs" / f"{EXPERIMENT_ID}.json",
        "result": repo_root / "research" / "results" / f"{EXPERIMENT_ID}.json.gz",
    }
    validator_driver.public_immutable_write(paths["config"], canonical_bytes(public_configuration))
    validator_driver.public_immutable_write(
        paths["result"], gzip.compress(canonical_bytes(public_result), mtime=0)
    )
    return {key: sha256_file(path) for key, path in paths.items()}


# ---------------------------------------------------------------------------
# Increment 2: live finite C>1 execution on the frozen 007-j validator.
#
# Method (fixed by the order): C=0 keeps the exact preserved 007-j behavior;
# C=1 keeps the exact preserved 007-j observations, copied byte-for-byte into
# this private root with zero new calls; for each unique CPU top in C>1 the
# frozen validator sees exactly that one candidate.  USE_CANDIDATE applies only
# the supplied candidate through the unchanged gates; KEEP_ORIGINAL,
# UNCERTAIN, protocol or operational failure, and a tied top keep the original
# target; a runner-up is never tried.  The primary projection is
# validated_only over all scheduled targets; rejected C>1 targets never fall
# back to the old ordinary-Qwen behavior.
#
# C>1 observation reuse is disabled by the strategy drift decision: the live
# profile hash is the strategy-accepted 007-m fresh-call identity and differs
# from the frozen 007-j profile hash, so the exact identity gate can never be
# satisfied.  reused=0, fresh=882.  No public artifact is published here.
#
# Harness revision (this head): verify_c_gt_1_observations accepts the
# canonical interrupted-finalization file set -- request.json, the stale
# ATTEMPTED dispatch.json marker, and raw/observation UNKNOWN with
# INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE -- as an uncertain delivery that
# stays distinguishable from a completed ATTEMPTED observation.  The
# cross-root adoption harness (prepare_adopted_live) reuses the preserved
# failed root ffdf13: 196 completed C>1 observations are copied under exact
# request/raw/observation/profile/prompt/parser identity, 8 request+dispatch
# interruptions are carried to conservative uncertain observations without
# any call, and only the remaining 678 requests are scheduled fresh.
# ---------------------------------------------------------------------------


def _git_bytes(repo_root: Path, *arguments: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), *arguments],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ExperimentError("implementation Git identity cannot be read") from exc
    return completed.stdout


def verify_live_implementation_identity(repo_root: Path, expected_head: str) -> dict[str, Any]:
    """Prove a clean worktree at the freeze head and bind every 007-m blob."""
    identity = validator_driver.source_and_code_identity(repo_root, expected_head)
    for relative in LIVE_CODE_FILES:
        repo_file = repo_root / relative
        validator_driver.require_owned_file(repo_file)
        blob = _git_bytes(repo_root, "show", f"HEAD:{relative}")
        if repo_file.read_bytes() != blob:
            raise ExperimentError(f"007-m implementation bytes differ from HEAD: {relative}")
        identity["head_blobs"][relative] = {"sha256": sha256_bytes(blob)}
    return identity


def verify_007j_request_tree(source_root: Path) -> dict[str, Any]:
    identity = validator_driver.request_tree_identity(source_root / "requests")
    if identity != EXPECTED_007J_REQUEST_TREE:
        raise ExperimentError("007-j request tree identity changed")
    return identity


def verify_census_root(census_root: Path) -> dict[str, str]:
    """Bind the accepted census root artifact-by-artifact."""
    validator_driver.require_owned_dir(census_root)
    if census_root.name != EXPECTED_CENSUS_ROOT:
        raise ExperimentError("census root is not the strategy-accepted 007-m census root")
    for name, digest in EXPECTED_CENSUS_SHA.items():
        validator_driver.require_private_file(census_root / name, expected_sha=digest)
    return dict(EXPECTED_CENSUS_SHA)


def verify_c1_population(
    source_root: Path,
    rebuilt: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Require the persisted 007-j C=1 candidates to equal the rebuilt union."""
    persisted = read_json(source_root / "CANDIDATES.json")
    if not isinstance(persisted, list) or len(persisted) != EXPECTED_007J_C1_TOTAL:
        raise ExperimentError("007-j C=1 candidate count mismatch")
    for name, digest in SOURCE_007J_EVIDENCE.items():
        validator_driver.require_private_file(source_root / name, expected_sha=digest)
    ordered = protocol.ordered_candidates(persisted)
    manifest, digest = protocol.candidate_manifest(ordered)
    if digest != EXPECTED_007J_CANDIDATE_MANIFEST:
        raise ExperimentError("007-j C=1 candidate manifest digest mismatch")
    if read_json(source_root / "CANDIDATE-MANIFEST.json") != manifest:
        raise ExperimentError("007-j C=1 persisted manifest mismatch")
    if ordered != rebuilt:
        raise ExperimentError("007-j C=1 candidate identity drift")
    counts = {phase: sum(1 for item in ordered if item["phase"] == phase) for phase in PHASES}
    if counts != EXPECTED_007J_C1_COUNTS:
        raise ExperimentError(f"007-j C=1 phase counts mismatch: {counts}")
    return ordered


def copy_c1_observations(
    source_root: Path,
    scratch: Path,
    c1_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Copy the exact 007-j C=1 observation directories, verified one by one."""
    prior_j.ensure_request_root(scratch)
    case_hashes: dict[tuple[str, int], str] = {}
    records: list[dict[str, Any]] = []
    for item in c1_items:
        candidate_id = protocol.candidate_path_id(item)
        source_dir = source_root / "requests" / candidate_id
        validator_driver.require_owned_dir(source_dir)
        names = {entry.name for entry in source_dir.iterdir()}
        if names != {"request.json", "dispatch.json", "raw-response.json", "observation.json"}:
            raise ExperimentError(f"007-j C=1 request set is invalid: {candidate_id}")
        body = protocol.request_body(
            item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
        )
        request_bytes = canonical_bytes(body)
        request_path = source_dir / "request.json"
        if request_path.read_bytes() != request_bytes:
            raise ExperimentError(f"007-j C=1 request bytes changed: {candidate_id}")
        observation = read_json(source_dir / "observation.json")
        if not isinstance(observation, dict):
            raise ExperimentError(f"007-j C=1 observation is malformed: {candidate_id}")
        if observation.get("request_sha256") != sha256_bytes(request_bytes) or observation.get(
            "response_sha256"
        ) != sha256_file(source_dir / "raw-response.json"):
            raise ExperimentError(f"007-j C=1 observation identity is invalid: {candidate_id}")
        target_key = (item["phase"], item["case_index"])
        if target_key not in case_hashes:
            case_hashes[target_key] = sha256_file(
                source_root / "cases" / item["phase"] / f"{item['case_index']:06d}.json"
            )
        validator_driver.copy_tree_exact(source_dir, scratch / "requests" / candidate_id)
        records.append(
            {
                "candidate_id": candidate_id,
                "stable_key": list(protocol.stable_key(item)),
                "source_case_sha256": case_hashes[target_key],
                "request_sha256": sha256_bytes(request_bytes),
                "raw_response_sha256": sha256_file(source_dir / "raw-response.json"),
                "observation_sha256": sha256_file(source_dir / "observation.json"),
                "source": "007-j immutable request/raw/observation copy",
            }
        )
    if len(records) != EXPECTED_007J_C1_TOTAL:
        raise ExperimentError("007-j C=1 observation copy count mismatch")
    tree = validator_driver.request_tree_identity(scratch / "requests")
    if tree != EXPECTED_007J_REQUEST_TREE:
        raise ExperimentError("copied 007-j C=1 request tree identity changed")
    return records


def live_deployment(
    source_configuration: dict[str, Any],
    profile_path: Path,
    credential_env: str | None,
) -> dict[str, Any]:
    """Freeze the 007-m fresh-call deployment on the strategy-accepted profile."""
    source_deployment = source_configuration.get("deployment")
    if not isinstance(source_deployment, dict):
        raise ExperimentError("007-j deployment identity is unavailable")
    endpoint = source_deployment.get("endpoint")
    frozen_credential = source_deployment.get("credential_env")
    if not isinstance(endpoint, str) or not endpoint:
        raise ExperimentError("frozen endpoint identity is unavailable")
    if not isinstance(frozen_credential, str) or not frozen_credential:
        raise ExperimentError("frozen credential environment identity is unavailable")
    if credential_env is not None and credential_env != frozen_credential:
        raise ExperimentError("credential environment is not the frozen 007-j identity")
    validator_driver.require_owned_file(profile_path)
    actual_sha = sha256_file(profile_path)
    if actual_sha != EXPECTED_007M_PROFILE_SHA256:
        raise ExperimentError(
            "live profile SHA-256 is not the strategy-accepted 007-m fresh-call identity"
        )
    return {
        "class": "A100-FP8",
        "model": protocol.MODEL,
        "endpoint": endpoint,
        "profile_path": str(profile_path),
        "profile_sha256": actual_sha,
        "frozen_007j_profile_sha256": prior_j.EXPECTED_PROFILE,
        "profile_drift": actual_sha != prior_j.EXPECTED_PROFILE,
        "credential_env": frozen_credential,
        "protocol": "Responses non-streaming",
    }


def c_gt_1_reuse_reason(live_profile_sha: str) -> str:
    """C>1 observation reuse is disabled by the strategy drift decision."""
    if live_profile_sha == prior_j.EXPECTED_PROFILE:
        raise ExperimentError(
            "007-m is frozen with the profile-drift decision; a matching frozen "
            "007-j profile is a different experiment configuration"
        )
    return C_GT_1_REUSE_DISABLED


def build_live_candidates(
    dispatch: list[dict[str, Any]],
    population: list[dict[str, Any]],
    *,
    expected_total: int = EXPECTED_C_GT_1_TOTAL,
    expected_counts: Mapping[str, int] = EXPECTED_C_GT_1,
) -> list[dict[str, Any]]:
    """Project dispatch payloads into frozen validator candidate items."""
    by_key = {
        (item["phase"], item["case_index"], item["target_ordinal"]): item for item in population
    }
    items: list[dict[str, Any]] = []
    for payload in dispatch:
        key = (payload["phase"], payload["case_index"], payload["target_ordinal"])
        source = by_key.get(key)
        if source is None:
            raise ExperimentError("dispatch payload does not match a census target")
        if payload["candidate"] != source["candidate"]:
            raise ExperimentError("dispatch candidate identity drifted from the frozen target")
        items.append(
            {
                name: payload[name]
                for name in (
                    "phase",
                    "case_index",
                    "case_id",
                    "target_ordinal",
                    "target_start",
                    "target_end",
                    "candidate",
                    "candidate_form",
                    "operation",
                    "mechanical_edit",
                    "sentence",
                )
            }
        )
    ordered = protocol.ordered_candidates(items)
    if len(ordered) != expected_total:
        raise ExperimentError("live C>1 candidate count mismatch")
    counts = {phase: sum(1 for item in ordered if item["phase"] == phase) for phase in PHASES}
    if counts != dict(expected_counts):
        raise ExperimentError(f"live C>1 phase counts mismatch: {counts}")
    return ordered


def build_live_configuration(
    identity: dict[str, Any],
    source: dict[str, Any],
    request_tree: dict[str, Any],
    census_hashes: dict[str, str],
    source_configuration: dict[str, Any],
    deployment: dict[str, Any],
    analysis: dict[str, Any],
    fresh: list[dict[str, Any]],
    c1_records: list[dict[str, Any]],
    scratch: Path,
    *,
    reuse_records: list[dict[str, Any]] = (),
    adoption: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "run_id": RUN_ID,
        "status": "FROZEN_BEFORE_LIVE_EXECUTION",
        "implementation_head": identity["implementation_head"],
        "implementation_branch": identity["branch"],
        "code_identity": {"head_blobs": identity["head_blobs"]},
        "census_root": {
            "name": EXPECTED_CENSUS_ROOT,
            "superseded_diagnostic_root": SUPERSEDED_CENSUS_ROOT,
            "artifacts_sha256": census_hashes,
        },
        "source_007j_identity": {
            **source,
            "case_identity_manifest_sha256": prior_j.EXPECTED_PRIOR_CASES,
            "c1_candidates_sha256": EXPECTED_007J_CANDIDATES,
            "c1_case_results_sha256": EXPECTED_007J_CASE_RESULTS,
            "c1_reuse_records_sha256": EXPECTED_007J_REUSE_RECORDS,
            "request_tree": request_tree,
            "prior_007i_identity": source_configuration.get("prior_007i_identity"),
        },
        "population": {
            "c1_counts": EXPECTED_007J_C1_COUNTS,
            "c1_total": EXPECTED_007J_C1_TOTAL,
            "c_gt_1_counts": EXPECTED_C_GT_1,
            "c_gt_1_total": EXPECTED_C_GT_1_TOTAL,
            "scheduled_total": EXPECTED_007J_C1_TOTAL + EXPECTED_C_GT_1_TOTAL,
            "entering_targets": analysis["entering_targets"],
            "transition_matrix": analysis["transition_matrix"],
            "c0_counts": analysis["c0_counts"],
            **({
                "c_gt_1_completed_reused": adoption["completed_reused"],
                "c_gt_1_completed_reused_attempted": adoption["completed_reused_attempted"],
                "c_gt_1_completed_reused_uncertain": adoption["completed_reused_uncertain"],
                "c_gt_1_interrupted_carried": adoption["interrupted_carried"],
                "c_gt_1_fresh": adoption["fresh"],
            } if adoption is not None else {}),
        },
        "method": {
            "c0": "exact preserved 007-j behavior; no observation",
            "c1": "exact preserved 007-j observations, copied byte-exact; zero new calls",
            "c_gt_1": (
                "the unique CPU top is the only candidate the frozen validator "
                "sees; USE_CANDIDATE applies only it through unchanged gates; "
                "KEEP_ORIGINAL, UNCERTAIN, protocol or operational failure, and "
                "a tied top keep the original target; no runner-up is tried"
            ),
            "primary_projection": "validated_only over the C=1 and C>1 scheduled targets",
            "rejected_c_gt_1": (
                "original target retained; unrelated accepted edits in the same "
                "case are preserved through exact original coordinates; the old "
                "ordinary-Qwen fallback is never substituted"
            ),
            "paired_evidence": "007-m case results plus 007-j replay case results",
        },
        "deployment": deployment,
        "prompt": {
            "sha256": protocol.FROZEN_PROMPT_SHA256,
            "template": "owner-supplied frozen 007-i validator prompt",
        },
        "request": {
            "fields": prior_j.EXPECTED_REQUEST_FIELDS,
            "stream": False,
            "store": False,
            "include_reasoning": True,
            "reasoning_effort": protocol.EFFORT,
            "serializer": "canonical UTF-8 JSON with one final LF",
        },
        "parser": prior_j.EXPECTED_PARSER,
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
            "new_call_budget": len(fresh),
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
        },
        "reuse": {
            "policy": (
                "exact case/coordinate/sentence/candidate/request/prompt/deployment/"
                "parser/response identity only"
            ),
            "c1_copied_observations": len(c1_records),
            "c_gt_1_reused": len(reuse_records),
            "c_gt_1_fresh": len(fresh),
            "c_gt_1_disabled_reason": C_GT_1_REUSE_DISABLED,
            **({
                "c_gt_1_cross_root_reuse_basis": (
                    "exact request/raw/observation/profile/prompt/parser identity "
                    "from the preserved failed 007-m root under the strategy-"
                    "accepted 007-m fresh-call profile"
                ),
                "c_gt_1_interrupted_carried": adoption["interrupted_carried"],
            } if adoption is not None else {}),
        },
        "privacy": {
            "public": "no public artifact is published by increment 2",
            "private": (
                "sentences, targets, candidates, gold, prompts, responses, "
                "endpoint/profile and credentials remain in the private native root"
            ),
        },
        "no_resampling": True,
        "private_evidence_root": str(scratch),
        **({"adoption": adoption} if adoption is not None else {}),
    }


def persist_live_preparation(
    scratch: Path,
    configuration: dict[str, Any],
    source_record: dict[str, Any],
    index_schema_value: dict[str, Any],
    c1_records: list[dict[str, Any]],
    fresh: list[dict[str, Any]],
    census_records: list[dict[str, Any]],
    dispatch_envelope: dict[str, Any],
    *,
    reuse_records: list[dict[str, Any]] = (),
    carry_records: list[dict[str, Any]] = (),
    linkage: dict[str, Any] | None = None,
    adopted_items: list[dict[str, Any]] = (),
) -> str:
    validator_driver.immutable_json(scratch / "SOURCE.json", source_record)
    if (
        sha256_bytes(canonical_bytes(index_schema_value))
        != EXPECTED_CENSUS_SHA["INDEX-SCHEMA.json"]
    ):
        raise ExperimentError("re-derived index schema is not byte-identical to the census root")
    validator_driver.immutable_json(scratch / "INDEX-SCHEMA.json", index_schema_value)
    if sha256_bytes(canonical_bytes(census_records)) != EXPECTED_CENSUS_SHA["RANK-POPULATION.json"]:
        raise ExperimentError(
            "re-derived census population is not byte-identical to the census root"
        )
    validator_driver.immutable_json(scratch / "RANK-POPULATION.json", census_records)
    if (
        sha256_bytes(canonical_bytes(dispatch_envelope))
        != EXPECTED_CENSUS_SHA["DISPATCH-MANIFEST.json"]
    ):
        raise ExperimentError(
            "re-derived dispatch manifest is not byte-identical to the census root"
        )
    validator_driver.immutable_json(scratch / "DISPATCH-MANIFEST.json", dispatch_envelope)
    validator_driver.immutable_json(scratch / "C1-OBSERVATION-RECORDS.json", c1_records)
    manifest, _digest = protocol.candidate_manifest(fresh)
    validator_driver.immutable_json(scratch / "CANDIDATES.json", fresh)
    validator_driver.immutable_json(scratch / "CANDIDATE-MANIFEST.json", manifest)
    validator_driver.immutable_json(scratch / "FRESH-CALL-MANIFEST.json", fresh)
    validator_driver.immutable_json(scratch / "REUSE-RECORDS.json", list(reuse_records))
    adoption_config = configuration.get("adoption")
    if carry_records:
        if not isinstance(adoption_config, dict) or (
            sha256_bytes(canonical_bytes(carry_records))
            != adoption_config["carry_records_sha256"]
        ):
            raise ExperimentError("carry records drift from the frozen configuration")
        validator_driver.immutable_json(scratch / "CARRY-RECORDS.json", carry_records)
    if linkage is not None:
        if not isinstance(adoption_config, dict) or (
            sha256_bytes(canonical_bytes(linkage)) != adoption_config["linkage_sha256"]
        ):
            raise ExperimentError("failed-root linkage drifts from the frozen configuration")
        validator_driver.immutable_json(scratch / "FAILED-ROOT-LINKAGE.json", linkage)
    if isinstance(adoption_config, dict) and sha256_bytes(canonical_bytes(reuse_records)) != (
        adoption_config["reuse_records_sha256"]
    ):
        raise ExperimentError("reuse records drift from the frozen configuration")
    if adopted_items:
        adopted_manifest, _adopted_digest = protocol.candidate_manifest(adopted_items)
        if not isinstance(adoption_config, dict) or (
            sha256_bytes(canonical_bytes(adopted_items))
            != adoption_config["adopted_candidates_sha256"]
            or sha256_bytes(canonical_bytes(adopted_manifest))
            != adoption_config["adopted_candidate_manifest_sha256"]
        ):
            raise ExperimentError("adopted candidates drift from the frozen configuration")
        validator_driver.immutable_json(scratch / "ADOPTED-CANDIDATES.json", adopted_items)
        validator_driver.immutable_json(
            scratch / "ADOPTED-CANDIDATE-MANIFEST.json", adopted_manifest
        )
    return validator_driver.immutable_json(scratch / "CONFIGURATION.json", configuration)


def _load_prepared_lists(
    scratch: Path,
    *,
    expected_fresh_total: int,
    expected_reuse_total: int,
    expected_carry_total: int,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any] | None,
]:
    c1_items = protocol.ordered_candidates(read_json(scratch / "SOURCE-007J-CANDIDATES.json"))
    if len(c1_items) != EXPECTED_007J_C1_TOTAL:
        raise ExperimentError("prepared 007-j C=1 candidate count mismatch")
    fresh = read_json(scratch / "CANDIDATES.json")
    manifest = read_json(scratch / "CANDIDATE-MANIFEST.json")
    fresh_manifest = read_json(scratch / "FRESH-CALL-MANIFEST.json")
    reuse_records = read_json(scratch / "REUSE-RECORDS.json")
    c1_records = read_json(scratch / "C1-OBSERVATION-RECORDS.json")
    if not all(
        isinstance(value, list)
        for value in (fresh, manifest, fresh_manifest, reuse_records, c1_records, c1_items)
    ):
        raise ExperimentError("prepared private artifacts are malformed")
    recomputed, _digest = protocol.candidate_manifest(fresh)
    if recomputed != manifest or fresh_manifest != fresh:
        raise ExperimentError("prepared fresh manifest or reuse identity mismatch")
    if len(fresh) != expected_fresh_total:
        raise ExperimentError("prepared fresh candidate count mismatch")
    if len(reuse_records) != expected_reuse_total:
        raise ExperimentError("prepared reuse record count mismatch")
    adopted_bundle = None
    if expected_reuse_total or expected_carry_total:
        adopted_items = read_json(scratch / "ADOPTED-CANDIDATES.json")
        adopted_manifest = read_json(scratch / "ADOPTED-CANDIDATE-MANIFEST.json")
        carry_records = read_json(scratch / "CARRY-RECORDS.json")
        linkage = read_json(scratch / "FAILED-ROOT-LINKAGE.json")
        if not all(
            isinstance(value, list)
            for value in (adopted_items, adopted_manifest, carry_records)
        ) or not isinstance(linkage, dict):
            raise ExperimentError("prepared adoption artifacts are malformed")
        recomputed_adopted, _digest = protocol.candidate_manifest(adopted_items)
        if recomputed_adopted != adopted_manifest:
            raise ExperimentError("prepared adopted candidate manifest mismatch")
        if len(adopted_items) != expected_reuse_total + expected_carry_total:
            raise ExperimentError("prepared adopted candidate count mismatch")
        if len(carry_records) != expected_carry_total:
            raise ExperimentError("prepared carry record count mismatch")
        if (
            {record["candidate_id"] for record in carry_records}
            | {record["candidate_id"] for record in reuse_records}
            != {protocol.candidate_path_id(item) for item in adopted_items}
        ):
            raise ExperimentError(
                "prepared adoption records do not cover the adopted candidates"
            )
        adopted_bundle = {
            "items": adopted_items,
            "reuse_records": reuse_records,
            "carry_records": carry_records,
            "linkage": linkage,
        }
    return c1_items, fresh, c1_records, adopted_bundle


def verify_c1_observations(
    scratch: Path,
    c1_items: list[dict[str, Any]],
    c1_records: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Re-verify every copied 007-j C=1 observation from the private root."""
    by_id = {record["candidate_id"]: record for record in c1_records}
    observations: dict[str, dict[str, Any]] = {}
    for item in c1_items:
        candidate_id = protocol.candidate_path_id(item)
        record = by_id.get(candidate_id)
        if record is None:
            raise ExperimentError(f"missing C=1 observation record: {candidate_id}")
        directory = scratch / "requests" / candidate_id
        validator_driver.require_owned_dir(directory)
        names = {entry.name for entry in directory.iterdir()}
        if names != {"request.json", "dispatch.json", "raw-response.json", "observation.json"}:
            raise ExperimentError(f"C=1 request set is invalid: {candidate_id}")
        body = protocol.request_body(
            item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
        )
        request_bytes = canonical_bytes(body)
        if (directory / "request.json").read_bytes() != request_bytes:
            raise ExperimentError(f"C=1 request bytes changed: {candidate_id}")
        observation = read_json(directory / "observation.json")
        if (
            observation.get("dispatch") != "ATTEMPTED"
            or observation.get("request_sha256") != sha256_bytes(request_bytes)
            or observation.get("response_sha256") != sha256_file(directory / "raw-response.json")
            or sha256_file(directory / "observation.json") != record["observation_sha256"]
        ):
            raise ExperimentError(f"C=1 observation identity is invalid: {candidate_id}")
        observations[candidate_id] = observation
    if len(observations) != EXPECTED_007J_C1_TOTAL:
        raise ExperimentError("C=1 observation count mismatch")
    return observations


def load_prepared_live(
    scratch: Path,
    repo_root: Path,
    expected_head: str,
    source_root: Path,
    census_root: Path,
) -> dict[str, Any]:
    validator_driver.require_private_file(scratch / "CONFIGURATION.json")
    configuration = read_json(scratch / "CONFIGURATION.json")
    configuration_sha = sha256_file(scratch / "CONFIGURATION.json")
    if not isinstance(configuration, dict) or configuration.get("status") != (
        "FROZEN_BEFORE_LIVE_EXECUTION"
    ):
        raise ExperimentError("prepared live configuration status mismatch")
    status = read_json(scratch / "RUN-STATUS.json")
    if status.get("configuration_sha256") != configuration_sha:
        raise ExperimentError("prepared live configuration hash mismatch")
    identity = verify_live_implementation_identity(repo_root, expected_head)
    if identity["implementation_head"] != configuration.get("implementation_head"):
        raise ExperimentError("prepared live implementation head mismatch")
    verify_source_root(source_root)
    if (
        verify_007j_request_tree(source_root)
        != configuration["source_007j_identity"]["request_tree"]
    ):
        raise ExperimentError("007-j request tree identity changed on resume")
    if verify_census_root(census_root) != configuration["census_root"]["artifacts_sha256"]:
        raise ExperimentError("census root identity changed on resume")
    if (
        sha256_file(scratch / "RANK-POPULATION.json")
        != configuration["census_root"]["artifacts_sha256"]["RANK-POPULATION.json"]
    ):
        raise ExperimentError("prepared census population hash mismatch")
    if (
        sha256_file(scratch / "DISPATCH-MANIFEST.json")
        != configuration["census_root"]["artifacts_sha256"]["DISPATCH-MANIFEST.json"]
    ):
        raise ExperimentError("prepared dispatch manifest hash mismatch")
    for name, digest in SOURCE_007J_EVIDENCE.items():
        validator_driver.require_private_file(scratch / f"SOURCE-007J-{name}", expected_sha=digest)
    adoption = configuration.get("adoption")
    if isinstance(adoption, dict):
        expected_fresh_total = adoption["fresh"]
        expected_reuse_total = adoption["completed_reused"]
        expected_carry_total = adoption["interrupted_carried"]
    else:
        expected_fresh_total = EXPECTED_C_GT_1_TOTAL
        expected_reuse_total = 0
        expected_carry_total = 0
    c1_items, fresh, c1_records, adopted_bundle = _load_prepared_lists(
        scratch,
        expected_fresh_total=expected_fresh_total,
        expected_reuse_total=expected_reuse_total,
        expected_carry_total=expected_carry_total,
    )
    pairs, _baseline, uv_indices, records, case_digest = validator_driver.load_frozen_state(scratch)
    if case_digest != prior_j.EXPECTED_PRIOR_CASES:
        raise ExperimentError("staged frozen case identity mismatch on resume")
    c1_observations = verify_c1_observations(scratch, c1_items, c1_records)
    prepared: dict[str, Any] = {
        "configuration": configuration,
        "configuration_sha256": configuration_sha,
        "c1_items": c1_items,
        "c1_observations": c1_observations,
        "c1_records": c1_records,
        "fresh": fresh,
        "c_gt_1_all": list(fresh),
        "pairs": pairs,
        "records": records,
        "uv_indices": uv_indices,
        "source_root": str(source_root),
    }
    if adopted_bundle is None:
        return prepared
    if not isinstance(adoption, dict):
        raise ExperimentError("prepared adoption bundle lacks its configuration block")
    adopted_items = adopted_bundle["items"]
    if (
        sha256_bytes(canonical_bytes(adopted_bundle["linkage"]))
        != adoption["linkage_sha256"]
        or sha256_bytes(canonical_bytes(adopted_bundle["carry_records"]))
        != adoption["carry_records_sha256"]
        or sha256_bytes(canonical_bytes(adopted_bundle["reuse_records"]))
        != adoption["reuse_records_sha256"]
        or sha256_file(scratch / "ADOPTED-CANDIDATES.json")
        != adoption["adopted_candidates_sha256"]
        or sha256_file(scratch / "ADOPTED-CANDIDATE-MANIFEST.json")
        != adoption["adopted_candidate_manifest_sha256"]
    ):
        raise ExperimentError("prepared adoption artifact identity drifted")
    verify_c_gt_1_observations(scratch, adopted_items)
    prepared["c_gt_1_all"] = protocol.ordered_candidates([*fresh, *adopted_items])
    prepared["adopted_items"] = adopted_items
    prepared["reuse_records"] = adopted_bundle["reuse_records"]
    prepared["carry_records"] = adopted_bundle["carry_records"]
    return prepared


def prepare_live(
    repo_root: Path,
    scratch: Path,
    source_root: Path,
    census_root: Path,
    expected_head: str,
    profile_path: Path,
    credential_env: str | None,
) -> dict[str, Any]:
    ensure_scratch(scratch)
    identity = verify_live_implementation_identity(repo_root, expected_head)
    source = verify_source_root(source_root)
    request_tree = verify_007j_request_tree(source_root)
    census_hashes = verify_census_root(census_root)
    validator_driver.stage_frozen_inputs(source_root, scratch)
    pairs, _baseline, uv_indices, records, case_digest = validator_driver.load_frozen_state(scratch)
    if case_digest != prior_j.EXPECTED_PRIOR_CASES:
        raise ExperimentError("staged frozen case identity mismatch")
    index_path = scratch / "inputs" / "index" / "index.sqlite"
    vocabulary, _buckets, _vocabulary_seconds, _vocabulary_rows = baseline_driver.load_vocabulary(
        index_path
    )
    index = IndexQueries(index_path)
    try:
        schema = verify_index_schema(index)
        deletion_index = distance_one.build_deletion_signature_index(vocabulary)
        _c1_digest, c1_rebuilt = verify_007j_c1_identity(records, vocabulary, deletion_index)
        c1_items = verify_c1_population(source_root, c1_rebuilt)
        population, analysis = build_c_gt_1_population(records, vocabulary, deletion_index)
        census = census_population(population, index, vocabulary, uv_indices)
    finally:
        index.close()
    census_records = census["records"]
    dispatch_envelope = {
        "policy": DISPATCH_POLICY,
        "count": len(census["dispatch"]),
        "payloads": census["dispatch"],
    }
    source_configuration = read_json(source_root / "CONFIGURATION.json")
    deployment = live_deployment(source_configuration, profile_path, credential_env)
    c_gt_1_reuse_reason(deployment["profile_sha256"])
    c1_records = copy_c1_observations(source_root, scratch, c1_items)
    fresh = build_live_candidates(census["dispatch"], population)
    if {protocol.candidate_path_id(item) for item in fresh} & {
        protocol.candidate_path_id(item) for item in c1_items
    }:
        raise ExperimentError("C=1 and C>1 candidate path identities collide")
    configuration = build_live_configuration(
        identity,
        source,
        request_tree,
        census_hashes,
        source_configuration,
        deployment,
        analysis,
        fresh,
        c1_records,
        scratch,
    )
    source_record = {
        **identity,
        **source,
        "census_root": str(census_root),
        "census_artifacts_sha256": census_hashes,
        "request_tree": request_tree,
    }
    index_schema_value = {
        "index_sha256": sha256_file(index_path),
        "index_size": index_path.stat().st_size,
        **schema,
    }
    configuration_sha = persist_live_preparation(
        scratch,
        configuration,
        source_record,
        index_schema_value,
        c1_records,
        fresh,
        census_records,
        dispatch_envelope,
    )
    for name, digest in SOURCE_007J_EVIDENCE.items():
        validator_driver.copy_file_exact(source_root / name, scratch / f"SOURCE-007J-{name}")
        validator_driver.require_private_file(scratch / f"SOURCE-007J-{name}", expected_sha=digest)
    validator_driver.mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "run_id": RUN_ID,
            "implementation_head": identity["implementation_head"],
            "configuration_sha256": configuration_sha,
            "census_root": EXPECTED_CENSUS_ROOT,
            "c1_copied_observations": EXPECTED_007J_C1_TOTAL,
            "c_gt_1_reused_observations": 0,
            "scheduled_new_calls": len(fresh),
            "dispatched_http_requests": 0,
        },
    )
    c1_observations = verify_c1_observations(scratch, c1_items, c1_records)
    return {
        "configuration": configuration,
        "configuration_sha256": configuration_sha,
        "c1_items": c1_items,
        "c1_observations": c1_observations,
        "c1_records": c1_records,
        "fresh": fresh,
        "c_gt_1_all": list(fresh),
        "pairs": pairs,
        "records": records,
        "uv_indices": uv_indices,
        "source_root": str(source_root),
    }


def prepare_adopted_live(
    repo_root: Path,
    scratch: Path,
    source_root: Path,
    census_root: Path,
    failed_root: Path,
    expected_head: str,
    profile_path: Path,
    credential_env: str | None,
) -> dict[str, Any]:
    """Freeze a new 007-m root that adopts the preserved failed root ffdf13.

    The 1035 C=1 observations are copied from the frozen 007-j source root as
    before; the 196 completed C>1 observations are copied from the failed root
    under exact request/raw/observation/profile/prompt/parser identity; the 8
    request+dispatch interruptions are carried to conservative uncertain
    observations without any call; only the remaining 678 requests are
    scheduled fresh.  The failed root is never modified or resampled.
    """
    ensure_scratch(scratch)
    identity = verify_live_implementation_identity(repo_root, expected_head)
    source = verify_source_root(source_root)
    request_tree = verify_007j_request_tree(source_root)
    census_hashes = verify_census_root(census_root)
    validator_driver.stage_frozen_inputs(source_root, scratch)
    pairs, _baseline, uv_indices, records, case_digest = validator_driver.load_frozen_state(scratch)
    if case_digest != prior_j.EXPECTED_PRIOR_CASES:
        raise ExperimentError("staged frozen case identity mismatch")
    index_path = scratch / "inputs" / "index" / "index.sqlite"
    vocabulary, _buckets, _vocabulary_seconds, _vocabulary_rows = baseline_driver.load_vocabulary(
        index_path
    )
    index = IndexQueries(index_path)
    try:
        schema = verify_index_schema(index)
        deletion_index = distance_one.build_deletion_signature_index(vocabulary)
        _c1_digest, c1_rebuilt = verify_007j_c1_identity(records, vocabulary, deletion_index)
        c1_items = verify_c1_population(source_root, c1_rebuilt)
        population, analysis = build_c_gt_1_population(records, vocabulary, deletion_index)
        census = census_population(population, index, vocabulary, uv_indices)
    finally:
        index.close()
    census_records = census["records"]
    dispatch_envelope = {
        "policy": DISPATCH_POLICY,
        "count": len(census["dispatch"]),
        "payloads": census["dispatch"],
    }
    all_c_gt_1 = build_live_candidates(census["dispatch"], population)
    spec = failed_root_spec(failed_root.name)
    failed = verify_failed_root(failed_root, scratch, all_c_gt_1, spec)
    failed_configuration = read_json(failed_root / "CONFIGURATION.json")
    source_configuration = read_json(source_root / "CONFIGURATION.json")
    deployment = live_deployment(source_configuration, profile_path, credential_env)
    c_gt_1_reuse_reason(deployment["profile_sha256"])
    c1_records = copy_c1_observations(source_root, scratch, c1_items)
    identity_basis = _reuse_identity_basis(failed_configuration)
    reuse_records = adopt_completed_c_gt_1(
        failed_root,
        scratch,
        all_c_gt_1,
        failed["states"],
        identity_basis,
        expected_total=spec["completed_attempted"] + spec["completed_uncertain"],
    )
    carry_records = carry_interrupted_c_gt_1(
        failed_root, scratch, all_c_gt_1, failed["states"], expected_total=spec["request_only"]
    )
    adopted_ids = (
        {record["candidate_id"] for record in reuse_records}
        | {record["candidate_id"] for record in carry_records}
    )
    fresh = [item for item in all_c_gt_1 if protocol.candidate_path_id(item) not in adopted_ids]
    if {protocol.candidate_path_id(item) for item in fresh} & {
        protocol.candidate_path_id(item) for item in c1_items
    }:
        raise ExperimentError("C=1 and C>1 candidate path identities collide")
    if len(fresh) != spec["missing"]:
        raise ExperimentError("adopted fresh call count mismatch")
    fresh_counts = {phase: sum(1 for item in fresh if item["phase"] == phase) for phase in PHASES}
    if fresh_counts != dict(spec["fresh_counts"]):
        raise ExperimentError(f"adopted fresh phase counts mismatch: {fresh_counts}")
    adopted_items = [item for item in all_c_gt_1 if protocol.candidate_path_id(item) in adopted_ids]
    adopted_manifest, _adopted_digest = protocol.candidate_manifest(adopted_items)
    linkage = {
        "schema_version": 1,
        "failed_root": failed["failed_root"],
        "failed_root_path": failed["failed_root_path"],
        "configuration_sha256": failed["configuration_sha256"],
        "run_status_sha256": failed["run_status_sha256"],
        "implementation_head": failed["implementation_head"],
        "request_tree": failed["request_tree"],
        "state_census": failed["state_census"],
        "defect": failed["defect"],
        "preserved_unchanged": True,
        "resampled": False,
        "harness_revision_head": identity["implementation_head"],
        "adoption": {
            "c_gt_1_completed_reused": len(reuse_records),
            "c_gt_1_completed_reused_attempted": spec["completed_attempted"],
            "c_gt_1_completed_reused_uncertain": spec["completed_uncertain"],
            "c_gt_1_interrupted_carried": len(carry_records),
            "c_gt_1_fresh": len(fresh),
        },
    }
    adoption = {
        "failed_root": failed["failed_root"],
        "failed_root_path": failed["failed_root_path"],
        "failed_root_configuration_sha256": failed["configuration_sha256"],
        "failed_root_run_status_sha256": failed["run_status_sha256"],
        "failed_root_implementation_head": failed["implementation_head"],
        "failed_root_request_tree": failed["request_tree"],
        "failed_root_state_census": failed["state_census"],
        "failed_root_defect": failed["defect"],
        "harness_revision_head": identity["implementation_head"],
        "completed_reused": len(reuse_records),
        "completed_reused_attempted": spec["completed_attempted"],
        "completed_reused_uncertain": spec["completed_uncertain"],
        "interrupted_carried": len(carry_records),
        "fresh": len(fresh),
        "linkage_artifact": "FAILED-ROOT-LINKAGE.json",
        "linkage_sha256": sha256_bytes(canonical_bytes(linkage)),
        "reuse_records_sha256": sha256_bytes(canonical_bytes(reuse_records)),
        "carry_records_sha256": sha256_bytes(canonical_bytes(carry_records)),
        "adopted_candidates_sha256": sha256_bytes(canonical_bytes(adopted_items)),
        "adopted_candidate_manifest_sha256": sha256_bytes(canonical_bytes(adopted_manifest)),
    }
    configuration = build_live_configuration(
        identity,
        source,
        request_tree,
        census_hashes,
        source_configuration,
        deployment,
        analysis,
        fresh,
        c1_records,
        scratch,
        reuse_records=reuse_records,
        adoption=adoption,
    )
    source_record = {
        **identity,
        **source,
        "census_root": str(census_root),
        "census_artifacts_sha256": census_hashes,
        "request_tree": request_tree,
        "failed_root": failed["failed_root_path"],
    }
    index_schema_value = {
        "index_sha256": sha256_file(index_path),
        "index_size": index_path.stat().st_size,
        **schema,
    }
    configuration_sha = persist_live_preparation(
        scratch,
        configuration,
        source_record,
        index_schema_value,
        c1_records,
        fresh,
        census_records,
        dispatch_envelope,
        reuse_records=reuse_records,
        carry_records=carry_records,
        linkage=linkage,
        adopted_items=adopted_items,
    )
    for name, digest in SOURCE_007J_EVIDENCE.items():
        validator_driver.copy_file_exact(source_root / name, scratch / f"SOURCE-007J-{name}")
        validator_driver.require_private_file(scratch / f"SOURCE-007J-{name}", expected_sha=digest)
    validator_driver.mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "run_id": RUN_ID,
            "implementation_head": identity["implementation_head"],
            "configuration_sha256": configuration_sha,
            "census_root": EXPECTED_CENSUS_ROOT,
            "failed_root": EXPECTED_FAILED_ROOT,
            "c1_copied_observations": EXPECTED_007J_C1_TOTAL,
            "c_gt_1_reused_observations": len(reuse_records),
            "c_gt_1_interrupted_carried": len(carry_records),
            "c_gt_1_fresh_observations": len(fresh),
            "scheduled_new_calls": len(fresh),
            "dispatched_http_requests": 0,
        },
    )
    c1_observations = verify_c1_observations(scratch, c1_items, c1_records)
    verify_c_gt_1_observations(scratch, adopted_items)
    return {
        "configuration": configuration,
        "configuration_sha256": configuration_sha,
        "c1_items": c1_items,
        "c1_observations": c1_observations,
        "c1_records": c1_records,
        "fresh": fresh,
        "c_gt_1_all": all_c_gt_1,
        "adopted_items": adopted_items,
        "reuse_records": reuse_records,
        "carry_records": carry_records,
        "pairs": pairs,
        "records": records,
        "uv_indices": uv_indices,
        "source_root": str(source_root),
    }


def execute_fresh_007m(
    scratch: Path,
    fresh: list[dict[str, Any]],
    endpoint: str,
    credential_env: str,
    *,
    transport: protocol.ResponseTransport | None = None,
) -> dict[int, dict[str, Any]]:
    if transport is None and not os.environ.get(credential_env):
        raise ExperimentError("LIVE_CREDENTIAL_MISSING")
    prior_j.ensure_request_root(scratch)
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

    with ThreadPoolExecutor(max_workers=protocol.WORKERS, thread_name_prefix="oap-007-m") as pool:
        futures = [pool.submit(worker, worker_id) for worker_id in range(protocol.WORKERS)]
        for future in futures:
            worker_id, status = future.result()
            statuses[worker_id] = status
    if sum(value["completed"] for value in statuses.values()) != len(fresh):
        raise ExperimentError("fresh observation set is incomplete")
    worker_result = scratch / "WORKER-RESULT.json"
    if worker_result.exists() or worker_result.is_symlink():
        validator_driver.require_private_file(worker_result)
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
        validator_driver.immutable_json(worker_result, statuses)
    validator_driver.mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "VALIDATOR_OBSERVATIONS_COMPLETE",
            "run_id": RUN_ID,
            "scheduled_new_calls": len(fresh),
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
    return statuses


C_GT_1_STATE_ATTEMPTED = "ATTEMPTED"
C_GT_1_STATE_INTERRUPTED_4FILE = "INTERRUPTED_4FILE"
C_GT_1_STATE_INTERRUPTED_3FILE = "INTERRUPTED_3FILE"
C_GT_1_STATE_REQUEST_ONLY = "REQUEST_ONLY"


def _c_gt_1_directory_state(
    directory: Path,
    request_bytes: bytes,
) -> tuple[str, dict[str, Any]]:
    """Classify one C>1 request directory under the frozen persistence contract.

    ATTEMPTED: full completed cycle (dispatch marker plus ATTEMPTED
    raw/observation, including explicit protocol/operational failures).
    INTERRUPTED_4FILE: the request reached the dispatch marker and the process
    died before persisting the raw response; the frozen finalizer closed it as
    raw/observation UNKNOWN without a new call.  The stale ATTEMPTED marker
    remains and the state stays distinguishable from a completed ATTEMPTED
    observation.
    INTERRUPTED_3FILE: the same finalization with no dispatch marker present.
    REQUEST_ONLY: the pre-finalization crash state (request plus dispatch
    marker, no raw response); only the failed-root census may observe it.
    """
    names = {entry.name for entry in directory.iterdir()}
    request_sha = sha256_bytes(request_bytes)
    if names == {"request.json", "dispatch.json", "raw-response.json", "observation.json"}:
        for name in sorted(names):
            validator_driver.require_private_file(directory / name)
        dispatch = read_json(directory / "dispatch.json")
        raw = read_json(directory / "raw-response.json")
        observation = read_json(directory / "observation.json")
        if (
            dispatch != {"dispatch": "ATTEMPTED"}
            or (directory / "request.json").read_bytes() != request_bytes
            or observation.get("request_sha256") != request_sha
            or observation.get("response_sha256")
            != sha256_file(directory / "raw-response.json")
        ):
            raise ExperimentError(
                f"persisted C>1 observation identity is invalid: {directory.name}"
            )
        if raw.get("dispatch") == "ATTEMPTED" and observation.get("dispatch") == "ATTEMPTED":
            return C_GT_1_STATE_ATTEMPTED, observation
        if (
            raw.get("dispatch") == "UNKNOWN"
            and raw.get("failure") == "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE"
            and observation.get("dispatch") == "UNKNOWN"
            and observation.get("failure") == "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE"
        ):
            return C_GT_1_STATE_INTERRUPTED_4FILE, observation
        raise ExperimentError(
            f"persisted C>1 observation identity is invalid: {directory.name}"
        )
    if names == {"request.json", "raw-response.json", "observation.json"}:
        for name in sorted(names):
            validator_driver.require_private_file(directory / name)
        raw = read_json(directory / "raw-response.json")
        observation = read_json(directory / "observation.json")
        if (
            (directory / "request.json").read_bytes() != request_bytes
            or raw.get("dispatch") != "UNKNOWN"
            or raw.get("failure") != "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE"
            or observation.get("dispatch") != "UNKNOWN"
            or observation.get("failure") != "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE"
            or observation.get("request_sha256") != request_sha
            or observation.get("response_sha256")
            != sha256_file(directory / "raw-response.json")
        ):
            raise ExperimentError(
                f"persisted C>1 interruption identity is invalid: {directory.name}"
            )
        return C_GT_1_STATE_INTERRUPTED_3FILE, observation
    if names == {"request.json", "dispatch.json"}:
        validator_driver.require_private_file(directory / "request.json")
        validator_driver.require_private_file(directory / "dispatch.json")
        if (
            (directory / "request.json").read_bytes() != request_bytes
            or read_json(directory / "dispatch.json") != {"dispatch": "ATTEMPTED"}
        ):
            raise ExperimentError(
                f"persisted C>1 request-only identity is invalid: {directory.name}"
            )
        return C_GT_1_STATE_REQUEST_ONLY, {}
    raise ExperimentError(f"persisted C>1 request set is invalid: {directory.name}")


def verify_c_gt_1_observations(
    scratch: Path, fresh: list[dict[str, Any]]
) -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
    """Verify every persisted C>1 observation or uncertain-delivery request.

    Completed ATTEMPTED observations count as dispatched; the canonical
    interrupted finalization (with or without the stale dispatch marker)
    counts as an uncertain delivery that is never resampled.
    """
    observations: dict[str, dict[str, Any]] = {}
    dispatched = 0
    uncertain = 0
    failures = 0
    for item in fresh:
        candidate_id = protocol.candidate_path_id(item)
        directory = scratch / "requests" / candidate_id
        validator_driver.require_owned_dir(directory)
        body = protocol.request_body(
            item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
        )
        request_bytes = canonical_bytes(body)
        state, observation = _c_gt_1_directory_state(directory, request_bytes)
        if state == C_GT_1_STATE_ATTEMPTED:
            dispatched += 1
        elif state in (C_GT_1_STATE_INTERRUPTED_4FILE, C_GT_1_STATE_INTERRUPTED_3FILE):
            uncertain += 1
        else:
            raise ExperimentError(f"persisted C>1 request set is invalid: {candidate_id}")
        failures += int(bool(observation.get("operational_failure")))
        observations[candidate_id] = observation
    if len(observations) != len(fresh):
        raise ExperimentError("fresh observation count mismatch")
    return observations, {
        "dispatched": dispatched,
        "uncertain": uncertain,
        "operational_failures": failures,
    }


def failed_root_spec(name: str) -> dict[str, Any]:
    """Bind one preserved failed-instrument root to its adoption contract."""
    if name == EXPECTED_FAILED_ROOT:
        return {
            "name": name,
            "configuration_sha256": EXPECTED_FAILED_ROOT_CONFIGURATION,
            "implementation_head": EXPECTED_FAILED_ROOT_HEAD,
            "run_status_sha256": EXPECTED_FAILED_ROOT_RUN_STATUS,
            "run_status_status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "request_tree": dict(EXPECTED_FAILED_ROOT_REQUEST_TREE),
            "completed_attempted": EXPECTED_ADOPTED_COMPLETED_ATTEMPTED,
            "completed_uncertain": EXPECTED_ADOPTED_COMPLETED_UNCERTAIN,
            "request_only": EXPECTED_ADOPTED_REQUEST_ONLY,
            "missing": EXPECTED_ADOPTED_FRESH,
            "fresh_counts": dict(EXPECTED_ADOPTED_FRESH_COUNTS),
            "defect": (
                "88ca4dfe verify_c_gt_1_observations rejected the canonical "
                "interrupted-finalization file set (request + dispatch marker + "
                "raw/observation UNKNOWN), so the root cannot complete its own "
                "live resume; preserved unchanged as failed-instrument evidence"
            ),
        }
    if name == EXPECTED_SECOND_FAILED_ROOT:
        return {
            "name": name,
            "configuration_sha256": EXPECTED_SECOND_FAILED_ROOT_CONFIGURATION,
            "implementation_head": EXPECTED_SECOND_FAILED_ROOT_HEAD,
            "run_status_sha256": EXPECTED_SECOND_FAILED_ROOT_RUN_STATUS,
            "run_status_status": "VALIDATOR_OBSERVATIONS_COMPLETE",
            "request_tree": dict(EXPECTED_SECOND_FAILED_ROOT_REQUEST_TREE),
            "completed_attempted": EXPECTED_SECOND_ADOPTED_COMPLETED_ATTEMPTED,
            "completed_uncertain": EXPECTED_SECOND_ADOPTED_COMPLETED_UNCERTAIN,
            "request_only": EXPECTED_SECOND_ADOPTED_REQUEST_ONLY,
            "missing": EXPECTED_SECOND_ADOPTED_FRESH,
            "fresh_counts": dict(EXPECTED_SECOND_ADOPTED_FRESH_COUNTS),
            "defect": (
                "92bee3a complete_live_result 007-j replay identity gate "
                "compared in-memory tuple-typed attribution fields against the "
                "JSON-normalized persisted rows, so the fully observed root "
                "could not aggregate; preserved unchanged as failed-instrument "
                "evidence"
            ),
        }
    raise ExperimentError("failed root is not a preserved 007-m evidence root")


def verify_failed_root(
    failed_root: Path,
    scratch: Path,
    c_gt_1_items: list[dict[str, Any]],
    spec: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Bind the preserved failed-instrument root identity and census its states."""
    validator_driver.require_owned_dir(failed_root)
    if spec is None:
        spec = failed_root_spec(failed_root.name)
    if failed_root.name != spec["name"]:
        raise ExperimentError("failed root does not match its adoption spec")
    if failed_root.absolute() == scratch.absolute():
        raise ExperimentError("failed root and adoption scratch are the same root")
    validator_driver.require_private_file(
        failed_root / "CONFIGURATION.json", expected_sha=spec["configuration_sha256"]
    )
    configuration = read_json(failed_root / "CONFIGURATION.json")
    deployment = configuration.get("deployment") if isinstance(configuration, dict) else None
    prompt = configuration.get("prompt") if isinstance(configuration, dict) else None
    if not all(
        (
            isinstance(configuration, dict),
            configuration.get("run_id") == "007-m",
            configuration.get("status") == "FROZEN_BEFORE_LIVE_EXECUTION",
            configuration.get("implementation_head") == spec["implementation_head"],
            isinstance(deployment, dict),
            deployment.get("profile_sha256") == EXPECTED_007M_PROFILE_SHA256,
            deployment.get("model") == protocol.MODEL,
            deployment.get("credential_env") == "OAP_007_J_QWEN_BEARER",
            isinstance(prompt, dict),
            prompt.get("sha256") == protocol.FROZEN_PROMPT_SHA256,
            configuration.get("parser") == prior_j.EXPECTED_PARSER,
        )
    ):
        raise ExperimentError("failed root configuration identity drifted")
    validator_driver.require_private_file(
        failed_root / "RUN-STATUS.json", expected_sha=spec["run_status_sha256"]
    )
    status = read_json(failed_root / "RUN-STATUS.json")
    if status.get("status") != spec["run_status_status"]:
        raise ExperimentError("failed root run status is not the frozen identity")
    request_tree = validator_driver.request_tree_identity(failed_root / "requests")
    if request_tree != spec["request_tree"]:
        raise ExperimentError("failed root request tree identity changed")
    states: dict[str, str] = {}
    for item in c_gt_1_items:
        candidate_id = protocol.candidate_path_id(item)
        directory = failed_root / "requests" / candidate_id
        body = protocol.request_body(
            item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
        )
        request_bytes = canonical_bytes(body)
        if not directory.is_dir():
            states[candidate_id] = "MISSING"
            continue
        validator_driver.require_owned_dir(directory)
        state, _observation = _c_gt_1_directory_state(directory, request_bytes)
        if state == C_GT_1_STATE_REQUEST_ONLY:
            states[candidate_id] = "REQUEST_ONLY"
        elif state == C_GT_1_STATE_ATTEMPTED:
            states[candidate_id] = "ATTEMPTED"
        elif state == C_GT_1_STATE_INTERRUPTED_4FILE:
            states[candidate_id] = "INTERRUPTED_4FILE"
        else:
            raise ExperimentError(f"failed root holds an unadoptable C>1 state: {candidate_id}")
    census = Counter(states.values())
    if (
        census.get("ATTEMPTED", 0) != spec["completed_attempted"]
        or census.get("INTERRUPTED_4FILE", 0) != spec["completed_uncertain"]
        or census.get("REQUEST_ONLY", 0) != spec["request_only"]
        or census.get("MISSING", 0) != spec["missing"]
        or len(states) != len(c_gt_1_items)
    ):
        raise ExperimentError(f"failed root C>1 state census drifted: {dict(census)}")
    return {
        "failed_root": failed_root.name,
        "failed_root_path": str(failed_root.absolute()),
        "configuration_sha256": spec["configuration_sha256"],
        "run_status_sha256": spec["run_status_sha256"],
        "implementation_head": spec["implementation_head"],
        "request_tree": request_tree,
        "state_census": {
            "completed_attempted": census.get("ATTEMPTED", 0),
            "completed_uncertain_persisted": census.get("INTERRUPTED_4FILE", 0),
            "request_only_interrupted": census.get("REQUEST_ONLY", 0),
            "missing": census.get("MISSING", 0),
        },
        "defect": spec["defect"],
        "resampled": False,
        "states": states,
    }


def _reuse_identity_basis(failed_configuration: dict[str, Any]) -> dict[str, Any]:
    deployment = failed_configuration["deployment"]
    return {
        "request": (
            "byte-exact frozen validator request body "
            "(canonical UTF-8 JSON with one final LF)"
        ),
        "raw_response": "byte-exact immutable bounded raw response",
        "observation": "byte-exact immutable parsed observation",
        "prompt_sha256": protocol.FROZEN_PROMPT_SHA256,
        "profile_sha256": EXPECTED_007M_PROFILE_SHA256,
        "parser": prior_j.EXPECTED_PARSER,
        "deployment": {
            "endpoint": deployment["endpoint"],
            "model": protocol.MODEL,
            "credential_env": deployment["credential_env"],
            "profile_sha256": EXPECTED_007M_PROFILE_SHA256,
        },
        "source_configuration_sha256": EXPECTED_FAILED_ROOT_CONFIGURATION,
    }


def adopt_completed_c_gt_1(
    failed_root: Path,
    scratch: Path,
    c_gt_1_items: list[dict[str, Any]],
    states: dict[str, str],
    identity_basis: dict[str, Any],
    *,
    expected_total: int,
) -> list[dict[str, Any]]:
    """Copy the failed root's completed C>1 observations under exact identity."""
    prior_j.ensure_request_root(scratch)
    records: list[dict[str, Any]] = []
    for item in c_gt_1_items:
        candidate_id = protocol.candidate_path_id(item)
        state = states[candidate_id]
        if state not in (C_GT_1_STATE_ATTEMPTED, C_GT_1_STATE_INTERRUPTED_4FILE):
            continue
        source_dir = failed_root / "requests" / candidate_id
        destination_dir = scratch / "requests" / candidate_id
        if destination_dir.exists():
            raise ExperimentError(f"adoption destination already exists: {candidate_id}")
        validator_driver.copy_tree_exact(source_dir, destination_dir)
        body = protocol.request_body(
            item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
        )
        destination_state, observation = _c_gt_1_directory_state(
            destination_dir, canonical_bytes(body)
        )
        if destination_state != state:
            raise ExperimentError(f"adopted C>1 state drifted: {candidate_id}")
        records.append(
            {
                "candidate_id": candidate_id,
                "stable_key": list(protocol.stable_key(item)),
                "source_root": failed_root.name,
                "state": (
                    "completed-attempted"
                    if state == C_GT_1_STATE_ATTEMPTED
                    else "interrupted-uncertain"
                ),
                "request_sha256": sha256_file(destination_dir / "request.json"),
                "dispatch_sha256": sha256_file(destination_dir / "dispatch.json"),
                "raw_response_sha256": sha256_file(destination_dir / "raw-response.json"),
                "observation_sha256": sha256_file(destination_dir / "observation.json"),
                "decision": observation.get("decision"),
                "new_calls": 0,
                "identity_basis": identity_basis,
            }
        )
    if len(records) != expected_total:
        raise ExperimentError("adoption reuse count mismatch")
    return records


def carry_interrupted_c_gt_1(
    failed_root: Path,
    scratch: Path,
    c_gt_1_items: list[dict[str, Any]],
    states: dict[str, str],
    *,
    expected_total: int,
) -> list[dict[str, Any]]:
    """Carry request-only interruptions to conservative uncertain observations.

    Copies the frozen request + dispatch marker bytes, then closes the request
    with the frozen interrupted_observation finalizer: no transport, no call,
    no resampling.
    """
    prior_j.ensure_request_root(scratch)
    records: list[dict[str, Any]] = []
    for item in c_gt_1_items:
        candidate_id = protocol.candidate_path_id(item)
        if states[candidate_id] != C_GT_1_STATE_REQUEST_ONLY:
            continue
        source_dir = failed_root / "requests" / candidate_id
        destination_dir = scratch / "requests" / candidate_id
        if destination_dir.exists():
            raise ExperimentError(f"carry destination already exists: {candidate_id}")
        body = protocol.request_body(
            item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
        )
        request_bytes = canonical_bytes(body)
        destination_dir.mkdir(mode=0o700)
        validator_driver.require_owned_dir(destination_dir)
        source_request_sha = sha256_file(source_dir / "request.json")
        source_dispatch_sha = sha256_file(source_dir / "dispatch.json")
        validator_driver.copy_file_exact(
            source_dir / "request.json", destination_dir / "request.json"
        )
        validator_driver.copy_file_exact(
            source_dir / "dispatch.json", destination_dir / "dispatch.json"
        )
        observation = protocol.interrupted_observation(destination_dir, body)
        destination_state, _ = _c_gt_1_directory_state(destination_dir, request_bytes)
        if (
            destination_state != C_GT_1_STATE_INTERRUPTED_4FILE
            or observation.get("failure") != "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE"
        ):
            raise ExperimentError(
                f"carried C>1 interruption is not the conservative state: {candidate_id}"
            )
        records.append(
            {
                "candidate_id": candidate_id,
                "stable_key": list(protocol.stable_key(item)),
                "source_root": failed_root.name,
                "source_request_sha256": source_request_sha,
                "source_dispatch_sha256": source_dispatch_sha,
                "request_sha256": sha256_bytes(request_bytes),
                "dispatch_sha256": sha256_file(destination_dir / "dispatch.json"),
                "raw_response_sha256": sha256_file(destination_dir / "raw-response.json"),
                "observation_sha256": sha256_file(destination_dir / "observation.json"),
                "new_calls": 0,
                "failure": "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE",
            }
        )
    if len(records) != expected_total:
        raise ExperimentError("carry count mismatch")
    return records


def _slice_tpfpfn(view: dict[str, Any]) -> dict[str, Any]:
    return {
        "tp": view["tp"],
        "fp": view["fp"],
        "fn": view["fn"],
        "precision": view.get("precision"),
        "recall": view.get("recall"),
    }


def complete_live_result(
    scratch: Path,
    prepared: dict[str, Any],
    c_gt_1_observations: dict[str, dict[str, Any]],
    observation_counts: dict[str, int],
    worker_status: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    pairs = prepared["pairs"]
    records = prepared["records"]
    uv_indices = prepared["uv_indices"]
    c1_items = prepared["c1_items"]
    c1_observations = prepared["c1_observations"]
    fresh = prepared["fresh"]
    # The scheduled C>1 population is fresh plus the adopted (reused or
    # carried) targets; only ``fresh`` receives new calls.
    c_gt_1_all = prepared.get("c_gt_1_all", fresh)
    new_ids = {protocol.candidate_path_id(item) for item in fresh}
    reuse_records = prepared.get("reuse_records", [])
    carry_records = prepared.get("carry_records", [])
    configuration_sha = prepared["configuration_sha256"]
    observations = {**c1_observations, **c_gt_1_observations}

    candidates_by_case: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for item in [*c1_items, *c_gt_1_all]:
        candidates_by_case.setdefault((item["phase"], item["case_index"]), []).append(item)
    c1_by_case: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for item in c1_items:
        c1_by_case.setdefault((item["phase"], item["case_index"]), []).append(item)

    by_case: dict[str, list[dict[str, Any]]] = {phase: [] for phase in PHASES}
    for phase, cases in records.items():
        for case in cases:
            value = validator_driver.make_case_result(
                phase,
                case,
                candidates_by_case.get((phase, case["index"]), []),
                observations,
                configuration_sha,
            )
            value["experiment_id"] = EXPERIMENT_ID
            by_case[phase].append(value)

    replay_by_case: dict[str, list[dict[str, Any]]] = {phase: [] for phase in PHASES}
    for phase, cases in records.items():
        for case in cases:
            value = validator_driver.make_case_result(
                phase,
                case,
                c1_by_case.get((phase, case["index"]), []),
                c1_observations,
                configuration_sha,
            )
            value["experiment_id"] = prior_j.EXPERIMENT_ID
            replay_by_case[phase].append(value)
    reuse_ids = {
        record["candidate_id"] for record in read_json(scratch / "SOURCE-007J-REUSE-RECORDS.json")
    }
    for phase_records in replay_by_case.values():
        for record in phase_records:
            for target in record["validator_targets"]:
                target["observation_source"] = (
                    "reuse" if target["candidate_id"] in reuse_ids else "fresh"
                )

    persisted_case_results = read_json(scratch / "SOURCE-007J-CASE-RESULTS.json")
    if not isinstance(persisted_case_results, dict):
        raise ExperimentError("007-j case results are malformed")
    for phase in PHASES:
        persisted_rows = persisted_case_results.get(phase)
        if not isinstance(persisted_rows, list) or len(persisted_rows) != len(
            replay_by_case[phase]
        ):
            raise ExperimentError(f"007-j replay case count drift: {phase}")
        for replay_row, persisted_row in zip(replay_by_case[phase], persisted_rows, strict=True):
            replay_stripped = {
                key: value for key, value in replay_row.items() if key != "configuration_sha256"
            }
            persisted_stripped = {
                key: value
                for key, value in persisted_row.items()
                if key != "configuration_sha256"
            }
            if not json_normalized_equal(replay_stripped, persisted_stripped):
                raise ExperimentError(
                    f"007-j replay case result drift: {phase}/{replay_row.get('index')}"
                )

    persisted_metrics = read_json(scratch / "SOURCE-007J-RESULTS.json")
    persisted_views = (persisted_metrics.get("metrics") or {}).get("views")
    if not isinstance(persisted_views, dict):
        raise ExperimentError("007-j persisted metrics views are malformed")
    replay_metrics = validator_driver.make_views(
        pairs, replay_by_case, c1_items, c1_observations, uv_indices, {}
    )
    for phase in PHASES:
        persisted_phase = persisted_views.get(phase)
        if not isinstance(persisted_phase, dict):
            raise ExperimentError(f"007-j persisted views lack {phase}")
        for view, replay_view in replay_metrics["views"][phase].items():
            if not json_normalized_equal(persisted_phase.get(view), replay_view):
                raise ExperimentError(f"007-j replay view drift: {phase}/{view}")
    if not json_normalized_equal(
        replay_metrics["global_validator"],
        (persisted_metrics.get("metrics") or {}).get("global_validator"),
    ):
        raise ExperimentError("007-j replay global validator drift")
    for slice_name, (tp, fn) in EXPECTED_SLICE_BASELINE.items():
        phase, view = SLICE_VIEW[slice_name]
        fallback = replay_metrics["views"][phase][view]["validated_fallback"]
        if fallback.get("tp") != tp or fallback.get("fn") != fn:
            raise ExperimentError(f"007-j replay baseline tp/fn drift for {slice_name}")

    all_items = protocol.ordered_candidates([*c1_items, *c_gt_1_all])
    primary_metrics = validator_driver.make_views(
        pairs, by_case, all_items, observations, uv_indices, worker_status
    )

    c_gt_1_ids = {protocol.candidate_path_id(item) for item in c_gt_1_all}
    outcomes: Counter[str] = Counter()
    attribution: Counter[str] = Counter()
    attribution_by_decision = {
        key: Counter() for key in ("USE_CANDIDATE", "KEEP_ORIGINAL", "UNCERTAIN", "FAILURE")
    }
    latencies: list[float] = []
    new_latencies: list[float] = []
    inherited_latencies: list[float] = []
    token_totals = {"input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0}
    new_token_totals = {"input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0}
    inherited_token_totals = {"input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0}
    accepted = {"exact_reference": 0, "non_reference": 0, "unresolved": 0}
    for phase_records in by_case.values():
        for record in phase_records:
            for target in record["validator_targets"]:
                if target["candidate_id"] not in c_gt_1_ids:
                    continue
                decision = target["decision"] or "FAILURE"
                outcomes[decision] += 1
                status = target["attribution"]["status"]
                attribution[status] += 1
                attribution_by_decision[decision][status] += 1
                if decision == "USE_CANDIDATE":
                    accepted[status] += 1
                observation = target["observation"]
                is_new_call = target["candidate_id"] in new_ids
                latency_pool = new_latencies if is_new_call else inherited_latencies
                token_pool = new_token_totals if is_new_call else inherited_token_totals
                if observation.get("http_seconds") is not None:
                    latencies.append(float(observation["http_seconds"]))
                    latency_pool.append(float(observation["http_seconds"]))
                for key in token_totals:
                    if observation.get(key) is not None:
                        token_totals[key] += int(observation[key])
                        token_pool[key] += int(observation[key])

    paired: dict[str, Any] = {}
    for slice_name, (phase, view) in SLICE_VIEW.items():
        primary = primary_metrics["views"][phase][view]["validated_only"]
        fallback = replay_metrics["views"][phase][view]["validated_fallback"]
        replay_only = replay_metrics["views"][phase][view]["validated_only"]
        paired[slice_name] = {
            "007m_validated_only": _slice_tpfpfn(primary),
            "007j_validated_fallback": _slice_tpfpfn(fallback),
            "007j_validated_only": _slice_tpfpfn(replay_only),
            "delta_vs_007j_validated_fallback": {
                key: primary[key] - fallback[key] for key in ("tp", "fp", "fn")
            },
        }

    preservation_phase = "dassle-spelling-preservation"
    preservation = {
        "007m_validated_only": primary_metrics["views"][preservation_phase]["all"].get(
            "preservation_changed"
        ),
        "007j_validated_fallback": replay_metrics["views"][preservation_phase]["all"].get(
            "preservation_changed"
        ),
        "integrity_007m_validated_only": primary_metrics["views"][preservation_phase]["all"][
            "integrity"
        ]["validated_only"],
    }

    validator_driver.immutable_json(scratch / "CASE-RESULTS-007M.json", by_case)
    validator_driver.immutable_json(scratch / "CASE-RESULTS-007J-REPLAY.json", replay_by_case)
    aggregate = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "run_id": RUN_ID,
        "status": "LIVE_CENSUS_COMPLETE",
        "implementation_head": prepared["configuration"]["implementation_head"],
        "configuration_sha256": configuration_sha,
        "population": {
            "c1": len(c1_items),
            "c_gt_1": len(c_gt_1_all),
            "scheduled_total": len(c1_items) + len(c_gt_1_all),
            "c_gt_1_new_calls": len(fresh),
            "c_gt_1_by_phase": {
                phase: sum(1 for item in c_gt_1_all if item["phase"] == phase) for phase in PHASES
            },
            "c_gt_1_new_calls_by_phase": {
                phase: sum(1 for item in fresh if item["phase"] == phase) for phase in PHASES
            },
        },
        "reuse": prepared["configuration"]["reuse"],
        **({
            "adoption": prepared["configuration"]["adoption"]
        } if "adoption" in prepared["configuration"] else {}),
        "observations": {
            "total": len(observations),
            "c1_copied": len(c1_observations),
            "c_gt_1": len(c_gt_1_observations),
            "dispatched_http": observation_counts["dispatched"],
            "uncertain_deliveries": observation_counts["uncertain"],
            "operational_failures": observation_counts["operational_failures"],
            "c_gt_1_new_calls": len(new_ids),
            "c_gt_1_reused": len(reuse_records),
            "c_gt_1_reused_attempted": sum(
                1 for record in reuse_records if record.get("state") == "completed-attempted"
            ),
            "c_gt_1_reused_uncertain": sum(
                1 for record in reuse_records if record.get("state") == "interrupted-uncertain"
            ),
            "c_gt_1_interrupted_carried": len(carry_records),
        },
        "c_gt_1_outcomes": {
            "decisions": dict(outcomes),
            "attribution": dict(attribution),
            "attribution_by_decision": {
                key: dict(value) for key, value in attribution_by_decision.items()
            },
            "accepted_exact_reference": accepted["exact_reference"],
            "accepted_non_reference": accepted["non_reference"],
            "accepted_unresolved": accepted["unresolved"],
            "latency_seconds": protocol.distribution(latencies),
            "latency_seconds_new_calls": protocol.distribution(new_latencies),
            "latency_seconds_inherited": protocol.distribution(inherited_latencies),
            "token_totals": token_totals,
            "token_totals_new_calls": new_token_totals,
            "token_totals_inherited": inherited_token_totals,
        },
        "worker_counts": {
            str(worker): {
                key: status[key] for key in ("assigned", "completed", "dispatched_http", "failures")
            }
            for worker, status in sorted(worker_status.items())
        },
        "paired_slices": paired,
        "preservation": preservation,
        "views": {
            "007m_primary": primary_metrics,
            "007j_replay": replay_metrics,
        },
        "artifacts_sha256": {
            "case_results_007m": sha256_file(scratch / "CASE-RESULTS-007M.json"),
            "case_results_007j_replay": sha256_file(scratch / "CASE-RESULTS-007J-REPLAY.json"),
        },
    }
    aggregate_sha = validator_driver.immutable_json(scratch / "LIVE-AGGREGATE.json", aggregate)
    validator_driver.mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "LIVE_CENSUS_COMPLETE",
            "run_id": RUN_ID,
            "implementation_head": prepared["configuration"]["implementation_head"],
            "configuration_sha256": configuration_sha,
            "live_aggregate_sha256": aggregate_sha,
            "c1_copied_observations": len(c1_observations),
            "c_gt_1_observations": len(c_gt_1_observations),
            "c_gt_1_reused_observations": len(reuse_records),
            "c_gt_1_interrupted_carried": len(carry_records),
            "dispatched_http_requests": observation_counts["dispatched"],
            "uncertain_deliveries": observation_counts["uncertain"],
            "operational_failures": observation_counts["operational_failures"],
            "workers": protocol.WORKERS,
            "aggregate_artifacts_verified": True,
        },
    )
    return aggregate


def _live_summary(
    scratch: Path, prepared: dict[str, Any], aggregate: dict[str, Any]
) -> dict[str, Any]:
    return {
        "status": aggregate["status"],
        "run_id": RUN_ID,
        "scratch": str(scratch),
        "implementation_head": aggregate["implementation_head"],
        "configuration_sha256": prepared["configuration_sha256"],
        "population": aggregate["population"],
        "observations": aggregate["observations"],
        **({"adoption": aggregate["adoption"]} if "adoption" in aggregate else {}),
        "c_gt_1_outcomes": aggregate["c_gt_1_outcomes"],
        "worker_counts": aggregate["worker_counts"],
        "paired_slices": aggregate["paired_slices"],
        "preservation": aggregate["preservation"],
        "private_artifact_sha256": {
            "LIVE-AGGREGATE.json": sha256_file(scratch / "LIVE-AGGREGATE.json"),
            "CASE-RESULTS-007M.json": sha256_file(scratch / "CASE-RESULTS-007M.json"),
            "CASE-RESULTS-007J-REPLAY.json": sha256_file(scratch / "CASE-RESULTS-007J-REPLAY.json"),
            "CONFIGURATION.json": prepared["configuration_sha256"],
            "WORKER-RESULT.json": sha256_file(scratch / "WORKER-RESULT.json"),
        },
    }


def blocked_live_result(scratch: Path, prepared: dict[str, Any], reason: str) -> dict[str, Any]:
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "run_id": RUN_ID,
        "configuration_sha256": prepared["configuration_sha256"],
        "status": "BLOCKED",
        "blocker": reason,
        "offline": {
            "c1_copied_observations": len(prepared["c1_items"]),
            "scheduled_new_calls": len(prepared["fresh"]),
            "fresh_candidates_without_dispatch": len(prepared["fresh"]),
            "c_gt_1_reused_observations": len(prepared.get("reuse_records", ())),
            "c_gt_1_interrupted_carried": len(prepared.get("carry_records", ())),
            "dispatched_http_requests": 0,
        },
    }
    result_sha = validator_driver.immutable_json(scratch / "RESULTS.json", result)
    validator_driver.mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "BLOCKED",
            "run_id": RUN_ID,
            "blocker": reason,
            "configuration_sha256": prepared["configuration_sha256"],
            "dispatched_http_requests": 0,
        },
    )
    return {
        "status": "BLOCKED",
        "run_id": RUN_ID,
        "scratch": str(scratch),
        "blocker": reason,
        "configuration_sha256": prepared["configuration_sha256"],
        "private_results_sha256": result_sha,
    }


def run_live(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    scratch = Path(args.scratch).absolute()
    if args.census_root:
        census_root = Path(args.census_root).absolute()
    else:
        census_root = NATIVE_RUNTIME_PARENT / EXPECTED_CENSUS_ROOT
    source_root = Path(args.source_root).absolute() if args.source_root else None
    if (scratch / "CONFIGURATION.json").exists():
        if source_root is None:
            raise ExperimentError("live resume requires the frozen 007-j source root")
        prepared = load_prepared_live(
            scratch, repo_root, args.expected_implementation_head, source_root, census_root
        )
    else:
        if source_root is None:
            raise ExperimentError("initial live preparation requires the frozen 007-j source root")
        if args.profile is None:
            raise ExperimentError("initial live preparation requires the explicit profile path")
        profile_path = Path(args.profile).absolute()
        if args.adopt_failed_root is not None:
            prepared = prepare_adopted_live(
                repo_root,
                scratch,
                source_root,
                census_root,
                Path(args.adopt_failed_root).absolute(),
                args.expected_implementation_head,
                profile_path,
                args.credential_env,
            )
        else:
            prepared = prepare_live(
                repo_root,
                scratch,
                source_root,
                census_root,
                args.expected_implementation_head,
                profile_path,
                args.credential_env,
            )
    if args.prepare_only:
        return {
            "status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "run_id": RUN_ID,
            "scratch": str(scratch),
            "configuration_sha256": prepared["configuration_sha256"],
            "c1_copied_observations": EXPECTED_007J_C1_TOTAL,
            "c_gt_1_reused_observations": len(prepared.get("reuse_records", ())),
            "c_gt_1_interrupted_carried": len(prepared.get("carry_records", ())),
            "scheduled_new_calls": len(prepared["fresh"]),
            "fresh_calls": 0,
        }
    if (scratch / "LIVE-AGGREGATE.json").exists():
        existing = read_json(scratch / "LIVE-AGGREGATE.json")
        if isinstance(existing, dict) and existing.get("status") == "LIVE_CENSUS_COMPLETE":
            summary = _live_summary(scratch, prepared, existing)
            summary["resampled"] = False
            return summary
    deployment = prepared["configuration"]["deployment"]
    try:
        worker_status = execute_fresh_007m(
            scratch, prepared["fresh"], deployment["endpoint"], deployment["credential_env"]
        )
    except ExperimentError as exc:
        if str(exc) != "LIVE_CREDENTIAL_MISSING":
            raise
        return blocked_live_result(scratch, prepared, str(exc))
    c_gt_1_observations, observation_counts = verify_c_gt_1_observations(
        scratch, prepared["c_gt_1_all"]
    )
    aggregate = complete_live_result(
        scratch, prepared, c_gt_1_observations, observation_counts, worker_status
    )
    summary = _live_summary(scratch, prepared, aggregate)
    summary["resampled"] = False
    return summary


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.live:
        return run_live(args)
    repo_root = Path(args.repo_root).resolve()
    scratch = Path(args.scratch).absolute()
    ensure_scratch(scratch)
    source_root = Path(args.source_root).absolute()
    identity = verify_implementation_identity(repo_root, args.expected_implementation_head)
    source = verify_source_root(source_root)
    validator_driver.stage_frozen_inputs(source_root, scratch)
    pairs, _baseline, uv_indices, records, case_digest = validator_driver.load_frozen_state(scratch)
    if case_digest != prior_j.EXPECTED_PRIOR_CASES:
        raise ExperimentError("staged frozen case identity mismatch")
    index_path = scratch / "inputs" / "index" / "index.sqlite"
    vocabulary, _buckets, vocabulary_seconds, vocabulary_rows = baseline_driver.load_vocabulary(
        index_path
    )
    index = IndexQueries(index_path)
    try:
        schema = verify_index_schema(index)
        deletion_index = distance_one.build_deletion_signature_index(vocabulary)
        c1_digest, _c1_population = verify_007j_c1_identity(records, vocabulary, deletion_index)
        population, analysis = build_c_gt_1_population(records, vocabulary, deletion_index)
        census = census_population(population, index, vocabulary, uv_indices)
    finally:
        index.close()
    analysis["vocabulary_forms"] = vocabulary_rows
    census["runtime"] = {
        "vocabulary_loading_seconds": vocabulary_seconds,
        "vocabulary_rows": vocabulary_rows,
        "candidate_search_seconds": analysis["lookup_seconds"],
        "ranking_seconds": census["ranking_seconds"],
        "headroom_seconds": census["headroom_seconds"],
    }
    private_sha256: dict[str, str] = {}
    private_sha256["source"] = validator_driver.immutable_json(
        scratch / "SOURCE.json", {**identity, **source}
    )
    private_sha256["index_schema"] = validator_driver.immutable_json(
        scratch / "INDEX-SCHEMA.json",
        {
            "index_sha256": sha256_file(index_path),
            "index_size": index_path.stat().st_size,
            **schema,
        },
    )
    private_sha256["population"] = validator_driver.immutable_json(
        scratch / "RANK-POPULATION.json", census["records"]
    )
    private_sha256["dispatch"] = validator_driver.immutable_json(
        scratch / "DISPATCH-MANIFEST.json",
        {
            "policy": DISPATCH_POLICY,
            "count": len(census["dispatch"]),
            "payloads": census["dispatch"],
        },
    )
    aggregate = {
        "experiment_id": EXPERIMENT_ID,
        "status": "CPU_CENSUS_COMPLETE",
        "implementation_head": identity["implementation_head"],
        "c1_identity_sha256": c1_digest,
        "supersedes_census_root": SUPERSEDED_CENSUS_ROOT,
        "slices": census["slices"],
        "totals": census["totals"],
        "runtime": census["runtime"],
    }
    private_sha256["aggregate"] = validator_driver.immutable_json(
        scratch / "RANK-AGGREGATE.json", aggregate
    )
    census["private_sha256"] = private_sha256
    validator_driver.mutable_status(
        scratch / "RUN-STATUS.json",
        {
            "status": "CPU_CENSUS_COMPLETE",
            "run_id": RUN_ID,
            "implementation_head": identity["implementation_head"],
            "c1_identity_sha256": c1_digest,
            "population_sha256": private_sha256["population"],
            "aggregate_sha256": private_sha256["aggregate"],
            "dispatch_sha256": private_sha256["dispatch"],
            "index_schema_sha256": private_sha256["index_schema"],
        },
    )
    public: dict[str, str] | None = None
    if args.write_public:
        public_configuration, public_result = public_projection(
            {**identity, **source}, schema, analysis, census
        )
        public = write_public(repo_root, public_configuration, public_result)
    return {
        "status": "CPU_CENSUS_COMPLETE",
        "run_id": RUN_ID,
        "scratch": str(scratch),
        "population": {**analysis["c_gt_1_counts"], "total": len(population)},
        "totals": census["totals"],
        "slices": census["slices"],
        "runtime": census["runtime"],
        "private_sha256": private_sha256,
        "public": public,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--expected-implementation-head", required=True)
    parser.add_argument("--write-public", action="store_true")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--census-root", type=Path)
    parser.add_argument("--profile", "--profile-path", dest="profile")
    parser.add_argument("--credential-env")
    parser.add_argument("--adopt-failed-root", type=Path)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(run(args), ensure_ascii=False, sort_keys=True))
    except (ExperimentError, OSError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "reason": str(exc)}, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
