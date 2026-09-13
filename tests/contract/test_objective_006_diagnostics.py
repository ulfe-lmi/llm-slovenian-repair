"""Synthetic contract tests for content-free objective-006 row diagnosis."""

from __future__ import annotations

import json
import sys
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Any, Protocol, cast

import pytest

ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.diagnose_unigram_rows import (  # noqa: E402
    ABSOLUTE_COUNT_COLUMNS,
    DEFAULT_MAX_LINE_BYTES,
    NUMERIC_CATEGORY_ORDER,
    NUMERIC_COLUMNS,
    NUMERIC_MARKER_CATEGORY_ORDER,
    PUBLISHED_DECIMAL_COLUMNS,
    DiagnosticError,
    NumericTokenCategory,
    RowStructureLimits,
    classify_identity_token,
    classify_numeric_marker,
    classify_numeric_rows,
    classify_numeric_token,
    classify_rows,
    classify_stream,
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


class ReadableBinary(Protocol):
    def readline(self, size: int = -1, /) -> bytes: ...


class CountingBinaryStream:
    def __init__(self, stream: ReadableBinary) -> None:
        self.stream = stream
        self.readline_calls = 0

    def readline(self, size: int = -1, /) -> bytes:
        self.readline_calls += 1
        return self.stream.readline(size)


def diagnostic_rows() -> list[bytes]:
    variants = (
        row(),
        row(terminal_tabs=1),
        row(terminal_tabs=2),
        row(field_count=29),
        row(embedded_tab=True),
        row(escaped_quote=True),
        row(quoted=False),
    )
    return [variants[index % len(variants)] for index in range(32)]


def synthetic_member() -> bytes:
    return b"# synthetic preamble\r\n" * 14 + b'"synthetic header"\r\n' + b"".join(
        diagnostic_rows()
    )


def test_classify_stream_routes_one_prefix_and_classifies_once() -> None:
    stream = CountingBinaryStream(
        BytesIO(b"# preamble\r\n" * 15 + b"".join(diagnostic_rows()))
    )
    result = classify_stream(stream, skip_rows=15, requested_rows=32)

    assert stream.readline_calls == 15 + 32
    assert result["requested_row_count"] == result["read_row_count"] == 32


def test_double_skip_and_header_inclusion_are_distinguishable() -> None:
    rows = diagnostic_rows()
    header = b'"synthetic header"\r\n'
    with pytest.raises(DiagnosticError, match="requested-row-incomplete"):
        classify_stream(
            CountingBinaryStream(BytesIO(b"".join(rows))), skip_rows=14, requested_rows=32
        )

    included_header = classify_stream(
        CountingBinaryStream(BytesIO(b"# preamble\r\n" * 14 + header + b"".join(rows))),
        skip_rows=14,
        requested_rows=32,
    )
    assert included_header["read_row_count"] == 32
    assert included_header["csv_field_count_histogram"] == {
        "1": 1,
        "28": 17,
        "29": 9,
        "30": 5,
    }
    assert included_header["first_structurally_failing_source_line_number"] == 1


def test_zip_member_routes_fifteen_lines_and_thirty_two_rows_without_output(
    tmp_path: Path,
) -> None:
    archive = BytesIO()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as handle:
        handle.writestr("synthetic/member.tsv", synthetic_member())

    with zipfile.ZipFile(BytesIO(archive.getvalue())) as handle, handle.open(
        "synthetic/member.tsv"
    ) as member:
        counted = CountingBinaryStream(member)
        result = classify_stream(counted, skip_rows=15, requested_rows=32)

    assert counted.readline_calls == 15 + 32
    assert result["read_row_count"] == 32
    terminal_histogram = cast(dict[str, int], result["terminal_tab_count_histogram"])
    field_histogram = cast(dict[str, int], result["csv_field_count_histogram"])
    assert sum(terminal_histogram.values()) == 32
    assert sum(field_histogram.values()) == 32
    assert result["first_structurally_failing_source_line_number"] == 4
    assert cast(int, result["nonempty_field_after_28_count"]) > 0
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True)
    assert "synthetic-" not in rendered
    assert not list(tmp_path.iterdir())


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


def test_numeric_token_priority_is_fixed_and_mutually_exclusive() -> None:
    expected = {
        "": NumericTokenCategory.EMPTY,
        "123": NumericTokenCategory.ASCII_DIGITS,
        "12.34": NumericTokenCategory.ASCII_DECIMAL_DOT,
        "12,34": NumericTokenCategory.ASCII_DECIMAL_COMMA,
        "1.234": NumericTokenCategory.ASCII_GROUPED_DOT_TRIPLETS,
        "1,234": NumericTokenCategory.ASCII_GROUPED_COMMA_TRIPLETS,
        "1 234": NumericTokenCategory.ASCII_GROUPED_SPACE_TRIPLETS,
        "1\u00a0234": NumericTokenCategory.UNICODE_SPACE_GROUPED_TRIPLETS,
        "1.2e3": NumericTokenCategory.ASCII_SCIENTIFIC_DOT,
        "1,2e3": NumericTokenCategory.ASCII_SCIENTIFIC_COMMA,
        "+123": NumericTokenCategory.SIGN_PREFIX,
        "123%": NumericTokenCategory.PERCENT_SUFFIX,
        " 123 ": NumericTokenCategory.LEADING_OR_TRAILING_WHITESPACE,
        "NaN": NumericTokenCategory.OTHER_ASCII,
        "ž": NumericTokenCategory.OTHER_UNICODE,
    }
    assert all(
        classify_numeric_token(value.encode("utf-8")) is category
        for value, category in expected.items()
    )
    assert tuple(expected.values()) == tuple(NUMERIC_CATEGORY_ORDER)


def numeric_row(values: dict[int, str]) -> bytes:
    row_values = [f"identity-{column}" for column in range(1, 29)]
    for column in ABSOLUTE_COUNT_COLUMNS:
        row_values[column - 1] = "1"
    for column in PUBLISHED_DECIMAL_COLUMNS:
        row_values[column - 1] = "1.2"
    for column, value in values.items():
        row_values[column - 1] = value
    return row_values_bytes(row_values)


def row_values_bytes(values: list[str]) -> bytes:
    return b"\t".join(
        b'"' + value.encode("utf-8").replace(b'"', b'""') + b'"' for value in values
    ) + b"\r\n"


def test_numeric_profile_conserves_all_24_columns_and_is_content_free() -> None:
    categories = (
        "",
        "123",
        "12.34",
        "12,34",
        "1.234",
        "1,234",
        "1 234",
        "1\u00a0234",
        "1.2e3",
        "1,2e3",
        "+123",
        "123%",
        " 123 ",
        "NaN",
        "ž",
    )
    rows = [
        numeric_row(
            {
                column: categories[(row + column) % len(categories)]
                for column in NUMERIC_COLUMNS
            }
        )
        for row in range(len(categories))
    ]
    first = classify_numeric_rows(BytesIO(b"".join(rows)), requested_row_count=len(rows))
    second = classify_numeric_rows(BytesIO(b"".join(rows)), requested_row_count=len(rows))
    assert first == second
    assert first["row_count"] == len(categories)
    assert first["numeric_cell_count"] == len(categories) * 24
    assert first["absolute_count_cell_count"] == len(categories) * 8
    assert first["published_decimal_cell_count"] == len(categories) * 16
    histograms = cast(dict[str, dict[str, object]], first["column_histograms"])
    assert set(histograms) == {str(column) for column in NUMERIC_COLUMNS}
    for item in histograms.values():
        category_histogram = cast(dict[str, int], item["category_histogram"])
        assert set(category_histogram) == {category.value for category in NUMERIC_CATEGORY_ORDER}
        assert sum(category_histogram.values()) == len(categories)
    compatibility = cast(dict[str, dict[str, int]], first["current_parser_compatibility"])
    assert sum(
        item["compatible_cell_count"] + item["incompatible_cell_count"]
        for item in compatibility.values()
    ) == first["numeric_cell_count"]
    rendered = json.dumps(first, ensure_ascii=False, sort_keys=True)
    assert all(fragment not in rendered for fragment in categories if fragment)
    assert not any(
        key in rendered
        for key in (
            "token",
            "digits",
            "prefixes",
            "suffixes",
            "code_points",
            "byte_substrings",
        )
    )


def test_numeric_profile_first_incompatible_is_row_and_column_ordered() -> None:
    rows = [numeric_row({}), numeric_row({5: "12,34"}), numeric_row({})]
    result = classify_numeric_rows(BytesIO(b"".join(rows)), requested_row_count=3)
    assert result["first_incompatible"] == {
        "row_ordinal": 2,
        "column": 5,
        "semantic_kind": "absolute_count",
        "category": "ASCII_DECIMAL_COMMA",
    }
    assert result["current_parser_compatibility"] == {
        "absolute_count": {"compatible_cell_count": 23, "incompatible_cell_count": 1},
        "published_decimal": {"compatible_cell_count": 48, "incompatible_cell_count": 0},
    }


def test_numeric_profile_rejects_structure_before_any_profile() -> None:
    malformed = numeric_row({5: "1"})[:-2] + b"\n"
    with pytest.raises(DiagnosticError, match="numeric-structure-invalid"):
        classify_numeric_rows(BytesIO(malformed), requested_row_count=1)


def test_numeric_marker_refinement_covers_fixed_priority_and_no_content() -> None:
    expected = {
        b"-": "HYPHEN_MINUS",
        b"--": "REPEATED_HYPHEN_MINUS",
        b".": "DOT",
        b"..": "REPEATED_DOT",
        b"/": "SLASH",
        b"%%": "PERCENT_ONLY",
        b"ABC": "ASCII_LETTERS_ONLY",
        b"A1": "ASCII_ALNUM",
        b"?!": "ASCII_PUNCTUATION_OTHER",
        b"A-": "ASCII_MIXED_OTHER",
    }
    assert tuple(category.value for category in NUMERIC_MARKER_CATEGORY_ORDER) == tuple(
        expected.values()
    )
    assert {classify_numeric_marker(value).value for value in expected} == set(expected.values())


def test_numeric_profile_refines_marker_row_and_identity_relations() -> None:
    row_one = ["Forma", "forma", "FORMA", "NOUN"] + ["NaN"] * 24
    row_two = ["Other", "other", "OTHER", "NOUN"] + ["NaN"] * 24
    row_three = ["Different", "lemma", "lower", "VERB"] + ["NaN"] * 24
    data = row_values_bytes(row_one) + row_values_bytes(row_two) + row_values_bytes(row_three)
    result = classify_numeric_rows(
        BytesIO(data),
        requested_row_count=3,
    )
    profile = cast(dict[str, object], result["row_1_marker_profile"])
    assert profile["other_ascii_marker_cell_count"] == 24
    assert profile["distinct_numeric_marker_count"] == 1
    assert profile["all_numeric_markers_identical"] is True
    assert set(cast(dict[str, str], profile["refinement_by_column"]).values()) == {
        "ASCII_LETTERS_ONLY"
    }
    family_profiles = cast(dict[str, dict[str, object]], profile["family_profiles"])
    assert set(family_profiles) == {"absolute", "share", "relative"}
    assert all(item["distinct_marker_count"] == 1 for item in family_profiles.values())
    assert all(cast(dict[str, bool], profile["same_column_marker_recurrence"]).values())
    identity = cast(dict[str, object], profile["identity_profile"])
    assert identity["nonempty_mask"] == "1111"
    assert identity["equality_pattern"] == "ALL_DISTINCT"
    assert identity["pos_shape_category"] == "ASCII_LETTERS"
    assert identity["nfc_casefold_relations"] == {
        "form_equals_lemma": True,
        "form_equals_lowercase_lemma": True,
        "lemma_equals_lowercase_lemma": True,
    }
    assert profile["identity_profile_matches_rows_2_to_32"] == 1
    assert profile["evidence_predicates"] == ["NUMERIC_MARKERS_UNIFORM"]
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True)
    assert all(sentinel not in rendered for sentinel in ("Forma", "NaN", "Different", "NOUN"))
    assert not any(
        field in rendered
        for field in ("token", "value", "raw", "length", "hash", "record")
    )


def test_identity_categories_cover_all_closed_values() -> None:
    values = ("", "ABC", "ž", "!?", "123", "A-1")
    assert tuple(classify_identity_token(value).value for value in values) == (
        "EMPTY",
        "ASCII_LETTERS",
        "UNICODE_LETTERS",
        "ASCII_PUNCTUATION",
        "ALNUM",
        "MIXED",
    )


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


def test_complete_real_receipt_has_count_consistent_aggregate_and_new_identity() -> None:
    receipt = json.loads(
        (ROOT / "resources/source-acquisitions/gigafida-2.0-words-006-e.json").read_text(
            encoding="utf-8"
        )
    )
    prior = json.loads(
        (ROOT / "resources/source-acquisitions/gigafida-2.0-words-006-d.json").read_text(
            encoding="utf-8"
        )
    )
    assert receipt["receipt_id"] == "gigafida-2.0-words-006-e"
    assert receipt["receipt_id"] != prior["receipt_id"]
    assert receipt["status"] == "COMPLETE_ROW_DIAGNOSTIC"
    assert receipt["acquisition_evidence"]["006_e_get_count"] == 1
    assert receipt["acquisition_evidence"]["cumulative_observed_objective_get_count"] == 7
    assert receipt["acquisition_evidence"]["prefix_invocation"] == {
        "mode": "direct ZipFile.open member stream",
        "skip_rows": 15,
        "requested_rows": 32,
        "logical_readline_count": 47,
    }
    assert receipt["real_importer_smoke"]["runs_completed"] == 0
    assert receipt["source_data_retained"] is False
    assert receipt["redistribution_ready"] is False
    assert "implementation_head" not in receipt

    aggregate = receipt["structural_diagnostic"]["aggregate"]
    expected_keys = {
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
    assert set(aggregate) == expected_keys
    assert aggregate["schema_version"] == 1
    assert aggregate["requested_row_count"] == aggregate["read_row_count"] == 32
    count_keys = {
        "utf8_valid_row_count",
        "utf8_invalid_row_count",
        "crlf_row_count",
        "lf_row_count",
        "missing_newline_row_count",
        "empty_final_field_count",
        "nonempty_field_after_28_count",
        "fully_all_fields_quoted_count",
        "embedded_tab_in_quoted_field_row_count",
        "quote_parse_error_count",
    }
    for key in count_keys:
        value = aggregate[key]
        assert type(value) is int
        assert 0 <= value <= 32

    for key, expected_histogram_keys in {
        "terminal_tab_count_histogram": {"0", "1", "2+"},
        "csv_field_count_histogram": {"28", "29"},
    }.items():
        histogram = aggregate[key]
        assert set(histogram) == expected_histogram_keys
        assert all(type(value) is int and 0 <= value <= 32 for value in histogram.values())
        assert sum(histogram.values()) == 32
    parser_histogram = aggregate["existing_parser_failure_reason_histogram"]
    assert all(isinstance(key, str) for key in parser_histogram)
    assert all(type(value) is int and 0 <= value <= 32 for value in parser_histogram.values())
    assert sum(parser_histogram.values()) <= 32

    minimum = aggregate["min_whole_row_byte_length"]
    maximum = aggregate["max_whole_row_byte_length"]
    assert type(minimum) is int and type(maximum) is int
    assert 0 < minimum <= maximum <= DEFAULT_MAX_LINE_BYTES
    first_failure = aggregate["first_structurally_failing_source_line_number"]
    assert first_failure is None or 1 <= first_failure <= 32

    forbidden = {"fields", "values", "raw", "row_hash", "decoded_strings"}

    def keys(value: object) -> list[str]:
        if isinstance(value, dict):
            nested = [item for child in value.values() for item in keys(child)]
            return [key for key in value] + nested
        if isinstance(value, list):
            return [item for child in value for item in keys(child)]
        return []

    assert not forbidden.intersection(keys(receipt))
