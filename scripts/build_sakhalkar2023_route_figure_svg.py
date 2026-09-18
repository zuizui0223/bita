"""Build candidate BITA Figure 4 from the public Sakhalkar et al. 2023 workbook."""

from __future__ import annotations

import argparse
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
    / "FIGURE_4_SAKHALKAR_ACCESS_ROUTING.svg"
)


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
) -> str:
    if not points:
        raise ValueError("cannot build Figure 4 without species-level route points")

    width, height = 1500, 940
    plot_x0, plot_x1 = 120, 910
    plot_y0, plot_y1 = 145, 650
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
        _text(750, 42, "Figure 4. Floral access geometry reroutes cheating mode", size=29, anchor="middle", weight="bold"),
        _text(750, 75, "Independent reanalysis of the Sakhalkar et al. 2023 Afrotropical visitor network", size=18, anchor="middle"),
        _text(120, 115, "Species-level tube length versus robbing–thieving balance", size=20, weight="bold"),
        f'<rect x="{plot_x0}" y="{plot_y0}" width="{plot_x1-plot_x0}" height="{plot_y1-plot_y0}" fill="#fafafa" stroke="#222" stroke-width="2"/>',
    ]

    # Horizontal reference lines: thief-only, equal balance, robber-only.
    for balance, label in [(-1.0, "thieving only"), (0.0, "equal balance"), (1.0, "robbing only")]:
        y = _scale(balance, -1.0, 1.0, plot_y1, plot_y0)
        parts.append(
            f'<line x1="{plot_x0}" y1="{y}" x2="{plot_x1}" y2="{y}" '
            'stroke="#bbbbbb" stroke-width="1.4" stroke-dasharray="6 5"/>'
        )
        parts.append(_text(plot_x0 - 12, y + 5, label, size=13, anchor="end"))

    # X ticks.
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
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.4" fill="{fill}" '
            'fill-opacity="0.72" stroke="#222" stroke-width="0.6"/>'
        )

    parts.extend([
        _text(plot_x1 - 12, plot_y0 + 28, "B = (R − T)/(R + T)", size=14, anchor="end"),
        _text((plot_x0 + plot_x1) / 2, plot_y1 + 60, "tube length (source trait scale)", size=16, anchor="middle"),
        _text(140, 748, f"n = {n_species} species", size=17, weight="bold"),
        _text(345, 748, f"rho = {rho:.3f}", size=17, weight="bold"),
        _text(510, 748, f"permutation p = {pval:.4f}", size=17, weight="bold"),
        _text(140, 773, "Plant species are inferential units; individual visits are not treated as replicates.", size=13),
    ])

    # Legend.
    legend_y = 818
    for i, (key, label) in enumerate([
        ("robber_only", "robber-only"),
        ("mixed", "mixed robbing + thieving"),
        ("thief_only", "thief-only"),
    ]):
        x = 140 + i * 245
        parts.append(f'<circle cx="{x}" cy="{legend_y}" r="6" fill="{class_fill[key]}" stroke="#222"/>')
        parts.append(_text(x + 14, legend_y + 5, label, size=14))

    # Panel on right: medians and routing interpretation.
    box_x = 970
    parts.extend([
        f'<rect x="{box_x}" y="135" width="470" height="250" rx="14" fill="#f7f7f7" stroke="#444" stroke-width="2"/>',
        _text(box_x + 22, 170, "Route-specific tube-length contrast", size=19, weight="bold"),
        _text(box_x + 22, 215, f'robber-only median = {float(result["median_tube_length_robber_only"]):.3f}', size=17, weight="bold", fill="#8c2d2d"),
        _text(box_x + 22, 252, f'thief-only median = {float(result["median_tube_length_thief_only"]):.3f}', size=17, weight="bold", fill="#315f8c"),
        _text(box_x + 22, 300, "Descriptive contrast only; not a second inferential test.", size=14),
        _text(box_x + 22, 345, "Longer tubes are associated with", size=15, weight="bold"),
        _text(box_x + 22, 370, "relatively more robbery.", size=15, weight="bold"),
        f'<rect x="{box_x}" y="420" width="470" height="310" rx="14" fill="#fffdf7" stroke="#444" stroke-width="2"/>',
        _text(box_x + 22, 458, "Access-routing interpretation", size=19, weight="bold"),
        _text(box_x + 35, 505, "short / accessible flower", size=16, weight="bold"),
        _text(box_x + 55, 535, "→ thieving through opening", size=16, fill="#315f8c"),
        _text(box_x + 35, 585, "long / constrained flower", size=16, weight="bold"),
        _text(box_x + 55, 615, "→ bypass / robbing", size=16, fill="#8c2d2d"),
        _text(box_x + 22, 675, "Access barriers can reroute exploitation", size=17, weight="bold"),
        _text(box_x + 22, 705, "rather than simply eliminating it.", size=17, weight="bold"),
        _text(120, 875, "Public data: Sakhalkar et al. 2023, Zenodo 10.5281/zenodo.8398202. No species identifiers or raw visit rows are emitted in this figure.", size=13),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def build_from_public_data() -> str:
    workbook = _find_workbook(_download())
    visits = read_xlsx_sheet_rows(workbook, "cheater_data")
    traits = read_xlsx_sheet_rows(workbook, "plant_traits")
    points = species_route_points(visits, traits)
    result = analyze_workbook(workbook, permutations=9999)
    return build_svg(points, result)


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
