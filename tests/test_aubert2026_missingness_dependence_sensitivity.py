from __future__ import annotations

from scripts.analyze_aubert2026_missingness_dependence_sensitivity import (
    _piercing_value,
    build_pair_site_rows_policy,
    cluster_aggregated_rho_summary,
    bird_within_species_continuous_summary,
    cluster_label_swap_summary,
)


def _fixtures():
    cameras = [
        {"waypoint": "w1", "site": "S1", "plant_species": "P1"},
        {"waypoint": "w2", "site": "S1", "plant_species": "P2"},
    ]
    plants = [
        {"plant_species": "P1", "site": "S1", "Tubelength": "4.0", "Country": "Ecuador"},
        {"plant_species": "P2", "site": "S1", "Tubelength": "1.0", "Country": "Ecuador"},
    ]
    birds = [
        {"hummingbird_species": "B1", "culmen_length": "20"},
        {"hummingbird_species": "B2", "culmen_length": "25"},
    ]
    return cameras, plants, birds


def test_missing_policy_only_reclassifies_missing_codes() -> None:
    assert _piercing_value("yes", missing_as_no=True) is True
    assert _piercing_value("no", missing_as_no=True) is False
    assert _piercing_value("NA", missing_as_no=False) is None
    assert _piercing_value("NA", missing_as_no=True) is False
    assert _piercing_value("", missing_as_no=True) is False
    assert _piercing_value("maybe", missing_as_no=True) is None
    assert _piercing_value("thief", missing_as_no=True) is None
    assert _piercing_value("not_interacting", missing_as_no=True) is None


def test_na_as_no_changes_denominator_without_turning_other_states_into_no() -> None:
    cameras, plants, birds = _fixtures()
    interactions = [
        {"waypoint": "w1", "hummingbird_species": "B1", "hummingbird_genus": "X", "hummingbird_family": "Trochilidae", "piercing": "yes"},
        {"waypoint": "w1", "hummingbird_species": "B1", "hummingbird_genus": "X", "hummingbird_family": "Trochilidae", "piercing": "NA"},
        {"waypoint": "w1", "hummingbird_species": "B1", "hummingbird_genus": "X", "hummingbird_family": "Trochilidae", "piercing": "maybe"},
        {"waypoint": "w2", "hummingbird_species": "B2", "hummingbird_genus": "X", "hummingbird_family": "Trochilidae", "piercing": "no"},
    ]

    cc_rows, cc_audit = build_pair_site_rows_policy(
        interactions, cameras, plants, birds, missing_as_no=False
    )
    na_rows, na_audit = build_pair_site_rows_policy(
        interactions, cameras, plants, birds, missing_as_no=True
    )

    cc_p1 = next(row for row in cc_rows if row["plant_species"] == "P1")
    na_p1 = next(row for row in na_rows if row["plant_species"] == "P1")
    assert cc_p1["n_interactions"] == 1
    assert cc_p1["robbery_rate"] == 1.0
    assert na_p1["n_interactions"] == 2
    assert na_p1["robbery_rate"] == 0.5
    assert cc_audit["included_by_piercing_policy"] == 2
    assert na_audit["included_by_piercing_policy"] == 3
    assert na_audit["raw_piercing_status_counts"]["maybe"] == 1


def test_cluster_label_swap_uses_one_difference_per_species() -> None:
    rows = [
        {"plant_species": "P1", "bird_species": "B1", "trait_barrier": True, "robbery_rate": 0.9},
        {"plant_species": "P1", "bird_species": "B2", "trait_barrier": False, "robbery_rate": 0.1},
        {"plant_species": "P2", "bird_species": "B1", "trait_barrier": True, "robbery_rate": 0.8},
        {"plant_species": "P2", "bird_species": "B2", "trait_barrier": False, "robbery_rate": 0.2},
        # P3 is ineligible because it has only one barrier class.
        {"plant_species": "P3", "bird_species": "B1", "trait_barrier": True, "robbery_rate": 0.7},
    ]
    out = cluster_label_swap_summary(
        rows,
        cluster_key="plant_species",
        permutations=199,
        seed=7,
    )
    assert out["eligible_clusters"] == 2
    assert out["positive_clusters"] == 2
    assert out["mean_cluster_difference"] > 0
    assert 0 < out["cluster_label_swap_permutation_p"] <= 1


def test_cluster_aggregated_rho_uses_one_point_per_species() -> None:
    rows = [
        {"plant_species": "P1", "mismatch_log_t_over_b": -0.4, "robbery_rate": 0.0},
        {"plant_species": "P1", "mismatch_log_t_over_b": -0.2, "robbery_rate": 0.1},
        {"plant_species": "P2", "mismatch_log_t_over_b": 0.0, "robbery_rate": 0.4},
        {"plant_species": "P2", "mismatch_log_t_over_b": 0.1, "robbery_rate": 0.5},
        {"plant_species": "P3", "mismatch_log_t_over_b": 0.5, "robbery_rate": 0.9},
        {"plant_species": "P3", "mismatch_log_t_over_b": 0.7, "robbery_rate": 1.0},
    ]
    out = cluster_aggregated_rho_summary(
        rows,
        cluster_key="plant_species",
        permutations=199,
        seed=11,
    )
    assert out["n_clusters"] == 3
    assert out["rho"] > 0
    assert 0 < out["permutation_p_two_sided"] <= 1


def test_within_bird_continuous_summary_uses_bird_x_plant_dyads() -> None:
    rows = []
    for bird in ("B1", "B2", "B3", "B4"):
        for plant_i in range(5):
            mismatch = -1.0 + plant_i * 0.5
            robbery = plant_i / 4
            for site in ("S1", "S2"):
                rows.append(
                    {
                        "site": site,
                        "bird_species": bird,
                        "plant_species": f"P{plant_i}",
                        "mismatch_log_t_over_b": mismatch,
                        "robbery_rate": robbery,
                        "trait_barrier": mismatch > 0,
                    }
                )
    out = bird_within_species_continuous_summary(
        rows,
        permutations=199,
        seed=12,
    )
    assert out["bird_species_total"] == 4
    assert out["eligible_bird_species_continuous"] == 4
    assert out["bird_plant_dyads_in_pooled_test"] == 20
    assert out["pooled_within_bird_rank_rho"] > 0.9
    assert out["within_bird_permutation_p_two_sided"] <= 0.05
    assert out["bird_specific_positive_rho_count"] == 4


def test_native_pair_site_summary_is_explicitly_descriptive() -> None:
    rows = [
        {
            "site": "S1",
            "bird_species": "B1",
            "plant_species": f"P{i}",
            "bird_group": "hummingbird",
            "n_interactions": 2,
            "robbery_rate": robbery,
            "mismatch_log_t_over_b": mismatch,
            "trait_barrier": mismatch > 0,
        }
        for i, (mismatch, robbery) in enumerate(
            [
                (-0.6, 0.00),
                (-0.3, 0.05),
                (-0.1, 0.10),
                (0.1, 0.30),
                (0.3, 0.50),
                (0.6, 0.70),
            ],
            start=1,
        )
    ]
    from scripts.analyze_aubert2026_missingness_dependence_sensitivity import summarize_policy

    out = summarize_policy(
        rows,
        audit={"missing_as_no": True},
        permutations=19,
        seed=7,
    )
    claim = out["native_pair_site_summary"]["claim_boundary"]
    assert "Descriptive pair-site summary" in claim
    assert "not the primary inferential units" in claim
