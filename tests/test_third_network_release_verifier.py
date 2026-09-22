from __future__ import annotations

import json

from scripts.package_third_network_confirmatory_release import package_release
from scripts.run_third_network_release_rehearsal import run as run_release_rehearsal
from scripts.verify_third_network_confirmatory_release import (
    INVALID_STATUS,
    VERIFIED_STATUS,
    verify,
)


def _package(tmp_path, scenario: str = "positive"):
    rehearsal = tmp_path / f"rehearsal_{scenario}"
    run_release_rehearsal(rehearsal, scenario=scenario, permutations=19)

    release = tmp_path / f"release_{scenario}"
    receipt = package_release(
        bundle_dir=rehearsal / "confirmatory_bundle",
        source_dir=rehearsal / "synthetic_fixture",
        output_dir=release,
        development_only=True,
    )
    return rehearsal, release, receipt


def test_release_verifier_accepts_complete_package_and_zip(tmp_path) -> None:
    _rehearsal, release, package = _package(tmp_path, "positive")
    result = verify(
        release,
        zip_path=package["zip_path"],
        zip_sha256_receipt=package["zip_sha256_receipt"],
    )

    assert result["status"] == VERIFIED_STATUS
    assert result["failures"] == []
    assert result["nested_bundle_verification"]["status"] == "CONFIRMATORY_BUNDLE_VERIFIED"
    assert result["nested_bundle_verification"]["source_recheck_mode"] == "SOURCE_INPUTS_RECHECKED"
    assert all(entry["match"] for entry in result["release_file_checks"].values())
    assert all(entry["match"] for entry in result["frozen_input_checks"].values())
    assert all(entry["match"] for entry in result["code_file_checks"].values())
    assert all(entry["match"] for entry in result["protocol_file_checks"].values())
    assert result["zip_verification"]["zip_sha256_match"] is True
    assert all(
        entry["content_match"] and entry["fixed_timestamp"] and entry["safe_path"]
        for entry in result["zip_verification"]["member_checks"].values()
    )


def test_release_verifier_detects_protocol_tampering(tmp_path) -> None:
    _rehearsal, release, _package_receipt = _package(tmp_path)
    path = release / "protocol" / "THIRD_ACCESS_ROUTING_NETWORK_PREREG_V1.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nTAMPERED\n", encoding="utf-8")

    result = verify(release)
    assert result["status"] == INVALID_STATUS
    assert any(x.startswith("release_file_hash_mismatch:protocol/") for x in result["failures"])
    assert any(x.startswith("protocol_file_hash_mismatch:") for x in result["failures"])


def test_release_verifier_detects_code_tampering(tmp_path) -> None:
    _rehearsal, release, _package_receipt = _package(tmp_path)
    path = release / "code" / "trait_architecture" / "numerics.py"
    path.write_text(path.read_text(encoding="utf-8") + "\n# tampered\n", encoding="utf-8")

    result = verify(release)
    assert result["status"] == INVALID_STATUS
    assert "code_file_hash_mismatch:trait_architecture/numerics.py" in result["failures"]


def test_release_verifier_detects_claim_plan_tampering(tmp_path) -> None:
    _rehearsal, release, _package_receipt = _package(tmp_path, "opposite")
    path = release / "claim_transition_plan.json"
    plan = json.loads(path.read_text(encoding="utf-8"))
    plan["third_network_must_be_retained"] = False
    path.write_text(json.dumps(plan), encoding="utf-8")

    result = verify(release)
    assert result["status"] == INVALID_STATUS
    assert "claim_transition_retention_rule_missing" in result["failures"]


def test_release_verifier_detects_missing_frozen_input(tmp_path) -> None:
    _rehearsal, release, _package_receipt = _package(tmp_path)
    (release / "frozen_inputs" / "confirmatory_events.csv").unlink()

    result = verify(release)
    assert result["status"] == INVALID_STATUS
    assert "frozen_input_hash_mismatch:events" in result["failures"]
    assert "nested_confirmatory_bundle_invalid" in result["failures"]


def test_release_verifier_detects_extra_file(tmp_path) -> None:
    _rehearsal, release, _package_receipt = _package(tmp_path)
    (release / "unexpected.txt").write_text("unexpected", encoding="utf-8")

    result = verify(release)
    assert result["status"] == INVALID_STATUS
    assert "release_file_inventory_mismatch" in result["failures"]


def test_release_verifier_detects_zip_sha_receipt_tampering(tmp_path) -> None:
    _rehearsal, release, package = _package(tmp_path)
    sha_path = package["zip_sha256_receipt"]
    from pathlib import Path

    receipt = Path(sha_path)
    receipt.write_text("0" * 64 + "  " + Path(package["zip_path"]).name + "\n", encoding="utf-8")

    result = verify(
        release,
        zip_path=package["zip_path"],
        zip_sha256_receipt=receipt,
    )
    assert result["status"] == INVALID_STATUS
    assert "release_zip_sha256_mismatch" in result["failures"]


def test_release_verifier_detects_zip_member_tampering_without_sha_receipt(tmp_path) -> None:
    _rehearsal, release, package = _package(tmp_path)
    from pathlib import Path
    import zipfile

    original = Path(package["zip_path"])
    tampered = tmp_path / "tampered.zip"
    with zipfile.ZipFile(original) as src, zipfile.ZipFile(tampered, "w") as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "README.md":
                data += b"tamper"
            dst.writestr(info, data)

    result = verify(release, zip_path=tampered)
    assert result["status"] == INVALID_STATUS
    assert "release_zip_content_mismatch:README.md" in result["failures"]
