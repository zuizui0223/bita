import pytest

from trait_architecture.shared_region_convexity import (
    audit_joint_convexity_chord,
    certify_shared_chord,
    convex_chord_margin_upper,
)


def test_shared_endpoints_exclude_hidden_bita_island_under_convexity():
    out = certify_shared_chord(margin0=-0.4, margin1=-0.1)
    assert out.shared_endpoints
    assert out.hidden_bita_excluded
    assert out.segment_margin_upper == pytest.approx(-0.1)


def test_bita_endpoint_does_not_receive_shared_chord_certificate():
    out = certify_shared_chord(margin0=-0.4, margin1=0.2)
    assert not out.hidden_bita_excluded


def test_convex_chord_upper_bound_and_shape_audit():
    upper = convex_chord_margin_upper(margin0=-0.4, margin1=-0.1, t=0.5)
    assert upper == pytest.approx(-0.25)

    ok = audit_joint_convexity_chord(
        margin0=-0.4,
        margin1=-0.1,
        observed_margin=-0.3,
        t=0.5,
    )
    assert not ok.convexity_violated

    bad = audit_joint_convexity_chord(
        margin0=-0.4,
        margin1=-0.1,
        observed_margin=-0.2,
        t=0.5,
    )
    assert bad.convexity_violated
    assert bad.residual == pytest.approx(0.05)


def test_boundary_endpoints_still_exclude_positive_interior():
    out = certify_shared_chord(margin0=0.0, margin1=-0.2)
    assert out.hidden_bita_excluded


def test_invalid_t_fails_closed():
    with pytest.raises(ValueError):
        convex_chord_margin_upper(margin0=0.0, margin1=0.0, t=-0.1)
