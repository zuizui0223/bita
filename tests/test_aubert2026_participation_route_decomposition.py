from __future__ import annotations

import pytest

from scripts.analyze_aubert2026_participation_route_decomposition import (
    aggregate_bird_plant_dyads,
    aggregate_site_dyads,
    analyze_tables,
    build_opportunity_rows,
    classify,
)


def _tables():
    cameras = []
    plants = []
    birds = []
    interactions = []
    for plant_i, tube in enumerate((1.5, 2.0, 3.0, 4.0), start=1):
        plant = f"P{plant_i}"
        waypoint = f"W{plant_i}"
        cameras.append(
            {
                "waypoint": waypoint,
                "site": "S1",
                "plant_species": plant,
                "start_date": "2026-01-01",
                "end_date": "2026-01-10",
                "duration_sampling_hours": "100",
                "camera_problem": "no",
            }
        )
        plants.append(
            {
                "plant_species": plant,
                "site": "S1",
                "Tubelength": str(tube),
                "Country": "Ecuador",
            }
        )

    for bird_i, bill_mm in enumerate((20, 30, 40), start=1):
        bird = f"B{bird_i}"
        birds.append({"hummingbird_species": bird, "culmen_length": str(bill_mm)})
        # Presence establishes availability at this site-period.
        interactions.append(
            {
                "waypoint": "W1",
                "site": "S1",
                "date": "2026-01-02",
                "hummingbird_species": bird,
                "hummingbird_genus": "X",
                "hummingbird_family": "Trochilidae",
                "piercing": "not_interacting",
                "feeding_activity": "no_feeding",
            }
        )

    # Create decreasing total participation with mismatch and increasing robbery share.
    for plant_i in range(1, 5):
        waypoint = f"W{plant_i}"
        for bird_i in range(1, 4):
            bird = f"B{bird_i}"
            total = max(1, 8 - plant_i)
            rob = min(total, plant_i - 1)
            leg = total - rob
            for k in range(rob):
                interactions.append(
                    {
                        "waypoint": waypoint,
                        "site": "S1",
                        "date": "2026-01-03",
                        "hummingbird_species": bird,
                        "hummingbird_genus": "X",
                        "hummingbird_family": "Trochilidae",
                        "piercing": "yes",
                        "feeding_activity": "perching",
                    }
                )
            for k in range(leg):
                interactions.append(
                    {
                        "waypoint": waypoint,
                        "site": "S1",
                        "date": "2026-01-03",
                        "hummingbird_species": bird,
                        "hummingbird_genus": "X",
                        "hummingbird_family": "Trochilidae",
                        "piercing": "no",
                        "feeding_activity": "hoverflying",
                    }
                )
    return interactions, cameras, plants, birds


def test_opportunity_builder_adds_local_zero_opportunities_and_excludes_no_feeding() -> None:
    interactions, cameras, plants, birds = _tables()
    rows, audit = build_opportunity_rows(interactions, cameras, plants, birds)
    assert audit["potential_waypoint_bird_rows"] == 12
    assert len(rows) == 12
    # Presence-only no_feeding rows must not add to exploitation counts.
    assert all(int(row["total_count"]) <= 7 for row in rows)


def test_aggregation_preserves_counts_and_effort() -> None:
    interactions, cameras, plants, birds = _tables()
    rows, _ = build_opportunity_rows(interactions, cameras, plants, birds)
    site = aggregate_site_dyads(rows)
    dyads = aggregate_bird_plant_dyads(site)
    assert len(site) == 12
    assert len(dyads) == 12
    assert sum(int(row["total_count"]) for row in site) == sum(
        int(row["total_count"]) for row in dyads
    )


def test_synthetic_analysis_can_identify_suppression_plus_rerouting() -> None:
    result = analyze_tables(*_tables(), permutations=199, seed=123)
    assert result["participation"]["pooled_within_bird_rank_rho"] < 0
    assert result["routing_reconstructed"]["pooled_within_bird_rank_rho"] > 0
    assert result["outcome_classification"] == "SUPPRESSION_PLUS_REROUTING"


def test_classification_does_not_call_nonsignificance_equivalence() -> None:
    participation = {
        "pooled_within_bird_rank_rho": -0.2,
        "within_bird_permutation_p_two_sided": 0.2,
    }
    routing = {
        "pooled_within_bird_rank_rho": 0.4,
        "within_bird_permutation_p_two_sided": 0.01,
    }
    assert classify(participation, routing) == "ROUTING_WITHOUT_DETECTED_PARTICIPATION_LOSS"


def test_unknown_camera_problem_fails_closed() -> None:
    interactions, cameras, plants, birds = _tables()
    cameras[0]["camera_problem"] = "mystery_state"
    with pytest.raises(ValueError, match="unrecognized camera_problem"):
        build_opportunity_rows(interactions, cameras, plants, birds)
