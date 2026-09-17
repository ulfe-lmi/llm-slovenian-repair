"""Copied pinned GLEU/ERRANT scorer driver with explicit scorer resources."""

from __future__ import annotations

import re
import subprocess
import time
from pathlib import Path
from typing import Any


def tokenize(text: str) -> str:
    from syntok.tokenizer import Tokenizer

    return " ".join(str(token).strip() for token in Tokenizer().tokenize(text))


def command(args: list[str | Path], directory: str | Path, label: str, *, timeout: int = 1500, cwd: str | Path | None = None) -> dict[str, Any]:
    directory = Path(directory)
    record = directory / (label + ".command.json")
    if record.exists():
        import json
        return json.loads(record.read_text())
    started = time.monotonic()
    try:
        completed = subprocess.run([str(arg) for arg in args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        value = {"argv": [str(arg) for arg in args], "returncode": completed.returncode, "stdout": completed.stdout.decode(errors="replace"), "stderr": completed.stderr.decode(errors="replace"), "seconds": time.monotonic() - started}
    except Exception as exc:
        value = {"argv": [str(arg) for arg in args], "failure": type(exc).__name__, "message": str(exc), "seconds": time.monotonic() - started}
    from .historical_common import save
    save(record, value)
    return value


def score_pairs(directory: str | Path, sources: list[str], references: list[str], hypotheses: dict[str, list[str]], *, scorer_bin: str | Path, scorer_cwd: str | Path) -> dict[str, Any]:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    from .historical_common import immutable_bytes
    for name, values in (("source.tmp", sources), ("reference.tmp", references)):
        immutable_bytes(directory / name, ("\n".join(tokenize(text) for text in values) + "\n").encode())
    original, reference, reference_m2 = directory / "source.tmp", directory / "reference.tmp", directory / "reference.m2"
    reference_command = command([Path(scorer_bin) / "errant_parallel", "-orig", original, "-cor", reference, "-out", reference_m2, "-lang", "sl"], directory, "reference-errant", cwd=scorer_cwd)
    results = {}
    for method, values in hypotheses.items():
        hypothesis = directory / (method + ".tmp")
        immutable_bytes(hypothesis, ("\n".join(tokenize(text) for text in values) + "\n").encode())
        gleu = command([Path(scorer_bin) / "gleu", "-s", original, "-r", reference, "-o", hypothesis, "-d", "4", "-f", "-n", "4", "-t", "word", "-p", "1"], directory, method + "-gleu", cwd=scorer_cwd)
        parsed = None
        match = re.search(r"(?m)^" + re.escape(str(hypothesis)) + r"\t([0-9.]+)\s*$", gleu.get("stdout", ""))
        if gleu.get("returncode") == 0 and match:
            parsed = float(match.group(1))
        item: dict[str, Any] = {"GLEU": parsed, "GLEU_command": gleu, "ERRANT": None}
        if reference_command.get("returncode") == 0 and reference_m2.exists():
            hypothesis_m2 = directory / (method + ".m2")
            hypothesis_command = command([Path(scorer_bin) / "errant_parallel", "-orig", original, "-cor", hypothesis, "-out", hypothesis_m2, "-lang", "sl"], directory, method + "-errant", cwd=scorer_cwd)
            item["ERRANT_hypothesis_command"] = hypothesis_command
            if hypothesis_command.get("returncode") == 0 and hypothesis_m2.exists():
                compare = command([Path(scorer_bin) / "errant_compare", "-hyp", hypothesis_m2, "-ref", reference_m2], directory, method + "-compare", cwd=scorer_cwd)
                item["ERRANT_compare_command"] = compare
                match = re.search(r"(?m)^\s*(\d+)\s+(\d+)\s+(\d+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s*$", compare.get("stdout", ""))
                if compare.get("returncode") == 0 and match:
                    tp, fp, fn, precision, recall, f05 = match.groups()
                    item["ERRANT"] = {"tp": int(tp), "fp": int(fp), "fn": int(fn), "precision": float(precision), "recall": float(recall), "F0.5": float(f05)}
        if item["ERRANT"] is None:
            item["ERRANT_status"] = "NOT_EXECUTED — ACCESS/DEPENDENCY BLOCKED or scorer failure"
        results[method] = item
    return {"methods": results, "reference_command": reference_command, "examples": len(sources),
            "authority": "Unmodified pinned MultiGEC-linked GLEU and ERRANT CLIs with exact official syntok pretokenization; local reproduction only."}
