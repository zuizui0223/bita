"""Render a bounded markdown readout for response-scale Impatiens models.

The input contains aggregate model output only. This renderer reports rate ratios or
odds ratios with their robust intervals and separates primary response-scale models
from explicitly labelled post-primary model-adequacy sensitivities.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FOCAL_TERMS = ("A_z", "D_z", "A_z:D_z")
ORDER = (
    "impatiens_pollinator_rate_quasi_poisson",
    "impatiens_pollinator_presence_hurdle_sensitivity",
    "impatiens_pollinator_positive_rate_hurdle_sensitivity",
    "impatiens_flower_level_florivory_fractional_logit",
    "impatiens_ch_seed_count_quasi_poisson",
)


def _index(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    summaries = report.get("model_summaries")
    if not isinstance(summaries, list):
        raise ValueError("model report has no model_summaries list")
    return {
        str(item.get("analysis_id")): item
        for item in summaries
        if isinstance(item, dict) and item.get("analysis_id")
    }


def _coefficient(model: dict[str, Any], term: str) -> dict[str, Any]:
    values = model.get("coefficients")
    if not isinstance(values, list):
        raise ValueError(f"{model.get('analysis_id')}: coefficients missing")
    matches = [item for item in values if isinstance(item, dict) and item.get("term") == term]
    if len(matches) != 1:
        raise ValueError(f"{model.get('analysis_id')}: expected one coefficient for {term}")
    return matches[0]


def _effect_name(family: str) -> str:
    if family == "poisson_log":
        return "rate ratio per 1 SD"
    if family == "fractional_logit":
        return "odds ratio per 1 SD"
    raise ValueError(f"unsupported family {family}")


def _ratio_interpretation(coefficient: dict[str, Any]) -> str:
    lower = float(coefficient["exp_ci95_lower"])
    upper = float(coefficient["exp_ci95_upper"])
    if lower > 1:
        return "robust 95% interval is above 1"
    if upper < 1:
        return "robust 95% interval is below 1"
    return "robust 95% interval crosses 1"


def _row(term_label: str, coefficient: dict[str, Any]) -> str:
    ratio = float(coefficient["exp_estimate"])
    lower = float(coefficient["exp_ci95_lower"])
    upper = float(coefficient["exp_ci95_upper"])
    return f"| {term_label} | {ratio:.3f} | [{lower:.3f}, {upper:.3f}] | {_ratio_interpretation(coefficient)} |"


def _append_model(lines: list[str], model: dict[str, Any]) -> None:
    family = str(model["family"])
    lines += [
        f"### {model['analysis_id']}",
        "",
        f"- role: `{model.get('analysis_role', 'unspecified')}`",
        f"- response: `{model['outcome_field']}` from `{model['source_table']}`",
        f"- {model['response_contract']}",
        f"- {model['inference_contract']}",
        f"- response records: {int(model['n_response_records'])}; clusters: {int(model['cluster_count'])}; omitted candidate records: {int(model['n_omitted'])}; filtered by rule: {int(model.get('n_filtered_by_rule', 0))}",
        f"- mean response: {float(model['mean_response']):.4f}; Pearson dispersion: {float(model['pearson_dispersion']):.3f}",
        f"- predictor standardization unit: {model['predictor_standardization_unit']}",
        "",
        f"| Predictor | {_effect_name(family)} | Robust 95% CI | Interpretation |",
        "|---|---:|---|---|",
    ]
    labels = {
        "A_z": "A: early flower redness",
        "D_z": "D candidate: floral tannins",
        "A_z:D_z": "A × D candidate",
    }
    for term in FOCAL_TERMS:
        try:
            coefficient = _coefficient(model, term)
        except ValueError:
            continue
        lines.append(_row(labels[term], coefficient))
    lines.append("")


def render_readout(report: dict[str, Any]) -> str:
    models = _index(report)
    lines = [
        "# *Impatiens capensis* response-scale analysis",
        "",
        "## Scope",
        "",
        "These are predeclared response-scale observational models recomputed from the title-validated Dryad archive. Raw records were used only in memory. Rate and odds ratios describe conditional associations, not causal effects of flower redness or floral tannins.",
        "",
        "## Primary response-scale models",
        "",
    ]
    for analysis_id in ORDER:
        model = models.get(analysis_id)
        if model is None or model.get("analysis_role") != "primary_response_scale_model":
            continue
        _append_model(lines, model)
    sensitivity_present = any(
        model.get("analysis_role") == "post_primary_model_adequacy_sensitivity"
        for model in models.values()
    )
    if sensitivity_present:
        lines += [
            "## Pollinator hurdle model-adequacy sensitivity",
            "",
            "The following two-part models are post-primary diagnostic sensitivities triggered by the primary rate model's zero mass and overdispersion. They must not replace the primary model or be used for result selection.",
            "",
        ]
        for analysis_id in ORDER:
            model = models.get(analysis_id)
            if model is None or model.get("analysis_role") != "post_primary_model_adequacy_sensitivity":
                continue
            _append_model(lines, model)
    lines += [
        "## Boundary of inference",
        "",
        "The primary pollinator-rate and florivory models together provide a response-scale D1 channel map in one system. The CH seed-count interaction is a reproductive-component surface, not total lifetime reproductive fitness. None of these estimates identifies the Part A mixed partial or the residual shared-allocation cost `c_AD`.",
        "",
    ]
    return "\n".join(lines)


def build_readout(report_path: str | Path, output_path: str | Path) -> None:
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    Path(output_path).write_text(render_readout(report), encoding="utf-8")
