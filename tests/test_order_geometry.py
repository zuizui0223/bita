import pytest

from trait_architecture.order_geometry import (
    componentwise_leq,
    has_positive_to_negative_reentry,
    minimal_positive_indices,
    monotone_path_audit,
)


def test_monotone_path_margin_cannot_decrease_in_valid_example():
    points = [(0.0, 0.0), (0.2, 0.0), (0.2, 0.4), (0.7, 0.4)]
    margins = [-0.6, -0.4, 0.1, 0.8]
    assert monotone_path_audit(points, margins)
    assert not has_positive_to_negative_reentry(margins)


def test_positive_to_negative_reentry_is_detected():
    margins = [-0.2, 0.1, 0.4, -0.1]
    assert has_positive_to_negative_reentry(margins)


def test_monotone_path_audit_rejects_margin_reversal():
    points = [(0.0, 0.0), (0.5, 0.0), (0.5, 0.5)]
    margins = [-0.3, 0.4, 0.1]
    assert not monotone_path_audit(points, margins)


def test_nonmonotone_treatment_path_fails_closed():
    with pytest.raises(ValueError):
        monotone_path_audit(
            [(0.0, 0.0), (0.5, 0.2), (0.4, 0.3)],
            [-0.2, 0.1, 0.2],
        )


def test_minimal_positive_interventions_form_frontier_candidates():
    points = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
        (0.5, 0.5),
    ]
    margins = [-1.0, 0.2, 0.3, 1.0, 0.1]
    minimal = minimal_positive_indices(points, margins)
    assert set(minimal) == {1, 2, 4}


def test_componentwise_order_requires_equal_dimension():
    assert componentwise_leq((0.0, 1.0), (0.2, 1.0))
    with pytest.raises(ValueError):
        componentwise_leq((0.0,), (0.0, 1.0))
