from __future__ import annotations

import math

import pytest

from scripts import analyze_peucedanum_causal_selection as stage_a
from scripts import analyze_peucedanum_stage_b_fitness as stage_b_fitness
from scripts import evaluate_peucedanum_stage_b_manipulation as stage_b_validation
from trait_architecture.scale_free_stats import (
    population_sd,
    sample_sd,
    standardized_mean_difference,
    zscore,
)


def test_zscore_is_invariant_to_positive_unit_rescaling():
    reference = zscore([1.0, 2.0, 3.0])
    for scale in (1e-16, 1e-8, 1.0, 1e8, 1e16):
        values = [scale, 2.0 * scale, 3.0 * scale]
        observed = zscore(values)
        assert observed == pytest.approx(reference, rel=2e-15, abs=2e-15)
        assert stage_a._zscore(values) == pytest.approx(reference, rel=2e-15, abs=2e-15)


def test_sample_and_population_sd_transform_with_units_without_disappearing():
    reference_sample = sample_sd([1.0, 2.0, 3.0])
    reference_population = population_sd([1.0, 2.0, 3.0])
    for scale in (1e-16, 1e-8, 1.0, 1e8, 1e16):
        values = [scale, 2.0 * scale, 3.0 * scale]
        assert sample_sd(values) == pytest.approx(reference_sample * scale, rel=2e-15)
        assert population_sd(values) == pytest.approx(reference_population * scale, rel=2e-15)
        assert stage_a._sample_sd(values) == pytest.approx(reference_sample * scale, rel=2e-15)
        assert stage_b_validation._sample_sd(values) == pytest.approx(reference_sample * scale, rel=2e-15)
        assert stage_b_fitness._population_sd(values) == pytest.approx(reference_population * scale, rel=2e-15)


def test_standardized_mean_difference_is_unit_invariant_in_both_peucedanum_routes():
    for scale in (1e-16, 1e-8, 1.0, 1e8, 1e16):
        a = [1.0 * scale, 2.0 * scale, 3.0 * scale]
        b = [2.0 * scale, 3.0 * scale, 4.0 * scale]
        assert standardized_mean_difference(a, b) == pytest.approx(1.0, rel=2e-15)
        assert stage_b_validation._pairwise_smd(a, b) == pytest.approx(1.0, rel=2e-15)

        rows = [
            {"g_state": stage_a.G_REMOVED, "x": str(value)} for value in a
        ] + [
            {"g_state": stage_a.G_RETAINED, "x": str(value)} for value in b
        ]
        assert stage_a._smd(rows, "x") == pytest.approx(1.0, rel=2e-15)


def test_exactly_constant_inputs_keep_fail_closed_degeneracy_semantics():
    with pytest.raises(ValueError, match="constant variable"):
        zscore([2.0, 2.0, 2.0])
    with pytest.raises(ValueError, match="constant outcome"):
        population_sd([2.0, 2.0, 2.0])
    assert sample_sd([2.0, 2.0, 2.0]) == 0.0
    assert standardized_mean_difference([2.0, 2.0], [2.0, 2.0]) == 0.0
    assert math.isinf(standardized_mean_difference([2.0, 2.0], [3.0, 3.0]))
