"""Project an SCH fitness-scale conflict-budget receipt onto the BITA critical surface.

The structural quadratic boundary is Phi = s * L_S - K. This script consumes a
SCH_COMPONENT_CONFLICT_BUDGET_V1 receipt and a preregistered BITA cost/decoupling
configuration on the SAME fitness scale. It propagates declared 95% intervals
conservatively and fails closed when scales or cost semantics are ambiguous.

Important: local BITA joint-channel curvature (kappa_delta) is not architecture
cost K and is not accepted by this interface.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


SCH_SCHEMA = "SCH_COMPONENT_CONFLICT_BUDGET_V1"
ALLOWED_COST_SEMANTICS = {
    "FUNCTIONAL_STATE_DEPLOYMENT_COST",
    "STRUCTURAL_ARCHITECTURE_MAINTENANCE_COST",
}


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _nonnegative(value: float, name: str) -> float:
    value = _finite(value, name)
    if value < 0:
        raise ValueError(f"{name} must be >= 0")
    return value


def _unit_interval(value: float, name: str) -> float:
    value = _nonnegative(value, name)
    if value > 1:
        raise ValueError(f"{name} must be <= 1")
    return value


def _interval(config: dict, stem: str, validator) -> tuple[float, tuple[float, float]]:
    point = validator(config[stem], stem)
    raw = config.get(f"{stem}_95_ci", [point, point])
    if not isinstance(raw, list) or len(raw) != 2:
        raise ValueError(f"{stem}_95_ci must be a two-element list")
    lo = validator(raw[0], f"{stem}_95_ci[0]")
    hi = validator(raw[1], f"{stem}_95_ci[1]")
    if lo > point or point > hi:
        raise ValueError(f"{stem} must lie inside its 95% interval")
    return point, (lo, hi)


def _sch_budget(receipt: dict) -> tuple[float, tuple[float, float], str]:
    if receipt.get("receipt_schema_version") != SCH_SCHEMA:
        raise ValueError(f"SCH receipt must use schema {SCH_SCHEMA}")
    if receipt.get("status") != "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED":
        raise ValueError("SCH receipt must identify a fitness-scale shared conflict budget")
    scale = str(receipt.get("fitness_scale_id", "")).strip()
    if not scale:
        raise ValueError("SCH receipt lacks fitness_scale_id")
    try:
        point = _nonnegative(receipt["criticality_export"]["L_S_component"], "L_S_component")
        ci_raw = receipt["criticality_export"]["L_S_component_95_ci"]
    except (KeyError, TypeError) as exc:
        raise ValueError("SCH receipt lacks criticality_export conflict budget") from exc
    if not isinstance(ci_raw, list) or len(ci_raw) != 2:
        raise ValueError("L_S_component_95_ci must be a two-element list")
    lo = _nonnegative(ci_raw[0], "L_S_component_95_ci[0]")
    hi = _nonnegative(ci_raw[1], "L_S_component_95_ci[1]")
    if not lo <= point <= hi:
        raise ValueError("SCH conflict-budget point estimate must lie inside its 95% interval")
    return point, (lo, hi), scale


def _classification(lo: float, hi: float) -> str:
    if lo > 0:
        return "DIFFERENTIATED_SIDE_SUPPORTED_ON_DECLARED_SCALE"
    if hi < 0:
        return "SHARED_SIDE_SUPPORTED_ON_DECLARED_SCALE"
    return "CRITICAL_SURFACE_NOT_RESOLVED_WITH_CURRENT_INTERVALS"


def project(sch_receipt: dict, config: dict) -> dict:
    l_point, (l_lo, l_hi), sch_scale = _sch_budget(sch_receipt)

    scale = str(config.get("fitness_scale_id", "")).strip()
    if scale != sch_scale:
        raise ValueError("BITA config fitness_scale_id must exactly match SCH receipt")

    semantics = str(config.get("cost_semantics", "")).strip()
    if semantics not in ALLOWED_COST_SEMANTICS:
        raise ValueError(
            "cost_semantics must be FUNCTIONAL_STATE_DEPLOYMENT_COST or "
            "STRUCTURAL_ARCHITECTURE_MAINTENANCE_COST"
        )
    if "kappa" in str(config.get("cost_source", "")).lower():
        raise ValueError("local kappa/joint-channel cost is not accepted as architecture cost K")

    s_point, (s_lo, s_hi) = _interval(config, "decoupling_fraction", _unit_interval)
    k_point, (k_lo, k_hi) = _interval(config, "architecture_cost", _nonnegative)

    recoverable = s_point * l_point
    margin = recoverable - k_point
    margin_lo = s_lo * l_lo - k_hi
    margin_hi = s_hi * l_hi - k_lo

    if s_point == 0:
        critical_load = 0.0 if k_point == 0 else math.inf
    else:
        critical_load = k_point / s_point

    if l_point == 0:
        critical_s = 0.0 if k_point == 0 else None
    else:
        candidate = k_point / l_point
        critical_s = candidate if candidate <= 1 else None

    architecture_level = semantics == "STRUCTURAL_ARCHITECTURE_MAINTENANCE_COST"
    return {
        "analysis": "sch_conflict_budget_to_bita_critical_surface",
        "critical_surface": "Phi = s*L_S_component - K = 0",
        "fitness_scale_id": scale,
        "cost_semantics": semantics,
        "cost_source": str(config.get("cost_source", "")).strip(),
        "inputs": {
            "L_S_component": l_point,
            "L_S_component_95_ci": [l_lo, l_hi],
            "decoupling_fraction": s_point,
            "decoupling_fraction_95_ci": [s_lo, s_hi],
            "architecture_cost": k_point,
            "architecture_cost_95_ci": [k_lo, k_hi],
        },
        "derived": {
            "recoverable_component_loss": recoverable,
            "critical_shared_conflict_load": critical_load,
            "critical_decoupling_fraction": critical_s,
            "architecture_margin": margin,
            "architecture_margin_conservative_95_bounds": [margin_lo, margin_hi],
        },
        "classification": _classification(margin_lo, margin_hi),
        "claim_level": (
            "ARCHITECTURE_LEVEL_C2_PROJECTION"
            if architecture_level
            else "FUNCTIONAL_STATE_C2_PROJECTION_ONLY"
        ),
        "claim_ceiling": (
            "Structural architecture criticality only when K is an independently justified maintenance/developmental "
            "cost of the differentiated architecture on the same fitness scale. Functional-state deployment cost "
            "supports only a contemporary state-level threshold. Neither is historical modularization."
        ),
        "explicit_non_equivalence": "kappa_delta != K; within_bita_optimum_fitness_gain != independently measured K",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sch_conflict_budget_json", type=Path)
    parser.add_argument("bita_config_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = json.loads(args.sch_conflict_budget_json.read_text(encoding="utf-8"))
    config = json.loads(args.bita_config_json.read_text(encoding="utf-8"))
    result = project(receipt, config)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
