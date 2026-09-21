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
    "coding_manual_version",
    "route_code",
    "visitor_id_confidence",
    "route_visibility",
    "tissue_damage",
    "pollen_presenter_contact",
    "nectar_behavior_confidence",
    "preexisting_bypass_opening",
    "clip_quality",
    "coder_id",
    "double_coded",
}
PLANT_REQUIRED = {
    "site_id",
    "plant_species",
    "protocol_version",
    "inflorescence_id",
    "access_depth_mm",
    "repeat_index",
}
MAMMAL_REQUIRED = {
    "mammal_species",
    "protocol_version",
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


def _bool_text(value: object, label: str) -> bool:
    text = str(value).strip().lower()
    if text == "true":
        return True
    if text == "false":
        return False
    raise ValueError(f"{label} must be true or false")


def _cohen_kappa(pairs: list[tuple[str, str]]) -> float:
    if not pairs:
        raise ValueError("INTER_RATER_KAPPA_NOT_ESTIMABLE: no double-coded events")

    labels = sorted(ALLOWED_ROUTE_CODES)
    n = len(pairs)
    observed = sum(a == b for a, b in pairs) / n
    first = {label: 0 for label in labels}
    second = {label: 0 for label in labels}
    for a, b in pairs:
        first[a] += 1
        second[b] += 1
    expected = sum((first[label] / n) * (second[label] / n) for label in labels)
    if expected >= 1.0 - 1e-15:
        raise ValueError(
            "INTER_RATER_KAPPA_NOT_ESTIMABLE: double-coded labels have no marginal variation"
        )
    return (observed - expected) / (1.0 - expected)


def _validate_events(
    rows: list[dict[str, str]],
    *,
    final_sites: set[str],
    final_plants: set[str],
    final_mammals: set[str],
    final_site_plant_pairs: set[tuple[str, str]],
    camera_windows: dict[tuple[str, str, str], list[tuple[dt.datetime, dt.datetime]]],
    coding_manual_version: str,
    minimum_double_code_fraction: float,
    minimum_kappa: float,
) -> dict[str, object]:
    ids: list[str] = []
    visitors: set[str] = set()
    plants: set[str] = set()
    sites: set[str] = set()
    feeding_events = 0
    double_coded_feeding_events = 0
    double_coded_pairs: list[tuple[str, str]] = []

    for row in rows:
        event_id = str(row["event_id"]).strip()
        if not event_id:
            raise ValueError("events.event_id must not be blank")
        ids.append(event_id)

        if str(row["dataset_role"]).strip().upper() != "CONFIRMATORY":
            raise ValueError("PILOT_OR_NONCONFIRMATORY_EVENT_SUPPLIED")

        version = str(row["coding_manual_version"]).strip()
        if version != coding_manual_version:
            raise ValueError(
                "ROUTE_CODING_MANUAL_VERSION_MISMATCH: "
                f"expected={coding_manual_version}, observed={version}"
            )

        route = str(row["route_code"]).strip().upper()
        if route not in ALLOWED_ROUTE_CODES:
            raise ValueError(f"invalid route_code: {route!r}")

        visibility = str(row["route_visibility"]).strip().upper()
        if visibility not in {"FULL", "PARTIAL", "POOR"}:
            raise ValueError(f"invalid route_visibility: {visibility!r}")
        for field in (
            "tissue_damage",
            "pollen_presenter_contact",
            "preexisting_bypass_opening",
        ):
            value = str(row[field]).strip().upper()
            if value not in {"YES", "NO", "UNCLEAR"}:
                raise ValueError(f"invalid {field}: {value!r}")
        nectar_conf = str(row["nectar_behavior_confidence"]).strip().upper()
        if nectar_conf not in {"HIGH", "MEDIUM", "LOW"}:
            raise ValueError(
                f"invalid nectar_behavior_confidence: {nectar_conf!r}"
            )
        coder = str(row["coder_id"]).strip()
        if not coder:
            raise ValueError("coder_id must not be blank")

        is_double = _bool_text(row["double_coded"], "double_coded")
        second_route = str(row.get("second_route_code", "")).strip().upper()
        if is_double:
            if second_route not in ALLOWED_ROUTE_CODES:
                raise ValueError(
                    "second_route_code must be L/B/A/N when double_coded=true"
                )
            double_coded_pairs.append((route, second_route))
        elif second_route:
            raise ValueError(
                "second_route_code must be blank when double_coded=false"
            )

        if route != "N":
            feeding_events += 1
            if is_double:
                double_coded_feeding_events += 1

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
    if feeding_events <= 0:
        raise ValueError("NO_CONFIRMATORY_FEEDING_EVENTS_FOR_RELIABILITY")

    fraction = double_coded_feeding_events / feeding_events
    if fraction + 1e-15 < minimum_double_code_fraction:
        raise ValueError(
            "DOUBLE_CODE_FRACTION_BELOW_FROZEN_MINIMUM: "
            f"observed={fraction:.6f}, required={minimum_double_code_fraction:.6f}"
        )

    kappa = _cohen_kappa(double_coded_pairs)
    if kappa + 1e-15 < minimum_kappa:
        raise ValueError(
            "INTER_RATER_KAPPA_BELOW_FROZEN_TARGET: "
            f"observed={kappa:.6f}, required={minimum_kappa:.6f}"
        )

    return {
        "rows": len(rows),
        "sites": len(sites),
        "plants": len(plants),
        "mammals": len(visitors),
        "feeding_events": feeding_events,
        "double_coded_feeding_events": double_coded_feeding_events,
        "double_code_fraction": fraction,
        "cohen_kappa_LBAN": kappa,
        "coding_manual_version": coding_manual_version,
    }


def _validate_plant_traits(
    rows: list[dict[str, str]],
    *,
    final_sites: set[str],
    final_plants: set[str],
    final_site_plant_pairs: set[tuple[str, str]],
    protocol_version: str,
) -> dict[str, object]:
    replicates: set[tuple[str, str, str, int]] = set()
    sites: set[str] = set()
    plants: set[str] = set()

    for row in rows:
        site = str(row["site_id"]).strip()
        plant = str(row["plant_species"]).strip()
        observed_version = str(row["protocol_version"]).strip()
        if observed_version != protocol_version:
            raise ValueError(
                "PLANT_MORPHOLOGY_PROTOCOL_VERSION_MISMATCH: "
                f"expected={protocol_version}, observed={observed_version}"
            )
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

    return {
        "rows": len(rows),
        "sites": len(sites),
        "plants": len(plants),
        "protocol_version": protocol_version,
    }


def _validate_mammal_traits(
    rows: list[dict[str, str]],
    *,
    final_mammals: set[str],
    protocol_version: str,
) -> dict[str, object]:
    replicates: set[tuple[str, str, int]] = set()
    mammals: set[str] = set()

    for row in rows:
        mammal = str(row["mammal_species"]).strip()
        observed_version = str(row["protocol_version"]).strip()
        if observed_version != protocol_version:
            raise ValueError(
                "MAMMAL_MORPHOLOGY_PROTOCOL_VERSION_MISMATCH: "
                f"expected={protocol_version}, observed={observed_version}"
            )
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
    return {
        "rows": len(rows),
        "mammals": len(mammals),
        "protocol_version": protocol_version,
    }


def _validate_camera_deployment(
    rows: list[dict[str, str]],
    *,
    final_sites: set[str],
    final_plants: set[str],
    final_site_plant_pairs: set[tuple[str, str]],
    effort_rule_version: str,
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
        if rule != effort_rule_version:
            raise ValueError(
                "CAMERA_EFFORT_RULE_VERSION_MISMATCH: "
                f"expected={effort_rule_version}, observed={rule}"
            )
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
        available_hours = (end - start).total_seconds() / 3600.0
        if hours > available_hours + 1e-9:
            raise ValueError(
                "PLANNED_CAMERA_HOURS_EXCEED_DEPLOYMENT_WINDOW: "
                f"planned={hours}, available={available_hours}"
            )
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
        "effort_rule_version": effort_rule_version,
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
    route_coding = freeze.get("route_coding", {})
    morphology = freeze.get("morphology", {})
    camera_effort = freeze.get("camera_effort", {})
    if not all(isinstance(value, dict) for value in (site_selection, route_coding, morphology, camera_effort)):
        raise ValueError("CONFIRMATORY_FREEZE_PROTOCOL_BLOCK_MISSING")

    coding_manual_version = str(route_coding.get("manual", "")).strip()
    minimum_double_code_fraction = float(route_coding.get("double_code_fraction_minimum", -1))
    minimum_kappa = float(route_coding.get("target_kappa_LBAN", -1))
    plant_protocol_version = str(morphology.get("plant_protocol_version", "")).strip()
    mammal_protocol_version = str(morphology.get("mammal_protocol_version", "")).strip()
    effort_rule_version = str(camera_effort.get("rule_version", "")).strip()

    if not coding_manual_version or not plant_protocol_version or not mammal_protocol_version or not effort_rule_version:
        raise ValueError("CONFIRMATORY_FREEZE_PROTOCOL_VERSION_MISSING")
    if not (0 < minimum_double_code_fraction <= 1):
        raise ValueError("invalid frozen double_code_fraction_minimum")
    if not (-1 <= minimum_kappa <= 1):
        raise ValueError("invalid frozen target_kappa_LBAN")

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
        effort_rule_version=effort_rule_version,
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
            coding_manual_version=coding_manual_version,
            minimum_double_code_fraction=minimum_double_code_fraction,
            minimum_kappa=minimum_kappa,
        ),
        "plant_traits": _validate_plant_traits(
            plant_traits,
            final_sites=final_sites,
            final_plants=final_plants,
            final_site_plant_pairs=final_site_plant_pairs,
            protocol_version=plant_protocol_version,
        ),
        "mammal_traits": _validate_mammal_traits(
            mammal_traits,
            final_mammals=final_mammals,
            protocol_version=mammal_protocol_version,
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
