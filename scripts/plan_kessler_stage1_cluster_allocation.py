"""Translate Kessler Stage-1 effective sample sizes into plant/block budgets.

The original prospective planner reports flower-level observations under a
scalar design-effect assumption. This companion sensitivity makes the cluster
assumption explicit using the exchangeable approximation

    design effect = 1 + (m - 1) * ICC

where ``m`` is introduced flowers per plant and ICC is the within-plant
intraclass correlation. It then converts effective n/cell to introduced
flowers, plants/cell, and—if one plant from each A x D cell forms a matched
block—the corresponding matched-block count.

This is a planning sensitivity, not a mixed-model power calculation. It is
intended to prevent flower counts from being mistaken for independent plants.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from scripts.plan_kessler_type_replication import (
    DEFAULT_SCENARIOS,
    additive_delta,
    balanced_effective_n_per_cell,
)


DEFAULT_CLUSTER_SIZES = (3, 5, 8, 10)
DEFAULT_ICCS = (0.05, 0.10, 0.20)
DEFAULT_POWERS = (0.80, 0.90)


def exchangeable_design_effect(cluster_size: int, icc: float) -> float:
    if cluster_size < 1:
        raise ValueError("cluster_size must be >= 1")
    if not 0.0 <= icc < 1.0:
        raise ValueError("icc must lie in [0, 1)")
    return 1.0 + (cluster_size - 1) * icc


def cluster_allocation(
    effective_n_per_cell: int,
    *,
    flowers_per_plant: int,
    icc: float,
    retention: float = 0.90,
) -> dict[str, object]:
    if effective_n_per_cell < 1:
        raise ValueError("effective_n_per_cell must be >= 1")
    if not 0.0 < retention <= 1.0:
        raise ValueError("retention must lie in (0, 1]")
    deff = exchangeable_design_effect(flowers_per_plant, icc)
    required_flowers = math.ceil(effective_n_per_cell * deff / retention)
    plants_per_cell = math.ceil(required_flowers / flowers_per_plant)
    introduced_flowers_per_cell = plants_per_cell * flowers_per_plant
    return {
        "flowers_per_plant": flowers_per_plant,
        "icc": icc,
        "design_effect": round(deff, 6),
        "required_flowers_per_cell_before_plant_rounding": required_flowers,
        "plants_per_cell": plants_per_cell,
        "introduced_flowers_per_cell_after_plant_rounding": introduced_flowers_per_cell,
        "total_plants_four_cells": 4 * plants_per_cell,
        "total_introduced_flowers_four_cells": 4 * introduced_flowers_per_cell,
        "matched_blocks_if_one_plant_per_cell_per_block": plants_per_cell,
    }


def build_cluster_plan(
    *,
    retention: float = 0.90,
    cluster_sizes=DEFAULT_CLUSTER_SIZES,
    iccs=DEFAULT_ICCS,
    powers=DEFAULT_POWERS,
) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for scenario in DEFAULT_SCENARIOS[:2]:
        delta = additive_delta(
            scenario["p11"], scenario["p10"], scenario["p01"], scenario["p00"]
        )
        for power in powers:
            effective = balanced_effective_n_per_cell(
                p11=scenario["p11"],
                p10=scenario["p10"],
                p01=scenario["p01"],
                p00=scenario["p00"],
                power=power,
            )
            for flowers_per_plant in cluster_sizes:
                for icc in iccs:
                    allocation = cluster_allocation(
                        effective,
                        flowers_per_plant=flowers_per_plant,
                        icc=icc,
                        retention=retention,
                    )
                    rows.append(
                        {
                            "scenario": scenario["name"],
                            "delta_ad": round(delta, 6),
                            "power": power,
                            "effective_n_per_cell": effective,
                            "retention": retention,
                            **allocation,
                        }
                    )
    return {
        "analysis_id": "kessler_stage1_cluster_allocation_v1",
        "design_effect_formula": "1 + (flowers_per_plant - 1) * ICC",
        "rows": rows,
        "claim_boundary": (
            "This exchangeable-ICC grid is a prospective cluster sensitivity, not a hierarchical or randomization-based power guarantee. "
            "It assumes the declared flowers-per-plant and ICC summarize within-plant dependence and does not add extra day/site correlation. "
            "The final Stage-1 analysis must use the realized matched-block/plant structure rather than treating flower counts as independent."
        ),
    }


def render_markdown(plan: dict[str, object]) -> str:
    lines = [
        "# Kessler Stage-1 plant/cluster allocation sensitivity v1",
        "",
        "Exchangeable planning approximation: `DE = 1 + (m - 1) * ICC`.",
        "",
        "| scenario | power | flowers/plant | ICC | DE | plants/cell | total plants | total introduced flowers |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in plan["rows"]:
        lines.append(
            f"| {row['scenario']} | {row['power']:.2f} | {row['flowers_per_plant']} | "
            f"{row['icc']:.2f} | {row['design_effect']:.2f} | {row['plants_per_cell']} | "
            f"{row['total_plants_four_cells']} | {row['total_introduced_flowers_four_cells']} |"
        )
    lines += ["", "## Boundary", "", str(plan["claim_boundary"]), ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("out_md", type=Path)
    parser.add_argument("--retention", type=float, default=0.90)
    args = parser.parse_args(argv)
    plan = build_cluster_plan(retention=args.retention)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    args.out_md.write_text(render_markdown(plan), encoding="utf-8")
    print(json.dumps({"analysis_id": plan["analysis_id"], "rows": len(plan["rows"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
