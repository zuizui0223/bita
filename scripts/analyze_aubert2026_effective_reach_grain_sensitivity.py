"""Post-open hummingbird effective-reach and grain sensitivity for Aubert/EPHI.

This analysis is frozen in
AUBERT2026_EFFECTIVE_REACH_GRAIN_SENSITIVITY_FREEZE_V1.md before real results are
opened. It does not replace the culmen-based primary analyses.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from dataclasses import replace
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_missingness_dependence_sensitivity import (
    build_pair_site_rows_policy,
    cluster_label_swap_summary,
)
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
from scripts.analyze_joint_access_routing_species_robust import (
    aggregate_aubert_by_plant,
)
from trait_architecture.numerics import spearman

ROOT = Path(__file__).resolve().parents[1]
FIRST_OPEN_THRESHOLD = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "results"
    / "aubert2026_routing_threshold_first_open.json"
)
SEED = 20261005
PERMUTATIONS = 9999
REACH_MULTIPLIERS = (1.0, 4.0 / 3.0, 2.0)
PROXIMITY_MARGIN = math.log(1.25)


def _hummingbird_species(
    interactions: list[dict[str, str]],
) -> set[str]:
    return {
        str(row.get("hummingbird_species", "")).strip()
        for row in interactions
        if str(row.get("hummingbird_family", "")).strip() == "Trochilidae"
        and str(row.get("hummingbird_species", "")).strip()
    }


def _reparameterize_edge(edge: Edge, multiplier: float) -> Edge:
    if multiplier <= 0:
        raise ValueError("reach multiplier must be positive")
    mismatch = float(edge.mismatch) - math.log(multiplier)
    return replace(
        edge,
        mismatch=mismatch,
        barrier=1 if mismatch > 0 else 0,
    )


def _reparameterize_rows(
    rows: list[dict[str, object]],
    multiplier: float,
) -> list[dict[str, object]]:
    if multiplier <= 0:
        raise ValueError("reach multiplier must be positive")
    shift = math.log(multiplier)
    out: list[dict[str, object]] = []
    for row in rows:
        if str(row.get("bird_group", "")) != "hummingbird":
            continue
        updated = dict(row)
        mismatch = float(row["mismatch_log_t_over_b"]) - shift
        updated["mismatch_log_t_over_b"] = mismatch
        updated["trait_barrier"] = mismatch > 0
        out.append(updated)
    return out


def _direction(fit: dict[str, object]) -> str:
    lo, hi = [float(x) for x in fit["ci95_rate_ratio"]]
    if lo > 1.0:
        return "INCREASED_UNDER_BARRIER"
    if hi < 1.0:
        return "DECREASED_UNDER_BARRIER"
    return "UNRESOLVED_AROUND_ONE"


def _fit_or_error(edges: list[Edge]) -> dict[str, object]:
    try:
        fit = plant_cluster_jackknife(edges, count_field="primary_count")
        return {
            "status": "FIT",
            "rate_ratio": float(fit["fit"]["rate_ratio"]),
            "ci95_rate_ratio": [float(x) for x in fit["ci95_rate_ratio"]],
            "ci90_rate_ratio": [float(x) for x in fit["ci90_rate_ratio"]],
            "plant_clusters": int(fit["plant_clusters"]),
            "supported_edges": int(fit["fit"]["supported_edges"]),
            "supported_waypoints": int(fit["fit"]["supported_waypoints"]),
            "supported_birds": int(fit["fit"]["supported_birds"]),
            "direction": _direction(fit),
        }
    except ValueError as exc:
        return {"status": "NOT_IDENTIFIED", "reason": str(exc)}


def _spearman_permutation(
    x: list[float],
    y: list[float],
    *,
    permutations: int,
    seed: int,
) -> dict[str, float | int]:
    observed = spearman(x, y)
    rng = random.Random(seed)
    shuffled = list(y)
    extreme = 0
    for _ in range(permutations):
        rng.shuffle(shuffled)
        value = spearman(x, shuffled)
        if abs(value) >= abs(observed) - 1e-15:
            extreme += 1
    return {
        "rho": observed,
        "permutation_p_two_sided": (extreme + 1) / (permutations + 1),
        "permutations": permutations,
    }


def translate_threshold(
    threshold: dict[str, object],
    multiplier: float,
) -> dict[str, object]:
    """Translate a fixed-multiplier mismatch coordinate exactly."""
    shift = math.log(multiplier)
    primary = threshold["primary_sigmoid"]
    bootstrap = threshold["bootstrap"]
    ci = [float(x) - shift for x in bootstrap["ci90_xstar"]]
    xstar = float(primary["xstar"]) - shift
    low = float(primary["x_search_low"]) - shift
    high = float(primary["x_search_high"]) - shift
    return {
        "reach_multiplier": multiplier,
        "log_shift": shift,
        "translated_xstar": xstar,
        "translated_x_search_low": low,
        "translated_x_search_high": high,
        "translated_ci90_xstar": ci,
        "xstar_at_same_upper_support_boundary": math.isclose(
            xstar, high, rel_tol=0.0, abs_tol=1e-12
        ),
        "effective_reach_ratio_at_xstar": math.exp(xstar),
        "ci90_within_original_equality_margin": (
            ci[0] >= -PROXIMITY_MARGIN and ci[1] <= PROXIMITY_MARGIN
        ),
        "classification_invariant_under_translation": (
            threshold["threshold_classification"]
        ),
        "note": (
            "A constant reach multiplier is a coordinate translation only; it "
            "cannot move the fitted midpoint off the same support boundary."
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

    pooled_all, pooled_audit = build_opportunity_edges(
        interactions, cameras, plants, birds
    )
    robbing_all, legitimate_all, route_audit = split_route_counts(
        interactions, cameras, plants, birds
    )

    pooled_hb = [edge for edge in pooled_all if edge.bird in hb_species]
    robbing_hb = [edge for edge in robbing_all if edge.bird in hb_species]
    legitimate_hb = [edge for edge in legitimate_all if edge.bird in hb_species]

    pair_rows_all, pair_audit = build_pair_site_rows_policy(
        interactions,
        cameras,
        plants,
        birds,
        missing_as_no=True,
    )

    threshold = json.loads(FIRST_OPEN_THRESHOLD.read_text(encoding="utf-8"))
    multiplier_results: dict[str, object] = {}

    for idx, multiplier in enumerate(REACH_MULTIPLIERS):
        pooled = [_reparameterize_edge(edge, multiplier) for edge in pooled_hb]
        robbing = [_reparameterize_edge(edge, multiplier) for edge in robbing_hb]
        legitimate = [
            _reparameterize_edge(edge, multiplier) for edge in legitimate_hb
        ]
        pair_rows = _reparameterize_rows(pair_rows_all, multiplier)
        plant_points = aggregate_aubert_by_plant(pair_rows)

        p1_continuous = _spearman_permutation(
            [float(row["mismatch"]) for row in plant_points],
            [float(row["robbery_rate"]) for row in plant_points],
            permutations=permutations,
            seed=seed + idx,
        )
        p1_binary = cluster_label_swap_summary(
            pair_rows,
            cluster_key="plant_species",
            permutations=permutations,
            seed=seed + 100 + idx,
        )

        multiplier_results[f"{multiplier:.12g}"] = {
            "reach_multiplier": multiplier,
            "barrier_definition": f"tube > {multiplier:.12g} * culmen",
            "opportunity_edges": len(pooled),
            "barrier_edges": sum(edge.barrier == 1 for edge in pooled),
            "accessible_edges": sum(edge.barrier == 0 for edge in pooled),
            "barrier_fraction": (
                sum(edge.barrier == 1 for edge in pooled) / len(pooled)
                if pooled
                else None
            ),
            "bird_species": len({edge.bird for edge in pooled}),
            "plant_species": len({edge.plant for edge in pooled}),
            "waypoints": len({edge.waypoint for edge in pooled}),
            "p2_zero_inclusive": {
                "pooled_resolved_feeding": _fit_or_error(pooled),
                "legitimate_nonrobbing": _fit_or_error(legitimate),
                "robbing_only": _fit_or_error(robbing),
            },
            "p1_hummingbird_only": {
                "plant_species": len(plant_points),
                "continuous_mismatch_robbery": p1_continuous,
                "paired_binary_barrier": p1_binary,
            },
            "threshold_coordinate_translation": translate_threshold(
                threshold, multiplier
            ),
        }

    rhos = [
        float(
            multiplier_results[key]["p1_hummingbird_only"][
                "continuous_mismatch_robbery"
            ]["rho"]
        )
        for key in multiplier_results
    ]
    if max(rhos) - min(rhos) > 1e-12:
        raise ValueError(
            "constant-multiplier continuous Spearman changed unexpectedly"
        )

    return {
        "analysis_name": "aubert_ephi_effective_reach_grain_sensitivity",
        "analysis_timing": "POST_OPEN_SENSITIVITY",
        "status": "FIT",
        "reach_multipliers": list(REACH_MULTIPLIERS),
        "taxonomic_scope": (
            "Trochilidae only for reach sensitivity; Diglossa excluded because "
            "a hummingbird tongue multiplier is not biologically transferable."
        ),
        "literature_basis": {
            "4_over_3": (
                "Vizentin-Bugoni, Maruyama & Sazima 2014, Proc R Soc B, "
                "doi:10.1098/rspb.2013.2397; pragmatic correction when "
                "species-specific tongue lengths were unavailable."
            ),
            "2": (
                "Grant & Temeles 1992, PNAS, doi:10.1073/pnas.89.20.9400; "
                "Selasphorus rufus maximum tongue extension approximately one "
                "bill length, used here only as a maximum-reach stress test."
            ),
        },
        "grain_statement": {
            "p1": (
                "Plant-level and within-bird routing comparisons vary the flower "
                "encountered by a bird and estimate route composition."
            ),
            "p2": (
                "Waypoint fixed effects hold one plant/tube context fixed; the "
                "barrier varies through bird bill length and estimates feeding "
                "participation among locally available birds relative to bird "
                "baseline. It is not the same estimand as P1."
            ),
        },
        "base_audits": {
            "pooled": pooled_audit,
            "route_specific": route_audit,
            "pair_site": pair_audit,
            "hummingbird_species_in_interactions": len(hb_species),
            "hummingbird_only_opportunity_edges": len(pooled_hb),
        },
        "multipliers": multiplier_results,
        "claim_boundary": (
            "Post-open observational sensitivity. Fixed multipliers are not "
            "species-specific tongue allometries and cannot establish a causal "
            "access threshold. The original culmen-based results remain primary."
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
