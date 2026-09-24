from __future__ import annotations

import json

import pytest

import scripts.freeze_third_network_confirmatory_inputs as freezer
from scripts.freeze_third_network_confirmatory_inputs import freeze_inputs
from scripts.run_third_network_synthetic_e2e import run as run_synthetic_e2e


def _fixture(tmp_path):
    root = tmp_path / "fixture"
    run_synthetic_e2e(root, permutations=19, scenario="positive")
    return root


def _freeze(root):
    return freeze_inputs(
        events_csv=root / "confirmatory_events.csv",
        plant_traits_csv=root / "plant_traits.csv",
        mammal_traits_csv=root / "mammal_traits.csv",
        camera_deployment_csv=root / "camera_deployment.csv",
        confirmatory_freeze_json=root / "confirmatory_freeze.json",
        field_readiness_json=root / "field_readiness_receipt.json",
    )


def test_input_freeze_records_semantic_resource_receipt(tmp_path) -> None:
    root = _fixture(tmp_path)
    receipt = _freeze(root)
    resource = receipt["semantic_resource_limits"]

    assert resource["status"] == "SEMANTIC_RESOURCE_LIMITS_PASS"
    assert resource["observed"]["events_rows"] > 0
    assert resource["observed"]["plant_trait_rows"] > 0
    assert resource["observed"]["mammal_trait_rows"] > 0
    assert resource["observed"]["camera_deployment_rows"] > 0
    assert resource["limits"]["max_event_rows"] == freezer.MAX_EVENT_ROWS
    assert resource["limits"]["max_control_json_bytes"] == freezer.MAX_CONTROL_JSON_BYTES

    for entry in receipt["files"].values():
        assert int(entry["bytes"]) > 0
        assert len(entry["sha256"]) == 64


def test_input_freeze_rejects_event_row_exhaustion_before_analysis(
    tmp_path,
    monkeypatch,
) -> None:
    root = _fixture(tmp_path)
    monkeypatch.setattr(freezer, "MAX_EVENT_ROWS", 1)

    with pytest.raises(
        ValueError,
        match="SEMANTIC_RESOURCE_LIMIT_EXCEEDED:events:rows=",
    ):
        _freeze(root)


def test_input_freeze_rejects_control_json_size_exhaustion(
    tmp_path,
    monkeypatch,
) -> None:
    root = _fixture(tmp_path)
    monkeypatch.setattr(freezer, "MAX_CONTROL_JSON_BYTES", 1)

    with pytest.raises(
        ValueError,
        match="SEMANTIC_RESOURCE_LIMIT_EXCEEDED:field_readiness:bytes=",
    ):
        _freeze(root)


def test_input_freeze_rejects_csv_byte_exhaustion(
    tmp_path,
    monkeypatch,
) -> None:
    root = _fixture(tmp_path)
    monkeypatch.setattr(freezer, "MAX_PLANT_TRAIT_CSV_BYTES", 1)

    with pytest.raises(
        ValueError,
        match="SEMANTIC_RESOURCE_LIMIT_EXCEEDED:plant_traits:bytes=",
    ):
        _freeze(root)
