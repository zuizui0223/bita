from __future__ import annotations

import hashlib
import json

import pytest
import scripts.run_third_network_confirmatory_pipeline as runner

from scripts.run_third_network_confirmatory_pipeline import (
    COMPLETE_STATUS,
    RECEIPT,
    _validate_production_repository_commit,
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
            permutations=19,
        )



def test_confirmatory_runner_commits_outputs_atomically(tmp_path) -> None:
    _fixture_dir, output, receipt = _run_production_fixture(tmp_path, scenario="positive")
    assert receipt["status"] == COMPLETE_STATUS
    assert output.is_dir()
    assert not output.with_name(output.name + ".inprogress").exists()


def test_confirmatory_runner_cleans_staging_after_analysis_failure(tmp_path, monkeypatch) -> None:
    fixture = _fixture(tmp_path, scenario="positive")
    output = tmp_path / "failing_confirmatory_run"

    def _fail(*args, **kwargs):
        raise RuntimeError("synthetic-analysis-failure")

    monkeypatch.setattr(runner, "summarize_third_network", _fail)

    with pytest.raises(RuntimeError, match="synthetic-analysis-failure"):
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

    assert not output.exists()
    assert not output.with_name(output.name + ".inprogress").exists()


def test_confirmatory_runner_refuses_stale_staging_directory(tmp_path) -> None:
    fixture = _fixture(tmp_path)
    output = tmp_path / "stale_run"
    staging = output.with_name(output.name + ".inprogress")
    staging.mkdir()
    (staging / "partial.json").write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="CONFIRMATORY_STAGING_DIR_EXISTS"):
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


def test_confirmatory_receipt_hashes_existing_network_analysis_inputs(tmp_path) -> None:
    _fixture_dir, _output, receipt = _run_production_fixture(tmp_path, scenario="null")
    for name, expected_n in (("sakhalkar", 6), ("aubert_ephi", 12)):
        entry = receipt["existing_network_inputs"][name]
        assert entry["analysis_units"] == expected_n
        assert len(entry["stable_json_sha256"]) == 64
        int(entry["stable_json_sha256"], 16)

    assert receipt["existing_network_inputs"]["sakhalkar"]["source_doi"] == "10.5281/zenodo.8398202"
    assert receipt["existing_network_inputs"]["aubert_ephi"]["source_doi"] == "10.5281/zenodo.14185547"


def test_production_repository_commit_requires_exact_sha(monkeypatch) -> None:
    monkeypatch.setattr(runner, "_current_checkout_commit", lambda: None)
    with pytest.raises(ValueError, match="exact 40-character git SHA"):
        _validate_production_repository_commit("TEST-COMMIT")

    sha = "a" * 40
    assert _validate_production_repository_commit(sha) == sha


def test_production_repository_commit_must_match_checkout_when_resolvable(monkeypatch) -> None:
    current = "b" * 40
    monkeypatch.setattr(runner, "_current_checkout_commit", lambda: current)
    with pytest.raises(ValueError, match="REPOSITORY_COMMIT_MISMATCH"):
        _validate_production_repository_commit("a" * 40)
    assert _validate_production_repository_commit(current) == current
