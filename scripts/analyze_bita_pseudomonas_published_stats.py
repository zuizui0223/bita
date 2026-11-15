"""Source-locked reconstruction of JEB 2022 Pseudomonas experimental statistics.

NOT original Dryad replicate data (official download endpoint HTTP 401);
four strata of ONE published study, not four evolution-programme replicates.
New standardized values are t / sqrt(df+1), not population-level fitness.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

JATS_SHA256 = "ff26c2e12bcd44bc7137656a7290ac9944ebc6823e8aae405e7a7f4ce999d55e"
JATS_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9323447/fullTextXML"
MEDIA = (
    ("iron_replete", "CAA + 100 uM FeCl3"),
    ("plain_CAA", "plain CAA"),
    ("chelator_100uM", "CAA + 100 uM 2,2-bipyridyl"),
    ("chelator_300uM", "CAA + 300 uM 2,2-bipyridyl"),
)
T_EXPECTED = [(73,12.17,"<",.0001),(73,1.819,"=",.0730),
              (73,-12.89,"<",.0001),(71,-6.745,"<",.0001)]
PROD_SLOPE_EXPECTED = [.0002,-.0008,-.0011,-.0054]
FITNESS_SLOPE_EXPECTED = [-.0129,-.0048,-.0070,-.0075]
EQUILIBRIUM_EXPECTED = [69.80,38.99,22.29,30.09]


def _norm(s: str) -> str:
    return " ".join(s.replace("−","-").replace("‐","-").replace("–","-").split())


def _txt(element: ET.Element) -> str:
    return _norm("".join(element.itertext()))


def _section(root: ET.Element, start: str) -> list[str]:
    matches = []
    for sec in root.iter("sec"):
        t=sec.find("title")
        if t is not None and _txt(t).startswith(start):
            matches.append([_txt(p) for p in sec.findall("p")])
    if len(matches)!=1:
        raise ValueError("missing or duplicate primary-study section "+start)
    return matches[0]


def parse_original_jats(xml_content: bytes) -> dict:
    if hashlib.sha256(xml_content).hexdigest()!=JATS_SHA256:
        raise ValueError("original JATS sha256 mismatch")
    root=ET.fromstring(xml_content)
    paragraphs=_section(root,"Specialization increases productivity")
    coex=_section(root,"Negative frequency")
    method=_section(root,"Productivity of specialist and wildtype cultures")
    if len(paragraphs)!=2 or len(coex)!=1:
        raise ValueError("source RESULTS paragraph count changed")
    pat=r"\bslope\s*[:=]\s*([+-]?\d+\.\d+)"
    pslopes=[float(x) for x in re.findall(pat,paragraphs[0])]
    fslopes=[float(x) for x in re.findall(pat,coex[0])]
    eq=[float(x) for x in re.findall(r"\b(\d{1,3}\.\d{2})%",coex[0])]
    t_found=[(int(df),float(t),op,float(p)) for df,t,op,p in re.findall(
        r"\bt\s*(\d+)\s*=\s*([+-]?\d+(?:\.\d+)?)\s*,\s*p\s*(<|=)\s*(\d+(?:\.\d+)?)",
        paragraphs[1])]
    if t_found!=T_EXPECTED:
        raise ValueError("source WT relative-productivity t statistics changed")
    if pslopes!=PROD_SLOPE_EXPECTED or fslopes!=FITNESS_SLOPE_EXPECTED:
        raise ValueError("source frequency slope vector changed")
    if eq!=EQUILIBRIUM_EXPECTED:
        raise ValueError("source fitted equilibrium vector changed")
    if not any("four experimental blocks" in p and "eight (monocultures)" in p
               and "twelve (mixes)" in p for p in method):
        raise ValueError("block/replicate design missing from Methods")
    figures=[_txt(cap) for figure in root.iter("fig")
             for cap in figure.findall("caption")]
    if not any("12 (mixes) independent replicates" in c for c in figures):
        raise ValueError("mixing-ratio figure replicate grain unverified")
    conditions=[]
    for i,((key,description),(df,t,op,p)) in enumerate(zip(MEDIA,t_found)):
        conditions.append({
            "condition":key,"medium":description,
            "one_sample_t":t,"t_df":df,"t_test_n_implied":df+1,
            "reported_p_operator":op,"reported_p_value":p,
            "standardized_departure_from_wildtype_reference":t/math.sqrt(df+1),
            "productivity_direction_vs_wildtype":
                ("higher" if t>0 and (op=="<" or p<.05)
                 else "lower" if t<0 and (op=="<" or p<.05)
                 else "not_resolved"),
            "productivity_slope_vs_initial_pyochelin":pslopes[i],
            "within_mix_relative_fitness_slope":fslopes[i],
            "fitted_pyochelin_equilibrium_percent":eq[i],
        })
    return {
        "study_doi":"10.1111/jeb.14001",
        "pmcid":"PMC9323447",
        "source_jats_url":JATS_URL,
        "source_jats_sha256":JATS_SHA256,
        "source_grade":"ORIGINAL_PEER_REVIEWED_REPORTED_STATS_NOT_RAW_DRYAD",
        "dryad_dataset_doi":"10.5061/dryad.2bvq83bs4",
        "dryad_data_file_sha256_expected":"b64f8febcc72f30394169d593de5a9ab7cbc3b753d5253dd865a711bc77887f9",
        "dryad_download_gate":{"api_files_http":401,"browser_file_stream_http":403},
        "independent_studies_n":1,"environmental_strata_n":4,
        "new_individual_growth_observations":0,
        "pooled_meta_analysis_performed":False,
        "design":{"growth_metric":"OD600 24-hour integral / matched-media WT integral",
                  "independent_experimental_blocks":4,
                  "mix_replicates_per_medium_and_ratio":12,
                  "monoculture_replicates_per_medium_and_background":8,
                  "initial_pyochelin_percent":[0,5,25,50,75,95,100],
                  "wildtype":"PAO1 produces both siderophores",
                  "pyochelin_only":"PAO1 delta pvdD",
                  "pyoverdine_only":"PAO1 delta pchEF"},
        "conditions":conditions,
        "claim_limit":(
            "Only source-reported four condition-specific one-sample tests and "
            "ANCOVA slopes were re-extracted. Newly derived t/sqrt(df+1) is a "
            "within-study descriptive standardized departure, not a raw mean "
            "difference in OD600 or meta-analytic effect across independent "
            "studies. There are four experiment blocks and 12 replicates per "
            "specialist mixing ratio; the implied t-test n=74 or 72 is not the "
            "number of independent evolutionary origins. Missing original "
            "Dryad XLSX makes joint raw WT uncertainty, block-aware variance "
            "and effect size confidence intervals not identifiable here. "
            "Non-significant p=.073 is not equivalence. A fitted coexistence "
            "frequency is not a long-term evolutionary observation. No BITA "
            "startup cost K(u) or historical shared-to-split origin is measured."
        ),
    }


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--jats",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    o=a.parse_args()
    d=parse_original_jats(o.jats.read_bytes())
    o.output.parent.mkdir(parents=True,exist_ok=True)
    o.output.write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print("BITA_PSEUDOMONAS_SOURCE_READOUT:"+json.dumps({
        "sha":d["source_jats_sha256"],"n":d["environmental_strata_n"],
        "conditions":d["conditions"]},ensure_ascii=False,separators=(',',':')))


if __name__=="__main__":
    main()
