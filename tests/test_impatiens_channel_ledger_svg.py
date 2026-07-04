from __future__ import annotations

from trait_architecture.impatiens_channel_ledger_svg import render_svg


def _ratio(term: str, ratio: float, lower: float, upper: float) -> dict[str, object]:
    return {"term": term, "exp_estimate": ratio, "exp_ci95_lower": lower, "exp_ci95_upper": upper}


def _coefficient(term: str, estimate: float, lower: float, upper: float) -> dict[str, object]:
    return {"term": term, "estimate": estimate, "ci95_lower": lower, "ci95_upper": upper}


def _response_model(analysis_id: str, coefficients: list[dict[str, object]]) -> dict[str, object]:
    return {"analysis_id": analysis_id, "coefficients": coefficients}


def _factorial_model(analysis_id: str, coefficients: list[dict[str, object]]) -> dict[str, object]:
    return {"analysis_id": analysis_id, "coefficients": coefficients}


def test_svg_labels_observational_and_randomized_edges() -> None:
    response = {
        "model_summaries": [
            _response_model("impatiens_pollinator_rate_quasi_poisson", [_ratio("A_z", 0.95, 0.65, 1.39), _ratio("D_z", 0.68, 0.48, 0.97)]),
            _response_model("impatiens_flower_level_florivory_fractional_logit", [_ratio("A_z", 1.07, 0.92, 1.24), _ratio("D_z", 1.12, 0.99, 1.27)]),
            _response_model("impatiens_ch_seed_count_quasi_poisson", [_ratio("A_z:D_z", 1.01, 0.97, 1.05)]),
        ]
    }
    factorial = {
        "model_summaries": [
            _factorial_model("impatiens_factorial_ch_fruit_rate", [_coefficient("Florivory_c", -0.29, -0.54, -0.04), _coefficient("Phenology_z", -0.49, -0.62, -0.37)]),
        ]
    }
    svg = render_svg(response, factorial)
    assert svg.startswith("<svg")
    assert "Dashed = observational trait association" in svg
    assert "randomized imposed-florivory effect" in svg
    assert "obs RR 0.68 [0.48, 0.97]" in svg
    assert "β -0.29 [-0.54, -0.04]" in svg
    assert "c_AD estimate" in svg
    assert "stroke-dasharray" in svg
