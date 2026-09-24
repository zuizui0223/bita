from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from scripts.ingest_third_network_release_archive import (
    INGEST_READY,
    ingest_release_archive,
)
from scripts.package_third_network_confirmatory_release import (
    _deterministic_zip,
    _write_checksums,
    package_release,
)
from scripts.reproduce_third_network_confirmatory_release import reproduce
from scripts.run_third_network_release_rehearsal import run as run_release_rehearsal


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    return zip_path, Path(str(zip_path) + ".sha256")


def _refresh_receipt(zip_path: Path, sha_path: Path) -> None:
    sha_path.write_text(
        f"{_sha256(zip_path)}  {zip_path.name}\n",
        encoding="utf-8",
    )


def test_valid_release_zip_ingests_transactionally_and_replays_offline(tmp_path) -> None:
    release = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(release)
    ingested = tmp_path / "ingested"

    receipt = ingest_release_archive(zip_path, sha_path, ingested)
    assert receipt["status"] == INGEST_READY
    assert receipt["pre_extraction_shell_status"] == INGEST_READY
    assert receipt["full_release_verification_status"] == "RELEASE_PACKAGE_VERIFIED"
    assert receipt["scientific_claim_allowed_by_ingest_alone"] is False
    assert ingested.is_dir()
    assert not Path(str(ingested) + ".staging").exists()

    replay = reproduce(ingested)
    assert replay["status"] == "REPRODUCTION_MATCH"


def test_path_traversal_member_is_rejected_before_extraction(tmp_path) -> None:
    release = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(release)
    outside = tmp_path / "escape.txt"
    ingested = tmp_path / "ingested"

    with zipfile.ZipFile(zip_path, "a", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr("../escape.txt", b"escape")
    _refresh_receipt(zip_path, sha_path)

    with pytest.raises(ValueError, match="ARCHIVE_SHELL_INVALID"):
        ingest_release_archive(zip_path, sha_path, ingested)

    assert not outside.exists()
    assert not ingested.exists()
    assert not Path(str(ingested) + ".staging").exists()


def test_internal_checksum_tampering_is_rejected_before_extraction(tmp_path) -> None:
    release = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(release)
    ingested = tmp_path / "ingested"

    # Duplicate README with changed bytes. The adjacent ZIP digest is refreshed,
    # but the internal checksum/inventory must still reject the archive.
    with zipfile.ZipFile(zip_path, "a", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr("README.md", b"tampered")
    _refresh_receipt(zip_path, sha_path)

    with pytest.raises(ValueError, match="ARCHIVE_SHELL_INVALID"):
        ingest_release_archive(zip_path, sha_path, ingested)

    assert not ingested.exists()
    assert not Path(str(ingested) + ".staging").exists()


def test_full_verifier_failure_rolls_back_staging_after_shell_passes(tmp_path) -> None:
    release = _package(tmp_path, "positive")
    zip_path, sha_path = _zip_paths(release)
    ingested = tmp_path / "ingested"

    # Change a claim guard, then deliberately rebuild internal checksums and the
    # deterministic ZIP. Transport and internal checksums are now self-consistent,
    # so only the full semantic verifier should reject it after staging extraction.
    manifest_path = release / "release_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["scientific_claim_allowed_by_archive_alone"] = True
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_checksums(release)
    _deterministic_zip(release, zip_path)
    _refresh_receipt(zip_path, sha_path)

    with pytest.raises(ValueError, match="EXTRACTED_RELEASE_INVALID"):
        ingest_release_archive(zip_path, sha_path, ingested)

    assert not ingested.exists()
    assert not Path(str(ingested) + ".staging").exists()


def test_ingest_refuses_to_overwrite_existing_destination(tmp_path) -> None:
    release = _package(tmp_path, "null")
    zip_path, sha_path = _zip_paths(release)
    ingested = tmp_path / "ingested"
    ingested.mkdir()
    sentinel = ingested / "keep.txt"
    sentinel.write_text("keep", encoding="utf-8")

    with pytest.raises(ValueError, match="OUTPUT_ALREADY_EXISTS"):
        ingest_release_archive(zip_path, sha_path, ingested)

    assert sentinel.read_text(encoding="utf-8") == "keep"
