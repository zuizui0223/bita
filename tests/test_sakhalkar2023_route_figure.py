from __future__ import annotations

from scripts.analyze_sakhalkar2023_network import species_route_points
from scripts.build_sakhalkar2023_route_figure_svg import build_svg


def _data():
    visits = [
        {"spcode": "A", "behavior": "robbing", "freq_fm_per_species": "3"},
        {"spcode": "B", "behavior": "thieving", "freq_fm_per_species": "2"},
        {"spcode": "C", "behavior": "robbing", "freq_fm_per_species": "1"},
        {"spcode": "C", "behavior": "thieving", "freq_fm_per_species": "1"},
        {"spcode": "D", "behavior": "touching", "freq_fm_per_species": "4"},
    ]
    traits = [
        {"spcode": "A", "tube_length": "8"},
        {"spcode": "B", "tube_length": "2"},
        {"spcode": "C", "tube_length": "5"},
        {"spcode": "D", "tube_length": "4"},
    ]
    return visits, traits


def test_species_route_points_are_anonymous_and_cheater_only() -> None:
    visits, traits = _data()
    points = species_route_points(visits, traits)

    assert len(points) == 3
    assert all(set(point) == {"tube_length", "balance", "route_class"} for point in points)
    assert {point["route_class"] for point in points} == {"robber_only", "thief_only", "mixed"}
    assert not any("spcode" in point for point in points)


def test_figure4_svg_contains_points_and_frozen_stats_without_species_ids() -> None:
    visits, traits = _data()
    points = species_route_points(visits, traits)
    result = {
        "tube_length_cheating_mode_balance": {
            "n_species": 3,
            "spearman_rho": 0.5,
            "permutation_p_two_sided": 0.04,
        },
        "median_tube_length_robber_only": 8.0,
        "median_tube_length_thief_only": 2.0,
    }
    svg = build_svg(points, result)

    assert svg.count("<circle") >= 3
    assert "n = 3 species" in svg
    assert "rho = 0.500" in svg
    assert "p = 0.0400" in svg
    assert "robber-only median = 8.000" in svg
    assert "thief-only median = 2.000" in svg
    assert ">A<" not in svg
    assert ">B<" not in svg
    assert ">C<" not in svg
