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
        "Robbing": "Y" if int(plot) % 4 == 0 else "N",
        "Florivory": "Y" if int(plot) % 2 else "N",
        "Pollination": "Y" if int(plot) % 3 else "N",
        "Pollinators_Per_Hour": str(rate),
    }


def _processed_rows() -> list[dict[str, str]]:
    return [
        _processed(
            str(index),
            float(index),
            float((index * index) % 13 + 1),
            float(100 + (index * 3) % 7),
            float(index % 4),
        )
        for index in range(1, 18)
    ]


def _rate_model(rule: str) -> dict:
    return {
        "outcome_field": "Pollinators_Per_Hour",
        "response_rule": rule,
        "family": "fractional_logit" if rule == "binary_nonzero" else "poisson_log",
        "interaction": False,
        "analysis_id": rule,
        "source_table": "Processed_Data.csv",
        "response_contract": "x",
        "inference_contract": "x",
    }


def test_processed_rate_uses_plant_level_counts_without_offset() -> None:
    records, omitted, filtered = _processed_rate_records(_processed_rows(), _config(), _rate_model("as_recorded"))
    assert omitted == 0
    assert filtered == 0
    assert len(records) == 17
    assert records[0]["y"] == 1.0
    assert "Seconds" not in records[0]


def test_pollinator_hurdle_rules_are_explicit() -> None:
    binary, omitted_binary, filtered_binary = _processed_rate_records(_processed_rows(), _config(), _rate_model("binary_nonzero"))
    positive, omitted_positive, filtered_positive = _processed_rate_records(_processed_rows(), _config(), _rate_model("positive_only"))
    assert omitted_binary == omitted_positive == 0
    assert filtered_binary == 0
    assert set(record["y"] for record in binary).issubset({0.0, 1.0})
    assert filtered_positive == 4
    assert len(positive) == 13
    assert all(record["y"] > 0 for record in positive)


def test_flower_percent_is_fractional_response_not_binomial_trials() -> None:
    indexed = _processed_by_plot(_processed_rows())
    model = {
        "outcome_field": "Per_Florivory",
        "outcome_scale": "percent_to_fraction",
        "cluster_field": "Plot",
        "family": "fractional_logit",
        "interaction": False,
    }
    raw = [
        {"Plot": str(index), "Per_Florivory": str((index * 7) % 100), "Tot_Flwrs": "10"}
        for index in range(1, 18)
    ]
    records, omitted, filtered = _raw_records(raw, indexed, _config(), model)
    assert omitted == 0
    assert filtered == 0
    assert records[0]["y"] == 0.07
    assert records[0]["cluster"] == "1"
    result = _serialize_model(
        model | {
            "analysis_id": "h",
            "source_table": "Raw_Florivory_Data.csv",
            "response_contract": "x",
            "inference_contract": "x",
        },
        records,
        omitted,
        filtered,
    )
    assert result["cluster_count"] == 17
    assert result["family"] == "fractional_logit"


def test_seed_filter_keeps_ch_fruit_records_only() -> None:
    indexed = _processed_by_plot(_processed_rows())
    model = {
        "outcome_field": "Num_Seeds",
        "filter_field": "Fruit_type",
        "filter_value": "CH",
        "family": "poisson_log",
        "interaction": True,
    }
    raw = []
    for index in range(1, 18):
        raw.append({"Plot": str(index), "Fruit_type": "CH", "Num_Seeds": str(1 + index % 5)})
        raw.append({"Plot": str(index), "Fruit_type": "CL", "Num_Seeds": "4"})
    records, omitted, filtered = _raw_records(raw, indexed, _config(), model)
    assert omitted == 0
    assert filtered == 17
    assert len(records) == 17
    assert all(record["y"] >= 1 for record in records)
    result = _serialize_model(
        model | {
            "analysis_id": "seed",
            "source_table": "Raw_Seed_Data.csv",
            "response_contract": "x",
            "inference_contract": "x",
        },
        records,
        omitted,
        filtered,
    )
    assert result["cluster_count"] == 17
    assert any(item["term"] == "A_z:D_z" for item in result["coefficients"])
