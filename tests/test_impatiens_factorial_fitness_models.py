from __future__ import annotations

from trait_architecture.impatiens_factorial_fitness_models import (
    _design,
    _effect_code,
    _prepare_records,
)


def _config() -> dict:
    return {
        "phenology_adjustment": {
            "field": "Date_of_First_CH_Flower",
            "transform": "identity_then_zscore",
        }
    }


def _row(robbing: str, florivory: str, pollination: str, fruit: float, seed: float, phenology: float) -> dict[str, str]:
    return {
        "Robbing": robbing,
        "Florivory": florivory,
        "Pollination": pollination,
        "Average_CH_Fruits_Per_Day": str(fruit),
        "Average_Seeds_Per_CH_Fruit": str(seed),
        "Date_of_First_CH_Flower": str(phenology),
    }


def test_effect_coding_is_centered() -> None:
    assert _effect_code("N", "Florivory") == -0.5
    assert _effect_code("Y", "Florivory") == 0.5


def test_design_keeps_all_factorial_interactions() -> None:
    records = []
    index = 0
    for robbing in ("N", "Y"):
        for florivory in ("N", "Y"):
            for pollination in ("N", "Y"):
                for replicate in range(2):
                    index += 1
                    row = _row(
                        robbing,
                        florivory,
                        pollination,
                        fruit=1.0 + index / 10,
                        seed=2.0 + index,
                        phenology=100.0 + (index * 3) % 11,
                    )
                    prepared, omitted = _prepare_records(
                        [row],
                        {"outcome_field": "Average_CH_Fruits_Per_Day", "outcome_transform": "log1p"},
                        "Date_of_First_CH_Flower",
                    )
                    assert omitted == 0
                    records.extend(prepared)
    y, design, terms = _design(records)
    assert len(y) == 16
    assert len(design) == 16
    assert terms == [
        "Intercept",
        "Robbing_c",
        "Florivory_c",
        "Pollination_c",
        "Robbing_c:Florivory_c",
        "Robbing_c:Pollination_c",
        "Florivory_c:Pollination_c",
        "Robbing_c:Florivory_c:Pollination_c",
        "Phenology_z",
    ]
    first = design[0]
    assert first[1:4] == [-0.5, -0.5, -0.5]
    assert first[4:8] == [0.25, 0.25, 0.25, -0.125]


def test_missing_outcomes_are_omitted_without_dropping_factorial_terms() -> None:
    rows = [
        _row("N", "N", "N", fruit=1.0, seed=2.0, phenology=100.0),
        _row("Y", "Y", "Y", fruit=2.0, seed=3.0, phenology=101.0),
        _row("N", "Y", "N", fruit=float("nan"), seed=4.0, phenology=102.0),
    ]
    records, omitted = _prepare_records(
        rows,
        {"outcome_field": "Average_CH_Fruits_Per_Day", "outcome_transform": "log1p"},
        "Date_of_First_CH_Flower",
    )
    assert len(records) == 2
    assert omitted == 1
