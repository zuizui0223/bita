"""Direct matched-mutant Fcy1 rescue contrasted against both parental homomers.

Input: the previously verified 22-plate author-derived per-pair JSON.
These descriptive pair contrasts are NOT selection coefficients, full-fitness
comparisons, independent evolution events, or estimates of BITA K(u).
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
from statistics import mean, median

AUTHOR_COMMIT = "f124cef96a3b5806a096b679b2bd57b68aec6514"
AUTHOR_DOI = "10.1126/science.ado5719"
CORRECTED_EXCLUSION = "RESOLVED_BY_PUBLISHED_CROSS_CONTAMINATION_EXCLUSION"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "empirical/trait_architecture_history/despres2024_growth_validation_readout.json"
DEFAULT_OUTPUT = ROOT / "empirical/trait_architecture_history/despres2024_matched_complementarity_readout.json"


def _graph(edges: list[dict]) -> dict:
    adj: dict[str, set[str]] = {}
    for e in edges:
        a,b = e["pair"]
        adj.setdefault(a,set()).add(b)
        adj.setdefault(b,set()).add(a)
    visited=set()
    sizes=[]
    for node in sorted(adj):
        if node in visited:
            continue
        stack=[node]
        visited.add(node)
        n=0
        while stack:
            cur=stack.pop()
            n+=1
            for neighbour in adj[cur]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    stack.append(neighbour)
        sizes.append(n)
    sizes.sort(reverse=True)
    degree=sorted(((a,len(n)) for a,n in adj.items()), key=lambda z:(-z[1],z[0]))
    return {
        "component_sizes":sizes,
        "n_vertices":len(adj),
        "n_edges":len(edges),
        "top_distinct_partner_counts":[
            {"allele":a,"verified_rescue_partners":n} for a,n in degree[:15]],
    }


def match_self_controls(rows: list[dict],threshold:float=.02)->dict:
    """Use a shared OD/h endpoint and the more functional *parental homomer*.

    Test the complete pairs and retain all NA. Thresholding is descriptive;
    153 pair types share alleles and are not independent causal replicates.
    """
    if not math.isfinite(threshold) or threshold<=0:
        raise ValueError("threshold must be finite and positive")
    entries={}
    for r in rows:
        pair=tuple(sorted((r["allele_1"],r["allele_2"])))
        if not pair[0] or not pair[1] or pair in entries:
            raise ValueError("duplicate or blank allele pair")
        v=r["mean_growth_od_per_hour"]
        n=r["n_measured_reciprocal_directions"]
        if v is None:
            if n!=0:raise ValueError("inconsistent missing growth and replicate count")
        elif (not isinstance(v,(int,float)) or not math.isfinite(v)):
            raise ValueError("nonfinite or nonnumeric growth")
        elif type(n) is not int or n not in (1,2):
            raise ValueError("inconsistent number of measured orientations")
        entries[pair]=r
    self_values={a:entries[(a,a)]["mean_growth_od_per_hour"]
                 for a,b in entries if a==b}
    edges=[]
    eligible=[]
    unknown_positive=[]
    disqualified_positive=[]
    n_measured_distinct=0
    n_both_control_measured=0
    n_missing_distinct=0
    for (a,b),row in sorted(entries.items()):
        if a==b:continue
        val=row["mean_growth_od_per_hour"]
        if val is None:
            n_missing_distinct+=1
            continue
        n_measured_distinct+=1
        av=self_values.get(a)
        bv=self_values.get(b)
        if av is None or bv is None:
            if val>=threshold:
                unknown_positive.append({"pair":[a,b], "growth_rate":val,
                    "missing_self_controls":[x for x,v in ((a,av),(b,bv)) if v is None]})
            continue
        n_both_control_measured+=1
        baseline=max(av,bv)
        if baseline>=threshold:
            if val>=threshold:
                disqualified_positive.append({"pair":[a,b],
                                               "growth_rate":val,
                                               "best_self_control":baseline})
            continue
        delta=val-baseline
        record={
            "pair":[a,b],
            "growth_rate":val,
            "parent_homomer_a":av,
            "parent_homomer_b":bv,
            "best_self_control":baseline,
            "gain_over_best_self":delta,
            "n_measured_orientations":row["n_measured_reciprocal_directions"],
            "source_screen_positive":row.get("source_screen_positive"),
        }
        eligible.append(record)
        if val>=threshold:
            edges.append(record)
    all_rescue=sum(r["mean_growth_od_per_hour"] is not None
                   and r["mean_growth_od_per_hour"]>=threshold
                   for (a,b),r in entries.items() if a!=b)
    if all_rescue != len(edges)+len(unknown_positive)+len(disqualified_positive):
        raise ArithmeticError("disconnected phenotype classification")
    graph=_graph(edges)
    values=[p["gain_over_best_self"] for p in eligible]
    return {
        "threshold_od_per_hour":threshold,
        "n_all_distinct_mutant_pairs":sum(a!=b for a,b in entries),
        "n_measured_distinct_mutant_pairs":n_measured_distinct,
        "n_unmeasured_distinct_pairs":n_missing_distinct,
        "n_pairs_with_two_measured_self_controls":n_both_control_measured,
        "n_pairs_with_active_parent_control":sum(
            1 for (a,b),r in entries.items()
            if a!=b and r["mean_growth_od_per_hour"] is not None
            and self_values.get(a) is not None
            and self_values.get(b) is not None
            and max(self_values[a],self_values[b])>=threshold
        ),
        "n_strict_eligible_pairs":len(eligible),
        "n_strict_rescues":len(edges),
        "n_eligible_nonrescues":len(eligible)-len(edges),
        "n_strict_rescues_two_orientations":sum(
            r["n_measured_orientations"]==2 for r in edges
        ),
        "n_positive_distinct_pairs":all_rescue,
        "n_positive_pairs_with_unknown_self_controls":len(unknown_positive),
        "n_positive_pairs_disqualified_by_active_self_control":len(disqualified_positive),
        "unknown_parent_positive_pairs":unknown_positive,
        "active_self_positive_pairs":disqualified_positive,
        "strict_edges":edges,
        "strict_edge_component_sizes":graph["component_sizes"],
        "strict_edge_network":graph,
        "eligible_gain_distribution":{
            "mean_difference_od_per_hour":mean(values) if values else None,
            "median_difference_od_per_hour":median(values) if values else None,
            "n_gain_over_best_self_positive":sum(v>0 for v in values),
            "n_gain_over_best_self_gte_0_02":sum(v>=.02 for v in values),
        },
        "pair_independent_p_value":None,
    }


def derive_source_complementarity(data:dict)->dict:
    if (data.get("paper_doi")!=AUTHOR_DOI
        or data.get("original_ref")!=AUTHOR_COMMIT):
        raise ValueError("wrong source paper or author commit")
    if data.get("raw_source_discrepancy_status")!=CORRECTED_EXCLUSION:
        raise ValueError("published excluded contamination not applied")
    exc=data.get("source_excluded_contaminated_control",{})
    if (exc.get("pair")!=["M93G","M93G"]
        or exc.get("reason")!="cross_contamination_reported_by_authors"):
        raise ValueError("published excluded contamination source is missing")
    rows=data["pair_values"]
    if len(rows)!=171:
        raise ValueError("expected 171 selected genotype pairs")
    m93g=[r for r in rows if r["allele_1"]==r["allele_2"]=="M93G"]
    if len(m93g)!=1 or m93g[0]["mean_growth_od_per_hour"] is not None:
        raise ValueError("contaminated M93G/M93G scored as growth")
    r=match_self_controls(rows,threshold=.02)
    check={
        "n_all_distinct_mutant_pairs":153,
        "n_measured_distinct_mutant_pairs":152,
        "n_strict_eligible_pairs":105,
        "n_strict_rescues":22,
        "n_eligible_nonrescues":83,
        "n_strict_rescues_two_orientations":22,
        "n_positive_distinct_pairs":27,
        "n_positive_pairs_with_unknown_self_controls":5,
    }
    for k,v in check.items():
        if r[k]!=v:
            raise ValueError(f"source reconstruction drift for {k}: {r[k]} vs {v}")
    sensitivity={
        f"{c:.3f}":{
            "eligible":s["n_strict_eligible_pairs"],
            "matched_rescues":s["n_strict_rescues"],
            "positive_with_unknown_homomer":s["n_positive_pairs_with_unknown_self_controls"],
        }
        for c in (.01,.015,.02,.03,.05)
        for s in [match_self_controls(rows,threshold=c)]
    }
    return {
        "source_doi":AUTHOR_DOI,
        "source_commit":AUTHOR_COMMIT,
        "author_notebook_sha":data.get("source_notebook_blob"),
        "author_positive_csv_blob":data.get("original_positive_csv_blob"),
        "data_level":"ORIGINAL_AUTHOR_GROWTH_XLSX_DERIVED_ASSAY_COMPARISON",
        "source_exclusion":exc,
        "same_assay_parental_homomer_baseline":"max(g_AA,g_BB), both same-mutant diploid crosses",
        "source_sample_frame":"18 preselected alleles; 171 unordered genotypes; 153 distinct pairs",
        "matching_method":"Both parental homo controls observed below threshold; same cytosine OD/h assay",
        "comparison":r,
        "threshold_sensitivity":sensitivity,
        "strict_claim_ceiling":(
            "Positive functional rescue of individually defective homomer controls "
            "under one assay; not 22 independent evolutionary origins, a benefit "
            "over ancestral WT, an overall evolutionary selection coefficient, "
            "a neutral-to-specialist historical path or direct BITA K(u) evidence. "
            "Five other positive cross-types lack complete parental homo controls; "
            "no imputation or treating untested combinations as negative."
        ),
        "pooled_meta_analysis_performed":False,
        "independent_evolutionary_transitions_estimated":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,default=DEFAULT_INPUT)
    parser.add_argument("--output",type=Path,default=DEFAULT_OUTPUT)
    args=parser.parse_args()
    data=json.loads(args.source.read_text(encoding="utf-8"))
    result=derive_source_complementarity(data)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    out=result["comparison"]
    print("BITA_FCY1_MATCHED_JSON:"+json.dumps({
        "source":result["source_commit"],
        "verified_strict_pairs":out["n_strict_rescues"],
        "comparable_pairs":out["n_strict_eligible_pairs"],
        "two_direction_rescues":out["n_strict_rescues_two_orientations"],
        "positive_without_homo_controls":out["n_positive_pairs_with_unknown_self_controls"],
        "component_sizes":out["strict_edge_component_sizes"],
        "threshold_sensitivity":result["threshold_sensitivity"],
        "top_edges":out["strict_edges"][:3],
    },ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
