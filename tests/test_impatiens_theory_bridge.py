from __future__ import annotations

from trait_architecture.impatiens_theory_bridge import render_bridge


def _ratio(term: str, ratio: float, lower: float, upper: float) -> dict[str, object]:
    return {
        "term": term,
        "exp_estimate": ratio,
        "exp_ci95_lower": lower,
        "exp_ci95_upper": upper,
    }


def _coefficient(term: str, estimate: float, lower: float, upper: float) -> dict[str, object]:
    return {
        "term": term,
        "estimate": estimate,
        "ci95_lower": lower,
        "ci95_upper": upper,
    }


def _response_model(analysis_id: str, coefficients: list[dict[str, object]], *, role: str = "primary_response_scale_model", n: int = 81, mean: float = 5.0, dispersion: float = 1.0) -> dict[str, object]:
    return {
        "analysis_id": analysis_id,
        "analysis_role": role,
        "n_response_records": n,
        "mean_response": mean,
        "pearson_dispersion": dispersion,
        "coefficients": coefficients,
    }


def _factorial_model(analysis_id: str, coefficients: list[dict[str, object]]) -> dict[str, object]:
    return {"analysis_id": analysis_id, "coefficients": coefficients}


def test_bridge_reports_component_status_without_claiming_exact_mixed_partial() -> None:
    response = {
        "model_summaries": [
            _response_model("impatiens_pollinator_rate_quasi_poisson", [_ratio("A_z", 1.0, 0.8, 1.2), _ratio("D_z", 0.7, 0.5, 0.9)], dispersion=20.0),
            _response_model("impatiens_pollinator_presence_hurdle_sensitivity", [_ratio("D_z", 0.8, 0.5, 1.3)], role="post_primary_model_adequacy_sensitivity"),
            _response_model("impatiens_pollinator_positive_rate_hurdle_sensitivity", [_ratio("D_z", 0.8, 0.6, 0.95)], role="post_primary_model_adequacy_sensitivity", n=35),
            _response_model("impatiens_flower_level_florivory_fractional_logit", [_ratio("A_z", 1.0, 0.8, 1.2), _ratio("D_z", 1.1, 0.9, 1.3)], n=760),
            _response_model("impatiens_ch_seed_count_quasi_poisson", [_ratio("A_z:D_z", 1.0, 0.9, 1.1)], n=439),
        ]
    }
    factorial = {
        "model_summaries": [
            _factorial_model("impatiens_factorial_ch_fruit_rate", [_coefficient("Florivory_c", -0.3, -0.5, -0.1), _coefficient("Phenology_z", -0.4, -0.6, -0.2)]),
            _factorial_model("impatiens_factorial_ch_seed_per_fruit", [_coefficient("Florivory_c", -0.2, -0.6, 0.2)]),
        ]
    }
    text = render_bridge(response, factorial)
    assert "directionally consistent association" in text
    assert "directionally consistent experimental effect" in text
    assert "not resolve a protective `e_F` direction" in text
    assert "does **not** estimate the exact mixed partial" in text
    assert "c_AD" in text
    assert "case-study constraint on the theory" in text
