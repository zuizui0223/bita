from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READOUT = ROOT / "empirical" / "mechanism_pattern_synthesis" / "PATTERN_EXPANSION_READOUT_V1.json"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"


def test_manuscript_facing_pattern_counts_match_admitted_combined_readout() -> None:
    payload = json.loads(READOUT.read_text(encoding="utf-8"))
    combined = payload["combined_provisional"]
    assert combined["records"] == 56
    assert combined["independent_clusters"] == 25
    assert combined["same_system_clusters"] == 14
    assert payload["context_switch_clusters_provisional"] == 17
    assert payload["context_programs_excluded_from_route_N"] == 7

    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "56 route-level records from 25 independent biological study clusters" in text
    assert "Fourteen same-system clusters" in text
    assert "17 sign/state-switch clusters" in text
    assert "seven context-only programs" in text
    assert "These annotations are not additive counts" in text


def test_readout_itself_records_nonadditivity_boundary() -> None:
    payload = json.loads(READOUT.read_text(encoding="utf-8"))
    boundary = "\n".join(payload["interpretation_boundary"])
    assert "route counts overlap" in boundary
    assert "must not be summed" in boundary
    assert "context-only" in boundary.lower() or "environmental-context-only" in boundary.lower()
