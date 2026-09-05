import math

from trait_architecture.criticality import (
    architecture_margin,
    classify_architecture_margin,
    classify_empirical_release,
    critical_coupling,
    critical_decoupling,
    critical_optimum_distance,
    critical_shared_load,
    criticality_map,
    cross_world_equivalence_statement,
    decoupling_fraction,
    empirical_release_margin,
    shared_conflict_load,
)


def test_reference_case_hits_same_surface_from_cost_and_conflict_coordinates() -> None:
    s = decoupling_fraction(1.0, 1.0, 1.0)
    assert math.isclose(s, 1.0 / 3.0)
    load_crit = critical_shared_load(0.1, s)
    assert math.isclose(load_crit, 0.3)
    dcrit = critical_optimum_distance(0.1, 1.0, 1.0, 1.0)
    assert math.isclose(dcrit, math.sqrt(0.6), rel_tol=1e-12)
    load = shared_conflict_load(dcrit, 1.0, 1.0)
    margin = architecture_margin(load, s, 0.1)
    assert abs(margin) < 1e-12
    assert classify_architecture_margin(margin) == "COMMON_ARCHITECTURE_CRITICAL_SURFACE"


def test_fixed_conflict_distance_gives_lambda_two_as_same_boundary() -> None:
    load = shared_conflict_load(1.0, 1.0, 1.0)
    assert math.isclose(load, 0.5)
    scrit = critical_decoupling(load, 0.1)
    assert math.isclose(scrit, 0.2)
    lcrit = critical_coupling(load, 0.1, 1.0, 1.0)
    assert math.isclose(lcrit, 2.0)
    result = criticality_map(1.0, 1.0, 1.0, 2.0, 0.1)
    assert abs(result.architecture_margin) < 1e-12


def test_architecture_cost_above_full_decoupling_gain_has_no_reachable_s_boundary() -> None:
    load = 0.2
    assert critical_decoupling(load, 0.3) is None
    assert critical_coupling(load, 0.3, 1.0, 1.0) is None


def test_zero_cost_collapses_projected_architecture_load_to_conflict_onset() -> None:
    result = criticality_map(0.0, 1.0, 1.0, 10.0, 0.0)
    assert result.shared_conflict_load == 0.0
    assert result.critical_shared_load == 0.0
    assert result.critical_optimum_distance == 0.0
    assert result.architecture_status == "COMMON_ARCHITECTURE_CRITICAL_SURFACE"


def test_empirical_release_boundary_is_not_relabelled_as_fitness_architecture_boundary() -> None:
    assert empirical_release_margin(1.0, 1.0) == 0.0
    assert classify_empirical_release(0.0) == "EMPIRICAL_RELEASE_CRITICAL_BOUNDARY"
    statement = cross_world_equivalence_statement()
    assert statement["theory_architecture_surface"].startswith("SAME")
    assert statement["sch_intrinsic_conflict_boundary"].startswith("DIFFERENT")
    assert statement["bita_empirical_release_boundary"].startswith("DIFFERENT_UNITS")
    assert statement["current_empirical_equivalence"].startswith("NOT_YET_IDENTIFIED")
