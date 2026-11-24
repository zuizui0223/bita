"""Source-first biological denominator and negative-mechanism diagnostic tests.

Publication source is Al-Tameemi & Rodriguez-Verdugo (2024), DOI 10.1128/
msystems.01053-24. Four lines in each exposure, not 30 x 8 colonies or six
replay tubes counted as new independent evolution origins.
"""
import json
from pathlib import Path
import pytest
from scripts.audit_bita_altameemi2024_source import (
    DOI, PMCID, PUB_URL, STUDY_FAMILY, exact_independent_hypergeometric_test,
    validate_original_source, source_record, REQUIRED,
)

ROOT=Path(__file__).resolve().parents[1]
FREEZE=(ROOT/"empirical/trait_architecture_history/"
        "altameemi2024_source_grade_evolution_and_nfds_readout.json")


def synthetic_jats(tamper_doi=False,omit_nfds=False):
    phrases=list(REQUIRED)
    if omit_nfds:
        phrases=[x for x in phrases if x!="frequency-dependent selection does not explain"]
    contents=" . ".join(phrases) + " . benzoate was not externally supplemented "
    contents+=" . 138 generations . "
    contents+= "bioinformatics and experimental evolution original peer reviewed fulltext. "*250
    doi="10.1128/not-the-original-article" if tamper_doi else DOI
    raw=(
        '<article><front><article-meta><article-id pub-id-type="doi">'+doi+
        '</article-id></article-meta></front><body><sec><title>'+
        'Phenotypic diversification persisted only in co-culture'+
        '</title><p>'+contents+'</p></sec></body></article>'
    )
    return raw.encode("utf8")


def test_original_fulltext_requires_doi_denominator_mechanism_and_caveat():
    q=validate_original_source(synthetic_jats(), "jats")
    assert q["source_type"]=="jats"
    assert q["source_sha256"]
    assert q["all_original_result_tokens_verified"] is True
    with pytest.raises(ValueError,match="wrong DOI"):
        validate_original_source(synthetic_jats(tamper_doi=True),"jats")
    with pytest.raises(ValueError,match="result token"):
        validate_original_source(synthetic_jats(omit_nfds=True),"jats")
    with pytest.raises(ValueError,match="full article"):
        validate_original_source(b"not an original full text","jats")
    with pytest.raises(ValueError,match="unsupported"):
        validate_original_source(synthetic_jats(),"markdown")


def test_true_line_level_4of4_vs_0of4_and_design_sensitive_exact_references():
    d=exact_independent_hypergeometric_test()
    assert d["co_culture_detectable_bimodal_lines"]==4
    assert d["co_culture_started_Pputida_lines"]==4
    assert d["mono_culture_detectable_bimodal_lines"]==0
    assert d["mono_culture_started_Pputida_lines"]==4
    assert d["unpaired_Fisher_table_allocations"]==70
    assert d["unpaired_Fisher_two_sided_p_descriptive"]==pytest.approx(2/70)
    assert d["conditional_pairing_4_discordant_pairs_exact_two_sided_p_sensitivity"]==.125
    assert d["post_source_analytical_tests_not_preregistered"]
    assert d["pairing_requires_source_lineage_adjudication"]


def test_maintenance_is_not_origination_and_simple_nfds_is_not_identified():
    receipt=validate_original_source(synthetic_jats(),"jats")
    d=source_record(receipt,[{"provider":"synthetic","valid_original_fulltext":True}])
    assert d["paper_DOI"]==DOI
    assert d["original_article_PMCID"]==PMCID
    assert d["one_new_independent_programme_relative_to_current_BITA_11"] is True
    evo=d["source_evolution"]
    assert evo["Pputida_coculture_bimodal_lines_at_endpoint"]==4
    assert evo["Pputida_monoculture_bimodal_lines_at_endpoint"]==0
    assert evo["Pputida_monoculture_larger_morphotype_appeared_during_evolution"] is True
    assert evo["Pputida_coculture_larger_morphotype_appeared_during_evolution"] is True
    assert evo["source_historical_origin_probability_4of4_vs_0of4"] is False
    assert evo["isolated_colonies_do_not_count_as_independent_founding_lines"] is True
    mechanism=d["mechanism_diagnostics"]
    assert mechanism["reciprocal_invasion_pair_source_replicate_2_only"] is True
    assert mechanism["reciprocal_invasion_negative_frequency_dependence_not_supported"] is True
    assert mechanism["this_does_not_rule_out_frequency_dependence_in_whole_multigenotype_population"] is True
    assert mechanism["published_pooled_rare_genotype_fitness_p_for_Ajohnsonii_presence"]==.814
    assert mechanism["replay_uses_one_original_138_generation_coculture_population"]
    assert mechanism["replay_tubes_per_Ajohnsonii_present_absent_arm"]==6
    assert mechanism["without_Ajohnsonii_both_morphotypes_not_extinct"] is True
    assert d["cross_programme_comparability"]["resource_demand_confound_benzoate_not_externally_supplied_to_mono"]
    assert d["cross_programme_comparability"]["no_ancestral_same_genotype_two_function_optimum_test"]


def test_article_binary_unavailable_cannot_be_invented():
    r=source_record(None, [{"provider":"EuropePMC","valid_original_fulltext":False}])
    assert r["article_source_receipt"] is None
    assert r["source_grade"]=="PUBLISHER_WEB_FULLTEXT_VERIFIED_SEPARATELY_ORIGINAL_BINARY_NOT_RETRIEVED"


def test_frozen_source_outcome_roundtrip():
    if not FREEZE.exists():
        pytest.skip("source original binary grade awaits first reproducible freeze")
    d=json.loads(FREEZE.read_text())
    assert d["paper_DOI"]==DOI
    assert d["source_evolution"]["Pputida_coculture_bimodal_lines_at_endpoint"]==4
    assert d["source_evolution"]["Pputida_monoculture_bimodal_lines_at_endpoint"]==0
    assert d["mechanism_diagnostics"]["reciprocal_invasion_negative_frequency_dependence_not_supported"]
    assert d["mechanism_diagnostics"]["without_Ajohnsonii_both_morphotypes_not_extinct"]
    assert d["source_specific_4_arm_exact_sensitivity"]["unpaired_Fisher_two_sided_p_descriptive"]==pytest.approx(2/70)
    assert d["source_specific_4_arm_exact_sensitivity"]["conditional_pairing_4_discordant_pairs_exact_two_sided_p_sensitivity"]==.125
    assert d["cross_programme_comparability"]["no_genetic_module_duplication_established"] is True
    # Strict derived source record equality; runtime receipt is trusted only
    # if the full original source is truly available and its digest matches.
    assert d["source_specific_4_arm_exact_sensitivity"]==exact_independent_hypergeometric_test()
