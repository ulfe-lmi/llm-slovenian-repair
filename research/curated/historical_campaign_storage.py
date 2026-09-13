"""Copied storage8 source: explicit logical-root and cache injection."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class Storage:
    def __init__(self, root: str | Path, *, workspace_root: str | Path | None = None, cache_root: str | Path | None = None, metadata_root: str | Path | None = None):
        self.root = Path(root)
        self.workspace_root = Path(workspace_root).resolve() if workspace_root else None
        self.cache_root = Path(cache_root) if cache_root else None
        self.metadata_root = Path(metadata_root) if metadata_root else None

    @staticmethod
    def digest(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def sha(path: str | Path) -> str:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    @staticmethod
    def read(path: str | Path) -> Any:
        return json.loads(Path(path).read_text(encoding="utf-8"))

    def source_bytes(self, path: str | Path) -> bytes:
        path = Path(path)
        if self.workspace_root is None or self.cache_root is None or self.metadata_root is None:
            return path.read_bytes()
        resolved = path.resolve()
        if not resolved.is_relative_to(self.workspace_root):
            return path.read_bytes()
        relative = resolved.relative_to(self.workspace_root)
        cache, metadata = self.cache_root / relative, self.metadata_root / relative
        if not cache.is_file() or not metadata.is_file():
            return path.read_bytes()
        before = self.read(metadata)
        size, end = before["Size"], 0
        for region in sorted(before.get("Rs") or [], key=lambda item: item["Pos"]):
            if region["Pos"] > end:
                raise ValueError("incomplete cached source")
            end = max(end, region["Pos"] + region["Size"])
        if end < size:
            raise ValueError("incomplete cached source")
        content = cache.read_bytes()
        after = self.read(metadata)
        if len(content) != size or (before.get("Size"), before.get("Rs"), before.get("ModTime")) != (after.get("Size"), after.get("Rs"), after.get("ModTime")):
            raise ValueError("unstable cached source")
        return content

    def source_read(self, path: str | Path) -> Any:
        return json.loads(self.source_bytes(path))

    def source_sha(self, path: str | Path) -> str:
        return self.digest(self.source_bytes(path))

    def source_tree(self, path: str | Path) -> Path:
        path = Path(path)
        if self.workspace_root is not None and path.resolve().is_relative_to(self.workspace_root) and self.cache_root is not None:
            return self.cache_root / path.resolve().relative_to(self.workspace_root)
        return path
