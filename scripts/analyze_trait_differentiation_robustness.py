#!/usr/bin/env python3
"""Reproduce the declared nonquadratic trait-differentiation robustness grid."""

from __future__ import annotations

import json
from pathlib import Path

from trait_architecture.differentiation_robustness import compare_power_architectures


FUNCTIONAL_POWERS = (1.5, 2.0, 3.0, 4.0)
WEIGHTS = ((1.0, 1.0), (0.4, 2.0), (3.0, 0.7))
COUPLINGS = (0.0, 0.1, 0.5, 2.0, 10.0)
CONFLICT_DISTANCES = (0.1, 0.25, 0.5, 1.0, 2.0)
MISMATCHED_POWERS = ((1.5, 2.0), (2.0, 4.0), (4.0, 2.0))


def build_readout() -> dict:
    rows = []
    for power in FUNCTIONAL_POWERS:
        for weight_1, weight_2 in WEIGHTS:
            for coupling in COUPLINGS:
                for conflict in CONFLICT_DISTANCES:
                    result = compare_power_architectures(
                        0.0,
                        conflict,
                        weight_1=weight_1,
                        weight_2=weight_2,
                        coupling=coupling,
                        architecture_cost=0.0,
                        functional_power=power,
                        coupling_power=power,
                    )
                    rows.append(
                        {
                            "functional_power": power,
                            "coupling_power": power,
                            "weight_1": weight_1,
                            "weight_2": weight_2,
                            "coupling": coupling,
                            "conflict_distance": conflict,
                            "recoverable_conflict_loss": result.recoverable_conflict_loss,
                            "axis_separation": result.differentiated.separation,
                        }
                    )

    positive = sum(row["recoverable_conflict_loss"] > 0.0 for row in rows)

    conflict_series = 0
    conflict_monotone = 0
    for power in FUNCTIONAL_POWERS:
        for weight_1, weight_2 in WEIGHTS:
            for coupling in COUPLINGS:
                conflict_series += 1
                values = [
                    next(
                        row["recoverable_conflict_loss"]
                        for row in rows
                        if row["functional_power"] == power
                        and row["weight_1"] == weight_1
                        and row["weight_2"] == weight_2
                        and row["coupling"] == coupling
                        and row["conflict_distance"] == conflict
                    )
                    for conflict in CONFLICT_DISTANCES
                ]
                if all(a < b for a, b in zip(values, values[1:])):
                    conflict_monotone += 1

    coupling_series = 0
    coupling_monotone = 0
    for power in FUNCTIONAL_POWERS:
        for weight_1, weight_2 in WEIGHTS:
            for conflict in CONFLICT_DISTANCES:
                coupling_series += 1
                values = [
                    next(
                        row["recoverable_conflict_loss"]
                        for row in rows
                        if row["functional_power"] == power
                        and row["weight_1"] == weight_1
                        and row["weight_2"] == weight_2
                        and row["coupling"] == coupling
                        and row["conflict_distance"] == conflict
                    )
                    for coupling in COUPLINGS
                ]
                if all(a >= b - 1e-8 for a, b in zip(values, values[1:])):
                    coupling_monotone += 1

    mismatch_checks = []
    for functional_power, coupling_power in MISMATCHED_POWERS:
        baseline = compare_power_architectures(
            -0.5,
            1.2,
            weight_1=0.6,
            weight_2=2.2,
            coupling=0.9,
            architecture_cost=0.0,
            functional_power=functional_power,
            coupling_power=coupling_power,
        )
        threshold = baseline.recoverable_conflict_loss
        below = compare_power_architectures(
            -0.5,
            1.2,
            weight_1=0.6,
            weight_2=2.2,
            coupling=0.9,
            architecture_cost=0.9 * threshold,
            functional_power=functional_power,
            coupling_power=coupling_power,
        )
        above = compare_power_architectures(
            -0.5,
            1.2,
            weight_1=0.6,
            weight_2=2.2,
            coupling=0.9,
            architecture_cost=1.1 * threshold,
            functional_power=functional_power,
            coupling_power=coupling_power,
        )
        mismatch_checks.append(
            {
                "functional_power": functional_power,
                "coupling_power": coupling_power,
                "threshold": threshold,
                "below_threshold_preference": below.preferred_architecture,
                "above_threshold_preference": above.preferred_architecture,
            }
        )

    thresholds = [row["recoverable_conflict_loss"] for row in rows]
    return {
        "grid_n": len(rows),
        "positive_recoverable_gain_n": positive,
        "conflict_monotonic_series": {
            "passed": conflict_monotone,
            "total": conflict_series,
        },
        "coupling_monotonic_series": {
            "passed": coupling_monotone,
            "total": coupling_series,
        },
        "recoverable_gain_min": min(thresholds),
        "recoverable_gain_max": max(thresholds),
        "mismatched_curvature_checks": mismatch_checks,
        "declared_grid": {
            "functional_powers": FUNCTIONAL_POWERS,
            "weights": WEIGHTS,
            "couplings": COUPLINGS,
            "conflict_distances": CONFLICT_DISTANCES,
        },
    }


def main() -> None:
    readout = build_readout()
    print(json.dumps(readout, indent=2, sort_keys=True))

    output = Path("docs/TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json")
    output.write_text(json.dumps(readout, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
