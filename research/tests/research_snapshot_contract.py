"""Authorized historical review snapshot contract (objective 012, round 012-b).

The research machine block's Git identity fields are an authorized historical
review snapshot, not a live cursor.  The snapshot is bound to the immutable
012-a order (pinned SHA-256 of the published order bytes) rather than to
candidate state values alone: ``main_sha`` and ``reviewed_branch_head_sha``
must equal the order's recorded merge commit and
``reviewed_branch_head_parent_sha`` its frozen PR head.  A normal descendant
of the snapshot on the current default branch is accepted (the snapshot must
be an ancestor of the available current main, not equal to every future main
revision).  Tampered order bytes, unauthorized (older or otherwise different)
snapshots and foreign/future lineage are rejected.

CPU-only, no network calls.  Callers without git history keep the existing
explicit skip semantics for the ancestry assertion; the order-bound identity
check is file-only and runs everywhere the order file is present.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ORDER_012A_REL = "oap/orders/012-a-native-migration-and-merged-round-reconciliation.md"
PINNED_ORDER_012A_SHA256 = "e320df8eb44e76877ec063abf5ca0bd6af6306684beb1bf985cfc25fafd22b34"


class SnapshotError(ValueError):
    """Bounded historical-snapshot contract failure."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


def _fail(reason: str) -> None:
    raise SnapshotError(reason)


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        check=False,
    )
    return proc.stdout.decode("utf-8").strip()


def git_ok(repo: Path, *args: str) -> int:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        check=False,
    )
    return proc.returncode


def load_bound_order(
    repo: Path,
    *,
    order_rel: str = ORDER_012A_REL,
    pinned_sha256: str = PINNED_ORDER_012A_SHA256,
) -> dict:
    """Load the immutable order metadata, verifying its pinned digest first."""
    path = Path(repo) / order_rel
    try:
        data = path.read_bytes()
    except OSError:
        _fail("SNAPSHOT_ORDER_MISSING")
    if hashlib.sha256(data).hexdigest() != pinned_sha256:
        _fail("SNAPSHOT_ORDER_TAMPERED")
    match = re.search(rb"```oap-metadata\n(.*?)\n```", data, re.S)
    if match is None:
        _fail("SNAPSHOT_ORDER_METADATA_MISSING")
    try:
        meta = json.loads(match.group(1))
    except ValueError:
        _fail("SNAPSHOT_ORDER_METADATA_INVALID")
    tail = meta.get("merged_tail_recovery")
    if not isinstance(tail, dict):
        _fail("SNAPSHOT_ORDER_METADATA_INVALID")
    return meta


def validate_historical_snapshot(
    repo: Path,
    identities: dict,
    *,
    current_main: str | None = None,
    order_rel: str = ORDER_012A_REL,
    pinned_sha256: str = PINNED_ORDER_012A_SHA256,
) -> dict:
    """Validate the machine-block Git identity as the authorized snapshot.

    Raises SnapshotError with: SNAPSHOT_ORDER_MISSING / SNAPSHOT_ORDER_TAMPERED
    / SNAPSHOT_ORDER_METADATA_INVALID (order binding),
    SNAPSHOT_IDENTITY_MISMATCH (unauthorized or older snapshot),
    SNAPSHOT_UNKNOWN_COMMIT / SNAPSHOT_LINEAGE (foreign or future lineage when
    a current main is supplied).
    """
    meta = load_bound_order(repo, order_rel=order_rel, pinned_sha256=pinned_sha256)
    tail = meta["merged_tail_recovery"]
    if identities.get("main_sha") != tail["merge_commit"]:
        _fail("SNAPSHOT_IDENTITY_MISMATCH")
    if identities.get("reviewed_branch_head_sha") != tail["merge_commit"]:
        _fail("SNAPSHOT_IDENTITY_MISMATCH")
    if identities.get("reviewed_branch_head_parent_sha") != tail["frozen_pr_head"]:
        _fail("SNAPSHOT_IDENTITY_MISMATCH")
    main_sha = identities["main_sha"]
    if current_main is not None:
        if git_ok(repo, "cat-file", "-e", main_sha + "^{commit}") != 0:
            _fail("SNAPSHOT_UNKNOWN_COMMIT")
        if git_ok(repo, "cat-file", "-e", str(current_main) + "^{commit}") != 0:
            _fail("SNAPSHOT_LINEAGE")
        if git_ok(repo, "merge-base", "--is-ancestor", main_sha, str(current_main)) != 0:
            _fail("SNAPSHOT_LINEAGE")
    return {
        "main_sha": main_sha,
        "merge_commit": tail["merge_commit"],
        "frozen_pr_head": tail["frozen_pr_head"],
        "current_main": current_main,
    }
