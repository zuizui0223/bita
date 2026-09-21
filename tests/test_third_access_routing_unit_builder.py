from __future__ import annotations

import math

import pytest

from scripts.build_third_access_routing_units import build_units


def _plant_traits() -> list[dict[str, str]]:
    rows = []
    for site in ("S1", "S2"):
        for p in range(5):
            for rep in range(2):
                rows.append(
                    {
                        "site_id": site,
                        "plant_species": f"P{p}",
                        "access_depth_mm": str(20 + 2 * p + rep),
                    }
                )
    return rows


def _mammal_traits() -> list[dict[str, str]]:
    rows = []
    for m in range(5):
        for rep in range(2):
            rows.append(
                {
                    "mammal_species": f"M{m}",
                    "rostral_reach_mm": str(12 + 1.5 * m + rep),
                }
            )
    return rows


def _events(role: str = "CONFIRMATORY") -> list[dict[str, str]]:
    rows = []
    event = 0
    for site in ("S1", "S2"):
        for p in range(5):
            for m in range(5):
                event += 1
                rows.append(
                    {
                        "event_id": f"E{event:04d}",
                        "dataset_role": role,
                        "site_id": site,
                        "plant_species": f"P{p}",
                        "mammal_species": f"M{m}",
                        "route_code": "B" if p > m else "L",
                        "visitor_id_confidence": "HIGH",
                        "clip_quality": "PASS",
                    }
                )
    return rows


def test_builder_rejects_pilot_events_instead_of_silently_dropping_them() -> None:
    with pytest.raises(ValueError, match="PILOT_OR_NONCONFIRMATORY_EVENT_SUPPLIED"):
        build_units(_events("PILOT"), _plant_traits(), _mammal_traits())

    mixed = _events()
    mixed[0]["dataset_role"] = "PILOT"
    with pytest.raises(ValueError, match="PILOT_OR_NONCONFIRMATORY_EVENT_SUPPLIED"):
        build_units(mixed, _plant_traits(), _mammal_traits())


def test_builder_aggregates_only_frozen_confirmatory_route_classes() -> None:
    events = _events()
    events.extend(
        [
            {
                "event_id": "A001",
                "dataset_role": "CONFIRMATORY",
                "site_id": "S1",
                "plant_species": "P0",
                "mammal_species": "M0",
                "route_code": "A",
                "visitor_id_confidence": "HIGH",
                "clip_quality": "PASS",
            },
            {
                "event_id": "N001",
                "dataset_role": "CONFIRMATORY",
                "site_id": "S1",
                "plant_species": "P0",
                "mammal_species": "M0",
                "route_code": "N",
                "visitor_id_confidence": "HIGH",
                "clip_quality": "PASS",
            },
            {
                "event_id": "LOW1",
                "dataset_role": "CONFIRMATORY",
                "site_id": "S1",
                "plant_species": "P0",
                "mammal_species": "M0",
                "route_code": "B",
                "visitor_id_confidence": "LOW",
                "clip_quality": "PASS",
            },
            {
                "event_id": "FAIL1",
                "dataset_role": "CONFIRMATORY",
                "site_id": "S1",
                "plant_species": "P0",
                "mammal_species": "M0",
                "route_code": "B",
                "visitor_id_confidence": "HIGH",
                "clip_quality": "FAIL",
            },
        ]
    )
    units, audit = build_units(events, _plant_traits(), _mammal_traits())
    assert len(units) == 50
    assert audit["events_ambiguous_or_nonnectar_excluded"] == 2
    assert audit["events_low_identity_excluded"] == 1
    assert audit["events_quality_excluded"] == 1


def test_builder_uses_median_morphology_and_frozen_log_ratio() -> None:
    units, _audit = build_units(_events(), _plant_traits(), _mammal_traits())
    row = next(
        row
        for row in units
        if row["site_id"] == "S1"
        and row["plant_species"] == "P0"
        and row["mammal_species"] == "M0"
    )
    # medians of (20,21) and (12,13)
    assert row["P_j_mm"] == 20.5
    assert row["V_i_mm"] == 12.5
    assert math.isclose(
        float(row["M_log_ratio"]),
        math.log(20.5 / 12.5),
        rel_tol=0.0,
        abs_tol=1e-15,
    )
    assert int(row["B_count"]) + int(row["L_count"]) == 1
    assert float(row["Y_bypass_prop"]) in {0.0, 1.0}


def test_builder_rejects_duplicate_event_ids() -> None:
    events = _events()
    events[1]["event_id"] = events[0]["event_id"]
    with pytest.raises(ValueError, match="event_id must be unique"):
        build_units(events, _plant_traits(), _mammal_traits())
