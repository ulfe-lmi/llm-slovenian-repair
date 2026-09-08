#!/usr/bin/env python3
"""Validate objective-006 acquisition receipts and cache generations."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SOURCE_ID = "gigafida-2.0-words"
ARCHIVE_SHA256 = "77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a"
INVENTORY_SHA256 = "439bbd51e04e338569b9785c44d1b05c0ea023aae39898aa7d494568d6f49de3"
EXPECTED_MD5 = "b20a959f9c113aeb6504f0d753d36d10"
EXPECTED_SIZE = 115865656
LEGACY_COUNTS = {
    suffix: count for suffix, count in zip("abcdefghij", range(3, 13), strict=True)
}
RECEIPT_RE = re.compile(r"gigafida-2\.0-words-006-([a-z]{1,2})\.json\Z")
PROMOTION_DELETION_REASON = "CACHE_PROMOTION_FAILED; exact part removed; no retry"
LEGACY_RECEIPT_REPAIR = {
    "resources/source-acquisitions/gigafida-2.0-words-006-a.json": (
        "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
        "b8202c63b4fa609e35824705df53b4282d752b23",
    )
}


class AcquisitionHistoryError(ValueError):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


def _fail(reason: str) -> None:
    raise AcquisitionHistoryError(reason)


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail("ACQUISITION_DUPLICATE_KEY")
        result[key] = value
    return result


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes(), object_pairs_hook=_unique_pairs)
    except (OSError, ValueError, UnicodeError) as exc:
        raise AcquisitionHistoryError("ACQUISITION_RECEIPT_INVALID") from exc
    if not isinstance(value, dict):
        _fail("ACQUISITION_RECEIPT_INVALID")
    return value


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "-C", str(repo), "-c", "gc.auto=0", "-c", "maintenance.auto=false", *args],
        capture_output=True,
        timeout=30,
    )
    if result.returncode:
        _fail("ACQUISITION_GIT_FAILURE")
    return result


def _history_once(repo: Path, revision: str) -> None:
    raw = _git(
        repo,
        "log",
        "--reverse",
        "--format=@@%H",
        "--name-status",
        "--diff-filter=AMDR",
        "--find-renames=0",
        revision,
        "--",
        "resources/source-acquisitions",
    ).stdout.decode("utf-8", "strict")
    touches: dict[str, list[tuple[str, str]]] = {}
    commit = None
    for line in raw.splitlines():
        if line.startswith("@@"):
            commit = line[2:].split()[0]
            continue
        if not line or commit is None:
            continue
        parts = line.split("\t")
        status = parts[0][:1]
        if status not in {"A", "M", "D", "R"}:
            continue
        for path in parts[1:]:
            if RECEIPT_RE.fullmatch(Path(path).name):
                touches.setdefault(path, []).append((status, commit))
    for path, events in touches.items():
        if path in LEGACY_RECEIPT_REPAIR:
            expected = LEGACY_RECEIPT_REPAIR[path]
            if events != [("A", expected[0]), ("M", expected[1])]:
                _fail("ACQUISITION_RECEIPT_REWRITE")
        elif events != [("A", events[0][1])]:
            _fail("ACQUISITION_RECEIPT_REWRITE")


def _legacy_receipt(path: Path, suffix: str, expected: int) -> dict[str, Any]:
    value = _load(path)
    if value.get("source_id") != SOURCE_ID:
        _fail("ACQUISITION_SOURCE_ID")
    if (
        value.get("expected_byte_size") != EXPECTED_SIZE
        or value.get("expected_md5") != EXPECTED_MD5
    ):
        _fail("ACQUISITION_SOURCE_IDENTITY")
    archive = value.get("archive_sha256", value.get("archive_sha256_from_recovery"))
    if (
        archive != ARCHIVE_SHA256
        or value.get("inventory_sha256", INVENTORY_SHA256) != INVENTORY_SHA256
    ):
        _fail("ACQUISITION_SOURCE_IDENTITY")
    evidence = value.get("acquisition_evidence")
    if not isinstance(evidence, dict):
        _fail("ACQUISITION_EVIDENCE")
    if suffix == "a":
        if evidence.get("prior_get_count") != expected:
            _fail("ACQUISITION_COUNT")
    else:
        if evidence.get(f"006_{suffix}_get_count") != 1:
            _fail("ACQUISITION_COUNT")
        if evidence.get("cumulative_observed_objective_get_count") != expected:
            _fail("ACQUISITION_COUNT")
    return value


def _cache_receipt(value: dict[str, Any], prior: int) -> int:
    if value.get("schema_version") != 2 or value.get("receipt_id") != "gigafida-2.0-words-006-k":
        _fail("ACQUISITION_CURRENT_RECEIPT")
    if value.get("source_id") != SOURCE_ID or value.get("expected_byte_size") != EXPECTED_SIZE:
        _fail("ACQUISITION_SOURCE_IDENTITY")
    if value.get("expected_md5") != EXPECTED_MD5 or value.get("archive_sha256") != ARCHIVE_SHA256:
        _fail("ACQUISITION_SOURCE_IDENTITY")
    if value.get("inventory_sha256") != INVENTORY_SHA256:
        _fail("ACQUISITION_SOURCE_IDENTITY")
    if value.get("generation") != ARCHIVE_SHA256:
        _fail("ACQUISITION_CACHE_STATE")
    if value.get("prior_validation") not in {"MISSING_FETCH_REQUIRED", "INVALID_FETCH_REQUIRED"}:
        _fail("ACQUISITION_PRIOR_VALIDATION")
    network = value.get("network_get_count")
    cumulative = value.get("cumulative_observed_objective_get_count")
    if network not in {0, 1} or cumulative != prior + network:
        _fail("ACQUISITION_COUNT")
    if value.get("status") == "BLOCKED_CACHE_PROMOTION":
        if value.get("cache_state") != "MISSING" or network != 1:
            _fail("ACQUISITION_CACHE_STATE")
        if value.get("promotion_result") != "FAILED_HARDLINK_BOUNDARY":
            _fail("ACQUISITION_PROMOTION")
        if value.get("invalidation_deletion_reason") != PROMOTION_DELETION_REASON:
            _fail("ACQUISITION_DELETION_REASON")
        if value.get("consumer_count") != 0 or value.get("revalidation_count") != 0:
            _fail("ACQUISITION_CONSUMERS")
        if value.get("retention") != "NONE_AFTER_FAILED_PROMOTION":
            _fail("ACQUISITION_RETENTION")
        if value.get("source_data_retained") is not False:
            _fail("ACQUISITION_RETENTION")
    else:
        if value.get("cache_state") != "VERIFIED_REUSABLE":
            _fail("ACQUISITION_CACHE_STATE")
        if value.get("invalidation_deletion_reason") is not None:
            _fail("ACQUISITION_DELETION_REASON")
        if not isinstance(value.get("consumer_count"), int) or value["consumer_count"] < 2:
            _fail("ACQUISITION_CONSUMERS")
        if not isinstance(value.get("revalidation_count"), int) or value["revalidation_count"] < 2:
            _fail("ACQUISITION_REVALIDATIONS")
        if (
            value.get("redistribution_ready") is not False
            or value.get("retention") != "UNTIL_CONCEPT_EXPERIMENT_COMPLETION"
        ):
            _fail("ACQUISITION_RETENTION")
    if value.get("no_content_logged") is not True or value.get("retry_attempted") is not False:
        _fail("ACQUISITION_PRIVACY_OR_RETRY")
    forbidden = {"absolute_path", "private_path", "source_rows", "raw_values", "content"}
    if forbidden.intersection(value):
        _fail("ACQUISITION_PRIVATE_DATA")
    return cumulative


def validate_acquisition_history(repo: str | Path, *, revision: str = "HEAD") -> dict[str, Any]:
    repo_path = Path(repo)
    root = repo_path / "resources/source-acquisitions"
    paths: dict[str, Path] = {}
    for path in root.glob("gigafida-2.0-words-006-*.json"):
        match = RECEIPT_RE.fullmatch(path.name)
        if match:
            paths[match[1]] = path
    for suffix in LEGACY_COUNTS:
        if suffix not in paths:
            _fail("ACQUISITION_RECEIPT_MISSING")
    _history_once(repo_path, revision)
    for suffix, count in LEGACY_COUNTS.items():
        _legacy_receipt(paths[suffix], suffix, count)
    current = None
    if "k" in paths:
        current = _cache_receipt(_load(paths["k"]), LEGACY_COUNTS["j"])
    elif any(suffix not in LEGACY_COUNTS for suffix in paths):
        _fail("ACQUISITION_SUFFIX")
    if current is not None:
        # A current receipt must explicitly hand off the exact generation to the
        # concept experiment; a later refetch can only follow a recorded invalid
        # generation and exact deletion, which this round did not perform.
        for suffix, path in paths.items():
            if suffix > "k":
                value = _load(path)
                if (
                    value.get("network_get_count")
                    and value.get("invalidation_deletion_reason") is None
                ):
                    _fail("ACQUISITION_ACCIDENTAL_REFETCH")
    return {
        "result": "valid",
        "legacy_cumulative_get_count": LEGACY_COUNTS["j"],
        "current_network_get_count": 0 if current is None else current - LEGACY_COUNTS["j"],
        "current_cumulative_get_count": LEGACY_COUNTS["j"] if current is None else current,
        "receipt_count": len(paths),
        "history_rewrites": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--revision", default="HEAD")
    args = parser.parse_args(argv)
    try:
        print(
            json.dumps(
                validate_acquisition_history(args.repo_root, revision=args.revision), sort_keys=True
            )
        )
        return 0
    except AcquisitionHistoryError as exc:
        print(json.dumps({"error": exc.reason}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
