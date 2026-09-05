import json
import math
from pathlib import Path

from scripts.analyze_peucedanum_antagonist_proxy_criticality import analyze


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_ANTAGONIST_PROXY_CRITICALITY_INPUT_V1.json"


def test_proxy_point_estimates_are_definition_specific_but_inside_same_observed_bracket() -> None:
    result = analyze(json.loads(INPUT.read_text(encoding="utf-8")))
    definitions = result["definitions"]
    assert math.isclose(
        definitions["final_fruit_selection_gradient_beta"]["point_critical_proxy"],
        2.422539682539682,
        rel_tol=1e-12,
    )
    assert math.isclose(
        definitions["final_fruit_selection_differential_S"]["point_critical_proxy"],
        2.24,
        rel_tol=1e-12,
    )
    assert math.isclose(
        definitions["female_gain_exponent_b_minus_1"]["point_critical_proxy"],
        1.9507142857142856,
        rel_tol=1e-12,
    )
    for definition in definitions.values():
        assert 1.64 <= definition["point_critical_proxy"] <= 3.09


def test_published_coefficient_uncertainty_keeps_one_common_proxy_interval() -> None:
    result = analyze(json.loads(INPUT.read_text(encoding="utf-8")))
    assert result["classification"] == "SAME_NUMERIC_PROXY_CRITICAL_CONTEXT_COMPATIBLE"
    overlap = result["common_conditional_95_interval"]
    assert overlap is not None
    assert overlap[0] < overlap[1]
    assert 1.64 <= overlap[0] <= 3.09
    assert 1.64 <= overlap[1] <= 3.09


def test_gain_curve_crossing_is_less_certain_than_final_fruit_selection_crossings() -> None:
    result = analyze(json.loads(INPUT.read_text(encoding="utf-8")))
    definitions = result["definitions"]
    assert definitions["final_fruit_selection_gradient_beta"]["sign_consistent_draw_fraction"] > 0.98
    assert definitions["final_fruit_selection_differential_S"]["sign_consistent_draw_fraction"] > 0.99
    gain_fraction = definitions["female_gain_exponent_b_minus_1"]["sign_consistent_draw_fraction"]
    assert 0.65 < gain_fraction < 0.85


def test_proxy_analysis_does_not_promote_to_causal_c2_or_parallel_world_proof() -> None:
    result = analyze(json.loads(INPUT.read_text(encoding="utf-8")))
    assert "not_causal_C2" in result["claim_ceiling"]
    assert "not_parallel_world_proof" in result["claim_ceiling"]
    assert "egg_load_not_calibrated_functional_weight" in result["claim_ceiling"]
