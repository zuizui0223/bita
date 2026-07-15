"""Sensitivity evaluator for the Part I floral attraction–barrier score.

The baseline model in :mod:`trait_architecture.model` is intentionally
qualitative. This module does not calibrate it from data. It evaluates whether
the sign of the local A×D mixed partial remains stable across a finite declared
family of nonlinear response shapes and biological parameter scenarios.

The nonlinear response shapes are endpoint-normalized on the declared 0–1 trait
range. For fixed biological parameters:

* attraction-mediated gain at ``A=1`` matches the linear baseline;
* antagonist protection at ``D=1`` matches the linear baseline; and
* direct joint cost at ``A=D=1`` matches the baseline corner cost.

This normalization reduces confounding between response-shape sensitivity and a
simple change in endpoint effect scale. It does not make the functions identical
in local derivatives or prove structural robustness.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import exp, isfinite
from typing import Iterable, Sequence

from .model import ModelParameters


@dataclass(frozen=True)
class FunctionalForm:
    """Endpoint-normalized response-shape choices for the Part I sensitivity set.

    For attraction, ``q_A = attraction_saturation`` gives

        b_A (1 + q_A) A / (1 + q_A A).

    For defence, ``q_D = defence_saturation`` gives

        e_F (1 + q_D) D / (1 + q_D D).

    Both reduce to the linear baseline when the corresponding saturation
    parameter is zero and match the linear endpoint at trait value one.

    ``joint_cost_curvature = k_AD`` gives

        c_AD A D [1 + k_AD(A + D)] / (1 + 2 k_AD),

    which preserves the baseline corner cost at ``A=D=1`` while changing local
    cross-cost curvature.
    """

    form_id: str
    attraction_saturation: float = 0.0
    defence_saturation: float = 0.0
    joint_cost_curvature: float = 0.0

    def __post_init__(self) -> None:
        if not self.form_id.strip():
            raise ValueError("form_id must be non-empty")
        for name, value in (
            ("attraction_saturation", self.attraction_saturation),
            ("defence_saturation", self.defence_saturation),
            ("joint_cost_curvature", self.joint_cost_curvature),
        ):
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")


@dataclass(frozen=True)
class RobustnessCase:
    """One local phenotype and interaction regime used in a sign sweep."""

    case_id: str
    attraction: float
    defence: float
    assurance: float
    pollinator_service: float
    floral_damage_pressure: float

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id must be non-empty")
        for name, value in (
            ("attraction", self.attraction),
            ("defence", self.defence),
            ("assurance", self.assurance),
            ("pollinator_service", self.pollinator_service),
            ("floral_damage_pressure", self.floral_damage_pressure),
        ):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be finite and lie in [0, 1]")


@dataclass(frozen=True)
class MixedPartialResult:
    """Mixed-partial decomposition for one case and response shape."""

    case_id: str
    form_id: str
    antagonism_term: float
    pollination_obstruction_term: float
    joint_cost_curvature_term: float
    mixed_partial: float
    sign: str


@dataclass(frozen=True)
class RobustnessSummary:
    """Sign agreement across the finite set of evaluations supplied for one case."""

    case_id: str
    modal_sign: str
    non_neutral_form_count: int
    total_form_count: int
    modal_sign_agreement: float
    robustness_class: str


BASELINE_FORM = FunctionalForm(form_id="baseline")


def default_functional_forms() -> tuple[FunctionalForm, ...]:
    """Return the baseline and three declared endpoint-normalized variants."""

    return (
        BASELINE_FORM,
        FunctionalForm(form_id="saturating_attraction", attraction_saturation=1.0),
        FunctionalForm(form_id="saturating_defence", defence_saturation=1.0 / 0.35),
        FunctionalForm(
            form_id="saturating_both_curved_cost",
            attraction_saturation=1.0,
            defence_saturation=1.0 / 0.35,
            joint_cost_curvature=1.0,
        ),
    )


def _sign(value: float, tolerance: float) -> str:
    if not isfinite(value):
        raise ValueError("mixed partial must be finite")
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and non-negative")
    if value > tolerance:
        return "complementary"
    if value < -tolerance:
        return "substitutable"
    return "neutral"


def _attraction_marginal_gain(
    parameters: ModelParameters, attraction: float, form: FunctionalForm
) -> float:
    """Return the derivative of endpoint-normalized attraction benefit."""

    q = form.attraction_saturation
    denominator = 1.0 + q * attraction
    return parameters.attraction_gain * (1.0 + q) / (denominator * denominator)


def _defence_marginal_efficacy(
    parameters: ModelParameters, defence: float, form: FunctionalForm
) -> float:
    """Return the derivative of endpoint-normalized antagonist protection."""

    q = form.defence_saturation
    denominator = 1.0 + q * defence
    return parameters.floral_defence_efficacy * (1.0 + q) / (denominator * denominator)


def _joint_cost_cross_curvature(
    parameters: ModelParameters,
    attraction: float,
    defence: float,
    form: FunctionalForm,
) -> float:
    """Return local C_AD for the endpoint-normalized curved joint-cost family."""

    k = form.joint_cost_curvature
    return parameters.attraction_defence_shared_cost * (
        1.0 + 2.0 * k * (attraction + defence)
    ) / (1.0 + 2.0 * k)


def mixed_partial(
    case: RobustnessCase,
    parameters: ModelParameters,
    form: FunctionalForm = BASELINE_FORM,
    *,
    tolerance: float = 1e-12,
) -> MixedPartialResult:
    """Evaluate the local A×D mixed partial under one response-shape variant."""

    attraction_gain = _attraction_marginal_gain(parameters, case.attraction, form)
    defence_efficacy = _defence_marginal_efficacy(parameters, case.defence, form)
    antagonism_term = (
        case.floral_damage_pressure
        * parameters.attraction_tracking
        * defence_efficacy
    )
    pollination_obstruction_term = (
        case.pollinator_service
        * attraction_gain
        * parameters.defence_pollinator_cost
        * exp(-parameters.defence_pollinator_cost * case.defence)
        * (1.0 - parameters.assurance_outcross_dilution * case.assurance)
    )
    joint_cost_curvature_term = _joint_cost_cross_curvature(
        parameters, case.attraction, case.defence, form
    )
    value = antagonism_term - pollination_obstruction_term - joint_cost_curvature_term
    return MixedPartialResult(
        case_id=case.case_id,
        form_id=form.form_id,
        antagonism_term=antagonism_term,
        pollination_obstruction_term=pollination_obstruction_term,
        joint_cost_curvature_term=joint_cost_curvature_term,
        mixed_partial=value,
        sign=_sign(value, tolerance),
    )


def evaluate_forms(
    case: RobustnessCase,
    parameters: ModelParameters,
    forms: Iterable[FunctionalForm] | None = None,
    *,
    tolerance: float = 1e-12,
) -> tuple[MixedPartialResult, ...]:
    """Evaluate a fixed set of response-shape variants for one regime case."""

    chosen_forms = tuple(forms) if forms is not None else default_functional_forms()
    if not chosen_forms:
        raise ValueError("at least one functional form is required")
    return tuple(
        mixed_partial(case, parameters, form, tolerance=tolerance)
        for form in chosen_forms
    )


def summarise_case(results: Sequence[MixedPartialResult]) -> RobustnessSummary:
    """Summarize sign agreement across a finite tested set for one local case."""

    if not results:
        raise ValueError("cannot summarise an empty result set")
    case_ids = {result.case_id for result in results}
    if len(case_ids) != 1:
        raise ValueError("all results must belong to the same case")
    non_neutral = [result.sign for result in results if result.sign != "neutral"]
    total = len(results)
    if not non_neutral:
        return RobustnessSummary(
            case_id=results[0].case_id,
            modal_sign="neutral",
            non_neutral_form_count=0,
            total_form_count=total,
            modal_sign_agreement=0.0,
            robustness_class="mixed_or_sensitive",
        )
    complementary = non_neutral.count("complementary")
    substitutable = non_neutral.count("substitutable")
    if complementary > substitutable:
        modal_sign = "complementary"
    elif substitutable > complementary:
        modal_sign = "substitutable"
    else:
        modal_sign = "mixed"
    agreement = max(complementary, substitutable) / len(non_neutral)
    has_neutral = len(non_neutral) != total
    robustness = (
        "tested_set_unanimous"
        if agreement == 1.0 and not has_neutral
        else "mixed_or_sensitive"
    )
    return RobustnessSummary(
        case_id=results[0].case_id,
        modal_sign=modal_sign,
        non_neutral_form_count=len(non_neutral),
        total_form_count=total,
        modal_sign_agreement=agreement,
        robustness_class=robustness,
    )


def cartesian_cases(
    *,
    attraction: Iterable[float],
    defence: Iterable[float],
    assurance: Iterable[float],
    pollinator_service: Iterable[float],
    floral_damage_pressure: Iterable[float],
) -> tuple[RobustnessCase, ...]:
    """Build deterministic local cases from a declared parameter grid."""

    cases: list[RobustnessCase] = []
    for index, values in enumerate(
        product(attraction, defence, assurance, pollinator_service, floral_damage_pressure),
        start=1,
    ):
        a, d, r, p, h = values
        cases.append(
            RobustnessCase(
                case_id=f"case_{index:04d}",
                attraction=float(a),
                defence=float(d),
                assurance=float(r),
                pollinator_service=float(p),
                floral_damage_pressure=float(h),
            )
        )
    return tuple(cases)
