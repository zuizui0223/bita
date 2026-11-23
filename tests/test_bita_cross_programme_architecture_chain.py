"""Source-grain and no-overclaim tests for the 11-programme evidence matrix.

The 11 source programmes are a PURPOSEFUL research catalogue, not a
systematic sample, so no pooled source incidence or global origin rate.
"""
from __future__ import annotations
import copy
import json
import math
from pathlib import Path

import pytest
from scripts.audit_bita_cross_programme_architecture_chain import (
    DOI, ROLES, SOURCE_FILES, INDIVIDUAL_SOURCE_PATHS,
    read_source_catalogue, check_sources, synthesize, exact_ratio,
)

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"empirical/trait_architecture_history/bita_architecture_cross_programme_evidence_20261124.json"


def assembled():
    f,h=read_source_catalogue()
    return f,h,synthesize(f,h)


def test_exact_distinct_research_programmes_and_double_count_guards():
    f,h,report=assembled()
    assert len(DOI)==len(ROLES)==len(report["entries"])==11
    assert len(SOURCE_FILES)==len(h)==13
    entries=report["entries"]
    assert len({x["original_publication_doi"] for x in entries})==11
    assert len({x["programme_id"] for x in entries})==11
    assert all(x["fully_identifies_L_R_Phi_K_accessibility_invasion_fixation_occupancy"] is False for x in entries)
    assert all(x["ancestral_within_genotype_two_function_module_split_identified"] is False for x in entries)
    assert report["programme_sampling_frame"].startswith("purposefully selected")
    assert report["interpretation_contract"]["Pineau_4_derivative_receipts_count_as_one_programme"]
    assert report["interpretation_contract"]["Kim_and_Zhang_shared_receipt_count_as_two_separate_original_programmes"]
    assert report["interpretation_contract"]["Bacillus_two_article_programme_counted_once"]
    assert report["interpretation_contract"]["no_meta_analysis"]


def test_source_held_lineage_counts_distinct_from_selected_clone_and_assay_counts():
    _,_,r=assembled()
    entry={x["programme_id"]:x for x in r["entries"]}
    pine=entry["PINEAU2024"]
    assert pine["forward_founder_denominator_available"] is True
    assert pine["registered_source_counts"]["evolved_divergent_populations"]==3
    assert pine["registered_source_counts"]["evolved_PO_populations_started"]==5
    assert pine["registered_source_counts"]["QA_valid_Small_replay_day40_populations"]==3
    assert pine["registered_source_counts"]["QA_valid_Large_replay_day40_populations"]==2
    assert pine["registered_source_counts"]["excluded_duplicated_original_area_pairs"]==164
    assert pine["registered_source_counts"]["PO4_standard_O2_competitions"]==8
    assert pine["registered_source_counts"]["PO4_supplemented_O2_competitions"]==7
    assert pine["registered_source_counts"]["QA_valid_Small_mean_day40_minus_first_radius_um"]==pytest.approx(9.012177598717132)
    assert pine["registered_source_counts"]["QA_valid_Large_mean_day40_minus_first_radius_um"]==pytest.approx(-5.975551045357875)
    assert entry["KIM2016"]["registered_source_counts"]["individually_chosen_successful_D_fan_mutants"]==20
    assert entry["KIM2016"]["forward_founder_denominator_available"] is False
    assert entry["ZHANG2020"]["registered_source_counts"]["selected_mutants"]==30
    assert entry["BACILLUS_DRAGOS"]["registered_source_counts"]["mixed_cultures_eps_partner_extinct"]==4
    assert entry["BACILLUS_DRAGOS"]["registered_source_counts"]["mixed_cultures_started"]==6
    assert entry["CHEN2024"]["registered_source_counts"]["autonomist_events_by_regime"]==[0,0,5]
    assert entry["CHEN2024"]["registered_source_counts"]["started_lines_by_regime"]==[12,12,12]
    assert entry["DSOUZA2016"]["registered_source_counts"]["AA_supplied_started_lines"]==8
    assert entry["DSOUZA2016"]["registered_source_counts"]["AA_supplied_detectable_auxotroph_lines_gen2000"]==6
    assert entry["KINSLER2024"]["registered_source_counts"]["Evo2D_selected_clones"]==306
    assert entry["KINSLER2024"]["registered_source_counts"]["Evo3D_selected_clones"]==202
    assert entry["DESPRES2024"]["registered_source_counts"]["strict_heteromer_rescue_pairs"]==22
    assert entry["DESPRES2024"]["registered_source_counts"]["pairs_with_both_parent_controls"]==105
    assert entry["NASVALL2026"]["registered_source_counts"]["mutator_started"]==24
    assert entry["NASVALL2026"]["registered_source_counts"]["nonmutator_started"]==24
    assert entry["COGFP2025"]["registered_source_counts"]["two_gene_copy_subfunctionalization_in_source"] is False


def test_source_frozen_coverage_is_descriptive_not_meta_analysis_or_prevalence():
    _,_,report=assembled()
    counts=report["descriptive_catalogue_counts_not_natural_prevalence"]
    assert counts=={
        "programmes_with_forward_specialist_phenotype_or_partner_emergence":3,
        "programmes_with_unscreened_founder_denominator_for_forward_specialization":1,
        "programmes_with_registered_maintenance_or_group_intervention":5,
        "programmes_with_reverse_autonomy_or_partner_exit":2,
        "programmes_identifying_historical_ancestral_within_genotype_two_function_module_split":0,
        "programmes_closing_L_to_occupancy_full_chain":0,
    }
    assert report["interpretation_contract"]["no_inferred_cross_programme_effect_size_or_origin_rate"]
    assert report["interpretation_contract"]["no_prevalence_in_nature_or_complete_literature_universe"]
    for row in report["entries"]:
        assert row["source_specific_limit"]
        assert row["authoritative_existing_original_source_receipts"]
        assert set(row["authoritative_existing_original_source_receipts"])==set(
            INDIVIDUAL_SOURCE_PATHS[row["programme_id"]])


def test_fails_closed_on_source_identity_falsification_and_sample_inflation():
    sources,digests,_=assembled()
    wrong=copy.deepcopy(sources)
    wrong["pineau2024_original_forward_divergence.json"]["single_evolution_programme"][
        "independent_initial_aerobic_populations"]=100
    with pytest.raises(ValueError,match="Pineau"):
        synthesize(wrong,digests)
    wrong=copy.deepcopy(sources)
    wrong["pineau2024_f5_original_replay_readout.json"][
        "primary_quarantined_independent_day40_endpoints"]["small"][
            "independent_original_population_day40_endpoints_after_QA"]=4
    with pytest.raises(ValueError,match="Pineau"):
        synthesize(wrong,digests)
    wrong=copy.deepcopy(sources)
    wrong["pineau2024_publisher_source_adjudication.json"]["publisher_source_downloaded"]=True
    with pytest.raises(ValueError,match="publisher"):
        synthesize(wrong,digests)
    wrong=copy.deepcopy(sources)
    wrong["chen2024_autonomy_reversal_readout.json"]["forward_specialization_origin_identified"]=True
    with pytest.raises(ValueError,match="Chen"):
        synthesize(wrong,digests)
    wrong=copy.deepcopy(sources)
    wrong["mridha2022_published_stats_readout.json"]["environmental_strata_n"]=10
    with pytest.raises(ValueError,match="Mridha"):
        synthesize(wrong,digests)
    wrong=copy.deepcopy(sources)
    wrong["kim_zhang_forward_dol_readout.json"]["comparison"]["independent_research_programmes"]=20
    with pytest.raises(ValueError,match="Kim"):
        synthesize(wrong,digests)


def test_source_receipts_recomputed_exactly_equal_to_frozen_json():
    _,_,actual=assembled()
    if not OUTPUT.exists():
        pytest.skip("first original source assembly requires frozen derived JSON")
    expected=json.loads(OUTPUT.read_text(encoding="utf8"))
    assert actual==expected


def test_ratio_guards_on_biological_unit():
    assert exact_ratio(3,5)==.6
    assert exact_ratio(5,12)==5/12
    with pytest.raises(ValueError):
        exact_ratio(20,0)
    with pytest.raises(ValueError):
        exact_ratio(3,2)
