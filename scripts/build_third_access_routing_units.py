"""Build prospective third-network confirmatory analysis units.

The builder is the only supported path from event/morphology tables to the
frozen third-network analysis CSV. It rejects pilot events rather than silently
dropping them, preserving the preregistered pilot/confirmatory split.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

ALLOWED_ROUTE_CODES = {"L", "B", "A", "N"}
ANALYSIS_ROUTE_CODES = {"L", "B"}
ALLOWED_ID_CONFIDENCE = {"HIGH", "MEDIUM"}


def _read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _require_columns(rows: list[dict[str, str]], columns: set[str], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} table is empty")
    missing = columns.difference(rows[0].keys())
    if missing:
        raise ValueError(f"{label} missing required columns: {sorted(missing)}")


def _positive_float(value: str, label: str) -> float:
    number = float(str(value).strip())
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{label} must be positive and finite")
    return number


def _median_map(
    rows: list[dict[str, str]],
    *,
    key_fields: tuple[str, ...],
    value_field: str,
    label: str,
) -> dict[tuple[str, ...], float]:
    grouped: dict[tuple[str, ...], list[float]] = defaultdict(list)
    for row in rows:
        key = tuple(str(row[field]).strip() for field in key_fields)
        if not all(key):
            raise ValueError(f"{label} has blank key field")
        grouped[key].append(_positive_float(row[value_field], f"{label}.{value_field}"))
    return {key: float(statistics.median(values)) for key, values in grouped.items()}


def build_units(
    events: list[dict[str, str]],
    plant_traits: list[dict[str, str]],
    mammal_traits: list[dict[str, str]],
) -> tuple[list[dict[str, object]], dict[str, int]]:
    _require_columns(
        events,
        {
            "event_id",
            "dataset_role",
            "site_id",
            "plant_species",
            "mammal_species",
            "route_code",
            "visitor_id_confidence",
            "clip_quality",
        },
        "events",
    )
    _require_columns(
        plant_traits,
        {"site_id", "plant_species", "access_depth_mm"},
        "plant_traits",
    )
    _require_columns(
        mammal_traits,
        {"mammal_species", "rostral_reach_mm"},
        "mammal_traits",
    )

    roles = {str(row["dataset_role"]).strip().upper() for row in events}
    if roles != {"CONFIRMATORY"}:
        raise ValueError(
            "PILOT_OR_NONCONFIRMATORY_EVENT_SUPPLIED: "
            "confirmatory builder accepts dataset_role=CONFIRMATORY only"
        )

    event_ids = [str(row["event_id"]).strip() for row in events]
    if any(not event_id for event_id in event_ids):
        raise ValueError("event_id must not be blank")
    if len(event_ids) != len(set(event_ids)):
        raise ValueError("event_id must be unique")

    plant_depth = _median_map(
        plant_traits,
        key_fields=("site_id", "plant_species"),
        value_field="access_depth_mm",
        label="plant_traits",
    )
    mammal_reach = _median_map(
        mammal_traits,
        key_fields=("mammal_species",),
        value_field="rostral_reach_mm",
        label="mammal_traits",
    )

    counts: dict[tuple[str, str, str], dict[str, int]] = defaultdict(
        lambda: {"B": 0, "L": 0}
    )
    audit = {
        "events_supplied": len(events),
        "events_low_identity_excluded": 0,
        "events_quality_excluded": 0,
        "events_ambiguous_or_nonnectar_excluded": 0,
        "events_analysis_routes": 0,
        "events_unmatched_morphology": 0,
    }

    for row in events:
        route = str(row["route_code"]).strip().upper()
        if route not in ALLOWED_ROUTE_CODES:
            raise ValueError(f"invalid route_code: {route!r}")

        confidence = str(row["visitor_id_confidence"]).strip().upper()
        if confidence not in {"HIGH", "MEDIUM", "LOW"}:
            raise ValueError(f"invalid visitor_id_confidence: {confidence!r}")
        if confidence not in ALLOWED_ID_CONFIDENCE:
            audit["events_low_identity_excluded"] += 1
            continue

        quality = str(row["clip_quality"]).strip().upper()
        if quality not in {"PASS", "FAIL"}:
            raise ValueError(f"invalid clip_quality: {quality!r}")
        if quality != "PASS":
            audit["events_quality_excluded"] += 1
            continue

        if route not in ANALYSIS_ROUTE_CODES:
            audit["events_ambiguous_or_nonnectar_excluded"] += 1
            continue

        site = str(row["site_id"]).strip()
        plant = str(row["plant_species"]).strip()
        mammal = str(row["mammal_species"]).strip()
        if not site or not plant or not mammal:
            raise ValueError("site_id, plant_species and mammal_species must not be blank")

        if (site, plant) not in plant_depth or (mammal,) not in mammal_reach:
            audit["events_unmatched_morphology"] += 1
            continue

        counts[(site, plant, mammal)][route] += 1
        audit["events_analysis_routes"] += 1

    units: list[dict[str, object]] = []
    for site, plant, mammal in sorted(counts):
        b = counts[(site, plant, mammal)]["B"]
        l = counts[(site, plant, mammal)]["L"]
        if b + l <= 0:
            continue
        p_j = plant_depth[(site, plant)]
        v_i = mammal_reach[(mammal,)]
        m = math.log(p_j / v_i)
        units.append(
            {
                "site_id": site,
                "plant_species": plant,
                "mammal_species": mammal,
                "P_j_mm": p_j,
                "V_i_mm": v_i,
                "M_log_ratio": m,
                "B_count": b,
                "L_count": l,
                "Y_bypass_prop": b / (b + l),
            }
        )

    audit["analysis_units"] = len(units)
    audit["plant_site_trait_units"] = len(plant_depth)
    audit["mammal_trait_species"] = len(mammal_reach)

    if not units:
        raise ValueError("no confirmatory L/B analysis units after frozen exclusions")

    return units, audit


def write_units(path: str | Path, rows: list[dict[str, object]]) -> None:
    fields = [
        "site_id",
        "plant_species",
        "mammal_species",
        "P_j_mm",
        "V_i_mm",
        "M_log_ratio",
        "B_count",
        "L_count",
        "Y_bypass_prop",
    ]
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(
    events_csv: str | Path,
    plant_traits_csv: str | Path,
    mammal_traits_csv: str | Path,
    output_csv: str | Path,
    audit_json: str | Path,
) -> dict[str, int]:
    units, audit = build_units(
        _read_csv(events_csv),
        _read_csv(plant_traits_csv),
        _read_csv(mammal_traits_csv),
    )
    write_units(output_csv, units)
    audit_path = Path(audit_json)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("events_csv")
    parser.add_argument("plant_traits_csv")
    parser.add_argument("mammal_traits_csv")
    parser.add_argument("output_csv")
    parser.add_argument("audit_json")
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.events_csv,
                args.plant_traits_csv,
                args.mammal_traits_csv,
                args.output_csv,
                args.audit_json,
            ),
            indent=2,
            sort_keys=True,
        )
    )
