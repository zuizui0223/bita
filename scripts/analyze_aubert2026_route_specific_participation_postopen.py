"""Post-open route-specific decomposition of the frozen Ecuador participation model.

This diagnostic is deliberately separate from the frozen first-open participation
estimand. It keeps the same clean-camera opportunity matrix, barrier definition,
waypoint fixed effects, bird fixed effects, and plant-cluster jackknife, but splits
the response into:

- robbing feeding records: primary route status == "yes"
- legitimate/non-robbing feeding records: primary route status == "no"

Because this split was motivated after the aggregate first-open effect was observed,
it is a post-open diagnostic, not a separately preregistered confirmatory test.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import replace
from datetime import date
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_participation_route_decomposition import (
    FILES,
    Edge,
    _as_float,
    _download,
    _read,
    build_opportunity_edges,
    plant_cluster_jackknife,
)
from scripts.audit_aubert2026_participation_denominator import (
    _camera_is_clean,
    _date_in_any_interval,
    _is_target_bird,
    _parse_date,
    _primary_route_status,
)


def _clean_waypoint_intervals(
    cameras: list[dict[str, str]],
) -> dict[str, list[tuple[date, date]]]:
    by_waypoint: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in cameras:
        waypoint = str(row.get("waypoint", "")).strip()
        site = str(row.get("site", "")).strip()
        plant = str(row.get("plant_species", "")).strip()
        start = _parse_date(row.get("start_date"))
        end = _parse_date(row.get("end_date"))
        duration = _as_float(row.get("duration_sampling_hours"))
        if (
            not waypoint
            or not site
            or not plant
            or start is None
            or end is None
            or duration is None
            or duration <= 0
            or not _camera_is_clean(row.get("camera_problem"))
        ):
            continue
        by_waypoint[waypoint].append(
            {
                "site": site,
                "plant": plant,
                "start": start,
                "end": end,
            }
        )

    result: dict[str, list[tuple[date, date]]] = {}
    for waypoint, rows in by_waypoint.items():
        site_plant = {(str(r["site"]), str(r["plant"])) for r in rows}
        if len(site_plant) != 1:
            continue
        intervals = [
            (r["start"], r["end"])
            for r in rows
            if isinstance(r["start"], date) and isinstance(r["end"], date)
        ]
        result[waypoint] = intervals
    return result


def split_route_counts(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
) -> tuple[list[Edge], list[Edge], dict[str, object]]:
    base_edges, base_audit = build_opportunity_edges(
        interactions, cameras, plants, birds
    )
    edge_keys = {(edge.waypoint, edge.bird) for edge in base_edges}
    intervals = _clean_waypoint_intervals(cameras)

    robbery: dict[tuple[str, str], int] = defaultdict(int)
    legitimate: dict[tuple[str, str], int] = defaultdict(int)

    for row in interactions:
        waypoint = str(row.get("waypoint", "")).strip()
        if waypoint not in intervals or not _is_target_bird(row):
            continue
        d = _parse_date(row.get("date"))
        if d is None or not _date_in_any_interval(d, intervals[waypoint]):
            continue

        bird = str(row.get("hummingbird_species", "")).strip()
        key = (waypoint, bird)
        if key not in edge_keys:
            continue

        feeding = str(row.get("feeding_activity", "")).strip().lower()
        if feeding == "no_feeding":
            continue

        route = _primary_route_status(row.get("piercing"))
        if route == "yes":
            robbery[key] += 1
        elif route == "no":
            legitimate[key] += 1

    robbery_edges: list[Edge] = []
    legitimate_edges: list[Edge] = []
    mismatches = 0
    for edge in base_edges:
        key = (edge.waypoint, edge.bird)
        r = robbery[key]
        l = legitimate[key]
        if edge.primary_count != r + l:
            mismatches += 1
        robbery_edges.append(
            replace(
                edge,
                primary_count=r,
                strict_count=r,
                broad_count=r,
            )
        )
        legitimate_edges.append(
            replace(
                edge,
                primary_count=l,
                strict_count=l,
                broad_count=l,
            )
        )

    if mismatches:
        raise ValueError(
            f"route-specific counts do not reconstruct primary_count for {mismatches} edges"
        )

    audit = {
        **base_audit,
        "route_specific_reconstruction_mismatches": mismatches,
        "robbing_interaction_records": sum(edge.primary_count for edge in robbery_edges),
        "legitimate_interaction_records": sum(
            edge.primary_count for edge in legitimate_edges
        ),
        "robbing_positive_edges": sum(
            edge.primary_count > 0 for edge in robbery_edges
        ),
        "legitimate_positive_edges": sum(
            edge.primary_count > 0 for edge in legitimate_edges
        ),
    }
    return robbery_edges, legitimate_edges, audit


def _direction(fit: dict[str, object]) -> str:
    lo, hi = [float(x) for x in fit["ci95_rate_ratio"]]
    if lo > 1.0:
        return "INCREASED_UNDER_BARRIER"
    if hi < 1.0:
        return "DECREASED_UNDER_BARRIER"
    return "UNRESOLVED_AROUND_ONE"


def analyze_tables(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
) -> dict[str, object]:
    robbery_edges, legitimate_edges, audit = split_route_counts(
        interactions, cameras, plants, birds
    )

    robbery_fit = plant_cluster_jackknife(
        robbery_edges,
        count_field="primary_count",
    )
    legitimate_fit = plant_cluster_jackknife(
        legitimate_edges,
        count_field="primary_count",
    )

    return {
        "analysis_name": "aubert_ephi_route_specific_participation_postopen",
        "status": "FIT",
        "analysis_timing": "POST_OPEN_DIAGNOSTIC",
        "audit": audit,
        "robbing": {
            **robbery_fit,
            "direction": _direction(robbery_fit),
        },
        "legitimate_nonrobbing": {
            **legitimate_fit,
            "direction": _direction(legitimate_fit),
        },
        "model": {
            "formula": (
                "log(mu_waypoint,bird) = alpha_waypoint + gamma_bird "
                "+ beta * I[tube > culmen]"
            ),
            "robbing_response": (
                "feeding records with primary route status yes"
            ),
            "legitimate_response": (
                "feeding records with primary route status no, including the "
                "source-metadata missing-piercing-as-legitimate rule"
            ),
            "estimand": (
                "exp(beta) barrier/access route-specific feeding rate ratio"
            ),
            "uncertainty": "delete-one-plant-species jackknife",
        },
        "claim_boundary": (
            "Post-open observational decomposition motivated by the aggregate "
            "first-open participation result. It does not convert either route-specific "
            "association into a causal floral-geometry effect. Waypoint fixed "
            "effects absorb time-invariant waypoint/plant reward main effects; "
            "bird-specific reward responses and within-deployment temporal reward "
            "variation remain possible confounding."
        ),
    }


def run(output: str | Path) -> dict[str, object]:
    tables = {key: _read(_download(name)) for key, name in FILES.items()}
    result = analyze_tables(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
    )
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))
