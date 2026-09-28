"""Species-level robust cross-network access-routing analysis.

This revision addresses two inferential problems in the original Aubert/EPHI
extension:

- EPHI metadata says unspecified piercing values are most probably legitimate
  interactions ("no"), because some observers filled the field only for
  piercing events. The Aubert input is therefore rebuilt with explicit
  missing codes treated as legitimate while retaining exclusion of distinct
  states such as maybe, thief, and not_interacting.
- Repeated bird x plant x site rows are not treated as independent for the
  cross-network test. Aubert/EPHI is collapsed to one unweighted point per
  plant species before rank inference, matching the plant-species unit already
  used by Sakhalkar.

The output is aggregate-only and does not emit source species identifiers.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_missingness_dependence_sensitivity import (
    build_pair_site_rows_policy,
    cluster_label_swap_summary,
)
from scripts.analyze_aubert2026_zenodo_extension import (
    FILES as AUBERT_FILES,
    _download as _download_aubert,
    _mean,
    _read as _read_aubert,
)
from scripts.analyze_joint_access_routing import combine_rhos_equal_network
from scripts.analyze_sakhalkar2023_network import (
    _find_workbook,
    _pearson,
    _rankdata,
    species_route_points,
)
from scripts.audit_sakhalkar2023_zenodo import (
    _download as _download_sakhalkar,
    read_xlsx_sheet_rows,
)

SEED = 20260927


def aggregate_aubert_by_plant(
    rows: list[dict[str, object]],
) -> list[dict[str, float]]:
    by_plant: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_plant[str(row["plant_species"])].append(row)

    out: list[dict[str, float]] = []
    for plant_rows in by_plant.values():
        out.append(
            {
                "mismatch": _mean(
                    [float(row["mismatch_log_t_over_b"]) for row in plant_rows]
                ),
                "robbery_rate": _mean(
                    [float(row["robbery_rate"]) for row in plant_rows]
                ),
                "pair_site_n": float(len(plant_rows)),
            }
        )
    return out


def summarize_joint_species(
    sakhalkar_points: list[dict[str, float | str]],
    aubert_plant_points: list[dict[str, float]],
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    if len(sakhalkar_points) < 3:
        raise ValueError("too few Sakhalkar plant-species points")
    if len(aubert_plant_points) < 3:
        raise ValueError("too few Aubert plant-species points")
    if permutations <= 0:
        raise ValueError("permutations must be positive")

    sx = [float(row["tube_length"]) for row in sakhalkar_points]
    sy = [float(row["balance"]) for row in sakhalkar_points]
    ax = [float(row["mismatch"]) for row in aubert_plant_points]
    ay = [float(row["robbery_rate"]) for row in aubert_plant_points]

    sx_rank = _rankdata(sx)
    sy_rank = _rankdata(sy)
    ax_rank = _rankdata(ax)
    ay_rank = _rankdata(ay)

    s_rho = _pearson(sx_rank, sy_rank)
    a_rho = _pearson(ax_rank, ay_rank)
    if not math.isfinite(s_rho) or not math.isfinite(a_rho):
        raise ValueError("network correlations must be finite")

    joint = combine_rhos_equal_network([s_rho, a_rho])

    rng_s = random.Random(seed)
    rng_a = random.Random(seed + 1)
    shuffled_s = list(sy_rank)
    shuffled_a = list(ay_rank)

    s_extreme = 0
    a_extreme = 0
    joint_extreme = 0
    positive_both = 0

    for _ in range(permutations):
        rng_s.shuffle(shuffled_s)
        rng_a.shuffle(shuffled_a)
        ps = _pearson(sx_rank, shuffled_s)
        pa = _pearson(ax_rank, shuffled_a)
        pj = combine_rhos_equal_network([ps, pa])

        if abs(ps) >= abs(s_rho) - 1e-15:
            s_extreme += 1
        if abs(pa) >= abs(a_rho) - 1e-15:
            a_extreme += 1
        if abs(pj) >= abs(joint) - 1e-15:
            joint_extreme += 1
        if ps > 0 and pa > 0:
            positive_both += 1

    return {
        "analysis_name": "joint_equal_network_access_routing_species_robust",
        "network_count": 2,
        "network_effects": {
            "sakhalkar": {
                "n_units": len(sakhalkar_points),
                "unit": "plant_species",
                "rho": s_rho,
                "permutation_p_two_sided": (s_extreme + 1) / (permutations + 1),
            },
            "aubert_ephi": {
                "n_units": len(aubert_plant_points),
                "unit": "plant_species",
                "missingness_policy": "explicit missing piercing codes recoded as legitimate/no",
                "aggregation": "unweighted mean mismatch and robbery rate across pair-site rows within plant species",
                "rho": a_rho,
                "permutation_p_two_sided": (a_extreme + 1) / (permutations + 1),
            },
        },
        "joint_equal_network_fisher_z_rho": joint,
        "joint_permutation_p_two_sided": (joint_extreme + 1) / (permutations + 1),
        "null_probability_both_positive": (positive_both + 1) / (permutations + 1),
        "network_direction_concordance": "2_of_2_positive",
        "sakhalkar_permutation_scheme": "across_plant_species",
        "aubert_permutation_scheme": "across_plant_species_after_within_species_aggregation",
        "permutations": permutations,
        "seed": seed,
        "claim_boundary": (
            "Each network contributes one plant-species-level rank association. "
            "Aubert/EPHI missing piercing values are treated as legitimate interactions "
            "according to the source metadata. This removes pair-site pseudo-replication "
            "from the joint test but remains observational and does not establish a causal "
            "effect of floral geometry."
        ),
    }


def build_public_inputs() -> tuple[
    list[dict[str, float | str]],
    list[dict[str, object]],
    dict[str, object],
]:
    workbook = _find_workbook(_download_sakhalkar())
    visits = read_xlsx_sheet_rows(workbook, "cheater_data")
    traits = read_xlsx_sheet_rows(workbook, "plant_traits")
    sakh = species_route_points(visits, traits)

    tables = {
        key: _read_aubert(_download_aubert(name))
        for key, name in AUBERT_FILES.items()
    }
    aubert_rows, audit = build_pair_site_rows_policy(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
        missing_as_no=True,
    )
    return sakh, aubert_rows, audit


def run(
    output: str | Path,
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    sakh, aubert_rows, audit = build_public_inputs()
    plant_points = aggregate_aubert_by_plant(aubert_rows)
    result = summarize_joint_species(
        sakh,
        plant_points,
        permutations=permutations,
        seed=seed,
    )
    result["aubert_input_audit"] = audit
    result["aubert_binary_barrier_plant_species_check"] = cluster_label_swap_summary(
        aubert_rows,
        cluster_key="plant_species",
        permutations=permutations,
        seed=seed + 10,
    )
    result["guardrail"] = "Aggregate output only; source species identifiers are not emitted."

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--permutations", type=int, default=9999)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(json.dumps(run(args.output, permutations=args.permutations, seed=args.seed), indent=2, sort_keys=True))
