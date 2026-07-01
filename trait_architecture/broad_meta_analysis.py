"""Contracts and deterministic analysis for broad real-world evidence synthesis.

This module deliberately separates a high-recall directional map from numerical
random-effects mini-meta-analyses. It has no third-party dependencies so the
analysis contract is reproducible in the repository CI environment.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import NormalDist
from typing import Iterable


DIRECT_ROUTES = frozenset({
    "A_to_pollination",
    "A_to_antagonism",
    "B_to_antagonism",
    "B_to_pollination",
})
ROUTE_TRAIT_ROLE = {
    "A_to_pollination": "A",
    "A_to_antagonism": "A",
    "B_to_antagonism": "B",
    "B_to_pollination": "B",
}
ROUTE_EXPECTED_SIGN = {
    "A_to_pollination": "positive",
    "A_to_antagonism": "positive",
    "B_to_antagonism": "negative",
    "B_to_pollination": "negative",
}
DIRECTION_CODES = frozenset({"positive", "negative", "mixed", "null", "not_reported"})
DESIGN_CLASSES = frozenset({"observational", "manipulation", "comparative"})
RECORD_STATUSES = frozenset({"included_for_direction_map", "excluded", "unassessed"})
EFFECT_METRICS = frozenset({
    "log_response_ratio",
    "log_odds_ratio",
    "fisher_z",
    "hedges_g",
    "standardized_beta",
})
EFFECT_INPUT_TYPES = frozenset({"reported_effect", "group_means", "two_by_two", "correlation"})
EFFECT_STATUSES = frozenset({"eligible_for_quantitative_synthesis", "not_eligible", "unassessed"})
ORIENTATION = "positive_is_more_declared_trait_more_declared_outcome"
Z_975 = NormalDist().inv_cdf(0.975)

ROUTE_RECORD_FIELDS = (
    "record_id", "study_id", "study_cluster_id", "doi", "taxon", "route", "trait_role",
    "trait_class", "outcome_class", "design_class", "source_basis", "reported_direction",
    "is_primary_sign_record", "record_status", "context_note", "coder_id", "coding_date",
)
EFFECT_FIELDS = (
    "effect_id", "study_id", "study_cluster_id", "doi", "taxon", "route", "trait_role",
    "trait_class", "outcome_class", "design_class", "effect_input_type", "effect_metric",
    "effect_value", "standard_error", "n_treatment", "n_control", "mean_treatment",
    "sd_treatment", "mean_control", "sd_control", "event_treatment", "non_event_treatment",
    "event_control", "non_event_control", "correlation_r", "n_total", "effect_orientation",
    "is_primary_effect", "analysis_status", "source_basis", "source_locator", "extraction_note",
)
STRATUM_FIELDS = (
    "stratum_id", "route", "trait_class", "outcome_class", "effect_metric", "design_class",
    "min_clusters_exploratory", "min_clusters_stability", "expected_effect_direction",
    "part_i_parameter", "interpretation",
)
DIRECTION_OUTPUT_FIELDS = (
    "route", "trait_class", "outcome_class", "design_class", "expected_effect_direction",
    "independent_clusters", "positive_count", "negative_count", "mixed_count", "null_count",
    "not_reported_count", "evaluable_direction_count", "compatible_count", "contradictory_count",
    "compatible_fraction", "direction_map_status",
)
META_SUMMARY_FIELDS = (
    "stratum_id", "route", "trait_class", "outcome_class", "effect_metric", "design_class",
    "expected_effect_direction", "part_i_parameter", "independent_clusters", "effect_count",
    "analysis_status", "pooled_effect", "pooled_standard_error", "ci_low", "ci_high", "z_value",
    "two_sided_p_value", "tau_squared_DL", "Q", "Q_df", "I_squared_percent",
    "pooled_direction", "channel_assumption_comparison",
)
META_EFFECT_OUTPUT_FIELDS = EFFECT_FIELDS + ("computed_effect_value", "computed_standard_error", "conversion_method", "stratum_id")


@dataclass(frozen=True)
class EffectEstimate:
    effect_id: str
    study_cluster_id: str
    value: float
    standard_error: float
    conversion_method: str
    row: dict[str, str]


def _text(value: object) -> str:
    return str(value or "").strip()


def _bool(value: object) -> bool:
    return _text(value).lower() in {"true", "1", "yes", "y"}


def _float(value: object, field: str, *, positive: bool = False, nonnegative: bool = False) -> float:
    try:
        number = float(_text(value))
    except ValueError as error:
        raise ValueError(f"{field} must be numeric") from error
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    if positive and number <= 0:
        raise ValueError(f"{field} must be > 0")
    if nonnegative and number < 0:
        raise ValueError(f"{field} must be >= 0")
    return number


def _require_columns(rows: list[dict[str, str]], fields: Iterable[str], label: str) -> None:
    if not rows:
        return
    missing = [field for field in fields if field not in rows[0]]
    if missing:
        raise ValueError(f"{label} missing required columns: {', '.join(missing)}")


def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def write_csv_rows(path: str | Path, fieldnames: Iterable[str], rows: Iterable[dict[str, object]]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def validate_route_records(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Validate source-coded directional records without inferring any evidence."""

    rows = list(rows)
    _require_columns(rows, ROUTE_RECORD_FIELDS, "broad route records")
    seen_ids: set[str] = set()
    primary_keys: set[tuple[str, str, str, str, str]] = set()
    for index, row in enumerate(rows, start=1):
        record_id = _text(row.get("record_id"))
        if not record_id:
            raise ValueError(f"route record {index} has blank record_id")
        if record_id in seen_ids:
            raise ValueError(f"duplicate route record ID: {record_id}")
        seen_ids.add(record_id)
        status = _text(row.get("record_status"))
        if status not in RECORD_STATUSES:
            raise ValueError(f"route record {record_id} has invalid record_status")
        if status != "included_for_direction_map":
            continue
        route = _text(row.get("route"))
        if route not in DIRECT_ROUTES:
            raise ValueError(f"route record {record_id} has invalid direct route")
        expected_role = ROUTE_TRAIT_ROLE[route]
        if _text(row.get("trait_role")) != expected_role:
            raise ValueError(f"route record {record_id} has trait role inconsistent with {route}")
        if _text(row.get("design_class")) not in DESIGN_CLASSES:
            raise ValueError(f"route record {record_id} has invalid design_class")
        if _text(row.get("reported_direction")) not in DIRECTION_CODES:
            raise ValueError(f"route record {record_id} has invalid reported_direction")
        if not _text(row.get("study_cluster_id")):
            raise ValueError(f"route record {record_id} needs study_cluster_id")
        if not _text(row.get("trait_class")) or not _text(row.get("outcome_class")):
            raise ValueError(f"route record {record_id} needs trait_class and outcome_class")
        if _bool(row.get("is_primary_sign_record")):
            key = (
                _text(row["study_cluster_id"]), route, _text(row["trait_class"]),
                _text(row["outcome_class"]), _text(row["design_class"]),
            )
            if key in primary_keys:
                raise ValueError("more than one primary sign record for one study-cluster stratum")
            primary_keys.add(key)
    return rows


def direction_map(rows: Iterable[dict[str, str]]) -> list[dict[str, object]]:
    """Return cluster-level directional support/contradiction summaries."""

    valid = validate_route_records(rows)
    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in valid:
        if row.get("record_status") != "included_for_direction_map" or not _bool(row.get("is_primary_sign_record")):
            continue
        key = (row["route"], row["trait_class"], row["outcome_class"], row["design_class"])
        grouped[key].append(row)

    results: list[dict[str, object]] = []
    for (route, trait_class, outcome_class, design_class), records in sorted(grouped.items()):
        counts = Counter(record["reported_direction"] for record in records)
        expected = ROUTE_EXPECTED_SIGN[route]
        evaluable = counts["positive"] + counts["negative"]
        compatible = counts[expected]
        contradictory = counts["negative" if expected == "positive" else "positive"]
        fraction = compatible / evaluable if evaluable else None
        if evaluable < 3:
            status = "insufficient_directional_clusters"
        elif fraction is not None and fraction >= 0.8:
            status = "mostly_compatible_with_channel_assumption"
        elif fraction is not None and fraction <= 0.2:
            status = "mostly_contradictory_to_channel_assumption"
        else:
            status = "mixed_or_context_dependent"
        results.append({
            "route": route,
            "trait_class": trait_class,
            "outcome_class": outcome_class,
            "design_class": design_class,
            "expected_effect_direction": expected,
            "independent_clusters": len(records),
            "positive_count": counts["positive"],
            "negative_count": counts["negative"],
            "mixed_count": counts["mixed"],
            "null_count": counts["null"],
            "not_reported_count": counts["not_reported"],
            "evaluable_direction_count": evaluable,
            "compatible_count": compatible,
            "contradictory_count": contradictory,
            "compatible_fraction": "" if fraction is None else f"{fraction:.6f}",
            "direction_map_status": status,
        })
    return results


def _validate_effect_identity(row: dict[str, str]) -> None:
    route = _text(row.get("route"))
    if route not in DIRECT_ROUTES:
        raise ValueError(f"effect {row.get('effect_id', '')} has invalid direct route")
    if _text(row.get("trait_role")) != ROUTE_TRAIT_ROLE[route]:
        raise ValueError(f"effect {row.get('effect_id', '')} has trait role inconsistent with {route}")
    if _text(row.get("design_class")) not in DESIGN_CLASSES:
        raise ValueError(f"effect {row.get('effect_id', '')} has invalid design_class")
    if _text(row.get("effect_metric")) not in EFFECT_METRICS:
        raise ValueError(f"effect {row.get('effect_id', '')} has invalid effect_metric")
    if _text(row.get("effect_input_type")) not in EFFECT_INPUT_TYPES:
        raise ValueError(f"effect {row.get('effect_id', '')} has invalid effect_input_type")


def validate_effect_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Validate extraction rows and preserve one primary effect per cluster stratum."""

    rows = list(rows)
    _require_columns(rows, EFFECT_FIELDS, "broad effect extractions")
    seen_ids: set[str] = set()
    primary_keys: set[tuple[str, str, str, str, str, str]] = set()
    for index, row in enumerate(rows, start=1):
        effect_id = _text(row.get("effect_id"))
        if not effect_id:
            raise ValueError(f"effect row {index} has blank effect_id")
        if effect_id in seen_ids:
            raise ValueError(f"duplicate effect ID: {effect_id}")
        seen_ids.add(effect_id)
        status = _text(row.get("analysis_status"))
        if status not in EFFECT_STATUSES:
            raise ValueError(f"effect {effect_id} has invalid analysis_status")
        if status != "eligible_for_quantitative_synthesis":
            continue
        _validate_effect_identity(row)
        if _text(row.get("effect_orientation")) != ORIENTATION:
            raise ValueError(f"effect {effect_id} is not explicitly oriented to declared trait and outcome")
        if not _text(row.get("study_cluster_id")):
            raise ValueError(f"effect {effect_id} needs study_cluster_id")
        if not _bool(row.get("is_primary_effect")):
            continue
        key = (
            row["study_cluster_id"], row["route"], row["trait_class"], row["outcome_class"],
            row["effect_metric"], row["design_class"],
        )
        if key in primary_keys:
            raise ValueError("more than one primary effect for one study-cluster quantitative stratum")
        primary_keys.add(key)
    return rows


def effect_estimate(row: dict[str, str]) -> EffectEstimate:
    """Recover one correctly oriented effect and its standard error from declared inputs."""

    effect_id = _text(row.get("effect_id"))
    input_type = _text(row.get("effect_input_type"))
    metric = _text(row.get("effect_metric"))
    if input_type == "reported_effect":
        value = _float(row.get("effect_value"), "effect_value")
        standard_error = _float(row.get("standard_error"), "standard_error", positive=True)
        return EffectEstimate(effect_id, row["study_cluster_id"], value, standard_error, "reported_effect", row)

    if input_type == "group_means":
        nt = _float(row.get("n_treatment"), "n_treatment", positive=True)
        nc = _float(row.get("n_control"), "n_control", positive=True)
        mt = _float(row.get("mean_treatment"), "mean_treatment")
        mc = _float(row.get("mean_control"), "mean_control")
        sdt = _float(row.get("sd_treatment"), "sd_treatment", nonnegative=True)
        sdc = _float(row.get("sd_control"), "sd_control", nonnegative=True)
        if metric == "log_response_ratio":
            if mt <= 0 or mc <= 0:
                raise ValueError(f"effect {effect_id}: log_response_ratio needs positive group means")
            value = math.log(mt / mc)
            standard_error = math.sqrt((sdt ** 2) / (nt * mt ** 2) + (sdc ** 2) / (nc * mc ** 2))
            if standard_error <= 0:
                raise ValueError(f"effect {effect_id}: log_response_ratio needs nonzero uncertainty")
            return EffectEstimate(effect_id, row["study_cluster_id"], value, standard_error, "group_means_to_log_response_ratio", row)
        if metric == "hedges_g":
            if nt + nc <= 2:
                raise ValueError(f"effect {effect_id}: Hedges g needs total n > 2")
            df = nt + nc - 2
            pooled_sd = math.sqrt(((nt - 1) * sdt ** 2 + (nc - 1) * sdc ** 2) / df)
            if pooled_sd <= 0:
                raise ValueError(f"effect {effect_id}: Hedges g needs nonzero pooled SD")
            d = (mt - mc) / pooled_sd
            correction = 1 - 3 / (4 * df - 1)
            value = correction * d
            variance = (nt + nc) / (nt * nc) + (value ** 2) / (2 * df)
            return EffectEstimate(effect_id, row["study_cluster_id"], value, math.sqrt(variance), "group_means_to_hedges_g", row)
        raise ValueError(f"effect {effect_id}: group_means only supports log_response_ratio or hedges_g")

    if input_type == "two_by_two":
        if metric != "log_odds_ratio":
            raise ValueError(f"effect {effect_id}: two_by_two only supports log_odds_ratio")
        a = _float(row.get("event_treatment"), "event_treatment", nonnegative=True)
        b = _float(row.get("non_event_treatment"), "non_event_treatment", nonnegative=True)
        c = _float(row.get("event_control"), "event_control", nonnegative=True)
        d = _float(row.get("non_event_control"), "non_event_control", nonnegative=True)
        if min(a, b, c, d) == 0:
            a += 0.5
            b += 0.5
            c += 0.5
            d += 0.5
            method = "two_by_two_to_log_odds_ratio_with_half_cell_correction"
        else:
            method = "two_by_two_to_log_odds_ratio"
        value = math.log((a * d) / (b * c))
        standard_error = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
        return EffectEstimate(effect_id, row["study_cluster_id"], value, standard_error, method, row)

    if input_type == "correlation":
        if metric != "fisher_z":
            raise ValueError(f"effect {effect_id}: correlation only supports fisher_z")
        correlation = _float(row.get("correlation_r"), "correlation_r")
        n_total = _float(row.get("n_total"), "n_total", positive=True)
        if not -1 < correlation < 1:
            raise ValueError(f"effect {effect_id}: correlation_r must lie strictly between -1 and 1")
        if n_total <= 3:
            raise ValueError(f"effect {effect_id}: Fisher z needs n_total > 3")
        value = math.atanh(correlation)
        standard_error = 1 / math.sqrt(n_total - 3)
        return EffectEstimate(effect_id, row["study_cluster_id"], value, standard_error, "correlation_to_fisher_z", row)

    raise ValueError(f"effect {effect_id}: unsupported effect_input_type")


def read_strata(path: str | Path) -> list[dict[str, str]]:
    rows = read_csv_rows(path)
    _require_columns(rows, STRATUM_FIELDS, "meta-analysis strata")
    identifiers: set[str] = set()
    for row in rows:
        stratum_id = row.get("stratum_id", "")
        if not stratum_id or stratum_id in identifiers:
            raise ValueError("meta-analysis stratum IDs must be nonempty and unique")
        identifiers.add(stratum_id)
        route = row.get("route", "")
        if route not in DIRECT_ROUTES:
            raise ValueError(f"stratum {stratum_id} has invalid route")
        if row.get("effect_metric", "") not in EFFECT_METRICS:
            raise ValueError(f"stratum {stratum_id} has invalid effect_metric")
        if row.get("design_class", "") not in DESIGN_CLASSES:
            raise ValueError(f"stratum {stratum_id} has invalid design_class")
        expected = row.get("expected_effect_direction", "")
        if expected != ROUTE_EXPECTED_SIGN[route]:
            raise ValueError(f"stratum {stratum_id} expected direction conflicts with route contract")
        exploratory = int(_float(row.get("min_clusters_exploratory"), "min_clusters_exploratory", positive=True))
        stability = int(_float(row.get("min_clusters_stability"), "min_clusters_stability", positive=True))
        if exploratory < 3 or stability < exploratory:
            raise ValueError(f"stratum {stratum_id} has invalid pooling thresholds")
    return rows


def _der_simonian_laird(estimates: list[EffectEstimate]) -> dict[str, float]:
    if len(estimates) < 2:
        raise ValueError("DerSimonian–Laird calculation needs at least two effects")
    variances = [estimate.standard_error ** 2 for estimate in estimates]
    weights = [1 / variance for variance in variances]
    fixed_mean = sum(weight * estimate.value for weight, estimate in zip(weights, estimates)) / sum(weights)
    q = sum(weight * (estimate.value - fixed_mean) ** 2 for weight, estimate in zip(weights, estimates))
    df = len(estimates) - 1
    c_value = sum(weights) - sum(weight ** 2 for weight in weights) / sum(weights)
    tau_squared = max(0.0, (q - df) / c_value) if c_value > 0 else 0.0
    random_weights = [1 / (variance + tau_squared) for variance in variances]
    pooled = sum(weight * estimate.value for weight, estimate in zip(random_weights, estimates)) / sum(random_weights)
    pooled_se = math.sqrt(1 / sum(random_weights))
    z_value = pooled / pooled_se
    p_value = math.erfc(abs(z_value) / math.sqrt(2))
    i_squared = max(0.0, ((q - df) / q) * 100) if q > 0 else 0.0
    return {
        "pooled_effect": pooled,
        "pooled_standard_error": pooled_se,
        "ci_low": pooled - Z_975 * pooled_se,
        "ci_high": pooled + Z_975 * pooled_se,
        "z_value": z_value,
        "two_sided_p_value": p_value,
        "tau_squared_DL": tau_squared,
        "Q": q,
        "Q_df": float(df),
        "I_squared_percent": i_squared,
    }


def _matches_stratum(row: dict[str, str], stratum: dict[str, str]) -> bool:
    return all(row.get(field, "") == stratum[field] for field in (
        "route", "trait_class", "outcome_class", "effect_metric", "design_class",
    ))


def meta_analysis(effect_rows: Iterable[dict[str, str]], strata: Iterable[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run only predeclared, compatible random-effects mini-meta-analyses."""

    valid_effects = validate_effect_rows(effect_rows)
    strata = list(strata)
    eligible = [
        row for row in valid_effects
        if row.get("analysis_status") == "eligible_for_quantitative_synthesis" and _bool(row.get("is_primary_effect"))
    ]
    estimates: list[EffectEstimate] = [effect_estimate(row) for row in eligible]
    summaries: list[dict[str, object]] = []
    used_rows: list[dict[str, object]] = []
    for stratum in strata:
        matching = [estimate for estimate in estimates if _matches_stratum(estimate.row, stratum)]
        clusters = {estimate.study_cluster_id for estimate in matching}
        k = len(clusters)
        base = {
            "stratum_id": stratum["stratum_id"],
            "route": stratum["route"],
            "trait_class": stratum["trait_class"],
            "outcome_class": stratum["outcome_class"],
            "effect_metric": stratum["effect_metric"],
            "design_class": stratum["design_class"],
            "expected_effect_direction": stratum["expected_effect_direction"],
            "part_i_parameter": stratum["part_i_parameter"],
            "independent_clusters": k,
            "effect_count": len(matching),
        }
        exploratory_min = int(stratum["min_clusters_exploratory"])
        stability_min = int(stratum["min_clusters_stability"])
        if k < exploratory_min:
            summaries.append({
                **base,
                "analysis_status": "insufficient_independent_clusters",
                "pooled_effect": "", "pooled_standard_error": "", "ci_low": "", "ci_high": "",
                "z_value": "", "two_sided_p_value": "", "tau_squared_DL": "", "Q": "", "Q_df": "",
                "I_squared_percent": "", "pooled_direction": "", "channel_assumption_comparison": "not_pooled",
            })
            continue
        diagnostics = _der_simonian_laird(matching)
        pooled = diagnostics["pooled_effect"]
        pooled_direction = "positive" if pooled > 0 else "negative" if pooled < 0 else "zero"
        if diagnostics["ci_low"] <= 0 <= diagnostics["ci_high"]:
            comparison = "uncertain_direction"
        elif pooled_direction == stratum["expected_effect_direction"]:
            comparison = "compatible_with_channel_assumption"
        else:
            comparison = "contradictory_to_channel_assumption"
        analysis_status = "stability_eligible_random_effects" if k >= stability_min else "exploratory_random_effects"
        summaries.append({
            **base,
            "analysis_status": analysis_status,
            **{key: f"{value:.10g}" for key, value in diagnostics.items()},
            "pooled_direction": pooled_direction,
            "channel_assumption_comparison": comparison,
        })
        for estimate in matching:
            enriched = dict(estimate.row)
            enriched.update({
                "computed_effect_value": f"{estimate.value:.10g}",
                "computed_standard_error": f"{estimate.standard_error:.10g}",
                "conversion_method": estimate.conversion_method,
                "stratum_id": stratum["stratum_id"],
            })
            used_rows.append(enriched)
    diagnostics = {
        "eligible_primary_effect_count": len(estimates),
        "configured_stratum_count": len(strata),
        "pooled_stratum_count": sum(row["analysis_status"] != "insufficient_independent_clusters" for row in summaries),
        "interpretation_boundary": (
            "Random-effects estimates are limited to predeclared exact route/trait/outcome/metric/design strata. "
            "They are standardized empirical summaries, not raw Part I parameter values or direct D1/D2 tests."
        ),
    }
    return summaries, used_rows, diagnostics


def write_analysis_outputs(
    out_dir: str | Path,
    route_rows: Iterable[dict[str, str]],
    effect_rows: Iterable[dict[str, str]],
    strata: Iterable[dict[str, str]],
) -> dict[str, object]:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    map_rows = direction_map(route_rows)
    summary_rows, used_rows, diagnostics = meta_analysis(effect_rows, strata)
    write_csv_rows(destination / "broad_direction_map.csv", DIRECTION_OUTPUT_FIELDS, map_rows)
    write_csv_rows(destination / "broad_meta_analysis_summary.csv", META_SUMMARY_FIELDS, summary_rows)
    write_csv_rows(destination / "broad_meta_analysis_effects_used.csv", META_EFFECT_OUTPUT_FIELDS, used_rows)
    (destination / "broad_meta_analysis_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
    return diagnostics
