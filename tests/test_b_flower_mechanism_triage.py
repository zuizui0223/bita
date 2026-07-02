from trait_architecture.b_flower_mechanism_triage import build_b_triage


def candidate(candidate_id, routes, title, abstract, *, empirical=True, experimental=False, statistics=False):
    return {
        "candidate_id": candidate_id,
        "doi": f"10.test/{candidate_id}",
        "title": title,
        "publication_year": "2024",
        "work_type": "journal-article",
        "container_title": "Test Journal",
        "publisher": "Test Publisher",
        "source_queries": "test",
        "route_families": routes,
        "source_bucket": "empirical_nonreview" if empirical else "other",
        "route_memberships": routes,
        "screening_priority": "tier_3_empirical_full_text_screen",
        "cue_experimental": str(experimental).lower(),
        "cue_choice": "false",
        "cue_association": "false",
        "cue_effect_statistics": str(statistics).lower(),
        "crossref_abstract_text": abstract,
    }


def test_b_to_antagonist_is_censused_even_when_rank_is_low():
    rows = [
        candidate("bh_low", "B_to_antagonist", "Reproductive isolation", "Hybridization and self-incompatibility in flowers."),
        candidate("bh_high", "B_to_antagonist", "Floral trichomes", "Floral trichomes deter florivory damage in an experiment.", experimental=True, statistics=True),
        candidate("bp_high", "B_to_pollinator", "Nectar nicotine", "Nicotine in floral nectar changes bumblebee visitation in a treatment experiment.", experimental=True, statistics=True),
        candidate("bp_low", "B_to_pollinator", "Pollination ecology", "Pollination ecology of a species."),
    ]
    triage, batch, screening = build_b_triage(rows, b_pollinator_topup=1)

    by_id = {row["candidate_id"]: row for row in triage}
    assert by_id["bh_low"]["selection_lane"] == "B_to_antagonist_census"
    assert by_id["bh_high"]["selection_lane"] == "B_to_antagonist_census"
    assert by_id["bp_high"]["selection_lane"] == "B_to_pollinator_mechanism_topup"
    assert by_id["bp_low"]["selection_lane"] == "not_batch_1"
    assert {row["candidate_id"] for row in batch} == {"bh_low", "bh_high", "bp_high"}
    assert len(screening) == 3


def test_mechanism_signal_outranks_generic_pollination_context_for_b_to_pollinator_topup():
    rows = [
        candidate("mechanism", "B_to_pollinator", "Toxic nectar", "Nectar alkaloids act as floral deterrents and alter bee foraging preference.", experimental=True, statistics=True),
        candidate("generic", "B_to_pollinator", "Pollination ecology", "Pollination ecology and pollination syndrome are described for the species.", experimental=True, statistics=True),
    ]
    triage, batch, _ = build_b_triage(rows, b_pollinator_topup=1)
    by_id = {row["candidate_id"]: row for row in triage}
    assert int(by_id["mechanism"]["priority_score"]) > int(by_id["generic"]["priority_score"])
    assert [row["candidate_id"] for row in batch] == ["mechanism"]
