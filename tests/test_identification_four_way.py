from __future__ import annotations

import pytest

from trait_architecture.identification import IdentificationAssumptions, identify_crossed_design


def _cells(cross_consumer: float):
    cells = {}
    for a in (0, 1):
        for d in (0, 1):
            for g in (0, 1):
                for p in (0, 1):
                    cells[(a, d, g, p)] = (
                        1.0
                        + 0.2 * a
                        + 0.1 * d
                        - 0.4 * a * d
                        + 0.3 * p
                        - 0.2 * g
                        + cross_consumer * a * d * g * p
                    )
    return cells


def _assumptions():
    return IdentificationAssumptions(
        antagonist_intervention_selective=True,
        pollinator_intervention_selective=True,
        trait_levels_comparable_across_cells=True,
    )


def test_rho_and_iota_invariance_views_are_one_four_way_contrast() -> None:
    result = identify_crossed_design(_cells(0.25), _assumptions(), baseline_mutualist_delta=0.0)

    assert result.four_way_coupling == pytest.approx(0.25)
    assert result.rho_invariance_gap == pytest.approx(result.four_way_coupling)
    assert result.iota_increment_invariance_gap == pytest.approx(-result.four_way_coupling)
    assert not result.separability_pass


def test_zero_four_way_contrast_passes_deterministic_separability_gate() -> None:
    result = identify_crossed_design(_cells(0.0), _assumptions(), baseline_mutualist_delta=0.0)
    assert result.four_way_coupling == pytest.approx(0.0)
    assert result.separability_pass
