"""Part B support-route analytics: break-even bound on the unmeasured shared cost.

Part A proves that the local A x D sign is

    sign( H d_A e_F - P b_A c_D e^{-c_D D}(1 - c_R R) - c_AD ).

The four channel terms (``b_A``, ``d_A``, ``e_F``, ``c_D``) are the marginal
arrows that Part B pools from their own literatures. The shared cost ``c_AD`` is
not recoverable from those literatures and is therefore *bounded*, not estimated
(see ``docs/PART_B_MECHANISM_META_STRATEGY_v1.md`` layer B4).

For a declared local regime case and channel-parameter values, this module
computes the break-even shared cost

    tau = H d_A e_F - P b_A c_D e^{-c_D D}(1 - c_R R)

at which the predicted sign flips: the model predicts local complementarity iff
``c_AD < tau``. It reuses the exact Part I decomposition in
:mod:`trait_architecture.robustness`, so the two never diverge.

Nothing here estimates ``c_AD``. It turns "c_AD is unmeasured" into an explicit,
falsifiable threshold given the empirical channel envelopes from B2.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, Mapping, Sequence

from .model import ModelParameters
from .robustness import BASELINE_FORM, FunctionalForm, RobustnessCase, mixed_partial


# ModelParameters field names for the four marginal channel arrows. These are the
# only parameters Part B's marginal literatures are allowed to inform; c_AD and
# c_R stay declared sensitivity axes.
CHANNEL_PARAMETER_FIELDS = (
    "attraction_gain",          # b_A  <- A_to_pollination
    "attraction_tracking",      # d_A  <- A_to_antagonism
    "floral_defence_efficacy",  # e_F  <- B_to_antagonism
    "defence_pollinator_cost",  # c_D  <- B_to_pollination
)


@dataclass(frozen=True)
class BreakEvenResult:
    """Break-even shared cost for one local case and functional form.

    ``channel_balance`` is ``H d_A e_F - P b_A c_D e^{-c_D D}(1 - c_R R)`` and is
    independent of ``c_AD``. ``break_even_shared_cost`` (tau) is the value of
    ``c_AD`` at which the local mixed partial is zero for the chosen functional
    form. The model predicts local complementarity iff the declared shared cost is
    below tau.
    """

    case_id: str
    form_id: str
    channel_balance: float
    shared_cost_multiplier: float
    break_even_shared_cost: float
    declared_shared_cost: float
    margin_to_break_even: float
    predicted_sign: str


def _shared_cost_multiplier(case: RobustnessCase, form: FunctionalForm) -> float:
    """Return the ``c_AD`` multiplier for the chosen shared-cost curvature.

    This mirrors the shared-cost term in :func:`trait_architecture.robustness`
    exactly: ``c_AD * (1 + 2 k_AD (A + D))``. It is always >= 1.
    """

    return 1.0 + 2.0 * form.shared_cost_curvature * (case.attraction + case.defence)


def break_even_shared_cost(
    case: RobustnessCase,
    parameters: ModelParameters,
    form: FunctionalForm = BASELINE_FORM,
    *,
    tolerance: float = 1e-12,
) -> BreakEvenResult:
    """Compute the ``c_AD`` break-even threshold for one local regime case.

    The channel balance is taken from the exact Part I decomposition so the
    break-even and the mixed-partial sign are guaranteed consistent: the mixed
    partial is positive iff the declared shared cost lies below the returned
    ``break_even_shared_cost``.
    """

    result = mixed_partial(case, parameters, form, tolerance=tolerance)
    channel_balance = result.antagonism_term - result.pollination_obstruction_term
    multiplier = _shared_cost_multiplier(case, form)
    break_even = channel_balance / multiplier
    declared = parameters.attraction_defence_shared_cost
    return BreakEvenResult(
        case_id=case.case_id,
        form_id=form.form_id,
        channel_balance=channel_balance,
        shared_cost_multiplier=multiplier,
        break_even_shared_cost=break_even,
        declared_shared_cost=declared,
        margin_to_break_even=break_even - declared,
        predicted_sign=result.sign,
    )


def parameters_from_channel_levels(
    base_parameters: ModelParameters,
    channel_overrides: Mapping[str, float],
) -> ModelParameters:
    """Return a copy of ``base_parameters`` with the four channel arrows overridden.

    Only the four ``CHANNEL_PARAMETER_FIELDS`` may be supplied; ``c_AD`` and ``c_R``
    remain whatever the base declares, because Part B never estimates them.
    """

    unknown = [field for field in channel_overrides if field not in CHANNEL_PARAMETER_FIELDS]
    if unknown:
        raise ValueError(
            "Part B may only override the four channel arrows; got: " + ", ".join(sorted(unknown))
        )
    return replace(base_parameters, **{field: float(value) for field, value in channel_overrides.items()})


def envelope_break_even_map(
    cases: Iterable[RobustnessCase],
    level_channel_overrides: Mapping[str, Mapping[str, float]],
    *,
    base_parameters: ModelParameters | None = None,
    shared_cost_scenarios: Sequence[float] | None = None,
    form: FunctionalForm = BASELINE_FORM,
    tolerance: float = 1e-12,
) -> list[dict[str, object]]:
    """Empirically informed regime map: break-even tau per envelope level and case.

    ``level_channel_overrides`` maps an envelope level label (e.g. ``low``/``mid``/
    ``high`` from :func:`parameter_envelopes.ready_parameter_overrides`) to the four
    channel-parameter values pooled in B2. For each level and case the map reports
    the break-even ``c_AD`` and, for each declared shared-cost scenario, the
    predicted regime label. Shared-cost scenarios are declared sensitivity values,
    never estimates.
    """

    base = base_parameters if base_parameters is not None else ModelParameters()
    scenarios = tuple(shared_cost_scenarios) if shared_cost_scenarios is not None else ()
    cases = list(cases)
    rows: list[dict[str, object]] = []
    for level in sorted(level_channel_overrides):
        parameters = parameters_from_channel_levels(base, level_channel_overrides[level])
        for case in cases:
            result = break_even_shared_cost(case, parameters, form, tolerance=tolerance)
            row: dict[str, object] = {
                "envelope_level": level,
                "case_id": case.case_id,
                "attraction": case.attraction,
                "defence": case.defence,
                "assurance": case.assurance,
                "pollinator_service": case.pollinator_service,
                "floral_damage_pressure": case.floral_damage_pressure,
                "form_id": result.form_id,
                "channel_balance": result.channel_balance,
                "break_even_shared_cost": result.break_even_shared_cost,
            }
            for scenario in scenarios:
                row[f"regime_at_c_AD_{scenario:g}"] = (
                    "complementary" if scenario < result.break_even_shared_cost else "substitutable"
                )
            rows.append(row)
    return rows
