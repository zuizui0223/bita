from dataclasses import dataclass


@dataclass(frozen=True)
class CouplingRobustnessBound:
    net_margin: float
    active_coupling_penalty: float
    minimum_extra_coupling_to_crossing: float | None
    later_crossing_possible_under_model: bool


def coupling_robustness_bound(*, net_margin: float, active_coupling_penalty: float) -> CouplingRobustnessBound:
    if net_margin <= 0:
        raise ValueError("net_margin must be positive for a differentiation-favored starting point")
    if active_coupling_penalty < 0:
        raise ValueError("active_coupling_penalty must be nonnegative")

    if active_coupling_penalty == 0:
        return CouplingRobustnessBound(
            net_margin=net_margin,
            active_coupling_penalty=active_coupling_penalty,
            minimum_extra_coupling_to_crossing=None,
            later_crossing_possible_under_model=False,
        )

    return CouplingRobustnessBound(
        net_margin=net_margin,
        active_coupling_penalty=active_coupling_penalty,
        minimum_extra_coupling_to_crossing=net_margin / active_coupling_penalty,
        later_crossing_possible_under_model=True,
    )


def critical_coupling_cost_derivatives(*, recovery_first: float, recovery_second: float) -> tuple[float, float]:
    """Return d lambda_c / dK and d2 lambda_c / dK2 at a regular crossing."""
    if recovery_first >= 0:
        raise ValueError("recovery_first must be negative at a strictly decreasing crossing")
    if recovery_second < 0:
        raise ValueError("recovery_second must be nonnegative for convex recovery")
    first = 1.0 / recovery_first
    second = -recovery_second / (recovery_first ** 3)
    return first, second
