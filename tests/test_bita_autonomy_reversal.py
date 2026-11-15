"""Source-bound autonomous-genotype reversal: experimental line is inferential unit."""
import hashlib
import json
import math
from pathlib import Path
import pytest
from scripts.analyze_bita_autonomy_reversal import (
    SOURCE_XML_SHA256, fisher_exact_2sided, fisher_freeman_halton, holm,
    wilson, newcombe_difference, analyze_primary_jats,
)

SOURCE=Path(__file__).resolve().parents[1]/"empirical/trait_architecture_history/chen2024_autonomy_reversal_readout.json"


def test_three_arm_exact_source_12_per_regime():
    assert fisher_freeman_halton([12,12,12],[0,0,5])==pytest.approx(.0063025210084033615)
    assert fisher_freeman_halton([10,12,12],[0,0,5])==pytest.approx(.006598240469208211)
    assert fisher_exact_2sided(5,12,0,12)==pytest.approx(.03726708074534161)
    assert fisher_exact_2sided(5,12,0,10)==pytest.approx(.03964456596035544)
    assert holm([.03726708074534161]*2)==pytest.approx([.07453416149068322]*2)


def test_zero_reference_confidence_interval_without_fabricated_pseudocount():
    assert wilson(5,12)==pytest.approx((.1932603136587565,.6804886874504502))
    assert newcombe_difference(5,12,0,12)==pytest.approx((.08694899679135193,.6804886874504502))
    assert newcombe_difference(5,12,0,10)==pytest.approx((.06038748742091071,.6804886874504502))
    assert newcombe_difference(6,12,3,12)==pytest.approx((-.12459285070028103,.5442163962859665))


def test_invalid_population_grains_fail_closed():
    with pytest.raises(ValueError): fisher_exact_2sided(4,3,0,12)
    with pytest.raises(ValueError): fisher_freeman_halton([12,12,12],[0,0,13])
    with pytest.raises(ValueError): wilson(0,0)
    with pytest.raises(ValueError): holm([float("nan")])


def test_frozen_source_counts_and_dependent_clone_units():
    d=json.loads(SOURCE.read_text(encoding="utf8"))
    assert d["source_xml_sha256"]==SOURCE_XML_SHA256
    assert d["source_doi"]=="10.1073/pnas.2317182121"
    assert d["source_grain"]=="independent_experimentally_evolved_population"
    assert d["three_regime_success_counts"]==[0,0,5]
    assert d["three_regime_started_counts"]==[12,12,12]
    assert d["constant_mutualism_extinct_after_50_gen"]==2
    assert d["core_exact_omnibus_p_two_sided"]==pytest.approx(.0063025210084033615)
    assert d["dropout_sensitivity_omnibus_p"]==pytest.approx(.006598240469208211)
    assert d["two_separate_pairwise_holm_adjusted_p"]==pytest.approx([.07453416149068322]*2)
    g=d["fluctuating_genetic_origins"]
    assert (g["independent_lineages"],g["degrader_barcode_lineages"],
            g["detoxifier_barcode_lineages"],g["clonal_isolates_from_five_evolved_populations"])==(5,3,2,20)
    assert [(x["autonomy_lineages"],x["started_lineages"]) for x in d["readdition_experiments"]]==[(3,12),(6,12)]
    assert d["readdition_high_density_vs_low_density_RD"]["95pct_interval"]==pytest.approx(
        (-.12459285070028103,.5442163962859665))
    assert d["two_directions_tested"]==["specialists_to_autonomy"]
    assert d["forward_specialization_origin_identified"] is False
    assert d["hysteresis_identified"] is False
    assert d["original_per_line_growth_trajectories_acquired"] is False
    assert d["author_simulations_independent_evidence"] is False
    assert d["mixed_control_regimes_pooled_as_one_meta_study"] is False


def test_model_simulation_is_not_treated_as_evolutionary_replication():
    d=json.loads(SOURCE.read_text(encoding="utf8"))
    m=d["model_only"]
    assert m["parameter_sets"]==17501
    assert m["parameter_set_fluct_only"]==2269
    assert m["parameter_set_mut_only"]==1003
    assert m["parameter_set_both"]==10633
    assert m["parameter_set_neither"]==3596
    assert m["default_fluctuating_sim_successes"]==59
    assert m["default_mutualism_sim_successes"]==16
    assert m["modelled_parameter_sets_not_independent_experimental_replicates"] is True
