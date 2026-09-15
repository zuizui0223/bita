import math

from trait_architecture.functional_weight_criticality import (
    asymptotic_recoverable_loss,
    critical_function2_weight,
    monotonicity_log_derivative,
    recoverable_loss_at_function2_weight,
)


BASE_A = 1.0
BASE_LAMBDA = 1.0
BASE_D = 1.0
BASE_K = 0.1


def _baseline_critical() -> float:
    result = critical_function2_weight(BASE_A, BASE_LAMBDA, BASE_D, BASE_K)
    assert result.status == "FINITE_FUNCTION2_WEIGHT_CRITICAL_POINT"
    assert result.critical_function2_weight is not None
    return result.critical_function2_weight


def test_finite_critical_weight_covaries_with_common_fitness_units() -> None:
    baseline = _baseline_critical()
    baseline_derivative = monotonicity_log_derivative(1.0, 1.0, 1.0)

    for scale in (1e-300, 1e-16, 1.0, 1e16, 1e300):
        result = critical_function2_weight(
            function1_weight=BASE_A * scale,
            coupling=BASE_LAMBDA * scale,
            optimum_distance=BASE_D,
            architecture_cost=BASE_K * scale,
        )
        assert result.status == "FINITE_FUNCTION2_WEIGHT_CRITICAL_POINT"
        assert result.critical_function2_weight is not None
        assert math.isclose(
            result.critical_function2_weight,
            baseline * scale,
            rel_tol=5e-13,
            abs_tol=0.0,
        )
        assert math.isclose(
            result.asymptotic_recoverable_loss,
            0.5 * scale,
            rel_tol=5e-13,
            abs_tol=0.0,
        )
        recovered = recoverable_loss_at_function2_weight(
            result.critical_function2_weight,
            BASE_A * scale,
            BASE_LAMBDA * scale,
            BASE_D,
        )
        assert math.isclose(recovered, BASE_K * scale, rel_tol=2e-12, abs_tol=0.0)

        derivative = monotonicity_log_derivative(scale, scale, scale)
        assert math.isclose(
            derivative,
            baseline_derivative / scale,
            rel_tol=5e-13,
            abs_tol=0.0,
        )


def test_finite_critical_weight_covaries_with_trait_coordinate_units() -> None:
    baseline = _baseline_critical()

    for coordinate_scale in (1e-150, 1e-75, 1.0, 1e75, 1e150):
        weight_scale = 1.0 / (coordinate_scale * coordinate_scale)
        result = critical_function2_weight(
            function1_weight=BASE_A * weight_scale,
            coupling=BASE_LAMBDA * weight_scale,
            optimum_distance=BASE_D * coordinate_scale,
            architecture_cost=BASE_K,
        )
        assert result.status == "FINITE_FUNCTION2_WEIGHT_CRITICAL_POINT"
        assert result.critical_function2_weight is not None
        assert math.isclose(
            result.critical_function2_weight,
            baseline * weight_scale,
            rel_tol=2e-12,
            abs_tol=0.0,
        )
        assert math.isclose(
            result.asymptotic_recoverable_loss,
            0.5,
            rel_tol=5e-13,
            abs_tol=0.0,
        )
        recovered = recoverable_loss_at_function2_weight(
            result.critical_function2_weight,
            BASE_A * weight_scale,
            BASE_LAMBDA * weight_scale,
            BASE_D * coordinate_scale,
        )
        assert math.isclose(recovered, BASE_K, rel_tol=2e-12, abs_tol=0.0)


def test_tiny_positive_cost_is_not_relabelled_zero_cost() -> None:
    result = critical_function2_weight(
        function1_weight=1e-13,
        coupling=1e-13,
        optimum_distance=1.0,
        architecture_cost=1e-14,
    )
    assert result.status == "FINITE_FUNCTION2_WEIGHT_CRITICAL_POINT"
    assert result.critical_function2_weight is not None
    assert result.critical_function2_weight > 0.0
    assert math.isclose(
        result.critical_function2_weight,
        _baseline_critical() * 1e-13,
        rel_tol=2e-12,
        abs_tol=0.0,
    )


def test_ceiling_status_is_invariant_across_fitness_units() -> None:
    for scale in (1e-300, 1e-16, 1.0, 1e16, 1e300):
        at = critical_function2_weight(scale, scale, 1.0, 0.5 * scale)
        assert at.status == "ASYMPTOTIC_CRITICAL_WEIGHT_NO_FINITE_CROSSING"
        assert at.critical_function2_weight == math.inf

        above = critical_function2_weight(scale, scale, 1.0, 0.6 * scale)
        assert above.status == "COST_EXCEEDS_MAX_RECOVERABLE_LOSS_SHARED_ALWAYS_FAVOURED"
        assert above.critical_function2_weight is None


def test_no_conflict_uses_exact_zero_cost_semantics() -> None:
    positive = critical_function2_weight(1e-300, 1e-300, 0.0, 1e-300)
    assert positive.status == "NO_CONFLICT_SHARED_ARCHITECTURE_ALWAYS_FAVOURED"
    assert positive.critical_function2_weight is None

    zero = critical_function2_weight(1e-300, 1e-300, 0.0, 0.0)
    assert zero.status == "ALL_FUNCTION2_WEIGHTS_ON_ZERO_CONFLICT_BOUNDARY"
    assert zero.critical_function2_weight == 0.0


def test_recoverable_loss_handles_extreme_function2_weight_ratio() -> None:
    observed = recoverable_loss_at_function2_weight(
        function2_weight=1e150,
        function1_weight=1.0,
        coupling=1.0,
        optimum_distance=1.0,
    )
    assert math.isfinite(observed)
    assert 0.0 < observed <= asymptotic_recoverable_loss(1.0, 1.0, 1.0)
    assert math.isclose(observed, 0.5, rel_tol=1e-14, abs_tol=0.0)

    derivative = monotonicity_log_derivative(1e150, 1.0, 1.0)
    assert math.isfinite(derivative)
    assert derivative > 0.0
