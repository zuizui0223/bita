import math

import pytest

from trait_architecture.deposited_effect_ingest import (
    GroupContrast,
    aggregate_within_cluster,
    build_cluster_effects,
    log_response_ratio,
    read_group_contrasts,
    verify_deposited_effect,
)


def contrast(**overrides) -> GroupContrast:
    base = dict(
        source_row_id="1",
        study_cluster_id="StudyA",
        n_treatment=13.0, mean_treatment=519.89, sd_treatment=200.1,
        n_control=10.0, mean_control=590.81, sd_control=352.22,
        deposited_effect=None, deposited_variance=None,
    )
    base.update(overrides)
    return GroupContrast(**base)


def test_log_response_ratio_matches_closed_form() -> None:
    value, variance = log_response_ratio(contrast())
    assert value == pytest.approx(math.log(519.89 / 590.81))
    assert variance == pytest.approx(
        200.1 ** 2 / (13 * 519.89 ** 2) + 352.22 ** 2 / (10 * 590.81 ** 2)
    )


def test_non_positive_mean_is_not_recomputable() -> None:
    audit = verify_deposited_effect(contrast(mean_control=0.0, deposited_effect=0.1))
    assert audit["agreement_verdict"] == "not_recomputable"


def test_reproduced_deposited_effect_is_recognised() -> None:
    value, variance = log_response_ratio(contrast())
    audit = verify_deposited_effect(contrast(deposited_effect=value, deposited_variance=variance))
    assert audit["agreement_verdict"] == "reproduced"


def test_sign_flip_is_detected_rather_than_absorbed() -> None:
    value, variance = log_response_ratio(contrast())
    audit = verify_deposited_effect(contrast(deposited_effect=-value, deposited_variance=variance))
    assert audit["agreement_verdict"] == "sign_disagrees"
    assert audit["effect_agreement"] == "sign_flipped"


def test_variance_disagreement_does_not_discard_a_matching_point_estimate() -> None:
    value, variance = log_response_ratio(contrast())
    audit = verify_deposited_effect(
        contrast(deposited_effect=value, deposited_variance=variance * 2)
    )
    assert audit["agreement_verdict"] == "variance_disagrees"


def test_quarantined_rows_are_excluded_by_default_and_included_on_request() -> None:
    value, variance = log_response_ratio(contrast())
    rows = [
        contrast(source_row_id="1", deposited_effect=value, deposited_variance=variance),
        contrast(source_row_id="2", deposited_effect=-value, deposited_variance=variance),
    ]
    effects, audits = build_cluster_effects(rows, correlation=1.0)
    assert len(effects) == 1
    assert effects[0]["source_row_count"] == 1
    assert any(str(a["handling"]).startswith("excluded:") for a in audits)

    effects_all, _ = build_cluster_effects(rows, correlation=1.0, include_quarantined=True)
    assert effects_all[0]["source_row_count"] == 2
    # Adopting the deposited sign for row 2 makes the two effects cancel.
    assert effects_all[0]["effect_value"] == pytest.approx(0.0, abs=1e-12)


def test_aggregation_variance_is_monotone_in_the_declared_correlation() -> None:
    values = [0.2, -0.4, 0.1]
    variances = [0.04, 0.09, 0.01]
    previous = -1.0
    for rho in (0.0, 0.25, 0.5, 0.75, 1.0):
        mean, variance = aggregate_within_cluster(values, variances, rho)
        assert mean == pytest.approx(sum(values) / 3)
        assert variance > previous
        previous = variance


def test_independent_and_perfectly_correlated_aggregation_have_closed_forms() -> None:
    variances = [0.04, 0.09, 0.01]
    _, independent = aggregate_within_cluster([0.0] * 3, variances, 0.0)
    assert independent == pytest.approx(sum(variances) / 9)

    _, perfect = aggregate_within_cluster([0.0] * 3, variances, 1.0)
    assert perfect == pytest.approx((sum(math.sqrt(v) for v in variances) / 3) ** 2)


def test_single_effect_cluster_is_unchanged_by_the_correlation() -> None:
    for rho in (0.0, 0.5, 1.0):
        mean, variance = aggregate_within_cluster([0.3], [0.05], rho)
        assert (mean, variance) == pytest.approx((0.3, 0.05))


def test_aggregation_rejects_an_out_of_range_correlation() -> None:
    with pytest.raises(ValueError):
        aggregate_within_cluster([0.1, 0.2], [0.01, 0.02], 1.5)


def test_read_group_contrasts_requires_identifiers() -> None:
    rows = [{
        "sample": "", "study": "S", "n_larcenist": "5", "mean_larcenist": "10",
        "sd_larcenist": "1", "n_control": "5", "mean_control": "12", "sd_control": "1",
    }]
    with pytest.raises(ValueError):
        read_group_contrasts(
            rows, row_id_field="sample", cluster_field="study",
            treatment_prefix="larcenist", control_prefix="control",
        )
