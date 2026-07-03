"""Part B layer B5: arrow evidence synthesis + regime-leverage priority queue.

The B1-B4 layers say, per arrow, *what the evidence currently is*. B5 answers the
research-management question the results force: **which arrow should be collected
next, and why**. It combines two objective signals:

1. Evidence state per arrow (from the real anchors): absent / single_anchor /
   consistent / poolable, plus two explicitly different unresolved states:
   ``within_stratum_conflict`` and ``cross_stratum_heterogeneity``.
2. Regime leverage (from B4): how much the fraction of complementary local cases
   moves when that arrow's channel parameter swings across its declared range.
   High leverage = the regime boundary is sensitive to this arrow.

A sign difference is only a conflict when opposite signs occur in the same
trait × outcome × metric × design stratum. Opposite signs across distinct strata
are heterogeneity, not evidence that one biological mechanism changes sign. The
latter requires stratum-specific collection before a B3 moderator is proposed.
Nothing here estimates a parameter or pools across scales; it is a decision layer
over the finished analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .broad_meta_analysis import (
    DIRECT_ROUTES,
    ROUTE_EXPECTED_SIGN,
    _bool,
    _text,
    effect_estimate,
    validate_effect_rows,
)
from .model import ModelParameters
from .part_b_support import CHANNEL_PARAMETER_FIELDS, envelope_break_even_map
from .robustness import RobustnessCase


# Channel parameter field -> (route, Part I symbol, role in the mixed partial).
# The antagonism term (H d_A e_F) drives complementarity; the obstruction term
# (P b_A c_D) drives substitutability.
FIELD_TO_ARROW = {
    "attraction_gain": ("A_to_pollination", "b_A", "substitutability_driver"),
    "attraction_tracking": ("A_to_antagonism", "d_A", "complementarity_driver"),
    "floral_defence_efficacy": ("B_to_antagonism", "e_F", "complementarity_driver"),
    "defence_pollinator_cost": ("B_to_pollination", "c_D", "substitutability_driver"),
}
ROUTE_TO_FIELD = {route: field for field, (route, _sym, _role) in FIELD_TO_ARROW.items()}
# One primary moderator per arrow (first entry of the arrow's B3 moderator set in
# configs/part_b_arrow_literature_seeds.json). It applies only to a genuine,
# within-stratum sign conflict.
ARROW_PRIMARY_MODERATOR = {
    "A_to_pollination": "pollination_generalization",
    "A_to_antagonism": "pollination_generalization",
    "B_to_antagonism": "defence_type_chemical_vs_physical",
    "B_to_pollination": "access_restriction_strength",
}
DEFAULT_POOLING_THRESHOLD = 3

ARROW_EVIDENCE_FIELDS = (
    "route", "part_i_parameter", "mixed_partial_role", "expected_sign",
    "independent_clusters", "positive_signs", "negative_signs", "compatible_signs",
    "distinct_strata", "sign_state", "clusters_needed_to_pool",
    "regime_leverage", "priority_rank", "recommended_action",
)


@dataclass(frozen=True)
class ArrowEvidence:
    route: str
    part_i_parameter: str
    mixed_partial_role: str
    expected_sign: str
    independent_clusters: int
    positive_signs: int
    negative_signs: int
    compatible_signs: int
    distinct_strata: int
    sign_state: str
    clusters_needed_to_pool: int
    regime_leverage: float | None
    priority_rank: int | None
    recommended_action: str


def _stratum(row: Mapping[str, str]) -> tuple[str, str, str, str]:
    """Return the compatibility stratum required by the B2 pooling contract."""

    return (
        _text(row.get("trait_class")),
        _text(row.get("outcome_class")),
        _text(row.get("effect_metric")),
        _text(row.get("design_class")),
    )


def synthesise_arrow_evidence(
    effect_rows: Iterable[Mapping[str, str]],
    *,
    pooling_threshold: int = DEFAULT_POOLING_THRESHOLD,
) -> dict[str, ArrowEvidence]:
    """Classify the current evidence state of each of the four marginal arrows.

    ``within_stratum_conflict`` means at least one compatible B2 stratum contains
    both signs. ``cross_stratum_heterogeneity`` means opposite signs occur only
    across distinct strata. The latter must not be treated as a biological sign
    reversal or sent directly to a B3 moderator analysis.
    """

    valid = validate_effect_rows(effect_rows)
    eligible = [
        row for row in valid
        if _text(row.get("analysis_status")) == "eligible_for_quantitative_synthesis"
        and _bool(row.get("is_primary_effect"))
    ]
    by_route: dict[str, list[Mapping[str, str]]] = {route: [] for route in DIRECT_ROUTES}
    for row in eligible:
        route = _text(row.get("route"))
        if route in by_route:
            by_route[route].append(row)

    evidence: dict[str, ArrowEvidence] = {}
    for route, rows in by_route.items():
        clusters = {_text(row.get("study_cluster_id")) for row in rows}
        stratum_estimates: dict[tuple[str, str, str, str], list[float]] = {}
        for row in rows:
            stratum_estimates.setdefault(_stratum(row), []).append(effect_estimate(dict(row)).value)
        positives = sum(1 for values in stratum_estimates.values() for value in values if value > 0)
        negatives = sum(1 for values in stratum_estimates.values() for value in values if value < 0)
        expected = ROUTE_EXPECTED_SIGN[route]
        compatible = positives if expected == "positive" else negatives
        k = len(clusters)
        within_stratum_conflict = any(
            any(value > 0 for value in values) and any(value < 0 for value in values)
            for values in stratum_estimates.values()
        )
        cross_stratum_heterogeneity = positives > 0 and negatives > 0 and not within_stratum_conflict
        if k == 0:
            sign_state = "absent"
        elif k == 1:
            sign_state = "single_anchor"
        elif within_stratum_conflict:
            sign_state = "within_stratum_conflict"
        elif cross_stratum_heterogeneity:
            sign_state = "cross_stratum_heterogeneity"
        elif k >= pooling_threshold:
            sign_state = "poolable_consistent"
        else:
            sign_state = "consistent"
        _sym, _role = FIELD_TO_ARROW[ROUTE_TO_FIELD[route]][1:]
        evidence[route] = ArrowEvidence(
            route=route,
            part_i_parameter=_sym,
            mixed_partial_role=_role,
            expected_sign=expected,
            independent_clusters=k,
            positive_signs=positives,
            negative_signs=negatives,
            compatible_signs=compatible,
            distinct_strata=len(stratum_estimates),
            sign_state=sign_state,
            clusters_needed_to_pool=max(0, pooling_threshold - k),
            regime_leverage=None,
            priority_rank=None,
            recommended_action="",
        )
    return evidence


def _fraction_complementary(
    cases: Sequence[RobustnessCase],
    channel_values: Mapping[str, float],
    shared_cost: float,
    base_parameters: ModelParameters,
) -> float:
    rows = envelope_break_even_map(
        cases,
        {"probe": dict(channel_values)},
        base_parameters=base_parameters,
        shared_cost_scenarios=(shared_cost,),
    )
    if not rows:
        return 0.0
    column = f"regime_at_c_AD_{shared_cost:g}"
    complementary = sum(1 for row in rows if row[column] == "complementary")
    return complementary / len(rows)


def arrow_regime_leverage(
    cases: Sequence[RobustnessCase],
    channel_envelopes: Mapping[str, Mapping[str, float]],
    *,
    shared_cost: float,
    base_parameters: ModelParameters | None = None,
    param_ranges: Mapping[str, Sequence[float]] | None = None,
) -> dict[str, float]:
    """Return each arrow's swing in fraction-complementary across a declared range.

    Holding the other three arrows at the baseline level (or the first declared
    level), each arrow's channel parameter is set to a low and a high value; the
    leverage is ``frac_complementary(high) - frac_complementary(low)``. Its sign
    shows the direction, its magnitude the pull on the regime boundary.

    The low/high per arrow come from ``param_ranges`` when supplied (a declared
    ``field -> (low, high)`` map, so every arrow gets a comparable probe even if the
    named scenarios hold it constant); otherwise they fall back to the min and max
    of that parameter across the declared envelope levels, and an arrow the
    envelopes hold constant gets leverage 0.
    """

    base = base_parameters if base_parameters is not None else ModelParameters()
    levels = list(channel_envelopes.values())
    if not levels:
        raise ValueError("channel_envelopes must declare at least one level")
    baseline_level = dict(channel_envelopes.get("baseline", levels[0]))
    leverage: dict[str, float] = {}
    for field in CHANNEL_PARAMETER_FIELDS:
        if param_ranges is not None and field in param_ranges:
            low, high = float(param_ranges[field][0]), float(param_ranges[field][1])
        else:
            values = [float(level[field]) for level in levels]
            low, high = min(values), max(values)
        low_channel = {**baseline_level, field: low}
        high_channel = {**baseline_level, field: high}
        frac_low = _fraction_complementary(cases, low_channel, shared_cost, base)
        frac_high = _fraction_complementary(cases, high_channel, shared_cost, base)
        route = FIELD_TO_ARROW[field][0]
        leverage[route] = frac_high - frac_low
    return leverage


def _recommended_action(item: ArrowEvidence) -> str:
    if item.sign_state == "within_stratum_conflict":
        moderator = ARROW_PRIMARY_MODERATOR[item.route]
        return f"code moderator '{moderator}' to resolve the within-stratum sign conflict (B3)"
    if item.sign_state == "cross_stratum_heterogeneity":
        return "retain trait/outcome/metric/design strata; collect compatible within-stratum clusters before B3"
    if item.sign_state == "poolable_consistent":
        return "pool the envelope (B2), then run B3 moderators"
    if item.sign_state in {"single_anchor", "consistent"}:
        need = item.clusters_needed_to_pool
        return f"collect {need} more independent cluster(s) to reach the pooling threshold"
    return "collect the first independent effect for this arrow"


def _unresolved_priority(sign_state: str) -> int:
    """Lower values are addressed first without treating heterogeneity as conflict."""

    return {
        "within_stratum_conflict": 0,
        "cross_stratum_heterogeneity": 1,
        "single_anchor": 2,
        "consistent": 2,
        "absent": 2,
        "poolable_consistent": 3,
    }[sign_state]


def prioritise_arrows(
    evidence: Mapping[str, ArrowEvidence],
    leverage: Mapping[str, float],
) -> list[ArrowEvidence]:
    """Rank arrows by leverage and unresolved evidence state.

    Genuine within-stratum conflict comes first, then cross-stratum heterogeneity,
    then underpowered consistent/single-anchor evidence. Poolable evidence sinks to
    the bottom. Cross-stratum heterogeneity remains important because the analysis
    needs stratum-specific evidence, but it is not a sign-reversal claim.
    """

    def sort_key(route: str) -> tuple:
        item = evidence[route]
        lev = leverage.get(route, 0.0)
        return (
            _unresolved_priority(item.sign_state),
            -abs(lev),
            item.clusters_needed_to_pool,
            route,
        )

    ordered = sorted(evidence, key=sort_key)
    ranked: list[ArrowEvidence] = []
    for rank, route in enumerate(ordered, start=1):
        item = evidence[route]
        ranked.append(
            ArrowEvidence(
                **{**item.__dict__, "regime_leverage": leverage.get(route, 0.0),
                   "priority_rank": rank, "recommended_action": _recommended_action(item)}
            )
        )
    return ranked


def arrow_evidence_to_row(item: ArrowEvidence) -> dict[str, object]:
    return {
        "route": item.route,
        "part_i_parameter": item.part_i_parameter,
        "mixed_partial_role": item.mixed_partial_role,
        "expected_sign": item.expected_sign,
        "independent_clusters": item.independent_clusters,
        "positive_signs": item.positive_signs,
        "negative_signs": item.negative_signs,
        "compatible_signs": item.compatible_signs,
        "distinct_strata": item.distinct_strata,
        "sign_state": item.sign_state,
        "clusters_needed_to_pool": item.clusters_needed_to_pool,
        "regime_leverage": "" if item.regime_leverage is None else f"{item.regime_leverage:.6f}",
        "priority_rank": "" if item.priority_rank is None else item.priority_rank,
        "recommended_action": item.recommended_action,
    }
