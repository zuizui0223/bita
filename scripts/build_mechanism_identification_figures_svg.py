"""Build the five Main SVG figures for the active BITA mechanism-identification paper.

Figures 1-4 are delegated to the frozen source-backed implementation copied into
``build_mechanism_identification_figures_svg_base.py``. Figure 5 is kept here as
the publication-facing ownership diagram so the graphic matches the frozen
programme closure: SCH feeds identified conflict into SLK, whereas BITA is an
orthogonal mechanism-identification programme rather than a downstream SLK gate.
"""
from __future__ import annotations

import argparse
from pathlib import Path

try:  # package import in tests / repository-root execution
    from scripts import build_mechanism_identification_figures_svg_base as base
except ImportError:  # pragma: no cover - direct script execution path
    import build_mechanism_identification_figures_svg_base as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "mechanism_identification_figures"

_svg = base._svg
_box = base._box
_arrow = base._arrow

fig1 = base.fig1
fig2 = base.fig2
fig3 = base.fig3
fig4 = base.fig4


def fig5() -> str:
    """Show SCH->SLK transport and BITA as an orthogonal identification track."""
    b = [
        '<text x="650" y="46" text-anchor="middle" class="title">Three distinct inference problems should not be collapsed</text>'
    ]

    # The only cross-paper transport arrow is SCH -> SLK: a conflict budget is
    # exported downstream only after the SCH identification gate is passed.
    b.append(_box(35, 115, 345, 300, "SCH — identify conflict", [
        "multifunctionality ≠ conflict",
        "state optimum ≠ pure-function optimum",
        "crossed promotion gate",
        "",
        "Output when justified:",
        "identified conflict / L",
    ], "soft"))
    b.append(_arrow(390, 265, 440, 265))
    b.append('<text x="415" y="225" text-anchor="middle" class="tiny">exports identified L</text>')

    b.append(_box(450, 95, 420, 340, "SLK — transport evolutionary value", [
        "L → R → Φ",
        "→ accessibility",
        "→ invasion",
        "→ fixation",
        "→ occupancy",
        "",
        "Global value ≠ realized evolution",
    ], "dark"))

    # BITA is intentionally not connected to SLK by a transport arrow. The
    # dashed separator makes the orthogonal inference problem explicit.
    b.append('<line x1="910" y1="82" x2="910" y2="445" class="dash"/>')
    b.append('<text x="1085" y="78" text-anchor="middle" class="small">orthogonal mechanism-identification track</text>')
    b.append(_box(945, 115, 320, 300, "BITA — identify mechanism", [
        "observed A×D",
        "≠ mechanism",
        "identified set",
        "partial ID",
        "crossed intervention",
        "independent assay",
    ], "soft"))

    b.append('<text x="455" y="475" text-anchor="middle" class="small">SCH → SLK: identified conflict → evolutionary realization</text>')
    b.append('<text x="1080" y="475" text-anchor="middle" class="small">BITA: observed interaction → mechanism allocation</text>')

    b.append('<text x="650" y="525" text-anchor="middle" class="sub">BITA promotion ladder</text>')
    steps = [
        "interaction",
        "identified set",
        "partial ID",
        "crossed intervention",
        "separability",
        "independent assay",
        "mechanism",
    ]
    widths = [120, 150, 120, 175, 130, 155, 120]
    x = 90
    gap = 25
    for i, (step, width) in enumerate(zip(steps, widths)):
        b.append(f'<rect x="{x}" y="555" width="{width}" height="78" rx="12" class="box"/>')
        b.append(f'<text x="{x+width/2}" y="603" text-anchor="middle" class="small">{base.escape(step)}</text>')
        if i < len(steps) - 1:
            b.append(_arrow(x + width + 3, 594, x + width + gap - 3, 594))
        x += width + gap

    b.append('<text x="650" y="695" text-anchor="middle" class="body">Architecture-value equations are programme context here, not BITA novelty claims.</text>')
    b.append('<text x="650" y="740" text-anchor="middle" class="body">BITA starts from an observed joint trait effect and asks what mechanism generated it.</text>')
    return _svg(1300, 790, "".join(b))


FIGURE_NAMES = base.FIGURE_NAMES


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
