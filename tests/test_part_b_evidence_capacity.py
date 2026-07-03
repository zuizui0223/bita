from collections import Counter

from trait_architecture.broad_meta_analysis import EFFECT_FIELDS, ORIENTATION, read_csv_rows, read_strata
from trait_architecture.part_b_evidence_capacity import (
    evidence_capacity_diagnostics,
    evidence_inventory,
    quantitative_capacity,
)


REPO_ROUTE_RECORDS = "empirical/broad_reality_evidence/broad_route_records.csv"
REPO_EFFECTS = "empirical/broad_reality_evidence/part_b_arrow_effects.csv"
REPO_STRATA = "empirical/broad_reality_evidence/part_b_arrow_strata.csv"


def _effect(cluster: str, value: float) -> dict[str, str]:
    row = {field: "" for field in EFFECT_FIELDS}
    row.update({
        "effect_id": f"effect_{cluster}",
        "study_id": cluster,
        "study_cluster_id": cluster,
        "route": "B_to_pollination",
        "trait_role": "B",
        "trait_class": "chemical_barrier",
        "outcome_class": "visitation_rate",
        "design_class": "manipulation",
        "effect_input_type": "reported_effect",
        "effect_metric": "log_response_ratio",
        "effect_value": str(value),
        "standard_error": "0.15",
        "effect_orientation": ORIENTATION,
        "is_primary_effect": "true",
        "analysis_status": "eligible_for_quantitative_synthesis",
    })
    return row


def _stratum() -> dict[str, str]:
    return {
        "stratum_id": "BP_chemical_visitation_lrr_manipulation",
        "route": "B_to_pollination",
        "trait_class": "chemical_barrier",
        "outcome_class": "visitation_rate",
        "effect_metric": "log_response_ratio",
        "design_class": "manipulation",
        "min_clusters_exploratory": "3",
        "min_clusters_stability": "5",
        "expected_effect_direction": "negative",
        "part_i_parameter": "c_D",
        "interpretation": "demo",
    }


def test_repo_inputs_remain_multilayer_not_forced_to_pool() -> None:
    inventory = evidence_inventory(
        read_csv_rows(REPO_ROUTE_RECORDS),
        read_csv_rows(REPO_EFFECTS),
    )
    tiers = Counter(row["evidence_tier"] for row in inventory)
    # The current source-adjudicated direction map has thirteen primary records;
    # the five verified numerical anchors have not yet been duplicated into it.
    assert tiers["directional_only"] == 13
    assert tiers["quantitative_without_directional_record"] == 5

    capacity = quantitative_capacity(read_csv_rows(REPO_EFFECTS), read_strata(REPO_STRATA))
    statuses = Counter(row["capacity_status"] for row in capacity)
    assert statuses["single_quantitative_estimate"] == 5
    assert statuses["exploratory_synthesis_candidate"] == 0
    diagnostics = evidence_capacity_diagnostics(inventory, capacity)
    assert diagnostics["recommended_primary_synthesis"] == "multilayer_evidence_map_with_individual_effect_inventory"
    assert diagnostics["direct_interaction_identification"] == "not_assessed_by_marginal_route_inputs"


def test_three_compatible_clusters_are_only_an_exploratory_capacity_state() -> None:
    capacity = quantitative_capacity(
        [_effect("c1", -0.2), _effect("c2", -0.3), _effect("c3", -0.1)],
        [_stratum()],
    )
    assert capacity[0]["independent_clusters"] == 3
    assert capacity[0]["capacity_status"] == "exploratory_synthesis_candidate"
    assert "small-k limitation" in str(capacity[0]["recommended_action"])
