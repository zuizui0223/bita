from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.analyze_kessler_type_stage1 import REQUIRED_FIELDS


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "identification_design" / "KESSLER_TYPE_STAGE1_TRIAL_TEMPLATE_V1.csv"
RECEIPT = ROOT / "empirical" / "identification_design" / "KESSLER_STAGE1_CLUSTER_ALLOCATION_RECEIPT_V1.json"
READOUT = ROOT / "docs" / "KESSLER_STAGE1_CLUSTER_ALLOCATION_READOUT_V1.md"
CONTRACT = ROOT / "docs" / "KESSLER_TYPE_STAGE1_DATA_CONTRACT_V1.md"


def test_stage1_csv_template_exactly_matches_analyzer_contract() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        assert list(header) == list(REQUIRED_FIELDS)
        assert list(reader) == []


def test_actions_derived_cluster_receipt_freezes_practical_plant_anchors() -> None:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert data["source_workflow_run_id"] == 33237737070
    assert data["source_head_sha"] == "d4701bfb55bc8ab07b8b703e25f1e00f8f1f9b05"
    assert data["source_artifact_id"] == 9710411717
    assert data["source_artifact_sha256"] == "631c62c38b1fd09aca07c86b0897e96cd052ded91605b0a6b0b010292aff1008"

    anchors = {
        (row["scenario"], row["power"], row["flowers_per_plant"], row["icc"]): row
        for row in data["anchors"]
    }
    central = anchors[("published_central", 0.80, 5, 0.10)]
    attenuated = anchors[("attenuated_delta_0_17", 0.80, 5, 0.10)]
    assert central["plants_per_cell"] == 29
    assert central["total_plants_four_cells"] == 116
    assert central["total_introduced_flowers_four_cells"] == 580
    assert attenuated["plants_per_cell"] == 47
    assert attenuated["total_plants_four_cells"] == 188
    assert attenuated["total_introduced_flowers_four_cells"] == 940
    assert "not a hierarchical or randomization-based power guarantee" in data["claim_boundary"]


def test_readout_keeps_flower_counts_separate_from_independent_plant_replication() -> None:
    text = READOUT.read_text(encoding="utf-8")
    assert "29 plants per A×D state / 116 plants total" in text
    assert "47 plants per state / 188 plants total" in text
    assert "repeated flowers cannot be counted as independent replication" in text
    assert "block_id + plant_id + flower_id" in text
    assert "ESCAPE_IDENTIFIED / ESCAPE_REFUTED / ESCAPE_UNRESOLVED" in text


def test_data_contract_preserves_scope_complete_blocks_and_channel_boundary() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "FLOWER_RESTRICTED_VALIDATED" in text
    assert "SYSTEMIC_SOURCE_FAITHFUL" in text
    assert "UNVERIFIED" in text
    assert "Each retained block" in text
    assert "all four A × D cells" in text
    assert "None of the three outcome levels allocates the observed surface" in text
    assert "rho_delta    antagonist relief" in text
    assert "iota_delta   pollinator interference" in text
    assert "kappa_delta  remaining joint channel" in text
    assert "No Stage-1 result is allowed to manufacture channel values" in text
