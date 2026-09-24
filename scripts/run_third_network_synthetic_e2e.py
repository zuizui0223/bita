"""Run the complete prospective third-network pipeline on synthetic development data.

This is a wiring/integrity test only. It must never be used as biological
evidence. The runner exercises:

route-blind presurvey
-> confirmatory pre-video freeze
-> field readiness
-> confirmatory input freeze
-> checksum-verifying unit build
-> third-network r_T
-> equal-network synthetic k=3 integration
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing_k3 import summarize_joint_k3
from scripts.analyze_third_access_routing_network import summarize_third_network
from scripts.build_third_access_routing_units import run as build_units
from scripts.evaluate_third_network_field_readiness import (
    READY_STATUS as FIELD_READY_STATUS,
    SCHEMA as FIELD_SCHEMA,
    evaluate as evaluate_field_readiness,
)
from scripts.evaluate_third_network_route_blind_presurvey import run as run_presurvey
from scripts.freeze_third_network_confirmatory_inputs import (
    freeze_inputs,
    write_manifest,
)
from scripts.evaluate_third_network_route_reliability import expected_double_code_ids

RECEIPT = "BITA_THIRD_NETWORK_SYNTHETIC_E2E_V1"
SCENARIOS = {"positive", "null", "opposite"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _confirmatory_freeze() -> dict[str, object]:
    return {
        "receipt": "BITA_THIRD_NETWORK_CONFIRMATORY_FREEZE_V1",
        "status": "REQUIRED_BEFORE_CONFIRMATORY_VIDEO_OPEN",
        "parent_prereg_commit": "ae98e496a99fa7f5b333bbe7881025d13a8d8768",
        "design_system": "CAPE_SMALL_MAMMAL_X_PROTEA",
        "site_selection": {
            "final_sites": ["S1", "S2"],
            "final_plant_species": [f"P{i}" for i in range(6)],
            "route_outcome_blind": True,
            "pilot_B_or_L_presence_used_for_selection": False,
            "selection_basis": "synthetic route-blind presurvey fixture",
        },
        "visitor_identification": {
            "protocol_version": "SYNTHETIC_ID_V1",
            "minimum_confidence": "MEDIUM",
        },
        "morphology": {
            "plant_protocol_version": "SYNTHETIC_PLANT_MORPH_V1",
            "mammal_protocol_version": "SYNTHETIC_MAMMAL_MORPH_V1",
            "plant_primary_trait": "legitimate_nectar_access_depth_mm",
            "mammal_primary_trait": "functional_rostral_reach_mm",
        },
        "route_coding": {
            "manual": "THIRD_NETWORK_ROUTE_CODING_MANUAL_V1",
            "coders_blind_to_P_V_M": True,
            "double_code_fraction_minimum": 0.2,
            "target_kappa_LBAN": 0.8,
        },
        "camera_effort": {
            "rule": "SYNTHETIC_FIXED_120H_PER_PLANT_SITE",
            "planner_receipt_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "planner_status": "PLANNING_TARGET_EFFORT_IDENTIFIED",
            "uniform_camera_hours_per_plant_site": 120.0,
            "qualifying_fraction": 0.5,
            "planner_target_success_probability": 0.8,
            "planner_achieved_success_probability": 0.9,
            "may_extend_based_on_route_outcomes": False,
        },
        "analysis": {
            "third_network_seed": 20260921,
            "k3_joint_seed": 20260921,
            "permutations": 9999,
            "minimum_units": 30,
            "minimum_mammal_species": 5,
            "minimum_plant_species": 5,
            "planning_target_units": 70,
        },
        "permissions": {
            "land_access": "SYNTHETIC_RESOLVED",
            "animal_capture_or_handling": "NOT_PLANNED",
            "plant_measurement_or_collection": "SYNTHETIC_RESOLVED",
        },
        "freeze_time_utc": "2027-01-01T00:00:00Z",
        "frozen_by": "synthetic_e2e_runner",
        "claim": "Synthetic development fixture only.",
    }


def _presurvey_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    record = 0
    for site in ("S1", "S2"):
        for p in range(6):
            record += 1
            rows.append(
                {
                    "record_id": f"R{record:03d}",
                    "site_id": site,
                    "record_type": "PLANT",
                    "plant_species": f"P{p}",
                    "mammal_species": "",
                    "evidence_method": "synthetic route-blind flowering survey",
                    "flowering_available": "YES",
                    "camera_operable": "NA",
                }
            )
        for m in range(6):
            record += 1
            rows.append(
                {
                    "record_id": f"R{record:03d}",
                    "site_id": site,
                    "record_type": "MAMMAL",
                    "plant_species": "",
                    "mammal_species": f"M{m}",
                    "evidence_method": "synthetic independent mammal survey",
                    "flowering_available": "NA",
                    "camera_operable": "NA",
                }
            )
        record += 1
        rows.append(
            {
                "record_id": f"R{record:03d}",
                "site_id": site,
                "record_type": "CAMERA",
                "plant_species": "",
                "mammal_species": "",
                "evidence_method": "synthetic camera setup test",
                "flowering_available": "NA",
                "camera_operable": "YES",
            }
        )
    return rows


def _action(planned: bool = True) -> dict[str, object]:
    if not planned:
        return {"planned": False}
    return {
        "planned": True,
        "regulatory_status": "PERMITTED",
        "evidence_reference": "SYNTHETIC-AUTH",
        "authorization_valid_from": "2027-01-01",
        "authorization_valid_until": "2027-12-31",
    }


def _plant_trait_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for s_idx, site in enumerate(("S1", "S2")):
        for p in range(6):
            for rep in (1, 2):
                rows.append(
                    {
                        "site_id": site,
                        "plant_species": f"P{p}",
                        "inflorescence_id": f"{site}_P{p}_I1",
                        "access_depth_mm": 18.0 + 2.5 * p + 0.4 * s_idx + 0.1 * rep,
                        "repeat_index": rep,
                    }
                )
    return rows


def _mammal_trait_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for m in range(6):
        for rep in (1, 2):
            rows.append(
                {
                    "mammal_species": f"M{m}",
                    "individual_id": f"M{m}_IND1",
                    "rostral_reach_mm": 11.0 + 1.6 * m + 0.1 * rep,
                    "repeat_index": rep,
                }
            )
    return rows


def _event_rows(scenario: str) -> list[dict[str, object]]:
    if scenario not in SCENARIOS:
        raise ValueError(f"unknown synthetic scenario: {scenario!r}")
    rows: list[dict[str, object]] = []
    event = 0
    for s_idx, site in enumerate(("S1", "S2")):
        for p in range(6):
            depth = 18.0 + 2.5 * p + 0.4 * s_idx + 0.15
            for m in range(6):
                reach = 11.0 + 1.6 * m + 0.15
                mismatch = math.log(depth / reach)
                if scenario == "positive":
                    bypass_prop = 1.0 / (1.0 + math.exp(-3.0 * mismatch))
                    b_count = max(1, min(9, round(10 * bypass_prop)))
                elif scenario == "opposite":
                    bypass_prop = 1.0 / (1.0 + math.exp(3.0 * mismatch))
                    b_count = max(1, min(9, round(10 * bypass_prop)))
                else:
                    # Structured route variation that is approximately orthogonal
                    # to the frozen mismatch ranks.  It keeps B and L present
                    # without encoding the predicted direction.
                    b_count = 1 + ((2 * m + 3 * p) % 9)
                for visit in range(10):
                    event += 1
                    route = "B" if visit < b_count else "L"
                    rows.append(
                        {
                            "event_id": f"E{event:05d}",
                            "dataset_role": "CONFIRMATORY",
                            "site_id": site,
                            "plant_species": f"P{p}",
                            "mammal_species": f"M{m}",
                            "timestamp": f"2027-03-{1 + (visit % 9):02d}T00:00:00Z",
                            "camera_id": f"C_{site}_P{p}",
                            "route_code": route,
                            "visitor_id_confidence": "HIGH",
                            "clip_quality": "PASS",
                        }
                    )
    selected = expected_double_code_ids(rows)
    for row in rows:
        event_id = str(row["event_id"])
        row["coder_id"] = "PRIMARY_SYNTHETIC"
        row["double_coded"] = "true" if event_id in selected else "false"
        row["second_route_code"] = row["route_code"] if event_id in selected else ""
    return rows


def _camera_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    deployment = 0
    for site in ("S1", "S2"):
        for p in range(6):
            deployment += 1
            rows.append(
                {
                    "deployment_id": f"D{deployment:03d}",
                    "site_id": site,
                    "plant_species": f"P{p}",
                    "camera_id": f"C_{site}_P{p}",
                    "planned_start_utc": "2027-03-01T00:00:00Z",
                    "planned_end_utc": "2027-03-06T00:00:00Z",
                    "planned_camera_hours": 120,
                    "camera_angle": "PRIMARY",
                    "dataset_role": "CONFIRMATORY",
                    "effort_rule_version": "SYNTHETIC_EFFORT_V1",
                    "route_outcome_adaptive": "false",
                }
            )
    return rows


def _synthetic_sakhalkar() -> list[dict[str, float]]:
    return [
        {"tube_length": float(i + 1), "balance": (float(i) - 10.0) / 10.0}
        for i in range(20)
    ]


def _synthetic_aubert() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for site in ("A", "B"):
        for i in range(30):
            mismatch = (i - 14.5) / 10.0
            rows.append(
                {
                    "site": site,
                    "mismatch_log_t_over_b": mismatch,
                    "robbery_rate": 1.0 / (1.0 + math.exp(-mismatch)),
                }
            )
    return rows


def run(
    output_dir: str | Path,
    *,
    permutations: int = 199,
    scenario: str = "positive",
) -> dict[str, object]:
    if scenario not in SCENARIOS:
        raise ValueError(f"scenario must be one of {sorted(SCENARIOS)}")
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)

    presurvey_csv = root / "route_blind_presurvey.csv"
    presurvey_receipt = root / "route_blind_presurvey_receipt.json"
    freeze_json = root / "confirmatory_freeze.json"
    field_config = root / "field_readiness_config.json"
    field_receipt = root / "field_readiness_receipt.json"
    events_csv = root / "confirmatory_events.csv"
    plants_csv = root / "plant_traits.csv"
    mammals_csv = root / "mammal_traits.csv"
    camera_csv = root / "camera_deployment.csv"
    manifest_json = root / "input_freeze_manifest.json"
    units_csv = root / "analysis_units.csv"
    build_audit_json = root / "unit_build_audit.json"
    third_json = root / "third_network_result.json"
    joint_json = root / "synthetic_k3_result.json"
    receipt_json = root / "synthetic_e2e_receipt.json"

    _write_csv(
        presurvey_csv,
        [
            "record_id",
            "site_id",
            "record_type",
            "plant_species",
            "mammal_species",
            "evidence_method",
            "flowering_available",
            "camera_operable",
        ],
        _presurvey_rows(),
    )
    presurvey = run_presurvey(presurvey_csv, presurvey_receipt)

    freeze = _confirmatory_freeze()
    _write_json(freeze_json, freeze)

    field = {
        "schema_version": FIELD_SCHEMA,
        "system": "CAPE_SMALL_MAMMAL_X_PROTEA",
        "planned_field_start": "2027-03-01",
        "planned_field_end": "2027-05-31",
        "site_locations_verified_privately": True,
        "site_location_receipt_reference": "SYNTHETIC-SITE-RECEIPT",
        "route_blind_presurvey": {
            "receipt_path": presurvey_receipt.name,
            "sha256": _sha256(presurvey_receipt),
        },
        "confirmatory_freeze_receipt": {
            "path": freeze_json.name,
            "sha256": _sha256(freeze_json),
        },
        "land_site_access": _action(),
        "camera_deployment": _action(),
        "plant_morphology_measurement": _action(),
        "plant_tissue_collection": _action(False),
        "mammal_capture_or_handling": _action(False),
        "mammal_morphology_source": {
            "mode": "INDEPENDENT_MORPHOMETRIC_DATA",
            "evidence_reference": "SYNTHETIC-MORPH-RECEIPT",
            "same_regional_assemblage_supported": True,
        },
        "animal_ethics_or_institutional_review": _action(),
        "other_required_authorizations_checked": True,
    }
    _write_json(field_config, field)
    field_result = evaluate_field_readiness(field, base_dir=root)
    _write_json(field_receipt, field_result)
    if field_result["status"] != FIELD_READY_STATUS:
        raise RuntimeError("synthetic field-readiness fixture did not reach READY")

    _write_csv(
        events_csv,
        [
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
            "coder_id",
            "double_coded",
            "second_route_code",
        ],
        _event_rows(scenario),
    )
    _write_csv(
        plants_csv,
        [
            "site_id",
            "plant_species",
            "inflorescence_id",
            "access_depth_mm",
            "repeat_index",
        ],
        _plant_trait_rows(),
    )
    _write_csv(
        mammals_csv,
        [
            "mammal_species",
            "individual_id",
            "rostral_reach_mm",
            "repeat_index",
        ],
        _mammal_trait_rows(),
    )
    _write_csv(
        camera_csv,
        [
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
        ],
        _camera_rows(),
    )

    manifest = freeze_inputs(
        events_csv=events_csv,
        plant_traits_csv=plants_csv,
        mammal_traits_csv=mammals_csv,
        camera_deployment_csv=camera_csv,
        confirmatory_freeze_json=freeze_json,
        field_readiness_json=field_receipt,
    )
    write_manifest(manifest_json, manifest)

    build_audit = build_units(
        events_csv,
        plants_csv,
        mammals_csv,
        manifest_json,
        units_csv,
        build_audit_json,
    )

    from scripts.analyze_third_access_routing_network import load_analysis_units

    third_rows = load_analysis_units(units_csv)
    third_result = summarize_third_network(
        third_rows,
        permutations=permutations,
        seed=20260921,
    )
    _write_json(third_json, third_result)

    joint_result = summarize_joint_k3(
        _synthetic_sakhalkar(),
        _synthetic_aubert(),
        third_rows,
        permutations=permutations,
        seed=20260921,
    )
    _write_json(joint_json, joint_result)

    receipt = {
        "receipt": RECEIPT,
        "status": "PASS",
        "mode": "DEVELOPMENT_ONLY_SYNTHETIC",
        "scientific_claim_allowed": False,
        "scenario": scenario,
        "presurvey_status": presurvey["status"],
        "field_readiness_status": field_result["status"],
        "input_freeze_status": manifest["status"],
        "route_reliability_status": manifest["route_reliability"]["status"],
        "route_reliability_kappa": manifest["route_reliability"]["kappa_LBAN"],
        "analysis_units": build_audit["analysis_units"],
        "third_network_status": third_result["status"],
        "third_network_rho": third_result["effect"]["rho_site_adjusted_rank"],
        "k3_network_count": joint_result["network_count"],
        "k3_joint_rho": joint_result["joint_equal_network_fisher_z_rho"],
        "k3_direction_concordance": joint_result["network_direction_concordance"],
        "files": {
            path.name: _sha256(path)
            for path in (
                presurvey_receipt,
                freeze_json,
                field_receipt,
                events_csv,
                plants_csv,
                mammals_csv,
                camera_csv,
                manifest_json,
                units_csv,
                third_json,
                joint_json,
            )
        },
        "claim_boundary": (
            "Synthetic values are generated only to validate pipeline wiring, fail-closed gates, "
            "hash binding and reproducibility. They are not ecological observations."
        ),
    }
    _write_json(receipt_json, receipt)
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--permutations", type=int, default=199)
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="positive")
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.output_dir,
                permutations=args.permutations,
                scenario=args.scenario,
            ),
            indent=2,
            sort_keys=True,
        )
    )
