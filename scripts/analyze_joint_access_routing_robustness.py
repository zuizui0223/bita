"""Robustness of the joint access-routing effect to sparse Aubert pair-sites."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing import build_public_inputs, summarize_joint

SEED = 20260920


def filter_aubert_by_min_interactions(
    rows: list[dict[str, float | str | bool | int]],
    minimum: int,
) -> list[dict[str, float | str | bool | int]]:
    if minimum < 1:
        raise ValueError("minimum must be >= 1")
    return [row for row in rows if int(row.get("n_interactions", 1)) >= minimum]


def summarize_thresholds(
    sakhalkar_points: list[dict[str, float | str]],
    aubert_rows: list[dict[str, float | str | bool | int]],
    *,
    thresholds: tuple[int, ...] = (1, 2, 5),
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    results: dict[str, object] = {}
    for minimum in thresholds:
        subset = filter_aubert_by_min_interactions(aubert_rows, minimum)
        joint = summarize_joint(
            sakhalkar_points,
            subset,
            permutations=permutations,
            seed=seed,
        )
        aubert = joint["network_effects"]["aubert_ephi"]
        results[f"min_{minimum}"] = {
            "aubert_n_units": aubert["n_units"],
            "aubert_site_count": aubert["site_count"],
            "aubert_site_adjusted_rho": aubert["rho"],
            "aubert_permutation_p_two_sided_within_site": aubert[
                "permutation_p_two_sided_within_site"
            ],
            "sakhalkar_rho": joint["network_effects"]["sakhalkar"]["rho"],
            "joint_equal_network_fisher_z_rho": joint[
                "joint_equal_network_fisher_z_rho"
            ],
            "joint_equal_network_mean_rho": joint["joint_equal_network_mean_rho"],
            "joint_permutation_p_two_sided": joint["joint_permutation_p_two_sided"],
            "network_direction_concordance": joint["network_direction_concordance"],
        }

    return {
        "analysis_name": "joint_access_routing_sparse_pair_robustness",
        "thresholds": results,
        "permutations": permutations,
        "seed": seed,
        "claim_boundary": (
            "Sakhalkar species-level units are unchanged. Only Aubert/EPHI pair-site units "
            "are filtered by minimum resolved interaction count. Networks remain equally "
            "weighted and raw observations are not pooled."
        ),
        "guardrail": "Aggregate output only; no species or site identifiers are emitted.",
    }


def run(
    output: str | Path,
    *,
    permutations: int = 9999,
    seed: int = SEED,
) -> dict[str, object]:
    sakhalkar_points, aubert_rows = build_public_inputs()
    result = summarize_thresholds(
        sakhalkar_points,
        aubert_rows,
        permutations=permutations,
        seed=seed,
    )
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
