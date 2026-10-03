from __future__ import annotations

import math
import random

from scripts.analyze_aubert2026_routing_threshold import (
    analyze_points,
    classify_threshold,
    fit_sigmoid_threshold,
    upper_turnover_diagnostic,
)


def _sigmoid_points(
    *,
    xstar: float,
    slope: float = 5.0,
    lower: float = 0.10,
    upper: float = 0.80,
    n: int = 121,
) -> list[dict[str, float]]:
    points = []
    for i in range(n):
        x = -1.5 + 3.0 * i / (n - 1)
        q = 1.0 / (1.0 + math.exp(-slope * (x - xstar)))
        y = lower + (upper - lower) * q
        points.append({"mismatch": x, "robbery_rate": y})
    return points


def test_sigmoid_fit_recovers_threshold_near_zero() -> None:
    points = _sigmoid_points(xstar=0.0)
    fit = fit_sigmoid_threshold(
        [p["mismatch"] for p in points],
        [p["robbery_rate"] for p in points],
    )
    assert abs(float(fit["xstar"])) < 0.03
    assert 4.0 < float(fit["k"]) < 6.0
    assert float(fit["amplitude"]) > 0.6


def test_threshold_classification_requires_equivalence_not_zero_inclusion() -> None:
    fit = {
        "amplitude": 0.6,
        "at_search_boundary": False,
    }
    near = classify_threshold(
        fit,
        {
            "finite_fraction": 1.0,
            "ci90_xstar": [-0.10, 0.12],
        },
    )
    assert near == "THRESHOLD_NEAR_EQUALITY"

    unresolved = classify_threshold(
        fit,
        {
            "finite_fraction": 1.0,
            "ci90_xstar": [-0.30, 0.10],
        },
    )
    assert unresolved == "THRESHOLD_LOCATION_UNRESOLVED"


def test_threshold_classification_detects_displacement() -> None:
    fit = {"amplitude": 0.6, "at_search_boundary": False}
    high = classify_threshold(
        fit,
        {"finite_fraction": 1.0, "ci90_xstar": [0.30, 0.60]},
    )
    assert high == "THRESHOLD_ABOVE_EQUALITY"


def test_upper_turnover_detects_interior_peak_on_synthetic_data() -> None:
    rng = random.Random(123)
    points = []
    for i in range(121):
        x = -1.5 + 3.0 * i / 120
        y = 0.65 - 0.22 * (x - 0.25) ** 2 + rng.gauss(0, 0.015)
        points.append((x, y))
    result = upper_turnover_diagnostic(
        [x for x, _ in points],
        [y for _, y in points],
        permutations=499,
        seed=456,
    )
    assert result["classification"] == "INTERIOR_UPPER_TURNOVER_SUPPORTED"
    assert float(result["quadratic"]["quadratic"]) < 0
    assert float(result["curvature_permutation_p"]) < 0.05


def test_full_analysis_runs_on_sigmoid_without_promoting_turnover() -> None:
    result = analyze_points(
        _sigmoid_points(xstar=0.0),
        bootstraps=99,
        permutations=199,
        seed=42,
    )
    assert result["n_plant_species"] == 121
    assert result["threshold_classification"] in {
        "THRESHOLD_NEAR_EQUALITY",
        "THRESHOLD_LOCATION_UNRESOLVED",
    }
    assert result["primary_sigmoid"]["amplitude"] > 0.5
