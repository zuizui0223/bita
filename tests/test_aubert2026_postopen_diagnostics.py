from __future__ import annotations

import math

from scripts.analyze_aubert2026_route_specific_participation_postopen import (
    split_route_counts,
)
from scripts.analyze_aubert2026_routing_threshold import fit_sigmoid_threshold
from scripts.audit_aubert2026_threshold_bootstrap_boundary import (
    boundary_stickiness,
)


def test_route_specific_counts_reconstruct_frozen_primary_definition() -> None:
    cameras = [
        {
            "waypoint": "W1",
            "site": "S1",
            "plant_species": "P1",
            "start_date": "2026-01-01",
            "end_date": "2026-01-10",
            "duration_sampling_hours": "100",
            "camera_problem": "no",
        }
    ]
    plants = [
        {
            "plant_species": "P1",
            "site": "S1",
            "Tubelength": "3.0",
            "Country": "Ecuador",
        }
    ]
    birds = [
        {"hummingbird_species": "B1", "culmen_length": "20"},
        {"hummingbird_species": "B2", "culmen_length": "40"},
    ]
    common = {
        "waypoint": "W1",
        "site": "S1",
        "hummingbird_genus": "X",
        "hummingbird_family": "Trochilidae",
    }
    interactions = [
        {
            **common,
            "date": "2026-01-02",
            "hummingbird_species": "B1",
            "piercing": "yes",
            "feeding_activity": "perching",
        },
        {
            **common,
            "date": "2026-01-03",
            "hummingbird_species": "B1",
            "piercing": "no",
            "feeding_activity": "hoverflying",
        },
        {
            **common,
            "date": "2026-01-04",
            "hummingbird_species": "B1",
            "piercing": "yes",
            "feeding_activity": "no_feeding",
        },
        {
            **common,
            "date": "2026-01-05",
            "hummingbird_species": "B2",
            "piercing": "",
            "feeding_activity": "perching",
        },
    ]

    robbery, legitimate, audit = split_route_counts(
        interactions, cameras, plants, birds
    )
    r = {edge.bird: edge.primary_count for edge in robbery}
    l = {edge.bird: edge.primary_count for edge in legitimate}

    assert audit["route_specific_reconstruction_mismatches"] == 0
    assert r == {"B1": 1, "B2": 0}
    assert l == {"B1": 1, "B2": 1}
    assert audit["robbing_interaction_records"] == 1
    assert audit["legitimate_interaction_records"] == 2


def test_threshold_boundary_stickiness_accounts_for_all_finite_replicates() -> None:
    x = [-1.0 + 2.0 * i / 39 for i in range(40)]
    y = [0.05 + 0.40 / (1.0 + math.exp(-2.0 * (xx - 0.1))) for xx in x]
    full = fit_sigmoid_threshold(x, y)
    result = boundary_stickiness(
        x,
        y,
        full,
        replicates=25,
        seed=123,
    )

    total = (
        result["upper_boundary_replicates"]
        + result["lower_boundary_replicates"]
        + result["interior_replicates"]
    )
    fractions = (
        result["upper_boundary_fraction"]
        + result["lower_boundary_fraction"]
        + result["interior_fraction"]
    )
    assert result["finite_replicates"] == 25
    assert total == 25
    assert math.isclose(fractions, 1.0, rel_tol=0, abs_tol=1e-12)
    assert result["search_low"] <= result["median_xstar"] <= result["search_high"]
