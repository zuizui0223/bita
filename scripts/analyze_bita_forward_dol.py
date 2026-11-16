"""Compare two independent, experimentally documented forward microbial labour splits.

Source is ORIGINAL SHA-locked Kim 2016 and Zhang 2020 publication JATS.
No original culture-replicate table is inferred from figure p-values, and
sampling 20 selected spreading fans / 30 mutant clones is NOT an estimate
of the probability of a new architecture or independent population count.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCES={
  "kim":{"doi":"10.1038/ncomms10508","sha256":"a876e838044cb44ab28c47a1f9e243df3172c15650ad52f56be1e1a1d5c8ab68","pmcid":"PMC4748119"},
  "zhang":{"doi":"10.1126/sciadv.aay5781","sha256":"bfe5787f48f0c2dde277d9d6db6387180472b55c182c5d45738309e45cc0d092","pmcid":"PMC6962034"}
}

def F_to_r2(F:float,df1:int,df2:int)->float:
    if not math.isfinite(F) or F<=0 or type(df1) is not int or type(df2) is not int or min(df1,df2)<=0:
        raise ValueError("invalid F regression degrees of freedom")
    return F*df1/(F*df1+df2)

def _text(el:ET.Element)->str:
    return " ".join("".join(el.itertext()).split())

def _section(root:ET.Element,title:str)->str:
    matches=[]
    for sec in root.iter("sec"):
        name=sec.find("title")
        if name is not None and _text(name)==title:
            matches.append(" ".join(_text(x) for x in sec.findall("p")))
    if len(matches)!=1:
        raise ValueError("original section is not unique: "+title)
    return matches[0]

def _figure(root:ET.Element,label:str)->str:
    matches=[]
    for fig in root.iter("fig"):
        el=fig.find("label")
        if el is not None and _text(el)==label:
            cap=fig.find("caption")
            if cap is not None:matches.append(_text(cap))
    if len(matches)!=1:
        raise ValueError("source figure not unique: "+label)
    return matches[0]

def _require(original:str,items:list[str],description:str)->None:
    for word in items:
        if word.lower() not in original.lower():
            raise ValueError("original source lacks "+description+" term "+word)

def _number(pat:str,content:str,description:str)->float:
    vals=re.findall(pat,content,re.I|re.S)
    if len(vals)!=1:
        raise ValueError("original source expected exactly one numeric "+description)
    return float(vals[0])

def parse_original_jats(original:bytes,which:str)->dict:
    if which not in SOURCES:raise ValueError("unknown original publication")
    src=SOURCES[which]
    if hashlib.sha256(original).hexdigest()!=src["sha256"]:
        raise ValueError("original JATS sha256 mismatch")
    root=ET.fromstring(original)
    dois={x.text for x in root.iter("article-id") if x.get("pub-id-type")=="doi"}
    if src["doi"] not in dois:raise ValueError("original DOI does not match source")
    if which=="kim":
        methods=_section(root,"Identification of mutations in other D morphotypes")
        phen=_section(root,"Rapid radiation and the evolution of collective spreading")
        gen=_section(root,"Genetic basis of the evolution of the D morphotype")
        organisation=_section(root,"M and D robustly self-organize in space")
        controls=_section(root,"D and M carry out distinct tasks to spread collectively")
        reverse=_section(root,"Bidirectional selection of D and M morphotypes")
        figure1=_figure(root,"Figure 1")
        figure2=_figure(root,"Figure 2")
        figure4=_figure(root,"Figure 4")
        _require(methods,["20 dry variants","single spreading fan","discrete isolated M colonies"],
                 "20 independent selected spreading fans")
        _require(phen,["rsmE","D","M","spreading"],"genetic starting state")
        _require(gen,["all had a single mutation in a wsp locus","two-nucleotide deletion","wspC"],
                 "Wsp-dependent selected variants")
        _require(organisation,["10% M to 90% D","negative frequency-dependent selection"],
                 "current within-colony coexistence")
        _require(controls,["mucoid polymer","M*","spreading"],"lubrication deletion control")
        _require(reverse,["resequencing","nonsense mutation","wspE","re-evolves in each case"],
                 "source bidirectional return of partner")
        m=_number(r"(\d+)\s+dry\s+variants",methods,"sequenced variants")
        fig1_p=_number(r"ANOVA;?\s*P\s*=\s*([0-9.]+)",figure1,"mixed colony CFU ANOVA")
        fig4_p=_number(r"ANOVA;?\s*P\s*=\s*([0-9.]+)",figure4,"lubrication polymer-control ANOVA")
        _require(figure1,["M versus M+D","D versus M+D","P<0.01"],
                 "source single vs mixture controls")
        _require(figure2,["three independent colonies"],"within-condition replicate count")
        if (m,fig1_p,fig4_p)!=(20.,.000957,.000167):
            raise ValueError("original Kim observed-source quantities changed")
        return {
            "doi":src["doi"],"pmcid":src["pmcid"],"sha256":src["sha256"],
            "organism":"Pseudomonas fluorescens",
            "parental_genotype_state":"single M parent already carries rsmE frameshift enhancing mucoid polymer",
            "direct_origin_observed":"new D morphotype repeatedly selected from clonally plated M",
            "dry_mutants_sequenced_from_separate_fans":20,
            "all_selected_D_variants_had_Wsp_locus_mutation":True,
            "source_counterfactuals":{
                "pure_M":"no collective spreading phenotype until new D evolves",
                "pure_D":"no collective spreading phenotype until M evolves",
                "engineered_M_plus_D":"spreading and higher CFU than either pure state",
                "M_polymer_loss_plus_D":"no spreading; experimental lubrication dependency",
                "engineered_wspCD_mutant_plus_M":"new dry morphotype and collective spreading",
            },
            "figure_1_single_vs_mixed_cfu_anova_p":fig1_p,
            "figure_4_lubrication_control_cfu_anova_p":fig4_p,
            "figure_2_colonies_per_starting_frequency":3,
            "source_stable_M_fraction_approx":.10,
            "origin_frequency_estimated":False,
            "ancestral_two_function_generalist_documented":False,
            "selected_successes_all_plated_denominator_observed":False,
            "new_absolute_CFU_values_extracted":False,
        }
    src_sec=_section(root,"Antibiotic production is coordinated by a division of labor")
    fig4=_figure(root,"Fig. 4")
    _require(src_sec,["28 of 30","two-sample t tests","F1,29 = 26.58",
                      "F1,7 = 12.32","F1,7 = 37.97",
                      "three additional mutant clones","50%"],
             "selected mutant cost and colony composition")
    _require(fig4,["F2,7 = 107.7","F2,7 = 37.95","r2 = 0.969","r2 = 0.916"],
             "Fig4 within-study mixture-response model results")
    phenotype_sec=_section(root,"Mutants increase the production and diversity of antibiotics")
    _require(phenotype_sec,["Thirty mutant strains","40 of 48 targets"],"original antibacterial panels")
    numbers=re.search(r"(\d+) of (\d+); P < 0\.01",src_sec)
    if numbers is None:raise ValueError("original mutant reproductive-cost denominator unavailable")
    losing,total=(int(v) for v in numbers.groups())
    both=re.findall(r"F2,7\s*=\s*([0-9.]+)",fig4)
    if both!=["107.7","37.95"]:
        raise ValueError("figure 4 two model results changed")
    antibiotic_r2=F_to_r2(float(both[0]),2,7)
    fitness_r2=F_to_r2(float(both[1]),2,7)
    if abs(antibiotic_r2-.969)>.001 or abs(fitness_r2-.916)>.001:
        raise ValueError("original figure F/R2 inconsistent")
    if (losing,total)!=(28,30):
        raise ValueError("source selected mutant cost count changed")
    return {
        "doi":src["doi"],"pmcid":src["pmcid"],"sha256":src["sha256"],
        "organism":"Streptomyces coelicolor",
        "origin_type":"within-clonal-colony recurrent genomic terminal deletion and amplification",
        "selected_mutant_strains":total,
        "selected_mutants_with_reduced_spore_production":losing,
        "genome_change_subset_with_full_size_measurement":"F(1,7) means nine observations not thirty",
        "figure_4_mutant_frequency_model":{
            "antibiotic_F":float(both[0]),"antibiotic_df":[2,7],
            "antibiotic_R2_rederived":antibiotic_r2,
            "spore_fitness_F":float(both[1]),"spore_fitness_df":[2,7],
            "spore_fitness_R2_rederived":fitness_r2
        },
        "fig4_antibiotic_vs_mutant_fraction_F":float(both[0]),
        "fig4_spore_fitness_vs_mutant_fraction_F":float(both[1]),
        "report_composition_region":"up to approximately 50 percent mutant: stronger antibiotic output without reported colony spore loss",
        "selected_mutant_isolates_independent_evolved_architecture_origins":False,
        "single_ancestral_colony_genotype":"S. coelicolor A3(2) M145",
        "new_raw_figure4_growth_or_inhibition_values_extracted":False,
        "origin_frequency_estimated":False,
    }

def audit_two_origins(k:dict,z:dict)->dict:
    if (k.get("doi")!=SOURCES["kim"]["doi"]
        or z.get("doi")!=SOURCES["zhang"]["doi"]):
        raise ValueError("wrong or duplicated source paper")
    if (k.get("dry_mutants_sequenced_from_separate_fans")!=20
        or k.get("figure_1_single_vs_mixed_cfu_anova_p")!=.000957
        or k.get("figure_4_lubrication_control_cfu_anova_p")!=.000167
        or k.get("figure_2_colonies_per_starting_frequency")!=3):
        raise ValueError("Kim source experimental design or outcome changed")
    if (z.get("selected_mutant_strains")!=30
        or z.get("selected_mutants_with_reduced_spore_production")!=28
        or z.get("fig4_antibiotic_vs_mutant_fraction_F")!=107.7
        or z.get("fig4_spore_fitness_vs_mutant_fraction_F")!=37.95):
        raise ValueError("Zhang source experimental design or outcome changed")
    return {
        "independent_research_programmes":2,
        "kim_independent_spreading_fan_mutants_examined":20,
        "kim_origin_probability_estimated":False,
        "kim_selected_genetic_variants_with_Wsp_mutations":"20 sequenced from separate selected successful fans, NOT 20 of all founding colonies",
        "kim_group_CFU_benefit_figure_one_anova_p":.000957,
        "kim_polymer_deletion_abrogates_spreading_anova_p":.000167,
        "zhang_selected_mutant_strains":30,
        "zhang_selected_mutants_with_reduced_spore_production":28,
        "zhang_parental_mutant_spore_cost_fraction_descriptive":28/30,
        "zhang_independent_evolutionary_origins_estimated":False,
        "zhang_group_benefit_mutant_frequency_threshold":"approx 0.50, not an estimated change-point",
        "zhang_antibiotic_production_F2_7":107.7,
        "zhang_colony_spore_cost_F2_7":37.95,
        "pooled_fitness_effect":None,
        "forward_trait_axis_origin_identified":False,
        "category_associations_are_history_not_randomized_independent_effects":True,
        "scientific_boundaries":(
            "Kim M ancestral state already has an rsmE mucoid mutation; "
            "M and D cooperative emergence is NOT direct demonstration of "
            "separating two originally optimized functions in one generalist cell. "
            "Twenty dry isolates were deliberately chosen from different "
            "spreading fans, so 20/20 is not a rate of division-of-labour origin. "
            "Zhang 30 selected mutant clone phenotypes are not thirty independent "
            "new organ-origin events, nor are F2,7 regression fit statistics "
            "WT vs mutant colony mean effects. Higher antibiotic output with "
            "mutant investment up to about 50% without observed spore penalty "
            "is a colony context, not an empirical BITA K(u) threshold. "
            "Both studies use different collective fitness currencies, and no "
            "common meta-analytic effect can be pooled or historical ancestral "
            "two-function fitness landscape identified."
        ),
    }

def analyze(kim_raw:bytes,zhang_raw:bytes)->dict:
    kim=parse_original_jats(kim_raw,"kim")
    zhang=parse_original_jats(zhang_raw,"zhang")
    return {
      "sources":{"kim":{"doi":kim["doi"],"sha256":kim["sha256"],"pmcid":kim["pmcid"]},
                 "zhang":{"doi":zhang["doi"],"sha256":zhang["sha256"],"pmcid":zhang["pmcid"]}},
      "source_grade":"ORIGINAL_PUBLISHED_JATS_WITH_SOURCE_CHECKSUMS_NOT_ORIGINAL_REPLICATE_VALUES",
      "kim_source_readout":kim,
      "zhang_source_readout":zhang,
      "comparison":audit_two_origins(kim,zhang),
      "source_statement_excludes_genetic_ancestry_generalism":True,
      "experimental_raw_data_obtained":False,
      "publication_count_not_metanalysis_n":True,
      "evidence_direction":"new functional collaborator appears within same original colony lineage; not an observed irreversible two-trait architectural switch",
      "independent_reanalysis_claim":"F-to-R2 consistency checks for source published per-study regression fits, not new WT interaction-effect estimates",
    }

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--kim",type=Path,required=True)
    a.add_argument("--zhang",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    r=analyze(args.kim.read_bytes(),args.zhang.read_bytes())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print("BITA_FORWARD_SOURCE_CALC:"+json.dumps({
      "source_shas":r["sources"],
      "kim":r["comparison"]["kim_independent_spreading_fan_mutants_examined"],
      "zhang_selected":r["comparison"]["zhang_selected_mutant_strains"],
      "zhang_spore_cost":r["comparison"]["zhang_selected_mutants_with_reduced_spore_production"],
      "mixed_antibiotic_r2":r["zhang_source_readout"]["figure_4_mutant_frequency_model"]["antibiotic_R2_rederived"],
      "mixed_spore_r2":r["zhang_source_readout"]["figure_4_mutant_frequency_model"]["spore_fitness_R2_rederived"],
    },ensure_ascii=False,separators=(",",":")))

if __name__=="__main__":main()
