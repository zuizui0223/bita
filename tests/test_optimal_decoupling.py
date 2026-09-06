import math

from trait_architecture.optimal_decoupling import (
    best_single_channel,
    joint_diagonal_robustness,
    optimal_diagonal_decoupling,
)


def test_optimal_decoupling_uses_penalty_over_cost_geometry():
    plan = optimal_diagonal_decoupling(
        active_penalties=(3.0, 4.0),
        metric_diag=(1.0, 4.0),
        budget=2.0,
    )
    dual_norm = math.sqrt(9.0 + 4.0)
    assert math.isclose(plan.dual_penalty_norm, dual_norm, rel_tol=1e-12)
    assert math.isclose(plan.first_order_gain, 2.0 * dual_norm, rel_tol=1e-12)

    metric_cost = plan.direction[0] ** 2 + 4.0 * plan.direction[1] ** 2
    assert math.isclose(metric_cost, 4.0, rel_tol=1e-12)
    assert all(x <= 0 for x in plan.direction)


def test_best_single_channel_uses_c_over_sqrt_q():
    # Raw penalty is larger on channel 2, but channel 1 is cheaper enough to win.
    assert best_single_channel((3.0, 4.0), (1.0, 4.0)) == 0


def test_joint_robustness_reaches_linearized_boundary():
    margin = 5.0
    penalties = (3.0, 4.0)
    metric = (1.0, 4.0)
    result = joint_diagonal_robustness(
        margin=margin,
        active_penalties=penalties,
        coupling_metric_diag=metric,
        cost_metric_weight=1.0,
    )

    # Linearized adverse margin loss is c dot delta_lambda + delta_K = margin.
    loss = sum(c * d for c, d in zip(penalties, result.coupling_shift)) + result.cost_shift
    assert math.isclose(loss, margin, rel_tol=1e-12)

    metric_cost = sum(q * d * d for q, d in zip(metric, result.coupling_shift)) + result.cost_shift**2
    assert math.isclose(math.sqrt(metric_cost), result.distance, rel_tol=1e-12)
