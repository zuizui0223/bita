"""Build Ecology Letters access-routing Letter Figures 1 and 3 as SVG."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "submission" / "access_routing_letter_figures"
RESULT = ROOT / "empirical" / "floral_defence_selectivity" / "results" / "joint_access_routing.json"


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
    width, height = 1500, 880
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(750, 46, "Figure 1. Access constraints reroute exploitation", size=30, anchor="middle", weight="bold"),
        _text(750, 80, "A barrier can change interaction mode instead of simply removing interaction", size=18, anchor="middle"),
        _text(65, 145, "A", size=22, weight="bold"),
        _text(105, 145, "Low mismatch: legitimate route remains usable", size=21, weight="bold"),
        '<ellipse cx="355" cy="280" rx="150" ry="82" fill="#f5f5f5" stroke="#222" stroke-width="2"/>',
        '<rect x="325" y="198" width="60" height="88" fill="#dddddd" stroke="#222" stroke-width="2"/>',
        _text(355, 247, "opening", size=15, anchor="middle", weight="bold"),
        _text(130, 280, "visitor", size=17, anchor="middle", weight="bold"),
    ]
    parts.extend(_arrow(180, 280, 315, 280))
    parts.extend([
        _text(245, 263, "legitimate route", size=14, anchor="middle"),
        _text(625, 270, "reward reached through normal opening", size=17, weight="bold"),
        _text(625, 302, "filtering may reduce exploitation without forcing bypass", size=15),
        _text(65, 455, "B", size=22, weight="bold"),
        _text(105, 455, "High mismatch: legitimate route constrained, bypass remains", size=21, weight="bold"),
        '<ellipse cx="355" cy="610" rx="150" ry="82" fill="#f5f5f5" stroke="#222" stroke-width="2"/>',
        '<rect x="325" y="528" width="60" height="88" fill="#dddddd" stroke="#222" stroke-width="2"/>',
        _text(355, 577, "opening", size=15, anchor="middle", weight="bold"),
        _text(130, 610, "visitor", size=17, anchor="middle", weight="bold"),
        _line(180, 610, 305, 610, width=2, dash="8 6"),
        _text(245, 593, "constrained route", size=14, anchor="middle"),
        '<path d="M 180 635 C 250 730, 380 735, 505 635" fill="none" stroke="#222" stroke-width="3" stroke-dasharray="9 6"/>',
        _text(345, 735, "bypass / robbing", size=16, anchor="middle", weight="bold"),
        _text(625, 590, "mismatch ↑", size=18, weight="bold"),
        _text(625, 625, "legitimate access ↓", size=18),
        _text(625, 660, "relative bypass use ↑", size=18, weight="bold"),
        '<rect x="1010" y="185" width="405" height="505" rx="16" fill="#fafafa" stroke="#444" stroke-width="2"/>',
        _text(1035, 225, "General prediction", size=21, weight="bold"),
        _text(1210, 285, "access mismatch", size=18, anchor="middle", weight="bold"),
        _text(1210, 330, "↓", size=24, anchor="middle"),
        _text(1210, 377, "legitimate-route feasibility", size=17, anchor="middle"),
        _text(1210, 422, "↓", size=24, anchor="middle"),
        _text(1210, 468, "bypass propensity", size=18, anchor="middle", weight="bold"),
        _text(1035, 535, "Filtering outcome:", size=16, weight="bold"),
        _text(1060, 566, "interaction decreases", size=15),
        _text(1035, 615, "Rerouting outcome:", size=16, weight="bold"),
        _text(1060, 646, "interaction mode changes", size=15),
        _text(750, 835, "Prediction tested independently in an insect flower-visitor network and a bird–flower network.", size=15, anchor="middle"),
        "</svg>",
    ])
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
        ("Aubert / EPHI birds", a, "1,378 pair-site units; site-adjusted"),
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
        _text(747, 684, "shuffle robbery ranks", size=15, anchor="middle"),
        _text(747, 711, "within site", size=15, anchor="middle"),
        '<rect x="1005" y="615" width="385" height="120" rx="12" fill="#fafafa" stroke="#555"/>',
        _text(1197, 650, "Joint", size=17, anchor="middle", weight="bold"),
        _text(1197, 684, "Fisher-z mean", size=15, anchor="middle"),
        _text(1197, 711, "equal network weight", size=15, anchor="middle"),
        _text(60, 795, "C", size=22, weight="bold"),
        _text(100, 795, "Independent mechanistic corroboration", size=21, weight="bold"),
        _text(120, 835, "17 D-side study programs", size=16, weight="bold"),
        _text(535, 835, "11 / 11 scorable domain states aligned", size=16, weight="bold"),
        _text(1035, 835, "8 within-D switching systems", size=16, weight="bold"),
        _text(750, 880, "Joint network inference is primary; literature-based evidence supports interpretation and is not pooled into the network effect.", size=13, anchor="middle"),
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
