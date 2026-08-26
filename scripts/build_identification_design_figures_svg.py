"""Build candidate Main Figures 1–5 for the identification-design manuscript.

These figures belong to MANUSCRIPT_IDENTIFICATION_DESIGN.md and do not replace
canonical submission figures until the candidate manuscript is promoted.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "identification_figures"
COVERAGE = ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv"
IMPATIENS = ROOT / "empirical" / "identification_design" / "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json"

STYLE = """
<style>
.title{font:700 29px DejaVu Sans,Arial,sans-serif}.sub{font:700 21px DejaVu Sans,Arial,sans-serif}
.body{font:18px DejaVu Sans,Arial,sans-serif}.small{font:15px DejaVu Sans,Arial,sans-serif}.tiny{font:13px DejaVu Sans,Arial,sans-serif}
.box{fill:#fff;stroke:#222;stroke-width:2}.soft{fill:#f4f4f4;stroke:#333;stroke-width:1.8}.dark{fill:#e3e3e3;stroke:#111;stroke-width:2.4}
.line{stroke:#222;stroke-width:2;fill:none}.dash{stroke:#555;stroke-width:2;fill:none;stroke-dasharray:8 7}
</style>
"""


def _svg(width: int, height: int, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs>{STYLE}</defs><rect width="100%" height="100%" fill="#fff"/>{body}</svg>'


def _box(x: int, y: int, w: int, h: int, title: str, lines: list[str], cls: str = "box") -> str:
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}"/>',
           f'<text x="{x+w/2}" y="{y+30}" text-anchor="middle" class="sub">{escape(title)}</text>']
    for i, line in enumerate(lines):
        out.append(f'<text x="{x+18}" y="{y+62+i*25}" class="body">{escape(line)}</text>')
    return "".join(out)


def fig1() -> str:
    b = ['<text x="600" y="42" text-anchor="middle" class="title">A total trait interaction does not identify its mechanism</text>']
    b.append(_box(55, 95, 420, 500, "Measured four-cell trait factorial", ["A and D each have two experimental levels", "", "ΔAD W = W11 − W10 − W01 + W00", "", "This is the directly estimable trait interaction", "on the chosen biological outcome scale."], "dark"))
    coords = {(0,0):(95,390),(1,0):(275,390),(0,1):(95,480),(1,1):(275,480)}
    for (a,d),(x,y) in coords.items():
        b.append(f'<rect x="{x}" y="{y}" width="145" height="65" rx="8" class="soft"/><text x="{x+72}" y="{y+38}" text-anchor="middle" class="body">W{a}{d}</text>')
    b.append('<path d="M490 345 L620 345" class="line"/><polygon points="620,345 606,337 606,353" fill="#222"/>')
    b.append(_box(640, 85, 500, 165, "Possible allocation 1", ["large antagonist relief", "small pollinator interference", "non-negative joint cost"], "soft"))
    b.append(_box(640, 285, 500, 165, "Possible allocation 2", ["moderate antagonist relief", "moderate pollinator interference", "synergistic hidden joint channel"], "soft"))
    b.append(_box(640, 485, 500, 165, "Possible allocation 3", ["small relief and small interference", "different direct/allocation channel", "same observed ΔAD W"], "soft"))
    b.append('<text x="600" y="710" text-anchor="middle" class="sub">Interaction detection ≠ mechanism allocation</text>')
    return _svg(1200, 750, "".join(b))


def fig2() -> str:
    b = ['<text x="650" y="42" text-anchor="middle" class="title">Crossed interventions identify channels and test separability</text>']
    labels = [("G excluded / P excluded",60,105),("G present / P excluded",660,105),("G excluded / P present",60,405),("G present / P present",660,405)]
    for label,x,y in labels:
        b.append(_box(x,y,520,235,label,["Within this consumer state:","measure the same four A×D cells","W00   W10   W01   W11"],"soft"))
        for j,(a,d) in enumerate([(0,0),(1,0),(0,1),(1,1)]):
            cx=x+45+(j%2)*210; cy=y+145+(j//2)*55
            b.append(f'<rect x="{cx}" y="{cy}" width="165" height="42" rx="6" class="box"/><text x="{cx+82}" y="{cy+27}" text-anchor="middle" class="small">A={a}, D={d}</text>')
    b.append('<text x="650" y="690" text-anchor="middle" class="sub">Channel contrasts</text>')
    b.append('<text x="80" y="730" class="body">ρΔ = −ΔAD[W(G excluded) − W(G present)]</text>')
    b.append('<text x="80" y="766" class="body">ιΔinc = −ΔAD[W(P present) − W(P excluded)]</text>')
    b.append('<text x="80" y="802" class="body">ιΔ = ιΔinc − m0,Δ</text>')
    b.append('<rect x="690" y="690" width="540" height="125" rx="14" class="dark"/>')
    b.append('<text x="960" y="724" text-anchor="middle" class="sub">Internal separability diagnostic</text>')
    b.append('<text x="715" y="760" class="body">A×D×G×P four-way coupling = 0?</text>')
    b.append('<text x="715" y="792" class="small">ρ cross-P gap and ι cross-G gap are the same contrast up to sign.</text>')
    return _svg(1300, 850, "".join(b))


def fig3() -> str:
    b = ['<text x="600" y="42" text-anchor="middle" class="title">Do not define the joint cost as a residual</text>']
    b.append(_box(55,100,500,245,"Crossed consumer design",["Estimate ΔAD W, ρΔ and ιΔ", "after m0,Δ correction and separability test", "", "UΔ = ρΔ − ιΔ − ΔAD W", "UΔ remains an unallocated joint channel"],"soft"))
    b.append(_box(645,100,500,245,"Independent A×D cost assay",["Standardize/suppress biotic channels", "Measure construction or allocation endpoint", "", "κassay,Δ = ΔAD Cassay", "Do not derive this from UΔ"],"soft"))
    b.append('<path d="M305 365 L305 435 L600 435" class="line"/><path d="M895 365 L895 435 L600 435" class="line"/><polygon points="600,435 586,427 586,443" fill="#222"/>')
    b.append(_box(285,455,630,145,"Compare residual with independent assay",["agreement → supports channel allocation", "disagreement → missing channel / intervention failure / scale mismatch"],"dark"))
    b.append('<rect x="80" y="645" width="1040" height="90" rx="14" class="box"/>')
    b.append('<text x="600" y="678" text-anchor="middle" class="sub">Sign diagnostic</text>')
    b.append('<text x="600" y="713" text-anchor="middle" class="body">If ΔAD W &gt; 0 and ρΔ ≤ ιΔ, the remaining joint channel must be negative.</text>')
    return _svg(1200, 780, "".join(b))


def _read_coverage() -> list[dict[str,str]]:
    with COVERAGE.open(encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h))


def _impatiens_targets() -> list[dict[str,float|str]]:
    data = json.loads(IMPATIENS.read_text(encoding="utf-8"))
    targets=[]
    summaries = data.get("model_summaries") or data.get("models") or []
    for summary in summaries:
        analysis = str(summary.get("analysis_id") or summary.get("outcome") or "outcome")
        raw_coeffs = summary.get("all_coefficients") or summary.get("coefficients") or summary.get("target_coefficients") or []
        coeffs = list(raw_coeffs.values()) if isinstance(raw_coeffs, dict) else list(raw_coeffs)
        for c in coeffs:
            term=str(c.get("term", ""))
            if term == "A_z:D_z" or term.startswith("A_z:D_z:"):
                lo = c.get("ci95_lower", c.get("ci_lower"))
                hi = c.get("ci95_upper", c.get("ci_upper"))
                targets.append({"analysis":analysis,"term":term,"estimate":float(c["estimate"]),"lo":float(lo),"hi":float(hi)})
    if len(targets) != 8:
        raise ValueError(f"Expected eight Impatiens A×D target coefficients, found {len(targets)}")
    return targets


def _xscale(value: float, x0: float=600, lo: float=-1.8, hi: float=1.3, width: float=600) -> float:
    return x0 + (value-lo)/(hi-lo)*width


def fig4() -> str:
    rows=_read_coverage(); targets=_impatiens_targets()
    b=['<text x="650" y="42" text-anchor="middle" class="title">Existing studies occupy complementary parts of the identification design</text>']
    b.append(_box(50,85,565,220,"Trait-factorial side — Kessler et al. 2008",["manipulated floral benzylacetone × nicotine", "direct discrete A×D-like reproductive interaction", "published aggregate sign: positive", "Δ probability scale ≈ +0.19 to +0.25", "missing: selective G and P toggles; systemic-D caveat"],"dark"))
    b.append(_box(685,85,565,220,"Consumer-factorial side — Egan et al. 2021",["crossed herbivory × pollination environment", "selection on attraction/defence-related traits", "consumer-context structure is strong", "missing: independently manipulated floral A×D", "several defence metabolites are leaf-derived"],"dark"))
    b.append('<text x="650" y="345" text-anchor="middle" class="sub">The missing object is their intersection</text>')
    b.append(f'<text x="650" y="375" text-anchor="middle" class="body">High-information coverage matrix: {len(rows)} systems; independent κ assay = 0; full channel identification = 0</text>')
    b.append('<text x="60" y="430" class="sub">Impatiens public-data retrofit: observational A×D and randomized-agent modifiers</text>')
    x0=600; w=600
    for tick in [-1.5,-1.0,-0.5,0,0.5,1.0]:
        x=_xscale(tick,x0=x0,width=w)
        b.append(f'<line x1="{x}" y1="455" x2="{x}" y2="830" class="dash"/><text x="{x}" y="850" text-anchor="middle" class="tiny">{tick:+.1f}</text>')
    label_map={"A_z:D_z":"A×D","A_z:D_z:Robbing_c":"A×D×Robbing","A_z:D_z:Florivory_c":"A×D×Florivory","A_z:D_z:Pollination_c":"A×D×Pollination"}
    order=["A_z:D_z","A_z:D_z:Robbing_c","A_z:D_z:Florivory_c","A_z:D_z:Pollination_c"]
    targets=sorted(targets,key=lambda r:(str(r["analysis"]), order.index(str(r["term"]))))
    y=485; last_analysis=None
    for r in targets:
        analysis=str(r["analysis"])
        if analysis!=last_analysis:
            short="CH fruits/day" if "fruit" in analysis.lower() and "seed" not in analysis.lower() else "seeds/CH fruit"
            b.append(f'<text x="70" y="{y}" class="small">{escape(short)}</text>'); y+=25; last_analysis=analysis
        lo=_xscale(float(r["lo"]),x0=x0,width=w); hi=_xscale(float(r["hi"]),x0=x0,width=w); est=_xscale(float(r["estimate"]),x0=x0,width=w)
        b.append(f'<text x="230" y="{y+5}" class="tiny">{escape(label_map.get(str(r["term"]),str(r["term"])))}</text>')
        b.append(f'<line x1="{lo}" y1="{y}" x2="{hi}" y2="{y}" class="line"/><circle cx="{est}" cy="{y}" r="5" fill="#222"/>')
        y+=38
    b.append('<text x="900" y="885" text-anchor="middle" class="small">All eight target intervals cross zero; context modification is estimable but unresolved.</text>')
    return _svg(1300,920,"".join(b))


def fig5() -> str:
    b=['<text x="600" y="42" text-anchor="middle" class="title">An executable path from interaction detection to mechanism identification</text>']
    steps=[
        ("1", "Choose A and flower-specific D", "Independent biological manipulation of both trait coordinates"),
        ("2", "Engineer selective G and P interventions", "Use body size, route, diel period, phenology or other access asymmetry"),
        ("3", "Run A×D×G×P", "Estimate ΔAD W and the consumer contrasts"),
        ("4", "Measure m0,Δ", "Do not assume pollinator-independent reproduction has zero A×D interaction"),
        ("5", "Test four-way separability", "Non-zero A×D×G×P coupling is a biological result"),
        ("6", "Run independent A×D cost assay", "Keep UΔ unallocated until the assay constrains its interpretation"),
        ("7", "Classify the outcome", "channel-resolved / non-separable / assay-discordant / hidden-channel sign constrained"),
    ]
    y=90
    for num,title,desc in steps:
        b.append(f'<circle cx="115" cy="{y+40}" r="31" class="dark"/><text x="115" y="{y+47}" text-anchor="middle" class="sub">{num}</text>')
        b.append(f'<rect x="175" y="{y}" width="900" height="80" rx="13" class="soft"/><text x="200" y="{y+30}" class="sub">{escape(title)}</text><text x="200" y="{y+59}" class="small">{escape(desc)}</text>')
        if num!="7": b.append(f'<line x1="115" y1="{y+72}" x2="115" y2="{y+105}" class="line"/>')
        y+=105
    return _svg(1200,850,"".join(b))


def build(out_dir: Path=OUT) -> list[Path]:
    out_dir.mkdir(parents=True,exist_ok=True)
    svgs=[fig1(),fig2(),fig3(),fig4(),fig5()]
    paths=[]
    for i,svg in enumerate(svgs,1):
        path=out_dir/f"FIGURE_{i}_IDENTIFICATION_DESIGN.svg"
        path.write_text(svg,encoding="utf-8")
        paths.append(path)
    return paths


def main(argv: list[str]|None=None) -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--out-dir",type=Path,default=OUT)
    args=parser.parse_args(argv)
    for p in build(args.out_dir): print(p)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
