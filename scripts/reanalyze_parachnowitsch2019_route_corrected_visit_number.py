"""Reanalyse the 2019 visit-number evidence after correcting route and study mixing.

This script starts from the recovered Parachnowitsch, Manson & Sletvold (2019)
Pollinator preferences worksheet. It does not define a new model. It applies the
project's existing evidence rules to the one broad outcome lane that reaches
three papers:

- Adler & Irwin (2005): keep the source-audited 2004 natural-range row only;
- Jones & Agrawal (2016): keep the legitimate Bee row and exclude the
  Lepidoptera antagonist row;
- Manson et al. (2013): never count four dose rows as four studies; instead
  report one three-paper synthesis for each source-order dose contrast, plus
  one dependence-limited all-dose diagnostic matching the previous fixed
  within-paper convention.

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

SOURCE_ROWS = {
    "adler_2004": 3,
    "jones_bee": 17,
    "manson": (40, 41, 42, 43),
}


def _load_reproduction_module():
    path = Path(__file__).with_name("reproduce_parachnowitsch2019_pollinator_meta.py")
    spec = importlib.util.spec_from_file_location("parachnowitsch2019_reproduction", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixed_pool(effects: list[tuple[float, float]]) -> tuple[float, float]:
    weights = [1 / variance for _, variance in effects]
    pooled = sum(weight * effect for weight, (effect, _) in zip(weights, effects)) / sum(weights)
    return pooled, 1 / sum(weights)


def _dl(effects: list[tuple[float, float]]) -> dict[str, float]:
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
    pooled_variance = 1 / sum(random_weights)
    pooled_se = math.sqrt(pooled_variance)
    i_squared = max(0.0, (q_value - q_df) / q_value * 100) if q_value > 0 else 0.0
    return {
        "random_effects_hedges_g": pooled,
        "standard_error": pooled_se,
        "ci_low": pooled - Z_975 * pooled_se,
        "ci_high": pooled + Z_975 * pooled_se,
        "tau_squared_DL": tau_squared,
        "Q": q_value,
        "Q_df": float(q_df),
        "I_squared_percent": i_squared,
    }


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worksheet_csv")
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    module = _load_reproduction_module()
    rows = module.read_secondary_metabolite_rows(args.worksheet_csv)
    by_source_row = {int(row["source_row"]): row for row in rows}
    required = [SOURCE_ROWS["adler_2004"], SOURCE_ROWS["jones_bee"], *SOURCE_ROWS["manson"]]
    missing = [row_number for row_number in required if row_number not in by_source_row]
    if missing:
        raise ValueError(f"recovered worksheet is missing declared source rows: {missing}")

    adler = by_source_row[SOURCE_ROWS["adler_2004"]]
    jones = by_source_row[SOURCE_ROWS["jones_bee"]]
    manson_rows = [by_source_row[row_number] for row_number in SOURCE_ROWS["manson"]]

    declared_checks = [
        (adler, "Adler and Irwin 2005", "visit number", "Bee"),
        (jones, "Jones and Agrawal 2016", "visit number", "Bee"),
    ]
    for row, paper, outcome, pollinator in declared_checks:
        if (row["paper"], row["outcome"], row["pollinator"]) != (paper, outcome, pollinator):
            raise ValueError(f"source row {row['source_row']} no longer matches the declared study lane")
    for row in manson_rows:
        if (row["paper"], row["outcome"], row["pollinator"]) != (
            "Manson et al 2013", "visit number", "Bee"
        ):
            raise ValueError(f"Manson source row {row['source_row']} no longer matches the declared lane")

    selection_labels = {
        SOURCE_ROWS["adler_2004"]: "Adler_2004_natural_range_primary",
        SOURCE_ROWS["jones_bee"]: "Jones_legitimate_bee_only",
        SOURCE_ROWS["manson"][0]: "Manson_source_order_1_lower_dose",
        SOURCE_ROWS["manson"][1]: "Manson_source_order_2_lower_dose",
        SOURCE_ROWS["manson"][2]: "Manson_source_order_3_higher_dose",
        SOURCE_ROWS["manson"][3]: "Manson_source_order_4_higher_dose",
    }
    effects_out: list[dict[str, object]] = []
    for row_number in required:
        row = by_source_row[row_number]
        effects_out.append({
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

    base = [
        (float(adler["hedges_g_first_minus_second"]), float(adler["sampling_variance"])),
        (float(jones["hedges_g_first_minus_second"]), float(jones["sampling_variance"])),
    ]
    sensitivity: list[dict[str, object]] = []
    for index, row in enumerate(manson_rows, start=1):
        diagnostics = _dl(base + [(
            float(row["hedges_g_first_minus_second"]),
            float(row["sampling_variance"]),
        )])
        sensitivity.append({
            "scenario_id": f"manson_source_order_{index}",
            "adler_effect_choice": "2004 natural-range row only",
            "jones_effect_choice": "legitimate Bee row only; Lepidoptera antagonist excluded",
            "manson_effect_choice": f"source-order visit-number contrast {index} only",
            "manson_source_rows": int(row["source_row"]),
            "independent_papers": 3,
            **diagnostics,
            "interpretation": (
                "One Manson contrast is used; dose rows remain one study and are never counted "
                "as independent replication."
            ),
        })

    manson_fixed = _fixed_pool([
        (
            float(row["hedges_g_first_minus_second"]),
            float(row["sampling_variance"]),
        )
        for row in manson_rows
    ])
    diagnostics = _dl(base + [manson_fixed])
    sensitivity.append({
        "scenario_id": "manson_all_four_fixed_within_paper_diagnostic",
        "adler_effect_choice": "2004 natural-range row only",
        "jones_effect_choice": "legitimate Bee row only; Lepidoptera antagonist excluded",
        "manson_effect_choice": "inverse-variance fixed summary of all four visit-number rows",
        "manson_source_rows": "40;41;42;43",
        "independent_papers": 3,
        **diagnostics,
        "interpretation": (
            "Direct comparison with the previous within-paper pooling convention. The variance "
            "is dependence-limited because all four contrasts share one paper and control structure."
        ),
    })

    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    _write_csv(destination / "route_corrected_visit_number_effects.csv", effects_out)
    _write_csv(destination / "route_corrected_visit_number_sensitivity.csv", sensitivity)
    report = {
        "article_doi": "10.1093/aob/mcy132",
        "independent_papers": 3,
        "corrections": [
            "Adler and Irwin: retain the audited 2004 natural-range year only.",
            "Jones and Agrawal: retain the legitimate Bee row and exclude the Lepidoptera antagonist row.",
            "Manson et al.: retain one study cluster and expose dose-row choice as sensitivity.",
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
