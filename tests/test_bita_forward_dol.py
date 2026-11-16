"""Original published 2016/2020 forward differentiation, nested-unit guardrails."""
import json
import math
from pathlib import Path
import pytest
from scripts.analyze_bita_forward_dol import F_to_r2, audit_two_origins, parse_original_jats


def test_F_statistics_are_model_fit_not_effect_on_wt_group():
    for f,ndf,ddf,r2 in [
        (107.7,2,7,.969),
        (37.95,2,7,.916),
        (26.58,1,29,.478),
        (12.32,1,7,.638),
        (37.97,1,7,.844)]:
        assert F_to_r2(f,ndf,ddf)==pytest.approx(r2,abs=.0006)
    with pytest.raises(ValueError,match="invalid"):
        F_to_r2(12.3,0,10)


def test_source_registration_never_promotes_mutants_to_origin_frequency():
    k={
      "doi":"10.1038/ncomms10508",
      "dry_mutants_sequenced_from_separate_fans":20,
      "figure_1_single_vs_mixed_cfu_anova_p":.000957,
      "figure_4_lubrication_control_cfu_anova_p":.000167,
      "figure_2_colonies_per_starting_frequency":3,
    }
    z={
      "doi":"10.1126/sciadv.aay5781",
      "selected_mutant_strains":30,
      "selected_mutants_with_reduced_spore_production":28,
      "fig4_antibiotic_vs_mutant_fraction_F":107.7,
      "fig4_spore_fitness_vs_mutant_fraction_F":37.95,
    }
    r=audit_two_origins(k,z)
    assert r["independent_research_programmes"]==2
    assert r["kim_independent_spreading_fan_mutants_examined"]==20
    assert r["kim_origin_probability_estimated"] is False
    assert r["zhang_selected_mutant_strains"]==30
    assert r["zhang_parental_mutant_spore_cost_fraction_descriptive"]==pytest.approx(28/30)
    assert r["zhang_independent_evolutionary_origins_estimated"] is False
    assert r["pooled_fitness_effect"] is None
    assert r["forward_trait_axis_origin_identified"] is False
    assert r["category_associations_are_history_not_randomized_independent_effects"] is True


def test_wrong_source_ids_or_effect_measures_fail():
    k={"doi":"10.1038/ncomms10508","dry_mutants_sequenced_from_separate_fans":20,
       "figure_1_single_vs_mixed_cfu_anova_p":.000957,
       "figure_4_lubrication_control_cfu_anova_p":.000167,
       "figure_2_colonies_per_starting_frequency":3}
    z={"doi":"10.1126/sciadv.aay5781","selected_mutant_strains":30,
       "selected_mutants_with_reduced_spore_production":28,
       "fig4_antibiotic_vs_mutant_fraction_F":107.7,
       "fig4_spore_fitness_vs_mutant_fraction_F":37.95}
    with pytest.raises(ValueError):
        audit_two_origins({**k,"doi":"wrong"},z)
    with pytest.raises(ValueError):
        audit_two_origins(k,{**z,"selected_mutants_with_reduced_spore_production":31})
    with pytest.raises(ValueError):
        audit_two_origins(k,{**z,"fig4_antibiotic_vs_mutant_fraction_F":109.3})


def test_frozen_readout_contains_source_checksums_and_correct_denominators():
    root=Path(__file__).resolve().parents[1]
    result=json.loads((root/"empirical/trait_architecture_history/kim_zhang_forward_dol_readout.json").read_text("utf8"))
    assert result["sources"]["kim"]["sha256"]=="a876e838044cb44ab28c47a1f9e243df3172c15650ad52f56be1e1a1d5c8ab68"
    assert result["sources"]["zhang"]["sha256"]=="bfe5787f48f0c2dde277d9d6db6387180472b55c182c5d45738309e45cc0d092"
    summary=result["comparison"]
    assert summary["independent_research_programmes"]==2
    assert summary["kim_independent_spreading_fan_mutants_examined"]==20
    assert summary["zhang_selected_mutant_strains"]==30
    assert summary["zhang_parental_mutant_spore_cost_fraction_descriptive"]==pytest.approx(28/30)
    assert summary["pooled_fitness_effect"] is None
    assert summary["forward_trait_axis_origin_identified"] is False
    assert result["source_statement_excludes_genetic_ancestry_generalism"] is True
    assert result["experimental_raw_data_obtained"] is False
    assert result["publication_count_not_metanalysis_n"] is True


def test_five_programme_index_keeps_forward_engineering_and_reverse_separate():
    import csv
    root=Path(__file__).resolve().parents[1]
    path=root/"empirical/trait_architecture_history/bita_forward_group_benefit_evidence_20261116.csv"
    with path.open(newline="",encoding="utf8") as stream:
        records=list(csv.DictReader(stream))
    assert len(records)==5
    families=[r["programme_id"] for r in records]
    assert len(families)==len(set(families))
    assert all(r["effect_pooled_cross_study"]=="no" for r in records)
    by_id={r["programme_id"]:r for r in records}
    assert "one source M colony per selected dry spreading fan" in by_id["Kim2016_Pfluorescens"]["independent_biological_unit"]
    assert "source M" in by_id["Kim2016_Pfluorescens"]["reason_not_poolable"]
    assert "Somatic" in by_id["Zhang2020_Scoelicolor"]["architecture_origin"]
    assert "no unbiased" in by_id["Zhang2020_Scoelicolor"]["independent_evolutionary_origin_count_identified"]
    assert ";" in by_id["Dragos2018_Bsubtilis"]["source_doi"]  # same research programme, two papers
    assert "reverse" in by_id["Chen2024_Pstutzeri"]["architecture_origin"]
    assert "engineered" in by_id["Chen2024_Pstutzeri"]["architecture_origin"].lower()
    assert "Dryad original xlsx HTTP 401/403" in by_id["Mridha2022_Paeruginosa"]["original_raw_replicate_observations_acquired"]
