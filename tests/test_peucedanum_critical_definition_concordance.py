import json
from pathlib import Path

from scripts.analyze_peucedanum_critical_definition_concordance import analyze


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_OBSERVATIONAL_CRITICAL_BRACKET_V1.json"


def test_three_published_definitions_recover_same_hl_hc_bracket() -> None:
    result = analyze(json.loads(RECEIPT.read_text(encoding="utf-8")))
    assert result["classification"] == "SAME_COARSE_CRITICAL_BRACKET"
    assert result["common_contexts"] == ["HL", "HC"]
    assert len(result["brackets"]) == 3
    assert all(
        bracket["left_context"] == "HL" and bracket["right_context"] == "HC"
        for bracket in result["brackets"]
    )


def test_concordant_coarse_bracket_is_not_promoted_to_numeric_or_causal_c2() -> None:
    result = analyze(json.loads(RECEIPT.read_text(encoding="utf-8")))
    assert result["numeric_critical_context"] is None
    assert "not_same_numeric_critical_point" in result["claim_ceiling"]
    assert "not_causal_C2" in result["claim_ceiling"]
    assert "not_calibrated_functional_weight" in result["claim_ceiling"]
