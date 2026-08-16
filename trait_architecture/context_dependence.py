"""Predeclared moderator analysis for one constituent-pathway meta-analysis.

The pooled random-effects layer in :mod:`trait_architecture.broad_meta_analysis`
answers one question: what is the average oriented direction of a declared
marginal route inside one compatibility stratum?  That is only half of the
empirical target.  The local theory is conditional, so the empirical layer must
also report whether the route's realised direction *changes with declared
ecological context* rather than behaving as a single universal constant.

This module supplies that second half:

``subgroup_analysis``
    Pools each declared moderator level separately and tests between-level
    heterogeneity (``Q_between``).

``meta_regression``
    Fits a random-effects meta-regression on one declared moderator with a
    method-of-moments residual heterogeneity estimate, reporting both
    model-based and cluster-robust standard errors.

``leave_one_cluster_out``
    Reports whether the pooled direction survives removal of any single
    independent study cluster.

``egger_small_study_test``
    Reports a declared small-study/asymmetry diagnostic once enough independent
    clusters exist.

Boundaries that the rest of the repository already declares are preserved here.
A moderated marginal route effect is a statement about one *constituent*
pathway of the local mixed partial.  It is not the mixed partial, not a channel
curvature, and not an environmental derivative of the mixed partial.  What a
moderator result licenses is stated per analysis in the declared registry, and
the interface document ``docs/IOTA_PATHWAY_EMPIRICAL_TARGET.md`` states the
bridge assumption under which a marginal arrow constrains a channel sign.

Only the standard library is used, so the analysis contract stays reproducible
in the repository CI environment.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import NormalDist
from typing import Iterable, Sequence

from trait_architecture.broad_meta_analysis import (
    EffectEstimate,
    _text,
    _bool,
    _float,
    _require_columns,
    effect_estimate,
    random_effects_pool,
    read_csv_rows,
    validate_effect_rows,
    write_csv_rows,
)

Z_975 = NormalDist().inv_cdf(0.975)

MODERATOR_TYPES = frozenset({"categorical", "continuous"})
MODERATOR_CODING_STATUSES = frozenset({"coded", "needs_coding", "not_applicable"})

MODERATOR_REGISTRY_FIELDS = (
    "analysis_id",
    "stratum_id",
    "moderator_name",
    "moderator_type",
    "reference_level",
    "min_levels",
    "min_clusters_per_level",
    "min_clusters_total",
    "declared_hypothesis",
    "licensed_statement",
    "interpretation",
)
MODERATOR_CODING_FIELDS = (
    "effect_id",
    "moderator_name",
    "moderator_value",
    "coding_basis",
    "coder_id",
    "coding_date",
    "coding_status",
)

SUBGROUP_OUTPUT_FIELDS = (
    "analysis_id", "stratum_id", "moderator_name", "moderator_level",
    "independent_clusters", "effect_count", "pooled_effect", "pooled_standard_error",
    "ci_low", "ci_high", "tau_squared_DL", "I_squared_percent", "pooled_direction",
    "level_status",
)
SUBGROUP_TEST_FIELDS = (
    "analysis_id", "stratum_id", "moderator_name", "moderator_type", "analysis_status",
    "levels_analysed", "independent_clusters", "effect_count", "Q_between_fixed_effect",
    "Q_between_df", "Q_between_fixed_effect_p_value", "inferential_role",
    "context_dependence_verdict", "licensed_statement",
)
META_REGRESSION_FIELDS = (
    "analysis_id", "stratum_id", "moderator_name", "moderator_type", "analysis_status",
    "term", "coefficient", "model_standard_error", "cluster_robust_standard_error",
    "primary_standard_error", "standard_error_basis", "ci_low", "ci_high",
    "t_value", "degrees_of_freedom", "two_sided_p_value",
)
META_REGRESSION_MODEL_FIELDS = (
    "analysis_id", "stratum_id", "moderator_name", "moderator_type", "analysis_status",
    "effect_count", "independent_clusters", "parameters", "tau_squared_unconditional",
    "tau_squared_residual", "heterogeneity_explained_fraction", "Q_residual",
    "Q_moderator", "Q_moderator_df", "Q_moderator_p_value", "context_dependence_verdict",
    "licensed_statement",
)
INFLUENCE_FIELDS = (
    "analysis_id", "stratum_id", "omitted_study_cluster_id", "independent_clusters",
    "pooled_effect", "ci_low", "ci_high", "pooled_direction", "direction_matches_full_set",
)
SMALL_STUDY_FIELDS = (
    "analysis_id", "stratum_id", "analysis_status", "independent_clusters",
    "intercept", "intercept_standard_error", "t_value", "degrees_of_freedom",
    "two_sided_p_value", "asymmetry_verdict",
)


# ---------------------------------------------------------------------------
# small numerical helpers (standard library only)
# ---------------------------------------------------------------------------


def _log_beta(a: float, b: float) -> float:
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def _betacf(a: float, b: float, x: float) -> float:
    """Continued-fraction expansion for the incomplete beta function."""

    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        numerator = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        numerator = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return h


def regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(a * math.log(x) + b * math.log1p(-x) - _log_beta(a, b))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - math.exp(b * math.log1p(-x) + a * math.log(x) - _log_beta(b, a)) * _betacf(b, a, 1.0 - x) / b


def student_t_two_sided_p(t_value: float, df: float) -> float:
    """Two-sided Student-t p-value; needed because moderator tests use small df."""

    if df <= 0:
        raise ValueError("degrees of freedom must be positive")
    if not math.isfinite(t_value):
        raise ValueError("t value must be finite")
    x = df / (df + t_value * t_value)
    return regularized_incomplete_beta(df / 2.0, 0.5, x)


def student_t_quantile_975(df: float) -> float:
    """Upper 97.5% Student-t quantile by monotone bisection on the p-value."""

    if df <= 0:
        raise ValueError("degrees of freedom must be positive")
    low, high = 0.0, 2000.0
    for _ in range(200):
        middle = 0.5 * (low + high)
        if student_t_two_sided_p(middle, df) > 0.05:
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def chi_square_upper_p(statistic: float, df: int) -> float:
    """Upper-tail chi-square probability via the regularized gamma function."""

    if df <= 0:
        raise ValueError("degrees of freedom must be positive")
    if statistic <= 0:
        return 1.0
    shape = df / 2.0
    x = statistic / 2.0
    if x < shape + 1.0:
        term = 1.0 / shape
        total = term
        for index in range(1, 1000):
            term *= x / (shape + index)
            total += term
            if abs(term) < abs(total) * 1e-16:
                break
        lower = total * math.exp(-x + shape * math.log(x) - math.lgamma(shape))
        return max(0.0, 1.0 - lower)
    tiny = 1e-300
    b = x + 1.0 - shape
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for index in range(1, 1000):
        an = -index * (index - shape)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-15:
            break
    return min(1.0, h * math.exp(-x + shape * math.log(x) - math.lgamma(shape)))


def _invert(matrix: list[list[float]]) -> list[list[float]]:
    """Gauss-Jordan inverse for the small design matrices used here."""

    size = len(matrix)
    work = [list(row) + [1.0 if i == j else 0.0 for j in range(size)] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot_row = max(range(column, size), key=lambda r: abs(work[r][column]))
        if abs(work[pivot_row][column]) < 1e-12:
            raise ValueError("moderator design matrix is singular; declared levels are collinear")
        work[column], work[pivot_row] = work[pivot_row], work[column]
        pivot = work[column][column]
        work[column] = [value / pivot for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column]
            if factor == 0.0:
                continue
            work[row] = [value - factor * pivot_value for value, pivot_value in zip(work[row], work[column])]
    return [row[size:] for row in work]


def _matvec(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


# ---------------------------------------------------------------------------
# declared inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ModeratedEffect:
    estimate: EffectEstimate
    moderator_value: str

    @property
    def value(self) -> float:
        return self.estimate.value

    @property
    def variance(self) -> float:
        return self.estimate.standard_error ** 2

    @property
    def study_cluster_id(self) -> str:
        return self.estimate.study_cluster_id


def read_moderator_registry(path: str | Path) -> list[dict[str, str]]:
    rows = read_csv_rows(path)
    _require_columns(rows, MODERATOR_REGISTRY_FIELDS, "moderator registry")
    identifiers: set[str] = set()
    for row in rows:
        analysis_id = _text(row.get("analysis_id"))
        if not analysis_id or analysis_id in identifiers:
            raise ValueError("moderator analysis IDs must be nonempty and unique")
        identifiers.add(analysis_id)
        if _text(row.get("moderator_type")) not in MODERATOR_TYPES:
            raise ValueError(f"moderator analysis {analysis_id} has invalid moderator_type")
        if not _text(row.get("stratum_id")) or not _text(row.get("moderator_name")):
            raise ValueError(f"moderator analysis {analysis_id} needs stratum_id and moderator_name")
        if not _text(row.get("declared_hypothesis")) or not _text(row.get("licensed_statement")):
            raise ValueError(
                f"moderator analysis {analysis_id} needs a predeclared hypothesis and licensed statement"
            )
        min_levels = int(_float(row.get("min_levels"), "min_levels", positive=True))
        per_level = int(_float(row.get("min_clusters_per_level"), "min_clusters_per_level", positive=True))
        total = int(_float(row.get("min_clusters_total"), "min_clusters_total", positive=True))
        if min_levels < 2:
            raise ValueError(f"moderator analysis {analysis_id} needs at least two declared levels")
        if per_level < 2:
            raise ValueError(f"moderator analysis {analysis_id} needs at least two clusters per level")
        if total < min_levels * per_level:
            raise ValueError(f"moderator analysis {analysis_id} has inconsistent cluster thresholds")
    return rows


def read_moderator_coding(path: str | Path) -> list[dict[str, str]]:
    rows = read_csv_rows(path)
    _require_columns(rows, MODERATOR_CODING_FIELDS, "moderator coding")
    seen: set[tuple[str, str]] = set()
    for row in rows:
        effect_id = _text(row.get("effect_id"))
        moderator_name = _text(row.get("moderator_name"))
        if not effect_id or not moderator_name:
            raise ValueError("moderator coding rows need effect_id and moderator_name")
        key = (effect_id, moderator_name)
        if key in seen:
            raise ValueError(f"duplicate moderator coding for {effect_id} / {moderator_name}")
        seen.add(key)
        status = _text(row.get("coding_status"))
        if status not in MODERATOR_CODING_STATUSES:
            raise ValueError(f"moderator coding for {effect_id} has invalid coding_status")
        if status == "coded":
            if not _text(row.get("moderator_value")):
                raise ValueError(f"coded moderator row for {effect_id} needs a moderator_value")
            if not _text(row.get("coding_basis")):
                raise ValueError(f"coded moderator row for {effect_id} needs a coding_basis")
    return rows


def _matches_stratum(row: dict[str, str], stratum: dict[str, str]) -> bool:
    return all(row.get(field, "") == stratum[field] for field in (
        "route", "trait_class", "outcome_class", "effect_metric", "design_class",
    ))


def collect_moderated_effects(
    effect_rows: Iterable[dict[str, str]],
    coding_rows: Iterable[dict[str, str]],
    stratum: dict[str, str],
    moderator_name: str,
    moderator_type: str,
) -> list[ModeratedEffect]:
    """Return oriented effects in one stratum that carry a coded moderator value.

    ``is_primary_effect`` is deliberately *not* required here.  A context
    moderator is frequently manipulated within a single study, so restricting
    the analysis to one effect per cluster would discard exactly the contrast
    the analysis exists to measure.  Independence is instead protected by
    requiring at most one effect per cluster per categorical level, and by
    reporting cluster-robust standard errors and cluster-count degrees of
    freedom.
    """

    coding = {
        (_text(row["effect_id"]), _text(row["moderator_name"])): row
        for row in coding_rows
        if _text(row.get("coding_status")) == "coded"
    }
    selected: list[ModeratedEffect] = []
    level_keys: set[tuple[str, str]] = set()
    for row in effect_rows:
        if _text(row.get("analysis_status")) != "eligible_for_quantitative_synthesis":
            continue
        if not _matches_stratum(row, stratum):
            continue
        coded = coding.get((_text(row.get("effect_id")), moderator_name))
        if coded is None:
            continue
        value = _text(coded["moderator_value"])
        estimate = effect_estimate(row)
        if moderator_type == "categorical":
            key = (estimate.study_cluster_id, value)
            if key in level_keys:
                raise ValueError(
                    "more than one effect for one study cluster at one moderator level: "
                    f"{estimate.study_cluster_id} / {value}"
                )
            level_keys.add(key)
        else:
            _float(value, f"moderator value for {row.get('effect_id')}")
        selected.append(ModeratedEffect(estimate, value))
    return selected


# ---------------------------------------------------------------------------
# analyses
# ---------------------------------------------------------------------------


def _fixed_effect_q(effects: Sequence[ModeratedEffect]) -> tuple[float, float]:
    weights = [1.0 / effect.variance for effect in effects]
    mean = sum(w * e.value for w, e in zip(weights, effects)) / sum(weights)
    q = sum(w * (e.value - mean) ** 2 for w, e in zip(weights, effects))
    return q, mean


def subgroup_analysis(
    effects: Sequence[ModeratedEffect],
    registry_row: dict[str, str],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Pool each declared moderator level separately, descriptively.

    The classic between-level statistic ``Q_between`` is computed here from
    fixed-effect weights, which treat all within-level scatter as sampling
    noise. Simulation through this same code
    (:mod:`trait_architecture.design_power`) shows the consequence: its
    false-positive rate rises from 5% at zero between-cluster heterogeneity to
    roughly 28% at tau = 0.25 and 55% at tau = 0.50 on the declared effect
    scale. Any realistic value of tau for this literature therefore makes it
    unusable as an inferential test.

    It is retained as a descriptive partition of heterogeneity and explicitly
    marked as such. The inferential verdict for a categorical moderator comes
    from :func:`meta_regression`, whose contrast test is calibrated at or below
    nominal size across the same simulations.
    """

    analysis_id = registry_row["analysis_id"]
    stratum_id = registry_row["stratum_id"]
    moderator_name = registry_row["moderator_name"]
    per_level_min = int(float(registry_row["min_clusters_per_level"]))
    min_levels = int(float(registry_row["min_levels"]))
    total_min = int(float(registry_row["min_clusters_total"]))

    grouped: dict[str, list[ModeratedEffect]] = defaultdict(list)
    for effect in effects:
        grouped[effect.moderator_value].append(effect)

    level_rows: list[dict[str, object]] = []
    analysable: list[list[ModeratedEffect]] = []
    for level, members in sorted(grouped.items()):
        clusters = {member.study_cluster_id for member in members}
        base = {
            "analysis_id": analysis_id,
            "stratum_id": stratum_id,
            "moderator_name": moderator_name,
            "moderator_level": level,
            "independent_clusters": len(clusters),
            "effect_count": len(members),
        }
        if len(clusters) < per_level_min:
            level_rows.append({
                **base, "pooled_effect": "", "pooled_standard_error": "", "ci_low": "",
                "ci_high": "", "tau_squared_DL": "", "I_squared_percent": "",
                "pooled_direction": "", "level_status": "insufficient_clusters_at_level",
            })
            continue
        pooled = random_effects_pool([member.estimate for member in members])
        direction = "positive" if pooled["pooled_effect"] > 0 else "negative" if pooled["pooled_effect"] < 0 else "zero"
        level_rows.append({
            **base,
            "pooled_effect": f"{pooled['pooled_effect']:.10g}",
            "pooled_standard_error": f"{pooled['pooled_standard_error']:.10g}",
            "ci_low": f"{pooled['ci_low']:.10g}",
            "ci_high": f"{pooled['ci_high']:.10g}",
            "tau_squared_DL": f"{pooled['tau_squared_DL']:.10g}",
            "I_squared_percent": f"{pooled['I_squared_percent']:.10g}",
            "pooled_direction": direction,
            "level_status": "pooled_random_effects",
        })
        analysable.append(members)

    all_clusters = {effect.study_cluster_id for effect in effects}
    test_base = {
        "analysis_id": analysis_id,
        "stratum_id": stratum_id,
        "moderator_name": moderator_name,
        "moderator_type": registry_row["moderator_type"],
        "levels_analysed": len(analysable),
        "independent_clusters": len(all_clusters),
        "effect_count": len(effects),
        "licensed_statement": registry_row["licensed_statement"],
    }
    if len(analysable) < min_levels or len(all_clusters) < total_min:
        return level_rows, {
            **test_base, "analysis_status": "insufficient_moderator_capacity",
            "Q_between_fixed_effect": "", "Q_between_df": "",
            "Q_between_fixed_effect_p_value": "",
            "inferential_role": "descriptive_only_not_used_for_inference",
            "context_dependence_verdict": "not_evaluated",
        }

    pooled_members = [member for group in analysable for member in group]
    q_total, _ = _fixed_effect_q(pooled_members)
    q_within = sum(_fixed_effect_q(group)[0] for group in analysable)
    q_between = max(0.0, q_total - q_within)
    df = len(analysable) - 1
    p_value = chi_square_upper_p(q_between, df)
    return level_rows, {
        **test_base,
        "analysis_status": "subgroup_random_effects",
        "Q_between_fixed_effect": f"{q_between:.10g}",
        "Q_between_df": df,
        "Q_between_fixed_effect_p_value": f"{p_value:.10g}",
        "inferential_role": "descriptive_only_not_used_for_inference",
        "context_dependence_verdict": "see_meta_regression_verdict",
    }


def _design_matrix(
    effects: Sequence[ModeratedEffect],
    moderator_type: str,
    reference_level: str,
) -> tuple[list[list[float]], list[str]]:
    if moderator_type == "continuous":
        return [[1.0, float(effect.moderator_value)] for effect in effects], ["intercept", "moderator_slope"]
    levels = sorted({effect.moderator_value for effect in effects})
    if reference_level not in levels:
        raise ValueError(f"declared reference level '{reference_level}' is absent from the coded effects")
    contrasts = [level for level in levels if level != reference_level]
    matrix = [
        [1.0] + [1.0 if effect.moderator_value == level else 0.0 for level in contrasts]
        for effect in effects
    ]
    return matrix, ["intercept"] + [f"level[{level}]-vs-[{reference_level}]" for level in contrasts]


def _weighted_least_squares(
    design: Sequence[Sequence[float]],
    outcomes: Sequence[float],
    weights: Sequence[float],
) -> tuple[list[float], list[list[float]]]:
    parameters = len(design[0])
    xtwx = [[0.0] * parameters for _ in range(parameters)]
    xtwy = [0.0] * parameters
    for row, y, w in zip(design, outcomes, weights):
        for i in range(parameters):
            xtwy[i] += w * row[i] * y
            for j in range(parameters):
                xtwx[i][j] += w * row[i] * row[j]
    inverse = _invert(xtwx)
    return _matvec(inverse, xtwy), inverse


def _sign_reversal_between_levels(level_rows: Sequence[dict[str, object]]) -> bool:
    """True only when two pooled levels have opposite signs *and* exclude zero.

    Requiring the confidence intervals to exclude zero is not decoration. With
    a true level effect of exactly zero, pooled level directions differ by
    chance about half the time, so a sign-only rule reports a direction
    reversal in roughly a third of null simulations. Gating on the intervals
    removes that failure mode.
    """

    signed: list[int] = []
    for row in level_rows:
        if row.get("level_status") != "pooled_random_effects":
            continue
        try:
            low = float(row["ci_low"])
            high = float(row["ci_high"])
        except (KeyError, TypeError, ValueError):
            continue
        if low > 0:
            signed.append(1)
        elif high < 0:
            signed.append(-1)
    return 1 in signed and -1 in signed


def meta_regression(
    effects: Sequence[ModeratedEffect],
    registry_row: dict[str, str],
    level_summaries: Sequence[dict[str, object]] | None = None,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Fit a random-effects meta-regression on one predeclared moderator.

    Residual heterogeneity uses the method-of-moments (DerSimonian-Laird type)
    estimator generalised to a design matrix.  Model-based standard errors
    assume independent effects; cluster-robust standard errors do not, and are
    reported as primary whenever any study cluster contributes more than one
    effect.
    """

    analysis_id = registry_row["analysis_id"]
    stratum_id = registry_row["stratum_id"]
    moderator_name = registry_row["moderator_name"]
    moderator_type = registry_row["moderator_type"]
    total_min = int(float(registry_row["min_clusters_total"]))
    per_level_min = int(float(registry_row["min_clusters_per_level"]))
    min_levels = int(float(registry_row["min_levels"]))

    clusters = sorted({effect.study_cluster_id for effect in effects})
    model_base = {
        "analysis_id": analysis_id,
        "stratum_id": stratum_id,
        "moderator_name": moderator_name,
        "moderator_type": moderator_type,
        "effect_count": len(effects),
        "independent_clusters": len(clusters),
        "licensed_statement": registry_row["licensed_statement"],
    }
    empty_model = {
        **model_base, "analysis_status": "insufficient_moderator_capacity", "parameters": "",
        "tau_squared_unconditional": "", "tau_squared_residual": "",
        "heterogeneity_explained_fraction": "", "Q_residual": "", "Q_moderator": "",
        "Q_moderator_df": "", "Q_moderator_p_value": "", "context_dependence_verdict": "not_evaluated",
    }
    if len(clusters) < total_min:
        return [], empty_model
    if moderator_type == "categorical":
        level_clusters: dict[str, set[str]] = defaultdict(set)
        for effect in effects:
            level_clusters[effect.moderator_value].add(effect.study_cluster_id)
        usable = [level for level, members in level_clusters.items() if len(members) >= per_level_min]
        if len(usable) < min_levels:
            return [], empty_model
        effects = [effect for effect in effects if effect.moderator_value in usable]
        clusters = sorted({effect.study_cluster_id for effect in effects})
    elif len({effect.moderator_value for effect in effects}) < min_levels:
        return [], empty_model

    design, terms = _design_matrix(effects, moderator_type, _text(registry_row.get("reference_level")))
    parameters = len(terms)
    k = len(effects)
    if k - parameters < 1 or len(clusters) - parameters < 1:
        return [], empty_model

    outcomes = [effect.value for effect in effects]
    variances = [effect.variance for effect in effects]

    fixed_weights = [1.0 / v for v in variances]
    beta_fixed, _ = _weighted_least_squares(design, outcomes, fixed_weights)
    residuals_fixed = [y - sum(b * x for b, x in zip(beta_fixed, row)) for y, row in zip(outcomes, design)]
    q_residual = sum(w * r * r for w, r in zip(fixed_weights, residuals_fixed))

    # method-of-moments residual tau^2: (Q_E - (k - p)) / trace term
    xtwx_fixed = [[0.0] * parameters for _ in range(parameters)]
    xtw2x = [[0.0] * parameters for _ in range(parameters)]
    for row, w in zip(design, fixed_weights):
        for i in range(parameters):
            for j in range(parameters):
                xtwx_fixed[i][j] += w * row[i] * row[j]
                xtw2x[i][j] += w * w * row[i] * row[j]
    inverse_fixed = _invert(xtwx_fixed)
    product = [[sum(inverse_fixed[i][m] * xtw2x[m][j] for m in range(parameters)) for j in range(parameters)] for i in range(parameters)]
    trace_term = sum(fixed_weights) - sum(product[i][i] for i in range(parameters))
    tau_squared = max(0.0, (q_residual - (k - parameters)) / trace_term) if trace_term > 0 else 0.0

    weights = [1.0 / (v + tau_squared) for v in variances]
    beta, inverse = _weighted_least_squares(design, outcomes, weights)
    residuals = [y - sum(b * x for b, x in zip(beta, row)) for y, row in zip(outcomes, design)]

    unconditional = random_effects_pool([effect.estimate for effect in effects])
    tau_squared_total = unconditional["tau_squared_DL"]
    explained = (
        max(0.0, (tau_squared_total - tau_squared) / tau_squared_total) if tau_squared_total > 0 else 0.0
    )

    # cluster-robust (CR1) sandwich
    meat = [[0.0] * parameters for _ in range(parameters)]
    by_cluster: dict[str, list[float]] = defaultdict(lambda: [0.0] * parameters)
    for row, residual, w, effect in zip(design, residuals, weights, effects):
        score = by_cluster[effect.study_cluster_id]
        for i in range(parameters):
            score[i] += w * row[i] * residual
    for score in by_cluster.values():
        for i in range(parameters):
            for j in range(parameters):
                meat[i][j] += score[i] * score[j]
    n_clusters = len(by_cluster)
    correction = (n_clusters / (n_clusters - 1)) * ((k - 1) / (k - parameters)) if n_clusters > 1 else 1.0
    robust = [
        [
            correction * sum(
                inverse[i][m] * meat[m][n] * inverse[n][j]
                for m in range(parameters)
                for n in range(parameters)
            )
            for j in range(parameters)
        ]
        for i in range(parameters)
    ]

    multiple_effects_per_cluster = k > n_clusters
    basis = "cluster_robust_CR1" if multiple_effects_per_cluster else "model_based_random_effects"
    df = float(n_clusters - parameters)
    critical = student_t_quantile_975(df)

    coefficient_rows: list[dict[str, object]] = []
    for index, term in enumerate(terms):
        model_se = math.sqrt(max(inverse[index][index], 0.0))
        robust_se = math.sqrt(max(robust[index][index], 0.0))
        primary_se = robust_se if multiple_effects_per_cluster else model_se
        t_value = beta[index] / primary_se if primary_se > 0 else math.inf
        coefficient_rows.append({
            "analysis_id": analysis_id,
            "stratum_id": stratum_id,
            "moderator_name": moderator_name,
            "moderator_type": moderator_type,
            "analysis_status": "random_effects_meta_regression",
            "term": term,
            "coefficient": f"{beta[index]:.10g}",
            "model_standard_error": f"{model_se:.10g}",
            "cluster_robust_standard_error": f"{robust_se:.10g}",
            "primary_standard_error": f"{primary_se:.10g}",
            "standard_error_basis": basis,
            "ci_low": f"{beta[index] - critical * primary_se:.10g}",
            "ci_high": f"{beta[index] + critical * primary_se:.10g}",
            "t_value": f"{t_value:.10g}",
            "degrees_of_freedom": f"{df:.10g}",
            "two_sided_p_value": f"{student_t_two_sided_p(t_value, df):.10g}" if math.isfinite(t_value) else "0",
        })

    moderator_indices = list(range(1, parameters))
    covariance = robust if multiple_effects_per_cluster else inverse
    sub = [[covariance[i][j] for j in moderator_indices] for i in moderator_indices]
    sub_beta = [beta[i] for i in moderator_indices]
    try:
        sub_inverse = _invert(sub)
    except ValueError:
        # A cluster-robust covariance collapses when every cluster residual is
        # zero. The coefficients remain reportable; the omnibus test does not.
        omnibus_estimable = False
        q_moderator, q_moderator_df, q_moderator_p = 0.0, len(moderator_indices), 1.0
    else:
        omnibus_estimable = True
        q_moderator = sum(
            sub_beta[i] * sub_inverse[i][j] * sub_beta[j]
            for i in range(len(sub_beta))
            for j in range(len(sub_beta))
        )
        q_moderator_df = len(moderator_indices)
        q_moderator_p = chi_square_upper_p(q_moderator, q_moderator_df)

    if not omnibus_estimable:
        verdict = "omnibus_moderator_test_not_estimable"
    elif q_moderator_p >= 0.05:
        verdict = "no_detected_context_dependence"
    elif level_summaries is None:
        verdict = "moderator_changes_route_effect"
    elif _sign_reversal_between_levels(level_summaries):
        verdict = "context_dependent_direction_reversal"
    else:
        verdict = "context_dependent_magnitude_only"

    model_row = {
        **model_base,
        "analysis_status": "random_effects_meta_regression",
        "effect_count": k,
        "independent_clusters": n_clusters,
        "parameters": parameters,
        "tau_squared_unconditional": f"{tau_squared_total:.10g}",
        "tau_squared_residual": f"{tau_squared:.10g}",
        "heterogeneity_explained_fraction": f"{explained:.10g}",
        "Q_residual": f"{q_residual:.10g}",
        "Q_moderator": f"{q_moderator:.10g}" if omnibus_estimable else "",
        "Q_moderator_df": q_moderator_df,
        "Q_moderator_p_value": f"{q_moderator_p:.10g}" if omnibus_estimable else "",
        "context_dependence_verdict": verdict,
    }
    return coefficient_rows, model_row


def leave_one_cluster_out(
    effects: Sequence[ModeratedEffect],
    analysis_id: str,
    stratum_id: str,
) -> list[dict[str, object]]:
    """Report whether the pooled direction depends on any single study cluster."""

    clusters = sorted({effect.study_cluster_id for effect in effects})
    if len(clusters) < 3:
        return []
    full = random_effects_pool([effect.estimate for effect in effects])
    full_direction = "positive" if full["pooled_effect"] > 0 else "negative" if full["pooled_effect"] < 0 else "zero"
    rows: list[dict[str, object]] = []
    for omitted in clusters:
        retained = [effect for effect in effects if effect.study_cluster_id != omitted]
        if len({effect.study_cluster_id for effect in retained}) < 2:
            continue
        pooled = random_effects_pool([effect.estimate for effect in retained])
        direction = "positive" if pooled["pooled_effect"] > 0 else "negative" if pooled["pooled_effect"] < 0 else "zero"
        rows.append({
            "analysis_id": analysis_id,
            "stratum_id": stratum_id,
            "omitted_study_cluster_id": omitted,
            "independent_clusters": len({effect.study_cluster_id for effect in retained}),
            "pooled_effect": f"{pooled['pooled_effect']:.10g}",
            "ci_low": f"{pooled['ci_low']:.10g}",
            "ci_high": f"{pooled['ci_high']:.10g}",
            "pooled_direction": direction,
            "direction_matches_full_set": "true" if direction == full_direction else "false",
        })
    return rows


def egger_small_study_test(
    effects: Sequence[ModeratedEffect],
    analysis_id: str,
    stratum_id: str,
    *,
    min_clusters: int = 10,
) -> dict[str, object]:
    """Declared funnel-asymmetry diagnostic, withheld below the declared k."""

    clusters = {effect.study_cluster_id for effect in effects}
    base = {
        "analysis_id": analysis_id,
        "stratum_id": stratum_id,
        "independent_clusters": len(clusters),
    }
    if len(clusters) < min_clusters:
        return {
            **base, "analysis_status": "withheld_below_declared_cluster_minimum",
            "intercept": "", "intercept_standard_error": "", "t_value": "",
            "degrees_of_freedom": "", "two_sided_p_value": "", "asymmetry_verdict": "not_evaluated",
        }
    design = [[1.0, math.sqrt(effect.variance)] for effect in effects]
    outcomes = [effect.value for effect in effects]
    weights = [1.0 / effect.variance for effect in effects]
    beta, inverse = _weighted_least_squares(design, outcomes, weights)
    residuals = [y - sum(b * x for b, x in zip(beta, row)) for y, row in zip(outcomes, design)]
    df = float(len(effects) - 2)
    scale = sum(w * r * r for w, r in zip(weights, residuals)) / df
    intercept_se = math.sqrt(max(scale * inverse[0][0], 0.0))
    t_value = beta[0] / intercept_se if intercept_se > 0 else math.inf
    p_value = student_t_two_sided_p(t_value, df) if math.isfinite(t_value) else 0.0
    return {
        **base,
        "analysis_status": "weighted_egger_regression",
        "intercept": f"{beta[0]:.10g}",
        "intercept_standard_error": f"{intercept_se:.10g}",
        "t_value": f"{t_value:.10g}",
        "degrees_of_freedom": f"{df:.10g}",
        "two_sided_p_value": f"{p_value:.10g}",
        "asymmetry_verdict": "asymmetry_detected" if p_value < 0.05 else "no_detected_asymmetry",
    }


def run_context_dependence(
    effect_rows: Iterable[dict[str, str]],
    coding_rows: Iterable[dict[str, str]],
    strata: Iterable[dict[str, str]],
    registry: Iterable[dict[str, str]],
) -> dict[str, list[dict[str, object]]]:
    """Execute every predeclared moderator analysis and return its output tables."""

    effect_rows = validate_effect_rows(effect_rows)
    coding_rows = list(coding_rows)
    strata_by_id = {row["stratum_id"]: row for row in strata}
    subgroup_levels: list[dict[str, object]] = []
    subgroup_tests: list[dict[str, object]] = []
    regression_terms: list[dict[str, object]] = []
    regression_models: list[dict[str, object]] = []
    influence: list[dict[str, object]] = []
    small_study: list[dict[str, object]] = []

    for registry_row in registry:
        stratum_id = registry_row["stratum_id"]
        if stratum_id not in strata_by_id:
            raise ValueError(f"moderator analysis {registry_row['analysis_id']} names an undeclared stratum")
        effects = collect_moderated_effects(
            effect_rows,
            coding_rows,
            strata_by_id[stratum_id],
            registry_row["moderator_name"],
            registry_row["moderator_type"],
        )
        levels: list[dict[str, object]] | None = None
        if registry_row["moderator_type"] == "categorical":
            levels, test = subgroup_analysis(effects, registry_row)
            subgroup_levels.extend(levels)
            subgroup_tests.append(test)
        terms, model = meta_regression(effects, registry_row, levels)
        regression_terms.extend(terms)
        regression_models.append(model)
        influence.extend(leave_one_cluster_out(effects, registry_row["analysis_id"], stratum_id))
        small_study.append(egger_small_study_test(effects, registry_row["analysis_id"], stratum_id))

    return {
        "subgroup_levels": subgroup_levels,
        "subgroup_tests": subgroup_tests,
        "meta_regression_terms": regression_terms,
        "meta_regression_models": regression_models,
        "influence": influence,
        "small_study": small_study,
    }


def write_context_outputs(
    out_dir: str | Path,
    effect_rows: Iterable[dict[str, str]],
    coding_rows: Iterable[dict[str, str]],
    strata: Iterable[dict[str, str]],
    registry: Iterable[dict[str, str]],
) -> dict[str, object]:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    tables = run_context_dependence(effect_rows, coding_rows, strata, registry)
    write_csv_rows(destination / "context_subgroup_levels.csv", SUBGROUP_OUTPUT_FIELDS, tables["subgroup_levels"])
    write_csv_rows(destination / "context_subgroup_tests.csv", SUBGROUP_TEST_FIELDS, tables["subgroup_tests"])
    write_csv_rows(destination / "context_meta_regression_terms.csv", META_REGRESSION_FIELDS, tables["meta_regression_terms"])
    write_csv_rows(destination / "context_meta_regression_models.csv", META_REGRESSION_MODEL_FIELDS, tables["meta_regression_models"])
    write_csv_rows(destination / "context_influence.csv", INFLUENCE_FIELDS, tables["influence"])
    write_csv_rows(destination / "context_small_study.csv", SMALL_STUDY_FIELDS, tables["small_study"])
    diagnostics = {
        "declared_analysis_count": len(tables["meta_regression_models"]),
        "executed_meta_regression_count": sum(
            row["analysis_status"] == "random_effects_meta_regression"
            for row in tables["meta_regression_models"]
        ),
        "executed_subgroup_count": sum(
            row["analysis_status"] == "subgroup_random_effects" for row in tables["subgroup_tests"]
        ),
        "interpretation_boundary": (
            "Moderator results describe how one declared marginal route effect changes with one declared "
            "ecological context variable. They are not the local A x D mixed partial, not a channel curvature, "
            "and not an environmental derivative of the mixed partial."
        ),
    }
    (destination / "context_dependence_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
    return diagnostics
