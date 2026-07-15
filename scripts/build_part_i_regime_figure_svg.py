"""Build manuscript Figure 2 from reproduced Part I sensitivity CSV outputs.

The dependency-free SVG contains three panels:

A. Complementary occupancy by biological parameter scenario.
B. Complementary occupancy across pollinator-service × floral-damage pressure.
C. Complementary occupancy across endpoint-normalized response-shape variants.

Input rows must come from ``scripts/run_part_i_robustness.py``. Percentages are
unweighted occupancies of the declared finite grid, not empirical probabilities.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from html import escape
from pathlib import Path


def read_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def complementary_fraction(rows: list[dict[str, str]]) -> float:
    if not rows:
        raise ValueError("cannot summarize empty rows")
    return sum(r["sign"] == "complementary" for r in rows) / len(rows)


def grouped_fraction(rows: list[dict[str, str]], keys: tuple[str, ...]) -> dict[tuple[str, ...], float]:
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    return {key: complementary_fraction(value) for key, value in grouped.items()}


def _text(x: float, y: float, value: str, *, size: int = 14, anchor: str = "start", weight: str = "normal") -> str:
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">{escape(value)}</text>'


def build_svg(rows: list[dict[str, str]]) -> str:
    if not rows:
        raise ValueError("sensitivity evaluations are empty")

    width, height = 1320, 760
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(40, 42, "Figure 2. Conditional attraction–defence regimes across the declared finite tested set", size=22, weight="bold"),
    ]

    scen = grouped_fraction(rows, ("parameter_scenario_id",))
    x0, y0, pw, ph = 55, 95, 370, 520
    parts += [_text(x0, y0 - 22, "A  Biological parameter scenarios", size=18, weight="bold"),
              f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="none" stroke="black"/>']
    items = sorted(scen.items())
    bar_h = 54
    for i, ((label,), frac) in enumerate(items):
        y = y0 + 55 + i * 105
        label_short = label.replace("_", " ")
        parts.append(_text(x0 + 12, y - 10, label_short, size=12))
        parts.append(f'<rect x="{x0+12}" y="{y}" width="{(pw-24)*frac:.1f}" height="{bar_h}" fill="#555"/>')
        parts.append(f'<rect x="{x0+12}" y="{y}" width="{pw-24}" height="{bar_h}" fill="none" stroke="black"/>')
        parts.append(_text(x0 + pw - 18, y + 35, f"{100*frac:.1f}% complementary", size=13, anchor="end"))

    heat = grouped_fraction(rows, ("pollinator_service", "floral_damage_pressure"))
    x1, y1, cell = 475, 145, 92
    parts.append(_text(455, 73, "B  Interaction environment", size=18, weight="bold"))
    services = sorted({float(k[0]) for k in heat})
    damages = sorted({float(k[1]) for k in heat})
    for i, p in enumerate(services):
        parts.append(_text(x1 + i*cell + cell/2, y1 + len(damages)*cell + 34, f"P={p:.1f}", size=13, anchor="middle"))
    for j, h in enumerate(reversed(damages)):
        parts.append(_text(x1 - 14, y1 + j*cell + cell/2 + 5, f"H={h:.1f}", size=13, anchor="end"))
        for i, p in enumerate(services):
            frac = heat[(f"{p}", f"{h}")]
            shade = round(255 - 170*frac)
            fill = f"rgb({shade},{shade},{shade})"
            x, y = x1 + i*cell, y1 + j*cell
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{fill}" stroke="black"/>')
            parts.append(_text(x + cell/2, y + cell/2 + 5, f"{100*frac:.1f}%", size=14, anchor="middle", weight="bold"))
    parts.append(_text(x1 + 1.5*cell, y1 + len(damages)*cell + 66, "Pollinator service", size=14, anchor="middle"))
    parts.append(_text(x1 - 75, y1 + 1.5*cell, "Floral damage pressure", size=14, anchor="middle"))

    form = grouped_fraction(rows, ("form_id",))
    x2, y2, pw2, ph2 = 830, 95, 430, 520
    parts += [_text(x2, y2 - 22, "C  Endpoint-normalized response shapes", size=18, weight="bold"),
              f'<rect x="{x2}" y="{y2}" width="{pw2}" height="{ph2}" fill="none" stroke="black"/>']
    fitems = sorted(form.items())
    for i, ((label,), frac) in enumerate(fitems):
        y = y2 + 55 + i*105
        parts.append(_text(x2 + 12, y - 10, label.replace("_", " "), size=12))
        parts.append(f'<rect x="{x2+12}" y="{y}" width="{(pw2-24)*frac:.1f}" height="54" fill="#777"/>')
        parts.append(f'<rect x="{x2+12}" y="{y}" width="{pw2-24}" height="54" fill="none" stroke="black"/>')
        parts.append(_text(x2 + pw2 - 18, y + 35, f"{100*frac:.1f}% complementary", size=13, anchor="end"))

    parts.append(_text(55, 682, "Bars and cells show unweighted occupancy fractions of the declared finite grid; they are not empirical probabilities.", size=14))
    parts.append(_text(55, 708, "Panel C compares response shapes normalized to common endpoint scales on the declared 0–1 trait domain.", size=14))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evaluation_csv")
    parser.add_argument("output_svg")
    args = parser.parse_args(argv)
    svg = build_svg(read_rows(args.evaluation_csv))
    output = Path(args.output_svg)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
