import pytest

from trait_architecture.shared_region_convexity import (
    audit_strong_convex_chord,
    strong_convex_sag_bounds,
)


def test_midpoint_sag_uses_one_eighth_rule():
    lower, upper = strong_convex_sag_bounds(
        curvature_lower=2.0,
        curvature_upper=6.0,
        t=0.5,
        metric_distance_sq=4.0,
    )
    assert lower == pytest.approx(1.0)
    assert upper == pytest.approx(3.0)


def test_quadratic_convex_margin_hits_exact_sag():
    # F(t)=2(t-0.5)^2-1 -> F''=4, endpoints=-0.5, midpoint=-1.
    out = audit_strong_convex_chord(
        margin0=-0.5,
        margin1=-0.5,
        observed_margin=-1.0,
        t=0.5,
        curvature_lower=4.0,
        curvature_upper=4.0,
    )
    assert out.observed_sag == pytest.approx(0.5)
    assert out.sag_lower == pytest.approx(0.5)
    assert out.sag_upper == pytest.approx(0.5)
    assert not out.violates_lower
    assert not out.violates_upper


def test_too_shallow_sag_rejects_strong_convexity_floor():
    out = audit_strong_convex_chord(
        margin0=-0.2,
        margin1=-0.2,
        observed_margin=-0.25,
        t=0.5,
        curvature_lower=1.0,
        curvature_upper=4.0,
    )
    assert out.sag_lower == pytest.approx(0.125)
    assert out.observed_sag == pytest.approx(0.05)
    assert out.violates_lower


def test_invalid_bounds_fail_closed():
    with pytest.raises(ValueError):
        strong_convex_sag_bounds(
            curvature_lower=3.0,
            curvature_upper=2.0,
            t=0.5,
        )
