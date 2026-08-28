from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READOUT = ROOT / "empirical" / "identification_design" / "KESSLER_2008_MALE_SCALE_SENSITIVITY_V1.md"


def test_reported_male_ratios_change_interaction_sign_across_scales() -> None:
    ev = 1.0
    chal = 1.0 / 1.9
    pmt = 1.0 / 2.2
    cp = 1.0 / 4.7

    additive = ev - pmt - chal + cp
    log_interaction = math.log(ev) - math.log(pmt) - math.log(chal) + math.log(cp)
    interaction_ratio = (ev * cp) / (pmt * chal)

    assert abs(additive - 0.2319047134) < 1e-9
    assert additive > 0
    assert abs(log_interaction - (-0.1172512622)) < 1e-9
    assert log_interaction < 0
    assert abs(interaction_ratio - 0.8893617021) < 1e-9
    assert interaction_ratio < 1


def test_scale_sensitivity_readout_preserves_estimand_boundary() -> None:
    text = READOUT.read_text(encoding="utf-8")
    assert "outcome-scale dependent" in text
    assert "male relative-count additive scale: positive interaction sign" in text
    assert "male multiplicative/log scale:       slightly negative interaction sign" in text
    assert "must not be pooled with the female capsule analysis" in text
    assert "name the reproductive endpoint and scale" in text
