"""Copied resource-specific adapters with an explicit private data root."""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def md_parse(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in text.split("### essay_id = ")[1:]:
        identity, body = part.split("\n", 1)
        if identity in result:
            raise ValueError("duplicate official essay ID")
        result[identity] = body.strip("\n")
    return result


def md_render(pairs: Any) -> str:
    return "".join(f"### essay_id = {identity}\n{text}\n\n" for identity, text in pairs)


def multigec(split: str, root: str | Path) -> list[dict[str, Any]]:
    folder = Path(root) / "multigec-2025/data/extracted/multigec-2025-participants-1/slovene/Solar-Eval"
    source = md_parse((folder / f"sl-solar_eval-orig-{split}.md").read_text())
    references = {} if split == "test" else md_parse((folder / f"sl-solar_eval-ref1-{split}.md").read_text())
    if split != "test" and list(source) != list(references):
        raise ValueError("official source/reference IDs differ")
    expected = {"train": 10, "dev": 50, "test": 49}[split]
    if len(source) != expected:
        raise ValueError("unexpected MultiGEC split size")
    return [{"id": identity, "input": text, "reference": references.get(identity), "category": None, "problem_type": None,
             "reference_status": "WITHHELD" if split == "test" else "SUPPLIED"} for identity, text in source.items()]


def natural_key(name: str) -> tuple[tuple[int, int | str], ...]:
    return tuple((1, int(part)) if part.isdigit() else (0, part) for part in re.split(r"(\d+)", name))


def canonical_solar(root: str | Path) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = defaultdict(list)
    archive = Path(root) / "solar-eval-1.0/solar-eval.JSON.zip"
    with zipfile.ZipFile(archive) as handle:
        for name in handle.namelist():
            if name.endswith(".json"):
                groups[name.split("/")[1]].append(name)
        rows = []
        for identity in sorted(groups):
            source, target, chunks, labels = [], [], [], Counter()
            for name in sorted(groups[identity], key=natural_key):
                raw = handle.read(name)
                value = json.loads(raw)
                for side, parts in (("source", source), ("target", target)):
                    if not all(isinstance(token["text"], str) for token in value[side]):
                        raise ValueError("canonical token text is not a string")
                    if len({token["id"] for token in value[side]}) != len(value[side]):
                        raise ValueError("canonical token IDs are not unique")
                    parts.append("".join(token["text"] for token in value[side]))
                for edge in value["edges"].values():
                    labels.update(edge["labels"])
                chunks.append({"member": name, "sha256": __import__("hashlib").sha256(raw).hexdigest(), "source_tokens": len(value["source"]), "reference_tokens": len(value["target"])})
            rows.append({"id": identity, "input": "\n\n".join(source), "reference": "\n\n".join(target), "category": None, "problem_type": None,
                         "reference_status": "SUPPLIED", "canonical_chunks": chunks, "annotation_label_counts": dict(labels)})
    if len(rows) != 109:
        raise ValueError("unexpected canonical Solar document count")
    return rows


def dassle(root: str | Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(Path(root) / "dassle-1.0/DASSLE-v1.zip") as handle:
        raw = handle.read("DASSLE-v1/DASSLE-v1-DATA.tsv").decode("utf-8")
    records = list(csv.DictReader(io.StringIO(raw), delimiter="\t"))
    columns = list(records[0])
    if len(columns) != 5 or len(records) != 7385:
        raise ValueError("unexpected DASSLE shape")
    return [{"id": str(index), "input": record[columns[2]], "reference": record[columns[3]] or None,
             "category": record[columns[0]], "problem_type": record[columns[1]], "example_source": record[columns[4]],
             "reference_status": "SUPPLIED" if record[columns[3]] else "MISSING_BLANK_FIELD"} for index, record in enumerate(records, 1)]


def slobench(root: str | Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(Path(root) / "slobench-eng-slo/slobench_ensl.en.zip") as handle:
        text = handle.read("slobench_ensl.en.txt").decode("utf-8")
    lines = text.split("\n")[:-1]
    if "\r" in text or not text.endswith("\n") or len(lines) != 1232:
        raise ValueError("unexpected SloBench shape")
    return [{"id": str(index), "input": line, "reference": None, "category": None, "problem_type": None,
             "reference_status": "WITHHELD", "line_number": index} for index, line in enumerate(lines, 1)]


def preservation(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    import hashlib
    return [{**row, "input": row["reference"], "reference": row["reference"], "preservation": True,
             "parent_source_sha256": hashlib.sha256(row["input"].encode()).hexdigest()} for row in rows if row["reference"] is not None]


def build(root: str | Path, output: str | Path) -> dict[str, Any]:
    """Build the historical data-free metadata only when an explicit output is supplied."""
    from .historical_common import digest, immutable_bytes, save
    sets = {"multigec-train": multigec("train", root), "multigec-dev": multigec("dev", root)}
    sets["multigec-dev-preservation"] = preservation(sets["multigec-dev"])
    sets["solar-canonical"] = canonical_solar(root)
    sets["solar-canonical-preservation"] = preservation(sets["solar-canonical"])
    sets["dassle"] = dassle(root)
    sets["dassle-preservation"] = preservation(sets["dassle"])
    sets["multigec-test"] = multigec("test", root)
    sets["slobench"] = slobench(root)
    metadata = {}
    output = Path(output)
    for name, rows in sets.items():
        for index, row in enumerate(rows, 1):
            row["index"], row["benchmark"] = index, name
        raw = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode()
        path = output / "datasets" / (name + ".jsonl")
        immutable_bytes(path, raw)
        metadata[name] = {"path": str(path), "sha256": digest(raw), "examples": len(rows),
                          "reference_examples": sum(row["reference"] is not None for row in rows),
                          "gold_error_examples": sum(row["reference"] is not None and row["input"] != row["reference"] for row in rows)}
    save(output / "DATASET-ADAPTATION.json", {"datasets": metadata, "source_root_parameter": "root", "new_model_calls": 0})
    return metadata
