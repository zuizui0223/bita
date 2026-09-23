from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "docs" / "SUBMISSION_SCOPE.md"


def test_third_network_scope_has_no_literal_newline_escapes() -> None:
    text = SCOPE.read_text(encoding="utf-8")
    assert "\\n-" not in text
    assert "\\n\\n" not in text


def test_scope_registers_release_rehearsal_without_promoting_real_k3() -> None:
    text = SCOPE.read_text(encoding="utf-8")
    assert "scripts/run_third_network_release_rehearsal.py" in text
    assert "THIRD_NETWORK_RELEASE_REHEARSAL_V1.md" in text
    assert "RELEASE_REHEARSAL = IMPLEMENTED_BUNDLE_VERIFY_CLAIM_PLAN_MATRIX" in text
    assert "JOINT_NETWORK_K = 2" in text
    assert "REAL_THIRD_NETWORK_DATA = NOT_COLLECTED" in text



def test_scope_registers_canonical_existing_network_fingerprint_lock() -> None:
    text = SCOPE.read_text(encoding="utf-8")
    assert "EXISTING_K3_INPUT_FINGERPRINTS_V1.json" in text
    assert "trait_architecture/existing_k3_inputs.py" in text
    assert (
        "EXISTING_NETWORK_K3_INPUTS = "
        "BUNDLED_EXACT_ROWS_REVERIFIED_AND_CANONICAL_FINGERPRINT_LOCKED"
    ) in text
