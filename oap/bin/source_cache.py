#!/usr/bin/env python3
"""Fail-closed, explicit lifecycle for the objective-006 external cache.

This module never downloads.  Promotion accepts one caller-owned part after the
canonical inventory verifier has accepted it; consumers re-run that verifier.
Only bounded state/reason values are returned, never the private cache path or
source content.
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import pwd
import stat
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import verify_source_artifact  # noqa: E402

CACHE_SCHEMA_VERSION = 1
CACHE_STATE_MISSING = "MISSING"
CACHE_STATE_INVALID = "INVALID"
CACHE_STATE_VERIFIED = "VERIFIED_REUSABLE"
CACHE_STATE_CLEANED = "CLEANED"
SOURCE_ID = "gigafida-2.0-words"
CANONICAL_URL = (
    "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1273/"
    "GF2.0-words-all.zip?sequence=4&isAllowed=y"
)
EXPECTED_SIZE = 115865656
EXPECTED_MD5 = "b20a959f9c113aeb6504f0d753d36d10"
EXPECTED_SHA256 = "77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a"
EXPECTED_INVENTORY_SHA256 = "439bbd51e04e338569b9785c44d1b05c0ea023aae39898aa7d494568d6f49de3"
EXPECTED_GENERATION = EXPECTED_SHA256
ROOT_NAME = "gigafida-2.0-words"
FINAL_NAME = "final.zip"
PART_NAME = "part.zip"
METADATA_NAME = "metadata.json"
FIXED_NAMES = frozenset({FINAL_NAME, PART_NAME, METADATA_NAME})
METADATA_KEYS = frozenset(
    {
        "schema_version",
        "source_id",
        "canonical_url",
        "byte_size",
        "md5",
        "sha256",
        "inventory_sha256",
        "generation",
        "lifecycle",
        "redistribution",
        "created_at",
    }
)


class CacheError(ValueError):
    """Finite, non-sensitive cache boundary failure."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


def _fail(reason: str) -> None:
    raise CacheError(reason)


def _ubuntu_uid() -> int:
    try:
        return pwd.getpwnam("ubuntu").pw_uid
    except KeyError:
        return os.getuid()


def _owned(path: Path, *, kind: str | None = None, missing: bool = False) -> None:
    try:
        info = path.lstat()
    except FileNotFoundError:
        if missing:
            return
        _fail("CACHE_MISSING_PATH")
    if stat.S_ISLNK(info.st_mode):
        _fail("CACHE_SYMLINK")
    if info.st_uid != _ubuntu_uid():
        _fail("CACHE_WRONG_OWNER")
    if kind == "dir" and not stat.S_ISDIR(info.st_mode):
        _fail("CACHE_WRONG_TYPE")
    if kind == "file" and not stat.S_ISREG(info.st_mode):
        _fail("CACHE_WRONG_TYPE")
    if kind == "file" and info.st_nlink != 1:
        _fail("CACHE_HARDLINK")


def cache_root(strategic_home: str | Path) -> Path:
    strategy = Path(strategic_home)
    if not strategy.is_absolute() or strategy.name == "":
        _fail("CACHE_STRATEGIC_HOME")
    root = strategy / "source-cache" / "concept-verification" / ROOT_NAME
    # Verify every existing component without resolving through a symlink.
    current = root
    missing: list[Path] = []
    while True:
        if current.exists() or current.is_symlink():
            _owned(current, kind="dir" if current != root or root.exists() else None)
            break
        missing.append(current)
        if current == strategy:
            _fail("CACHE_STRATEGIC_HOME_MISSING")
        current = current.parent
    if current != strategy and strategy not in root.parents:
        _fail("CACHE_ROOT_PARENT")
    if root.parent != strategy / "source-cache" / "concept-verification":
        _fail("CACHE_ROOT_PARENT")
    for parent in (
        strategy,
        strategy / "source-cache",
        strategy / "source-cache" / "concept-verification",
    ):
        if parent.exists():
            _owned(parent, kind="dir")
    return root


def _read_json(path: Path) -> dict[str, Any]:
    _owned(path, kind="file")
    try:
        value = json.loads(path.read_bytes(), object_pairs_hook=_unique_pairs)
    except (OSError, ValueError, UnicodeError) as exc:
        raise CacheError("CACHE_METADATA_INVALID") from exc
    if not isinstance(value, dict):
        _fail("CACHE_METADATA_INVALID")
    return value


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail("CACHE_METADATA_DUPLICATE_KEY")
        result[key] = value
    return result


def _validate_metadata(value: dict[str, Any]) -> None:
    if set(value) != METADATA_KEYS:
        _fail("CACHE_METADATA_KEYS")
    if value["schema_version"] != CACHE_SCHEMA_VERSION:
        _fail("CACHE_METADATA_SCHEMA")
    if value["source_id"] != SOURCE_ID or value["canonical_url"] != CANONICAL_URL:
        _fail("CACHE_METADATA_SOURCE")
    if value["byte_size"] != EXPECTED_SIZE or value["md5"] != EXPECTED_MD5:
        _fail("CACHE_METADATA_DIGEST")
    if value["sha256"] != EXPECTED_SHA256 or value["generation"] != EXPECTED_GENERATION:
        _fail("CACHE_METADATA_DIGEST")
    if value["inventory_sha256"] != EXPECTED_INVENTORY_SHA256:
        _fail("CACHE_METADATA_INVENTORY")
    if value["lifecycle"] != "concept-verification" or value["redistribution"] is not False:
        _fail("CACHE_METADATA_LIFECYCLE")
    created = value["created_at"]
    if not isinstance(created, str) or not created.endswith("Z"):
        _fail("CACHE_METADATA_TIMESTAMP")
    try:
        datetime.fromisoformat(created[:-1] + "+00:00")
    except ValueError as exc:
        raise CacheError("CACHE_METADATA_TIMESTAMP") from exc


def _layout(root: Path) -> tuple[Path | None, Path | None, Path | None]:
    _owned(root, kind="dir")
    children = list(root.iterdir())
    for child in children:
        _owned(child, kind="file" if child.name in FIXED_NAMES else None)
    names = {child.name for child in children}
    if not names.issubset(FIXED_NAMES):
        _fail("CACHE_UNEXPECTED_FILE")
    return (
        root / FINAL_NAME if FINAL_NAME in names else None,
        root / PART_NAME if PART_NAME in names else None,
        root / METADATA_NAME if METADATA_NAME in names else None,
    )


def _hash_file(path: Path) -> tuple[int, str, str]:
    size = 0
    md5 = hashlib.md5(usedforsecurity=False)
    sha = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                size += len(chunk)
                md5.update(chunk)
                sha.update(chunk)
    except OSError as exc:
        raise CacheError("CACHE_READ_FAILED") from exc
    return size, md5.hexdigest(), sha.hexdigest()


def _inventory_path(inventory: str | Path | None) -> Path:
    if inventory is None:
        inventory_path = REPO_ROOT / "resources/source-inventory-v1.json"
    else:
        inventory_path = Path(inventory)
    if not inventory_path.is_absolute():
        _fail("CACHE_INVENTORY_PATH")
    _owned(inventory_path, kind="file")
    size, _, sha = _hash_file(inventory_path)
    if size == 0 or sha != EXPECTED_INVENTORY_SHA256:
        _fail("CACHE_INVENTORY_IDENTITY")
    return inventory_path


def _verify_final(final: Path, inventory: Path) -> dict[str, Any]:
    _owned(final, kind="file")
    size, md5, sha = _hash_file(final)
    if (size, md5, sha) != (EXPECTED_SIZE, EXPECTED_MD5, EXPECTED_SHA256):
        _fail("CACHE_DIGEST_MISMATCH")
    try:
        result = verify_source_artifact.verify_artifact(inventory, SOURCE_ID, final)
    except Exception as exc:
        raise CacheError("CACHE_VERIFIER_FAILED") from exc
    if (
        result.byte_size != EXPECTED_SIZE
        or result.md5 != EXPECTED_MD5
        or result.sha256 != EXPECTED_SHA256
    ):
        _fail("CACHE_VERIFIER_IDENTITY")
    return {"source_id": SOURCE_ID, "byte_size": size, "md5": md5, "sha256": sha}


def inspect(strategic_home: str | Path, *, inventory: str | Path | None = None) -> dict[str, Any]:
    """Inspect cache state without mutation or network access."""
    root = cache_root(strategic_home)
    if not root.exists():
        return {"state": CACHE_STATE_MISSING, "reason": "CACHE_ROOT_ABSENT", "network_get_count": 0}
    try:
        final, part, metadata = _layout(root)
        if final is None or metadata is None:
            return {
                "state": CACHE_STATE_INVALID,
                "reason": "CACHE_ARTIFACT_INCOMPLETE",
                "network_get_count": 0,
            }
        if part is not None:
            return {
                "state": CACHE_STATE_INVALID,
                "reason": "CACHE_PART_PRESENT",
                "network_get_count": 0,
            }
        value = _read_json(metadata)
        _validate_metadata(value)
        summary = _verify_final(final, _inventory_path(inventory))
    except CacheError as exc:
        return {"state": CACHE_STATE_INVALID, "reason": exc.reason, "network_get_count": 0}
    return {
        "state": CACHE_STATE_VERIFIED,
        "reason": "CACHE_VALID",
        "network_get_count": 0,
        "generation": value["generation"],
        "consumer_count": 0,
        "revalidation_count": 1,
        "summary": summary,
        "part_present": part is not None,
    }


def plan(strategic_home: str | Path, *, inventory: str | Path | None = None) -> dict[str, Any]:
    state = inspect(strategic_home, inventory=inventory)
    return {
        "state": state["state"],
        "action": "REUSE" if state["state"] == CACHE_STATE_VERIFIED else "FETCH_REQUIRED",
        "network_get_count": 0,
        "source_id": SOURCE_ID,
        "canonical_url_bound": True,
    }


def _make_dirs(root: Path) -> None:
    parent = root.parent
    parent.mkdir(parents=True, exist_ok=True)
    for path in (parent.parent, parent, root):
        _owned(path, kind="dir")


def _write_exclusive(path: Path, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    try:
        fd = os.open(path, flags, 0o600)
    except FileExistsError as exc:
        raise CacheError("CACHE_METADATA_EXISTS") from exc
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        path.unlink(missing_ok=True)
        raise


@contextlib.contextmanager
def _promotion_lock(root: Path):
    lock_path = root.parent / ("." + ROOT_NAME + ".promotion.lock")
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def promote(strategic_home: str | Path, *, inventory: str | Path | None = None) -> dict[str, Any]:
    """Promote the one fixed part.zip; callers own the download step."""
    root = cache_root(strategic_home)
    _make_dirs(root)
    _layout(root)
    final = root / FINAL_NAME
    part = root / PART_NAME
    metadata = root / METADATA_NAME
    if final.exists() or final.is_symlink():
        _fail("CACHE_FINAL_EXISTS")
    if metadata.exists() or metadata.is_symlink():
        _fail("CACHE_METADATA_EXISTS")
    _owned(part, kind="file")
    inventory_path = _inventory_path(inventory)
    summary = _verify_final(part, inventory_path)
    with _promotion_lock(root):
        if final.exists() or final.is_symlink():
            _fail("CACHE_FINAL_EXISTS")
        try:
            os.link(part, final, follow_symlinks=False)
            part.unlink()
        except FileExistsError as exc:
            raise CacheError("CACHE_FINAL_EXISTS") from exc
        except OSError:
            # Some owner-selected sync filesystems reject hard links.  A
            # rename of the fully verified, fixed part remains atomic and the
            # lock plus recheck prevents a cooperating writer from replacing a
            # valid final.
            if final.exists() or final.is_symlink():
                raise CacheError("CACHE_FINAL_EXISTS") from None
            try:
                os.replace(part, final)
            except OSError as exc:
                raise CacheError("CACHE_PROMOTION_FAILED") from exc
        with contextlib.suppress(OSError):
            os.chmod(final, 0o444, follow_symlinks=False)
        # Read-only mode is best effort on the selected sync filesystem;
        # ownership, type, link-count and digest checks remain mandatory.
    value = {
        "schema_version": CACHE_SCHEMA_VERSION,
        "source_id": SOURCE_ID,
        "canonical_url": CANONICAL_URL,
        "byte_size": EXPECTED_SIZE,
        "md5": EXPECTED_MD5,
        "sha256": EXPECTED_SHA256,
        "inventory_sha256": EXPECTED_INVENTORY_SHA256,
        "generation": EXPECTED_GENERATION,
        "lifecycle": "concept-verification",
        "redistribution": False,
        "created_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    _write_exclusive(metadata, (json.dumps(value, sort_keys=True, indent=2) + "\n").encode())
    return {
        "state": CACHE_STATE_VERIFIED,
        "action": "ESTABLISHED",
        "network_get_count": 1,
        **summary,
    }


def repair_invalid(strategic_home: str | Path) -> dict[str, Any]:
    """Remove only fixed cache artifacts after a verified root check."""
    root = cache_root(strategic_home)
    if not root.exists():
        return {"state": CACHE_STATE_MISSING, "deleted": 0}
    final, part, metadata = _layout(root)
    state = inspect(strategic_home)
    if state["state"] != CACHE_STATE_INVALID:
        _fail("CACHE_REPAIR_REQUIRES_INVALID")
    deleted = 0
    for path in (final, part, metadata):
        if path is not None:
            _owned(path, kind="file")
            path.unlink()
            deleted += 1
    return {"state": CACHE_STATE_MISSING, "deleted": deleted}


def cleanup(strategic_home: str | Path, *, lifecycle: str) -> dict[str, Any]:
    if lifecycle not in {"concept-experiment-complete", "abandoned"}:
        _fail("CACHE_CLEANUP_GATE")
    root = cache_root(strategic_home)
    if not root.exists():
        return {"state": CACHE_STATE_CLEANED, "deleted": 0}
    final, part, metadata = _layout(root)
    deleted = 0
    for path in (final, part, metadata):
        if path is not None:
            _owned(path, kind="file")
            path.unlink()
            deleted += 1
    if any(root.iterdir()):
        _fail("CACHE_CLEANUP_UNEXPECTED_FILE")
    root.rmdir()
    return {"state": CACHE_STATE_CLEANED, "deleted": deleted}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    for name in ("plan", "validate", "promote", "repair", "cleanup"):
        command = sub.add_parser(name)
        command.add_argument("--strategic-home", required=True)
        command.add_argument("--inventory")
        if name == "cleanup":
            command.add_argument("--lifecycle", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        kwargs = {"inventory": args.inventory} if hasattr(args, "inventory") else {}
        if args.operation == "plan":
            result = plan(args.strategic_home, **kwargs)
        elif args.operation == "validate":
            result = inspect(args.strategic_home, **kwargs)
        elif args.operation == "promote":
            result = promote(args.strategic_home, **kwargs)
        elif args.operation == "repair":
            result = repair_invalid(args.strategic_home)
        else:
            result = cleanup(args.strategic_home, lifecycle=args.lifecycle)
        print(json.dumps(result, sort_keys=True))
        return 0
    except CacheError as exc:
        print(json.dumps({"state": CACHE_STATE_INVALID, "error": exc.reason}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
