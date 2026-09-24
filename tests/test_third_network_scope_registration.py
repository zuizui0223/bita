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



def test_scope_registers_safe_release_archive_ingest() -> None:
    text = SCOPE.read_text(encoding="utf-8")
    assert "scripts/ingest_third_network_release_archive.py" in text
    assert (
        "RELEASE_ARCHIVE_INGEST = IMPLEMENTED_PREEXTRACTION_CHECKSUM_ATOMIC_PUBLISH"
        in text
    )
    assert "JOINT_NETWORK_K = 2" in text
    assert "REAL_THIRD_NETWORK_DATA = NOT_COLLECTED" in text
