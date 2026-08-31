from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "empirical" / "identification_design" / "KESSLER_TYPE_REPLICATION_POWER_V1.json"
PLAN = ROOT / "docs" / "KESSLER_TYPE_REPLICATION_AND_AUGMENTATION_V1.md"


def test_registered_key_level1_sample_sizes_remain_fail_closed() -> None:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    scenarios = {row["scenario"]: row for row in data["key_scenarios"]}
    central = scenarios["published_central"]
    conservative = scenarios["attenuated_delta_0_17"]
    assert central["planned_n_per_cell_80pct_design_effect_1_5"] == 154
    assert central["planned_total_four_cell_80pct_design_effect_1_5"] == 616
    assert conservative["planned_n_per_cell_80pct_design_effect_1_5"] == 250
    assert conservative["planned_total_four_cell_80pct_design_effect_1_5"] == 1000
    assert "not a power guarantee" in data["claim_boundary"]


def test_plan_separates_level1_release_and_mechanism_allocation() -> None:
    text = PLAN.read_text(encoding="utf-8")
    for token in (
        "Stage 1a — total interaction relief",
        "Stage 1b — strict Level-2/3 release is a different power problem",
        "Stage 2 — pilot the missing channel contrasts",
        "Stage 3 — full mechanism allocation",
        "alpha/2 = 0.025",
        "not high-power identifiable as strict Level 2/3",
        "11816",
        "No post-hoc epsilon rescue",
        "If A1 is positive but A0 remains zero-compatible: report **partial identification**",
        "Legacy token `ESCAPE_IDENTIFIED`",
    ):
        assert token in text
    assert "Do not borrow the Kessler total Delta" in text
    assert "tens of thousands of observations" in text
