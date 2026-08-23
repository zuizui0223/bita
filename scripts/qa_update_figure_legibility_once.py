from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing expected patch target: {label}")
    return text.replace(old, new, 1)


# Figure 3: preserve geometry and every frozen result, but increase the
# publication-facing type hierarchy so small annotations remain legible at
# a 6.5-inch final vector width.
fig3_path = ROOT / "scripts" / "build_empirical_mechanism_figure_svg.py"
fig3 = fig3_path.read_text(encoding="utf-8")
old_css = (
    '.title{{font:700 34px DejaVu Sans,Arial,sans-serif}} .subtitle{{font:700 24px DejaVu Sans,Arial,sans-serif}}\n'
    '.body{{font:20px DejaVu Sans,Arial,sans-serif}} .small{{font:17px DejaVu Sans,Arial,sans-serif}} .tiny{{font:15px DejaVu Sans,Arial,sans-serif}}'
)
new_css = (
    '.title{{font:700 34px DejaVu Sans,Arial,sans-serif}} .subtitle{{font:700 26px DejaVu Sans,Arial,sans-serif}}\n'
    '.body{{font:23px DejaVu Sans,Arial,sans-serif}} .small{{font:21px DejaVu Sans,Arial,sans-serif}} .tiny{{font:19px DejaVu Sans,Arial,sans-serif}}'
)
fig3 = must_replace(fig3, old_css, new_css, "Figure 3 typography")
fig3_path.write_text(fig3, encoding="utf-8")


# Figure 5 source (historically Supplementary Figure S3): use a more compact
# canvas while enlarging all text. The 14 rows and four route-presence columns
# are unchanged; this is presentation-only.
supp_path = ROOT / "scripts" / "build_supplementary_figures_svg.py"
supp = supp_path.read_text(encoding="utf-8")
pattern = re.compile(r"def build_s3\(\) -> str:\n.*?(?=\n\ndef parse_robustness\(\))", re.S)
new_s3 = '''def build_s3() -> str:
    matrix = same_system_routes()
    if len(matrix) != 14:
        raise ValueError(f"expected 14 same-system clusters, found {len(matrix)}")
    # Compact canvas + larger relative typography for publication-width use.
    width, height = 1000, 820
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    x0 = 370
    y0 = 86
    cw = 150
    rh = 48
    labels = {
        "A_to_pollination": "A → pollination",
        "A_to_antagonism": "A → antagonism",
        "D_to_antagonism": "D → antagonism",
        "D_to_pollination": "D → pollination",
    }
    for i, route in enumerate(ROUTES):
        parts.append(_svg_text(x0 + i*cw + (cw-8)/2, 52, labels[route], 16, anchor="middle", weight=700))
    for j, (cluster, routes) in enumerate(matrix.items()):
        y = y0 + j*rh
        parts.append(_svg_text(x0 - 14, y + 30, cluster.replace("_", " "), 14, anchor="end"))
        for i, route in enumerate(ROUTES):
            fill = "#444" if route in routes else "#f4f4f4"
            parts.append(f'<rect x="{x0+i*cw}" y="{y}" width="{cw-8}" height="{rh-7}" fill="{fill}" stroke="#777"/>')
            if route in routes:
                parts.append(_svg_text(x0 + i*cw + (cw-8)/2, y + 27, "present", 13, anchor="middle", weight=700))
    parts.append(_svg_text(500, 790, "Rows are independent biological clusters with at least two linked marginal routes (or an explicit same-system linkage flag).", 13, anchor="middle"))
    parts.append(_svg_text(500, 810, "Presence is categorical; cells are not effect sizes.", 13, anchor="middle"))
    parts.append('</svg>')
    return "\\n".join(parts) + "\\n"
'''
supp, count = pattern.subn(lambda _m: new_s3, supp, count=1)
if count != 1:
    raise RuntimeError("failed to patch Figure 5 source builder")
supp_path.write_text(supp, encoding="utf-8")


# Regenerate all three committed SVGs from their canonical sources. No result
# values are supplied here: Figure 2 is rebuilt from the 2,592-evaluation run;
# Figure 3 reads the frozen evidence ledgers; Figure 5 reads the same-system
# route universe.
qa_dir = ROOT / "artifacts" / "qa_figure_legibility" / "part_i"
qa_dir.mkdir(parents=True, exist_ok=True)
subprocess.run(
    [
        sys.executable,
        str(ROOT / "scripts" / "run_part_i_robustness.py"),
        str(ROOT / "configs" / "part_i_robustness_grid.json"),
        str(qa_dir),
    ],
    check=True,
)
subprocess.run(
    [
        sys.executable,
        str(ROOT / "scripts" / "build_part_i_regime_figure_svg.py"),
        str(qa_dir / "part_i_sensitivity_evaluations.csv"),
        str(ROOT / "manuscript" / "figures" / "FIGURE_2_THEORY_REGIME_MAP.svg"),
    ],
    check=True,
)
subprocess.run(
    [
        sys.executable,
        str(fig3_path),
        str(ROOT / "manuscript" / "figures" / "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg"),
    ],
    check=True,
)

spec = importlib.util.spec_from_file_location("supp_builder", supp_path)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load supplementary figure builder")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fig5 = module.build_s3()
fig5_path = ROOT / "manuscript" / "supplementary" / "figures" / "FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg"
fig5_path.write_text(fig5, encoding="utf-8")

# Guardrails: scientific values/counts must still be present.
fig2_text = (ROOT / "manuscript" / "figures" / "FIGURE_2_THEORY_REGIME_MAP.svg").read_text(encoding="utf-8")
for token in ("51.9% complementary", "48.1% complementary", "not empirical probabilities"):
    if token not in fig2_text:
        raise RuntimeError(f"Figure 2 guardrail missing: {token}")
fig3_text = (ROOT / "manuscript" / "figures" / "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg").read_text(encoding="utf-8")
for token in ("56 effect/directional records", "25 independent biological study clusters", "14 clusters", "17 clusters", "LRR −0.210 · 48 clusters", "Risk difference +0.129 · LOCO positive 32/32", "0 strict estimates · κ unidentified"):
    if token not in fig3_text:
        raise RuntimeError(f"Figure 3 guardrail missing: {token}")
for token in ("A → pollination", "D → pollination", "Rows are independent biological clusters"):
    if token not in fig5:
        raise RuntimeError(f"Figure 5 guardrail missing: {token}")

print("publication-legibility SVGs regenerated from frozen sources")
