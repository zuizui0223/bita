from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "scripts" / "build_part_i_regime_figure_svg.py"
SUPP = ROOT / "scripts" / "build_supplementary_figures_svg.py"
AUG = ROOT / "scripts" / "augment_supplementary_s4_modern_estimator.py"
WORKFLOW = ROOT / ".github" / "workflows" / "_visual-layout-patch-tmp.yml"
SELF = Path(__file__)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f"{label}: expected one match, found {text.count(old)}")
    return text.replace(old, new, 1)


# Main Fig. 2: rotate the environmental y-axis title into the inter-panel gutter.
text = MAIN.read_text(encoding="utf-8")
text = replace_once(
    text,
    '    parts.append(_text(x1 - 75, y1 + 1.5*cell, "Floral damage pressure", size=14, anchor="middle"))',
    '    axis_x, axis_y = x1 - 48, y1 + 1.5*cell\n'
    '    parts.append(f\'<text x="{axis_x}" y="{axis_y}" transform="rotate(-90 {axis_x} {axis_y})" font-family="Arial, sans-serif" font-size="14" text-anchor="middle">Floral damage pressure</text>\')',
    "Fig2 environmental axis label",
)
MAIN.write_text(text, encoding="utf-8")

# Supplement: fix S1 y labels, S2 left margin, and separate S4 panels.
text = SUPP.read_text(encoding="utf-8")
text = replace_once(
    text,
    '        parts.append(_svg_text(x0 + 10, y0 + 42, "finite-difference mixed partial", 12))',
    '        axis_x, axis_y = x0 + 12, y0 + 150\n'
    '        parts.append(f\'<text x="{axis_x:.1f}" y="{axis_y:.1f}" transform="rotate(-90 {axis_x:.1f} {axis_y:.1f})" text-anchor="middle" font-family="DejaVu Sans,Arial,sans-serif" font-size="12">finite-difference mixed partial</text>\')',
    "S1 y-axis label",
)
text = replace_once(text, '    width, height = 1700, 1500', '    width, height = 2050, 1500', "S2 width")
text = replace_once(text, '    cell = 62; panel_w = 390; panel_h = 330; x_start=105; y_start=115', '    cell = 62; panel_w = 390; panel_h = 330; x_start=360; y_start=115', "S2 margin")
text = replace_once(
    text,
    '        parts.append(_svg_text(15, y_start + rr*panel_h + 115, scenario.replace("_", " "), 13, weight=700))',
    '        parts.append(_svg_text(x_start - 28, y_start + rr*panel_h + 115, scenario.replace("_", " "), 13, anchor="end", weight=700))',
    "S2 row label anchor",
)
text = replace_once(text, '    width,height=1450,720', '    width,height=1600,720', "S4 width")
text = replace_once(text, '    x0=270; y0=120; scale=760', '    x0=250; y0=120; scale=560', "S4 panel A scale")
text = replace_once(text, '    parts.append(_svg_text(780,55,"B  FVOC reproduced synthesis",20,weight=700))', '    parts.append(_svg_text(900,55,"B  FVOC reproduced synthesis",20,weight=700))', "S4 panel B title")
text = replace_once(text, '    bx0=820; by=190; bscale=500; bmin=0.0; bmax=0.22', '    bx0=980; by=190; bscale=430; bmin=0.0; bmax=0.22', "S4 panel B scale")
old = '''    parts.append(f'<line x1="{bs(r["s_min"]):.1f}" y1="{by}" x2="{bs(r["s_max"]):.1f}" y2="{by}" stroke="#222" stroke-width="8"/>')
    parts.append(f'<circle cx="{bs(r["s_median"]):.1f}" cy="{by}" r="9" fill="#fff" stroke="#111" stroke-width="3"/>')
    parts.append(f'<circle cx="{bs(v["sas"]):.1f}" cy="{by}" r="7" fill="#111"/>')
    for x,label in ((r["s_min"],"min"),(r["s_median"],"median"),(r["s_max"],"max"),(v["sas"],"full")):
        parts.append(_svg_text(bs(x),by+42,f"{label} {x:+.4f}",11,anchor="middle"))
    parts.append(_svg_text(790,300,"32/32 leave-one-study-component-out contrasts remain positive",14,weight=700))
    parts.append(_svg_text(790,333,"Only three study components contain both physiological roles; all three paired differences are zero",12))
    parts.append(_svg_text(790,365,"The assembled +0.129 pattern is therefore not a causal within-study pollinator-versus-florivore effect",12))
    parts.append(_svg_text(725,680,"Robustness metrics remain module-specific: continuous LRR influence/heterogeneity for Leal; categorical study-component influence and composition limits for Sasidharan.",13,anchor="middle"))'''
new = '''    parts.append(f'<line x1="{bs(r["s_min"]):.1f}" y1="{by}" x2="{bs(r["s_max"]):.1f}" y2="{by}" stroke="#222" stroke-width="8"/>')
    parts.append(f'<circle cx="{bs(r["s_median"]):.1f}" cy="{by}" r="9" fill="#fff" stroke="#111" stroke-width="3"/>')
    parts.append(f'<circle cx="{bs(v["sas"]):.1f}" cy="{by-22}" r="7" fill="#111"/>')
    parts.append(_svg_text(bs(v["sas"]), by-42, f"full {v['sas']:+.3f}", 11, anchor="middle", weight=700))
    parts.append(_svg_text(bs(r["s_min"]), by+42, f"min {r['s_min']:+.4f}", 11, anchor="start"))
    parts.append(_svg_text(bs(r["s_median"]), by+42, f"median {r['s_median']:+.4f}", 11, anchor="middle"))
    parts.append(_svg_text(bs(r["s_max"]), by+42, f"max {r['s_max']:+.4f}", 11, anchor="end"))
    parts.append(_svg_text(920,300,"32/32 leave-one-study-component-out contrasts remain positive",14,weight=700))
    parts.append(_svg_text(920,333,"Only three study components contain both physiological roles; all three paired differences are zero",12))
    parts.append(_svg_text(920,365,"The assembled +0.129 pattern is therefore not a causal within-study pollinator-versus-florivore effect",12))
    parts.append(_svg_text(800,680,"Robustness metrics remain module-specific: continuous LRR influence/heterogeneity for Leal; categorical study-component influence and composition limits for Sasidharan.",13,anchor="middle"))'''
text = replace_once(text, old, new, "S4 panel B layout")
SUPP.write_text(text, encoding="utf-8")

# S4 modern-estimator inset: separate the interval plot from its numeric labels.
text = AUG.read_text(encoding="utf-8")
text = replace_once(
    text,
    'def _x(value: float, *, x0: float = 300.0, width: float = 390.0, lo: float = -0.85, hi: float = 0.05) -> float:',
    'def _x(value: float, *, x0: float = 330.0, width: float = 290.0, lo: float = -0.85, hi: float = 0.05) -> float:',
    "S4 inset x scale",
)
text = replace_once(text, '<rect x="55" y="474" width="690" height="170" fill="#ffffff" stroke="#aaaaaa" stroke-width="1"/>', '<rect x="55" y="474" width="930" height="170" fill="#ffffff" stroke="#aaaaaa" stroke-width="1"/>', "S4 inset width")
text = replace_once(
    text,
    '                f\'<text x="700" y="{y + 4:.1f}" text-anchor="end" font-family="DejaVu Sans,Arial,sans-serif" font-size="10">REML {_fmt(pooled)}; mHK [{_fmt(low)}, {_fmt(high)}]{"; borderline to zero" if borderline else ""}</text>\',',
    '                f\'<text x="640" y="{y + 4:.1f}" text-anchor="start" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">REML {_fmt(pooled)}; mHK [{_fmt(low)}, {_fmt(high)}]{"; borderline to zero" if borderline else ""}</text>\',',
    "S4 inset numeric labels",
)
text = replace_once(text, '<text x="300" y="638" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">-0.85</text>', '<text x="330" y="638" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">-0.85</text>', "S4 inset left tick")
text = replace_once(text, '<text x="690" y="638" text-anchor="end" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">0.05</text>', '<text x="620" y="638" text-anchor="end" font-family="DejaVu Sans,Arial,sans-serif" font-size="9">0.05</text>', "S4 inset right tick")
AUG.write_text(text, encoding="utf-8")

if WORKFLOW.exists():
    WORKFLOW.unlink()
if SELF.exists():
    SELF.unlink()
