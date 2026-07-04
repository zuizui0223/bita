from __future__ import annotations

from trait_architecture.impatiens_response_scale_models import (
    _processed_by_plot,
    _processed_rate_records,
    _raw_records,
    _serialize_model,
)


def _config() -> dict:
    return {
        "trait_predictors": {
            "A_flower": {"field": "Early_Season_Flower_Redness"},
            "D_candidate": {"field": "Early_Season_Condensed_Tannins"},
            "phenology": {"field": "Date_of_First_CH_Flower"},
        }
    }


def _processed(plot: str, a: float, b: float, phenology: float, rate: float) -> dict[str, str]:
    return {
        "Plot_Number": plot,
        "Early_Season_Flower_Redness": str(a),
        "Early_Season_Condensed_Tannins": str(b),
        "Date_of_First_CH_Flower": str(phenology),
        "Robbing": "N",
        "Florivory": "Y" if int(plot) % 2 else "N",
        "Pollination": "Y" if int(plot) % 3 else "N",
        "Pollinators_Per_Hour": str(rate),
    }


def test_processed_rate_uses_plant_level_counts_without_offset() -> None:
    processed = [_processed(str(index), index, index + 1, 100 + index, index % 4) for index in range(1, 12)]
    records, omitted = _processed_rate_records(processed, _config(), "Pollinators_Per_Hour")
    assert omitted == 0
    assert len(records) == 11
    assert records[0]["y"] == 1.0
    assert "Seconds" not in records[0]


def test_flower_percent_is_fractional_response_not_binomial_trials() -> None:
    processed = [_processed(str(index), index, index + 1, 100 + index, index % 4) for index in range(1, 12)]
    indexed = _processed_by_plot(processed)
    model = {
        "outcome_field": "Per_Florivory",
        "outcome_scale": "percent_to_fraction",
        "cluster_field": "Plot",
        "family": "fractional_logit",
        "interaction": False,
    }
    raw = [
        {"Plot": str(index), "Per_Florivory": str((index * 7) % 100), "Tot_Flwrs": "10"}
        for index in range(1, 12)
    ]
    records, omitted = _raw_records(raw, indexed, _config(), model)
    assert omitted == 0
    assert records[0]["y"] == 0.07
    assert records[0]["cluster"] == "1"
    result = _serialize_model(model | {"analysis_id": "h", "source_table": "Raw_Florivory_Data.csv", "response_contract": "x", "inference_contract": "x"}, records, omitted)
    assert result["cluster_count"] == 11
    assert result["family"] == "fractional_logit"


def test_seed_filter_keeps_ch_fruit_records_only() -> None:
    processed = [_processed(str(index), index, index + 1, 100 + index, index % 4) for index in range(1, 12)]
    indexed = _processed_by_plot(processed)
    model = {
        "outcome_field": "Num_Seeds",
        "filter_field": "Fruit_type",
        "filter_value": "CH",
        "family": "poisson_log",
        "interaction": True,
    }
    raw = []
    for index in range(1, 12):
        raw.append({"Plot": str(index), "Fruit_type": "CH", "Num_Seeds": str(1 + index % 5)})
        raw.append({"Plot": str(index), "Fruit_type": "CL", "Num_Seeds": "4"})
    records, omitted = _raw_records(raw, indexed, _config(), model)
    assert omitted == 0
    assert len(records) == 11
    assert all(record["y"] >= 1 for record in records)
    result = _serialize_model(model | {"analysis_id": "seed", "source_table": "Raw_Seed_Data.csv", "response_contract": "x", "inference_contract": "x"}, records, omitted)
    assert result["cluster_count"] == 11
    assert any(item["term"] == "A_z:D_z" for item in result["coefficients"])
