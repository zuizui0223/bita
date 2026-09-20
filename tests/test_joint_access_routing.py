from __future__ import annotations

import math

from scripts.analyze_joint_access_routing import (
    combine_rhos_equal_network,
    summarize_joint,
)


def test_equal_network_combination_uses_fisher_z_mean() -> None:
    observed = combine_rhos_equal_network([0.2, 0.8])
    expected = math.tanh((math.atanh(0.2) + math.atanh(0.8)) / 2)
    assert observed == expected


def test_joint_summary_keeps_networks_equally_weighted() -> None:
    sakh = [
        {"tube_length": 1.0, "balance": -1.0, "route_class": "thief_only"},
        {"tube_length": 2.0, "balance": -0.2, "route_class": "mixed"},
        {"tube_length": 3.0, "balance": 0.4, "route_class": "mixed"},
        {"tube_length": 4.0, "balance": 1.0, "route_class": "robber_only"},
    ]
    aubert = [
        {"site": "S1", "robbery_rate": 0.0, "mismatch_log_t_over_b": -0.3, "trait_barrier": False},
        {"site": "S1", "robbery_rate": 0.8, "mismatch_log_t_over_b": 0.3, "trait_barrier": True},
        {"site": "S2", "robbery_rate": 0.1, "mismatch_log_t_over_b": -0.2, "trait_barrier": False},
        {"site": "S2", "robbery_rate": 0.7, "mismatch_log_t_over_b": 0.2, "trait_barrier": True},
    ]

    result = summarize_joint(sakh, aubert, permutations=99, seed=7)

    assert result["network_count"] == 2
    assert result["network_effects"]["sakhalkar"]["rho"] > 0
    assert result["network_effects"]["aubert_ephi"]["rho"] > 0
    assert result["joint_equal_network_fisher_z_rho"] > 0
    assert result["joint_equal_network_mean_rho"] > 0
    assert 0 < result["joint_permutation_p_two_sided"] <= 1
    assert result["aubert_permutation_scheme"] == "within_site"
    assert result["sakhalkar_permutation_scheme"] == "across_species"


def test_joint_output_is_aggregate_only() -> None:
    sakh = [
        {"tube_length": 1.0, "balance": -1.0, "route_class": "thief_only"},
        {"tube_length": 2.0, "balance": 1.0, "route_class": "robber_only"},
        {"tube_length": 3.0, "balance": 0.0, "route_class": "mixed"},
    ]
    aubert = [
        {"site": "SecretSiteA", "robbery_rate": 0.0, "mismatch_log_t_over_b": -0.2, "trait_barrier": False},
        {"site": "SecretSiteA", "robbery_rate": 1.0, "mismatch_log_t_over_b": 0.2, "trait_barrier": True},
        {"site": "SecretSiteB", "robbery_rate": 0.1, "mismatch_log_t_over_b": -0.1, "trait_barrier": False},
        {"site": "SecretSiteB", "robbery_rate": 0.9, "mismatch_log_t_over_b": 0.1, "trait_barrier": True},
    ]

    result = summarize_joint(sakh, aubert, permutations=19, seed=3)
    text = str(result)
    assert "SecretSiteA" not in text
    assert "SecretSiteB" not in text
    assert "raw_rows" not in result
