"""v2 sourced 12-programme architecture evidence: no new denominator inflation.

This compares 11-programme frozen parent with the Al-Tameemi source and
does not treat 2024 follow-up to the original 200-gen evolution paper
as another distinct original founder programme.
"""
import json
from pathlib import Path
import pytest
from scripts.audit_bita_cross_programme_extension_12 import (
    DOI, EXPECTED_ARTICLE_SHA256, NEW_FILE, PARENT_FILE, SOURCE,
    extend,
)
from scripts.audit_bita_cross_programme_architecture_chain import (
    read_source_catalogue,synthesize,
)

ROOT=Path(__file__).resolve().parents[1]
FROZEN=SOURCE/"bita_architecture_cross_programme_v2_12_sources_20261124.json"


def result():
    return extend()


def test_original_source_identity_new_programme_not_original_2019_doubled():
    d=result()
    assert len(d["entries"])==12
    assert d["number_of_unique_independent_research_programmes"]==12
    assert d["number_of_distinct_machine_read_source_receipts"]==14
    assert len(d["source_receipts_sha256"])==14
    ids=[x["programme_id"] for x in d["entries"]]
    assert ids.count("ALTAMEEMI2024")==1
    assert len(set(ids))==12
    assert {x["original_publication_doi"] for x in d["entries"]}.__len__()==12
    assert d["programme_to_receipt_mapping"]["ALTAMEEMI2024"]==[NEW_FILE]
    assert d["interpretation_contract"]["AlTameemi_and_original_2019_200_generation_evolution_same_programme"]
    assert d["interpretation_contract"]["AlTameemi_2026_potential_followup_not_automatically_independent"]


def test_11_programme_source_freeze_untouched_and_v2_is_append_only():
    parents,hashes=read_source_catalogue()
    original=synthesize(parents,hashes)
    d=result()
    assert d["entries"][:11]==original["entries"]
    assert d["descriptive_catalogue_counts_not_natural_prevalence"][
        "programmes_with_forward_specialist_phenotype_or_partner_emergence"] == 3
    assert d["descriptive_catalogue_counts_not_natural_prevalence"][
        "programmes_with_unscreened_founder_denominator_for_forward_specialization"] == 1
    assert d["descriptive_catalogue_counts_not_natural_prevalence"][
        "programmes_with_registered_maintenance_or_group_intervention"]==6
    assert d["descriptive_catalogue_counts_not_natural_prevalence"][
        "programmes_with_reverse_autonomy_or_partner_exit"]==2
    assert d["descriptive_catalogue_counts_not_natural_prevalence"][
        "programmes_identifying_historical_ancestral_within_genotype_two_function_module_split"]==0
    assert d["descriptive_catalogue_counts_not_natural_prevalence"][
        "programmes_closing_L_to_occupancy_full_chain"]==0
    assert d["interpretation_contract"]["no_meta_analysis"]
    assert d["interpretation_contract"]["programmes_still_unpooled"]


def test_forward_role_split_must_not_confuse_retained_bimodality():
    d=result()
    q=d["entries"][-1]
    assert q["programme_id"]=="ALTAMEEMI2024"
    assert q["original_publication_doi"]==DOI
    assert q["registered_source_counts"]["coculture_bimodal_at_gen200"]==4
    assert q["registered_source_counts"]["coculture_started_evolving_Pputida_lines"]==4
    assert q["registered_source_counts"]["monoculture_bimodal_at_gen200"]==0
    assert q["registered_source_counts"]["monoculture_started_evolving_Pputida_lines"]==4
    assert q["founder_denominator_for_endpoint_polymorphism_available"]
    assert q["forward_founder_denominator_available"] is False
    assert q["observed_forward_specialist_phenotype_or_partner_emergence"] is False
    assert q["retained_two_morphotypes_in_coculture_after_evolution"]
    assert q["maintenance_or_group_intervention_present"]
    assert q["ancestral_within_genotype_two_function_module_split_identified"] is False
    assert q["matched_ancestral_shared_coordinate_conflict_fitness_assayed"] is False
    assert q["fully_identifies_L_R_Phi_K_accessibility_invasion_fixation_occupancy"] is False


def test_original_fisher_and_pairing_sensitivities_separate():
    d=result()
    q=d["new_12th_programme_specific_claim"]
    assert q["founder_4x4_unpaired_reference_p"]==pytest.approx(2/70)
    assert q["paired_original_founder_block_reference_p"]==.125
    assert q["negative_focal_clone_pair_NFDS_test_not_supported"] is True
    assert q["whole_population_crossfed_replay_no_morphotype_extinction_with_partner_removed"] is True
    assert q["replay_technical_6_per_arm_not_independent_parent_histories"] is True
    assert q["not_original_two_task_module_origin"] is True
    assert q["biotic_vs_resource_supplied_not_deconfounded"] is True
    assert d["interpretation_contract"]["new_4of4_vs0of4_measures_retained_polymorphism_not_first_origin_frequency"]
    assert d["interpretation_contract"]["source_NFDS_unconfirmed_in_focal_pair_not_proof_of_no_NFDS_globally"]
    assert d["interpretation_contract"]["Fisher_vs_possible_founder_pairing_exact_tests_not_conflated"]
    assert d["interpretation_contract"]["technically_replicated_replay_of_one_line_not_six_independent_origins"]


def test_all_source_SHA_ids_are_regenerated_and_new_JATS_fulltext_verified():
    d=result()
    source=json.loads((SOURCE/NEW_FILE).read_text())
    assert source["paper_DOI"]==DOI
    assert source["article_source_receipt"]["source_sha256"]==EXPECTED_ARTICLE_SHA256
    assert source["article_source_receipt"]["source_type"]=="jats"
    assert len(source["retrieval_receipts"])==1
    assert source["retrieval_receipts"][0]["valid_original_fulltext"]
    assert source["mechanism_diagnostics"]["reciprocal_invasion_pair_source_replicate_2_only"]
    assert source["cross_programme_comparability"]["resource_demand_confound_benzoate_not_externally_supplied_to_mono"]


def test_frozen_12_programme_roundtrip():
    if not FROZEN.exists():
        pytest.skip("12-programme output to be source-frozen first")
    actual=result()
    expected=json.loads(FROZEN.read_text())
    assert actual==expected
