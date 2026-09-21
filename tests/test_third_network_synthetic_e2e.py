from __future__ import annotations

import json

from scripts.run_third_network_synthetic_e2e import run


def test_positive_synthetic_e2e_reaches_k3_without_shortcuts(tmp_path) -> None:
    result = run(tmp_path / "positive", scenario="positive", permutations=49)

    assert result["status"] == "DEVELOPMENT_SYNTHETIC_ONLY"
    assert result["field_readiness_status"] == "THIRD_NETWORK_FIELD_EXECUTION_READY"
    assert result["input_freeze_status"] == "INPUTS_FROZEN_READY_FOR_JOIN"
    assert result["double_code_fraction"] >= 0.2
    assert result["double_code_fraction"] < 0.21
    assert result["cohen_kappa_LBAN"] == 1.0
    assert result["verified_join_input_count"] == 6
    assert result["third_gate"]["n_units"] == 72
    assert result["third_gate"]["n_visitor_species"] == 6
    assert result["third_gate"]["n_plant_species"] == 6
    assert result["third_rho"] > 0
    assert result["network_direction_concordance"] == "3_of_3_positive"
    assert "not ecological evidence" in result["claim_boundary"]

    summary = json.loads(
        (tmp_path / "positive" / "synthetic_e2e_summary.json").read_text(encoding="utf-8")
    )
    assert summary == result


def test_opposite_third_network_is_retained_not_reselected(tmp_path) -> None:
    result = run(tmp_path / "opposite", scenario="opposite", permutations=49)

    assert result["field_readiness_status"] == "THIRD_NETWORK_FIELD_EXECUTION_READY"
    assert result["input_freeze_status"] == "INPUTS_FROZEN_READY_FOR_JOIN"
    assert result["third_gate"]["n_units"] == 72
    assert result["third_rho"] < 0
    assert result["network_direction_concordance"] == "not_3_of_3_positive"
    assert 0 < result["third_p"] <= 1
    assert 0 < result["joint_k3_p"] <= 1


def test_orthogonal_synthetic_network_still_passes_sampling_gate(tmp_path) -> None:
    result = run(tmp_path / "orthogonal", scenario="orthogonal", permutations=29)

    assert result["third_gate"]["n_units"] == 72
    assert result["third_gate"]["total_bypass_events"] > 0
    assert result["third_gate"]["total_legitimate_events"] > 0
    assert result["status"] == "DEVELOPMENT_SYNTHETIC_ONLY"


def test_e2e_receipts_are_hash_bound(tmp_path) -> None:
    result = run(tmp_path / "hashes", scenario="positive", permutations=9)
    root = tmp_path / "hashes"

    for filename, expected in result["files"].items():
        path = root / filename
        assert path.exists()
        import hashlib
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
