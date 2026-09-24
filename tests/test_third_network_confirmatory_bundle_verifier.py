from __future__ import annotations

import hashlib
import json

from scripts.run_third_network_confirmatory_pipeline import run_with_network_inputs
from scripts.run_third_network_synthetic_e2e import (
    _synthetic_aubert,
    _synthetic_sakhalkar,
    run as run_synthetic_e2e,
)
from scripts.verify_third_network_confirmatory_bundle import (
    VERIFIED_STATUS,
    verify,
)


def _sha(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rewrite_bundle_checksums(root) -> None:
    lines = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name != "BUNDLE_SHA256SUMS.txt":
            lines.append(f"{_sha(path)}  {path.name}")
    (root / "BUNDLE_SHA256SUMS.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def _run_bundle(tmp_path):
    fixture = tmp_path / "fixture"
    run_synthetic_e2e(fixture, permutations=19, scenario="opposite")

    output = tmp_path / "bundle"
    run_with_network_inputs(
        events_csv=fixture / "confirmatory_events.csv",
        plant_traits_csv=fixture / "plant_traits.csv",
        mammal_traits_csv=fixture / "mammal_traits.csv",
        camera_deployment_csv=fixture / "camera_deployment.csv",
        confirmatory_freeze_json=fixture / "confirmatory_freeze.json",
        field_readiness_json=fixture / "field_readiness_receipt.json",
        sakhalkar_points=_synthetic_sakhalkar(),
        aubert_rows=_synthetic_aubert(),
        output_dir=output,
        repository_commit="TEST-COMMIT",
        existing_network_input_mode="TEST_SYNTHETIC_EXISTING_NETWORKS",
        permutations=19,
    )
    return fixture, output


def test_bundle_verifier_accepts_untampered_completed_run(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    result = verify(output)
    assert result["status"] == VERIFIED_STATUS
    assert result["failures"] == []
    assert result["source_recheck_mode"] == "SOURCE_INPUTS_NOT_RECHECKED"
    assert (output / "BUNDLE_SHA256SUMS.txt").is_file()
    assert all(entry["match"] for entry in result["bundle_checksum_checks"].values())


def test_bundle_verifier_can_recheck_original_source_inputs(tmp_path) -> None:
    fixture, output = _run_bundle(tmp_path)
    result = verify(output, source_dir=fixture)
    assert result["status"] == VERIFIED_STATUS
    assert result["source_recheck_mode"] == "SOURCE_INPUTS_RECHECKED"
    assert all(entry["match"] for entry in result["source_checks"].values())


def test_bundle_verifier_detects_tampered_scientific_output(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    path = output / "third_network_result.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["effect"]["rho_site_adjusted_rank"] = 0.999
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = verify(output)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert "output_hash_mismatch:third_network_result.json" in result["failures"]


def test_bundle_verifier_detects_missing_output(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    (output / "joint_access_routing_k3_result.json").unlink()
    result = verify(output)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert "output_hash_mismatch:joint_access_routing_k3_result.json" in result["failures"]


def test_bundle_verifier_detects_source_input_tampering_when_rechecked(tmp_path) -> None:
    fixture, output = _run_bundle(tmp_path)
    path = fixture / "plant_traits.csv"
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    result = verify(output, source_dir=fixture)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert "source_hash_mismatch:plant_traits" in result["failures"]



def test_bundle_verifier_reports_malformed_receipt_instead_of_crashing(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    receipt_path = output / "confirmatory_analysis_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["joint_k3"]["network_count"] = "not-an-integer"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

    result = verify(output)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert "joint_network_count_mismatch" in result["failures"]



def test_bundle_verifier_detects_tampered_analysis_receipt_via_bundle_checksum(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    receipt_path = output / "confirmatory_analysis_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["repository_commit"] = "tampered"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

    result = verify(output)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert "bundle_checksum_mismatch:confirmatory_analysis_receipt.json" in result["failures"]



def test_bundle_verifier_recomputes_existing_network_digests(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    result = verify(output)

    assert result["status"] == VERIFIED_STATUS
    checks = result["existing_network_checks"]
    assert set(checks) == {"sakhalkar", "aubert_ephi"}
    for entry in checks.values():
        assert entry["exists"] is True
        assert entry["is_list"] is True
        assert entry["analysis_units_match"] is True
        assert entry["stable_json_match"] is True
        assert entry["file_sha256_match"] is True
        assert entry["source_doi_match"] is True


def test_bundle_verifier_detects_tampered_existing_network_input(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    path = output / "existing_network_sakhalkar_input.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload[0]["tube_length"] = float(payload[0]["tube_length"]) + 1.0
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = verify(output)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert "existing_network_stable_digest_mismatch:sakhalkar" in result["failures"]
    assert "existing_network_file_digest_mismatch:sakhalkar" in result["failures"]


def test_bundle_verifier_detects_missing_existing_network_input(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    (output / "existing_network_aubert_ephi_input.json").unlink()

    result = verify(output)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert "existing_network_file_missing:aubert_ephi" in result["failures"]


def test_bundle_verifier_detects_existing_network_receipt_count_tampering(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)
    receipt_path = output / "confirmatory_analysis_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["existing_network_inputs"]["aubert_ephi"]["analysis_units"] += 1
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

    result = verify(output)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert "existing_network_analysis_units_mismatch:aubert_ephi" in result["failures"]



def test_bundle_verifier_rejects_coherently_rehashed_resource_limit_drift(tmp_path) -> None:
    _fixture, output = _run_bundle(tmp_path)

    manifest_path = output / "input_freeze_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["semantic_resource_limits"]["limits"]["max_event_rows"] += 1
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    receipt_path = output / "confirmatory_analysis_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["output_sha256"]["input_freeze_manifest.json"] = _sha(manifest_path)
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _rewrite_bundle_checksums(output)

    result = verify(output)
    assert result["status"] == "CONFIRMATORY_BUNDLE_INVALID"
    assert (
        "semantic_resource_limit_mismatch:max_event_rows"
        in result["failures"]
    )
