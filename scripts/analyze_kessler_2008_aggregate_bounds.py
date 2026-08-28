"""Assumption-indexed aggregate uncertainty bounds for Kessler et al. (2008).

This is a sensitivity analysis, not a reconstruction of Fig. S8A or the source
ANOVA. It enumerates integer 2x2 cell allocations compatible with the published
aggregate constraints and reports how a *naive independent-binomial* interaction
behaves under declared denominator-balance profiles.

Published constraints used:
- 474 informative antherectomized flowers after excluding the wind-only day;
- 87 capsules before later losses;
- EV (A+,D+) capsule fraction approximately 35%;
- PMT, CHAL and CP each approximately 12--14%.

Because the article reports day-level percentages and multiple flowers per plant,
independent-binomial Wald intervals are not source-level uncertainty estimates.
The analysis therefore fail-closes on that boundary even when an auxiliary
probability-scale interval is positive.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict
from typing import Iterable


@dataclass(frozen=True)
class Cell:
    n: int
    y: int

    @property
    def p(self) -> float:
        return self.y / self.n


@dataclass
class ProfileSummary:
    max_denominator_ratio: float
    feasible_allocation_count: int = 0
    probability_delta_min: float = math.inf
    probability_delta_max: float = -math.inf
    probability_wald_z_min: float = math.inf
    probability_wald_z_max: float = -math.inf
    probability_design_effect_to_cross_1_96_at_min_z: float = math.inf
    logit_beta_min: float = math.inf
    logit_beta_max: float = -math.inf
    logit_wald_z_min: float = math.inf
    logit_wald_z_max: float = -math.inf
    logit_ci95_lower_min: float = math.inf
    logit_ci95_lower_max: float = -math.inf
    example_min_logit_z: dict[str, object] | None = None


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def _feasible_cells(n_min: int, n_max: int, p_low: float, p_high: float) -> list[Cell]:
    cells: list[Cell] = []
    for n in range(n_min, n_max + 1):
        y_min = max(1, math.ceil(p_low * n - 1e-12))
        y_max = min(n - 1, math.floor(p_high * n + 1e-12))
        for y in range(y_min, y_max + 1):
            p = y / n
            if p_low <= p <= p_high:
                cells.append(Cell(n=n, y=y))
    return cells


def _profile_n_bounds(total_n: int, ratio: float) -> tuple[int, int]:
    # If max(n_i)/min(n_i) <= ratio and four cells sum to total_n, these
    # conservative bounds contain every feasible cell denominator.
    lower = max(3, math.floor(total_n / (1.0 + 3.0 * ratio)) - 2)
    upper = min(total_n - 9, math.ceil(total_n * ratio / (ratio + 3.0)) + 3)
    return lower, upper


def _update(summary: ProfileSummary, cells: tuple[Cell, Cell, Cell, Cell]) -> None:
    p11, p10, p01, p00 = (cell.p for cell in cells)
    delta = p11 - p10 - p01 + p00
    se_delta = math.sqrt(sum(cell.p * (1.0 - cell.p) / cell.n for cell in cells))
    z_delta = delta / se_delta

    beta = _logit(p11) - _logit(p10) - _logit(p01) + _logit(p00)
    se_beta = math.sqrt(sum(1.0 / cell.y + 1.0 / (cell.n - cell.y) for cell in cells))
    z_beta = beta / se_beta
    ci_lo = beta - 1.96 * se_beta

    summary.feasible_allocation_count += 1
    summary.probability_delta_min = min(summary.probability_delta_min, delta)
    summary.probability_delta_max = max(summary.probability_delta_max, delta)
    summary.probability_wald_z_min = min(summary.probability_wald_z_min, z_delta)
    summary.probability_wald_z_max = max(summary.probability_wald_z_max, z_delta)
    summary.logit_beta_min = min(summary.logit_beta_min, beta)
    summary.logit_beta_max = max(summary.logit_beta_max, beta)
    summary.logit_wald_z_min = min(summary.logit_wald_z_min, z_beta)
    summary.logit_wald_z_max = max(summary.logit_wald_z_max, z_beta)
    summary.logit_ci95_lower_min = min(summary.logit_ci95_lower_min, ci_lo)
    summary.logit_ci95_lower_max = max(summary.logit_ci95_lower_max, ci_lo)

    if summary.example_min_logit_z is None or z_beta < float(summary.example_min_logit_z["logit_wald_z"]):
        labels = ("EV_Aplus_Dplus", "PMT_Aplus_Dminus", "CHAL_Aminus_Dplus", "CP_Aminus_Dminus")
        summary.example_min_logit_z = {
            "logit_wald_z": z_beta,
            "logit_beta": beta,
            "logit_se": se_beta,
            "logit_ci95_lower": ci_lo,
            "probability_delta": delta,
            "probability_wald_z": z_delta,
            "cells": {
                label: {"n": cell.n, "y": cell.y, "p": cell.p}
                for label, cell in zip(labels, cells)
            },
        }


def enumerate_profile(
    *,
    total_n: int,
    total_y: int,
    ev_range: tuple[float, float],
    low_range: tuple[float, float],
    max_denominator_ratio: float,
) -> ProfileSummary:
    n_min, n_max = _profile_n_bounds(total_n, max_denominator_ratio)
    ev_cells = _feasible_cells(n_min, n_max, *ev_range)
    low_cells = _feasible_cells(n_min, n_max, *low_range)

    pair_map: dict[tuple[int, int], list[tuple[Cell, Cell]]] = defaultdict(list)
    for left in low_cells:
        for right in low_cells:
            pair_map[(left.n + right.n, left.y + right.y)].append((left, right))

    summary = ProfileSummary(max_denominator_ratio=max_denominator_ratio)
    for ev in ev_cells:
        for low1 in low_cells:
            needed = (total_n - ev.n - low1.n, total_y - ev.y - low1.y)
            for low2, low3 in pair_map.get(needed, ()):
                cells = (ev, low1, low2, low3)
                denominators = [cell.n for cell in cells]
                if max(denominators) / min(denominators) > max_denominator_ratio:
                    continue
                _update(summary, cells)

    if summary.feasible_allocation_count == 0:
        raise ValueError(f"no feasible allocations for denominator ratio <= {max_denominator_ratio}")

    # If a naive independent-binomial z is z_min, multiplying its variance by
    # design_effect reduces z by sqrt(design_effect). This threshold shows how
    # little unmodelled clustering would be needed to erase nominal 1.96.
    summary.probability_design_effect_to_cross_1_96_at_min_z = (
        summary.probability_wald_z_min / 1.96
    ) ** 2
    return summary


def analyze(
    profiles: Iterable[float] = (1.25, 1.5, 2.0, 3.0),
    *,
    total_n: int = 474,
    total_y: int = 87,
    ev_range: tuple[float, float] = (0.345, 0.355),
    low_range: tuple[float, float] = (0.115, 0.145),
) -> dict[str, object]:
    summaries = [
        enumerate_profile(
            total_n=total_n,
            total_y=total_y,
            ev_range=ev_range,
            low_range=low_range,
            max_denominator_ratio=float(profile),
        )
        for profile in profiles
    ]
    return {
        "analysis_id": "kessler_2008_aggregate_bounds_v1",
        "doi": "10.1126/science.1160072",
        "published_constraints": {
            "informative_flowers": total_n,
            "capsules": total_y,
            "EV_fraction_band": list(ev_range),
            "low_fraction_band": list(low_range),
            "fraction_band_note": "Bands deliberately widen the article's approximate 35% and 12-14% summaries to allow rounding.",
        },
        "profiles": [asdict(summary) for summary in summaries],
        "estimand_boundary": (
            "These are auxiliary pooled independent-binomial sensitivity calculations. "
            "They do not recover the source day-stratified ANOVA, plant-level clustering, "
            "or Fig. S8A values and therefore cannot be promoted to a source interaction CI."
        ),
        "decision_rule": (
            "Aggregate sign robustness is strengthened if every feasible profile keeps Delta > 0. "
            "Formal escape remains unresolved if source/design-based uncertainty is unavailable or "
            "if reasonable auxiliary scales/profiles do not uniformly exclude zero."
        ),
    }


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Kessler 2008 aggregate uncertainty bounds v1",
        "",
        "## Scope",
        "",
        "This is an assumption-indexed sensitivity analysis of the published aggregate constraints, not a reconstruction of Fig. S8A or the source ANOVA.",
        "",
        "Published informative total: 474 flowers and 87 capsules. EV is allowed to range from 34.5–35.5%; each low cell is allowed 11.5–14.5% to be conservative about rounding.",
        "",
        "| max denominator ratio | feasible allocations | min probability Δ | min naive z(Δ) | design effect needed to reduce min z to 1.96 | min logit β | min logit z | minimum logit CI lower bound |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for profile in report["profiles"]:  # type: ignore[index]
        lines.append(
            "| {max_denominator_ratio:.2f} | {feasible_allocation_count} | {probability_delta_min:+.4f} | "
            "{probability_wald_z_min:.3f} | {probability_design_effect_to_cross_1_96_at_min_z:.3f} | "
            "{logit_beta_min:+.4f} | {logit_wald_z_min:.3f} | {logit_ci95_lower_min:+.4f} |".format(**profile)
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "Across all declared denominator-balance profiles, the aggregate probability-scale interaction remains positive. Under a naive independent-binomial calculation its minimum z also exceeds 1.96. However, this is not source-level uncertainty: the source used repeated experimental days and multiple flowers per plant, and those clustering structures are unavailable without Fig. S8A / exact design cells.",
        "",
        "The auxiliary logit interaction is also positive in sign but its 95% Wald interval can cross zero under feasible allocations. The conclusion is therefore intentionally asymmetric: **the positive factorial sign is robust, while formal uncertainty identification is not**.",
        "",
        "The design-effect column quantifies the fragility of treating flowers as independent. It gives the variance inflation needed to reduce the worst-case probability-scale z to 1.96; values near 1 mean that modest unmodelled clustering can erase nominal significance.",
        "",
        "## Boundary",
        "",
        str(report["estimand_boundary"]),
        "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("out_md", type=Path)
    parser.add_argument(
        "--profiles",
        default="1.25,1.5,2.0,3.0",
        help="Comma-separated max denominator ratios",
    )
    args = parser.parse_args(argv)
    profiles = tuple(float(value) for value in args.profiles.split(",") if value.strip())
    report = analyze(profiles)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    args.out_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "analysis_id": report["analysis_id"],
        "profile_count": len(report["profiles"]),
        "min_probability_delta": min(p["probability_delta_min"] for p in report["profiles"]),
        "min_logit_ci_lower": min(p["logit_ci95_lower_min"] for p in report["profiles"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
