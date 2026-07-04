from __future__ import annotations

from trait_architecture.impatiens_factorial_fitness_readout import render_readout


def _coefficient(term: str, estimate: float, lower: float, upper: float) -> dict[str, object]:
    return {
        "term": term,
        "estimate": estimate,
        "ci95_lower": lower,
        "ci95_upper": upper,
    }


def _model(analysis_id: str) -> dict[str, object]:
    coefficients = [
        _coefficient("Robbing_c", -0.1, -0.4, 0.2),
        _coefficient("Florivory_c", -0.3, -0.5, -0.1),
        _coefficient("Pollination_c", 0.2, -0.1, 0.5),
        _coefficient("Robbing_c:Florivory_c", 0.1, -0.2, 0.4),
        _coefficient("Robbing_c:Pollination_c", 0.0, -0.3, 0.3),
        _coefficient("Florivory_c:Pollination_c", 0.2, -0.1, 0.5),
        _coefficient("Robbing_c:Florivory_c:Pollination_c", -0.1, -0.4, 0.2),
        _coefficient("Phenology_z", -0.2, -0.4, 0.0),
    ]
    return {
        "analysis_id": analysis_id,
        "outcome_field": "component",
        "outcome_transform": "log1p",
        "outcome_definition": "component definition",
        "interpretation": "component interpretation",
        "treatment_coding": "effect-coded N=-0.5, Y=+0.5; full 2x2x2 factorial retained",
        "n_complete": 150,
        "n_omitted": 5,
        "r_squared": 0.2,
        "coefficients": coefficients,
    }


def test_readout_reports_full_factorial_and_component_boundary() -> None:
    report = {
        "design": "randomized 2x2x2",
        "treatment_coding": "effect-coded",
        "model_summaries": [
            _model("impatiens_factorial_ch_fruit_rate"),
            _model("impatiens_factorial_ch_seed_per_fruit"),
        ],
    }
    text = render_readout(report)
    assert "randomized assignment contrasts" in text
    assert "Supplemental florivory assignment" in text
    assert "Factorial interaction checks" in text
    assert "HC3 95% CI is entirely negative" in text
    assert "Part A A×D mixed partial" in text
    assert "c_AD" in text
