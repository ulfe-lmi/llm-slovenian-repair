#!/usr/bin/env python3
"""Replay actual research boundaries offline; private roots are explicit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
from typing import Any

from research.curated.corpus import Corpus
from research.curated.pipeline import replay
from research.curated.review import Proposal


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def _manifest_bytes(path: Path) -> bytes:
    if path.name.endswith(".gz"):
        import gzip

        return gzip.decompress(path.read_bytes())
    return path.read_bytes()


def verify_manifest(manifest: Path, private_root: Path, limit: int | None = None) -> tuple[int, int]:
    """Verify exact private identities from the compact JSON or gzip census."""
    document = json.loads(_manifest_bytes(manifest))
    entries = document["entries"] if isinstance(document, dict) else document
    checked = 0
    eligible = [
        entry
        for entry in entries
        if entry.get("classification") in {"private-only", "reconstructible-dependency", "duplicate-linked"}
    ]
    for entry in eligible:
        if limit is not None and checked >= limit:
            break
        relative = Path(entry["relative_path"])
        if any(part in ("", ".", "..") for part in relative.parts):
            raise ValueError("unsafe census path")
        path = private_root / entry["root"] / relative
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise ValueError(f"private artifact is not a regular file: {entry['root']}/{relative}")
        if digest(path) != entry["sha256"]:
            raise ValueError(f"private artifact hash mismatch: {entry['root']}/{relative}")
        checked += 1
    return checked, max(0, len(eligible) - checked)


def _create_fixture_index(fixture: dict[str, Any], path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"fixture index already exists: {path}")
    connection = sqlite3.connect(path)
    try:
        connection.executescript(
            "CREATE TABLE unigram(word TEXT PRIMARY KEY, count INTEGER NOT NULL);"
            "CREATE TABLE bigram(phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);"
            "CREATE TABLE trigram(phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);"
            "CREATE TABLE middle(left_word TEXT, right_word TEXT, middle_word TEXT, count INTEGER, "
            "PRIMARY KEY(left_word,right_word,middle_word));"
        )
        for word, count in fixture.get("unigrams", {}).items():
            connection.execute("INSERT INTO unigram VALUES (?, ?)", (word, count))
        for phrase, count in fixture.get("bigrams", {}).items():
            connection.execute("INSERT INTO bigram VALUES (?, ?)", (phrase, count))
        for phrase, count in fixture.get("trigrams", {}).items():
            connection.execute("INSERT INTO trigram VALUES (?, ?)", (phrase, count))
        connection.commit()
    finally:
        connection.close()


def replay_fixture(fixture_path: Path, scratch: Path) -> dict[str, Any]:
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    scratch.mkdir(parents=True, exist_ok=True)
    index = scratch / "synthetic-index.sqlite"
    _create_fixture_index(fixture, index)
    try:
        with Corpus(index) as corpus:
            result = replay(
                fixture["original"],
                corpus,
                lambda word: fixture.get("english_zipf", {}).get(word, 0.0),
                fixture.get("proposals", {}),
                fixture.get("retry_proposals", {}),
                maximum=fixture.get("maximum"),
            )
        if result["output"] != fixture["expected_output"]:
            raise ValueError("synthetic replay output mismatch")
        return {
            "fixture": str(fixture_path),
            "output_sha256": hashlib.sha256(result["output"].encode()).hexdigest(),
            "detector_candidates": len(result["detector"]["candidates"]),
            "review_calls": result["review_calls"],
            "retry_calls": result["retry_calls"],
            "network_calls": result["network_calls"],
            "model_calls": result["model_calls"],
        }
    finally:
        index.unlink(missing_ok=True)


def replay_private(case_path: Path, index: Path, *, maximum: int | None = 4) -> dict[str, Any]:
    """Replay one preserved case record; no private text is printed."""
    record = json.loads(case_path.read_text(encoding="utf-8"))
    original = record.get("original")
    decisions = record.get("decisions")
    if not isinstance(original, str) or not isinstance(decisions, list):
        raise ValueError("private case record lacks original/decisions")
    proposals: dict[str, Proposal] = {}
    retries: dict[str, Proposal] = {}
    frequencies: dict[str, float] = {}
    for decision in decisions:
        candidate = decision["candidate"]
        key = str(candidate["start"])
        raw = decision.get("first_proposal_raw") or decision.get("first_proposal")
        if raw is not None:
            proposals[key] = Proposal(bool(raw["keep"]), raw.get("replacement"), bool(raw["needs_wider_edit"]))
        retry = decision.get("retry_proposal_raw")
        if retry is not None:
            retries[key] = Proposal(False, retry.get("replacement"), False)
    for evidence in record.get("english_evidence", []):
        policy = evidence.get("english_evidence", evidence)
        if policy.get("english_frequency") is not None:
            frequencies[policy["casefolded_target"]] = policy["english_frequency"]
    with Corpus(index) as corpus:
        result = replay(
            original,
            corpus,
            lambda word: frequencies.get(word, 0.0),
            proposals,
            retries,
            maximum=maximum,
        )
    expected = record.get("corrected", record.get("output"))
    if not isinstance(expected, str) or result["output"] != expected:
        raise ValueError("private replay output mismatch")
    return {
        "case": case_path.stem,
        "output_sha256": hashlib.sha256(result["output"].encode()).hexdigest(),
        "detector_candidates": len(result["detector"]["candidates"]),
        "review_calls": result["review_calls"],
        "retry_calls": result["retry_calls"],
        "network_calls": 0,
        "model_calls": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=Path("research/fixtures/replay.json"))
    parser.add_argument("--scratch", type=Path, default=None)
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--private-case", type=Path)
    parser.add_argument("--index", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args(argv)
    scratch = args.scratch or (Path(os.environ["TMPDIR"]) if os.environ.get("TMPDIR") else None)
    if scratch is None:
        raise SystemExit("--scratch or TMPDIR is required; a system temporary directory is not an allowed fallback")
    outputs: dict[str, Any] = {"network_calls": 0, "model_calls": 0}
    if args.private_case or args.index:
        if not args.private_case or not args.index:
            raise SystemExit("--private-case and --index must be supplied together")
        outputs["private_replay"] = replay_private(args.private_case, args.index)
    else:
        outputs["synthetic_replay"] = replay_fixture(args.fixture, scratch / "replay")
    if args.manifest:
        if not args.private_root:
            raise SystemExit("--private-root is required with --manifest")
        outputs["identity_replay"] = dict(
            zip(("checked", "skipped"), verify_manifest(args.manifest, args.private_root, args.limit), strict=True)
        )
    print(json.dumps(outputs, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
