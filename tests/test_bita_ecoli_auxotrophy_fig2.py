"""PLOS 2016 n=8×2 evolved line dependence and source heatmap audits."""
import json
import math
from pathlib import Path
import pytest
from scripts.analyze_bita_ecoli_auxotrophy_fig2 import (
    DOI, ARTICLE_SHA, FIG2_SHA, TABLE1_SHA, TABLE2_SHA, TABLE3_SHA,
    SOURCE_EXPECTED, bin_detected, two_sided_fisher, wilson,
    newcombe_diff, source_image, audit_source_documents,
)
ROOT=Path(__file__).resolve().parents[1]
FROZEN=(ROOT/"empirical/trait_architecture_history/"
        "dsouza2016_aa_auxotrophy_fig2_readout.json")


def record():
    return json.loads(FROZEN.read_text(encoding="utf8"))


def test_original_fig2_zero_and_positive_colors_fail_closed():
    assert bin_detected((1,2,2)) is False
    assert bin_detected((240,145,146)) is True
    assert bin_detected((250,198,199)) is True
    with pytest.raises(ValueError,match="ambiguous"):
        bin_detected((255,255,255))
    with pytest.raises(ValueError,match="ambiguous"):
        bin_detected((120,120,115))


def test_exact_n8_vs_n8_endpoint_not_n1000_colonies():
    assert two_sided_fisher(6,8,0,8)==pytest.approx(0.006993006993006993)
    assert newcombe_diff(6,8,0,8)==pytest.approx(
        (0.2795390552402786,0.9285207872478909),abs=1e-12)
    assert wilson(6,8)==pytest.approx((.40927543031016883,.9285207872478909))
    assert wilson(0,8)==pytest.approx((0.,.3244075648838804))
    for a,n1,b,n2 in [(8,7,0,8),(6,8,-1,8),(3,0,1,8)]:
        with pytest.raises(ValueError):
            two_sided_fisher(a,n1,b,n2)


def test_all_96_source_figure_cells_are_one_assay_per_line_timepoint():
    d=record()
    assert d["doi"]==DOI
    assert d["source_fig2_sha256"]==FIG2_SHA
    assert d["source_validation"]["article_jats_sha256"]==ARTICLE_SHA
    assert d["source_validation"]["supplement_sha256"]=={
        "S1_table":TABLE1_SHA,"S2_table":TABLE2_SHA,"S3_table":TABLE3_SHA}
    cells=d["figure_cells"]
    assert len(cells)==96
    keys={(r["condition"],r["population_id"],r["generation"]) for r in cells}
    assert len(keys)==len(cells)
    assert all(r["derived_from"].endswith("not_raw_colony_count") for r in cells)
    assert all(type(r["detectable_auxotrophic_colony"]) is bool for r in cells)
    arms=d["sampled_arm_summaries"]
    assert arms["AA_present"]["positive_population_count_per_generation"]==[0,0,0,4,2,6]
    assert arms["AA_absent"]["positive_population_count_per_generation"]==[0,0,1,0,2,0]
    assert arms["AA_present"]["ever_detected_population_ids"]==[
        "R1","R2","R3","R4","R5","R6","R8"]
    assert arms["AA_absent"]["ever_detected_population_ids"]==["R2","R7","R8"]
    assert arms["AA_present"]["detected_at_final_generation_ids"]==[
        "R2","R3","R4","R5","R6","R8"]
    assert arms["AA_absent"]["detected_at_final_generation_ids"]==[]


def test_frozen_endpoint_quantitative_contract_and_no_overclaim():
    d=record()
    source=d["source_validation"]
    assert source["source_design"]["total_evolved_populations"]==16
    assert source["source_design"]["colonies_phenotyped_per_population_per_sampled_generation"]==1000
    p=d["primary_endpoint"]
    assert (p["aa_positive_populations"],p["aa_evolutionary_populations"],
            p["nonAA_positive_populations"],p["nonAA_evolutionary_populations"])==(6,8,0,8)
    assert p["two_sided_fisher_exact_p"]==pytest.approx(.006993006993006993)
    assert p["risk_difference"]==pytest.approx(.75)
    assert tuple(p["95pct_newcombe_interval"])==pytest.approx(
        (.2795390552402786,.9285207872478909))
    assert d["ever_detected_descriptive"]["AA_ever_population_count"]==7
    assert d["ever_detected_descriptive"]["nonAA_ever_population_count"]==3
    assert d["previous_timepoint_rows_are_repeated_measures"] is True
    assert d["genetic_auxotrophy_equivalent_to_reciprocal_division_of_labour"] is False
    assert d["published_raw_dryad_xlsx_verified"] is False
    assert d["meta_analysis_performed"] is False


def test_published_figure_and_article_source_discrepancies_remain_visible():
    s=record()["source_validation"]
    c=s["S1_selected_isolate_tally"]
    assert c["AA_1000_gen"]==60 and c["AA_1500_gen"]==256 and c["AA_2000_gen"]==157
    assert c["source_table_AA_sum"]==473
    assert c["original_results_text_says_AA"]==483
    assert c["unexplained_difference_in_original_sources"]==10
    assert c["nonAA_source_table_sum_and_results_text"]==37
    assert s["source_500_nonAA_label_in_prose"]=="R3"
    assert s["source_500_nonAA_label_in_figure"]=="R2"
    assert s["source_500_nonAA_discrepancy"].startswith("GENOTYPE_LABEL_CONFLICT")


def test_mutation_source_counts_are_not_genome_or_population_counts():
    s=record()["source_validation"]
    x=s["S2_function_mutation_annotated_occurrences"]
    assert (x["auxotroph_structural_gene"],x["auxotroph_regulatory_gene"],
            x["prototroph_structural_gene"],x["prototroph_regulatory_gene"])==(18,19,5,6)
    assert x["counts_are_mutation_annotations_not_independent_genetic_origins"] is True
    genomes=s["S3_selected_sequenced_genotype_IDs"]
    assert len(genomes["AA_auxotroph"])==6
    assert len(genomes["nonAA_auxotroph"])==2
    assert len(genomes["AA_or_nonAA_prototroph"])==6
    assert genomes["selected_genomes_not_all_16_population_histories"] is True
