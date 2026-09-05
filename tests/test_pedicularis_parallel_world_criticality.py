from scripts.analyze_pedicularis_parallel_world_criticality import analyze


def _row(cid, e, l, s, k, direct, role="TEST"):
    return {
        "context_id": cid,
        "context_value": str(e),
        "fitness_scale_id": "INTACT_SEEDS_PER_FLOWER",
        "L_S_component": str(l),
        "L_S_lo": str(l),
        "L_S_hi": str(l),
        "release_efficiency": str(s),
        "release_efficiency_lo": str(s),
        "release_efficiency_hi": str(s),
        "architecture_cost": str(k),
        "architecture_cost_lo": str(k),
        "architecture_cost_hi": str(k),
        "projected_parameter_source": "INDEPENDENT_CALIBRATION_PLUS_COST_ASSAY",
        "direct_bita_margin": str(direct),
        "direct_bita_margin_lo": str(direct),
        "direct_bita_margin_hi": str(direct),
        "direct_margin_source": "DIRECT_NET_COMMON_FITNESS_COMPARISON",
        "context_role": role,
    }


def test_same_critical_context_when_projected_and_direct_margins_cross_together() -> None:
    rows = [
        _row("low", 0.0, 0.2, 0.5, 0.2, -0.1),
        _row("high", 2.0, 0.6, 0.5, 0.2, 0.1),
    ]
    result = analyze(rows, {"context_tolerance": 0.05})
    assert result["projected_sch_critical_context"] == 1.0
    assert result["direct_bita_critical_context"] == 1.0
    assert result["classification"] == "SAME_CRITICAL_CONTEXT_COMPATIBLE"


def test_parallel_world_context_when_direct_crossing_is_shifted() -> None:
    rows = [
        _row("low", 0.0, 0.2, 0.5, 0.2, -0.2),
        _row("mid", 1.0, 0.4, 0.5, 0.2, -0.1),
        _row("high", 2.0, 0.6, 0.5, 0.2, 0.1),
    ]
    result = analyze(rows, {"context_tolerance": 0.1})
    assert result["projected_sch_critical_context"] == 1.0
    assert result["direct_bita_critical_context"] == 1.5
    assert result["classification"] == "PARALLEL_WORLD_CRITICAL_CONTEXTS"
