#!/usr/bin/env python3
"""Exploratory extended-MLE diagnostic for the *unchanged* robbery M2 design.

The original finite-Poisson MLE is on a boundary. This module first finds its
transportation-polytope maximal face and fits the exact 3-category loglinear
model on that face. Each plant-deletion replicate must REDERIVE that face.
This is post-outcome methodological work, not a confirmatory analysis.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import lsqr

REACH = 1.8
DELTA = math.log(1.25)
EXPECTED_SHA256 = {
    "aubert_ephi_participation_opportunities.csv":
        "685f227a2aa2c5c322e18188ba5bd6d44aa67490b31514b9c728e6e033abc14f",
    "aubert_ephi_pair_site_analysis.csv":
        "94c74386d2c304b5816653e79b552a0e79487258c5021f8791c614afdc956afa",
}


def read_records(archive_zip: Path):
    with zipfile.ZipFile(archive_zip) as zf:
        def read(name):
            raw = zf.read("data_archive/" + name)
            if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256[name]:
                raise ValueError("SOURCE_SHA256_DRIFT: " + name)
            return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
        pair = read("aubert_ephi_pair_site_analysis.csv")
        opportunity = read("aubert_ephi_participation_opportunities.csv")

    groups = {}
    for item in pair:
        k, val = item["bird_unit"], item["bird_group"]
        if k in groups and groups[k] != val:
            raise ValueError("BIRD_GROUP_INCONSISTENT")
        groups[k] = val

    records = []
    for item in opportunity:
        bird = item["bird_unit"]
        if bird not in groups:
            raise ValueError("MISSING_BIRD_GROUP")
        if groups[bird] != "hummingbird":
            continue
        n = int(item["robbing_count"])
        legitimate = int(item["legitimate_count"])
        if n + legitimate != int(item["primary_count"]) or min(n, legitimate) < 0:
            raise ValueError("ROUTE_COUNT_NOT_RECONSTRUCTED")
        mismatch = float(item["mismatch_log_t_over_b"]) - math.log(REACH)
        cat = 0 if mismatch <= 0 else (1 if mismatch <= DELTA else 2)
        records.append((item["waypoint_unit"], bird + "@@" + item["site_id"],
                        cat, n, item["plant_unit"]))
    if len(records) != 19903 or len({e[1].split("@@")[0] for e in records}) != 49:
        raise ValueError("HUMMINGBIRD_OPPORTUNITY_POPULATION_DRIFT")
    return records


def supported_margin_system(records, *, exclude_plant=None):
    current = [e for e in records if e[4] != exclude_plant]
    while True:
        row, col = defaultdict(int), defaultdict(int)
        for e in current:
            row[e[0]] += e[3]
            col[e[1]] += e[3]
        filtered = [e for e in current if row[e[0]] > 0 and col[e[1]] > 0]
        if len(filtered) == len(current):
            break
        current = filtered
    if not current:
        raise ValueError("NO_POSITIVE_MARGIN_SUPPORT")
    rn = {key: i for i, key in enumerate(sorted({e[0] for e in current}))}
    cn = {key: i for i, key in enumerate(sorted({e[1] for e in current}))}
    r = np.array([rn[e[0]] for e in current], dtype=np.int32)
    c = np.array([cn[e[1]] for e in current], dtype=np.int32)
    cat = np.array([e[2] for e in current], dtype=np.int32)
    y = np.array([e[3] for e in current], dtype=np.float64)
    return r, c, cat, y, len(rn), len(cn)


def maximal_transport_face(r, c, y, nr, nc):
    """Transport-edge is possible iff positive in a feasible flow, or in a
    strongly connected component of that flow's residual bipartite network."""
    n = len(y)
    i = np.arange(n)
    a = coo_matrix((np.ones(2*n), (np.r_[r, nr+c], np.r_[i, i])),
                   shape=(nr+nc, n)).tocsr()
    margins = np.r_[np.bincount(r, weights=y, minlength=nr),
                    np.bincount(c, weights=y, minlength=nc)]
    solution = linprog(np.zeros(n), A_eq=a, b_eq=margins,
                       bounds=(0, None), method="highs")
    if not solution.success:
        raise RuntimeError("MARGIN_LP_FAILED:" + solution.message)
    flow = solution.x
    positive = flow > 1e-7
    start = np.r_[r, nr+c[positive]]
    end = np.r_[nr+c, r[positive]]
    graph = coo_matrix((np.ones(len(start)), (start, end)),
                       shape=(nr+nc, nr+nc)).tocsr()
    _, component = connected_components(graph, directed=True, connection="strong")
    face = positive | (component[r] == component[nr+c])
    if np.any(y[~face] > 0):
        raise RuntimeError("OBSERVED_POSITIVE_FORCED_TO_ZERO")
    return face


def fit_extended(records, *, exclude_plant=None):
    r, c, category, y, nr, nc = supported_margin_system(
        records, exclude_plant=exclude_plant)
    face = maximal_transport_face(r, c, y, nr, nc)
    forced = int((~face).sum())
    r, c, category, y = r[face], c[face], category[face], y[face]
    rt = np.bincount(r, weights=y, minlength=nr)
    ct = np.bincount(c, weights=y, minlength=nc)
    kt = np.bincount(category, weights=y, minlength=3)
    if np.any(kt <= 0):
        return {"status":"CATEGORY_COUNT_SEPARATED", "forced_zero_cells":forced}

    alpha, gamma, theta = np.ones(nr), np.ones(nc), np.ones(3)
    err = float("inf")
    for iteration in range(1, 10001):
        alpha = rt / np.bincount(r, weights=gamma[c]*theta[category], minlength=nr)
        gamma = ct / np.bincount(c, weights=alpha[r]*theta[category], minlength=nc)
        new = kt / np.bincount(category, weights=alpha[r]*gamma[c], minlength=3)
        alpha *= new[0]
        theta = new / new[0]
        if iteration % 100 == 0 or iteration == 1:
            mean = alpha[r]*gamma[c]*theta[category]
            err = max(
                np.max(np.abs(np.bincount(r,weights=mean,minlength=nr)-rt)/np.maximum(1,rt)),
                np.max(np.abs(np.bincount(c,weights=mean,minlength=nc)-ct)/np.maximum(1,ct)),
                np.max(np.abs(np.bincount(category,weights=mean,minlength=3)-kt)/np.maximum(1,kt)),
            )
            if err < 1e-9:
                break
    if err >= 1e-9:
        return {"status":"NOT_CONVERGED","forced_zero_cells":forced,
                "iterations":iteration,"max_margin_error":float(err)}
    return {
        "status":"FIT",
        "forced_zero_cells":forced,
        "active_cells":int(len(y)),
        "positive_margin_waypoints":nr,
        "positive_margin_bird_sites":nc,
        "iterations":iteration,
        "max_margin_error":float(err),
        "beta_moderate":float(math.log(theta[1])),
        "beta_severe":float(math.log(theta[2])),
        "rate_ratios":{
            "moderate_accessible":float(theta[1]),
            "severe_accessible":float(theta[2]),
            "severe_moderate":float(theta[2]/theta[1]),
        }
    }


def joint_category_rank(records):
    """Test whether both mismatch coefficients survive nuisance FE projection."""
    r,c,k,y,nr,nc = supported_margin_system(records)
    face = maximal_transport_face(r,c,y,nr,nc)
    r,c,k = r[face],c[face],k[face]
    n=len(r)
    i=np.arange(n)
    nuisance=coo_matrix((np.ones(2*n),(np.r_[i,i],np.r_[r,nr+c])),
                         shape=(n,nr+nc)).tocsr()
    X=np.column_stack([(k==1).astype(float),(k==2).astype(float)])
    residual=np.column_stack([
        X[:,j]-nuisance@lsqr(nuisance,X[:,j],atol=1e-12,btol=1e-12,iter_lim=5000)[0]
        for j in range(2)
    ])
    singular=np.linalg.svd(residual,compute_uv=False)
    return {"joint_contrast_rank":int(sum(singular>1e-7)),
            "residualized_singular_values":list(map(float,singular))}


def run(path,output):
    records=read_records(path)
    full=fit_extended(records)
    if full["status"]!="FIT":
        raise RuntimeError("EXTENDED_FULL_FIT_FAILED:"+full["status"])
    ranks=joint_category_rank(records)
    if ranks["joint_contrast_rank"]!=2:
        raise RuntimeError("MISMATCH_CONTRASTS_NOT_JOINTLY_IDENTIFIABLE")

    plants=sorted({e[4] for e in records})
    fits=[(p,fit_extended(records,exclude_plant=p)) for p in plants]
    failed=[{"plant":p,**fit} for p,fit in fits if fit["status"]!="FIT"]
    valid=[fit for _,fit in fits if fit["status"]=="FIT"]
    if len(valid)!=len(plants):
        raise RuntimeError("PLANT_DELETE_ONE_FIT_NOT_COMPLETE:" + repr(failed[:5]))
    forced=np.array([f["forced_zero_cells"] for f in valid])
    contrasts={}
    for name, mapping in (
        ("moderate_accessible", lambda f: f["beta_moderate"]),
        ("severe_accessible", lambda f: f["beta_severe"]),
        ("severe_moderate",lambda f: f["beta_severe"]-f["beta_moderate"]),
    ):
        rep=np.array([mapping(f) for f in valid])
        ref=math.log(full["rate_ratios"][name])
        n=len(rep)
        se=math.sqrt(float((n-1)/n * np.sum((rep-rep.mean())**2)))
        contrasts[name]={
            "rate_ratio":float(math.exp(ref)),
            "jackknife_se_log":se,
            "ci95":[float(math.exp(ref-1.96*se)),float(math.exp(ref+1.96*se))],
            "successful_plant_deletions":n,
            "leave_one_fraction_below_one":float(np.mean(rep<0)),
            "leave_one_min_rr":float(math.exp(float(rep.min()))),
            "leave_one_max_rr":float(math.exp(float(rep.max()))),
        }
    result={
        "analysis":"POST_OUTCOME_EXPLORATORY_EXTENDED_POISSON_MLE",
        "source":"BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V4",
        "source_artifact_id":11293379572,
        "source_sha256":EXPECTED_SHA256,
        "hummingbird_zero_inclusive_opportunities":len(records),
        "plants":len(plants),
        "full_fit":full,
        "mismatch_identifiability":ranks,
        "plant_jackknife":{
            "complete":True,
            "successful_replicates":len(valid),
            "forced_zero_cell_count":{"min":int(forced.min()),"median":float(np.median(forced)),
                                      "max":int(forced.max())},
            "contrasts":contrasts,
        },
        "claim_boundary":(
            "This repairs nuisance boundary separation only in a post-outcome exploratory "
            "extended likelihood. Intervals are plant-jackknife sensitivity, not "
            "confirmatory evidence; pair-level sorting, reward and observation confounding "
            "remain. The original finite-MLE test remains NOT_FIT."
        ),
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "full":full, "rank":ranks,
        "jackknife":{"n":len(valid),"forced":result["plant_jackknife"]["forced_zero_cell_count"],
                     "contrasts":contrasts},
    },indent=2))
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("source_zip",type=Path)
    parser.add_argument("output_json",type=Path)
    args=parser.parse_args()
    run(args.source_zip,args.output_json)
