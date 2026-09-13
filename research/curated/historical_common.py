"""Copied campaign utility source with explicit roots instead of private defaults."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


_SAFE_COMPONENT = re.compile(r"[A-Za-z0-9_.-]+")


def safe_component(value: object, *, label: str = "record identity") -> str:
    """Validate a caller-owned path component before any output is created."""
    if value is None or isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError(f"{label} is not a safe path component")
    text = str(value)
    if not text or text in {".", ".."} or not _SAFE_COMPONENT.fullmatch(text):
        raise ValueError(f"{label} is not a safe path component")
    return text


def sha(path: str | Path) -> str:
    return digest(Path(path).read_bytes())


def read(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def encoded(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def immutable_bytes(path: str | Path, data: bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"immutable artifact conflict: {path}")
        return
    fd, temporary = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save(path: str | Path, value: Any) -> None:
    immutable_bytes(path, encoded(value))


def pointer(path: str | Path, value: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name("." + path.name + ".pointer")
    temporary.write_bytes(encoded(value))
    os.replace(temporary, path)


def jsonlines(path: str | Path) -> list[Any]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def snapshot(paths: list[str | Path] | tuple[str | Path, ...]) -> dict[str, str]:
    return {str(path): sha(path) for path in sorted({Path(item) for item in paths})}


def verify(config: dict[str, Any]) -> None:
    for path, expected in config["frozen_files"].items():
        if sha(path) != expected:
            raise RuntimeError(f"freeze identity changed: {path}")


def result_path(root: str | Path, benchmark: str, index: int, method: str) -> Path:
    if type(index) is not int or index < 0:
        raise ValueError("result index must be a non-negative integer")
    benchmark_name = safe_component(benchmark, label="benchmark identity")
    method_name = safe_component(method, label="method identity")
    return Path(root) / "results" / "A100" / benchmark_name / f"{index:06d}" / (method_name + ".json")
