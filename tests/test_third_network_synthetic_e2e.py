from __future__ import annotations

import json

from scripts.run_third_network_synthetic_e2e import run


def test_third_network_synthetic_e2e_exercises_full_frozen_chain(tmp_path) -> None:
    receipt = run(tmp_path, permutations=49)

    assert receipt["status"] == "PASS"
    assert receipt["mode"] == "DEVELOPMENT_ONLY_SYNTHETIC"
    assert receipt["scientific_claim_allowed"] is False
    assert receipt["presurvey_status"] == "PRESURVEY_ROUTE_BLIND_ELIGIBLE_SITES_PRESENT"
    assert receipt["field_readiness_status"] == "THIRD_NETWORK_FIELD_EXECUTION_READY"
    assert receipt["input_freeze_status"] == "INPUTS_FROZEN_READY_FOR_JOIN"
    assert receipt["route_reliability_status"] == "ROUTE_RELIABILITY_PASS"
    assert receipt["route_reliability_kappa"] >= 0.8
    assert receipt["analysis_units"] == 72
    assert receipt["third_network_status"] == "CONFIRMATORY_GATE_PASS"
    assert receipt["third_network_rho"] > 0
    assert receipt["k3_network_count"] == 3

    saved = json.loads((tmp_path / "synthetic_e2e_receipt.json").read_text())
    assert saved == receipt
    assert len(receipt["files"]) >= 10


def test_synthetic_e2e_receipt_never_licenses_scientific_claim(tmp_path) -> None:
    receipt = run(tmp_path, permutations=19)
    assert receipt["scientific_claim_allowed"] is False
    assert "not ecological observations" in receipt["claim_boundary"]



def test_null_synthetic_third_network_is_retained_not_replaced(tmp_path) -> None:
    receipt = run(tmp_path, permutations=29, scenario="null")
    assert receipt["status"] == "PASS"
    assert receipt["scenario"] == "null"
    assert receipt["third_network_status"] == "CONFIRMATORY_GATE_PASS"
    assert abs(receipt["third_network_rho"]) < 0.1
    assert receipt["k3_network_count"] == 3
    assert receipt["scientific_claim_allowed"] is False


def test_opposite_synthetic_third_network_is_retained_in_k3(tmp_path) -> None:
    receipt = run(tmp_path, permutations=29, scenario="opposite")
    assert receipt["status"] == "PASS"
    assert receipt["scenario"] == "opposite"
    assert receipt["third_network_status"] == "CONFIRMATORY_GATE_PASS"
    assert receipt["third_network_rho"] < 0
    assert receipt["k3_network_count"] == 3
    assert receipt["k3_direction_concordance"] == "not_3_of_3_positive"
    assert receipt["scientific_claim_allowed"] is False
