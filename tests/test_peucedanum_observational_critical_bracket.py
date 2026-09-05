import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_OBSERVATIONAL_CRITICAL_BRACKET_V1.json"


def test_peucedanum_selection_sign_change_is_bracketed_without_promoting_to_c2() -> None:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    gradients = data["final_fruit_set_selection_gradient_on_perfect_flower_number"]
    assert gradients["HA"]["beta"] < 0
    assert gradients["HL"]["beta"] < 0
    assert gradients["HC"]["beta"] > 0
    assert gradients["HD"]["beta"] > 0
    bracket = data["critical_bracket"]
    assert bracket["left_context"] == "HL"
    assert bracket["right_context"] == "HC"
    assert bracket["numeric_ec"] is None
    assert bracket["status"] == "OBSERVATIONAL_SELECTION_SIGN_CHANGE_BRACKET_RECOVERED"
    assert "not causal_C2" in data["claim_ceiling"]


def test_female_gain_shape_switch_matches_same_phenological_bracket() -> None:
    exponents = data = json.loads(RECEIPT.read_text(encoding="utf-8"))["published_female_gain_exponent"]
    assert exponents["HA"]["b"] < 1
    assert exponents["HL"]["b"] < 1
    assert exponents["HC"]["b"] > 1
    assert exponents["KD"]["b"] > 1
    assert exponents["HD"]["b"] > 1
