"""Offline contract tests for the bounded Gigafida unigram importer."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

import pytest

from llm_slovenian_repair.contracts import EvidenceCompleteness
from llm_slovenian_repair.unigram_importer import (
    EXPECTED_HEADER,
    EXPECTED_HEADER_BYTE_LENGTH,
    EXPECTED_HEADER_SHA256,
    REAL_ACQUISITION_SHA256,
    REAL_INVENTORY_REVISION,
    REAL_INVENTORY_SHA256,
    REAL_RELEASE,
    REAL_SOURCE_ID,
    REAL_SOURCE_NAME,
    SYNTHETIC_INVENTORY_REVISION,
    SYNTHETIC_RELEASE,
    SYNTHETIC_SOURCE_ID,
    SYNTHETIC_SOURCE_NAME,
    UnigramImportError,
    UnigramImportFailure,
    UnigramImportLimits,
    UnigramImportResult,
    UnigramImportSummary,
    UnigramProvenance,
    UnigramRecord,
    import_unigrams,
)

ROOT = Path(__file__).parents[2]
FIXTURE = ROOT / "tests" / "fixtures" / "unigram" / "synthetic-gigafida.tsv"
SYNTHETIC_INVENTORY_SHA256 = "80ace517557091e9383b881320857b7c233b339bf7a6fca2fe5a8799b1e5bfcd"
SYNTHETIC_ACQUISITION_SHA256 = "84277bb10e13be1984c5929af20fffd3362349488d5366286a0ed75ca4783e0b"


def quote_row(values: list[str] | tuple[str, ...]) -> bytes:
    return ("\t".join('"' + value.replace('"', '""') + '"' for value in values)).encode(
        "utf-8"
    )


def fixture_bytes() -> bytes:
    # apply_patch stores text fixtures with the repository's LF convention;
    # the contract boundary receives the observed source CRLF bytes.
    return FIXTURE.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")


def rows_from_fixture() -> list[list[str]]:
    lines = fixture_bytes().splitlines()
    return [
        next(csv.reader([line.decode("utf-8")], delimiter="\t", quotechar='"'))
        for line in lines[15:]
    ]


def provenance(**changes: Any) -> UnigramProvenance:
    values: dict[str, Any] = {
        "provenance_kind": "project-synthetic",
        "source_id": SYNTHETIC_SOURCE_ID,
        "source_name": SYNTHETIC_SOURCE_NAME,
        "release": SYNTHETIC_RELEASE,
        "source_inventory_revision": SYNTHETIC_INVENTORY_REVISION,
        "source_inventory_sha256": SYNTHETIC_INVENTORY_SHA256,
        "acquisition_sha256": SYNTHETIC_ACQUISITION_SHA256,
        "evidence_scope": "complete project-authored synthetic query",
        "source_completeness": EvidenceCompleteness.COMPLETE,
        "query_completeness": EvidenceCompleteness.COMPLETE,
        "import_completeness": EvidenceCompleteness.COMPLETE,
    }
    values.update(changes)
    return UnigramProvenance(**values)


def real_provenance(**changes: Any) -> UnigramProvenance:
    values: dict[str, Any] = {
        "provenance_kind": "real",
        "source_id": REAL_SOURCE_ID,
        "source_name": REAL_SOURCE_NAME,
        "release": REAL_RELEASE,
        "source_inventory_revision": REAL_INVENTORY_REVISION,
        "source_inventory_sha256": REAL_INVENTORY_SHA256,
        "acquisition_sha256": REAL_ACQUISITION_SHA256,
        "evidence_scope": "publisher-declared release scope; bounded compatibility prefix",
        "source_completeness": EvidenceCompleteness.COMPLETE,
        "query_completeness": EvidenceCompleteness.COMPLETE,
        "import_completeness": EvidenceCompleteness.PARTIAL,
    }
    values.update(changes)
    return UnigramProvenance(**values)


def payload(
    rows: list[list[str]] | None = None,
    *,
    header: tuple[str, ...] = EXPECTED_HEADER,
    line_ending: bytes = b"\r\n",
    include_preamble: bool = True,
) -> bytes:
    base_rows = rows if rows is not None else rows_from_fixture()
    lines: list[bytes] = []
    if include_preamble:
        lines.extend(
            f"# project-authored synthetic metadata {index:02d}".encode()
            for index in range(1, 15)
        )
    lines.append(quote_row(header))
    lines.extend(quote_row(row) for row in base_rows)
    return line_ending.join(lines) + line_ending


def positive_row() -> list[str]:
    row = rows_from_fixture()[0]
    for index in (4, 7, 10, 13, 16, 19, 22, 25):
        row[index] = "1"
    for index in (5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 23, 24, 26, 27):
        row[index] = "0.1"
    return row


def expect_failure(data: bytes | str, reason: UnigramImportFailure, **kwargs: Any) -> None:
    stream = StringIO(data) if isinstance(data, str) else BytesIO(data)
    with pytest.raises(UnigramImportError, match=reason.value):
        import_unigrams(stream, provenance(**kwargs))


def test_observed_header_contract_is_exact() -> None:
    header_bytes = quote_row(EXPECTED_HEADER) + b"\r\n"
    assert len(EXPECTED_HEADER) == 28
    assert len(header_bytes) == EXPECTED_HEADER_BYTE_LENGTH == 834
    assert hashlib.sha256(header_bytes).hexdigest() == EXPECTED_HEADER_SHA256


def test_shared_completeness_is_the_only_importer_completeness_type() -> None:
    assert UnigramProvenance.model_fields["source_completeness"].annotation is EvidenceCompleteness
    assert "Completeness" not in __import__(
        "llm_slovenian_repair.unigram_importer", fromlist=["__all__"]
    ).__all__


def test_real_provenance_is_exactly_bound() -> None:
    value = real_provenance()
    assert value.source_id == REAL_SOURCE_ID
    assert value.source_inventory_sha256 == REAL_INVENTORY_SHA256
    assert value.acquisition_sha256 == REAL_ACQUISITION_SHA256


@pytest.mark.parametrize(
    "changes",
    [
        {"source_id": "other-source"},
        {"source_name": "other-name"},
        {"release": "other-release"},
        {"source_inventory_revision": "other-inventory"},
        {"source_inventory_sha256": "a" * 64},
        {"acquisition_sha256": "b" * 64},
        {"header_line_number": 1},
    ],
)
def test_real_provenance_rebinding_and_line_one_are_rejected(changes: dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        real_provenance(**changes)


def test_root_import_stays_lazy_and_submodule_has_one_entry_point() -> None:
    output = subprocess.check_output(
        [
            sys.executable,
            "-c",
            "import sys, llm_slovenian_repair; "
            "print('llm_slovenian_repair.unigram_importer' in sys.modules)",
        ],
        text=True,
    ).strip()
    assert output == "False"
    import llm_slovenian_repair.unigram_importer as importer

    assert "import_unigrams" in importer.__all__
    assert "parse_unigram_tsv" not in importer.__all__
    assert "import_unigram_tsv" not in importer.__all__
    assert not hasattr(importer, "parse_unigram_tsv")
    assert not hasattr(importer, "import_unigram_tsv")


def test_synthetic_import_preserves_identity_ambiguity_and_unicode() -> None:
    result = import_unigrams(BytesIO(fixture_bytes()), provenance())

    assert len(result.records) == 5
    assert result.records[1].source_form == result.records[2].source_form == "vodi"
    assert result.records[1].record_key != result.records[2].record_key
    assert result.records[3].source_form != result.records[3].derived_lookup_form
    assert result.records[3].derived_lookup_form == "élan"
    assert result.records[0].published_decimal_text[0] == "0.1200"
    assert result.records[-1].absolute_counts == (0, 0, 0, 0, 0, 0, 0, 0)
    assert result.summary.query_completeness is EvidenceCompleteness.COMPLETE
    assert result.summary.import_completeness is EvidenceCompleteness.COMPLETE
    assert result.summary.record_count == 5
    assert result.summary.output_sha256


def test_repeated_import_is_immutable_and_deterministic() -> None:
    first = import_unigrams(BytesIO(fixture_bytes()), provenance())
    second = import_unigrams(BytesIO(fixture_bytes()), provenance())

    assert first == second
    assert first.summary.input_sha256 == second.summary.input_sha256
    assert first.summary.output_sha256 == second.summary.output_sha256
    with pytest.raises((TypeError, ValueError)):
        first.records[0].source_form = "mutated"


@pytest.mark.parametrize("field,value", [("schema_version", 99), ("importer_version", "bogus")])
def test_summary_constant_tampering_is_rejected(field: str, value: Any) -> None:
    result = import_unigrams(BytesIO(fixture_bytes()), provenance())
    summary = result.summary.model_dump()
    summary[field] = value
    with pytest.raises(ValueError):
        UnigramImportResult(
            provenance=result.provenance,
            limits=result.limits,
            records=result.records,
            summary=UnigramImportSummary(**summary),
        )


def test_summary_output_hash_tampering_is_rejected() -> None:
    result = import_unigrams(BytesIO(fixture_bytes()), provenance())
    summary = result.summary.model_dump()
    summary["output_sha256"] = "a" * 64
    with pytest.raises(ValueError):
        UnigramImportResult(
            provenance=result.provenance,
            limits=result.limits,
            records=result.records,
            summary=UnigramImportSummary(**summary),
        )


def test_record_numeric_text_and_key_tampering_is_rejected() -> None:
    result = import_unigrams(BytesIO(fixture_bytes()), provenance())
    record = result.records[0].model_dump()
    record["absolute_counts"] = (2, *record["absolute_counts"][1:])
    with pytest.raises(ValueError):
        UnigramRecord(**record)
    record = result.records[0].model_dump()
    record["published_decimal_text"] = ("9.9", *record["published_decimal_text"][1:])
    with pytest.raises(ValueError):
        UnigramRecord(**record)
    record = result.records[0].model_dump()
    record["record_key"] = "a" * 64
    with pytest.raises(ValueError):
        UnigramRecord(**record)


def test_zero_is_rejected_without_complete_query_scope() -> None:
    expect_failure(
        payload(),
        UnigramImportFailure.ZERO_WITHOUT_COMPLETE_QUERY,
        query_completeness=EvidenceCompleteness.PARTIAL,
    )


@pytest.mark.parametrize("count", ["-1", "+1", "1.0", "1e3", "True"])
def test_count_syntax_is_strict(count: str) -> None:
    row = positive_row()
    row[4] = count
    expect_failure(payload([row]), UnigramImportFailure.INVALID_COUNT)


def test_count_overflow_is_bounded() -> None:
    row = positive_row()
    row[4] = "9" * 20
    expect_failure(payload([row]), UnigramImportFailure.COUNT_OVERFLOW)


def test_decimal_is_lossless_and_strict() -> None:
    row = positive_row()
    row[5] = "NaN"
    expect_failure(payload([row]), UnigramImportFailure.INVALID_DECIMAL)


def test_duplicate_and_conflicting_composite_keys_fail() -> None:
    row = positive_row()
    expect_failure(payload([row, row.copy()]), UnigramImportFailure.DUPLICATE_RECORD)
    conflicting = row.copy()
    conflicting[4] = "2"
    expect_failure(payload([row, conflicting]), UnigramImportFailure.CONFLICTING_RECORD)


@pytest.mark.parametrize(
    ("data", "reason"),
    [
        (
            payload(header=tuple("wrong" for _ in EXPECTED_HEADER)),
            UnigramImportFailure.HEADER_MISMATCH,
        ),
        (payload([positive_row()[:-1]]), UnigramImportFailure.FIELD_COUNT),
        (
            payload([positive_row()]).replace(b'"miza"', b"miza", 1),
            UnigramImportFailure.INVALID_QUOTING,
        ),
    ],
)
def test_header_columns_and_quoting_are_strict(data: bytes, reason: UnigramImportFailure) -> None:
    expect_failure(data, reason)


def test_truncated_and_non_crlf_inputs_fail_at_stream_boundary() -> None:
    expect_failure(fixture_bytes()[:-2], UnigramImportFailure.MISSING_FINAL_NEWLINE)
    expect_failure(
        fixture_bytes().replace(b"\r\n", b"\n"),
        UnigramImportFailure.INVALID_NEWLINE,
    )


def test_invalid_utf8_control_and_surrogate_are_not_accepted() -> None:
    invalid_utf8 = fixture_bytes().replace(b'"miza"', b'"\xff"', 1)
    expect_failure(invalid_utf8, UnigramImportFailure.INVALID_UTF8)
    control = fixture_bytes().replace(b'"miza"', b'"\x00"', 1)
    expect_failure(control, UnigramImportFailure.INVALID_SOURCE_TEXT)
    surrogate = fixture_bytes().decode("utf-8").replace("miza", "\ud800", 1)
    expect_failure(surrogate, UnigramImportFailure.INVALID_SOURCE_TEXT)


@pytest.mark.parametrize(
    ("limits", "reason"),
    [
        (UnigramImportLimits(max_field_bytes=1), UnigramImportFailure.FIELD_TOO_LARGE),
        (
            UnigramImportLimits(max_line_bytes=100, max_field_bytes=100),
            UnigramImportFailure.LINE_TOO_LARGE,
        ),
        (
            UnigramImportLimits(max_input_bytes=2450, max_line_bytes=2450, max_field_bytes=2450),
            UnigramImportFailure.INPUT_TOO_LARGE,
        ),
        (UnigramImportLimits(max_rows=1), UnigramImportFailure.ROW_LIMIT),
        (UnigramImportLimits(max_fields=27), UnigramImportFailure.FIELD_COUNT),
    ],
)
def test_input_resources_are_bounded(limits: Any, reason: UnigramImportFailure) -> None:
    with pytest.raises(UnigramImportError, match=reason.value):
        import_unigrams(BytesIO(fixture_bytes()), provenance(), limits=limits)


def test_header_line_one_is_rejected_even_for_synthetic_input() -> None:
    one_line = payload([positive_row()], include_preamble=False)
    with pytest.raises(ValueError):
        provenance(header_line_number=1)
    assert one_line


def test_006_a_receipt_uses_a_git_revision_field() -> None:
    receipt = json.loads(
        (ROOT / "resources/source-acquisitions/gigafida-2.0-words-006-a.json").read_text(
            encoding="utf-8"
        )
    )
    assert receipt["status"] == "PARTIAL_RECOVERY_HANDOFF"
    assert "project_sha256_observed_locally" not in receipt
    assert len(receipt["base_revision_observed_locally"]) == 40
    assert all(
        character in "0123456789abcdef"
        for character in receipt["base_revision_observed_locally"]
    )


def test_006_b_receipt_is_finite_and_preserves_blocked_smoke() -> None:
    receipt = json.loads(
        (ROOT / "resources/source-acquisitions/gigafida-2.0-words-006-b.json").read_text(
            encoding="utf-8"
        )
    )
    assert receipt["schema_version"] == 1
    assert receipt["status"] == "BLOCKED_PARSER_INCOMPATIBILITY"
    assert receipt["acquisition_evidence"]["006_b_get_count"] == 1
    assert receipt["acquisition_evidence"]["cumulative_observed_objective_get_count"] == 4
    assert receipt["acquisition_evidence"]["006_a_exact_one_fetch_condition_satisfied"] is False
    for field in ("inventory_sha256", "archive_sha256", "header_sha256"):
        assert len(receipt[field]) == 64
        assert all(character in "0123456789abcdef" for character in receipt[field])
    assert receipt["real_importer_smoke"]["status"] == "BLOCKED"
    assert receipt["real_importer_smoke"]["sampled_row_count"] is None
    assert receipt["real_importer_smoke"]["input_sha256"] is None
    assert receipt["real_importer_smoke"]["output_sha256"] is None
    assert receipt["acquisition_evidence"]["temporary_tree_absent"] is True
    assert receipt["acquisition_evidence"]["source_data_retained"] is False


def test_fixture_is_project_authored_and_not_a_runtime_resource() -> None:
    assert "project-authored" in (FIXTURE.parent / "README.md").read_text(encoding="utf-8")
    assert "tests/fixtures" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
