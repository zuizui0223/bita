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
    aubert = {
        "missing_as_no": {
            "native_pair_site_summary": {
                "pair_site_n": 2265,
                "mean_robbery_rate_barrier": 0.14664,
                "mean_robbery_rate_accessible": 0.01995,
                "site_difference": {
                    "eligible_sites": 18,
                    "positive_sites": 18,
                    "sign_test_p": 7.62939453125e-06,
                },
            },
            "plant_species_rho_check": {
                "n_clusters": 259,
                "rho": 0.50316,
                "permutation_p_two_sided": 0.0001,
            },
            "plant_species_cluster_check": {
                "eligible_clusters": 130,
                "mean_cluster_difference": 0.09146,
                "cluster_label_swap_permutation_p": 0.0001,
            },
            "bird_species_cluster_check": {
                "eligible_clusters": 36,
                "mean_cluster_difference": 0.09334,
                "cluster_label_swap_permutation_p": 0.0001,
            },
            "bird_within_species_continuous_check": {
                "eligible_bird_species_continuous": 28,
                "bird_plant_dyads_in_pooled_test": 1285,
                "pooled_within_bird_rank_rho": 0.33976,
                "within_bird_permutation_p_two_sided": 0.0001,
            },
        },
    }
    participation = {
        "decision": {
            "rate_ratio": 1.7717,
            "ci95_rate_ratio": [1.1050, 2.8405],
        }
    }
    svg = build_svg(points, result, aubert, participation)

    assert svg.count("<circle") >= 3
    assert "n = 3 species" in svg
    assert "rho = 0.500" in svg
    assert "p = 0.0400" in svg
    assert "robber-only median = 8.000" in svg
    assert "thief-only median = 2.000" in svg
    assert "Aubert / EPHI" in svg
    assert "total exploitation RR = 1.77" in svg
    assert "95% CI 1.10–2.84" in svg
    assert "route composition: barrier robbery 0.147 vs accessible 0.020" in svg
    assert "18 / 18 sites positive" in svg
    assert "plant-level mismatch rho = 0.503" in svg
    assert "bird paired barrier: 36 species" in svg
    assert "within-bird continuous: 28 species / 1,285 dyads" in svg
    assert "centered-rank rho = 0.340" in svg
    assert ">A<" not in svg
    assert ">B<" not in svg
    assert ">C<" not in svg
