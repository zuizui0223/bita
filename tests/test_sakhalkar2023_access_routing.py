from __future__ import annotations

import math

from scripts.analyze_sakhalkar2023_network import analyze_rows


def test_species_level_route_balance_tracks_tube_length_without_pseudoreplication() -> None:
    visits = [
        {"spcode": "A", "behavior": "robbing", "freq_fm_per_species": "2.0"},
        {"spcode": "A", "behavior": "visiting", "freq_fm_per_species": "9.0"},
        {"spcode": "B", "behavior": "thieving", "freq_fm_per_species": "2.0"},
        {"spcode": "C", "behavior": "robbing", "freq_fm_per_species": "1.0"},
        {"spcode": "C", "behavior": "thieving", "freq_fm_per_species": "1.0"},
        {"spcode": "C", "behavior": "pollinating", "freq_fm_per_species": "3.0"},
    ]
    traits = [
        {"spcode": "A", "tube_length": "10"},
        {"spcode": "B", "tube_length": "2"},
        {"spcode": "C", "tube_length": "6"},
    ]

    result = analyze_rows(visits, traits, permutations=999, seed=7)

    assert result["raw_cheater_rows"] == 6
    assert result["analysis_visit_rows"] == 5
    assert result["behavior_counts"] == {
        "pollinating": 1,
        "robbing": 2,
        "thieving": 2,
    }
    balance = result["tube_length_cheating_mode_balance"]
    assert balance["n_species"] == 3
    assert math.isclose(balance["spearman_rho"], 1.0, abs_tol=1e-12)
    assert 0.0 < balance["permutation_p_two_sided"] <= 1.0
    assert balance["seed"] == 7


def test_species_without_cheater_activity_does_not_enter_route_balance() -> None:
    visits = [
        {"spcode": "A", "behavior": "pollinating", "freq_fm_per_species": "2.0"},
        {"spcode": "B", "behavior": "robbing", "freq_fm_per_species": "1.0"},
    ]
    traits = [
        {"spcode": "A", "tube_length": "9"},
        {"spcode": "B", "tube_length": "4"},
    ]

    result = analyze_rows(visits, traits, permutations=99, seed=3)

    balance = result["tube_length_cheating_mode_balance"]
    assert balance["n_species"] == 1
    assert balance["spearman_rho"] is None
    assert balance["permutation_p_two_sided"] is None


def test_missing_or_non_numeric_frequencies_are_not_promoted_to_signal() -> None:
    visits = [
        {"spcode": "A", "behavior": "robbing", "freq_fm_per_species": ""},
        {"spcode": "A", "behavior": "thieving", "freq_fm_per_species": "bad"},
    ]
    traits = [{"spcode": "A", "tube_length": "5"}]

    result = analyze_rows(visits, traits, permutations=99, seed=1)

    assert result["tube_length_cheating_mode_balance"]["n_species"] == 0
    assert result["tube_length_cheating_mode_balance"]["spearman_rho"] is None
