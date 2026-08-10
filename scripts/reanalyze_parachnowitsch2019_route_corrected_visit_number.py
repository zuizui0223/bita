"""Reanalyse the 2019 visit-number lane after correcting route and dose mixing.

The fixed evidence rules are applied to the recovered Parachnowitsch, Manson &
Sletvold (2019) worksheet:

* Adler & Irwin (2005): retain the audited 2004 natural-range row;
* Jones & Agrawal (2016): retain the legitimate Bee row, not Lepidoptera;
* Manson et al. (2013): keep one study cluster and expose the 0.1, 1, 2 and
  4 microgram-per-microlitre contrasts separately.

No mathematical or biological definition is added.

Usage:
    python scripts/reanalyze_parachnowitsch2019_route_corrected_visit_number.py \
        PATH/04_Pollinator_preferences.csv OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
from pathlib import Path

Z_975 = 1.959963984540054
ADLER_ROW = 3
JONES_BEE_ROW = 17
MANSON_ROWS_AND_DOSES = ((40, 0.1), (41, 1.0), (42, 2.0), (43, 4.0))


def load_reproduction_module():
    path = Path(__file__).with_name("reproduce_parachnowitsch2019_pollinator_meta.py")
    spec = importlib.util.spec_from_file_location("parachnowitsch2019_reproduction", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixed_pool(effects: list[tuple[float, float]]) -> tuple[float, float]:
    weights = [1 / variance for _, variance in effects]
    return (
        sum(weight * effect for weight, (effect, _) in zip(weights, effects)) / sum(weights),
        1 / sum(weights),
    )


def dersimonian_laird(effects: list[tuple[float, float]]) -> dict[str, float]:
    values = [effect for effect, _ in effects]
    variances = [variance for _, variance in effects]
    weights = [1 / variance for variance in variances]
    fixed = sum(weight * value for weight, value in zip(weights, values)) / sum(weights)
    q_value = sum(weight * (value - fixed) ** 2 for weight, value in zip(weights, values))
    q_df = len(values) - 1
    c_value = sum(weights) - sum(weight**2 for weight in weights) / sum(weights)
    tau_squared = max(0.0, (q_value - q_df) / c_value) if c_value > 0 else 0.0
    random_weights = [1 / (variance + tau_squared) for variance in variances]
    pooled = sum(weight * value for weight, value in zip(random_weights, values)) / sum(random_weights)
    pooled_se = math.sqrt(1 / sum(random_weights))
    return {
        "random_effects_hedges_g": pooled,
        "standard_error": pooled_se,
        "ci_low": pooled - Z_975 * pooled_se,
        "ci_high": pooled + Z_975 * pooled_se,
        "tau_squared_DL": tau_squared,
        "Q": q_value,
        "Q_df": float(q_df),
        "I_squared_percent": max(0.0, (q_value - q_df) / q_value * 100) if q_value > 0 else 0.0,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def effect_pair(row: dict[str, object]) -> tuple[float, float]:
    return (
        float(row["hedges_g_first_minus_second"]),
        float(row["sampling_variance"]),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worksheet_csv")
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    source_rows = load_reproduction_module().read_secondary_metabolite_rows(args.worksheet_csv)
    by_row = {int(row["source_row"]): row for row in source_rows}
    required = [ADLER_ROW, JONES_BEE_ROW, *(row for row, _ in MANSON_ROWS_AND_DOSES)]
    missing = [row for row in required if row not in by_row]
    if missing:
        raise ValueError(f"recovered worksheet is missing declared source rows: {missing}")

    adler = by_row[ADLER_ROW]
    jones = by_row[JONES_BEE_ROW]
    manson = [(by_row[row_number], dose) for row_number, dose in MANSON_ROWS_AND_DOSES]

    checks = [
        (adler, "Adler and Irwin 2005", "visit number", "Bee"),
        (jones, "Jones and Agrawal 2016", "visit number", "Bee"),
        *[
            (row, "Manson et al 2013", "visit number", "Bee")
            for row, _ in manson
        ],
    ]
    for row, paper, outcome, pollinator in checks:
        observed = (row["paper"], row["outcome"], row["pollinator"])
        if observed != (paper, outcome, pollinator):
            raise ValueError(f"source row {row['source_row']} no longer matches the declared lane")

    selection_labels = {
        ADLER_ROW: "Adler_2004_natural_range_primary",
        JONES_BEE_ROW: "Jones_legitimate_bee_only",
        40: "Manson_0p1_ug_per_uL",
        41: "Manson_1_ug_per_uL",
        42: "Manson_2_ug_per_uL",
        43: "Manson_4_ug_per_uL",
    }
    effect_rows: list[dict[str, object]] = []
    for row_number in required:
        row = by_row[row_number]
        effect_rows.append({
            "source_row": row_number,
            "paper": row["paper"],
            "location": row["location"],
            "outcome_lane": row["outcome"],
            "consumer_role": row["pollinator"],
            "mean_first": row["mean_first"],
            "sd_first": row["sd_first"],
            "n_first": row["n_first"],
            "mean_second": row["mean_second"],
            "sd_second": row["sd_second"],
            "n_second": row["n_second"],
            "hedges_g_first_minus_second": row["hedges_g_first_minus_second"],
            "sampling_variance": row["sampling_variance"],
            "standard_error": row["standard_error"],
            "selection_role": selection_labels[row_number],
        })

    base = [effect_pair(adler), effect_pair(jones)]
    sensitivity: list[dict[str, object]] = []
    for row, dose in manson:
        diagnostics = dersimonian_laird(base + [effect_pair(row)])
        sensitivity.append({
            "scenario_id": f"manson_{str(dose).replace('.', 'p')}_ug_per_uL",
            "adler_effect_choice": "2004 natural-range row only",
            "jones_effect_choice": "legitimate Bee row only; Lepidoptera antagonist excluded",
            "manson_effect_choice": f"{dose:g} microgram per microlitre versus 0 control",
            "manson_source_rows": int(row["source_row"]),
            "independent_papers": 3,
            **diagnostics,
            "interpretation": (
                "One Manson contrast is used; dose rows remain one study and are never counted "
                "as independent replication."
            ),
        })

    manson_summary = fixed_pool([effect_pair(row) for row, _ in manson])
    sensitivity.append({
        "scenario_id": "manson_all_four_fixed_within_paper_diagnostic",
        "adler_effect_choice": "2004 natural-range row only",
        "jones_effect_choice": "legitimate Bee row only; Lepidoptera antagonist excluded",
        "manson_effect_choice": "inverse-variance fixed summary of all four visit-number rows",
        "manson_source_rows": "40;41;42;43",
        "independent_papers": 3,
        **dersimonian_laird(base + [manson_summary]),
        "interpretation": (
            "Direct comparison with the previous within-paper pooling convention. The variance "
            "is dependence-limited because all four contrasts share one paper and control structure."
        ),
    })

    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    write_csv(destination / "route_corrected_visit_number_effects.csv", effect_rows)
    write_csv(destination / "route_corrected_visit_number_sensitivity.csv", sensitivity)
    report = {
        "article_doi": "10.1093/aob/mcy132",
        "independent_papers": 3,
        "manson_doses_microgram_per_microlitre": [dose for _, dose in MANSON_ROWS_AND_DOSES],
        "corrections": [
            "Adler and Irwin: retain the audited 2004 natural-range year only.",
            "Jones and Agrawal: retain the legitimate Bee row and exclude the Lepidoptera antagonist row.",
            "Manson et al.: retain one study cluster and expose the 0.1, 1, 2, and 4 microgram-per-microlitre contrasts as sensitivity.",
        ],
        "all_scenario_intervals_include_zero": all(
            float(row["ci_low"]) <= 0 <= float(row["ci_high"]) for row in sensitivity
        ),
        "interpretation_boundary": (
            "This is an exploratory route-correction sensitivity for a defence-associated "
            "visit-number lane. It does not estimate iota or W_AD, and the Manson all-dose "
            "summary is diagnostic rather than a dependence-corrected canonical effect."
        ),
    }
    (destination / "route_corrected_visit_number_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
