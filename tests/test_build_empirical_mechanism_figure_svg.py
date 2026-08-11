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
        "38 effect/directional records",
        "14 independent biological study clusters",
        "4 independent clusters",
        "5 independent clusters",
        "10 independent clusters",
        "7 independent clusters",
        "Same-system multi-route:",
        "10 clusters",
        "Context/sign switch:",
        "11 clusters",
        "LRR −0.210 · 48 clusters",
        "LRR −0.483 · 28",
        "LRR −0.291 · 22",
        "florivore 84/103 · pollinator 151/220",
        "risk difference +0.129 · LOCO positive 32/32",
        "1 strict cluster · sign unresolved",
        "0 strict estimates · κ unidentified",
        "Zero eligible estimates ≠ κ = 0",
        "IDENTIFICATION BOUNDARY",
        "not W_AD",
    ]
    for token in required:
        assert token in generated
