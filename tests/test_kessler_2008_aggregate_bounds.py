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
    assert summary.probability_delta_min > 0
    assert summary.logit_beta_min > 0
    assert summary.feasible_allocation_count == 1


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

    report = {
        "profiles": [MODULE.asdict(summary)],
        "estimand_boundary": "not source-level uncertainty",
    }
    md = MODULE.render_markdown(report)
    assert "assumption-indexed sensitivity analysis" in md
    assert "not source-level uncertainty" in md
    assert "formal uncertainty identification is not" in md


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
    summary.probability_design_effect_to_cross_1_96_at_min_z = (
        summary.probability_wald_z_min / 1.96
    ) ** 2
    assert summary.probability_design_effect_to_cross_1_96_at_min_z > 1
