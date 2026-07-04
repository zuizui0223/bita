"""Render a monochrome theory-to-empirics channel-ledger SVG for Impatiens.

The figure intentionally distinguishes observational trait associations (dashed
arrows) from the randomized imposed-florivory treatment effect (solid arrow). It
uses aggregate reports only and never writes raw observations.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


WIDTH = 1260
HEIGHT = 760


def _model(report: dict[str, Any], analysis_id: str) -> dict[str, Any]:
    summaries = report.get("model_summaries")
    if not isinstance(summaries, list):
        raise ValueError("report has no model_summaries list")
    matches = [item for item in summaries if isinstance(item, dict) and item.get("analysis_id") == analysis_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one model {analysis_id}")
    return matches[0]


def _coefficient(model: dict[str, Any], term: str) -> dict[str, Any]:
    values = model.get("coefficients")
    if not isinstance(values, list):
        raise ValueError(f"{model.get('analysis_id')}: coefficients missing")
    matches = [item for item in values if isinstance(item, dict) and item.get("term") == term]
    if len(matches) != 1:
        raise ValueError(f"{model.get('analysis_id')}: expected one coefficient for {term}")
    return matches[0]


def _ratio_label(coefficient: dict[str, Any], prefix: str) -> str:
    ratio = float(coefficient["exp_estimate"])
    lower = float(coefficient["exp_ci95_lower"])
    upper = float(coefficient["exp_ci95_upper"])
    return f"{prefix} {ratio:.2f} [{lower:.2f}, {upper:.2f}]"


def _beta_label(coefficient: dict[str, Any]) -> str:
    estimate = float(coefficient["estimate"])
    lower = float(coefficient["ci95_lower"])
    upper = float(coefficient["ci95_upper"])
    return f"β {estimate:+.2f} [{lower:+.2f}, {upper:+.2f}]"


def _node(x: int, y: int, w: int, h: int, title: str, subtitle: str, *, bold: bool = False) -> str:
    weight = "700" if bold else "600"
    return f"""
      <rect x=\"{x}\" y=\"{y}\" width=\"{w}\" height=\"{h}\" rx=\"12\" fill=\"white\" stroke=\"#111\" stroke-width=\"2\"/>
      <text x=\"{x + w / 2}\" y=\"{y + 34}\" text-anchor=\"middle\" font-family=\"Arial, sans-serif\" font-size=\"19\" font-weight=\"{weight}\">{html.escape(title)}</text>
      <text x=\"{x + w / 2}\" y=\"{y + 59}\" text-anchor=\"middle\" font-family=\"Arial, sans-serif\" font-size=\"14\">{html.escape(subtitle)}</text>
    """


def _arrow(x1: int, y1: int, x2: int, y2: int, label: str, *, dashed: bool, label_dx: int = 0, label_dy: int = 0, weight: int = 2) -> str:
    dash = 'stroke-dasharray="9 7"' if dashed else ""
    return f"""
      <line x1=\"{x1}\" y1=\"{y1}\" x2=\"{x2}\" y2=\"{y2}\" stroke=\"#111\" stroke-width=\"{weight}\" {dash} marker-end=\"url(#arrowhead)\"/>
      <text x=\"{(x1 + x2) / 2 + label_dx}\" y=\"{(y1 + y2) / 2 + label_dy}\" text-anchor=\"middle\" font-family=\"Arial, sans-serif\" font-size=\"13\" fill=\"#111\">{html.escape(label)}</text>
    """


def render_svg(response_report: dict[str, Any], factorial_report: dict[str, Any]) -> str:
    pollinator = _model(response_report, "impatiens_pollinator_rate_quasi_poisson")
    natural_damage = _model(response_report, "impatiens_flower_level_florivory_fractional_logit")
    seed = _model(response_report, "impatiens_ch_seed_count_quasi_poisson")
    fruit_factorial = _model(factorial_report, "impatiens_factorial_ch_fruit_rate")

    a_to_p = _ratio_label(_coefficient(pollinator, "A_z"), "obs RR")
    d_to_p = _ratio_label(_coefficient(pollinator, "D_z"), "obs RR")
    a_to_h = _ratio_label(_coefficient(natural_damage, "A_z"), "obs OR")
    d_to_h = _ratio_label(_coefficient(natural_damage, "D_z"), "obs OR")
    a_d_seed = _ratio_label(_coefficient(seed, "A_z:D_z"), "obs RR")
    imposed_h_to_f = _beta_label(_coefficient(fruit_factorial, "Florivory_c"))
    phenology_to_f = _beta_label(_coefficient(fruit_factorial, "Phenology_z"))

    svg = f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{WIDTH}\" height=\"{HEIGHT}\" viewBox=\"0 0 {WIDTH} {HEIGHT}\" role=\"img\" aria-labelledby=\"title desc\">
      <title id=\"title\">Impatiens capensis empirical channel ledger</title>
      <desc id=\"desc\">Observational flower-trait associations are dashed arrows. The imposed florivory treatment effect on chasmogamous fruit production is a solid randomized arrow. The diagram does not estimate total fitness or the Part A mixed partial.</desc>
      <defs>
        <marker id=\"arrowhead\" markerWidth=\"10\" markerHeight=\"7\" refX=\"9\" refY=\"3.5\" orient=\"auto\">
          <polygon points=\"0 0, 10 3.5, 0 7\" fill=\"#111\"/>
        </marker>
      </defs>
      <rect width=\"100%\" height=\"100%\" fill=\"white\"/>
      <text x=\"630\" y=\"42\" text-anchor=\"middle\" font-family=\"Arial, sans-serif\" font-size=\"27\" font-weight=\"700\">Impatiens capensis: empirical channel ledger</text>
      <text x=\"630\" y=\"67\" text-anchor=\"middle\" font-family=\"Arial, sans-serif\" font-size=\"15\">Dashed = observational trait association; solid = randomized imposed-florivory effect</text>
      <line x1=\"40\" y1=\"92\" x2=\"1220\" y2=\"92\" stroke=\"#777\" stroke-width=\"1\"/>

      {_node(70, 150, 240, 84, 'A: flower redness', 'pre-treatment attraction candidate')}
      {_node(70, 390, 240, 84, 'D candidate: floral tannins', 'pre-treatment chemical candidate')}
      {_node(500, 145, 245, 84, 'P: pollinator use', '60-min standardized visit rate')}
      {_node(500, 395, 245, 84, 'H: natural floral damage', 'flower-level tissue-loss fraction')}
      {_node(940, 155, 230, 84, 'Seeds per CH fruit', 'observational component surface')}
      {_node(940, 410, 230, 84, 'CH fruits per day', 'randomized treatment component', bold=True)}
      {_node(480, 600, 280, 84, 'Experimental florivory', 'randomized imposed floral damage', bold=True)}

      {_arrow(310, 192, 500, 187, a_to_p, dashed=True, label_dy=-12)}
      {_arrow(310, 432, 500, 437, d_to_h, dashed=True, label_dy=26)}
      {_arrow(310, 192, 500, 437, a_to_h, dashed=True, label_dx=-35, label_dy=-9)}
      {_arrow(310, 432, 500, 187, d_to_p, dashed=True, label_dx=36, label_dy=9, weight=3)}
      {_arrow(745, 187, 940, 197, 'pollination service not linked to component here', dashed=True, label_dy=-11)}
      {_arrow(745, 437, 940, 452, 'natural damage-to-fitness pathway not directly identified', dashed=True, label_dy=26)}
      {_arrow(760, 642, 940, 452, imposed_h_to_f, dashed=False, label_dx=40, label_dy=8, weight=3)}
      {_arrow(310, 432, 940, 197, 'A×D seed surface ' + a_d_seed, dashed=True, label_dy=-20)}
      <text x=\"940\" y=\"525\" text-anchor=\"middle\" font-family=\"Arial, sans-serif\" font-size=\"13\">Phenology → CH fruits/day: {html.escape(phenology_to_f)}</text>

      <rect x=\"66\" y=\"535\" width=\"367\" height=\"134\" rx=\"10\" fill=\"#f5f5f5\" stroke=\"#777\" stroke-width=\"1\"/>
      <text x=\"85\" y=\"563\" font-family=\"Arial, sans-serif\" font-size=\"15\" font-weight=\"700\">Interpretation boundary</text>
      <text x=\"85\" y=\"588\" font-family=\"Arial, sans-serif\" font-size=\"13\">• Trait arrows are adjusted observational associations.</text>
      <text x=\"85\" y=\"610\" font-family=\"Arial, sans-serif\" font-size=\"13\">• The only solid causal arrow is imposed florivory → CH fruit component.</text>
      <text x=\"85\" y=\"632\" font-family=\"Arial, sans-serif\" font-size=\"13\">• No total fitness surface, Part A mixed partial, or c_AD estimate.</text>

      <text x=\"630\" y=\"719\" text-anchor=\"middle\" font-family=\"Arial, sans-serif\" font-size=\"12\">Robust 95% intervals are reported in the companion tables; no coefficient products are interpreted.</text>
    </svg>"""
    return svg


def build_svg(response_report_path: str | Path, factorial_report_path: str | Path, output_path: str | Path) -> None:
    response_report = json.loads(Path(response_report_path).read_text(encoding="utf-8"))
    factorial_report = json.loads(Path(factorial_report_path).read_text(encoding="utf-8"))
    Path(output_path).write_text(render_svg(response_report, factorial_report), encoding="utf-8")
