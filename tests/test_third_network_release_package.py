from __future__ import annotations

import json
import zipfile

import pytest

from scripts.package_third_network_confirmatory_release import package_release
from scripts.reproduce_third_network_confirmatory_release import reproduce
from scripts.run_third_network_release_rehearsal import run as run_release_rehearsal


def _rehearsal(tmp_path, scenario: str = "positive"):
    root = tmp_path / f"rehearsal_{scenario}"
    receipt = run_release_rehearsal(root, scenario=scenario, permutations=19)
    assert receipt["status"] == "PASS"
    return root


def test_development_release_package_replays_offline(tmp_path) -> None:
    rehearsal = _rehearsal(tmp_path, "positive")
    output = tmp_path / "release_positive"

    receipt = package_release(
        bundle_dir=rehearsal / "confirmatory_bundle",
        source_dir=rehearsal / "synthetic_fixture",
        output_dir=output,
        development_only=True,
    )

    assert receipt["status"] == "RELEASE_PACKAGE_READY"
    assert receipt["mode"] == "DEVELOPMENT_ONLY_SYNTHETIC"
    assert receipt["scientific_claim_allowed_by_archive_alone"] is False
    assert receipt["claim_transition_plan_ready"] is True
    assert receipt["automatic_manuscript_edit_permitted"] is False
    assert receipt["existing_network_inputs_verified"] is True

    replay = reproduce(output)
    assert replay["status"] == "REPRODUCTION_MATCH"
    assert replay["bundle_verification_status"] == "CONFIRMATORY_BUNDLE_VERIFIED"
    assert replay["source_recheck_mode"] == "SOURCE_INPUTS_RECHECKED"
    assert all(replay["third_network_matches"].values())
    assert all(replay["joint_k3_matches"].values())

    assert (output / "FILE_SHA256SUMS.txt").is_file()
    assert (output / "release_manifest.json").is_file()
    assert (output / "claim_transition_plan.json").is_file()
    assert (output / "code" / "scripts" / "reproduce_third_network_confirmatory_release.py").is_file()
    assert (output / "frozen_inputs" / "confirmatory_events.csv").is_file()


def test_release_zip_uses_stored_members_for_cross_environment_stability(tmp_path) -> None:
    rehearsal = _rehearsal(tmp_path, "positive")
    output = tmp_path / "stored_release"

    receipt = package_release(
        bundle_dir=rehearsal / "confirmatory_bundle",
        source_dir=rehearsal / "synthetic_fixture",
        output_dir=output,
        development_only=True,
    )

    manifest = json.loads((output / "release_manifest.json").read_text(encoding="utf-8"))
    assert manifest["archive_zip_method"] == "ZIP_STORED"
    assert "without zlib compression" in manifest["archive_byte_determinism_contract"]
    assert receipt["archive_zip_method"] == "ZIP_STORED"

    with zipfile.ZipFile(tmp_path / "stored_release.zip") as archive:
        infos = archive.infolist()
        assert infos
        assert all(info.compress_type == zipfile.ZIP_STORED for info in infos)
        assert all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in infos)


def test_release_zip_is_deterministic_across_output_locations(tmp_path) -> None:
    rehearsal = _rehearsal(tmp_path, "null")

    first = package_release(
        bundle_dir=rehearsal / "confirmatory_bundle",
        source_dir=rehearsal / "synthetic_fixture",
        output_dir=tmp_path / "package_a",
        development_only=True,
    )
    second = package_release(
        bundle_dir=rehearsal / "confirmatory_bundle",
        source_dir=rehearsal / "synthetic_fixture",
        output_dir=tmp_path / "nested" / "package_b",
        development_only=True,
    )

    assert first["zip_sha256"] == second["zip_sha256"]
    assert (
        (tmp_path / "package_a.zip").read_bytes()
        == (tmp_path / "nested" / "package_b.zip").read_bytes()
    )


def test_release_package_rejects_tampered_frozen_source(tmp_path) -> None:
    rehearsal = _rehearsal(tmp_path, "opposite")
    source = rehearsal / "synthetic_fixture"
    path = source / "plant_traits.csv"
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="CONFIRMATORY_BUNDLE_NOT_VERIFIED"):
        package_release(
            bundle_dir=rehearsal / "confirmatory_bundle",
            source_dir=source,
            output_dir=tmp_path / "must_not_exist",
            development_only=True,
        )

    assert not (tmp_path / "must_not_exist").exists()


def test_production_mode_rejects_synthetic_bundle(tmp_path) -> None:
    rehearsal = _rehearsal(tmp_path, "positive")

    with pytest.raises(ValueError, match="NONPRODUCTION_CONFIRMATORY_BUNDLE"):
        package_release(
            bundle_dir=rehearsal / "confirmatory_bundle",
            source_dir=rehearsal / "synthetic_fixture",
            output_dir=tmp_path / "production_forbidden",
            development_only=False,
        )


def test_release_package_refuses_nonempty_output(tmp_path) -> None:
    rehearsal = _rehearsal(tmp_path, "positive")
    output = tmp_path / "occupied"
    output.mkdir()
    (output / "stale.txt").write_text("stale", encoding="utf-8")

    with pytest.raises(ValueError, match="RELEASE_OUTPUT_EXISTS"):
        package_release(
            bundle_dir=rehearsal / "confirmatory_bundle",
            source_dir=rehearsal / "synthetic_fixture",
            output_dir=output,
            development_only=True,
        )


def test_release_manifest_is_path_independent(tmp_path) -> None:
    rehearsal = _rehearsal(tmp_path, "positive")
    first_dir = tmp_path / "manifest_a"
    second_dir = tmp_path / "elsewhere" / "manifest_b"

    package_release(
        bundle_dir=rehearsal / "confirmatory_bundle",
        source_dir=rehearsal / "synthetic_fixture",
        output_dir=first_dir,
        development_only=True,
    )
    package_release(
        bundle_dir=rehearsal / "confirmatory_bundle",
        source_dir=rehearsal / "synthetic_fixture",
        output_dir=second_dir,
        development_only=True,
    )

    first = json.loads((first_dir / "release_manifest.json").read_text(encoding="utf-8"))
    second = json.loads((second_dir / "release_manifest.json").read_text(encoding="utf-8"))
    assert first == second
