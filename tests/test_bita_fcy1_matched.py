"""Fcy1 fixed-panel, matched self-control complementarity safeguards.

Synthetic tests of inference contracts. Original 22-plate reconstruction is
covered separately by a source-pinned Actions workflow; not recreated in CI.
"""
import copy
import pytest

from scripts.analyze_bita_fcy1_matched import (
    match_self_controls, derive_source_complementarity,
)


def synthetic_pairs():
    def rec(a,b,g,screen=False,n=2):
        return dict(allele_1=a, allele_2=b,
                    mean_growth_od_per_hour=g,
                    n_measured_reciprocal_directions=(0 if g is None else n),
                    source_screen_positive=screen)
    return [
        rec("A","A",.003),
        rec("B","B",.005),
        rec("C","C",None),
        rec("A","B",.09,screen=True),
        rec("A","C",.08,screen=True),
        rec("B","C",None),
    ]


def test_exact_comparison_to_best_homomer_not_wild_type_or_zero():
    x=match_self_controls(synthetic_pairs(),threshold=.02)
    assert x["n_all_distinct_mutant_pairs"] == 3
    assert x["n_measured_distinct_mutant_pairs"] == 2
    assert x["n_pairs_with_two_measured_self_controls"] == 1
    assert x["n_strict_eligible_pairs"] == 1
    assert x["n_strict_rescues"] == 1
    assert x["n_eligible_nonrescues"] == 0
    assert x["n_positive_pairs_with_unknown_self_controls"] == 1
    assert x["n_unmeasured_distinct_pairs"] == 1
    assert x["strict_edges"][0]["pair"] == ["A","B"]
    assert x["strict_edges"][0]["growth_rate"] == pytest.approx(.09)
    assert x["strict_edges"][0]["best_self_control"] == pytest.approx(.005)
    assert x["strict_edges"][0]["gain_over_best_self"] == pytest.approx(.085)
    assert x["strict_edges"][0]["n_measured_orientations"] == 2


def test_contaminated_self_control_cannot_be_imputed_as_zero():
    p=synthetic_pairs()
    for x in p:
        if x["allele_1"]==x["allele_2"]=="B":
            x["mean_growth_od_per_hour"]=None
            x["n_measured_reciprocal_directions"]=0
    r=match_self_controls(p)
    assert r["n_strict_rescues"]==0
    assert r["n_positive_pairs_with_unknown_self_controls"]==2
    assert r["n_pairs_with_two_measured_self_controls"]==0


def test_complete_reciprocal_orientation_gate():
    p=synthetic_pairs()
    for x in p:
        if [x["allele_1"],x["allele_2"]]==["A","B"]:
            x["n_measured_reciprocal_directions"]=1
    r=match_self_controls(p)
    assert r["n_strict_rescues"]==1
    assert r["n_strict_rescues_two_orientations"]==0


def test_alternative_thresholds_recompute_both_self_and_pair():
    p=synthetic_pairs()
    r=match_self_controls(p, threshold=.10)
    assert r["n_strict_rescues"]==0
    r=match_self_controls(p,threshold=.05)
    assert r["n_strict_rescues"]==1
    with pytest.raises(ValueError,match="threshold"):
        match_self_controls(p,threshold=-.1)


def test_duplicate_pairs_or_nans_are_rejected():
    p=synthetic_pairs()
    with pytest.raises(ValueError,match="duplicate"):
        match_self_controls(p+[copy.deepcopy(p[0])])
    p=synthetic_pairs()
    p[0]["mean_growth_od_per_hour"]=float("nan")
    with pytest.raises(ValueError,match="nonfinite"):
        match_self_controls(p)
    p=synthetic_pairs()
    p[0]["mean_growth_od_per_hour"]=None
    p[0]["n_measured_reciprocal_directions"]=2
    with pytest.raises(ValueError,match="inconsistent"):
        match_self_controls(p)


def test_source_wrapper_rejects_old_contaminated_full_panel():
    old={"paper_doi":"10.1126/science.ado5719",
         "original_ref":"f124cef96a3b5806a096b679b2bd57b68aec6514",
         "raw_source_discrepancy_status":"ONE_ADDITIONAL_MEASURED_M93G_M93G_HIGH_GROWTH_VS_SAVED_NOTEBOOK_OUTPUT",
         "pair_values":synthetic_pairs()}
    with pytest.raises(ValueError,match="excluded contamination"):
        derive_source_complementarity(old)


def test_small_set_can_be_empty_without_invented_p():
    rows=[dict(allele_1="A",allele_2="A",mean_growth_od_per_hour=.001,
               n_measured_reciprocal_directions=2),
          dict(allele_1="B",allele_2="B",mean_growth_od_per_hour=.002,
               n_measured_reciprocal_directions=2),
          dict(allele_1="A",allele_2="B",mean_growth_od_per_hour=.003,
               n_measured_reciprocal_directions=2)]
    res=match_self_controls(rows)
    assert res["n_strict_eligible_pairs"]==1
    assert res["n_strict_rescues"]==0
    assert res["strict_edge_component_sizes"]==[]
    assert res["pair_independent_p_value"] is None


def test_frozen_original_source_strict_edges_and_summary_are_self_consistent():
    import csv
    import json
    from collections import Counter
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    base=root/"empirical/trait_architecture_history"
    s=json.loads((base/"despres2024_matched_summary.json").read_text(encoding="utf-8"))
    with (base/"despres2024_matched_strict_rescues.csv").open(newline="",encoding="utf-8") as stream:
        edges=list(csv.DictReader(stream))
    assert len(edges)==s["strict_both_parent_nonfunctional_and_pair_functional"]==22
    assert s["both_parent_homomers_directly_measured_nonfunctional_pairs"]==105
    assert s["strict_nonrescued_on_same_support"]==83
    assert s["growth_positive_pairs_missing_any_parental_control"]==5
    assert s["paper_contaminated_control_excluded"]=="M93G/M93G"
    assert not s["cross_study_meta_analysis_performed"]
    alleles=set()
    seen=set()
    degrees=Counter()
    n_unscreened=0
    for e in edges:
        a,b=e["allele_1"],e["allele_2"]
        assert a!=b and (a,b) not in seen
        seen.add((a,b))
        alleles.update((a,b))
        degrees.update([a,b])
        ab,aa,bb,delta=(float(e[key]) for key in (
            "growth_AB_OD_per_h","growth_AA_OD_per_h",
            "growth_BB_OD_per_h","gain_over_best_self_OD_per_h"))
        assert ab>=.02 and 0<=aa<.02 and 0<=bb<.02
        assert delta == pytest.approx(ab-max(aa,bb),abs=2e-8)
        assert int(e["n_reciprocal_directions"])==2
        assert e["screen_positive"] in ("true","false")
        n_unscreened+=e["screen_positive"]=="false"
    assert len(alleles)==s["strict_rescue_graph"]["distinct_allele_vertices"]==13
    assert degrees["M100W"]==9 and degrees["R73G"]==6
    assert n_unscreened==3
    sensitivity=s["threshold_sensitivity"]
    assert [(x["threshold_OD_per_hour"],x["strict_rescues"]) for x in sensitivity]==[
        (.01,28),(.015,22),(.02,22),(.03,19),(.05,18)]
