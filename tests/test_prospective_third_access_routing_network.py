from __future__ import annotations

import math

import pytest

from scripts.analyze_joint_access_routing import combine_rhos_equal_network
from scripts.analyze_joint_access_routing_k3 import summarize_joint_k3
from scripts.analyze_third_access_routing_network import (
    SEED,
    summarize_third_network,
    validate_confirmatory_gate,
)


def _third_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    plants = [f"Protea_{i}" for i in range(6)]
    visitors = [f"Mammal_{i}" for i in range(6)]
    sites = ["site_A", "site_B"]
    for s_idx, site in enumerate(sites):
        for p_idx, plant in enumerate(plants):
            for v_idx, visitor in enumerate(visitors):
                # A deterministic mechanical mismatch with within-site variation.
                m = math.log((18.0 + 2.5 * p_idx + 0.4 * s_idx) / (11.0 + 1.6 * v_idx))
                # Route balance rises monotonically with mismatch, but stays away
                # from 0/1 so every unit has both event types.
                scaled = 1.0 / (1.0 + math.exp(-3.0 * m))
                b = max(1, min(19, round(20 * scaled)))
                l = 20 - b
                rows.append(
                    {
                        "site": site,
                        "plant": plant,
                        "visitor": visitor,
                        "M": m,
                        "B": b,
                        "L": l,
                        "Y": b / (b + l),
                    }
                )
    return rows


def _sakhalkar_points() -> list[dict[str, float]]:
    return [
        {"tube_length": float(i + 1), "balance": float(i) / 20.0}
        for i in range(20)
    ]


def _aubert_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for site in ("A", "B"):
        for i in range(30):
            mismatch = (i - 14.5) / 10.0
            robbery = 1.0 / (1.0 + math.exp(-mismatch))
            rows.append(
                {
                    "site": site,
                    "mismatch_log_t_over_b": mismatch,
                    "robbery_rate": robbery,
                }
            )
    return rows


def test_third_network_gate_passes_target_synthetic_design() -> None:
    gate = validate_confirmatory_gate(_third_rows())
    assert gate["n_units"] == 72
    assert gate["n_visitor_species"] == 6
    assert gate["n_plant_species"] == 6
    assert gate["n_sites"] == 2
    assert gate["total_bypass_events"] > 0
    assert gate["total_legitimate_events"] > 0


@pytest.mark.parametrize(
    "mutator, token",
    [
        (lambda rows: rows[:29], "n_units<30"),
        (
            lambda rows: [
                dict(row, visitor="Mammal_0")
                for row in rows
            ],
            "n_visitor_species<5",
        ),
        (
            lambda rows: [
                dict(row, plant="Protea_0")
                for row in rows
            ],
            "n_plant_species<5",
        ),
        (
            lambda rows: [
                dict(row, B=0, L=20, Y=0.0)
                for row in rows
            ],
            "no_bypass_events",
        ),
        (
            lambda rows: [
                dict(row, B=20, L=0, Y=1.0)
                for row in rows
            ],
            "no_legitimate_events",
        ),
    ],
)
def test_third_network_gate_fails_closed(mutator, token: str) -> None:
    with pytest.raises(ValueError, match=token):
        validate_confirmatory_gate(mutator(_third_rows()))


def test_third_network_analysis_is_reproducible_and_positive_on_synthetic_data() -> None:
    first = summarize_third_network(_third_rows(), permutations=199, seed=SEED)
    second = summarize_third_network(_third_rows(), permutations=199, seed=SEED)
    assert first == second
    assert first["status"] == "CONFIRMATORY_GATE_PASS"
    assert first["effect"]["rho_site_adjusted_rank"] > 0
    assert 0 < first["effect"]["permutation_p_two_sided"] <= 1


def test_k3_joint_uses_equal_network_fisher_z_and_no_raw_pooling() -> None:
    result = summarize_joint_k3(
        _sakhalkar_points(),
        _aubert_rows(),
        _third_rows(),
        permutations=99,
        seed=20260921,
    )
    effects = result["network_effects"]
    expected = combine_rhos_equal_network(
        [
            effects["sakhalkar_insects"],
            effects["aubert_ephi_birds"],
            effects["prospective_mammals"],
        ]
    )
    assert result["network_count"] == 3
    assert math.isclose(
        result["joint_equal_network_fisher_z_rho"],
        expected,
        rel_tol=0.0,
        abs_tol=1e-15,
    )
    assert 0 < result["joint_permutation_p_two_sided"] <= 1
    assert "raw observations are not pooled" in result["claim_boundary"]
    assert "between-network heterogeneity" in result["claim_boundary"]
