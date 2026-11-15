"""Source-audited conditional genetic effects and partner preadaptation in Bacillus.

Published 2018 Nature Microbiology experimental manipulations are RECOVERED
from original manuscript and supplementary PDFs. No invented raw CFU data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist

SHA={
    'accepted':'5cf82d20baf805432c7a0afda748f67689d71c5614bb0a90f6baf54bc040d6af',
    'supplement':'d5a62567ab0818926f51892ac5750757d9f4e83c37d015664e1cfd4a4ec7e05c',
}
ALLELES={
    'Y124C':('rescue_vs_ancestral_TasA','no_demonstrated_productivity_gain','e4','pellicle_abolished'),
    'G183C':('rescue_vs_ancestral_TasA','negative_productivity_vs_wt_reported','e6','pellicle_maintained'),
}
PAIRS={
    'delta_eps_ancestral__delta_tasA_ancestral':'baseline',
    'ancestral_eps__evolved_tasA':'lower_for_nearly_all',
    'evolved_eps__ancestral_tasA':'similar_or_higher_tendency',
    'evolved_eps__evolved_tasA':'heterogeneous_some_higher',
}

def wilson95(k: int,n: int)->list[float]:
    if type(k) is not int or type(n) is not int or n<1 or not 0<=k<=n:
        raise ValueError('invalid count')
    z=NormalDist().inv_cdf(.975);p=k/n
    den=1+z*z/n
    centre=(p+z*z/(2*n))/den
    half=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/den
    return [centre-half,centre+half]

def analyse_context(d: dict)->dict:
    if d.get('paper_doi')!='10.1038/s41564-018-0263-y' or d.get('source_pdf_sha256')!=SHA:
        raise ValueError('wrong source DOI or PDF fingerprint')
    mutations={}
    for item in d['alleles']:
        name=item['mutation']
        if name in mutations:raise ValueError('duplicate allele')
        value=(item['eps_absent'],item['eps_present'],item['lineage'],item['bslA_knockout'])
        if name not in ALLELES or ALLELES[name]!=value or item['eps_present_wetting']!='hydrophobicity_lost':
            raise ValueError('unsupported original allele context')
        if not item.get('source_location'):
            raise ValueError('unlocated original allele evidence')
        mutations[name]=item
    if set(mutations)!=set(ALLELES):
        raise ValueError('missing allele background')
    pairs={}
    for item in d['partner_swaps']:
        if item['state'] in pairs:raise ValueError('duplicate partner-swap condition')
        if item['state'] not in PAIRS or PAIRS[item['state']]!=item['direction']:
            raise ValueError('unsupported source partner swap')
        pairs[item['state']]=item['direction']
    if pairs!=PAIRS:raise ValueError('missing source partner swap')
    endpoint=d['passaging']
    expected=[('mixed_delta_eps_extinct',4),('monoculture_delta_eps_autonomy',2),('monoculture_delta_tasA_autonomy',6)]
    for key,events in expected:
        if endpoint[key]!={'events':events,'n':6}:
            raise ValueError('original six-line count mismatch: '+key)
    if d.get('independent_evolved_tasa_cys_lineages')!=2 or d.get('isolates_in_two_e4_e6_lineages')!=6:
        raise ValueError('six descendant isolates are NOT independent evolved lineages')
    history=d['history']
    if (history['delta_tasA_coculture_vs_monoculture']!='co_culture_delays_recovery'
        or history['delta_tasA_final_productivity']!='roughly_similar'
        or history['supplementary_figure11_arms']!=3
        or history['independent_lines_per_arm']!=6
        or history['joint_original_mutation_productivity_pair_rows_available'] is not False):
        raise ValueError('invalid history observation or false raw phenotypes')
    if (d['extra_control']['engineered_eps_overproduction_in_delta_tasA']
         !='increased_mix_productivity_and_improved_delta_eps_partner'):
        raise ValueError('missing source perturbation falsifier')
    if d['pairwise_cfu_values_available'] or d['claimed_k_u_empirical_estimate']:
        raise ValueError('quantitative fitness/K(u) claim beyond source')
    return {
        'two_source_tasa_alleles':['Y124C','G183C'],
        'changed_conditional_benefit_n':2,
        'strict_productivity_sign_reversal':['G183C'],
        'eps_present_no_demonstrated_gain':['Y124C'],
        'eps_present_both_mutants_reduce_water_repellency':True,
        'bslA_deletion_results':{
            'e4A_Y124C':'pellicle_abolished',
            'e6A_G183C':'pellicle_maintained'},
        'bslA_universally_required':False,
        'independent_evolved_tasa_cys_lineages':2,
        'descendant_isolates_not_independent_origins':6,
        'partner_swaps':pairs,
        'verified_counterfactual_partner_swap':True,
        'paired_cfu_effect_estimated':False,
        'reestimated_fitness_p_values':False,
        'mixed_delta_eps_extinct':endpoint['mixed_delta_eps_extinct'],
        'monoculture_delta_eps_autonomy':endpoint['monoculture_delta_eps_autonomy'],
        'monoculture_delta_tasA_autonomy':endpoint['monoculture_delta_tasA_autonomy'],
        'extinction_wilson95':wilson95(4,6),
        'co_culture_delays_tasA_autonomy':True,
        'final_tasA_productivity_roughly_similar':True,
        'same_condition_different_preadaptation_records':True,
        'separate_eps_overproduction_control':d['extra_control'],
        'timepoint_matched_genotype_CFU_replicates_obtained':False,
        'hysteresis_effect_identified':False,
        'historical_ancestral_architecture_origin_identified':False,
        'scientific_boundaries':(
            'G183C gives EPS-conditional productivity gain versus reported decrease. '
            'Y124C EPS-present productivity has NO reported gain; it is not proven negative. '
            'Both lose water repellency when EPS is present. e4A/e6A show different '
            'BslA dependence, but BslA loss involves strain backgrounds as well. '
            'Evolved partner crossover differences describe experimentally sampled '
            'relative growth tendencies, not per-pair numeric fitness effects. '
            'In six coevolved cultures Δeps extinction occurred in four; distinct '
            'monoculture endpoints do not estimate adaptive-origin prevalence. '
            'No original matched genotype CFU time series, K(u), or hysteresis loop.'
        )
    }

def verify_pdf_sources(accepted_bytes: bytes,supplement_bytes: bytes)->dict:
    # The institutional portal can alter its cover/metadata without changing
    # the scientific manuscript. Validate *all scientific pages* by a second,
    # exact normalized-text digest instead of accepting a new raw PDF blindly.
    if hashlib.sha256(supplement_bytes).hexdigest()!=SHA['supplement']:
        raise ValueError('supplement original PDF sha256 mismatch')
    import fitz
    with fitz.open(stream=accepted_bytes,filetype='pdf') as a:
        text_a=' '.join(' '.join(page.get_text().split()) for page in a)
        na=len(a)
        body=''.join(' '.join(page.get_text().split()) for page in list(a)[1:])
        body_sha=hashlib.sha256(body.encode('utf8')).hexdigest()
        expected_body='d634c41c16509c699e845d5d4e4a958b1e152f16adb4084db43e4e7d23c58baf'
        if body_sha!=expected_body:
            raise ValueError('accepted manuscript scientific-text SHA256 differs from frozen original')
    accepted_raw=hashlib.sha256(accepted_bytes).hexdigest()
    with fitz.open(stream=supplement_bytes,filetype='pdf') as s:
        text_s=' '.join(' '.join(page.get_text().split()) for page in s)
        ns=len(s)
    if (na,ns)!=(30,23):raise ValueError('original paper pagination changed')
    checks={
      'accepted_mutant_reconstitution':(text_a,['Y124C','G183C','Both substitutions completely restored']),
      'accepted_four_of_six_extinction':(text_a,['four out of six','two out of six']),
      'accepted_evolved_partner_swap':(text_a,['Nearly all','lower productivity','Fig. 6']),
      'accepted_history_delay':(text_a,['monoculture-initiated','delayed']),
      'supp_eps_context':(text_s,['Supplementary Results 1','did not have positive effects','effects on fitness even']),
      'supp_bsla_dependence':(text_s,['completely abolished pellicle formation','performance of e6A was unaltered']),
      'supp_history_assay':(text_s,['Supplementary Fig. 11','six parallel']),
    }
    out={'source_pages':{'accepted':na,'supplement':ns},'verified_pdf_digests':SHA,
         'accepted_scientific_pages_normalized_sha256':'d634c41c16509c699e845d5d4e4a958b1e152f16adb4084db43e4e7d23c58baf'}
    for name,(text,terms) in checks.items():
        if not all(term.lower() in text.lower() for term in terms):
            raise ValueError('original source has no evidence for '+name)
        out[name]=True
    return out

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ledger',type=Path,required=True)
    p.add_argument('--accepted',type=Path,required=True)
    p.add_argument('--supplement',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    source=json.loads(a.ledger.read_text(encoding='utf8'))
    result={
        'paper_doi':source['paper_doi'],
        'original_data_level':'AUTHOR_ACCEPTED_AND_NATURE_SUPPLEMENT_PDF_TEXT_NO_RAW_CFU',
        'independent_evolution_programmes_n':1,
        'meta_analysis_performed':False,
        'effects':analyse_context(source),
        'original_source_validation':verify_pdf_sources(a.accepted.read_bytes(),a.supplement.read_bytes()),
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf8')
    print('BITA_CONTEXT_JSON:'+json.dumps({
      'alleles':result['effects']['two_source_tasa_alleles'],
      'conditional_gains':result['effects']['changed_conditional_benefit_n'],
      'strict_reversal':result['effects']['strict_productivity_sign_reversal'],
      'partner_matrix':result['effects']['partner_swaps'],
      'extinction':result['effects']['mixed_delta_eps_extinct'],
      'pdf_sha256':result['original_source_validation']['verified_pdf_digests'],
    },ensure_ascii=False,separators=(',',':')))

if __name__=='__main__': main()
