import math

import pytest

from trait_architecture.shared_region_convexity import (
    certify_interval_shared_chord,
    classify_interval_convex_chord,
    interval_convex_sag_bounds,
)


def test_interval_sag_bounds_are_sharp_under_marginal_intervals():
    lo, hi = interval_convex_sag_bounds(
        margin0_lower=-0.5,
        margin0_upper=-0.4,
        margin1_lower=-0.3,
        margin1_upper=-0.2,
        interior_lower=-0.6,
        interior_upper=-0.5,
        t=0.5,
    )
    assert lo == pytest.approx(0.1)
    assert hi == pytest.approx(0.3)


def test_interval_sag_identified_when_possible_set_inside_model_band():
    out = classify_interval_convex_chord(
        margin0_lower=-0.4,
        margin0_upper=-0.4,
        margin1_lower=-0.4,
        margin1_upper=-0.4,
        interior_lower=-0.54,
        interior_upper=-0.52,
        t=0.5,
        curvature_lower=0.8,
        curvature_upper=1.2,
    )
    assert out.required_sag_lower == pytest.approx(0.1)
    assert out.required_sag_upper == pytest.approx(0.15)
    assert out.classification == "IDENTIFIED_WITHIN_INTERVALS"


def test_interval_sag_robustly_rejects_convexity_when_upper_sag_negative():
    out = classify_interval_convex_chord(
        margin0_lower=-0.5,
        margin0_upper=-0.5,
        margin1_lower=-0.5,
        margin1_upper=-0.5,
        interior_lower=-0.45,
        interior_upper=-0.35,
        t=0.5,
    )
    assert out.possible_sag_upper < 0.0
    assert out.classification == "LOWER_BOUND_VIOLATED"
    assert math.isinf(out.required_sag_upper)


def test_partial_overlap_is_unresolved():
    out = classify_interval_convex_chord(
        margin0_lower=-0.5,
        margin0_upper=-0.4,
        margin1_lower=-0.5,
        margin1_upper=-0.4,
        interior_lower=-0.7,
        interior_upper=-0.45,
        t=0.5,
        curvature_lower=0.4,
        curvature_upper=1.6,
    )
    assert out.classification == "UNRESOLVED"


def test_endpoint_upper_bounds_robustly_exclude_hidden_bita_under_convexity():
    out = certify_interval_shared_chord(margin0_upper=-0.05, margin1_upper=0.0)
    assert out.shared_endpoints
    assert out.hidden_bita_excluded
    assert out.segment_margin_upper == pytest.approx(0.0)


def test_positive_endpoint_upper_bound_fails_closed():
    out = certify_interval_shared_chord(margin0_upper=-0.05, margin1_upper=0.01)
    assert not out.hidden_bita_excluded


def test_endpoint_t_with_unbounded_curvature_is_not_nan():
    out = classify_interval_convex_chord(
        margin0_lower=-0.4,
        margin0_upper=-0.4,
        margin1_lower=-0.4,
        margin1_upper=-0.4,
        interior_lower=-0.4,
        interior_upper=-0.4,
        t=0.0,
    )
    assert out.required_sag_upper == pytest.approx(0.0)


def test_invalid_interval_fails_closed():
    with pytest.raises(ValueError):
        interval_convex_sag_bounds(
            margin0_lower=1.0,
            margin0_upper=0.0,
            margin1_lower=0.0,
            margin1_upper=1.0,
            interior_lower=0.0,
            interior_upper=1.0,
            t=0.5,
        )
