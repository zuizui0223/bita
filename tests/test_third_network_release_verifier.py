from __future__ import annotations

import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path

import pytest

from scripts.package_third_network_confirmatory_release import package_release
from scripts.reproduce_third_network_confirmatory_release import reproduce
from scripts.run_third_network_release_rehearsal import run as run_release_rehearsal
from scripts.verify_third_network_release_package import (
    INVALID_STATUS,
    VERIFIED_STATUS,
    verify_release_package,
)


def _package(tmp_path: Path, scenario: str = "positive") -> Path:
    rehearsal = tmp_path / f"rehearsal_{scenario}"
    receipt = run_release_rehearsal(
        rehearsal,
        scenario=scenario,
        permutations=19,
    )
    assert receipt["status"] == "PASS"

    output = tmp_path / f"release_{scenario}"
    package_release(
        bundle_dir=rehearsal / "confirmatory_bundle",
        source_dir=rehearsal / "synthetic_fixture",
        output_dir=output,
        development_only=True,
    )
    return output


def _zip_paths(output: Path) -> tuple[Path, Path]:
    zip_path = Path(str(output) + ".zip")
    sha_path = Path(str(zip_path) + ".sha256")
    return zip_path, sha_path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()



def _rewrite_zip_with_mode(zip_path: Path, target_name: str, target_mode: int) -> None:
    with zipfile.ZipFile(zip_path, "r") as source:
        members = [(info.filename, source.read(info)) for info in source.infolist()]

    tmp = zip_path.with_suffix(zip_path.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in members:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            mode = target_mode if name == target_name else (stat.S_IFREG | 0o644)
            info.external_attr = (mode & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, data, compress_type=zipfile.ZIP_STORED)
    tmp.replace(zip_path)


def _refresh_zip_receipt(zip_path: Path, sha_path: Path) -> None:
    sha_path.write_text(
        f"{_sha256(zip_path)}  {zip_path.name}\\n",
        encoding="utf-8",
    )

def test_release_verifier_accepts_complete_directory_zip_and_receipt(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    result = verify_release_package(output, require_archive=True)

    assert result["status"] == VERIFIED_STATUS
    assert result["failures"] == []
    assert result["archive_recheck_mode"] == "ZIP_RECHECKED"
    assert result["nested_confirmatory_bundle_status"] == "CONFIRMATORY_BUNDLE_VERIFIED"
    assert all(entry["match"] for entry in result["file_checks"].values())
    archive = result["archive_verification"]
    assert archive["sha256_receipt_match"] is True
    assert all(
        entry["bytes_match"] and entry["metadata_match"]
        for entry in archive["member_checks"].values()
    )


def test_release_verifier_accepts_extracted_directory_without_adjacent_zip(tmp_path) -> None:
    output = _package(tmp_path, "null")
    extracted = tmp_path / "isolated" / "release"
    extracted.parent.mkdir()
    shutil.copytree(output, extracted)

    result = verify_release_package(extracted)
    assert result["status"] == VERIFIED_STATUS
    assert result["archive_recheck_mode"] == "ZIP_NOT_RECHECKED"


def test_release_verifier_detects_directory_file_tampering(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    readme = output / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\ntampered\n", encoding="utf-8")

    result = verify_release_package(output)
    assert result["status"] == INVALID_STATUS
    assert "file_checksum_mismatch:README.md" in result["failures"]


def test_release_verifier_detects_unmanifested_extra_file(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    (output / "unexpected.txt").write_text("unexpected", encoding="utf-8")

    result = verify_release_package(output)
    assert result["status"] == INVALID_STATUS
    assert "file_checksum_inventory_mismatch" in result["failures"]


def test_release_verifier_detects_tampered_sha256_receipt(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(output)
    sha_path.write_text(f"{'0' * 64}  {zip_path.name}\n", encoding="utf-8")

    result = verify_release_package(output, require_archive=True)
    assert result["status"] == INVALID_STATUS
    assert "release_zip_sha256_receipt_mismatch" in result["failures"]


def test_release_verifier_detects_zip_tampering_even_with_updated_sha_receipt(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(output)

    # Simulate an attacker changing the archive and then updating the adjacent
    # digest receipt. The internal package verifier must still reject it.
    with zipfile.ZipFile(zip_path, "a", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr("README.md", b"tampered duplicate member")

    sha_path.write_text(
        f"{_sha256(zip_path)}  {zip_path.name}\n",
        encoding="utf-8",
    )

    result = verify_release_package(output, require_archive=True)
    assert result["status"] == INVALID_STATUS
    assert "release_zip_duplicate_member" in result["failures"]



def test_release_verifier_rejects_symlink_member_metadata_even_when_bytes_match(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(output)

    _rewrite_zip_with_mode(zip_path, "README.md", stat.S_IFLNK | 0o777)
    _refresh_zip_receipt(zip_path, sha_path)

    result = verify_release_package(output, require_archive=True)
    assert result["status"] == INVALID_STATUS
    assert "release_zip_member_metadata_mismatch:README.md" in result["failures"]
    check = result["archive_verification"]["member_checks"]["README.md"]
    assert check["bytes_match"] is True
    assert check["regular_file"] is False


def test_release_verifier_rejects_executable_permission_drift(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(output)

    _rewrite_zip_with_mode(zip_path, "README.md", stat.S_IFREG | 0o755)
    _refresh_zip_receipt(zip_path, sha_path)

    result = verify_release_package(output, require_archive=True)
    assert result["status"] == INVALID_STATUS
    assert "release_zip_member_metadata_mismatch:README.md" in result["failures"]
    check = result["archive_verification"]["member_checks"]["README.md"]
    assert check["bytes_match"] is True
    assert check["regular_file"] is True
    assert check["permission_match"] is False


def test_release_verifier_rejects_archive_comment_even_with_refreshed_digest(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(output)

    with zipfile.ZipFile(zip_path, "a") as archive:
        archive.comment = b"tampered archival annotation"
    _refresh_zip_receipt(zip_path, sha_path)

    result = verify_release_package(output, require_archive=True)
    assert result["status"] == INVALID_STATUS
    assert "release_zip_archive_comment_forbidden" in result["failures"]
    assert result["archive_verification"]["archive_comment_empty"] is False

def test_release_verifier_detects_unsafe_checksum_member(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    checksum = output / "FILE_SHA256SUMS.txt"
    checksum.write_text(
        checksum.read_text(encoding="utf-8")
        + f"{'0' * 64}  ../outside.txt\n",
        encoding="utf-8",
    )

    result = verify_release_package(output)
    assert result["status"] == INVALID_STATUS
    assert "file_checksum_manifest_malformed" in result["failures"]


def test_release_verifier_enforces_claim_guardrails(tmp_path) -> None:
    output = _package(tmp_path, "positive")
    manifest_path = output / "release_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["scientific_claim_allowed_by_archive_alone"] = True
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    result = verify_release_package(output)
    assert result["status"] == INVALID_STATUS
    assert "release_manifest_claim_guard_missing" in result["failures"]


def test_offline_replay_refuses_tampered_release_before_scientific_recompute(tmp_path) -> None:
    output = _package(tmp_path, "opposite")
    readme = output / "README.md"
    readme.write_text("tampered\n", encoding="utf-8")

    with pytest.raises(ValueError, match="PACKAGED_RELEASE_INVALID"):
        reproduce(output)
