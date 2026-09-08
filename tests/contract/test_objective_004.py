"""Focused contract tests for source manifests and synthetic payloads."""

from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path
from typing import Any, cast

import pytest
from pydantic import ValidationError

from llm_slovenian_repair import (
    ManifestVerificationError,
    SourceManifest,
    SyntheticCountRecord,
    VerificationFailure,
    verify_manifest_payload,
)

FIXTURE_ROOT = Path(__file__).parents[1] / "fixtures" / "corpus"
MANIFEST_PATH = FIXTURE_ROOT / "synthetic-manifest.json"
PAYLOAD_PATH = FIXTURE_ROOT / "synthetic-counts.jsonl"


def manifest_data() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(MANIFEST_PATH.read_text(encoding="utf-8")))


def write_pair(
    root: Path,
    payload: bytes,
    *,
    payload_name: str = "synthetic-counts.jsonl",
    **manifest_updates: Any,
) -> Path:
    root.mkdir()
    payload_path = root / payload_name
    if not Path(payload_name).is_absolute() and "/" in payload_name:
        payload_path.parent.mkdir(parents=True, exist_ok=True)
    if not Path(payload_name).is_absolute():
        payload_path.write_bytes(payload)
    data = manifest_data()
    data.update(
        {
            "payload_path": payload_name,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_size": len(payload),
            **manifest_updates,
        }
    )
    manifest_path = root / "synthetic-manifest.json"
    manifest_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def assert_failure(call: Any, reason: VerificationFailure) -> None:
    with pytest.raises(ManifestVerificationError) as caught:
        call()
    assert caught.value.reason == reason.value


def test_checked_in_fixture_verifies_at_exact_bytes_and_preserves_record_order() -> None:
    verified = verify_manifest_payload(MANIFEST_PATH)
    assert verified.payload_bytes == PAYLOAD_PATH.read_bytes()
    assert verified.payload_size == 2097
    assert verified.payload_sha256 == (
        "67f47819954e81fd57c766a29a659c5bba5c8ffbbe2d40249b6be960bc795ce1"
    )
    assert [record.record_id for record in verified.records] == [
        "word-positive",
        "word-exact-zero",
        "bigram-censored",
        "trigram-unavailable",
    ]
    assert verified.records[0].evidence.lower_bound == 3
    assert verified.records[1].evidence.lower_bound == 0
    assert verified.records[2].evidence.context_denominator is None
    assert verified.records[2].evidence.cutoff == (
        "Values at/below synthetic cutoff 4 are represented only by [0,4]"
    )
    assert verified.records[3].evidence.state.value == "UNAVAILABLE"
    assert verified.manifest.authorized_use_scope == "local synthetic tests only"
    assert verified.manifest.importer_schema_version == "NOT_APPLICABLE_SYNTHETIC_FIXTURE"

    manifest_round_trip = SourceManifest.model_validate_json(
        verified.manifest.model_dump_json()
    )
    assert manifest_round_trip == verified.manifest
    for record in verified.records:
        assert SyntheticCountRecord.model_validate_json(record.model_dump_json()) == record


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_name", ""),
        ("source_name", "   "),
        ("source_id", ""),
        ("license_terms_reference", ""),
        ("attribution_redistribution_conditions", ""),
        ("rights_status", ""),
    ],
)
def test_manifest_rejects_missing_or_blank_required_provenance(field: str, value: str) -> None:
    data = manifest_data()
    data[field] = value
    with pytest.raises(ValidationError):
        SourceManifest.model_validate_json(json.dumps(data, ensure_ascii=False))


def test_manifest_rejects_unknown_fields_and_rights_readiness_contradictions() -> None:
    data = manifest_data()
    data["unexpected"] = True
    with pytest.raises(ValidationError):
        SourceManifest.model_validate_json(json.dumps(data, ensure_ascii=False))

    for rights, synthetic, redistribution_ready, use_ready in (
        ("UNKNOWN_UNVERIFIED", False, True, False),
        ("PROHIBITED_RESTRICTED", False, False, True),
        ("PROJECT_AUTHORED_SYNTHETIC", False, False, False),
        ("VERIFIED_PERMITTED", True, True, True),
    ):
        invalid = manifest_data()
        invalid.update(
            {
                "rights_status": rights,
                "synthetic": synthetic,
                "redistribution_ready": redistribution_ready,
                "use_ready": use_ready,
            }
        )
        with pytest.raises(ValidationError):
            SourceManifest.model_validate_json(json.dumps(invalid, ensure_ascii=False))


@pytest.mark.parametrize(
    "value",
    [
        "synthetic",
        "PERMITTED",
        "project-authored synthetic",
        "PROJECT-AUTHORED_SYNTHETIC",
        " PROJECT_AUTHORED_SYNTHETIC",
        True,
        None,
    ],
)
def test_manifest_requires_exact_serialized_rights_values(value: Any) -> None:
    data = manifest_data()
    data["rights_status"] = value
    with pytest.raises(ValidationError):
        SourceManifest.model_validate_json(json.dumps(data, ensure_ascii=False))


def test_manifest_field_aliases_are_rejected() -> None:
    aliases = {
        "source_identity": "source_id",
        "source_release": "release",
        "version": "release",
        "payload_relative_path": "payload_path",
        "payload_sha256": "sha256",
        "checksum_sha256": "sha256",
        "payload_byte_size": "byte_size",
        "size": "byte_size",
        "payload_media_format": "media_format",
        "payload_record_format": "record_format",
        "payload_encoding": "encoding",
        "annotation": "annotation_tagging",
        "tagging": "annotation_tagging",
        "source_completeness": "completeness",
        "cutoff": "cutoff_metadata",
        "threshold": "threshold_metadata",
        "denominator_state": "denominator_knowledge",
        "rights": "rights_status",
        "terms_reference": "license_terms_reference",
        "license": "license_terms_reference",
        "attribution_conditions": "attribution_redistribution_conditions",
        "redistribution_conditions": "attribution_redistribution_conditions",
    }
    for alias, canonical in aliases.items():
        invalid = manifest_data()
        invalid[alias] = invalid[canonical]
        with pytest.raises(ValidationError):
            SourceManifest.model_validate_json(json.dumps(invalid, ensure_ascii=False))


def test_only_canonical_manifest_public_names_are_available() -> None:
    package = importlib.import_module("llm_slovenian_repair")
    source_manifest = importlib.import_module("llm_slovenian_repair.source_manifest")
    removed = (
        "DenominatorKnowledge",
        "Manifest",
        "ManifestError",
        "SourceRightsStatus",
        "SyntheticCorpusPayload",
        "SyntheticRecord",
        "VerifiedCorpus",
        "load_verified_corpus",
        "load_verified_manifest",
    )
    for name in removed:
        assert name not in package.__all__
        assert name not in source_manifest.__all__
        with pytest.raises(AttributeError):
            getattr(package, name)
        with pytest.raises(AttributeError):
            getattr(source_manifest, name)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("encoding", "utf-8"),
        ("encoding", "UTF-8 "),
        ("record_format", "JSONL"),
        ("record_format", "csv"),
        ("media_format", "application/x-ndjson"),
        ("media_format", "APPLICATION/JSONL"),
    ],
)
def test_manifest_accepts_only_supported_exact_formats(field: str, value: str) -> None:
    invalid = manifest_data()
    invalid[field] = value
    with pytest.raises(ValidationError):
        SourceManifest.model_validate_json(json.dumps(invalid, ensure_ascii=False))


@pytest.mark.parametrize(
    ("record_format", "media_format"),
    [("json", "application/jsonl"), ("jsonl", "application/json")],
)
def test_manifest_rejects_mismatched_record_and_media_formats(
    record_format: str, media_format: str
) -> None:
    invalid = manifest_data()
    invalid.update({"record_format": record_format, "media_format": media_format})
    with pytest.raises(ValidationError):
        SourceManifest.model_validate_json(json.dumps(invalid, ensure_ascii=False))


def test_invalid_manifest_format_is_rejected_before_payload_parsing(tmp_path: Path) -> None:
    manifest = write_pair(
        tmp_path / "format-before-payload",
        b"not-json\n",
        record_format="JSONL",
        media_format="application/jsonl",
    )
    assert_failure(
        lambda: verify_manifest_payload(manifest),
        VerificationFailure.MANIFEST_SCHEMA_INVALID,
    )


@pytest.mark.parametrize(
    "update",
    [
        {"authorized_use_scope": ""},
        {"authorized_use_scope": "all uses", "use_ready": True},
        {"license_terms_reference": "Apache License 2.0"},
        {
            "attribution_redistribution_conditions": "Project-authored synthetic fixture",
        },
        {"importer_schema_version": "synthetic-record-importer-v1"},
    ],
)
def test_synthetic_manifest_readiness_and_provenance_are_bounded(update: dict[str, Any]) -> None:
    invalid = manifest_data()
    invalid.update(update)
    with pytest.raises(ValidationError):
        SourceManifest.model_validate_json(json.dumps(invalid, ensure_ascii=False))


def test_manifest_rejects_checksum_size_and_completeness_contradictions() -> None:
    for update in (
        {"sha256": "A" * 64},
        {"byte_size": 0},
        {"completeness": "PARTIAL", "cutoff_metadata": None, "threshold_metadata": None},
        {"denominator_knowledge": "KNOWN", "denominator": None},
        {"denominator_knowledge": "UNKNOWN", "denominator": 4},
    ):
        invalid = manifest_data()
        invalid.update(update)
        with pytest.raises(ValidationError):
            SourceManifest.model_validate_json(json.dumps(invalid, ensure_ascii=False))


def test_record_rejects_false_synthetic_label_wrong_arity_and_non_synthetic_evidence() -> None:
    verified = verify_manifest_payload(MANIFEST_PATH)
    base = json.loads(verified.records[0].model_dump_json())
    for update in (
        {"synthetic": False},
        {"tokens": ["žarek", "višek"]},
        {"evidence": {**base["evidence"], "source": "unverified source"}},
        {"evidence": {**base["evidence"], "scope": "unverified scope"}},
    ):
        invalid = {**base, **update}
        with pytest.raises(ValidationError):
            SyntheticCountRecord.model_validate_json(json.dumps(invalid, ensure_ascii=False))


def test_disposable_payload_mutation_has_bounded_checksum_failure(tmp_path: Path) -> None:
    payload = PAYLOAD_PATH.read_bytes()
    changed = payload.replace(b"\n", b" ", 1)
    manifest = write_pair(
        tmp_path / "checksum",
        changed,
        sha256=hashlib.sha256(payload).hexdigest(),
    )
    assert_failure(
        lambda: verify_manifest_payload(manifest),
        VerificationFailure.PAYLOAD_CHECKSUM_MISMATCH,
    )

    wrong_size_manifest = write_pair(
        tmp_path / "size",
        payload,
        byte_size=len(payload) + 1,
    )
    assert_failure(
        lambda: verify_manifest_payload(wrong_size_manifest),
        VerificationFailure.PAYLOAD_SIZE_MISMATCH,
    )


@pytest.mark.parametrize(
    "payload_name", ["../outside.jsonl", "/absolute.jsonl", "./synthetic-counts.jsonl"]
)
def test_payload_path_must_be_normalized_and_inside_fixture_root(
    tmp_path: Path, payload_name: str
) -> None:
    manifest = write_pair(tmp_path / "paths", PAYLOAD_PATH.read_bytes(), payload_name=payload_name)
    assert_failure(
        lambda: verify_manifest_payload(manifest),
        VerificationFailure.PAYLOAD_PATH_INVALID,
    )


def test_symlink_and_non_file_payloads_are_rejected(tmp_path: Path) -> None:
    root = tmp_path / "symlink"
    root.mkdir()
    target = root / "target.jsonl"
    target.write_bytes(PAYLOAD_PATH.read_bytes())
    manifest = write_pair(root / "pair", PAYLOAD_PATH.read_bytes())
    pair_payload = manifest.parent / "synthetic-counts.jsonl"
    pair_payload.unlink()
    pair_payload.symlink_to(target)
    assert_failure(
        lambda: verify_manifest_payload(manifest),
        VerificationFailure.PAYLOAD_SYMLINK,
    )

    directory_manifest = write_pair(tmp_path / "directory", PAYLOAD_PATH.read_bytes())
    directory_payload = directory_manifest.parent / "synthetic-counts.jsonl"
    directory_payload.unlink()
    directory_payload.mkdir()
    assert_failure(
        lambda: verify_manifest_payload(directory_manifest),
        VerificationFailure.PAYLOAD_NOT_REGULAR,
    )


def test_bounded_manifest_payload_json_and_utf8_failures_do_not_echo_data(tmp_path: Path) -> None:
    oversized_manifest = tmp_path / "oversized-manifest.json"
    oversized_manifest.write_bytes(b"{}")
    assert_failure(
        lambda: verify_manifest_payload(oversized_manifest, max_manifest_bytes=1),
        VerificationFailure.MANIFEST_TOO_LARGE,
    )

    oversized_payload = write_pair(tmp_path / "oversized-payload", PAYLOAD_PATH.read_bytes())
    assert_failure(
        lambda: verify_manifest_payload(oversized_payload, max_payload_bytes=1),
        VerificationFailure.PAYLOAD_TOO_LARGE,
    )

    invalid_manifest = tmp_path / "invalid-manifest.json"
    invalid_manifest.write_bytes(b"\xff")
    assert_failure(
        lambda: verify_manifest_payload(invalid_manifest),
        VerificationFailure.MANIFEST_UTF8_INVALID,
    )

    invalid_payload = write_pair(tmp_path / "invalid-payload", b"\xff")
    assert_failure(
        lambda: verify_manifest_payload(invalid_payload),
        VerificationFailure.PAYLOAD_UTF8_INVALID,
    )

    malformed_payload = write_pair(tmp_path / "malformed", b"not-json\n")
    assert_failure(
        lambda: verify_manifest_payload(malformed_payload),
        VerificationFailure.PAYLOAD_JSON_INVALID,
    )


def test_duplicate_record_ids_are_rejected_after_checksum_verification(tmp_path: Path) -> None:
    first_line = PAYLOAD_PATH.read_bytes().splitlines(keepends=True)[0]
    duplicate_payload = first_line + first_line
    manifest = write_pair(tmp_path / "duplicate", duplicate_payload)
    assert_failure(
        lambda: verify_manifest_payload(manifest),
        VerificationFailure.PAYLOAD_DUPLICATE_RECORD,
    )


def test_loader_does_not_follow_payload_symlink_during_open(tmp_path: Path) -> None:
    if not hasattr(os, "O_NOFOLLOW"):
        pytest.skip("platform has no O_NOFOLLOW")
    root = tmp_path / "race-resistant"
    root.mkdir()
    manifest = write_pair(root / "pair", PAYLOAD_PATH.read_bytes())
    payload = manifest.parent / "synthetic-counts.jsonl"
    replacement = manifest.parent / "replacement.jsonl"
    replacement.write_bytes(PAYLOAD_PATH.read_bytes())
    payload.unlink()
    payload.symlink_to(replacement)
    assert_failure(
        lambda: verify_manifest_payload(manifest),
        VerificationFailure.PAYLOAD_SYMLINK,
    )


def test_fixture_is_not_part_of_runtime_package_sources() -> None:
    assert "tests/fixtures/corpus" not in (Path("pyproject.toml").read_text(encoding="utf-8"))
    assert not (Path("src") / "llm_slovenian_repair" / "tests").exists()
