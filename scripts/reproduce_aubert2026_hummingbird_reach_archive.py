"""Reproduce the post-open hummingbird effective-reach sensitivity from archive tables.

The anonymous V5 participation table retains bird_group so this analysis can exclude
Diglossa flowerpiercers without restoring source taxon names.
"""
from __future__ import annotations

import csv
import math
from dataclasses import replace
from pathlib import Path

from scripts.analyze_aubert2026_missingness_dependence_sensitivity import (
    cluster_aggregated_rho_summary,
    cluster_label_swap_summary,
)
from scripts.analyze_aubert2026_participation_route_decomposition import (
    Edge,
    fit_two_way_poisson,
    plant_cluster_jackknife,
)

REACH_MULTIPLIERS = (1.0, 4.0 / 3.0, 1.8, 2.0)
JACKKNIFE_MULTIPLIER = 1.8
SEED = 20261005


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_pair_rows(input_dir: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in _read(input_dir / "aubert_ephi_pair_site_analysis.csv"):
        if row["bird_group"] != "hummingbird":
            continue
        rows.append({
            "plant_species": row["plant_unit"],
            "bird_species": row["bird_unit"],
            "site": row["site_id"],
            "robbery_rate": float(row["robbery_rate"]),
            "mismatch_log_t_over_b": float(row["mismatch_log_t_over_b"]),
            "trait_barrier": row["trait_barrier"].strip().lower() == "true",
        })
    return rows


def _load_participation(input_dir: Path) -> dict[str, list[Edge]]:
    groups: dict[str, list[Edge]] = {"primary": [], "robbing": [], "legitimate": []}
    for row in _read(input_dir / "aubert_ephi_participation_opportunities.csv"):
        if row.get("bird_group", "") != "hummingbird":
            continue
        common = dict(
            waypoint=row["waypoint_unit"],
            bird=row["bird_unit"],
            plant=row["plant_unit"],
            site=row["site_id"],
            barrier=1 if row["trait_barrier"].strip().lower() == "true" else 0,
            mismatch=float(row["mismatch_log_t_over_b"]),
        )
        for key, field in (
            ("primary", "primary_count"),
            ("robbing", "robbing_count"),
            ("legitimate", "legitimate_count"),
        ):
            count = int(row[field])
            groups[key].append(
                Edge(
                    **common,
                    primary_count=count,
                    strict_count=count,
                    broad_count=count,
                )
            )
    return groups


def _shift_pair(rows: list[dict[str, object]], multiplier: float) -> list[dict[str, object]]:
    shift = math.log(multiplier)
    out: list[dict[str, object]] = []
    for row in rows:
        x = float(row["mismatch_log_t_over_b"]) - shift
        updated = dict(row)
        updated["mismatch_log_t_over_b"] = x
        updated["trait_barrier"] = x > 0
        out.append(updated)
    return out


def _shift_edges(edges: list[Edge], multiplier: float) -> list[Edge]:
    shift = math.log(multiplier)
    return [
        replace(edge, mismatch=edge.mismatch - shift, barrier=1 if edge.mismatch - shift > 0 else 0)
        for edge in edges
    ]


def _rr_point(edges: list[Edge]) -> float:
    return float(fit_two_way_poisson(edges, count_field="primary_count")["rate_ratio"])


def _jackknife_summary(edges: list[Edge]) -> dict[str, object]:
    fit = plant_cluster_jackknife(edges, count_field="primary_count")
    return {
        "rr": float(fit["fit"]["rate_ratio"]),
        "ci95": [float(fit["ci95_rate_ratio"][0]), float(fit["ci95_rate_ratio"][1])],
        "plant_clusters": int(fit["plant_clusters"]),
    }


def _route_ratio_jackknife(robbing: list[Edge], legitimate: list[Edge]) -> dict[str, object]:
    plants = sorted({edge.plant for edge in robbing} | {edge.plant for edge in legitimate})
    full_r = fit_two_way_poisson(robbing, count_field="primary_count")
    full_l = fit_two_way_poisson(legitimate, count_field="primary_count")
    beta = float(full_r["beta_log_rate_ratio"]) - float(full_l["beta_log_rate_ratio"])

    leave_one: list[float] = []
    for plant in plants:
        r = [edge for edge in robbing if edge.plant != plant]
        l = [edge for edge in legitimate if edge.plant != plant]
        br = float(fit_two_way_poisson(r, count_field="primary_count")["beta_log_rate_ratio"])
        bl = float(fit_two_way_poisson(l, count_field="primary_count")["beta_log_rate_ratio"])
        leave_one.append(br - bl)

    n = len(leave_one)
    mean = sum(leave_one) / n
    var = (n - 1) / n * sum((value - mean) ** 2 for value in leave_one)
    se = math.sqrt(max(0.0, var))
    z = 1.96
    return {
        "ratio": math.exp(beta),
        "ci95": [math.exp(beta - z * se), math.exp(beta + z * se)],
        "plant_clusters": n,
    }


def reproduce_reach(input_dir: Path, *, permutations: int = 9999) -> dict[str, object]:
    pair_rows = _load_pair_rows(input_dir)
    participation = _load_participation(input_dir)
    if not pair_rows or not participation["primary"]:
        raise ValueError("archive lacks hummingbird-only support for reach sensitivity")

    out: dict[str, object] = {}
    for index, multiplier in enumerate(REACH_MULTIPLIERS):
        pair = _shift_pair(pair_rows, multiplier)
        primary = _shift_edges(participation["primary"], multiplier)
        robbing = _shift_edges(participation["robbing"], multiplier)
        legitimate = _shift_edges(participation["legitimate"], multiplier)

        entry: dict[str, object] = {
            "reach_multiplier": multiplier,
            "plant_rho": cluster_aggregated_rho_summary(
                pair,
                cluster_key="plant_species",
                permutations=permutations,
                seed=SEED + 20 * index,
            ),
            "paired_barrier": cluster_label_swap_summary(
                pair,
                cluster_key="plant_species",
                permutations=permutations,
                seed=SEED + 20 * index + 1,
            ),
            "point_rate_ratios": {
                "pooled": _rr_point(primary),
                "legitimate": _rr_point(legitimate),
                "robbing": _rr_point(robbing),
            },
            "barrier_edges": sum(edge.barrier == 1 for edge in primary),
            "accessible_edges": sum(edge.barrier == 0 for edge in primary),
        }
        if math.isclose(multiplier, JACKKNIFE_MULTIPLIER):
            entry["jackknife"] = {
                "pooled": _jackknife_summary(primary),
                "legitimate": _jackknife_summary(legitimate),
                "robbing": _jackknife_summary(robbing),
                "robbing_over_legitimate": _route_ratio_jackknife(robbing, legitimate),
            }
        out[f"{multiplier:.10g}"] = entry

    return {
        "archive_schema": "BITA_AUBERT_EFFECTIVE_REACH_REPRODUCTION_V1",
        "analysis_timing": "POST_OPEN_MECHANISM_SENSITIVITY",
        "hummingbird_pair_site_rows": len(pair_rows),
        "hummingbird_opportunity_edges": len(participation["primary"]),
        "sensitivities": out,
        "claim_boundary": (
            "Fixed literature-motivated reach multipliers; not measured species-specific tongue lengths. "
            "Production culmen-only results remain historically frozen."
        ),
    }
