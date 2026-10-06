from __future__ import annotations

import json
from pathlib import Path

from scripts.build_access_routing_letter_figures_svg import (
    build_figure1,
    build_figure3,
)

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "empirical" / "floral_defence_selectivity" / "results" / "joint_access_routing_species_robust.json"


def test_letter_figure1_states_prevalence_frequency_ambiguity() -> None:
    svg = build_figure1()
    assert "Higher robbery share can arise by different biological routes" in svg
    assert "robbery share = 10%" in svg
    assert "robbery share = 33%" in svg
    assert "robbery share = 44% ↑" in svg
    assert "45 ↑" in svg
    assert "10 ↓" in svg
    assert "8 ↓" in svg
    assert "Only zero-inclusive route-specific rates distinguish them" in svg
    assert "RR = 0.154" in svg
    assert "RR = 0.816" in svg
    assert "5.31  (1.92–14.67)" in svg
    assert "no detectable increase in robbery" in svg
    assert "Illustrative counts in A–C are schematic" in svg


def test_letter_figure3_uses_frozen_joint_result() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    svg = build_figure3(result)

    assert "One standardized routing effect recurs across networks" in svg
    assert "Sakhalkar insects" in svg
    assert "Aubert / EPHI birds" in svg
    assert "equal-network joint" in svg
    assert "0.347" in svg
    assert "0.503" in svg
    assert "0.428" in svg
    assert "p = 0.0001" in svg
    assert "What direct geometry studies can identify" in svg
    assert "Frozen 33-program direct frame" in svg
    assert "7  zero-inclusive both-route rates" in svg
    assert "18  robbery-prevalence only" in svg
    assert "6  conditional route choice" in svg
    assert "1 + 1  other non-strict designs" in svg
    assert "Post-hoc finite-frame design audit" in svg


def test_letter_figure3_keeps_equal_network_language() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    svg = build_figure3(result).lower()
    assert "equal network weight" in svg
    assert "raw observations are not pooled" in svg
    assert "causal" not in svg
