"""Post-open hummingbird effective-reach sensitivity for Aubert/EPHI.

This analysis is frozen in
empirical/floral_defence_selectivity/HUMMINGBIRD_EFFECTIVE_REACH_SENSITIVITY_FREEZE_V1.md
before the real output is opened.

It does not replace the production culmen-only mismatch.  It restricts the public
EPHI analysis to true hummingbirds (Trochilidae; excludes Diglossa flowerpiercers)
and reclassifies the binary access barrier under fixed literature-motivated reach
multipliers.

A fixed multiplier translates log mismatch by -log(k), so plant-level rank
correlations are expected to be invariant apart from the explicit removal of
flowerpiercers.  The informative sensitivity is the binary barrier decomposition.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_participation_route_decomposition import (
    FILES,
    Edge,
    _download,
    _read,
    build_opportunity_edges,
    plant_cluster_jackknife,
)
from scripts.analyze_aubert2026_route_specific_participation_postopen import (
    split_route_counts,
)
from scripts.analyze_aubert2026_missingness_dependence_sensitivity import (
    build_pair_site_rows_policy,
    cluster_aggregated_rho_summary,
    cluster_label_swap_summary,
)

ROOT = Path(__file__).resolve().parents[1]
THRESHOLD_RESULT = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "results"
    / "aubert2026_routing_threshold_first_open.json"
)
SEED = 20261005
PERMUTATIONS = 9999
REACH_MULTIPLIERS = (1.0, 4.0 / 3.0, 1.8, 2.0)
PROXIMITY_MARGIN = math.log(1.25)


def _hummingbird_species(interactions: list[dict[str, str]]) -> set[str]:
    out: set[str] = set()
    for row in interactions:
        family = str(row.get("hummingbird_family", "")).strip()
        genus = str(row.get("hummingbird_genus", "")).strip()
        species = str(row.get("hummingbird_species", "")).strip()
        if species and family == "Trochilidae" and genus != "Diglossa":
            out.add(species)
    return out


def _shift_pair_rows(
    rows: list[dict[str, object]],
    multiplier: float,
) -> list[dict[str, object]]:
    shift = math.log(multiplier)
    out: list[dict[str, object]] = []
    for row in rows:
        mismatch = float(row["mismatch_log_t_over_b"]) - shift
        updated = dict(row)
        updated["mismatch_log_t_over_b"] = mismatch
        updated["trait_barrier"] = mismatch > 0.0
        out.append(updated)
    return out


def _shift_edges(edges: list[Edge], multiplier: float) -> list[Edge]:
    shift = math.log(multiplier)
    return [
        replace(
            edge,
            mismatch=edge.mismatch - shift,
            barrier=1 if edge.mismatch - shift > 0.0 else 0,
        )
        for edge in edges
    ]


def _safe_jackknife(edges: list[Edge]) -> dict[str, object]:
    try:
        fit = plant_cluster_jackknife(edges, count_field="primary_count")
    except ValueError as exc:
        return {"status": "NOT_FIT", "reason": str(exc)}
    return {
        "status": "FIT",
        "rate_ratio": float(fit["fit"]["rate_ratio"]),
        "ci95_rate_ratio": [
            float(fit["ci95_rate_ratio"][0]),
            float(fit["ci95_rate_ratio"][1]),
        ],
        "plant_clusters": int(fit["plant_clusters"]),
        "supported_edges": int(fit["fit"]["supported_edges"]),
        "supported_waypoints": int(fit["fit"]["supported_waypoints"]),
        "supported_birds": int(fit["fit"]["supported_birds"]),
    }


def _descriptive_pair_barrier(rows: list[dict[str, object]]) -> dict[str, object]:
    barrier = [float(r["robbery_rate"]) for r in rows if bool(r["trait_barrier"])]
    accessible = [float(r["robbery_rate"]) for r in rows if not bool(r["trait_barrier"])]
    return {
        "barrier_pair_sites": len(barrier),
        "accessible_pair_sites": len(accessible),
        "mean_robbery_rate_barrier": (
            sum(barrier) / len(barrier) if barrier else None
        ),
        "mean_robbery_rate_accessible": (
            sum(accessible) / len(accessible) if accessible else None
        ),
    }


def _translated_threshold(multiplier: float) -> dict[str, object]:
    frozen = json.loads(THRESHOLD_RESULT.read_text(encoding="utf-8"))
    fit = frozen["primary_sigmoid"]
    shift = math.log(multiplier)
    xstar = float(fit["xstar"]) - shift
    low = float(fit["x_search_low"]) - shift
    high = float(fit["x_search_high"]) - shift
    ci = frozen["bootstrap"]["ci90_xstar"]
    ci_shifted = [float(ci[0]) - shift, float(ci[1]) - shift]
    return {
        "multiplier": multiplier,
        "translated_xstar": xstar,
        "translated_search_low": low,
        "translated_search_high": high,
        "translated_ci90_xstar": ci_shifted,
        "effective_reach_ratio_at_midpoint": math.exp(xstar),
        "point_midpoint_within_plusminus_log_1_25": abs(xstar) <= PROXIMITY_MARGIN,
        "distance_above_positive_proximity_margin": xstar - PROXIMITY_MARGIN,
        "boundary_classification_preserved": frozen["threshold_classification"],
        "reason": (
            "constant reach scaling translates all mismatch values, midpoint, "
            "bootstrap interval and search support by the same -log(k)"
        ),
    }


def analyze_tables(
    interactions: list[dict[str, str]],
    cameras: list[dict[str, str]],
    plants: list[dict[str, str]],
    birds: list[dict[str, str]],
    *,
    permutations: int = PERMUTATIONS,
    seed: int = SEED,
) -> dict[str, object]:
    hb_species = _hummingbird_species(interactions)

    pair_rows, pair_audit = build_pair_site_rows_policy(
        interactions,
        cameras,
        plants,
        birds,
        missing_as_no=True,
    )
    hb_pair_rows = [
        row
        for row in pair_rows
        if str(row.get("bird_group", "")) == "hummingbird"
        and str(row.get("bird_species", "")) in hb_species
    ]

    pooled_edges, pooled_audit = build_opportunity_edges(
        interactions, cameras, plants, birds
    )
    robbery_edges, legitimate_edges, route_audit = split_route_counts(
        interactions, cameras, plants, birds
    )

    pooled_hb = [edge for edge in pooled_edges if edge.bird in hb_species]
    robbery_hb = [edge for edge in robbery_edges if edge.bird in hb_species]
    legitimate_hb = [edge for edge in legitimate_edges if edge.bird in hb_species]

    if not (
        len(pooled_hb) == len(robbery_hb) == len(legitimate_hb)
    ):
        raise ValueError("hummingbird edge sets do not align")

    sensitivities: dict[str, object] = {}
    for idx, multiplier in enumerate(REACH_MULTIPLIERS):
        shifted_rows = _shift_pair_rows(hb_pair_rows, multiplier)
        shifted_pooled = _shift_edges(pooled_hb, multiplier)
        shifted_robbery = _shift_edges(robbery_hb, multiplier)
        shifted_legitimate = _shift_edges(legitimate_hb, multiplier)

        pooled_fit = _safe_jackknife(shifted_pooled)
        robbery_fit = _safe_jackknife(shifted_robbery)
        legitimate_fit = _safe_jackknife(shifted_legitimate)

        rr_ratio = None
        if (
            robbery_fit.get("status") == "FIT"
            and legitimate_fit.get("status") == "FIT"
        ):
            rr_ratio = (
                float(robbery_fit["rate_ratio"])
                / float(legitimate_fit["rate_ratio"])
            )

        sensitivities[f"{multiplier:.10g}"] = {
            "reach_multiplier": multiplier,
            "mismatch_shift_minus_log_k": -math.log(multiplier),
            "plant_route_composition": {
                "rho": cluster_aggregated_rho_summary(
                    shifted_rows,
                    cluster_key="plant_species",
                    permutations=permutations,
                    seed=seed + 10 * idx,
                ),
                "paired_barrier_contrast": cluster_label_swap_summary(
                    shifted_rows,
                    cluster_key="plant_species",
                    permutations=permutations,
                    seed=seed + 10 * idx + 1,
                ),
                "pair_site_descriptive": _descriptive_pair_barrier(shifted_rows),
            },
            "zero_inclusive_participation": {
                "pooled_resolved_feeding": pooled_fit,
                "legitimate_nonrobbing": legitimate_fit,
                "robbing": robbery_fit,
                "robbing_rr_over_legitimate_rr": rr_ratio,
                "barrier_edges": sum(edge.barrier == 1 for edge in shifted_pooled),
                "accessible_edges": sum(edge.barrier == 0 for edge in shifted_pooled),
            },
            "threshold_translation": _translated_threshold(multiplier),
        }

    return {
        "analysis_name": "aubert_ephi_hummingbird_effective_reach_sensitivity",
        "status": "FIT",
        "analysis_timing": "POST_OPEN_MECHANISM_SENSITIVITY",
        "freeze": (
            "empirical/floral_defence_selectivity/"
            "HUMMINGBIRD_EFFECTIVE_REACH_SENSITIVITY_FREEZE_V1.md"
        ),
        "reach_multipliers": list(REACH_MULTIPLIERS),
        "hummingbird_only": {
            "species": len(hb_species),
            "pair_site_rows": len(hb_pair_rows),
            "opportunity_edges": len(pooled_hb),
            "plants_pair_site": len({str(r["plant_species"]) for r in hb_pair_rows}),
            "plants_opportunity": len({e.plant for e in pooled_hb}),
        },
        "excluded_flowerpiercer_pair_site_rows": (
            len(pair_rows) - len(hb_pair_rows)
        ),
        "pair_input_audit": pair_audit,
        "pooled_opportunity_audit": pooled_audit,
        "route_split_audit": route_audit,
        "sensitivities": sensitivities,
        "claim_boundary": (
            "Post-open sensitivity. Fixed reach multipliers are literature-motivated "
            "barrier reclassifications, not measured species-specific tongue lengths. "
            "They do not replace the production culmen-only estimand and cannot create "
            "new threshold localization because they translate log mismatch uniformly."
        ),
    }


def run(
    output: str | Path,
    *,
    permutations: int = PERMUTATIONS,
    seed: int = SEED,
) -> dict[str, object]:
    tables = {key: _read(_download(name)) for key, name in FILES.items()}
    result = analyze_tables(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
        permutations=permutations,
        seed=seed,
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
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.output, permutations=args.permutations, seed=args.seed),
            indent=2,
            sort_keys=True,
        )
    )
