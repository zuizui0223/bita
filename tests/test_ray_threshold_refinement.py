import math

import pytest

from trait_architecture.ray_threshold_refinement import refine_convex_ray_threshold


def test_refinement_contains_exact_quadratic_threshold_and_tightens_raw_bracket():
    # m(t) = t^2 + t - 1.  Positive-root threshold is (-1+sqrt(5))/2.
    t0, t1, t2 = 0.0, 0.5, 1.0
    f = lambda t: t * t + t - 1.0
    out = refine_convex_ray_threshold(
        t0=t0,
        t1=t1,
        t2=t2,
        m0=f(t0),
        m1=f(t1),
        m2=f(t2),
    )
    exact = (-1.0 + math.sqrt(5.0)) / 2.0
    assert out.refined_lower <= exact <= out.refined_upper
    assert out.refined_lower > t1
    assert out.refined_upper < t2
    assert out.previous_slope <= out.crossing_slope


def test_zero_previous_slope_keeps_positive_sample_as_upper_bound():
    out = refine_convex_ray_threshold(
        t0=0.0,
        t1=1.0,
        t2=2.0,
        m0=-1.0,
        m1=-1.0,
        m2=1.0,
    )
    assert out.previous_slope == pytest.approx(0.0)
    assert out.refined_upper == pytest.approx(2.0)
    assert out.refined_lower == pytest.approx(1.5)


def test_linear_margin_collapses_to_exact_threshold():
    # m(t)=2t-1; all secants equal 2 and the root is exactly 0.5.
    out = refine_convex_ray_threshold(
        t0=0.0,
        t1=0.25,
        t2=0.75,
        m0=-1.0,
        m1=-0.5,
        m2=0.5,
    )
    assert out.refined_lower == pytest.approx(0.5)
    assert out.refined_upper == pytest.approx(0.5)


def test_concave_secant_pattern_fails_closed():
    with pytest.raises(ValueError, match="violate convexity"):
        refine_convex_ray_threshold(
            t0=0.0,
            t1=1.0,
            t2=2.0,
            m0=-3.0,
            m1=-1.0,
            m2=0.5,
        )


def test_invalid_sign_pattern_fails_closed():
    with pytest.raises(ValueError):
        refine_convex_ray_threshold(
            t0=0.0,
            t1=1.0,
            t2=2.0,
            m0=-2.0,
            m1=0.0,
            m2=1.0,
        )
