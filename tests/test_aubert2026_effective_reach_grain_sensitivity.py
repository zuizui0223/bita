from __future__ import annotations

import math

from scripts.analyze_aubert2026_effective_reach_grain_sensitivity import (
    _reparameterize_edge,
    _reparameterize_rows,
    translate_threshold,
)
from scripts.analyze_aubert2026_participation_route_decomposition import Edge


def _edge(mismatch: float) -> Edge:
    return Edge(
        waypoint="w",
        bird="b",
        plant="p",
        site="s",
        barrier=1 if mismatch > 0 else 0,
        mismatch=mismatch,
        primary_count=1,
        strict_count=1,
        broad_count=1,
    )


def test_fixed_reach_multiplier_is_log_translation() -> None:
    edge = _edge(math.log(2.5))
    shifted = _reparameterize_edge(edge, 2.0)
    assert math.isclose(shifted.mismatch, math.log(1.25), rel_tol=0, abs_tol=1e-12)
    assert shifted.barrier == 1


def test_binary_barrier_can_change_under_reach_multiplier() -> None:
    edge = _edge(math.log(1.5))
    assert edge.barrier == 1
    shifted = _reparameterize_edge(edge, 2.0)
    assert shifted.barrier == 0


def test_pair_rows_exclude_flowerpiercers_from_reach_sensitivity() -> None:
    rows = [
        {
            "bird_group": "hummingbird",
            "mismatch_log_t_over_b": math.log(1.5),
            "trait_barrier": True,
        },
        {
            "bird_group": "flowerpiercer",
            "mismatch_log_t_over_b": math.log(1.5),
            "trait_barrier": True,
        },
    ]
    out = _reparameterize_rows(rows, 2.0)
    assert len(out) == 1
    assert out[0]["bird_group"] == "hummingbird"
    assert out[0]["trait_barrier"] is False


def test_threshold_boundary_is_invariant_to_fixed_multiplier() -> None:
    threshold = {
        "threshold_classification": "THRESHOLD_AT_SUPPORT_BOUNDARY",
        "primary_sigmoid": {
            "xstar": 0.9197423428245373,
            "x_search_low": -0.9938168690755013,
            "x_search_high": 0.9197423428245373,
        },
        "bootstrap": {
            "ci90_xstar": [0.1176853690900638, 0.9197423428245373],
        },
    }
    result = translate_threshold(threshold, 2.0)
    assert result["xstar_at_same_upper_support_boundary"] is True
    assert math.isclose(
        result["translated_xstar"],
        0.9197423428245373 - math.log(2.0),
        rel_tol=0,
        abs_tol=1e-12,
    )
    assert result["classification_invariant_under_translation"] == (
        "THRESHOLD_AT_SUPPORT_BOUNDARY"
    )
