"""Simulation power analysis for the pre-registered moderator design.

A pre-registration is only honest if its declared capacity thresholds can, in
principle, answer the question it declares.  A threshold of "three independent
clusters per moderator level" is a rule about *permission to estimate*; it says
nothing about whether an estimate at that size can distinguish a real context
effect from noise.  If the declared design has low power against the contrast
the protocol was written to detect, then a future null result would be
uninformative, and the correct time to discover that is before extraction — not
after.

This module answers that question by simulating effect sets with known truth and
pushing them through the *deployed* analysis functions in
:mod:`trait_architecture.context_dependence`.  Nothing is re-derived here: the
power reported is the power of the code that will actually run.

The generative model is deliberately simple and declared rather than fitted:

```text
theta_ij ~ Normal(mu_level(i), tau^2)      between-cluster heterogeneity
se_ij    ~ Uniform(se_low, se_high)        sampling precision of study j
y_ij     ~ Normal(theta_ij, se_ij^2)       reported effect
```

All quantities are on the declared log-response-ratio scale, so a contrast of
0.69 is a doubling of pollinator use between moderator levels.  Simulation is
seeded, so a reported power is reproducible to the digit.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from trait_architecture.broad_meta_analysis import EffectEstimate, write_csv_rows
from trait_architecture.context_dependence import (
    ModeratedEffect,
    meta_regression,
    subgroup_analysis,
)


POWER_OUTPUT_FIELDS = (
    "scenario_id", "moderator_name", "clusters_per_level", "level_contrast",
    "between_cluster_sd", "standard_error_low", "standard_error_high", "replicates",
    "q_between_fixed_effect_rejection_rate", "meta_regression_contrast_power",
    "direction_reversal_detection_rate", "estimable_fraction", "design_verdict",
)

REFERENCE_LEVEL = "within_natural_range"
CONTRAST_LEVEL = "above_natural_range"


@dataclass(frozen=True)
class PowerScenario:
    """One declared generative scenario for the target stratum."""

    scenario_id: str
    clusters_per_level: int
    level_contrast: float
    between_cluster_sd: float
    standard_error_low: float = 0.10
    standard_error_high: float = 0.30
    reference_mean: float = 0.0

    def __post_init__(self) -> None:
        if self.clusters_per_level < 2:
            raise ValueError("a moderator level needs at least two clusters")
        if self.between_cluster_sd < 0:
            raise ValueError("between-cluster SD must be non-negative")
        if not 0 < self.standard_error_low <= self.standard_error_high:
            raise ValueError("standard-error bounds must be positive and ordered")


def _registry_row(scenario: PowerScenario, moderator_name: str) -> dict[str, str]:
    """A registry row matching the committed declaration for this stratum."""

    return {
        "analysis_id": scenario.scenario_id,
        "stratum_id": "BP_chemical_pollinator_use_lrr_manipulation",
        "moderator_name": moderator_name,
        "moderator_type": "categorical",
        "reference_level": REFERENCE_LEVEL,
        "min_levels": "2",
        "min_clusters_per_level": str(scenario.clusters_per_level),
        "min_clusters_total": str(2 * scenario.clusters_per_level),
        "declared_hypothesis": "simulated",
        "licensed_statement": "simulated",
        "interpretation": "simulated",
    }


def _draw_effects(scenario: PowerScenario, rng: random.Random) -> list[ModeratedEffect]:
    effects: list[ModeratedEffect] = []
    levels = (
        (REFERENCE_LEVEL, scenario.reference_mean),
        (CONTRAST_LEVEL, scenario.reference_mean + scenario.level_contrast),
    )
    for level, mean in levels:
        for index in range(scenario.clusters_per_level):
            theta = rng.gauss(mean, scenario.between_cluster_sd) if scenario.between_cluster_sd else mean
            se = rng.uniform(scenario.standard_error_low, scenario.standard_error_high)
            value = rng.gauss(theta, se)
            cluster = f"{level}-cluster-{index}"
            estimate = EffectEstimate(
                effect_id=f"{cluster}-effect",
                study_cluster_id=cluster,
                value=value,
                standard_error=se,
                conversion_method="simulated",
                row={},
            )
            effects.append(ModeratedEffect(estimate, level))
    return effects


def simulate_scenario(
    scenario: PowerScenario,
    *,
    moderator_name: str = "dose_realism",
    replicates: int = 2000,
    seed: int = 20260810,
) -> dict[str, object]:
    """Return detection rates for one declared scenario at the declared alpha."""

    if replicates < 1:
        raise ValueError("replicates must be positive")
    rng = random.Random(seed)
    registry_row = _registry_row(scenario, moderator_name)

    subgroup_hits = 0
    regression_hits = 0
    reversal_hits = 0
    estimable = 0
    for _ in range(replicates):
        effects = _draw_effects(scenario, rng)
        levels, test = subgroup_analysis(effects, registry_row)
        if test["analysis_status"] != "subgroup_random_effects":
            continue
        estimable += 1
        if float(test["Q_between_fixed_effect_p_value"]) < 0.05:
            subgroup_hits += 1
        terms, model = meta_regression(effects, registry_row, levels)
        if model["analysis_status"] != "random_effects_meta_regression":
            continue
        if model["context_dependence_verdict"] == "context_dependent_direction_reversal":
            reversal_hits += 1
        contrast = next((row for row in terms if row["term"].startswith("level[")), None)
        if contrast is not None and contrast["two_sided_p_value"] != "" and float(contrast["two_sided_p_value"]) < 0.05:
            regression_hits += 1

    denominator = estimable or 1
    subgroup_rejection = subgroup_hits / denominator
    regression_power = regression_hits / denominator
    # The design verdict reads the calibrated test only. The fixed-effect
    # Q_between rejection rate is reported alongside it as a diagnostic of how
    # badly that statistic would mislead at this heterogeneity, never as power.
    if regression_power >= 0.80:
        verdict = "declared_design_adequate"
    elif regression_power >= 0.50:
        verdict = "declared_design_underpowered_null_uninformative"
    else:
        verdict = "declared_design_cannot_answer"
    return {
        "scenario_id": scenario.scenario_id,
        "moderator_name": moderator_name,
        "clusters_per_level": scenario.clusters_per_level,
        "level_contrast": f"{scenario.level_contrast:.4g}",
        "between_cluster_sd": f"{scenario.between_cluster_sd:.4g}",
        "standard_error_low": f"{scenario.standard_error_low:.4g}",
        "standard_error_high": f"{scenario.standard_error_high:.4g}",
        "replicates": replicates,
        "q_between_fixed_effect_rejection_rate": f"{subgroup_rejection:.4f}",
        "meta_regression_contrast_power": f"{regression_power:.4f}",
        "direction_reversal_detection_rate": f"{reversal_hits / denominator:.4f}",
        "estimable_fraction": f"{estimable / replicates:.4f}",
        "design_verdict": verdict,
    }


def declared_scenario_grid(
    cluster_counts: Sequence[int] = (3, 5, 8, 12),
    contrasts: Sequence[float] = (-0.35, -0.69, -1.10),
    between_cluster_sds: Sequence[float] = (0.0, 0.25, 0.50),
) -> list[PowerScenario]:
    """The declared power grid for the target stratum.

    Contrasts are on the log-response-ratio scale: -0.35 is roughly a 30% drop
    in pollinator use between moderator levels, -0.69 a halving, -1.10 a
    two-thirds reduction. Cluster counts start at the protocol's declared
    minimum of three per level.
    """

    scenarios: list[PowerScenario] = []
    for clusters in cluster_counts:
        for contrast in contrasts:
            for tau in between_cluster_sds:
                scenarios.append(PowerScenario(
                    scenario_id=f"k{clusters}_d{abs(contrast):.2f}_tau{tau:.2f}".replace(".", "p"),
                    clusters_per_level=clusters,
                    level_contrast=contrast,
                    between_cluster_sd=tau,
                ))
    return scenarios


def run_power_grid(
    scenarios: Iterable[PowerScenario] | None = None,
    *,
    replicates: int = 2000,
    seed: int = 20260810,
) -> list[dict[str, object]]:
    scenarios = list(scenarios) if scenarios is not None else declared_scenario_grid()
    return [
        simulate_scenario(scenario, replicates=replicates, seed=seed + index)
        for index, scenario in enumerate(scenarios)
    ]


def minimum_adequate_cluster_count(
    rows: Sequence[dict[str, object]],
    contrast: float,
    between_cluster_sd: float,
) -> int | None:
    """Smallest declared cluster count reaching 80% power for one truth setting."""

    matching = [
        row for row in rows
        if abs(float(row["level_contrast"]) - contrast) < 1e-9
        and abs(float(row["between_cluster_sd"]) - between_cluster_sd) < 1e-9
        and row["design_verdict"] == "declared_design_adequate"
    ]
    if not matching:
        return None
    return min(int(row["clusters_per_level"]) for row in matching)


def write_power_outputs(
    out_dir: str | Path,
    *,
    replicates: int = 2000,
    seed: int = 20260810,
) -> list[dict[str, object]]:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    rows = run_power_grid(replicates=replicates, seed=seed)
    write_csv_rows(destination / "declared_design_power.csv", POWER_OUTPUT_FIELDS, rows)
    return rows
