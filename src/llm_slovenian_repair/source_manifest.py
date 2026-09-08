"""Strict source manifests and bounded synthetic corpus verification.

This module describes provenance for future corpus work without acquiring or
indexing any corpus.  The checked-in fixture used by the contract tests is
project-authored synthetic data; real-source manifests remain an inventory
seam and do not grant data rights.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PureWindowsPath
from typing import Annotated, Any, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    ValidationError,
    field_validator,
    model_validator,
)

from .contracts import EvidenceCompleteness, EvidenceRecord

MANIFEST_SCHEMA_VERSION = 1
RECORD_SCHEMA_VERSION = 1
DEFAULT_MAX_MANIFEST_BYTES = 64 * 1024
DEFAULT_MAX_PAYLOAD_BYTES = 1024 * 1024
DEFAULT_MAX_RECORDS = 1024


class RightsStatus(StrEnum):
    """Finite rights states; a state never substitutes for a rights review."""

    PROJECT_AUTHORED_SYNTHETIC = "PROJECT_AUTHORED_SYNTHETIC"
    VERIFIED_PERMITTED = "VERIFIED_PERMITTED"
    UNKNOWN_UNVERIFIED = "UNKNOWN_UNVERIFIED"
    PROHIBITED_RESTRICTED = "PROHIBITED_RESTRICTED"


class ManifestDenominatorKnowledge(StrEnum):
    """Whether the manifest has an explicit corpus denominator."""

    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"


class QueryKind(StrEnum):
    """The arity of a synthetic count query."""

    WORD = "word"
    BIGRAM = "bigram"
    TRIGRAM = "trigram"


class VerificationFailure(StrEnum):
    """Safe, finite labels exposed by local verification failures."""

    INVALID_LIMIT = "invalid-limit"
    ROOT_INVALID = "fixture-root-invalid"
    MANIFEST_FILE_INVALID = "manifest-file-invalid"
    MANIFEST_TOO_LARGE = "manifest-too-large"
    MANIFEST_UTF8_INVALID = "manifest-utf8-invalid"
    MANIFEST_JSON_INVALID = "manifest-json-invalid"
    MANIFEST_SCHEMA_INVALID = "manifest-schema-invalid"
    PAYLOAD_PATH_INVALID = "payload-path-invalid"
    PAYLOAD_MISSING = "payload-missing"
    PAYLOAD_SYMLINK = "payload-symlink"
    PAYLOAD_NOT_REGULAR = "payload-not-regular"
    PAYLOAD_TOO_LARGE = "payload-too-large"
    PAYLOAD_READ_FAILED = "payload-read-failed"
    PAYLOAD_SIZE_MISMATCH = "payload-size-mismatch"
    PAYLOAD_CHECKSUM_MISMATCH = "payload-checksum-mismatch"
    PAYLOAD_UTF8_INVALID = "payload-utf8-invalid"
    PAYLOAD_JSON_INVALID = "payload-json-invalid"
    PAYLOAD_FORMAT_UNSUPPORTED = "payload-format-unsupported"
    PAYLOAD_RECORD_INVALID = "payload-record-invalid"
    PAYLOAD_DUPLICATE_RECORD = "payload-duplicate-record"


class ManifestVerificationError(ValueError):
    """A bounded local verification failure with no payload echo."""

    def __init__(self, reason: VerificationFailure, field: str | None = None) -> None:
        self.reason = reason.value
        self.field = field
        suffix = f":{field}" if field is not None else ""
        super().__init__(f"{reason.value}{suffix}")

ManifestText = Annotated[StrictStr, Field(min_length=1, max_length=4096)]
ManifestIdentifier = Annotated[StrictStr, Field(min_length=1, max_length=128)]
ManifestNonNegativeInt = Annotated[StrictInt, Field(ge=0)]
Token = Annotated[StrictStr, Field(min_length=1, max_length=128)]
BuildValue = StrictStr | StrictInt | StrictFloat | StrictBool | None

MANIFEST_CONFIG = ConfigDict(
    extra="forbid",
    frozen=True,
    strict=True,
    validate_assignment=True,
    validate_default=True,
    allow_inf_nan=False,
    populate_by_name=True,
)


def _contains_control(value: str) -> bool:
    return any(ord(character) < 32 or 0x7F <= ord(character) <= 0x9F for character in value)


def _metadata_text(value: str | None) -> str | None:
    if value is None:
        return None
    if not value.strip():
        raise ValueError("metadata must be nonblank")
    if _contains_control(value):
        raise ValueError("metadata must not contain control characters")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("metadata must be valid UTF-8") from exc
    return value


def _repository_local_reference(value: str) -> bool:
    lower = value.casefold()
    return lower.startswith(
        (
            "repo://",
            "repository-local:",
            "project-local:",
            "tests/",
            "./tests/",
            "fixtures/",
            "./fixtures/",
        )
    )


class SourceManifest(BaseModel):
    """Immutable, versioned provenance for one bounded payload."""

    model_config = MANIFEST_CONFIG

    schema_version: StrictInt = MANIFEST_SCHEMA_VERSION
    source_id: ManifestIdentifier
    source_name: ManifestText
    release: ManifestText
    acquisition_reference: ManifestText
    payload_path: ManifestText
    sha256: Annotated[StrictStr, Field(pattern=r"[0-9a-f]{64}")]
    byte_size: Annotated[StrictInt, Field(gt=0)]
    media_format: Literal["application/jsonl", "application/json"]
    record_format: Literal["jsonl", "json"]
    encoding: Literal["UTF-8"]
    normalization: ManifestText
    annotation_tagging: ManifestText
    completeness: EvidenceCompleteness
    cutoff_metadata: ManifestText | None = None
    threshold_metadata: ManifestText | None = None
    denominator_knowledge: ManifestDenominatorKnowledge
    denominator: ManifestNonNegativeInt | None = None
    rights_status: RightsStatus
    authorized_use_scope: ManifestText
    license_terms_reference: ManifestText
    attribution_redistribution_conditions: ManifestText
    importer_schema_version: ManifestText
    record_schema_version: StrictInt = RECORD_SCHEMA_VERSION
    deterministic_build_parameters: dict[str, BuildValue] = Field(min_length=1)
    synthetic: StrictBool
    redistribution_ready: StrictBool
    use_ready: StrictBool

    _clean_text = field_validator(
        "source_id",
        "source_name",
        "release",
        "acquisition_reference",
        "payload_path",
        "media_format",
        "record_format",
        "encoding",
        "normalization",
        "annotation_tagging",
        "cutoff_metadata",
        "threshold_metadata",
        "authorized_use_scope",
        "license_terms_reference",
        "attribution_redistribution_conditions",
        "importer_schema_version",
    )(_metadata_text)

    @field_validator("sha256")
    @classmethod
    def validate_lowercase_sha256(cls, value: str) -> str:
        if value != value.lower():
            raise ValueError("sha256 must be lowercase")
        return value

    @field_validator("deterministic_build_parameters")
    @classmethod
    def validate_build_parameters(cls, value: dict[str, BuildValue]) -> dict[str, BuildValue]:
        for key in value:
            if not key.strip() or _contains_control(key):
                raise ValueError("build parameter keys must be nonblank and safe")
        return value

    @model_validator(mode="after")
    def validate_manifest(self) -> Self:
        if self.schema_version != MANIFEST_SCHEMA_VERSION:
            raise ValueError("unsupported manifest schema version")
        if self.record_schema_version != RECORD_SCHEMA_VERSION:
            raise ValueError("unsupported record schema version")
        expected_media_format = {
            "jsonl": "application/jsonl",
            "json": "application/json",
        }[self.record_format]
        if self.media_format != expected_media_format:
            raise ValueError("media_format does not match record_format")
        if self.completeness is EvidenceCompleteness.PARTIAL and not (
            self.cutoff_metadata or self.threshold_metadata
        ):
            raise ValueError("PARTIAL completeness requires cutoff or threshold metadata")
        if self.denominator_knowledge is ManifestDenominatorKnowledge.KNOWN:
            if self.denominator is None:
                raise ValueError("KNOWN denominator knowledge requires denominator")
        elif self.denominator is not None:
            raise ValueError("UNKNOWN denominator knowledge requires null denominator")

        synthetic_rights = RightsStatus.PROJECT_AUTHORED_SYNTHETIC
        closed_rights = {
            RightsStatus.UNKNOWN_UNVERIFIED,
            RightsStatus.PROHIBITED_RESTRICTED,
        }
        if self.rights_status in closed_rights and (
            self.redistribution_ready or self.use_ready
        ):
            raise ValueError("closed rights status requires both readiness flags false")
        if self.synthetic:
            if self.rights_status is not synthetic_rights:
                raise ValueError("synthetic manifest requires project-authored synthetic rights")
            if not _repository_local_reference(self.acquisition_reference):
                raise ValueError("synthetic manifest requires repository-local acquisition")
            attribution = self.attribution_redistribution_conditions.casefold()
            if (
                "project-authored" not in attribution
                or "synthetic" not in attribution
                or "no external corpus" not in attribution
            ):
                raise ValueError("synthetic manifest requires project-authored attribution")
            license_reference = self.license_terms_reference.casefold()
            if "repository" not in license_reference or "license" not in license_reference:
                raise ValueError("synthetic manifest must reference repository LICENSE")
            if self.use_ready and self.authorized_use_scope != "local synthetic tests only":
                raise ValueError("synthetic use_ready scope must be local synthetic tests only")
            if self.importer_schema_version != "NOT_APPLICABLE_SYNTHETIC_FIXTURE":
                raise ValueError("synthetic fixture must not claim an importer")
        elif self.rights_status is synthetic_rights:
            raise ValueError("project-authored synthetic rights require synthetic=True")
        return self

class SyntheticCountRecord(BaseModel):
    """One synthetic word, bigram, or trigram count with explicit evidence."""

    model_config = MANIFEST_CONFIG

    record_id: ManifestIdentifier
    synthetic: StrictBool
    query_kind: QueryKind
    tokens: tuple[Token, ...] = Field(min_length=1, max_length=3)
    evidence: EvidenceRecord

    @field_validator("record_id")
    @classmethod
    def validate_record_id(cls, value: str) -> str:
        return _metadata_text(value) or value

    @field_validator("tokens")
    @classmethod
    def validate_tokens(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        for token in value:
            if not token.strip() or any(character.isspace() for character in token):
                raise ValueError("tokens must be nonblank single-token strings")
            if _contains_control(token):
                raise ValueError("tokens must not contain control characters")
        return value

    @model_validator(mode="after")
    def validate_record(self) -> Self:
        if not self.synthetic:
            raise ValueError("synthetic count records require synthetic=True")
        expected_arity = {
            QueryKind.WORD: 1,
            QueryKind.BIGRAM: 2,
            QueryKind.TRIGRAM: 3,
        }[self.query_kind]
        if len(self.tokens) != expected_arity:
            raise ValueError("query kind and token arity do not match")
        if "synthetic" not in self.evidence.source.casefold():
            raise ValueError("record evidence source must be synthetic")
        if "synthetic" not in self.evidence.scope.casefold():
            raise ValueError("record evidence scope must be synthetic")
        return self

class SyntheticCorpus(BaseModel):
    """Bounded ordered records decoded from a checked payload."""

    model_config = MANIFEST_CONFIG

    records: tuple[SyntheticCountRecord, ...] = Field(
        min_length=1,
        max_length=DEFAULT_MAX_RECORDS,
    )

    @model_validator(mode="after")
    def validate_record_ids(self) -> Self:
        ids = [record.record_id for record in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError("record_id values must be unique")
        return self

@dataclass(frozen=True, slots=True)
class VerifiedSyntheticCorpus:
    """Typed result of verifying one manifest and its exact local payload."""

    manifest: SourceManifest
    records: tuple[SyntheticCountRecord, ...]
    payload_bytes: bytes

    @property
    def payload_size(self) -> int:
        return len(self.payload_bytes)

    @property
    def payload_sha256(self) -> str:
        return hashlib.sha256(self.payload_bytes).hexdigest()

def _validate_limit(value: int, reason: VerificationFailure) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ManifestVerificationError(reason)
    return value


def _lstat(path: Path, reason: VerificationFailure) -> os.stat_result:
    try:
        result = path.lstat()
    except (OSError, ValueError) as exc:
        raise ManifestVerificationError(reason) from exc
    return result


def _regular_file(path: Path, *, missing: VerificationFailure) -> None:
    result = _lstat(path, missing)
    if stat.S_ISLNK(result.st_mode):
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_SYMLINK)
    if not stat.S_ISREG(result.st_mode):
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_NOT_REGULAR)


def _read_bounded(path: Path, limit: int, *, too_large: VerificationFailure) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except (OSError, ValueError) as exc:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_READ_FAILED) from exc
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise ManifestVerificationError(VerificationFailure.PAYLOAD_NOT_REGULAR)
        if info.st_size > limit:
            raise ManifestVerificationError(too_large)
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(64 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > limit:
            raise ManifestVerificationError(too_large)
        if len(data) != info.st_size:
            raise ManifestVerificationError(VerificationFailure.PAYLOAD_READ_FAILED)
        return data
    except ManifestVerificationError:
        raise
    except OSError as exc:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_READ_FAILED) from exc
    finally:
        os.close(descriptor)


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _parse_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )


def _safe_relative_parts(value: str) -> tuple[str, ...]:
    if not value or value in {".", ".."}:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_PATH_INVALID)
    if _contains_control(value) or "\\" in value:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_PATH_INVALID)
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_PATH_INVALID) from exc
    windows_path = PureWindowsPath(value)
    if value.startswith("/") or windows_path.is_absolute() or windows_path.drive:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_PATH_INVALID)
    parts = tuple(value.split("/"))
    if any(part in {"", ".", ".."} for part in parts):
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_PATH_INVALID)
    return parts


def _payload_path(root: Path, relative_path: str) -> Path:
    parts = _safe_relative_parts(relative_path)
    try:
        root_info = root.lstat()
    except (OSError, ValueError) as exc:
        raise ManifestVerificationError(VerificationFailure.ROOT_INVALID) from exc
    if stat.S_ISLNK(root_info.st_mode) or not stat.S_ISDIR(root_info.st_mode):
        raise ManifestVerificationError(VerificationFailure.ROOT_INVALID)

    current = root
    for part in parts:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError as exc:
            raise ManifestVerificationError(VerificationFailure.PAYLOAD_MISSING) from exc
        except (OSError, ValueError) as exc:
            raise ManifestVerificationError(VerificationFailure.PAYLOAD_PATH_INVALID) from exc
        if stat.S_ISLNK(info.st_mode):
            raise ManifestVerificationError(VerificationFailure.PAYLOAD_SYMLINK)
    try:
        current.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_PATH_INVALID) from exc
    return current


def _manifest_from_bytes(data: bytes) -> SourceManifest:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ManifestVerificationError(VerificationFailure.MANIFEST_UTF8_INVALID) from exc
    try:
        parsed = _parse_json(text)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ManifestVerificationError(VerificationFailure.MANIFEST_JSON_INVALID) from exc
    if not isinstance(parsed, dict):
        raise ManifestVerificationError(VerificationFailure.MANIFEST_SCHEMA_INVALID)
    try:
        # JSON validation is deliberately used after the duplicate-key pass:
        # Pydantic's strict JSON mode parses enum literals while strict Python
        # validation correctly requires enum objects from typed callers.
        return SourceManifest.model_validate_json(data)
    except ValidationError as exc:
        raise ManifestVerificationError(VerificationFailure.MANIFEST_SCHEMA_INVALID) from exc


def _parse_records(
    payload_text: str, record_format: str, max_records: int
) -> tuple[SyntheticCountRecord, ...]:
    raw_records: list[Any]
    try:
        if record_format == "jsonl":
            lines = payload_text.splitlines()
            if not lines or any(not line.strip() for line in lines):
                raise ValueError("blank JSONL line")
            raw_records = [_parse_json(line) for line in lines]
        elif record_format == "json":
            parsed = _parse_json(payload_text)
            if not isinstance(parsed, list):
                raise ValueError("JSON payload must be an array")
            raw_records = parsed
        else:
            raise ManifestVerificationError(VerificationFailure.PAYLOAD_FORMAT_UNSUPPORTED)
    except ManifestVerificationError:
        raise
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_JSON_INVALID) from exc
    if len(raw_records) == 0 or len(raw_records) > max_records:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_RECORD_INVALID)
    records: list[SyntheticCountRecord] = []
    try:
        for item in raw_records:
            if not isinstance(item, dict):
                raise ValueError("record must be an object")
            record_json = json.dumps(item, ensure_ascii=False, separators=(",", ":"))
            records.append(SyntheticCountRecord.model_validate_json(record_json))
        ids = [record.record_id for record in records]
        if len(ids) != len(set(ids)):
            raise ManifestVerificationError(VerificationFailure.PAYLOAD_DUPLICATE_RECORD)
        return tuple(records)
    except ManifestVerificationError:
        raise
    except (TypeError, ValueError, ValidationError) as exc:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_RECORD_INVALID) from exc


def verify_manifest_payload(
    manifest_path: str | os.PathLike[str],
    *,
    fixture_root: str | os.PathLike[str] | None = None,
    max_manifest_bytes: int = DEFAULT_MAX_MANIFEST_BYTES,
    max_payload_bytes: int = DEFAULT_MAX_PAYLOAD_BYTES,
    max_records: int = DEFAULT_MAX_RECORDS,
) -> VerifiedSyntheticCorpus:
    """Verify and parse one local manifest/payload pair without writing or networking."""

    _validate_limit(max_manifest_bytes, VerificationFailure.INVALID_LIMIT)
    _validate_limit(max_payload_bytes, VerificationFailure.INVALID_LIMIT)
    _validate_limit(max_records, VerificationFailure.INVALID_LIMIT)
    manifest_file = Path(manifest_path)
    root = Path(fixture_root) if fixture_root is not None else manifest_file.parent
    try:
        root = root.resolve(strict=True)
    except (OSError, ValueError) as exc:
        raise ManifestVerificationError(VerificationFailure.ROOT_INVALID) from exc
    _regular_file(manifest_file, missing=VerificationFailure.MANIFEST_FILE_INVALID)
    manifest_bytes = _read_bounded(
        manifest_file,
        max_manifest_bytes,
        too_large=VerificationFailure.MANIFEST_TOO_LARGE,
    )
    manifest = _manifest_from_bytes(manifest_bytes)
    if not manifest.synthetic:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_RECORD_INVALID)
    if manifest.byte_size > max_payload_bytes:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_TOO_LARGE)
    payload_file = _payload_path(root, manifest.payload_path)
    _regular_file(payload_file, missing=VerificationFailure.PAYLOAD_MISSING)
    payload_bytes = _read_bounded(
        payload_file,
        max_payload_bytes,
        too_large=VerificationFailure.PAYLOAD_TOO_LARGE,
    )
    if len(payload_bytes) != manifest.byte_size:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_SIZE_MISMATCH)
    if hashlib.sha256(payload_bytes).hexdigest() != manifest.sha256:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_CHECKSUM_MISMATCH)
    try:
        payload_text = payload_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ManifestVerificationError(VerificationFailure.PAYLOAD_UTF8_INVALID) from exc
    records = _parse_records(payload_text, manifest.record_format, max_records)
    return VerifiedSyntheticCorpus(
        manifest=manifest,
        records=records,
        payload_bytes=payload_bytes,
    )


__all__ = [
    "DEFAULT_MAX_MANIFEST_BYTES",
    "DEFAULT_MAX_PAYLOAD_BYTES",
    "DEFAULT_MAX_RECORDS",
    "ManifestDenominatorKnowledge",
    "ManifestVerificationError",
    "QueryKind",
    "RightsStatus",
    "SourceManifest",
    "SyntheticCorpus",
    "SyntheticCountRecord",
    "VerifiedSyntheticCorpus",
    "VerificationFailure",
    "verify_manifest_payload",
]
