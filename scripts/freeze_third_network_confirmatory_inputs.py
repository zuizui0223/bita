"""Freeze prospective third-network confirmatory inputs before integration.

The route event table, plant morphology table, mammal morphology table, and
camera deployment table are independently completed before this script is run.
This script validates their frozen contracts, verifies field readiness, and
writes SHA256 receipts. The downstream unit builder must verify this manifest
before joining route outcomes to morphology.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

from scripts.evaluate_third_network_field_readiness import (
    SCHEMA as FIELD_READINESS_SCHEMA,
    READY_STATUS as FIELD_READY_STATUS,
)
from scripts.validate_third_network_confirmatory_freeze import validate as validate_confirmatory_freeze

RECEIPT = "BITA_THIRD_NETWORK_INPUT_FREEZE_V1"
READY_STATUS = "INPUTS_FROZEN_READY_FOR_JOIN"
ALLOWED_ROUTE_CODES = {"L", "B", "A", "N"}
ALLOWED_ID_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}
ALLOWED_CLIP_QUALITY = {"PASS", "FAIL"}
REQUIRED_FIELD_READINESS_GATES = {
    "site_locations_verified_privately",
    "route_blind_presurvey_checksum_matches",
    "route_blind_presurvey_receipt_type_valid",
    "route_blind_presurvey_ready",
    "route_and_morphology_fields_absent_from_presurvey",
    "final_sites_supported_by_route_blind_presurvey",
    "final_plants_supported_by_route_blind_presurvey",
    "final_mammals_supported_by_route_blind_presurvey",
    "final_site_plant_pairs_supported_by_route_blind_presurvey",
    "confirmatory_freeze_receipt_checksum_matches",
    "confirmatory_freeze_receipt_ready",
    "land_site_access_resolved",
    "camera_deployment_resolved",
    "plant_morphology_measurement_resolved",
    "plant_tissue_collection_resolved_or_not_planned",
    "mammal_capture_or_handling_resolved_or_not_planned",
    "animal_ethics_or_institutional_review_resolved",
    "mammal_morphology_mode_predeclared",
    "mammal_morphology_same_regional_assemblage_supported",
    "other_required_authorizations_checked",
}

EVENT_REQUIRED = {
    "event_id",
    "dataset_role",
    "site_id",
    "plant_species",
    "mammal_species",
    "timestamp",
    "camera_id",
    "route_code",
    "visitor_id_confidence",
    "clip_quality",
}
PLANT_REQUIRED = {
    "site_id",
    "plant_species",
    "inflorescence_id",
    "access_depth_mm",
    "repeat_index",
}
MAMMAL_REQUIRED = {
    "mammal_species",
    "individual_id",
    "rostral_reach_mm",
    "repeat_index",
}
CAMERA_REQUIRED = {
    "deployment_id",
    "site_id",
    "plant_species",
    "camera_id",
    "planned_start_utc",
    "planned_end_utc",
    "planned_camera_hours",
    "camera_angle",
    "dataset_role",
    "effort_rule_version",
    "route_outcome_adaptive",
}


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv(path: str | Path, required: set[str], label: str) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = required.difference(fields)
        if missing:
            raise ValueError(f"{label} missing required columns: {sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{label} table is empty")
    return rows


def _positive_float(value: object, label: str) -> float:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{label} must be positive and finite")
    return number


def _positive_int(value: object, label: str) -> int:
    try:
        number = int(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be integer") from exc
    if number <= 0:
        raise ValueError(f"{label} must be positive")
    return number


def _parse_iso(value: str, label: str) -> dt.datetime:
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO-8601 datetime") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include timezone")
    return parsed


def _validate_events(
    rows: list[dict[str, str]],
    *,
    final_sites: set[str],
    final_plants: set[str],
    final_mammals: set[str],
    final_site_plant_pairs: set[tuple[str, str]],
    camera_windows: dict[tuple[str, str, str], list[tuple[dt.datetime, dt.datetime]]],
) -> dict[str, object]:
    ids: list[str] = []
    visitors: set[str] = set()
    plants: set[str] = set()
    sites: set[str] = set()

    for row in rows:
        event_id = str(row["event_id"]).strip()
        if not event_id:
            raise ValueError("events.event_id must not be blank")
        ids.append(event_id)

        if str(row["dataset_role"]).strip().upper() != "CONFIRMATORY":
            raise ValueError("PILOT_OR_NONCONFIRMATORY_EVENT_SUPPLIED")

        route = str(row["route_code"]).strip().upper()
        if route not in ALLOWED_ROUTE_CODES:
            raise ValueError(f"invalid route_code: {route!r}")

        conf = str(row["visitor_id_confidence"]).strip().upper()
        if conf not in ALLOWED_ID_CONFIDENCE:
            raise ValueError(f"invalid visitor_id_confidence: {conf!r}")

        quality = str(row["clip_quality"]).strip().upper()
        if quality not in ALLOWED_CLIP_QUALITY:
            raise ValueError(f"invalid clip_quality: {quality!r}")

        site = str(row["site_id"]).strip()
        plant = str(row["plant_species"]).strip()
        visitor = str(row["mammal_species"]).strip()
        camera = str(row["camera_id"]).strip()
        if not site or not plant or not visitor or not camera:
            raise ValueError("events site/plant/mammal/camera identifiers must not be blank")
        if site not in final_sites:
            raise ValueError(f"event site outside frozen site list: {site}")
        if plant not in final_plants:
            raise ValueError(f"event plant outside frozen plant list: {plant}")
        if visitor not in final_mammals:
            raise ValueError(f"event mammal outside frozen mammal list: {visitor}")
        if (site, plant) not in final_site_plant_pairs:
            raise ValueError(
                f"event site x plant outside frozen pair list: {site}:{plant}"
            )

        key = (site, plant, camera)
        windows = camera_windows.get(key)
        if not windows:
            raise ValueError(
                "EVENT_CAMERA_NOT_IN_FROZEN_DEPLOYMENT: "
                f"site={site}, plant={plant}, camera={camera}"
            )
        timestamp = _parse_iso(row["timestamp"], "events.timestamp")
        if not any(start <= timestamp <= end for start, end in windows):
            raise ValueError(
                "EVENT_OUTSIDE_FROZEN_CAMERA_WINDOW: "
                f"event_id={event_id}, camera={camera}"
            )

        sites.add(site)
        plants.add(plant)
        visitors.add(visitor)

    if len(ids) != len(set(ids)):
        raise ValueError("events.event_id must be unique")

    return {
        "rows": len(rows),
        "sites": len(sites),
        "plants": len(plants),
        "mammals": len(visitors),
    }


def _validate_plant_traits(
    rows: list[dict[str, str]],
    *,
    final_sites: set[str],
    final_plants: set[str],
    final_site_plant_pairs: set[tuple[str, str]],
) -> dict[str, object]:
    replicates: set[tuple[str, str, str, int]] = set()
    sites: set[str] = set()
    plants: set[str] = set()

    for row in rows:
        site = str(row["site_id"]).strip()
        plant = str(row["plant_species"]).strip()
        inflo = str(row["inflorescence_id"]).strip()
        repeat = _positive_int(row["repeat_index"], "plant_traits.repeat_index")
        _positive_float(row["access_depth_mm"], "plant_traits.access_depth_mm")

        if site not in final_sites:
            raise ValueError(f"plant morphology site outside frozen site list: {site}")
        if plant not in final_plants:
            raise ValueError(f"plant morphology species outside frozen plant list: {plant}")
        if (site, plant) not in final_site_plant_pairs:
            raise ValueError(
                f"plant morphology site x plant outside frozen pair list: {site}:{plant}"
            )
        if not inflo:
            raise ValueError("plant_traits.inflorescence_id must not be blank")

        key = (site, plant, inflo, repeat)
        if key in replicates:
            raise ValueError("duplicate plant morphology replicate key")
        replicates.add(key)
        sites.add(site)
        plants.add(plant)

    observed_pairs = {(key[0], key[1]) for key in replicates}
    missing_pairs = final_site_plant_pairs.difference(observed_pairs)
    if missing_pairs:
        encoded = ",".join(f"{site}:{plant}" for site, plant in sorted(missing_pairs))
        raise ValueError("plant morphology missing frozen site x plant units: " + encoded)

    return {"rows": len(rows), "sites": len(sites), "plants": len(plants)}


def _validate_mammal_traits(
    rows: list[dict[str, str]],
    *,
    final_mammals: set[str],
) -> dict[str, object]:
    replicates: set[tuple[str, str, int]] = set()
    mammals: set[str] = set()

    for row in rows:
        mammal = str(row["mammal_species"]).strip()
        individual = str(row["individual_id"]).strip()
        repeat = _positive_int(row["repeat_index"], "mammal_traits.repeat_index")
        _positive_float(row["rostral_reach_mm"], "mammal_traits.rostral_reach_mm")
        if not mammal or not individual:
            raise ValueError("mammal morphology identifiers must not be blank")
        if mammal not in final_mammals:
            raise ValueError(f"mammal morphology species outside frozen mammal list: {mammal}")
        key = (mammal, individual, repeat)
        if key in replicates:
            raise ValueError("duplicate mammal morphology replicate key")
        replicates.add(key)
        mammals.add(mammal)

    missing = final_mammals.difference(mammals)
    if missing:
        raise ValueError(
            "mammal morphology missing frozen species: " + ",".join(sorted(missing))
        )
    return {"rows": len(rows), "mammals": len(mammals)}


def _validate_camera_deployment(
    rows: list[dict[str, str]],
    *,
    final_sites: set[str],
    final_plants: set[str],
    final_site_plant_pairs: set[tuple[str, str]],
) -> dict[str, object]:
    ids: list[str] = []
    sites: set[str] = set()
    plants: set[str] = set()
    total_hours = 0.0
    observed_pairs: set[tuple[str, str]] = set()

    for row in rows:
        deployment_id = str(row["deployment_id"]).strip()
        if not deployment_id:
            raise ValueError("deployment_id must not be blank")
        ids.append(deployment_id)

        if str(row["dataset_role"]).strip().upper() != "CONFIRMATORY":
            raise ValueError("camera deployment must be CONFIRMATORY only")
        if str(row["route_outcome_adaptive"]).strip().lower() != "false":
            raise ValueError("OUTCOME_ADAPTIVE_CAMERA_EFFORT_FORBIDDEN")

        site = str(row["site_id"]).strip()
        plant = str(row["plant_species"]).strip()
        camera = str(row["camera_id"]).strip()
        rule = str(row["effort_rule_version"]).strip()
        angle = str(row["camera_angle"]).strip().upper()

        if site not in final_sites:
            raise ValueError(f"camera site outside frozen site list: {site}")
        if plant not in final_plants:
            raise ValueError(f"camera plant outside frozen plant list: {plant}")
        if (site, plant) not in final_site_plant_pairs:
            raise ValueError(
                f"camera site x plant outside frozen pair list: {site}:{plant}"
            )
        if not camera or not rule:
            raise ValueError("camera_id and effort_rule_version must not be blank")
        if angle not in {"PRIMARY", "SECONDARY_VALIDATION"}:
            raise ValueError(f"invalid camera_angle: {angle!r}")

        start = _parse_iso(row["planned_start_utc"], "planned_start_utc")
        end = _parse_iso(row["planned_end_utc"], "planned_end_utc")
        if end <= start:
            raise ValueError("camera deployment end must be after start")

        hours = _positive_float(row["planned_camera_hours"], "planned_camera_hours")
        total_hours += hours
        sites.add(site)
        plants.add(plant)
        observed_pairs.add((site, plant))

    if len(ids) != len(set(ids)):
        raise ValueError("deployment_id must be unique")
    if sites != final_sites:
        raise ValueError("camera deployment does not cover every frozen site")
    if plants != final_plants:
        raise ValueError("camera deployment does not cover every frozen plant species")
    if observed_pairs != final_site_plant_pairs:
        missing = final_site_plant_pairs.difference(observed_pairs)
        extra = observed_pairs.difference(final_site_plant_pairs)
        detail = (
            "missing=" + ",".join(f"{s}:{p}" for s, p in sorted(missing))
            + ";extra=" + ",".join(f"{s}:{p}" for s, p in sorted(extra))
        )
        raise ValueError("camera deployment does not match frozen site x plant pairs: " + detail)

    return {
        "rows": len(rows),
        "sites": len(sites),
        "plants": len(plants),
        "planned_camera_hours_total": total_hours,
    }


def _validate_field_readiness_receipt(
    field: dict[str, object],
    *,
    confirmatory_freeze_sha256: str,
    freeze_payload: dict[str, object],
) -> dict[str, object]:
    if field.get("receipt_schema_version") != FIELD_READINESS_SCHEMA:
        raise ValueError("INVALID_FIELD_READINESS_RECEIPT_SCHEMA")
    if field.get("status") != FIELD_READY_STATUS:
        raise ValueError("FIELD_READINESS_NOT_READY")

    gates = field.get("gates")
    if not isinstance(gates, dict) or not gates:
        raise ValueError("FIELD_READINESS_GATES_MISSING")
    missing_gates = sorted(REQUIRED_FIELD_READINESS_GATES.difference(gates))
    if missing_gates:
        raise ValueError(
            "FIELD_READINESS_REQUIRED_GATES_MISSING: " + ",".join(missing_gates)
        )
    failed = sorted(str(key) for key, value in gates.items() if value is not True)
    if failed:
        raise ValueError("FIELD_READINESS_GATES_NOT_ALL_TRUE: " + ",".join(failed))

    freeze_ref = field.get("confirmatory_freeze_receipt")
    if not isinstance(freeze_ref, dict):
        raise ValueError("FIELD_READINESS_FREEZE_REFERENCE_MISSING")
    if str(freeze_ref.get("validator_status", "")) != "READY_FOR_CONFIRMATORY_VIDEO_OPEN":
        raise ValueError("FIELD_READINESS_FREEZE_NOT_READY")
    failures = freeze_ref.get("validator_failures")
    if failures not in ([], None):
        raise ValueError("FIELD_READINESS_FREEZE_HAS_FAILURES")

    expected = str(freeze_ref.get("expected_sha256", "")).strip().lower()
    actual = str(freeze_ref.get("actual_sha256", "")).strip().lower()
    if expected != confirmatory_freeze_sha256 or actual != confirmatory_freeze_sha256:
        raise ValueError("FIELD_READINESS_CONFIRMATORY_FREEZE_HASH_MISMATCH")

    selection = freeze_payload.get("site_selection", {})
    if not isinstance(selection, dict):
        raise ValueError("CONFIRMATORY_FREEZE_SITE_SELECTION_MISSING")
    frozen_sites = {
        str(site).strip()
        for site in selection.get("final_sites", [])
        if str(site).strip()
    }
    frozen_plants = {
        str(value).strip()
        for value in selection.get("final_plant_species", [])
        if str(value).strip()
    }
    frozen_mammals = {
        str(value).strip()
        for value in selection.get("final_mammal_species", [])
        if str(value).strip()
    }
    readiness_sites = {
        str(site).strip()
        for site in freeze_ref.get("final_sites", [])
        if str(site).strip()
    }
    readiness_plants = {
        str(value).strip()
        for value in freeze_ref.get("final_plant_species", [])
        if str(value).strip()
    }
    readiness_mammals = {
        str(value).strip()
        for value in freeze_ref.get("final_mammal_species", [])
        if str(value).strip()
    }
    frozen_pairs = {
        (
            str(row.get("site_id", "")).strip(),
            str(row.get("plant_species", "")).strip(),
        )
        for row in selection.get("final_site_plant_pairs", [])
        if isinstance(row, dict)
        and str(row.get("site_id", "")).strip()
        and str(row.get("plant_species", "")).strip()
    }
    readiness_pairs = {
        (
            str(row.get("site_id", "")).strip(),
            str(row.get("plant_species", "")).strip(),
        )
        for row in freeze_ref.get("final_site_plant_pairs", [])
        if isinstance(row, dict)
        and str(row.get("site_id", "")).strip()
        and str(row.get("plant_species", "")).strip()
    }
    if readiness_sites != frozen_sites:
        raise ValueError("FIELD_READINESS_FINAL_SITE_MISMATCH")
    if readiness_plants != frozen_plants:
        raise ValueError("FIELD_READINESS_FINAL_PLANT_MISMATCH")
    if readiness_mammals != frozen_mammals:
        raise ValueError("FIELD_READINESS_FINAL_MAMMAL_MISMATCH")
    if readiness_pairs != frozen_pairs:
        raise ValueError("FIELD_READINESS_FINAL_SITE_PLANT_PAIR_MISMATCH")

    route_blind = field.get("route_blind_presurvey")
    if not isinstance(route_blind, dict):
        raise ValueError("FIELD_READINESS_PRESURVEY_REFERENCE_MISSING")
    presurvey_actual = str(route_blind.get("actual_sha256", "")).strip().lower()
    presurvey_expected = str(route_blind.get("expected_sha256", "")).strip().lower()
    if not presurvey_actual or not presurvey_expected:
        raise ValueError("FIELD_READINESS_PRESURVEY_HASH_MISSING")
    if presurvey_actual != presurvey_expected:
        raise ValueError("FIELD_READINESS_PRESURVEY_HASH_MISMATCH")

    return {
        "receipt_schema_version": field.get("receipt_schema_version"),
        "status": field.get("status"),
        "confirmatory_freeze_sha256": confirmatory_freeze_sha256,
        "gates_verified_true": len(gates),
    }


def _camera_event_windows(
    rows: list[dict[str, str]],
) -> dict[tuple[str, str, str], list[tuple[dt.datetime, dt.datetime]]]:
    windows: dict[tuple[str, str, str], list[tuple[dt.datetime, dt.datetime]]] = {}
    for row in rows:
        key = (
            str(row["site_id"]).strip(),
            str(row["plant_species"]).strip(),
            str(row["camera_id"]).strip(),
        )
        start = _parse_iso(row["planned_start_utc"], "planned_start_utc")
        end = _parse_iso(row["planned_end_utc"], "planned_end_utc")
        windows.setdefault(key, []).append((start, end))
    return windows


def freeze_inputs(
    *,
    events_csv: str | Path,
    plant_traits_csv: str | Path,
    mammal_traits_csv: str | Path,
    camera_deployment_csv: str | Path,
    confirmatory_freeze_json: str | Path,
    field_readiness_json: str | Path,
) -> dict[str, object]:
    field_path = Path(field_readiness_json)
    freeze_path = Path(confirmatory_freeze_json)
    field = json.loads(field_path.read_text(encoding="utf-8"))
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    freeze_sha256 = _sha256(freeze_path)

    freeze_result = validate_confirmatory_freeze(freeze)
    if freeze_result["status"] != "READY_FOR_CONFIRMATORY_VIDEO_OPEN":
        raise ValueError("CONFIRMATORY_FREEZE_NOT_READY")

    field_validation = _validate_field_readiness_receipt(
        field,
        confirmatory_freeze_sha256=freeze_sha256,
        freeze_payload=freeze,
    )

    site_selection = freeze.get("site_selection", {})
    final_sites = {str(x) for x in site_selection.get("final_sites", []) if str(x).strip()}
    final_plants = {
        str(x) for x in site_selection.get("final_plant_species", []) if str(x).strip()
    }
    final_mammals = {
        str(x) for x in site_selection.get("final_mammal_species", []) if str(x).strip()
    }
    final_site_plant_pairs = {
        (
            str(row.get("site_id", "")).strip(),
            str(row.get("plant_species", "")).strip(),
        )
        for row in site_selection.get("final_site_plant_pairs", [])
        if isinstance(row, dict)
        and str(row.get("site_id", "")).strip()
        and str(row.get("plant_species", "")).strip()
    }
    if (
        not final_sites
        or not final_plants
        or not final_mammals
        or not final_site_plant_pairs
    ):
        raise ValueError("frozen site/plant/mammal/pair lists are empty")

    events = _read_csv(events_csv, EVENT_REQUIRED, "events")
    plant_traits = _read_csv(plant_traits_csv, PLANT_REQUIRED, "plant_traits")
    mammal_traits = _read_csv(mammal_traits_csv, MAMMAL_REQUIRED, "mammal_traits")
    camera = _read_csv(camera_deployment_csv, CAMERA_REQUIRED, "camera_deployment")

    camera_validation = _validate_camera_deployment(
        camera,
        final_sites=final_sites,
        final_plants=final_plants,
        final_site_plant_pairs=final_site_plant_pairs,
    )
    camera_windows = _camera_event_windows(camera)

    validation = {
        "events": _validate_events(
            events,
            final_sites=final_sites,
            final_plants=final_plants,
            final_mammals=final_mammals,
            final_site_plant_pairs=final_site_plant_pairs,
            camera_windows=camera_windows,
        ),
        "plant_traits": _validate_plant_traits(
            plant_traits,
            final_sites=final_sites,
            final_plants=final_plants,
            final_site_plant_pairs=final_site_plant_pairs,
        ),
        "mammal_traits": _validate_mammal_traits(
            mammal_traits,
            final_mammals=final_mammals,
        ),
        "camera_deployment": camera_validation,
    }

    paths = {
        "events": Path(events_csv),
        "plant_traits": Path(plant_traits_csv),
        "mammal_traits": Path(mammal_traits_csv),
        "camera_deployment": Path(camera_deployment_csv),
        "confirmatory_freeze": Path(confirmatory_freeze_json),
        "field_readiness": Path(field_readiness_json),
    }

    return {
        "receipt": RECEIPT,
        "status": READY_STATUS,
        "frozen_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "files": {
            key: {
                "filename": path.name,
                "sha256": _sha256(path),
            }
            for key, path in paths.items()
        },
        "validation": validation,
        "field_readiness_validation": field_validation,
        "final_sites": sorted(final_sites),
        "final_plant_species": sorted(final_plants),
        "final_mammal_species": sorted(final_mammals),
        "final_site_plant_pairs": [
            {"site_id": site, "plant_species": plant}
            for site, plant in sorted(final_site_plant_pairs)
        ],
        "join_rule": (
            "Route outcomes and morphology may be joined only through the checksum-verifying "
            "third-network unit builder using this manifest."
        ),
    }


def write_manifest(path: str | Path, manifest: dict[str, object]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("events_csv")
    parser.add_argument("plant_traits_csv")
    parser.add_argument("mammal_traits_csv")
    parser.add_argument("camera_deployment_csv")
    parser.add_argument("confirmatory_freeze_json")
    parser.add_argument("field_readiness_json")
    parser.add_argument("output_manifest_json")
    args = parser.parse_args()

    manifest = freeze_inputs(
        events_csv=args.events_csv,
        plant_traits_csv=args.plant_traits_csv,
        mammal_traits_csv=args.mammal_traits_csv,
        camera_deployment_csv=args.camera_deployment_csv,
        confirmatory_freeze_json=args.confirmatory_freeze_json,
        field_readiness_json=args.field_readiness_json,
    )
    write_manifest(args.output_manifest_json, manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
