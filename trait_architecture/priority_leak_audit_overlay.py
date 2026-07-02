"""Apply compact frozen decisions to a regenerated priority-leak audit packet.

The packet remains the retrieval receipt.  This module records source-screen and
target-route decisions only; it does not create live registry entries, effects,
or effect directions.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable

from trait_architecture.priority_leak_audit_adjudication import (
    FIELDS,
    PACKET,
    SOURCE,
    check_sheet,
    key,
    make_sheet,
    text,
)

IDENTITY_FIELDS = PACKET[:4]
OVERLAY_FIELDS = (
    *IDENTITY_FIELDS,
    "doi",
    *SOURCE,
    "route_screen_status",
    "route_screen_reason",
    "source_locator",
    "coder_id",
    "coding_date",
    "coding_note",
)
UPDATE_FIELDS = tuple(field for field in OVERLAY_FIELDS if field not in {*IDENTITY_FIELDS, "doi"})

ABSENCE_REASONS = {
    "A_to_pollination": "Abstract does not assess a declared floral attraction/access trait against a pollination response.",
    "A_to_antagonism": "Abstract does not assess a declared floral attraction/display trait against a floral-antagonism response.",
    "B_to_antagonism": "Abstract does not assess a declared flower-specific resistance/access trait against a floral-antagonism response.",
    "B_to_pollination": "Abstract does not assess a declared flower-specific resistance/access trait against a pollination response.",
    "joint_channels": "Abstract does not jointly assess pollination and antagonism in the same study.",
}


def read_overlay(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{name: text(value) for name, value in row.items()} for row in csv.DictReader(handle)]
    seen: set[tuple[str, str, str, str]] = set()
    for index, row in enumerate(rows, start=1):
        missing = [field for field in OVERLAY_FIELDS if field not in row]
        if missing:
            raise ValueError(f"overlay row {index} lacks fields: {', '.join(missing)}")
        identity = tuple(row[field] for field in IDENTITY_FIELDS)
        if not all(identity) or identity in seen:
            raise ValueError(f"overlay row {index} has blank or duplicate audit identity")
        seen.add(identity)
    return rows


def _study_id(row: dict[str, str]) -> str:
    value = text(row.get("doi")) or text(row.get("candidate_id"))
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _apply_overlay(sheet: list[dict[str, str]], overlay_rows: Iterable[dict[str, str]]) -> None:
    sheet_by_identity = {key(row): row for row in sheet}
    for overlay in overlay_rows:
        identity = tuple(overlay[field] for field in IDENTITY_FIELDS)
        if identity not in sheet_by_identity:
            raise ValueError(f"overlay row is not in the frozen packet: {identity}")
        target = sheet_by_identity[identity]
        if text(overlay["doi"]) != text(target["doi"]):
            raise ValueError(f"overlay DOI does not match frozen packet for {identity}")
        for field in UPDATE_FIELDS:
            target[field] = text(overlay[field])


def apply_overlay(
    packet_rows: Iterable[dict[str, str]], overlay_rows: Iterable[dict[str, str]]
) -> list[dict[str, str]]:
    """Layer explicit decisions onto an otherwise unassessed frozen packet."""
    packet_rows = list(packet_rows)
    sheet = make_sheet(packet_rows)
    _apply_overlay(sheet, overlay_rows)
    check_sheet(sheet, packet_rows=packet_rows)
    return sheet


def materialize_abstract_adjudication(
    packet_rows: Iterable[dict[str, str]], overlay_rows: Iterable[dict[str, str]]
) -> list[dict[str, str]]:
    """Recreate v1: all deposited abstracts were reviewed; exceptions are overlaid.

    Every row with a deposited Crossref abstract starts as a usable source whose
    *target audit route* was not directly assessed.  Explicit overlay rows then
    replace that default for direct-route hits, non-primary exclusions, and the
    one unusable metadata record.  Rows without a deposited abstract remain
    unassessed.
    """
    packet_rows = list(packet_rows)
    sheet = make_sheet(packet_rows)
    for row in sheet:
        if row["crossref_abstract_available"] != "true":
            continue
        study_id = _study_id(row)
        row.update({
            "source_screen_status": "included_for_source_coding",
            "source_access_status": "abstract_only",
            "study_type": "other",
            "taxon": "not extracted at abstract-screen resolution",
            "primary_study_id": study_id,
            "study_cluster_id": f"{study_id}_panel",
            "screen_exclusion_reason": "",
            "route_screen_status": "direct_route_absent",
            "route_screen_reason": ABSENCE_REASONS[row["route_family_audit"]],
            "source_locator": "Crossref deposited abstract",
            "coder_id": "assistant_abstract_screen",
            "coding_date": "2026-07-02",
            "coding_note": "Abstract-level priority-leak audit; not promoted to the live direction registry.",
        })
    _apply_overlay(sheet, overlay_rows)
    check_sheet(sheet, packet_rows=packet_rows)
    return sheet


def write_overlay(path: str | Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OVERLAY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_sheet(path: str | Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
    check_sheet(rows)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
