"""Which channel is worth measuring? A value-of-information ranking.

The declared empirical target measures one parameter, ``c_D``, of one channel.
That pathway was chosen because its literature is the most tractable — the
studies are manipulations, the outcome is a direct channel measurement, and the
route already has independent clusters in one compatibility cell. Feasibility is
a legitimate reason to start somewhere, but it is not the same as being the most
*informative* place to start, and the project should not confuse the two.

This module asks the comparable question for every parameter of the three-channel
balance:

    if this parameter could be pinned down to a given relative precision, what
    fraction of the declared grid's sign classifications would that settle?

The answer is computed by root-finding on the deployed mixed partial in
:mod:`trait_architecture.robustness`, so it holds for all four declared
endpoint-normalized response-shape variants rather than only the baseline
exponential form. That generality matters here: under the shape variants the
mixed partial depends on the attraction coordinate ``A`` through the
attraction-gain and joint-cost terms, so ``A`` is retained as a grid axis. It
cancels only in the baseline form.

Nothing here estimates any parameter. The output is a property of the declared
corollary, the declared grid, and the declared prior ranges. It is a statement
about which measurement would change conclusions, not about nature.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from trait_architecture.broad_meta_analysis import write_csv_rows
from trait_architecture.model import ModelParameters
from trait_architecture.robustness import (
    FunctionalForm,
    RobustnessCase,
    default_functional_forms,
    mixed_partial,
)


CHANNEL_LEVERAGE_FIELDS = (
    "parameter", "channel", "scenario_id", "form_id", "grid_points",
    "prior_low", "prior_high", "prior_sensitive_points", "prior_sensitive_fraction",
    "relative_half_width", "settled_points", "settled_fraction",
    "value_of_information",
)
RANKING_FIELDS = (
    "parameter", "channel", "relative_half_width", "grid_points",
    "prior_sensitive_fraction", "settled_fraction", "value_of_information", "rank",
)

#: Declared prior ranges. These bound what the parameter could plausibly be
#: before measurement; they are declared, not fitted, and are stated in the
#: readout so a reader can substitute their own.
DECLARED_PRIOR_RANGES: dict[str, tuple[float, float]] = {
    "attraction_tracking": (0.0, 3.0),
    "floral_defence_efficacy": (0.0, 1.0),
    "defence_pollinator_cost": (0.0, 3.0),
    "attraction_gain": (0.0, 3.0),
    "attraction_defence_shared_cost": (0.0, 1.0),
}
PARAMETER_CHANNEL = {
    "attraction_tracking": "antagonist_relief_rho",
    "floral_defence_efficacy": "antagonist_relief_rho",
    "defence_pollinator_cost": "mutualist_interference_iota",
    "attraction_gain": "mutualist_interference_iota",
    "attraction_defence_shared_cost": "direct_joint_cost_kappa",
}
DEFAULT_RELATIVE_HALF_WIDTHS = (0.10, 0.25, 0.50, 1.00)

_SCAN_POINTS = 160
_BISECTION_STEPS = 60


@dataclass(frozen=True)
class GridPoint:
    case: RobustnessCase
    form: FunctionalForm


def _with_parameter(parameters: ModelParameters, name: str, value: float) -> ModelParameters:
    fields = {**parameters.__dict__, name: value}
    return ModelParameters(**fields)


def _value_at(point: GridPoint, parameters: ModelParameters, name: str, value: float) -> float:
    return mixed_partial(
        point.case, _with_parameter(parameters, name, value), point.form
    ).mixed_partial


def sign_change_points(
    point: GridPoint,
    parameters: ModelParameters,
    name: str,
    low: float,
    high: float,
) -> list[float]:
    """Locate every value of one parameter where the local sign flips.

    A scan-then-bisect search is used rather than a closed form because the
    dependence is not monotone for every parameter and shape variant: the
    pollinator-cost term rises and then decays, so a parameter range can contain
    two boundaries. Missing the second one would report a straddling interval as
    settled.
    """

    if high <= low:
        raise ValueError("prior range must be increasing")
    step = (high - low) / _SCAN_POINTS
    roots: list[float] = []
    previous_x = low
    previous = _value_at(point, parameters, name, previous_x)
    for index in range(1, _SCAN_POINTS + 1):
        current_x = low + index * step
        current = _value_at(point, parameters, name, current_x)
        if previous == 0.0:
            roots.append(previous_x)
        elif (previous > 0) != (current > 0):
            lo, hi = previous_x, current_x
            lo_positive = previous > 0
            for _ in range(_BISECTION_STEPS):
                middle = 0.5 * (lo + hi)
                if (_value_at(point, parameters, name, middle) > 0) == lo_positive:
                    lo = middle
                else:
                    hi = middle
            roots.append(0.5 * (lo + hi))
        previous_x, previous = current_x, current
    return roots


def _grid_points(config: dict, forms: Sequence[FunctionalForm]) -> list[GridPoint]:
    grid = config["phenotype_and_regime_grid"]
    points: list[GridPoint] = []
    index = 0
    for attraction in grid["attraction"]:
        for defence in grid["defence"]:
            for assurance in grid["assurance"]:
                for service in grid["pollinator_service"]:
                    for pressure in grid["floral_damage_pressure"]:
                        index += 1
                        case = RobustnessCase(
                            case_id=f"case-{index}",
                            attraction=attraction,
                            defence=defence,
                            assurance=assurance,
                            pollinator_service=service,
                            floral_damage_pressure=pressure,
                        )
                        for form in forms:
                            points.append(GridPoint(case, form))
    return points


def _override(parameters: ModelParameters, overrides: dict[str, float]) -> ModelParameters:
    return ModelParameters(**{**parameters.__dict__, **overrides})


def channel_leverage(
    config: dict,
    parameters_of_interest: Sequence[str] | None = None,
    relative_half_widths: Sequence[float] = DEFAULT_RELATIVE_HALF_WIDTHS,
    forms: Sequence[FunctionalForm] | None = None,
) -> list[dict[str, object]]:
    """Settled fraction per parameter, scenario, shape variant, and precision."""

    names = list(parameters_of_interest or DECLARED_PRIOR_RANGES)
    for name in names:
        if name not in DECLARED_PRIOR_RANGES:
            raise ValueError(f"no declared prior range for parameter '{name}'")
    chosen_forms = list(forms) if forms is not None else list(default_functional_forms())
    rows: list[dict[str, object]] = []

    for scenario in config["parameter_scenarios"]:
        base = _override(ModelParameters(), scenario.get("overrides", {}))
        for form in chosen_forms:
            points = [point for point in _grid_points(config, [form])]
            for name in names:
                low, high = DECLARED_PRIOR_RANGES[name]
                centre = getattr(base, name)
                roots_by_point = [
                    sign_change_points(point, base, name, low, high) for point in points
                ]
                sensitive = sum(1 for roots in roots_by_point if roots)
                for relative in relative_half_widths:
                    half = relative * centre if centre > 0 else relative
                    window_low = max(low, centre - half)
                    window_high = min(high, centre + half)
                    settled = sum(
                        1 for roots in roots_by_point
                        if not any(window_low < root < window_high for root in roots)
                    )
                    total = len(points)
                    settled_fraction = settled / total if total else 0.0
                    insensitive_fraction = (total - sensitive) / total if total else 0.0
                    rows.append({
                        "parameter": name,
                        "channel": PARAMETER_CHANNEL[name],
                        "scenario_id": scenario["scenario_id"],
                        "form_id": form.form_id,
                        "grid_points": total,
                        "prior_low": f"{low:.6g}",
                        "prior_high": f"{high:.6g}",
                        "prior_sensitive_points": sensitive,
                        "prior_sensitive_fraction": f"{sensitive / total:.6f}" if total else "",
                        "relative_half_width": f"{relative:.4g}",
                        "settled_points": settled,
                        "settled_fraction": f"{settled_fraction:.6f}",
                        # What the measurement adds beyond what the declared prior
                        # already settles, expressed on the same 0-1 scale.
                        "value_of_information": f"{max(0.0, settled_fraction - insensitive_fraction):.6f}",
                    })
    return rows


def rank_parameters(
    rows: Sequence[dict[str, object]],
    relative_half_width: float = 0.25,
) -> list[dict[str, object]]:
    """Pool across scenarios and shape variants, then rank by value of information."""

    target = f"{relative_half_width:.4g}"
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        if row["relative_half_width"] != target:
            continue
        grouped.setdefault(str(row["parameter"]), []).append(row)
    if not grouped:
        raise ValueError(f"no rows at relative half-width {target}")

    summaries: list[dict[str, object]] = []
    for name, members in grouped.items():
        total = sum(int(row["grid_points"]) for row in members)
        settled = sum(int(row["settled_points"]) for row in members)
        sensitive = sum(int(row["prior_sensitive_points"]) for row in members)
        settled_fraction = settled / total
        insensitive_fraction = (total - sensitive) / total
        summaries.append({
            "parameter": name,
            "channel": PARAMETER_CHANNEL[name],
            "relative_half_width": target,
            "grid_points": total,
            "prior_sensitive_fraction": f"{sensitive / total:.6f}",
            "settled_fraction": f"{settled_fraction:.6f}",
            "value_of_information": f"{max(0.0, settled_fraction - insensitive_fraction):.6f}",
        })
    summaries.sort(key=lambda row: float(row["value_of_information"]), reverse=True)
    for position, row in enumerate(summaries, start=1):
        row["rank"] = position
    return summaries


def write_channel_leverage_outputs(
    out_dir: str | Path,
    config: dict,
    *,
    ranking_half_width: float = 0.25,
) -> dict[str, object]:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    rows = channel_leverage(config)
    ranking = rank_parameters(rows, ranking_half_width)
    write_csv_rows(destination / "channel_leverage_grid.csv", CHANNEL_LEVERAGE_FIELDS, rows)
    write_csv_rows(destination / "channel_leverage_ranking.csv", RANKING_FIELDS, ranking)
    diagnostics = {
        "ranking_relative_half_width": ranking_half_width,
        "parameters_evaluated": sorted(DECLARED_PRIOR_RANGES),
        "declared_prior_ranges": {k: list(v) for k, v in sorted(DECLARED_PRIOR_RANGES.items())},
        "top_parameter": ranking[0]["parameter"] if ranking else "",
        "top_channel": ranking[0]["channel"] if ranking else "",
        "declared_target_parameter": "defence_pollinator_cost",
        "declared_target_rank": next(
            (row["rank"] for row in ranking if row["parameter"] == "defence_pollinator_cost"), None
        ),
        "interpretation_boundary": (
            "Value of information is a property of the declared corollary, the declared finite grid, "
            "and the declared prior ranges. It ranks which measurement would change sign "
            "classifications. It estimates no parameter and says nothing about nature."
        ),
    }
    (destination / "channel_leverage_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
    return diagnostics
