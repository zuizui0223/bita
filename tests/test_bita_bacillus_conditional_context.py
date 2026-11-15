"""Source-locked conditional epistasis and preadaptation tests, one Bacillus programme."""
import json
from pathlib import Path
import pytest
from scripts.analyze_bita_bacillus_conditional_context import analyse_context, wilson95, verify_pdf_sources

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'empirical/trait_architecture_history/bacillus2018_partner_history_source_coding.json'

def load():
    return json.loads(DATA.read_text(encoding='utf8'))

def test_mutation_effect_is_background_specific_not_two_sign_reversals():
    x=analyse_context(load())
    assert x['two_source_tasa_alleles']==['Y124C','G183C']
    assert x['changed_conditional_benefit_n']==2
    assert x['strict_productivity_sign_reversal'] == ['G183C']
    assert x['eps_present_no_demonstrated_gain'] == ['Y124C']
    assert x['eps_present_both_mutants_reduce_water_repellency'] is True

def test_two_tasa_routes_have_opposite_bsla_dependency():
    x=analyse_context(load())
    assert x['bslA_deletion_results']=={
      'e4A_Y124C':'pellicle_abolished',
      'e6A_G183C':'pellicle_maintained'}
    assert x['bslA_universally_required'] is False
    assert x['independent_evolved_tasa_cys_lineages']==2
    assert x['descendant_isolates_not_independent_origins']==6

def test_partner_preadaptation_matrix_does_not_assume_numeric_raw_fitness():
    x=analyse_context(load())
    assert x['partner_swaps']=={
      'delta_eps_ancestral__delta_tasA_ancestral':'baseline',
      'ancestral_eps__evolved_tasA':'lower_for_nearly_all',
      'evolved_eps__ancestral_tasA':'similar_or_higher_tendency',
      'evolved_eps__evolved_tasA':'heterogeneous_some_higher'}
    assert x['paired_cfu_effect_estimated'] is False
    assert x['reestimated_fitness_p_values'] is False
    assert x['verified_counterfactual_partner_swap'] is True

def test_six_parallel_lines_are_not_architecture_origins():
    x=analyse_context(load())
    assert x['mixed_delta_eps_extinct']=={'events':4,'n':6}
    assert x['monoculture_delta_eps_autonomy']=={'events':2,'n':6}
    assert x['monoculture_delta_tasA_autonomy']=={'events':6,'n':6}
    assert x['co_culture_delays_tasA_autonomy'] is True
    assert x['final_tasA_productivity_roughly_similar'] is True
    assert x['extinction_wilson95'] == pytest.approx(wilson95(4,6))
    assert .299 < x['extinction_wilson95'][0] < .301
    assert .903 < x['extinction_wilson95'][1] < .904
    assert x['timepoint_matched_genotype_CFU_replicates_obtained'] is False
    assert x['hysteresis_effect_identified'] is False

def test_fail_closed_to_false_history_and_missing_genetic_contexts():
    y=load()
    y['alleles']=[q for q in y['alleles'] if q['mutation']!='G183C']
    with pytest.raises(ValueError,match='allele'):
        analyse_context(y)
    y=load();y['partner_swaps'].append(dict(y['partner_swaps'][0]))
    with pytest.raises(ValueError,match='duplicate'):
        analyse_context(y)
    y=load();y['passaging']['mixed_delta_eps_extinct']['events']=6
    with pytest.raises(ValueError,match='count'):
        analyse_context(y)

def test_original_pdf_sha_is_reported_and_replayed_not_invented():
    x=load()
    assert x['source_pdf_sha256']['accepted']=='5cf82d20baf805432c7a0afda748f67689d71c5614bb0a90f6baf54bc040d6af'
    assert x['source_pdf_sha256']['supplement']=='d5a62567ab0818926f51892ac5750757d9f4e83c37d015664e1cfd4a4ec7e05c'
    assert wilson95(4,6) == pytest.approx([.2999933151383921,.9032285888942196])

def test_frozen_readout_reproduces_without_new_subjects():
    d=json.loads((ROOT/'empirical/trait_architecture_history/bacillus2018_conditional_history_readout.json').read_text())
    x=analyse_context(load())
    assert d['effects']==x
    assert d['original_data_level']=='AUTHOR_ACCEPTED_AND_NATURE_SUPPLEMENT_PDF_TEXT_NO_RAW_CFU'
    assert d['independent_evolution_programmes_n']==1
    assert d['meta_analysis_performed'] is False
