from __future__ import annotations

from scripts.analyze_aubert2026_zenodo_extension import build_pair_site_rows, summarize_pair_sites


def test_build_pair_site_rows_converts_culmen_mm_to_cm_and_scores_barrier() -> None:
    cameras = [
        {"waypoint":"w1","site":"S1","plant_species":"P1"},
        {"waypoint":"w2","site":"S1","plant_species":"P2"},
    ]
    plants = [
        {"plant_species":"P1","site":"S1","Tubelength":"4.0","Country":"Ecuador"},
        {"plant_species":"P2","site":"S1","Tubelength":"1.0","Country":"Ecuador"},
    ]
    birds = [
        {"hummingbird_species":"B1","culmen_length":"20"},
    ]
    interactions = [
        {"waypoint":"w1","hummingbird_species":"B1","hummingbird_genus":"X","hummingbird_family":"Trochilidae","piercing":"yes"},
        {"waypoint":"w1","hummingbird_species":"B1","hummingbird_genus":"X","hummingbird_family":"Trochilidae","piercing":"no"},
        {"waypoint":"w2","hummingbird_species":"B1","hummingbird_genus":"X","hummingbird_family":"Trochilidae","piercing":"no"},
    ]
    rows, audit = build_pair_site_rows(interactions,cameras,plants,birds)
    assert audit["pair_site_rows"] == 2
    assert audit["trait_matched_interactions"] == 3
    barriers = sorted((round(float(r["mismatch_log_t_over_b"]),6), bool(r["trait_barrier"])) for r in rows)
    assert barriers[0][1] is False
    assert barriers[1][1] is True


def test_summary_detects_higher_robbery_under_barrier() -> None:
    rows=[]
    for i,rate in enumerate([0.8,0.9,0.7,0.85]):
        rows.append({"site":"S","bird_group":"hummingbird","robbery_rate":rate,"mismatch_log_t_over_b":0.2+i*0.1,"trait_barrier":True})
    for i,rate in enumerate([0.0,0.1,0.2,0.05]):
        rows.append({"site":"S","bird_group":"hummingbird","robbery_rate":rate,"mismatch_log_t_over_b":-0.4+i*0.1,"trait_barrier":False})
    out=summarize_pair_sites(rows,permutations=199,seed=4)
    assert out["pair_site_n"] == 8
    assert out["mean_robbery_rate_barrier"] > out["mean_robbery_rate_accessible"]
    assert out["barrier_minus_accessible_mean_rate"] > 0
    assert out["mismatch_spearman_rho"] > 0
    assert 0 < out["barrier_mean_difference_permutation_p"] <= 1
    assert out["site_difference"]["eligible_sites"] == 1


def test_summary_reports_min_interaction_sensitivity() -> None:
    rows = [
        {"site":"S1","bird_group":"hummingbird","n_interactions":1,"robbery_rate":1.0,"mismatch_log_t_over_b":0.4,"trait_barrier":True},
        {"site":"S1","bird_group":"hummingbird","n_interactions":5,"robbery_rate":0.8,"mismatch_log_t_over_b":0.3,"trait_barrier":True},
        {"site":"S1","bird_group":"hummingbird","n_interactions":5,"robbery_rate":0.1,"mismatch_log_t_over_b":-0.2,"trait_barrier":False},
        {"site":"S2","bird_group":"hummingbird","n_interactions":6,"robbery_rate":0.7,"mismatch_log_t_over_b":0.2,"trait_barrier":True},
        {"site":"S2","bird_group":"hummingbird","n_interactions":6,"robbery_rate":0.0,"mismatch_log_t_over_b":-0.3,"trait_barrier":False},
        {"site":"S3","bird_group":"hummingbird","n_interactions":7,"robbery_rate":0.6,"mismatch_log_t_over_b":0.25,"trait_barrier":True},
        {"site":"S3","bird_group":"hummingbird","n_interactions":7,"robbery_rate":0.05,"mismatch_log_t_over_b":-0.25,"trait_barrier":False},
        {"site":"S2","bird_group":"hummingbird","n_interactions":1,"robbery_rate":0.0,"mismatch_log_t_over_b":-0.4,"trait_barrier":False},
    ]
    out = summarize_pair_sites(rows, permutations=99, seed=8)
    sensitivity = out["min_interaction_sensitivity"]

    assert sensitivity["min_1"]["n_pair_sites"] == 8
    assert sensitivity["min_5"]["n_pair_sites"] == 6
    assert sensitivity["min_5"]["barrier_minus_accessible_mean_rate"] > 0
    assert sensitivity["min_5"]["mismatch_spearman_rho"] > 0
