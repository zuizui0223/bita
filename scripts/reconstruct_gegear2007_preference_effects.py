"""Reconstruct source-reported Gegear et al. (2007) preference effects.

Table 2 reports one-sample t tests of the proportion of visits to the lower-
gelsemine option against 0.5. Effects are re-oriented so negative values mean
that the higher-gelsemine option received fewer visits. All five assays remain
dependent effects from one study cluster.

Usage:
    python scripts/reconstruct_gegear2007_preference_effects.py OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

Z_975 = 1.959963984540054

ASSAYS = (
    {
        "assay": "1A", "low_gelsemine_ng_per_uL": 0, "high_gelsemine_ng_per_uL": 50,
        "low_sucrose_percent": 30, "high_sucrose_percent": 30,
        "mean_low_gelsemine_visit_proportion": 0.86, "sem_proportion": 0.04,
        "reported_t_low_vs_half": 7.932, "reported_df": 12,
        "ecological_context": "equal_sugar_middle_natural_gelsemine",
    },
    {
        "assay": "1B", "low_gelsemine_ng_per_uL": 0, "high_gelsemine_ng_per_uL": 50,
        "low_sucrose_percent": 50, "high_sucrose_percent": 50,
        "mean_low_gelsemine_visit_proportion": 0.76, "sem_proportion": 0.09,
        "reported_t_low_vs_half": 2.54, "reported_df": 10,
        "ecological_context": "equal_high_sugar_middle_natural_gelsemine",
    },
    {
        "assay": "1C", "low_gelsemine_ng_per_uL": 0, "high_gelsemine_ng_per_uL": 5,
        "low_sucrose_percent": 30, "high_sucrose_percent": 30,
        "mean_low_gelsemine_visit_proportion": 0.84, "sem_proportion": 0.07,
        "reported_t_low_vs_half": 4.89, "reported_df": 8,
        "ecological_context": "equal_sugar_lowest_natural_gelsemine",
    },
    {
        "assay": "2", "low_gelsemine_ng_per_uL": 0, "high_gelsemine_ng_per_uL": 50,
        "low_sucrose_percent": 30, "high_sucrose_percent": 50,
        "mean_low_gelsemine_visit_proportion": 0.50, "sem_proportion": 0.10,
        "reported_t_low_vs_half": -0.149, "reported_df": 10,
        "ecological_context": "high_gelsemine_compensated_by_higher_sucrose",
    },
    {
        "assay": "3", "low_gelsemine_ng_per_uL": 50, "high_gelsemine_ng_per_uL": 125,
        "low_sucrose_percent": 30, "high_sucrose_percent": 30,
        "mean_low_gelsemine_visit_proportion": 0.82, "sem_proportion": 0.04,
        "reported_t_low_vs_half": 7.04, "reported_df": 8,
        "ecological_context": "equal_sugar_middle_vs_high_natural_gelsemine",
    },
)


def one_sample_hedges_g_from_t(t_value: float, df: int) -> tuple[float, float]:
    """Return re-oriented g and SE using the repository's existing t-to-g rule."""
    n = df + 1
    d_value = -t_value / math.sqrt(n)
    correction = 1 - 3 / (4 * df - 1)
    g_value = correction * d_value
    variance = correction**2 * (1 / n + d_value**2 / (2 * df))
    return g_value, math.sqrt(variance)


def effect_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in ASSAYS:
        df = int(source["reported_df"])
        n = df + 1
        effect, standard_error = one_sample_hedges_g_from_t(
            float(source["reported_t_low_vs_half"]), df
        )
        rows.append({
            "effect_id": f"Gegear_2007_assay_{source['assay']}",
            "study_id": "Gegear_Manson_Thomson_2007",
            "doi": "10.1111/j.1461-0248.2007.01027.x",
            "assay": source["assay"],
            "ecological_context": source["ecological_context"],
            "low_gelsemine_ng_per_uL": source["low_gelsemine_ng_per_uL"],
            "high_gelsemine_ng_per_uL": source["high_gelsemine_ng_per_uL"],
            "low_sucrose_percent": source["low_sucrose_percent"],
            "high_sucrose_percent": source["high_sucrose_percent"],
            "outcome_lane": "binary_choice_preference",
            "n_bees": n,
            "mean_high_gelsemine_visit_percent": 100 * (
                1 - float(source["mean_low_gelsemine_visit_proportion"])
            ),
            "sem_percent": 100 * float(source["sem_proportion"]),
            "reported_t_for_low_gelsemine": source["reported_t_low_vs_half"],
            "reported_df": df,
            "effect_metric": "one_sample_hedges_g_from_reported_t_on_arcsin_proportion",
            "effect_estimate": effect,
            "effect_se": standard_error,
            "ci_low": effect - Z_975 * standard_error,
            "ci_high": effect + Z_975 * standard_error,
            "effect_orientation": "negative_means_higher_gelsemine_received_fewer_visits",
            "source_locator": "author PDF Table 1 and Table 2, pages 377-378",
            "b_role_status": "linked_primary_verified_same_Gelsemium_nectar_defence_system",
            "reconstruction_status": "source_verified_from_reported_t_df_and_assay_conditions",
            "independence_cluster": "Gegear_2007_Gelsemium",
            "primary_pool_eligible": "no_single_primary_contrast_predeclared",
            "notes": (
                "All assays are dependent effects from one bee-choice study. The reported t test "
                "used arcsin-transformed proportions; raw means and SE are shown for interpretation."
            ),
        })
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    rows = effect_rows()
    write_csv(destination / "gegear2007_preference_effects.csv", rows)
    report = {
        "article_doi": "10.1111/j.1461-0248.2007.01027.x",
        "effect_rows": len(rows),
        "independent_study_clusters": 1,
        "all_equal_sugar_assays_negative": all(
            float(row["effect_estimate"]) < 0
            for row in rows
            if float(row["low_sucrose_percent"]) == float(row["high_sucrose_percent"])
        ),
        "higher_sugar_compensation_assay_includes_zero": (
            float(rows[3]["ci_low"]) <= 0 <= float(rows[3]["ci_high"])
        ),
        "interpretation_boundary": (
            "Source-complete preference effects from one dependent study cluster. No pooled "
            "cross-study estimate is produced, and no effect is interpreted as iota or W_AD."
        ),
    }
    (destination / "gegear2007_preference_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
