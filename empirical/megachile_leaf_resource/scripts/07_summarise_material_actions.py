#!/usr/bin/env python3
"""Summarise observation-first material-action evidence and plant-ID yield."""

from __future__ import annotations
import argparse
import csv
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    with args.input.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    confirmed = [row for row in rows if row.get("action_status") == "material_action_confirmed"]
    plant_identified = [row for row in confirmed if row.get("plant_taxon_status") in {"accepted", "synonym_resolved", "genus_only"}]
    species_ready = [row for row in confirmed if row.get("plant_taxon_status") in {"accepted", "synonym_resolved"}]
    print(f"candidate records: {len(rows)}")
    print(f"confirmed material actions: {len(confirmed)}")
    print(f"plant named at any rank: {len(plant_identified)}")
    print(f"species-level trait-ready plants: {len(species_ready)}")
    print("action types:")
    for action, count in sorted(Counter(row.get("action_type", "") for row in confirmed).items()):
        print(f"  {action}: {count}")


if __name__ == "__main__":
    main()
