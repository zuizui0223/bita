"""Build the five Main SVG figures for the active BITA mechanism-identification paper.

The active paper is organized around the inference boundary

    trait interaction != ecological mechanism

and no longer uses the architecture-value figures as its Main sequence.  Figure 4
reuses the source-backed empirical frontier renderer from the mature identification
figure builder so the 17-system V2 audit and the 56-route / 25-cluster recurrence
counts remain data-driven rather than copied into artwork by hand.
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

STYLE = legacy.STYLE
_svg = legacy._svg
_box = legacy._box


def _arrow(x1: int, y1: int, x2: int, y2: int) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line"/>'
        f'<polygon points="{x2},{y2} {x2-14},{y2-8} {x2-14},{y2+8}" fill="#222"/>'
    )


def fig1() -> str:
    """Outcome-level promotion: interaction relief is weaker than release/reversal."""
    b = [
        '<text x="650" y="42" text-anchor="middle" class="title">A positive trait interaction is not yet functional release</text>'
    ]
    b.append(_box(45, 90, 360, 245, "Four-cell outcome surface", [
        "A0 = W10 − W00",
        "A1 = W11 − W01",
        "ΔAD W = A1 − A0",
        "",
        "The four cells identify outcomes",
        "before they identify mechanism.",
    ], "dark"))

    b.append(_box(470, 85, 360, 155, "Level 1 — interaction relief", [
        "ΔAD W > 0",
        "Defence shifts the A effect upward.",
        "A can still be harmful in both states.",
    ], "soft"))
    b.append(_box(470, 285, 360, 155, "Level 2 — constraint release", [
        "A0 ≤ 0 < A1",
        "A becomes beneficial with D.",
        "Stronger than positive interaction alone.",
    ], "soft"))
    b.append(_box(470, 485, 360, 155, "Level 3 — strict reversal", [
        "A0 < 0 < A1",
        "Negative-to-positive sign reversal.",
        "Strongest outcome claim in the ladder.",
    ], "soft"))
    b.append(_arrow(650, 245, 650, 280))
    b.append(_arrow(650, 445, 650, 480))

    examples = [
        ("positive interaction only", "A0 = −0.8", "A1 = −0.2", "Δ = +0.6"),
        ("Level 2 boundary", "A0 = 0", "A1 = +0.3", "Δ = +0.3"),
        ("Level 3 reversal", "A0 = −0.2", "A1 = +0.3", "Δ = +0.5"),
    ]
    y = 120
    for title, a0, a1, delta in examples:
        b.append(_box(880, y, 360, 145, title, [a0, a1, delta], "box"))
        y += 190

    b.append('<text x="650" y="705" text-anchor="middle" class="sub">Level 3 ⇒ Level 2 ⇒ Level 1; the reverse implications fail.</text>')
    return _svg(1300, 750, "".join(b))


def fig2() -> str:
    """Identified-set geometry and partial identification."""
    b = [
        '<text x="650" y="42" text-anchor="middle" class="title">The total interaction defines an identified set, not a unique mechanism</text>'
    ]
    b.append(_box(45, 90, 395, 230, "Mechanism accounting", [
        "ΔAD W = ρΔ − ιΔ − κΔ",
        "",
        "Let B = ρΔ − ιΔ.",
        "For observed δ:",
        "B = δ + κΔ",
    ], "dark"))

    # Panel A: projection of the identified plane onto (kappa, rho-iota).
    x0, y0, w, h = 515, 115, 700, 450
    b.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="box"/>')
    b.append('<text x="865" y="95" text-anchor="middle" class="sub">Projection of I(δ) onto (κΔ, ρΔ−ιΔ)</text>')
    # axes
    b.append(f'<line x1="{x0+65}" y1="{y0+h-55}" x2="{x0+w-35}" y2="{y0+h-55}" class="line"/>')
    b.append(f'<line x1="{x0+65}" y1="{y0+h-55}" x2="{x0+65}" y2="{y0+35}" class="line"/>')
    b.append(f'<text x="{x0+w/2}" y="{y0+h-15}" text-anchor="middle" class="body">κΔ — remaining joint channel</text>')
    b.append(f'<text x="{x0+10}" y="{y0+35}" class="small">ρΔ−ιΔ</text>')
    # line B=delta+kappa
    b.append(f'<line x1="{x0+110}" y1="{y0+h-110}" x2="{x0+w-80}" y2="{y0+85}" class="line"/>')
    b.append(f'<text x="{x0+w-250}" y="{y0+100}" class="body">B = δ + κΔ</text>')
    # kappa=0 boundary
    k0 = x0 + 245
    b.append(f'<line x1="{k0}" y1="{y0+35}" x2="{k0}" y2="{y0+h-55}" class="dash"/>')
    b.append(f'<text x="{k0}" y="{y0+h-70}" text-anchor="middle" class="small">κΔ = 0</text>')
    b.append(f'<text x="{k0+135}" y="{y0+h-125}" text-anchor="middle" class="small">κΔ ≥ 0 ⇒ ρΔ−ιΔ ≥ δ</text>')

    b.append(_box(55, 365, 380, 155, "What extra information does", [
        "Restriction only → half-line / bound",
        "Bounded κ assay → finite segment",
        "Selective channel measure → smaller set",
        "Full crossed design + assay → point target",
    ], "soft"))
    b.append('<text x="650" y="625" text-anchor="middle" class="sub">More precision in δ alone does not collapse I(δ).</text>')
    b.append('<text x="650" y="663" text-anchor="middle" class="body">Identification improves only when biologically new information is added.</text>')
    return _svg(1300, 710, "".join(b))


def fig3() -> str:
    """Selective crossed consumer design, separability gate, and independent joint assay."""
    b = [
        '<text x="650" y="42" text-anchor="middle" class="title">Crossed intervention promotes interaction toward mechanism identification</text>'
    ]
    states = [
        ("G− / P−", 55, 95),
        ("G+ / P−", 365, 95),
        ("G− / P+", 675, 95),
        ("G+ / P+", 985, 95),
    ]
    for label, x, y in states:
        b.append(_box(x, y, 260, 190, label, [
            "same A×D contrast",
            "W00 W10",
            "W01 W11",
            "common outcome scale",
        ], "soft"))

    b.append(_box(80, 350, 340, 180, "Antagonist channel", [
        "G exclusion contrast",
        "→ ρΔ when selective",
        "",
        "Main-effect defence ≠ ρΔ",
    ], "dark"))
    b.append(_box(480, 350, 340, 180, "Pollinator channel", [
        "P increment contrast",
        "→ ιΔinc",
        "correct with m0,Δ",
        "Do not assume baseline = 0",
    ], "dark"))
    b.append(_box(880, 350, 340, 180, "Separability gate", [
        "A×D×G×P = 0?",
        "Non-zero ⇒ channels depend",
        "on alternate consumer state",
        "Do not force one allocation",
    ], "dark"))

    b.append(_arrow(250, 555, 585, 610))
    b.append(_arrow(650, 555, 650, 610))
    b.append(_arrow(1050, 555, 715, 610))
    b.append(_box(355, 620, 590, 155, "Independent remaining-channel assay", [
        "Compare UΔ = ρΔ − ιΔ − ΔAD W with an independently measured A×D channel.",
        "Agreement supports the proposed allocation; disagreement diagnoses omitted biology,",
        "intervention failure, baseline error, or scale mismatch.",
    ], "box"))
    b.append('<text x="650" y="825" text-anchor="middle" class="sub">Residual by subtraction ≠ identified joint cost.</text>')
    return _svg(1300, 865, "".join(b))


def fig4() -> str:
    """Source-backed fragmented-frontier figure from the mature identification builder."""
    rows = legacy._read_coverage()
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
    return legacy.fig4()


def fig5() -> str:
    """Scientific ownership boundary: precondition, evolutionary transport, mechanism inference."""
    b = [
        '<text x="650" y="42" text-anchor="middle" class="title">Three distinct inference problems should not be collapsed</text>'
    ]
    b.append(_box(60, 105, 350, 285, "SCH — identify conflict", [
        "multifunctionality ≠ conflict",
        "state optimum ≠ pure-function optimum",
        "crossed promotion gate",
        "",
        "Output when justified:",
        "identified conflict / L",
    ], "soft"))
    b.append(_arrow(425, 245, 500, 245))
    b.append(_box(505, 85, 390, 325, "SLK — transport evolutionary value", [
        "L → R → Φ",
        "→ accessibility",
        "→ invasion",
        "→ fixation",
        "→ occupancy",
        "",
        "Global value ≠ realized evolution",
    ], "dark"))
    b.append(_arrow(910, 245, 985, 245))
    b.append(_box(990, 105, 250, 285, "BITA — identify mechanism", [
        "observed A×D",
        "≠ mechanism",
        "identified set",
        "partial ID",
        "crossed intervention",
        "independent assay",
    ], "soft"))

    b.append('<text x="650" y="475" text-anchor="middle" class="sub">BITA promotion ladder</text>')
    steps = [
        "interaction",
        "identified set",
        "partial ID",
        "crossed intervention",
        "separability",
        "independent assay",
        "mechanism",
    ]
    x = 45
    widths = [135, 155, 130, 190, 145, 165, 130]
    for i, (step, width) in enumerate(zip(steps, widths)):
        b.append(f'<rect x="{x}" y="520" width="{width}" height="70" rx="12" class="box"/>')
        b.append(f'<text x="{x+width/2}" y="562" text-anchor="middle" class="small">{escape(step)}</text>')
        if i < len(steps) - 1:
            b.append(_arrow(x + width + 4, 555, x + width + 28, 555))
        x += width + 35

    b.append('<text x="650" y="660" text-anchor="middle" class="body">Architecture-value equations are programme context here, not BITA novelty claims.</text>')
    b.append('<text x="650" y="700" text-anchor="middle" class="body">The active BITA question starts once multiple trait axes and their joint fitness effect are observed.</text>')
    return _svg(1300, 750, "".join(b))


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
