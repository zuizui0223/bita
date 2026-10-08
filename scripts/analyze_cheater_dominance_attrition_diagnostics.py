#!/usr/bin/env python3
"""Prespecified diagnostics for the cheater-dominance attrition cross-fit.

Implements only diagnostics already frozen in
CHEATER_DOMINANCE_ATTRITION_CROSSFIT_PREREG_V1.md:
1) zero-inclusive opportunity response,
2) mismatch-conditioned residual cross-fit,
3) within-site centered-rank sensitivity.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_zenodo_extension import FILES, _download, _read
from scripts.analyze_aubert2026_participation_route_decomposition import (
    build_opportunity_edges,
)
from scripts.analyze_aubert2026_route_specific_participation_postopen import (
    split_route_counts,
)
from scripts.analyze_cheater_dominance_attrition_crossfit import (
    PRIMARY_MIN_EVENTS,
    PRIMARY_MIN_WAYPOINTS,
    MIN_DIRECTION_PLANTS,
    build_fold_plants,
    build_waypoints,
    directional_rows,
    fisher_mean,
    fold_of_waypoint,
    spearman,
)

@dataclass
class OpportunityFold:
    opportunities: int = 0
    any_feeding: int = 0
    legitimate: int = 0
    robbery: int = 0
    mismatch_sum: float = 0.0

    @property
    def mean_mismatch(self) -> float | None:
        return self.mismatch_sum / self.opportunities if self.opportunities else None


def _rank(values: list[float]) -> list[float]:
    order=sorted(range(len(values)), key=lambda i: values[i])
    ranks=[0.0]*len(values)
    i=0
    while i<len(order):
        j=i+1
        while j<len(order) and values[order[j]]==values[order[i]]:
            j+=1
        r=(i+1+j)/2.0
        for k in range(i,j):
            ranks[order[k]]=r
        i=j
    return ranks


def _pearson(x:list[float], y:list[float]) -> float:
    if len(x)!=len(y) or len(x)<3:
        return float("nan")
    mx=sum(x)/len(x); my=sum(y)/len(y)
    dx=[v-mx for v in x]; dy=[v-my for v in y]
    den=math.sqrt(sum(v*v for v in dx)*sum(v*v for v in dy))
    return sum(a*b for a,b in zip(dx,dy))/den if den>0 else float("nan")


def _residualize(y:list[float], x:list[float]) -> list[float]:
    if len(y)!=len(x) or len(y)<3:
        return []
    mx=sum(x)/len(x); my=sum(y)/len(y)
    den=sum((v-mx)**2 for v in x)
    slope=(sum((a-mx)*(b-my) for a,b in zip(x,y))/den) if den>0 else 0.0
    intercept=my-slope*mx
    return [b-(intercept+slope*a) for a,b in zip(x,y)]


def build_opportunity_groups(interactions,cameras,plants,birds):
    pooled,audit=build_opportunity_edges(interactions,cameras,plants,birds)
    robbery,legitimate,route_audit=split_route_counts(interactions,cameras,plants,birds)
    if not (len(pooled)==len(robbery)==len(legitimate)):
        raise ValueError("opportunity edge sets not aligned")
    out:dict[tuple[str,str],OpportunityFold]={}
    for p,r,l in zip(pooled,robbery,legitimate):
        if (p.waypoint,p.bird,p.plant)!=(r.waypoint,r.bird,r.plant) or (p.waypoint,p.bird,p.plant)!=(l.waypoint,l.bird,l.plant):
            raise ValueError("route edge identities not aligned")
        key=(p.plant,fold_of_waypoint(p.waypoint))
        g=out.setdefault(key,OpportunityFold())
        g.opportunities+=1
        g.any_feeding+=int(p.primary_count>0)
        g.legitimate+=int(l.primary_count>0)
        g.robbery+=int(r.primary_count>0)
        g.mismatch_sum+=float(p.mismatch)
    return out,{"pooled":audit,"route":route_audit}


def zero_inclusive_direction(event_groups, opportunity_groups, predictor_fold, outcome_fold):
    rows=[]
    plants=sorted({p for p,_ in event_groups})
    for plant in plants:
        pred=event_groups.get((plant,predictor_fold))
        event_out=event_groups.get((plant,outcome_fold))
        opp=opportunity_groups.get((plant,outcome_fold))
        if pred is None or event_out is None or opp is None:
            continue
        if len(pred.waypoints)<PRIMARY_MIN_WAYPOINTS or len(event_out.waypoints)<PRIMARY_MIN_WAYPOINTS:
            continue
        if pred.total<PRIMARY_MIN_EVENTS or opp.opportunities<=0:
            continue
        rows.append({
            "plant":plant,
            "share":pred.robbery/pred.total,
            "any":opp.any_feeding/opp.opportunities,
            "legitimate":opp.legitimate/opp.opportunities,
            "robbery":opp.robbery/opp.opportunities,
        })
    x=[r["share"] for r in rows]
    return rows,{
        "n":len(rows),
        "rho_any_opportunity":spearman(x,[r["any"] for r in rows]),
        "rho_legitimate_opportunity":spearman(x,[r["legitimate"] for r in rows]),
        "rho_robbery_opportunity":spearman(x,[r["robbery"] for r in rows]),
    }


def mismatch_conditioned_direction(event_groups, opportunity_groups, predictor_fold, outcome_fold):
    rows=directional_rows(
        event_groups,predictor_fold,outcome_fold,
        min_events=PRIMARY_MIN_EVENTS,
        min_waypoints=PRIMARY_MIN_WAYPOINTS,
    )
    use=[]
    for r in rows:
        p=str(r["plant"])
        mp=opportunity_groups.get((p,predictor_fold))
        mo=opportunity_groups.get((p,outcome_fold))
        if mp is None or mo is None or mp.mean_mismatch is None or mo.mean_mismatch is None:
            continue
        use.append({
            **r,
            "mismatch_predictor":float(mp.mean_mismatch),
            "mismatch_outcome":float(mo.mean_mismatch),
        })
    if len(use)<3:
        return {"n":len(use),"partial_rank_rho":None}
    share_rank=_rank([float(r["share"]) for r in use])
    total_rank=_rank([math.log1p(float(r["total_flux"])) for r in use])
    mp_rank=_rank([float(r["mismatch_predictor"]) for r in use])
    mo_rank=_rank([float(r["mismatch_outcome"]) for r in use])
    res_share=_residualize(share_rank,mp_rank)
    res_total=_residualize(total_rank,mo_rank)
    return {
        "n":len(use),
        "partial_rank_rho":_pearson(res_share,res_total),
        "raw_rho":spearman(
            [float(r["share"]) for r in use],
            [math.log1p(float(r["total_flux"])) for r in use],
        ),
    }


def build_site_fold_plants(interactions,waypoints):
    # Reuse primary event classification at waypoint level, but retain site in the key.
    # Every accepted waypoint has exactly one site/plant identity.
    events:dict[tuple[str,str,str],dict[str,object]]={}
    for wp in waypoints.values():
        key=(wp.site,wp.plant,wp.fold)
        g=events.setdefault(key,{
            "waypoints":set(),"hours":0.0,"robbery":0,"legitimate":0
        })
        g["waypoints"].add(wp.waypoint)
        g["hours"]+=wp.sampling_hours

    from scripts.analyze_cheater_dominance_attrition_crossfit import _is_target,_route_status
    from scripts.audit_aubert2026_participation_denominator import _parse_date,_date_in_any_interval
    for row in interactions:
        waypoint=str(row.get("waypoint","")).strip()
        wp=waypoints.get(waypoint)
        if wp is None or not _is_target(row,"all_target"):
            continue
        d=_parse_date(row.get("date"))
        if d is None or not _date_in_any_interval(d,list(wp.intervals)):
            continue
        if str(row.get("feeding_activity","")).strip().lower()=="no_feeding":
            continue
        route=_route_status(row.get("piercing"),"primary")
        if route not in {"yes","no"}:
            continue
        g=events[(wp.site,wp.plant,wp.fold)]
        g["robbery" if route=="yes" else "legitimate"]+=1
    return events


def site_direction(site_groups,pred_fold,out_fold):
    rows=[]
    keys={(site,plant) for site,plant,_ in site_groups}
    for site,plant in sorted(keys):
        p=site_groups.get((site,plant,pred_fold))
        o=site_groups.get((site,plant,out_fold))
        if p is None or o is None:
            continue
        ptotal=int(p["robbery"])+int(p["legitimate"])
        ototal=int(o["robbery"])+int(o["legitimate"])
        if len(p["waypoints"])<PRIMARY_MIN_WAYPOINTS or len(o["waypoints"])<PRIMARY_MIN_WAYPOINTS:
            continue
        if ptotal<PRIMARY_MIN_EVENTS or float(o["hours"])<=0:
            continue
        rows.append({
            "site":site,"plant":plant,
            "share":int(p["robbery"])/ptotal,
            "flux":ototal/float(o["hours"]),
        })
    by_site=defaultdict(list)
    for r in rows: by_site[r["site"]].append(r)

    xr=[]; yr=[]; eligible_sites=0
    for site,vals in by_site.items():
        if len(vals)<3:
            continue
        xrank=_rank([float(v["share"]) for v in vals])
        yrank=_rank([math.log1p(float(v["flux"])) for v in vals])
        mx=sum(xrank)/len(xrank); my=sum(yrank)/len(yrank)
        xr.extend([v-mx for v in xrank])
        yr.extend([v-my for v in yrank])
        eligible_sites+=1
    return {
        "plant_site_rows":len(rows),
        "eligible_sites_ge3":eligible_sites,
        "pooled_centered_rank_rho":_pearson(xr,yr) if len(xr)>=3 else None,
        "centered_rows":len(xr),
    }


def analyze(interactions,cameras,plants,birds):
    waypoints=build_waypoints(cameras)
    event_groups=build_fold_plants(
        interactions,waypoints,consumer_mode="all_target",route_policy="primary"
    )
    opp_groups,opp_audit=build_opportunity_groups(interactions,cameras,plants,birds)

    _,za=zero_inclusive_direction(event_groups,opp_groups,"A","B")
    _,zb=zero_inclusive_direction(event_groups,opp_groups,"B","A")
    zero_combined={
        "A_to_B":za,
        "B_to_A":zb,
        "rho_X_any_opportunity":fisher_mean(za["rho_any_opportunity"],zb["rho_any_opportunity"]),
        "rho_X_legitimate_opportunity":fisher_mean(za["rho_legitimate_opportunity"],zb["rho_legitimate_opportunity"]),
        "rho_X_robbery_opportunity":fisher_mean(za["rho_robbery_opportunity"],zb["rho_robbery_opportunity"]),
    }

    ma=mismatch_conditioned_direction(event_groups,opp_groups,"A","B")
    mb=mismatch_conditioned_direction(event_groups,opp_groups,"B","A")
    mismatch_combined={
        "A_to_B":ma,
        "B_to_A":mb,
        "rho_X_partial_rank":(
            fisher_mean(ma["partial_rank_rho"],mb["partial_rank_rho"])
            if ma["partial_rank_rho"] is not None and mb["partial_rank_rho"] is not None
            else None
        ),
    }

    site_groups=build_site_fold_plants(interactions,waypoints)
    sa=site_direction(site_groups,"A","B")
    sb=site_direction(site_groups,"B","A")
    site_combined={
        "A_to_B":sa,"B_to_A":sb,
        "rho_X_within_site":(
            fisher_mean(sa["pooled_centered_rank_rho"],sb["pooled_centered_rank_rho"])
            if sa["pooled_centered_rank_rho"] is not None and sb["pooled_centered_rank_rho"] is not None
            else None
        ),
    }

    return {
        "analysis_name":"cheater_dominance_attrition_crossfit_prespecified_diagnostics",
        "status":"FIT",
        "freeze":"empirical/mutualism_attrition/CHEATER_DOMINANCE_ATTRITION_CROSSFIT_PREREG_V1.md",
        "zero_inclusive_opportunity":zero_combined,
        "mismatch_conditioned":mismatch_combined,
        "within_site_centered":site_combined,
        "opportunity_audit":opp_audit,
        "claim_boundary":(
            "Prespecified secondary diagnostics. They cannot replace the weak primary "
            "total-flux cross-fit or alter its permutation p-value."
        ),
    }


def run(output):
    tables={key:_read(_download(name)) for key,name in FILES.items()}
    result=analyze(
        tables["interactions"],tables["cameras"],tables["plants"],tables["birds"]
    )
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("output");args=ap.parse_args()
    print(json.dumps(run(args.output),indent=2,sort_keys=True))
