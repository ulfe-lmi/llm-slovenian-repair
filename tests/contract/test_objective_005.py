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


def write_inventory(root: Path, data: dict[str, Any], *, name: str = "inventory.json") -> Path:
    path = root / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_zip(root: Path, *, name: str = "artifact.zip", member_name: str = "safe.tsv") -> Path:
    path = root / name
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member_name, "sintetični zapis\n")
    return path


def inventory_for_zip(root: Path, archive_path: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    data = inventory_data()
    entry = data["entries"][0]
    archive_bytes = archive_path.read_bytes()
    entry["artifact"]["byte_size"] = len(archive_bytes)
    entry["artifact"]["repository_checksum"]["value"] = hashlib.md5(
        archive_bytes, usedforsecurity=False
    ).hexdigest()
    return write_inventory(root, data)


def test_committed_inventory_is_strict_and_has_exact_four_entries() -> None:
    inventory = load_inventory(INVENTORY_PATH)
    assert inventory["schema_version"] == 1
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
    inventory = inventory_for_zip(tmp_path, archive)
    before = sorted(path.name for path in tmp_path.iterdir())

    result = verify_artifact(inventory, "gigafida-2.0-words", archive)

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
    inventory_data_for_test = inventory_data()
    entry = inventory_data_for_test["entries"][0]
    if failure == "size":
        entry["artifact"]["byte_size"] = archive.stat().st_size + 1
    else:
        entry["artifact"]["byte_size"] = archive.stat().st_size
        entry["artifact"]["repository_checksum"]["value"] = "0" * 32
    inventory = write_inventory(tmp_path, inventory_data_for_test)

    expected_reason = "artifact-size-mismatch" if failure == "size" else "artifact-md5-mismatch"
    with pytest.raises(ArtifactVerificationError, match=expected_reason):
        verify_artifact(inventory, "gigafida-2.0-words", archive)


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
    inventory = inventory_for_zip(tmp_path, archive)
    with pytest.raises(ArtifactVerificationError, match=reason):
        verify_artifact(inventory, "gigafida-2.0-words", archive)
    assert not (tmp_path / "escape.tsv").exists()


def test_duplicate_encrypted_and_symlink_members_are_rejected(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.zip"
    with zipfile.ZipFile(duplicate, "w") as archive:
        archive.writestr("same.tsv", "one")
        archive.writestr("same.tsv", "two")
    duplicate_inventory = inventory_for_zip(tmp_path / "duplicate-meta", duplicate)
    with pytest.raises(ArtifactVerificationError, match="zip-duplicate-member"):
        verify_artifact(duplicate_inventory, "gigafida-2.0-words", duplicate)

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
    encrypted_inventory = inventory_for_zip(tmp_path / "encrypted-meta", encrypted)
    with pytest.raises(ArtifactVerificationError, match="zip-encrypted-member"):
        verify_artifact(encrypted_inventory, "gigafida-2.0-words", encrypted)

    symlink = tmp_path / "symlink.zip"
    with zipfile.ZipFile(symlink, "w") as archive:
        info = zipfile.ZipInfo("link.tsv")
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive.writestr(info, "target")
    symlink_inventory = inventory_for_zip(tmp_path / "symlink-meta", symlink)
    with pytest.raises(ArtifactVerificationError, match="zip-symlink-member"):
        verify_artifact(symlink_inventory, "gigafida-2.0-words", symlink)


def test_source_specific_member_limit_is_bounded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    archive = write_zip(tmp_path)
    inventory = inventory_for_zip(tmp_path, archive)
    monkeypatch.setitem(
        verifier._ZIP_LIMITS,
        "gigafida-2.0-words",
        verifier.ZipLimits(0, 1_000_000, 1_000_000, 1.0),
    )
    with pytest.raises(ArtifactVerificationError, match="zip-member-count-limit"):
        verify_artifact(inventory, "gigafida-2.0-words", archive)


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
    inventory = inventory_for_zip(tmp_path, archive)
    with pytest.raises(ArtifactVerificationError, match="source-id-not-downloadable"):
        verify_artifact(inventory, "gigafida-2.2-query-interface", archive)


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
