"""Project the shared three-world SCH conflict handoff onto BITA.

This wrapper preserves the existing SCH_COMPONENT_CONFLICT_BUDGET_V1 -> BITA
projection while adding exact biological-context identity.  It fails closed if
BITA attempts to combine a different context or fitness scale.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.project_sch_conflict_budget_into_bita import project


HANDOFF_SCHEMA = "THREE_WORLD_CONFLICT_HANDOFF_V1"


def _required_text(value: object, name: str) -> str:
    out = str(value).strip()
    if not out or out == "REQUIRED_BEFORE_USE":
        raise ValueError(f"{name} must be frozen before use")
    return out


def project_handoff(handoff: dict, config: dict) -> dict:
    if handoff.get("receipt_schema_version") != HANDOFF_SCHEMA:
        raise ValueError(f"handoff must use {HANDOFF_SCHEMA}")
    if handoff.get("status") != "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED":
        raise ValueError("handoff status is not positive")

    context_id = _required_text(handoff.get("context_id"), "handoff context_id")
    config_context = _required_text(config.get("context_id"), "BITA context_id")
    if context_id != config_context:
        raise ValueError("BITA context_id must exactly match the SCH/BALANCE handoff")

    scale = _required_text(handoff.get("fitness_scale_id"), "handoff fitness_scale_id")
    config_scale = _required_text(config.get("fitness_scale_id"), "BITA fitness_scale_id")
    if scale != config_scale:
        raise ValueError("BITA fitness_scale_id must exactly match the SCH/BALANCE handoff")

    raw = handoff.get("conflict_load", {})
    try:
        point = float(raw["point"])
        lo = float(raw["lower_95"])
        hi = float(raw["upper_95"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("handoff lacks a valid conflict_load") from exc

    legacy_compatible = {
        "receipt_schema_version": "SCH_COMPONENT_CONFLICT_BUDGET_V1",
        "status": "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED",
        "fitness_scale_id": scale,
        "criticality_export": {
            "L_S_component": point,
            "L_S_component_95_ci": [lo, hi],
        },
    }
    result = project(legacy_compatible, config)
    result["three_world_handoff"] = {
        "receipt_schema_version": HANDOFF_SCHEMA,
        "context_id": context_id,
        "system": _required_text(handoff.get("system"), "system"),
        "population_id": _required_text(handoff.get("population_id"), "population_id"),
        "season_id": _required_text(handoff.get("season_id"), "season_id"),
        "fitness_scale_id": scale,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("three_world_handoff_json", type=Path)
    parser.add_argument("bita_config_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    handoff = json.loads(args.three_world_handoff_json.read_text(encoding="utf-8"))
    config = json.loads(args.bita_config_json.read_text(encoding="utf-8"))
    result = project_handoff(handoff, config)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
