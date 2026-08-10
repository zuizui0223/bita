"""Reanalyse the recovered 2019 nectar meta-analysis by response construct.

The published synthesis combines visit number, visit length, and volume
consumed under a broad pollinator-preference heading. This script preserves the
published secondary-metabolite corpus but separates those response constructs
before pooling. It is a broad empirical benchmark, not a strict bita B-trait
meta-analysis.

Usage:
    python scripts/reanalyze_parachnowitsch2019_outcome_lanes.py \
        PATH/04_Pollinator_preferences.csv OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

Z_975 = 1.959963984540054
LANE_NORMALIZATION = {"vist length": "visit length"}


def _load_reproduction_module():
    path = Path(__file__).with_name("reproduce_parachnowitsch2019_pollinator_meta.py")
    spec = importlib.util.spec_from_file_location("parachnowitsch2019_reproduction", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixed_pool(rows: list[dict[str, object]]) -> tuple[float, float]:
    weights = [1 / float(row["sampling_variance"]) for row in rows]
    pooled = sum(
        weight * float(row["hedges_g_first_minus_second"])
        for weight, row in zip(weights, rows)
    ) / sum(weights)
    return pooled, 1 / sum(weights)


def _dl(studies: list[dict[str, object]]) -> dict[str, float]:
    effects = [float(row["paper_effect_hedges_g"]) for row in studies]
    variances = [float(row["sampling_variance"]) for row in studies]
    weights = [1 / variance for variance in variances]
    fixed_mean = sum(w * y for w, y in zip(weights, effects)) / sum(weights)
    q_value = sum(w * (y - fixed_mean) ** 2 for w, y in zip(weights, effects))
    q_df = len(studies) - 1
    c_value = sum(weights) - sum(w * w for w in weights) / sum(weights)
    tau_squared = max(0.0, (q_value - q_df) / c_value) if c_value > 0 else 0.0
    random_weights = [1 / (variance + tau_squared) for variance in variances]
    pooled = sum(w * y for w, y in zip(random_weights, effects)) / sum(random_weights)
    pooled_se = math.sqrt(1 / sum(random_weights))
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
        raise ValueError(f"cannot write empty {path.name}")
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
    source_rows = module.read_secondary_metabolite_rows(args.worksheet_csv)
    for row in source_rows:
        row["outcome_lane"] = LANE_NORMALIZATION.get(str(row["outcome"]), str(row["outcome"]))

    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    paper_rows: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    loo_rows: list[dict[str, object]] = []

    by_lane: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in source_rows:
        by_lane[str(row["outcome_lane"])].append(row)

    for lane, lane_rows in sorted(by_lane.items()):
        by_paper: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in lane_rows:
            by_paper[str(row["paper"])].append(row)
        studies: list[dict[str, object]] = []
        for paper, rows in sorted(by_paper.items()):
            effect, variance = _fixed_pool(rows)
            study = {
                "outcome_lane": lane,
                "paper": paper,
                "effect_rows": len(rows),
                "pollinator_groups": ";".join(sorted({str(row["pollinator"]) for row in rows})),
                "paper_effect_hedges_g": effect,
                "sampling_variance": variance,
                "standard_error": math.sqrt(variance),
                "ci_low": effect - Z_975 * math.sqrt(variance),
                "ci_high": effect + Z_975 * math.sqrt(variance),
            }
            studies.append(study)
            paper_rows.append(study)

        if len(studies) >= 2:
            result = _dl(studies)
            status = "exploratory_random_effects" if len(studies) >= 3 else "two_study_context_only"
            summaries.append({
                "outcome_lane": lane,
                "effect_rows": len(lane_rows),
                "independent_papers": len(studies),
                "analysis_status": status,
                **result,
            })
            if len(studies) >= 3:
                for omitted in studies:
                    reduced = [study for study in studies if study["paper"] != omitted["paper"]]
                    diagnostics = _dl(reduced)
                    loo_rows.append({
                        "outcome_lane": lane,
                        "omitted_paper": omitted["paper"],
                        "remaining_papers": len(reduced),
                        **diagnostics,
                    })
        else:
            study = studies[0]
            summaries.append({
                "outcome_lane": lane,
                "effect_rows": len(lane_rows),
                "independent_papers": 1,
                "analysis_status": "single_study_not_pooled",
                "fixed_effect_mean": study["paper_effect_hedges_g"],
                "random_effects_mean": study["paper_effect_hedges_g"],
                "random_effects_standard_error": study["standard_error"],
                "ci_low": study["ci_low"],
                "ci_high": study["ci_high"],
                "tau_squared_DL": "",
                "Q": "",
                "Q_df": "",
                "I_squared_percent": "",
            })

    _write_csv(destination / "parachnowitsch2019_outcome_lane_paper_effects.csv", paper_rows)
    _write_csv(destination / "parachnowitsch2019_outcome_lane_summary.csv", summaries)
    _write_csv(destination / "parachnowitsch2019_outcome_lane_leave_one_out.csv", loo_rows)
    report = {
        "article_doi": "10.1093/aob/mcy132",
        "secondary_metabolite_effect_rows": len(source_rows),
        "outcome_lanes": summaries,
        "interpretation_boundary": (
            "Response constructs are separated, but paper-level summaries can still combine "
            "dose levels, pollinator taxa, and assays. The source corpus uses a broad secondary-"
            "metabolite definition rather than bita's strict flower-defence role. These results "
            "are an empirical benchmark and source map, not estimates of iota or W_AD."
        ),
    }
    (destination / "parachnowitsch2019_outcome_lane_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
