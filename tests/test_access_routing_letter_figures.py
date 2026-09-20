from __future__ import annotations

import json
from pathlib import Path

from scripts.build_access_routing_letter_figures_svg import (
    build_figure1,
    build_figure3,
)

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "empirical" / "floral_defence_selectivity" / "results" / "joint_access_routing.json"


def test_letter_figure1_states_access_routing_prediction() -> None:
    svg = build_figure1()
    assert "Access constraints reroute exploitation" in svg
    assert "legitimate route" in svg
    assert "bypass / robbing" in svg
    assert "mismatch" in svg.lower()
    assert "filtering" in svg.lower()
    assert "rerouting" in svg.lower()


def test_letter_figure3_uses_frozen_joint_result() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    svg = build_figure3(result)

    assert "One standardized routing effect recurs across networks" in svg
    assert "Sakhalkar insects" in svg
    assert "Aubert / EPHI birds" in svg
    assert "equal-network joint" in svg
    assert "0.347" in svg
    assert "0.351" in svg
    assert "0.349" in svg
    assert "p = 0.0001" in svg
    assert "17 D-side study programs" in svg
    assert "11 / 11" in svg
    assert "8 within-D switching systems" in svg


def test_letter_figure3_keeps_equal_network_language() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    svg = build_figure3(result).lower()
    assert "equal network weight" in svg
    assert "raw observations are not pooled" in svg
    assert "causal" not in svg
