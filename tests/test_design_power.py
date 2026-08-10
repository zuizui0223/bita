from __future__ import annotations

import pytest

from trait_architecture.design_power import (
    PowerScenario,
    declared_scenario_grid,
    minimum_adequate_cluster_count,
    run_power_grid,
    simulate_scenario,
)


def test_scenario_rejects_a_design_that_cannot_be_analysed() -> None:
    with pytest.raises(ValueError, match="at least two clusters"):
        PowerScenario("bad", 1, -0.5, 0.2)
    with pytest.raises(ValueError, match="standard-error bounds"):
        PowerScenario("bad", 3, -0.5, 0.2, standard_error_low=0.4, standard_error_high=0.1)


def test_declared_tests_stay_calibrated_under_the_null() -> None:
    """Regression guard for the two defects the power analysis exposed.

    Before the fix, the verdict rule reported a direction reversal whenever the
    pooled level directions differed in sign, which happens about half the time
    when the true level effect is zero. The reversal rate under the null must
    stay near zero, and the meta-regression contrast must stay near its nominal
    5%, at the heterogeneity where the old rule failed worst.
    """

    result = simulate_scenario(
        PowerScenario("null_k3_tau050", clusters_per_level=3, level_contrast=0.0, between_cluster_sd=0.50),
        replicates=600,
        seed=99,
    )

    assert float(result["meta_regression_contrast_power"]) < 0.10
    assert float(result["direction_reversal_detection_rate"]) < 0.05


def test_fixed_effect_q_between_is_documented_as_uncalibrated() -> None:
    """The reason Q_between is reported descriptively rather than as a test."""

    calibrated = simulate_scenario(
        PowerScenario("null_tau0", clusters_per_level=5, level_contrast=0.0, between_cluster_sd=0.0),
        replicates=600,
        seed=99,
    )
    heterogeneous = simulate_scenario(
        PowerScenario("null_tau050", clusters_per_level=5, level_contrast=0.0, between_cluster_sd=0.50),
        replicates=600,
        seed=99,
    )

    assert float(calibrated["q_between_fixed_effect_rejection_rate"]) < 0.10
    assert float(heterogeneous["q_between_fixed_effect_rejection_rate"]) > 0.25


def test_power_rises_with_cluster_count_and_contrast_size() -> None:
    small = simulate_scenario(
        PowerScenario("small", clusters_per_level=3, level_contrast=-0.35, between_cluster_sd=0.25),
        replicates=400,
        seed=5,
    )
    large = simulate_scenario(
        PowerScenario("large", clusters_per_level=12, level_contrast=-1.10, between_cluster_sd=0.25),
        replicates=400,
        seed=5,
    )

    assert float(small["meta_regression_contrast_power"]) < float(large["meta_regression_contrast_power"])
    assert large["design_verdict"] == "declared_design_adequate"


def test_declared_grid_covers_the_protocol_minimum_and_reports_verdicts() -> None:
    scenarios = declared_scenario_grid()

    assert min(scenario.clusters_per_level for scenario in scenarios) == 3
    assert all(scenario.level_contrast < 0 for scenario in scenarios)

    rows = run_power_grid(scenarios[:2], replicates=200)
    allowed = {
        "declared_design_adequate",
        "declared_design_underpowered_null_uninformative",
        "declared_design_cannot_answer",
    }
    assert {row["design_verdict"] for row in rows} <= allowed
    assert minimum_adequate_cluster_count(rows, -99.0, 0.0) is None
