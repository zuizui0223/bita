from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "empirical" / "identification_design" / "KESSLER_TYPE_REPLICATION_POWER_V1.json"
PLAN = ROOT / "docs" / "KESSLER_TYPE_REPLICATION_AND_AUGMENTATION_V1.md"


def test_registered_key_sample_sizes_are_fail_closed() -> None:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    scenarios = {row["scenario"]: row for row in data["key_scenarios"]}
    central = scenarios["published_central"]
    conservative = scenarios["attenuated_delta_0_17"]
    assert central["planned_n_per_cell_80pct_design_effect_1_5"] == 154
    assert central["planned_total_four_cell_80pct_design_effect_1_5"] == 616
    assert conservative["planned_n_per_cell_80pct_design_effect_1_5"] == 250
    assert conservative["planned_total_four_cell_80pct_design_effect_1_5"] == 1000
    assert "not a power guarantee" in data["claim_boundary"]


def test_plan_stages_total_sign_before_mechanism_allocation() -> None:
    text = PLAN.read_text(encoding="utf-8")
    assert "Stage 1 — confirm the total escape sign" in text
    assert "Stage 2 — pilot the missing channel contrasts" in text
    assert "Stage 3 — full mechanism allocation" in text
    assert "16-cell number is a budget warning" in text
    assert "do not borrow the Kessler total Delta" in text
    assert "ESCAPE_IDENTIFIED" in text
    assert "ESCAPE_REFUTED" in text
    assert "ESCAPE_UNRESOLVED" in text
