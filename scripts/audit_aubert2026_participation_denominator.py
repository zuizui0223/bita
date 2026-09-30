"""Outcome-blind denominator audit for the Aubert/EPHI participation analysis.

This audit asks only whether the public EPHI camera/interactions tables support a
defensible participation denominator before any mismatch -> participation effect is
computed.

Proposed opportunity unit:
    camera deployment x bird species locally available in the same site and
    overlapping the deployment date interval.

Local availability is defined from any target-bird observation row (Trochilidae or
Diglossa) in the interaction table, regardless of piercing outcome. This avoids
using the route outcome itself to define the consumer pool.

No mismatch effect, coefficient, correlation, or p-value is computed here.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

from scripts.analyze_aubert2026_zenodo_extension import (
    FILES,
    _as_float,
    _download,
    _read,
)

TARGET_FAMILY = "Trochilidae"
TARGET_GENUS = "Diglossa"

DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%m/%d/%Y",
    "%d.%m.%Y",
)


def _parse_date(value: object) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        pass
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _quantiles(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"min": None, "median": None, "max": None}
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    median = ordered[mid] if n % 2 else (ordered[mid - 1] + ordered[mid]) / 2
    return {
        "min": ordered[0],
        "median": median,
        "max": ordered[-1],
    }


def _is_target_bird(row: dict[str, str]) -> bool:
    family = str(row.get("hummingbird_family", "")).strip()
    genus = str(row.get("hummingbird_genus", "")).strip()
    species = str(row.get("hummingbird_species", "")).strip()
    return bool(species) and (family == TARGET_FAMILY or genus == TARGET_GENUS)


def _primary_route_status(value: object) -> str | None:
    raw = str(value or "").strip().lower()
    if raw in {"yes", "no"}:
        return raw
    if raw in {"", "na", "n/a", "nan", "none"}:
        return "no"
    return None


def _date_in_any_interval(
    value: date | None,
    intervals: list[tuple[date, date]],
) -> bool:
    if value is None:
        return False
    return any(start <= value <= end for start, end in intervals)


def audit_denominator(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
) -> dict[str, object]:
    plant_values: dict[tuple[str, str], list[float]] = defaultdict(list)
    plant_global: dict[str, list[float]] = defaultdict(list)
    for row in plants:
        if str(row.get("Country", "")).strip().lower() not in {"ecuador", ""}:
            continue
        species = str(row.get("plant_species", "")).strip()
        site = str(row.get("site", "")).strip()
        tube = _as_float(row.get("Tubelength"))
        if species and tube is not None and tube > 0:
            plant_global[species].append(tube)
            if site:
                plant_values[(site, species)].append(tube)

    bird_values: dict[str, list[float]] = defaultdict(list)
    for row in birds:
        species = str(row.get("hummingbird_species", "")).strip()
        culmen = _as_float(row.get("culmen_length"))
        if species and culmen is not None and culmen > 0:
            bird_values[species].append(culmen)

    target_obs: list[dict[str, object]] = []
    interaction_date_parseable = 0
    for row in interactions:
        if not _is_target_bird(row):
            continue
        species = str(row.get("hummingbird_species", "")).strip()
        site = str(row.get("site", "")).strip()
        waypoint = str(row.get("waypoint", "")).strip()
        d = _parse_date(row.get("date"))
        if d is not None:
            interaction_date_parseable += 1
        target_obs.append(
            {
                "species": species,
                "site": site,
                "waypoint": waypoint,
                "date": d,
                "route_status": _primary_route_status(row.get("piercing")),
            }
        )

    by_site_obs: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_waypoint_species: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    site_species_all: dict[str, set[str]] = defaultdict(set)
    for obs in target_obs:
        site = str(obs["site"])
        species = str(obs["species"])
        if site:
            by_site_obs[site].append(obs)
            site_species_all[site].add(species)
        waypoint = str(obs["waypoint"])
        if waypoint:
            by_waypoint_species[(waypoint, species)].append(obs)

    deployments: list[dict[str, object]] = []
    camera_date_both_parseable = 0
    duration_positive = 0
    flowers_positive = 0
    camera_problem_nonblank = 0
    problem_counts: Counter[str] = Counter()
    duration_values: list[float] = []
    flower_values: list[float] = []
    duplicate_key_counts: Counter[tuple[str, str, str, str, str]] = Counter()

    for idx, row in enumerate(cameras):
        waypoint = str(row.get("waypoint", "")).strip()
        site = str(row.get("site", "")).strip()
        plant = str(row.get("plant_species", "")).strip()
        start_raw = str(row.get("start_date", "")).strip()
        end_raw = str(row.get("end_date", "")).strip()
        start = _parse_date(start_raw)
        end = _parse_date(end_raw)
        if start is not None and end is not None:
            camera_date_both_parseable += 1
        duration = _as_float(row.get("duration_sampling_hours"))
        flowers = _as_float(row.get("camera_flowers_count"))
        if duration is not None and duration > 0:
            duration_positive += 1
            duration_values.append(duration)
        if flowers is not None and flowers > 0:
            flowers_positive += 1
            flower_values.append(flowers)
        problem = str(row.get("camera_problem", "")).strip()
        if problem:
            camera_problem_nonblank += 1
            problem_counts[problem] += 1
        duplicate_key_counts[(waypoint, site, plant, start_raw, end_raw)] += 1
        deployments.append(
            {
                "deployment_id": idx,
                "waypoint": waypoint,
                "site": site,
                "plant": plant,
                "start": start,
                "end": end,
                "duration": duration,
                "flowers": flowers,
                "problem": problem,
            }
        )

    waypoint_camera_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
    for dep in deployments:
        if dep["waypoint"]:
            waypoint_camera_rows[str(dep["waypoint"])].append(dep)

    waypoint_units: list[dict[str, object]] = []
    waypoint_inconsistent_site_plant = 0
    for waypoint, rows in waypoint_camera_rows.items():
        site_plant = {
            (str(row["site"]), str(row["plant"]))
            for row in rows
            if row["site"] and row["plant"]
        }
        if len(site_plant) != 1:
            waypoint_inconsistent_site_plant += 1
            continue
        site, plant = next(iter(site_plant))
        valid_rows = [
            row
            for row in rows
            if row["start"] is not None
            and row["end"] is not None
            and row["duration"] is not None
            and float(row["duration"]) > 0
        ]
        if not valid_rows:
            continue
        intervals = [
            (row["start"], row["end"])
            for row in valid_rows
            if isinstance(row["start"], date) and isinstance(row["end"], date)
        ]
        total_hours = sum(float(row["duration"]) for row in valid_rows)
        flower_hours_values = [
            float(row["duration"]) * float(row["flowers"])
            for row in valid_rows
            if row["flowers"] is not None and float(row["flowers"]) > 0
        ]
        flower_hours_complete = len(flower_hours_values) == len(valid_rows)
        waypoint_units.append(
            {
                "waypoint": waypoint,
                "site": site,
                "plant": plant,
                "intervals": intervals,
                "sampling_hours": total_hours,
                "flower_hours": (
                    sum(flower_hours_values) if flower_hours_complete else None
                ),
                "camera_rows": len(rows),
                "valid_camera_rows": len(valid_rows),
            }
        )

    eligible_deployments = [
        d
        for d in deployments
        if d["waypoint"]
        and d["site"]
        and d["plant"]
        and d["start"] is not None
        and d["end"] is not None
        and d["duration"] is not None
        and float(d["duration"]) > 0
    ]

    temporal_pool_sizes: list[int] = []
    site_pool_sizes: list[int] = []
    deployment_with_temporal_pool = 0
    deployment_with_site_pool = 0
    opportunity_count_temporal = 0
    opportunity_count_site = 0
    route_eligible_positive_temporal = 0
    zero_opportunities_temporal = 0
    trait_matched_opportunities_temporal = 0
    trait_matched_positive_temporal = 0
    effort_flower_hours_available = 0

    for dep in eligible_deployments:
        site = str(dep["site"])
        waypoint = str(dep["waypoint"])
        plant = str(dep["plant"])
        start = dep["start"]
        end = dep["end"]
        assert isinstance(start, date)
        assert isinstance(end, date)

        temporal_species = {
            str(obs["species"])
            for obs in by_site_obs.get(site, [])
            if isinstance(obs["date"], date) and start <= obs["date"] <= end
        }
        site_species = set(site_species_all.get(site, set()))

        temporal_pool_sizes.append(len(temporal_species))
        site_pool_sizes.append(len(site_species))
        if temporal_species:
            deployment_with_temporal_pool += 1
        if site_species:
            deployment_with_site_pool += 1
        opportunity_count_temporal += len(temporal_species)
        opportunity_count_site += len(site_species)

        if dep["flowers"] is not None and float(dep["flowers"]) > 0:
            effort_flower_hours_available += 1

        tube_vals = plant_values.get((site, plant)) or plant_global.get(plant)
        tube_cm = (
            sum(tube_vals) / len(tube_vals)
            if tube_vals
            else None
        )

        for species in temporal_species:
            route_rows = [
                obs
                for obs in by_waypoint_species.get((waypoint, species), [])
                if isinstance(obs["date"], date)
                and start <= obs["date"] <= end
                and obs["route_status"] in {"yes", "no"}
            ]
            if route_rows:
                route_eligible_positive_temporal += 1
            else:
                zero_opportunities_temporal += 1

            bill_vals = bird_values.get(species)
            bill_cm = (
                sum(bill_vals) / len(bill_vals) / 10.0
                if bill_vals
                else None
            )
            if (
                tube_cm is not None
                and tube_cm > 0
                and bill_cm is not None
                and bill_cm > 0
            ):
                trait_matched_opportunities_temporal += 1
                if route_rows:
                    trait_matched_positive_temporal += 1

    waypoint_pool_sizes: list[int] = []
    waypoint_opportunities = 0
    waypoint_zero_opportunities = 0
    waypoint_route_positive = 0
    waypoint_trait_matched = 0
    waypoint_trait_matched_positive = 0
    waypoint_flower_hours_complete = 0
    rows_per_waypoint = [float(len(rows)) for rows in waypoint_camera_rows.values()]

    for unit in waypoint_units:
        waypoint = str(unit["waypoint"])
        site = str(unit["site"])
        plant = str(unit["plant"])
        intervals = list(unit["intervals"])
        temporal_species = {
            str(obs["species"])
            for obs in by_site_obs.get(site, [])
            if _date_in_any_interval(obs["date"], intervals)
        }
        waypoint_pool_sizes.append(len(temporal_species))
        waypoint_opportunities += len(temporal_species)
        if unit["flower_hours"] is not None:
            waypoint_flower_hours_complete += 1

        tube_vals = plant_values.get((site, plant)) or plant_global.get(plant)
        tube_cm = sum(tube_vals) / len(tube_vals) if tube_vals else None

        for species in temporal_species:
            route_rows = [
                obs
                for obs in by_waypoint_species.get((waypoint, species), [])
                if _date_in_any_interval(obs["date"], intervals)
                and obs["route_status"] in {"yes", "no"}
            ]
            if route_rows:
                waypoint_route_positive += 1
            else:
                waypoint_zero_opportunities += 1

            bill_vals = bird_values.get(species)
            bill_cm = (
                sum(bill_vals) / len(bill_vals) / 10.0
                if bill_vals
                else None
            )
            if (
                tube_cm is not None
                and tube_cm > 0
                and bill_cm is not None
                and bill_cm > 0
            ):
                waypoint_trait_matched += 1
                if route_rows:
                    waypoint_trait_matched_positive += 1

    duplicate_deployment_keys = sum(
        count - 1 for count in duplicate_key_counts.values() if count > 1
    )

    camera_n = len(cameras)
    target_n = len(target_obs)
    eligible_n = len(eligible_deployments)

    return {
        "analysis_name": "aubert_ephi_participation_denominator_audit",
        "status": "OUTCOME_BLIND_WITH_RESPECT_TO_MISMATCH_EFFECT",
        "source": "EPHI Zenodo 10.5281/zenodo.14185547",
        "camera_table": {
            "rows": camera_n,
            "date_parseable_both": camera_date_both_parseable,
            "date_parseable_both_fraction": (
                camera_date_both_parseable / camera_n if camera_n else None
            ),
            "positive_duration_rows": duration_positive,
            "positive_duration_fraction": duration_positive / camera_n if camera_n else None,
            "positive_flower_count_rows": flowers_positive,
            "positive_flower_count_fraction": flowers_positive / camera_n if camera_n else None,
            "camera_problem_nonblank_rows": camera_problem_nonblank,
            "duplicate_waypoint_site_plant_date_rows": duplicate_deployment_keys,
            "unique_waypoints": len(waypoint_camera_rows),
            "eligible_waypoint_units": len(waypoint_units),
            "waypoint_inconsistent_site_plant": waypoint_inconsistent_site_plant,
            "camera_rows_per_waypoint_summary": _quantiles(rows_per_waypoint),
            "duration_hours_summary": _quantiles(duration_values),
            "camera_flowers_count_summary": _quantiles(flower_values),
            "top_camera_problem_values": problem_counts.most_common(20),
        },
        "target_bird_observations": {
            "rows": target_n,
            "date_parseable_rows": interaction_date_parseable,
            "date_parseable_fraction": (
                interaction_date_parseable / target_n if target_n else None
            ),
            "site_count": len(site_species_all),
            "species_count": len(
                {str(obs["species"]) for obs in target_obs}
            ),
        },
        "candidate_denominator": {
            "rule": (
                "camera deployment x target bird species observed anywhere in the same "
                "site during the deployment start/end dates"
            ),
            "eligible_camera_deployments": eligible_n,
            "deployments_with_nonempty_temporal_bird_pool": deployment_with_temporal_pool,
            "deployments_with_nonempty_sitewide_bird_pool": deployment_with_site_pool,
            "temporal_pool_size_summary": _quantiles(
                [float(x) for x in temporal_pool_sizes]
            ),
            "sitewide_pool_size_summary": _quantiles(
                [float(x) for x in site_pool_sizes]
            ),
            "potential_dyads_temporal_pool": opportunity_count_temporal,
            "potential_dyads_sitewide_pool": opportunity_count_site,
            "route_eligible_positive_dyads_temporal_pool": route_eligible_positive_temporal,
            "zero_dyads_temporal_pool": zero_opportunities_temporal,
            "trait_matched_potential_dyads_temporal_pool": trait_matched_opportunities_temporal,
            "trait_matched_positive_dyads_temporal_pool": trait_matched_positive_temporal,
            "deployments_with_flower_hours_effort_available": effort_flower_hours_available,
            "flower_hours_effort_fraction_among_eligible": (
                effort_flower_hours_available / eligible_n if eligible_n else None
            ),
        },
        "waypoint_candidate_denominator": {
            "primary_rule_candidate": (
                "unique camera waypoint x target bird species observed in the same "
                "site during any valid camera interval for that waypoint"
            ),
            "eligible_waypoints": len(waypoint_units),
            "temporal_pool_size_summary": _quantiles(
                [float(x) for x in waypoint_pool_sizes]
            ),
            "potential_dyads": waypoint_opportunities,
            "route_eligible_positive_dyads": waypoint_route_positive,
            "zero_dyads": waypoint_zero_opportunities,
            "trait_matched_potential_dyads": waypoint_trait_matched,
            "trait_matched_positive_dyads": waypoint_trait_matched_positive,
            "waypoints_with_complete_flower_hours": waypoint_flower_hours_complete,
            "flower_hours_complete_fraction": (
                waypoint_flower_hours_complete / len(waypoint_units)
                if waypoint_units else None
            ),
            "sampling_hours_offset": "sum positive duration_sampling_hours across camera rows within waypoint",
            "flower_hours_sensitivity": "sum duration_sampling_hours * camera_flowers_count only when all valid camera rows for a waypoint have positive flower count",
        },
        "decision_inputs": {
            "waypoint_temporal_denominator_is_possible": (
                len(waypoint_units) > 0
                and waypoint_opportunities > 0
                and waypoint_zero_opportunities > 0
                and waypoint_trait_matched > waypoint_trait_matched_positive > 0
            ),
            "temporal_denominator_is_possible": (
                eligible_n > 0
                and deployment_with_temporal_pool > 0
                and opportunity_count_temporal > 0
                and zero_opportunities_temporal > 0
            ),
            "hours_offset_is_possible": eligible_n > 0,
            "flower_hours_offset_is_possible": (
                eligible_n > 0
                and effort_flower_hours_available == eligible_n
            ),
            "trait_matched_participation_analysis_is_possible": (
                trait_matched_opportunities_temporal > 0
                and trait_matched_positive_temporal > 0
                and trait_matched_opportunities_temporal
                > trait_matched_positive_temporal
            ),
        },
        "claim_boundary": (
            "This audit constructs no mismatch-participation effect and computes no "
            "association or p-value. It exists only to decide whether a defensible "
            "zero-inclusive participation denominator and effort offset can be frozen. "
            "The waypoint-aggregated denominator is preferred if viable because it "
            "avoids assigning one interaction row to multiple repeated camera deployments."
        ),
    }


def _metadata_rows_for_terms(
    rows: list[dict[str, str]],
    terms: tuple[str, ...],
) -> list[dict[str, str]]:
    out = []
    for row in rows:
        blob = " | ".join(str(value) for value in row.values()).lower()
        if any(term.lower() in blob for term in terms):
            out.append({str(key): str(value) for key, value in row.items()})
    return out


def run(output: str | Path) -> dict[str, object]:
    tables = {key: _read(_download(name)) for key, name in FILES.items()}
    result = audit_denominator(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
    )
    camera_metadata = _read(_download("Metadata EPHI cameras.csv"))
    result["camera_metadata_matches"] = _metadata_rows_for_terms(
        camera_metadata,
        (
            "duration_sampling_hours",
            "camera_flowers_count",
            "camera_problem",
            "duration_from_pics",
        ),
    )
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))
