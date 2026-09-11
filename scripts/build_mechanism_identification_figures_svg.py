"""Build the five Main SVG figures for the active BITA mechanism-identification paper.

The active paper is organized around the inference boundary

    trait interaction != ecological mechanism

Figure 4 is source-backed: it reads the authoritative 17-system V2 audit, the
Impatiens retrofit, and the frozen 56-route / 25-cluster recurrence state.  The
active figures use larger internal type than the historical identification figures
so labels remain readable after full-page-width Word/PDF scaling.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

try:  # works both as `python scripts/...py` and as an imported test module
    from scripts import build_identification_design_figures_svg as legacy
except ImportError:  # pragma: no cover - direct script execution path
    import build_identification_design_figures_svg as legacy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "mechanism_identification_figures"

STYLE = """
<style>
.title{font:700 34px DejaVu Sans,Arial,sans-serif}.sub{font:700 24px DejaVu Sans,Arial,sans-serif}
.body{font:22px DejaVu Sans,Arial,sans-serif}.small{font:20px DejaVu Sans,Arial,sans-serif}.tiny{font:18px DejaVu Sans,Arial,sans-serif}
.box{fill:#fff;stroke:#222;stroke-width:2}.soft{fill:#f4f4f4;stroke:#333;stroke-width:1.8}.dark{fill:#e3e3e3;stroke:#111;stroke-width:2.4}
.line{stroke:#222;stroke-width:2.2;fill:none}.dash{stroke:#555;stroke-width:1.8;fill:none;stroke-dasharray:8 7}
</style>
"""


def _svg(width: int, height: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><defs>{STYLE}</defs>'
        f'<rect width="100%" height="100%" fill="#fff"/>{body}</svg>'
    )


def _box(x: int, y: int, w: int, h: int, title: str, lines: list[str], cls: str = "box") -> str:
    out = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}"/>',
        f'<text x="{x+w/2}" y="{y+34}" text-anchor="middle" class="sub">{escape(title)}</text>',
    ]
    for i, line in enumerate(lines):
        out.append(f'<text x="{x+18}" y="{y+72+i*30}" class="body">{escape(line)}</text>')
    return "".join(out)


def _arrow(x1: int, y1: int, x2: int, y2: int) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line"/>'
        f'<polygon points="{x2},{y2} {x2-14},{y2-8} {x2-14},{y2+8}" fill="#222"/>'
    )


def fig1() -> str:
    """Outcome-level promotion: interaction relief is weaker than release/reversal."""
    b = [
        '<text x="650" y="46" text-anchor="middle" class="title">A positive trait interaction is not yet functional release</text>'
    ]
    b.append(_box(35, 100, 370, 250, "Four-cell outcome surface", [
        "A0 = W10 − W00",
        "A1 = W11 − W01",
        "ΔAD W = A1 − A0",
        "",
        "Four cells identify outcomes",
        "before they identify mechanism.",
    ], "dark"))

    b.append(_box(455, 90, 390, 160, "Level 1 — interaction relief", [
        "ΔAD W > 0",
        "Defence shifts A upward.",
        "A can remain harmful in both states.",
    ], "soft"))
    b.append(_box(455, 300, 390, 160, "Level 2 — constraint release", [
        "A0 ≤ 0 < A1",
        "A becomes beneficial with D.",
        "Stronger than interaction alone.",
    ], "soft"))
    b.append(_box(455, 510, 390, 160, "Level 3 — strict reversal", [
        "A0 < 0 < A1",
        "Negative-to-positive reversal.",
        "Strongest outcome claim.",
    ], "soft"))
    b.append(_arrow(650, 255, 650, 292))
    b.append(_arrow(650, 465, 650, 502))

    examples = [
        ("interaction only", "A0 = −0.8", "A1 = −0.2", "Δ = +0.6"),
        ("Level 2 boundary", "A0 = 0", "A1 = +0.3", "Δ = +0.3"),
        ("Level 3 reversal", "A0 = −0.2", "A1 = +0.3", "Δ = +0.5"),
    ]
    y = 120
    for title, a0, a1, delta in examples:
        b.append(_box(890, y, 360, 150, title, [a0, a1, delta], "box"))
        y += 205

    b.append('<text x="650" y="735" text-anchor="middle" class="sub">Level 3 ⇒ Level 2 ⇒ Level 1; reverse implications fail.</text>')
    return _svg(1300, 785, "".join(b))


def fig2() -> str:
    """Identified-set geometry and partial identification."""
    b = [
        '<text x="650" y="46" text-anchor="middle" class="title">The total interaction defines an identified set, not a unique mechanism</text>'
    ]
    b.append(_box(35, 105, 400, 245, "Mechanism accounting", [
        "ΔAD W = ρΔ − ιΔ − κΔ",
        "",
        "Let B = ρΔ − ιΔ.",
        "Observed total: δ",
        "B = δ + κΔ",
    ], "dark"))

    x0, y0, w, h = 500, 125, 735, 455
    b.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="box"/>')
    b.append('<text x="868" y="105" text-anchor="middle" class="sub">Projection of I(δ) onto (κΔ, ρΔ−ιΔ)</text>')
    b.append(f'<line x1="{x0+70}" y1="{y0+h-60}" x2="{x0+w-40}" y2="{y0+h-60}" class="line"/>')
    b.append(f'<line x1="{x0+70}" y1="{y0+h-60}" x2="{x0+70}" y2="{y0+40}" class="line"/>')
    b.append(f'<text x="{x0+w/2}" y="{y0+h-18}" text-anchor="middle" class="body">κΔ — remaining joint channel</text>')
    b.append(f'<text x="{x0+12}" y="{y0+42}" class="small">ρΔ−ιΔ</text>')
    b.append(f'<line x1="{x0+120}" y1="{y0+h-120}" x2="{x0+w-90}" y2="{y0+90}" class="line"/>')
    b.append(f'<text x="{x0+w-265}" y="{y0+105}" class="body">B = δ + κΔ</text>')
    k0 = x0 + 260
    b.append(f'<line x1="{k0}" y1="{y0+40}" x2="{k0}" y2="{y0+h-60}" class="dash"/>')
    b.append(f'<text x="{k0}" y="{y0+h-78}" text-anchor="middle" class="small">κΔ = 0</text>')
    b.append(f'<text x="{k0+165}" y="{y0+h-140}" text-anchor="middle" class="small">κΔ ≥ 0 ⇒ ρΔ−ιΔ ≥ δ</text>')

    b.append(_box(45, 395, 385, 195, "What new information does", [
        "Restriction → bound",
        "Bounded κ assay → segment",
        "Channel measure → smaller set",
        "Crossed design + assay → point",
    ], "soft"))
    b.append('<text x="650" y="650" text-anchor="middle" class="sub">More precision in δ alone does not collapse I(δ).</text>')
    b.append('<text x="650" y="695" text-anchor="middle" class="body">Identification improves only when biologically new information is added.</text>')
    return _svg(1300, 740, "".join(b))


def fig3() -> str:
    """Selective crossed consumer design, separability gate, and independent joint assay."""
    b = [
        '<text x="650" y="46" text-anchor="middle" class="title">Crossed intervention promotes interaction toward mechanism identification</text>'
    ]
    states = [
        ("G− / P−", 35, 105),
        ("G+ / P−", 355, 105),
        ("G− / P+", 675, 105),
        ("G+ / P+", 995, 105),
    ]
    for label, x, y in states:
        b.append(_box(x, y, 270, 195, label, [
            "same A×D contrast",
            "W00   W10",
            "W01   W11",
            "common outcome scale",
        ], "soft"))

    b.append(_box(55, 365, 365, 190, "Antagonist channel", [
        "G exclusion contrast",
        "→ ρΔ when selective",
        "",
        "Defence main effect ≠ ρΔ",
    ], "dark"))
    b.append(_box(468, 365, 365, 190, "Pollinator channel", [
        "P increment contrast",
        "→ ιΔinc",
        "correct with m0,Δ",
        "baseline is not assumed zero",
    ], "dark"))
    b.append(_box(880, 365, 365, 190, "Separability gate", [
        "A×D×G×P = 0?",
        "Non-zero ⇒ channel coupling",
        "depends on consumer state",
        "do not force one allocation",
    ], "dark"))

    b.append(_arrow(238, 580, 570, 645))
    b.append(_arrow(650, 580, 650, 645))
    b.append(_arrow(1062, 580, 730, 645))
    b.append(_box(330, 655, 640, 200, "Independent remaining-channel assay", [
        "Compare UΔ with an independent A×D assay.",
        "Agreement supports the proposed allocation.",
        "Disagreement diagnoses omitted biology,",
        "intervention failure, baseline error, or scale mismatch.",
    ], "box"))
    b.append('<text x="650" y="910" text-anchor="middle" class="sub">Residual by subtraction ≠ identified joint cost.</text>')
    return _svg(1300, 955, "".join(b))


def _xscale(value: float, x0: float = 610, lo: float = -1.8, hi: float = 1.3, width: float = 580) -> float:
    return x0 + (value - lo) / (hi - lo) * width


def fig4() -> str:
    """Source-backed fragmented-frontier figure with readable submission-scale labels."""
    rows = legacy._read_coverage()
    targets = legacy._impatiens_targets()
    counts = legacy._pattern_counts()
    if len(rows) != 17:
        raise ValueError(f"Expected 17 high-information systems, found {len(rows)}")
    expected = {
        "records": 56,
        "clusters": 25,
        "a_poll": 5,
        "a_ant": 8,
        "d_ant": 18,
        "d_poll": 10,
        "same": 14,
        "switch": 17,
    }
    if counts != expected:
        raise ValueError(f"Mechanism-pattern count drift: {counts!r}")

    b = ['<text x="650" y="46" text-anchor="middle" class="title">Recurrent pathways, fragmented mechanism identification</text>']
    b.append(_box(25, 95, 400, 215, "A×D face — Kessler 2008", [
        "benzylacetone × nicotine",
        "manipulated A×D-like factorial",
        "Δ ≈ +0.19 to +0.25",
        "missing selective G/P toggles",
    ], "dark"))
    b.append(_box(450, 95, 400, 215, "G×P face — Egan 2021", [
        "herbivory × pollination",
        "strong consumer factorial",
        "traits measured, not crossed",
        "missing manipulated floral A×D",
    ], "dark"))
    b.append(_box(875, 95, 400, 215, "A×G×Pₛ — Theis 2012", [
        "fragrance × beetle removal",
        "× supplemental pollination",
        "three-factor reproductive bridge",
        "missing distinct D axis",
    ], "dark"))
    b.append('<text x="650" y="355" text-anchor="middle" class="sub">The missing object is their intersection</text>')
    b.append(
        f'<text x="650" y="395" text-anchor="middle" class="small">'
        f'{counts["records"]} routes / {counts["clusters"]} clusters; A→P {counts["a_poll"]}; A→G {counts["a_ant"]}; '
        f'D→G {counts["d_ant"]}; D→P {counts["d_poll"]}</text>'
    )
    b.append(
        f'<text x="650" y="430" text-anchor="middle" class="small">'
        f'{len(rows)}-system audit; independent κ assay 0; full channel allocation 0</text>'
    )
    b.append('<text x="55" y="475" class="sub">Impatiens retrofit: observational A×D under randomized context modification</text>')

    x0, w = 610, 580
    for tick in [-1.5, -1.0, -0.5, 0, 0.5, 1.0]:
        x = _xscale(tick, x0=x0, width=w)
        b.append(f'<line x1="{x}" y1="505" x2="{x}" y2="870" class="dash"/>')
        b.append(f'<text x="{x}" y="898" text-anchor="middle" class="tiny">{tick:+.1f}</text>')

    label_map = {
        "A_z:D_z": "A×D",
        "A_z:D_z:Robbing_c": "A×D×Robbing",
        "A_z:D_z:Florivory_c": "A×D×Florivory",
        "A_z:D_z:Pollination_c": "A×D×Pollination",
    }
    order = ["A_z:D_z", "A_z:D_z:Robbing_c", "A_z:D_z:Florivory_c", "A_z:D_z:Pollination_c"]
    targets = sorted(targets, key=lambda r: (str(r["analysis"]), order.index(str(r["term"]))))
    y = 535
    last_analysis = None
    for r in targets:
        analysis = str(r["analysis"])
        if analysis != last_analysis:
            short = "CH fruits/day" if "fruit" in analysis.lower() and "seed" not in analysis.lower() else "seeds/CH fruit"
            b.append(f'<text x="55" y="{y}" class="small">{escape(short)}</text>')
            y += 30
            last_analysis = analysis
        lo = _xscale(float(r["lo"]), x0=x0, width=w)
        hi = _xscale(float(r["hi"]), x0=x0, width=w)
        est = _xscale(float(r["estimate"]), x0=x0, width=w)
        b.append(f'<text x="235" y="{y+6}" class="tiny">{escape(label_map.get(str(r["term"]), str(r["term"])))}</text>')
        b.append(f'<line x1="{lo}" y1="{y}" x2="{hi}" y2="{y}" class="line"/><circle cx="{est}" cy="{y}" r="6" fill="#222"/>')
        y += 42
    b.append('<text x="900" y="940" text-anchor="middle" class="small">All eight intervals cross zero: context modification is estimable but unresolved.</text>')
    return _svg(1300, 985, "".join(b))


def fig5() -> str:
    """Scientific ownership boundary: precondition, evolutionary transport, mechanism inference."""
    b = [
        '<text x="650" y="46" text-anchor="middle" class="title">Three distinct inference problems should not be collapsed</text>'
    ]
    b.append(_box(35, 115, 365, 300, "SCH — identify conflict", [
        "multifunctionality ≠ conflict",
        "state optimum ≠ pure-function optimum",
        "crossed promotion gate",
        "",
        "Output when justified:",
        "identified conflict / L",
    ], "soft"))
    b.append(_arrow(415, 260, 500, 260))
    b.append(_box(505, 95, 400, 340, "SLK — transport evolutionary value", [
        "L → R → Φ",
        "→ accessibility",
        "→ invasion",
        "→ fixation",
        "→ occupancy",
        "",
        "Global value ≠ realized evolution",
    ], "dark"))
    b.append(_arrow(920, 260, 995, 260))
    b.append(_box(1000, 115, 270, 300, "BITA — identify mechanism", [
        "observed A×D",
        "≠ mechanism",
        "identified set",
        "partial ID",
        "crossed intervention",
        "independent assay",
    ], "soft"))

    b.append('<text x="650" y="500" text-anchor="middle" class="sub">BITA promotion ladder</text>')
    steps = [
        "interaction",
        "identified set",
        "partial ID",
        "crossed intervention",
        "separability",
        "independent assay",
        "mechanism",
    ]
    x = 25
    widths = [145, 160, 135, 200, 155, 175, 140]
    for i, (step, width) in enumerate(zip(steps, widths)):
        b.append(f'<rect x="{x}" y="545" width="{width}" height="78" rx="12" class="box"/>')
        b.append(f'<text x="{x+width/2}" y="593" text-anchor="middle" class="small">{escape(step)}</text>')
        if i < len(steps) - 1:
            b.append(_arrow(x + width + 3, 584, x + width + 25, 584))
        x += width + 32

    b.append('<text x="650" y="695" text-anchor="middle" class="body">Architecture-value equations are programme context here, not BITA novelty claims.</text>')
    b.append('<text x="650" y="740" text-anchor="middle" class="body">BITA starts once multiple trait axes and their joint fitness effect are observed.</text>')
    return _svg(1300, 790, "".join(b))


FIGURE_NAMES = [
    "FIGURE_1_OUTCOME_PROMOTION.svg",
    "FIGURE_2_IDENTIFIED_SET.svg",
    "FIGURE_3_CROSSED_INTERVENTION.svg",
    "FIGURE_4_FRAGMENTED_FRONTIER.svg",
    "FIGURE_5_INFERENCE_BOUNDARIES.svg",
]


def build(out_dir: Path = OUT) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    svgs = [fig1(), fig2(), fig3(), fig4(), fig5()]
    paths: list[Path] = []
    for name, svg in zip(FIGURE_NAMES, svgs):
        path = out_dir / name
        path.write_text(svg, encoding="utf-8")
        paths.append(path)
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=OUT)
    args = parser.parse_args(argv)
    for path in build(args.out_dir):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
