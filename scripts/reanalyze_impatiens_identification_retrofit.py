"""Retrofit the *Impatiens capensis* public panel to the identification question.

This analysis deliberately does **not** estimate rho, iota, or kappa. The source
experiment randomized supplemental nectar robbing, florivory, and pollination;
it did not selectively exclude consumer channels, and A/D are observational
pre-treatment traits. The registered question is narrower:

    Does the observational A x D reproductive association change across
    randomized agent assignments?

Four reproductive readouts are analyzed with one unchanged hierarchical model:
CH fruit production, the deposited total-fruit production endpoint, seeds per CH
fruit, and a predeclared reconstructed mature-seed-output sensitivity. The latter
is computed row-wise as

    Mature_CH_Fruits_Per_Day * Average_Seeds_Per_CH_Fruit
  + Mature_CL_Fruits_Per_Day * Average_Seeds_Per_CL_Fruit

and is explicitly a derived proxy, not a deposited response variable or lifetime
fitness estimate. HC3 uncertainty is reported and no individual raw records are
written to output.

Usage:
    python scripts/reanalyze_impatiens_identification_retrofit.py \
        Processed_Data.csv OUT_JSON OUT_MD
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from trait_architecture.ols_hc3 import fit_ols_hc3


A_FIELD = "Early_Season_Flower_Redness"
D_FIELD = "Early_Season_Condensed_Tannins"
PHENOLOGY_FIELD = "Date_of_First_CH_Flower"
DERIVED_MATURE_SEED_OUTPUT = "__estimated_mature_seed_output_per_day__"
TREATMENTS = ("Robbing", "Florivory", "Pollination")
MODELS = (
    ("ch_fruits_per_plant_per_day", "Average_CH_Fruits_Per_Day", "log1p", "CH fruit-production component"),
    (
        "total_fruits_per_plant_per_day",
        "Total_Fruits_Per_Day",
        "log1p",
        "Deposited CH+CL total-fruit endpoint; more integrative than CH-only fruit production but not total lifetime seed fitness",
    ),
    ("seeds_per_ch_fruit", "Average_Seeds_Per_CH_Fruit", "identity", "Seeds per CH fruit component"),
    (
        "estimated_mature_seed_output_per_day",
        DERIVED_MATURE_SEED_OUTPUT,
        "log1p",
        "Derived CH+CL mature-seed-output proxy = mature fruit rate x average seeds per fruit summed across CH and CL; sensitivity only, not a deposited endpoint or lifetime fitness",
    ),
)

TERMS = (
    "Intercept",
    "A_z", "D_z", "Robbing_c", "Florivory_c", "Pollination_c",
    "A_z:D_z",
    "A_z:Robbing_c", "A_z:Florivory_c", "A_z:Pollination_c",
    "D_z:Robbing_c", "D_z:Florivory_c", "D_z:Pollination_c",
    "Robbing_c:Florivory_c", "Robbing_c:Pollination_c", "Florivory_c:Pollination_c",
    "A_z:D_z:Robbing_c", "A_z:D_z:Florivory_c", "A_z:D_z:Pollination_c",
    "Robbing_c:Florivory_c:Pollination_c",
    "Phenology_z",
)
TARGET_TERMS = (
    "A_z:D_z",
    "A_z:D_z:Robbing_c",
    "A_z:D_z:Florivory_c",
    "A_z:D_z:Pollination_c",
)


def _number(value: object, field: str) -> float:
    text = str(value or "").strip()
    if not text or text.upper() in {"NA", "N/A", "NAN", "."}:
        raise ValueError(f"missing {field}")
    number = float(text)
    if not math.isfinite(number):
        raise ValueError(f"non-finite {field}")
    return number


def _effect_code(value: object, field: str) -> float:
    label = str(value or "").strip().upper()
    if label == "N":
        return -0.5
    if label == "Y":
        return 0.5
    raise ValueError(f"{field} must be Y/N")


def _zscore(values: list[float]) -> list[float]:
    if len(values) < 2:
        raise ValueError("zscore needs at least two values")
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    if variance <= 0:
        raise ValueError("cannot zscore a constant variable")
    sd = math.sqrt(variance)
    return [(x - mean) / sd for x in values]


def _outcome_value(row: dict[str, str], outcome_field: str) -> float:
    if outcome_field != DERIVED_MATURE_SEED_OUTPUT:
        return _number(row.get(outcome_field), outcome_field)
    ch_mature = _number(row.get("Mature_CH_Fruits_Per_Day"), "Mature_CH_Fruits_Per_Day")
    ch_seeds = _number(row.get("Average_Seeds_Per_CH_Fruit"), "Average_Seeds_Per_CH_Fruit")
    cl_mature = _number(row.get("Mature_CL_Fruits_Per_Day"), "Mature_CL_Fruits_Per_Day")
    cl_seeds = _number(row.get("Average_Seeds_Per_CL_Fruit"), "Average_Seeds_Per_CL_Fruit")
    if min(ch_mature, ch_seeds, cl_mature, cl_seeds) < 0:
        raise ValueError("mature seed-output components must be non-negative")
    return ch_mature * ch_seeds + cl_mature * cl_seeds


def _prepare(rows: list[dict[str, str]], outcome_field: str, transform: str):
    complete = []
    omitted = 0
    for row in rows:
        try:
            a = _number(row.get(A_FIELD), A_FIELD)
            d = _number(row.get(D_FIELD), D_FIELD)
            y = _outcome_value(row, outcome_field)
            if transform == "log1p":
                if y < 0:
                    raise ValueError("log1p outcome must be non-negative")
                y = math.log1p(y)
            phenology = _number(row.get(PHENOLOGY_FIELD), PHENOLOGY_FIELD)
            r = _effect_code(row.get("Robbing"), "Robbing")
            f = _effect_code(row.get("Florivory"), "Florivory")
            p = _effect_code(row.get("Pollination"), "Pollination")
            complete.append((a, d, r, f, p, phenology, y))
        except (TypeError, ValueError):
            omitted += 1
    if not complete:
        raise ValueError(f"no complete rows for {outcome_field}")
    a_z = _zscore([r[0] for r in complete])
    d_z = _zscore([r[1] for r in complete])
    phen_z = _zscore([r[5] for r in complete])
    y_z = _zscore([r[6] for r in complete])

    prepared = []
    for i, raw in enumerate(complete):
        _, _, rob, flo, pol, _, _ = raw
        prepared.append({
            "A": a_z[i], "D": d_z[i], "R": rob, "F": flo, "P": pol,
            "Phenology": phen_z[i], "y": y_z[i],
        })
    return prepared, omitted


def _design_row(row: dict[str, float]) -> list[float]:
    a, d, r, f, p = row["A"], row["D"], row["R"], row["F"], row["P"]
    return [
        1.0,
        a, d, r, f, p,
        a*d,
        a*r, a*f, a*p,
        d*r, d*f, d*p,
        r*f, r*p, f*p,
        a*d*r, a*d*f, a*d*p,
        r*f*p,
        row["Phenology"],
    ]


def _cell_counts(records: list[dict[str, float]]) -> dict[str, int]:
    counter = Counter()
    for row in records:
        key = tuple("Y" if row[k] > 0 else "N" for k in ("R", "F", "P"))
        counter["/".join(key)] += 1
    return dict(sorted(counter.items()))


def analyze(rows: list[dict[str, str]]) -> dict[str, object]:
    summaries = []
    for analysis_id, outcome_field, transform, outcome_scope in MODELS:
        records, omitted = _prepare(rows, outcome_field, transform)
        result = fit_ols_hc3(
            [row["y"] for row in records],
            [_design_row(row) for row in records],
            TERMS,
        )
        coefficients = {c.term: asdict(c) for c in result.coefficients}
        targets = {term: coefficients[term] for term in TARGET_TERMS}
        counts = _cell_counts(records)
        summaries.append({
            "analysis_id": analysis_id,
            "outcome_field": outcome_field,
            "outcome_transform": transform,
            "outcome_scope": outcome_scope,
            "n_complete": result.n,
            "n_omitted": omitted,
            "parameter_count": result.parameter_count,
            "residual_df": result.residual_df,
            "r_squared": result.r_squared,
            "randomized_treatment_cell_counts": counts,
            "minimum_cell_n": min(counts.values()),
            "maximum_cell_n": max(counts.values()),
            "target_coefficients": targets,
            "all_coefficients": coefficients,
        })
    return {
        "analysis_id": "impatiens_2018_identification_retrofit_v2",
        "study": "Soper Gorden & Adler 2018, Impatiens capensis",
        "study_doi": "10.1002/ajb2.1182",
        "dataset_doi": "10.5061/dryad.0j96d17",
        "A_axis": A_FIELD,
        "D_axis": D_FIELD,
        "design": "observational A and D crossed analytically with randomized supplemental Robbing x Florivory x Pollination assignments",
        "registered_model": "hierarchical HC3 OLS with full R*F*P factorial, A/D-by-treatment lower-order terms, A:D, A:D:R, A:D:F, A:D:P, and pre-treatment phenology adjustment",
        "causal_boundary": (
            "Randomized treatment modifiers are causal assignment effect-modification contrasts, but A and D are observational traits. "
            "Robbing/florivory/pollination were simulated increases, not selective consumer exclusions. Results therefore do not identify rho_delta, iota_delta, M0_delta, or kappa_delta. "
            "Total_Fruits_Per_Day is a deposited CH+CL fruit endpoint but not total lifetime seed fitness. The reconstructed mature-seed-output readout multiplies deposited per-row mature fruit rates by average seeds per fruit and is a sensitivity proxy rather than a deposited response variable. Neither can be promoted to a causal escape estimate."
        ),
        "model_summaries": summaries,
    }


def _fmt(value: float) -> str:
    return f"{value:+.4f}"


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Impatiens 2018 identification retrofit v2",
        "",
        "## Question",
        "",
        "Can the strongest current public-data anchor go beyond a treatment-adjusted observational A×D association? We test whether that association changes across the source experiment's randomized supplemental robbing, florivory, and pollination assignments.",
        "",
        "This is **not** a rho/iota/kappa reconstruction. The randomized treatments simulated increased interaction intensity rather than selectively excluding consumer channels, and A/D themselves were not randomized.",
        "",
        "## Registered model",
        "",
        "The same hierarchical model is fit to three deposited reproductive readouts plus one derived sensitivity. The deposited readouts are CH fruit production, Total_Fruits_Per_Day, and seeds per CH fruit. The derived mature-seed-output proxy sums mature CH fruit rate × CH seeds/fruit and mature CL fruit rate × CL seeds/fruit. It is explicitly not a deposited response variable or lifetime-fitness measure.",
        "",
        "For each readout, standardized response is regressed on standardized early flower redness (A), standardized early floral condensed tannins (D), the full randomized Robbing × Florivory × Pollination factorial, all A- and D-by-treatment lower-order interactions needed for hierarchy, A×D, the three targeted A×D×treatment modifiers, and standardized pre-treatment flowering date. HC3 intervals are reported.",
        "",
        "Because treatments are effect-coded N=-0.5 / Y=+0.5, each A×D×treatment coefficient is the difference in the observational A×D slope between the randomized Y and N assignment levels, conditional on the declared model.",
        "",
        "## Results",
        "",
    ]
    for summary in report["model_summaries"]:  # type: ignore[index]
        lines += [
            f"### {summary['analysis_id']}",
            "",
            f"Outcome scope: {summary['outcome_scope']}.",
            "",
            f"Complete cases: {summary['n_complete']}; residual df: {summary['residual_df']}; randomized-cell n range: {summary['minimum_cell_n']}–{summary['maximum_cell_n']}.",
            "",
            "| target term | estimate | HC3 SE | 95% CI |",
            "|---|---:|---:|---:|",
        ]
        targets = summary["target_coefficients"]
        for term in TARGET_TERMS:
            c = targets[term]
            lines.append(
                f"| `{term}` | {_fmt(c['estimate'])} | {c['hc3_se']:.4f} | [{_fmt(c['ci95_lower'])}, {_fmt(c['ci95_upper'])}] |"
            )
        lines += ["", "Randomized treatment cell counts: " + ", ".join(f"{k}={v}" for k, v in summary["randomized_treatment_cell_counts"].items()) + ".", ""]

    lines += [
        "## Identification interpretation",
        "",
        "The A×D term is still an observational trait association. The A×D×Robbing, A×D×Florivory, and A×D×Pollination terms ask whether randomized supplemental agent assignments modify that association. Even if one of these terms is nonzero, it cannot be renamed rho or iota because the source treatments are intensity additions rather than selective present/excluded channel toggles.",
        "",
        "Total_Fruits_Per_Day closes a deposited endpoint-coverage gap. The reconstructed mature-seed-output model goes one step further by combining fruit maturation and seeds per fruit across CH and CL reproduction, but at the price of a stronger construction assumption and greater complete-case loss. It is a sensitivity analysis only.",
        "",
        "This retrofit therefore has a deliberately asymmetric role: it pushes one high-information public dataset as far as its deposited columns permit while preserving the point at which causal identification fails.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("processed_csv", type=Path)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("out_md", type=Path)
    args = parser.parse_args(argv)
    with args.processed_csv.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        rows = list(csv.DictReader(handle))
    report = analyze(rows)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    args.out_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "analysis_id": report["analysis_id"],
        "model_n": [m["n_complete"] for m in report["model_summaries"]],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
