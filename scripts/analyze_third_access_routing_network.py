"""Prospective third-network access-routing analysis.

This module implements the frozen non-Insecta/non-Aves confirmatory estimand.
It is deliberately fail-closed on the preregistered sample-composition gates.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from trait_architecture.numerics import pearson, rankdata

SEED = 20260921
MIN_UNITS = 30
MIN_VISITOR_SPECIES = 5
MIN_PLANT_SPECIES = 5


def _center_within_site(values: list[float], sites: list[str]) -> list[float]:
    if len(values) != len(sites):
        raise ValueError("values and sites must have equal length")
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for value, site in zip(values, sites):
        sums[site] += value
        counts[site] += 1
    means = {site: sums[site] / counts[site] for site in sums}
    return [value - means[site] for value, site in zip(values, sites)]


def _permute_within_site(
    values: list[float],
    sites: list[str],
    *,
    rng: random.Random,
) -> list[float]:
    by_site: dict[str, list[int]] = defaultdict(list)
    for index, site in enumerate(sites):
        by_site[site].append(index)
    out = list(values)
    for indices in by_site.values():
        local = [values[index] for index in indices]
        rng.shuffle(local)
        for index, value in zip(indices, local):
            out[index] = value
    return out


def load_analysis_units(path: str | Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "site_id",
            "plant_species",
            "mammal_species",
            "M_log_ratio",
            "B_count",
            "L_count",
        }
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")
        for raw in reader:
            m = float(raw["M_log_ratio"])
            b = int(raw["B_count"])
            l = int(raw["L_count"])
            if not math.isfinite(m):
                raise ValueError("M_log_ratio must be finite")
            if b < 0 or l < 0:
                raise ValueError("route counts must be non-negative")
            if b + l <= 0:
                raise ValueError(
                    "every inferential unit must contain at least one legitimate or bypass event"
                )
            rows.append(
                {
                    "site": str(raw["site_id"]).strip(),
                    "plant": str(raw["plant_species"]).strip(),
                    "visitor": str(raw["mammal_species"]).strip(),
                    "M": m,
                    "B": b,
                    "L": l,
                    "Y": b / (b + l),
                }
            )
    return rows


def validate_confirmatory_gate(rows: list[dict[str, object]]) -> dict[str, int]:
    n_units = len(rows)
    visitors = {str(row["visitor"]) for row in rows}
    plants = {str(row["plant"]) for row in rows}
    sites = {str(row["site"]) for row in rows}
    total_b = sum(int(row["B"]) for row in rows)
    total_l = sum(int(row["L"]) for row in rows)
    m_values = {float(row["M"]) for row in rows}
    y_values = {float(row["Y"]) for row in rows}

    failures: list[str] = []
    if n_units < MIN_UNITS:
        failures.append(f"n_units<{MIN_UNITS}")
    if len(visitors) < MIN_VISITOR_SPECIES:
        failures.append(f"n_visitor_species<{MIN_VISITOR_SPECIES}")
    if len(plants) < MIN_PLANT_SPECIES:
        failures.append(f"n_plant_species<{MIN_PLANT_SPECIES}")
    if len(m_values) < 2:
        failures.append("no_M_variation")
    if total_b <= 0:
        failures.append("no_bypass_events")
    if total_l <= 0:
        failures.append("no_legitimate_events")
    if len(y_values) < 2:
        failures.append("no_Y_variation")

    if failures:
        raise ValueError(
            "INELIGIBLE_CONFIRMATORY_DATASET: " + ",".join(failures)
        )

    return {
        "n_units": n_units,
        "n_visitor_species": len(visitors),
        "n_plant_species": len(plants),
        "n_sites": len(sites),
        "total_bypass_events": total_b,
        "total_legitimate_events": total_l,
    }


def effect_components(
    rows: list[dict[str, object]],
) -> tuple[float, list[float], list[float], list[str]]:
    validate_confirmatory_gate(rows)
    m = [float(row["M"]) for row in rows]
    y = [float(row["Y"]) for row in rows]
    sites = [str(row["site"]) for row in rows]

    m_rank = rankdata(m)
    y_rank = rankdata(y)
    m_centered = _center_within_site(m_rank, sites)
    y_centered = _center_within_site(y_rank, sites)
    r_t = pearson(
        m_centered,
        y_centered,
        mean_method="fmean",
        denominator_method="joint",
        zero_variance="nan",
    )
    if not math.isfinite(r_t):
        raise ValueError("third-network site-adjusted rank effect is not estimable")
    return r_t, m_centered, y_rank, sites


def summarize_third_network(
    rows: list[dict[str, object]],
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    if permutations <= 0:
        raise ValueError("permutations must be positive")
    gate = validate_confirmatory_gate(rows)
    r_t, m_centered, y_rank, sites = effect_components(rows)

    rng = random.Random(seed)
    extreme = 0
    for _ in range(permutations):
        perm_y = _permute_within_site(y_rank, sites, rng=rng)
        perm_y_centered = _center_within_site(perm_y, sites)
        value = pearson(
            m_centered,
            perm_y_centered,
            mean_method="fmean",
            denominator_method="joint",
            zero_variance="nan",
        )
        if math.isfinite(value) and abs(value) >= abs(r_t) - 1e-15:
            extreme += 1

    return {
        "analysis_name": "prospective_third_access_routing_network",
        "status": "CONFIRMATORY_GATE_PASS",
        "effect": {
            "rho_site_adjusted_rank": r_t,
            "permutation_p_two_sided": (extreme + 1) / (permutations + 1),
            "permutations": permutations,
            "seed": seed,
        },
        "gate": gate,
        "planning_target_units": 70,
        "access_constraint": "M_log_ratio = log(P_j_mm / V_i_mm)",
        "bypass_response": "Y = B_count / (B_count + L_count)",
        "stratum": "site_id",
        "claim_boundary": (
            "Prospective third-fauna rank association only. Passing this gate does "
            "not establish universal causality or a population-level mean across networks."
        ),
    }


def run(
    input_csv: str | Path,
    output_json: str | Path,
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    rows = load_analysis_units(input_csv)
    result = summarize_third_network(rows, permutations=permutations, seed=seed)
    path = Path(output_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_json")
    parser.add_argument("--permutations", type=int, default=9999)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.input_csv,
                args.output_json,
                permutations=args.permutations,
                seed=args.seed,
            ),
            indent=2,
            sort_keys=True,
        )
    )
