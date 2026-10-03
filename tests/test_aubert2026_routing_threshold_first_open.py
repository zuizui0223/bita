from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "results"
    / "aubert2026_routing_threshold_first_open.json"
)
RECEIPT = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "results"
    / "AUBERT2026_ROUTING_THRESHOLD_FIRST_OPEN_RECEIPT_V1.json"
)
FREEZE = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "AUBERT_ROUTING_THRESHOLD_FREEZE_V1.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_first_open_threshold_result_is_frozen_exactly() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    decision = result["threshold_classification"]
    fit = result["primary_sigmoid"]
    boot = result["bootstrap"]
    turnover = result["upper_turnover"]

    assert result["status"] == "FIT"
    assert result["n_plant_species"] == 259
    assert decision == "THRESHOLD_AT_SUPPORT_BOUNDARY"
    assert fit["xstar"] == 0.9197423428245373
    assert fit["at_search_boundary"] is True
    assert fit["amplitude"] == 0.4130984092633582
    assert boot["ci90_xstar"] == [
        0.1176853690900638,
        0.9197423428245373,
    ]
    assert boot["finite_replicates"] == 999
    assert turnover["classification"] == "CURVATURE_WITHOUT_INTERIOR_TURNOVER"
    assert turnover["curvature_permutation_p"] == 0.0049
    assert turnover["quadratic"]["quadratic"] == 0.042703579536178454
    assert turnover["derivative_at_q90"] == 0.1662165245277788


def test_first_open_receipt_matches_result_and_freeze_lifecycle() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))

    assert receipt["status"] == "FIRST_REAL_THRESHOLD_EFFECT_OPENED_RETAIN_REGARDLESS_OF_SIGN"
    assert receipt["result_sha256"] == _sha256(RESULT)
    assert receipt["result_sha256"] == "33a1ee2248f69aaa308a8424f4acac0f59148b07e4607075614d8171a900b931"
    assert receipt["first_open_workflow_run"] == 37090321341
    assert receipt["first_open_artifact_id"] == 11262262598

    assert freeze["status"] == "FIRST_THRESHOLD_EFFECT_OPENED_RETAIN_REGARDLESS_OF_SIGN"
    assert freeze["threshold_effect_opened"] is True
    assert freeze["first_open"]["threshold_classification"] == "THRESHOLD_AT_SUPPORT_BOUNDARY"
    assert freeze["first_open"]["result_sha256"] == receipt["result_sha256"]
