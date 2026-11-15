"""Audit original PNAS 2024 evolution from two specialists to an autonomist.

Population grain = independently evolved culture (12 per original regimen).
Derived tests are exploratory comparisons of published event counts, not
raw trajectories, new experimental observations, a forward BITA origin, or
an empirically calibrated startup cost/hysteresis.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from statistics import NormalDist

SOURCE_XML_SHA256 = "64bfc840381c06b3fd417da5ea068a51d9c1854e67af22b8b7a54e54cc3494d6"
DOI = "10.1073/pnas.2317182121"
JATS_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11363282/fullTextXML"


def _counts(x: int, n: int) -> None:
    if type(x) is not int or type(n) is not int or n < 1 or x < 0 or x > n:
        raise ValueError("counts must be nonnegative integers bounded by n")


def wilson(x: int, n: int) -> tuple[float, float]:
    _counts(x, n)
    z = NormalDist().inv_cdf(.975)
    p = x / n
    d = 1 + z*z/n
    centre = (p + z*z/(2*n))/d
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return centre-half, centre+half


def newcombe_difference(a: int, n1: int, b: int, n2: int) -> tuple[float, float]:
    _counts(a, n1)
    _counts(b, n2)
    p, q = a/n1, b/n2
    l1, u1 = wilson(a, n1)
    l2, u2 = wilson(b, n2)
    return (p-q-math.hypot(p-l1, u2-q),
            p-q+math.hypot(u1-p, q-l2))


def fisher_exact_2sided(a: int, n1: int, b: int, n2: int) -> float:
    _counts(a, n1)
    _counts(b, n2)
    total = a+b
    denom = math.comb(n1+n2, total)
    def probability(x):
        return math.comb(n1,x)*math.comb(n2,total-x)/denom
    observed = probability(a)
    return sum(probability(x)
               for x in range(max(0,total-n2),min(total,n1)+1)
               if probability(x) <= observed+1e-16)


def fisher_freeman_halton(n: list[int], x: list[int]) -> float:
    if len(n) != 3 or len(x) != 3:
        raise ValueError("requires exactly three regimes")
    for xi,ni in zip(x,n):
        _counts(xi,ni)
    total_successes = sum(x)
    denominator = math.comb(sum(n),total_successes)
    observed = math.prod(math.comb(ni,xi)
                         for ni,xi in zip(n,x))/denominator
    exact_p = 0.
    for values in itertools.product(*(range(min(ni,total_successes)+1) for ni in n)):
        if sum(values) != total_successes:
            continue
        probability = math.prod(math.comb(ni,xi)
                                for ni,xi in zip(n,values))/denominator
        if probability <= observed+1e-16:
            exact_p += probability
    return exact_p


def holm(pvalues: list[float]) -> list[float]:
    if not pvalues or any(not math.isfinite(p) or p<0 or p>1 for p in pvalues):
        raise ValueError("invalid p-values")
    ranked = sorted(range(len(pvalues)),key=lambda i:pvalues[i])
    out = [0.] * len(pvalues)
    running = 0.
    for j,i in enumerate(ranked):
        running = max(running,(len(pvalues)-j)*pvalues[i])
        out[i] = min(1.,running)
    return out


def _text(el: ET.Element) -> str:
    return " ".join("".join(el.itertext()).split())


def _section(root: ET.Element, beginning: str) -> str:
    matches=[]
    for sec in root.iter("sec"):
        title=sec.find("title")
        if title is not None and _text(title).startswith(beginning):
            matches.append(" ".join(_text(p) for p in sec.findall("p")))
    if len(matches)!=1:
        raise ValueError("source section not uniquely identified: "+beginning)
    return matches[0]


def _caption(root: ET.Element, index: int) -> str:
    matches=[]
    for fig in root.iter("fig"):
        label=fig.find("label")
        if label is None or _text(label)!=f"Fig. {index}.":
            continue
        cap=fig.find("caption")
        if cap is not None:
            matches.append(_text(cap))
    if len(matches)!=1:
        raise ValueError("original figure caption missing")
    return matches[0]


def parse_source_counts(source: bytes) -> dict:
    root=ET.fromstring(source)
    dois=[(id.text or "") for id in root.iter("article-id")
          if id.get("pub-id-type")=="doi"]
    if DOI not in dois:
        raise ValueError("wrong source paper DOI")
    methods=_section(root,"Cultural Conditions and the Evolution Experiments.")
    mutual=_section(root,"Degrader dominated the community when the mutualistic consortium evolved")
    conditions=_section(root,"Fluctuating Environments Create Conditions Critical for the Evolution of Autonomy.")
    fluct=_section(root,"Autonomous genotypes evolved from the cooperative specialists under the fluctuating environment.")
    simulation=_section(root,"Quantitative explanations for the evolution of autonomy from the mutualistic consortium")
    simulated_sets=_section(root,"The effect of fluctuating environments on the evolution of autonomy is pathway-dependent.")
    discussion=_section(root,"Discussion")
    fig3=_caption(root,3)
    fig4=_caption(root,4)
    required={
        "design":(methods,("Twelve independent replicates","two out of 12 replicates","extinct after 50 generations")),
        "constant_mutualism":(mutual,("did not observe","autonomous genotypes","280 generations")),
        "competition_and_immigration":(conditions,("autonomous genotypes did not evolve","competition condition","three of twelve replicates","twelve novel replicates")),
        "fluctuating_lineages":(fluct,("five of 12 replicates","replicates 1, 4, 6, 7, and 11","all isolates evolved to regain","three of five replicates","other two replicates")),
        "figure3":(fig3,("five replicates","Four clonal isolates","all the evolved isolates regained")),
        "figure4":(fig4,("three out of twelve replicates","six out of twelve replicates","OD600 = 0.05","OD600 = 0.1")),
        "model_defaults":(simulation,("59 replicates","16 of 100 replicates","100 replicated simulations")),
        "model_parameter_sets":(simulated_sets,("17,501","13,905","2,269","1,003","10,633")),
        "discussion":(discussion,("five of twelve replicates",)),
    }
    for name,(text,terms) in required.items():
        if not all(term.lower() in text.lower() for term in terms):
            raise ValueError("original publication wording changed: "+name)
    match=re.search(r"namely replicates\s+((?:\d+[, ]+(?:and\s+)?){4}\d+)",fluct)
    if match is None:
        raise ValueError("no source lineage identifiers")
    lineages=[int(v) for v in re.findall(r"\d+",match.group(1))]
    if lineages != [1,4,6,7,11]:
        raise ValueError("unexpected original lineages")
    return {
        "lineage_ids":lineages,
        "readdition_counts":(3,6),
        "barcodes":(3,2),
        "source_mutualism_still_success":0,
        "source_competition_still_success":0,
        "simulations_default":(59,16,100),
        "parameter_partition":(2269,1003,10633,17501-13905),
        "mutualism_censored_at_50_gen":2,
        "default_independent_rep_per_regime":12,
    }


def analyze_primary_jats(source: bytes) -> dict:
    if hashlib.sha256(source).hexdigest()!=SOURCE_XML_SHA256:
        raise ValueError("original PNAS JATS SHA256 mismatch")
    coding=parse_source_counts(source)
    conditions=[
        {"condition":"constant_mutualism","carbon_regime":"naphthalene always",
         "autonomy_lineages":0,"started_lineages":12,
         "censored_extinct_lineages":2,"eventually_analyzed_surviving_lineages":10},
        {"condition":"constant_competition","carbon_regime":"pyruvate always",
         "autonomy_lineages":0,"started_lineages":12,
         "censored_extinct_lineages":0,"eventually_analyzed_surviving_lineages":12},
        {"condition":"alternating_mutualism_competition",
         "carbon_regime":"naphthalene alternates with pyruvate",
         "autonomy_lineages":5,"started_lineages":12,
         "censored_extinct_lineages":0,"eventually_analyzed_surviving_lineages":12}
    ]
    p=fisher_exact_2sided(5,12,0,12)
    return {
        "source_doi":DOI,
        "source_jats_url":JATS_URL,
        "source_xml_sha256":SOURCE_XML_SHA256,
        "source_grade":"ORIGINAL_PNAS_JATS_PUBLISHED_COUNTS_NOT_RAW_PER_LINE_DATA",
        "one_independent_programme":True,
        "source_grain":"independent_experimentally_evolved_population",
        "source_publication_year":2024,
        "organism":"Pseudomonas stutzeri",
        "design":"Engineered Degrader and Detoxifier: naphthalene to salicylate to small molecules",
        "three_original_regimes":conditions,
        "constant_mutualism_extinct_after_50_gen":2,
        "three_regime_success_counts":[0,0,5],
        "three_regime_started_counts":[12,12,12],
        "fluctuation_autonomy_success_proportion":5/12,
        "fluctuation_success_95pct_wilson":wilson(5,12),
        "constant_success_95pct_wilson":wilson(0,12),
        "core_exact_omnibus_p_two_sided":fisher_freeman_halton([12]*3,[0,0,5]),
        "dropout_sensitivity_omnibus_p":fisher_freeman_halton([10,12,12],[0,0,5]),
        "exploratory_two_pairwise_unadjusted_p":[p,p],
        "two_separate_pairwise_holm_adjusted_p":holm([p,p]),
        "pairwise_mutualism_survivor_sensitivity_unadjusted_p":fisher_exact_2sided(5,12,0,10),
        "exploratory_fluctuating_vs_constant_wilson_newcombe_RD":{
            "difference":5/12,
            "95pct_interval":newcombe_difference(5,12,0,12),
            "95pct_interval_dropouts_excluded":newcombe_difference(5,12,0,10)
        },
        "readdition_experiments":[
            {"environment":"mutualism_with_detoxifier_readded","od600_at_start":.05,
             "autonomy_lineages":3,"started_lineages":12,"independent_experiment":True},
            {"environment":"mutualism_with_detoxifier_readded_higher_density","od600_at_start":.1,
             "autonomy_lineages":6,"started_lineages":12,"independent_experiment":True}
        ],
        "readdition_high_density_vs_low_density_RD":{
            "difference":.25,
            "95pct_interval":newcombe_difference(6,12,3,12),
            "fisher_2sided_p":fisher_exact_2sided(6,12,3,12)
        },
        "fluctuating_genetic_origins":{
            "independent_lineages":5,
            "degrader_barcode_lineages":3,
            "detoxifier_barcode_lineages":2,
            "four_clones_per_lineage":4,
            "clonal_isolates_from_five_evolved_populations":20,
            "restored_missing_operons_in_sequenced_isolates":True,
            "hgt_route_supported_by_homologous_recombination":"reported_consistent_with_HGT_not_direct_time_resolved_transfer"
        },
        "experimental_mechanism":{
            "fluctuation_favors_parent_coexistence":"source_association_and_readdition_test",
            "higher_cell_density_favors_autonomy":"source_trend_from_0_05_to_0_1_no_significant_between_arm_test",
            "pyruvate_cycle_od600_approx":1.,
            "naphthalene_cycle_od600_approx":.4,
            "gene_transfer_directly_time_resolved":False
        },
        "model_only":{
            "default_fluctuating_sim_successes":59,
            "default_mutualism_sim_successes":16,
            "default_simulation_replicates_per_regime":100,
            "parameter_sets":17501,
            "parameter_set_fluct_only":2269,
            "parameter_set_mut_only":1003,
            "parameter_set_both":10633,
            "parameter_set_neither":17501-2269-1003-10633,
            "modelled_parameter_sets_not_independent_experimental_replicates":True
        },
        "two_directions_tested":["specialists_to_autonomy"],
        "forward_specialization_origin_identified":False,
        "hysteresis_identified":False,
        "original_per_line_growth_trajectories_acquired":False,
        "author_simulations_independent_evidence":False,
        "mixed_control_regimes_pooled_as_one_meta_study":False,
        "publication_stage":"EXPLORATORY_REANALYSIS_NOT_PREREGISTERED",
        "claim_ceiling":(
            "Autonomist evolved from engineered specialists in 5/12 alternating lineages, "
            "0/12 constant mutualism and 0/12 constant competition. Two mutualism lineages "
            "went extinct early, requiring 0/10 survival sensitivity alongside original 0/12. "
            "Exploratory exact tests presume independent culture lines and treatment exchangeability. "
            "No raw times-to-origin or growth trajectories. Immigration studies are independent "
            "cohorts, not the same histories or direct HGT mechanism knockouts. 3/12 versus 6/12 "
            "density manipulation is not significant by two-sided Fisher. Source barcode tags "
            "and restored deleted operons support recombination, but actual transfer events "
            "were not observed in real time. Reverse direction only: no historical "
            "shared-to-specialized origin, no empirical K(u), no hysteresis loop. "
            "Authors' 17,501 model parameter sets are not biological replicates."
        )
    }


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xml",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    record=analyze_primary_jats(args.xml.read_bytes())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
                           encoding="utf8")
    print("BITA_AUTONOMY_EXPERIMENT_JSON:"+json.dumps({
        "source_sha256":record["source_xml_sha256"],
        "regimes":record["three_original_regimes"],
        "three_arm_exact_p":record["core_exact_omnibus_p_two_sided"],
        "censor_sensitivity_exact_p":record["dropout_sensitivity_omnibus_p"],
        "Holm_pairwise":record["two_separate_pairwise_holm_adjusted_p"],
        "readdition":record["readdition_experiments"]
    },ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
