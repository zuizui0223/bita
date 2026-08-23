from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing expected patch target: {label}")
    return text.replace(old, new, 1)


# Figure 2: create more breathing room between Panel A and the vertical
# environment-axis label. Numerical values and panel geometry are otherwise
# unchanged.
fig2_path = ROOT / "scripts" / "build_part_i_regime_figure_svg.py"
fig2 = fig2_path.read_text(encoding="utf-8")
fig2 = must_replace(fig2, "    x1, y1, cell = 390, 165, 66", "    x1, y1, cell = 410, 165, 66", "Figure 2 grid position")
fig2 = must_replace(fig2, '    parts.append(_text(365, 68, "B  Interaction environment", size=16, weight="bold"))', '    parts.append(_text(390, 68, "B  Interaction environment", size=16, weight="bold"))', "Figure 2 panel title")
fig2 = must_replace(fig2, "    axis_x, axis_y = x1 - 44, y1 + 1.5*cell", "    axis_x, axis_y = x1 - 50, y1 + 1.5*cell", "Figure 2 axis label")
fig2_path.write_text(fig2, encoding="utf-8")


# Figure 3: the larger publication-facing typography is retained, but two long
# conditionality bullets are wrapped inside a slightly deeper right-hand box.
fig3_path = ROOT / "scripts" / "build_empirical_mechanism_figure_svg.py"
fig3 = fig3_path.read_text(encoding="utf-8")
fig3 = must_replace(
    fig3,
    '<rect x="960" y="225" width="585" height="310" rx="16" class="box"/>',
    '<rect x="960" y="225" width="585" height="330" rx="16" class="box"/>',
    "Figure 3 conditionality box",
)
old_block = '''<text x="995" y="415" class="small">Recurring state transitions</text>
<text x="1015" y="444" class="tiny">• guarded defence: antagonist relief without universal pollinator cost</text>
<text x="1015" y="468" class="tiny">• spatial / temporal / attack-mode filtering</text>
<text x="1015" y="492" class="tiny">• visitor functional-mode and lifecycle-role switching</text>
<text x="1015" y="516" class="tiny">• response-stage, resource, population and trait-class dependence</text>'''
new_block = '''<text x="995" y="407" class="small">Recurring state transitions</text>
<text x="1015" y="431" class="tiny">• guarded defence: antagonist relief</text>
<text x="1035" y="451" class="tiny">without universal pollinator cost</text>
<text x="1015" y="475" class="tiny">• spatial / temporal / attack-mode filtering</text>
<text x="1015" y="499" class="tiny">• visitor functional-mode and lifecycle-role switching</text>
<text x="1015" y="523" class="tiny">• response-stage, resource, population</text>
<text x="1035" y="543" class="tiny">and trait-class dependence</text>'''
fig3 = must_replace(fig3, old_block, new_block, "Figure 3 wrapped conditionality bullets")
fig3_path.write_text(fig3, encoding="utf-8")


# Regenerate committed Figure 2 from the canonical 2,592-evaluation run and
# committed Figure 3 from the frozen evidence ledgers.
qa_dir = ROOT / "artifacts" / "qa_final_figure_spacing" / "part_i"
qa_dir.mkdir(parents=True, exist_ok=True)
subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "run_part_i_robustness.py"), str(ROOT / "configs" / "part_i_robustness_grid.json"), str(qa_dir)],
    check=True,
)
subprocess.run(
    [sys.executable, str(fig2_path), str(qa_dir / "part_i_sensitivity_evaluations.csv"), str(ROOT / "manuscript" / "figures" / "FIGURE_2_THEORY_REGIME_MAP.svg")],
    check=True,
)
subprocess.run(
    [sys.executable, str(fig3_path), str(ROOT / "manuscript" / "figures" / "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg")],
    check=True,
)

print("final Figure 2/3 spacing fixes regenerated from frozen sources")
