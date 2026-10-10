#!/usr/bin/env python3
"""Audit finite-Poisson-MLE existence for the frozen EPHI route-retention models.

This is a numerical feasibility test on sufficient-statistic margins, *not* a
new rate-ratio estimator. A finite Poisson loglinear fit assigns strictly
positive means to every supported design cell. Such a fit can exist only when
its observed row, column and (if included) mismatch-category margins admit
strictly positive values on all supported cells.

We maximize a common lower bound epsilon >= 0 for these means by linear
programming. epsilon == 0 at the optimum signals a boundary / separation
problem, not a biological zero effect. No fitting tolerance or category
boundary is modified.
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
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix, eye, hstack

REACH = 1.8
UPPER = math.log(1.25)
SHA256 = {
    "aubert_ephi_participation_opportunities.csv":
        "685f227a2aa2c5c322e18188ba5bd6d44aa67490b31514b9c728e6e033abc14f",
    "aubert_ephi_pair_site_analysis.csv":
        "94c74386d2c304b5816653e79b552a0e79487258c5021f8791c614afdc956afa",
}
EXISTENCE_TOL = 1e-7


@dataclass(frozen=True)
class Cell:
    waypoint: str
    bird: str
    site: str
    plant: str
    category: int
    robbery: int
    legitimate: int


def _read_frozen_archive(path: Path) -> tuple[list[Cell], dict]:
    with zipfile.ZipFile(path) as zf:
        def load(name: str) -> list[dict[str, str]]:
            raw = zf.read("data_archive/" + name)
            actual = hashlib.sha256(raw).hexdigest()
            if actual != SHA256[name]:
                raise ValueError("FROZEN_ARCHIVE_SHA256_MISMATCH:" + name)
            return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))

        pairs = load("aubert_ephi_pair_site_analysis.csv")
        opportunities = load("aubert_ephi_participation_opportunities.csv")

    groups: dict[str, str] = {}
    for pair in pairs:
        b = pair["bird_unit"]
        group = pair["bird_group"]
        if b in groups and groups[b] != group:
            raise ValueError("BIRD_GROUP_CONFLICT")
        groups[b] = group

    cells: list[Cell] = []
    for item in opportunities:
        group = groups.get(item["bird_unit"])
        if not group:
            raise ValueError("MISSING_BIRD_GROUP")
        if group != "hummingbird":
            continue
        m = float(item["mismatch_log_t_over_b"]) - math.log(REACH)
        cat = 0 if m <= 0 else (1 if m <= UPPER else 2)
        robbery = int(item["robbing_count"])
        legitimate = int(item["legitimate_count"])
        if robbery < 0 or legitimate < 0 or robbery + legitimate != int(item["primary_count"]):
            raise ValueError("ROUTE_COUNT_SUM_MISMATCH")
        cells.append(Cell(
            item["waypoint_unit"], item["bird_unit"], item["site_id"],
            item["plant_unit"], cat, robbery, legitimate
        ))

    if len(cells) != 19903:
        raise ValueError("HUMMINGBIRD_OPPORTUNITY_SUPPORT_DRIFT")
    return cells, {"archive_artifact_id": 11293379572,
                   "verified_sha256": SHA256, "opportunity_edges": len(cells),
                   "categories": [sum(c.category == k for c in cells) for k in range(3)]}


def _prune_positive_margins(cells: list[Cell], route: str, bird_site: bool) -> list[Cell]:
    current = list(cells)
    while True:
        rows: dict[str, int] = defaultdict(int)
        cols: dict[str, int] = defaultdict(int)
        for c in current:
            n = int(getattr(c, route))
            rows[c.waypoint] += n
            cols[c.bird + "@@" + c.site if bird_site else c.bird] += n
        next_cells = [
            c for c in current
            if rows[c.waypoint] > 0
            and cols[c.bird + "@@" + c.site if bird_site else c.bird] > 0
        ]
        if len(next_cells) == len(current):
            return current
        current = next_cells


def positive_margin_lp(
    cells: list[Cell], *, route: str, bird_site: bool,
    include_category: bool,
) -> dict:
    """Return maximal common positive cell expectation preserving all margins."""
    edges = _prune_positive_margins(cells, route, bird_site)
    row_names = sorted({c.waypoint for c in edges})
    col_names = sorted({c.bird + "@@" + c.site if bird_site else c.bird for c in edges})
    ri = {name: idx for idx, name in enumerate(row_names)}
    ci = {name: idx for idx, name in enumerate(col_names)}
    nr, nc, ne = len(ri), len(ci), len(edges)
    if ne == 0:
        return {"status":"NO_SUPPORTED_CELLS"}

    n_constraints = nr + nc + (3 if include_category else 0)
    ii, jj, vv = [], [], []
    margins = np.zeros(n_constraints)
    for k, e in enumerate(edges):
        constraints = [ri[e.waypoint], nr + ci[e.bird + "@@" + e.site if bird_site else e.bird]]
        if include_category:
            constraints.append(nr + nc + e.category)
        for c in constraints:
            ii.append(c)
            jj.append(k)
            vv.append(1.0)
            margins[c] += getattr(e, route)

    mat = coo_matrix((vv,(ii,jj)),shape=(n_constraints,ne)).tocsr()
    eq = hstack((mat,csr_matrix((n_constraints,1))),format="csr")
    ub = hstack((-eye(ne,format="csr"),csr_matrix(np.ones((ne,1)))),format="csr")
    objective = np.zeros(ne+1)
    objective[-1] = -1.0
    res = linprog(
        objective, A_ub=ub, b_ub=np.zeros(ne),
        A_eq=eq, b_eq=margins,
        bounds=[(0,None)]*(ne+1), method="highs",
    )
    if not res.success or res.x is None:
        return {"status":"LP_FAILED","message":res.message,"solver_status":int(res.status)}
    eps = float(max(0.0,res.x[-1]))
    eq_error = float(np.abs(eq@res.x - margins).max())
    if eq_error > 1e-6:
        return {"status":"LP_MARGINS_INVALID","max_margin_absolute_error":eq_error}

    # Finite parameter means are strictly positive on every supported cell.
    # A strictly positive vector is possible iff max-min epsilon > 0.
    return {
        "status":"STRICTLY_POSITIVE_FEASIBLE" if eps > EXISTENCE_TOL else "BOUNDARY_SEPARATION",
        "route":route,
        "fixed_effect_groups":"waypoint+bird_site" if bird_site else "waypoint+bird",
        "include_three_mismatch_categories":include_category,
        "positive_margin_supported_edges":ne,
        "positive_margin_waypoints":nr,
        "positive_margin_consumer_groups":nc,
        "observed_route_events":int(sum(getattr(e,route) for e in edges)),
        "max_common_positive_mean":eps,
        "max_margin_absolute_error":eq_error,
        "solver_status":int(res.status),
        "diagnostic_only":True,
    }


def run(path: Path, output: Path) -> dict:
    cells, audit = _read_frozen_archive(path)
    fits = []
    for route in ("robbery","legitimate"):
        for bird_site in (False,True):
            for include_category in (False,True):
                fits.append(positive_margin_lp(
                    cells, route=route,bird_site=bird_site,
                    include_category=include_category))
    receipt = {
        "analysis":"route_specific_fixed_effect_poisson_existence_audit",
        "source":audit,
        "fits":fits,
        "claim_boundary":(
            "Boundary separation concerns the finite maximum-likelihood solution "
            "of the specified high-dimensional loglinear design. It does not prove "
            "zero ecological robbery effects, individual route switching or causal "
            "mismatch impacts. It does not select a replacement model."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({ "fits":[
        {k:v for k,v in f.items() if k in
            ("status","route","fixed_effect_groups","include_three_mismatch_categories",
             "positive_margin_supported_edges","max_common_positive_mean")}
        for f in fits]},indent=2))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_zip",type=Path)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    run(args.archive_zip,args.output)
