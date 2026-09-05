from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SCOPE = ROOT / "docs" / "SUBMISSION_SCOPE.md"


def test_bita_receives_the_exact_sch_shared_axis_output() -> None:
    text = README.read_text(encoding="utf-8")
    for token in (
        "SCH / Chapter 1 — BALANCE",
        "BITA / Chapter 2 — DIFFERENTIATION",
        "z*     = argmin_z L_S(z)",
        "L_S*   = L_S(z*)",
        "recover R from the Chapter 1 conflict load L_S*",
        "Delta_arch = R - K",
        "R = s L_S*",
    ):
        assert token in text, token


def test_chapter_pair_is_defined_by_architecture_not_floral_labels() -> None:
    text = README.read_text(encoding="utf-8")
    assert "not specifically pollination versus defence" in text
    assert "empirical realizations of those two architectural stages, not their general definitions" in text


def test_bita_historical_ceiling_remains_fail_closed_after_symmetry_sync() -> None:
    scope = SCOPE.read_text(encoding="utf-8")
    assert "one-trait compromise" in scope
    assert "!= proof that differentiation evolved" in scope
    assert "structural separation" in scope
    assert "!= functional independence" in scope
    assert "positive A x D interaction" in scope
    assert "!= historical splitting" in scope
