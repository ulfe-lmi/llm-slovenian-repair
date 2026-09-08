"""Offline contract tests for the verifier-first real-prefix smoke boundary."""

from __future__ import annotations

import json
import subprocess
import sys
import warnings
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from llm_slovenian_repair.unigram_importer import EXPECTED_HEADER  # noqa: E402
from scripts import smoke_unigram_prefix as smoke  # noqa: E402
from scripts import verify_source_artifact as verifier  # noqa: E402


def quote_row(values: list[str] | tuple[str, ...], *, terminal_tab: bool = False) -> bytes:
    encoded = ("\t".join('"' + value.replace('"', '""') + '"' for value in values)).encode()
    return encoded + (b"\t" if terminal_tab else b"") + b"\r\n"


def valid_row(index: int) -> list[str]:
    values = [f"value-{index}-{column}" for column in range(28)]
    for column in (4, 7, 10, 13, 16, 19, 22, 25):
        values[column] = "0"
    for column in (5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 23, 24, 26, 27):
        values[column] = "0.1"
    return values


def prefix_bytes(rows: list[list[str]] | None = None) -> bytes:
    lines = [f"# synthetic preamble {index:02d}".encode() + b"\r\n" for index in range(14)]
    lines.append(quote_row(EXPECTED_HEADER))
    selected_rows = rows if rows is not None else [valid_row(index) for index in range(32)]
    lines.extend(
        quote_row(row, terminal_tab=index == 0) for index, row in enumerate(selected_rows)
    )
    return b"".join(lines)


def write_archive(root: Path, content: bytes, *, member: str = smoke.EXPECTED_MEMBER_NAME) -> Path:
    path = root / "source.zip"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for index in range(4):
            archive.writestr(f"other-{index}.txt", b"owned synthetic metadata")
        archive.writestr(member, content)
    return path


def evidence_for(archive: Path) -> verifier.ArtifactVerification:
    return verifier.ArtifactVerification(
        source_id="gigafida-2.0-words",
        byte_size=smoke.EXPECTED_ARCHIVE_BYTE_SIZE,
        md5=smoke.EXPECTED_ARCHIVE_MD5,
        sha256=smoke.EXPECTED_ARCHIVE_SHA256,
        member_count=smoke.EXPECTED_MEMBER_COUNT,
        total_uncompressed_size=smoke.EXPECTED_TOTAL_UNCOMPRESSED_SIZE,
    )


def test_verified_prefix_opens_one_member_and_imports_twice(tmp_path: Path) -> None:
    archive = write_archive(tmp_path, prefix_bytes())
    result = smoke._run_verified_prefix(archive, evidence_for(archive))

    assert result["status"] == "COMPLETE_REAL_PREFIX_SMOKE"
    assert result["prefix"] == {
        "member": smoke.EXPECTED_MEMBER_NAME,
        "preamble_lines": 14,
        "header_byte_length": 834,
        "header_sha256": smoke.EXPECTED_HEADER_SHA256,
        "data_rows": 32,
        "readline_calls": 47,
        "envelope_bytes": len(prefix_bytes()),
    }
    aggregate = result["structural_aggregate"]
    assert isinstance(aggregate, dict)
    assert aggregate["utf8_valid_row_count"] == 32
    assert aggregate["crlf_row_count"] == 32
    assert aggregate["csv_field_count_histogram"] == {"28": 31, "29": 1}
    assert aggregate["terminal_tab_count_histogram"] == {"0": 31, "1": 1, "2+": 0}
    assert aggregate["empty_final_field_count"] == 1
    assert aggregate["nonempty_field_after_28_count"] == 0
    assert aggregate["embedded_tab_in_quoted_field_row_count"] == 0
    assert aggregate["quote_parse_error_count"] == 0
    assert aggregate["first_structurally_failing_source_line_number"] is None
    imported = result["real_importer_smoke"]
    assert isinstance(imported, dict)
    assert imported["attempts"] == imported["runs_completed"] == 2
    assert imported["sampled_row_count"] == 32
    assert imported["results_equal"] is True
    assert imported["summary_bindings_equal"] is True
    assert all(
        isinstance(imported[key], str) and len(imported[key]) == 64
        for key in ("input_sha256", "output_sha256")
    )
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True)
    assert "value-0-0" not in rendered
    assert "header_values" not in rendered
    assert "records" not in rendered


@pytest.mark.parametrize(
    ("mutator", "reason"),
    [
        (lambda data: data[: -len(b"\r\n")], "row-incomplete"),
        (
            lambda data: data.replace(quote_row(EXPECTED_HEADER), b'"wrong"\r\n', 1),
            "header-mismatch",
        ),
    ],
)
def test_prefix_shape_failures_are_content_free(
    tmp_path: Path, mutator: object, reason: str
) -> None:
    data = mutator(prefix_bytes())  # type: ignore[operator]
    archive = write_archive(tmp_path, data)
    with pytest.raises(smoke.PrefixSmokeError, match=reason):
        smoke._run_verified_prefix(archive, evidence_for(archive))


def test_preamble_and_line_bounds_fail_closed(tmp_path: Path) -> None:
    preamble = prefix_bytes().replace(b"# synthetic preamble 00\r\n", b"# broken", 1)
    archive = write_archive(tmp_path, preamble)
    with pytest.raises(smoke.PrefixSmokeError, match="header-mismatch"):
        smoke._run_verified_prefix(archive, evidence_for(archive))

    long_row = valid_row(0)
    long_row[0] = "x" * smoke.MAX_PREFIX_LINE_BYTES
    oversized_line = prefix_bytes([long_row] + [valid_row(index) for index in range(1, 32)])
    archive = write_archive(tmp_path, oversized_line, member="line-bound.bin")
    with pytest.raises(smoke.PrefixSmokeError, match="member-missing"):
        smoke._run_verified_prefix(archive, evidence_for(archive))

    archive = write_archive(tmp_path, oversized_line)
    with pytest.raises(smoke.PrefixSmokeError, match="row-incomplete"):
        smoke._run_verified_prefix(archive, evidence_for(archive))


def test_prefix_envelope_bound_is_independent_of_line_bound(tmp_path: Path) -> None:
    rows = []
    for index in range(32):
        value = valid_row(index)
        value[0] = "x" * 132_000
        rows.append(value)
    archive = write_archive(tmp_path, prefix_bytes(rows))
    with pytest.raises(smoke.PrefixSmokeError, match="prefix-too-large"):
        smoke._run_verified_prefix(archive, evidence_for(archive))


@pytest.mark.parametrize(
    ("member", "reason"),
    [("missing", "member-missing"), ("wrong", "member-wrong")],
)
def test_selected_member_identity_is_required(
    tmp_path: Path, member: str, reason: str
) -> None:
    name = "wrong.tsv" if member == "wrong" else "other.bin"
    archive = write_archive(tmp_path, prefix_bytes(), member=name)
    with pytest.raises(smoke.PrefixSmokeError, match=reason):
        smoke._run_verified_prefix(archive, evidence_for(archive))


def test_duplicate_selected_member_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "duplicate.zip"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as handle:
            for index in range(4):
                handle.writestr(f"other-{index}.txt", b"owned synthetic metadata")
            handle.writestr(smoke.EXPECTED_MEMBER_NAME, prefix_bytes())
            handle.writestr(smoke.EXPECTED_MEMBER_NAME, prefix_bytes())
    with pytest.raises(smoke.PrefixSmokeError, match="member-duplicate"):
        smoke._run_verified_prefix(archive, evidence_for(archive))


def test_structural_and_importer_failures_are_distinct(tmp_path: Path) -> None:
    bad_shape = valid_row(0)
    bad_shape.append("nonempty")
    archive = write_archive(
        tmp_path, prefix_bytes([bad_shape] + [valid_row(index) for index in range(1, 32)])
    )
    with pytest.raises(smoke.PrefixSmokeError, match="structural-aggregate-mismatch"):
        smoke._run_verified_prefix(archive, evidence_for(archive))

    bad_import = valid_row(0)
    bad_import[0] = ""
    archive = write_archive(
        tmp_path, prefix_bytes([bad_import] + [valid_row(index) for index in range(1, 32)])
    )
    with pytest.raises(smoke.PrefixSmokeError, match="import-record-invalid"):
        smoke._run_verified_prefix(archive, evidence_for(archive))


@pytest.mark.parametrize("kind", ["symlink", "directory"])
def test_public_path_verification_stops_before_member_access(
    tmp_path: Path, kind: str
) -> None:
    target = tmp_path / "artifact"
    if kind == "symlink":
        target.symlink_to(ROOT / "resources/source-inventory-v1.json")
    else:
        target.mkdir()
    with pytest.raises(smoke.PrefixSmokeError, match="verify-artifact-(symlink|not-regular)"):
        smoke.run_smoke(
            ROOT / "resources/source-inventory-v1.json", smoke.EXPECTED_SOURCE_ID, target
        )


def test_006_g_receipt_preserves_verifier_and_helper_stop_without_content() -> None:
    receipt = json.loads(
        (
            ROOT
            / "resources/source-acquisitions/gigafida-2.0-words-006-g.json"
        ).read_text(encoding="utf-8")
    )
    assert receipt["schema_version"] == 1
    assert receipt["receipt_id"] == "gigafida-2.0-words-006-g"
    assert receipt["status"] == "BLOCKED_SMOKE_HELPER_IMPORT"
    assert receipt["acquisition_evidence"]["006_g_get_count"] == 1
    assert receipt["acquisition_evidence"]["cumulative_observed_objective_get_count"] == 9
    assert receipt["acquisition_evidence"]["verifier_before_member_access"] is True
    assert receipt["acquisition_evidence"]["accepted_offline_verifier"] == "PASSED"
    assert receipt["acquisition_evidence"]["member_access_attempted"] is False
    assert receipt["acquisition_evidence"]["temporary_tree_absent"] is True
    assert receipt["acquisition_evidence"]["source_data_retained"] is False
    assert receipt["redistribution_ready"] is False
    assert receipt["structural_sample"]["aggregate"] is None
    assert receipt["real_importer_smoke"]["attempts"] == 0
    assert receipt["real_importer_smoke"]["runs_completed"] == 0
    assert receipt["real_importer_smoke"]["sampled_row_count"] is None
    assert receipt["real_importer_smoke"]["input_sha256"] is None
    assert receipt["real_importer_smoke"]["output_sha256"] is None
    assert (
        receipt["real_importer_smoke"]["configured_provenance"]["import_completeness"]
        == "PARTIAL"
    )
    assert receipt["prior_rounds"]["006_f"]["failure"].startswith(
        "SMOKE_HARNESS_SYNTAX_ERROR"
    )

    forbidden = {
        "fields",
        "values",
        "raw",
        "row_hash",
        "decoded_strings",
        "source_rows",
        "header_values",
    }

    def keys(value: object) -> list[str]:
        if isinstance(value, dict):
            nested = [item for child in value.values() for item in keys(child)]
            return [key for key in value] + nested
        if isinstance(value, list):
            return [item for child in value for item in keys(child)]
        return []

    assert not forbidden.intersection(keys(receipt))


def test_verifier_identity_is_required_before_member_access(tmp_path: Path) -> None:
    archive = write_archive(tmp_path, prefix_bytes())
    wrong = verifier.ArtifactVerification(
        source_id="gigafida-2.0-words",
        byte_size=1,
        md5=smoke.EXPECTED_ARCHIVE_MD5,
        sha256=smoke.EXPECTED_ARCHIVE_SHA256,
        member_count=5,
        total_uncompressed_size=smoke.EXPECTED_TOTAL_UNCOMPRESSED_SIZE,
    )
    with pytest.raises(smoke.PrefixSmokeError, match="artifact-identity-mismatch"):
        smoke._run_verified_prefix(archive, wrong)


def test_cli_serializes_only_bounded_error(tmp_path: Path) -> None:
    archive = write_archive(tmp_path, prefix_bytes())
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/smoke_unigram_prefix.py",
            "--inventory",
            str(ROOT / "resources/source-inventory-v1.json"),
            "--source-id",
            "wrong-source",
            "--artifact",
            str(archive),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert json.loads(completed.stderr) == {"error": "source-id-not-canonical"}
    assert completed.stdout == ""
