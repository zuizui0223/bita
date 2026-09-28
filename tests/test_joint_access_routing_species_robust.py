from __future__ import annotations

from scripts.analyze_joint_access_routing_species_robust import (
    aggregate_aubert_by_plant,
    summarize_joint_species,
)


def test_aubert_aggregation_creates_one_point_per_plant_species() -> None:
    rows = [
        {"plant_species": "P1", "mismatch_log_t_over_b": -0.4, "robbery_rate": 0.0},
        {"plant_species": "P1", "mismatch_log_t_over_b": -0.2, "robbery_rate": 0.2},
        {"plant_species": "P2", "mismatch_log_t_over_b": 0.4, "robbery_rate": 0.8},
    ]
    out = aggregate_aubert_by_plant(rows)
    assert len(out) == 2
    assert sorted(point["pair_site_n"] for point in out) == [1.0, 2.0]


def test_species_level_joint_detects_shared_positive_direction() -> None:
    sakh = [
        {"tube_length": 1.0, "balance": -0.8},
        {"tube_length": 2.0, "balance": -0.1},
        {"tube_length": 3.0, "balance": 0.5},
        {"tube_length": 4.0, "balance": 0.9},
    ]
    aubert = [
        {"mismatch": -0.5, "robbery_rate": 0.0},
        {"mismatch": -0.1, "robbery_rate": 0.2},
        {"mismatch": 0.3, "robbery_rate": 0.7},
        {"mismatch": 0.7, "robbery_rate": 0.9},
    ]
    out = summarize_joint_species(sakh, aubert, permutations=199, seed=5)
    assert out["network_effects"]["sakhalkar"]["rho"] > 0
    assert out["network_effects"]["aubert_ephi"]["rho"] > 0
    assert out["joint_equal_network_fisher_z_rho"] > 0
    assert 0 < out["joint_permutation_p_two_sided"] <= 1
    assert out["network_effects"]["aubert_ephi"]["unit"] == "plant_species"
