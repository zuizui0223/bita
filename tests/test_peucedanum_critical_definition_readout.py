import json
from pathlib import Path

from scripts.analyze_peucedanum_critical_definition_concordance import analyze


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_OBSERVATIONAL_CRITICAL_BRACKET_V1.json"
READOUT = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_CRITICAL_DEFINITION_CONCORDANCE_V1.json"


def test_static_readout_matches_registered_analyzer() -> None:
    expected = analyze(json.loads(SOURCE.read_text(encoding="utf-8")))
    observed = json.loads(READOUT.read_text(encoding="utf-8"))
    for key in (
        "analysis",
        "system",
        "source_receipt_version",
        "ordered_contexts",
        "definition_semantics",
        "brackets",
        "classification",
        "common_contexts",
        "numeric_critical_context",
        "claim_ceiling",
    ):
        assert observed[key] == expected[key], key


def test_receipt_preserves_verified_published_values() -> None:
    data = json.loads(READOUT.read_text(encoding="utf-8"))
    verified = data["source_verification"]["verified_values"]
    assert verified["final_fruit_beta"] == {
        "HA": -0.035,
        "HL": -0.029,
        "HC": 0.034,
        "KD": 0.008,
        "HD": 0.026,
    }
    assert verified["final_fruit_S"] == {
        "HA": -0.027,
        "HL": -0.051,
        "HC": 0.036,
        "KD": 0.021,
        "HD": 0.024,
    }
    assert verified["female_gain_exponent_b"] == {
        "HA": 0.63,
        "HL": 0.45,
        "HC": 1.15,
        "KD": 1.26,
        "HD": 1.55,
    }
