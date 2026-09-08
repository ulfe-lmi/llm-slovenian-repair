"""Run one bounded, content-free smoke over a verified Gigafida ZIP prefix.

The command-line path accepts an explicit canonical inventory and source ID. A
preflight validates the installed importer runtime without an artifact. The
smoke path additionally accepts an already-acquired artifact, verifies it
before opening the named member, captures only the observed 14-line
preamble/header/32-row prefix, and then performs two deterministic importer
calls over fresh in-memory streams. It never downloads, extracts, or emits
source fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import sys
import zipfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Protocol

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))
if str(REPOSITORY_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from scripts import diagnose_unigram_rows as diagnostics  # noqa: E402
from scripts import verify_source_artifact as verifier  # noqa: E402

MAX_PREFIX_ENVELOPE_BYTES = 4 * 1024 * 1024
MAX_PREFIX_LINE_BYTES = 256 * 1024
PREAMBLE_LINE_COUNT = 14
DATA_ROW_COUNT = 32
PREFIX_READLINE_COUNT = PREAMBLE_LINE_COUNT + 1 + DATA_ROW_COUNT

EXPECTED_ARCHIVE_BYTE_SIZE = 115865656
EXPECTED_ARCHIVE_MD5 = "b20a959f9c113aeb6504f0d753d36d10"
EXPECTED_ARCHIVE_SHA256 = "77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a"
EXPECTED_MEMBER_COUNT = 5
EXPECTED_TOTAL_UNCOMPRESSED_SIZE = 1487654024
EXPECTED_SOURCE_ID = "gigafida-2.0-words"
EXPECTED_MEMBER_NAME = (
    "GF2.0-words-all-lowercase_forms-lemmas-parts_of_speech-taxonomy-entire.tsv"
)
EXPECTED_HEADER_BYTE_LENGTH = 834
EXPECTED_HEADER_SHA256 = "c2ce44548818b72a04691c7060c0e35106393edbfde13336c60d4cd072a00638"


class PrefixSmokeError(ValueError):
    """A finite, non-content failure at the verified prefix boundary."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class PreflightError(ValueError):
    """A finite, non-content failure while checking CLI runtime readiness."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class BinaryLineStream(Protocol):
    """The bounded binary line surface needed from a ZIP member."""

    def readline(self, size: int = -1, /) -> bytes: ...


@dataclass(frozen=True, slots=True)
class PrefixEnvelope:
    data: bytes
    preamble_lines: int
    header_bytes: int
    data_rows: int
    readline_calls: int


def _fail(reason: str) -> None:
    raise PrefixSmokeError(reason)


def _preflight_fail(reason: str) -> None:
    raise PreflightError(reason)


def _canonical_verification(verification: verifier.ArtifactVerification) -> None:
    expected = (
        EXPECTED_ARCHIVE_BYTE_SIZE,
        EXPECTED_ARCHIVE_MD5,
        EXPECTED_ARCHIVE_SHA256,
        EXPECTED_MEMBER_COUNT,
        EXPECTED_TOTAL_UNCOMPRESSED_SIZE,
    )
    actual = (
        verification.source_id,
        verification.byte_size,
        verification.md5,
        verification.sha256,
        verification.member_count,
        verification.total_uncompressed_size,
    )
    if actual != (EXPECTED_SOURCE_ID, *expected):
        _fail("artifact-identity-mismatch")


def _canonical_inventory_entry(
    inventory_path: Path, source_id: str
) -> tuple[dict[str, Any], int]:
    """Load the canonical inventory and return one ID-bound entry."""

    if source_id != EXPECTED_SOURCE_ID:
        _preflight_fail("source-id-not-canonical")
    try:
        inventory = verifier.load_inventory(inventory_path)
    except verifier.InventoryError as exc:
        raise PreflightError(f"preflight-verify-{exc.reason}") from exc

    entries = [entry for entry in inventory["entries"] if entry.get("id") == source_id]
    if len(entries) != 1:
        _preflight_fail("source-entry-not-canonical")
    entry = entries[0]
    artifact = entry.get("artifact")
    if not isinstance(artifact, dict):
        _preflight_fail("source-artifact-not-canonical")
    checksum = artifact.get("repository_checksum")
    if not isinstance(checksum, dict):
        _preflight_fail("source-artifact-not-canonical")
    if (
        entry.get("source_name") != "Gigafida 2.0 word lists"
        or entry.get("release") != "2.0"
        or artifact.get("name") != "GF2.0-words-all.zip"
        or artifact.get("media_type") != "application/zip"
        or artifact.get("container_format") != "ZIP"
        or artifact.get("byte_size") != EXPECTED_ARCHIVE_BYTE_SIZE
        or checksum.get("algorithm") != "MD5"
        or checksum.get("value") != EXPECTED_ARCHIVE_MD5
    ):
        _preflight_fail("source-artifact-not-canonical")
    return entry, len(inventory["entries"])


def run_preflight(inventory_path: Path, source_id: str) -> dict[str, object]:
    """Validate the canonical inventory and installed importer runtime."""

    entry, inventory_entry_count = _canonical_inventory_entry(inventory_path, source_id)
    try:
        from llm_slovenian_repair.contracts import EvidenceCompleteness
        from llm_slovenian_repair.unigram_importer import (
            EXPECTED_DATA_RECORD_TERMINATOR,
            EXPECTED_HEADER_BYTES,
            EXPECTED_HEADER_LINE_NUMBER,
            IMPORTER_VERSION,
            REAL_ACQUISITION_SHA256,
            REAL_INVENTORY_REVISION,
            REAL_INVENTORY_SHA256,
            REAL_RELEASE,
            REAL_SOURCE_ID,
            REAL_SOURCE_NAME,
            UnigramImportLimits,
            UnigramProvenance,
            import_unigrams,
        )
        from llm_slovenian_repair.unigram_importer import (
            EXPECTED_HEADER_SHA256 as IMPORTER_HEADER_SHA256,
        )
        from llm_slovenian_repair.unigram_importer import (
            EXPECTED_MEMBER_NAME as IMPORTER_MEMBER_NAME,
        )
    except ImportError as exc:
        raise PreflightError("preflight-dependency-unavailable") from exc

    if (
        len(EXPECTED_HEADER_BYTES) != EXPECTED_HEADER_BYTE_LENGTH
        or hashlib.sha256(EXPECTED_HEADER_BYTES).hexdigest() != EXPECTED_HEADER_SHA256
        or IMPORTER_HEADER_SHA256 != EXPECTED_HEADER_SHA256
        or EXPECTED_HEADER_SHA256
        != "c2ce44548818b72a04691c7060c0e35106393edbfde13336c60d4cd072a00638"
        or EXPECTED_HEADER_BYTE_LENGTH != 834
        or IMPORTER_MEMBER_NAME != EXPECTED_MEMBER_NAME
        or EXPECTED_HEADER_LINE_NUMBER != PREAMBLE_LINE_COUNT + 1
    ):
        _preflight_fail("preflight-header-contract-invalid")

    try:
        provenance = UnigramProvenance(
            provenance_kind="real",
            source_id=REAL_SOURCE_ID,
            source_name=REAL_SOURCE_NAME,
            release=REAL_RELEASE,
            source_inventory_revision=REAL_INVENTORY_REVISION,
            source_inventory_sha256=REAL_INVENTORY_SHA256,
            acquisition_sha256=REAL_ACQUISITION_SHA256,
            evidence_scope="publisher-declared release scope; bounded compatibility prefix",
            source_completeness=EvidenceCompleteness.COMPLETE,
            query_completeness=EvidenceCompleteness.COMPLETE,
            import_completeness=EvidenceCompleteness.PARTIAL,
        )
        limits = UnigramImportLimits(
            max_input_bytes=MAX_PREFIX_ENVELOPE_BYTES,
            max_rows=DATA_ROW_COUNT,
            max_line_bytes=MAX_PREFIX_LINE_BYTES,
            max_field_bytes=MAX_PREFIX_LINE_BYTES,
        )
    except (TypeError, ValueError) as exc:
        raise PreflightError("preflight-contract-invalid") from exc

    if (
        not callable(import_unigrams)
        or provenance.source_id != EXPECTED_SOURCE_ID
        or provenance.source_name != entry["source_name"]
        or provenance.release != entry["release"]
        or provenance.source_inventory_revision != "source-inventory-v1"
        or provenance.source_inventory_sha256
        != "439bbd51e04e338569b9785c44d1b05c0ea023aae39898aa7d494568d6f49de3"
        or provenance.acquisition_sha256 != EXPECTED_ARCHIVE_SHA256
        or provenance.source_completeness is not EvidenceCompleteness.COMPLETE
        or provenance.query_completeness is not EvidenceCompleteness.COMPLETE
        or provenance.import_completeness is not EvidenceCompleteness.PARTIAL
        or limits.max_input_bytes != MAX_PREFIX_ENVELOPE_BYTES
        or limits.max_rows != DATA_ROW_COUNT
        or limits.max_line_bytes != MAX_PREFIX_LINE_BYTES
        or limits.max_field_bytes != MAX_PREFIX_LINE_BYTES
    ):
        _preflight_fail("preflight-runtime-contract-invalid")

    artifact = entry["artifact"]
    assert isinstance(artifact, dict)
    return {
        "schema_version": 1,
        "status": "READY",
        "mode": "PRE_FLIGHT",
        "inventory": {
            "id": "source-inventory-v1",
            "entry_count": inventory_entry_count,
            "source_id": entry["id"],
            "source_name": entry["source_name"],
            "release": entry["release"],
        },
        "artifact_identity": {
            "name": artifact["name"],
            "expected_byte_size": EXPECTED_ARCHIVE_BYTE_SIZE,
            "expected_md5": EXPECTED_ARCHIVE_MD5,
            "archive_sha256": EXPECTED_ARCHIVE_SHA256,
        },
        "header_contract": {
            "byte_length": EXPECTED_HEADER_BYTE_LENGTH,
            "sha256": EXPECTED_HEADER_SHA256,
            "field_count": len(EXPECTED_HEADER_BYTES.split(b"\t")),
            "line_number": EXPECTED_HEADER_LINE_NUMBER,
        },
        "importer": {
            "entry_point": "llm_slovenian_repair.unigram_importer.import_unigrams",
            "version": IMPORTER_VERSION,
            "limits": {
                "max_input_bytes": limits.max_input_bytes,
                "max_rows": limits.max_rows,
                "max_line_bytes": limits.max_line_bytes,
                "max_field_bytes": limits.max_field_bytes,
                "max_fields": limits.max_fields,
            },
        },
        "completeness": {
            "source": provenance.source_completeness.value,
            "query": provenance.query_completeness.value,
            "import": provenance.import_completeness.value,
        },
        "text_contract": {
            "encoding": "UTF-8",
            "newline": "CRLF",
            "delimiter": "TAB",
            "data_record_terminator": EXPECTED_DATA_RECORD_TERMINATOR,
        },
    }


def _read_complete_line(stream: BinaryLineStream, limit: int, reason: str) -> bytes:
    try:
        line = stream.readline(limit + 1)
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise PrefixSmokeError("member-read-failed") from exc
    if not isinstance(line, bytes):
        _fail("member-not-binary")
    if not line or len(line) > limit:
        _fail(reason)
    if not line.endswith(b"\r\n"):
        _fail(reason)
    return line


def _capture_prefix(artifact_path: Path) -> PrefixEnvelope:
    try:
        from llm_slovenian_repair.unigram_importer import EXPECTED_HEADER_BYTES
    except (ImportError, TypeError, ValueError) as exc:
        raise PrefixSmokeError("header-contract-unavailable") from exc

    try:
        with zipfile.ZipFile(artifact_path, "r") as archive:
            infos = archive.infolist()
            matches = [
                info for info in infos if info.filename == EXPECTED_MEMBER_NAME
            ]
            if len(matches) > 1:
                _fail("member-duplicate")
            if not matches:
                if any(info.filename.endswith(".tsv") for info in infos):
                    _fail("member-wrong")
                _fail("member-missing")
            selected = matches[0]
            mode = (selected.external_attr >> 16) & 0o170000
            if selected.is_dir() or (mode and mode != stat.S_IFREG):
                _fail("member-not-regular")

            envelope = bytearray()
            readline_calls = 0

            def append_line(line: bytes) -> None:
                if len(envelope) + len(line) > MAX_PREFIX_ENVELOPE_BYTES:
                    _fail("prefix-too-large")
                envelope.extend(line)

            with archive.open(selected, "r") as member:
                for _ in range(PREAMBLE_LINE_COUNT):
                    readline_calls += 1
                    append_line(
                        _read_complete_line(
                            member, MAX_PREFIX_LINE_BYTES, "preamble-incomplete"
                        )
                    )

                readline_calls += 1
                header = _read_complete_line(
                    member, EXPECTED_HEADER_BYTE_LENGTH, "header-incomplete"
                )
                if header != EXPECTED_HEADER_BYTES:
                    _fail("header-mismatch")
                append_line(header)

                for _ in range(DATA_ROW_COUNT):
                    readline_calls += 1
                    append_line(
                        _read_complete_line(member, MAX_PREFIX_LINE_BYTES, "row-incomplete")
                    )

            if readline_calls != PREFIX_READLINE_COUNT:
                _fail("prefix-readline-count")
            return PrefixEnvelope(
                data=bytes(envelope),
                preamble_lines=PREAMBLE_LINE_COUNT,
                header_bytes=len(header),
                data_rows=DATA_ROW_COUNT,
                readline_calls=readline_calls,
            )
    except PrefixSmokeError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        raise PrefixSmokeError("member-open-failed") from exc


def _expected_aggregate(aggregate: dict[str, object]) -> None:
    expected: dict[str, object] = {
        "requested_row_count": DATA_ROW_COUNT,
        "read_row_count": DATA_ROW_COUNT,
        "utf8_valid_row_count": DATA_ROW_COUNT,
        "utf8_invalid_row_count": 0,
        "crlf_row_count": DATA_ROW_COUNT,
        "lf_row_count": 0,
        "missing_newline_row_count": 0,
        "terminal_tab_count_histogram": {"0": 31, "1": 1, "2+": 0},
        "csv_field_count_histogram": {"28": 31, "29": 1},
        "empty_final_field_count": 1,
        "nonempty_field_after_28_count": 0,
        "embedded_tab_in_quoted_field_row_count": 0,
        "quote_parse_error_count": 0,
        "first_structurally_failing_source_line_number": None,
    }
    if any(aggregate.get(key) != value for key, value in expected.items()):
        _fail("structural-aggregate-mismatch")


def _real_provenance() -> Any:
    try:
        from llm_slovenian_repair.contracts import EvidenceCompleteness
        from llm_slovenian_repair.unigram_importer import (
            REAL_ACQUISITION_SHA256,
            REAL_INVENTORY_REVISION,
            REAL_INVENTORY_SHA256,
            REAL_RELEASE,
            REAL_SOURCE_ID,
            REAL_SOURCE_NAME,
            UnigramProvenance,
        )

        return UnigramProvenance(
            provenance_kind="real",
            source_id=REAL_SOURCE_ID,
            source_name=REAL_SOURCE_NAME,
            release=REAL_RELEASE,
            source_inventory_revision=REAL_INVENTORY_REVISION,
            source_inventory_sha256=REAL_INVENTORY_SHA256,
            acquisition_sha256=REAL_ACQUISITION_SHA256,
            evidence_scope="publisher-declared release scope; bounded compatibility prefix",
            source_completeness=EvidenceCompleteness.COMPLETE,
            query_completeness=EvidenceCompleteness.COMPLETE,
            import_completeness=EvidenceCompleteness.PARTIAL,
        )
    except (ImportError, TypeError, ValueError) as exc:
        raise PrefixSmokeError("provenance-construction-failed") from exc


def _import_twice(envelope: PrefixEnvelope) -> tuple[Any, Any]:
    try:
        from llm_slovenian_repair.unigram_importer import UnigramImportLimits, import_unigrams

        provenance = _real_provenance()
        limits = UnigramImportLimits(
            max_input_bytes=MAX_PREFIX_ENVELOPE_BYTES,
            max_rows=DATA_ROW_COUNT,
            max_line_bytes=MAX_PREFIX_LINE_BYTES,
            max_field_bytes=MAX_PREFIX_LINE_BYTES,
        )
        first = import_unigrams(BytesIO(envelope.data), provenance, limits=limits)
        second = import_unigrams(BytesIO(envelope.data), provenance, limits=limits)
    except PrefixSmokeError:
        raise
    except (ImportError, OSError, TypeError, ValueError) as exc:
        reason = getattr(exc, "reason", "failed")
        if (
            not isinstance(reason, str)
            or not reason.isascii()
            or not reason.replace("-", "").isalnum()
        ):
            reason = "failed"
        raise PrefixSmokeError(f"import-{reason}") from exc

    if first != second:
        _fail("import-nondeterministic")
    if len(first.records) != DATA_ROW_COUNT:
        _fail("import-record-count-mismatch")
    if not first.summary.input_sha256 or not first.summary.output_sha256:
        _fail("import-hash-missing")
    if first.summary.input_sha256 != second.summary.input_sha256:
        _fail("import-input-hash-mismatch")
    if first.summary.output_sha256 != second.summary.output_sha256:
        _fail("import-output-hash-mismatch")
    summary = first.summary
    if summary.import_completeness.value != "PARTIAL":
        _fail("import-completeness-mismatch")
    if summary.input_bytes != len(envelope.data):
        _fail("import-input-size-binding-mismatch")
    if summary.record_count != DATA_ROW_COUNT:
        _fail("import-summary-binding-mismatch")
    if summary.source_inventory_revision != "source-inventory-v1":
        _fail("import-summary-binding-mismatch")
    if summary.source_inventory_sha256 != (
        "439bbd51e04e338569b9785c44d1b05c0ea023aae39898aa7d494568d6f49de3"
    ):
        _fail("import-summary-binding-mismatch")
    if summary.acquisition_sha256 != EXPECTED_ARCHIVE_SHA256:
        _fail("import-summary-binding-mismatch")
    return first, second


def _run_verified_prefix(
    artifact_path: Path, verification: verifier.ArtifactVerification
) -> dict[str, object]:
    """Run member/import work after prior verifier evidence.

    This is the synthetic-test seam: tests may inject verifier evidence, but
    this function still opens the real ZIP member and invokes the real
    classifier/importer boundary.  The CLI always obtains evidence from
    ``verify_artifact`` immediately before calling this seam.
    """

    _canonical_verification(verification)
    envelope = _capture_prefix(artifact_path)
    try:
        aggregate = diagnostics.classify_stream(
            BytesIO(envelope.data),
            skip_rows=PREAMBLE_LINE_COUNT + 1,
            requested_rows=DATA_ROW_COUNT,
            limits=diagnostics.RowStructureLimits(
                max_rows=DATA_ROW_COUNT,
                max_total_bytes=MAX_PREFIX_ENVELOPE_BYTES,
                max_line_bytes=MAX_PREFIX_LINE_BYTES,
            ),
            include_parser_probe=False,
        )
    except (diagnostics.DiagnosticError, OSError, TypeError, ValueError) as exc:
        reason = exc.reason if isinstance(exc, diagnostics.DiagnosticError) else "failed"
        raise PrefixSmokeError(f"diagnostic-{reason}") from exc
    _expected_aggregate(aggregate)
    first, second = _import_twice(envelope)
    summary = first.summary
    return {
        "schema_version": 1,
        "status": "COMPLETE_REAL_PREFIX_SMOKE",
        "verifier": {
            "result": "PASSED",
            "source_id": verification.source_id,
            "byte_size": verification.byte_size,
            "md5": verification.md5,
            "archive_sha256": verification.sha256,
            "member_count": verification.member_count,
            "total_uncompressed_size": verification.total_uncompressed_size,
        },
        "prefix": {
            "member": EXPECTED_MEMBER_NAME,
            "preamble_lines": envelope.preamble_lines,
            "header_byte_length": envelope.header_bytes,
            "header_sha256": EXPECTED_HEADER_SHA256,
            "data_rows": envelope.data_rows,
            "readline_calls": envelope.readline_calls,
            "envelope_bytes": len(envelope.data),
        },
        "structural_aggregate": aggregate,
        "real_importer_smoke": {
            "attempts": 2,
            "runs_completed": 2,
            "sampled_row_count": len(first.records),
            "input_sha256": summary.input_sha256,
            "output_sha256": summary.output_sha256,
            "results_equal": first == second,
            "summary_bindings_equal": first.summary == second.summary,
            "import_completeness": summary.import_completeness.value,
            "record_count_binding": summary.record_count,
            "input_bytes_binding": summary.input_bytes,
        },
    }


def run_smoke(
    inventory_path: Path, source_id: str, artifact_path: Path
) -> dict[str, object]:
    """Verify canonical metadata, then run the bounded real-prefix smoke."""

    if source_id != EXPECTED_SOURCE_ID:
        _fail("source-id-not-canonical")
    try:
        inventory = verifier.load_inventory(inventory_path)
        entries = [entry for entry in inventory["entries"] if entry.get("id") == source_id]
        if len(entries) != 1:
            _fail("source-entry-not-canonical")
        verification = verifier.verify_artifact(inventory_path, source_id, artifact_path)
    except PrefixSmokeError:
        raise
    except (verifier.InventoryError, verifier.ArtifactVerificationError) as exc:
        raise PrefixSmokeError(f"verify-{exc.reason}") from exc
    _canonical_verification(verification)
    return _run_verified_prefix(artifact_path, verification)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--source-id", required=True)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument(
        "--preflight",
        action="store_true",
        help="validate the canonical inventory and installed importer runtime",
    )
    modes.add_argument(
        "--artifact",
        type=Path,
        help="run the bounded smoke over one already-acquired artifact",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.preflight:
            result = run_preflight(args.inventory, args.source_id)
        else:
            result = run_smoke(args.inventory, args.source_id, args.artifact)
    except (PreflightError, PrefixSmokeError) as exc:
        print(json.dumps({"error": exc.reason}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
