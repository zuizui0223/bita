"""Inspect original Merianieae floral-trait/phylogeny overlap, not evolutionary causation.

Source: Dellinger et al. 2024 *Systematic Biology*, public Zenodo record
7659158, 135861-byte scripts+data ZIP (SHA256 pinned). Original floral
morphology and reward codes derive from Dellinger et al. 2019/2021; papers
are NOT independent replications of floral heteranthery origins.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

DOI = "10.1093/sysbio/syae011"
ZENODO_URL = "https://zenodo.org/api/records/7659158/files/skripts.zip/content"
ZIP_SHA256 = "9d4013d470d1d201ef89196442614429a4146ba2958e1367b0a197ef50b03ed8"
CSV_SHA256 = "1f4fc947db34e31ed6f7e76642f19763d473419617aa6563c0f6421dc33394ae"
SOURCE_CSV = "1_morphospaces_disparity/floraltraits.csv"
SOURCE_TREE = "1_morphospaces_disparity/Marcelo_Meris.tre"
REWARDS = {"0": "pollen", "1": "nectar", "2": "food_body"}
SHAPES = {
    "0": "isomorphic_or_no_shape_difference",
    "1": "shape_difference_code_1",
    "2": "shape_difference_code_2",
}
MISSING = {"", "NA"}


def reward_group(raw: str) -> str | None:
    if raw in MISSING:
        return None
    if raw not in REWARDS:
        raise ValueError("unexpected original reward code: "+raw)
    return REWARDS[raw]


def source_category(raw: str) -> str | None:
    if raw in MISSING:
        return None
    if raw not in SHAPES:
        raise ValueError("unexpected original shape code: "+raw)
    return SHAPES[raw]


def summarize_records(rows: list[dict], phylogeny_tips: set[str]) -> dict:
    required = {"x","species","confirmed.reward.type","stamen.shape.dimorphism"}
    if not rows or not phylogeny_tips:
        raise ValueError("empty trait data or tree")
    ids=set()
    names=set()
    for r in rows:
        if not required.issubset(r):
            raise ValueError("missing source trait column")
        if r["species"] in names or r["x"] in ids:
            raise ValueError("duplicate taxon or source phylogeny key")
        names.add(r["species"])
        ids.add(r["x"])
    joined=[r for r in rows if r["x"] in phylogeny_tips]
    if not joined:
        raise ValueError("no matched tree-tip taxa")
    excluded=[{"species":r["species"],"x":r["x"]} for r in rows
              if r["x"] not in phylogeny_tips]
    group={reward:{"known_shape":0,"positive":0,"shape_code_0":0,
                   "shape_code_1":0,"shape_code_2":0,
                   "missing_shape":0}
           for reward in REWARDS.values()}
    per_genus={}
    missing_reward=0
    for r in joined:
        reward=reward_group(r["confirmed.reward.type"])
        shape=source_category(r["stamen.shape.dimorphism"])
        if reward is None:
            missing_reward+=1
            continue
        g=group[reward]
        genus=r["species"].split(" ")[0]
        gg=per_genus.setdefault(genus,{})
        ge=gg.setdefault(reward,{"known_shape":0,"positive":0,
                                 "shape_code_0":0,"missing_shape":0})
        if shape is None:
            g["missing_shape"]+=1
            ge["missing_shape"]+=1
            continue
        g["known_shape"]+=1
        g["shape_code_"+r["stamen.shape.dimorphism"]]+=1
        ge["known_shape"]+=1
        if r["stamen.shape.dimorphism"]=="0":
            g["shape_code_0"]+=0  # already recorded above
            ge["shape_code_0"]+=1
        else:
            g["positive"]+=1
            ge["positive"]+=1
    poll=group["pollen"]
    n_not=group["nectar"]["known_shape"]+group["food_body"]["known_shape"]
    pos_not=group["nectar"]["positive"]+group["food_body"]["positive"]
    return {
        "n_source_rows":len(rows),
        "n_distinct_source_species":len(ids),
        "n_phylogeny_joined":len(joined),
        "n_taxa_not_in_tree":len(excluded),
        "taxa_not_in_tree":excluded,
        "n_reward_known_in_tree":sum(g["known_shape"]+g["missing_shape"]
                                    for g in group.values()),
        "n_reward_missing_in_tree":missing_reward,
        "n_reward_and_shape_complete":sum(g["known_shape"] for g in group.values()),
        "known_reward_counts":{k:v["known_shape"] for k,v in group.items()},
        "known_reward_shape_differentiated_counts":{k:v["positive"]
                                                   for k,v in group.items()},
        "reward_shape_code_counts":group,
        "genus_reward_shape":per_genus,
        "all_nonpollen_vs_pollen":{
            "nonpollen_known":n_not,
            "nonpollen_positive":pos_not,
            "pollen_known":poll["known_shape"],
            "pollen_positive":poll["positive"],
            "nonpollen_fraction":pos_not/n_not if n_not else None,
            "pollen_fraction":poll["positive"]/poll["known_shape"] if poll["known_shape"] else None,
            "observed_risk_difference":(
                pos_not/n_not-poll["positive"]/poll["known_shape"]
                if n_not and poll["known_shape"] else None),
        },
        "phylogenetic_transition_events_inferred":False,
        "new_experimental_observations":0,
        "pooled_meta_analysis_performed":False,
        "inference_caveat":(
            "Source stamen.shape.dimorphism codes 0 vs 1/2 are a single floral "
            "shape trait, not all-dimensional heteranthery. Reward labels are "
            "source-based; missing rewards are excluded not treated as pollen. "
            "Species are phylogenetically dependent, reward and shape concentrated "
            "in genera; no independent historical origins, phylogenetic model, "
            "selection mechanism, causal effect or meta-analytic k is estimated. "
            "Data reuse published Dellinger 2019/2021 taxa in the 2024 study."
        )
    }


def analyze_source_zip(raw: bytes) -> dict:
    if hashlib.sha256(raw).hexdigest()!=ZIP_SHA256:
        raise ValueError("source Zenodo zip sha256 mismatch")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        traits=z.read(SOURCE_CSV)
        tree=z.read(SOURCE_TREE)
    if hashlib.sha256(traits).hexdigest()!=CSV_SHA256:
        raise ValueError("source floraltraits.csv sha256 mismatch")
    df=list(csv.DictReader(io.StringIO(traits.decode("utf-8-sig"))))
    newick=tree.decode("utf-8-sig")
    taxa=set(re.findall(r"(?<=[(,])([^():,;]+):",newick))
    result=summarize_records(df,taxa)
    # The original trait table has six taxa that do not match original tree tips.
    if result["n_source_rows"]!=145 or result["n_phylogeny_joined"]!=139:
        raise ValueError("author source/phylogeny alignment drift")
    if result["n_reward_known_in_tree"]!=62:
        raise ValueError("unexpected reward ascertainment drift")
    result["source_doi"]=DOI
    result["source_flora_doi"]="10.1111/nph.17390"
    result["published_heteranthery_doi"]="10.1111/evo.14260"
    result["source_zenodo_record"]=7659158
    result["source_url"]=ZENODO_URL
    result["source_archive_sha256"]=ZIP_SHA256
    result["source_trait_sha256"]=CSV_SHA256
    result["source_tree_sha256"]=hashlib.sha256(tree).hexdigest()
    result["tree_token_count_before_exact_join"]=len(taxa)
    result["source_trait"]="stamen.shape.dimorphism"
    result["source_reward"]="confirmed.reward.type"
    result["reward_coding_provenance"]="Dellinger 2019 NPhyt Table 3: bee=pollen; mixed vertebrate=nectar; passerine=food body"
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-zip",type=Path,required=True)
    p.add_argument("--output",type=Path,default=Path(
        "empirical/trait_architecture_history/dellinger2024_reward_shape_readout.json"))
    args=p.parse_args()
    result=analyze_source_zip(args.source_zip.read_bytes())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
                           encoding="utf8")
    print("BITA_MERIANIEAE_READOUT:"+json.dumps({
        "counts":result["known_reward_counts"],
        "shape_positive":result["known_reward_shape_differentiated_counts"],
        "n_reward_missing_in_tree":result["n_reward_missing_in_tree"],
        "n_phylogeny_joined":result["n_phylogeny_joined"],
        "genus_Meriania":result["genus_reward_shape"].get("Meriania",{}),
        "genus_Axinaea":result["genus_reward_shape"].get("Axinaea",{}),
    },separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
