from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_kessler_2008_mechanism_bound_handoff.py"
DOC_SUFFIX = "." + "md"
RECEIPT = ROOT / "empirical" / "identification_design" / f"KESSLER_2008_MECHANISM_BOUND_HANDOFF_V1{DOC_SUFFIX}"
SOURCE = ROOT / "empirical" / "identification_design" / "KESSLER_2008_AGGREGATE_BOUNDS_V1.json"


def _load_module():
    assert SCRIPT.exists(), "mechanism-bound handoff builder is missing"
    spec = importlib.util.spec_from_file_location("kessler_mechanism_bound_handoff", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_builder_turns_registered_delta_floor_into_conditional_biotic_balance_floor() -> None:
    module = _load_module()
    report = module.build_report(SOURCE)
    assert report["delta_ad_lower_bound"] == pytest.approx(0.17102387942745256)
    assert report["conditional_restriction"] == "kappa_delta >= 0"
    assert report["conditional_biotic_balance_lower_bound"] == pytest.approx(0.17102387942745256)
    assert report["unconditional_channel_allocation"] == "NOT_POINT_IDENTIFIED"
    assert report["rho_delta"] == "NOT_POINT_IDENTIFIED"
    assert report["iota_delta"] == "NOT_POINT_IDENTIFIED"


def test_receipt_states_numeric_gain_without_promoting_channel_measurement() -> None:
    assert RECEIPT.exists(), "mechanism-bound handoff receipt is missing"
    text = RECEIPT.read_text(encoding="utf-8")
    for token in (
        "KESSLER_CONDITIONAL_BIOTIC_BALANCE_LOWER_BOUND = +0.1710239",
        "ASSUMPTION = kappa_delta >= 0",
        "RHO_DELTA = NOT_POINT_IDENTIFIED",
        "IOTA_DELTA = NOT_POINT_IDENTIFIED",
        "CHANNEL_ALLOCATION = NOT_POINT_IDENTIFIED",
        "conditional partial-identification bound",
        "not a measured channel effect",
    ):
        assert token in text
