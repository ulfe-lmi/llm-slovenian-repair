"""Focused offline source-inventory and ZIP-boundary contract tests."""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import stat
import struct
import subprocess
import sys
import warnings
import zipfile
from pathlib import Path
from typing import Any, cast

import pytest

REPO_ROOT = Path(__file__).parents[2]
INVENTORY_PATH = REPO_ROOT / "resources" / "source-inventory-v1.json"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

verifier = importlib.import_module("scripts.verify_source_artifact")
ArtifactVerificationError = verifier.ArtifactVerificationError
InventoryError = verifier.InventoryError
load_inventory = verifier.load_inventory
validate_inventory = verifier.validate_inventory
verify_artifact = verifier.verify_artifact


def inventory_data() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(INVENTORY_PATH.read_text(encoding="utf-8")))


def write_zip(root: Path, *, name: str = "artifact.zip", member_name: str = "safe.tsv") -> Path:
    path = root / name
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member_name, "sintetični zapis\n")
    return path


def write_zip_members(
    root: Path, members: list[tuple[str, bytes]], *, name: str = "artifact.zip"
) -> Path:
    path = root / name
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for member_name, content in members:
            archive.writestr(member_name, content)
    return path


def metadata_for_zip(archive_path: Path) -> dict[str, Any]:
    data = inventory_data()
    entry = data["entries"][0]
    archive_bytes = archive_path.read_bytes()
    entry["artifact"]["byte_size"] = len(archive_bytes)
    entry["artifact"]["repository_checksum"]["value"] = hashlib.md5(
        archive_bytes, usedforsecurity=False
    ).hexdigest()
    return cast(dict[str, Any], entry)


def test_committed_inventory_is_strict_and_has_exact_four_entries() -> None:
    inventory = load_inventory(INVENTORY_PATH)
    assert inventory["schema_version"] == 1
    assert inventory["snapshot_at"] == "2026-09-08T09:13:23Z"
    assert all(entry["observed_at"] == inventory["snapshot_at"] for entry in inventory["entries"])
    assert [entry["id"] for entry in inventory["entries"]] == [
        "gigafida-2.0-words",
        "gigafida-2.0-word-ngrams",
        "sloleks-3.1",
        "gigafida-2.2-query-interface",
    ]
    assert all(entry["acquisition_state"] == "NOT_ACQUIRED" for entry in inventory["entries"][:3])
    assert inventory["entries"][1]["absence_semantics"] == "CENSORED_NOT_ZERO"
    assert inventory["entries"][3]["bulk_access_status"] == "UNKNOWN_UNVERIFIED"
    assert inventory["entries"][3]["artifact"] is None
    canonical = json.dumps(
        inventory, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == (
        "0bc3dd7d043f3c6a96bf4e97fa0bbf02660f26263c0fc88a098cd449f0bc85e7"
    )


@pytest.mark.parametrize(
    ("field", "mutate", "reason"),
    [
        ("release", lambda entry: entry.__setitem__("release", "9.9"), "canonical-entry-mismatch"),
        (
            "item path",
            lambda entry: entry.__setitem__("item_url", entry["item_url"] + "/wrong"),
            "canonical-entry-mismatch",
        ),
        (
            "artifact path",
            lambda entry: entry["artifact"].__setitem__("url", entry["artifact"]["url"] + "/wrong"),
            "canonical-entry-mismatch",
        ),
        (
            "byte size",
            lambda entry: entry["artifact"].__setitem__("byte_size", 1),
            "canonical-entry-mismatch",
        ),
        (
            "MD5",
            lambda entry: entry["artifact"]["repository_checksum"].__setitem__("value", "0" * 32),
            "canonical-entry-mismatch",
        ),
        (
            "license name",
            lambda entry: entry["license"].__setitem__("name", "Apache-2.0"),
            "canonical-entry-mismatch",
        ),
        (
            "license URI",
            lambda entry: entry["license"].__setitem__("uri", "https://creativecommons.org/publicdomain/zero/1.0/"),
            "canonical-entry-mismatch",
        ),
        (
            "blank publisher",
            lambda entry: entry["publishers"].__setitem__(0, " "),
            "invalid-publisher",
        ),
        (
            "future issue date",
            lambda entry: entry.__setitem__("issued_date", "2026-09-09"),
            "issued-date-after-observation",
        ),
    ],
)
def test_canonical_source_facts_reject_rebinding(
    field: str, mutate: Any, reason: str
) -> None:
    data = inventory_data()
    mutate(data["entries"][0])
    with pytest.raises(InventoryError, match=reason):
        validate_inventory(data)


@pytest.mark.parametrize(
    ("change", "reason"),
    [
        (lambda checksum: checksum.__setitem__("value", "0" * 31), "invalid-repository-checksum"),
        (lambda checksum: checksum.__setitem__("value", "A" * 32), "invalid-repository-checksum"),
        (
            lambda checksum: checksum.__setitem__("algorithm", "SHA-256"),
            "invalid-repository-checksum",
        ),
    ],
)
def test_malformed_checksum_is_rejected(change: Any, reason: str) -> None:
    data = inventory_data()
    change(data["entries"][0]["artifact"]["repository_checksum"])
    with pytest.raises(InventoryError, match=reason):
        validate_inventory(data)


@pytest.mark.parametrize(
    ("change", "reason"),
    [
        (
            lambda entry: entry["license"].update(
                {"name": "CC BY-SA 4.0", "uri": "https://creativecommons.org/licenses/by-sa/4.0/"}
            ),
            "canonical-entry-mismatch",
        ),
        (
            lambda entry: entry.__setitem__("artifact", {"unexpected": True}),
            "query-artifact-forbidden",
        ),
        (
            lambda entry: entry.__setitem__("acquisition_ready", True),
            "query-readiness-contradiction",
        ),
    ],
)
def test_query_entry_cannot_gain_download_rights(change: Any, reason: str) -> None:
    data = inventory_data()
    change(data["entries"][3])
    with pytest.raises(InventoryError, match=reason):
        validate_inventory(data)


@pytest.mark.parametrize(
    ("path", "reason"),
    [
        ("unknown-key", "invalid-inventory"),
        ("bool-size", "invalid-artifact-byte-size"),
        ("wrong-host", "invalid-item-url"),
        ("project-sha", "project-sha256-must-be-null-before-fetch"),
        ("provider-ready", "query-readiness-contradiction"),
        ("cutoff-zero", "ngram-cutoff-zero-contradiction"),
        ("over-limit-size", "artifact-byte-size-too-large"),
    ],
)
def test_inventory_rejects_strictness_and_evidence_contradictions(
    tmp_path: Path, path: str, reason: str
) -> None:
    data = inventory_data()
    if path == "unknown-key":
        data["unexpected"] = True
    elif path == "bool-size":
        data["entries"][0]["artifact"]["byte_size"] = True
    elif path == "wrong-host":
        data["entries"][0]["item_url"] = "http://example.invalid/item"
    elif path == "project-sha":
        data["entries"][0]["artifact"]["project_sha256"] = "a" * 64
    elif path == "provider-ready":
        data["entries"][3]["acquisition_ready"] = True
    elif path == "over-limit-size":
        data["entries"][0]["artifact"]["byte_size"] = 512 * 1024 * 1024 + 1
    else:
        data["entries"][1]["absence_semantics"] = "EXACT_WITHIN_DECLARED_SCOPE"
    with pytest.raises(InventoryError, match=reason):
        validate_inventory(data)


def test_duplicate_json_key_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text(
        '{"schema_version":1,"schema_version":1,"inventory_id":"source-inventory-v1"}',
        encoding="utf-8",
    )
    with pytest.raises(InventoryError, match="inventory-json-invalid"):
        load_inventory(path)


def test_safe_zip_passes_and_emits_exact_hashes_without_extraction(tmp_path: Path) -> None:
    archive = write_zip(tmp_path)
    entry = metadata_for_zip(archive)
    before = sorted(path.name for path in tmp_path.iterdir())

    result = verifier._verify_artifact_entry(entry, entry["id"], archive)

    archive_bytes = archive.read_bytes()
    assert result.byte_size == len(archive_bytes)
    assert result.md5 == hashlib.md5(archive_bytes, usedforsecurity=False).hexdigest()
    assert result.sha256 == hashlib.sha256(archive_bytes).hexdigest()
    assert result.member_count == 1
    assert result.total_uncompressed_size == len("sintetični zapis\n".encode())
    assert sorted(path.name for path in tmp_path.iterdir()) == before
    assert not (tmp_path / "safe.tsv").exists()


@pytest.mark.parametrize("failure", ["size", "checksum"])
def test_size_and_checksum_mismatch_fail_before_zip_use(tmp_path: Path, failure: str) -> None:
    archive = write_zip(tmp_path)
    entry = inventory_data()["entries"][0]
    if failure == "size":
        entry["artifact"]["byte_size"] = archive.stat().st_size + 1
    else:
        entry["artifact"]["byte_size"] = archive.stat().st_size
        entry["artifact"]["repository_checksum"]["value"] = "0" * 32

    expected_reason = "artifact-size-mismatch" if failure == "size" else "artifact-md5-mismatch"
    with pytest.raises(ArtifactVerificationError, match=expected_reason):
        verifier._verify_artifact_entry(entry, entry["id"], archive)


@pytest.mark.parametrize(
    ("member_name", "reason"),
    [
        ("../escape.tsv", "zip-unsafe-member-name"),
        ("C:/drive.tsv", "zip-unsafe-member-name"),
        ("folder\\escape.tsv", "zip-unsafe-member-name"),
    ],
)
def test_unsafe_member_names_fail_without_extraction(
    tmp_path: Path, member_name: str, reason: str
) -> None:
    archive = write_zip(tmp_path, member_name=member_name)
    entry = metadata_for_zip(archive)
    with pytest.raises(ArtifactVerificationError, match=reason):
        verifier._verify_artifact_entry(entry, entry["id"], archive)
    assert not (tmp_path / "escape.tsv").exists()


def test_duplicate_encrypted_and_symlink_members_are_rejected(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.zip"
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=r"Duplicate name: 'same\.tsv'")
        with zipfile.ZipFile(duplicate, "w") as archive:
            archive.writestr("same.tsv", "one")
            archive.writestr("same.tsv", "two")
    duplicate_entry = metadata_for_zip(duplicate)
    with pytest.raises(ArtifactVerificationError, match="zip-duplicate-member"):
        verifier._verify_artifact_entry(duplicate_entry, duplicate_entry["id"], duplicate)

    encrypted = tmp_path / "encrypted.zip"
    with zipfile.ZipFile(encrypted, "w") as archive:
        info = zipfile.ZipInfo("secret.tsv")
        info.flag_bits |= 0x1
        archive.writestr(info, "secret")
    encrypted_bytes = bytearray(encrypted.read_bytes())
    for signature in (b"PK\x03\x04", b"PK\x01\x02"):
        flag_offset = 6 if signature == b"PK\x03\x04" else 8
        offset = 0
        while True:
            found = encrypted_bytes.find(signature, offset)
            if found < 0:
                break
            flags = struct.unpack_from("<H", encrypted_bytes, found + flag_offset)[0]
            struct.pack_into("<H", encrypted_bytes, found + flag_offset, flags | 0x1)
            offset = found + len(signature)
    encrypted.write_bytes(encrypted_bytes)
    encrypted_entry = metadata_for_zip(encrypted)
    with pytest.raises(ArtifactVerificationError, match="zip-encrypted-member"):
        verifier._verify_artifact_entry(encrypted_entry, encrypted_entry["id"], encrypted)

    symlink = tmp_path / "symlink.zip"
    with zipfile.ZipFile(symlink, "w") as archive:
        info = zipfile.ZipInfo("link.tsv")
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive.writestr(info, "target")
    symlink_entry = metadata_for_zip(symlink)
    with pytest.raises(ArtifactVerificationError, match="zip-symlink-member"):
        verifier._verify_artifact_entry(symlink_entry, symlink_entry["id"], symlink)


def test_directory_member_is_rejected_as_nonregular(tmp_path: Path) -> None:
    archive = tmp_path / "directory.zip"
    with zipfile.ZipFile(archive, "w") as zip_file:
        zip_file.writestr("folder/", "")
    entry = metadata_for_zip(archive)
    with pytest.raises(ArtifactVerificationError, match="zip-nonregular-member"):
        verifier._verify_artifact_entry(entry, entry["id"], archive)


@pytest.mark.parametrize(
    ("limit", "reason", "members"),
    [
        (
            verifier.ZipLimits(1, 1_000_000, 1_000_000, 1_000.0),
            "zip-member-count-limit",
            [("one.tsv", b"one"), ("two.tsv", b"two")],
        ),
        (
            verifier.ZipLimits(10, 2, 1_000_000, 1_000.0),
            "zip-member-size-limit",
            [("large.tsv", b"three")],
        ),
        (
            verifier.ZipLimits(10, 1_000_000, 5, 1_000.0),
            "zip-total-size-limit",
            [("one.tsv", b"123"), ("two.tsv", b"456")],
        ),
        (
            verifier.ZipLimits(10, 1_000_000, 1_000_000, 2.0),
            "zip-compression-ratio-limit",
            [("repetitive.tsv", b"x" * 10_000)],
        ),
    ],
)
def test_each_zip_limit_has_a_synthetic_boundary_case(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    limit: Any,
    reason: str,
    members: list[tuple[str, bytes]],
) -> None:
    archive = write_zip_members(tmp_path, members)
    entry = metadata_for_zip(archive)
    monkeypatch.setitem(verifier._ZIP_LIMITS, entry["id"], limit)
    with pytest.raises(ArtifactVerificationError, match=reason):
        verifier._verify_artifact_entry(entry, entry["id"], archive)


def test_source_specific_member_limit_is_bounded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive = write_zip(tmp_path)
    entry = metadata_for_zip(archive)
    monkeypatch.setitem(
        verifier._ZIP_LIMITS,
        "gigafida-2.0-words",
        verifier.ZipLimits(0, 1_000_000, 1_000_000, 1.0),
    )
    with pytest.raises(ArtifactVerificationError, match="zip-member-count-limit"):
        verifier._verify_artifact_entry(entry, entry["id"], archive)


def test_cli_validate_only_is_offline_and_bounded() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/verify_source_artifact.py",
            "--inventory",
            str(INVENTORY_PATH),
            "--validate-only",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    assert json.loads(completed.stdout) == {
        "entry_count": 4,
        "inventory_id": "source-inventory-v1",
        "schema_version": 1,
    }
    assert completed.stderr == ""


def test_symlink_inventory_and_non_downloadable_source_are_rejected(tmp_path: Path) -> None:
    symlink = tmp_path / "inventory-link.json"
    symlink.symlink_to(INVENTORY_PATH)
    with pytest.raises(InventoryError, match="path-symlink"):
        load_inventory(symlink)

    archive = write_zip(tmp_path)
    entry = metadata_for_zip(archive)
    with pytest.raises(ArtifactVerificationError, match="source-id-not-downloadable"):
        verifier._verify_artifact_entry(entry, "gigafida-2.2-query-interface", archive)


def test_inventory_and_artifact_boundaries_do_not_need_network_or_package_imports() -> None:
    assert os.environ.get("REPAIR_ALLOW_LIVE_TESTS") != "YES"
    completed = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; import scripts.verify_source_artifact; "
                "print('pydantic' in sys.modules)",
            ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout.strip() == "False"
