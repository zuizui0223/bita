"""Original Fig5 area->radius / biomass-weighting with replay-population grain."""
import math
import pytest

from scripts.analyze_bita_pineau2024_f5_replay import (
    LINES, SHEET_DAY_LABELS, AUTHOR_F5_PLOT_DAYS,
    slope, weighted_phenotype, exact_population_label_permutation,
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
    assert q["extreme_partition_count"]==2
    assert q["two_sided_reference_fraction"]==pytest.approx(2/35)
    assert q["reference_only_not_a_randomized_label_test"]
    with pytest.raises(ValueError,match="3 Large"):
        exact_population_label_permutation([-1,-2],[1,2,3,4])
