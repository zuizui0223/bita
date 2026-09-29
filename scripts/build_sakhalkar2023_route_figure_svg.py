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
AUBERT_RESULT = ROOT / "empirical" / "floral_defence_selectivity" / "results" / "aubert2026_missingness_dependence_sensitivity.json"


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
        primary = aubert["missing_as_no"]
        native = primary["native_pair_site_summary"]
        site = native["site_difference"]
        plant_rho = primary["plant_species_rho_check"]
        plant_barrier = primary["plant_species_cluster_check"]
        bird_barrier = primary["bird_species_cluster_check"]
        bird_within = primary["bird_within_species_continuous_check"]
        barrier_rate = float(native["mean_robbery_rate_barrier"])
        accessible_rate = float(native["mean_robbery_rate_accessible"])

        parts.extend([
            _text(1090, 332, "B  Aubert / EPHI — plant and within-bird tests", size=20, weight="bold"),
            '<rect x="1090" y="354" width="700" height="318" rx="14" fill="#fffdf7" stroke="#444" stroke-width="2"/>',
            _text(1115, 386, f'{int(plant_rho["n_clusters"]):,} plant species | missing piercing → legitimate/no', size=15, weight="bold"),
            _text(1115, 421, f'plant-level mismatch rho = {float(plant_rho["rho"]):.3f}; p = {float(plant_rho["permutation_p_two_sided"]):.4f}', size=14, weight="bold"),
            _text(1115, 455, f'plant paired barrier: {int(plant_barrier["eligible_clusters"])} species; Δ = +{float(plant_barrier["mean_cluster_difference"]):.3f}; p = {float(plant_barrier["cluster_label_swap_permutation_p"]):.4f}', size=13),
            _text(1115, 493, f'bird paired barrier: {int(bird_barrier["eligible_clusters"])} species; Δ = +{float(bird_barrier["mean_cluster_difference"]):.3f}; p = {float(bird_barrier["cluster_label_swap_permutation_p"]):.4f}', size=13, weight="bold"),
            _text(1115, 531, f'within-bird continuous: {int(bird_within["eligible_bird_species_continuous"])} species / {int(bird_within["bird_plant_dyads_in_pooled_test"]):,} dyads', size=13, weight="bold"),
            _text(1115, 560, f'centered-rank rho = {float(bird_within["pooled_within_bird_rank_rho"]):.3f}; p = {float(bird_within["within_bird_permutation_p_two_sided"]):.4f}', size=13, weight="bold"),
            _text(1115, 598, f'descriptive pair-site robbery: barrier {barrier_rate:.3f} vs accessible {accessible_rate:.3f}', size=13),
            _text(1115, 632, f'{int(site["positive_sites"])} / {int(site["eligible_sites"])} sites positive; {int(native["pair_site_n"]):,} pair-site units', size=13),
        ])
    else:
        parts.extend([
            _text(1090, 332, "B  Aubert / EPHI — aggregate unavailable", size=20, weight="bold"),
        ])

    parts.extend([
        '<rect x="1090" y="700" width="700" height="180" rx="14" fill="#f7f7f7" stroke="#444" stroke-width="2"/>',
        _text(1115, 735, "Cross-network ecological readout", size=19, weight="bold"),
        _text(1115, 775, "Insects: increasing access constraint shifts cheating toward bypass/robbing.", size=15),
        _text(1115, 810, "Birds: plant-level and within-bird comparisons both recover rerouting.", size=15),
        _text(1115, 850, "Consumer-grain behavior survives after bird-specific baselines are removed.", size=15, weight="bold"),
        _text(120, 908, "Sakhalkar: significant univariate association; correlated morphology prevents a unique tube-length claim.", size=12, fill="#555"),
        _text(120, 934, "Aubert/EPHI: observational all-site extension; missing piercing is recoded as legitimate/no from source metadata.", size=12, fill="#555"),
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
