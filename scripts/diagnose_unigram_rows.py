"""Content-free structural diagnosis for a bounded unigram row prefix.

The public classifier accepts a caller-owned binary stream.  It never opens a
path, contacts a source, writes a file, or returns decoded field data.  The
command-line wrapper reads a bounded prefix from standard input so a verified
archive/member reader can remain outside this module.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from io import BytesIO
from typing import BinaryIO, Final, Protocol

SCHEMA_VERSION: Final = 1
MAX_REQUESTED_ROWS: Final = 32
DEFAULT_MAX_TOTAL_BYTES: Final = 4 * 1024 * 1024
DEFAULT_MAX_LINE_BYTES: Final = 256 * 1024
_DIAGNOSTIC_INVENTORY_SHA256: Final = "a" * 64
_DIAGNOSTIC_ACQUISITION_SHA256: Final = "b" * 64


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
