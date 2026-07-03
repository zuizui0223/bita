import pytest

from trait_architecture.broad_meta_analysis import EFFECT_FIELDS, ORIENTATION
from trait_architecture.part_b_moderator import moderator_contrast


def _effect(cluster: str, value: float, se: float, level: str, *, primary: bool = True) -> dict[str, str]:
    row = {field: "" for field in EFFECT_FIELDS}
    row.update({
        "effect_id": f"{cluster}_{level}",
        "study_id": cluster,
        "study_cluster_id": cluster,
        "route": "A_to_antagonism",
        "trait_role": "A",
        "trait_class": "display_conspicuousness",
        "outcome_class": "florivory_incidence",
        "design_class": "observational",
        "effect_input_type": "reported_effect",
        "effect_metric": "log_odds_ratio",
        "effect_value": str(value),
        "standard_error": str(se),
        "effect_orientation": ORIENTATION,
        "is_primary_effect": "true" if primary else "false",
        "analysis_status": "eligible_for_quantitative_synthesis",
    })
    row["moderator_variable"] = "pollination_generalization"
    row["moderator_level"] = level
    return row


def _contrast(rows, **overrides):
    kwargs = dict(
        route="A_to_antagonism",
        trait_class="display_conspicuousness",
        outcome_class="florivory_incidence",
        effect_metric="log_odds_ratio",
        design_class="observational",
        moderator_variable="pollination_generalization",
        low_level="specialized",
        high_level="generalized",
        predicted_contrast_sign="positive",
    )
    kwargs.update(overrides)
    return moderator_contrast(rows, **kwargs)


def test_moderator_supported_when_contrast_matches_prediction() -> None:
    # d_A predicted more positive where pollination is more generalized.
    rows = [
        _effect("g1", 0.9, 0.15, "generalized"),
        _effect("g2", 1.0, 0.15, "generalized"),
        _effect("g3", 0.8, 0.15, "generalized"),
        _effect("s1", 0.0, 0.15, "specialized"),
        _effect("s2", -0.1, 0.15, "specialized"),
        _effect("s3", 0.1, 0.15, "specialized"),
    ]
    result = _contrast(rows)
    assert result.high.clusters == 3
    assert result.low.clusters == 3
    assert result.contrast > 0
    assert result.contrast_ci_low > 0  # CI excludes zero on the predicted side
    assert result.status == "moderator_supported"


def test_moderator_contradicted_when_contrast_opposes_prediction() -> None:
    # Same predicted-positive hypothesis, but the data move the other way.
    rows = [
        _effect("g1", -0.9, 0.15, "generalized"),
        _effect("g2", -1.0, 0.15, "generalized"),
        _effect("g3", -0.8, 0.15, "generalized"),
        _effect("s1", 0.9, 0.15, "specialized"),
        _effect("s2", 1.0, 0.15, "specialized"),
        _effect("s3", 0.8, 0.15, "specialized"),
    ]
    result = _contrast(rows)
    assert result.contrast < 0
    assert result.status == "moderator_contradicted"


def test_wide_uncertainty_is_uncertain_not_supported() -> None:
    rows = [
        _effect("g1", 0.9, 2.0, "generalized"),
        _effect("g2", 1.0, 2.0, "generalized"),
        _effect("g3", 0.8, 2.0, "generalized"),
        _effect("s1", 0.0, 2.0, "specialized"),
        _effect("s2", -0.1, 2.0, "specialized"),
        _effect("s3", 0.1, 2.0, "specialized"),
    ]
    result = _contrast(rows)
    assert result.contrast_ci_low < 0 < result.contrast_ci_high
    assert result.status == "moderator_uncertain"


def test_single_cluster_level_gives_no_between_study_inference() -> None:
    rows = [
        _effect("g1", 0.9, 0.15, "generalized"),
        _effect("s1", 0.0, 0.15, "specialized"),
    ]
    result = _contrast(rows)
    assert result.contrast is not None  # exploratory contrast still computed
    assert result.status == "single_effect_no_between_study_inference"
    assert result.high.inference == "single_effect_no_between_study_inference"


def test_missing_level_is_insufficient() -> None:
    rows = [
        _effect("g1", 0.9, 0.15, "generalized"),
        _effect("g2", 1.0, 0.15, "generalized"),
    ]
    result = _contrast(rows)
    assert result.low.inference == "no_effects"
    assert result.contrast is None
    assert result.status == "insufficient_levels"


def test_other_moderator_variable_is_ignored() -> None:
    rows = [_effect("g1", 0.9, 0.15, "generalized"), _effect("s1", 0.0, 0.15, "specialized")]
    result = _contrast(rows, moderator_variable="antagonist_guild")
    # No rows carry that moderator variable, so both levels are empty.
    assert result.status == "insufficient_levels"


def test_invalid_prediction_sign_rejected() -> None:
    with pytest.raises(ValueError):
        _contrast([], predicted_contrast_sign="mixed")
