from __future__ import annotations

import math

import pytest

from trait_architecture.broad_meta_analysis import ORIENTATION
from trait_architecture.context_dependence import (
    chi_square_upper_p,
    collect_moderated_effects,
    egger_small_study_test,
    leave_one_cluster_out,
    meta_regression,
    read_moderator_coding,
    read_moderator_registry,
    run_context_dependence,
    student_t_quantile_975,
    student_t_two_sided_p,
    subgroup_analysis,
)


IOTA_STRATUM = {
    "stratum_id": "BP_chemical_pollinator_use_lrr_manipulation",
    "route": "B_to_pollination",
    "trait_class": "chemical_barrier",
    "outcome_class": "pollinator_preference_or_foraging",
    "effect_metric": "log_response_ratio",
    "design_class": "manipulation",
    "min_clusters_exploratory": "3",
    "min_clusters_stability": "5",
    "expected_effect_direction": "negative",
    "part_i_parameter": "c_D",
    "interpretation": "test",
}


def effect_row(effect_id: str, cluster: str, value: float, se: float, **overrides: str) -> dict[str, str]:
    row = {
        "effect_id": effect_id,
        "study_id": f"study-{cluster}",
        "study_cluster_id": cluster,
        "doi": "10.1/example",
        "taxon": "Example plant",
        "route": "B_to_pollination",
        "trait_role": "B",
        "trait_class": "chemical_barrier",
        "outcome_class": "pollinator_preference_or_foraging",
        "design_class": "manipulation",
        "effect_input_type": "reported_effect",
        "effect_metric": "log_response_ratio",
        "effect_value": f"{value}",
        "standard_error": f"{se}",
        "n_treatment": "", "n_control": "", "mean_treatment": "", "sd_treatment": "",
        "mean_control": "", "sd_control": "", "event_treatment": "", "non_event_treatment": "",
        "event_control": "", "non_event_control": "", "correlation_r": "", "n_total": "",
        "effect_orientation": ORIENTATION,
        "is_primary_effect": "false",
        "analysis_status": "eligible_for_quantitative_synthesis",
        "source_basis": "public_fulltext",
        "source_locator": "Table 1",
        "extraction_note": "",
    }
    row.update(overrides)
    return row


def coding_row(effect_id: str, value: str, moderator_name: str = "dose_realism") -> dict[str, str]:
    return {
        "effect_id": effect_id,
        "moderator_name": moderator_name,
        "moderator_value": value,
        "coding_basis": "reported concentration compared with reported natural nectar range",
        "coder_id": "tester",
        "coding_date": "2026-08-10",
        "coding_status": "coded",
    }


def registry_row(**overrides: str) -> dict[str, str]:
    row = {
        "analysis_id": "iota_dose_realism",
        "stratum_id": "BP_chemical_pollinator_use_lrr_manipulation",
        "moderator_name": "dose_realism",
        "moderator_type": "categorical",
        "reference_level": "within_natural_range",
        "min_levels": "2",
        "min_clusters_per_level": "2",
        "min_clusters_total": "4",
        "declared_hypothesis": "test hypothesis",
        "licensed_statement": "test licensed statement",
        "interpretation": "test",
    }
    row.update(overrides)
    return row


# ---------------------------------------------------------------------------
# numerical primitives
# ---------------------------------------------------------------------------


def test_student_t_and_chi_square_match_published_critical_values() -> None:
    assert math.isclose(student_t_two_sided_p(2.228138852, 10), 0.05, rel_tol=1e-6)
    assert math.isclose(student_t_two_sided_p(1.959963985, 100000), 0.05, rel_tol=1e-3)
    assert math.isclose(student_t_quantile_975(10), 2.228138852, rel_tol=1e-6)
    assert math.isclose(chi_square_upper_p(3.841458821, 1), 0.05, rel_tol=1e-6)
    assert math.isclose(chi_square_upper_p(5.991464547, 2), 0.05, rel_tol=1e-6)


# ---------------------------------------------------------------------------
# collection and independence rules
# ---------------------------------------------------------------------------


def test_collection_keeps_within_cluster_moderator_contrasts() -> None:
    effects = [
        effect_row("e1", "cluster-1", -0.5, 0.1),
        effect_row("e2", "cluster-1", 0.1, 0.1),
    ]
    coding = [coding_row("e1", "above_natural_range"), coding_row("e2", "within_natural_range")]

    collected = collect_moderated_effects(effects, coding, IOTA_STRATUM, "dose_realism", "categorical")

    assert len(collected) == 2
    assert {effect.moderator_value for effect in collected} == {"above_natural_range", "within_natural_range"}


def test_collection_rejects_two_effects_for_one_cluster_at_one_level() -> None:
    effects = [effect_row("e1", "cluster-1", -0.5, 0.1), effect_row("e2", "cluster-1", -0.4, 0.1)]
    coding = [coding_row("e1", "above_natural_range"), coding_row("e2", "above_natural_range")]

    with pytest.raises(ValueError, match="more than one effect for one study cluster"):
        collect_moderated_effects(effects, coding, IOTA_STRATUM, "dose_realism", "categorical")


def test_collection_ignores_uncoded_and_out_of_stratum_effects() -> None:
    effects = [
        effect_row("e1", "cluster-1", -0.5, 0.1),
        effect_row("e2", "cluster-2", -0.5, 0.1),
        effect_row("e3", "cluster-3", -0.5, 0.1, outcome_class="visitation_rate"),
    ]
    coding = [
        coding_row("e1", "above_natural_range"),
        {**coding_row("e2", ""), "coding_status": "needs_coding"},
        coding_row("e3", "above_natural_range"),
    ]

    collected = collect_moderated_effects(effects, coding, IOTA_STRATUM, "dose_realism", "categorical")

    assert [effect.estimate.effect_id for effect in collected] == ["e1"]


# ---------------------------------------------------------------------------
# subgroup analysis
# ---------------------------------------------------------------------------


def _reversal_effects() -> list:
    # Both levels are individually well separated from zero, which is what the
    # direction-reversal verdict requires.
    effects = [
        effect_row(f"high-{index}", f"cluster-h{index}", -0.80, 0.10) for index in range(1, 4)
    ] + [
        effect_row(f"natural-{index}", f"cluster-n{index}", 0.25, 0.05) for index in range(1, 4)
    ]
    coding = [coding_row(f"high-{index}", "above_natural_range") for index in range(1, 4)]
    coding += [coding_row(f"natural-{index}", "within_natural_range") for index in range(1, 4)]
    return collect_moderated_effects(effects, coding, IOTA_STRATUM, "dose_realism", "categorical")


def test_subgroup_analysis_pools_levels_but_issues_no_verdict() -> None:
    levels, test = subgroup_analysis(_reversal_effects(), registry_row())

    assert test["analysis_status"] == "subgroup_random_effects"
    assert test["levels_analysed"] == 2
    assert float(test["Q_between_fixed_effect_p_value"]) < 0.001
    # The fixed-effect Q_between rejects far too often under heterogeneity, so
    # it is reported descriptively and never converted into a verdict here.
    assert test["inferential_role"] == "descriptive_only_not_used_for_inference"
    assert test["context_dependence_verdict"] == "see_meta_regression_verdict"

    by_level = {row["moderator_level"]: row for row in levels}
    assert by_level["above_natural_range"]["pooled_direction"] == "negative"
    assert by_level["within_natural_range"]["pooled_direction"] == "positive"
    assert math.isclose(float(by_level["above_natural_range"]["pooled_effect"]), -0.80, abs_tol=1e-9)


def test_verdict_is_direction_reversal_only_when_both_levels_exclude_zero() -> None:
    effects = _reversal_effects()
    levels, _ = subgroup_analysis(effects, registry_row())

    _, model = meta_regression(effects, registry_row(), levels)

    assert model["context_dependence_verdict"] == "context_dependent_direction_reversal"


def test_verdict_falls_back_to_magnitude_only_when_a_level_straddles_zero() -> None:
    # The reference level is centred on zero with wide intervals, so its sign is
    # not established even though the level contrast itself is large.
    effects_rows = [
        effect_row(f"high-{index}", f"cluster-h{index}", -0.80, 0.05) for index in range(1, 4)
    ] + [
        effect_row(f"natural-{index}", f"cluster-n{index}", 0.02, 0.30) for index in range(1, 4)
    ]
    coding = [coding_row(f"high-{index}", "above_natural_range") for index in range(1, 4)]
    coding += [coding_row(f"natural-{index}", "within_natural_range") for index in range(1, 4)]
    effects = collect_moderated_effects(effects_rows, coding, IOTA_STRATUM, "dose_realism", "categorical")
    levels, _ = subgroup_analysis(effects, registry_row())

    _, model = meta_regression(effects, registry_row(), levels)

    assert model["context_dependence_verdict"] == "context_dependent_magnitude_only"


def test_subgroup_analysis_withholds_verdict_below_declared_capacity() -> None:
    effects_rows = [
        effect_row("high-1", "cluster-h1", -0.8, 0.1),
        effect_row("natural-1", "cluster-n1", 0.1, 0.1),
    ]
    coding = [coding_row("high-1", "above_natural_range"), coding_row("natural-1", "within_natural_range")]
    effects = collect_moderated_effects(effects_rows, coding, IOTA_STRATUM, "dose_realism", "categorical")

    levels, test = subgroup_analysis(effects, registry_row())

    assert test["analysis_status"] == "insufficient_moderator_capacity"
    assert test["context_dependence_verdict"] == "not_evaluated"
    assert all(row["level_status"] == "insufficient_clusters_at_level" for row in levels)


# ---------------------------------------------------------------------------
# meta-regression
# ---------------------------------------------------------------------------


def test_categorical_meta_regression_recovers_the_designed_level_contrast() -> None:
    terms, model = meta_regression(_reversal_effects(), registry_row())

    assert model["analysis_status"] == "random_effects_meta_regression"
    assert model["independent_clusters"] == 6
    by_term = {row["term"]: row for row in terms}
    assert math.isclose(float(by_term["intercept"]["coefficient"]), 0.25, abs_tol=1e-9)
    contrast = by_term["level[above_natural_range]-vs-[within_natural_range]"]
    assert math.isclose(float(contrast["coefficient"]), -1.05, abs_tol=1e-9)
    assert float(model["Q_moderator_p_value"]) < 0.001
    assert model["context_dependence_verdict"] == "moderator_changes_route_effect"
    assert contrast["standard_error_basis"] == "model_based_random_effects"


def test_continuous_meta_regression_recovers_an_exact_dose_slope() -> None:
    doses = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    effects_rows = [
        effect_row(f"e{index}", f"cluster-{index}", 0.30 - 0.20 * dose, 0.05)
        for index, dose in enumerate(doses, start=1)
    ]
    coding = [
        coding_row(f"e{index}", f"{dose}", moderator_name="log_dose_multiple_of_natural_maximum")
        for index, dose in enumerate(doses, start=1)
    ]
    effects = collect_moderated_effects(
        effects_rows, coding, IOTA_STRATUM, "log_dose_multiple_of_natural_maximum", "continuous"
    )

    terms, model = meta_regression(effects, registry_row(
        analysis_id="iota_dose_slope",
        moderator_name="log_dose_multiple_of_natural_maximum",
        moderator_type="continuous",
        reference_level="",
    ))

    by_term = {row["term"]: row for row in terms}
    assert math.isclose(float(by_term["intercept"]["coefficient"]), 0.30, abs_tol=1e-9)
    assert math.isclose(float(by_term["moderator_slope"]["coefficient"]), -0.20, abs_tol=1e-9)
    assert math.isclose(float(model["tau_squared_residual"]), 0.0, abs_tol=1e-12)
    assert float(model["heterogeneity_explained_fraction"]) > 0.99


def test_meta_regression_switches_to_cluster_robust_errors_under_within_study_contrasts() -> None:
    offsets = [-0.06, -0.02, 0.02, 0.06]
    effects_rows = []
    coding = []
    for index, offset in enumerate(offsets, start=1):
        effects_rows.append(effect_row(f"high-{index}", f"cluster-{index}", -0.70 + offset, 0.10))
        effects_rows.append(effect_row(f"nat-{index}", f"cluster-{index}", 0.00 + offset, 0.10))
        coding.append(coding_row(f"high-{index}", "above_natural_range"))
        coding.append(coding_row(f"nat-{index}", "within_natural_range"))
    effects = collect_moderated_effects(effects_rows, coding, IOTA_STRATUM, "dose_realism", "categorical")

    terms, model = meta_regression(effects, registry_row())

    assert model["effect_count"] == 8
    assert model["independent_clusters"] == 4
    contrast = next(row for row in terms if row["term"].startswith("level["))
    assert contrast["standard_error_basis"] == "cluster_robust_CR1"
    assert float(contrast["primary_standard_error"]) == float(contrast["cluster_robust_standard_error"])
    assert math.isclose(float(contrast["degrees_of_freedom"]), 2.0, abs_tol=1e-12)
    # The within-cluster contrast is identical in every cluster, so the robust
    # standard error of that contrast is far smaller than the model-based one.
    assert float(contrast["cluster_robust_standard_error"]) < float(contrast["model_standard_error"])


def test_meta_regression_reports_a_collapsed_cluster_robust_omnibus_as_not_estimable() -> None:
    effects_rows = []
    coding = []
    for index in range(1, 5):
        effects_rows.append(effect_row(f"high-{index}", f"cluster-{index}", -0.70, 0.10))
        effects_rows.append(effect_row(f"nat-{index}", f"cluster-{index}", 0.00, 0.10))
        coding.append(coding_row(f"high-{index}", "above_natural_range"))
        coding.append(coding_row(f"nat-{index}", "within_natural_range"))
    effects = collect_moderated_effects(effects_rows, coding, IOTA_STRATUM, "dose_realism", "categorical")

    terms, model = meta_regression(effects, registry_row())

    contrast = next(row for row in terms if row["term"].startswith("level["))
    assert math.isclose(float(contrast["coefficient"]), -0.70, abs_tol=1e-9)
    assert model["Q_moderator_p_value"] == ""
    assert model["context_dependence_verdict"] == "omnibus_moderator_test_not_estimable"


def test_meta_regression_withholds_below_declared_cluster_minimum() -> None:
    effects_rows = [
        effect_row("high-1", "cluster-h1", -0.8, 0.1),
        effect_row("natural-1", "cluster-n1", 0.1, 0.1),
    ]
    coding = [coding_row("high-1", "above_natural_range"), coding_row("natural-1", "within_natural_range")]
    effects = collect_moderated_effects(effects_rows, coding, IOTA_STRATUM, "dose_realism", "categorical")

    terms, model = meta_regression(effects, registry_row())

    assert terms == []
    assert model["analysis_status"] == "insufficient_moderator_capacity"


# ---------------------------------------------------------------------------
# robustness diagnostics
# ---------------------------------------------------------------------------


def test_leave_one_cluster_out_flags_a_direction_that_depends_on_one_cluster() -> None:
    effects_rows = [
        effect_row("e1", "cluster-1", -0.05, 0.10),
        effect_row("e2", "cluster-2", -0.05, 0.10),
        effect_row("e3", "cluster-3", 0.60, 0.05),
    ]
    coding = [coding_row(f"e{index}", "within_natural_range") for index in range(1, 4)]
    effects = collect_moderated_effects(effects_rows, coding, IOTA_STRATUM, "dose_realism", "categorical")

    rows = leave_one_cluster_out(effects, "iota_dose_realism", IOTA_STRATUM["stratum_id"])

    assert len(rows) == 3
    assert any(row["direction_matches_full_set"] == "false" for row in rows)


def test_egger_test_is_withheld_below_the_declared_cluster_minimum() -> None:
    effects_rows = [effect_row(f"e{i}", f"cluster-{i}", -0.3, 0.1) for i in range(1, 5)]
    coding = [coding_row(f"e{i}", "within_natural_range") for i in range(1, 5)]
    effects = collect_moderated_effects(effects_rows, coding, IOTA_STRATUM, "dose_realism", "categorical")

    result = egger_small_study_test(effects, "iota_dose_realism", IOTA_STRATUM["stratum_id"])

    assert result["analysis_status"] == "withheld_below_declared_cluster_minimum"
    assert result["asymmetry_verdict"] == "not_evaluated"


def test_egger_test_detects_designed_funnel_asymmetry() -> None:
    effects_rows = []
    coding = []
    for index in range(1, 13):
        se = 0.02 * index
        effects_rows.append(effect_row(f"e{index}", f"cluster-{index}", -0.20 - 2.0 * se, se))
        coding.append(coding_row(f"e{index}", "within_natural_range"))
    effects = collect_moderated_effects(effects_rows, coding, IOTA_STRATUM, "dose_realism", "categorical")

    result = egger_small_study_test(effects, "iota_dose_realism", IOTA_STRATUM["stratum_id"])

    assert result["analysis_status"] == "weighted_egger_regression"
    assert math.isclose(float(result["intercept"]), -0.20, abs_tol=1e-6)


# ---------------------------------------------------------------------------
# declared-input validation and end-to-end wiring
# ---------------------------------------------------------------------------


def test_registry_and_coding_readers_reject_undeclared_or_unsupported_rows(tmp_path) -> None:
    registry_path = tmp_path / "registry.csv"
    registry_path.write_text(
        "analysis_id,stratum_id,moderator_name,moderator_type,reference_level,min_levels,"
        "min_clusters_per_level,min_clusters_total,declared_hypothesis,licensed_statement,interpretation\n"
        "a,s,m,ordinal,ref,2,2,4,h,l,i\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="invalid moderator_type"):
        read_moderator_registry(registry_path)

    coding_path = tmp_path / "coding.csv"
    coding_path.write_text(
        "effect_id,moderator_name,moderator_value,coding_basis,coder_id,coding_date,coding_status\n"
        "e1,m,high,,tester,2026-08-10,coded\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="needs a coding_basis"):
        read_moderator_coding(coding_path)


def test_run_context_dependence_executes_every_declared_analysis() -> None:
    effects_rows = [
        effect_row(f"high-{index}", f"cluster-h{index}", -0.80, 0.10) for index in range(1, 4)
    ] + [
        effect_row(f"natural-{index}", f"cluster-n{index}", 0.25, 0.05) for index in range(1, 4)
    ]
    coding = [coding_row(f"high-{index}", "above_natural_range") for index in range(1, 4)]
    coding += [coding_row(f"natural-{index}", "within_natural_range") for index in range(1, 4)]

    tables = run_context_dependence(effects_rows, coding, [IOTA_STRATUM], [registry_row()])

    assert tables["subgroup_tests"][0]["context_dependence_verdict"] == "see_meta_regression_verdict"
    assert tables["meta_regression_models"][0]["context_dependence_verdict"] == "context_dependent_direction_reversal"
    assert tables["meta_regression_models"][0]["analysis_status"] == "random_effects_meta_regression"
    assert len(tables["influence"]) == 6
    assert tables["small_study"][0]["analysis_status"] == "withheld_below_declared_cluster_minimum"


def test_run_context_dependence_rejects_an_undeclared_stratum() -> None:
    with pytest.raises(ValueError, match="names an undeclared stratum"):
        run_context_dependence([], [], [IOTA_STRATUM], [registry_row(stratum_id="missing")])
