import pytest

from trait_architecture.curvature_dividend import (
    decompose_decoupling_gain,
    finite_effective_curvature,
    static_crossing_surplus,
)


def test_quadratic_decoupling_dividend_matches_exact_curvature_term():
    # R(lambda)=(3-lambda)^2. At lambda0=1, c0=-R'(1)=4.
    # Decouple by x=0.5: exact gain=R(0.5)-R(1)=2.25,
    # tangent gain=4*0.5=2, dividend=0.25.
    result = decompose_decoupling_gain(total_gain=2.25, tangent_gain=2.0)
    assert result.curvature_dividend == pytest.approx(0.25)
    assert result.curvature_share == pytest.approx(1.0 / 9.0)


def test_finite_effective_curvature_recovers_constant_quadratic_curvature():
    # Same example has Hessian R''=2. With Q=1 and x=0.5,
    # metric squared length is 0.25 and 2*dividend/0.25=2.
    kappa = finite_effective_curvature(
        total_gain=2.25,
        tangent_gain=2.0,
        metric_squared_length=0.25,
    )
    assert kappa == pytest.approx(2.0)


def test_affine_recovery_has_zero_curvature_dividend():
    result = decompose_decoupling_gain(total_gain=1.2, tangent_gain=1.2)
    assert result.curvature_dividend == pytest.approx(0.0)
    assert result.curvature_share == pytest.approx(0.0)
    assert finite_effective_curvature(
        total_gain=1.2,
        tangent_gain=1.2,
        metric_squared_length=0.5,
    ) == pytest.approx(0.0)


def test_zero_starting_pressure_can_make_gain_all_curvature():
    result = decompose_decoupling_gain(total_gain=0.5, tangent_gain=0.0)
    assert result.curvature_dividend == pytest.approx(0.5)
    assert result.curvature_share == pytest.approx(1.0)


def test_negative_dividend_fails_closed_under_convex_model():
    with pytest.raises(ValueError):
        decompose_decoupling_gain(total_gain=0.9, tangent_gain=1.0)


def test_effective_curvature_requires_positive_metric_length():
    with pytest.raises(ValueError):
        finite_effective_curvature(
            total_gain=1.0,
            tangent_gain=0.5,
            metric_squared_length=0.0,
        )


def test_static_crossing_surplus_uses_total_finite_gain():
    assert static_crossing_surplus(deficit=1.0, total_gain=1.3) == pytest.approx(0.3)
    assert static_crossing_surplus(deficit=1.0, total_gain=0.8) == pytest.approx(-0.2)
