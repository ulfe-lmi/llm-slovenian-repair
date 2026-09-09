"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Eval helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        case = json.loads(line)
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            raise ValueError("case is not an object with an id")
        start, end = case.get("start"), case.get("end")
        if (
            not isinstance(start, int)
            or not isinstance(end, int)
            or case["text"][start:end] != case["target"]
        ):
            raise ValueError(f"case {case['id']} has an invalid exact target span")
        cases.append(case)
    if len({case["id"] for case in cases}) != len(cases):
        raise ValueError("case IDs must be unique")
    return cases


def dataset_identity(path: Path) -> dict[str, Any]:
    cases = load_cases(path)
    return {"path": path.name, "count": len(cases), "sha256": file_sha256(path)}


def aggregate_candidates(
    cases: list[dict[str, Any]], candidates_by_id: dict[str, list[dict[str, Any]]]
) -> dict[str, Any]:
    candidates = [item for values in candidates_by_id.values() for item in values]
    hits = sum(
        any(
            item["start"] == case["start"] and item["end"] == case["end"]
            for item in candidates_by_id.get(case["id"], [])
        )
        for case in cases
        if case["known_error"]
    )
    false_hits = sum(
        bool(candidates_by_id.get(case["id"])) for case in cases if not case["known_error"]
    )
    return {
        "cases": len(cases),
        "known_errors": sum(bool(case["known_error"]) for case in cases),
        "candidates": len(candidates),
        "candidate_recall": hits / max(1, sum(bool(case["known_error"]) for case in cases)),
        "candidate_false_positive_cases": false_hits,
        "candidate_precision": hits / max(1, len(candidates)),
    }
