import math


def shared_loss(a: float, b: float, d: float) -> float:
    return (a * b / (a + b)) * d * d


def recovery(a: float, b: float, d: float, lam: float) -> float:
    return (a * a * b * b * d * d) / ((a + b) * (a * b + lam * (a + b)))


def separation(a: float, b: float, d: float, lam: float) -> float:
    return (a * b / (a * b + lam * (a + b))) * d


def critical_lambda(a: float, b: float, d: float, K: float) -> float:
    L = shared_loss(a, b, d)
    if not (0.0 < K < L):
        raise ValueError("quadratic finite critical coupling requires 0<K<L")
    return (a * b * (L - K)) / (K * (a + b))


def test_recovery_is_nonnegative_decreasing_and_convex_in_lambda():
    a, b, d = 1.7, 0.8, 2.3
    grid = [0.0, 0.2, 0.7, 1.5, 3.0, 7.0]
    values = [recovery(a, b, d, lam) for lam in grid]
    assert all(value >= 0 for value in values)
    assert all(values[i + 1] <= values[i] for i in range(len(values) - 1))

    # Convexity: midpoint recovery cannot exceed the chord midpoint.
    for left, right in zip(grid[:-2], grid[2:]):
        mid = 0.5 * (left + right)
        chord = 0.5 * (recovery(a, b, d, left) + recovery(a, b, d, right))
        assert recovery(a, b, d, mid) <= chord + 1e-12


def test_envelope_derivative_equals_negative_active_coupling_penalty():
    a, b, d, lam = 1.7, 0.8, 2.3, 1.4
    eps = 1e-6
    derivative = (
        recovery(a, b, d, lam + eps) - recovery(a, b, d, lam - eps)
    ) / (2 * eps)
    active_penalty = separation(a, b, d, lam) ** 2
    assert abs(derivative + active_penalty) < 2e-7


def test_stronger_architecture_cost_lowers_critical_coupling():
    a, b, d = 1.3, 1.1, 2.0
    L = shared_loss(a, b, d)
    k1 = 0.2 * L
    k2 = 0.5 * L
    lam1 = critical_lambda(a, b, d, k1)
    lam2 = critical_lambda(a, b, d, k2)
    assert lam2 < lam1
    assert abs(recovery(a, b, d, lam1) - k1) < 1e-12
    assert abs(recovery(a, b, d, lam2) - k2) < 1e-12


def test_strong_coupling_limit_recovers_shared_constraint():
    a, b, d = 1.3, 1.1, 2.0
    assert recovery(a, b, d, 1e9) < 1e-8
    assert math.isclose(recovery(a, b, d, 0.0), shared_loss(a, b, d), rel_tol=1e-12)
