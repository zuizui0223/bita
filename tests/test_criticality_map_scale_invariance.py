import math

from trait_architecture.criticality import (
    classify_architecture_margin,
    criticality_map,
)


def _reference_map():
    return criticality_map(
        optimum_distance=1.0,
        weight1=1.0,
        weight2=1.0,
        coupling=1.0,
        architecture_cost=0.1,
    )


def test_criticality_map_covaries_with_common_fitness_units() -> None:
    baseline = _reference_map()
    assert baseline.architecture_status == "DIFFERENTIATED_ARCHITECTURE_FAVOURED"

    for scale in (1e-300, 1e-16, 1.0, 1e16, 1e300):
        result = criticality_map(
            optimum_distance=1.0,
            weight1=scale,
            weight2=scale,
            coupling=scale,
            architecture_cost=0.1 * scale,
        )
        assert result.architecture_status == baseline.architecture_status
        assert math.isclose(result.decoupling_fraction, baseline.decoupling_fraction, rel_tol=2e-15)
        for key in (
            "shared_conflict_load",
            "recoverable_loss",
            "architecture_margin",
            "critical_cost",
            "critical_shared_load",
            "critical_coupling",
        ):
            observed = getattr(result, key)
            expected = getattr(baseline, key) * scale
            assert math.isclose(observed, expected, rel_tol=3e-13, abs_tol=0.0)
        assert math.isclose(
            result.critical_decoupling,
            baseline.critical_decoupling,
            rel_tol=2e-15,
            abs_tol=0.0,
        )
        assert math.isclose(
            result.critical_optimum_distance,
            baseline.critical_optimum_distance,
            rel_tol=3e-13,
            abs_tol=0.0,
        )


def test_criticality_map_is_invariant_to_trait_coordinate_units() -> None:
    baseline = _reference_map()

    for coordinate_scale in (1e-150, 1e-75, 1.0, 1e75, 1e150):
        weight_scale = 1.0 / (coordinate_scale * coordinate_scale)
        result = criticality_map(
            optimum_distance=coordinate_scale,
            weight1=weight_scale,
            weight2=weight_scale,
            coupling=weight_scale,
            architecture_cost=0.1,
        )
        assert result.architecture_status == baseline.architecture_status
        for key in (
            "shared_conflict_load",
            "decoupling_fraction",
            "recoverable_loss",
            "architecture_margin",
            "critical_cost",
            "critical_shared_load",
            "critical_decoupling",
        ):
            assert math.isclose(
                getattr(result, key),
                getattr(baseline, key),
                rel_tol=4e-13,
                abs_tol=0.0,
            )
        assert math.isclose(
            result.critical_coupling,
            baseline.critical_coupling * weight_scale,
            rel_tol=4e-13,
            abs_tol=0.0,
        )
        assert math.isclose(
            result.critical_optimum_distance,
            baseline.critical_optimum_distance * coordinate_scale,
            rel_tol=4e-13,
            abs_tol=0.0,
        )


def test_tiny_signed_default_map_margin_is_not_collapsed_to_critical() -> None:
    scale = 1e-13
    result = criticality_map(
        optimum_distance=1.0,
        weight1=scale,
        weight2=scale,
        coupling=scale,
        architecture_cost=0.1 * scale,
    )
    assert 0.0 < result.architecture_margin < 1e-12
    assert result.architecture_status == "DIFFERENTIATED_ARCHITECTURE_FAVOURED"


def test_exact_common_surface_remains_critical_across_fitness_units() -> None:
    for scale in (1e-300, 1e-16, 1.0, 1e16, 1e300):
        result = criticality_map(
            optimum_distance=1.0,
            weight1=scale,
            weight2=scale,
            coupling=2.0 * scale,
            architecture_cost=0.1 * scale,
        )
        assert result.architecture_status == "COMMON_ARCHITECTURE_CRITICAL_SURFACE"
        assert abs(result.architecture_margin) <= 64.0 * math.ulp(1.0) * max(
            result.recoverable_loss,
            result.architecture_cost,
        )


def test_public_explicit_absolute_neutral_band_is_preserved() -> None:
    assert classify_architecture_margin(5e-13) == "COMMON_ARCHITECTURE_CRITICAL_SURFACE"
    assert classify_architecture_margin(5e-13, tolerance=0.0) == "DIFFERENTIATED_ARCHITECTURE_FAVOURED"
