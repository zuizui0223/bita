"""Compare projected SCH-side and direct BITA critical contexts in Pedicularis.

The projected margin is release_efficiency * L_S_component - architecture_cost.
To keep the comparison non-circular in TEST contexts, release efficiency and cost
must be marked as independently calibrated/assayed. The direct BITA margin must
come from a net common-fitness comparison and may not be reused to define the
projected parameters in the same test context.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from trait_architecture.critical_context import compare_critical_contexts


FIELDS = (
    "context_id",
    "context_value",
    "fitness_scale_id",
    "L_S_component",
    "L_S_lo",
    "L_S_hi",
    "release_efficiency",
    "release_efficiency_lo",
    "release_efficiency_hi",
    "architecture_cost",
    "architecture_cost_lo",
    "architecture_cost_hi",
    "projected_parameter_source",
    "direct_bita_margin",
    "direct_bita_margin_lo",
    "direct_bita_margin_hi",
    "direct_margin_source",
    "context_role",
)

ALLOWED_ROLES = {"CALIBRATION", "TEST"}
REQUIRED_PROJECTED_SOURCE_TEST = "INDEPENDENT_CALIBRATION_PLUS_COST_ASSAY"
REQUIRED_DIRECT_SOURCE_TEST = "DIRECT_NET_COMMON_FITNESS_COMPARISON"


def _num(row: dict[str, str], field: str) -> float:
    try:
        return float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"invalid {field}: {row.get(field)!r}") from exc


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError(f"columns must be exactly {FIELDS!r}")
        rows = list(reader)
    if not rows:
        raise ValueError("no context rows")
    scale_ids = {row["fitness_scale_id"].strip() for row in rows}
    if len(scale_ids) != 1 or "" in scale_ids:
        raise ValueError("all contexts must use one non-empty fitness_scale_id")
    seen = set()
    for row in rows:
        cid = row["context_id"].strip()
        if not cid or cid in seen:
            raise ValueError("context_id values must be unique and non-empty")
        seen.add(cid)
        role = row["context_role"].strip()
        if role not in ALLOWED_ROLES:
            raise ValueError("context_role must be CALIBRATION or TEST")
        for field in (
            "context_value",
            "L_S_component",
            "L_S_lo",
            "L_S_hi",
            "release_efficiency",
            "release_efficiency_lo",
            "release_efficiency_hi",
            "architecture_cost",
            "architecture_cost_lo",
            "architecture_cost_hi",
            "direct_bita_margin",
            "direct_bita_margin_lo",
            "direct_bita_margin_hi",
        ):
            _num(row, field)
        if not 0 <= _num(row, "release_efficiency") <= 1:
            raise ValueError("release_efficiency must lie in [0,1]")
        if role == "TEST":
            if row["projected_parameter_source"].strip() != REQUIRED_PROJECTED_SOURCE_TEST:
                raise ValueError("TEST projected parameters must come from independent calibration plus cost assay")
            if row["direct_margin_source"].strip() != REQUIRED_DIRECT_SOURCE_TEST:
                raise ValueError("TEST direct margin must be a direct net common-fitness comparison")
    return rows


def analyze(rows: list[dict[str, str]], config: dict) -> dict:
    test = [row for row in rows if row["context_role"].strip() == "TEST"]
    if len(test) < 2:
        raise ValueError("at least two TEST contexts are required")

    projected_points = []
    direct_points = []
    context_details = []
    for row in test:
        e = _num(row, "context_value")
        l = _num(row, "L_S_component")
        s = _num(row, "release_efficiency")
        k = _num(row, "architecture_cost")
        projected = s * l - k
        direct = _num(row, "direct_bita_margin")
        projected_points.append((e, projected))
        direct_points.append((e, direct))
        context_details.append(
            {
                "context_id": row["context_id"],
                "context_value": e,
                "projected_sch_margin": projected,
                "direct_bita_margin": direct,
                "margin_discrepancy": direct - projected,
            }
        )

    comparison = compare_critical_contexts(
        projected_points,
        direct_points,
        context_tolerance=float(config["context_tolerance"]),
        zero_tolerance=float(config.get("zero_tolerance", 1e-12)),
    )
    return {
        "analysis": "pedicularis_parallel_world_criticality",
        "fitness_scale_id": test[0]["fitness_scale_id"].strip(),
        "projected_sch_critical_context": comparison.sch_crossing.context,
        "direct_bita_critical_context": comparison.bita_crossing.context,
        "delta_e_c": comparison.delta_context,
        "absolute_delta_e_c": comparison.absolute_delta_context,
        "context_tolerance": comparison.tolerance,
        "classification": comparison.classification,
        "test_contexts": context_details,
        "identification_contract": {
            "projected_parameters": REQUIRED_PROJECTED_SOURCE_TEST,
            "direct_margin": REQUIRED_DIRECT_SOURCE_TEST,
            "same_population_season_requirement": True,
            "noncircular_sch_antagonist_requirement": True,
        },
        "claim_ceiling": (
            "same-versus-parallel contemporary functional-state critical context; "
            "not structural architecture origin and not historical modularization"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contexts_csv", type=Path)
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = read_rows(args.contexts_csv)
    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    result = analyze(rows, config)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
