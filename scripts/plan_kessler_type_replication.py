"""Prospective sample-size planner for a Kessler-type 2x2 reproductive assay.

Two distinct planning targets are kept separate.

Level 1 powers a two-sided 95% interval for the additive probability-scale
interaction Delta_AD that lies above zero.

Levels 2/3 require the Stage-1 attraction contrasts

    A0 = p10 - p00   (attraction effect when defence is low)
    A1 = p11 - p01   (attraction effect when defence is high)

and the registered sufficient interval rule

    upper95(A0) <= 0 and lower95(A1) > 0     [Level 2]
    upper95(A0) <  0 and lower95(A1) > 0     [Level 3].

Under a continuous normal planning approximation Level 2 and Level 3 have the
same decision probability because an estimated interval endpoint has zero
probability of landing exactly on zero.  Crucially, if the true A0 is exactly
zero, increasing sample size cannot make the strict zero-bound rule highly
powerful: the asymptotic probability that a two-sided 95% interval has its
upper endpoint at or below zero is alpha/2 = 0.025.  A positive practical
margin epsilon would define a different, prospectively justified claim and is
therefore not inserted post hoc here.

These are planning calculations, not recovered uncertainty estimates for
Kessler et al. (2008).  Historical day/plant dependence is unavailable, so
clustering is represented only by an explicit design-effect multiplier.
Mechanism-channel three- and four-way interactions are NOT declared powered by
this calculation.
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

# These are prospective sensitivity scenarios, not claims about the historical
# Kessler source.  They expose how strongly negative A0 must be before the
# strict Level-2/3 zero-bound decision becomes realistically powerable.
DEFAULT_RELEASE_SCENARIOS = (
    {"name": "boundary_A0_zero", "p11": 0.35, "p10": 0.13, "p01": 0.13, "p00": 0.13},
    {"name": "weak_negative_A0_minus_0_03", "p11": 0.35, "p10": 0.10, "p01": 0.13, "p00": 0.13},
    {"name": "moderate_negative_A0_minus_0_05", "p11": 0.35, "p10": 0.08, "p01": 0.13, "p00": 0.13},
)

DEFAULT_POWERS = (0.80, 0.90)
DEFAULT_DESIGN_EFFECTS = (1.0, 1.5, 2.0)


def additive_delta(p11: float, p10: float, p01: float, p00: float) -> float:
    return p11 - p10 - p01 + p00


def stage1_contrasts(p11: float, p10: float, p01: float, p00: float) -> tuple[float, float, float]:
    a0 = p10 - p00
    a1 = p11 - p01
    return a0, a1, a1 - a0


def variance_numerator(p11: float, p10: float, p01: float, p00: float) -> float:
    return sum(p * (1.0 - p) for p in (p11, p10, p01, p00))


def contrast_variance_numerator(p_high: float, p_low: float) -> float:
    return p_high * (1.0 - p_high) + p_low * (1.0 - p_low)


def _validate_probabilities(*probabilities: float) -> None:
    if any(not 0.0 < p < 1.0 for p in probabilities):
        raise ValueError("planning probabilities must lie strictly between 0 and 1")


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
    _validate_probabilities(*probabilities)
    if not 0.0 < power < 1.0:
        raise ValueError("power must lie strictly between 0 and 1")
    if not 0.0 < alpha_two_sided < 1.0:
        raise ValueError("alpha_two_sided must lie strictly between 0 and 1")
    delta = additive_delta(*probabilities)
    if delta <= 0:
        raise ValueError("the positive-interaction planning scenario must have Delta_AD > 0")
    z_alpha = NormalDist().inv_cdf(1.0 - alpha_two_sided / 2.0)
    z_power = NormalDist().inv_cdf(power)
    n = ((z_alpha + z_power) ** 2) * variance_numerator(*probabilities) / (delta**2)
    return math.ceil(n)


def level23_component_decision_probabilities(
    effective_n_per_cell: int,
    *,
    p11: float,
    p10: float,
    p01: float,
    p00: float,
    alpha_two_sided: float = 0.05,
    a0_upper_margin: float = 0.0,
) -> tuple[float, float, float]:
    """Approximate P[upper(A0)<=margin], P[lower(A1)>0], and their product.

    A0 and A1 use disjoint cells in a balanced four-cell design, so under the
    independent effective-sample planning approximation their estimators are
    independent and the joint decision probability is the product.

    ``a0_upper_margin`` defaults to the strict zero boundary.  A positive value
    represents a different practical/noninferiority claim and must be justified
    prospectively; the canonical planner does not use a positive margin.
    """
    _validate_probabilities(p11, p10, p01, p00)
    if effective_n_per_cell <= 1:
        raise ValueError("effective_n_per_cell must be > 1")
    if not 0.0 < alpha_two_sided < 1.0:
        raise ValueError("alpha_two_sided must lie strictly between 0 and 1")

    a0, a1, _ = stage1_contrasts(p11, p10, p01, p00)
    se0 = math.sqrt(contrast_variance_numerator(p10, p00) / effective_n_per_cell)
    se1 = math.sqrt(contrast_variance_numerator(p11, p01) / effective_n_per_cell)
    zcrit = NormalDist().inv_cdf(1.0 - alpha_two_sided / 2.0)

    p_a0_upper_below_margin = NormalDist().cdf((a0_upper_margin - a0) / se0 - zcrit)
    p_a1_lower_above_zero = NormalDist().cdf(a1 / se1 - zcrit)
    joint = p_a0_upper_below_margin * p_a1_lower_above_zero
    return p_a0_upper_below_margin, p_a1_lower_above_zero, joint


def asymptotic_level23_decision_probability(
    *,
    p11: float,
    p10: float,
    p01: float,
    p00: float,
    alpha_two_sided: float = 0.05,
    a0_upper_margin: float = 0.0,
) -> float:
    """Asymptotic upper limit of the registered Level-2/3 interval decision."""
    _validate_probabilities(p11, p10, p01, p00)
    a0, a1, _ = stage1_contrasts(p11, p10, p01, p00)
    tol = 1e-12

    if a0 < a0_upper_margin - tol:
        p0 = 1.0
    elif abs(a0 - a0_upper_margin) <= tol:
        p0 = alpha_two_sided / 2.0
    else:
        p0 = 0.0

    if a1 > tol:
        p1 = 1.0
    elif abs(a1) <= tol:
        p1 = alpha_two_sided / 2.0
    else:
        p1 = 0.0
    return p0 * p1


def balanced_effective_n_per_cell_level23(
    *,
    p11: float,
    p10: float,
    p01: float,
    p00: float,
    power: float,
    alpha_two_sided: float = 0.05,
    a0_upper_margin: float = 0.0,
    max_n_per_cell: int = 10_000_000,
) -> int | None:
    """Minimum effective n/cell for the joint Level-2/3 interval decision.

    Returns ``None`` when the target power exceeds the asymptotic decision
    probability under the declared true cell probabilities.  This is the
    expected result for the historical central scenario with true A0=0 and an
    80% or 90% target under a strict zero-bound 95% CI rule.
    """
    if not 0.0 < power < 1.0:
        raise ValueError("power must lie strictly between 0 and 1")
    asymptotic = asymptotic_level23_decision_probability(
        p11=p11,
        p10=p10,
        p01=p01,
        p00=p00,
        alpha_two_sided=alpha_two_sided,
        a0_upper_margin=a0_upper_margin,
    )
    if power > asymptotic + 1e-12:
        return None

    def joint_at(n: int) -> float:
        return level23_component_decision_probabilities(
            n,
            p11=p11,
            p10=p10,
            p01=p01,
            p00=p00,
            alpha_two_sided=alpha_two_sided,
            a0_upper_margin=a0_upper_margin,
        )[2]

    hi = 2
    while hi <= max_n_per_cell and joint_at(hi) < power:
        hi *= 2
    if hi > max_n_per_cell:
        return None

    lo = 2
    while lo < hi:
        mid = (lo + hi) // 2
        if joint_at(mid) >= power:
            hi = mid
        else:
            lo = mid + 1
    return lo


def planned_observations_per_cell(effective_n: int, *, design_effect: float, retention: float) -> int:
    if design_effect < 1.0:
        raise ValueError("design_effect must be >= 1")
    if not 0.0 < retention <= 1.0:
        raise ValueError("retention must lie in (0, 1]")
    return math.ceil(effective_n * design_effect / retention)


def build_plan(
    *,
    scenarios=DEFAULT_SCENARIOS,
    release_scenarios=DEFAULT_RELEASE_SCENARIOS,
    powers=DEFAULT_POWERS,
    design_effects=DEFAULT_DESIGN_EFFECTS,
    retention: float = 0.90,
    alpha_two_sided: float = 0.05,
) -> dict[str, object]:
    level1_rows: list[dict[str, object]] = []
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
                level1_rows.append(
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

    level23_rows: list[dict[str, object]] = []
    for scenario in release_scenarios:
        p11 = scenario["p11"]
        p10 = scenario["p10"]
        p01 = scenario["p01"]
        p00 = scenario["p00"]
        a0, a1, delta = stage1_contrasts(p11, p10, p01, p00)
        asymptotic = asymptotic_level23_decision_probability(
            p11=p11,
            p10=p10,
            p01=p01,
            p00=p00,
            alpha_two_sided=alpha_two_sided,
        )
        for power in powers:
            effective = balanced_effective_n_per_cell_level23(
                p11=p11,
                p10=p10,
                p01=p01,
                p00=p00,
                power=power,
                alpha_two_sided=alpha_two_sided,
            )
            for design_effect in design_effects:
                if effective is None:
                    planned = None
                    total = None
                    status = "TARGET_POWER_NOT_ATTAINABLE_UNDER_STRICT_ZERO_CI_RULE"
                    p0 = None
                    p1 = None
                    joint = None
                else:
                    planned = planned_observations_per_cell(
                        effective,
                        design_effect=design_effect,
                        retention=retention,
                    )
                    total = 4 * planned
                    p0, p1, joint = level23_component_decision_probabilities(
                        effective,
                        p11=p11,
                        p10=p10,
                        p01=p01,
                        p00=p00,
                        alpha_two_sided=alpha_two_sided,
                    )
                    status = "POWERABLE_UNDER_DECLARED_NORMAL_APPROXIMATION"
                level23_rows.append(
                    {
                        "scenario": scenario["name"],
                        "a0": round(a0, 6),
                        "a1": round(a1, 6),
                        "delta_ad": round(delta, 6),
                        "target_joint_power": power,
                        "alpha_two_sided": alpha_two_sided,
                        "a0_upper_margin": 0.0,
                        "asymptotic_max_joint_decision_probability": asymptotic,
                        "effective_n_per_trait_cell": effective,
                        "component_probability_A0_upper_at_or_below_zero": p0,
                        "component_probability_A1_lower_above_zero": p1,
                        "joint_decision_probability_at_effective_n": joint,
                        "design_effect": design_effect,
                        "retention": retention,
                        "planned_observations_per_cell": planned,
                        "planned_total_four_cell_trait_factorial": total,
                        "status": status,
                    }
                )

    return {
        "analysis_id": "kessler_type_replication_power_v2",
        "level1_target": {
            "estimand": "additive_probability_scale_Delta_AD",
            "decision": "two-sided_95pct_interval_wholly_above_zero",
        },
        "level23_target": {
            "estimands": "A0_and_A1",
            "decision": "upper95_A0_at_or_below_zero_AND_lower95_A1_above_zero",
            "strict_zero_margin": 0.0,
            "note": (
                "Under the continuous normal approximation the Level-2 <=0 and Level-3 <0 interval rules "
                "have the same decision probability. If true A0=0, the asymptotic maximum probability "
                "of satisfying the A0 upper-bound rule is alpha/2, so conventional 80/90% power is unattainable."
            ),
        },
        # Keep the historical key name for backwards-compatible consumers.
        "rows": level1_rows,
        "level23_rows": level23_rows,
        "claim_boundary": (
            "The Level-1 four-cell calculation powers only the total additive A x D interaction under the declared probabilities. "
            "The Level-2/3 calculation separately evaluates the joint A0/A1 interval decision and can correctly return an unattainable "
            "target at the A0=0 boundary. A positive A0 margin would define a different prospectively justified practical-release claim "
            "and is not selected from the historical data. The 16-cell total remains a budgeting extrapolation, not a power guarantee for "
            "A x D x antagonist, A x D x pollinator, or the four-way separability diagnostic. Mechanism contrasts require their own effect-size "
            "assumptions or pilot data."
        ),
    }


def render_markdown(plan: dict[str, object]) -> str:
    lines = [
        "# Kessler-type replication power plan v2",
        "",
        "## Level 1 — total interaction",
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

    lines += [
        "",
        "## Levels 2/3 — A0/A1 decision",
        "",
        "Registered sufficient rule: `upper95(A0) <= 0` and `lower95(A1) > 0`. Under a continuous normal planning approximation the Level-2 `<=0` and Level-3 `<0` versions have the same decision probability.",
        "",
        "| scenario | A0 | A1 | target joint power | design effect | effective n/cell | planned n/cell | 4-cell total | asymptotic max joint P | status |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in plan["level23_rows"]:
        effective = "NA" if row["effective_n_per_trait_cell"] is None else str(row["effective_n_per_trait_cell"])
        planned = "NA" if row["planned_observations_per_cell"] is None else str(row["planned_observations_per_cell"])
        total = "NA" if row["planned_total_four_cell_trait_factorial"] is None else str(row["planned_total_four_cell_trait_factorial"])
        lines.append(
            f"| {row['scenario']} | {row['a0']:+.3f} | {row['a1']:+.3f} | {row['target_joint_power']:.2f} | "
            f"{row['design_effect']:.1f} | {effective} | {planned} | {total} | "
            f"{row['asymptotic_max_joint_decision_probability']:.3f} | {row['status']} |"
        )

    lines += [
        "",
        "### Boundary result",
        "",
        "For the historical central planning state `A0=0`, no increase in sample size can deliver 80% or 90% probability that a two-sided 95% interval has `upper(A0) <= 0`. Its asymptotic maximum is `alpha/2 = 0.025` when `A1>0`. Strict Level-2/3 confirmation is therefore a different and much harder design problem than detecting a positive `Delta_AD`.",
        "",
        "The negative-A0 rows are sensitivity scenarios, not historical effect estimates. They show how quickly the required sample size grows as the undefended attraction effect approaches zero. A positive practical margin `epsilon` would change the scientific claim and must be justified before seeing the confirmatory data.",
        "",
        "## Boundary",
        "",
        str(plan["claim_boundary"]),
        "",
    ]
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
    boundary = [row for row in plan["level23_rows"] if row["scenario"] == "boundary_A0_zero"]
    print(json.dumps({
        "rows_level1": len(plan["rows"]),
        "rows_level23": len(plan["level23_rows"]),
        "analysis_id": plan["analysis_id"],
        "boundary_level23_target_attainable": any(row["effective_n_per_trait_cell"] is not None for row in boundary),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
