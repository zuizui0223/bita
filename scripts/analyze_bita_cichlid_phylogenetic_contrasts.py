"""Phylogenetic independent-contrast extension of BITA's cichlid reality check.

Public data: original Conith & Albertson (2021) oral + pharyngeal jaw PCs
(n=88 species) and the authors' accompanying large time-scaled Newick tree.
The source Git commit, three Git blob SHA1 hashes and file lengths are pinned.

Hypothesis tested: do independently evolving jaw modules retain correlated
evolutionary shape contrasts after tree-based Brownian standardization?
This is NOT proof that the two jaw modules evolved via the BITA trait
architecture fitness advantage, not a test of historic jaw origin, and
not a measurement of K(u), genetic accessibility or specialized fitness.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import math
import random
import urllib.request
from pathlib import Path

from scripts.analyze_bita_cichlid_public_integration import (
    INPUTS, SOURCE_COMMIT, SOURCE_REPOSITORY,
    fetch_source, join_inputs, load_rows, rv_coefficient,
)

TREE = {
    "path": "MacroevolutionSetUp/CichlidTreeNature2020.tre",
    "bytes": 76749,
    "blob_sha1": "23076ac2c895a92aaf36cebfa059124ec1139bd7",
}
N_TAXA = 88
PERMUTATIONS = 4999
SEED = 20261019


@dataclasses.dataclass
class Node:
    name: str
    length: float
    children: list["Node"]


def parse_newick(value: str) -> Node:
    """Read a conservative plain Newick (no quoted labels/comments).

    The pinned source does not require a third-party tree parser. Reject
    unexpected syntax and malformed branch lengths, not just bad tip joins.
    """
    s = value.strip()
    pos = 0
    def token() -> str:
        nonlocal pos
        begin = pos
        while pos < len(s) and s[pos] not in ":,();":
            pos += 1
        return s[begin:pos].strip()

    def subtree() -> Node:
        nonlocal pos
        children = []
        if pos < len(s) and s[pos] == "(":
            pos += 1
            children.append(subtree())
            while pos < len(s) and s[pos] == ",":
                pos += 1
                children.append(subtree())
            if pos >= len(s) or s[pos] != ")":
                raise ValueError("NEWICK_MISSING_PARENTHESIS")
            pos += 1
        name = token()
        if not children and not name:
            raise ValueError("NEWICK_EMPTY_LEAF")
        length = 0.0
        if pos < len(s) and s[pos] == ":":
            pos += 1
            raw = token()
            try:
                length = float(raw)
            except ValueError as exc:
                raise ValueError("NEWICK_INVALID_BRANCH") from exc
            if not math.isfinite(length) or length < 0:
                raise ValueError("NEWICK_INVALID_BRANCH")
        return Node(name, length, children)

    root = subtree()
    if pos >= len(s) or s[pos] != ";" or s[pos+1:].strip():
        raise ValueError("NEWICK_TRAILING_OR_MISSING_SEMICOLON")
    seen = set()
    def check(node):
        if not node.children:
            if node.name in seen:
                raise ValueError("NEWICK_DUPLICATE_TIP")
            seen.add(node.name)
        else:
            for child in node.children:
                check(child)
    check(root)
    return root


def tips(root: Node) -> set[str]:
    if not root.children:
        return {root.name}
    out = set()
    for child in root.children:
        out.update(tips(child))
    return out


def prune(root: Node, accepted: set[str]) -> Node:
    """Collapse unsampled subtrees while summing skipped branch lengths."""
    if not root.children:
        if root.name not in accepted:
            raise ValueError("CALL_PRUNE_WITH_COMPLETE_TIP_SET")
        return Node(root.name, root.length, [])
    def restrict(node: Node) -> Node | None:
        if not node.children:
            return Node(node.name, node.length, []) if node.name in accepted else None
        children = [z for c in node.children if (z:=restrict(c)) is not None]
        if not children:
            return None
        if len(children) == 1:
            one = children[0]
            return Node(one.name, one.length+node.length, one.children)
        return Node(node.name, node.length, children)
    missing = accepted - tips(root)
    if missing:
        raise ValueError(f"PHYLOGENY_MISSING_{len(missing)}_REQUIRED_SPECIES")
    result = restrict(root)
    if result is None or tips(result) != accepted:
        raise ValueError("PHYLOGENY_PRUNED_TIP_MISMATCH")
    return result


def contrasts(tree: Node, data: dict[str,list[float]]) -> list[list[float]]:
    """Standardized Felsenstein PIC under an assumed Brownian tree.

    A child's propagated variance includes the branch to its parent. At a
    binary fork, contrast is (state_a-state_b)/sqrt(var_a+var_b).
    """
    p = len(next(iter(data.values())))
    all_rows = []
    def recurse(node: Node) -> tuple[list[float], float]:
        if not node.children:
            if node.name not in data:
                raise ValueError("UNMATCHED_PHYLOGENY_TIP")
            return list(data[node.name]),node.length
        if len(node.children) != 2:
            raise ValueError("PHYLOGENY_NONBINARY_AFTER_PRUNING")
        (a,va),(b,vb) = [recurse(child) for child in node.children]
        total = va+vb
        if total <= 0 or not math.isfinite(total):
            raise ValueError("DEGENERATE_PHYLOGENETIC_CONTRAST_VARIANCE")
        all_rows.append([(x-y)/math.sqrt(total) for x,y in zip(a,b)])
        centre = [(x*vb+y*va)/total for x,y in zip(a,b)]
        # Root length does not enter a contrast, but child propagated
        # uncertainty does. Reject zero-length divisions at every fork.
        return centre, node.length+va*vb/total

    recurse(tree)
    if len(all_rows) != len(data)-1 or any(len(row)!=p for row in all_rows):
        raise ValueError("PHYLOGENY_CONTRAST_COUNT_OR_DIMENSION_MISMATCH")
    return all_rows


def standardize_rows(rows: list[list[float]], ncols: int) -> list[list[float]]:
    """Center/scale each PIC axis, retaining their joint row pairing."""
    n=len(rows)
    if n<5:
        raise ValueError("NOT_ENOUGH_INDEPENDENT_CONTRAST_ROWS")
    out=[r[:ncols].copy() for r in rows]
    for j in range(ncols):
        mean=sum(r[j] for r in out)/n
        sd=math.sqrt(sum((r[j]-mean)**2 for r in out)/(n-1))
        if sd<=0 or not math.isfinite(sd):
            raise ValueError("UNINFORMATIVE_PIC_AXIS")
        for row in out:
            row[j]=(row[j]-mean)/sd
    return out


def permuted_pic_rv(oral: list[list[float]], pharyngeal: list[list[float]],
                    axes: int, permutations: int=PERMUTATIONS, seed: int=SEED) -> dict:
    """Permute pharyngeal *PIC row vectors* under Brownian exchangeability.

    One-sided test of positive RV magnitude. Null requires correctly
    specified tree/branch lengths and exchangeable standardized contrasts.
    """
    if permutations < 1:
        raise ValueError("NO_PERMUTATIONS")
    x=standardize_rows(oral,axes)
    y=standardize_rows(pharyngeal,axes)
    observed=rv_coefficient(x,y)
    randomizer=random.Random(seed)
    order=list(range(len(x)))
    null=[]
    exceed=0
    for _ in range(permutations):
        randomizer.shuffle(order)
        value=rv_coefficient(x,[y[i] for i in order])
        null.append(value)
        if value>=observed-1e-12:
            exceed+=1
    null.sort()
    return {
        "n_independent_contrasts":len(x),
        "pc_axes_per_module":axes,
        "rv_pic":observed,
        "permutations":permutations,
        "permutation_p":(exceed+1)/(permutations+1),
        "null_rv_mean":sum(null)/permutations,
        "null_rv_q95":null[int(.95*permutations)],
    }


def source_tree_url() -> str:
    return ("https://raw.githubusercontent.com/"+SOURCE_REPOSITORY+"/"
            +SOURCE_COMMIT+"/"+TREE["path"])


def fetch_tree() -> str:
    url=source_tree_url()
    request=urllib.request.Request(
        url,headers={"User-Agent":"BITA-cichlid-public-PIC/1.0"},
    )
    with urllib.request.urlopen(request,timeout=40) as resp:
        raw=resp.read(TREE["bytes"]+1)
    if len(raw)!=TREE["bytes"]:
        raise ValueError("PINNED_PHYLOGENY_BYTE_LENGTH_DRIFT")
    signature=hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii")+raw
    ).hexdigest()
    if signature!=TREE["blob_sha1"]:
        raise ValueError("PINNED_PHYLOGENY_GIT_BLOB_SHA1_DRIFT")
    return raw.decode("utf-8")



def alter_branch_model(tree: Node, model: str) -> Node:
    """Post-open sensitivity: tree topology alone or amplified terminal change.

    This changes the *assumed* branch variance model, not any observed
    anatomical measurements. It is not a fitted optimum branch-length model.
    """
    if model not in {"equal_edge_lengths", "double_terminal_lengths"}:
        raise ValueError("UNREGISTERED_PHYLOGENETIC_VARIANCE_SENSITIVITY")
    def clone(node: Node, *, root: bool=False) -> Node:
        children=[clone(ch) for ch in node.children]
        length=node.length
        if not root:
            if model=="equal_edge_lengths":
                length=1.0
            elif not children:
                length*=2.0
        return Node(node.name,length,children)
    return clone(tree,root=True)



def analyze(oral_data: bytes, pharyngeal_data: bytes, tree_string: str) -> dict:
    oral=load_rows("oral",oral_data)
    phar=load_rows("pharyngeal",pharyngeal_data)
    pairs=join_inputs(oral,phar)
    if len(pairs)!=N_TAXA:
        raise ValueError("UNEXPECTED_REAL_SOURCE_SAMPLE")
    root=parse_newick(tree_string)
    full_tip_count=len(tips(root))
    ids={r["TaxaID"] for r in oral}
    reduced=prune(root,ids)
    source_oral={r["TaxaID"]:r["pc"] for r in oral}
    source_phar={r["TaxaID"]:r["pc"] for r in phar}
    contrasts_oj=contrasts(reduced,source_oral)
    contrasts_pj=contrasts(reduced,source_phar)
    sensitivity=[]
    for model in ("equal_edge_lengths","double_terminal_lengths"):
        alternative=alter_branch_model(reduced,model)
        changed_oral=contrasts(alternative,source_oral)
        changed_phar=contrasts(alternative,source_phar)
        result=permuted_pic_rv(changed_oral,changed_phar,axes=5)
        result["branch_variance_model"]=model
        result["post_open"]=True
        sensitivity.append(result)
    return {
        "receipt_schema":"BITA_CICHLID_PHYLOGENETIC_CONTRASTS_V1",
        "data_level":"REAL_PUBLIC_PINNED_SOURCE_EVOLUTIONARY_COVARIANCE",
        "paper_doi":"10.1038/s41467-021-25755-5",
        "source_repository":SOURCE_REPOSITORY,
        "source_commit":SOURCE_COMMIT,
        "source_trait_blob_sha1s":{k:v["blob_sha1"] for k,v in INPUTS.items()},
        "source_tree_blob_sha1":TREE["blob_sha1"],
        "source_tree_tips":full_tip_count,
        "matched_species":len(ids),
        "n_pruned_contrasts":len(contrasts_oj),
        "methods":"Felsenstein independent contrasts with original source tree branches; PC axes recomputed as contrasts from separately published module PC scores; axis-standardized RV; 4999 whole-contrast label permutations under Brownian contrast exchangeability",
        "results":[permuted_pic_rv(contrasts_oj,contrasts_pj,axes=k) for k in (5,3)],
        "post_open_branch_length_sensitivity":sensitivity,
        "raw_source_files_redistributed":False,
        "phylogenetic_assumptions":(
            "Tree, branch lengths, Brownian covariance, absence of relevant "
            "undermodelled directional trends and exchangeability of contrast "
            "vectors under the null are assumptions; original authors' "
            "shape-landmark phylo.integration estimate is a different estimator. "
            "Equal-edge and doubled-terminal results are post-open branch-variance "
            "sensitivities, not biological hypotheses measured independently."
        ),
        "claim_ceiling":(
            "Tree-adjusted cross-module jaw-shape covariation is not a measure "
            "of ecological tradeoff strength, ontogenetic/genetic constraint, "
            "causal diet selection, functionally optimal morphology, historical "
            "origin of separate jaws, BITA K(u), or evolutionary accessibility. "
            "All 88 taxa belong to one fish radiation, not 88 independent "
            "origins of modularization."
        ),
    }


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,default=Path(
        "artifacts/bita_cichlid_phylogenetic_contrasts_v1.json",
    ))
    args=ap.parse_args()
    result=analyze(fetch_source("oral"),fetch_source("pharyngeal"),fetch_tree())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__":
    main()
