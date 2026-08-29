"""Prospective sample-size planner for a Kessler-type 2x2 reproductive assay.

The primary design target is a two-sided 95% interval for the additive
probability-scale interaction Delta_AD that lies above zero with predeclared
power. This is a planning calculation, not a recovered uncertainty estimate
for Kessler et al. (2008).

Because the historical day/plant dependence is unavailable, clustering is
handled only through an explicit design-effect multiplier. Mechanism-channel
three- and four-way interactions are NOT declared powered by this calculation.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import NormalDist


DEFAULT_SCENARIOS = (
    {"name": "published_central", "p11": 0.35, "p10": 0.13, "p01": 0.13, "p00": 0.13},
    {"name": "attenuated_delta_0_17", "p11": 0.30, "p10": 0.13, "p01": 0.13, "p00": 0.13},
    {"name": "attenuated_delta_0_12", "p11": 0.25, "p10": 0.13, "p01": 0.13, "p00": 0.13},
)
DEFAULT_POWERS = (0.80, 0.90)
DEFAULT_DESIGN_EFFECTS = (1.0, 1.5, 2.0)


def additive_delta(p11: float, p10: float, p01: float, p00: float) -> float:
    return p11 - p10 - p01 + p00


def variance_numerator(p11: float, p10: float, p01: float, p00: float) -> float:
    return sum(p * (1.0 - p) for p in (p11, p10, p01, p00))


def balanced_effective_n_per_cell(
    *,
    p11: float,
    p10: float,
    p01: float,
    p00: float,
    power: float,
    alpha_two_sided: float = 0.05,
) -> int:
    """Normal-approximation effective n/cell for additive difference-in-differences."""
    probabilities = (p11, p10, p01, p00)
    if any(not 0.0 < p < 1.0 for p in probabilities):
        raise ValueError("planning probabilities must lie strictly between 0 and 1")
    if not 0.0 < power < 1.0:
        raise ValueError("power must lie strictly between 0 and 1")
    if not 0.0 < alpha_two_sided < 1.0:
        raise ValueError("alpha_two_sided must lie strictly between 0 and 1")
    delta = additive_delta(*probabilities)
    if delta <= 0:
        raise ValueError("the positive-escape planning scenario must have Delta_AD > 0")
    z_alpha = NormalDist().inv_cdf(1.0 - alpha_two_sided / 2.0)
    z_power = NormalDist().inv_cdf(power)
    n = ((z_alpha + z_power) ** 2) * variance_numerator(*probabilities) / (delta**2)
    return math.ceil(n)


def planned_observations_per_cell(effective_n: int, *, design_effect: float, retention: float) -> int:
    if design_effect < 1.0:
        raise ValueError("design_effect must be >= 1")
    if not 0.0 < retention <= 1.0:
        raise ValueError("retention must lie in (0, 1]")
    return math.ceil(effective_n * design_effect / retention)


def build_plan(
    *,
    scenarios=DEFAULT_SCENARIOS,
    powers=DEFAULT_POWERS,
    design_effects=DEFAULT_DESIGN_EFFECTS,
    retention: float = 0.90,
    alpha_two_sided: float = 0.05,
) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        delta = additive_delta(scenario["p11"], scenario["p10"], scenario["p01"], scenario["p00"])
        for power in powers:
            effective = balanced_effective_n_per_cell(
                p11=scenario["p11"],
                p10=scenario["p10"],
                p01=scenario["p01"],
                p00=scenario["p00"],
                power=power,
                alpha_two_sided=alpha_two_sided,
            )
            for design_effect in design_effects:
                planned = planned_observations_per_cell(
                    effective,
                    design_effect=design_effect,
                    retention=retention,
                )
                rows.append(
                    {
                        "scenario": scenario["name"],
                        "delta_ad": round(delta, 6),
                        "power": power,
                        "alpha_two_sided": alpha_two_sided,
                        "effective_n_per_trait_cell": effective,
                        "design_effect": design_effect,
                        "retention": retention,
                        "planned_observations_per_cell": planned,
                        "planned_total_four_cell_trait_factorial": 4 * planned,
                        "budget_if_same_n_in_all_16_cells": 16 * planned,
                    }
                )
    return {
        "analysis_id": "kessler_type_replication_power_v1",
        "primary_estimand": "additive_probability_scale_Delta_AD",
        "decision_target": "two-sided_95pct_interval_wholly_above_zero",
        "rows": rows,
        "claim_boundary": (
            "The four-cell calculation powers only the total additive A x D interaction under the declared probabilities. "
            "The 16-cell total is a budgeting extrapolation, not a power guarantee for A x D x antagonist, A x D x pollinator, "
            "or the four-way separability diagnostic. Those mechanism contrasts require their own effect-size assumptions or pilot data."
        ),
    }


def render_markdown(plan: dict[str, object]) -> str:
    lines = [
        "# Kessler-type replication power plan v1",
        "",
        "Primary target: a two-sided 95% interval for the additive probability-scale `Delta_AD` that lies wholly above zero.",
        "",
        "| scenario | power | design effect | effective n/cell | planned n/cell | 4-cell total | 16-cell budget |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in plan["rows"]:
        lines.append(
            f"| {row['scenario']} | {row['power']:.2f} | {row['design_effect']:.1f} | "
            f"{row['effective_n_per_trait_cell']} | {row['planned_observations_per_cell']} | "
            f"{row['planned_total_four_cell_trait_factorial']} | {row['budget_if_same_n_in_all_16_cells']} |"
        )
    lines += ["", "## Boundary", "", str(plan["claim_boundary"]), ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("out_md", type=Path)
    parser.add_argument("--retention", type=float, default=0.90)
    args = parser.parse_args(argv)
    plan = build_plan(retention=args.retention)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    args.out_md.write_text(render_markdown(plan), encoding="utf-8")
    print(json.dumps({"rows": len(plan["rows"]), "analysis_id": plan["analysis_id"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
