from __future__ import annotations

from trait_architecture.impatiens_response_scale_readout import render_readout


def _coefficient(term: str, ratio: float, lower: float, upper: float) -> dict[str, object]:
    return {
        "term": term,
        "exp_estimate": ratio,
        "exp_ci95_lower": lower,
        "exp_ci95_upper": upper,
    }


def _model(analysis_id: str, family: str, coefficients: list[dict[str, object]], role: str = "primary_response_scale_model") -> dict[str, object]:
    return {
        "analysis_id": analysis_id,
        "analysis_role": role,
        "family": family,
        "source_table": "table.csv",
        "outcome_field": "response",
        "response_rule": "as_recorded",
        "response_contract": "declared response",
        "inference_contract": "declared robust inference",
        "n_response_records": 100,
        "cluster_count": 25,
        "n_omitted": 3,
        "n_filtered_by_rule": 0,
        "mean_response": 1.2,
        "pearson_dispersion": 1.5,
        "predictor_standardization_unit": "plant",
        "coefficients": coefficients,
    }


def test_readout_labels_primary_hurdle_and_component_boundaries() -> None:
    report = {
        "model_summaries": [
            _model("impatiens_pollinator_rate_quasi_poisson", "poisson_log", [
                _coefficient("A_z", 1.2, 0.8, 1.7),
                _coefficient("D_z", 0.9, 0.6, 1.4),
            ]),
            _model("impatiens_pollinator_presence_hurdle_sensitivity", "fractional_logit", [
                _coefficient("A_z", 1.1, 0.8, 1.5),
                _coefficient("D_z", 0.7, 0.5, 0.9),
            ], "post_primary_model_adequacy_sensitivity"),
            _model("impatiens_pollinator_positive_rate_hurdle_sensitivity", "poisson_log", [
                _coefficient("A_z", 1.0, 0.7, 1.4),
                _coefficient("D_z", 0.9, 0.6, 1.3),
            ], "post_primary_model_adequacy_sensitivity"),
            _model("impatiens_flower_level_florivory_fractional_logit", "fractional_logit", [
                _coefficient("A_z", 0.7, 0.5, 0.9),
                _coefficient("D_z", 1.1, 0.7, 1.8),
            ]),
            _model("impatiens_ch_seed_count_quasi_poisson", "poisson_log", [
                _coefficient("A_z", 1.0, 0.8, 1.2),
                _coefficient("D_z", 1.1, 0.9, 1.3),
                _coefficient("A_z:D_z", 0.8, 0.6, 1.0),
            ]),
        ]
    }
    text = render_readout(report)
    assert "Primary response-scale models" in text
    assert "Pollinator hurdle model-adequacy sensitivity" in text
    assert "post-primary diagnostic sensitivities" in text
    assert "rate ratio per 1 SD" in text
    assert "odds ratio per 1 SD" in text
    assert "robust 95% interval is below 1" in text
    assert "Part A mixed partial" in text
    assert "c_AD" in text
