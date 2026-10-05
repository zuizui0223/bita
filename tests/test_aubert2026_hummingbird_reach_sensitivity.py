from __future__ import annotations

import math
from dataclasses import replace

from scripts.analyze_aubert2026_hummingbird_reach_sensitivity import (
    _shift_edges,
    _shift_pair_rows,
    _translated_threshold,
)
from scripts.analyze_aubert2026_participation_route_decomposition import Edge


def test_fixed_reach_multiplier_translates_pair_mismatch_only() -> None:
    rows = [
        {
            "mismatch_log_t_over_b": math.log(2.0),
            "trait_barrier": True,
            "robbery_rate": 0.5,
        }
    ]
    shifted = _shift_pair_rows(rows, 2.0)
    assert math.isclose(float(shifted[0]["mismatch_log_t_over_b"]), 0.0, abs_tol=1e-12)
    assert shifted[0]["trait_barrier"] is False
    assert shifted[0]["robbery_rate"] == 0.5


def test_fixed_reach_multiplier_translates_edge_and_barrier() -> None:
    edge = Edge(
        waypoint="w",
        bird="b",
        plant="p",
        site="s",
        barrier=1,
        mismatch=math.log(1.5),
        primary_count=2,
        strict_count=2,
        broad_count=2,
    )
    shifted = _shift_edges([edge], 1.8)[0]
    assert math.isclose(shifted.mismatch, math.log(1.5 / 1.8), abs_tol=1e-12)
    assert shifted.barrier == 0
    assert shifted.primary_count == edge.primary_count


def test_threshold_translation_preserves_search_boundary() -> None:
    raw = _translated_threshold(1.0)
    for multiplier in (4.0 / 3.0, 1.8, 2.0):
        shifted = _translated_threshold(multiplier)
        delta = math.log(multiplier)
        assert math.isclose(
            float(shifted["translated_xstar"]),
            float(raw["translated_xstar"]) - delta,
            abs_tol=1e-12,
        )
        assert math.isclose(
            float(shifted["translated_search_high"]),
            float(raw["translated_search_high"]) - delta,
            abs_tol=1e-12,
        )
        assert (
            shifted["boundary_classification_preserved"]
            == "THRESHOLD_AT_SUPPORT_BOUNDARY"
        )


def test_two_x_reach_moves_point_midpoint_close_to_equality_but_not_inside_margin() -> None:
    shifted = _translated_threshold(2.0)
    assert 1.24 < float(shifted["effective_reach_ratio_at_midpoint"]) < 1.27
    assert shifted["point_midpoint_within_plusminus_log_1_25"] is False
