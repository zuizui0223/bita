"""Evaluate route-blind collaboration response extracts for the prospective k=3 network."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ALLOWED_COLUMNS = {
    "response_id",
    "source_contact",
    "response_date",
    "candidate_site_id",
    "candidate_region",
    "plant_species",
    "mammal_species",
    "flowering_window",
    "camera_feasible",
    "plant_depth_feasible",
    "mammal_morph_source_available",
    "land_permit_path_known",
    "ethics_path_known",
    "collaboration_interest",
    "outcome_exposure_status",
    "exposure_scope_id",
    "notes_route_blind",
}
REQUIRED_COLUMNS = ALLOWED_COLUMNS
YES_NO_UNKNOWN = {"YES", "NO", "UNKNOWN"}
INTEREST = {"YES", "NO", "MAYBE", "UNKNOWN"}
EXPOSURE = {
    "CLEAN",
    "GENERIC_ONLY",
    "SITE_EXPOSED",
    "PLANT_EXPOSED",
    "MAMMAL_EXPOSED",
    "SYSTEM_EXPOSED",
}

FORBIDDEN_COLUMN_TOKENS = {
    "route_code",
    "b_count",
    "l_count",
    "bypass_prop",
    "y_bypass",
    "robbery_rate",
    "mismatch",
    "m_log_ratio",
    "p_value",
    "coefficient",
    "rho",
}


def _read(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS.difference(fields)
        if missing:
            raise ValueError(f"response extract missing required columns: {sorted(missing)}")
        extra = fields.difference(ALLOWED_COLUMNS)
        if extra:
            raise ValueError(f"response extract has non-schema columns: {sorted(extra)}")
        lower_fields = {field.lower() for field in fields}
        forbidden = {
            field for field in lower_fields
            if any(token in field for token in FORBIDDEN_COLUMN_TOKENS)
        }
        if forbidden:
            raise ValueError(
                "OUTCOME_FIELD_FORBIDDEN_IN_COLLABORATION_EXTRACT: "
                + ",".join(sorted(forbidden))
            )
        return list(reader)


def evaluate_rows(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        raise ValueError("collaboration response extract is empty")

    ids = [str(row["response_id"]).strip() for row in rows]
    if any(not value for value in ids):
        raise ValueError("response_id must not be blank")
    if len(ids) != len(set(ids)):
        raise ValueError("response_id must be unique")

    sites: set[str] = set()
    plants: set[str] = set()
    mammals: set[str] = set()

    exposed_sites: set[str] = set()
    exposed_plants: set[str] = set()
    exposed_mammals: set[str] = set()
    system_exposed = False

    site_logistics: dict[str, dict[str, bool]] = {}

    for row in rows:
        site = str(row["candidate_site_id"]).strip()
        if not site:
            raise ValueError("candidate_site_id must not be blank")
        sites.add(site)

        plant = str(row["plant_species"]).strip()
        mammal = str(row["mammal_species"]).strip()
        if plant:
            plants.add(plant)
        if mammal:
            mammals.add(mammal)

        for field in (
            "camera_feasible",
            "plant_depth_feasible",
            "mammal_morph_source_available",
            "land_permit_path_known",
            "ethics_path_known",
        ):
            value = str(row[field]).strip().upper()
            if value not in YES_NO_UNKNOWN:
                raise ValueError(f"{field} must be YES, NO or UNKNOWN")

        interest = str(row["collaboration_interest"]).strip().upper()
        if interest not in INTEREST:
            raise ValueError("collaboration_interest has invalid value")

        exposure = str(row["outcome_exposure_status"]).strip().upper()
        if exposure not in EXPOSURE:
            raise ValueError(f"invalid outcome_exposure_status: {exposure!r}")

        scope = str(row["exposure_scope_id"]).strip()
        if exposure == "SITE_EXPOSED":
            if not scope:
                raise ValueError("SITE_EXPOSED requires exposure_scope_id")
            exposed_sites.add(scope)
        elif exposure == "PLANT_EXPOSED":
            if not scope:
                raise ValueError("PLANT_EXPOSED requires exposure_scope_id")
            exposed_plants.add(scope)
        elif exposure == "MAMMAL_EXPOSED":
            if not scope:
                raise ValueError("MAMMAL_EXPOSED requires exposure_scope_id")
            exposed_mammals.add(scope)
        elif exposure == "SYSTEM_EXPOSED":
            system_exposed = True

        logistics = site_logistics.setdefault(
            site,
            {
                "camera_feasible": False,
                "plant_depth_feasible": False,
                "land_permit_path_known": False,
                "ethics_path_known": False,
                "collaboration_interest": False,
            },
        )
        logistics["camera_feasible"] |= str(row["camera_feasible"]).strip().upper() == "YES"
        logistics["plant_depth_feasible"] |= str(row["plant_depth_feasible"]).strip().upper() == "YES"
        logistics["land_permit_path_known"] |= str(row["land_permit_path_known"]).strip().upper() == "YES"
        logistics["ethics_path_known"] |= str(row["ethics_path_known"]).strip().upper() == "YES"
        logistics["collaboration_interest"] |= interest in {"YES", "MAYBE"}

    clean_sites = sorted(sites.difference(exposed_sites))
    clean_plants = sorted(plants.difference(exposed_plants))
    clean_mammals = sorted(mammals.difference(exposed_mammals))

    if system_exposed:
        status = "SYSTEM_OUTCOME_EXPOSED_CONFIRMATORY_LANE_BLOCKED"
        clean_sites = []
        clean_plants = []
        clean_mammals = []
    elif clean_sites:
        status = "ROUTE_BLIND_COLLABORATION_POOL_AVAILABLE"
    else:
        status = "NO_CLEAN_COLLABORATION_SITE_POOL"

    route_blind_site_candidates = [
        site
        for site in clean_sites
        if all(site_logistics[site].values())
    ]

    return {
        "receipt": "BITA_THIRD_NETWORK_COLLABORATION_RESPONSE_V1",
        "status": status,
        "candidate_sites_clean": clean_sites,
        "candidate_plants_clean": clean_plants,
        "candidate_mammals_clean": clean_mammals,
        "route_blind_logistically_ready_sites": route_blind_site_candidates,
        "quarantine": {
            "exposed_sites": sorted(exposed_sites),
            "exposed_plants": sorted(exposed_plants),
            "exposed_mammals": sorted(exposed_mammals),
            "system_exposed": system_exposed,
        },
        "claim_boundary": (
            "This receipt extracts route-blind feasibility only. It does not establish field eligibility, "
            "does not replace the route-blind presurvey, and contains no route outcome direction or value."
        ),
    }


def run(path: str | Path, output: str | Path | None = None) -> dict[str, object]:
    result = evaluate_rows(_read(path))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output is not None:
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("response_extract_csv")
    parser.add_argument("--output")
    args = parser.parse_args()
    print(json.dumps(run(args.response_extract_csv, args.output), indent=2, sort_keys=True))
