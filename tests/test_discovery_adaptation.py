from trait_architecture.discovery_adaptation import DiscoveryRound, decide_next_strategy, round_from_records


def test_short_round_must_finish_fixed_batch() -> None:
    decision = decide_next_strategy(DiscoveryRound("image_observation_genus_action", 2, 1, 1, 0))
    assert decision.status == "continue_batch"
    assert decision.next_strategy_id == "image_observation_genus_action"


def test_zero_action_batch_pivots() -> None:
    decision = decide_next_strategy(DiscoveryRound("image_observation_genus_action", 20, 0, 0, 0))
    assert decision.status == "pivot_source_class"
    assert decision.next_strategy_id == "source_internal_action_search"


def test_action_only_batch_is_not_promoted_to_trait_analysis() -> None:
    decision = decide_next_strategy(DiscoveryRound("image_observation_genus_action", 20, 4, 2, 0))
    assert decision.status == "retain_for_action_only_and_pivot_plant_search"
    assert decision.next_strategy_id == "source_internal_action_search"


def test_trait_ready_yield_expands_strategy() -> None:
    decision = decide_next_strategy(DiscoveryRound("image_observation_genus_action", 20, 4, 2, 1))
    assert decision.status == "expand_strategy"
    assert decision.next_strategy_id == "image_observation_genus_action"


def test_record_summary_requires_taxonomic_resolution_for_trait_ready() -> None:
    records = [
        {"action_status": "material_action_confirmed", "plant_taxon_status": "genus_only"},
        {"action_status": "material_action_confirmed", "plant_taxon_status": "accepted"},
        {"action_status": "needs_source_review", "plant_taxon_status": "accepted"},
    ]
    summary = round_from_records("source_internal_action_search", records)
    assert summary.candidates_checked == 3
    assert summary.direct_actions == 2
    assert summary.plant_named_any_rank == 2
    assert summary.trait_ready_records == 1
