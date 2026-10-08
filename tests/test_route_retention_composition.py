from dataclasses import replace
import math

from scripts.analyze_aubert2026_participation_route_decomposition import Edge
from scripts.analyze_route_retention_composition import (
    bird_site_fe, route_sorting_expectation,
)


def make(bird, site, wp, mismatch, count):
    return Edge(
        waypoint=wp, bird=bird, plant=wp, site=site,
        barrier=int(mismatch > 0), mismatch=mismatch,
        primary_count=count, strict_count=count, broad_count=count,
    )


def test_sorting_only_expected_conditions_on_bird_site_totals():
    edges = [
        make("A", "S", "W1", -1.0, 1),
        make("A", "S", "W2", 1.0, 3),
        make("B", "S", "W1", -1.0, 2),
        make("B", "S", "W2", 1.0, 2),
    ]
    summary = route_sorting_expectation(edges)
    info = summary["accessible_and_severe_support_strata"]
    assert info["strata"] == 2
    assert info["observed_counts"]["ACCESSIBLE"] == 3
    assert info["observed_counts"]["SEVERE_MISMATCH"] == 5
    assert info["expected_sorting_only_counts"]["ACCESSIBLE"] == 4
    assert info["expected_sorting_only_counts"]["SEVERE_MISMATCH"] == 4
    assert math.isclose(info["observed_to_expected"]["ACCESSIBLE"], 0.75)
    assert math.isclose(info["observed_to_expected"]["SEVERE_MISMATCH"], 1.25)


def test_site_groups_not_mixed_and_identifiers_preserved():
    edges = [
        make("A", "S1", "W1", -1.0, 2),
        make("A", "S2", "W2", 1.0, 4),
    ]
    assert route_sorting_expectation(edges)["accessible_and_severe_support_strata"]["strata"] == 0
    grouped = bird_site_fe(edges)
    assert [x.bird for x in grouped] == ["A@@S1", "A@@S2"]
    assert [x.waypoint for x in grouped] == ["W1", "W2"]
    assert [x.primary_count for x in grouped] == [2, 4]
