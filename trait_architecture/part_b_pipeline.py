"""Part B orchestrator: run layers B1-B4 as one reproducible pipeline.

This ties the finished Part B pieces into a single, deterministic run:

    B1  direction map                 broad_meta_analysis.direction_map
    B2  per-arrow effect envelopes     broad_meta_analysis.meta_analysis
    B3  moderator/conditionality        part_b_moderator.moderator_contrast
    B4  break-even regime map           part_b_support.envelope_break_even_map

It has no third-party dependencies and emits CSV + JSON artefacts plus an honest
diagnostics block. It never fabricates a pooled or moderated result: with the
current evidence base every arrow-stratum is a single cluster, so B2/B3 report
``insufficient`` and B4 is an explicitly declared sensitivity map.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .broad_meta_analysis import (
    DIRECTION_OUTPUT_FIELDS,
    META_SUMMARY_FIELDS,
    direction_map,
    meta_analysis,
    write_csv_rows,
)
from .model import ModelParameters
from .part_b_moderator import moderator_contrast
from .part_b_support import envelope_break_even_map
from .robustness import cartesian_cases


MODERATOR_CONTRAST_FIELDS = (
    "hypothesis_label", "route", "part_i_parameter", "trait_class", "outcome_class",
    "effect_metric", "design_class", "moderator_variable", "low_level", "high_level",
    "predicted_contrast_sign", "low_clusters", "low_pooled", "high_clusters", "high_pooled",
    "contrast", "contrast_ci_low", "contrast_ci_high", "two_sided_p_value", "status",
)
ROUTE_PART_I_PARAMETER = {
    "A_to_pollination": "b_A",
    "A_to_antagonism": "d_A",
    "B_to_antagonism": "e_F",
    "B_to_pollination": "c_D",
}
_MODERATOR_KWARGS = (
    "route", "trait_class", "outcome_class", "effect_metric", "design_class",
    "moderator_variable", "low_level", "high_level", "predicted_contrast_sign",
)


def _number(value: object) -> str:
    return "" if value is None else f"{float(value):.10g}"


def run_moderator_hypotheses(
    effect_rows: Iterable[Mapping[str, str]],
    hypotheses: Iterable[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Run one moderator contrast per declared hypothesis and flatten for CSV."""

    rows = list(effect_rows)
    output: list[dict[str, object]] = []
    for hypothesis in hypotheses:
        kwargs = {key: hypothesis[key] for key in _MODERATOR_KWARGS}
        if "min_clusters_per_level" in hypothesis:
            kwargs["min_clusters_per_level"] = int(hypothesis["min_clusters_per_level"])
        result = moderator_contrast(rows, **kwargs)
        output.append({
            "hypothesis_label": str(hypothesis.get("label", "")),
            "route": result.route,
            "part_i_parameter": ROUTE_PART_I_PARAMETER[result.route],
            "trait_class": result.trait_class,
            "outcome_class": result.outcome_class,
            "effect_metric": result.effect_metric,
            "design_class": result.design_class,
            "moderator_variable": result.moderator_variable,
            "low_level": result.low_level,
            "high_level": result.high_level,
            "predicted_contrast_sign": result.predicted_contrast_sign,
            "low_clusters": result.low.clusters,
            "low_pooled": _number(result.low.pooled_effect),
            "high_clusters": result.high.clusters,
            "high_pooled": _number(result.high.pooled_effect),
            "contrast": _number(result.contrast),
            "contrast_ci_low": _number(result.contrast_ci_low),
            "contrast_ci_high": _number(result.contrast_ci_high),
            "two_sided_p_value": _number(result.two_sided_p_value),
            "status": result.status,
        })
    return output


def _cases_from_config(grid: Mapping[str, Sequence[float]]):
    return cartesian_cases(
        attraction=grid["attraction"],
        defence=grid["defence"],
        assurance=grid["assurance"],
        pollinator_service=grid["pollinator_service"],
        floral_damage_pressure=grid["floral_damage_pressure"],
    )


def run_break_even_map(config: Mapping[str, object]) -> list[dict[str, object]]:
    """Build the B4 empirically-informed regime map from a declared config."""

    cases = _cases_from_config(config["case_grid"])  # type: ignore[index]
    base = config.get("base_parameters")
    base_parameters = ModelParameters(**base) if isinstance(base, Mapping) else ModelParameters()
    return envelope_break_even_map(
        cases,
        config["channel_envelopes"],  # type: ignore[index]
        base_parameters=base_parameters,
        shared_cost_scenarios=tuple(config.get("shared_cost_scenarios", ())),
    )


def write_part_b_outputs(
    out_dir: str | Path,
    *,
    route_rows: Iterable[Mapping[str, str]],
    effect_rows: Iterable[Mapping[str, str]],
    strata: Iterable[Mapping[str, str]],
    moderator_hypotheses: Iterable[Mapping[str, object]],
    break_even_config: Mapping[str, object],
) -> dict[str, object]:
    """Run B1-B4 and write the full Part B artefact bundle."""

    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)

    effect_rows = list(effect_rows)
    map_rows = direction_map(route_rows)
    summary_rows, _used_rows, meta_diag = meta_analysis(effect_rows, strata)
    moderator_rows = run_moderator_hypotheses(effect_rows, moderator_hypotheses)
    break_even_rows = run_break_even_map(break_even_config)

    write_csv_rows(destination / "part_b_b1_direction_map.csv", DIRECTION_OUTPUT_FIELDS, map_rows)
    write_csv_rows(destination / "part_b_b2_arrow_envelopes.csv", META_SUMMARY_FIELDS, summary_rows)
    write_csv_rows(destination / "part_b_b3_moderator_contrasts.csv", MODERATOR_CONTRAST_FIELDS, moderator_rows)
    break_even_fields = list(break_even_rows[0].keys()) if break_even_rows else []
    write_csv_rows(destination / "part_b_b4_break_even_regime_map.csv", break_even_fields, break_even_rows)

    diagnostics = {
        "b1_direction_strata": len(map_rows),
        "b1_strata_with_sufficient_clusters": sum(
            row["direction_map_status"] != "insufficient_directional_clusters" for row in map_rows
        ),
        "b2_configured_strata": meta_diag["configured_stratum_count"],
        "b2_pooled_strata": meta_diag["pooled_stratum_count"],
        "b2_eligible_primary_effects": meta_diag["eligible_primary_effect_count"],
        "b3_moderator_hypotheses": len(moderator_rows),
        "b3_supported": sum(row["status"] == "moderator_supported" for row in moderator_rows),
        "b3_contradicted": sum(row["status"] == "moderator_contradicted" for row in moderator_rows),
        "b4_regime_map_rows": len(break_even_rows),
        "interpretation_boundary": (
            "B2/B3 pool marginal arrows and count clusters per arrow; a stratum with "
            "fewer than three independent clusters is reported as insufficient, not forced. "
            "B4 is a declared sensitivity map bounding c_AD, never an estimate of it. No "
            "output is a joint-panel D1/D2 identification."
        ),
    }
    (destination / "part_b_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
    return diagnostics
