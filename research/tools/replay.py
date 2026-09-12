#!/usr/bin/env python3
"""Replay actual research boundaries offline; private roots are explicit."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
from typing import Any

from research.curated.corpus import Corpus
from research.curated.pipeline import replay
from research.curated.review import Proposal, parse_expression, parse_proposal


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


def _ledger_entries(document: object) -> list[dict[str, Any]]:
    if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
        raise ValueError("an exact file-level ledger is required; use registry/file-census.json.gz, not its summary")
    entries = document["entries"]
    if not all(isinstance(entry, dict) for entry in entries):
        raise ValueError("exact file-level ledger contains a non-object entry")
    return entries


def _mapped_root(logical_root: str, private_root: Path | None, root_map: Mapping[str, Path] | None) -> Path:
    if root_map:
        if logical_root in root_map:
            return root_map[logical_root]
        for prefix, candidate in root_map.items():
            if prefix.endswith("/") and logical_root.startswith(prefix):
                return candidate / logical_root[len(prefix):]
        raise ValueError(f"no current private root mapping for logical root: {logical_root}")
    if private_root is None:
        raise ValueError(f"no current private root mapping for logical root: {logical_root}")
    return private_root / logical_root


def verify_manifest(
    manifest: Path,
    private_root: Path | None = None,
    limit: int | None = None,
    *,
    root_map: Mapping[str, Path] | None = None,
) -> tuple[int, int]:
    """Verify exact private identities using explicit logical-root mappings."""
    document = json.loads(_manifest_bytes(manifest))
    entries = _ledger_entries(document)
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
        root = entry.get("root")
        if not isinstance(root, str) or not root:
            raise ValueError("ledger entry lacks a logical root")
        path = _mapped_root(root, private_root, root_map) / relative
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise ValueError(f"private artifact is not a regular file: {entry['root']}/{relative}")
        if digest(path) != entry["sha256"]:
            raise ValueError(f"private artifact hash mismatch: {entry['root']}/{relative}")
        expected_size = entry.get("size")
        if expected_size is not None and (not isinstance(expected_size, int) or info.st_size != expected_size):
            raise ValueError(f"private artifact size mismatch: {entry['root']}/{relative}")
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


class ReplayEvidenceError(ValueError):
    """A saved record is incomplete or unverifiable; replay fails closed."""


def _record_payload(record: dict[str, Any]) -> dict[str, Any]:
    payload = record.get("input")
    if isinstance(payload, dict):
        merged = dict(payload)
        merged.update({key: value for key, value in record.items() if key != "input"})
        return merged
    return record


def _proposal(value: Any, *, retry: bool = False) -> Proposal:
    if isinstance(value, Proposal):
        return value
    if isinstance(value, str):
        value = json.loads(value)
    if isinstance(value, dict) and set(value) == {"keep", "replacement", "needs_wider_edit"}:
        return Proposal(bool(value["keep"]), value["replacement"], bool(value["needs_wider_edit"]))
    return parse_expression(value) if retry else parse_proposal(value)


def _saved_original(record: dict[str, Any]) -> str:
    for key in ("original", "source", "document", "text", "input"):
        value = record.get(key)
        if isinstance(value, str):
            return value
    raise ReplayEvidenceError("saved record lacks a complete original document")


def _saved_decisions(record: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("decisions", "first_decisions", "proposal_decisions"):
        value = record.get(key)
        if isinstance(value, list) and all(isinstance(item, dict) for item in value):
            return value
    raise ReplayEvidenceError("saved record lacks first-stage decisions")


def _decision_offset(decision: dict[str, Any]) -> str:
    for source in (decision, decision.get("candidate"), decision.get("span")):
        if isinstance(source, dict):
            value = source.get("start")
            if isinstance(value, int) and value >= 0:
                return str(value)
    raise ReplayEvidenceError("saved decision lacks an original-coordinate start")


def _nested_proposal(value: Any) -> Any:
    if isinstance(value, dict) and "proposal" in value and not {"keep", "replacement", "needs_wider_edit"}.issubset(value):
        return value["proposal"]
    return value


def _saved_proposal(decision: dict[str, Any], names: tuple[str, ...], *, retry: bool = False) -> Any:
    for name in names:
        if name in decision and decision[name] is not None:
            return _nested_proposal(decision[name])
    stages = decision.get("stages")
    if isinstance(stages, dict):
        stage = stages.get("retry" if retry else "first")
        if stage is not None:
            return _nested_proposal(stage)
    return None


def _saved_english(record: dict[str, Any]) -> dict[str, float]:
    detector = record.get("detector") if isinstance(record.get("detector"), dict) else {}
    raw = record.get("english_evidence", record.get("english", detector.get("english")))
    if raw is None:
        return {}
    values = raw.values() if isinstance(raw, dict) else raw if isinstance(raw, list) else ()
    frequencies: dict[str, float] = {}
    for item in values:
        if not isinstance(item, dict):
            raise ReplayEvidenceError("English evidence entry is not an object")
        policy = item.get("english_evidence", item)
        key = policy.get("casefolded_target") or policy.get("target_key")
        frequency = policy.get("english_frequency")
        if not isinstance(key, str):
            raise ReplayEvidenceError("English evidence is missing a numeric value; zero is not a substitute")
        if frequency is None and policy.get("english_classification") == "NOT_QUERIED_SLOVENE_AVAILABLE":
            continue
        if not isinstance(frequency, (int, float)):
            raise ReplayEvidenceError("English evidence is missing a numeric value; zero is not a substitute")
        frequencies[key.casefold()] = float(frequency)
    return frequencies


def replay_saved_record(record: dict[str, Any], index: Path, *, record_name: str = "saved") -> dict[str, Any]:
    """Replay small-study or campaign input/decisions with zero model calls."""
    record = _record_payload(record)
    original = _saved_original(record)
    decisions = _saved_decisions(record)
    detector = record.get("detector") if isinstance(record.get("detector"), dict) else {}
    marker = record["maximum"] if "maximum" in record else detector.get("maximum", _MISSING)
    if marker is _MISSING:
        raise ReplayEvidenceError("saved detector maximum/uncapped setting is missing")
    if marker is not None and (not isinstance(marker, int) or isinstance(marker, bool) or marker < 0):
        raise ReplayEvidenceError("saved detector maximum is invalid")
    proposals: dict[str, Proposal] = {}
    retries: dict[str, Proposal] = {}
    retry_failures: dict[str, dict[str, Any]] = {}
    frequencies = _saved_english(record)
    recorded_first_failure = False
    for decision in decisions:
        key = _decision_offset(decision)
        raw = _saved_proposal(decision, ("first_proposal_raw", "first_proposal", "first", "proposal"))
        if raw is not None:
            proposals[key] = _proposal(raw)
        first = decision.get("first")
        if isinstance(first, dict) and first.get("operational_failure"):
            recorded_first_failure = True
        retry = _saved_proposal(decision, ("retry_proposal_raw", "retry_proposal", "retry", "retry_decision"), retry=True)
        if retry is not None:
            retries[key] = _proposal(retry, retry=True)
        retry_record = decision.get("retry")
        if isinstance(retry_record, dict) and retry_record.get("operational_failure"):
            retry_failures[key] = {
                "kind": retry_record.get("kind", "expression-retry"),
                "failure": retry_record.get("failure"),
            }

    if recorded_first_failure:
        expected = record.get("corrected", record.get("output", record.get("final")))
        if not isinstance(expected, str) or expected != original:
            raise ReplayEvidenceError("saved first-stage failure must preserve the original output")
        return {"case": record_name, "schema": "campaign-input-decisions" if "input" in record else "original-decisions",
                "detector_maximum": marker, "first_stage_decisions": len(proposals), "retry_stage_decisions": len(retries),
                "english_values": len(frequencies), "output_sha256": hashlib.sha256(expected.encode()).hexdigest(),
                "detector_candidates": len(decisions), "review_calls": len(decisions), "retry_calls": 0,
                "operational_failure": True, "network_calls": 0, "model_calls": 0}

    def english_lookup(word: str) -> float:
        key = word.casefold()
        if key not in frequencies:
            raise ReplayEvidenceError("English evidence missing for an evaluated target; zero is not inferred")
        return frequencies[key]

    with Corpus(index) as corpus:
        result = replay(
            original,
            corpus,
            english_lookup,
            proposals,
            retries,
            maximum=marker,
            retry_failures=retry_failures,
        )
    expected = record.get("corrected", record.get("output", record.get("final")))
    if not isinstance(expected, str) or result["output"] != expected:
        raise ReplayEvidenceError("private replay output mismatch or expected output is absent")
    expected_no_retry = record.get("no_retry_output")
    if expected_no_retry is not None and result["no_retry_output"] != expected_no_retry:
        raise ReplayEvidenceError("private replay no-retry output mismatch")
    if "operational_failure" in record and bool(result["operational_failure"]) != bool(record["operational_failure"]):
        raise ReplayEvidenceError("private replay operational-failure flag mismatch")
    if "no_retry_operational_failure" in record and bool(result["no_retry_operational_failure"]) != bool(record["no_retry_operational_failure"]):
        raise ReplayEvidenceError("private replay no-retry failure flag mismatch")
    return {
        "case": record_name,
        "schema": "campaign-input-decisions" if "input" in record else "original-decisions",
        "detector_maximum": marker,
        "first_stage_decisions": len(proposals),
        "retry_stage_decisions": len(retries),
        "english_values": len(frequencies),
        "output_sha256": hashlib.sha256(result["output"].encode()).hexdigest(),
        "detector_candidates": len(result["detector"]["candidates"]),
        "review_calls": result["review_calls"],
        "retry_calls": result["retry_calls"],
        "operational_failure": result["operational_failure"],
        "no_retry_operational_failure": result["no_retry_operational_failure"],
        "network_calls": 0,
        "model_calls": 0,
    }


_MISSING = object()


def replay_private(case_path: Path, index: Path, *, maximum: int | None = None) -> dict[str, Any]:
    """Replay one saved record or a fail-closed collection of records."""
    document = json.loads(case_path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ReplayEvidenceError("saved replay document must be an object")
    rows = document.get("records", document.get("cases"))
    if isinstance(rows, list):
        receipts = [replay_saved_record(item, index, record_name=f"{case_path.stem}:{i}") for i, item in enumerate(rows) if isinstance(item, dict)]
        if len(receipts) != len(rows):
            raise ReplayEvidenceError("saved replay collection contains a non-object record")
        return {"records": len(receipts), "receipts": receipts, "network_calls": 0, "model_calls": 0}
    if maximum is not None and "maximum" not in document and "detector" not in document:
        document = {**document, "maximum": maximum}
    return replay_saved_record(document, index, record_name=case_path.stem)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=Path("research/fixtures/replay.json"))
    parser.add_argument("--scratch", type=Path, default=None)
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--private-case", type=Path)
    parser.add_argument("--saved-record", type=Path, help="small-study or campaign input/decisions JSON")
    parser.add_argument("--index", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--root-map", action="append", default=[], metavar="LOGICAL_ROOT=CURRENT_PRIVATE_ROOT",
                        help="map a ledger logical root (or prefix ending /) to its current private root")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args(argv)
    scratch = args.scratch or (Path(os.environ["TMPDIR"]) if os.environ.get("TMPDIR") else None)
    if scratch is None:
        raise SystemExit("--scratch or TMPDIR is required; a system temporary directory is not an allowed fallback")
    outputs: dict[str, Any] = {"network_calls": 0, "model_calls": 0}
    case = args.saved_record or args.private_case
    if case or args.index:
        if not case or not args.index:
            raise SystemExit("--saved-record/--private-case and --index must be supplied together")
        outputs["private_replay"] = replay_private(case, args.index)
    else:
        outputs["synthetic_replay"] = replay_fixture(args.fixture, scratch / "replay")
    if args.manifest:
        root_map: dict[str, Path] = {}
        for item in args.root_map:
            logical, separator, current = item.partition("=")
            if not separator or not logical or not current:
                raise SystemExit("--root-map must be LOGICAL_ROOT=CURRENT_PRIVATE_ROOT")
            root_map[logical] = Path(current)
        if not args.private_root and not root_map:
            raise SystemExit("--private-root or at least one --root-map is required with --manifest")
        outputs["identity_replay"] = dict(
            zip(("checked", "skipped"), verify_manifest(args.manifest, args.private_root, args.limit, root_map=root_map or None), strict=True)
        )
    print(json.dumps(outputs, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
