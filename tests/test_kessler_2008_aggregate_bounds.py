from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_kessler_2008_aggregate_bounds.py"
SPEC = importlib.util.spec_from_file_location("kessler_aggregate_bounds", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_known_balanced_allocation_has_positive_probability_and_logit_interaction() -> None:
    summary = MODULE.ProfileSummary(max_denominator_ratio=1.0)
    cells = (
        MODULE.Cell(n=40, y=14),  # A+, D+ = 0.35
        MODULE.Cell(n=40, y=5),   # A+, D- = 0.125
        MODULE.Cell(n=40, y=5),   # A-, D+ = 0.125
        MODULE.Cell(n=40, y=5),   # A-, D- = 0.125
    )
    MODULE._update(summary, cells)
    MODULE._finalize(summary)
    assert summary.probability_delta_min > 0
    assert summary.logit_beta_min > 0
    assert summary.a0_min == 0
    assert summary.a0_max == 0
    assert summary.a1_min > 0
    assert summary.a1_uniformly_positive
    assert summary.level2_strict_identified
    assert not summary.level3_strict_identified
    assert summary.feasible_allocation_count == 1


def test_a0_crossing_zero_blocks_strict_release_while_a1_stays_positive() -> None:
    summary = MODULE.ProfileSummary(max_denominator_ratio=1.0)
    MODULE._update(
        summary,
        (
            MODULE.Cell(n=100, y=35),  # p11 = .35
            MODULE.Cell(n=100, y=14),  # p10 = .14
            MODULE.Cell(n=100, y=13),  # p01 = .13
            MODULE.Cell(n=100, y=12),  # p00 = .12 -> A0 = +.02
        ),
    )
    MODULE._update(
        summary,
        (
            MODULE.Cell(n=100, y=35),
            MODULE.Cell(n=100, y=12),
            MODULE.Cell(n=100, y=13),
            MODULE.Cell(n=100, y=14),  # A0 = -.02
        ),
    )
    MODULE._finalize(summary)

    assert summary.a0_min < 0 < summary.a0_max
    assert summary.a1_min > 0
    assert summary.a1_uniformly_positive
    assert not summary.level2_strict_identified
    assert not summary.level3_strict_identified
    assert summary.a0_upper_tolerance_to_zero == summary.a0_max


def test_small_enumeration_preserves_sign_but_not_source_uncertainty_claim() -> None:
    summary = MODULE.enumerate_profile(
        total_n=160,
        total_y=29,
        ev_range=(0.34, 0.36),
        low_range=(0.12, 0.13),
        max_denominator_ratio=1.1,
    )
    assert summary.feasible_allocation_count > 0
    assert summary.probability_delta_min > 0
    assert summary.logit_beta_min > 0
    assert summary.a1_min > 0

    report = {
        "profiles": [MODULE.asdict(summary)],
        "estimand_boundary": "not source-level uncertainty",
    }
    md = MODULE.render_markdown(report)
    assert "assumption-indexed sensitivity analysis" in md
    assert "Stage-1 partial-identification readout" in md
    assert "undefended attraction response is not identified" in md
    assert "not source-level uncertainty" in md
    assert "formal source/design uncertainty identification is not" in md


def test_design_effect_threshold_is_variance_inflation_not_a_claim_of_clustering() -> None:
    summary = MODULE.ProfileSummary(max_denominator_ratio=1.0)
    MODULE._update(
        summary,
        (
            MODULE.Cell(n=100, y=35),
            MODULE.Cell(n=100, y=13),
            MODULE.Cell(n=100, y=13),
            MODULE.Cell(n=100, y=13),
        ),
    )
    MODULE._finalize(summary)
    assert summary.probability_design_effect_to_cross_1_96_at_min_z > 1
