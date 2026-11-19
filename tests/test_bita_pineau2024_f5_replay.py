"""Original Fig5 area->radius / biomass-weighting with replay-population grain."""
import math
import pytest

from scripts.analyze_bita_pineau2024_f5_replay import (
    LINES, SHEET_DAY_LABELS, AUTHOR_F5_PLOT_DAYS,
    slope, weighted_phenotype, exact_population_label_permutation,
    audit_exact_source_column_duplicates,
)


def test_same_7_independent_author_replay_lines_as_frozen_original_R_script():
    assert [(n,t) for n,t,_ in LINES] == [
        ("l1","large"),("l3","large"),("l4","large"),
        ("s1","small"),("s2","small"),("s3","small"),("s4","small")
    ]
    assert AUTHOR_F5_PLOT_DAYS==(0,5,10,15,20,40)
    assert SHEET_DAY_LABELS==("Day1","Day5","Day10","Day15","Day20","Day40")


def test_area_to_radius_weighted_estimator_not_cluster_count_weighted():
    areas=[math.pi*2*2,math.pi*4*4]
    result=weighted_phenotype(areas)
    assert result["original_cluster_objects"]==2
    assert result["mean_radius_um_cluster_count_weighted"]==pytest.approx(3)
    # radius 2 and 4 weighted by volume proportional to r^3
    assert result["mean_radius_um_biomass_weighted_direct"]==pytest.approx(
        (2*2**3 + 4*4**3)/(2**3 + 4**3))
    assert result["mean_radius_um_biomass_weighted_direct"] > 3


def test_explicit_outlier_filter_is_sensitivity_not_silent_main_exclusion():
    areas=[math.pi*25*25,math.pi*120*120]
    full=weighted_phenotype(areas)
    quality=weighted_phenotype(areas,trim_radius_above=100)
    assert full["original_cluster_objects"]==2
    assert full["removed_after_explicit_radius_QC"]==0
    assert quality["removed_after_explicit_radius_QC"]==1
    assert quality["mean_radius_um_biomass_weighted_direct"]==pytest.approx(25)
    assert full["mean_radius_um_biomass_weighted_direct"]>100
    with pytest.raises(ValueError,match="removed all"):
        weighted_phenotype([math.pi*120**2],trim_radius_above=100)


def test_population_slope_not_timepoint_replication():
    assert slope((0,1,2),[2,4,6])==pytest.approx(2)
    assert slope((0,10,20),[10,8,6])==pytest.approx(-.2)
    with pytest.raises(ValueError):
        slope((1,1,1),[1,2,3])


def test_exact_seven_population_label_enumeration_not_cluster_permutation():
    q=exact_population_label_permutation([-3,-2,-1],[1,2,3,4])
    assert q["seven_line_source_label_partition_count"]==35
    assert q["extreme_partition_count"]==1
    assert q["two_sided_reference_fraction"]==pytest.approx(1/35)
    assert q["reference_only_not_a_randomized_label_test"]
    with pytest.raises(ValueError,match="3 Large"):
        exact_population_label_permutation([-1,-2],[1,2,3,4])


def test_exact_original_numeric_vector_duplication_is_not_a_new_replay_line():
    rows=[
        {"excel_row":1,"cells":{0:"Figure 5A"},"formula_count":0},
        {"excel_row":2,"cells":{},"formula_count":0},
        {"excel_row":3,"cells":{},"formula_count":0},
    ]
    for i in range(4,9):
        values={j:1000*j+i for j in range(42)}
        values[23]=values[5]  # large l1 Day40 duplicated as small s1 Day40
        rows.append({"excel_row":i,"cells":values,"formula_count":0})
    q=audit_exact_source_column_duplicates(rows)
    assert q["cross_population_duplicate_pairs"]==1
    assert q["cross_population_suspect_excel_columns_1indexed"]==[6,24]
    assert q["exact_duplicate_source_column_pairs"]==[{
        "left_population":"l1",
        "left_original_day":"Day40",
        "left_excel_column_1indexed":6,
        "right_population":"s1",
        "right_original_day":"Day40",
        "right_excel_column_1indexed":24,
        "identical_excel_row_and_numeric_value_pairs":5,
        "cross_independent_evolution_population":True,
    }]
    assert q["no_independent_endpoints_claim_for_duplicated_columns"]


def test_frozen_original_doubled_day40_is_quarantined_in_both_source_groups():
    import json
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    path=root/"empirical/trait_architecture_history/pineau2024_f5_original_replay_readout.json"
    d=json.loads(path.read_text())
    audit=d["original_Fig5A_source_duplicate_audit"]
    assert audit["cross_population_duplicate_pairs"]==1
    assert audit["cross_population_suspect_excel_columns_1indexed"]==[6,24]
    assert audit["exact_duplicate_source_column_pairs"][0][
        "identical_excel_row_and_numeric_value_pairs"]==164
    assert d["all_seven_original_day40_endpoints_do_not_pass_independent_source_QA"]
    valid=d["primary_quarantined_independent_day40_endpoints"]
    assert valid["small"]["independent_original_population_day40_endpoints_after_QA"]==3
    assert valid["small"]["population_IDs"]==["s2","s3","s4"]
    assert valid["large"]["independent_original_population_day40_endpoints_after_QA"]==2
    assert valid["large"]["population_IDs"]==["l3","l4"]
    assert valid["small"]["mean_per_valid_line_day40_minus_initial_um"]==pytest.approx(9.012177598717132)
    assert valid["large"]["mean_per_valid_line_day40_minus_initial_um"]==pytest.approx(-5.975551045357875)
    assert valid["small"]["each_source_valid_line_changed_in_predeclared_direction"]
    assert valid["large"]["each_source_valid_line_changed_in_predeclared_direction"]
    assert {p["author_population_ID"] for p in
            d["quarantined_duplicated_day40_populations"]}=={"l1","s1"}
    assert d["between_founder_phenotypes_exploratory_label_sensitivity"][
        "not_eligible_as_primary_source_QA_inference"]
    assert d["interpretation_ceiling"]["both_duplicated_day40_endpoints_quarantined_not_arbitrarily_assigned"]
