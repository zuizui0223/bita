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
    / "aubert2026_participation_route_decomposition_first_open.json"
)
RECEIPT = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "results"
    / "AUBERT2026_PARTICIPATION_FIRST_OPEN_RECEIPT_V1.json"
)
FREEZE = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "PARTICIPATION_ROUTE_DENOMINATOR_FREEZE_V1.json"
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def test_first_open_result_matches_original_artifact_sha() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert _sha256(RESULT) == receipt["result_sha256"]
    assert receipt["result_sha256"] == (
        "5d0e48f208077aedafd251a576ca2a927adef9ac4516102570988df0944a344f"
    )
    assert receipt["status"] == "FIRST_REAL_EFFECT_OPENED_RETAIN_REGARDLESS_OF_SIGN"


def test_first_open_participation_decision_is_frozen() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    decision = result["decision"]

    assert result["status"] == "FIT"
    assert result["support_gate"]["passes"] is True
    assert decision["classification"] == "PARTICIPATION_INCREASE_PLUS_ROUTING"
    assert decision["rate_ratio"] == 1.7717025981047398
    assert decision["ci95_rate_ratio"] == [
        1.1050441908815296,
        2.8405471220359604,
    ]
    assert decision["ci90_rate_ratio"] == [
        1.192183703242776,
        2.632924848404738,
    ]
    assert decision["equivalence_supported"] is False
    assert decision["participation_increase_supported"] is True
    assert decision["material_enhancement_supported"] is False

    assert result["sensitivities"]["strict_feeding_rate_ratio"] == 1.7149095800301755
    assert result["sensitivities"]["broad_feeding_rate_ratio"] == 1.7716648514423483


def test_freeze_contract_records_single_effect_opening() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert freeze["participation_effect_opened"] is True
    first = freeze["first_open"]
    assert first["workflow_run_id"] == 36741117582
    assert first["artifact_id"] == 11110059325
    assert first["classification"] == "PARTICIPATION_INCREASE_PLUS_ROUTING"
    assert first["result_sha256"] == _sha256(RESULT)
