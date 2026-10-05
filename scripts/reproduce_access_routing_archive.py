"""Reproduce Letter statistics from the DOI-archive analysis tables only."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import math
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_missingness_dependence_sensitivity import (
    bird_within_species_continuous_summary,
    cluster_aggregated_rho_summary,
    cluster_label_swap_summary,
)
from scripts.analyze_aubert2026_zenodo_extension import summarize_pair_sites
from scripts.analyze_aubert2026_participation_route_decomposition import (
    Edge,
    classify_participation,
    fit_two_way_poisson,
    plant_cluster_jackknife,
)
from scripts.analyze_aubert2026_routing_threshold import (
    BOOTSTRAPS as THRESHOLD_BOOTSTRAPS,
    PERMUTATIONS as THRESHOLD_PERMUTATIONS,
    SEED as THRESHOLD_SEED,
    analyze_points as analyze_threshold_points,
)
from scripts.audit_aubert2026_threshold_bootstrap_boundary import boundary_stickiness
from scripts.analyze_joint_access_routing_species_robust import (
    aggregate_aubert_by_plant,
    summarize_joint_species,
)
from scripts.analyze_sakhalkar2023_network import _permutation_p, _spearman
from scripts.analyze_sakhalkar2023_trait_routing import fit_source_model_set
from scripts.reproduce_aubert2026_hummingbird_reach_archive import reproduce_reach

SAKHALKAR_SEED = 20260919
JOINT_SEED = 20260927


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _optional_float(value: str) -> float | None:
    text = str(value).strip()
    if text == "":
        return None
    number = float(text)
    if not math.isfinite(number):
        raise ValueError(f"non-finite archive value: {value!r}")
    return number


def load_sakhalkar(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in _read_csv(path):
        rows.append({
            "route_balance": float(row["route_balance"]),
            "tube_length": _optional_float(row["tube_length"]),
            "tube_width": _optional_float(row["tube_width"]),
            "brightness": _optional_float(row["brightness"]),
            "shape": row["shape"],
        })
    return rows


def load_aubert(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in _read_csv(path):
        rows.append({
            "site": row["site_id"],
            "plant_species": row["plant_unit"],
            "bird_species": row["bird_unit"],
            "bird_group": row["bird_group"],
            "n_interactions": int(row["n_interactions"]),
            "robbery_rate": float(row["robbery_rate"]),
            "mismatch_log_t_over_b": float(row["mismatch_log_t_over_b"]),
            "trait_barrier": row["trait_barrier"].strip().lower() == "true",
        })
    return rows



def load_aubert_participation(path: Path) -> dict[str, list[Edge]]:
    primary: list[Edge] = []
    robbing: list[Edge] = []
    legitimate: list[Edge] = []
    for row in _read_csv(path):
        common = {
            "waypoint": row["waypoint_unit"],
            "bird": row["bird_unit"],
            "plant": row["plant_unit"],
            "site": row["site_id"],
            "barrier": 1 if row["trait_barrier"].strip().lower() == "true" else 0,
            "mismatch": float(row["mismatch_log_t_over_b"]),
        }
        primary_count = int(row["primary_count"])
        robbing_count = int(row["robbing_count"])
        legitimate_count = int(row["legitimate_count"])
        if robbing_count + legitimate_count != primary_count:
            raise ValueError(
                "archive route-specific counts do not reconstruct primary_count "
                f"for {row['analysis_unit']}"
            )
        primary.append(
            Edge(
                **common,
                primary_count=primary_count,
                strict_count=int(row["strict_count"]),
                broad_count=int(row["broad_count"]),
            )
        )
        robbing.append(
            Edge(
                **common,
                primary_count=robbing_count,
                strict_count=robbing_count,
                broad_count=robbing_count,
            )
        )
        legitimate.append(
            Edge(
                **common,
                primary_count=legitimate_count,
                strict_count=legitimate_count,
                broad_count=legitimate_count,
            )
        )
    return {
        "primary": primary,
        "robbing": robbing,
        "legitimate": legitimate,
    }


def _route_direction(result: dict[str, object]) -> str:
    lo, hi = [float(value) for value in result["ci95_rate_ratio"]]
    if lo > 1.0:
        return "INCREASED_UNDER_BARRIER"
    if hi < 1.0:
        return "DECREASED_UNDER_BARRIER"
    return "UNRESOLVED_AROUND_ONE"

def reproduce(input_dir: Path, *, permutations: int = 9999) -> dict[str, object]:
    sakh_rows = load_sakhalkar(input_dir / "sakhalkar_species_analysis.csv")
    aubert_rows = load_aubert(input_dir / "aubert_ephi_pair_site_analysis.csv")
    participation = load_aubert_participation(
        input_dir / "aubert_ephi_participation_opportunities.csv"
    )
    participation_edges = participation["primary"]

    sx = [float(row["tube_length"]) for row in sakh_rows if row["tube_length"] is not None]
    sy = [float(row["route_balance"]) for row in sakh_rows if row["tube_length"] is not None]
    s_rho = _spearman(sx, sy)
    s_p = _permutation_p(
        sx,
        sy,
        s_rho,
        permutations,
        seed=SAKHALKAR_SEED,
    )

    sakh_points = [
        {
            "tube_length": float(row["tube_length"]),
            "balance": float(row["route_balance"]),
        }
        for row in sakh_rows
        if row["tube_length"] is not None
    ]

    aubert_plant_points = aggregate_aubert_by_plant(aubert_rows)

    participation_primary = plant_cluster_jackknife(
        participation_edges,
        count_field="primary_count",
    )
    participation_decision = classify_participation(participation_primary)
    participation_strict = fit_two_way_poisson(
        participation_edges,
        count_field="strict_count",
    )
    participation_broad = fit_two_way_poisson(
        participation_edges,
        count_field="broad_count",
    )
    route_robbing = plant_cluster_jackknife(
        participation["robbing"],
        count_field="primary_count",
    )
    route_legitimate = plant_cluster_jackknife(
        participation["legitimate"],
        count_field="primary_count",
    )

    threshold = analyze_threshold_points(
        aubert_plant_points,
        bootstraps=THRESHOLD_BOOTSTRAPS,
        permutations=THRESHOLD_PERMUTATIONS,
        seed=THRESHOLD_SEED,
    )
    threshold_x = [float(row["mismatch"]) for row in aubert_plant_points]
    threshold_y = [float(row["robbery_rate"]) for row in aubert_plant_points]
    threshold_boundary = boundary_stickiness(
        threshold_x,
        threshold_y,
        threshold["primary_sigmoid"],
        replicates=THRESHOLD_BOOTSTRAPS,
        seed=THRESHOLD_SEED,
    )

    return {
        "archive_schema": "BITA_ACCESS_ROUTING_LETTER_ARCHIVE_REPRODUCTION_V5",
        "sakhalkar": {
            "n_species": len(sakh_points),
            "spearman_rho": s_rho,
            "permutation_p_two_sided": s_p,
            "multitrait": fit_source_model_set(
                sakh_rows,
                permutations=permutations,
                seed=SAKHALKAR_SEED,
            ),
        },
        "aubert_ephi": {
            "pair_site_descriptive": summarize_pair_sites(
                aubert_rows,
                permutations=permutations,
                seed=20261919,
            ),
            "plant_species_rho_check": cluster_aggregated_rho_summary(
                aubert_rows,
                cluster_key="plant_species",
                permutations=permutations,
                seed=20261919 + 350,
            ),
            "plant_species_cluster_check": cluster_label_swap_summary(
                aubert_rows,
                cluster_key="plant_species",
                permutations=permutations,
                seed=20261919 + 300,
            ),
            "bird_species_rho_check": cluster_aggregated_rho_summary(
                aubert_rows,
                cluster_key="bird_species",
                permutations=permutations,
                seed=20261919 + 450,
            ),
            "bird_species_cluster_check": cluster_label_swap_summary(
                aubert_rows,
                cluster_key="bird_species",
                permutations=permutations,
                seed=20261919 + 400,
            ),
            "bird_within_species_continuous_check": bird_within_species_continuous_summary(
                aubert_rows,
                permutations=permutations,
                seed=20261919 + 500,
            ),
        },
        "joint": summarize_joint_species(
            sakh_points,
            aubert_plant_points,
            permutations=permutations,
            seed=JOINT_SEED,
        ),
        "aubert_ephi_participation": {
            "opportunity_edges": len(participation_edges),
            "positive_edges": sum(edge.primary_count > 0 for edge in participation_edges),
            "zero_edges": sum(edge.primary_count == 0 for edge in participation_edges),
            "primary_participation": participation_primary,
            "decision": participation_decision,
            "sensitivities": {
                "strict_feeding_rate_ratio": participation_strict["rate_ratio"],
                "broad_feeding_rate_ratio": participation_broad["rate_ratio"],
            },
            "postopen_route_specific": {
                "analysis_timing": "POST_OPEN_DIAGNOSTIC",
                "robbing": {
                    **route_robbing,
                    "direction": _route_direction(route_robbing),
                },
                "legitimate_nonrobbing": {
                    **route_legitimate,
                    "direction": _route_direction(route_legitimate),
                },
            },
        },
        "aubert_ephi_threshold": {
            "first_open_reproduction": threshold,
            "postopen_boundary_audit": threshold_boundary,
        },
        "aubert_ephi_effective_reach_sensitivity": reproduce_reach(
            input_dir,
            permutations=permutations,
            full_jackknife=False,
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--permutations", type=int, default=9999)
    args = parser.parse_args()

    result = reproduce(args.input_dir, permutations=args.permutations)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
