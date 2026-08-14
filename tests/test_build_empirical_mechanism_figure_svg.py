from __future__ import annotations

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_empirical_mechanism_figure_svg.py"
COMMITTED = ROOT / "manuscript" / "figures" / "FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg"


def test_empirical_mechanism_figure_is_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "figure3.svg"
    subprocess.run([sys.executable, str(SCRIPT), str(output)], check=True)
    ET.parse(output)
    generated = output.read_text(encoding="utf-8")
    committed = COMMITTED.read_text(encoding="utf-8")
    assert generated == committed

    required = [
        "56 effect/directional records",
        "25 independent biological study clusters",
        "5 independent clusters",
        "8 independent clusters",
        "18 independent clusters",
        "10 independent clusters",
        "Same-system multi-route:",
        "14 clusters",
        "Context/sign switch:",
        "17 clusters",
        "Context-only programs:",
        ">7<",
        "guarded defence",
        "spatial / temporal / attack-mode filtering",
        "visitor functional-mode and lifecycle-role switching",
        "LRR −0.210 · 48 clusters",
        "LRR −0.483 · 28",
        "LRR −0.291 · 22",
        "florivore 84/103 · pollinator 151/220",
        "Risk difference +0.129 · LOCO positive 32/32",
        "Secondary contextual syntheses (3)",
        "1 strict cluster · sign unresolved",
        "0 strict estimates · κ unidentified",
        "Zero eligible estimates ≠ κ = 0",
        "IDENTIFICATION BOUNDARY",
        "not prevalence in nature",
        "none of the upper layers is W_AD",
    ]
    for token in required:
        assert token in generated
