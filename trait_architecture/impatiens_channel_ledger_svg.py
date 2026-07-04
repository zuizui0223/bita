"""Render a monochrome theory-to-empirics channel-ledger SVG for Impatiens.

The figure intentionally distinguishes observational trait associations (dashed
arrows) from the randomized imposed-florivory treatment effect (solid arrow). It
shows only measured links: the four trait-channel associations, the separate A×D
seed-component surface, and the imposed-damage effect on CH fruit production.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Iterable


WIDTH = 1280
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


def _node(x: int, y: int, w: int, h: int, title: str, lines: Iterable[str], *, bold: bool = False) -> str:
    weight = "700" if bold else "600"
    output = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="white" stroke="#111" stroke-width="2"/>',
        f'<text x="{x + w / 2}" y="{y + 31}" text-anchor="middle" font-family="Arial, sans-serif" font-size="19" font-weight="{weight}">{html.escape(title)}</text>',
    ]
    for index, line in enumerate(lines):
        output.append(
            f'<text x="{x + w / 2}" y="{y + 57 + index * 22}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13">{html.escape(line)}</text>'
        )
    return "\n      ".join(output)


def _arrow(x1: int, y1: int, x2: int, y2: int, *, dashed: bool, weight: int = 2) -> str:
    dash = 'stroke-dasharray="9 7"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="{weight}" {dash} marker-end="url(#arrowhead)"/>'


def render_svg(response_report: dict[str, Any], factorial_report: dict[str, Any]) -> str:
    pollinator = _model(response_report, "impatiens_pollinator_rate_quasi_poisson")
    natural_damage = _model(response_report, "impatiens_flower_level_florivory_fractional_logit")
    seed = _model(response_report, "impatiens_ch_seed_count_quasi_poisson")
    fruit_factorial = _model(factorial_report, "impatiens_factorial_ch_fruit_rate")

    a_to_p = _ratio_label(_coefficient(pollinator, "A_z"), "A→P obs RR")
    d_to_p = _ratio_label(_coefficient(pollinator, "D→P obs RR") if False else _coefficient(pollinator, "D_z"), "D→P obs RR")
    a_to_h = _ratio_label(_coefficient(natural_damage, "A_z"), "A→H obs OR")
    d_to_h = _ratio_label(_coefficient(natural_damage, "D_z"), "D→H obs OR")
    a_d_seed = _ratio_label(_coefficient(seed, "A_z:D_z"), "A×D obs RR")
    imposed_h_to_f = _beta_label(_coefficient(fruit_factorial, "Florivory_c"))
    phenology_to_f = _beta_label(_coefficient(fruit_factorial, "Phenology_z"))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
      <title id="title">Impatiens capensis empirical channel ledger</title>
      <desc id="desc">Dashed arrows are observational trait associations. The one solid arrow is the randomized imposed-florivory effect on chasmogamous fruit production. The diagram does not estimate total fitness or the Part A mixed partial.</desc>
      <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="#111"/>
        </marker>
      </defs>
      <rect width="100%" height="100%" fill="white"/>
      <text x="640" y="42" text-anchor="middle" font-family="Arial, sans-serif" font-size="27" font-weight="700">Impatiens capensis: empirical channel ledger</text>
      <text x="640" y="67" text-anchor="middle" font-family="Arial, sans-serif" font-size="15">Dashed = observational trait association; solid = randomized imposed-florivory effect</text>
      <line x1="40" y1="92" x2="1240" y2="92" stroke="#777" stroke-width="1"/>

      {_node(60, 155, 250, 82, 'A: flower redness', ('pre-treatment attraction candidate',))}
      {_node(60, 405, 250, 82, 'D candidate: floral tannins', ('pre-treatment chemical candidate',))}
      {_node(470, 125, 325, 142, 'P: pollinator use', ('60-min standardized visit rate', a_to_p, d_to_p))}
      {_node(470, 380, 325, 142, 'H: natural floral damage', ('flower-level tissue-loss fraction', a_to_h, d_to_h))}
      {_node(940, 135, 280, 128, 'Seeds per CH fruit', ('observational component surface', a_d_seed, 'No resolved A×D component interaction'))}
      {_node(940, 410, 280, 128, 'CH fruits per day', ('randomized treatment component', 'Imposed florivory ' + imposed_h_to_f, 'Phenology ' + phenology_to_f), bold=True)}
      {_node(495, 620, 280, 72, 'Experimental florivory', ('randomized imposed floral damage',), bold=True)}

      {_arrow(310, 196, 470, 187, dashed=True)}
      {_arrow(310, 446, 470, 447, dashed=True)}
      {_arrow(310, 196, 470, 447, dashed=True)}
      {_arrow(310, 446, 470, 187, dashed=True, weight=3)}
      {_arrow(775, 656, 940, 474, dashed=False, weight=3)}

      <rect x="55" y="555" width="382" height="132" rx="10" fill="#f5f5f5" stroke="#777" stroke-width="1"/>
      <text x="76" y="582" font-family="Arial, sans-serif" font-size="15" font-weight="700">Interpretation boundary</text>
      <text x="76" y="607" font-family="Arial, sans-serif" font-size="13">• All flower-trait arrows are adjusted observational associations.</text>
      <text x="76" y="629" font-family="Arial, sans-serif" font-size="13">• The solid arrow is an assigned-treatment effect on a reproductive component.</text>
      <text x="76" y="651" font-family="Arial, sans-serif" font-size="13">• No total fitness surface, Part A mixed partial, or c_AD estimate.</text>

      <text x="640" y="730" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Robust 95% intervals are reported in companion tables; no coefficient products are interpreted.</text>
    </svg>"""


def build_svg(response_report_path: str | Path, factorial_report_path: str | Path, output_path: str | Path) -> None:
    response_report = json.loads(Path(response_report_path).read_text(encoding="utf-8"))
    factorial_report = json.loads(Path(factorial_report_path).read_text(encoding="utf-8"))
    Path(output_path).write_text(render_svg(response_report, factorial_report), encoding="utf-8")
