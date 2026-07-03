"""Capacity diagnostics for a layered Part B evidence synthesis.

This module does not manufacture comparability between studies.  It reports every
registered source at the strongest role justified by its current extraction state:

* a primary numerical effect in a declared compatibility stratum;
* a direct-route directional record without a numerical effect; or
* an unassessed / excluded source candidate.

It also audits each pre-registered quantitative stratum.  A stratum with three
clusters is an *exploratory synthesis candidate*, not a completed or stable
meta-analysis.  The marginal-route inputs cannot identify an A x D interaction;
that question is deliberately reported as not assessed rather than inferred from
separate arrows.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable, Mapping

from .broad_meta_analysis import (
    DIRECT_ROUTES,
    ROUTE_EXPECTED_SIGN,
    _bool,
    _text,
    effect_estimate,
    validate_effect_rows,
    validate_route_records,
)


EVIDENCE_INVENTORY_FIELDS = (
    "evidence_id", "source_kind", "study_id", "study_cluster_id", "doi", "taxon",
    "route", "trait_class", "outcome_class", "design_class", "effect_metric",
    "evidence_tier", "reported_direction", "numeric_effect_count", "record_status",
    "source_basis", "source_locator", "context_or_extraction_note",
)

QUANTITATIVE_CAPACITY_FIELDS = (
    "stratum_id", "route", "trait_class", "outcome_class", "effect_metric",
    "design_class", "expected_effect_direction", "part_i_parameter",
    "independent_clusters", "primary_effect_count", "min_clusters_exploratory",
    "min_clusters_stability", "capacity_status", "recommended_action",
)


def _direction_key(row: Mapping[str, str]) -> tuple[str, str, str, str, str]:
    """Identity shared by route-direction and effect records before metric choice."""

    return (
        _text(row.get("study_cluster_id")),
        _text(row.get("route")),
        _text(row.get("trait_class")),
        _text(row.get("outcome_class")),
        _text(row.get("design_class")),
    )


def _numeric_effects_by_direction_key(
    effect_rows: Iterable[Mapping[str, str]],
) -> dict[tuple[str, str, str, str, str], list[Mapping[str, str]]]:
    """Return primary eligible numerical effects linked to a route-direction cell."""

    grouped: dict[tuple[str, str, str, str, str], list[Mapping[str, str]]] = defaultdict(list)
    for row in validate_effect_rows(effect_rows):
        if (
            _text(row.get("analysis_status")) == "eligible_for_quantitative_synthesis"
            and _bool(row.get("is_primary_effect"))
        ):
            # Validate numerical recoverability here; invalid rows must not be promoted.
            effect_estimate(dict(row))
            grouped[_direction_key(row)].append(row)
    return grouped


def evidence_inventory(
    route_rows: Iterable[Mapping[str, str]],
    effect_rows: Iterable[Mapping[str, str]],
) -> list[dict[str, object]]:
    """Emit one joined source cell at its highest currently justified evidence tier.

    Directional records are joined to numerical effects only when they share the
    same independent study cluster, direct route, trait class, outcome class, and
    design.  Numerical effects without a registered directional record are retained
    as orphan quantitative cells rather than silently discarded.
    """

    valid_routes = validate_route_records(route_rows)
    numeric_by_key = _numeric_effects_by_direction_key(effect_rows)
    route_keys: set[tuple[str, str, str, str, str]] = set()
    output: list[dict[str, object]] = []

    for row in valid_routes:
        if not _bool(row.get("is_primary_sign_record")):
            continue
        key = _direction_key(row)
        route_keys.add(key)
        status = _text(row.get("record_status"))
        linked_effects = numeric_by_key.get(key, [])
        if status == "included_for_direction_map" and linked_effects:
            tier = "quantitative_with_directional_record"
        elif status == "included_for_direction_map":
            tier = "directional_only"
        elif status == "unassessed":
            tier = "unassessed_candidate"
        else:
            tier = "excluded_candidate"
        output.append({
            "evidence_id": _text(row.get("record_id")),
            "source_kind": "route_record",
            "study_id": _text(row.get("study_id")),
            "study_cluster_id": _text(row.get("study_cluster_id")),
            "doi": _text(row.get("doi")),
            "taxon": _text(row.get("taxon")),
            "route": _text(row.get("route")),
            "trait_class": _text(row.get("trait_class")),
            "outcome_class": _text(row.get("outcome_class")),
            "design_class": _text(row.get("design_class")),
            "effect_metric": ";".join(sorted({_text(item.get("effect_metric")) for item in linked_effects})),
            "evidence_tier": tier,
            "reported_direction": _text(row.get("reported_direction")),
            "numeric_effect_count": len(linked_effects),
            "record_status": status,
            "source_basis": _text(row.get("source_basis")),
            "source_locator": "",
            "context_or_extraction_note": _text(row.get("context_note")),
        })

    # Preserve numerical anchors that were entered from a verified effect registry
    # before a matching directional source record was registered.
    for effects in numeric_by_key.values():
        for row in effects:
            if _direction_key(row) in route_keys:
                continue
            output.append({
                "evidence_id": _text(row.get("effect_id")),
                "source_kind": "quantitative_effect",
                "study_id": _text(row.get("study_id")),
                "study_cluster_id": _text(row.get("study_cluster_id")),
                "doi": _text(row.get("doi")),
                "taxon": _text(row.get("taxon")),
                "route": _text(row.get("route")),
                "trait_class": _text(row.get("trait_class")),
                "outcome_class": _text(row.get("outcome_class")),
                "design_class": _text(row.get("design_class")),
                "effect_metric": _text(row.get("effect_metric")),
                "evidence_tier": "quantitative_without_directional_record",
                "reported_direction": "",
                "numeric_effect_count": 1,
                "record_status": _text(row.get("analysis_status")),
                "source_basis": _text(row.get("source_basis")),
                "source_locator": _text(row.get("source_locator")),
                "context_or_extraction_note": _text(row.get("extraction_note")),
            })

    return sorted(output, key=lambda item: (str(item["route"]), str(item["evidence_tier"]), str(item["evidence_id"])))


def quantitative_capacity(
    effect_rows: Iterable[Mapping[str, str]],
    strata: Iterable[Mapping[str, str]],
) -> list[dict[str, object]]:
    """Audit all pre-registered quantitative cells without pooling them.

    A cell becomes an exploratory candidate only when it reaches its declared
    exploratory cluster threshold.  It becomes a stable candidate only at its
    declared stability threshold.  These labels report capacity, never a result.
    """

    valid_effects = validate_effect_rows(effect_rows)
    primary = [
        row for row in valid_effects
        if _text(row.get("analysis_status")) == "eligible_for_quantitative_synthesis"
        and _bool(row.get("is_primary_effect"))
    ]
    output: list[dict[str, object]] = []
    for stratum in strata:
        matching = [
            row for row in primary
            if all(_text(row.get(field)) == _text(stratum.get(field)) for field in (
                "route", "trait_class", "outcome_class", "effect_metric", "design_class",
            ))
        ]
        for row in matching:
            effect_estimate(dict(row))
        clusters = {_text(row.get("study_cluster_id")) for row in matching}
        k = len(clusters)
        exploratory = int(_text(stratum.get("min_clusters_exploratory")))
        stability = int(_text(stratum.get("min_clusters_stability")))
        if k == 0:
            capacity_status = "no_quantitative_effect"
            action = "retain as a mapped evidence gap; collect a compatible numerical effect"
        elif k == 1:
            capacity_status = "single_quantitative_estimate"
            action = "report the individual estimate; do not pool or estimate heterogeneity"
        elif k < exploratory:
            capacity_status = "multiple_estimates_below_exploratory_threshold"
            action = f"report individual estimates; collect {exploratory - k} compatible independent cluster(s)"
        elif k < stability:
            capacity_status = "exploratory_synthesis_candidate"
            action = "an exploratory pooled summary may be shown with an explicit small-k limitation"
        else:
            capacity_status = "stable_synthesis_candidate"
            action = "assess clinical/biological comparability and risk of bias before a formal pooled estimate"
        output.append({
            "stratum_id": _text(stratum.get("stratum_id")),
            "route": _text(stratum.get("route")),
            "trait_class": _text(stratum.get("trait_class")),
            "outcome_class": _text(stratum.get("outcome_class")),
            "effect_metric": _text(stratum.get("effect_metric")),
            "design_class": _text(stratum.get("design_class")),
            "expected_effect_direction": _text(stratum.get("expected_effect_direction")),
            "part_i_parameter": _text(stratum.get("part_i_parameter")),
            "independent_clusters": k,
            "primary_effect_count": len(matching),
            "min_clusters_exploratory": exploratory,
            "min_clusters_stability": stability,
            "capacity_status": capacity_status,
            "recommended_action": action,
        })
    return output


def evidence_capacity_diagnostics(
    inventory_rows: Iterable[Mapping[str, object]],
    capacity_rows: Iterable[Mapping[str, object]],
) -> dict[str, object]:
    """Summarise what the current committed inputs can and cannot identify."""

    inventory = list(inventory_rows)
    capacity = list(capacity_rows)
    tiers = Counter(str(row.get("evidence_tier", "")) for row in inventory)
    capacity_statuses = Counter(str(row.get("capacity_status", "")) for row in capacity)
    exploratory = capacity_statuses["exploratory_synthesis_candidate"]
    stable = capacity_statuses["stable_synthesis_candidate"]
    return {
        "evidence_inventory_cells": len(inventory),
        "quantitative_effect_cells": (
            tiers["quantitative_with_directional_record"]
            + tiers["quantitative_without_directional_record"]
        ),
        "directional_only_cells": tiers["directional_only"],
        "unassessed_candidate_cells": tiers["unassessed_candidate"],
        "excluded_candidate_cells": tiers["excluded_candidate"],
        "configured_quantitative_cells": len(capacity),
        "exploratory_synthesis_candidate_cells": exploratory,
        "stable_synthesis_candidate_cells": stable,
        "direct_interaction_identification": "not_assessed_by_marginal_route_inputs",
        "recommended_primary_synthesis": (
            "multilayer_evidence_map_with_individual_effect_inventory"
            if exploratory == 0 else "multilayer_evidence_map_plus_limited_exploratory_quantitative_synthesis"
        ),
        "interpretation_boundary": (
            "This diagnostic classifies registered marginal-route evidence only. It does not "
            "infer a direct A_x_D interaction from separate arrows, and it does not treat an "
            "exploratory capacity label as a completed meta-analysis."
        ),
    }
