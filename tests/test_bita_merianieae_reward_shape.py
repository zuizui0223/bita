"""Source-linked 139-tip Merianieae trait coding and denominator safeguards."""
import csv
import io
import pytest
from scripts.analyze_bita_merianieae_reward_shape import (
    summarize_records, source_category, reward_group,
)

def record(species, reward, shape, tip=None):
    return {'species':species,'x':tip or 'Merianieae_'+species.replace(' ','_'),
            'confirmed.reward.type':reward,'stamen.shape.dimorphism':shape,
            'estimated_pollinator':'bee'}

def test_reject_ambiguous_reward_and_shape_values():
    assert source_category('0')=='isomorphic_or_no_shape_difference'
    assert source_category('1')=='shape_difference_code_1'
    assert source_category('2')=='shape_difference_code_2'
    assert reward_group('0')=='pollen'
    assert reward_group('1')=='nectar'
    assert reward_group('2')=='food_body'
    assert reward_group('NA') is None
    with pytest.raises(ValueError,match="reward"):
        reward_group('3')
    with pytest.raises(ValueError,match="shape"):
        source_category('3')

def test_source_missingness_is_not_negative_and_tree_join_is_explicit():
    rows=[record('A a','0','0'),
          record('A b','0','1'),
          record('A c','1','0'),
          record('A d','2','1'),
          record('B x','NA','2'),
          record('B y','0','2')]
    tips={r['x'] for r in rows[:-1]}
    x=summarize_records(rows,tips)
    assert x['n_source_rows']==6
    assert x['n_phylogeny_joined']==5
    assert x['n_reward_known_in_tree']==4
    assert x['n_reward_missing_in_tree']==1
    assert x['known_reward_counts']=={'pollen':2,'nectar':1,'food_body':1}
    assert x['known_reward_shape_differentiated_counts']=={'pollen':1,'nectar':0,'food_body':1}
    assert x['all_nonpollen_vs_pollen']['nonpollen_positive']==1
    assert x['all_nonpollen_vs_pollen']['pollen_positive']==1

def test_known_genus_contrast_is_diagnostic_not_phylogenetic_significance():
    rows=[record('Meriania a','0','0'),
          record('Meriania b','0','2'),
          record('Meriania c','1','0'),
          record('Axinaea x','2','1'),
          record('Axinaea y','2','1')]
    x=summarize_records(rows,{r['x'] for r in rows})
    assert x['genus_reward_shape']['Meriania']['pollen']['positive']==1
    assert x['genus_reward_shape']['Meriania']['nectar']['positive']==0
    assert x['genus_reward_shape']['Axinaea']['food_body']['positive']==2
    assert x['phylogenetic_transition_events_inferred'] is False
    assert x['pooled_meta_analysis_performed'] is False

def test_duplicate_taxa_and_unmatched_traits_fail_closed():
    x=record('Meriania a','0','1')
    with pytest.raises(ValueError,match="duplicate"):
        summarize_records([x,x],{x['x']})
    with pytest.raises(ValueError,match="no matched"):
        summarize_records([x],{'bogus'})
