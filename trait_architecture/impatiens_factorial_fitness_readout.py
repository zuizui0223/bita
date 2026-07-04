"""Render a bounded markdown readout for randomized Impatiens fitness models.

The input contains aggregate coefficients from a full 2x2x2 randomized treatment
factorial. This renderer reports treatment-assignment contrasts separately from the
observational trait-path models and preserves the component-fitness boundary.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MAIN_TERMS = (
    ("Robbing_c", "Supplemental robbing assignment"),
    ("Florivory_c", "Supplemental florivory assignment"),
    ("Pollination_c", "Supplemental pollination assignment"),
)
INTERACTION_TERMS = (
    ("Robbing_c:Florivory_c", "Robbing × florivory"),
    ("Robbing_c:Pollination_c", "Robbing × pollination"),
    ("Florivory_c:Pollination_c", "Florivory × pollination"),
    ("Robbing_c:Florivory_c:Pollination_c", "Robbing × florivory × pollination"),
)


def _index(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    summaries = report.get("model_summaries")
    if not isinstance(summaries, list):
        raise ValueError("factorial report has no model_summaries list")
    return {
        str(item.get("analysis_id")): item
        for item in summaries
        if isinstance(item, dict) and item.get("analysis_id")
    }


def _coefficient(model: dict[str, Any], term: str) -> dict[str, Any]:
    coefficients = model.get("coefficients")
    if not isinstance(coefficients, list):
        raise ValueError(f"{model.get('analysis_id')}: coefficients missing")
    matches = [item for item in coefficients if isinstance(item, dict) and item.get("term") == term]
    if len(matches) != 1:
        raise ValueError(f"{model.get('analysis_id')}: expected one coefficient for {term}")
    return matches[0]


def _interpretation(coefficient: dict[str, Any]) -> str:
    lower = float(coefficient["ci95_lower"])
    upper = float(coefficient["ci95_upper"])
    if lower > 0:
        return "HC3 95% CI is entirely positive"
    if upper < 0:
        return "HC3 95% CI is entirely negative"
    return "HC3 95% CI crosses zero"


def _row(label: str, coefficient: dict[str, Any]) -> str:
    estimate = float(coefficient["estimate"])
    lower = float(coefficient["ci95_lower"])
    upper = float(coefficient["ci95_upper"])
    return f"| {label} | {estimate:+.3f} | [{lower:+.3f}, {upper:+.3f}] | {_interpretation(coefficient)} |"


def _append_model(lines: list[str], model: dict[str, Any]) -> None:
    lines += [
        f"## {model['analysis_id']}",
        "",
        f"- response: `{model['outcome_field']}`; transform: `{model['outcome_transform']}`",
        f"- {model['outcome_definition']}",
        f"- {model['interpretation']}",
        f"- complete-case n: {int(model['n_complete'])}; omitted: {int(model['n_omitted'])}; R²: {float(model['r_squared']):.3f}",
        f"- {model['treatment_coding']}",
        "",
        "### Assigned-treatment contrasts",
        "",
        "| Treatment assignment | Standardized coefficient | HC3 95% CI | Interpretation |",
        "|---|---:|---|---|",
    ]
    for term, label in MAIN_TERMS:
        lines.append(_row(label, _coefficient(model, term)))
    lines += [
        "",
        "### Factorial interaction checks",
        "",
        "| Interaction | Standardized coefficient | HC3 95% CI | Interpretation |",
        "|---|---:|---|---|",
    ]
    for term, label in INTERACTION_TERMS:
        lines.append(_row(label, _coefficient(model, term)))
    lines.append("")


def render_readout(report: dict[str, Any]) -> str:
    models = _index(report)
    lines = [
        "# *Impatiens capensis* randomized treatment effects on reproductive components",
        "",
        "## Design and scope",
        "",
        f"- design: {report['design']}",
        f"- treatment coding: {report['treatment_coding']}",
        "- treatment coefficients are randomized assignment contrasts within the stated factorial design; they are not causal effects of flower redness or floral tannins.",
        "",
    ]
    for analysis_id in (
        "impatiens_factorial_ch_fruit_rate",
        "impatiens_factorial_ch_seed_per_fruit",
    ):
        _append_model(lines, models[analysis_id])
    lines += [
        "## Boundary of inference",
        "",
        "These outcomes are reproductive components rather than total lifetime fitness. The factorial model can test downstream experimental consequences of florivory, robbing, and supplemental pollination in this system, but it does not identify the Part A A×D mixed partial or the shared-allocation term `c_AD`.",
        "",
    ]
    return "\n".join(lines)


def build_readout(report_path: str | Path, output_path: str | Path) -> None:
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    Path(output_path).write_text(render_readout(report), encoding="utf-8")
