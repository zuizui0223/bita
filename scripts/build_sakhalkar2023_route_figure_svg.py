"""Build candidate BITA Figure 4 from the public Sakhalkar et al. 2023 workbook."""

from __future__ import annotations

import argparse
import json
import math
import sys
from html import escape
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_sakhalkar2023_network import (
    _find_workbook,
    analyze_workbook,
    species_route_points,
)
from scripts.audit_sakhalkar2023_zenodo import _download, read_xlsx_sheet_rows


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT
    / "manuscript"
    / "figures_macro_candidate"
    / "FIGURE_4_TWO_NETWORK_ACCESS_ROUTING.svg"
)
AUBERT_RESULT = ROOT / "empirical" / "floral_defence_selectivity" / "results" / "aubert2026_zenodo_extension.json"


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


def _scale(value: float, lo: float, hi: float, start: float, end: float) -> float:
    if not math.isfinite(value):
        raise ValueError("non-finite plot value")
    if hi <= lo:
        return (start + end) / 2
    return start + (value - lo) / (hi - lo) * (end - start)


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def build_svg(
    points: list[dict[str, float | str]],
    result: dict[str, object],
    aubert: dict[str, object] | None = None,
) -> str:
    if not points:
        raise ValueError("cannot build Figure 4 without species-level route points")

    width, height = 1840, 1040
    plot_x0, plot_x1 = 120, 1050
    plot_y0, plot_y1 = 155, 680
    tubes = [float(point["tube_length"]) for point in points]
    lo, hi = min(tubes), max(tubes)
    pad = max((hi - lo) * 0.05, 0.05)
    xlo, xhi = max(0.0, lo - pad), hi + pad

    stats = result["tube_length_cheating_mode_balance"]
    rho = float(stats["spearman_rho"])
    pval = float(stats["permutation_p_two_sided"])
    n_species = int(stats["n_species"])

    class_fill = {
        "robber_only": "#b24a4a",
        "thief_only": "#4777a8",
        "mixed": "#777777",
    }

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(920, 42, "Figure 4. Access geometry predicts exploitation route in two independent networks", size=28, anchor="middle", weight="bold"),
        _text(920, 76, "Afrotropical insect cheating modes + Ecuadorian bird–flower access barriers", size=17, anchor="middle"),
        _text(120, 120, "A  Sakhalkar 2023 — plant-level robbing versus thieving", size=20, weight="bold"),
        f'<rect x="{plot_x0}" y="{plot_y0}" width="{plot_x1-plot_x0}" height="{plot_y1-plot_y0}" fill="#fafafa" stroke="#222" stroke-width="2"/>',
    ]

    for balance, label in [(-1.0, "thieving only"), (0.0, "equal balance"), (1.0, "robbing only")]:
        y = _scale(balance, -1.0, 1.0, plot_y1, plot_y0)
        parts.append(
            f'<line x1="{plot_x0}" y1="{y}" x2="{plot_x1}" y2="{y}" '
            'stroke="#bbbbbb" stroke-width="1.4" stroke-dasharray="6 5"/>'
        )
        parts.append(_text(plot_x0 - 12, y + 5, label, size=13, anchor="end"))

    for i in range(6):
        value = xlo + (xhi - xlo) * i / 5
        x = _scale(value, xlo, xhi, plot_x0, plot_x1)
        parts.append(f'<line x1="{x}" y1="{plot_y1}" x2="{x}" y2="{plot_y1+7}" stroke="#222"/>')
        parts.append(_text(x, plot_y1 + 27, f"{value:.2f}", size=12, anchor="middle"))

    for point in points:
        x = _scale(float(point["tube_length"]), xlo, xhi, plot_x0, plot_x1)
        y = _scale(float(point["balance"]), -1.0, 1.0, plot_y1, plot_y0)
        route_class = str(point["route_class"])
        fill = class_fill.get(route_class, "#777")
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.2" fill="{fill}" '
            'fill-opacity="0.72" stroke="#222" stroke-width="0.6"/>'
        )

    parts.extend([
        _text(plot_x1 - 12, plot_y0 + 28, "B = (R − T)/(R + T)", size=14, anchor="end"),
        _text((plot_x0 + plot_x1) / 2, plot_y1 + 58, "tube length (source trait scale)", size=16, anchor="middle"),
        _text(140, 756, f"n = {n_species} species", size=17, weight="bold"),
        _text(345, 756, f"rho = {rho:.3f}", size=17, weight="bold"),
        _text(510, 756, f"permutation p = {pval:.4f}", size=17, weight="bold"),
        _text(140, 782, "Plant species are inferential units; individual visits are not treated as replicates.", size=13),
    ])

    legend_y = 825
    for i, (key, label) in enumerate([
        ("robber_only", "robber-only"),
        ("mixed", "mixed robbing + thieving"),
        ("thief_only", "thief-only"),
    ]):
        x = 140 + i * 245
        parts.append(f'<circle cx="{x}" cy="{legend_y}" r="6" fill="{class_fill[key]}" stroke="#222"/>')
        parts.append(_text(x + 14, legend_y + 5, label, size=14))

    # Sakhalkar descriptive box
    parts.extend([
        '<rect x="1090" y="112" width="700" height="172" rx="14" fill="#f7f7f7" stroke="#444" stroke-width="2"/>',
        _text(1115, 143, "Sakhalkar route-specific contrast", size=18, weight="bold"),
        _text(1115, 181, f'robber-only median = {float(result["median_tube_length_robber_only"]):.3f}', size=16, weight="bold", fill="#8c2d2d"),
        _text(1115, 213, f'thief-only median = {float(result["median_tube_length_thief_only"]):.3f}', size=16, weight="bold", fill="#315f8c"),
        _text(1115, 249, "Multitrait sensitivity: tube-length block p = 0.211; no unique partial-effect claim.", size=13, fill="#555"),
    ])

    if aubert is not None:
        site = aubert["site_difference"]
        barrier_rate = float(aubert["mean_robbery_rate_barrier"])
        accessible_rate = float(aubert["mean_robbery_rate_accessible"])
        max_rate = max(0.35, barrier_rate * 1.12)
        bar_x0, bar_w = 1260, 440
        barrier_w = bar_w * barrier_rate / max_rate
        accessible_w = bar_w * accessible_rate / max_rate

        parts.extend([
            _text(1090, 332, "B  Aubert / EPHI — bird–flower access barrier", size=20, weight="bold"),
            '<rect x="1090" y="354" width="700" height="318" rx="14" fill="#fffdf7" stroke="#444" stroke-width="2"/>',
            _text(1115, 386, f'{int(aubert["pair_site_n"]):,} bird × plant × site units | 18 Ecuador sites', size=15, weight="bold"),
            _text(1115, 425, "mean robbery rate", size=15, weight="bold"),
            _text(1115, 466, "tube > bill barrier", size=14),
            f'<rect x="{bar_x0}" y="448" width="{barrier_w:.1f}" height="24" fill="#b24a4a" fill-opacity="0.75"/>',
            _text(1715, 467, f'barrier = {barrier_rate:.3f}', size=15, anchor="end", weight="bold"),
            _text(1115, 510, "tube ≤ bill accessible", size=14),
            f'<rect x="{bar_x0}" y="492" width="{accessible_w:.1f}" height="24" fill="#4777a8" fill-opacity="0.75"/>',
            _text(1715, 511, f'accessible = {accessible_rate:.3f}', size=15, anchor="end", weight="bold"),
            _text(1115, 548, f'pair-site difference = +{float(aubert["barrier_minus_accessible_mean_rate"]):.3f}; permutation p = {float(aubert["barrier_mean_difference_permutation_p"]):.4f}', size=14),
            _text(1115, 582, f'mismatch rho = {float(aubert["mismatch_spearman_rho"]):.3f}; permutation p = {float(aubert["mismatch_spearman_permutation_p"]):.4f}', size=14, weight="bold"),
            _text(1115, 620, f'{int(site["positive_sites"])} / {int(site["eligible_sites"])} sites show higher robbery under barrier', size=15, weight="bold"),
            _text(1115, 648, f'within-site mean Δ = +{float(site["mean_within_site_difference"]):.3f}; sign p = {float(site["sign_test_p"]):.5f}; stratified p = {float(site["site_stratified_permutation_p"]):.4f}', size=13),
        ])
    else:
        parts.extend([
            _text(1090, 332, "B  Aubert / EPHI — aggregate unavailable", size=20, weight="bold"),
        ])

    parts.extend([
        '<rect x="1090" y="700" width="700" height="180" rx="14" fill="#f7f7f7" stroke="#444" stroke-width="2"/>',
        _text(1115, 735, "Cross-network ecological readout", size=19, weight="bold"),
        _text(1115, 775, "Insects: increasing access constraint shifts cheating toward bypass/robbing.", size=15),
        _text(1115, 810, "Birds: flower tube > bill mismatch raises robbery rate across sites.", size=15),
        _text(1115, 850, "Same routing direction; different fauna, response scale and inferential unit.", size=15, weight="bold"),
        _text(120, 908, "Sakhalkar: significant univariate association; correlated morphology prevents a unique tube-length claim.", size=12, fill="#555"),
        _text(120, 934, "Aubert/EPHI: observational all-18-site extension, not an exact replication of the published three-transect GLMM.", size=12, fill="#555"),
        _text(120, 960, "No raw species identifiers or individual interaction rows are emitted in the figure.", size=12),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"

def build_from_public_data() -> str:
    workbook = _find_workbook(_download())
    visits = read_xlsx_sheet_rows(workbook, "cheater_data")
    traits = read_xlsx_sheet_rows(workbook, "plant_traits")
    points = species_route_points(visits, traits)
    result = analyze_workbook(workbook, permutations=9999)
    aubert = json.loads(AUBERT_RESULT.read_text(encoding="utf-8")) if AUBERT_RESULT.exists() else None
    return build_svg(points, result, aubert)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    svg = build_from_public_data()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
