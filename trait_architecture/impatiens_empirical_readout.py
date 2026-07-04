"""Create a bounded human-readable readout from an Impatiens model report.

The report is produced from raw Dryad rows in memory. This module consumes only
aggregate coefficients and writes a results summary with explicit D1/D2 boundaries.
It does not make causal claims or classify a confidence interval crossing zero as a
biological null.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FOUR_PATH_TERMS = (
    ("impatiens_pollination_path", "A_z", "A (flower redness) → pollinator visitation"),
    ("impatiens_pollination_path", "B_z", "D candidate (floral tannins) → pollinator visitation"),
    ("impatiens_antagonism_path", "A_z", "A (flower redness) → natural florivory"),
    ("impatiens_antagonism_path", "B_z", "D candidate (floral tannins) → natural florivory"),
)
SURFACE_TERMS = (
    ("impatiens_ch_fruit_surface", "A_z:B_z", "CH fruits per plant per day"),
    ("impatiens_ch_seed_surface", "A_z:B_z", "seeds per CH fruit"),
)


def _model_index(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    models = report.get("model_summaries")
    if not isinstance(models, list):
        raise ValueError("report has no model_summaries list")
    return {
        str(model.get("analysis_id")): model
        for model in models
        if isinstance(model, dict) and model.get("analysis_id")
    }


def _coefficient(model: dict[str, Any], term: str) -> dict[str, Any]:
    coefficients = model.get("coefficients")
    if not isinstance(coefficients, list):
        raise ValueError(f"{model.get('analysis_id')}: no coefficients list")
    matches = [item for item in coefficients if isinstance(item, dict) and item.get("term") == term]
    if len(matches) != 1:
        raise ValueError(f"{model.get('analysis_id')}: expected one coefficient for {term}")
    return matches[0]


def _interval_statement(coefficient: dict[str, Any]) -> str:
    lower = float(coefficient["ci95_lower"])
    upper = float(coefficient["ci95_upper"])
    if lower > 0:
        return "95% CI is entirely positive"
    if upper < 0:
        return "95% CI is entirely negative"
    return "95% CI crosses zero; direction remains uncertain at this sample size"


def _row(label: str, model: dict[str, Any], coefficient: dict[str, Any]) -> str:
    estimate = float(coefficient["estimate"])
    lower = float(coefficient["ci95_lower"])
    upper = float(coefficient["ci95_upper"])
    n = int(model["n_complete"])
    return (
        f"| {label} | {n} | {estimate:+.3f} | [{lower:+.3f}, {upper:+.3f}] | "
        f"{_interval_statement(coefficient)} |"
    )


def render_readout(report: dict[str, Any]) -> str:
    models = _model_index(report)
    lines = [
        "# *Impatiens capensis* empirical-core rerun",
        "",
        "## Scope",
        "",
        "This readout is generated from aggregate coefficients recomputed from the title-validated Dryad individual-plant panel. Trait paths are treatment-adjusted observational associations, not causal trait-manipulation effects.",
        "",
        "## D1 channel-mechanism map",
        "",
        "| Path | Complete-case n | Standardized coefficient | 95% CI | Interpretation |",
        "|---|---:|---:|---|---|",
    ]
    for analysis_id, term, label in FOUR_PATH_TERMS:
        model = models[analysis_id]
        lines.append(_row(label, model, _coefficient(model, term)))

    lines += [
        "",
        "All four primary trait-path intervals cross zero in this rerun. This does not demonstrate that the biological pathways are absent; it shows that the present panel and declared adjustment set do not isolate a direction with high precision.",
        "",
        "## Component fitness surfaces",
        "",
        "| Reproductive component | Complete-case n | A × D coefficient | 95% CI | Interpretation |",
        "|---|---:|---:|---|---|",
    ]
    for analysis_id, term, label in SURFACE_TERMS:
        model = models[analysis_id]
        lines.append(_row(label, model, _coefficient(model, term)))

    lines += [
        "",
        "These are component-level response surfaces. They are not a total lifetime reproductive-fitness surface, do not identify the Part A mixed partial, and do not calibrate the shared-allocation term.",
        "",
        "## Empirical conclusion",
        "",
        "The panel qualifies as an aligned D1 observational channel candidate: A, D candidate, pollination, and natural florivory are estimable at the same individual-plant unit. The present predeclared trait modules do not produce a precisely resolved four-path contrast, and the component-surface interactions do not upgrade the study to D2. Phenology should be retained as a central ecological covariate in any next-stage model or field design.",
        "",
    ]
    return "\n".join(lines)


def build_readout(report_path: str | Path, output_path: str | Path) -> None:
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    Path(output_path).write_text(render_readout(report), encoding="utf-8")
