import math

from trait_architecture.functional_weight_criticality import (
    asymptotic_recoverable_loss,
    critical_function2_weight,
    monotonicity_log_derivative,
    recoverable_loss_at_function2_weight,
)


def test_recoverable_loss_increases_with_function2_weight() -> None:
    values = [
        recoverable_loss_at_function2_weight(b, 1.0, 1.0, 1.0)
        for b in (0.1, 0.25, 0.5, 1.0, 2.0, 10.0)
    ]
    assert all(right > left for left, right in zip(values, values[1:]))
    assert all(monotonicity_log_derivative(b, 1.0, 1.0) > 0 for b in (0.1, 1.0, 10.0))


def test_finite_weight_threshold_solves_architecture_boundary() -> None:
    result = critical_function2_weight(
        function1_weight=1.0,
        coupling=1.0,
        optimum_distance=1.0,
        architecture_cost=0.1,
    )
    assert result.status == "FINITE_FUNCTION2_WEIGHT_CRITICAL_POINT"
    assert result.critical_function2_weight is not None
    assert math.isfinite(result.critical_function2_weight)
    recovered = recoverable_loss_at_function2_weight(
        result.critical_function2_weight, 1.0, 1.0, 1.0
    )
    assert math.isclose(recovered, 0.1, rel_tol=1e-12, abs_tol=1e-12)


def test_reference_finite_weight_threshold_has_expected_value() -> None:
    # a=1, lambda=1, d=1, K=0.1 gives A=0.8 and
    # bcrit = [0.3 + sqrt(0.41)] / 1.6.
    expected = (0.3 + math.sqrt(0.41)) / 1.6
    result = critical_function2_weight(1.0, 1.0, 1.0, 0.1)
    assert math.isclose(result.critical_function2_weight, expected, rel_tol=1e-12)


def test_asymptotic_ceiling_can_make_differentiation_unreachable() -> None:
    ceiling = asymptotic_recoverable_loss(1.0, 1.0, 1.0)
    assert math.isclose(ceiling, 0.5)

    at_ceiling = critical_function2_weight(1.0, 1.0, 1.0, 0.5)
    assert at_ceiling.critical_function2_weight == math.inf
    assert at_ceiling.status == "ASYMPTOTIC_CRITICAL_WEIGHT_NO_FINITE_CROSSING"

    above = critical_function2_weight(1.0, 1.0, 1.0, 0.6)
    assert above.critical_function2_weight is None
    assert above.status == "COST_EXCEEDS_MAX_RECOVERABLE_LOSS_SHARED_ALWAYS_FAVOURED"


def test_zero_cost_collapses_weight_threshold_to_conflict_onset() -> None:
    result = critical_function2_weight(1.0, 3.0, 2.0, 0.0)
    assert result.critical_function2_weight == 0.0
    assert result.status == "ZERO_COST_COLLAPSES_ARCHITECTURE_THRESHOLD_TO_CONFLICT_ONSET"


def test_no_optimum_separation_has_no_tradeoff_driven_crossing() -> None:
    positive_cost = critical_function2_weight(1.0, 0.5, 0.0, 0.1)
    assert positive_cost.critical_function2_weight is None
    assert positive_cost.status == "NO_CONFLICT_SHARED_ARCHITECTURE_ALWAYS_FAVOURED"

    zero_cost = critical_function2_weight(1.0, 0.5, 0.0, 0.0)
    assert zero_cost.critical_function2_weight == 0.0
    assert zero_cost.status == "ALL_FUNCTION2_WEIGHTS_ON_ZERO_CONFLICT_BOUNDARY"
