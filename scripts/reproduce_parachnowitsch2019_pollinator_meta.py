"""Reproduce the published secondary-metabolite pollinator-preference synthesis.

This utility reads the ``Pollinator preferences`` worksheet exported from the
Parachnowitsch, Manson & Sletvold (2019) supplement (doi:10.1093/aob/mcy132).
It reproduces the broad published secondary-metabolite summary without
reclassifying any row as a strict defence-trait effect for bita.

The worksheet contains duplicate ``SD`` and ``N`` column names, so values are
read by their declared column positions rather than by a dictionary header.
Good et al. (2014) rows are excluded because the published forest plot reports
63 secondary-metabolite effects from nine studies, while including those nine
rows would yield 72 effects from ten labelled studies.

Usage:
    python scripts/reproduce_parachnowitsch2019_pollinator_meta.py \
        PATH/04_Pollinator_preferences.csv OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable

Z_975 = 1.959963984540054
EXPECTED_EFFECT_ROWS = 63
EXPECTED_STUDIES = 9
EXCLUDED_LABELLED_PAPER = "Good et al 2014"


def _float(value: str, field: str, row_number: int) -> float:
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"row {row_number}: {field} must be numeric") from error
    if not math.isfinite(number):
        raise ValueError(f"row {row_number}: {field} must be finite")
    return number


def _hedges_g(
    mean_first: float,
    sd_first: float,
    n_first: float,
    mean_second: float,
    sd_second: float,
    n_second: float,
) -> tuple[float, float]:
    """Return Hedges g and its conventional independent-groups variance."""
    if min(n_first, n_second) <= 1:
        raise ValueError("Hedges g requires both group sizes > 1")
    if min(sd_first, sd_second) < 0:
        raise ValueError("standard deviations must be non-negative")
    df = n_first + n_second - 2
    pooled_variance = (
        (n_first - 1) * sd_first**2 + (n_second - 1) * sd_second**2
    ) / df
    if pooled_variance <= 0:
        raise ValueError("pooled variance must be positive")
    d_value = (mean_first - mean_second) / math.sqrt(pooled_variance)
    correction = 1 - 3 / (4 * df - 1)
    g_value = correction * d_value
    variance = (n_first + n_second) / (n_first * n_second) + g_value**2 / (2 * df)
    return g_value, variance


def read_secondary_metabolite_rows(path: str | Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        expected_header = [
            "Paper", "Location", "Factor investigated", "Variable measured",
            "Pollinator", "Mean Control ", "SD", "N", "Mean Treatment", "SD", "N",
        ]
        if header != expected_header:
            raise ValueError(f"unexpected worksheet header: {header!r}")
        for row_number, values in enumerate(reader, start=2):
            if len(values) < 11:
                raise ValueError(f"row {row_number}: expected 11 columns")
            paper, location, factor, outcome, pollinator = values[:5]
            if factor != "secondary metabolites" or paper == EXCLUDED_LABELLED_PAPER:
                continue
            mean_first = _float(values[5], "first mean", row_number)
            sd_first = _float(values[6], "first SD", row_number)
            n_first = _float(values[7], "first N", row_number)
            mean_second = _float(values[8], "second mean", row_number)
            sd_second = _float(values[9], "second SD", row_number)
            n_second = _float(values[10], "second N", row_number)
            effect, variance = _hedges_g(
                mean_first, sd_first, n_first, mean_second, sd_second, n_second
            )
            rows.append({
                "source_row": row_number,
                "paper": paper,
                "location": location,
                "outcome": outcome,
                "pollinator": pollinator,
                "mean_first": mean_first,
                "sd_first": sd_first,
                "n_first": n_first,
                "mean_second": mean_second,
                "sd_second": sd_second,
                "n_second": n_second,
                "hedges_g_first_minus_second": effect,
                "sampling_variance": variance,
                "standard_error": math.sqrt(variance),
            })
    if len(rows) != EXPECTED_EFFECT_ROWS:
        raise ValueError(
            f"expected {EXPECTED_EFFECT_ROWS} published effect rows, found {len(rows)}"
        )
    return rows


def fixed_pool(rows: Iterable[dict[str, object]]) -> tuple[float, float]:
    rows = list(rows)
    weights = [1 / float(row["sampling_variance"]) for row in rows]
    pooled = sum(
        weight * float(row["hedges_g_first_minus_second"])
        for weight, row in zip(weights, rows)
    ) / sum(weights)
    variance = 1 / sum(weights)
    return pooled, variance


def pool_within_study(rows: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["paper"])].append(row)
    if len(grouped) != EXPECTED_STUDIES:
        raise ValueError(f"expected {EXPECTED_STUDIES} studies, found {len(grouped)}")
    studies: list[dict[str, object]] = []
    for paper, paper_rows in sorted(grouped.items()):
        pooled, variance = fixed_pool(paper_rows)
        studies.append({
            "paper": paper,
            "effect_rows": len(paper_rows),
            "outcomes": ";".join(sorted({str(row["outcome"]) for row in paper_rows})),
            "pollinator_groups": ";".join(
                sorted({str(row["pollinator"]) for row in paper_rows})
            ),
            "fixed_effect_hedges_g": pooled,
            "sampling_variance": variance,
            "standard_error": math.sqrt(variance),
            "ci_low": pooled - Z_975 * math.sqrt(variance),
            "ci_high": pooled + Z_975 * math.sqrt(variance),
        })
    return studies


def dersimonian_laird(studies: Iterable[dict[str, object]]) -> dict[str, float]:
    studies = list(studies)
    variances = [float(study["sampling_variance"]) for study in studies]
    effects = [float(study["fixed_effect_hedges_g"]) for study in studies]
    weights = [1 / variance for variance in variances]
    fixed_mean = sum(w * y for w, y in zip(weights, effects)) / sum(weights)
    q_value = sum(w * (y - fixed_mean) ** 2 for w, y in zip(weights, effects))
    q_df = len(studies) - 1
    c_value = sum(weights) - sum(w**2 for w in weights) / sum(weights)
    tau_squared = max(0.0, (q_value - q_df) / c_value) if c_value > 0 else 0.0
    random_weights = [1 / (variance + tau_squared) for variance in variances]
    pooled = sum(w * y for w, y in zip(random_weights, effects)) / sum(random_weights)
    pooled_variance = 1 / sum(random_weights)
    pooled_se = math.sqrt(pooled_variance)
    i_squared = max(0.0, (q_value - q_df) / q_value * 100) if q_value > 0 else 0.0
    return {
        "fixed_effect_mean": fixed_mean,
        "random_effects_mean": pooled,
        "random_effects_standard_error": pooled_se,
        "ci_low": pooled - Z_975 * pooled_se,
        "ci_high": pooled + Z_975 * pooled_se,
        "tau_squared_DL": tau_squared,
        "Q": q_value,
        "Q_df": float(q_df),
        "I_squared_percent": i_squared,
    }


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError("cannot write empty CSV")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worksheet_csv")
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    rows = read_secondary_metabolite_rows(args.worksheet_csv)
    studies = pool_within_study(rows)
    summary = {
        "article_doi": "10.1093/aob/mcy132",
        "effect_metric": "Hedges_g_first_worksheet_mean_minus_second_worksheet_mean",
        "published_secondary_metabolite_effect_rows": len(rows),
        "published_independent_studies": len(studies),
        "excluded_labelled_rows": {
            "paper": EXCLUDED_LABELLED_PAPER,
            "row_count": 9,
            "reason": (
                "The published forest plot reports 63 secondary-metabolite effects from nine "
                "studies; retaining these labelled rows would produce 72 effects from ten studies."
            ),
        },
        "study_dependence_handling": (
            "Inverse-variance fixed pooling within each paper, followed by a "
            "DerSimonian-Laird random-effects synthesis across paper-level summaries."
        ),
        "result": dersimonian_laird(studies),
        "interpretation_boundary": (
            "This reproduces the broad published secondary-metabolite synthesis. Worksheet "
            "labels and headers do not establish bita's strict flower-defence role or safe "
            "biological treatment orientation. No row is canonical until re-audited against "
            "the primary study, outcome lane, and independence rules."
        ),
    }
    _write_csv(destination / "parachnowitsch2019_row_effects.csv", rows)
    _write_csv(destination / "parachnowitsch2019_study_effects.csv", studies)
    (destination / "parachnowitsch2019_reproduction.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
