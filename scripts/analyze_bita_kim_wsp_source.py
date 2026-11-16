"""Read Kim et al. 2016 original Supplementary Table 2 without pseudo-origins.

Only the source strain catalogue is extracted, NOT a complete twenty-fan
mutation-by-fan table. Genetically engineered controls are not independent
natural origins. The published paper and supplemental PDF are SHA-pinned.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

SOURCE_DOI = "10.1038/ncomms10508"
SOURCE_SHA256 = "deadd620be9018aa3b7f196971a243c703a69db50e49364fe17f6d667a671475"
ARTICLE_SHA256 = "a876e838044cb44ab28c47a1f9e243df3172c15650ad52f56be1e1a1d5c8ab68"
EXPECTED_EVOLVED_DRY = {
    "Pf0-1DV (D)": "wspC", "WspAΔ850-933": "wspA",
    "WspAA381V": "wspA", "WspED648G": "wspE",
}
VALID_PHENOTYPES = {"Wildtype", "Mucoid", "Dry", "Non-mucoid"}


def parse_lines(lines: list[str]) -> list[dict]:
    rows=[]
    for line in lines:
        cols=[v.strip() for v in re.split(r"\s{2,}",line.strip()) if v.strip()]
        if len(cols)<3 or cols[2] not in VALID_PHENOTYPES:
            continue
        if len(cols)>4:
            raise ValueError("original source strain catalogue field count changed")
        if len(cols)==3:
            if cols[0] not in ("Pf0-1","Pf0-1MV (M)"):
                raise ValueError("source reference class missing on unexpected genotype")
            reference="published_ancestor"
        else:
            reference=cols[3]
            if reference not in ("Evolved isolate","Constructed isolate"):
                raise ValueError("unexpected original source reference class")
        rows.append({
            "source_row_number":len(rows)+1, "strain":cols[0],
            "genotype":cols[1], "phenotype":cols[2],
            "source_reference":reference,
        })
    return rows


def analyze_rows(rows: list[dict]) -> dict:
    if len(rows)!=26:
        raise ValueError("original Supplementary Table 2 has 26 strain entries")
    names=[r["strain"] for r in rows]
    if len(names)!=len(set(names)):
        raise ValueError("duplicate source strain")
    if [r["source_row_number"] for r in rows]!=list(range(1,27)):
        raise ValueError("source strain catalogue row index changed")
    classes=Counter(r["source_reference"] for r in rows)
    phenotypes=Counter(r["phenotype"] for r in rows)
    if classes!={"published_ancestor":2,"Constructed isolate":19,"Evolved isolate":5}:
        raise ValueError("unexpected original strain classes")
    if phenotypes!={"Wildtype":1,"Mucoid":10,"Dry":9,"Non-mucoid":6}:
        raise ValueError("source phenotype classification drift")
    dry={r["strain"]:r for r in rows if r["phenotype"]=="Dry"
         and r["source_reference"]=="Evolved isolate"}
    if set(dry)!=set(EXPECTED_EVOLVED_DRY):
        raise ValueError("dry evolved source genotype identities changed")
    for name,gene in EXPECTED_EVOLVED_DRY.items():
        if gene not in dry[name]["genotype"] or "Pf0-1MV" not in dry[name]["genotype"]:
            raise ValueError("evolved dry allele/genetic background mismatch")
    by={r["strain"]:r for r in rows}
    mucoid=by["wspE#"]
    if (mucoid["source_reference"]!="Evolved isolate"
        or mucoid["phenotype"]!="Mucoid"
        or "WspAΔ850-933" not in mucoid["genotype"]
        or "wspE" not in mucoid["genotype"]):
        raise ValueError("D-to-M reversion source not correctly identified")
    if (by["wspC:D"]["source_reference"]!="Constructed isolate"
        or by["wspC:D"]["phenotype"]!="Dry"
        or by["wspC:D"]["genotype"]!=by["Pf0-1DV (D)"]["genotype"]):
        raise ValueError("engineered WspCD reconstruction did not match original evolved Dry allele")
    for name in ("ΔwspC","ΔwspD","ΔwspCΔwspD"):
        if by[name]["source_reference"]!="Constructed isolate" or by[name]["phenotype"]!="Mucoid":
            raise ValueError("source Wsp knockout negative control was recoded")
    if by["M*"]["source_reference"]!="Constructed isolate" or by["M*"]["phenotype"]!="Non-mucoid":
        raise ValueError("polymer knockout control missing")
    return {
        "paper_doi":SOURCE_DOI,
        "source_pdf_sha256":SOURCE_SHA256,
        "parent_article_jats_sha256":ARTICLE_SHA256,
        "source_document":"Kim et al. 2016 Nature Communications, Supplementary Information Table 2, PDF page 7",
        "sample_frame":"selected original experimental strain catalogue, not the 20 independent selected dry fans",
        "source_table_strains_n":len(rows),
        "source_classes":dict(classes),
        "phenotype_counts":dict(phenotypes),
        "evolved_dry_representative_strains_n":len(dry),
        "evolved_dry_representative_mutation_targets":dict(EXPECTED_EVOLVED_DRY),
        "evolved_dry_representative_targets_gene_count":dict(Counter(EXPECTED_EVOLVED_DRY.values())),
        "representative_dry_wsp_target_genes":sorted(set(EXPECTED_EVOLVED_DRY.values())),
        "evolved_M_reversion_entries_n":1,
        "evolved_M_reversion_from":mucoid["genotype"],
        "constructed_matching_D_allele":"wspC:D",
        "constructed_Wsp_knockout_negative_controls":["ΔwspC","ΔwspD","ΔwspCΔwspD"],
        "constructed_polymer_negative_control":"M*",
        "published_separately_selected_dry_fans_sequenced_n":20,
        "per_20_fan_allele_frequency_identified":False,
        "gene_specific_mutation_origin_rate_identified":False,
        "all_ancestral_plated_colonies_total_identified":False,
        "evolved_representative_entries_are_not_an_unbiased_origin_denominator":True,
        "fitness_gain_per_genotype_estimated_from_table":False,
        "claim_ceiling":(
            "Original Supplementary Table 2 is a strain catalogue: exactly four "
            "source-labelled evolved Dry representative genotypes across WspA, "
            "WspC and WspE; one evolved Mucoid revertant; 19 constructed "
            "isolates and two source ancestor/prior strains. The 20 selected "
            "sequenced D morphotypes referenced in Methods do not appear "
            "individually with their alleles in this table. Therefore 2/4 at "
            "wspA cannot be interpreted as the mutation-target frequency among "
            "the 20 selected fans, nor can 20/20 estimate the incidence of "
            "division of labour from all founding M colonies. Constructed "
            "isolates do not count as independent natural evolution. This table "
            "does not identify BITA K(u), trait-axis split in a two-function "
            "generalist, or historical hysteresis."
        ),
        "table_rows":rows,
    }


def parse_source_pdf(pdf_bytes: bytes) -> dict:
    if hashlib.sha256(pdf_bytes).hexdigest()!=SOURCE_SHA256:
        raise ValueError("original source PDF SHA256 mismatch")
    import fitz
    with fitz.open(stream=pdf_bytes,filetype="pdf") as pdf:
        if len(pdf)!=9:
            raise ValueError("original supplement pagination changed")
        if "Supplementary Table 2. Description" not in pdf[6].get_text("text"):
            raise ValueError("original source Table 2 not on page 7")
        words=pdf[6].get_text("words")
    anchors=[x for x in words
             if 320<=x[0]<390 and x[4] in VALID_PHENOTYPES
             and 120<x[1]<495]
    if len(anchors)!=26:
        raise ValueError("source PDF physical row count changed")
    lines=[]
    for anchor in anchors:
        row=[x for x in words if 72<=x[0]<535 and abs(x[1]-anchor[1])<3.5]
        cells=[]
        for lo,hi in ((72,145),(145,320),(320,390),(390,535)):
            cells.append(" ".join(x[4] for x in sorted(
                row,key=lambda x:x[0]) if lo<=x[0]<hi))
        if cells[0] in ("Pf0-1","Pf0-1MV (M)"):
            if cells[3] not in ("1","2"):
                raise ValueError("original bibliography footnotes changed")
            cells=cells[:3]
        lines.append("   ".join(cells))
    return analyze_rows(parse_lines(lines))


def verify_source_article_jats(source: bytes) -> dict:
    if hashlib.sha256(source).hexdigest()!=ARTICLE_SHA256:
        raise ValueError("original parent article JATS SHA256 mismatch")
    root=ET.fromstring(source)
    dois={e.text for e in root.iter("article-id") if e.get("pub-id-type")=="doi"}
    if SOURCE_DOI not in dois:
        raise ValueError("source article DOI changed")
    methods=[]
    for sec in root.iter("sec"):
        title=sec.find("title")
        if title is not None and "".join(title.itertext()).strip()=="Identification of mutations in other D morphotypes":
            methods.append(" ".join("".join(sec.itertext()).split()))
    if (len(methods)!=1
        or "sequenced in 20 dry variants" not in methods[0]
        or "each isolated from a single spreading fan emerging from discrete isolated M colonies" not in methods[0]):
        raise ValueError("source Methods positive-fan sampling units missing")
    return {
        "primary_source_jats_sha256":ARTICLE_SHA256,
        "selected_dry_fans_sequenced_according_to_methods":20,
        "per_fan_allele_data_available_in_supp_table2":False,
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pdf",type=Path,required=True)
    p.add_argument("--jats",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    d=parse_source_pdf(a.pdf.read_bytes())
    d["original_article_methods_confirmation"]=verify_source_article_jats(a.jats.read_bytes())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("BITA_KIM_WSP_READOUT:"+json.dumps({
        "source_sha256":d["source_pdf_sha256"],
        "n_strains":d["source_table_strains_n"],
        "n_evolved_dry":d["evolved_dry_representative_strains_n"],
        "genes":d["representative_dry_wsp_target_genes"],
        "per_20_fan_frequency_estimated":d["per_20_fan_allele_frequency_identified"],
    },ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
