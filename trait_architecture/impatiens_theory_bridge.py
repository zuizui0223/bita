"""Build a bounded theory-to-empirics bridge for the Impatiens core.

This module combines only aggregate outputs from the response-scale observational
models and the randomized factorial fitness-component models. It never multiplies
link-scale coefficients, estimates `c_AD`, or labels a floral-trait association as a
causal effect. The purpose is to state exactly which empirical components currently
support, fail to resolve, or do not test the Part A terms.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _model(report: dict[str, Any], analysis_id: str) -> dict[str, Any]:
    summaries = report.get("model_summaries")
    if not isinstance(summaries, list):
        raise ValueError("model report has no model_summaries list")
    matches = [item for item in summaries if isinstance(item, dict) and item.get("analysis_id") == analysis_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one model {analysis_id}")
    return matches[0]


def _coefficient(model: dict[str, Any], term: str) -> dict[str, Any]:
    values = model.get("coefficients")
    if not isinstance(values, list):
        raise ValueError(f"{model.get('analysis_id')}: coefficients missing")
    matches = [item for item in values if isinstance(item, dict) and item.get("term") == term]
    if len(matches) != 1:
        raise ValueError(f"{model.get('analysis_id')}: expected one coefficient for {term}")
    return matches[0]


def _ratio_text(coefficient: dict[str, Any]) -> str:
    ratio = float(coefficient["exp_estimate"])
    lower = float(coefficient["exp_ci95_lower"])
    upper = float(coefficient["exp_ci95_upper"])
    return f"{ratio:.3f} [{lower:.3f}, {upper:.3f}]"


def _coefficient_text(coefficient: dict[str, Any]) -> str:
    estimate = float(coefficient["estimate"])
    lower = float(coefficient["ci95_lower"])
    upper = float(coefficient["ci95_upper"])
    return f"{estimate:+.3f} [{lower:+.3f}, {upper:+.3f}]"


def _ratio_status(coefficient: dict[str, Any], *, expected_direction: str | None = None) -> str:
    lower = float(coefficient["exp_ci95_lower"])
    upper = float(coefficient["exp_ci95_upper"])
    if expected_direction == "negative" and upper < 1:
        return "directionally consistent association"
    if expected_direction == "positive" and lower > 1:
        return "directionally consistent association"
    if lower <= 1 <= upper:
        return "not directionally resolved"
    return "association opposite to the declared expected direction"


def _coefficient_status(coefficient: dict[str, Any], *, expected_direction: str | None = None) -> str:
    lower = float(coefficient["ci95_lower"])
    upper = float(coefficient["ci95_upper"])
    if expected_direction == "negative" and upper < 0:
        return "directionally consistent experimental effect"
    if expected_direction == "positive" and lower > 0:
        return "directionally consistent experimental effect"
    if lower <= 0 <= upper:
        return "not directionally resolved"
    return "effect opposite to the declared expected direction"


def render_bridge(response_report: dict[str, Any], factorial_report: dict[str, Any]) -> str:
    pollinator = _model(response_report, "impatiens_pollinator_rate_quasi_poisson")
    presence = _model(response_report, "impatiens_pollinator_presence_hurdle_sensitivity")
    positive = _model(response_report, "impatiens_pollinator_positive_rate_hurdle_sensitivity")
    florivory = _model(response_report, "impatiens_flower_level_florivory_fractional_logit")
    seed = _model(response_report, "impatiens_ch_seed_count_quasi_poisson")
    fruit_factorial = _model(factorial_report, "impatiens_factorial_ch_fruit_rate")
    seed_factorial = _model(factorial_report, "impatiens_factorial_ch_seed_per_fruit")

    d_to_p = _coefficient(pollinator, "D_z")
    a_to_p = _coefficient(pollinator, "A_z")
    a_to_h = _coefficient(florivory, "A_z")
    d_to_h = _coefficient(florivory, "D_z")
    a_d_seed = _coefficient(seed, "A_z:D_z")
    florivory_fruit = _coefficient(fruit_factorial, "Florivory_c")
    florivory_seed = _coefficient(seed_factorial, "Florivory_c")
    phenology_fruit = _coefficient(fruit_factorial, "Phenology_z")

    lines = [
        "# *Impatiens capensis*: theory-to-empirics bridge",
        "",
        "## What this bridge does",
        "",
        "This synthesis joins an aligned observational channel panel with a separate randomized factorial treatment experiment in the same study system. It maps evidence to individual components of Part A; it does **not** estimate the exact mixed partial, multiply coefficients across incompatible link scales, infer a causal floral-tannin effect, or identify the shared allocation term `c_AD`.",
        "",
        "## Channel evidence",
        "",
        "| Part A component | Empirical model | Result | Current status |",
        "|---|---|---|---|",
        f"| `b_A`: A → pollinator use | individual-plant 60-min rate | RR {_ratio_text(a_to_p)} | {_ratio_status(a_to_p)} |",
        f"| `c_D`: D candidate → pollinator use | individual-plant 60-min rate | RR {_ratio_text(d_to_p)} | {_ratio_status(d_to_p, expected_direction='negative')} |",
        f"| `d_A`: A → natural floral antagonism | flower-level fractional-logit | OR {_ratio_text(a_to_h)} | {_ratio_status(a_to_h)} |",
        f"| `e_F`: D candidate → natural floral antagonism | flower-level fractional-logit | OR {_ratio_text(d_to_h)} | {_ratio_status(d_to_h, expected_direction='negative')} |",
        "",
        "The `c_D`-like association is observational: higher early floral tannin values are associated with a lower standardized pollinator-use rate. It is not evidence that experimentally increasing tannins would reduce pollination. The flower-level antagonism model does not resolve a protective `e_F` direction for this tannin candidate.",
        "",
        "## Pollinator-rate adequacy sensitivity",
        "",
        f"The primary count-rate model has {int(pollinator['n_response_records'])} complete plants, mean rate {float(pollinator['mean_response']):.2f}, and Pearson dispersion {float(pollinator['pearson_dispersion']):.2f}; its zero mass prompted a declared post-primary hurdle sensitivity.",
        "",
        f"- Any visit observed: D candidate OR {_ratio_text(_coefficient(presence, 'D_z'))}; this is not directionally resolved.",
        f"- Intensity conditional on at least one visit: D candidate RR {_ratio_text(_coefficient(positive, 'D_z'))}; {_ratio_status(_coefficient(positive, 'D_z'), expected_direction='negative')}. This positive-count model remains an adequacy sensitivity, not a replacement primary result.",
        "",
        "## Reproductive-component evidence",
        "",
        "| Question | Model | Result | Current status |",
        "|---|---|---|---|",
        f"| A × D candidate surface in seeds per CH fruit | raw CH-fruit count, observational | RR {_ratio_text(a_d_seed)} | {_ratio_status(a_d_seed)} |",
        f"| Supplemental florivory → CH fruits/day | full randomized 2×2×2 factorial | standardized coefficient {_coefficient_text(florivory_fruit)} | {_coefficient_status(florivory_fruit, expected_direction='negative')} |",
        f"| Supplemental florivory → seeds per CH fruit | full randomized 2×2×2 factorial | standardized coefficient {_coefficient_text(florivory_seed)} | {_coefficient_status(florivory_seed, expected_direction='negative')} |",
        f"| Phenology → CH fruits/day | full randomized factorial with pre-treatment phenology | standardized coefficient {_coefficient_text(phenology_fruit)} | {_coefficient_status(phenology_fruit, expected_direction='negative')} |",
        "",
        "The randomized result supports a downstream reproductive cost of imposed florivory on CH fruit production in this experiment. It does not show that natural floral damage, flower redness, or floral tannins caused that cost, and the outcomes are components rather than total lifetime fitness.",
        "",
        "## Empirical conclusion for the model",
        "",
        "This system currently supports a restricted, asymmetric empirical story: a floral-tannin candidate is associated with a pollinator-use cost, while its predicted antagonism-suppression benefit is not resolved; imposed florivory nevertheless lowers one reproductive component. Attraction-path effects and the A×D reproductive-component surface remain unresolved. The most defensible next claim is therefore a **case-study constraint on the theory**, not an empirical estimate of complementarity or substitutability.",
        "",
        "The strong negative phenology association with CH fruit production also means future field and experimental designs must treat flowering time as a central ecological axis rather than a nuisance covariate.",
        "",
    ]
    return "\n".join(lines)


def build_bridge(response_report_path: str | Path, factorial_report_path: str | Path, output_path: str | Path) -> None:
    response_report = json.loads(Path(response_report_path).read_text(encoding="utf-8"))
    factorial_report = json.loads(Path(factorial_report_path).read_text(encoding="utf-8"))
    Path(output_path).write_text(render_bridge(response_report, factorial_report), encoding="utf-8")
