from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_empirical_mechanism_figure_svg.py"
OUTPUT = ROOT / "manuscript" / "figures" / "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg"

text = BUILDER.read_text(encoding="utf-8")
old = '<text x="800" y="813" text-anchor="middle" class="body">Secondary contextual syntheses ({stats.secondary_context_modules}): Haas-Desmarais 2026 · Caruso 2019 · Junker &amp; Blüthgen 2010</text>'
new = '<text x="800" y="813" text-anchor="middle" class="small">Secondary contextual syntheses ({stats.secondary_context_modules}): Haas-Desmarais 2026 · Caruso 2019 · Junker &amp; Blüthgen 2010</text>'
if old not in text:
    raise RuntimeError("missing Figure 3 secondary-context line")
BUILDER.write_text(text.replace(old, new, 1), encoding="utf-8")
subprocess.run([sys.executable, str(BUILDER), str(OUTPUT)], check=True)
print("Figure 3 secondary-context line fitted inside its box")
