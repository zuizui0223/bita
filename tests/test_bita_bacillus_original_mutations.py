"""Source-unit audit for Nature follow-up Bacillus mutants (one programme).

No six-independent-origins claims from sister isolates, no phenotype inferred
from raw mutation X calls, no unobserved transfers called wild type.
"""
import pytest
from pathlib import Path
import json
from scripts.analyze_bita_bacillus_original_mutations import analyze_source_xlsx, F_TO_R2


def test_f_to_r2_from_original_bacillus_figure_captions():
    x=F_TO_R2(54.9,3,68)
    assert x["r2_raw"]==pytest.approx(0.7077782549,abs=5e-6)
    assert x["r2_adjusted"]==pytest.approx(.695,abs=.0005)
    x=F_TO_R2(94.7,3,46)
    assert x["r2_raw"]==pytest.approx(.86065,abs=.0005)
    assert x["r2_adjusted"]==pytest.approx(.852,abs=.0005)


def test_source_archive_sha_missing_fails_closed():
    with pytest.raises(ValueError,match="sha256"):
        analyze_source_xlsx(b"not original source")


def test_original_source_phenotypes_are_not_inferred_from_mutations():
    path=Path(__file__).resolve().parents[1]/"empirical/trait_architecture_history/bacillus2018_evolved_mutation_summary.json"
    s=json.loads(path.read_text(encoding="utf8"))
    assert s["source_doi"]=="10.1038/s41564-018-0263-y"
    assert s["original_supplement_sha256"]=="ec916667dbd7a288246737979e3b0d2e4336acfcc8dd98d641339973361d9a43"
    assert s["evolved_eps_deficient_tasa_cysteine_alleles"]==[
        {"gene":"tasA","position":2552702,"amino_acid":"Tyr124Cys",
         "clonal_lineage":"e4","clone_ids":["e4A","e4B","e4C"]},
        {"gene":"tasA","position":2552526,"amino_acid":"Gly183Cys",
         "clonal_lineage":"e6","clone_ids":["e6A","e6B","e6C"]},
    ]
    assert s["genetically_independent_tasa_cys_lineages_lower_bound"]==2
    assert s["distinct_mutant_clones_not_independent_lineages"]==6
    assert s["mixed_population_transfer_records"]==18
    assert s["mixed_population_groups"]==6
    assert s["first_observed_transfer"]==5
    assert s["last_observed_transfer"]==24
    assert s["mixed_mutations_newly_detected_at_24_vs_5"]==5
    assert s["mixed_mutations_not_detected_at_24_but_detected_at_5"]==3
    assert s["n_ambiguous_or_non_X_cells"]==1
    assert s["phenotypic_productivity_effect_from_supplement_estimated"] is False
    assert s["evolutionary_origin_of_division_identified"] is False


def test_cross_lineage_backgrounds_not_convergent_mutations():
    path=Path(__file__).resolve().parents[1]/"empirical/trait_architecture_history/bacillus2018_evolved_mutation_summary.json"
    r=json.loads(path.read_text(encoding="utf8"))
    assert sorted(x["gene"] for x in r["mixed_mutations_present_in_all_9_within_genotype"]["delta_eps"])==["ganA","hxlA"]
    assert sorted(x["gene"] for x in r["mixed_mutations_present_in_all_9_within_genotype"]["delta_tasA"])==["(unannotated)","epsK"]
    assert r["identical_baseline_markers_coded_as_independent_recurrent_mutations"] is False
    assert r["mixed_populations_collapsed_from_genotypes"] is False
