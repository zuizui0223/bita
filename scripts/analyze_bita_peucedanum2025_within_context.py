"""Observational within-context tests for Kudo & Shibata (2025) raw data.

This is explicitly exploratory. It compares allocation and egg-laying within
plot×year, controlling for display size and floral height. It does NOT identify
the causal advantage, developmental startup cost, or evolution of flower classes.
All original input rows remain off the BITA repository and downloadable report.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

from scripts.audit_bita_peucedanum2025_huscap import fetch
from scripts.inspect_bita_peucedanum2025_raw import checked_csvs, number

SEED = 20261019
NULL = None


def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n=len(vector)
    aug=[list(matrix[i])+[vector[i]] for i in range(n)]
    for j in range(n):
        pivot=max(range(j,n),key=lambda k:abs(aug[k][j]))
        if abs(aug[pivot][j])<=1e-11:
            raise ValueError("ILL_CONDITIONED_FIT")
        aug[j],aug[pivot]=aug[pivot],aug[j]
        fac=aug[j][j]
        for k in range(j,n+1):
            aug[j][k]/=fac
        for i in range(n):
            if i==j:
                continue
            weight=aug[i][j]
            for k in range(j,n+1):
                aug[i][k]-=weight*aug[j][k]
    return [aug[i][n] for i in range(n)]


def covariate_projection(cols: list[list[float]], y: list[float]) -> list[float]:
    p=len(cols[0])
    gram=[[sum(row[j]*row[k] for row in cols) for k in range(p)]
          for j in range(p)]
    rhs=[sum(row[j]*z for row,z in zip(cols,y)) for j in range(p)]
    return solve(gram,rhs)


def fwl(data: list[dict], *, permutations: int = 4999,
        seed: int = SEED) -> dict:
    """Freedman-Lane residual permutation within declared observation blocks.

    Response, predictor and controls are demeaned within group. Freedman-Lane
    residual permutations preserve group membership but do NOT guarantee
    exchangeability under heteroskedastic count outcomes.
    """
    if len(data)<20 or permutations<1:
        raise ValueError("INSUFFICIENT_ROWS")
    members=defaultdict(list)
    for i,row in enumerate(data):
        members[row["group"]].append(i)
    if any(len(ids)<3 for ids in members.values()):
        raise ValueError("INSUFFICIENT_WITHIN_GROUP_REPLICATION")
    names=("x","y","log_total","height")
    centered={name:[0.0]*len(data) for name in names}
    for idx in members.values():
        for name in names:
            mean=statistics.fmean(data[i][name] for i in idx)
            for i in idx:
                centered[name][i]=data[i][name]-mean
    C=list(zip(centered["log_total"],centered["height"]))
    C=[list(r) for r in C]
    beta_x_controls=covariate_projection(C,centered["x"])
    beta_y_controls=covariate_projection(C,centered["y"])
    rx=[v-sum(a*b for a,b in zip(row,beta_x_controls))
        for v,row in zip(centered["x"],C)]
    ry=[v-sum(a*b for a,b in zip(row,beta_y_controls))
        for v,row in zip(centered["y"],C)]
    den=sum(v*v for v in rx)
    if den<=1e-10:
        raise ValueError("NO_WITHIN_CONTEXT_ALLOCATION_VARIATION")
    obs=sum(x*y for x,y in zip(rx,ry))/den
    rng=random.Random(seed)
    exceed=0
    for _ in range(permutations):
        shuffled=ry.copy()
        for ids in members.values():
            vals=[shuffled[i] for i in ids]
            rng.shuffle(vals)
            for i,z in zip(ids,vals):
                shuffled[i]=z
        nul=sum(x*y for x,y in zip(rx,shuffled))/den
        if abs(nul)>=abs(obs)-1e-12:
            exceed+=1
    xsd=math.sqrt(sum(v*v for v in rx)/(len(data)-1))
    return {
        "n_individuals":len(data),
        "n_context_groups":len(members),
        "within_context_allocation_beta":obs,
        "effect_per_10pp_male_share":obs*.1,
        "beta_per_1sd_residual_allocation":obs*xsd,
        "two_sided_within_context_residual_permutation_p":(exceed+1)/(permutations+1),
        "permutations":permutations,
        "response_transformation":"outcome-specific as declared in receipt",
        "notes":"Within-group fixed-effect transformed OLS with log(total flowers) and height covariates; exploratory conditional association, not a causal treatment effect or Poisson model.",
    }


def make_population_rows(rows: list[dict], response: str) -> tuple[list[dict],int]:
    valid=[]
    excluded=0
    for r in rows:
        h,m=number(r["HflowerN"]),number(r["MflowerN"])
        height=number(r["Height"])
        v=number(r["OvipN"] if response=="ovip" else r["PredationR"])
        if (h is None or m is None or h+m<=0 or height is None
                or v is None or v<0 or (response=="predation" and v>1)):
            excluded+=1
            continue
        valid.append({
            "group":r["Year"]+"/"+r["Plot"],"plot":r["Plot"],
            "x":m/(m+h),
            "y":math.log1p(v) if response=="ovip" else v,
            "log_total":math.log1p(m+h),
            "height":height,
        })
    return valid,excluded


def make_paternity_rows(rows: list[dict]) -> tuple[list[dict],int]:
    out=[]
    omitted=0
    for r in rows:
        h,m=number(r["HFlowerNo"]),number(r["MFlowerNo"])
        height=number(r["Height"])
        size=number(r["TotalFlowerNo"])
        seeds=number(r["SiredSeedNo"])
        if (h is None or m is None or h+m<=0 or height is None
                or size is None or size<=0 or seeds is None or seeds<0):
            omitted+=1
            continue
        out.append({
            "group":"HA_PLOT","plot":"HA",
            "x":m/(h+m),
            "y":math.log1p(seeds),
            "log_total":math.log1p(size),
            "height":height,
        })
    return out,omitted


def analyze(blob: bytes) -> dict:
    data=checked_csvs(blob)
    results={}
    for name in ("ovip","predation"):
        x,missing=make_population_rows(data["population"],name)
        test=fwl(x)
        test["outcome"]=(
            "log1p(predator_egg_count)" if name=="ovip"
            else "observed_predation_fraction"
        )
        test["n_excluded_missing_or_invalid"]=missing
        sensitivity={}
        for plot in sorted({r["plot"] for r in x}):
            subset=[r for r in x if r["plot"]!=plot]
            try:
                sensitivity[plot]=fwl(subset,permutations=199,seed=SEED)[
                    "within_context_allocation_beta"]
            except ValueError:
                sensitivity[plot]=None
        test["leave_one_geographic_plot_out_betas"]=sensitivity
        results[name]=test
    pat,pat_missing=make_paternity_rows(data["paternity"])
    p=fwl(pat)
    p["outcome"]="log1p(paternity_assigned_sired_seed_count)"
    p["n_excluded_missing_or_invalid"]=pat_missing
    results["paternity"]=p
    return {
        "analysis":"BITA_PEUCEDANUM2025_WITHIN_CONTEXT_ALLOC_V1",
        "data_level":"SOURCE_SHA256_VERIFIED_PUBLIC_OBSERVATIONAL_DATA",
        "doi":"10.14943/hu95572",
        "primary_hypothesis":"Within a plot×year, higher allocation to male-only flowers is associated with lower antagonist egg count at fixed total display and flower height.",
        "models":results,
        "raw_rows_redistributed":False,
        "claim_limit":(
            "Post-open observational within-plot/year regression. Each outcome "
            "uses nonmissing cases; predation missingness is substantial and "
            "potentially nonrandom. Exchangeability for residual permutation "
            "is not assured. Flower-sex allocation is not randomized. "
            "A null male-fitness association cannot establish equivalence; "
            "none of this estimates BITA's developmental startup K(u), "
            "common-fitness architecture advantage or heritable change."
        ),
    }


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,default=Path(
        "artifacts/bita_peucedanum2025_within_context_v1.json"))
    args=ap.parse_args()
    result=analyze(fetch())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",
                           encoding="utf-8")
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__":
    main()
