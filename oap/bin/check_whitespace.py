#!/usr/bin/env python3
"""Fail-closed accepted-base whitespace verification for immutable OAP history.

The workflows still run Git's literal ``diff --check BASE...REVISION``.  The
only tolerated diagnostics are the three already-published blank-at-EOF
incidents below.  Each exception is bound to its exact diagnostic, introducing
commit, current blob, byte hash, and byte size.  This is intentionally a
fixed corrective contract: a changed, missing, re-added, or additional
whitespace incident fails rather than becoming a new allowlist entry.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import NamedTuple


COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
AUTHORIZED_BASES = frozenset(
    {
        "2832fa1e51bdf3641aabbd81feab8ddb64a876da",
        "82ea1e6f4173934fa47bb34ee6a6f78338d3603a",
    }
)


class Incident(NamedTuple):
    path: str
    line: int
    message: str
    introduction_commit: str
    blob: str
    content_sha256: str
    byte_size: int

    @property
    def diagnostic(self) -> str:
        return f"{self.path}:{self.line}: {self.message}"


KNOWN_INCIDENTS = (
    Incident(
        "oap/orders/007-e-recover-forward-from-an-immutable-invalid-report.md",
        290,
        "new blank line at EOF.",
        "02084dd33ac23d3bd1caf17847ad3069fdbed6b7",
        "c6125ac107f8f6f6dbf52e175ac1e913c382a817",
        "454f91b1f98d3a0ddbafbc93c0b12be9c8517661db1f132b000cdaf0fc5b6875",
        17006,
    ),
    Incident(
        "oap/orders/007-f-complete-faithful-research-archive-and-ci-portable-reproduction.md",
        349,
        "new blank line at EOF.",
        "f17152e0c9700c81a7bd7f24a74c07f5d9ed79b3",
        "9a57556f87d2d86a63bc39757f04c3e67fd8db68",
        "516bee9cec2a52f75beba27cc4ae1756426386ab65b5ac2ce62a7c6854dbf87d",
        21642,
    ),
    Incident(
        "oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md",
        164,
        "new blank line at EOF.",
        "88af5cefb76e5aaf727806ff589df93fa08f0861",
        "5bf351e69509f61860e123790d80f889ef2bfdf4",
        "d19ac48b77f8d856ec79214de83590f0dcfc0cdf1c11b61c4ba421a962f864dd",
        13794,
    ),
)


class CheckError(RuntimeError):
    """A public, bounded failure reason for the workflow boundary."""


def _git(repo: Path, *args: str, timeout: float = 30.0) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    for name in (
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    ):
        env.pop(name, None)
    env.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_PAGER": "cat",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            check=False,
            timeout=timeout,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckError("GIT_EXECUTION_FAILED") from exc


def _successful_git(repo: Path, *args: str) -> bytes:
    result = _git(repo, *args)
    if result.returncode != 0 or result.stderr:
        raise CheckError("GIT_QUERY_FAILED")
    return result.stdout


def _resolve_commit(repo: Path, revision: str) -> str:
    if not revision or "\x00" in revision or "\n" in revision:
        raise CheckError("REVISION_INVALID")
    result = _git(repo, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")
    if result.returncode != 0 or result.stderr:
        raise CheckError("REVISION_INVALID")
    try:
        resolved = result.stdout.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise CheckError("REVISION_INVALID") from exc
    if not COMMIT_RE.fullmatch(resolved):
        raise CheckError("REVISION_INVALID")
    return resolved


def _parse_diagnostics(data: bytes) -> list[str]:
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise CheckError("DIFF_OUTPUT_MALFORMED") from exc
    if not text or not text.endswith("\n"):
        raise CheckError("DIFF_OUTPUT_MALFORMED")
    diagnostics: list[str] = []
    expects_added_line = False
    for line in text.splitlines():
        match = re.fullmatch(r"[^:\n]+:[1-9][0-9]*: ([^\n]+)", line)
        if match:
            if expects_added_line:
                raise CheckError("DIFF_OUTPUT_MALFORMED")
            diagnostics.append(line)
            expects_added_line = match.group(1) == "trailing whitespace."
        elif expects_added_line and line.startswith("+"):
            expects_added_line = False
        else:
            raise CheckError("DIFF_OUTPUT_MALFORMED")
    if expects_added_line:
        raise CheckError("DIFF_OUTPUT_MALFORMED")
    return diagnostics


def _verify_incident(repo: Path, revision: str, incident: Incident) -> None:
    try:
        blob = _successful_git(
            repo, "rev-parse", f"{revision}:{incident.path}"
        ).decode("ascii").strip()
    except (UnicodeDecodeError, CheckError) as exc:
        raise CheckError("INCIDENT_BLOB_MISMATCH") from exc
    if blob != incident.blob:
        raise CheckError("INCIDENT_BLOB_MISMATCH")
    content = _successful_git(repo, "cat-file", "blob", blob)
    if (
        len(content) != incident.byte_size
        or hashlib.sha256(content).hexdigest() != incident.content_sha256
    ):
        raise CheckError("INCIDENT_CONTENT_MISMATCH")
    try:
        introductions = _successful_git(
            repo,
            "log",
            "--reverse",
            "--format=%H",
            "--diff-filter=A",
            revision,
            "--",
            incident.path,
        ).decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise CheckError("INCIDENT_HISTORY_MALFORMED") from exc
    if introductions != [incident.introduction_commit]:
        raise CheckError("INCIDENT_INTRODUCTION_MISMATCH")


def verify(repo: Path, base: str, revision: str) -> dict[str, object]:
    if base not in AUTHORIZED_BASES:
        raise CheckError("BASE_NOT_AUTHORIZED")
    if not repo.is_dir() or repo.is_symlink():
        raise CheckError("REPOSITORY_INVALID")
    _resolve_commit(repo, base)
    resolved_revision = _resolve_commit(repo, revision)
    for incident in KNOWN_INCIDENTS:
        _verify_incident(repo, resolved_revision, incident)
    diff = _git(
        repo,
        "diff",
        "--check",
        "--no-ext-diff",
        "--no-textconv",
        f"{base}...{resolved_revision}",
    )
    if diff.stderr or diff.returncode not in (0, 2):
        raise CheckError("DIFF_FAILED")
    diagnostics = [] if diff.returncode == 0 else _parse_diagnostics(diff.stdout)
    expected = [incident.diagnostic for incident in KNOWN_INCIDENTS]
    if diagnostics != expected:
        raise CheckError("DIAGNOSTIC_SET_MISMATCH")
    return {
        "result": "PASSED",
        "base": base,
        "revision": resolved_revision,
        "diagnostics": len(diagnostics),
        "incident_paths": [incident.path for incident in KNOWN_INCIDENTS],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args(argv)
    try:
        result = verify(Path(args.repo_root).resolve(), args.base, args.revision)
    except CheckError as exc:
        print(json.dumps({"result": "FAILED", "reason": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
