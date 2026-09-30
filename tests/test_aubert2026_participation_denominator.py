from __future__ import annotations

from scripts.audit_aubert2026_participation_denominator import audit_denominator


def _tables():
    cameras = [
        {
            "waypoint": "w1",
            "site": "s1",
            "plant_species": "P1",
            "start_date": "2026-01-01",
            "end_date": "2026-01-10",
            "duration_sampling_hours": "100",
            "camera_flowers_count": "2",
            "camera_problem": "",
        },
        {
            "waypoint": "w2",
            "site": "s1",
            "plant_species": "P2",
            "start_date": "2026-01-01",
            "end_date": "2026-01-10",
            "duration_sampling_hours": "120",
            "camera_flowers_count": "3",
            "camera_problem": "",
        },
    ]
    interactions = [
        {
            "waypoint": "w1",
            "site": "s1",
            "date": "2026-01-02",
            "hummingbird_species": "B1",
            "hummingbird_genus": "X",
            "hummingbird_family": "Trochilidae",
            "piercing": "no",
        },
        {
            "waypoint": "w2",
            "site": "s1",
            "date": "2026-01-03",
            "hummingbird_species": "B2",
            "hummingbird_genus": "X",
            "hummingbird_family": "Trochilidae",
            "piercing": "yes",
        },
        {
            "waypoint": "w2",
            "site": "s1",
            "date": "2026-02-01",
            "hummingbird_species": "B3",
            "hummingbird_genus": "X",
            "hummingbird_family": "Trochilidae",
            "piercing": "no",
        },
    ]
    plants = [
        {"plant_species": "P1", "site": "s1", "Tubelength": "2.0", "Country": "Ecuador"},
        {"plant_species": "P2", "site": "s1", "Tubelength": "3.0", "Country": "Ecuador"},
    ]
    birds = [
        {"hummingbird_species": "B1", "culmen_length": "20"},
        {"hummingbird_species": "B2", "culmen_length": "25"},
        {"hummingbird_species": "B3", "culmen_length": "30"},
    ]
    return interactions, cameras, plants, birds


def test_temporal_site_pool_creates_defensible_zeros_without_global_cross_product() -> None:
    result = audit_denominator(*_tables())
    d = result["candidate_denominator"]
    assert d["eligible_camera_deployments"] == 2
    assert d["potential_dyads_temporal_pool"] == 4
    assert d["potential_dyads_sitewide_pool"] == 6
    assert d["route_eligible_positive_dyads_temporal_pool"] == 2
    assert d["zero_dyads_temporal_pool"] == 2
    assert d["trait_matched_potential_dyads_temporal_pool"] == 4
    assert result["decision_inputs"]["temporal_denominator_is_possible"] is True
    assert result["decision_inputs"]["flower_hours_offset_is_possible"] is True


def test_route_status_is_not_used_to_define_local_bird_availability() -> None:
    interactions, cameras, plants, birds = _tables()
    interactions.append(
        {
            "waypoint": "w1",
            "site": "s1",
            "date": "2026-01-04",
            "hummingbird_species": "B4",
            "hummingbird_genus": "X",
            "hummingbird_family": "Trochilidae",
            "piercing": "not_interacting",
        }
    )
    birds.append({"hummingbird_species": "B4", "culmen_length": "22"})
    result = audit_denominator(interactions, cameras, plants, birds)
    d = result["candidate_denominator"]
    assert d["potential_dyads_temporal_pool"] == 6
    assert d["route_eligible_positive_dyads_temporal_pool"] == 2
    assert d["zero_dyads_temporal_pool"] == 4
