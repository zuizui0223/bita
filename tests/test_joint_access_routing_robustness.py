from __future__ import annotations

from scripts.analyze_joint_access_routing_robustness import (
    filter_aubert_by_min_interactions,
    summarize_thresholds,
)


def _sakh():
    return [
        {"tube_length": 1.0, "balance": -1.0, "route_class": "thief_only"},
        {"tube_length": 2.0, "balance": -0.3, "route_class": "mixed"},
        {"tube_length": 3.0, "balance": 0.4, "route_class": "mixed"},
        {"tube_length": 4.0, "balance": 1.0, "route_class": "robber_only"},
    ]


def _aubert():
    return [
        {"site":"S1","n_interactions":1,"robbery_rate":1.0,"mismatch_log_t_over_b":0.5,"trait_barrier":True},
        {"site":"S1","n_interactions":5,"robbery_rate":0.8,"mismatch_log_t_over_b":0.3,"trait_barrier":True},
        {"site":"S1","n_interactions":5,"robbery_rate":0.1,"mismatch_log_t_over_b":-0.3,"trait_barrier":False},
        {"site":"S2","n_interactions":6,"robbery_rate":0.7,"mismatch_log_t_over_b":0.2,"trait_barrier":True},
        {"site":"S2","n_interactions":6,"robbery_rate":0.0,"mismatch_log_t_over_b":-0.2,"trait_barrier":False},
        {"site":"S3","n_interactions":7,"robbery_rate":0.6,"mismatch_log_t_over_b":0.25,"trait_barrier":True},
        {"site":"S3","n_interactions":7,"robbery_rate":0.05,"mismatch_log_t_over_b":-0.25,"trait_barrier":False},
        {"site":"S2","n_interactions":1,"robbery_rate":0.0,"mismatch_log_t_over_b":-0.4,"trait_barrier":False},
    ]


def test_filter_aubert_by_min_interactions() -> None:
    rows = _aubert()
    assert len(filter_aubert_by_min_interactions(rows, 1)) == 8
    assert len(filter_aubert_by_min_interactions(rows, 2)) == 6
    assert len(filter_aubert_by_min_interactions(rows, 5)) == 6


def test_joint_threshold_summary_preserves_positive_direction() -> None:
    out = summarize_thresholds(
        _sakh(),
        _aubert(),
        thresholds=(1, 2, 5),
        permutations=99,
        seed=11,
    )
    assert set(out["thresholds"]) == {"min_1", "min_2", "min_5"}
    for key in ["min_1", "min_2", "min_5"]:
        result = out["thresholds"][key]
        assert result["aubert_n_units"] >= 4
        assert result["aubert_site_adjusted_rho"] > 0
        assert result["joint_equal_network_fisher_z_rho"] > 0
        assert 0 < result["joint_permutation_p_two_sided"] <= 1


def test_robustness_output_is_aggregate_only() -> None:
    out = summarize_thresholds(
        _sakh(),
        _aubert(),
        thresholds=(1, 5),
        permutations=19,
        seed=3,
    )
    text = str(out)
    assert "S1" not in text
    assert "S2" not in text
    assert "S3" not in text
    assert "raw_rows" not in out
