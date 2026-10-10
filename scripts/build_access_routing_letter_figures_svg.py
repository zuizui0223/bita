"""Build Ecology Letters access-routing Letter Figures 1 and 3 as SVG."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "submission" / "access_routing_letter_figures"
RESULT = ROOT / "empirical" / "floral_defence_selectivity" / "results" / "joint_access_routing_species_robust.json"


def _text(
    x: float,
    y: float,
    value: object,
    *,
    size: int = 18,
    anchor: str = "start",
    weight: str = "normal",
    fill: str = "#111",
) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="DejaVu Sans,Arial,sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
        f'fill="{fill}">{escape(str(value))}</text>'
    )


def _line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    width: float = 2.0,
    dash: str | None = None,
) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="#222" stroke-width="{width}"{extra}/>'
    )


def _arrow(x1: float, y1: float, x2: float, y2: float, *, width: float = 3.0) -> list[str]:
    parts = [_line(x1, y1, x2, y2, width=width)]
    # Simple rightward arrowhead; all uses in these figures are horizontal.
    parts.append(
        f'<path d="M {x2} {y2} l -14 -8 l 0 16 z" fill="#222"/>'
    )
    return parts


def build_figure1() -> str:
    width, height = 1500, 900
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(750, 46, "Figure 1. Higher robbery share can arise by different biological routes", size=29, anchor="middle", weight="bold"),
        _text(750, 80, "Composition alone cannot distinguish more robbery from loss of legitimate interaction", size=17, anchor="middle"),

        # Baseline
        '<rect x="70" y="125" width="410" height="235" rx="15" fill="#fafafa" stroke="#444" stroke-width="2"/>',
        _text(95, 160, "A  Baseline", size=21, weight="bold"),
        _text(95, 195, "Illustrative interaction counts", size=14),
        _text(95, 235, "legitimate", size=15, weight="bold"),
        '<rect x="195" y="215" width="225" height="25" fill="#dddddd" stroke="#555"/>',
        _text(430, 234, "90", size=15, weight="bold"),
        _text(95, 285, "robbery", size=15, weight="bold"),
        '<rect x="195" y="265" width="25" height="25" fill="#777777" stroke="#333"/>',
        _text(230, 284, "10", size=15, weight="bold"),
        _text(275, 330, "robbery share = 10%", size=18, anchor="middle", weight="bold"),

        # Numerator-driven scenario
        '<rect x="545" y="125" width="410" height="235" rx="15" fill="#fafafa" stroke="#444" stroke-width="2"/>',
        _text(570, 160, "B  More robbery", size=21, weight="bold"),
        _text(570, 195, "legitimate unchanged; robbery increases", size=14),
        _text(570, 235, "legitimate", size=15, weight="bold"),
        '<rect x="670" y="215" width="225" height="25" fill="#dddddd" stroke="#555"/>',
        _text(905, 234, "90", size=15, weight="bold"),
        _text(570, 285, "robbery", size=15, weight="bold"),
        '<rect x="670" y="265" width="112.5" height="25" fill="#777777" stroke="#333"/>',
        _text(795, 284, "45 ↑", size=15, weight="bold"),
        _text(750, 330, "robbery share = 33%", size=18, anchor="middle", weight="bold"),

        # Denominator-loss scenario
        '<rect x="1020" y="125" width="410" height="235" rx="15" fill="#fafafa" stroke="#444" stroke-width="2"/>',
        _text(1045, 160, "C  Loss of legitimate interaction", size=21, weight="bold"),
        _text(1045, 195, "robbery need not increase", size=14),
        _text(1045, 235, "legitimate", size=15, weight="bold"),
        '<rect x="1145" y="215" width="25" height="25" fill="#dddddd" stroke="#555"/>',
        _text(1180, 234, "10 ↓", size=15, weight="bold"),
        _text(1045, 285, "robbery", size=15, weight="bold"),
        '<rect x="1145" y="265" width="20" height="25" fill="#777777" stroke="#333"/>',
        _text(1175, 284, "8 ↓", size=15, weight="bold"),
        _text(1225, 330, "robbery share = 44% ↑", size=18, anchor="middle", weight="bold"),

        _text(750, 405, "Both B and C produce higher robbery prevalence, but they imply different ecology.", size=18, anchor="middle", weight="bold"),
        _text(750, 438, "Only zero-inclusive route-specific rates distinguish them.", size=17, anchor="middle"),

        # Ecuador empirical result
        '<rect x="160" y="485" width="1180" height="310" rx="18" fill="#f7f7f7" stroke="#333" stroke-width="2"/>',
        _text(190, 525, "D  Ecuador: post-open 1.8× effective-reach sensitivity", size=22, weight="bold"),
        _text(190, 565, "same constructed opportunities; route-specific fit supports differ", size=14),

        _text(215, 625, "legitimate feeding", size=17, weight="bold"),
        _text(470, 625, "RR = 0.154", size=20, weight="bold"),
        _text(650, 625, "95% CI 0.087–0.271", size=16),
        _text(215, 680, "robbery", size=17, weight="bold"),
        _text(470, 680, "RR = 0.816", size=20, weight="bold"),
        _text(650, 680, "95% CI 0.358–1.860", size=16),

        '<rect x="925" y="585" width="360" height="125" rx="12" fill="white" stroke="#555" stroke-width="1.5"/>',
        _text(1105, 620, "ratio of separately fitted RRs", size=15, anchor="middle", weight="bold"),
        _text(1105, 660, "5.31  (1.92–14.67)", size=23, anchor="middle", weight="bold"),
        _text(1105, 693, "different FE supports; descriptive", size=12, anchor="middle"),

        _text(750, 750, "Observed pattern: strong loss of legitimate feeding; no detectable increase in robbery.", size=18, anchor="middle", weight="bold"),
        _text(750, 780, "Interpretation is observational and the 1.8× reach analysis is explicitly post-open.", size=14, anchor="middle"),

        _text(750, 855, "Illustrative counts in A–C are schematic; panel D reports the Ecuadorian estimates.", size=13, anchor="middle"),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"

def _scale(value: float, lo: float, hi: float, x0: float, x1: float) -> float:
    return x0 + (value - lo) / (hi - lo) * (x1 - x0)


def build_figure3(result: dict[str, object]) -> str:
    width, height = 1500, 910
    effects = result["network_effects"]
    s = float(effects["sakhalkar"]["rho"])
    a = float(effects["aubert_ephi"]["rho"])
    j = float(result["joint_equal_network_fisher_z_rho"])
    p = float(result["joint_permutation_p_two_sided"])

    x0, x1 = 235, 1080
    lo, hi = 0.0, 0.5
    rows = [
        ("Sakhalkar insects", s, "57 plant species"),
        ("Aubert / EPHI birds", a, "259 plant species; missing-as-no"),
        ("equal-network joint", j, "Fisher-z mean; equal network weight"),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(750, 46, "Figure 3. One standardized routing effect recurs across networks", size=29, anchor="middle", weight="bold"),
        _text(750, 80, "Each network contributes one rank association; raw observations are not pooled", size=17, anchor="middle"),
        _text(60, 135, "A", size=22, weight="bold"),
        _text(100, 135, "Observed standardized effects", size=21, weight="bold"),
        _line(x0, 220, x1, 220, width=2.5),
        _text(x0, 252, "0.0", size=13, anchor="middle"),
        _text(_scale(0.1,lo,hi,x0,x1), 252, "0.1", size=13, anchor="middle"),
        _text(_scale(0.2,lo,hi,x0,x1), 252, "0.2", size=13, anchor="middle"),
        _text(_scale(0.3,lo,hi,x0,x1), 252, "0.3", size=13, anchor="middle"),
        _text(_scale(0.4,lo,hi,x0,x1), 252, "0.4", size=13, anchor="middle"),
        _text(x1, 252, "0.5", size=13, anchor="middle"),
        _text((x0+x1)/2, 282, "rank association: access constraint → bypass propensity", size=15, anchor="middle"),
    ]
    y_values = [330, 405, 480]
    for (label, effect, note), y in zip(rows, y_values):
        x = _scale(effect, lo, hi, x0, x1)
        parts.append(_text(205, y+5, label, size=16, anchor="end", weight="bold" if "joint" in label else "normal"))
        parts.append(f'<circle cx="{x:.2f}" cy="{y}" r="9" fill="#555" stroke="#111" stroke-width="1.5"/>')
        parts.append(_text(x+18, y+5, f"{effect:.3f}", size=16, weight="bold"))
        parts.append(_text(1130, y+5, note, size=13))
    parts.extend([
        '<rect x="1110" y="170" width="330" height="120" rx="12" fill="#f7f7f7" stroke="#555" stroke-width="1.5"/>',
        _text(1275, 205, f"joint ρ = {j:.3f}", size=20, anchor="middle", weight="bold"),
        _text(1275, 240, f"permutation p = {p:.4f}", size=18, anchor="middle", weight="bold"),
        _text(1275, 272, "2 / 2 networks positive", size=14, anchor="middle"),
        _text(60, 585, "B", size=22, weight="bold"),
        _text(100, 585, "Structure-preserving permutation", size=21, weight="bold"),
        '<rect x="105" y="615" width="385" height="120" rx="12" fill="#fafafa" stroke="#555"/>',
        _text(297, 650, "Sakhalkar", size=17, anchor="middle", weight="bold"),
        _text(297, 684, "shuffle route response", size=15, anchor="middle"),
        _text(297, 711, "across plant species", size=15, anchor="middle"),
        '<rect x="555" y="615" width="385" height="120" rx="12" fill="#fafafa" stroke="#555"/>',
        _text(747, 650, "Aubert / EPHI", size=17, anchor="middle", weight="bold"),
        _text(747, 684, "shuffle response ranks", size=15, anchor="middle"),
        _text(747, 711, "across plant species", size=15, anchor="middle"),
        '<rect x="1005" y="615" width="385" height="120" rx="12" fill="#fafafa" stroke="#555"/>',
        _text(1197, 650, "Joint", size=17, anchor="middle", weight="bold"),
        _text(1197, 684, "Fisher-z mean", size=15, anchor="middle"),
        _text(1197, 711, "equal network weight", size=15, anchor="middle"),
        _text(60, 795, "C", size=22, weight="bold"),
        _text(100, 795, "What direct geometry studies can identify", size=21, weight="bold"),
        _text(120, 832, "Frozen 33-program direct frame", size=15, weight="bold"),
        _text(120, 860, "7  zero-inclusive both-route rates", size=15, weight="bold"),
        _text(455, 860, "18  robbery-prevalence only", size=15),
        _text(785, 860, "6  conditional route choice", size=15),
        _text(1110, 860, "1 + 1  other non-strict designs", size=15),
        _text(750, 892, "Post-hoc finite-frame design audit; not literature prevalence and not an increment to network k.", size=13, anchor="middle"),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def write_figures(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    payloads = {
        "FIGURE_1_ACCESS_ROUTING_HYPOTHESIS.svg": build_figure1(),
        "FIGURE_3_JOINT_ACCESS_ROUTING.svg": build_figure3(result),
    }
    paths: list[Path] = []
    for name, svg in payloads.items():
        path = out_dir / name
        path.write_text(svg, encoding="utf-8")
        paths.append(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    for path in write_figures(args.output_dir):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
