"""Apply a compact frozen decision overlay to a regenerated priority-leak packet.

The overlay preserves the packet as the retrieval receipt while recording only
human source-screen and target-route decisions.  It does not create live
route-record registry entries or effect estimates.
"""

from __future__ import annotations

import csv
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


def apply_overlay(
    packet_rows: Iterable[dict[str, str]], overlay_rows: Iterable[dict[str, str]]
) -> list[dict[str, str]]:
    """Return a fully validated coding sheet with decisions layered onto the packet."""
    packet_rows = list(packet_rows)
    sheet = make_sheet(packet_rows)
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
