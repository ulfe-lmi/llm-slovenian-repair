"""Synthetic contract tests for content-free objective-006 row diagnosis."""

from __future__ import annotations

import json
import sys
from io import BytesIO
from pathlib import Path
from typing import Any, cast

import pytest

ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.diagnose_unigram_rows import (  # noqa: E402
    DEFAULT_MAX_LINE_BYTES,
    DiagnosticError,
    RowStructureLimits,
    classify_rows,
)


def row(
    *,
    field_count: int = 28,
    terminal_tabs: int = 0,
    quoted: bool = True,
    embedded_tab: bool = False,
    escaped_quote: bool = False,
) -> bytes:
    values = [f"synthetic-{index}" for index in range(field_count)]
    if embedded_tab:
        values[0] = "left\tright"
    if escaped_quote:
        values[1] = 'escaped"quote'
    if quoted:
        encoded = b"\t".join(b'"' + value.encode().replace(b'"', b'""') + b'"' for value in values)
    else:
        encoded = b"\t".join(value.encode() for value in values)
    return encoded + (b"\t" * terminal_tabs) + b"\r\n"


def diagnosis(data: bytes, **kwargs: Any) -> dict[str, object]:
    return classify_rows(BytesIO(data), requested_row_count=kwargs.pop("requested", 1), **kwargs)


def test_exact_28_fields_without_terminal_tab_is_classified() -> None:
    result = diagnosis(row())
    assert result["read_row_count"] == 1
    assert result["terminal_tab_count_histogram"] == {"0": 1, "1": 0, "2+": 0}
    assert result["csv_field_count_histogram"] == {"28": 1}
    assert result["fully_all_fields_quoted_count"] == 1
    assert result["first_structurally_failing_source_line_number"] is None


def test_one_and_double_terminal_tabs_are_distinct_shape_evidence() -> None:
    result = diagnosis(row(terminal_tabs=1) + row(terminal_tabs=2), requested=2)
    assert result["terminal_tab_count_histogram"] == {"0": 0, "1": 1, "2+": 1}
    assert result["csv_field_count_histogram"] == {"29": 1, "30": 1}
    assert result["empty_final_field_count"] == 2
    assert result["nonempty_field_after_28_count"] == 0


def test_nonempty_field_after_28_is_not_silently_discarded() -> None:
    result = diagnosis(row(field_count=29))
    assert result["csv_field_count_histogram"] == {"29": 1}
    assert result["nonempty_field_after_28_count"] == 1
    assert result["first_structurally_failing_source_line_number"] == 1


def test_quoted_tab_and_doubled_quote_are_shape_only() -> None:
    result = diagnosis(row(embedded_tab=True) + row(escaped_quote=True), requested=2)
    assert result["embedded_tab_in_quoted_field_row_count"] == 1
    assert result["quote_parse_error_count"] == 0
    assert result["fully_all_fields_quoted_count"] == 2


def test_malformed_unclosed_quote_is_counted_and_has_first_failure() -> None:
    result = diagnosis(b'"unclosed\t"still\r\n')
    assert result["quote_parse_error_count"] == 1
    assert result["first_structurally_failing_source_line_number"] == 1
    assert result["existing_parser_failure_reason_histogram"]


def test_lf_and_missing_newline_are_counted_without_normalization() -> None:
    data = row()[:-2] + b"\n" + row()[:-2]
    result = diagnosis(data, requested=2)
    assert result["crlf_row_count"] == 0
    assert result["lf_row_count"] == 1
    assert result["missing_newline_row_count"] == 1


def test_invalid_utf8_is_counted_without_decoding_into_output() -> None:
    invalid = row().replace(b'"synthetic-0"', b'"\xff"', 1)
    result = diagnosis(invalid)
    assert result["utf8_valid_row_count"] == 0
    assert result["utf8_invalid_row_count"] == 1
    rendered = json.dumps(result, ensure_ascii=False)
    assert "synthetic-0" not in rendered
    assert "fields" not in result
    assert "values" not in result
    assert "raw" not in result


def test_mixed_sample_reports_bounded_aggregate_only_schema() -> None:
    data = row() + row(terminal_tabs=1) + row(field_count=29) + row(embedded_tab=True)
    result = diagnosis(data, requested=4)
    assert result["schema_version"] == 1
    assert result["requested_row_count"] == 4
    assert result["read_row_count"] == 4
    minimum = cast(int, result["min_whole_row_byte_length"])
    maximum = cast(int, result["max_whole_row_byte_length"])
    assert minimum <= maximum
    assert set(result) == {
        "schema_version",
        "requested_row_count",
        "read_row_count",
        "utf8_valid_row_count",
        "utf8_invalid_row_count",
        "crlf_row_count",
        "lf_row_count",
        "missing_newline_row_count",
        "terminal_tab_count_histogram",
        "csv_field_count_histogram",
        "empty_final_field_count",
        "nonempty_field_after_28_count",
        "fully_all_fields_quoted_count",
        "embedded_tab_in_quoted_field_row_count",
        "quote_parse_error_count",
        "existing_parser_failure_reason_histogram",
        "min_whole_row_byte_length",
        "max_whole_row_byte_length",
        "first_structurally_failing_source_line_number",
    }


@pytest.mark.parametrize(
    ("data", "reason"),
    [
        (b"", "no-rows"),
        (row() * 2, "more-rows-than-requested"),
        (row(), "line-too-large"),
    ],
)
def test_row_and_byte_limits_are_strict(data: bytes, reason: str) -> None:
    if reason == "more-rows-than-requested":
        with pytest.raises(DiagnosticError, match=reason):
            diagnosis(data, requested=1)
    elif reason == "line-too-large":
        long_row = row()[:-2] + (b"x" * DEFAULT_MAX_LINE_BYTES) + b"\r\n"
        with pytest.raises(DiagnosticError, match=reason):
            diagnosis(long_row, limits=RowStructureLimits(max_line_bytes=DEFAULT_MAX_LINE_BYTES))
    else:
        with pytest.raises(DiagnosticError, match=reason):
            diagnosis(data)


def test_requested_and_total_limits_reject_out_of_range_inputs() -> None:
    with pytest.raises(DiagnosticError, match="invalid-requested-row-count"):
        diagnosis(row(), requested=33)
    with pytest.raises(DiagnosticError, match="input-too-large"):
        diagnosis(row(), limits=RowStructureLimits(max_total_bytes=10, max_line_bytes=10))


def test_blocked_real_receipt_is_bounded_and_content_free() -> None:
    receipt = json.loads(
        (ROOT / "resources/source-acquisitions/gigafida-2.0-words-006-d.json").read_text(
            encoding="utf-8"
        )
    )
    assert receipt["schema_version"] == 1
    assert receipt["status"] == "BLOCKED_ROW_DIAGNOSTIC_INPUT"
    assert receipt["acquisition_evidence"]["006_d_get_count"] == 1
    assert receipt["acquisition_evidence"]["cumulative_observed_objective_get_count"] == 6
    assert receipt["acquisition_evidence"]["accepted_offline_verifier"] == "PASSED"
    assert receipt["acquisition_evidence"]["requested_complete_row_count"] == 32
    assert receipt["acquisition_evidence"]["temporary_tree_absent"] is True
    assert receipt["source_data_retained"] is False
    assert receipt["redistribution_ready"] is False
    assert receipt["structural_diagnostic"]["aggregate"] is None
    assert receipt["real_importer_smoke"]["runs_completed"] == 0
    assert receipt["real_importer_smoke"]["input_sha256"] is None
    assert receipt["real_importer_smoke"]["output_sha256"] is None
    assert "implementation_head" not in receipt

    forbidden = {"fields", "values", "raw", "row_hash", "decoded_strings"}

    def keys(value: object) -> list[str]:
        if isinstance(value, dict):
            nested = [item for child in value.values() for item in keys(child)]
            return [key for key in value] + nested
        if isinstance(value, list):
            return [item for child in value for item in keys(child)]
        return []

    assert not forbidden.intersection(keys(receipt))
