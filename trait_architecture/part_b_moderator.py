"""Part B layer B3: moderator / conditionality test for a single marginal arrow.

Part A's central result is that the local A x D sign is *regime-conditional*, not
universal. The strongest real-world support is therefore not a pooled grand mean
but evidence that an arrow's strength **shifts across ecological context** in the
direction Part A predicts changes the mixed-partial sign
(see ``docs/PART_B_MECHANISM_META_STRATEGY_v1.md`` layer B3).

This module runs a dependency-free subgroup-contrast meta-analysis within one
arrow-stratum (route x trait_class x outcome_class x effect_metric x design_class):
it pools eligible effects separately at two declared moderator levels and reports
whether the between-level contrast has the predicted sign. It reuses the exact
effect recovery and DerSimonian-Laird pooling in
:mod:`trait_architecture.broad_meta_analysis`, so B2 and B3 never diverge.

It is a subgroup contrast, not a full meta-regression, and it never recodes a
contrary result: a contradicted moderator is a finding, not an error.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from .broad_meta_analysis import (
    DIRECT_ROUTES,
    ORIENTATION,
    ROUTE_TRAIT_ROLE,
    Z_975,
    EffectEstimate,
    _bool,
    _der_simonian_laird,
    _text,
    effect_estimate,
    validate_effect_rows,
)


STRATUM_MATCH_FIELDS = ("route", "trait_class", "outcome_class", "effect_metric", "design_class")
CONTRAST_SIGNS = frozenset({"positive", "negative"})


@dataclass(frozen=True)
class LevelPool:
    """Pooled effect for one moderator level within an arrow-stratum."""

    level: str
    clusters: int
    effect_count: int
    pooled_effect: float | None
    pooled_standard_error: float | None
    inference: str  # pooled | single_effect_no_between_study_inference | no_effects


@dataclass(frozen=True)
class ModeratorContrast:
    """Between-level contrast for one moderator within one arrow-stratum."""

    route: str
    trait_class: str
    outcome_class: str
    effect_metric: str
    design_class: str
    moderator_variable: str
    low_level: str
    high_level: str
    predicted_contrast_sign: str
    low: LevelPool
    high: LevelPool
    contrast: float | None
    contrast_standard_error: float | None
    contrast_ci_low: float | None
    contrast_ci_high: float | None
    z_value: float | None
    two_sided_p_value: float | None
    status: str


def _pool_level(level: str, estimates: list[EffectEstimate], *, min_clusters: int) -> LevelPool:
    clusters = len({estimate.study_cluster_id for estimate in estimates})
    if not estimates:
        return LevelPool(level, 0, 0, None, None, "no_effects")
    if len(estimates) == 1 or clusters < 2:
        estimate = estimates[0]
        inference = (
            "single_effect_no_between_study_inference"
            if clusters < min_clusters
            else "pooled"
        )
        # With one cluster there is no between-study variance; carry the reported SE.
        return LevelPool(level, clusters, len(estimates), estimate.value, estimate.standard_error, inference)
    diagnostics = _der_simonian_laird(estimates)
    inference = "pooled" if clusters >= min_clusters else "single_effect_no_between_study_inference"
    return LevelPool(
        level,
        clusters,
        len(estimates),
        diagnostics["pooled_effect"],
        diagnostics["pooled_standard_error"],
        inference,
    )


def _matches_stratum(row: dict[str, str], stratum: dict[str, str]) -> bool:
    return all(_text(row.get(field)) == stratum[field] for field in STRATUM_MATCH_FIELDS)


def moderator_contrast(
    effect_rows: Iterable[dict[str, str]],
    *,
    route: str,
    trait_class: str,
    outcome_class: str,
    effect_metric: str,
    design_class: str,
    moderator_variable: str,
    low_level: str,
    high_level: str,
    predicted_contrast_sign: str,
    min_clusters_per_level: int = 2,
) -> ModeratorContrast:
    """Contrast an arrow's pooled effect between two moderator levels.

    ``predicted_contrast_sign`` is the sign Part A predicts for ``high - low`` under
    the moderator hypothesis (e.g. for ``d_A`` the antagonist-tracking arrow is
    predicted to be *more positive* where pollination generalization is higher, so
    the contrast is ``positive``). A verdict of ``moderator_supported`` requires the
    contrast confidence interval to exclude zero on the predicted side and both
    levels to have at least ``min_clusters_per_level`` independent clusters.
    """

    if route not in DIRECT_ROUTES:
        raise ValueError(f"unknown route: {route}")
    if predicted_contrast_sign not in CONTRAST_SIGNS:
        raise ValueError("predicted_contrast_sign must be 'positive' or 'negative'")
    if low_level == high_level:
        raise ValueError("low_level and high_level must differ")
    if min_clusters_per_level < 1:
        raise ValueError("min_clusters_per_level must be >= 1")

    stratum = {
        "route": route,
        "trait_class": trait_class,
        "outcome_class": outcome_class,
        "effect_metric": effect_metric,
        "design_class": design_class,
    }
    valid = validate_effect_rows(effect_rows)
    eligible = [
        row for row in valid
        if _text(row.get("analysis_status")) == "eligible_for_quantitative_synthesis"
        and _bool(row.get("is_primary_effect"))
        and _matches_stratum(row, stratum)
    ]
    if any(_text(row.get("trait_role")) != ROUTE_TRAIT_ROLE[route] for row in eligible):
        raise ValueError("an eligible effect has a trait_role inconsistent with the route")
    if any(_text(row.get("effect_orientation")) != ORIENTATION for row in eligible):
        raise ValueError("an eligible effect is not oriented to the declared trait and outcome")

    by_level: dict[str, list[EffectEstimate]] = {low_level: [], high_level: []}
    for row in eligible:
        level = _text(row.get("moderator_level"))
        if _text(row.get("moderator_variable")) != moderator_variable or level not in by_level:
            continue
        by_level[level].append(effect_estimate(row))

    low = _pool_level(low_level, by_level[low_level], min_clusters=min_clusters_per_level)
    high = _pool_level(high_level, by_level[high_level], min_clusters=min_clusters_per_level)

    contrast = contrast_se = ci_low = ci_high = z_value = p_value = None
    if low.pooled_effect is not None and high.pooled_effect is not None:
        contrast = high.pooled_effect - low.pooled_effect
        contrast_se = math.sqrt(low.pooled_standard_error ** 2 + high.pooled_standard_error ** 2)
        ci_low = contrast - Z_975 * contrast_se
        ci_high = contrast + Z_975 * contrast_se
        z_value = contrast / contrast_se if contrast_se > 0 else math.inf
        p_value = math.erfc(abs(z_value) / math.sqrt(2))

    both_replicated = low.inference == "pooled" and high.inference == "pooled"
    if contrast is None:
        status = "insufficient_levels"
    elif not both_replicated:
        status = "single_effect_no_between_study_inference"
    elif ci_low <= 0 <= ci_high:
        status = "moderator_uncertain"
    else:
        observed_sign = "positive" if contrast > 0 else "negative"
        status = "moderator_supported" if observed_sign == predicted_contrast_sign else "moderator_contradicted"

    return ModeratorContrast(
        route=route,
        trait_class=trait_class,
        outcome_class=outcome_class,
        effect_metric=effect_metric,
        design_class=design_class,
        moderator_variable=moderator_variable,
        low_level=low_level,
        high_level=high_level,
        predicted_contrast_sign=predicted_contrast_sign,
        low=low,
        high=high,
        contrast=contrast,
        contrast_standard_error=contrast_se,
        contrast_ci_low=ci_low,
        contrast_ci_high=ci_high,
        z_value=z_value,
        two_sided_p_value=p_value,
        status=status,
    )
