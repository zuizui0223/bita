from __future__ import annotations

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
