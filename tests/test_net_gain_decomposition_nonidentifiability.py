import math


def test_many_R_K_pairs_share_the_same_net_gap():
    pairs = [(0.5, 0.3), (1.0, 0.8), (2.2, 2.0)]
    gaps = [R - K for R, K in pairs]
    assert all(math.isclose(gap, 0.2, abs_tol=1e-12) for gap in gaps)


def test_common_additive_offset_preserves_R_minus_K():
    R, K = 0.7, 0.4
    base = R - K
    for delta in (-0.2, 0.0, 0.5, 3.0):
        Rp, Kp = R + delta, K + delta
        if Rp >= 0 and Kp >= 0:
            assert math.isclose(Rp - Kp, base, abs_tol=1e-12)


def test_theory_note_keeps_direct_order_separate_from_decomposition():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    text = (root / "theory" / "NET_GAIN_DECOMPOSITION_NONIDENTIFIABILITY_V1.md").read_text(encoding="utf-8")
    assert "direct worldline order" in text
    assert "R/K decomposition" in text
    assert "kappa_delta" in text
