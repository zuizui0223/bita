"""Evaluate outcome-blind Cape collaboration replies.

This evaluator never reads or stores the direction/magnitude of historical
access-routing outcomes. It applies predeclared contamination quarantine and
selects the earliest route-blind feasible collaboration response.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path

INTAKE_REQUIRED = {
    "response_id",
    "contact_id",
    "received_utc",
    "candidate_site_id",
    "region",
    "flowering_plant_species_count",
    "mammal_species_count",
    "flowering_window",
    "camera_feasible",
    "plant_access_depth_feasible",
    "mammal_rostral_morphometrics_feasible",
    "land_permit_ethics_path_identified",
    "collaboration_interest",
    "outcome_exposure_flag",
}
EXPOSURE_REQUIRED = {
    "exposure_id",
    "response_id",
    "exposure_level",
    "site_id",
    "plant_species",
    "mammal_species",
    "recorded_without_direction",
    "required_action",
}
FORBIDDEN_INTAKE_COLUMNS = {
    "route_code",
    "b_count",
    "l_count",
    "y_bypass_prop",
    "bypass_rate",
    "robbery_rate",
    "route_effect",
    "route_coefficient",
    "route_p_value",
    "m_log_ratio",
    "mismatch_route_association",
    "historical_route_direction",
}
YES_NO_UNCERTAIN = {"YES", "NO", "UNCERTAIN"}
INTEREST = {"YES", "NO", "MAYBE"}
EXPOSURE_FLAGS = {"NONE", "EXPOSED"}
EXPOSURE_LEVELS = {"SITE", "PLANT", "MAMMAL", "GENERAL"}
EXPECTED_ACTION = {
    "SITE": "QUARANTINE_SITE",
    "PLANT": "NO_TAXON_CHERRY_PICKING",
    "MAMMAL": "NO_TAXON_CHERRY_PICKING",
    "GENERAL": "FEASIBILITY_CONTEXT_ONLY",
}
MIN_PLANTS = 5
MIN_MAMMALS = 5


def _read(path: str | Path, required: set[str], label: str) -> tuple[list[str], list[dict[str, str]]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        missing = required.difference(fields)
        if missing:
            raise ValueError(f"{label} missing required columns: {sorted(missing)}")
        rows = list(reader)
    return fields, rows


def _parse_utc(value: str) -> dt.datetime:
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError("received_utc must be ISO-8601 datetime") from exc
    if parsed.tzinfo is None:
        raise ValueError("received_utc must include timezone")
    return parsed.astimezone(dt.timezone.utc)


def _count(value: str, label: str) -> int:
    try:
        number = int(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be integer") from exc
    if number < 0:
        raise ValueError(f"{label} must be >=0")
    return number


def evaluate(
    intake_rows: list[dict[str, str]],
    exposure_rows: list[dict[str, str]],
) -> dict[str, object]:
    if not intake_rows:
        raise ValueError("collaboration intake is empty")

    response_ids = [str(row["response_id"]).strip() for row in intake_rows]
    if any(not value for value in response_ids):
        raise ValueError("response_id must not be blank")
    if len(response_ids) != len(set(response_ids)):
        raise ValueError("response_id must be unique")

    exposures_by_response: dict[str, list[dict[str, str]]] = {}
    site_quarantine: set[str] = set()
    taxon_exposure = False
    exposure_audit: list[dict[str, str]] = []

    exposure_ids: set[str] = set()
    for row in exposure_rows:
        exposure_id = str(row["exposure_id"]).strip()
        response_id = str(row["response_id"]).strip()
        level = str(row["exposure_level"]).strip().upper()
        recorded = str(row["recorded_without_direction"]).strip().lower()
        action = str(row["required_action"]).strip().upper()

        if not exposure_id or exposure_id in exposure_ids:
            raise ValueError("exposure_id must be unique and nonblank")
        exposure_ids.add(exposure_id)

        if response_id not in set(response_ids):
            raise ValueError(f"exposure references unknown response_id: {response_id}")
        if level not in EXPOSURE_LEVELS:
            raise ValueError(f"invalid exposure_level: {level!r}")
        if recorded != "true":
            raise ValueError("EXPOSURE_DIRECTION_MUST_NOT_BE_RECORDED")
        if action != EXPECTED_ACTION[level]:
            raise ValueError(
                f"incorrect required_action for {level}: expected {EXPECTED_ACTION[level]}"
            )

        site = str(row["site_id"]).strip()
        plant = str(row["plant_species"]).strip()
        mammal = str(row["mammal_species"]).strip()

        if level == "SITE":
            if not site:
                raise ValueError("SITE exposure requires site_id")
            site_quarantine.add(site)
        elif level == "PLANT":
            if not plant:
                raise ValueError("PLANT exposure requires plant_species")
            taxon_exposure = True
        elif level == "MAMMAL":
            if not mammal:
                raise ValueError("MAMMAL exposure requires mammal_species")
            taxon_exposure = True

        normalized = {
            "exposure_id": exposure_id,
            "response_id": response_id,
            "exposure_level": level,
            "site_id": site,
            "plant_species": plant,
            "mammal_species": mammal,
            "required_action": action,
        }
        exposures_by_response.setdefault(response_id, []).append(normalized)
        exposure_audit.append(normalized)

    normalized_responses: list[dict[str, object]] = []
    for row in intake_rows:
        response_id = str(row["response_id"]).strip()
        site = str(row["candidate_site_id"]).strip()
        contact = str(row["contact_id"]).strip()
        region = str(row["region"]).strip()
        flowering = str(row["flowering_window"]).strip()
        exposure_flag = str(row["outcome_exposure_flag"]).strip().upper()

        if not site or not contact or not region or not flowering:
            raise ValueError("contact/site/region/flowering fields must not be blank")
        if exposure_flag not in EXPOSURE_FLAGS:
            raise ValueError(f"invalid outcome_exposure_flag: {exposure_flag!r}")

        linked_exposures = exposures_by_response.get(response_id, [])
        if exposure_flag == "EXPOSED" and not linked_exposures:
            raise ValueError("EXPOSED response requires exposure registry row")
        if exposure_flag == "NONE" and linked_exposures:
            raise ValueError("NONE response cannot have exposure registry row")

        plant_n = _count(
            row["flowering_plant_species_count"],
            "flowering_plant_species_count",
        )
        mammal_n = _count(row["mammal_species_count"], "mammal_species_count")

        flags: dict[str, str] = {}
        for key in (
            "camera_feasible",
            "plant_access_depth_feasible",
            "mammal_rostral_morphometrics_feasible",
            "land_permit_ethics_path_identified",
        ):
            value = str(row[key]).strip().upper()
            if value not in YES_NO_UNCERTAIN:
                raise ValueError(f"invalid {key}: {value!r}")
            flags[key] = value

        interest = str(row["collaboration_interest"]).strip().upper()
        if interest not in INTEREST:
            raise ValueError(f"invalid collaboration_interest: {interest!r}")

        quarantined = site in site_quarantine
        feasible = (
            plant_n >= MIN_PLANTS
            and mammal_n >= MIN_MAMMALS
            and all(value == "YES" for value in flags.values())
            and interest == "YES"
            and not quarantined
        )

        normalized_responses.append(
            {
                "response_id": response_id,
                "contact_id": contact,
                "received_utc": _parse_utc(row["received_utc"]),
                "candidate_site_id": site,
                "region": region,
                "flowering_plant_species_count": plant_n,
                "mammal_species_count": mammal_n,
                **flags,
                "collaboration_interest": interest,
                "outcome_exposure_flag": exposure_flag,
                "site_quarantined": quarantined,
                "route_blind_feasible": feasible,
            }
        )

    feasible = sorted(
        (row for row in normalized_responses if row["route_blind_feasible"]),
        key=lambda row: (row["received_utc"], str(row["response_id"])),
    )
    selected = feasible[0] if feasible else None

    def _serializable(row: dict[str, object]) -> dict[str, object]:
        out = dict(row)
        if isinstance(out.get("received_utc"), dt.datetime):
            out["received_utc"] = out["received_utc"].isoformat()
        return out

    return {
        "receipt": "BITA_THIRD_NETWORK_COLLABORATION_INTAKE_V1",
        "status": (
            "ROUTE_BLIND_COLLABORATION_SELECTED"
            if selected is not None
            else "NO_ROUTE_BLIND_FEASIBLE_COLLABORATION_YET"
        ),
        "selected_response": _serializable(selected) if selected else None,
        "site_quarantine": sorted(site_quarantine),
        "taxon_exposure_requires_no_cherry_picking": taxon_exposure,
        "responses": [_serializable(row) for row in normalized_responses],
        "exposure_audit_without_direction": exposure_audit,
        "stopping_rule": (
            "Select the earliest response that passes all route-blind feasibility gates; "
            "do not continue shopping for a historically more favorable route outcome."
        ),
        "claim_boundary": (
            "Collaboration replies are feasibility inputs only and contribute no B, L, Y, M, r_T, or k=3 observations."
        ),
    }


def run(
    intake_csv: str | Path,
    exposure_csv: str | Path,
    output_json: str | Path | None = None,
) -> dict[str, object]:
    intake_fields, intake_rows = _read(intake_csv, INTAKE_REQUIRED, "intake")
    forbidden = FORBIDDEN_INTAKE_COLUMNS.intersection(intake_fields)
    if forbidden:
        raise ValueError(
            "ROUTE_OUTCOME_COLUMN_FORBIDDEN_IN_COLLABORATION_INTAKE: "
            + ",".join(sorted(forbidden))
        )

    _exposure_fields, exposure_rows = _read(
        exposure_csv,
        EXPOSURE_REQUIRED,
        "exposure_registry",
    )

    result = evaluate(intake_rows, exposure_rows)
    if output_json is not None:
        path = Path(output_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("intake_csv")
    parser.add_argument("exposure_csv")
    parser.add_argument("--output")
    args = parser.parse_args()
    print(json.dumps(run(args.intake_csv, args.exposure_csv, args.output), indent=2, sort_keys=True))
