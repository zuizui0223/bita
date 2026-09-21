"""Equal-network k=3 access-routing test.

This script preserves the original Sakhalkar and Aubert/EPHI permutation
schemes and adds the frozen prospective third-network within-site permutation.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing import (
    _center_within_group,
    _pearson,
    _permute_within_site,
    _rankdata,
    build_public_inputs,
    combine_rhos_equal_network,
)
from scripts.analyze_third_access_routing_network import (
    SEED as THIRD_SEED,
    load_analysis_units,
    validate_confirmatory_gate,
)

SEED = 20260921


def summarize_joint_k3(
    sakhalkar_points: list[dict[str, float | str]],
    aubert_rows: list[dict[str, float | str | bool | int]],
    third_rows: list[dict[str, object]],
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    if permutations <= 0:
        raise ValueError("permutations must be positive")
    gate = validate_confirmatory_gate(third_rows)

    sx = [float(row["tube_length"]) for row in sakhalkar_points]
    sy = [float(row["balance"]) for row in sakhalkar_points]
    ax = [float(row["mismatch_log_t_over_b"]) for row in aubert_rows]
    ay = [float(row["robbery_rate"]) for row in aubert_rows]
    asites = [str(row["site"]) for row in aubert_rows]

    tx = [float(row["M"]) for row in third_rows]
    ty = [float(row["Y"]) for row in third_rows]
    tsites = [str(row["site"]) for row in third_rows]

    sxr, syr = _rankdata(sx), _rankdata(sy)
    axr, ayr = _rankdata(ax), _rankdata(ay)
    txr, tyr = _rankdata(tx), _rankdata(ty)

    r_s = _pearson(sxr, syr)
    axc = _center_within_group(axr, asites)
    ayc = _center_within_group(ayr, asites)
    r_a = _pearson(axc, ayc)
    txc = _center_within_group(txr, tsites)
    tyc = _center_within_group(tyr, tsites)
    r_t = _pearson(txc, tyc)

    if not all(math.isfinite(value) for value in (r_s, r_a, r_t)):
        raise ValueError("all three network effects must be estimable")

    r_j3 = combine_rhos_equal_network([r_s, r_a, r_t])

    rng_s = random.Random(seed)
    rng_a = random.Random(seed + 1)
    rng_t = random.Random(THIRD_SEED)
    s_shuffled = list(syr)
    extreme = 0
    positive_all = 0

    for _ in range(permutations):
        rng_s.shuffle(s_shuffled)

        a_perm = _permute_within_site(ayr, asites, rng=rng_a)
        a_perm_c = _center_within_group(a_perm, asites)

        t_perm = _permute_within_site(tyr, tsites, rng=rng_t)
        t_perm_c = _center_within_group(t_perm, tsites)

        ps = _pearson(sxr, s_shuffled)
        pa = _pearson(axc, a_perm_c)
        pt = _pearson(txc, t_perm_c)
        if not all(math.isfinite(value) for value in (ps, pa, pt)):
            continue

        pj = combine_rhos_equal_network([ps, pa, pt])
        if abs(pj) >= abs(r_j3) - 1e-15:
            extreme += 1
        if ps > 0 and pa > 0 and pt > 0:
            positive_all += 1

    return {
        "analysis_name": "joint_equal_network_access_routing_k3",
        "network_count": 3,
        "network_effects": {
            "sakhalkar_insects": r_s,
            "aubert_ephi_birds": r_a,
            "prospective_mammals": r_t,
        },
        "joint_equal_network_fisher_z_rho": r_j3,
        "joint_permutation_p_two_sided": (extreme + 1) / (permutations + 1),
        "null_probability_all_positive": (positive_all + 1) / (permutations + 1),
        "third_network_gate": gate,
        "permutations": permutations,
        "seed": seed,
        "third_seed": THIRD_SEED,
        "network_direction_concordance": (
            "3_of_3_positive" if r_s > 0 and r_a > 0 and r_t > 0 else "not_3_of_3_positive"
        ),
        "claim_boundary": (
            "Three independent networks receive equal weight; raw observations are "
            "not pooled. k=3 still does not estimate between-network heterogeneity, "
            "a population-level network mean, or universal causality."
        ),
    }


def run(
    third_csv: str | Path,
    output_json: str | Path,
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    sakhalkar_points, aubert_rows = build_public_inputs()
    third_rows = load_analysis_units(third_csv)
    result = summarize_joint_k3(
        sakhalkar_points,
        aubert_rows,
        third_rows,
        permutations=permutations,
        seed=seed,
    )
    path = Path(output_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("third_csv")
    parser.add_argument("output_json")
    parser.add_argument("--permutations", type=int, default=9999)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.third_csv,
                args.output_json,
                permutations=args.permutations,
                seed=args.seed,
            ),
            indent=2,
            sort_keys=True,
        )
    )
