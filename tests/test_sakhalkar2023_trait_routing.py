from __future__ import annotations

import math

from scripts.analyze_sakhalkar2023_trait_routing import (
    benjamini_hochberg,
    build_species_trait_rows,
    fit_source_defined_model,
    fit_source_model_set,
    trait_coverage_summary,
)


def _synthetic():
    visits = []
    traits = []
    shapes = ["open", "open", "open", "open", "tubular", "tubular", "tubular", "tubular"]
    for i in range(8):
        sp = f"S{i}"
        rob = float(i + 1)
        thief = float(8 - i)
        visits.extend([
            {"spcode": sp, "behavior": "robbing", "freq_fm_per_species": str(rob)},
            {"spcode": sp, "behavior": "thieving", "freq_fm_per_species": str(thief)},
        ])
        traits.append({
            "spcode": sp,
            "tube_length": str(i + 1),
            "tube_width": str(2 + (i % 3)),
            "brightness": str(10 - i),
            "shape": shapes[i],
        })
    return visits, traits


def test_species_trait_rows_are_anonymous_and_source_defined() -> None:
    visits, traits = _synthetic()
    rows = build_species_trait_rows(visits, traits)

    assert len(rows) == 8
    assert all(set(row) == {
        "route_balance", "tube_length", "tube_width", "brightness", "shape"
    } for row in rows)
    assert all("spcode" not in row for row in rows)


def test_source_defined_model_returns_bounded_permutation_results() -> None:
    visits, traits = _synthetic()
    rows = build_species_trait_rows(visits, traits)
    result = fit_source_defined_model(rows, permutations=199, seed=11)

    assert result["n_species_complete"] == 8
    assert result["predictor_blocks"] == ["tube_length", "tube_width", "brightness", "shape"]
    assert 0.0 <= result["full_model_r2"] <= 1.0
    assert 0.0 < result["full_model_permutation_p"] <= 1.0
    assert set(result["block_tests"]) == {"tube_length", "tube_width", "brightness", "shape"}
    assert all(0.0 <= item["delta_r2"] <= 1.0 for item in result["block_tests"].values())
    assert all(0.0 < item["permutation_p"] <= 1.0 for item in result["block_tests"].values())
    assert all(0.0 < item["bh_q"] <= 1.0 for item in result["block_tests"].values())


def test_bh_is_monotone_after_sorting() -> None:
    q = benjamini_hochberg({
        "a": 0.001,
        "b": 0.02,
        "c": 0.04,
        "d": 0.5,
    })
    assert q["a"] <= q["b"] <= q["c"] <= q["d"]
    assert all(0.0 < value <= 1.0 for value in q.values())


def test_missing_source_defined_trait_excludes_species_from_complete_model() -> None:
    visits, traits = _synthetic()
    traits[0]["brightness"] = ""
    rows = build_species_trait_rows(visits, traits)
    result = fit_source_defined_model(rows, permutations=49, seed=2)
    assert result["n_species_complete"] == 7


def test_trait_coverage_reports_source_model_complete_cases() -> None:
    visits, traits = _synthetic()
    traits[0]["brightness"] = ""
    traits[1]["tube_width"] = ""
    rows = build_species_trait_rows(visits, traits)
    coverage = trait_coverage_summary(rows)

    assert coverage["cheating_species"] == 8
    assert coverage["nonmissing"]["tube_length"] == 8
    assert coverage["nonmissing"]["tube_width"] == 7
    assert coverage["nonmissing"]["brightness"] == 7
    assert coverage["nonmissing"]["shape"] == 8
    assert coverage["robber_source_complete"] == 7
    assert coverage["thief_source_complete"] == 7
    assert coverage["union_complete"] == 6


def test_source_model_set_fits_available_models_without_imputation() -> None:
    visits, traits = _synthetic()
    for i in range(4):
        traits[i]["brightness"] = ""
    rows = build_species_trait_rows(visits, traits)
    result = fit_source_model_set(rows, permutations=49, seed=5)

    assert result["coverage"]["cheating_species"] == 8
    assert result["models"]["robber_source_predictors"]["status"] == "FIT"
    assert result["models"]["thief_source_predictors"]["status"] == "INSUFFICIENT_COMPLETE_CASES"
    assert result["models"]["union_predictors"]["status"] == "INSUFFICIENT_COMPLETE_CASES"
