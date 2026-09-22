from __future__ import annotations

import copy
import hashlib
import json

import pytest

from scripts.analyze_joint_access_routing import summarize_joint
from scripts.run_third_network_confirmatory_pipeline import (
    COMPLETE_STATUS,
    RECEIPT,
    run_with_network_inputs,
)
from scripts.run_third_network_synthetic_e2e import (
    _synthetic_aubert,
    _synthetic_sakhalkar,
    run as run_synthetic_e2e,
)


def _sha(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture(tmp_path, scenario: str = "opposite"):
    fixture = tmp_path / "frozen_fixture"
    run_synthetic_e2e(fixture, permutations=19, scenario=scenario)
    return fixture


def _synthetic_canonical_k2() -> dict[str, object]:
    return summarize_joint(
        _synthetic_sakhalkar(),
        _synthetic_aubert(),
        permutations=19,
        seed=20260920,
    )


def _run_production_fixture(tmp_path, *, scenario: str = "opposite"):
    fixture = _fixture(tmp_path, scenario=scenario)
    output = tmp_path / "confirmatory_run"
    receipt = run_with_network_inputs(
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
        canonical_k2_receipt=_synthetic_canonical_k2(),
        canonical_k2_receipt_id="TEST-CANONICAL-K2",
        permutations=19,
    )
    return fixture, output, receipt


def test_confirmatory_runner_keeps_opposite_third_network_and_finishes_k3(tmp_path) -> None:
    _fixture_dir, output, receipt = _run_production_fixture(
        tmp_path,
        scenario="opposite",
    )

    assert receipt["receipt"] == RECEIPT
    assert receipt["status"] == COMPLETE_STATUS
    assert receipt["repository_commit"] == "TEST-COMMIT"
    assert receipt["input_freeze_status"] == "INPUTS_FROZEN_READY_FOR_JOIN"
    assert receipt["route_reliability_status"] == "ROUTE_RELIABILITY_PASS"
    assert receipt["route_reliability_kappa"] >= 0.8
    assert receipt["analysis_units"] == 72
    assert receipt["canonical_k2_anchor"]["status"] == "CANONICAL_K2_ANCHOR_MATCH"
    assert receipt["canonical_k2_anchor"]["canonical_receipt_id"] == "TEST-CANONICAL-K2"
    assert all(receipt["canonical_k2_anchor"]["checks"].values())

    assert receipt["third_network"]["status"] == "CONFIRMATORY_GATE_PASS"
    assert receipt["third_network"]["direction"] == "opposite"
    assert receipt["third_network"]["rho_site_adjusted_rank"] < 0

    assert receipt["joint_k3"]["network_count"] == 3
    assert (
        receipt["joint_k3"]["network_direction_concordance"]
        == "not_3_of_3_positive"
    )
    assert (
        receipt["third_network_retention_rule"]
        == "retain_confirmatory_third_network_regardless_of_positive_null_or_opposite_direction"
    )

    saved = json.loads(
        (output / "confirmatory_analysis_receipt.json").read_text(encoding="utf-8")
    )
    assert saved == receipt


def test_confirmatory_receipt_hashes_every_generated_scientific_output(tmp_path) -> None:
    _fixture_dir, output, receipt = _run_production_fixture(
        tmp_path,
        scenario="null",
    )

    for filename, expected in receipt["output_sha256"].items():
        path = output / filename
        assert path.exists()
        assert _sha(path) == expected

    assert receipt["third_network"]["status"] == "CONFIRMATORY_GATE_PASS"
    assert abs(receipt["third_network"]["rho_site_adjusted_rank"]) < 0.1
    assert receipt["joint_k3"]["network_count"] == 3


def test_confirmatory_runner_refuses_to_overwrite_existing_run(tmp_path) -> None:
    fixture, output, _receipt = _run_production_fixture(tmp_path)

    with pytest.raises(ValueError, match="CONFIRMATORY_OUTPUT_DIR_NOT_EMPTY"):
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
            canonical_k2_receipt=_synthetic_canonical_k2(),
            canonical_k2_receipt_id="TEST-CANONICAL-K2",
            permutations=19,
        )


def test_confirmatory_runner_requires_repository_commit_before_analysis(tmp_path) -> None:
    fixture = _fixture(tmp_path)
    with pytest.raises(ValueError, match="repository_commit is required"):
        run_with_network_inputs(
            events_csv=fixture / "confirmatory_events.csv",
            plant_traits_csv=fixture / "plant_traits.csv",
            mammal_traits_csv=fixture / "mammal_traits.csv",
            camera_deployment_csv=fixture / "camera_deployment.csv",
            confirmatory_freeze_json=fixture / "confirmatory_freeze.json",
            field_readiness_json=fixture / "field_readiness_receipt.json",
            sakhalkar_points=_synthetic_sakhalkar(),
            aubert_rows=_synthetic_aubert(),
            output_dir=tmp_path / "not_created",
            repository_commit="",
            existing_network_input_mode="TEST_SYNTHETIC_EXISTING_NETWORKS",
            canonical_k2_receipt=_synthetic_canonical_k2(),
            canonical_k2_receipt_id="TEST-CANONICAL-K2",
            permutations=19,
        )



def test_confirmatory_runner_blocks_changed_existing_network_anchor(tmp_path) -> None:
    fixture = _fixture(tmp_path, scenario="positive")
    canonical = copy.deepcopy(_synthetic_canonical_k2())
    canonical["network_effects"]["sakhalkar"]["rho"] += 0.01

    with pytest.raises(ValueError, match="CANONICAL_K2_ANCHOR_MISMATCH"):
        run_with_network_inputs(
            events_csv=fixture / "confirmatory_events.csv",
            plant_traits_csv=fixture / "plant_traits.csv",
            mammal_traits_csv=fixture / "mammal_traits.csv",
            camera_deployment_csv=fixture / "camera_deployment.csv",
            confirmatory_freeze_json=fixture / "confirmatory_freeze.json",
            field_readiness_json=fixture / "field_readiness_receipt.json",
            sakhalkar_points=_synthetic_sakhalkar(),
            aubert_rows=_synthetic_aubert(),
            output_dir=tmp_path / "mismatch_run",
            repository_commit="TEST-COMMIT",
            existing_network_input_mode="TEST_SYNTHETIC_EXISTING_NETWORKS",
            canonical_k2_receipt=canonical,
            canonical_k2_receipt_id="TAMPERED-CANONICAL-K2",
            permutations=19,
        )


@pytest.mark.parametrize(
    ("field", "delta"),
    [
        ("sakhalkar_n_units", 1),
        ("aubert_n_units", 1),
    ],
)
def test_confirmatory_runner_blocks_changed_existing_network_sample_size(
    tmp_path,
    field,
    delta,
) -> None:
    fixture = _fixture(tmp_path, scenario="positive")
    canonical = copy.deepcopy(_synthetic_canonical_k2())
    if field == "sakhalkar_n_units":
        canonical["network_effects"]["sakhalkar"]["n_units"] += delta
    else:
        canonical["network_effects"]["aubert_ephi"]["n_units"] += delta

    with pytest.raises(ValueError, match="CANONICAL_K2_ANCHOR_MISMATCH"):
        run_with_network_inputs(
            events_csv=fixture / "confirmatory_events.csv",
            plant_traits_csv=fixture / "plant_traits.csv",
            mammal_traits_csv=fixture / "mammal_traits.csv",
            camera_deployment_csv=fixture / "camera_deployment.csv",
            confirmatory_freeze_json=fixture / "confirmatory_freeze.json",
            field_readiness_json=fixture / "field_readiness_receipt.json",
            sakhalkar_points=_synthetic_sakhalkar(),
            aubert_rows=_synthetic_aubert(),
            output_dir=tmp_path / f"mismatch_{field}",
            repository_commit="TEST-COMMIT",
            existing_network_input_mode="TEST_SYNTHETIC_EXISTING_NETWORKS",
            canonical_k2_receipt=canonical,
            canonical_k2_receipt_id="TAMPERED-CANONICAL-K2",
            permutations=19,
        )
