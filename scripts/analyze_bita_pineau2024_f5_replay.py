"""Pineau 2024 Figure 5 replay: original measured cluster areas, 7 lineages.

Source SHA and workbook layout are verified using the existing Fig5 source
audit. The phenotype-level cluster measurements are NESTED in the 3 Large
and 4 Small independently replay-evolved monoculture populations.

Main estimator: direct volume-weighted cluster radius by line and time,
using the author's area-to-radius and radius-to-volume transformations.
This is mathematically close to, but not identical to, the source R script's
1,500-bin biomass-weighted midpoint approximation.

R plot's day vector 0,5,10,15,20,40 versus XLSX Day1,... is kept as an
explicit time-origin discrepancy, not silently repaired.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import statistics
import zipfile
import io
from pathlib import Path

from scripts.audit_bita_pineau2024_f2_workbook import (
    verify_author_bytes, get_workbook_sheets, get_shared_strings, read_cells,
)
from scripts.audit_bita_pineau2024_f5_source import (
    validate_author_scripts,
)

LINES = (
    ("l1", "large", "Line1_large_area"),
    ("l3", "large", "Line3_large_area"),
    ("l4", "large", "Line4_large_area"),
    ("s1", "small", "Line1_small_area"),
    ("s2", "small", "Line2_small_area"),
    ("s3", "small", "Line3_small_area"),
    ("s4", "small", "Line4_small_area"),
)
SHEET_DAY_LABELS=("Day1","Day5","Day10","Day15","Day20","Day40")
AUTHOR_F5_PLOT_DAYS=(0,5,10,15,20,40)
WORKBOOK_PATH="Fig5A"


def slope(xs:tuple[int,...],ys:list[float])->float:
    xm=statistics.mean(xs)
    ym=statistics.mean(ys)
    den=sum((x-xm)**2 for x in xs)
    if den <= 0:
        raise ValueError("time grid has no variation")
    return sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/den


def exact_population_label_permutation(large:list[float],small:list[float])->dict:
    """All C(7,3)=35 units as an *exploratory label sensitivity*, not an
    experimental randomization test (lineage types were not randomized)."""
    if len(large)!=3 or len(small)!=4:
        raise ValueError("Fig5 source has only 3 Large + 4 Small replay lines")
    all_scores=large+small
    obs=statistics.mean(small)-statistics.mean(large)
    n=0
    extreme=0
    for ids in itertools.combinations(range(7),3):
        n+=1
        big=[all_scores[i] for i in ids]
        little=[all_scores[i] for i in range(7) if i not in ids]
        dd=statistics.mean(little)-statistics.mean(big)
        if abs(dd)>=abs(obs)-1e-12:
            extreme+=1
    if n!=35: raise ValueError("wrong 7-line finite enumeration")
    return {
        "observed_small_minus_large_mean_slope":obs,
        "seven_line_source_label_partition_count":n,
        "extreme_partition_count":extreme,
        "two_sided_reference_fraction":extreme/n,
        "reference_only_not_a_randomized_label_test":True,
        "no_cluster_or_time_cell_pseudoreplication":True,
    }


def weighted_phenotype(area:list[float],trim_radius_above:float|None=None)->dict:
    if not area or any(not 0<r and math.isfinite(r) for r in area):
        raise ValueError("source area measurements must be finite and positive")
    radii=[math.sqrt(x/math.pi) for x in area]
    if trim_radius_above is not None:
        subset=[x for x in radii if x<=trim_radius_above]
    else:
        subset=radii
    if not subset:
        raise ValueError("source QC removed all clusters")
    weights=[(4/3)*math.pi*r*r*r for r in subset]
    mean=sum(r*w for r,w in zip(subset,weights))/sum(weights)
    return {
        "original_cluster_objects":len(area),
        "retained_after_explicit_radius_QC":len(subset),
        "removed_after_explicit_radius_QC":len(area)-len(subset),
        "mean_radius_um_cluster_count_weighted":statistics.mean(subset),
        "mean_radius_um_biomass_weighted_direct":mean,
    }


def build_original(source_xlsx:bytes,load_r:bytes,plot_r:bytes)->dict:
    origin=verify_author_bytes(source_xlsx)
    source=validate_author_scripts(load_r,plot_r)
    with zipfile.ZipFile(io.BytesIO(source_xlsx)) as z:
        names=get_workbook_sheets(z)
        if WORKBOOK_PATH not in names:
            raise ValueError("original Fig5A source worksheet missing")
        rows=read_cells(z,names[WORKBOOK_PATH],get_shared_strings(z))
    if len(rows)<8 or rows[0]["excel_row"]!=1 or rows[1]["excel_row"]!=2 or rows[2]["excel_row"]!=3:
        raise ValueError("original Fig5A title/line/time header has changed")
    if "Size distributions" not in str(rows[0]["cells"].get(0,"")):
        raise ValueError("original Fig5A sheet is not the source size panel")
    src_names=[rows[1]["cells"].get(i*6) for i in range(7)]
    if src_names!=[r[2] for r in LINES]:
        raise ValueError("original 7 Fig5A source lineage headers changed")
    src_days=[rows[2]["cells"].get(i) for i in range(42)]
    if src_days!=list(SHEET_DAY_LABELS)*7:
        raise ValueError("source Fig5A day labels do not align with original R code")
    if max((max(r["cells"]) for r in rows if r["cells"]),default=0)!=41:
        raise ValueError("original Fig5A 42 population-time columns changed")

    profiles=[]
    for index,(name,kind,source_header) in enumerate(LINES):
        by_day=[]
        for k,day in enumerate(SHEET_DAY_LABELS):
            col=6*index+k
            raw=[float(r["cells"][col]) for r in rows[3:]
                 if col in r["cells"] and type(r["cells"][col]) in (float,int)]
            if len(raw)<8:
                raise ValueError(f"too few clusters in source {name} at {day}")
            as_measured=weighted_phenotype(raw)
            # Published source code excludes >100-um bins only for s2 day10;
            # calculate a clean variant here but *do not* silently use it.
            author_flag=name=="s2" and day=="Day10"
            source_qc=(weighted_phenotype(raw,trim_radius_above=100)
                       if author_flag else None)
            by_day.append({
                "original_xlsx_day_label":day,
                "author_R_analysis_day":AUTHOR_F5_PLOT_DAYS[k],
                "source_excel_column_1indexed":col+1,
                **as_measured,
                "source_R_explicit_radius_outlier_filter_gt_100":author_flag,
                "corresponding_trimmed_sensitivity":source_qc,
            })
        y=[p["mean_radius_um_biomass_weighted_direct"] for p in by_day]
        yy=[p["corresponding_trimmed_sensitivity"]["mean_radius_um_biomass_weighted_direct"]
            if p["corresponding_trimmed_sensitivity"] is not None
            else p["mean_radius_um_biomass_weighted_direct"] for p in by_day]
        profiles.append({
            "author_population_ID":name,
            "founder_phenotype":kind,
            "source_header":source_header,
            "raw_source_measured_objects_across_time":sum(x["original_cluster_objects"] for x in by_day),
            "source_rows":by_day,
            "change_day40_minus_first_um_biomass_weighted":y[-1]-y[0],
            "ordinary_population_time_slope_um_per_R_plot_day":slope(AUTHOR_F5_PLOT_DAYS,y),
            "R_explicit_outlier_trimmed_population_time_slope_um_per_R_plot_day":
                slope(AUTHOR_F5_PLOT_DAYS,yy),
            "population_timepoints_not_independent_evolved_origins":True,
        })
    groups={}
    for kind in ("small","large"):
        pp=[x for x in profiles if x["founder_phenotype"]==kind]
        if len(pp)!=(4 if kind=="small" else 3):
            raise ValueError("seven replay founder lineage audit changed")
        dd=[x["change_day40_minus_first_um_biomass_weighted"] for x in pp]
        ss=[x["ordinary_population_time_slope_um_per_R_plot_day"] for x in pp]
        qq=[x["R_explicit_outlier_trimmed_population_time_slope_um_per_R_plot_day"] for x in pp]
        groups[kind]={
            "independent_original_monoculture_replay_population_n":len(pp),
            "population_IDs":[p["author_population_ID"] for p in pp],
            "all_replay_lines_change_towards_intermediate_size": all(
                x>0 if kind=="small" else x<0 for x in dd),
            "mean_per_line_day40_minus_initial_um":statistics.mean(dd),
            "min_per_line_day40_minus_initial_um":min(dd),
            "max_per_line_day40_minus_initial_um":max(dd),
            "mean_per_line_linear_slope_um_per_day":statistics.mean(ss),
            "population_slope_values":ss,
            "population_day40_minus_first_values":dd,
            "trimmed_R_source_quality_control_mean_slope":statistics.mean(qq),
            "population_IDs_not_cluster_measures_are_independent_units":True,
        }
    diff=exact_population_label_permutation(
        groups["large"]["population_slope_values"],
        groups["small"]["population_slope_values"],
    )
    return {
        "article_doi":"10.1038/s41559-024-02367-y",
        "original_git_pinned_xlsx":origin,
        "author_R_script_original_sha_gates":source,
        "original_Fig5A_column_grain": {
            "author_replication_populations":7,
            "author_timepoint_columns_per_population":6,
            "source_measurement_columns":42,
            "original_day1_source_is_R_analysis_day0_proxy":True,
            "no_independent_growth_vs_survival_dissection_in_this_sheet":True,
        },
        "per_evolving_population":profiles,
        "independent_replay_population_summary":groups,
        "between_founder_phenotypes_exploratory_label_sensitivity":diff,
        "interpretation_ceiling": {
            "not_a_randomly_allocated_lineage_treatment":True,
            "same_source_programme_as_parent_Pineau2024":True,
            "unavailable_original_separate_image_raw_files":True,
            "direct_volume_weighted_estimator_differs_from_author_1500_bin_approx":True,
            "not_five_replays_per_phenotype_in_author_code_or_workbook":True,
            "population_repeated_timepoints_not_42_independent_origins":True,
            "original_source_inconsistent_four_or_five_per_type_unresolved":True,
            "no_genotypic_module_splitting_or_theoretical_Ku_calibrated":True,
        },
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--xlsx",type=Path,required=True)
    p.add_argument("--load-r",type=Path,required=True)
    p.add_argument("--plot-r",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    obj=build_original(args.xlsx.read_bytes(),args.load_r.read_bytes(),args.plot_r.read_bytes())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(obj,indent=2,allow_nan=False,ensure_ascii=False)+"\n")
    print("BITA_PINEAU_F5_REPLAY_RESULT:"+json.dumps(obj,separators=(",",":")),flush=True)


if __name__=="__main__":
    main()
