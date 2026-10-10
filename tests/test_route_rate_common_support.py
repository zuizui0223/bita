from scripts.diagnose_route_retention_poisson_mle_existence import Cell
from scripts.audit_route_rate_common_support import prune_route, prune_joint


def cell(waypoint, bird, robbery, legitimate):
    return Cell(waypoint=waypoint, bird=bird, site="s", plant=waypoint,
                category=0, robbery=robbery, legitimate=legitimate)


def test_route_positive_margins_not_a_common_risk_set():
    edges = [
        cell("w1", "a", 1, 1),
        cell("w1", "b", 0, 1),
        cell("w2", "a", 1, 0),
        cell("w2", "b", 0, 0),
    ]
    robbery = prune_route(edges, "robbery")
    legitimate = prune_route(edges, "legitimate")
    assert len(robbery) == 2
    assert len(legitimate) == 2
    assert len(set(map(id, robbery)) & set(map(id, legitimate))) == 1
    jointly, iterations = prune_joint(edges)
    assert len(jointly) == 1
    assert jointly[0].waypoint == "w1"
    assert jointly[0].bird == "a"
    assert iterations >= 2


def test_joint_pruning_is_already_stable_when_all_routes_positive():
    edges = [cell("w1","a",1,2),cell("w1","b",3,1)]
    jointly, iterations = prune_joint(edges)
    assert len(jointly) == len(edges)
    assert iterations == 1
