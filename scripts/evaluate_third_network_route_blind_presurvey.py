"""Evaluate route-blind third-network site feasibility before confirmatory video opening."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

MIN_PLANTS = 5
MIN_MAMMALS = 5

REQUIRED_COLUMNS = {
    "record_id",
    "site_id",
    "record_type",
    "plant_species",
    "mammal_species",
    "evidence_method",
    "flowering_available",
    "camera_operable",
}

FORBIDDEN_COLUMNS = {
    "route_code",
    "bypass",
    "legitimate",
    "b_count",
    "l_count",
    "y_bypass_prop",
    "m_log_ratio",
    "mismatch",
    "access_depth_mm",
    "rostral_reach_mm",
    "robbery_rate",
}


def _read(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS.difference(fields)
        if missing:
            raise ValueError(f"presurvey missing required columns: {sorted(missing)}")
        forbidden = FORBIDDEN_COLUMNS.intersection(fields)
        if forbidden:
            raise ValueError(
                "ROUTE_OR_MORPHOLOGY_FIELD_FORBIDDEN_IN_PRESURVEY: "
                + ",".join(sorted(forbidden))
            )
        return list(reader)


def evaluate_rows(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        raise ValueError("presurvey is empty")

    record_ids = [str(row["record_id"]).strip() for row in rows]
    if any(not value for value in record_ids):
        raise ValueError("record_id must not be blank")
    if len(record_ids) != len(set(record_ids)):
        raise ValueError("record_id must be unique")

    plant_by_site: dict[str, set[str]] = {}
    mammal_by_site: dict[str, set[str]] = {}
    camera_ok: dict[str, bool] = {}
    methods: set[str] = set()

    for row in rows:
        site = str(row["site_id"]).strip()
        kind = str(row["record_type"]).strip().upper()
        method = str(row["evidence_method"]).strip()
        flowering = str(row["flowering_available"]).strip().upper()
        operable = str(row["camera_operable"]).strip().upper()

        if not site:
            raise ValueError("site_id must not be blank")
        if kind not in {"PLANT", "MAMMAL", "CAMERA"}:
            raise ValueError(f"invalid record_type: {kind!r}")
        if not method:
            raise ValueError("evidence_method must not be blank")
        methods.add(method)

        plant_by_site.setdefault(site, set())
        mammal_by_site.setdefault(site, set())
        camera_ok.setdefault(site, False)

        if kind == "PLANT":
            plant = str(row["plant_species"]).strip()
            if not plant:
                raise ValueError("PLANT row requires plant_species")
            if flowering not in {"YES", "NO"}:
                raise ValueError("PLANT flowering_available must be YES or NO")
            if flowering == "YES":
                plant_by_site[site].add(plant)

        elif kind == "MAMMAL":
            mammal = str(row["mammal_species"]).strip()
            if not mammal:
                raise ValueError("MAMMAL row requires mammal_species")
            mammal_by_site[site].add(mammal)

        else:
            if operable not in {"YES", "NO"}:
                raise ValueError("CAMERA camera_operable must be YES or NO")
            if operable == "YES":
                camera_ok[site] = True

    all_sites = sorted(set(plant_by_site) | set(mammal_by_site) | set(camera_ok))
    summaries: dict[str, dict[str, object]] = {}
    eligible: list[str] = []

    for site in all_sites:
        n_plants = len(plant_by_site.get(site, set()))
        n_mammals = len(mammal_by_site.get(site, set()))
        camera = bool(camera_ok.get(site, False))
        gate = n_plants >= MIN_PLANTS and n_mammals >= MIN_MAMMALS and camera
        summaries[site] = {
            "flowering_plant_species": n_plants,
            "mammal_species": n_mammals,
            "camera_operable": camera,
            "route_blind_eligibility_gate": gate,
        }
        if gate:
            eligible.append(site)

    status = (
        "PRESURVEY_ROUTE_BLIND_ELIGIBLE_SITES_PRESENT"
        if eligible
        else "PRESURVEY_NO_ELIGIBLE_SITE"
    )
    return {
        "receipt": "BITA_THIRD_NETWORK_ROUTE_BLIND_PRESURVEY_V1",
        "status": status,
        "minimum_flowering_plant_species": MIN_PLANTS,
        "minimum_mammal_species": MIN_MAMMALS,
        "eligible_sites": eligible,
        "site_summary": summaries,
        "evidence_methods": sorted(methods),
        "route_outcome_fields_present": False,
        "morphology_fields_present": False,
        "claim_boundary": (
            "Eligibility uses only flowering plant richness, mammal presence, and camera operability. "
            "No legitimate/bypass route outcome or access-mismatch morphology is permitted in this presurvey."
        ),
    }


def run(input_csv: str | Path, output_json: str | Path | None = None) -> dict[str, object]:
    result = evaluate_rows(_read(input_csv))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output_json is not None:
        path = Path(output_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("presurvey_csv")
    parser.add_argument("--output")
    args = parser.parse_args()
    print(json.dumps(run(args.presurvey_csv, args.output), indent=2, sort_keys=True))
