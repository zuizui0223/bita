"""Build candidate BITA macro-ecology Figures 1 and 2 as dependency-free SVG."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path

from trait_architecture.floral_defence_selectivity import load_csv_rows


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "empirical" / "floral_defence_selectivity"
DEFAULT_OUT = ROOT / "manuscript" / "figures_macro_candidate"


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


def _line(x1: float, y1: float, x2: float, y2: float, *, width: float = 2, dash: str = "") -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="#222" stroke-width="{width}"{extra}/>'
    )


def build_figure1() -> str:
    width, height = 1500, 900
    x0, x1 = 110, 1390
    axis_y = 310
    xh, xp = 535, 965
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(750, 48, "Figure 1. Effective-exposure selectivity", size=30, anchor="middle", weight="bold"),
        _text(750, 82, "Unequal access, susceptibility and response thresholds create a selective window", size=19, anchor="middle"),
        _text(65, 135, "A", size=22, weight="bold"),
        _text(105, 135, "Threshold model", size=22, weight="bold"),
        _line(x0, axis_y, x1, axis_y, width=3),
        _text(x1, axis_y + 38, "defence / access intensity x", size=18, anchor="end"),
        f'<rect x="{x0}" y="{axis_y-80}" width="{xh-x0}" height="72" fill="#eeeeee"/>',
        f'<rect x="{xh}" y="{axis_y-80}" width="{xp-xh}" height="72" fill="#d8ead8"/>',
        f'<rect x="{xp}" y="{axis_y-80}" width="{x1-xp}" height="72" fill="#ead8d8"/>',
        _text((x0+xh)/2, axis_y-37, "ineffective", anchor="middle", size=18, weight="bold"),
        _text((xh+xp)/2, axis_y-37, "selective / guarded", anchor="middle", size=18, weight="bold"),
        _text((xp+x1)/2, axis_y-37, "interfering", anchor="middle", size=18, weight="bold"),
        _line(xh, axis_y-115, xh, axis_y+25, width=2, dash="8 6"),
        _line(xp, axis_y-115, xp, axis_y+25, width=2, dash="8 6"),
        _text(xh, axis_y-128, "x_H*", anchor="middle", size=20, weight="bold"),
        _text(xp, axis_y-128, "x_P*", anchor="middle", size=20, weight="bold"),
        _text(750, 390, "xH* = τH/qH     |     xH* < x < xP*     |     xP* = τP/qP", size=20, anchor="middle"),
        _text(65, 480, "B", size=22, weight="bold"),
        _text(105, 480, "What changes effective exposure?", size=22, weight="bold"),
    ]
    labels = [
        (("susceptibility",), 180, 185),
        (("geometry /", "body size"), 395, 190),
        (("attack route",), 610, 180),
        (("timing",), 810, 165),
        (("cumulative", "exposure"), 1000, 185),
        (("functional mode /", "response stage"), 1250, 245),
    ]
    for lines, x, box_w in labels:
        parts.append(
            f'<rect x="{x-box_w/2}" y="515" width="{box_w}" height="70" '
            'rx="12" fill="#f7f7f7" stroke="#444" stroke-width="1.5"/>'
        )
        if len(lines) == 1:
            parts.append(_text(x, 557, lines[0], anchor="middle", size=15, weight="bold"))
        else:
            parts.append(_text(x, 548, lines[0], anchor="middle", size=14, weight="bold"))
            parts.append(_text(x, 568, lines[1], anchor="middle", size=14, weight="bold"))
    parts.extend([
        _text(750, 625, "separation: q_H >> q_P  -> wider window", anchor="middle", size=19, weight="bold"),
        _text(750, 656, "overlap: q_H ~ q_P  -> narrow / absent window", anchor="middle", size=19),
        _text(65, 735, "C", size=22, weight="bold"),
        _text(105, 735, "Bypass prediction", size=22, weight="bold"),
        f'<ellipse cx="365" cy="790" rx="120" ry="55" fill="#f7f7f7" stroke="#222" stroke-width="2"/>',
        f'<rect x="335" y="724" width="60" height="76" fill="#d9d9d9" stroke="#222" stroke-width="2"/>',
        _text(365, 770, "barrier", anchor="middle", size=16, weight="bold"),
        _line(485, 790, 650, 790, width=3),
        _text(565, 776, "legitimate route", anchor="middle", size=15),
        f'<path d="M 475 810 C 555 870, 650 865, 735 805" fill="none" stroke="#222" stroke-width="3" stroke-dasharray="9 7"/>',
        _text(610, 862, "bypass / robbing", anchor="middle", size=16, weight="bold"),
        _text(1040, 782, "Blocking one route need not eliminate exploitation.", anchor="middle", size=19, weight="bold"),
        _text(1040, 815, "It can change which interaction mode is realised.", anchor="middle", size=19),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


DOMAIN_FILL = {
    "SEPARATED": "#e3f1e4",
    "OVERLAPPED": "#f1dfdf",
    "BYPASS_TOLERANCE": "#eadff2",
    "TRANSITIONAL": "#f2ecd8",
    "UNCLEAR": "#eeeeee",
}
POLL_FILL = {
    "PRESERVED_OR_IMPROVED": "#d6ead8",
    "NO_DETECTED_CHANGE": "#fff4c7",
    "IMPAIRED": "#f1cccc",
    "MIXED": "#e7dcf1",
    "UNRESOLVED": "#ededed",
}


def _short(value: str, limit: int = 27) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 1] + "…"


def build_figure2(rows: list[dict[str, str]], gate: dict[str, object]) -> str:
    rows = sorted(rows, key=lambda r: (r["derivation_or_holdout"], r["study_cluster_id"]))
    width, height = 1750, 1300
    left = 45
    header_y = 125
    row_h = 48
    y0 = 160
    cols = [
        ("Plant system", 55, 330),
        ("Cohort", 390, 160),
        ("Modality", 555, 180),
        ("Domain", 740, 210),
        ("Antagonist", 955, 180),
        ("Pollinator", 1140, 250),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(875, 43, "Figure 2. Matched floral-defence systems and the current Stage-2 gate", size=28, anchor="middle", weight="bold"),
        _text(875, 78, f'{len(rows)} matched floral systems; outcome states remain on source-supported qualitative scales', size=18, anchor="middle"),
    ]
    for label, x, w in cols:
        parts.append(f'<rect x="{x}" y="{header_y}" width="{w}" height="34" fill="#e8e8e8" stroke="#555"/>')
        parts.append(_text(x + 8, header_y + 23, label, size=15, weight="bold"))

    for i, row in enumerate(rows):
        y = y0 + i * row_h
        domain = row["pre_outcome_domain_code"]
        poll = row["pollinator_cost_state_derived"]
        ant = row["defence_efficacy_state"]
        cohort = row["derivation_or_holdout"]
        parts.append(f'<g data-cluster="{escape(row["study_cluster_id"])}">')
        parts.append(f'<rect x="{left}" y="{y}" width="1355" height="{row_h}" fill="#fff" stroke="#dddddd"/>')
        parts.append(_text(63, y + 30, _short(row["plant_taxon"], 32), size=15, weight="bold"))
        parts.append(_text(398, y + 30, _short(cohort.replace("_", " "), 20), size=14))
        parts.append(_text(563, y + 30, _short(row["defence_modality"].replace("_", " "), 22), size=14))
        parts.append(f'<rect x="748" y="{y+7}" width="194" height="34" rx="8" fill="{DOMAIN_FILL.get(domain, "#eee")}" stroke="#777"/>')
        parts.append(_text(845, y + 29, domain.replace("_", " "), anchor="middle", size=13, weight="bold"))
        parts.append(_text(963, y + 30, ant.replace("_", " "), size=14))
        parts.append(f'<rect x="1148" y="{y+7}" width="234" height="34" rx="8" fill="{POLL_FILL.get(poll, "#eee")}" stroke="#777"/>')
        parts.append(_text(1265, y + 29, _short(poll.replace("_", " "), 29), anchor="middle", size=13, weight="bold"))
        parts.append("</g>")

    box_y = y0 + len(rows) * row_h + 32
    strict = gate["strict_table"]
    sens = gate["compatibility_sensitivity_table"]
    p_strict = gate["strict_fisher_two_sided_p"]
    p_sens = gate["compatibility_sensitivity_fisher_two_sided_p"]
    parts.extend([
        f'<rect x="45" y="{box_y}" width="510" height="230" rx="12" fill="#fafafa" stroke="#333" stroke-width="2"/>',
        _text(65, box_y + 30, "Strict Stage-2 exact subset", size=18, weight="bold"),
        _text(65, box_y + 63, "SEPARATED", size=15, weight="bold"),
        _text(230, box_y + 63, f'compatible {strict["SEPARATED"]["compatible"]}', size=15),
        _text(375, box_y + 63, f'impaired {strict["SEPARATED"]["impaired"]}', size=15),
        _text(65, box_y + 92, "OVERLAPPED", size=15, weight="bold"),
        _text(230, box_y + 92, f'compatible {strict["OVERLAPPED"]["compatible"]}', size=15),
        _text(375, box_y + 92, f'impaired {strict["OVERLAPPED"]["impaired"]}', size=15),
        _text(65, box_y + 130, f'Fisher p = {p_strict:.3f}', size=17, weight="bold"),
        _text(65, box_y + 162, "DESCRIPTIVE_EXACT_ONLY", size=15, weight="bold"),
        _text(65, box_y + 194, "domain vs modality not identified", size=15, weight="bold", fill="#8a1d1d"),
        f'<rect x="585" y="{box_y}" width="570" height="230" rx="12" fill="#fffdf3" stroke="#555" stroke-width="2"/>',
        _text(605, box_y + 30, "Null-compatible sensitivity", size=18, weight="bold"),
        _text(605, box_y + 63, f'SEPARATED compatible-or-null = {sens["SEPARATED"]["compatible_or_null"]}', size=15),
        _text(605, box_y + 92, f'OVERLAPPED impaired = {sens["OVERLAPPED"]["impaired"]}', size=15),
        _text(605, box_y + 130, f'Fisher p = {p_sens:.3f}', size=17, weight="bold"),
        _text(605, box_y + 164, "null-compatible ≠ equivalence-supported preservation", size=15, weight="bold"),
        f'<rect x="1185" y="{box_y}" width="500" height="230" rx="12" fill="#f7f7f7" stroke="#555" stroke-width="2"/>',
        _text(1205, box_y + 30, "Strict-set confounding", size=18, weight="bold"),
        _text(1205, box_y + 65, "Thunia: separated / physical", size=15),
        _text(1205, box_y + 94, "Caryopteris: separated / physical", size=15),
        _text(1205, box_y + 123, "Gelsemium: overlapped / chemical", size=15),
        _text(1205, box_y + 166, "No domain > modality claim", size=16, weight="bold", fill="#8a1d1d"),
        _text(45, height - 24, "Rows are independent study clusters. Repeated outcomes do not increase N; architecture and outcome codes retain separate provenance.", size=14),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"



def _wrap_state(value: str, max_chars: int = 28) -> tuple[str, ...]:
    words = value.replace("_", " ").split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return tuple(lines[:3])


def _state_box(
    x: float,
    y: float,
    width: float,
    height: float,
    value: str,
    *,
    fill: str,
) -> list[str]:
    lines = _wrap_state(value)
    out = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="10" '
        f'fill="{fill}" stroke="#555" stroke-width="1.5"/>'
    ]
    if len(lines) == 1:
        ys = [y + height / 2 + 5]
    elif len(lines) == 2:
        ys = [y + height / 2 - 5, y + height / 2 + 16]
    else:
        ys = [y + height / 2 - 17, y + height / 2 + 4, y + height / 2 + 25]
    for line, yy in zip(lines, ys):
        out.append(_text(x + width / 2, yy, line, size=13, anchor="middle"))
    return out


def build_figure3(rows: list[dict[str, str]]) -> str:
    if len(rows) != 8:
        raise ValueError(f"expected 8 defence-side conditionality clusters, got {len(rows)}")

    ordered_ids = {
        "Galen_2011_Polemonium",
        "Jones_Agrawal_2016_Asclepias",
        "Villalona_Ezray_2020_Asclepias",
        "Barlow_2017_Aconitum",
    }
    ordered = [row for row in rows if row["study_cluster_id"] in ordered_ids]
    other = [row for row in rows if row["study_cluster_id"] not in ordered_ids]

    width, height = 1680, 1120
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(840, 46, "Figure 3. The same defence axis changes ecological state", size=29, anchor="middle", weight="bold"),
        _text(840, 80, "8 defence-side state-switch systems; each row is one independent study cluster", size=18, anchor="middle"),
        _text(45, 127, "Ordered exposure / intensity contrasts", size=21, weight="bold"),
        _text(855, 127, "Other conditionality axes", size=21, weight="bold"),
    ]

    def render_lane(row: dict[str, str], x0: float, y: float) -> None:
        parts.append(f'<g data-cluster="{escape(row["study_cluster_id"])}">')
        plant_label = row["plant_taxon"].replace("_and_A_napellus", " / A. napellus").replace("_", " ")\n        parts.append(_text(x0, y + 22, _short(plant_label, 35), size=16, weight="bold"))
        parts.append(_text(x0, y + 44, row["macro_axis"].replace("_", " "), size=13, fill="#555"))
        parts.extend(_state_box(x0, y + 58, 285, 82, row["low_or_first_state"], fill="#f2f2f2"))
        parts.append(_line(x0 + 292, y + 99, x0 + 350, y + 99, width=2.5))
        parts.append(f'<path d="M {x0+350} {y+99} l -12 -7 l 0 14 z" fill="#222"/>')
        parts.extend(_state_box(x0 + 362, y + 58, 310, 82, row["high_or_second_state"], fill="#f7eadc"))
        parts.append(
            _text(
                x0 + 336,
                y + 164,
                _short(row["ecological_transition"].replace("_", " "), 48),
                size=13,
                anchor="middle",
                weight="bold",
            )
        )
        parts.append("</g>")

    for i, row in enumerate(sorted(ordered, key=lambda r: r["study_cluster_id"])):
        render_lane(row, 45, 150 + i * 185)

    for i, row in enumerate(sorted(other, key=lambda r: r["study_cluster_id"])):
        render_lane(row, 855, 150 + i * 185)

    bottom_y = 910
    parts.extend([
        f'<rect x="45" y="{bottom_y}" width="1590" height="155" rx="14" fill="#f7f7f7" stroke="#444" stroke-width="2"/>',
        _text(70, bottom_y + 32, "Kessler 2015 consumer-context bridge", size=19, weight="bold"),
        _text(70, bottom_y + 66, "same nectar-restriction axis", size=16, weight="bold"),
        _text(355, bottom_y + 66, "Manduca: SWEET9 seed production = 44.6% of EV (supported cost)", size=15),
        _text(355, bottom_y + 96, "Hyles: SWEET9 seed production = 111.69% of EV (single-axis cost not detected)", size=15),
        _text(70, bottom_y + 129, "Main inference: same trait, different ecological state as consumer, exposure, stage or timing changes.", size=17, weight="bold"),
        _text(1230, bottom_y + 129, "No universal threshold ratio is inferred.", size=14, anchor="middle", fill="#555"),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"

def write_figures(out_dir: Path, module: Path = MODULE) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = load_csv_rows(module / "results" / "analysis_ready_matched_systems.csv")
    gate = json.loads((module / "results" / "stage2_model_gate.json").read_text(encoding="utf-8"))
    conditionality = load_csv_rows(module / "d_side_conditionality_registry.csv")
    payloads = {
        "FIGURE_1_EFFECTIVE_EXPOSURE_THEORY.svg": build_figure1(),
        "FIGURE_2_MATCHED_D_STATE_MAP.svg": build_figure2(rows, gate),
        "FIGURE_3_DEFENCE_STATE_SWITCHES.svg": build_figure3(conditionality),
    }
    paths: list[Path] = []
    for name, svg in payloads.items():
        path = out_dir / name
        path.write_text(svg, encoding="utf-8")
        paths.append(path)
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    for path in write_figures(args.output_dir):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
