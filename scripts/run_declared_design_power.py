"""Simulate the pre-registered moderator design and report its detection rates.

Usage:
    python scripts/run_declared_design_power.py artifacts/supplement/design_power [replicates]

The grid crosses declared cluster counts, level contrasts on the log-response-ratio
scale, and between-cluster heterogeneity. Every replicate is pushed through the
deployed analysis functions, so the reported rates are properties of the code that
will run on the real extraction, not of a separate derivation.

Null scenarios (zero true contrast) are included so the table reports calibration
alongside power: a detection rate in a null row is a false-positive rate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from trait_architecture.broad_meta_analysis import write_csv_rows
from trait_architecture.design_power import (
    POWER_OUTPUT_FIELDS,
    PowerScenario,
    declared_scenario_grid,
    minimum_adequate_cluster_count,
    run_power_grid,
)


def null_scenario_grid() -> list[PowerScenario]:
    return [
        PowerScenario(
            scenario_id=f"null_k{clusters}_tau{tau:.2f}".replace(".", "p"),
            clusters_per_level=clusters,
            level_contrast=0.0,
            between_cluster_sd=tau,
        )
        for clusters in (3, 5, 8, 12)
        for tau in (0.0, 0.25, 0.50)
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir")
    parser.add_argument("replicates", nargs="?", type=int, default=2000)
    args = parser.parse_args(argv)

    destination = Path(args.out_dir)
    destination.mkdir(parents=True, exist_ok=True)

    power_rows = run_power_grid(declared_scenario_grid(), replicates=args.replicates)
    null_rows = run_power_grid(null_scenario_grid(), replicates=args.replicates, seed=770001)
    write_csv_rows(destination / "declared_design_power.csv", POWER_OUTPUT_FIELDS, power_rows)
    write_csv_rows(destination / "declared_design_null_calibration.csv", POWER_OUTPUT_FIELDS, null_rows)

    summary = {
        "replicates": args.replicates,
        "minimum_adequate_clusters_per_level": {
            f"contrast_{contrast}_tau_{tau}": minimum_adequate_cluster_count(power_rows, contrast, tau)
            for contrast in (-0.35, -0.69, -1.10)
            for tau in (0.0, 0.25, 0.50)
        },
        "max_meta_regression_false_positive_rate": max(
            float(row["meta_regression_contrast_power"]) for row in null_rows
        ),
        "max_false_direction_reversal_rate": max(
            float(row["direction_reversal_detection_rate"]) for row in null_rows
        ),
        "max_fixed_effect_q_between_false_positive_rate": max(
            float(row["q_between_fixed_effect_rejection_rate"]) for row in null_rows
        ),
        "interpretation_boundary": (
            "Detection rates are properties of the declared design and the deployed code under a "
            "declared generative model. They are not evidence about nature and do not estimate any "
            "route effect."
        ),
    }
    (destination / "declared_design_power_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
