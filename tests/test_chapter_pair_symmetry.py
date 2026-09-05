from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SCOPE = ROOT / "docs" / "SUBMISSION_SCOPE.md"
HANDOFF = ROOT / "docs" / "SCH_BITA_EMPIRICAL_HANDOFF_V1.md"


def test_theory_level_chapter_interface_uses_pure_function_optima_only_as_theory() -> None:
    text = README.read_text(encoding="utf-8")
    for token in (
        "SCH / Chapter 1 — BALANCE",
        "BITA / Chapter 2 — DIFFERENTIATION",
        "z_F1* = argmax F1(z)",
        "z_F2* = argmax F2(z)",
        "L_compromise,theory*",
        "R = s L_S*",
        "Delta_arch = R - K",
        "theory-level architecture comparison",
    ):
        assert token in text, token


def test_default_empirical_handoff_is_state_specific_not_pure_function_relabeling() -> None:
    text = HANDOFF.read_text(encoding="utf-8")
    for token in (
        "z_P* = argmax W10(z)",
        "z_G* = argmax W01(z)",
        "z_C* = argmax W11(z)",
        "z_P* != automatically z_F1*",
        "z_G* != automatically z_F2*",
        "|x*(y1) - z_P*| < |x*(y0) - z_P*|",
        "state-specific dimensional release",
    ):
        assert token in text, token


def test_pure_function_release_is_an_optional_stricter_lane() -> None:
    text = HANDOFF.read_text(encoding="utf-8")
    assert "Only then may BITA add the stricter question" in text
    assert "|x*(y1) - z_F1*| < |x*(y0) - z_F1*|" in text
    assert "state-specific and pure-function release analyses must be reported separately" in text


def test_local_AxD_relief_is_not_silently_equated_with_dimensional_release() -> None:
    text = README.read_text(encoding="utf-8")
    assert "positive A x D interaction" in text
    assert "!= dimensional release toward z_P*" in text
    assert "Level 1  positive interaction relief" in text
    assert "These local two-level outcomes are not the same as the multi-level SCH-to-BITA dimensional-release test" in text


def test_chapter_pair_is_defined_by_architecture_not_floral_labels() -> None:
    text = README.read_text(encoding="utf-8")
    assert "not specifically pollination versus defence" in text
    assert "empirical realizations" not in text or "not their general definitions" in text


def test_bita_historical_ceiling_remains_fail_closed_after_symmetry_sync() -> None:
    scope = SCOPE.read_text(encoding="utf-8")
    assert "one-trait compromise" in scope
    assert "!= proof that differentiation evolved" in scope
    assert "structural separation" in scope
    assert "!= functional independence" in scope
    assert "positive A x D interaction" in scope
    assert "!= historical splitting" in scope
