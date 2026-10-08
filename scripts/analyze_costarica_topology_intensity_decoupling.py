#!/usr/bin/env python3
"""Independent Costa Rica validation of cheating topology-intensity decoupling.

Frozen before Costa Rica outcome in:
empirical/mutualism_attrition/COSTARICA_TOPOLOGY_INTENSITY_DECOUPLING_PREREG_V1.md
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_zenodo_extension import _as_float, _download, _read
from scripts.audit_aubert2026_participation_denominator import (
    _camera_is_clean,
    _date_in_any_interval,
    _parse_date,
    _primary_route_status,
)
from scripts.analyze_cheater_dominance_attrition_crossfit import (
    FoldPlant,
    build_fold_plants,
    build_waypoints,
    fisher_mean,
    fold_of_waypoint,
    spearman,
)

FILES_CR = {
    "interactions": "Interactions_data_Costa-Rica.txt",
    "cameras": "Cameras_data_Costa-Rica.txt",
    "plants": "Plant_traits.txt",
    "birds": "Hummingbird_traits.txt",
}

SEED = 20261008
PERMUTATIONS = 99_999
BOOTSTRAPS = 9_999
PRIMARY_MIN_EVENTS = 5
PRIMARY_MIN_WAYPOINTS = 2
MIN_DIRECTION_PLANTS = 20


@dataclass
class OppFold:
    opportunities: int = 0
    positive: int = 0


def _mean(values):
    return sum(values) / len(values)


def _rank(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        r = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = r
        i = j
    return ranks


def _pearson(x, y):
    if len(x) != len(y) or len(x) < 3:
        return float("nan")
    mx = _mean(x); my = _mean(y)
    dx = [v - mx for v in x]; dy = [v - my for v in y]
    den = math.sqrt(sum(v*v for v in dx) * sum(v*v for v in dy))
    return sum(a*b for a,b in zip(dx,dy)) / den if den > 0 else float("nan")


def _atanh_clip(r):
    e = 1e-12
    return math.atanh(max(-1+e, min(1-e, r)))


def _is_hummingbird(row):
    return (
        str(row.get("hummingbird_species", "")).strip() != ""
        and str(row.get("hummingbird_family", "")).strip() == "Trochilidae"
    )


def build_cr_opportunity_groups(interactions, cameras, plants, birds):
    waypoints = build_waypoints(cameras)
    cr_sites = {w.site for w in waypoints.values()}

    plant_by_site = defaultdict(list)
    plant_global = defaultdict(list)
    for row in plants:
        species = str(row.get("plant_species", "")).strip()
        site = str(row.get("site", "")).strip()
        country = str(row.get("Country", "")).strip().lower().replace("-", " ")
        tube = _as_float(row.get("Tubelength"))
        if not species or tube is None or tube <= 0:
            continue
        in_cr = site in cr_sites or country == "costa rica"
        if not in_cr:
            continue
        plant_global[species].append(float(tube))
        if site in cr_sites:
            plant_by_site[(site, species)].append(float(tube))

    bird_values = defaultdict(list)
    for row in birds:
        species = str(row.get("hummingbird_species", "")).strip()
        culmen = _as_float(row.get("culmen_length"))
        if species and culmen is not None and culmen > 0:
            bird_values[species].append(float(culmen))

    by_site = defaultdict(list)
    by_wp_bird = defaultdict(list)
    for row in interactions:
        wp_id = str(row.get("waypoint", "")).strip()
        wp = waypoints.get(wp_id)
        if wp is None or not _is_hummingbird(row):
            continue
        d = _parse_date(row.get("date"))
        if d is None or not _date_in_any_interval(d, list(wp.intervals)):
            continue
        species = str(row.get("hummingbird_species", "")).strip()
        route = _primary_route_status(row.get("piercing"))
        feeding = str(row.get("feeding_activity", "")).strip().lower()
        obs = {
            "species": species,
            "date": d,
            "route": route,
            "feeding": feeding,
        }
        by_site[wp.site].append(obs)
        by_wp_bird[(wp_id, species)].append(obs)

    groups = defaultdict(OppFold)
    site_groups = defaultdict(OppFold)
    edges = 0
    positive_edges = 0
    used_waypoints = set()
    birds_used = set()
    plants_used = set()

    for wp in waypoints.values():
        local_birds = {
            str(obs["species"])
            for obs in by_site.get(wp.site, [])
            if _date_in_any_interval(obs["date"], list(wp.intervals))
        }
        tube_vals = plant_by_site.get((wp.site, wp.plant)) or plant_global.get(wp.plant)
        if not tube_vals:
            continue
        tube = _mean(tube_vals)
        if tube <= 0:
            continue
        for bird in local_birds:
            bills = bird_values.get(bird)
            if not bills:
                continue
            bill = _mean(bills) / 10.0
            if bill <= 0:
                continue
            focal = by_wp_bird.get((wp.waypoint, bird), [])
            count = sum(
                1
                for obs in focal
                if obs["feeding"] != "no_feeding" and obs["route"] in {"yes", "no"}
            )
            positive = int(count > 0)
            key = (wp.plant, wp.fold)
            groups[key].opportunities += 1
            groups[key].positive += positive
            skey = (wp.site, wp.plant, wp.fold)
            site_groups[skey].opportunities += 1
            site_groups[skey].positive += positive
            edges += 1
            positive_edges += positive
            used_waypoints.add(wp.waypoint)
            birds_used.add(bird)
            plants_used.add(wp.plant)

    audit = {
        "clean_waypoints": len(waypoints),
        "trait_matched_opportunity_edges": edges,
        "positive_opportunity_edges": positive_edges,
        "zero_opportunity_edges": edges - positive_edges,
        "waypoints_with_trait_matched_opportunity": len(used_waypoints),
        "bird_species": len(birds_used),
        "plant_species": len(plants_used),
        "sites": len(cr_sites),
    }
    return groups, site_groups, audit


def direction_rows(event_groups, opp_groups, pred_fold, out_fold, min_events=5, min_waypoints=2):
    rows = []
    for plant in sorted({p for p,_ in event_groups}):
        pred = event_groups.get((plant,pred_fold))
        out = event_groups.get((plant,out_fold))
        opp = opp_groups.get((plant,out_fold))
        if pred is None or out is None or opp is None:
            continue
        if len(pred.waypoints) < min_waypoints or len(out.waypoints) < min_waypoints:
            continue
        if pred.total < min_events or out.sampling_hours <= 0 or opp.opportunities <= 0:
            continue
        rows.append({
            "plant": plant,
            "share": pred.robbery / pred.total,
            "occupancy": opp.positive / opp.opportunities,
            "flux": out.total / out.sampling_hours,
            "legitimate_flux": out.legitimate / out.sampling_hours,
            "robbery_flux": out.robbery / out.sampling_hours,
        })
    return rows


def summarize_direction(rows):
    x = [float(r["share"]) for r in rows]
    return {
        "n": len(rows),
        "rho_occupancy": spearman(x,[float(r["occupancy"]) for r in rows]),
        "rho_flux": spearman(x,[math.log1p(float(r["flux"])) for r in rows]),
        "rho_legitimate_flux": spearman(x,[math.log1p(float(r["legitimate_flux"])) for r in rows]),
        "rho_robbery_flux": spearman(x,[math.log1p(float(r["robbery_flux"])) for r in rows]),
    }


def combined(rows_ab, rows_ba):
    a = summarize_direction(rows_ab); b = summarize_direction(rows_ba)
    if len(rows_ab) < 3 or len(rows_ba) < 3:
        return {"A_to_B":a,"B_to_A":b}
    rho_o = fisher_mean(a["rho_occupancy"],b["rho_occupancy"])
    rho_f = fisher_mean(a["rho_flux"],b["rho_flux"])
    z_o = (_atanh_clip(a["rho_occupancy"]) + _atanh_clip(b["rho_occupancy"])) / 2
    z_f = (_atanh_clip(a["rho_flux"]) + _atanh_clip(b["rho_flux"])) / 2
    return {
        "A_to_B":a,"B_to_A":b,
        "rho_OX":rho_o,
        "rho_FX":rho_f,
        "rho_legitimate_X":fisher_mean(a["rho_legitimate_flux"],b["rho_legitimate_flux"]),
        "rho_robbery_X":fisher_mean(a["rho_robbery_flux"],b["rho_robbery_flux"]),
        "D_fisher_z":z_o-z_f,
    }


def permutation_test(rows_ab, rows_ba, permutations=PERMUTATIONS, seed=SEED):
    if len(rows_ab) < MIN_DIRECTION_PLANTS or len(rows_ba) < MIN_DIRECTION_PLANTS:
        return {"status":"INSUFFICIENT_DIRECTIONAL_PLANTS"}

    def vecs(rows):
        return (
            _rank([float(r["share"]) for r in rows]),
            _rank([float(r["occupancy"]) for r in rows]),
            _rank([math.log1p(float(r["flux"])) for r in rows]),
        )
    xa,oa,fa = vecs(rows_ab); xb,ob,fb = vecs(rows_ba)
    def stats(xa,xb):
        roa=_pearson(xa,oa); rob=_pearson(xb,ob)
        rfa=_pearson(xa,fa); rfb=_pearson(xb,fb)
        zo=(_atanh_clip(roa)+_atanh_clip(rob))/2
        zf=(_atanh_clip(rfa)+_atanh_clip(rfb))/2
        return math.tanh(zo), math.tanh(zf), zo-zf
    obs_o,obs_f,obs_d=stats(xa,xb)

    rng=random.Random(seed)
    po=pf=pd=0
    pa=list(xa); pb=list(xb)
    for _ in range(permutations):
        rng.shuffle(pa); rng.shuffle(pb)
        ro,rf,d=stats(pa,pb)
        if ro >= obs_o - 1e-15: po += 1
        if rf <= obs_f + 1e-15: pf += 1
        if d >= obs_d - 1e-15: pd += 1
    return {
        "status":"FIT",
        "rho_OX":obs_o,"rho_FX":obs_f,"D_fisher_z":obs_d,
        "p_occupancy_greater":(po+1)/(permutations+1),
        "p_flux_lower":(pf+1)/(permutations+1),
        "p_D_greater":(pd+1)/(permutations+1),
        "permutations":permutations,
    }


def bootstrap(rows_ab,rows_ba,n=BOOTSTRAPS,seed=SEED+1):
    ma={str(r["plant"]):r for r in rows_ab}
    mb={str(r["plant"]):r for r in rows_ba}
    universe=sorted(set(ma)|set(mb))
    rng=random.Random(seed)
    os=[];fs=[];ds=[]
    for _ in range(n):
        sample=[rng.choice(universe) for _ in universe]
        a=[ma[p] for p in sample if p in ma]
        b=[mb[p] for p in sample if p in mb]
        if len(a)<3 or len(b)<3: continue
        c=combined(a,b)
        ro=float(c["rho_OX"]); rf=float(c["rho_FX"]); d=float(c["D_fisher_z"])
        if all(math.isfinite(v) for v in [ro,rf,d]):
            os.append(ro);fs.append(rf);ds.append(d)
    def ci(vals):
        vals=sorted(vals)
        if not vals:return None
        return [vals[int(math.floor(.025*(len(vals)-1)))],vals[int(math.ceil(.975*(len(vals)-1)))]]
    return {"finite":len(os),"rho_OX_ci95":ci(os),"rho_FX_ci95":ci(fs),"D_ci95":ci(ds)}


def build_event_groups(interactions,waypoints,route_policy):
    return build_fold_plants(
        interactions,waypoints,
        consumer_mode="hummingbird_only",
        route_policy=route_policy,
    )


def evaluate(interactions,waypoints,opp_groups,min_events,min_waypoints,route_policy):
    groups=build_event_groups(interactions,waypoints,route_policy)
    ab=direction_rows(groups,opp_groups,"A","B",min_events,min_waypoints)
    ba=direction_rows(groups,opp_groups,"B","A",min_events,min_waypoints)
    return ab,ba,combined(ab,ba)


def site_centered(interactions,waypoints,site_opp_groups):
    # Build event counts retaining site.
    stats={}
    for wp in waypoints.values():
        stats.setdefault((wp.site,wp.plant,wp.fold),{
            "waypoints":set(),"hours":0.0,"robbery":0,"legitimate":0
        })
        g=stats[(wp.site,wp.plant,wp.fold)]
        g["waypoints"].add(wp.waypoint);g["hours"]+=wp.sampling_hours

    for row in interactions:
        wp=waypoints.get(str(row.get("waypoint","")).strip())
        if wp is None or not _is_hummingbird(row):continue
        d=_parse_date(row.get("date"))
        if d is None or not _date_in_any_interval(d,list(wp.intervals)):continue
        if str(row.get("feeding_activity","")).strip().lower()=="no_feeding":continue
        route=_primary_route_status(row.get("piercing"))
        if route not in {"yes","no"}:continue
        stats[(wp.site,wp.plant,wp.fold)]["robbery" if route=="yes" else "legitimate"]+=1

    def one(pred_fold,out_fold):
        rows=[]
        for site,plant in sorted({(s,p) for s,p,_ in stats}):
            p=stats.get((site,plant,pred_fold));o=stats.get((site,plant,out_fold))
            opp=site_opp_groups.get((site,plant,out_fold))
            if p is None or o is None or opp is None:continue
            pt=p["robbery"]+p["legitimate"]
            if len(p["waypoints"])<2 or len(o["waypoints"])<2 or pt<5 or o["hours"]<=0 or opp.opportunities<=0:continue
            rows.append({
                "site":site,"share":p["robbery"]/pt,
                "occupancy":opp.positive/opp.opportunities,
                "flux":(o["robbery"]+o["legitimate"])/o["hours"],
            })
        by=defaultdict(list)
        for r in rows:by[r["site"]].append(r)
        xo=[];oo=[];ff=[]
        sites=0
        for vals in by.values():
            if len(vals)<3:continue
            xr=_rank([v["share"] for v in vals])
            orr=_rank([v["occupancy"] for v in vals])
            fr=_rank([math.log1p(v["flux"]) for v in vals])
            mx=_mean(xr);mo=_mean(orr);mf=_mean(fr)
            xo.extend([v-mx for v in xr]);oo.extend([v-mo for v in orr]);ff.extend([v-mf for v in fr])
            sites+=1
        return {"rows":len(rows),"centered_rows":len(xo),"eligible_sites":sites,
                "rho_occupancy":_pearson(xo,oo) if len(xo)>=3 else None,
                "rho_flux":_pearson(xo,ff) if len(xo)>=3 else None}
    a=one("A","B");b=one("B","A")
    return {"A_to_B":a,"B_to_A":b,
            "rho_OX":fisher_mean(a["rho_occupancy"],b["rho_occupancy"]) if a["rho_occupancy"] is not None and b["rho_occupancy"] is not None else None,
            "rho_FX":fisher_mean(a["rho_flux"],b["rho_flux"]) if a["rho_flux"] is not None and b["rho_flux"] is not None else None}


def analyze(interactions,cameras,plants,birds):
    waypoints=build_waypoints(cameras)
    opp_groups,site_opp_groups,audit=build_cr_opportunity_groups(interactions,cameras,plants,birds)

    ab,ba,primary=evaluate(interactions,waypoints,opp_groups,5,2,"primary")
    primary["permutation"]=permutation_test(ab,ba)
    primary["bootstrap"]=bootstrap(ab,ba)

    _,_,min10=evaluate(interactions,waypoints,opp_groups,10,2,"primary")
    _,_,min3=evaluate(interactions,waypoints,opp_groups,5,3,"primary")
    _,_,explicit=evaluate(interactions,waypoints,opp_groups,5,2,"explicit")
    site=site_centered(interactions,waypoints,site_opp_groups)

    enough=len(ab)>=MIN_DIRECTION_PLANTS and len(ba)>=MIN_DIRECTION_PLANTS
    full=(
        enough
        and primary.get("rho_OX") is not None and float(primary["rho_OX"])>0
        and float(primary["rho_FX"])<0
        and float(primary["D_fisher_z"])>0
        and float(primary["rho_legitimate_X"])<0
        and float(primary["rho_robbery_X"])>0
        and min10.get("rho_OX") is not None and float(min10["rho_OX"])>0
        and float(min10["rho_FX"])<0
    )
    decision={
        "eligible_directional_n":enough,
        "rho_OX_positive":primary.get("rho_OX") is not None and float(primary["rho_OX"])>0,
        "rho_FX_negative":primary.get("rho_FX") is not None and float(primary["rho_FX"])<0,
        "D_positive":primary.get("D_fisher_z") is not None and float(primary["D_fisher_z"])>0,
        "legitimate_flux_negative":primary.get("rho_legitimate_X") is not None and float(primary["rho_legitimate_X"])<0,
        "robbery_flux_positive":primary.get("rho_robbery_X") is not None and float(primary["rho_robbery_X"])>0,
        "min10_signs_replicate":min10.get("rho_OX") is not None and float(min10["rho_OX"])>0 and float(min10["rho_FX"])<0,
        "classification":"FULL_TOPOLOGY_INTENSITY_DECOUPLING" if full else "NOT_REPLICATED",
        "promotion_eligible":full,
    }
    return {
        "analysis_name":"costarica_topology_intensity_decoupling_validation",
        "status":"FIT",
        "freeze":"empirical/mutualism_attrition/COSTARICA_TOPOLOGY_INTENSITY_DECOUPLING_PREREG_V1.md",
        "seed":SEED,"permutations":PERMUTATIONS,"bootstraps":BOOTSTRAPS,
        "waypoint_split":{"clean_waypoints":len(waypoints),
                          "fold_A":sum(w.fold=="A" for w in waypoints.values()),
                          "fold_B":sum(w.fold=="B" for w in waypoints.values())},
        "opportunity_audit":audit,
        "primary":primary,
        "sensitivities":{"min10_events":min10,"min3_waypoints":min3,"explicit_yes_no":explicit,"within_site":site},
        "decision":decision,
        "claim_boundary":"Independent-country observational cross-fit; no causal or species-persistence inference."
    }


def run(output):
    tables={key:_read(_download(name)) for key,name in FILES_CR.items()}
    result=analyze(tables["interactions"],tables["cameras"],tables["plants"],tables["birds"])
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result


if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("output");args=ap.parse_args()
    print(json.dumps(run(args.output),indent=2,sort_keys=True))
