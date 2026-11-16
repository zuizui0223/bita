"""Replicate-true conditional evolution of auxotrophy from original Fig2 pixels.

Original PLOS Genetics article, publisher's full-resolution Figure 2 and
supplemental PDFs are SHA-verified. A heatmap color denotes DETECTION, not
raw colony counts: 96 cells are repeated observations of sixteen independent
evolution populations (8 per environment). Do not infer temporal origin,
fixation, or reciprocal division of labour from auxotrophy detection.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
import argparse
import hashlib
import io
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from statistics import NormalDist

DOI="10.1371/journal.pgen.1006364"
ARTICLE_SHA="6eb810ff515b2aa0a7ccb4190067e97810e7cbaca26bc2947d1ef720f77e0e97"
FIG2_SHA="71da8f3c1707d1ade887d4030446d1869f9fd33b05fa8cfed6fb3cd49823bd8b"
TABLE1_SHA="249f0657f5ce93f155b6ef9b23a59437f5c205ddc3436ea1fdbf71db37074ca7"
TABLE2_SHA="a0bc2dbb9a4bf5c590bb59cfce226986bfa1bdd94274489ebae25413d70b2ab4"
TABLE3_SHA="3047c6a82418eb18378f1d60546f88656db6c9a7ce237ab7bcd9196235dfb0af"
FIG2_URL="https://journals.plos.org/plosgenetics/article/figure/image?size=large&id=10.1371/journal.pgen.1006364.g002"
JATS_URL="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5096674/fullTextXML"
GEN=(0,250,500,1000,1500,2000)
# Readable *interiors* of the exact original 3233×3124-pixel Figure 2
# heatmap. Coordinates are source-original pixel positions, not OCR.
X={
    "AA_present":(411,538,668,796,926,1053),
    "AA_absent":(2022,2152,2282,2415,2542,2672),
}
Y=(170,296,424,553,681,810,938,1064)
SOURCE_EXPECTED={
    "AA_present":(0,0,0,4,2,6),
    "AA_absent":(0,0,1,0,2,0),
}


def sha_gate(raw:bytes,expected:str,desc:str)->None:
    if hashlib.sha256(raw).hexdigest()!=expected:
        raise ValueError(desc+" original source SHA256 mismatch")


def bin_detected(color:tuple[int,int,int])->bool:
    r,g,b=color
    # Exact source figure has nearly-black empty cells and pink-red positive
    # cells. Invalid/gray/white colors must FAIL, not be silently treated zero.
    if max(color)<35:
        return False
    if r>140 and r-g>25 and g<230 and abs(g-b)<15:
        return True
    raise ValueError("ambiguous source Figure 2 cell color "+str(color))


def two_sided_fisher(a:int,n1:int,b:int,n2:int)->float:
    if not all(type(v) is int for v in (a,n1,b,n2)) or min(n1,n2)<1 or not(0<=a<=n1 and 0<=b<=n2):
        raise ValueError("invalid independent population denominator")
    total=a+b;d=math.comb(n1+n2,total)
    def prob(k):return math.comb(n1,k)*math.comb(n2,total-k)/d
    obs=prob(a)
    return sum(prob(k) for k in range(max(0,total-n2),min(total,n1)+1) if prob(k)<=obs+1e-14)


def wilson(k:int,n:int)->tuple[float,float]:
    if not type(k) is int or not type(n) is int or not 0<=k<=n or n<1:
        raise ValueError("invalid success denominator")
    z=NormalDist().inv_cdf(.975);p=k/n
    div=1+z*z/n
    center=(p+z*z/(2*n))/div
    width=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/div
    return center-width,center+width


def newcombe_diff(a:int,n1:int,b:int,n2:int)->tuple[float,float]:
    l1,u1=wilson(a,n1);l2,u2=wilson(b,n2)
    p=a/n1;q=b/n2
    return (p-q-math.hypot(p-l1,u2-q), p-q+math.hypot(u1-p,q-l2))


def source_image(read_image:bytes)->tuple[list[dict],dict]:
    sha_gate(read_image,FIG2_SHA,"Figure 2")
    from PIL import Image
    with Image.open(io.BytesIO(read_image)) as im:
        if im.size!=(3233,3124):raise ValueError("original Figure 2 dimensions changed")
        im=im.convert("RGB")
        rows=[]
        summaries={}
        for condition in ("AA_present","AA_absent"):
            binary=[]
            for row_id,y in enumerate(Y,1):
                current=[]
                for col_id,x in enumerate(X[condition]):
                    pixels=[im.getpixel((x+dx,y+dy)) for dx,dy in
                            ((0,0),(-6,0),(6,0),(0,-6),(0,6))]
                    result=[bin_detected(p) for p in pixels]
                    if len(set(result))!=1:
                        raise ValueError("source pixel classification unstable across interior")
                    v=result[0]
                    current.append(v)
                    rows.append({
                        "condition":condition,
                        "population_id":"R"+str(row_id),
                        "generation":GEN[col_id],
                        "detectable_auxotrophic_colony":v,
                        "figure_cell_rgb":list(pixels[0]),
                        "source_figure_cell_origin_pixel":[x,y],
                        "derived_from":"original_published_heatmap_color_not_raw_colony_count",
                    })
                binary.append(current)
            positive=[sum(s[col] for s in binary) for col in range(len(GEN))]
            if tuple(positive)!=SOURCE_EXPECTED[condition]:
                raise ValueError("source published heatmap counts changed "+condition)
            summaries[condition]={
                "sampled_population_count":len(Y),
                "generations":list(GEN),
                "positive_population_count_per_generation":positive,
                "ever_detected_population_ids":[f"R{i+1}" for i,s in enumerate(binary) if any(s)],
                "detected_at_final_generation_ids":[f"R{i+1}" for i,s in enumerate(binary) if s[-1]],
                "full_source_row_by_generation_binary":binary,
                "inference_unit":"distinct evolved populations not 1000 assayed colonies",
            }
        if len(rows)!=96:
            raise ArithmeticError("source 2×8×6 figure count wrong")
    return rows,summaries


def audit_source_documents(article:bytes,tab1:bytes,tab2:bytes,tab3:bytes)->dict:
    sha_gate(article,ARTICLE_SHA,"JATS")
    root=ET.fromstring(article)
    doi={e.text for e in root.iter("article-id") if e.get("pub-id-type")=="doi"}
    if DOI not in doi:raise ValueError("wrong primary DOI")
    matching=[]
    for sec in root.iter("sec"):
        title=sec.find("title")
        if title is not None and "Amino acid auxotrophies rapidly evolved" in "".join(title.itertext()):
            matching.append(" ".join("".join(sec.itertext()).split()))
    if len(matching)!=1:raise ValueError("source experimental section missing")
    sec=matching[0]
    required=("1,000 colonies","50% (1,000 generations)","25% (1,500 gens.)",
              "75% (2,000 gens.)","Replicate population 3",
              "replicate populations 7 and 8","n = 483","37 (non-AA regime)")
    if not all(w in sec for w in required):
        raise ValueError("published auxiliary source experimental counts changed")
    import fitz
    sources={}
    for name,raw,sha,pages in [
        ("S1_table",tab1,TABLE1_SHA,1),
        ("S2_mutations",tab2,TABLE2_SHA,4),
        ("S3_genomes",tab3,TABLE3_SHA,1)]:
        sha_gate(raw,sha,name)
        with fitz.open(stream=raw,filetype="pdf") as doc:
            if len(doc)!=pages:raise ValueError(name+" PDF page count changed")
            text=" ".join(" ".join(p.get_text("text").split()) for p in doc)
        sources[name]=text
    t1=sources["S1_table"]
    if not all(term in t1 for term in
               ("1,000, AA","1,500, AA","2,000, AA","60 256 157",
                "500, Non-AA","1,500, Non-AA","18 19",
                "Number of strains used")):
        raise ValueError("original S1 Table selection/cohort counts changed")
    t2=sources["S2_mutations"]
    if not all(term in t2 for term in
               ("AT: 18, PT: 5","AT: 19, PT: 6")):
        raise ValueError("original S2 Table mutation-class counts changed")
    t3=sources["S3_genomes"]
    chosen_aa=("2-AA-AT","3-AA-AT","4-AA-AT","5-AA-AT","6-AA-AT","8-AA-AT")
    chosen_na=("7-NA-AT","8-NA-AT")
    chosen_pro=("3-AA-PT","4-AA-PT","5-AA-PT","6-AA-PT","7-NA-PT","8-NA-PT")
    if not all(x in t3 for x in chosen_aa+chosen_na+chosen_pro):
        raise ValueError("original S3 sequenced genotype identities changed")
    return {
        "article_jats_sha256":ARTICLE_SHA,
        "supplement_sha256":{
            "S1_table":TABLE1_SHA,"S2_table":TABLE2_SHA,"S3_table":TABLE3_SHA},
        "source_design":{
            "initial_ancestral_genotype":"prototrophic E. coli",
            "independent_populations_per_regime":8,
            "total_evolved_populations":16,
            "colonies_phenotyped_per_population_per_sampled_generation":1000,
            "generation_samples":list(GEN),
            "regimes":["AA_present","AA_absent"],
            "source_genome_sequencing_subset":{"AA_auxotroph":6,"nonAA_auxotroph":2,
                                               "AA_prototroph":4,"nonAA_prototroph":2},
        },
        "S1_selected_isolate_tally":{
            "AA_1000_gen":60,"AA_1500_gen":256,"AA_2000_gen":157,
            "source_table_AA_sum":473,
            "original_results_text_says_AA":483,
            "unexplained_difference_in_original_sources":10,
            "nonAA_500_gen":18,"nonAA_1500_gen":19,
            "nonAA_source_table_sum_and_results_text":37,
            "scientific_status":"UNRESOLVED_ORIGINAL_TEXT_TABLE_DISCREPANCY"},
        "S2_function_mutation_annotated_occurrences":{
            "auxotroph_structural_gene":18,
            "auxotroph_regulatory_gene":19,
            "prototroph_structural_gene":5,
            "prototroph_regulatory_gene":6,
            "counts_are_mutation_annotations_not_independent_genetic_origins":True,
        },
        "S3_selected_sequenced_genotype_IDs":{
            "AA_auxotroph":list(chosen_aa),
            "nonAA_auxotroph":list(chosen_na),
            "AA_or_nonAA_prototroph":list(chosen_pro),
            "selected_genomes_not_all_16_population_histories":True,
        },
        "source_500_nonAA_label_in_prose":"R3",
        "source_500_nonAA_label_in_figure":"R2",
        "source_500_nonAA_discrepancy":"GENOTYPE_LABEL_CONFLICT_SOURCE_FIGURE_VS_RESULTS_TEXT",
        "source_jats_pubdate_year":2016,
        "original_dryad_doi":"10.5061/dryad.9b47j",
    }


def analyze_source(fig:bytes,jats:bytes,s1:bytes,s2:bytes,s3:bytes)->dict:
    cells,arm=source_image(fig)
    docs=audit_source_documents(jats,s1,s2,s3)
    aa=arm["AA_present"];na=arm["AA_absent"]
    n=8;a=aa["positive_population_count_per_generation"][-1]
    b=na["positive_population_count_per_generation"][-1]
    if (a,b)!=(6,0):
        raise ValueError("source endpoints changed, do not reuse significance test")
    return {
        "doi":DOI,
        "source_fig2_url":FIG2_URL,
        "source_fig2_sha256":FIG2_SHA,
        "primary_jats_url":JATS_URL,
        "source_grade":"ORIGINAL_PUBLISHER_FIG2_BINARY_HEATMAP_NOT_RAW_COLONY_FREQUENCIES",
        "source_validation":docs,
        "figure_cells":cells,
        "sampled_arm_summaries":arm,
        "primary_endpoint":{
            "generation":2000,"aa_positive_populations":a,
            "aa_evolutionary_populations":n,
            "nonAA_positive_populations":b,
            "nonAA_evolutionary_populations":n,
            "risk_difference":a/n-b/n,
            "95pct_newcombe_interval":newcombe_diff(a,n,b,n),
            "two_sided_fisher_exact_p":two_sided_fisher(a,n,b,n),
            "inference":"at-gen-2000 DETECTABLE auxotrophy only, not lifetime mutation origin/fixation",
        },
        "ever_detected_descriptive":{
            "AA_ever_population_count":len(aa["ever_detected_population_ids"]),
            "nonAA_ever_population_count":len(na["ever_detected_population_ids"]),
            "time_window":"0_to_2000_gen","not_an_independent_timepoint_study":True,
            "prevalence_comparison_not_preregistered":True,
        },
        "raw_isolate_frequencies_estimated":False,
        "previous_timepoint_rows_are_repeated_measures":True,
        "independent_research_programmes":1,
        "genetic_auxotrophy_equivalent_to_reciprocal_division_of_labour":False,
        "fitness_effect_of_each_16_lineages_at_timepoint_measured":False,
        "published_raw_dryad_xlsx_verified":False,
        "meta_analysis_performed":False,
        "evidence_ceiling":(
            "Randomized/parallel AA availability comparison identifies an "
            "environment-associated difference in detectably auxotrophic "
            "evolved population outcomes at generation 2000 (6/8 vs 0/8). "
            "The original color heatmap reports categorical bins, not exact "
            "colony numbers, and 1000 phenotyped colonies per line are NOT "
            "1000 independent evolutionary replicates. Earlier and later "
            "timepoints repeatedly sample the same sixteen populations. "
            "AA conditions can change both selection and total population "
            "size or mutation supply, so the experiment does not identify a "
            "pure mutation-rate or pure selection-pressure coefficient. "
            "Prose R3 vs Figure R2 at generation 500 NA and prose n=483 "
            "AA isolates versus original S1 table sum=473 remain unresolved "
            "source inconsistencies and are NOT silently reconciled. "
            "Auxotrophy can derive AA from the medium, not necessarily "
            "another specialist: no proof of two-way reciprocal labour "
            "division, BITA startup cost K(u), optimum functional split "
            "or selection-dependent hysteresis."
        ),
    }


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fig2",type=Path,required=True)
    parser.add_argument("--jats",type=Path,required=True)
    parser.add_argument("--s1",type=Path,required=True)
    parser.add_argument("--s2",type=Path,required=True)
    parser.add_argument("--s3",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    arg=parser.parse_args()
    d=analyze_source(arg.fig2.read_bytes(),arg.jats.read_bytes(),
                     arg.s1.read_bytes(),arg.s2.read_bytes(),arg.s3.read_bytes())
    arg.output.parent.mkdir(parents=True,exist_ok=True)
    arg.output.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print("BITA_ECOLI_AUXOTROPHY_SOURCE_RECEIPT:"+json.dumps({
        "source_fig_sha256":d["source_fig2_sha256"],
        "population_ever":d["ever_detected_descriptive"],
        "endpoint":d["primary_endpoint"],
        "source_errors":d["source_validation"]["S1_selected_isolate_tally"],
    },ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":main()
