from __future__ import annotations

import math

from scripts.analyze_aubert2026_participation_route_decomposition import (
    Edge,
    build_opportunity_edges,
    classify_participation,
    fit_two_way_poisson,
    plant_cluster_jackknife,
)


def _synthetic_edges(rate_ratio: float) -> list[Edge]:
    edges: list[Edge] = []
    row_scale = [10, 14, 18, 22, 26, 30]
    bird_scale = [1, 2, 3, 4]
    for wi, a in enumerate(row_scale):
        for bi, b in enumerate(bird_scale):
            barrier = (wi + bi) % 2
            mu = a * b * (rate_ratio if barrier else 1.0)
            y = max(1, int(round(mu)))
            edges.append(
                Edge(
                    waypoint=f"W{wi}",
                    bird=f"B{bi}",
                    plant=f"P{wi // 2}",
                    site="S1",
                    barrier=barrier,
                    mismatch=0.5 if barrier else -0.5,
                    primary_count=y,
                    strict_count=y,
                    broad_count=y,
                )
            )
    return edges


def test_two_way_poisson_recovers_suppression_with_row_and_bird_effects() -> None:
    result = fit_two_way_poisson(
        _synthetic_edges(0.5),
        count_field="primary_count",
    )
    assert 0.35 < result["rate_ratio"] < 0.70
    assert result["max_margin_relative_error"] < 1e-8


def test_two_way_poisson_recovers_null_rate_ratio() -> None:
    result = fit_two_way_poisson(
        _synthetic_edges(1.0),
        count_field="primary_count",
    )
    assert math.isclose(result["rate_ratio"], 1.0, rel_tol=0.08)


def test_two_way_poisson_recovers_enhancement() -> None:
    result = fit_two_way_poisson(
        _synthetic_edges(2.0),
        count_field="primary_count",
    )
    assert 1.6 < result["rate_ratio"] < 2.4


def test_classification_uses_frozen_equivalence_rule() -> None:
    equivalent = classify_participation(
        {
            "fit": {"rate_ratio": 1.02},
            "ci95_rate_ratio": [0.85, 1.20],
            "ci90_rate_ratio": [0.88, 1.18],
        }
    )
    assert equivalent["classification"] == "ROUTING_WITHOUT_MATERIAL_PARTICIPATION_LOSS"

    reduced = classify_participation(
        {
            "fit": {"rate_ratio": 0.70},
            "ci95_rate_ratio": [0.60, 0.82],
            "ci90_rate_ratio": [0.61, 0.80],
        }
    )
    assert reduced["classification"] == "PARTICIPATION_REDUCTION_PLUS_ROUTING"

    unresolved = classify_participation(
        {
            "fit": {"rate_ratio": 0.90},
            "ci95_rate_ratio": [0.72, 1.08],
            "ci90_rate_ratio": [0.76, 1.04],
        }
    )
    assert unresolved["classification"] == "PARTICIPATION_UNRESOLVED_ROUTING_ESTABLISHED"


def test_builder_uses_clean_camera_presence_for_pool_and_excludes_no_feeding() -> None:
    cameras = [
        {
            "waypoint": "W1",
            "site": "S1",
            "plant_species": "P1",
            "start_date": "2026-01-01",
            "end_date": "2026-01-10",
            "duration_sampling_hours": "100",
            "camera_problem": "no",
        },
        {
            "waypoint": "W2",
            "site": "S1",
            "plant_species": "P2",
            "start_date": "2026-01-01",
            "end_date": "2026-01-10",
            "duration_sampling_hours": "100",
            "camera_problem": "yes",
        },
    ]
    plants = [
        {"plant_species": "P1", "site": "S1", "Tubelength": "3.0", "Country": "Ecuador"},
        {"plant_species": "P2", "site": "S1", "Tubelength": "2.0", "Country": "Ecuador"},
    ]
    birds = [
        {"hummingbird_species": "B1", "culmen_length": "20"},
        {"hummingbird_species": "B2", "culmen_length": "40"},
    ]
    interactions = [
        {
            "waypoint": "W1",
            "site": "S1",
            "date": "2026-01-02",
            "hummingbird_species": "B1",
            "hummingbird_genus": "X",
            "hummingbird_family": "Trochilidae",
            "piercing": "no",
            "feeding_activity": "no_feeding",
        },
        {
            "waypoint": "W1",
            "site": "S1",
            "date": "2026-01-03",
            "hummingbird_species": "B2",
            "hummingbird_genus": "X",
            "hummingbird_family": "Trochilidae",
            "piercing": "yes",
            "feeding_activity": "perching",
        },
        {
            "waypoint": "W2",
            "site": "S1",
            "date": "2026-01-03",
            "hummingbird_species": "B1",
            "hummingbird_genus": "X",
            "hummingbird_family": "Trochilidae",
            "piercing": "yes",
            "feeding_activity": "perching",
        },
    ]
    edges, audit = build_opportunity_edges(interactions, cameras, plants, birds)
    assert audit["clean_waypoints"] == 1
    assert len(edges) == 2
    counts = {edge.bird: edge.primary_count for edge in edges}
    assert counts["B1"] == 0
    assert counts["B2"] == 1


def test_plant_cluster_jackknife_runs_on_many_clusters() -> None:
    edges: list[Edge] = []
    for plant_i in range(30):
        for bird_i in range(4):
            waypoint = f"W{plant_i}"
            barrier = (plant_i + bird_i) % 2
            base = (8 + plant_i % 5) * (1 + bird_i)
            y = max(1, int(round(base * (0.9 if barrier else 1.0))))
            edges.append(
                Edge(
                    waypoint=waypoint,
                    bird=f"B{bird_i}",
                    plant=f"P{plant_i}",
                    site=f"S{plant_i % 3}",
                    barrier=barrier,
                    mismatch=0.3 if barrier else -0.3,
                    primary_count=y,
                    strict_count=y,
                    broad_count=y,
                )
            )
    result = plant_cluster_jackknife(edges, count_field="primary_count")
    assert result["plant_clusters"] == 30
    assert result["jackknife_se_beta"] >= 0
    assert len(result["ci95_rate_ratio"]) == 2
    assert len(result["ci90_rate_ratio"]) == 2
    assert result["ci95_rate_ratio"][0] <= result["fit"]["rate_ratio"] <= result["ci95_rate_ratio"][1]
