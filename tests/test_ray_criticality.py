import pytest

from trait_architecture.ray_criticality import analyze_decoupling_ray


def test_convex_monotone_ray_returns_unique_crossing_bracket():
    out = analyze_decoupling_ray(
        [0.0, 0.5, 1.0, 1.5],
        [-1.0, -0.4, 0.4, 1.8],
    )
    assert out.classification == "UNIQUE_CROSSING_BRACKET"
    assert out.crossing_lower == pytest.approx(0.5)
    assert out.crossing_upper == pytest.approx(1.0)
    assert out.monotone_ok
    assert out.convex_ok


def test_exact_sampled_zero_identifies_contact_point():
    out = analyze_decoupling_ray(
        [0.0, 1.0, 2.0, 3.0],
        [-1.0, 0.0, 1.0, 3.0],
    )
    assert out.classification == "EXACT_ZERO_OBSERVED"
    assert out.crossing_lower == pytest.approx(1.0)
    assert out.crossing_upper == pytest.approx(1.0)
    assert out.monotone_ok
    assert out.convex_ok


def test_zero_plateau_can_occur_at_ray_start_before_positive_side():
    out = analyze_decoupling_ray(
        [0.0, 1.0, 2.0, 3.0],
        [0.0, 0.0, 1.0, 3.0],
    )
    assert out.classification == "ZERO_PLATEAU_WITHOUT_BOTH_SIDES"
    assert out.crossing_lower == pytest.approx(0.0)
    assert out.crossing_upper == pytest.approx(1.0)
    assert out.convex_ok


def test_interior_negative_zero_plateau_positive_pattern_fails_convexity():
    out = analyze_decoupling_ray(
        [0.0, 1.0, 2.0, 3.0],
        [-1.0, 0.0, 0.0, 1.0],
    )
    assert out.monotone_ok
    assert not out.convex_ok
    assert out.classification == "RAY_MODEL_VIOLATION"


def test_slope_reversal_fails_closed():
    out = analyze_decoupling_ray(
        [0.0, 1.0, 2.0, 3.0],
        [-2.0, -0.5, 0.5, 1.0],
    )
    assert out.monotone_ok
    assert not out.convex_ok
    assert out.classification == "RAY_MODEL_VIOLATION"


def test_margin_reentry_fails_monotonicity():
    out = analyze_decoupling_ray(
        [0.0, 1.0, 2.0, 3.0],
        [-1.0, 0.2, -0.1, 0.8],
    )
    assert not out.monotone_ok
    assert out.classification == "RAY_MODEL_VIOLATION"


def test_invalid_levels_fail_closed():
    with pytest.raises(ValueError):
        analyze_decoupling_ray([0.0, 0.0], [-1.0, 1.0])
