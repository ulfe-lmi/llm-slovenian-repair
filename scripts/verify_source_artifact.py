"""Validate the checked-in source inventory and inspect one local ZIP artifact.

This is deliberately a standard-library-only, offline boundary.  It treats the
inventory as metadata, never follows its URLs, and inspects ZIP members without
extracting or writing them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import zipfile
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path, PureWindowsPath
from typing import Any, NoReturn
from urllib.parse import urlparse

INVENTORY_SCHEMA_VERSION = 1
CANONICAL_SNAPSHOT_AT = "2026-09-08T09:13:23Z"
MAX_INVENTORY_BYTES = 256 * 1024
MAX_ARTIFACT_BYTES = 512 * 1024 * 1024
ALLOWED_SOURCE_IDS = frozenset(
    {
        "gigafida-2.0-words",
        "gigafida-2.0-word-ngrams",
        "sloleks-3.1",
        "gigafida-2.2-query-interface",
    }
)
ALLOWED_HOSTS = frozenset(
    {"www.clarin.si", "clarin.si", "viri.cjvt.si", "creativecommons.org"}
)
DOWNLOADABLE_SOURCE_IDS = frozenset(ALLOWED_SOURCE_IDS - {"gigafida-2.2-query-interface"})

_TOP_LEVEL_KEYS = frozenset(
    {"schema_version", "inventory_id", "snapshot_at", "project", "entries"}
)
_PROJECT_KEYS = frozenset({"code_license", "external_data_note"})
_ENTRY_KEYS = frozenset(
    {
        "id",
        "kind",
        "source_name",
        "release",
        "issued_date",
        "item_url",
        "publishers",
        "observed_at",
        "publisher_access_label",
        "license",
        "artifact",
        "source_scope",
        "completeness",
        "cutoff",
        "absence_semantics",
        "denominator_status",
        "normalization_tagging",
        "downstream_objective",
        "selection_status",
        "acquisition_state",
        "bulk_access_status",
        "redistribution_status",
        "acquisition_ready",
        "fallback",
    }
)
_LICENSE_KEYS = frozenset({"name", "uri"})
_ARTIFACT_KEYS = frozenset(
    {
        "url",
        "name",
        "media_type",
        "byte_size",
        "repository_checksum",
        "container_format",
        "member_format",
        "project_sha256",
    }
)
_CHECKSUM_KEYS = frozenset({"algorithm", "value"})
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MD5 = re.compile(r"^[0-9a-f]{32}$")

_CANONICAL_ENTRY_ORDER = (
    "gigafida-2.0-words",
    "gigafida-2.0-word-ngrams",
    "sloleks-3.1",
    "gigafida-2.2-query-interface",
)
_CANONICAL_PROJECT_SHA256 = (
    "ded7c28548d3acc08df593039c51c8eb4bc3455a991ef6b9cd1f607e890e787d"
)
_CANONICAL_ENTRY_SHA256 = {
    "gigafida-2.0-words": "46a63ab2d00114ca4acb5d72a90d8a481076a15a93471d33aa47a64c3bdacfbc",
    "gigafida-2.0-word-ngrams": "addf6b6084c93bf7898a99ac9de8fa321a2312b82a31240df813113d111a8924",
    "sloleks-3.1": "05d0e672881c2b50bdb80bb2197f16408fc9d26753dc26d898844d03fc3a4112",
    "gigafida-2.2-query-interface": (
        "890003b281e79fd1fd8a4cc65d1a5aeb0c6e0d91bc0087b4263d24c160a216f7"
    ),
}


class InventoryError(ValueError):
    """A finite, non-sensitive inventory validation failure."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class ArtifactVerificationError(ValueError):
    """A finite, non-sensitive local artifact verification failure."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True, slots=True)
class ArtifactVerification:
    """Safe summary emitted after a local ZIP has been inspected."""

    source_id: str
    byte_size: int
    md5: str
    sha256: str
    member_count: int
    total_uncompressed_size: int


@dataclass(frozen=True, slots=True)
class ZipLimits:
    max_members: int
    max_member_uncompressed_size: int
    max_total_uncompressed_size: int
    max_compression_ratio: float


_ZIP_LIMITS: dict[str, ZipLimits] = {
    "gigafida-2.0-words": ZipLimits(100_000, 1_000_000_000, 8_000_000_000, 1_000.0),
    "gigafida-2.0-word-ngrams": ZipLimits(50_000, 1_000_000_000, 4_000_000_000, 1_000.0),
    "sloleks-3.1": ZipLimits(10_000, 2_000_000_000, 8_000_000_000, 1_000.0),
}


def _fail(reason: str) -> NoReturn:
    raise InventoryError(reason)


def _artifact_fail(reason: str) -> NoReturn:
    raise ArtifactVerificationError(reason)


def _keys(value: Any, expected: frozenset[str], reason: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        _fail(reason)


def _string(value: Any, field: str, *, max_length: int = 4096) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or len(value) > max_length
    ):
        _fail(f"invalid-{field}")
    if any(ord(character) < 32 or 0x7F <= ord(character) <= 0x9F for character in value):
        _fail(f"unsafe-{field}")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _fail(f"invalid-{field}")
    return value


def _nullable_string(value: Any, field: str, *, max_length: int = 4096) -> str | None:
    if value is None:
        return None
    return _string(value, field, max_length=max_length)


def _strict_int(value: Any, field: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        _fail(f"invalid-{field}")
    return value


def _strict_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        _fail(f"invalid-{field}")
    return value


def _strict_list(value: Any, field: str, *, minimum: int = 1, maximum: int = 32) -> list[Any]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        _fail(f"invalid-{field}")
    return value


def _validate_timestamp(value: Any, field: str) -> datetime:
    text = _string(value, field, max_length=32)
    if not text.endswith("Z"):
        _fail(f"invalid-{field}")
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError:
        _fail(f"invalid-{field}")
    if parsed.tzinfo != UTC or parsed.microsecond:
        _fail(f"invalid-{field}")
    return parsed


def _validate_date(value: Any, field: str) -> date:
    text = _string(value, field, max_length=10)
    if not _ISO_DATE.fullmatch(text):
        _fail(f"invalid-{field}")
    try:
        return date.fromisoformat(text)
    except ValueError:
        _fail(f"invalid-{field}")


def _validate_url(value: Any, field: str, *, hosts: frozenset[str] = ALLOWED_HOSTS) -> str:
    text = _string(value, field, max_length=2048)
    parsed = urlparse(text)
    if (
        parsed.scheme != "https"
        or parsed.hostname is None
        or parsed.hostname.casefold() not in hosts
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or not parsed.netloc
    ):
        _fail(f"invalid-{field}")
    return text


def _validate_filename(value: Any, field: str) -> str:
    text = _string(value, field, max_length=255)
    windows = PureWindowsPath(text)
    if (
        text in {".", ".."}
        or "/" in text
        or "\\" in text
        or windows.is_absolute()
        or bool(windows.drive)
        or text.endswith(".")
    ):
        _fail(f"unsafe-{field}")
    return text


def _validate_license(value: Any, kind: str) -> None:
    _keys(value, _LICENSE_KEYS, "invalid-license")
    assert isinstance(value, dict)
    _string(value["name"], "license-name", max_length=256)
    uri = value["uri"]
    if kind == "downloadable":
        _validate_url(uri, "license-uri", hosts=frozenset({"creativecommons.org"}))
    elif uri is not None:
        _validate_url(uri, "license-uri")


def _validate_checksum(value: Any) -> None:
    _keys(value, _CHECKSUM_KEYS, "invalid-repository-checksum")
    assert isinstance(value, dict)
    if value["algorithm"] != "MD5" or not isinstance(value["value"], str):
        _fail("invalid-repository-checksum")
    if not _MD5.fullmatch(value["value"]):
        _fail("invalid-repository-checksum")


def _validate_artifact(value: Any) -> None:
    _keys(value, _ARTIFACT_KEYS, "invalid-artifact")
    assert isinstance(value, dict)
    _validate_url(value["url"], "artifact-url", hosts=frozenset({"www.clarin.si", "clarin.si"}))
    _validate_filename(value["name"], "artifact-name")
    if value["media_type"] != "application/zip":
        _fail("invalid-artifact-media-type")
    size = _strict_int(value["byte_size"], "artifact-byte-size", minimum=1)
    if size > MAX_ARTIFACT_BYTES:
        _fail("artifact-byte-size-too-large")
    _validate_checksum(value["repository_checksum"])
    if value["container_format"] != "ZIP" or not isinstance(value["member_format"], str):
        _fail("invalid-artifact-format")
    _string(value["member_format"], "member-format", max_length=128)
    project_sha256 = value["project_sha256"]
    if project_sha256 is not None and (
        not isinstance(project_sha256, str) or not _SHA256.fullmatch(project_sha256)
    ):
        _fail("invalid-project-sha256")
    if project_sha256 is not None:
        _fail("project-sha256-must-be-null-before-fetch")


def _validate_entry(value: Any, snapshot: datetime) -> dict[str, Any]:
    _keys(value, _ENTRY_KEYS, "invalid-entry")
    assert isinstance(value, dict)
    source_id = _string(value["id"], "source-id", max_length=128)
    if source_id not in ALLOWED_SOURCE_IDS:
        _fail("unknown-source-id")
    kind = value["kind"]
    if kind not in {"downloadable", "query_interface"}:
        _fail("invalid-entry-kind")
    if (source_id in DOWNLOADABLE_SOURCE_IDS) != (kind == "downloadable"):
        _fail("source-kind-mismatch")
    _string(value["source_name"], "source-name")
    _string(value["release"], "release", max_length=128)
    issued = _validate_date(value["issued_date"], "issued-date")
    item_host = "www.clarin.si" if kind == "downloadable" else "viri.cjvt.si"
    _validate_url(value["item_url"], "item-url", hosts=frozenset({item_host}))
    publishers = _strict_list(value["publishers"], "publishers", maximum=8)
    publisher_values = [_string(item, "publisher", max_length=256) for item in publishers]
    if len(set(publisher_values)) != len(publisher_values):
        _fail("duplicate-publisher")
    observed = _validate_timestamp(value["observed_at"], "observed-at")
    if issued > observed.date():
        _fail("issued-date-after-observation")
    if observed > snapshot:
        _fail("observation-after-snapshot")
    if observed != snapshot:
        _fail("observation-does-not-match-snapshot")
    _string(value["publisher_access_label"], "publisher-access-label")
    _validate_license(value["license"], kind)
    artifact = value["artifact"]
    if kind == "downloadable":
        if not isinstance(artifact, dict):
            _fail("downloadable-artifact-required")
        _validate_artifact(artifact)
    elif artifact is not None:
        _fail("query-artifact-forbidden")
    _string(value["source_scope"], "source-scope")
    completeness = value["completeness"]
    if completeness not in {"DECLARED_RELEASE_SCOPE", "CENSORED", "UNAVAILABLE"}:
        _fail("invalid-completeness")
    cutoff = _nullable_string(value["cutoff"], "cutoff")
    if completeness in {"DECLARED_RELEASE_SCOPE", "CENSORED"} and cutoff is None:
        _fail("cutoff-required")
    if completeness == "UNAVAILABLE" and cutoff is not None:
        _fail("unavailable-cutoff-forbidden")
    absence_semantics = value["absence_semantics"]
    if absence_semantics not in {
        "EXACT_WITHIN_DECLARED_SCOPE",
        "CENSORED_NOT_ZERO",
        "UNAVAILABLE",
    }:
        _fail("invalid-absence-semantics")
    denominator_status = value["denominator_status"]
    if denominator_status not in {"DECLARED_SCOPE_ONLY", "UNKNOWN"}:
        _fail("invalid-denominator-status")
    if source_id == "gigafida-2.0-word-ngrams":
        if completeness != "CENSORED" or absence_semantics != "CENSORED_NOT_ZERO":
            _fail("ngram-cutoff-zero-contradiction")
        if denominator_status != "UNKNOWN":
            _fail("ngram-denominator-contradiction")
    elif kind == "query_interface":
        if absence_semantics != "UNAVAILABLE" or denominator_status != "UNKNOWN":
            _fail("query-evidence-contradiction")
    elif absence_semantics != "EXACT_WITHIN_DECLARED_SCOPE":
        _fail("declared-scope-evidence-contradiction")
    _string(value["normalization_tagging"], "normalization-tagging")
    _string(value["downstream_objective"], "downstream-objective", max_length=64)
    _string(value["selection_status"], "selection-status", max_length=128)
    acquisition_state = value["acquisition_state"]
    _string(acquisition_state, "acquisition-state", max_length=64)
    _string(value["bulk_access_status"], "bulk-access-status", max_length=64)
    _string(value["redistribution_status"], "redistribution-status", max_length=64)
    acquisition_ready = _strict_bool(value["acquisition_ready"], "acquisition-ready")
    fallback = _strict_bool(value["fallback"], "fallback")

    if kind == "downloadable":
        if acquisition_state != "NOT_ACQUIRED" or acquisition_ready or fallback:
            _fail("downloadable-readiness-contradiction")
        if value["bulk_access_status"] != "PUBLISHED_DERIVED_ARCHIVE":
            _fail("downloadable-access-status-invalid")
        if value["redistribution_status"] != "SEPARATE_REVIEW_REQUIRED":
            _fail("downloadable-redistribution-status-invalid")
    else:
        if (
            acquisition_state != "QUERY_ONLY_UNVERIFIED"
            or value["bulk_access_status"] != "UNKNOWN_UNVERIFIED"
            or value["redistribution_status"] != "UNKNOWN_UNVERIFIED"
            or acquisition_ready
            or fallback
            or completeness != "UNAVAILABLE"
        ):
            _fail("query-readiness-contradiction")
    return value


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, item in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = item
    return result


def _load_json_bytes(data: bytes) -> Any:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InventoryError("inventory-utf8-invalid") from exc
    if text.startswith("\ufeff"):
        raise InventoryError("inventory-utf8-invalid")
    try:
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise InventoryError("inventory-json-invalid") from exc


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_regular(path: Path, *, missing_reason: str, max_bytes: int) -> bytes:
    try:
        info = path.lstat()
    except (OSError, ValueError) as exc:
        raise InventoryError(missing_reason) from exc
    if stat.S_ISLNK(info.st_mode):
        raise InventoryError("path-symlink")
    if not stat.S_ISREG(info.st_mode):
        raise InventoryError("path-not-regular")
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise InventoryError("path-open-failed") from exc
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise InventoryError("path-not-regular")
        if opened.st_size > max_bytes:
            raise InventoryError("inventory-too-large")
        chunks: list[bytes] = []
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(descriptor, min(64 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > max_bytes:
            raise InventoryError("inventory-too-large")
        if len(data) != opened.st_size:
            raise InventoryError("path-read-failed")
        return data
    except InventoryError:
        raise
    except OSError as exc:
        raise InventoryError("path-read-failed") from exc
    finally:
        os.close(descriptor)


def validate_inventory(value: Any) -> dict[str, Any]:
    """Validate and return one strict source inventory without network access."""

    _keys(value, _TOP_LEVEL_KEYS, "invalid-inventory")
    assert isinstance(value, dict)
    if value["schema_version"] != INVENTORY_SCHEMA_VERSION or isinstance(
        value["schema_version"], bool
    ):
        _fail("unsupported-inventory-schema")
    inventory_id = _string(value["inventory_id"], "inventory-id", max_length=128)
    if inventory_id != "source-inventory-v1":
        _fail("invalid-inventory-id")
    snapshot = _validate_timestamp(value["snapshot_at"], "snapshot-at")
    if value["snapshot_at"] != CANONICAL_SNAPSHOT_AT:
        _fail("canonical-snapshot-mismatch")
    project = value["project"]
    _keys(project, _PROJECT_KEYS, "invalid-project-metadata")
    assert isinstance(project, dict)
    if project["code_license"] != "Apache-2.0":
        _fail("invalid-code-license")
    _string(project["external_data_note"], "external-data-note")
    entries = _strict_list(value["entries"], "entries", minimum=4, maximum=4)
    validated = [_validate_entry(entry, snapshot) for entry in entries]
    ids = [entry["id"] for entry in validated]
    if tuple(ids) != _CANONICAL_ENTRY_ORDER:
        _fail("inventory-entry-set-invalid")
    if _canonical_digest(project) != _CANONICAL_PROJECT_SHA256:
        _fail("canonical-project-mismatch")
    for entry in validated:
        if _canonical_digest(entry) != _CANONICAL_ENTRY_SHA256[entry["id"]]:
            _fail(f"canonical-entry-mismatch-{entry['id']}")
    return value


def load_inventory(path: Path) -> dict[str, Any]:
    """Read and validate one regular inventory file, never following URLs."""

    data = _read_regular(
        path, missing_reason="inventory-file-invalid", max_bytes=MAX_INVENTORY_BYTES
    )
    return validate_inventory(_load_json_bytes(data))


def _safe_member_name(name: str) -> bool:
    windows = PureWindowsPath(name)
    if (
        not name
        or name in {".", ".."}
        or name.startswith(("/", "\\"))
        or "\\" in name
        or windows.is_absolute()
        or windows.drive
        or any(ord(character) < 32 or 0x7F <= ord(character) <= 0x9F for character in name)
    ):
        return False
    path_name = name[:-1] if name.endswith("/") else name
    if not path_name:
        return False
    parts = path_name.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def _hash_file(descriptor: int, expected_size: int, expected_md5: str) -> tuple[str, str, int]:
    md5 = hashlib.md5(usedforsecurity=False)
    sha256 = hashlib.sha256()
    total = 0
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > MAX_ARTIFACT_BYTES:
            _artifact_fail("artifact-too-large")
        md5.update(chunk)
        sha256.update(chunk)
    if total != expected_size:
        _artifact_fail("artifact-size-mismatch")
    actual_md5 = md5.hexdigest()
    if actual_md5 != expected_md5:
        _artifact_fail("artifact-md5-mismatch")
    return actual_md5, sha256.hexdigest(), total


def _entry_for_id(inventory: dict[str, Any], source_id: str) -> dict[str, Any]:
    if not isinstance(source_id, str) or source_id not in DOWNLOADABLE_SOURCE_IDS:
        _artifact_fail("source-id-not-downloadable")
    for entry in inventory["entries"]:
        if isinstance(entry, dict) and entry.get("id") == source_id:
            return entry
    _artifact_fail("source-id-not-found")


def _verify_artifact_entry(
    entry: dict[str, Any], source_id: str, artifact_path: Path
) -> ArtifactVerification:
    """Verify a local ZIP against one already selected metadata entry.

    This lower seam exists for synthetic ZIP fixtures only.  The public function
    and CLI always load the canonical, ID-bound inventory before reaching it.
    """

    if source_id not in DOWNLOADABLE_SOURCE_IDS or entry.get("id") != source_id:
        _artifact_fail("source-id-not-downloadable")
    artifact = entry["artifact"]
    if not isinstance(artifact, dict):
        _artifact_fail("downloadable-artifact-required")
    expected_size = artifact["byte_size"]
    checksum = artifact["repository_checksum"]
    if not isinstance(expected_size, int) or isinstance(expected_size, bool) or not isinstance(
        checksum, dict
    ):
        _artifact_fail("inventory-artifact-invalid")
    expected_md5 = checksum.get("value")
    if not isinstance(expected_md5, str):
        _artifact_fail("inventory-checksum-invalid")
    try:
        info = artifact_path.lstat()
    except (OSError, ValueError) as exc:
        raise ArtifactVerificationError("artifact-file-invalid") from exc
    if stat.S_ISLNK(info.st_mode):
        _artifact_fail("artifact-symlink")
    if not stat.S_ISREG(info.st_mode):
        _artifact_fail("artifact-not-regular")
    try:
        descriptor = os.open(artifact_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise ArtifactVerificationError("artifact-open-failed") from exc
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            _artifact_fail("artifact-not-regular")
        if opened.st_size > MAX_ARTIFACT_BYTES:
            _artifact_fail("artifact-too-large")
        actual_md5, sha256, total = _hash_file(descriptor, expected_size, expected_md5)
        os.lseek(descriptor, 0, os.SEEK_SET)
        try:
            with os.fdopen(descriptor, "rb", closefd=False) as stream, zipfile.ZipFile(
                stream
            ) as archive:
                    limits = _ZIP_LIMITS[source_id]
                    infos = archive.infolist()
                    if not infos or len(infos) > limits.max_members:
                        _artifact_fail("zip-member-count-limit")
                    names: set[str] = set()
                    total_uncompressed = 0
                    for info in infos:
                        if not _safe_member_name(info.filename):
                            _artifact_fail("zip-unsafe-member-name")
                        if info.filename in names:
                            _artifact_fail("zip-duplicate-member")
                        names.add(info.filename)
                        mode = (info.external_attr >> 16) & 0o170000
                        if mode == stat.S_IFLNK:
                            _artifact_fail("zip-symlink-member")
                        if info.is_dir() or (mode and mode != stat.S_IFREG):
                            _artifact_fail("zip-nonregular-member")
                        if info.flag_bits & 0x1:
                            _artifact_fail("zip-encrypted-member")
                        if info.file_size > limits.max_member_uncompressed_size:
                            _artifact_fail("zip-member-size-limit")
                        compressed_size = max(info.compress_size, 1)
                        if info.file_size / compressed_size > limits.max_compression_ratio:
                            _artifact_fail("zip-compression-ratio-limit")
                        total_uncompressed += info.file_size
                        if total_uncompressed > limits.max_total_uncompressed_size:
                            _artifact_fail("zip-total-size-limit")
        except zipfile.BadZipFile as exc:
            raise ArtifactVerificationError("zip-invalid") from exc
        return ArtifactVerification(
            source_id=source_id,
            byte_size=total,
            md5=actual_md5,
            sha256=sha256,
            member_count=len(infos),
            total_uncompressed_size=total_uncompressed,
        )
    except ArtifactVerificationError:
        raise
    except OSError as exc:
        raise ArtifactVerificationError("artifact-read-failed") from exc
    finally:
        os.close(descriptor)


def verify_artifact(
    inventory_path: Path, source_id: str, artifact_path: Path
) -> ArtifactVerification:
    """Verify one explicit local ZIP against the canonical inventory."""

    inventory = load_inventory(inventory_path)
    entry = _entry_for_id(inventory, source_id)
    return _verify_artifact_entry(entry, source_id, artifact_path)


def _result_json(result: ArtifactVerification) -> str:
    return json.dumps(
        {
            "source_id": result.source_id,
            "byte_size": result.byte_size,
            "md5": result.md5,
            "sha256": result.sha256,
            "member_count": result.member_count,
            "total_uncompressed_size": result.total_uncompressed_size,
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--source-id")
    parser.add_argument("--artifact", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.validate_only:
            inventory = load_inventory(args.inventory)
            print(
                json.dumps(
                    {
                        "inventory_id": inventory["inventory_id"],
                        "schema_version": inventory["schema_version"],
                        "entry_count": len(inventory["entries"]),
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                )
            )
            return 0
        if args.source_id is None or args.artifact is None:
            print("ERROR source-id-and-artifact-required", file=sys.stderr)
            return 2
        print(_result_json(verify_artifact(args.inventory, args.source_id, args.artifact)))
        return 0
    except (InventoryError, ArtifactVerificationError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
