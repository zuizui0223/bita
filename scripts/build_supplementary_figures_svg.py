"""Build Supplementary Figures S1-S4 from frozen theory and synthesis outputs.

This is presentation-only code. It does not change the theory, evidence ledgers,
or quantitative estimates. The figures make already-declared robustness and
same-system architecture auditable in a compact reader-facing form.
"""
from __future__ import annotations

import argparse
import csv
import math
import re
from collections import defaultdict
from html import escape
from pathlib import Path

from trait_architecture.model import ModelParameters

ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / "empirical" / "mechanism_pattern_synthesis"

BASE_LEDGER_NAMES = (
    "MASTER_LEDGER_V1.csv",
    "LEDGER_BATCH_2_V1.csv",
    "LEDGER_BATCH_3_V1.csv",
    "LEDGER_BATCH_4_V1.csv",
    "LEDGER_BATCH_5_V1.csv",
)
ROUTES = (
    "A_to_pollination",
    "A_to_antagonism",
    "D_to_antagonism",
    "D_to_pollination",
)


def _text(value: object) -> str:
    return str(value or "").strip()


def _bool(value: object) -> bool:
    return _text(value).lower() == "true"


def _read_csv(path: Path, *, strict_overflow: bool = False) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows: list[dict[str, str]] = []
        for row in csv.DictReader(handle):
            if strict_overflow and None in row:
                raise ValueError(f"CSV overflow in {path.name}: {row.get('record_id')}: {row[None]}")
            rows.append({k: _text(v) for k, v in row.items() if k is not None})
        return rows


def read_evaluations(path: Path) -> list[dict[str, str]]:
    rows = _read_csv(path, strict_overflow=True)
    required = {
        "parameter_scenario_id", "form_id", "attraction", "defence", "assurance",
        "pollinator_service", "floral_damage_pressure", "attraction_gain",
        "attraction_tracking", "floral_defence_efficacy", "defence_pollinator_cost",
        "attraction_defence_shared_cost", "attraction_saturation", "defence_saturation",
        "joint_cost_curvature", "mixed_partial", "sign",
    }
    missing = required - set(rows[0]) if rows else required
    if missing:
        raise ValueError(f"evaluation CSV missing columns: {sorted(missing)}")
    return rows


def _f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def nonlinear_score(row: dict[str, str], a: float, d: float) -> float:
    """Reconstruct the endpoint-normalized score whose analytic W_AD is stored.

    Parameters not varied by the sensitivity grid come from ModelParameters;
    scenario/form-varying quantities are read from the evaluation row.
    """
    defaults = ModelParameters()
    r = _f(row, "assurance")
    p = _f(row, "pollinator_service")
    h = _f(row, "floral_damage_pressure")
    b_a = _f(row, "attraction_gain")
    q_a = _f(row, "attraction_saturation")
    e_f = _f(row, "floral_defence_efficacy")
    q_d = _f(row, "defence_saturation")
    obstruction = _f(row, "defence_pollinator_cost")
    tracking = _f(row, "attraction_tracking")
    shared = _f(row, "attraction_defence_shared_cost")
    k = _f(row, "joint_cost_curvature")

    attraction_response = b_a * (1.0 + q_a) * a / (1.0 + q_a * a)
    outcross = (
        p
        * (defaults.baseline_outcross + attraction_response)
        * math.exp(-obstruction * d)
        * (1.0 - defaults.assurance_outcross_dilution * r)
    )
    assurance = (1.0 - p) * defaults.assurance_gain * r
    defence_response = e_f * (1.0 + q_d) * d / (1.0 + q_d * d)
    damage = h * (defaults.floral_damage_baseline + tracking * a) * (1.0 - defence_response)
    joint = shared * a * d * (1.0 + k * (a + d)) / (1.0 + 2.0 * k)
    cost = (
        defaults.attraction_cost * a * a
        + defaults.defence_cost * d * d
        + defaults.assurance_cost * r * r
        + joint
    )
    return outcross + assurance - damage - cost


def finite_difference_mixed_partial(row: dict[str, str], step: float = 1e-5) -> float:
    a = _f(row, "attraction")
    d = _f(row, "defence")
    h = step
    return (
        nonlinear_score(row, a + h, d + h)
        - nonlinear_score(row, a + h, d - h)
        - nonlinear_score(row, a - h, d + h)
        + nonlinear_score(row, a - h, d - h)
    ) / (4.0 * h * h)


def derivative_agreement(rows: list[dict[str, str]]) -> dict[str, list[tuple[float, float, float]]]:
    grouped: dict[str, list[tuple[float, float, float]]] = defaultdict(list)
    for row in rows:
        analytic = _f(row, "mixed_partial")
        numeric = finite_difference_mixed_partial(row)
        grouped[row["form_id"]].append((analytic, numeric, abs(analytic - numeric)))
    return dict(grouped)


def _svg_text(x: float, y: float, value: str, size: int = 14, *, anchor: str = "start", weight: int = 400) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}">{escape(value)}</text>'
    )


def build_s1(rows: list[dict[str, str]]) -> str:
    grouped = derivative_agreement(rows)
    forms = sorted(grouped)
    if len(forms) != 4:
        raise ValueError(f"expected four response shapes, found {forms}")
    width, height = 1300, 900
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']
    positions = [(70, 70), (680, 70), (70, 470), (680, 470)]
    for form, (x0, y0) in zip(forms, positions):
        pts = grouped[form]
        values = [v for p in pts for v in p[:2]]
        lo, hi = min(values), max(values)
        pad = max((hi - lo) * 0.08, 0.02)
        lo -= pad; hi += pad
        w, h = 500, 300
        sx = lambda v: x0 + 55 + (v - lo) / (hi - lo) * (w - 85)
        sy = lambda v: y0 + h - 45 - (v - lo) / (hi - lo) * (h - 85)
        parts.append(_svg_text(x0, y0 - 18, form.replace("_", " "), 18, weight=700))
        parts.append(f'<rect x="{x0+55}" y="{y0+25}" width="{w-85}" height="{h-85}" fill="none" stroke="#333" stroke-width="1.5"/>')
        parts.append(f'<line x1="{sx(lo):.1f}" y1="{sy(lo):.1f}" x2="{sx(hi):.1f}" y2="{sy(hi):.1f}" stroke="#555" stroke-width="1.5" stroke-dasharray="7 6"/>')
        for analytic, numeric, _ in pts:
            parts.append(f'<circle cx="{sx(analytic):.2f}" cy="{sy(numeric):.2f}" r="1.7" fill="#222" fill-opacity="0.45"/>')
        maxerr = max(p[2] for p in pts)
        parts.append(_svg_text(x0 + 65, y0 + h - 10, f"max |analytic − finite difference| = {maxerr:.2e}", 13))
        parts.append(_svg_text(x0 + w/2, y0 + h + 18, "analytic mixed partial", 13, anchor="middle"))
        axis_x, axis_y = x0 + 12, y0 + 150
        parts.append(f'<text x="{axis_x:.1f}" y="{axis_y:.1f}" transform="rotate(-90 {axis_x:.1f} {axis_y:.1f})" text-anchor="middle" font-family="DejaVu Sans,Arial,sans-serif" font-size="12">finite-difference mixed partial</text>')
        for val in (lo, 0.0, hi):
            if lo <= val <= hi:
                parts.append(_svg_text(sx(val), y0 + h - 27, f"{val:.2f}", 10, anchor="middle"))
                parts.append(_svg_text(x0 + 47, sy(val)+4, f"{val:.2f}", 10, anchor="end"))
    parts.append(_svg_text(650, 875, "Central difference step = 1e-5; all 2,592 declared evaluations are shown. Agreement is a numerical implementation check, not empirical validation.", 14, anchor="middle"))
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def build_s2(rows: list[dict[str, str]]) -> str:
    scenarios = sorted({r["parameter_scenario_id"] for r in rows})
    forms = sorted({r["form_id"] for r in rows})
    if len(scenarios) != 4 or len(forms) != 4:
        raise ValueError("S2 expects four scenarios x four forms")
    grouped: dict[tuple[str, str, float, float], list[str]] = defaultdict(list)
    for r in rows:
        key = (r["parameter_scenario_id"], r["form_id"], _f(r, "pollinator_service"), _f(r, "floral_damage_pressure"))
        grouped[key].append(r["sign"])
    width, height = 2200, 1500
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']
    cell = 62; panel_w = 390; panel_h = 330; x_start=460; y_start=115
    for c, form in enumerate(forms):
        parts.append(_svg_text(x_start + c*panel_w + 120, 45, form.replace("_", " "), 16, anchor="middle", weight=700))
    for rr, scenario in enumerate(scenarios):
        parts.append(_svg_text(x_start - 28, y_start + rr*panel_h + 115, scenario.replace("_", " "), 13, anchor="end", weight=700))
        for cc, form in enumerate(forms):
            x0 = x_start + cc*panel_w
            y0 = y_start + rr*panel_h
            for j, hval in enumerate((0.8,0.5,0.2)):
                parts.append(_svg_text(x0-8, y0+j*cell+37, f"H={hval:.1f}", 10, anchor="end"))
                for i, pval in enumerate((0.2,0.5,0.8)):
                    signs = grouped[(scenario, form, pval, hval)]
                    frac = sum(s == "complementary" for s in signs)/len(signs)
                    shade = round(245 - 165*frac)
                    x=x0+i*cell; y=y0+j*cell
                    parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="rgb({shade},{shade},{shade})" stroke="#333"/>')
                    parts.append(_svg_text(x+cell/2, y+36, f"{100*frac:.0f}%", 11, anchor="middle", weight=700))
            for i,pval in enumerate((0.2,0.5,0.8)):
                parts.append(_svg_text(x0+i*cell+cell/2, y0+3*cell+20, f"P={pval:.1f}", 10, anchor="middle"))
    parts.append(_svg_text(850, 1470, "Each cell is the unweighted complementary fraction across A × D × R coordinates at fixed scenario, response shape, P and H; it is not prevalence in nature.", 14, anchor="middle"))
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def coverage_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for name in BASE_LEDGER_NAMES:
        rows.extend(_read_csv(SYNTHESIS / name))
    for path in sorted(SYNTHESIS.glob("EXPANSION_LEDGER_BATCH_*_V1.csv")):
        rows.extend(_read_csv(path, strict_overflow=True))
    return rows


def same_system_routes() -> dict[str, set[str]]:
    rows = coverage_rows()
    routes_by: dict[str, set[str]] = defaultdict(set)
    explicit: set[str] = set()
    for r in rows:
        cluster = r.get("independence_cluster", "")
        route = r.get("route", "")
        if cluster and route in ROUTES:
            routes_by[cluster].add(route)
        if cluster and _bool(r.get("is_same_system_multi_route")):
            explicit.add(cluster)
    keep = {c for c, routes in routes_by.items() if len(routes) >= 2} | explicit
    return {c: routes_by[c] for c in sorted(keep)}


def build_s3() -> str:
    matrix = same_system_routes()
    if len(matrix) != 14:
        raise ValueError(f"expected 14 same-system clusters, found {len(matrix)}")
    width, height = 1350, 860
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="white"/>']
    x0=560; y0=100; cw=165; rh=49
    labels={"A_to_pollination":"A → pollination","A_to_antagonism":"A → antagonism","D_to_antagonism":"D → antagonism","D_to_pollination":"D → pollination"}
    for i,route in enumerate(ROUTES):
        parts.append(_svg_text(x0+i*cw+cw/2, 58, labels[route], 13, anchor="middle", weight=700))
    for j,(cluster,routes) in enumerate(matrix.items()):
        y=y0+j*rh
        parts.append(_svg_text(x0-18, y+31, cluster.replace("_", " "), 12, anchor="end"))
        for i,route in enumerate(ROUTES):
            fill="#444" if route in routes else "#f4f4f4"
            parts.append(f'<rect x="{x0+i*cw}" y="{y}" width="{cw-8}" height="{rh-7}" fill="{fill}" stroke="#777"/>')
            if route in routes:
                parts.append(_svg_text(x0+i*cw+(cw-8)/2, y+28, "present", 10, anchor="middle", weight=700))
    parts.append(_svg_text(675, 835, "Rows are independent biological clusters with at least two linked marginal routes (or an explicit same-system linkage flag). Presence is categorical; cells are not effect sizes.", 13, anchor="middle"))
    parts.append('</svg>')
    return "\n".join(parts)+"\n"


def parse_robustness() -> dict[str, float]:
    text = (SYNTHESIS / "SYNTHESIS_ROBUSTNESS_AUDIT_V1.md").read_text(encoding="utf-8")
    def req(pattern: str, label: str) -> float:
        m=re.search(pattern,text,flags=re.I)
        if not m: raise ValueError(f"could not parse {label}")
        return float(m.group(1))
    return {
        "i2_female": req(r"female fitness\s+I2\s*=\s*([0-9.]+)%", "female I2"),
        "i2_nectar": req(r"nectar standing crop\s+I2\s*=\s*([0-9.]+)%", "nectar I2"),
        "i2_visit": req(r"legitimate visitation\s+I2\s*=\s*([0-9.]+)%", "visitation I2"),
        "s_min": req(r"minimum difference:\s*\+([0-9.]+)", "Sasidharan LOCO minimum"),
        "s_median": req(r"median difference:\s*\+([0-9.]+)", "Sasidharan LOCO median"),
        "s_max": req(r"maximum difference:\s*\+([0-9.]+)", "Sasidharan LOCO maximum"),
    }


def parse_module_values() -> dict[str, float]:
    modules={r["module_id"]:r for r in _read_csv(SYNTHESIS/"SECONDARY_SYNTHESIS_MODULES_V1.csv")}
    leal=modules["SM001"]["current_result"]
    sas=modules["SM003"]["current_result"]
    def m(pattern,text,label):
        x=re.search(pattern,text,flags=re.I)
        if not x: raise ValueError(f"could not parse {label}")
        return float(x.group(1))
    return {
        "female":m(r"female fitness LRR\s*([+-]?[0-9.]+)",leal,"female LRR"),
        "nectar":m(r"nectar standing crop\s*([+-]?[0-9.]+)",leal,"nectar LRR"),
        "visit":m(r"legitimate visitation\s*([+-]?[0-9.]+)",leal,"visit LRR"),
        "sas":m(r"risk difference\s*\+([0-9.]+)",sas,"Sasidharan RD"),
    }


def build_s4() -> str:
    r=parse_robustness(); v=parse_module_values()
    width,height=1600,720
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="white"/>']
    parts.append(_svg_text(70,55,"A  Floral-larceny reproduced meta-analysis",20,weight=700))
    labels=[("female fitness","female","i2_female"),("nectar standing crop","nectar","i2_nectar"),("legitimate visitation","visit","i2_visit")]
    x0=250; y0=120; scale=560
    xmin,xmax=-0.60,0.05
    sx=lambda x:x0+(x-xmin)/(xmax-xmin)*scale
    parts.append(f'<line x1="{sx(0):.1f}" y1="{y0-25}" x2="{sx(0):.1f}" y2="{y0+250}" stroke="#555" stroke-dasharray="6 5"/>')
    for j,(label,key,i2key) in enumerate(labels):
        y=y0+j*90
        val=v[key]
        parts.append(_svg_text(x0-15,y+8,label,13,anchor="end"))
        parts.append(f'<line x1="{sx(0):.1f}" y1="{y}" x2="{sx(val):.1f}" y2="{y}" stroke="#222" stroke-width="12"/>')
        parts.append(_svg_text(sx(val)-8,y-12,f"LRR {val:.3f}",12,anchor="end",weight=700))
        parts.append(_svg_text(x0+scale+15,y+5,f"I² {r[i2key]:.1f}%",12))
    parts.append(_svg_text(70,420,"Direction retained in 100% of declared leave-one-cluster-out refits; within-cluster-correlation and quarantined-row sensitivities preserve the three informative conclusions.",12))
    parts.append(_svg_text(70,448,"High heterogeneity is retained as part of the Pattern result; the bars are pooled LRRs, not W_AD or model parameters.",12))

    parts.append(_svg_text(900,55,"B  FVOC reproduced synthesis",20,weight=700))
    bx0=980; by=190; bscale=430; bmin=0.0; bmax=0.22
    bs=lambda x:bx0+(x-bmin)/(bmax-bmin)*bscale
    parts.append(f'<line x1="{bs(r["s_min"]):.1f}" y1="{by}" x2="{bs(r["s_max"]):.1f}" y2="{by}" stroke="#222" stroke-width="8"/>')
    parts.append(f'<circle cx="{bs(r["s_median"]):.1f}" cy="{by}" r="9" fill="#fff" stroke="#111" stroke-width="3"/>')
    parts.append(f'<circle cx="{bs(v["sas"]):.1f}" cy="{by-22}" r="7" fill="#111"/>')
    parts.append(_svg_text(bs(v["sas"]), by-42, f"full {v['sas']:+.3f}", 11, anchor="middle", weight=700))
    parts.append(_svg_text(bs(r["s_min"]), by+42, f"min {r['s_min']:+.4f}", 11, anchor="start"))
    parts.append(_svg_text(bs(r["s_median"]), by+62, f"median {r['s_median']:+.4f}", 11, anchor="middle"))
    parts.append(_svg_text(bs(r["s_max"]), by+42, f"max {r['s_max']:+.4f}", 11, anchor="end"))
    parts.append(_svg_text(920,300,"32/32 leave-one-study-component-out contrasts remain positive",14,weight=700))
    parts.append(_svg_text(920,333,"Only three study components contain both physiological roles; all three paired differences are zero",12))
    parts.append(_svg_text(920,365,"The assembled +0.129 pattern is therefore not a causal within-study pollinator-versus-florivore effect",12))
    parts.append(_svg_text(800,680,"Robustness metrics remain module-specific: continuous LRR influence/heterogeneity for Leal; categorical study-component influence and composition limits for Sasidharan.",13,anchor="middle"))
    parts.append('</svg>')
    return "\n".join(parts)+"\n"


def write_all(evaluations: Path, outdir: Path) -> dict[str, Path]:
    rows=read_evaluations(evaluations)
    if len(rows)!=2592:
        raise ValueError(f"expected 2,592 evaluations, found {len(rows)}")
    outdir.mkdir(parents=True,exist_ok=True)
    payloads={
        "FIGURE_S1_DERIVATIVE_AGREEMENT.svg":build_s1(rows),
        "FIGURE_S2_SCENARIO_SIGN_MAPS.svg":build_s2(rows),
        "FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg":build_s3(),
        "FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg":build_s4(),
    }
    result={}
    for name,text in payloads.items():
        p=outdir/name; p.write_text(text,encoding="utf-8"); result[name]=p
    return result


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evaluation_csv",type=Path)
    parser.add_argument("output_dir",type=Path)
    args=parser.parse_args(argv)
    outputs=write_all(args.evaluation_csv,args.output_dir)
    grouped=derivative_agreement(read_evaluations(args.evaluation_csv))
    maxerr=max(e for pts in grouped.values() for _,_,e in pts)
    print(f"wrote {len(outputs)} supplementary SVGs; max analytic-vs-FD error={maxerr:.3e}; same_system={len(same_system_routes())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
