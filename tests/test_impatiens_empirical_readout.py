from __future__ import annotations

from trait_architecture.impatiens_empirical_readout import render_readout


def _coefficient(term: str, estimate: float, lower: float, upper: float) -> dict[str, object]:
    return {
        "term": term,
        "estimate": estimate,
        "ci95_lower": lower,
        "ci95_upper": upper,
    }


def _model(analysis_id: str, n: int, coefficients: list[dict[str, object]]) -> dict[str, object]:
    return {"analysis_id": analysis_id, "n_complete": n, "coefficients": coefficients}


def test_render_readout_reports_all_paths_and_component_boundaries() -> None:
    report = {
        "model_summaries": [
            _model("impatiens_pollination_path", 81, [
                _coefficient("A_z", 0.01, -0.23, 0.25),
                _coefficient("B_z", -0.18, -0.42, 0.06),
            ]),
            _model("impatiens_antagonism_path", 154, [
                _coefficient("A_z", -0.09, -0.23, 0.04),
                _coefficient("B_z", 0.09, -0.06, 0.24),
            ]),
            _model("impatiens_ch_fruit_surface", 170, [
                _coefficient("A_z:B_z", -0.08, -0.19, 0.03),
            ]),
            _model("impatiens_ch_seed_surface", 85, [
                _coefficient("A_z:B_z", 0.10, -0.10, 0.31),
            ]),
        ]
    }
    text = render_readout(report)
    assert "A (flower redness) → pollinator visitation" in text
    assert "D candidate (floral tannins) → natural florivory" in text
    assert text.count("95% CI crosses zero") == 6
    assert "not a total lifetime reproductive-fitness surface" in text
    assert "do not identify the Part A mixed partial" in text
    assert "causal trait-manipulation effects" in text
