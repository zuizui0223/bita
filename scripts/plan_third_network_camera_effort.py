"""Route-blind camera-effort planner for the prospective third network.

The planner is deliberately separated from the access-routing outcome.

Input rows contain only:
- site identity;
- plant identity;
- mammal identity;
- route-blind mammal detection rate per camera-hour.

No L/B route label, bypass proportion, access mismatch, or morphology value is
accepted. Every candidate plant x site receives the same planned camera-hours;
the rates are used only to estimate whether a uniform effort rule is likely to
yield enough realized mammal x plant x site units.

Planning model
--------------
For one candidate unit with route-blind detection rate lambda and a predeclared
qualifying fraction q, classifiable-event arrivals are approximated as Poisson
with rate lambda*q. One exponential waiting time is drawn per simulation/unit.
Using common waiting times across the hours grid makes simulated coverage
monotone with increasing effort.

This is a planning approximation, not the confirmatory analysis.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from pathlib import Path

from trait_architecture.serialization import canonicalize_generated_floats

SEED = 20260924
MIN_UNITS = 30
MIN_VISITOR_SPECIES = 5
MIN_PLANT_SPECIES = 5
PLANNING_TARGET_UNITS = 70

EXPECTED_COLUMNS = (
    "site_id",
    "plant_species",
    "mammal_species",
    "route_blind_detection_rate_per_camera_hour",
)

BANNED_COLUMN_TOKENS = (
    "route",
    "bypass",
    "legitimate",
    "robbery",
    "thiev",
    "mismatch",
    "access_depth",
    "rostr",
    "tongue",
    "snout",
    "m_log",
    "y_",
    "b_count",
    "l_count",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _keyset_sha256(keys: set[tuple[str, ...]]) -> str:
    payload = "\n".join("\t".join(key) for key in sorted(keys)) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _rate(value: str) -> float:
    number = float(str(value).strip())
    if not math.isfinite(number) or number < 0:
        raise ValueError(
            "route_blind_detection_rate_per_camera_hour must be finite and non-negative"
        )
    return number


def load_rates(path: str | Path) -> list[dict[str, object]]:
    source = Path(path)
    with source.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = tuple(reader.fieldnames or ())
        if fields != EXPECTED_COLUMNS:
            lowered = [field.lower() for field in fields]
            leaked = [
                field
                for field in lowered
                if any(token in field for token in BANNED_COLUMN_TOKENS)
                and field != "route_blind_detection_rate_per_camera_hour"
            ]
            if leaked:
                raise ValueError(
                    "OUTCOME_OR_MORPHOLOGY_COLUMN_FORBIDDEN_IN_EFFORT_PLANNER: "
                    + ",".join(leaked)
                )
            raise ValueError(
                "effort-rate table must contain exactly: "
                + ",".join(EXPECTED_COLUMNS)
            )

        rows: list[dict[str, object]] = []
        seen: set[tuple[str, str, str]] = set()
        for raw in reader:
            site = str(raw["site_id"]).strip()
            plant = str(raw["plant_species"]).strip()
            mammal = str(raw["mammal_species"]).strip()
            if not site or not plant or not mammal:
                raise ValueError(
                    "site_id, plant_species and mammal_species must be nonblank"
                )
            key = (site, plant, mammal)
            if key in seen:
                raise ValueError(
                    "duplicate site x plant x mammal unit in effort-rate table"
                )
            seen.add(key)
            rows.append(
                {
                    "site": site,
                    "plant": plant,
                    "mammal": mammal,
                    "rate": _rate(
                        raw["route_blind_detection_rate_per_camera_hour"]
                    ),
                }
            )

    if not rows:
        raise ValueError("effort-rate table is empty")
    return rows


def _quantile(values: list[int], probability: float) -> int:
    if not values:
        raise ValueError("quantile requires values")
    ordered = sorted(values)
    index = int(round((len(ordered) - 1) * probability))
    return ordered[max(0, min(index, len(ordered) - 1))]


def _validate_hours(hours_grid: list[float]) -> list[float]:
    if not hours_grid:
        raise ValueError("hours_grid must not be empty")
    hours = sorted(set(float(value) for value in hours_grid))
    if any(not math.isfinite(value) or value <= 0 for value in hours):
        raise ValueError("camera-hour values must be positive and finite")
    return hours


def plan_effort(
    rows: list[dict[str, object]],
    *,
    hours_grid: list[float],
    qualifying_fraction: float,
    simulations: int = 5000,
    seed: int = SEED,
    target_success_probability: float = 0.80,
    camera_count: int | None = None,
) -> dict[str, object]:
    hours = _validate_hours(hours_grid)
    q = float(qualifying_fraction)
    if not math.isfinite(q) or not (0 < q <= 1):
        raise ValueError("qualifying_fraction must be in (0, 1]")
    if simulations <= 0:
        raise ValueError("simulations must be positive")
    threshold = float(target_success_probability)
    if not math.isfinite(threshold) or not (0 < threshold <= 1):
        raise ValueError("target_success_probability must be in (0, 1]")
    if camera_count is not None and camera_count <= 0:
        raise ValueError("camera_count must be positive when supplied")

    normalized: list[tuple[str, str, str, float]] = []
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        site = str(row["site"]).strip()
        plant = str(row["plant"]).strip()
        mammal = str(row["mammal"]).strip()
        rate = float(row["rate"])
        if not site or not plant or not mammal:
            raise ValueError("planning rows require nonblank site/plant/mammal")
        if not math.isfinite(rate) or rate < 0:
            raise ValueError("planning rates must be finite and non-negative")
        key = (site, plant, mammal)
        if key in seen:
            raise ValueError("duplicate planning unit")
        seen.add(key)
        normalized.append((site, plant, mammal, rate))

    positive = [row for row in normalized if row[3] > 0]
    candidate_visitors = {row[2] for row in positive}
    candidate_plants = {row[1] for row in positive}
    deployments = {(row[0], row[1]) for row in normalized}
    candidate_units = {(row[0], row[1], row[2]) for row in normalized}
    deployment_set_sha256 = _keyset_sha256(deployments)
    candidate_unit_set_sha256 = _keyset_sha256(candidate_units)

    structural_minimum_possible = (
        len(positive) >= MIN_UNITS
        and len(candidate_visitors) >= MIN_VISITOR_SPECIES
        and len(candidate_plants) >= MIN_PLANT_SPECIES
    )
    structural_target_possible = (
        len(positive) >= PLANNING_TARGET_UNITS
        and len(candidate_visitors) >= MIN_VISITOR_SPECIES
        and len(candidate_plants) >= MIN_PLANT_SPECIES
    )

    # Common random numbers across the complete hours grid guarantee that
    # simulated realization can only increase with additional camera effort.
    rng = random.Random(seed)
    waiting_times: list[list[float]] = []
    for _ in range(simulations):
        waits: list[float] = []
        for _site, _plant, _mammal, rate in normalized:
            effective = rate * q
            if effective <= 0:
                waits.append(math.inf)
                continue
            u = 1.0 - rng.random()
            # random() is in [0,1); therefore u is in (0,1].
            waits.append(-math.log(u) / effective)
        waiting_times.append(waits)

    grid: list[dict[str, object]] = []
    for camera_hours in hours:
        unit_counts: list[int] = []
        minimum_successes = 0
        target_successes = 0

        for waits in waiting_times:
            detected_indices = [
                index
                for index, wait in enumerate(waits)
                if wait <= camera_hours
            ]
            units = len(detected_indices)
            visitors = {
                normalized[index][2]
                for index in detected_indices
            }
            plants = {
                normalized[index][1]
                for index in detected_indices
            }

            minimum_ok = (
                units >= MIN_UNITS
                and len(visitors) >= MIN_VISITOR_SPECIES
                and len(plants) >= MIN_PLANT_SPECIES
            )
            target_ok = (
                units >= PLANNING_TARGET_UNITS
                and len(visitors) >= MIN_VISITOR_SPECIES
                and len(plants) >= MIN_PLANT_SPECIES
            )
            minimum_successes += int(minimum_ok)
            target_successes += int(target_ok)
            unit_counts.append(units)

        total_camera_hours = camera_hours * len(deployments)
        row: dict[str, object] = {
            "uniform_camera_hours_per_plant_site": camera_hours,
            "distinct_plant_site_deployments": len(deployments),
            "total_equivalent_camera_hours": total_camera_hours,
            "minimum_gate_success_probability": minimum_successes / simulations,
            "planning_target_success_probability": target_successes / simulations,
            "realized_units_mean": sum(unit_counts) / simulations,
            "realized_units_median": _quantile(unit_counts, 0.50),
            "realized_units_q10": _quantile(unit_counts, 0.10),
            "realized_units_q90": _quantile(unit_counts, 0.90),
        }
        if camera_count is not None:
            row["approx_elapsed_hours_at_camera_count"] = (
                total_camera_hours / camera_count
            )
        grid.append(row)

    recommended = next(
        (
            row
            for row in grid
            if float(row["planning_target_success_probability"]) >= threshold
        ),
        None,
    )

    result = {
        "receipt": "BITA_THIRD_NETWORK_CAMERA_EFFORT_PLAN_V1",
        "status": (
            "PLANNING_TARGET_EFFORT_IDENTIFIED"
            if recommended is not None
            else (
                "PLANNING_TARGET_STRUCTURALLY_IMPOSSIBLE"
                if not structural_target_possible
                else "PLANNING_TARGET_NOT_REACHED_IN_HOURS_GRID"
            )
        ),
        "route_blind_contract": {
            "uses_route_outcome": False,
            "uses_access_mismatch": False,
            "uses_morphology": False,
            "effort_allocation": "uniform_camera_hours_per_plant_x_site",
        },
        "model": {
            "arrival_process": "Poisson_planning_approximation",
            "qualifying_fraction": q,
            "qualifying_fraction_source_rule": (
                "predeclared sensitivity/technical assumption; never estimated "
                "from confirmatory B/L direction"
            ),
            "simulations": simulations,
            "seed": seed,
            "target_success_probability": threshold,
        },
        "frozen_gates": {
            "minimum_units": MIN_UNITS,
            "minimum_visitor_species": MIN_VISITOR_SPECIES,
            "minimum_plant_species": MIN_PLANT_SPECIES,
            "planning_target_units": PLANNING_TARGET_UNITS,
        },
        "candidate_structure": {
            "candidate_units": len(normalized),
            "positive_rate_candidate_units": len(positive),
            "candidate_visitor_species": len(candidate_visitors),
            "candidate_plant_species": len(candidate_plants),
            "distinct_plant_site_deployments": len(deployments),
            "plant_site_deployment_set_sha256": deployment_set_sha256,
            "candidate_unit_set_sha256": candidate_unit_set_sha256,
            "minimum_gate_structurally_possible": structural_minimum_possible,
            "planning_target_structurally_possible": structural_target_possible,
        },
        "hours_grid": grid,
        "recommended_uniform_effort": recommended,
        "claim_boundary": (
            "This planner selects a fixed uniform camera-effort rule using only "
            "route-blind detection rates and a predeclared qualifying fraction. "
            "It is not the confirmatory analysis, does not estimate r_T, and "
            "cannot adapt effort to B/L direction or significance."
        ),
    }
    return canonicalize_generated_floats(result)


def run(
    input_csv: str | Path,
    output_json: str | Path,
    *,
    hours_grid: list[float],
    qualifying_fraction: float,
    simulations: int = 5000,
    seed: int = SEED,
    target_success_probability: float = 0.80,
    camera_count: int | None = None,
) -> dict[str, object]:
    source = Path(input_csv)
    rows = load_rates(source)
    result = plan_effort(
        rows,
        hours_grid=hours_grid,
        qualifying_fraction=qualifying_fraction,
        simulations=simulations,
        seed=seed,
        target_success_probability=target_success_probability,
        camera_count=camera_count,
    )
    result["input"] = {
        "filename": source.name,
        "sha256": _sha256(source),
    }

    path = Path(output_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def _hours_arg(value: str) -> list[float]:
    try:
        return [float(token.strip()) for token in value.split(",") if token.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "--hours-grid must be comma-separated numbers"
        ) from exc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_json")
    parser.add_argument("--hours-grid", type=_hours_arg, required=True)
    parser.add_argument("--qualifying-fraction", type=float, required=True)
    parser.add_argument("--simulations", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--target-success-probability", type=float, default=0.80)
    parser.add_argument("--camera-count", type=int)
    args = parser.parse_args()

    print(
        json.dumps(
            run(
                args.input_csv,
                args.output_json,
                hours_grid=args.hours_grid,
                qualifying_fraction=args.qualifying_fraction,
                simulations=args.simulations,
                seed=args.seed,
                target_success_probability=args.target_success_probability,
                camera_count=args.camera_count,
            ),
            indent=2,
            sort_keys=True,
        )
    )
