"""Synthetic end-to-end development harness for the prospective third network.

This is a software/inference-contract test only. Synthetic outputs are never
licensed as ecological evidence or manuscript results.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from scripts.analyze_joint_access_routing_k3 import summarize_joint_k3
from scripts.analyze_third_access_routing_network import run as run_third
from scripts.build_third_access_routing_units import run as build_units
from scripts.evaluate_third_network_field_readiness import evaluate as evaluate_field
from scripts.evaluate_third_network_route_blind_presurvey import evaluate_rows as evaluate_presurvey
from scripts.freeze_third_network_confirmatory_inputs import freeze_inputs, write_manifest

SCENARIOS = {"positive", "orthogonal", "opposite"}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _presurvey_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    record = 0
    for site in ("S1", "S2"):
        for p in range(6):
            record += 1
            rows.append({
                "record_id": f"R{record:03d}",
                "site_id": site,
                "record_type": "PLANT",
                "plant_species": f"P{p}",
                "mammal_species": "",
                "evidence_method": "synthetic route-blind flowering presurvey",
                "flowering_available": "YES",
                "camera_operable": "NA",
            })
        for m in range(6):
            record += 1
            rows.append({
                "record_id": f"R{record:03d}",
                "site_id": site,
                "record_type": "MAMMAL",
                "plant_species": "",
                "mammal_species": f"M{m}",
                "evidence_method": "synthetic independent mammal presurvey",
                "flowering_available": "NA",
                "camera_operable": "NA",
            })
        record += 1
        rows.append({
            "record_id": f"R{record:03d}",
            "site_id": site,
            "record_type": "CAMERA",
            "plant_species": "",
            "mammal_species": "",
            "evidence_method": "synthetic camera operability test",
            "flowering_available": "NA",
            "camera_operable": "YES",
        })
    return rows


def _freeze_receipt() -> dict[str, object]:
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
            "selection_basis": "synthetic route-blind presurvey only",
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
            "rule": "synthetic fixed 120 camera-hours per plant x site",
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
            "land_access": "RESOLVED",
            "animal_capture_or_handling": "NOT_PLANNED",
            "plant_measurement_or_collection": "RESOLVED",
        },
        "freeze_time_utc": "2027-01-01T00:00:00Z",
        "frozen_by": "synthetic_harness",
        "claim": "Synthetic development receipt only.",
    }


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


def _field_config(presurvey_path: Path, freeze_path: Path) -> dict[str, object]:
    return {
        "schema_version": "BITA_THIRD_NETWORK_FIELD_READINESS_V1",
        "system": "CAPE_SMALL_MAMMAL_X_PROTEA",
        "planned_field_start": "2027-03-01",
        "planned_field_end": "2027-05-31",
        "site_locations_verified_privately": True,
        "site_location_receipt_reference": "SYNTHETIC-SITE-RECEIPT",
        "route_blind_presurvey": {
            "receipt_path": presurvey_path.name,
            "sha256": _sha(presurvey_path),
        },
        "confirmatory_freeze_receipt": {
            "path": freeze_path.name,
            "sha256": _sha(freeze_path),
        },
        "land_site_access": _action(),
        "camera_deployment": _action(),
        "plant_morphology_measurement": _action(),
        "plant_tissue_collection": _action(False),
        "mammal_capture_or_handling": _action(False),
        "mammal_morphology_source": {
            "mode": "INDEPENDENT_MORPHOMETRIC_DATA",
            "evidence_reference": "SYNTHETIC-MORPH",
            "same_regional_assemblage_supported": True,
        },
        "animal_ethics_or_institutional_review": _action(),
        "other_required_authorizations_checked": True,
    }


def _mismatch(site_index: int, plant_index: int, mammal_index: int) -> float:
    p = 18.0 + 2.5 * plant_index + 0.4 * site_index
    v = 11.0 + 1.6 * mammal_index
    return math.log(p / v)


def _bypass_count(
    scenario: str,
    *,
    site_index: int,
    plant_index: int,
    mammal_index: int,
    total: int = 12,
) -> int:
    m = _mismatch(site_index, plant_index, mammal_index)
    if scenario == "positive":
        score = 1.0 / (1.0 + math.exp(-3.0 * m))
    elif scenario == "opposite":
        score = 1.0 / (1.0 + math.exp(3.0 * m))
    elif scenario == "orthogonal":
        score = 0.2 + 0.6 * (((plant_index + 2 * mammal_index + site_index) % 5) / 4.0)
    else:
        raise ValueError(f"unknown scenario: {scenario}")
    return max(1, min(total - 1, round(total * score)))


def _raw_tables(outdir: Path, scenario: str) -> dict[str, Path]:
    events = outdir / "confirmatory_events.csv"
    plants = outdir / "plant_traits.csv"
    mammals = outdir / "mammal_traits.csv"
    cameras = outdir / "camera_deployment.csv"

    plant_rows: list[dict[str, object]] = []
    for s_idx, site in enumerate(("S1", "S2")):
        for p in range(6):
            for rep in (1, 2):
                plant_rows.append({
                    "site_id": site,
                    "plant_species": f"P{p}",
                    "inflorescence_id": f"{site}_P{p}_I{rep}",
                    "access_depth_mm": 18.0 + 2.5 * p + 0.4 * s_idx + (rep - 1.5) * 0.02,
                    "repeat_index": rep,
                })
    _write_csv(
        plants,
        ["site_id", "plant_species", "inflorescence_id", "access_depth_mm", "repeat_index"],
        plant_rows,
    )

    mammal_rows: list[dict[str, object]] = []
    for m in range(6):
        for rep in (1, 2):
            mammal_rows.append({
                "mammal_species": f"M{m}",
                "individual_id": f"M{m}_IND{rep}",
                "rostral_reach_mm": 11.0 + 1.6 * m + (rep - 1.5) * 0.02,
                "repeat_index": rep,
            })
    _write_csv(
        mammals,
        ["mammal_species", "individual_id", "rostral_reach_mm", "repeat_index"],
        mammal_rows,
    )

    camera_rows: list[dict[str, object]] = []
    for site in ("S1", "S2"):
        for p in range(6):
            camera_rows.append({
                "deployment_id": f"D_{site}_P{p}",
                "site_id": site,
                "plant_species": f"P{p}",
                "camera_id": f"C_{site}_P{p}",
                "planned_start_utc": "2027-03-01T00:00:00Z",
                "planned_end_utc": "2027-03-06T00:00:00Z",
                "planned_camera_hours": 120,
                "camera_angle": "PRIMARY",
                "dataset_role": "CONFIRMATORY",
                "effort_rule_version": "SYNTHETIC_FIXED_V1",
                "route_outcome_adaptive": "false",
            })
    _write_csv(
        cameras,
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
        camera_rows,
    )

    event_rows: list[dict[str, object]] = []
    event_id = 0
    for s_idx, site in enumerate(("S1", "S2")):
        for p in range(6):
            for m in range(6):
                b = _bypass_count(
                    scenario,
                    site_index=s_idx,
                    plant_index=p,
                    mammal_index=m,
                )
                l = 12 - b
                for route, count in (("B", b), ("L", l)):
                    for _ in range(count):
                        event_id += 1
                        event_rows.append({
                            "event_id": f"E{event_id:05d}",
                            "dataset_role": "CONFIRMATORY",
                            "site_id": site,
                            "plant_species": f"P{p}",
                            "mammal_species": f"M{m}",
                            "timestamp": f"2027-03-{1 + (event_id % 5):02d}T00:00:00Z",
                            "camera_id": f"C_{site}_P{p}",
                            "route_code": route,
                            "visitor_id_confidence": "HIGH",
                            "clip_quality": "PASS",
                        })
    _write_csv(
        events,
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
        ],
        event_rows,
    )
    return {
        "events": events,
        "plants": plants,
        "mammals": mammals,
        "cameras": cameras,
    }


def _synthetic_sakhalkar() -> list[dict[str, float]]:
    return [
        {"tube_length": float(i + 1), "balance": float(i) / 20.0}
        for i in range(20)
    ]


def _synthetic_aubert() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for site in ("A", "B"):
        for i in range(30):
            mismatch = (i - 14.5) / 10.0
            rows.append({
                "site": site,
                "mismatch_log_t_over_b": mismatch,
                "robbery_rate": 1.0 / (1.0 + math.exp(-mismatch)),
            })
    return rows


def run(outdir: str | Path, *, scenario: str = "positive", permutations: int = 199) -> dict[str, object]:
    if scenario not in SCENARIOS:
        raise ValueError(f"scenario must be one of {sorted(SCENARIOS)}")
    root = Path(outdir)
    root.mkdir(parents=True, exist_ok=True)

    presurvey_csv = root / "route_blind_presurvey.csv"
    presurvey_rows = _presurvey_rows()
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
        presurvey_rows,
    )
    presurvey_receipt = root / "route_blind_presurvey_receipt.json"
    presurvey_receipt.write_text(
        json.dumps(evaluate_presurvey(presurvey_rows), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    freeze_path = root / "confirmatory_freeze.json"
    freeze_path.write_text(json.dumps(_freeze_receipt(), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    field_config = _field_config(presurvey_receipt, freeze_path)
    field_config_path = root / "field_readiness_config.json"
    field_config_path.write_text(json.dumps(field_config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    field_receipt_path = root / "field_readiness_receipt.json"
    field_receipt = evaluate_field(field_config, base_dir=root)
    field_receipt_path.write_text(json.dumps(field_receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    raw = _raw_tables(root, scenario)
    manifest_path = root / "input_freeze_manifest.json"
    manifest = freeze_inputs(
        events_csv=raw["events"],
        plant_traits_csv=raw["plants"],
        mammal_traits_csv=raw["mammals"],
        camera_deployment_csv=raw["cameras"],
        confirmatory_freeze_json=freeze_path,
        field_readiness_json=field_receipt_path,
    )
    write_manifest(manifest_path, manifest)

    units_path = root / "third_analysis_units.csv"
    unit_audit_path = root / "third_unit_build_audit.json"
    build_units(
        raw["events"],
        raw["plants"],
        raw["mammals"],
        raw["cameras"],
        freeze_path,
        field_receipt_path,
        manifest_path,
        units_path,
        unit_audit_path,
    )

    third_result_path = root / "third_network_result.json"
    third = run_third(
        units_path,
        third_result_path,
        permutations=permutations,
        seed=20260921,
    )

    from scripts.analyze_third_access_routing_network import load_analysis_units
    third_rows = load_analysis_units(units_path)
    joint = summarize_joint_k3(
        _synthetic_sakhalkar(),
        _synthetic_aubert(),
        third_rows,
        permutations=permutations,
        seed=20260921,
    )
    joint_path = root / "joint_k3_synthetic_result.json"
    joint_path.write_text(json.dumps(joint, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary = {
        "receipt": "BITA_THIRD_NETWORK_SYNTHETIC_E2E_V1",
        "status": "DEVELOPMENT_SYNTHETIC_ONLY",
        "scenario": scenario,
        "permutations": permutations,
        "field_readiness_status": field_receipt["status"],
        "input_freeze_status": manifest["status"],
        "third_gate": third["gate"],
        "third_rho": third["effect"]["rho_site_adjusted_rank"],
        "third_p": third["effect"]["permutation_p_two_sided"],
        "joint_k3_rho": joint["joint_equal_network_fisher_z_rho"],
        "joint_k3_p": joint["joint_permutation_p_two_sided"],
        "network_direction_concordance": joint["network_direction_concordance"],
        "claim_boundary": (
            "Synthetic development output only. It tests plumbing and fail-closed inference contracts; "
            "it is not ecological evidence and must never be cited as a BITA empirical result."
        ),
        "files": {
            path.name: _sha(path)
            for path in (
                presurvey_receipt,
                freeze_path,
                field_receipt_path,
                manifest_path,
                units_path,
                third_result_path,
                joint_path,
            )
        },
    }
    summary_path = root / "synthetic_e2e_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="positive")
    parser.add_argument("--permutations", type=int, default=199)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, scenario=args.scenario, permutations=args.permutations), indent=2, sort_keys=True))
