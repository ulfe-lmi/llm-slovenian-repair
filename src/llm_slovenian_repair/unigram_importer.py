"""Bounded, deterministic import of the observed Gigafida 2.0 unigram TSV.

The importer is deliberately a parser boundary, not a downloader or a lookup
index.  Callers provide a binary or text stream and explicit provenance.  The
source fields are retained exactly; the lookup value is an explicitly derived
NFC/case-folded view and never replaces the source value.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Iterator
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Any, BinaryIO, Protocol, Self, TextIO, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    StrictStr,
    field_validator,
    model_validator,
)

from .contracts import EvidenceCompleteness

IMPORTER_VERSION = "unigram-importer-v1"
SCHEMA_VERSION = 1
REAL_SOURCE_ID = "gigafida-2.0-words"
REAL_SOURCE_NAME = "Gigafida 2.0 word lists"
REAL_RELEASE = "2.0"
REAL_INVENTORY_REVISION = "source-inventory-v1"
REAL_INVENTORY_SHA256 = "439bbd51e04e338569b9785c44d1b05c0ea023aae39898aa7d494568d6f49de3"
REAL_ACQUISITION_SHA256 = "77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a"
SYNTHETIC_SOURCE_ID = "project-synthetic-unigram"
SYNTHETIC_SOURCE_NAME = "Project-authored synthetic fixture"
SYNTHETIC_RELEASE = "fixture-v1"
SYNTHETIC_INVENTORY_REVISION = "project-synthetic-v1"
EXPECTED_MEMBER_NAME = (
    "GF2.0-words-all-lowercase_forms-lemmas-parts_of_speech-taxonomy-entire.tsv"
)
EXPECTED_DELIMITER = "\t"
EXPECTED_ENCODING = "UTF-8"
EXPECTED_NEWLINE = "CRLF"
EXPECTED_DATA_RECORD_TERMINATOR = "TAB_BEFORE_CRLF"
EXPECTED_HEADER_LINE_NUMBER = 15
EXPECTED_HEADER: tuple[str, ...] = (
    "Oblika z malimi črkami",
    "Lema",
    "Lema (male črke)",
    "Besedna vrsta",
    "Skupna absolutna pogostost oblike z malimi črkami",
    "Delež glede na vse najdene oblike z malimi črkami",
    "Skupna relativna pogostost (na milijon pojavitev)",
    "Absolutna pogostost [SSJ.T.K.N]",
    "Delež [SSJ.T.K.N]",
    "Relativna pogostost [SSJ.T.K.N]",
    "Absolutna pogostost [SSJ.T.K.L]",
    "Delež [SSJ.T.K.L]",
    "Relativna pogostost [SSJ.T.K.L]",
    "Absolutna pogostost [SSJ.T.D]",
    "Delež [SSJ.T.D]",
    "Relativna pogostost [SSJ.T.D]",
    "Absolutna pogostost [SSJ.T.P.C]",
    "Delež [SSJ.T.P.C]",
    "Relativna pogostost [SSJ.T.P.C]",
    "Absolutna pogostost [SSJ.T.P.R]",
    "Delež [SSJ.T.P.R]",
    "Relativna pogostost [SSJ.T.P.R]",
    "Absolutna pogostost [SSJ.I]",
    "Delež [SSJ.I]",
    "Relativna pogostost [SSJ.I]",
    "Absolutna pogostost [SSJ.T.K.S]",
    "Delež [SSJ.T.K.S]",
    "Relativna pogostost [SSJ.T.K.S]",
)
EXPECTED_HEADER_BYTES = b'"' + b'"\t"'.join(
    header.encode("utf-8") for header in EXPECTED_HEADER
) + b'"\r\n'
EXPECTED_HEADER_SHA256 = hashlib.sha256(EXPECTED_HEADER_BYTES).hexdigest()
EXPECTED_HEADER_BYTE_LENGTH = len(EXPECTED_HEADER_BYTES)
EXPECTED_HEADER_SHA256_FROM_HANDOFF = (
    "c2ce44548818b72a04691c7060c0e35106393edbfde13336c60d4cd072a00638"
)
if EXPECTED_HEADER_SHA256 != EXPECTED_HEADER_SHA256_FROM_HANDOFF:
    raise AssertionError("observed header contract is internally inconsistent")

_ABSOLUTE_INDICES = (4, 7, 10, 13, 16, 19, 22, 25)
_DECIMAL_INDICES = tuple(
    index for index in range(4, len(EXPECTED_HEADER)) if index not in _ABSOLUTE_INDICES
)
_COUNT_RE = re.compile(r"[0-9]+")
_DECIMAL_RE = re.compile(r"(?:0|[0-9]+)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
_MAX_COUNT = (1 << 63) - 1
_CHUNK_SIZE = 8192
_RECORD_KEY_SEPARATOR = "\u241f"


class UnigramImportFailure(StrEnum):
    """Finite, non-content failure labels returned by the parser boundary."""

    INVALID_LIMIT = "invalid-limit"
    INPUT_TOO_LARGE = "input-too-large"
    INPUT_READ_FAILED = "input-read-failed"
    MISSING_FINAL_NEWLINE = "missing-final-newline"
    INVALID_NEWLINE = "invalid-newline"
    INVALID_UTF8 = "invalid-utf8"
    INVALID_SOURCE_TEXT = "invalid-source-text"
    LINE_TOO_LARGE = "line-too-large"
    FIELD_TOO_LARGE = "field-too-large"
    FIELD_COUNT = "field-count"
    INVALID_QUOTING = "invalid-quoting"
    HEADER_MISSING = "header-missing"
    HEADER_MISMATCH = "header-mismatch"
    INVALID_PROVENANCE = "invalid-provenance"
    RECORD_INVALID = "record-invalid"
    INVALID_COUNT = "invalid-count"
    COUNT_OVERFLOW = "count-overflow"
    ZERO_WITHOUT_COMPLETE_QUERY = "zero-without-complete-query"
    INVALID_DECIMAL = "invalid-decimal"
    DUPLICATE_RECORD = "duplicate-record"
    CONFLICTING_RECORD = "conflicting-record"
    ROW_LIMIT = "row-limit"


class UnigramImportError(ValueError):
    """A bounded parser error that never contains source field contents."""

    def __init__(self, reason: UnigramImportFailure, detail: str | None = None) -> None:
        self.reason = reason.value
        suffix = f":{detail}" if detail is not None else ""
        super().__init__(f"{reason.value}{suffix}")


IMPORT_CONFIG = ConfigDict(
    extra="forbid",
    frozen=True,
    strict=True,
    validate_assignment=True,
    validate_default=True,
    allow_inf_nan=False,
)


def _safe_text(value: str) -> str:
    if any(ord(character) < 32 or 0x7F <= ord(character) <= 0x9F for character in value):
        raise ValueError("source text contains a control character")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise ValueError("source text contains a surrogate")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("source text is not valid UTF-8") from exc
    return value


class UnigramImportLimits(BaseModel):
    """Finite resource limits applied while reading one TSV stream."""

    model_config = IMPORT_CONFIG

    max_input_bytes: StrictInt = Field(default=8 * 1024 * 1024, gt=0, le=512 * 1024 * 1024)
    max_rows: StrictInt = Field(default=1024, gt=0, le=1_000_000)
    max_line_bytes: StrictInt = Field(default=64 * 1024, gt=0, le=16 * 1024 * 1024)
    max_field_bytes: StrictInt = Field(default=16 * 1024, gt=0, le=4 * 1024 * 1024)
    max_fields: StrictInt = Field(default=len(EXPECTED_HEADER), gt=0, le=256)

    @model_validator(mode="after")
    def validate_relationships(self) -> Self:
        if self.max_line_bytes > self.max_input_bytes:
            raise ValueError("max_line_bytes exceeds max_input_bytes")
        if self.max_field_bytes > self.max_line_bytes:
            raise ValueError("max_field_bytes exceeds max_line_bytes")
        return self


class UnigramProvenance(BaseModel):
    """Source and query evidence attached to every imported result."""

    model_config = IMPORT_CONFIG

    provenance_kind: StrictStr
    schema_version: StrictInt = SCHEMA_VERSION
    source_id: StrictStr = Field(min_length=1, max_length=128)
    source_name: StrictStr = Field(min_length=1, max_length=256)
    release: StrictStr = Field(min_length=1, max_length=128)
    source_inventory_revision: StrictStr = Field(min_length=1, max_length=128)
    source_inventory_sha256: StrictStr = Field(pattern=r"[0-9a-f]{64}")
    acquisition_sha256: StrictStr = Field(pattern=r"[0-9a-f]{64}")
    member_name: StrictStr = EXPECTED_MEMBER_NAME
    header_fields: tuple[StrictStr, ...] = EXPECTED_HEADER
    header_sha256: StrictStr = EXPECTED_HEADER_SHA256
    delimiter: StrictStr = EXPECTED_DELIMITER
    encoding: StrictStr = EXPECTED_ENCODING
    newline: StrictStr = EXPECTED_NEWLINE
    data_record_terminator: StrictStr = EXPECTED_DATA_RECORD_TERMINATOR
    header_line_number: StrictInt = EXPECTED_HEADER_LINE_NUMBER
    normalization: StrictStr = "source-exact"
    derived_lookup_transform: StrictStr = "NFC_CASEFOLD"
    source_completeness: EvidenceCompleteness = EvidenceCompleteness.UNKNOWN
    query_completeness: EvidenceCompleteness = EvidenceCompleteness.UNKNOWN
    import_completeness: EvidenceCompleteness = EvidenceCompleteness.PARTIAL
    evidence_scope: StrictStr = Field(min_length=1, max_length=512)
    redistribution_ready: StrictBool = False

    _clean_text = field_validator(
        "source_id",
        "source_name",
        "release",
        "source_inventory_revision",
        "provenance_kind",
        "member_name",
        "encoding",
        "newline",
        "data_record_terminator",
        "normalization",
        "derived_lookup_transform",
        "evidence_scope",
    )(_safe_text)

    @model_validator(mode="after")
    def validate_contract(self) -> Self:
        if self.provenance_kind not in {"real", "project-synthetic"}:
            raise ValueError("unsupported provenance kind")
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("unsupported schema version")
        if self.provenance_kind == "real":
            expected = {
                "source_id": REAL_SOURCE_ID,
                "source_name": REAL_SOURCE_NAME,
                "release": REAL_RELEASE,
                "source_inventory_revision": REAL_INVENTORY_REVISION,
                "source_inventory_sha256": REAL_INVENTORY_SHA256,
                "acquisition_sha256": REAL_ACQUISITION_SHA256,
            }
        else:
            expected = {
                "source_id": SYNTHETIC_SOURCE_ID,
                "source_name": SYNTHETIC_SOURCE_NAME,
                "release": SYNTHETIC_RELEASE,
                "source_inventory_revision": SYNTHETIC_INVENTORY_REVISION,
            }
            if self.source_inventory_sha256 in {"0" * 64, "1" * 64}:
                raise ValueError("synthetic inventory hash must identify fixture data")
            if self.acquisition_sha256 in {"0" * 64, "1" * 64}:
                raise ValueError("synthetic acquisition hash must identify fixture data")
        for field, value in expected.items():
            if getattr(self, field) != value:
                raise ValueError(f"{self.provenance_kind} provenance mismatch: {field}")
        if self.member_name != EXPECTED_MEMBER_NAME:
            raise ValueError("unsupported member name")
        if self.header_fields != EXPECTED_HEADER:
            raise ValueError("header fields do not match observed schema")
        if self.header_sha256 != EXPECTED_HEADER_SHA256:
            raise ValueError("header hash does not match observed schema")
        if self.delimiter != EXPECTED_DELIMITER:
            raise ValueError("unsupported delimiter")
        if self.encoding != EXPECTED_ENCODING or self.newline != EXPECTED_NEWLINE:
            raise ValueError("unsupported encoding or newline")
        if self.data_record_terminator != EXPECTED_DATA_RECORD_TERMINATOR:
            raise ValueError("unsupported data-record terminator")
        if self.header_line_number != EXPECTED_HEADER_LINE_NUMBER:
            raise ValueError("header line does not match observed schema")
        if self.normalization != "source-exact":
            raise ValueError("source normalization must remain exact")
        if self.derived_lookup_transform != "NFC_CASEFOLD":
            raise ValueError("unsupported lookup transform")
        if self.redistribution_ready:
            raise ValueError("import receipt cannot authorize redistribution")
        return self


class UnigramRecord(BaseModel):
    """One immutable row, including exact fields and lossless numeric views."""

    model_config = IMPORT_CONFIG

    row_number: StrictInt = Field(gt=0, le=2_000_000_000)
    raw_fields: tuple[StrictStr, ...] = Field(
        min_length=len(EXPECTED_HEADER), max_length=len(EXPECTED_HEADER)
    )
    source_form: StrictStr = Field(min_length=1, max_length=4096)
    lemma: StrictStr = Field(min_length=1, max_length=4096)
    lowercase_lemma: StrictStr = Field(min_length=1, max_length=4096)
    part_of_speech: StrictStr = Field(min_length=1, max_length=4096)
    derived_lookup_form: StrictStr = Field(min_length=1, max_length=4096)
    derived_lookup_transform: StrictStr = "NFC_CASEFOLD"
    absolute_counts: tuple[StrictInt | None, ...] = Field(
        min_length=len(_ABSOLUTE_INDICES), max_length=len(_ABSOLUTE_INDICES)
    )
    published_decimals: tuple[Decimal | None, ...] = Field(
        min_length=len(_DECIMAL_INDICES), max_length=len(_DECIMAL_INDICES)
    )
    published_decimal_text: tuple[StrictStr | None, ...] = Field(
        min_length=len(_DECIMAL_INDICES), max_length=len(_DECIMAL_INDICES)
    )
    record_key: StrictStr = Field(pattern=r"[0-9a-f]{64}")

    @field_validator("raw_fields")
    @classmethod
    def validate_raw_fields(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(EXPECTED_HEADER):
            raise ValueError("raw field count does not match schema")
        return tuple(_safe_text(field) for field in value)

    @field_validator("source_form", "lemma", "lowercase_lemma", "part_of_speech")
    @classmethod
    def validate_identity_fields(cls, value: str) -> str:
        return _safe_text(value)

    @field_validator("derived_lookup_form")
    @classmethod
    def validate_lookup_form(cls, value: str) -> str:
        return _safe_text(value)

    @field_validator("derived_lookup_transform")
    @classmethod
    def validate_lookup_transform(cls, value: str) -> str:
        return _safe_text(value)

    @field_validator("published_decimal_text")
    @classmethod
    def validate_decimal_text(
        cls, value: tuple[str | None, ...]
    ) -> tuple[str | None, ...]:
        for item in value:
            if item is not None:
                _safe_text(item)
        return value

    @field_validator("published_decimals")
    @classmethod
    def validate_decimals(cls, value: tuple[Decimal | None, ...]) -> tuple[Decimal | None, ...]:
        for decimal in value:
            if decimal is not None and (not decimal.is_finite() or decimal < 0):
                raise ValueError("published decimals must be finite and nonnegative")
        return value

    @model_validator(mode="after")
    def validate_record(self) -> Self:
        if len(self.raw_fields) != len(EXPECTED_HEADER):
            raise ValueError("raw field count does not match schema")
        if self.raw_fields[:4] != (
            self.source_form,
            self.lemma,
            self.lowercase_lemma,
            self.part_of_speech,
        ):
            raise ValueError("identity fields do not match raw fields")
        expected_lookup = unicodedata.normalize("NFC", self.source_form).casefold()
        if self.derived_lookup_form != expected_lookup:
            raise ValueError("derived lookup does not match source form")
        if self.derived_lookup_transform != "NFC_CASEFOLD":
            raise ValueError("unsupported lookup transform")
        for tuple_index, field_index in enumerate(_ABSOLUTE_INDICES):
            raw_value = self.raw_fields[field_index]
            if raw_value == "":
                if (
                    field_index == _ABSOLUTE_INDICES[0]
                    or self.absolute_counts[tuple_index] is not None
                ):
                    raise ValueError("absolute count does not match raw field")
                continue
            if _COUNT_RE.fullmatch(raw_value) is None:
                raise ValueError("absolute count does not match raw field")
            expected_count = int(raw_value)
            if expected_count > _MAX_COUNT or self.absolute_counts[tuple_index] != expected_count:
                raise ValueError("absolute count does not match raw field")
        for tuple_index, field_index in enumerate(_DECIMAL_INDICES):
            raw_value = self.raw_fields[field_index]
            expected_text = raw_value or None
            if self.published_decimal_text[tuple_index] != expected_text:
                raise ValueError("decimal text does not match raw field")
            if raw_value == "":
                if self.published_decimals[tuple_index] is not None:
                    raise ValueError("decimal value does not match raw field")
            else:
                if _DECIMAL_RE.fullmatch(raw_value) is None:
                    raise ValueError("decimal value does not match raw field")
                expected_decimal = Decimal(raw_value)
                if self.published_decimals[tuple_index] != expected_decimal:
                    raise ValueError("decimal value does not match raw field")
        expected_key = _record_key(
            self.source_form, self.lemma, self.lowercase_lemma, self.part_of_speech
        )
        if self.record_key != expected_key:
            raise ValueError("record key does not match identity fields")
        if any(value is not None and value > _MAX_COUNT for value in self.absolute_counts):
            raise ValueError("absolute count exceeds supported range")
        return self


class UnigramImportSummary(BaseModel):
    """Canonical, non-self-referential summary for one import."""

    model_config = IMPORT_CONFIG

    schema_version: StrictInt = SCHEMA_VERSION
    importer_version: StrictStr = IMPORTER_VERSION
    source_inventory_revision: StrictStr
    source_inventory_sha256: StrictStr = Field(pattern=r"[0-9a-f]{64}")
    acquisition_sha256: StrictStr = Field(pattern=r"[0-9a-f]{64}")
    member_name: StrictStr = EXPECTED_MEMBER_NAME
    header_sha256: StrictStr = EXPECTED_HEADER_SHA256
    normalization: StrictStr = "source-exact"
    derived_lookup_transform: StrictStr = "NFC_CASEFOLD"
    data_record_terminator: StrictStr = EXPECTED_DATA_RECORD_TERMINATOR
    source_completeness: EvidenceCompleteness
    query_completeness: EvidenceCompleteness
    import_completeness: EvidenceCompleteness
    max_input_bytes: StrictInt = Field(gt=0)
    max_rows: StrictInt = Field(gt=0)
    max_line_bytes: StrictInt = Field(gt=0)
    max_field_bytes: StrictInt = Field(gt=0)
    max_fields: StrictInt = Field(gt=0)
    input_bytes: StrictInt = Field(ge=0)
    record_count: StrictInt = Field(ge=0)
    input_sha256: StrictStr = Field(pattern=r"[0-9a-f]{64}")
    output_sha256: StrictStr = Field(pattern=r"[0-9a-f]{64}")

    @model_validator(mode="after")
    def validate_constants(self) -> Self:
        expected = {
            "schema_version": SCHEMA_VERSION,
            "importer_version": IMPORTER_VERSION,
            "member_name": EXPECTED_MEMBER_NAME,
            "header_sha256": EXPECTED_HEADER_SHA256,
            "normalization": "source-exact",
            "derived_lookup_transform": "NFC_CASEFOLD",
            "data_record_terminator": EXPECTED_DATA_RECORD_TERMINATOR,
        }
        for field, value in expected.items():
            if getattr(self, field) != value:
                raise ValueError(f"summary constant mismatch: {field}")
        return self


class UnigramImportResult(BaseModel):
    """Immutable result of one bounded import."""

    model_config = IMPORT_CONFIG

    provenance: UnigramProvenance
    limits: UnigramImportLimits
    records: tuple[UnigramRecord, ...] = Field(max_length=1_000_000)
    summary: UnigramImportSummary

    @model_validator(mode="after")
    def validate_summary_binding(self) -> Self:
        expected = {
            "source_inventory_revision": self.provenance.source_inventory_revision,
            "source_inventory_sha256": self.provenance.source_inventory_sha256,
            "acquisition_sha256": self.provenance.acquisition_sha256,
            "member_name": self.provenance.member_name,
            "header_sha256": self.provenance.header_sha256,
            "normalization": self.provenance.normalization,
            "derived_lookup_transform": self.provenance.derived_lookup_transform,
            "data_record_terminator": self.provenance.data_record_terminator,
            "source_completeness": self.provenance.source_completeness,
            "query_completeness": self.provenance.query_completeness,
            "import_completeness": self.provenance.import_completeness,
            "max_input_bytes": self.limits.max_input_bytes,
            "max_rows": self.limits.max_rows,
            "max_line_bytes": self.limits.max_line_bytes,
            "max_field_bytes": self.limits.max_field_bytes,
            "max_fields": self.limits.max_fields,
            "record_count": len(self.records),
        }
        for field, value in expected.items():
            if getattr(self.summary, field) != value:
                raise ValueError(f"summary binding mismatch: {field}")
        if self.summary.output_sha256 != hashlib.sha256(
            _canonical_json_bytes([_canonical_record(record) for record in self.records])
        ).hexdigest():
            raise ValueError("summary binding mismatch: output_sha256")
        if self.summary.record_count > self.limits.max_rows:
            raise ValueError("summary binding mismatch: max_rows")
        if self.summary.input_bytes > self.limits.max_input_bytes:
            raise ValueError("summary binding mismatch: input_bytes")
        return self


class _ReadableStream(Protocol):
    def read(self, size: int = -1) -> bytes | str: ...


def _record_key(source_form: str, lemma: str, lowercase_lemma: str, pos: str) -> str:
    identity = _RECORD_KEY_SEPARATOR.join((source_form, lemma, lowercase_lemma, pos))
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _canonical_record(record: UnigramRecord) -> dict[str, Any]:
    return {
        "row_number": record.row_number,
        "raw_fields": list(record.raw_fields),
        "source_form": record.source_form,
        "lemma": record.lemma,
        "lowercase_lemma": record.lowercase_lemma,
        "part_of_speech": record.part_of_speech,
        "derived_lookup_form": record.derived_lookup_form,
        "derived_lookup_transform": record.derived_lookup_transform,
        "absolute_counts": list(record.absolute_counts),
        "published_decimals": [
            None if value is None else str(value) for value in record.published_decimals
        ],
        "published_decimal_text": list(record.published_decimal_text),
        "record_key": record.record_key,
    }


def _failure(reason: UnigramImportFailure, detail: str | None = None) -> UnigramImportError:
    return UnigramImportError(reason, detail)


def _read_chunks(stream: _ReadableStream, limits: UnigramImportLimits) -> Iterator[bytes]:
    """Yield bounded chunks without materializing the input stream."""

    total = 0
    while True:
        try:
            chunk = stream.read(_CHUNK_SIZE)
        except (OSError, ValueError, UnicodeError) as exc:
            raise _failure(UnigramImportFailure.INPUT_READ_FAILED) from exc
        if chunk == b"" or chunk == "":
            break
        if isinstance(chunk, str):
            try:
                encoded = chunk.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise _failure(UnigramImportFailure.INVALID_SOURCE_TEXT) from exc
        elif isinstance(chunk, bytes):
            encoded = chunk
        else:
            raise _failure(UnigramImportFailure.INPUT_READ_FAILED)
        total += len(encoded)
        if total > limits.max_input_bytes:
            raise _failure(UnigramImportFailure.INPUT_TOO_LARGE)
        yield encoded


def _iter_lines(stream: _ReadableStream, limits: UnigramImportLimits) -> Iterator[bytes]:
    """Split an input stream without calling an unbounded ``readline``."""

    pending = bytearray()
    for chunk in _read_chunks(stream, limits):
        pending.extend(chunk)
        if len(pending) > limits.max_line_bytes and pending.find(b"\n") < 0:
            raise _failure(UnigramImportFailure.LINE_TOO_LARGE)
        while True:
            newline = pending.find(b"\n")
            if newline < 0:
                break
            line = bytes(pending[: newline + 1])
            del pending[: newline + 1]
            if len(line) > limits.max_line_bytes:
                raise _failure(UnigramImportFailure.LINE_TOO_LARGE)
            yield line
    if pending:
        raise _failure(UnigramImportFailure.MISSING_FINAL_NEWLINE)


def _decode_line(raw_line: bytes, line_number: int) -> str:
    if not raw_line.endswith(b"\r\n"):
        if raw_line.endswith(b"\n"):
            raise _failure(UnigramImportFailure.INVALID_NEWLINE, str(line_number))
        raise _failure(UnigramImportFailure.MISSING_FINAL_NEWLINE, str(line_number))
    try:
        value = raw_line[:-2].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _failure(UnigramImportFailure.INVALID_UTF8, str(line_number)) from exc
    try:
        # Tabs are the declared structural delimiter; field validation below
        # rejects them when they occur inside a quoted value.
        _safe_text(value.replace(EXPECTED_DELIMITER, ""))
        return value
    except ValueError as exc:
        raise _failure(UnigramImportFailure.INVALID_SOURCE_TEXT, str(line_number)) from exc


def _parse_quoted_tsv(
    line: str,
    limits: UnigramImportLimits,
    line_number: int,
    *,
    data_record: bool = False,
) -> tuple[str, ...]:
    """Parse the observed all-fields-quoted TSV form with no row buffering."""

    if data_record:
        if not line.endswith("\t"):
            raise _failure(UnigramImportFailure.INVALID_QUOTING, str(line_number))
        line = line[:-1]
    elif line.endswith("\t"):
        raise _failure(UnigramImportFailure.INVALID_QUOTING, str(line_number))

    fields: list[str] = []
    position = 0
    while position < len(line):
        if line[position] != '"':
            raise _failure(UnigramImportFailure.INVALID_QUOTING, str(line_number))
        position += 1
        value: list[str] = []
        while position < len(line):
            character = line[position]
            if character == '"':
                if position + 1 < len(line) and line[position + 1] == '"':
                    value.append('"')
                    position += 2
                    continue
                position += 1
                break
            value.append(character)
            position += 1
        else:
            raise _failure(UnigramImportFailure.INVALID_QUOTING, str(line_number))
        field = "".join(value)
        try:
            _safe_text(field)
            field_size = len(field.encode("utf-8"))
        except (UnicodeEncodeError, ValueError) as exc:
            raise _failure(UnigramImportFailure.INVALID_SOURCE_TEXT, str(line_number)) from exc
        if field_size > limits.max_field_bytes:
            raise _failure(UnigramImportFailure.FIELD_TOO_LARGE, str(line_number))
        fields.append(field)
        if position == len(line):
            break
        if line[position] != EXPECTED_DELIMITER:
            raise _failure(UnigramImportFailure.INVALID_QUOTING, str(line_number))
        position += 1
        if position == len(line):
            raise _failure(UnigramImportFailure.INVALID_QUOTING, str(line_number))
    if len(fields) > limits.max_fields:
        raise _failure(UnigramImportFailure.FIELD_COUNT, str(line_number))
    return tuple(fields)


def _parse_count(
    text: str, *, index: int, query_complete: bool
) -> int | None:
    if text == "":
        if index == _ABSOLUTE_INDICES[0]:
            raise _failure(UnigramImportFailure.INVALID_COUNT, str(index + 1))
        return None
    if _COUNT_RE.fullmatch(text) is None:
        raise _failure(UnigramImportFailure.INVALID_COUNT, str(index + 1))
    if len(text) > 19:
        raise _failure(UnigramImportFailure.COUNT_OVERFLOW, str(index + 1))
    value = int(text)
    if value > _MAX_COUNT:
        raise _failure(UnigramImportFailure.COUNT_OVERFLOW, str(index + 1))
    if value == 0 and not query_complete:
        raise _failure(UnigramImportFailure.ZERO_WITHOUT_COMPLETE_QUERY, str(index + 1))
    return value


def _parse_decimal(text: str, *, index: int) -> Decimal | None:
    if text == "":
        return None
    if _DECIMAL_RE.fullmatch(text) is None:
        raise _failure(UnigramImportFailure.INVALID_DECIMAL, str(index + 1))
    try:
        value = Decimal(text)
    except InvalidOperation as exc:
        raise _failure(UnigramImportFailure.INVALID_DECIMAL, str(index + 1)) from exc
    if not value.is_finite() or value < 0:
        raise _failure(UnigramImportFailure.INVALID_DECIMAL, str(index + 1))
    return value


def _make_record(
    fields: tuple[str, ...], *, row_number: int, provenance: UnigramProvenance
) -> UnigramRecord:
    if len(fields) != len(EXPECTED_HEADER):
        raise _failure(UnigramImportFailure.FIELD_COUNT, str(row_number))
    absolute_counts = tuple(
        _parse_count(
            fields[index],
            index=index,
        query_complete=provenance.query_completeness is EvidenceCompleteness.COMPLETE,
        )
        for index in _ABSOLUTE_INDICES
    )
    decimal_values = tuple(_parse_decimal(fields[index], index=index) for index in _DECIMAL_INDICES)
    decimal_text = tuple(fields[index] or None for index in _DECIMAL_INDICES)
    try:
        return UnigramRecord(
            row_number=row_number,
            raw_fields=fields,
            source_form=fields[0],
            lemma=fields[1],
            lowercase_lemma=fields[2],
            part_of_speech=fields[3],
            derived_lookup_form=unicodedata.normalize("NFC", fields[0]).casefold(),
            derived_lookup_transform=provenance.derived_lookup_transform,
            absolute_counts=absolute_counts,
            published_decimals=decimal_values,
            published_decimal_text=decimal_text,
            record_key=_record_key(fields[0], fields[1], fields[2], fields[3]),
        )
    except (TypeError, ValueError) as exc:
        raise _failure(UnigramImportFailure.RECORD_INVALID, str(row_number)) from exc


def _validate_provenance(provenance: UnigramProvenance) -> None:
    try:
        if provenance.header_line_number <= 0:
            raise ValueError("header line must be positive")
    except (TypeError, ValueError) as exc:
        raise _failure(UnigramImportFailure.INVALID_PROVENANCE) from exc


def import_unigrams(
    stream: BinaryIO | TextIO | _ReadableStream,
    provenance: UnigramProvenance,
    *,
    limits: UnigramImportLimits | None = None,
) -> UnigramImportResult:
    """Import one bounded TSV stream using the observed Gigafida schema.

    The stream is consumed incrementally in bounded chunks.  It must contain
    CRLF-terminated, all-fields-quoted UTF-8 lines, with the observed header at
    ``provenance.header_line_number``.  The importer never opens paths or uses
    the network; ZIP/member acquisition remains the caller's responsibility.
    """

    if not isinstance(provenance, UnigramProvenance):
        raise _failure(UnigramImportFailure.INVALID_PROVENANCE)
    _validate_provenance(provenance)
    actual_limits = limits if limits is not None else UnigramImportLimits()
    if not isinstance(actual_limits, UnigramImportLimits):
        raise _failure(UnigramImportFailure.INVALID_LIMIT)
    try:
        lines = _iter_lines(cast(_ReadableStream, stream), actual_limits)
    except UnigramImportError:
        raise
    except (AttributeError, TypeError) as exc:
        raise _failure(UnigramImportFailure.INPUT_READ_FAILED) from exc
    records: list[UnigramRecord] = []
    records_by_key: dict[str, UnigramRecord] = {}
    input_digest = hashlib.sha256()
    input_bytes = 0
    saw_header = False
    for row_number, raw_line in enumerate(lines, start=1):
        input_digest.update(raw_line)
        input_bytes += len(raw_line)
        if row_number < provenance.header_line_number:
            _decode_line(raw_line, row_number)
            continue
        if row_number == provenance.header_line_number:
            header_line = _decode_line(raw_line, row_number)
            header = _parse_quoted_tsv(header_line, actual_limits, row_number)
            if header != EXPECTED_HEADER:
                raise _failure(UnigramImportFailure.HEADER_MISMATCH, str(row_number))
            saw_header = True
            continue
        if not saw_header:
            raise _failure(UnigramImportFailure.HEADER_MISSING)
        if len(records) >= actual_limits.max_rows:
            raise _failure(UnigramImportFailure.ROW_LIMIT)
        line = _decode_line(raw_line, row_number)
        fields = _parse_quoted_tsv(line, actual_limits, row_number, data_record=True)
        record = _make_record(fields, row_number=row_number, provenance=provenance)
        previous = records_by_key.get(record.record_key)
        if previous is not None:
            if previous.raw_fields == record.raw_fields:
                raise _failure(UnigramImportFailure.DUPLICATE_RECORD, str(row_number))
            raise _failure(UnigramImportFailure.CONFLICTING_RECORD, str(row_number))
        records_by_key[record.record_key] = record
        records.append(record)
    if not saw_header:
        raise _failure(UnigramImportFailure.HEADER_MISSING)

    canonical_records = [_canonical_record(record) for record in records]
    output_sha256 = hashlib.sha256(_canonical_json_bytes(canonical_records)).hexdigest()
    input_sha256 = input_digest.hexdigest()
    summary = UnigramImportSummary(
        source_inventory_revision=provenance.source_inventory_revision,
        source_inventory_sha256=provenance.source_inventory_sha256,
        acquisition_sha256=provenance.acquisition_sha256,
        member_name=provenance.member_name,
        header_sha256=provenance.header_sha256,
        normalization=provenance.normalization,
        derived_lookup_transform=provenance.derived_lookup_transform,
        source_completeness=provenance.source_completeness,
        query_completeness=provenance.query_completeness,
        import_completeness=provenance.import_completeness,
        max_input_bytes=actual_limits.max_input_bytes,
        max_rows=actual_limits.max_rows,
        max_line_bytes=actual_limits.max_line_bytes,
        max_field_bytes=actual_limits.max_field_bytes,
        max_fields=actual_limits.max_fields,
        input_bytes=input_bytes,
        record_count=len(records),
        input_sha256=input_sha256,
        output_sha256=output_sha256,
    )
    return UnigramImportResult(
        provenance=provenance,
        limits=actual_limits,
        records=tuple(records),
        summary=summary,
    )


__all__ = [
    "EXPECTED_DELIMITER",
    "EXPECTED_ENCODING",
    "EXPECTED_HEADER",
    "EXPECTED_HEADER_BYTE_LENGTH",
    "EXPECTED_HEADER_LINE_NUMBER",
    "EXPECTED_DATA_RECORD_TERMINATOR",
    "EXPECTED_HEADER_SHA256",
    "EXPECTED_MEMBER_NAME",
    "EXPECTED_NEWLINE",
    "IMPORTER_VERSION",
    "EvidenceCompleteness",
    "REAL_ACQUISITION_SHA256",
    "REAL_INVENTORY_REVISION",
    "REAL_INVENTORY_SHA256",
    "REAL_RELEASE",
    "REAL_SOURCE_ID",
    "REAL_SOURCE_NAME",
    "SYNTHETIC_INVENTORY_REVISION",
    "SYNTHETIC_RELEASE",
    "SYNTHETIC_SOURCE_ID",
    "SYNTHETIC_SOURCE_NAME",
    "UnigramImportError",
    "UnigramImportFailure",
    "UnigramImportLimits",
    "UnigramImportResult",
    "UnigramImportSummary",
    "UnigramProvenance",
    "UnigramRecord",
    "import_unigrams",
]
