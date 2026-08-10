"""How precise must the constituent-pathway estimate be to move the theory?

The declared empirical target estimates one parameter of the implemented
corollary: the defence-pollinator cost ``c_D``, recovered from the oriented log
response ratio of the ``D -> legitimate pollinator use`` route.  Estimating a
parameter is only worth doing if the estimate can change a conclusion, so this
module answers the question in advance, without any data:

    for each declared phenotype-and-regime point, which values of ``c_D`` make
    the local interaction complementary, and how tight must an interval around
    ``c_D`` be before that point's sign classification is settled?

The result is a required-precision statement. It tells the extraction effort what
it is buying before it is spent, and it identifies the regime points where no
achievable precision on this one parameter would settle the sign — those points
are governed by the other two channels and must be attacked differently.

## The boundary in closed form

In the implemented corollary,

```text
W_AD = H*d_A*e_F - P*b_A*c_D*exp(-c_D*D)*(1 - c_R*R) - c_AD.
```

Writing the pollination prefactor ``S = P*b_A*(1 - c_R*R) > 0`` and

```text
K = (H*d_A*e_F - c_AD) / S,
```

the sign condition becomes

```text
W_AD > 0   <=>   K > f(c_D),      f(c) = c*exp(-c*D).
```

``f`` is not monotone. On ``c >= 0`` it rises to a single maximum ``1/(D*e)`` at
``c = 1/D`` and then decays, so the complementary set is an interval complement
rather than a half line:

```text
K <= 0            substitutable for every c_D >= 0
0 < K < 1/(D*e)   complementary for c_D < c_low or c_D > c_high
K >= 1/(D*e)      complementary for every c_D >= 0
```

The upper branch is a real property of the corollary rather than an artefact: a
very large pollinator cost drives ``exp(-c_D*D)`` toward zero, the mutualist
channel is almost entirely shut off at the focal defence level, and its cross
curvature vanishes with it. It is reported explicitly rather than hidden, and it
is flagged when an empirical interval lands near it, because that is a regime
where the corollary's functional form — not the data — is doing the work.

At ``D = 0`` the decay term is absent, ``f(c) = c``, and the boundary is the
single value ``c_D = K``.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from trait_architecture.broad_meta_analysis import write_csv_rows
from trait_architecture.model import Architecture, InteractionRegime, ModelParameters


LEVERAGE_OUTPUT_FIELDS = (
    "scenario_id", "defence", "assurance", "pollinator_service",
    "floral_damage_pressure", "relief_minus_joint_cost_ratio_K", "boundary_type",
    "lower_boundary_c_D", "upper_boundary_c_D", "classification_at_interval_low",
    "classification_at_interval_high", "interval_verdict",
)
SUMMARY_FIELDS = (
    "scenario_id", "grid_points", "settled_complementary", "settled_substitutable",
    "unsettled_by_interval", "always_substitutable", "always_complementary",
    "settled_fraction",
)

_UPPER_BRANCH_SEARCH_LIMIT = 1e4


@dataclass(frozen=True)
class SignBoundary:
    """The set of ``c_D`` values giving local complementarity at one grid point."""

    k_value: float
    defence: float
    boundary_type: str
    lower: float | None
    upper: float | None

    def is_complementary(self, defence_pollinator_cost: float) -> bool:
        if defence_pollinator_cost < 0:
            raise ValueError("defence_pollinator_cost must be non-negative")
        if self.boundary_type == "always_substitutable":
            return False
        if self.boundary_type == "always_complementary":
            return True
        if self.boundary_type == "single_threshold":
            return defence_pollinator_cost < self.lower
        return defence_pollinator_cost < self.lower or defence_pollinator_cost > self.upper


def _f(cost: float, defence: float) -> float:
    return cost * math.exp(-cost * defence)


def _bisect(low: float, high: float, defence: float, target: float, rising: bool) -> float:
    for _ in range(200):
        middle = 0.5 * (low + high)
        above = _f(middle, defence) > target
        if above == rising:
            high = middle
        else:
            low = middle
    return 0.5 * (low + high)


def sign_boundary(
    architecture: Architecture,
    regime: InteractionRegime,
    parameters: ModelParameters = ModelParameters(),
) -> SignBoundary:
    """Return the complementary set of ``c_D`` at one declared grid point."""

    prefactor = (
        regime.pollinator_service
        * parameters.attraction_gain
        * (1.0 - parameters.assurance_outcross_dilution * architecture.assurance)
    )
    relief = (
        regime.floral_damage_pressure
        * parameters.attraction_tracking
        * parameters.floral_defence_efficacy
    )
    joint_cost = parameters.attraction_defence_shared_cost
    defence = architecture.defence

    if prefactor <= 0:
        # No pollination channel at this point, so c_D cannot influence the sign.
        boundary = "always_complementary" if relief - joint_cost > 0 else "always_substitutable"
        return SignBoundary(math.inf, defence, boundary, None, None)

    k_value = (relief - joint_cost) / prefactor

    if k_value <= 0:
        return SignBoundary(k_value, defence, "always_substitutable", None, None)
    if defence <= 0:
        return SignBoundary(k_value, defence, "single_threshold", k_value, None)

    peak = 1.0 / (defence * math.e)
    if k_value >= peak:
        return SignBoundary(k_value, defence, "always_complementary", None, None)

    mode = 1.0 / defence
    lower = _bisect(0.0, mode, defence, k_value, rising=True)
    upper = _bisect(mode, _UPPER_BRANCH_SEARCH_LIMIT, defence, k_value, rising=False)
    return SignBoundary(k_value, defence, "two_sided_window", lower, upper)


def cost_from_log_response_ratio(log_response_ratio: float, trait_contrast: float) -> float:
    """Recover ``c_D`` from an oriented route effect.

    Under the corollary's multiplicative access term, a manipulation contrasting
    two declared defence levels gives ``LRR = -c_D * (d1 - d0)``. A non-negative
    ``c_D`` is required by the orientation gate, so a positive route effect
    returns zero and must be reported as a gate failure, not as a negative cost.
    """

    if trait_contrast <= 0:
        raise ValueError("trait_contrast must be positive on the declared 0-1 defence scale")
    return max(0.0, -log_response_ratio / trait_contrast)


def evaluate_interval(
    boundary: SignBoundary,
    interval_low: float,
    interval_high: float,
) -> tuple[str, str, str]:
    """Classify an empirical ``c_D`` interval against one grid point's boundary."""

    if interval_low > interval_high:
        raise ValueError("interval_low must not exceed interval_high")
    at_low = "complementary" if boundary.is_complementary(interval_low) else "substitutable"
    at_high = "complementary" if boundary.is_complementary(interval_high) else "substitutable"
    if boundary.boundary_type == "always_complementary":
        verdict = "settled_complementary_regardless_of_c_D"
    elif boundary.boundary_type == "always_substitutable":
        verdict = "settled_substitutable_regardless_of_c_D"
    elif at_low == at_high:
        # The whole interval agrees, but a two-sided window can hide a sign flip
        # strictly inside it, so that case is checked rather than assumed.
        if (
            boundary.boundary_type == "two_sided_window"
            and interval_low <= boundary.lower
            and boundary.upper <= interval_high
        ):
            verdict = "unsettled_interval_spans_boundary"
        elif (
            boundary.boundary_type == "two_sided_window"
            and interval_low < boundary.lower < interval_high
        ):
            verdict = "unsettled_interval_spans_boundary"
        else:
            verdict = f"settled_{at_low}"
    else:
        verdict = "unsettled_interval_spans_boundary"
    return at_low, at_high, verdict


def _override(parameters: ModelParameters, overrides: dict[str, float]) -> ModelParameters:
    fields = {**parameters.__dict__, **overrides}
    return ModelParameters(**fields)


def leverage_grid(
    config: dict,
    interval_low: float,
    interval_high: float,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Evaluate every declared grid point against one candidate ``c_D`` interval."""

    grid = config["phenotype_and_regime_grid"]
    rows: list[dict[str, object]] = []
    # The mixed partial of the implemented corollary does not depend on A: the
    # attraction trait enters every channel linearly, so it cancels from the
    # cross derivative. The attraction axis of the Part I grid is therefore
    # omitted here rather than replicated into identical rows.
    for scenario in config["parameter_scenarios"]:
        parameters = _override(ModelParameters(), scenario.get("overrides", {}))
        for defence in grid["defence"]:
            for assurance in grid["assurance"]:
                for service in grid["pollinator_service"]:
                    for pressure in grid["floral_damage_pressure"]:
                        architecture = Architecture(grid["attraction"][0], defence, assurance)
                        regime = InteractionRegime(service, pressure)
                        boundary = sign_boundary(architecture, regime, parameters)
                        at_low, at_high, verdict = evaluate_interval(
                            boundary, interval_low, interval_high
                        )
                        rows.append({
                            "scenario_id": scenario["scenario_id"],
                            "defence": defence,
                            "assurance": assurance,
                            "pollinator_service": service,
                            "floral_damage_pressure": pressure,
                            "relief_minus_joint_cost_ratio_K": f"{boundary.k_value:.10g}",
                            "boundary_type": boundary.boundary_type,
                            "lower_boundary_c_D": "" if boundary.lower is None else f"{boundary.lower:.10g}",
                            "upper_boundary_c_D": "" if boundary.upper is None else f"{boundary.upper:.10g}",
                            "classification_at_interval_low": at_low,
                            "classification_at_interval_high": at_high,
                            "interval_verdict": verdict,
                        })

    summaries: list[dict[str, object]] = []
    for scenario in config["parameter_scenarios"]:
        subset = [row for row in rows if row["scenario_id"] == scenario["scenario_id"]]
        counts = {
            "settled_complementary": sum(row["interval_verdict"] == "settled_complementary" for row in subset),
            "settled_substitutable": sum(row["interval_verdict"] == "settled_substitutable" for row in subset),
            "unsettled_by_interval": sum(
                row["interval_verdict"] == "unsettled_interval_spans_boundary" for row in subset
            ),
            "always_substitutable": sum(
                row["interval_verdict"] == "settled_substitutable_regardless_of_c_D" for row in subset
            ),
            "always_complementary": sum(
                row["interval_verdict"] == "settled_complementary_regardless_of_c_D" for row in subset
            ),
        }
        settled = len(subset) - counts["unsettled_by_interval"]
        summaries.append({
            "scenario_id": scenario["scenario_id"],
            "grid_points": len(subset),
            **counts,
            "settled_fraction": f"{settled / len(subset):.6f}" if subset else "",
        })
    return rows, summaries


def required_precision(
    config: dict,
    centre: float,
    half_widths: Sequence[float] = (0.05, 0.10, 0.20, 0.40, 0.80),
) -> list[dict[str, object]]:
    """Settled fraction of the declared grid as a function of interval width.

    This is the analysis that tells the extraction effort what precision it needs:
    the smallest half-width whose settled fraction stops improving is the point
    beyond which more studies no longer change any sign classification.
    """

    results: list[dict[str, object]] = []
    for half_width in half_widths:
        low = max(0.0, centre - half_width)
        rows, _ = leverage_grid(config, low, centre + half_width)
        unsettled = sum(row["interval_verdict"] == "unsettled_interval_spans_boundary" for row in rows)
        results.append({
            "centre_c_D": f"{centre:.6g}",
            "half_width": f"{half_width:.6g}",
            "interval_low": f"{low:.6g}",
            "interval_high": f"{centre + half_width:.6g}",
            "grid_points": len(rows),
            "unsettled_points": unsettled,
            "settled_fraction": f"{(len(rows) - unsettled) / len(rows):.6f}" if rows else "",
        })
    return results


def write_leverage_outputs(
    out_dir: str | Path,
    config: dict,
    interval_low: float,
    interval_high: float,
) -> dict[str, object]:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    rows, summaries = leverage_grid(config, interval_low, interval_high)
    centre = 0.5 * (interval_low + interval_high)
    precision = required_precision(config, centre)
    write_csv_rows(destination / "empirical_leverage_grid.csv", LEVERAGE_OUTPUT_FIELDS, rows)
    write_csv_rows(destination / "empirical_leverage_summary.csv", SUMMARY_FIELDS, summaries)
    write_csv_rows(
        destination / "empirical_required_precision.csv",
        ("centre_c_D", "half_width", "interval_low", "interval_high", "grid_points",
         "unsettled_points", "settled_fraction"),
        precision,
    )
    diagnostics = {
        "interval_low": interval_low,
        "interval_high": interval_high,
        "grid_points": len(rows),
        "unsettled_points": sum(
            row["interval_verdict"] == "unsettled_interval_spans_boundary" for row in rows
        ),
        "points_insensitive_to_c_D": sum(
            row["boundary_type"] in {"always_complementary", "always_substitutable"} for row in rows
        ),
        "interpretation_boundary": (
            "This is a property of the declared corollary and the declared finite grid. It states "
            "which sign classifications a given precision on c_D would settle. It is not an estimate "
            "of c_D, not evidence about nature, and not a prevalence statement."
        ),
    }
    (destination / "empirical_leverage_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
    return diagnostics


def load_config(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


__all__ = [
    "SignBoundary",
    "cost_from_log_response_ratio",
    "evaluate_interval",
    "leverage_grid",
    "load_config",
    "required_precision",
    "sign_boundary",
    "write_leverage_outputs",
]
