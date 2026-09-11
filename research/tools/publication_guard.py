#!/usr/bin/env python3
"""Fail-closed public research boundary and staged-byte guard."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any, Iterable, Iterator
import zipfile


ARCHIVE_SUFFIXES = (".tar", ".tar.gz", ".tgz", ".zip", ".7z", ".sqlite", ".db")
BINARY_SUFFIXES = (".bin", ".onnx", ".pt", ".pth", ".safetensors", ".npy")
PRIVATE_COMPONENTS = {
    ".git", ".venv", "venv", "private", "raw", "traces", "submissions", "datasets", "dataset"
}
ALLOWED_COMPRESSED = {"registry/file-census.json.gz"}
DENIED_JSON_KEYS = {
    "request", "response", "raw_response", "body", "body_base64", "input", "output", "reference", "text",
    "replacement", "replacement_text",
    "original_text", "input_text", "reference_text", "dataset_row", "prompt_filled", "response_body",
    "source_text", "target_text", "gold_text", "api_key", "access_token", "credential", "secret",
}
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt", ".csv", ".jsonl"}
PATH_MARKERS = tuple(
    ("/" + part + "/").encode() for part in ("tmp", "home", "root")
) + (b"C:\\Users\\",)
BEARER_VALUE = re.compile(rb"(?i)bearer[ \t]+[A-Za-z0-9._~+/=-]{20,}")
LONG_BASE64 = re.compile(rb"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{160,}={0,2}(?![A-Za-z0-9+/])")
PRIVATE_KEY_MARKER = b"-" * 5 + b"BEGIN"


def iter_regular_files(root: Path) -> Iterator[Path]:
    """Walk without following symlinks and reject every symlink component."""
    root = root.absolute()
    info = root.lstat()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise ValueError(f"publication root must be a real directory: {root}")
    stack = [root]
    while stack:
        current = stack.pop()
        with os.scandir(current) as entries:
            children = sorted(entries, key=lambda entry: entry.name, reverse=True)
            for entry in children:
                path = Path(entry.path)
                entry_info = entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(entry_info.st_mode):
                    raise ValueError(f"symlink refused: {path.relative_to(root)}")
                if stat.S_ISDIR(entry_info.st_mode):
                    stack.append(path)
                elif stat.S_ISREG(entry_info.st_mode):
                    yield path
                else:
                    raise ValueError(f"unsupported file type: {path.relative_to(root)}")


def _json_keys(value: object, path: str = "$", allowed: frozenset[str] = frozenset()) -> Iterator[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            if key_text.casefold() in DENIED_JSON_KEYS and key_text.casefold() not in allowed:
                yield f"{path}.{key_text}"
            yield from _json_keys(child, f"{path}.{key_text}", allowed)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _json_keys(child, f"{path}[{index}]", allowed)


def _compressed_payload(relative: str, data: bytes) -> bytes:
    if relative.endswith(".json.gz"):
        try:
            payload = gzip.decompress(data)
        except (OSError, EOFError) as exc:
            raise ValueError(f"invalid gzip artifact: {relative}") from exc
        if len(payload) > 500_000_000:
            raise ValueError(f"compressed artifact exceeds validation bound: {relative}")
        return payload
    return data


def _validate_bytes(relative: str, data: bytes) -> list[str]:
    errors: list[str] = []
    lower = relative.casefold()
    allowed_gzip = lower in ALLOWED_COMPRESSED or (
        lower.startswith("results/") and lower.endswith(".json.gz")
    )
    if any(lower.endswith(suffix) for suffix in BINARY_SUFFIXES) or (
        any(lower.endswith(suffix) for suffix in ARCHIVE_SUFFIXES) and not allowed_gzip
    ):
        errors.append(f"forbidden binary/archive artifact: {relative}")
    if lower.endswith(".csv") and not lower.startswith("tables/"):
        errors.append(f"CSV outside numeric tables: {relative}")
    if lower.endswith(".jsonl") and not lower.startswith("results/"):
        errors.append(f"JSONL outside numeric results: {relative}")
    payload = _compressed_payload(relative, data) if allowed_gzip else data
    if b"\x00" in payload:
        errors.append(f"binary content: {relative}")
    if any(marker in payload for marker in PATH_MARKERS):
        errors.append(f"absolute/private path: {relative}")
    if BEARER_VALUE.search(payload) or PRIVATE_KEY_MARKER in payload:
        errors.append(f"credential marker/value: {relative}")
    if LONG_BASE64.search(payload):
        errors.append(f"raw payload/base64: {relative}")
    if lower == "registry/file-census.json.gz":
        if b'"entries":[' not in payload:
            errors.append(f"census schema marker missing: {relative}")
        for key in DENIED_JSON_KEYS:
            if (b'"' + key.encode() + b'"' + b":") in payload:
                errors.append(f"raw JSON field: {relative}:$.{key}")
    elif lower.endswith(".json") or lower.endswith(".json.gz"):
        try:
            parsed = json.loads(payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON: {relative}: {exc}")
        else:
                allowed = frozenset({"replacement"}) if relative.casefold() == "fixtures/replay.json" else frozenset()
                errors.extend(f"raw JSON field: {relative}:{path}" for path in _json_keys(parsed, allowed=allowed))
    return errors


def scan_public(root: Path) -> list[str]:
    root = root.absolute()
    errors: list[str] = []
    for path in iter_regular_files(root):
        relative = path.relative_to(root).as_posix()
        if any(part.casefold() in PRIVATE_COMPONENTS for part in Path(relative).parts):
            errors.append(f"private path: {relative}")
        try:
            data = path.read_bytes()
        except OSError as exc:
            errors.append(f"unreadable artifact: {relative}: {type(exc).__name__}")
            continue
        errors.extend(_validate_bytes(relative, data))
    return errors


def _tokens(data: bytes) -> list[str]:
    text = data.decode("utf-8")
    return re.findall(r"[\wÀ-ž]+(?:['’\-][\wÀ-ž]+)*", text.casefold(), re.UNICODE)


def _add_windows(hashes: set[str], tokens: list[str]) -> None:
    width = 16
    for start in range(max(0, len(tokens) - width + 1)):
        window = " ".join(tokens[start : start + width])
        if len(window) >= 12:
            hashes.add(hashlib.sha256(window.encode()).hexdigest())


def _add_short_windows(hashes: set[str], tokens: list[str]) -> None:
    if len(tokens) > 20:
        return
    for width in range(4, len(tokens) + 1):
        for start in range(len(tokens) - width + 1):
            hashes.add(hashlib.sha256(" ".join(tokens[start : start + width]).encode()).hexdigest())


def _structured_strings(value: object) -> Iterator[bytes]:
    if isinstance(value, str):
        yield value.encode("utf-8")
    elif isinstance(value, dict):
        for child in value.values():
            yield from _structured_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _structured_strings(child)


def _private_fragments(path: Path) -> Iterable[bytes]:
    suffix = path.name.casefold()
    if suffix.endswith(".zip"):
        with zipfile.ZipFile(path) as archive:
            members = [info for info in archive.infolist() if not info.is_dir()]
            if not members:
                raise ValueError(f"empty private archive: {path.name}")
            for info in members:
                if info.file_size > 50_000_000:
                    continue
                if info.filename.casefold().endswith((".txt", ".tsv", ".csv", ".json", ".jsonl", ".md")):
                    data = archive.read(info)
                    if info.filename.casefold().endswith(".json"):
                        try:
                            yield from _structured_strings(json.loads(data))
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            raise ValueError(f"private structured source is not valid JSON: {info.filename}")
                    else:
                        yield data
        return
    if path.stat().st_size > 50_000_000:
        raise ValueError(f"private text source exceeds scan bound: {path.name}")
    data = path.read_bytes()
    if path.suffix.casefold() == ".json":
        try:
            yield from _structured_strings(json.loads(data))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"private structured source is not valid JSON: {path.name}") from exc
    else:
        yield data


def scan_private_overlap(public_root: Path, private_root: Path) -> list[str]:
    """Hash short and long source windows, including structured archive members."""
    public_root = public_root.absolute()
    private_root = private_root.absolute()
    private_hashes: set[str] = set()
    source_files = 0
    source_fragments = 0
    for path in iter_regular_files(private_root):
        if path.suffix.casefold() not in TEXT_SUFFIXES and not path.name.casefold().endswith(".zip"):
            continue
        source_files += 1
        try:
            for fragment in _private_fragments(path):
                tokens = _tokens(fragment)
                if not tokens:
                    continue
                source_fragments += 1
                _add_windows(private_hashes, tokens)
                _add_short_windows(private_hashes, tokens)
        except (OSError, UnicodeDecodeError, ValueError, zipfile.BadZipFile) as exc:
            return [f"private source scan failed closed: {path.relative_to(private_root)}:{type(exc).__name__}"]
    if source_files == 0 or source_fragments == 0 or not private_hashes:
        return ["private source scan failed closed: no readable prepared source coverage"]
    overlaps: list[str] = []
    for path in iter_regular_files(public_root):
        relative = path.relative_to(public_root).as_posix()
        if path.suffix.casefold() not in TEXT_SUFFIXES:
            continue
        try:
            tokens = _tokens(path.read_bytes())
        except (OSError, UnicodeDecodeError) as exc:
            overlaps.append(f"unreadable public overlap input: {relative}:{type(exc).__name__}")
            continue
        candidate_hashes: set[str] = set()
        _add_windows(candidate_hashes, tokens)
        if path.suffix.casefold() != ".py" and len(tokens) <= 20:
            _add_short_windows(candidate_hashes, tokens)
        elif path.suffix.casefold() != ".py":
            for start in range(len(tokens) - 19):
                _add_short_windows(candidate_hashes, tokens[start : start + 20])
        if private_hashes.intersection(candidate_hashes):
            overlaps.append(f"private text overlap: {relative}")
    return overlaps


def _component_check(root: Path, relative: Path) -> Path:
    if relative.is_absolute() or not relative.parts or any(part in ("", ".", "..") for part in relative.parts):
        raise ValueError("export destination must be a simple relative path")
    root = root.absolute()
    if root.is_symlink() or not root.is_dir():
        raise ValueError("publication root is not a real directory")
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"unsafe destination symlink: {current.relative_to(root)}")
        if current.exists() and current != root and not current.is_dir() and current != root / relative:
            raise ValueError(f"unsafe destination component: {current.relative_to(root)}")
    destination = root / relative
    if destination == root:
        raise ValueError("export destination must be a file")
    if destination.exists() and not destination.is_file():
        raise ValueError("export destination is not a regular file")
    return destination


def safe_destination(root: Path, destination: Path, *, overwrite: bool = False) -> Path:
    path = _component_check(root, destination)
    if path.exists() and not overwrite:
        raise FileExistsError(f"overwrite refused: {destination.as_posix()}")
    return path


def export_json(root: Path, relative_destination: str, value: object) -> Path:
    destination = safe_destination(root, Path(relative_destination))
    encoded = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    errors = _validate_bytes(Path(relative_destination).as_posix(), encoded)
    if errors:
        raise ValueError("export rejected before write: " + "; ".join(errors))
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("export destination appeared during validation")
    temporary = destination.with_name("." + destination.name + ".guard-tmp")
    if temporary.exists() or temporary.is_symlink():
        raise FileExistsError("export temporary destination exists")
    try:
        temporary.write_bytes(encoded)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("research"))
    parser.add_argument("--private-root", type=Path)
    parser.add_argument("--export-json", nargs=2, metavar=("RELATIVE_PATH", "JSON_FILE"))
    parser.add_argument("--staged-tree", type=Path, help="scan a materialized Git index/tree instead of the worktree")
    args = parser.parse_args(argv)
    root = args.staged_tree or args.root
    try:
        errors = scan_public(root)
        if args.private_root:
            errors.extend(scan_private_overlap(root, args.private_root))
        if args.export_json:
            relative_path, source = args.export_json
            export_json(root, relative_path, json.loads(Path(source).read_text(encoding="utf-8")))
            errors.extend(scan_public(root))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"publication guard: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"publication guard: PASS ({sum(1 for _ in iter_regular_files(root))} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
