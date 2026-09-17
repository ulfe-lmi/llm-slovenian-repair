"""Explicit dataset adapters from the campaign, without bundling dataset bytes."""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any


def _digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def md_parse(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in text.split("### essay_id = ")[1:]:
        identity, body = part.split("\n", 1)
        if identity in result:
            raise ValueError("duplicate official essay ID")
        result[identity] = body.strip("\n")
    return result


def multigec(split: str, data_root: str | Path) -> list[dict[str, Any]]:
    root = Path(data_root)
    folder = root / "multigec-2025/data/extracted/multigec-2025-participants-1/slovene/Solar-Eval"
    source = md_parse((folder / f"sl-solar_eval-orig-{split}.md").read_text(encoding="utf-8"))
    reference = {} if split == "test" else md_parse(
        (folder / f"sl-solar_eval-ref1-{split}.md").read_text(encoding="utf-8")
    )
    if split != "test" and list(source) != list(reference):
        raise ValueError("MultiGEC source/reference IDs differ")
    expected = {"train": 10, "dev": 50, "test": 49}[split]
    if len(source) != expected:
        raise ValueError("unexpected MultiGEC split size")
    return [
        {
            "id": identity,
            "input": text,
            "reference": reference.get(identity),
            "reference_status": "WITHHELD" if split == "test" else "SUPPLIED",
        }
        for identity, text in source.items()
    ]


def _natural_key(name: str) -> tuple[tuple[int, int | str], ...]:
    return tuple((1, int(part)) if part.isdigit() else (0, part) for part in re.split(r"(\d+)", name))


def canonical_solar(data_root: str | Path) -> list[dict[str, Any]]:
    path = Path(data_root) / "solar-eval-1.0/solar-eval.JSON.zip"
    groups: dict[str, list[str]] = defaultdict(list)
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.endswith(".json"):
                groups[name.split("/")[1]].append(name)
        rows = []
        for identity in sorted(groups):
            source: list[str] = []
            target: list[str] = []
            labels: Counter[str] = Counter()
            chunks = []
            for name in sorted(groups[identity], key=_natural_key):
                raw = archive.read(name)
                value = json.loads(raw)
                for side, parts in (("source", source), ("target", target)):
                    if not all(isinstance(item["text"], str) for item in value[side]):
                        raise ValueError("Solar token text is not a string")
                    parts.append("".join(item["text"] for item in value[side]))
                for edge in value["edges"].values():
                    labels.update(edge["labels"])
                chunks.append(
                    {
                        "member": name,
                        "sha256": _digest(raw),
                        "source_tokens": len(value["source"]),
                        "reference_tokens": len(value["target"]),
                    }
                )
            rows.append(
                {
                    "id": identity,
                    "input": "\n\n".join(source),
                    "reference": "\n\n".join(target),
                    "reference_status": "SUPPLIED",
                    "canonical_chunks": chunks,
                    "annotation_label_counts": dict(labels),
                }
            )
    if len(rows) != 109:
        raise ValueError("unexpected canonical Solar document count")
    return rows


def dassle(data_root: str | Path) -> list[dict[str, Any]]:
    path = Path(data_root) / "dassle-1.0/DASSLE-v1.zip"
    with zipfile.ZipFile(path) as archive:
        raw = archive.read("DASSLE-v1/DASSLE-v1-DATA.tsv").decode("utf-8")
    records = list(csv.DictReader(io.StringIO(raw), delimiter="\t"))
    columns = list(records[0])
    if len(columns) != 5 or len(records) != 7385:
        raise ValueError("unexpected DASSLE schema or size")
    return [
        {
            "id": str(index),
            "input": record[columns[2]],
            "reference": record[columns[3]] or None,
            "category": record[columns[0]],
            "problem_type": record[columns[1]],
            "example_source": record[columns[4]],
            "reference_status": "SUPPLIED" if record[columns[3]] else "MISSING_BLANK_FIELD",
        }
        for index, record in enumerate(records, 1)
    ]


def slobench(data_root: str | Path) -> list[dict[str, Any]]:
    path = Path(data_root) / "slobench-eng-slo/slobench_ensl.en.zip"
    with zipfile.ZipFile(path) as archive:
        text = archive.read("slobench_ensl.en.txt").decode("utf-8")
    if "\r" in text or not text.endswith("\n"):
        raise ValueError("SloBench line framing mismatch")
    lines = text.split("\n")[:-1]
    if len(lines) != 1232:
        raise ValueError("unexpected SloBench size")
    return [
        {"id": str(index), "input": line, "reference": None, "reference_status": "WITHHELD", "line_number": index}
        for index, line in enumerate(lines, 1)
    ]


def preservation(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "input": row["reference"],
            "preservation": True,
            "parent_source_sha256": _digest(row["input"].encode()),
        }
        for row in rows
        if row.get("reference") is not None
    ]


def metadata_only(data_root: str | Path) -> dict[str, dict[str, int | str]]:
    """Validate and describe source preparation without writing rows to Git."""
    sets = {
        "multigec-train": multigec("train", data_root),
        "multigec-dev": multigec("dev", data_root),
        "solar-canonical": canonical_solar(data_root),
        "dassle": dassle(data_root),
        "slobench": slobench(data_root),
    }
    return {
        name: {
            "examples": len(rows),
            "reference_examples": sum(row.get("reference") is not None for row in rows),
            "unique_inputs": len({row["input"] for row in rows}),
            "ordered_ids_sha256": _digest(json.dumps([row["id"] for row in rows]).encode()),
        }
        for name, rows in sets.items()
    }
