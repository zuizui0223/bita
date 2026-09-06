import math


def recovery(lam1: float, lam2: float) -> float:
    return math.exp(-(lam1 + 2.0 * lam2))


def penalty1(lam1: float, lam2: float) -> float:
    return recovery(lam1, lam2)


def penalty2(lam1: float, lam2: float) -> float:
    return 2.0 * recovery(lam1, lam2)


def test_two_coordinate_paths_have_same_exact_penalty_integral():
    a = 0.7
    b = 0.4

    # Path A: lambda1 first, then lambda2.
    path_a = (1.0 - math.exp(-a)) + math.exp(-a) * (1.0 - math.exp(-2.0 * b))

    # Path B: lambda2 first, then lambda1.
    path_b = (1.0 - math.exp(-2.0 * b)) + math.exp(-2.0 * b) * (1.0 - math.exp(-a))

    endpoint_loss = recovery(0.0, 0.0) - recovery(a, b)
    assert math.isclose(path_a, path_b, rel_tol=1e-12, abs_tol=1e-12)
    assert math.isclose(path_a, endpoint_loss, rel_tol=1e-12, abs_tol=1e-12)


def test_cross_channel_reciprocity():
    lam1 = 0.3
    lam2 = 0.2
    # dc1/dlambda2 = -4 exp(-(lambda1+2lambda2))
    cross_12 = -4.0 * recovery(lam1, lam2)
    # dc2/dlambda1 is the same.
    cross_21 = -4.0 * recovery(lam1, lam2)
    assert math.isclose(cross_12, cross_21, rel_tol=0, abs_tol=1e-15)


def test_active_penalties_decline_with_own_coupling():
    eps = 1e-6
    lam1 = 0.4
    lam2 = 0.25
    dc1 = (penalty1(lam1 + eps, lam2) - penalty1(lam1 - eps, lam2)) / (2 * eps)
    dc2 = (penalty2(lam1, lam2 + eps) - penalty2(lam1, lam2 - eps)) / (2 * eps)
    assert dc1 < 0
    assert dc2 < 0
