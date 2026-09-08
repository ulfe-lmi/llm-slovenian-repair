"""Content-free structural diagnosis for a bounded unigram row prefix.

The public classifier accepts a caller-owned binary stream.  It never opens a
path, contacts a source, writes a file, or returns decoded field data.  The
command-line wrapper reads a bounded prefix from standard input so a verified
archive/member reader can remain outside this module.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Final, Protocol

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

SCHEMA_VERSION: Final = 1
MAX_REQUESTED_ROWS: Final = 32
DEFAULT_MAX_TOTAL_BYTES: Final = 4 * 1024 * 1024
DEFAULT_MAX_LINE_BYTES: Final = 256 * 1024
_DIAGNOSTIC_INVENTORY_SHA256: Final = "a" * 64
_DIAGNOSTIC_ACQUISITION_SHA256: Final = "b" * 64

ABSOLUTE_COUNT_COLUMNS: Final = (5, 8, 11, 14, 17, 20, 23, 26)
PUBLISHED_DECIMAL_COLUMNS: Final = tuple(
    column
    for column in range(5, 29)
    if column not in ABSOLUTE_COUNT_COLUMNS
)
NUMERIC_COLUMNS: Final = tuple(range(5, 29))


class NumericTokenCategory(StrEnum):
    """Closed, content-free syntax categories for one numeric cell."""

    EMPTY = "EMPTY"
    ASCII_DIGITS = "ASCII_DIGITS"
    ASCII_DECIMAL_DOT = "ASCII_DECIMAL_DOT"
    ASCII_DECIMAL_COMMA = "ASCII_DECIMAL_COMMA"
    ASCII_GROUPED_DOT_TRIPLETS = "ASCII_GROUPED_DOT_TRIPLETS"
    ASCII_GROUPED_COMMA_TRIPLETS = "ASCII_GROUPED_COMMA_TRIPLETS"
    ASCII_GROUPED_SPACE_TRIPLETS = "ASCII_GROUPED_SPACE_TRIPLETS"
    UNICODE_SPACE_GROUPED_TRIPLETS = "UNICODE_SPACE_GROUPED_TRIPLETS"
    ASCII_SCIENTIFIC_DOT = "ASCII_SCIENTIFIC_DOT"
    ASCII_SCIENTIFIC_COMMA = "ASCII_SCIENTIFIC_COMMA"
    SIGN_PREFIX = "SIGN_PREFIX"
    PERCENT_SUFFIX = "PERCENT_SUFFIX"
    LEADING_OR_TRAILING_WHITESPACE = "LEADING_OR_TRAILING_WHITESPACE"
    OTHER_ASCII = "OTHER_ASCII"
    OTHER_UNICODE = "OTHER_UNICODE"


NUMERIC_CATEGORY_ORDER: Final = tuple(NumericTokenCategory)
_ASCII_DIGITS_RE = re.compile(r"[0-9]+")
_ASCII_DECIMAL_DOT_RE = re.compile(r"(?:0|[0-9]+)\.[0-9]+")
_ASCII_DECIMAL_COMMA_RE = re.compile(r"(?:0|[0-9]+),[0-9]+")
_ASCII_GROUPED_DOT_RE = re.compile(r"[0-9]{1,3}(?:\.[0-9]{3})+")
_ASCII_GROUPED_COMMA_RE = re.compile(r"[0-9]{1,3}(?:,[0-9]{3})+")
_ASCII_GROUPED_SPACE_RE = re.compile(r"[0-9]{1,3}(?: [0-9]{3})+")
_ASCII_SCIENTIFIC_DOT_RE = re.compile(
    r"(?:0|[0-9]+)(?:\.[0-9]+)?[eE][+-]?[0-9]+"
)
_ASCII_SCIENTIFIC_COMMA_RE = re.compile(
    r"(?:0|[0-9]+)(?:,[0-9]+)?[eE][+-]?[0-9]+"
)
_CURRENT_DECIMAL_RE = re.compile(
    r"(?:0|[0-9]+)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?"
)
_CURRENT_COUNT_MAX = (1 << 63) - 1


class DiagnosticError(ValueError):
    """A finite, content-free diagnostic failure."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class BinaryLineStream(Protocol):
    """The caller-owned binary stream surface needed for prefix routing."""

    def readline(self, size: int = -1, /) -> bytes: ...


@dataclass(frozen=True, slots=True)
class RowStructureLimits:
    """Finite limits for one diagnosis input."""

    max_rows: int = MAX_REQUESTED_ROWS
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES
    max_line_bytes: int = DEFAULT_MAX_LINE_BYTES

    def __post_init__(self) -> None:
        if not 1 <= self.max_rows <= MAX_REQUESTED_ROWS:
            raise DiagnosticError("invalid-max-rows")
        if self.max_total_bytes <= 0:
            raise DiagnosticError("invalid-max-total-bytes")
        if self.max_line_bytes <= 0 or self.max_line_bytes > self.max_total_bytes:
            raise DiagnosticError("invalid-max-line-bytes")


@dataclass(frozen=True, slots=True)
class _RowShape:
    field_count: int
    terminal_tab_count: int
    empty_final_field: bool
    nonempty_after_28: bool
    all_fields_quoted: bool
    all_semantic_fields_quoted: bool
    embedded_tab_in_quoted_field: bool
    quote_parse_error: bool


def _line_parts(data: bytes) -> list[bytes]:
    """Split only on LF, retaining each physical row terminator."""

    if not data:
        raise DiagnosticError("no-rows")
    parts = data.split(b"\n")
    has_final_newline = data.endswith(b"\n")
    if has_final_newline:
        parts.pop()
    if not parts:
        raise DiagnosticError("no-rows")
    return [
        part + (b"\n" if has_final_newline or index < len(parts) - 1 else b"")
        for index, part in enumerate(parts)
    ]


def _read_bounded(stream: BinaryIO, limits: RowStructureLimits) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while total <= limits.max_total_bytes:
        try:
            chunk = stream.read(min(64 * 1024, limits.max_total_bytes + 1 - total))
        except (AttributeError, OSError, TypeError) as exc:
            raise DiagnosticError("input-read-failed") from exc
        if not isinstance(chunk, bytes):
            raise DiagnosticError("input-not-binary")
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > limits.max_total_bytes:
            raise DiagnosticError("input-too-large")
    return b"".join(chunks)


def _strip_terminator(row: bytes) -> bytes:
    if row.endswith(b"\r\n"):
        return row[:-2]
    if row.endswith(b"\n"):
        return row[:-1]
    return row


def _terminal_tabs(body: bytes) -> int:
    count = 0
    for value in reversed(body):
        if value != 9:
            break
        count += 1
    return count


def _parse_shape(body: bytes) -> _RowShape:
    """Parse CSV/quoted-tab structure without decoding or retaining values."""

    field_count = 0
    quoted: list[bool] = []
    empty: list[bool] = []
    embedded_tab = False
    index = 0
    length = len(body)

    while True:
        field_count += 1
        if index < length and body[index] == 34:
            quoted.append(True)
            index += 1
            has_value = False
            closed = False
            while index < length:
                value = body[index]
                if value == 34:
                    if index + 1 < length and body[index + 1] == 34:
                        has_value = True
                        index += 2
                        continue
                    index += 1
                    closed = True
                    break
                if value == 9:
                    embedded_tab = True
                has_value = True
                index += 1
            if not closed:
                return _RowShape(
                    field_count,
                    _terminal_tabs(body),
                    False,
                    False,
                    False,
                    False,
                    embedded_tab,
                    True,
                )
            if index < length and body[index] != 9:
                return _RowShape(
                    field_count,
                    _terminal_tabs(body),
                    False,
                    False,
                    False,
                    False,
                    embedded_tab,
                    True,
                )
            empty.append(not has_value)
        else:
            quoted.append(False)
            start = index
            while index < length and body[index] != 9:
                if body[index] == 34:
                    return _RowShape(
                        field_count,
                        _terminal_tabs(body),
                        False,
                        False,
                        False,
                        False,
                        embedded_tab,
                        True,
                    )
                index += 1
            empty.append(index == start)

        if index == length:
            break
        index += 1

    return _RowShape(
        field_count=field_count,
        terminal_tab_count=_terminal_tabs(body),
        empty_final_field=empty[-1],
        nonempty_after_28=any(not value for value in empty[28:]),
        all_fields_quoted=bool(quoted) and all(quoted),
        all_semantic_fields_quoted=len(quoted) >= 28 and all(quoted[:28]),
        embedded_tab_in_quoted_field=embedded_tab,
        quote_parse_error=False,
    )


def _parse_semantic_bytes(body: bytes) -> tuple[bytes, ...]:
    """Parse the already shape-checked 28 semantic fields without decoding them."""

    if body.endswith(b"\t"):
        body = body[:-1]
    values: list[bytes] = []
    position = 0
    while position < len(body):
        if body[position] != 34:
            raise DiagnosticError("numeric-structure-invalid")
        position += 1
        value = bytearray()
        while position < len(body):
            character = body[position]
            if character == 34:
                if position + 1 < len(body) and body[position + 1] == 34:
                    value.extend(b'"')
                    position += 2
                    continue
                position += 1
                break
            value.append(character)
            position += 1
        else:
            raise DiagnosticError("numeric-structure-invalid")
        values.append(bytes(value))
        if position == len(body):
            break
        if body[position] != 9:
            raise DiagnosticError("numeric-structure-invalid")
        position += 1
        if position == len(body):
            raise DiagnosticError("numeric-structure-invalid")
    if len(values) != 28:
        raise DiagnosticError("numeric-structure-invalid")
    return tuple(values)


def _unicode_text(value: bytes) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DiagnosticError("numeric-invalid-utf8") from exc


def classify_numeric_token(value: bytes) -> NumericTokenCategory:
    """Classify one numeric token using a fixed mutually exclusive priority.

    Priority is EMPTY, boundary whitespace, percent suffix, sign prefix,
    scientific notation, grouped triplets, ordinary decimal notation, digits,
    then the ASCII/Unicode fallback.  The classifier records syntax only; it
    never interprets separators or numeric values.
    """

    if value == b"":
        return NumericTokenCategory.EMPTY
    text = _unicode_text(value)
    if text != text.strip() or any(character.isspace() for character in text[:1] + text[-1:]):
        return NumericTokenCategory.LEADING_OR_TRAILING_WHITESPACE
    if text.endswith("%"):
        return NumericTokenCategory.PERCENT_SUFFIX
    if text.startswith(("+", "-")):
        return NumericTokenCategory.SIGN_PREFIX
    if _ASCII_SCIENTIFIC_DOT_RE.fullmatch(text):
        return NumericTokenCategory.ASCII_SCIENTIFIC_DOT
    if _ASCII_SCIENTIFIC_COMMA_RE.fullmatch(text):
        return NumericTokenCategory.ASCII_SCIENTIFIC_COMMA
    if _ASCII_GROUPED_DOT_RE.fullmatch(text):
        return NumericTokenCategory.ASCII_GROUPED_DOT_TRIPLETS
    if _ASCII_GROUPED_COMMA_RE.fullmatch(text):
        return NumericTokenCategory.ASCII_GROUPED_COMMA_TRIPLETS
    if _ASCII_GROUPED_SPACE_RE.fullmatch(text):
        return NumericTokenCategory.ASCII_GROUPED_SPACE_TRIPLETS
    if (
        len(text) > 1
        and text[0].isdigit()
        and all(character.isdigit() or character.isspace() for character in text)
        and any(character.isspace() and character != " " for character in text)
        and re.fullmatch(r"[0-9]{1,3}(?:\s[0-9]{3})+", text) is not None
    ):
        return NumericTokenCategory.UNICODE_SPACE_GROUPED_TRIPLETS
    if _ASCII_DECIMAL_DOT_RE.fullmatch(text):
        return NumericTokenCategory.ASCII_DECIMAL_DOT
    if _ASCII_DECIMAL_COMMA_RE.fullmatch(text):
        return NumericTokenCategory.ASCII_DECIMAL_COMMA
    if _ASCII_DIGITS_RE.fullmatch(text):
        return NumericTokenCategory.ASCII_DIGITS
    if value.isascii():
        return NumericTokenCategory.OTHER_ASCII
    return NumericTokenCategory.OTHER_UNICODE


def _is_current_count_compatible(value: bytes, *, first_column: bool) -> bool:
    if value == b"":
        return not first_column
    if not value.isascii() or _ASCII_DIGITS_RE.fullmatch(value.decode("ascii")) is None:
        return False
    if len(value) > 19:
        return False
    return int(value) <= _CURRENT_COUNT_MAX


def _is_current_decimal_compatible(value: bytes) -> bool:
    if value == b"":
        return True
    text = _unicode_text(value)
    if _CURRENT_DECIMAL_RE.fullmatch(text) is None:
        return False
    try:
        return Decimal(text).is_finite() and Decimal(text) >= 0
    except InvalidOperation:
        return False


def _validate_numeric_row(row: bytes) -> tuple[bytes, ...]:
    if not row.endswith(b"\r\n"):
        raise DiagnosticError("numeric-structure-invalid")
    body = row[:-2]
    shape = _parse_shape(body)
    if (
        shape.quote_parse_error
        or shape.field_count not in (28, 29)
        or shape.terminal_tab_count not in (0, 1)
        or shape.nonempty_after_28
        or not shape.all_semantic_fields_quoted
    ):
        raise DiagnosticError("numeric-structure-invalid")
    try:
        row.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DiagnosticError("numeric-invalid-utf8") from exc
    return _parse_semantic_bytes(body)


def _numeric_profile(rows: list[bytes]) -> dict[str, object]:
    histograms: dict[str, dict[str, object]] = {}
    for column in NUMERIC_COLUMNS:
        kind = "absolute_count" if column in ABSOLUTE_COUNT_COLUMNS else "published_decimal"
        histograms[str(column)] = {
            "semantic_kind": kind,
            "category_histogram": {
                category.value: 0 for category in NUMERIC_CATEGORY_ORDER
            },
            "current_parser_compatible_cell_count": 0,
            "current_parser_incompatible_cell_count": 0,
        }

    compatible = {"absolute_count": 0, "published_decimal": 0}
    incompatible = {"absolute_count": 0, "published_decimal": 0}
    first_incompatible: dict[str, object] | None = None
    for row_ordinal, row in enumerate(rows, start=1):
        fields = _validate_numeric_row(row)
        for column in NUMERIC_COLUMNS:
            kind = "absolute_count" if column in ABSOLUTE_COUNT_COLUMNS else "published_decimal"
            value = fields[column - 1]
            category = classify_numeric_token(value)
            column_data = histograms[str(column)]
            category_histogram = column_data["category_histogram"]
            assert isinstance(category_histogram, dict)
            category_histogram[category.value] += 1
            if kind == "absolute_count":
                is_compatible = _is_current_count_compatible(
                    value, first_column=column == ABSOLUTE_COUNT_COLUMNS[0]
                )
            else:
                is_compatible = _is_current_decimal_compatible(value)
            if is_compatible:
                compatible[kind] += 1
                current_count = column_data["current_parser_compatible_cell_count"]
                assert isinstance(current_count, int)
                column_data["current_parser_compatible_cell_count"] = current_count + 1
            else:
                incompatible[kind] += 1
                current_count = column_data["current_parser_incompatible_cell_count"]
                assert isinstance(current_count, int)
                column_data["current_parser_incompatible_cell_count"] = current_count + 1
                if first_incompatible is None:
                    first_incompatible = {
                        "row_ordinal": row_ordinal,
                        "column": column,
                        "semantic_kind": kind,
                        "category": category.value,
                    }

    row_count = len(rows)
    return {
        "schema_version": SCHEMA_VERSION,
        "row_count": row_count,
        "numeric_cell_count": row_count * len(NUMERIC_COLUMNS),
        "absolute_count_cell_count": row_count * len(ABSOLUTE_COUNT_COLUMNS),
        "published_decimal_cell_count": row_count * len(PUBLISHED_DECIMAL_COLUMNS),
        "column_histograms": histograms,
        "current_parser_compatibility": {
            "absolute_count": {
                "compatible_cell_count": compatible["absolute_count"],
                "incompatible_cell_count": incompatible["absolute_count"],
            },
            "published_decimal": {
                "compatible_cell_count": compatible["published_decimal"],
                "incompatible_cell_count": incompatible["published_decimal"],
            },
        },
        "first_incompatible": first_incompatible,
    }


def classify_numeric_rows(
    stream: BinaryIO,
    *,
    requested_row_count: int,
    limits: RowStructureLimits | None = None,
) -> dict[str, object]:
    """Profile exactly one structurally valid bounded row set."""

    actual_limits = limits or RowStructureLimits()
    if not 1 <= requested_row_count <= MAX_REQUESTED_ROWS:
        raise DiagnosticError("invalid-requested-row-count")
    if requested_row_count > actual_limits.max_rows:
        raise DiagnosticError("requested-row-limit")
    rows = _line_parts(_read_bounded(stream, actual_limits))
    if len(rows) != requested_row_count:
        raise DiagnosticError("numeric-row-count")
    return _numeric_profile(rows)


def classify_numeric_stream(
    stream: BinaryLineStream,
    *,
    skip_rows: int,
    requested_rows: int,
    limits: RowStructureLimits | None = None,
) -> dict[str, object]:
    """Route one bounded member prefix, then profile its semantic rows once."""

    actual_limits = limits or RowStructureLimits()
    prefix = _read_prefix(
        stream,
        skip_rows=skip_rows,
        requested_rows=requested_rows,
        max_line_bytes=actual_limits.max_line_bytes,
    )
    return classify_numeric_rows(
        prefix,
        requested_row_count=requested_rows,
        limits=actual_limits,
    )


def _parser_failure_reason(row: bytes) -> str | None:
    """Probe only the existing parser's finite failure label, never its result."""

    # The shape classifier itself remains standard-library-only. This bounded
    # optional probe is separate and contributes only the parser's finite label.
    try:
        from llm_slovenian_repair.contracts import EvidenceCompleteness
        from llm_slovenian_repair.unigram_importer import (
            EXPECTED_HEADER_BYTES,
            SYNTHETIC_INVENTORY_REVISION,
            SYNTHETIC_RELEASE,
            SYNTHETIC_SOURCE_ID,
            SYNTHETIC_SOURCE_NAME,
            UnigramImportError,
            UnigramImportFailure,
            UnigramProvenance,
            import_unigrams,
        )
    except ImportError:
        return None

    provenance = UnigramProvenance(
        provenance_kind="project-synthetic",
        source_id=SYNTHETIC_SOURCE_ID,
        source_name=SYNTHETIC_SOURCE_NAME,
        release=SYNTHETIC_RELEASE,
        source_inventory_revision=SYNTHETIC_INVENTORY_REVISION,
        source_inventory_sha256=_DIAGNOSTIC_INVENTORY_SHA256,
        acquisition_sha256=_DIAGNOSTIC_ACQUISITION_SHA256,
        evidence_scope="diagnostic-only synthetic parser probe",
        source_completeness=EvidenceCompleteness.COMPLETE,
        query_completeness=EvidenceCompleteness.COMPLETE,
        import_completeness=EvidenceCompleteness.PARTIAL,
    )
    envelope = b"#\r\n" * 14 + EXPECTED_HEADER_BYTES + row
    try:
        import_unigrams(BytesIO(envelope), provenance)
    except UnigramImportError as error:
        if error.reason in {reason.value for reason in UnigramImportFailure}:
            return error.reason
    return None


def _is_structurally_failing(shape: _RowShape) -> bool:
    """Flag only a bounded shape outside 28 fields plus empty terminal tabs."""

    if shape.quote_parse_error:
        return True
    if not 28 <= shape.field_count <= 30:
        return True
    if shape.nonempty_after_28:
        return True
    # The first 28 fields are the candidate semantic record; trailing empty
    # fields are retained as evidence for terminal-delimiter hypotheses.
    return not shape.all_semantic_fields_quoted


def classify_rows(
    stream: BinaryIO,
    *,
    requested_row_count: int,
    limits: RowStructureLimits | None = None,
    include_parser_probe: bool = True,
) -> dict[str, object]:
    """Return aggregate-only structure metadata for one bounded row stream."""

    actual_limits = limits or RowStructureLimits()
    if not 1 <= requested_row_count <= MAX_REQUESTED_ROWS:
        raise DiagnosticError("invalid-requested-row-count")
    if requested_row_count > actual_limits.max_rows:
        raise DiagnosticError("requested-row-limit")
    data = _read_bounded(stream, actual_limits)
    rows = _line_parts(data)
    if not 1 <= len(rows) <= actual_limits.max_rows:
        raise DiagnosticError("row-count-limit")
    if len(rows) > requested_row_count:
        raise DiagnosticError("more-rows-than-requested")

    utf8_valid = 0
    utf8_invalid = 0
    crlf = 0
    lf = 0
    missing_newline = 0
    terminal_tabs: Counter[str] = Counter({"0": 0, "1": 0, "2+": 0})
    field_counts: Counter[str] = Counter()
    empty_final = 0
    nonempty_after_28 = 0
    all_quoted = 0
    embedded_tabs = 0
    quote_errors = 0
    parser_failures: Counter[str] = Counter()
    minimum = min(len(row) for row in rows)
    maximum = max(len(row) for row in rows)
    first_failure: int | None = None

    for line_number, row in enumerate(rows, start=1):
        if len(row) > actual_limits.max_line_bytes:
            raise DiagnosticError("line-too-large")
        if row.endswith(b"\r\n"):
            crlf += 1
        elif row.endswith(b"\n"):
            lf += 1
        else:
            missing_newline += 1
        try:
            row.decode("utf-8")
        except UnicodeDecodeError:
            utf8_invalid += 1
        else:
            utf8_valid += 1

        shape = _parse_shape(_strip_terminator(row))
        terminal_key = "2+" if shape.terminal_tab_count >= 2 else str(shape.terminal_tab_count)
        terminal_tabs[terminal_key] += 1
        field_counts[str(shape.field_count)] += 1
        empty_final += int(shape.empty_final_field)
        nonempty_after_28 += int(shape.nonempty_after_28)
        all_quoted += int(shape.all_fields_quoted)
        embedded_tabs += int(shape.embedded_tab_in_quoted_field)
        quote_errors += int(shape.quote_parse_error)
        if first_failure is None and _is_structurally_failing(shape):
            first_failure = line_number
        if include_parser_probe:
            reason = _parser_failure_reason(row)
            if reason is not None:
                parser_failures[reason] += 1

    return {
        "schema_version": SCHEMA_VERSION,
        "requested_row_count": requested_row_count,
        "read_row_count": len(rows),
        "utf8_valid_row_count": utf8_valid,
        "utf8_invalid_row_count": utf8_invalid,
        "crlf_row_count": crlf,
        "lf_row_count": lf,
        "missing_newline_row_count": missing_newline,
        "terminal_tab_count_histogram": dict((key, terminal_tabs[key]) for key in ("0", "1", "2+")),
        "csv_field_count_histogram": dict(
            sorted(field_counts.items(), key=lambda item: int(item[0]))
        ),
        "empty_final_field_count": empty_final,
        "nonempty_field_after_28_count": nonempty_after_28,
        "fully_all_fields_quoted_count": all_quoted,
        "embedded_tab_in_quoted_field_row_count": embedded_tabs,
        "quote_parse_error_count": quote_errors,
        "existing_parser_failure_reason_histogram": dict(sorted(parser_failures.items())),
        "min_whole_row_byte_length": minimum,
        "max_whole_row_byte_length": maximum,
        "first_structurally_failing_source_line_number": first_failure,
    }


def _read_prefix(
    stream: BinaryLineStream, *, skip_rows: int, requested_rows: int, max_line_bytes: int
) -> BytesIO:
    if not 0 <= skip_rows <= 1000:
        raise DiagnosticError("invalid-skip-row-count")
    if not 1 <= requested_rows <= MAX_REQUESTED_ROWS:
        raise DiagnosticError("invalid-requested-row-count")
    for _ in range(skip_rows):
        line = stream.readline(max_line_bytes + 1)
        if not line or len(line) > max_line_bytes or not line.endswith(b"\n"):
            raise DiagnosticError("preamble-row-incomplete")
    rows: list[bytes] = []
    for _ in range(requested_rows):
        line = stream.readline(max_line_bytes + 1)
        if not line or len(line) > max_line_bytes or not line.endswith(b"\n"):
            raise DiagnosticError("requested-row-incomplete")
        rows.append(line)
    return BytesIO(b"".join(rows))


def classify_stream(
    stream: BinaryLineStream,
    *,
    skip_rows: int,
    requested_rows: int,
    limits: RowStructureLimits | None = None,
    include_parser_probe: bool = True,
) -> dict[str, object]:
    """Read one bounded prefix from ``stream`` and classify it exactly once.

    The caller owns the already-open binary stream.  Prefix routing and row
    classification live at this boundary so callers cannot accidentally apply
    the preamble skip twice or pass the header into the classifier.
    """

    actual_limits = limits or RowStructureLimits()
    prefix = _read_prefix(
        stream,
        skip_rows=skip_rows,
        requested_rows=requested_rows,
        max_line_bytes=actual_limits.max_line_bytes,
    )
    return classify_rows(
        prefix,
        requested_row_count=requested_rows,
        limits=actual_limits,
        include_parser_probe=include_parser_probe,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-rows", type=int, default=0)
    parser.add_argument("--rows", type=int, default=32)
    parser.add_argument("--max-line-bytes", type=int, default=DEFAULT_MAX_LINE_BYTES)
    parser.add_argument("--max-total-bytes", type=int, default=DEFAULT_MAX_TOTAL_BYTES)
    args = parser.parse_args(argv)
    try:
        limits = RowStructureLimits(
            max_rows=MAX_REQUESTED_ROWS,
            max_total_bytes=args.max_total_bytes,
            max_line_bytes=args.max_line_bytes,
        )
        result = classify_stream(
            sys.stdin.buffer,
            skip_rows=args.skip_rows,
            requested_rows=args.rows,
            limits=limits,
        )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (DiagnosticError, OSError, ValueError) as error:
        print(
            json.dumps({"error": getattr(error, "reason", type(error).__name__)}, sort_keys=True),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
