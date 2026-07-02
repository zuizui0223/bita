"""Integrated effect ledger for floral trait--animal interaction meta-analysis.

This is the large-data layer of the project. It preserves all four channels
(A/B x pollinator/floral antagonist) in one ledger and treats mechanism,
outcome construction, source metric, design, dose, and ecological context as
moderators rather than pre-analysis split points.

It deliberately does not turn candidate abstracts into effects. Full-text
records remain in one effect ledger regardless of whether they can be
harmonized immediately to Fisher-z. Effects that cannot safely enter the
common-scale analysis are retained in metric-specific lanes for later
measurement-model or sensitivity analysis.
"""

from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Mapping

from trait_architecture.floral_trait_animal_response_meta import ROUTE_INTERPRETATION


CANDIDATE_QUEUE_REQUIRED = {
    "candidate_id", "doi", "title", "publication_year", "work_type",
    "container_title", "publisher", "route_memberships", "source_bucket",
    "screening_priority", "crossref_abstract_text",
}

ROUTE_TO_TRAIT_PARTNER = {
    "A_to_pollinator": ("A_flower", "pollinator"),
    "A_to_antagonist": ("A_flower", "floral_antagonist"),
    "B_to_antagonist": ("B_flower", "floral_antagonist"),
    "B_to_pollinator": ("B_flower", "pollinator"),
}
ROUTE_ORDER = tuple(ROUTE_TO_TRAIT_PARTNER)

MECHANISM_CLASSES = frozenset({
    "chemical", "physical_access", "visual", "temporal", "reward", "mixed", "other",
})
OUTCOME_CONSTRUCTS = frozenset({
    "consumer_use", "consumer_preference", "consumer_visitation",
    "consumer_attack", "consumer_damage", "consumer_abundance",
    "pollen_transfer", "reproductive_output", "learning_or_constancy",
    "other_predeclared",
})
STUDY_DESIGNS = frozenset({
    "direct_experiment", "choice_assay", "observational_association",
    "natural_comparison",
})
ORGAN_MATCHES = frozenset({
    "flower_or_inflorescence", "nectar", "reproductive_structure",
})
METRICS = frozenset({
    "fisher_z", "correlation_r", "hedges_g", "log_odds_ratio",
    "log_response_ratio", "log_rate_ratio",
})
INCLUSION_STATES = frozenset({
    "pending_full_text", "included", "excluded",
})

CANDIDATE_LEDGER_FIELDS = (
    "candidate_route_id", "candidate_id", "doi", "title", "publication_year",
    "work_type", "container_title", "publisher", "route", "trait_role",
    "partner_role", "route_direction_convention", "source_bucket",
    "screening_priority", "route_memberships", "candidate_status",
    "full_text_screen_status", "full_text_screen_note", "source_queries",
    "abstract_text", "candidate_boundary",
)

EFFECT_LEDGER_FIELDS = (
    "candidate_route_id", "candidate_id", "doi", "title", "study_id",
    "independent_study_id", "effect_id", "species", "trait_role",
    "partner_role", "route", "trait_name", "mechanism_class", "organ_match",
    "trait_contrast_or_predictor", "outcome_construct", "study_design",
    "dose_relation", "consumer_specialization", "alternative_resource_context",
    "source_effect_metric", "source_effect_estimate", "source_effect_variance",
    "sample_size_total", "direction_is_higher_trait", "full_text_inclusion",
    "source_locator", "extractor_id", "extraction_note", "is_primary_effect",
    "harmonization_status", "harmonization_method", "common_effect_fisher_z",
    "common_effect_variance", "metric_specific_analysis_lane",
    "model_inclusion_status", "exclusion_reason", "effect_boundary",
)

BALANCE_FIELDS = (
    "trait_role", "partner_role", "route", "candidate_route_rows",
    "full_text_included_effect_rows", "numeric_effect_rows",
    "common_scale_effect_rows", "native_metric_effect_rows",
    "independent_studies_numeric", "independent_studies_common_scale",
    "interpretation_boundary",
)


class IntegratedInteractionMetaError(ValueError):
    """Raised when an integrated candidate or effect ledger violates its contract."""


def _text(value: object) -> str:
    return str(value or "").strip()


def _float(value: object, field: str) -> float:
    try:
        number = float(_text(value))
    except ValueError as error:
        raise IntegratedInteractionMetaError(f"{field} must be numeric") from error
    if not math.isfinite(number):
        raise IntegratedInteractionMetaError(f"{field} must be finite")
    return number


def read_rows(path: str | Path, required: Iterable[str]) -> list[dict[str, str]]:
    location = Path(path)
    with location.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(required).difference(reader.fieldnames or [])
        if missing:
            raise IntegratedInteractionMetaError(
                f"{location} missing required columns: {', '.join(sorted(missing))}"
            )
        return [{key: _text(value) for key, value in row.items()} for row in reader]


def build_candidate_ledger(candidate_queue: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    """Expand all candidate-route memberships into one integrated ledger.

    This is an intake expansion only. Every four-channel membership is retained,
    and no candidate is ranked out because it is rare or has an uncommon
    mechanism/outcome.
    """
    rows = list(candidate_queue)
    identifiers = [row.get("candidate_id", "") for row in rows]
    if len(identifiers) != len(set(identifiers)):
        raise IntegratedInteractionMetaError("candidate queue requires unique candidate_id")
    result: list[dict[str, str]] = []
    for source in rows:
        route_memberships = [route for route in _text(source.get("route_memberships")).split(";") if route]
        unknown = set(route_memberships).difference(ROUTE_TO_TRAIT_PARTNER)
        if unknown:
            raise IntegratedInteractionMetaError(f"unknown route memberships: {', '.join(sorted(unknown))}")
        for route in route_memberships:
            trait_role, partner_role = ROUTE_TO_TRAIT_PARTNER[route]
            candidate_id = _text(source.get("candidate_id"))
            result.append({
                "candidate_route_id": f"{candidate_id}::{route}",
                "candidate_id": candidate_id,
                "doi": _text(source.get("doi")),
                "title": _text(source.get("title")),
                "publication_year": _text(source.get("publication_year")),
                "work_type": _text(source.get("work_type")),
                "container_title": _text(source.get("container_title")),
                "publisher": _text(source.get("publisher")),
                "route": route,
                "trait_role": trait_role,
                "partner_role": partner_role,
                "route_direction_convention": ROUTE_INTERPRETATION[route],
                "source_bucket": _text(source.get("source_bucket")),
                "screening_priority": _text(source.get("screening_priority")),
                "route_memberships": _text(source.get("route_memberships")),
                "candidate_status": "candidate_abstract_only",
                "full_text_screen_status": _text(source.get("full_text_screen_status")) or "unreviewed",
                "full_text_screen_note": _text(source.get("full_text_screen_note")),
                "source_queries": _text(source.get("source_queries")),
                "abstract_text": _text(source.get("crossref_abstract_text")),
                "candidate_boundary": (
                    "Candidate route membership from fixed-corpus abstract mapping. "
                    "It is neither a study effect nor a numerical observation."
                ),
            })
    return sorted(result, key=lambda row: (row["route"], row["candidate_id"]))


def make_effect_ledger(candidate_ledger: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    """Create one full-text extraction row per candidate route.

    Multiple rows can be added later for independent comparisons. The initial
    ledger deliberately keeps all channels together and makes metric/outcome
    differences explicit rather than pre-splitting the dataset.
    """
    rows: list[dict[str, str]] = []
    for candidate in candidate_ledger:
        rows.append({
            "candidate_route_id": _text(candidate.get("candidate_route_id")),
            "candidate_id": _text(candidate.get("candidate_id")),
            "doi": _text(candidate.get("doi")),
            "title": _text(candidate.get("title")),
            "study_id": "",
            "independent_study_id": "",
            "effect_id": "",
            "species": "",
            "trait_role": _text(candidate.get("trait_role")),
            "partner_role": _text(candidate.get("partner_role")),
            "route": _text(candidate.get("route")),
            "trait_name": "",
            "mechanism_class": "",
            "organ_match": "",
            "trait_contrast_or_predictor": "",
            "outcome_construct": "",
            "study_design": "",
            "dose_relation": "",
            "consumer_specialization": "",
            "alternative_resource_context": "",
            "source_effect_metric": "",
            "source_effect_estimate": "",
            "source_effect_variance": "",
            "sample_size_total": "",
            "direction_is_higher_trait": "true",
            "full_text_inclusion": "pending_full_text",
            "source_locator": "",
            "extractor_id": "",
            "extraction_note": "",
            "is_primary_effect": "",
            "harmonization_status": "pending_full_text",
            "harmonization_method": "",
            "common_effect_fisher_z": "",
            "common_effect_variance": "",
            "metric_specific_analysis_lane": "",
            "model_inclusion_status": "pending_full_text",
            "exclusion_reason": "",
            "effect_boundary": (
                "All effects are oriented so a positive source effect means a higher "
                "focal floral trait increases the measured consumer response. "
                "Trait role, partner role, mechanism, outcome, design, and metric "
                "are model moderators; candidate rows are not numeric effects."
            ),
        })
    return rows


def _z_from_g(g: float, variance: float) -> tuple[float, float]:
    r = g / math.sqrt(g * g + 4.0)
    z = math.atanh(r)
    z_variance = variance / (g * g + 4.0)
    return z, z_variance


def _z_from_log_or(log_or: float, variance: float) -> tuple[float, float]:
    """Use an explicitly labelled log-odds-to-SMD approximation before g-to-z."""
    g = log_or * math.sqrt(3.0) / math.pi
    g_variance = variance * 3.0 / (math.pi * math.pi)
    return _z_from_g(g, g_variance)


def _z_from_r(r: float, variance: float | None, sample_size: int | None) -> tuple[float, float]:
    if not -1.0 < r < 1.0:
        raise IntegratedInteractionMetaError("correlation_r must lie strictly between -1 and 1")
    z = math.atanh(r)
    if sample_size is not None and sample_size > 3:
        return z, 1.0 / (sample_size - 3)
    if variance is None:
        raise IntegratedInteractionMetaError(
            "correlation_r requires sample_size_total > 3 or source_effect_variance"
        )
    return z, variance / ((1.0 - r * r) ** 2)


def harmonize_effect_rows(rows: Iterable[Mapping[str, str]]) -> list[dict[str, str]]:
    """Validate effects and annotate common-scale or metric-specific analysis lanes.

    The common-scale column is Fisher-z of the directional association between
    higher focal trait and consumer response. Direct r/Fisher-z, Hedges g, and
    log odds ratios have documented transformations. Log response/rate ratios
    are retained in a native-metric lane rather than forcibly transformed.
    """
    result: list[dict[str, str]] = []
    effect_ids: set[str] = set()
    for source in rows:
        row = {field: _text(source.get(field)) for field in EFFECT_LEDGER_FIELDS}
        inclusion = row["full_text_inclusion"]
        if inclusion not in INCLUSION_STATES:
            raise IntegratedInteractionMetaError(
                "full_text_inclusion must be pending_full_text, included, or excluded"
            )
        if inclusion != "included":
            row["harmonization_status"] = "not_included" if inclusion == "excluded" else "pending_full_text"
            row["model_inclusion_status"] = "not_included" if inclusion == "excluded" else "pending_full_text"
            result.append(row)
            continue

        for field, allowed in (
            ("trait_role", {"A_flower", "B_flower"}),
            ("partner_role", {"pollinator", "floral_antagonist"}),
            ("mechanism_class", MECHANISM_CLASSES),
            ("organ_match", ORGAN_MATCHES),
            ("outcome_construct", OUTCOME_CONSTRUCTS),
            ("study_design", STUDY_DESIGNS),
            ("source_effect_metric", METRICS),
        ):
            if row[field] not in allowed:
                raise IntegratedInteractionMetaError(f"included row has invalid {field}: {row[field]!r}")
        expected_trait, expected_partner = ROUTE_TO_TRAIT_PARTNER.get(row["route"], ("", ""))
        if row["trait_role"] != expected_trait or row["partner_role"] != expected_partner:
            raise IntegratedInteractionMetaError("route must agree with trait_role and partner_role")
        if not row["effect_id"] or not row["independent_study_id"]:
            raise IntegratedInteractionMetaError("included row requires effect_id and independent_study_id")
        if row["effect_id"] in effect_ids:
            raise IntegratedInteractionMetaError("effect_id must be unique among included effects")
        effect_ids.add(row["effect_id"])
        if row["direction_is_higher_trait"].lower() not in {"true", "yes", "1"}:
            raise IntegratedInteractionMetaError(
                "included effect must be oriented so positive means higher trait increases consumer response"
            )

        metric = row["source_effect_metric"]
        estimate = _float(row["source_effect_estimate"], "source_effect_estimate")
        variance = _float(row["source_effect_variance"], "source_effect_variance")
        if variance <= 0:
            raise IntegratedInteractionMetaError("source_effect_variance must be positive")
        raw_n = row["sample_size_total"]
        n = int(raw_n) if raw_n else None
        if n is not None and n <= 0:
            raise IntegratedInteractionMetaError("sample_size_total must be positive")

        if metric == "fisher_z":
            z, z_variance, method = estimate, variance, "reported_fisher_z"
        elif metric == "correlation_r":
            z, z_variance = _z_from_r(estimate, variance, n)
            method = "fisher_z_from_correlation_r"
        elif metric == "hedges_g":
            z, z_variance = _z_from_g(estimate, variance)
            method = "fisher_z_from_hedges_g"
        elif metric == "log_odds_ratio":
            z, z_variance = _z_from_log_or(estimate, variance)
            method = "fisher_z_from_log_odds_ratio_via_standardized_mean_difference"
        else:
            row["harmonization_status"] = "native_metric_retained"
            row["harmonization_method"] = "no_safe_automatic_common_scale_conversion"
            row["metric_specific_analysis_lane"] = metric
            row["model_inclusion_status"] = "metric_specific_layer"
            result.append(row)
            continue

        if not math.isfinite(z) or not math.isfinite(z_variance) or z_variance <= 0:
            raise IntegratedInteractionMetaError("common-scale conversion produced invalid values")
        row["harmonization_status"] = "common_scale_ready"
        row["harmonization_method"] = method
        row["common_effect_fisher_z"] = f"{z:.12g}"
        row["common_effect_variance"] = f"{z_variance:.12g}"
        row["metric_specific_analysis_lane"] = ""
        row["model_inclusion_status"] = "integrated_common_scale_model"
        result.append(row)
    return result


def build_balance_dashboard(
    candidate_ledger: Iterable[Mapping[str, str]],
    effect_ledger: Iterable[Mapping[str, str]],
) -> list[dict[str, str]]:
    """Report large-data coverage without treating candidate rows as effects."""
    candidates = list(candidate_ledger)
    effects = harmonize_effect_rows(effect_ledger)
    candidate_counts = Counter((row["trait_role"], row["partner_role"]) for row in candidates)
    included = Counter()
    numeric = Counter()
    common = Counter()
    native = Counter()
    studies_numeric: dict[tuple[str, str], set[str]] = defaultdict(set)
    studies_common: dict[tuple[str, str], set[str]] = defaultdict(set)

    for row in effects:
        cell = (row["trait_role"], row["partner_role"])
        if row["full_text_inclusion"] != "included":
            continue
        included[cell] += 1
        if row["source_effect_metric"]:
            numeric[cell] += 1
            studies_numeric[cell].add(row["independent_study_id"])
        if row["harmonization_status"] == "common_scale_ready":
            common[cell] += 1
            studies_common[cell].add(row["independent_study_id"])
        elif row["harmonization_status"] == "native_metric_retained":
            native[cell] += 1

    rows: list[dict[str, str]] = []
    for route, (trait_role, partner_role) in ROUTE_TO_TRAIT_PARTNER.items():
        rows.append({
            "trait_role": trait_role,
            "partner_role": partner_role,
            "route": route,
            "candidate_route_rows": str(candidate_counts[(trait_role, partner_role)]),
            "full_text_included_effect_rows": str(included[(trait_role, partner_role)]),
            "numeric_effect_rows": str(numeric[(trait_role, partner_role)]),
            "common_scale_effect_rows": str(common[(trait_role, partner_role)]),
            "native_metric_effect_rows": str(native[(trait_role, partner_role)]),
            "independent_studies_numeric": str(len(studies_numeric[(trait_role, partner_role)])),
            "independent_studies_common_scale": str(len(studies_common[(trait_role, partner_role)])),
            "interpretation_boundary": (
                "Candidate-route rows are abstract-level full-text screening universe only. "
                "Numerical and common-scale counts are full-text ledger states."
            ),
        })
    return rows


def model_contract() -> str:
    """Return the primary integrated meta-regression contract."""
    return """# Integrated interaction meta-regression contract

## Primary estimand

All common-scale records are oriented so positive values mean that increasing
the focal floral trait increases the measured response of the focal consumer.
The primary effect is Fisher's z of that standardized directional association.

## Primary large-data model

```text
z_effect_i ~ trait_role_i * partner_role_i
           + mechanism_class_i
           + outcome_construct_i
           + study_design_i
           + dose_relation_i
           + consumer_specialization_i
           + alternative_resource_context_i
           + trait_role_i:partner_role_i:mechanism_class_i
           + (1 | independent_study_id)
           + (1 | species)
```

The `trait_role * partner_role` interaction estimates the broad empirical
contrast among A/P, A/H, B/P, and B/H. Mechanism, outcome construction, design,
and context remain moderators; they are not automatic pre-analysis split
points. Exact mechanism subsets are sensitivity/interpretation layers only.

## Native-metric layer

Log response ratios and log rate ratios remain in the same master ledger.
They are retained for a metric-aware model or metric-specific sensitivity
analysis until a documented common-scale conversion is justified. They are not
discarded and they are not silently coerced into Fisher-z.

## Interpretation limit

The large model can test functional separation: whether A/B traits have
different directional associations with pollinators and antagonists and whether
those associations vary by mechanism and context. It cannot by itself estimate
the within-system A-by-B interaction or the shared-cost parameter. Those need
joint-system data and remain a linked evidence layer.
"""


def _write_csv(path: Path, fields: Iterable[str], rows: Iterable[Mapping[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in writer.fieldnames})


def write_packet(
    out_dir: str | Path,
    candidate_ledger: list[dict[str, str]],
    effect_ledger: list[dict[str, str]],
) -> None:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    harmonized = harmonize_effect_rows(effect_ledger)
    _write_csv(destination / "integrated_interaction_candidate_ledger.csv", CANDIDATE_LEDGER_FIELDS, candidate_ledger)
    _write_csv(destination / "integrated_interaction_effect_ledger.csv", EFFECT_LEDGER_FIELDS, harmonized)
    _write_csv(destination / "integrated_interaction_balance_dashboard.csv", BALANCE_FIELDS, build_balance_dashboard(candidate_ledger, harmonized))
    (destination / "INTEGRATED_INTERACTION_META_MODEL_CONTRACT.md").write_text(model_contract(), encoding="utf-8")
    (destination / "README.md").write_text(
        "# Integrated interaction meta-analysis packet\n\n"
        "This packet preserves the full A/B x pollinator/antagonist candidate universe in one master ledger. "
        "Candidate rows are not effects. Full-text records keep mechanism, outcome, design, metric, and context "
        "as moderators. Only documented common-scale conversions enter the Fisher-z layer; non-convertible metrics "
        "remain in the native-metric ledger for later metric-aware analysis.\n",
        encoding="utf-8",
    )
