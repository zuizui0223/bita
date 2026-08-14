from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts" / "build_supplementary_figures_svg.py"
WORKFLOW = ROOT / ".github" / "workflows" / "_visual-layout-final-tmp.yml"
SELF = Path(__file__)
text = TARGET.read_text(encoding="utf-8")
replacements = (
    ("    width, height = 2050, 1500", "    width, height = 2200, 1500"),
    ("    cell = 62; panel_w = 390; panel_h = 330; x_start=360; y_start=115", "    cell = 62; panel_w = 390; panel_h = 330; x_start=460; y_start=115"),
    ('    parts.append(_svg_text(bs(r["s_median"]), by+42, f"median {r[\'s_median\']:+.4f}", 11, anchor="middle"))', '    parts.append(_svg_text(bs(r["s_median"]), by+62, f"median {r[\'s_median\']:+.4f}", 11, anchor="middle"))'),
)
for old, new in replacements:
    if text.count(old) != 1:
        raise RuntimeError(f"expected one match for {old!r}, found {text.count(old)}")
    text = text.replace(old, new, 1)
TARGET.write_text(text, encoding="utf-8")
if WORKFLOW.exists():
    WORKFLOW.unlink()
if SELF.exists():
    SELF.unlink()
