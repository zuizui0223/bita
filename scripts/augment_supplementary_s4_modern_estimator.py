"""Augment Supplementary Figure S4 with the registered modern-estimator sensitivity.

Presentation-only post-processing. Canonical DerSimonian-Laird pooled estimates remain
unchanged; this inset visualizes the already-registered REML + modified
Hartung-Knapp sensitivity from the machine-readable Gate G receipt.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "empirical" / "mechanism_pattern_synthesis" / "LEAL_2025_MODERN_ESTIMATOR_SENSITIVITY_V1.json"
START = "<!-- MODERN_ESTIMATOR_INSET_START -->"
END = "<!-- MODERN_ESTIMATOR_INSET_END -->"


def _fmt(value: float) -> str:
    return f"{value:.4f}"


def _x(value: float, *, x0: float = 330.0, width: float = 290.0, lo: float = -0.85, hi: float = 0.05) -> float:
    return x0 + (value - lo) / (hi - lo) * width


def build_inset(payload: dict) -> str:
    results = payload["results"]
    order = ("female_reproductive_success", "nectar_standing_crop", "visitation_rate")
    y_positions = (535.0, 575.0, 615.0)
    zero_x = _x(0.0)

    parts = [
        START,
        '<rect x="55" y="474" width="930" height="170" fill="#ffffff" stroke="#aaaaaa" stroke-width="1"/>',
        '<text x="70" y="500" font-family="DejaVu Sans,Arial,sans-serif" font-size="13" font-weight="700">REML + modified Hartung-Knapp sensitivity (same independent-cluster inputs)</text>',
        f'<line x1="{zero_x:.1f}" y1="515" x2="{zero_x:.1f}" y2="632" stroke="#777" stroke-width="1.2" stroke-dasharray="5 4"/>',
    ]

    for key, y in zip(order, y_positions):
        row = results[key]
        label = row["label"]
        pooled = float(row["pooled"])
        low = float(row["mkh_ci_low"])
        high = float(row["mkh_ci_high"])
        borderline = bool(row["modified_hartung_knapp_borderline_zero_margin"])
        parts.extend(
            [
                f'<text x="70" y="{y + 4:.1f}" font-family="DejaVu Sans,Arial,sans-serif" font-size="11">{label}</text>',
                f'<line x1="{_x(low):.1f}" y1="{y:.1f}" x2="{_x(high):.1f}" y2="{y:.1f}" stroke="#222" stroke-width="3"/>',
                f'<circle cx="{_x(pooled):.1f}" cy="{y:.1f}" r="5" fill="#ffffff" stroke="#111" stroke-width="2"/>',
                f'<text x="640" y="{y + 4:.1f}" text-anchor="start" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">REML {_fmt(pooled)}; mHK [{_fmt(low)}, {_fmt(high)}]{"; borderline to zero" if borderline else ""}</text>',
            ]
        )

    parts.extend(
        [
            '<text x="330" y="638" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">-0.85</text>',
            f'<text x="{zero_x:.1f}" y="638" text-anchor="middle" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">0</text>',
            '<text x="620" y="638" text-anchor="end" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">0.05</text>',
            END,
        ]
    )
    return "\n".join(parts)


def augment(svg_text: str, payload: dict) -> str:
    svg_text = re.sub(
        re.escape(START) + r".*?" + re.escape(END) + r"\n?",
        "",
        svg_text,
        flags=re.DOTALL,
    )
    if "</svg>" not in svg_text:
        raise ValueError("S4 SVG has no closing </svg> tag")
    inset = build_inset(payload)
    return svg_text.replace("</svg>", inset + "\n</svg>", 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", type=Path)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    args = parser.parse_args()

    payload = json.loads(args.json.read_text(encoding="utf-8"))
    if payload.get("status") != "ROBUSTNESS_PASS":
        raise ValueError("modern-estimator sensitivity receipt is not ROBUSTNESS_PASS")
    if not payload.get("canonical_results_remain_der_simonian_laird"):
        raise ValueError("receipt no longer preserves canonical DerSimonian-Laird results")

    text = args.svg.read_text(encoding="utf-8")
    args.svg.write_text(augment(text, payload), encoding="utf-8")
    print(f"augmented {args.svg} with REML + modified Hartung-Knapp inset")


if __name__ == "__main__":
    main()
