"""Score a screened Megachile leaf-material-use study registry.

The script does not download papers or infer evidence. It makes the
predeclared feasibility gates reproducible after human screening.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path


def truth(value: str) -> bool:
    return value.strip().lower() in {"yes", "true", "1"}


def main(path: str) -> int:
    rows = list(csv.DictReader(Path(path).open(encoding="utf-8")))
    real = [row for row in rows if row.get("study_id", "").strip() and not row["study_id"].startswith("EXAMPLE_")]
    target_a = [row for row in real if truth(row.get("target_a_eligible", ""))]
    target_b = [row for row in real if truth(row.get("target_b_eligible", ""))]
    eligible = target_a + [row for row in target_b if row not in target_a]
    landscapes = {(row.get("study_id", ""), row.get("landscape_id", ""), row.get("sampling_years", "")) for row in eligible}
    regions = {row.get("region", "").strip() for row in eligible if row.get("region", "").strip()}
    plant_records = sum(int(row.get("plant_use_record_count", "0") or 0) for row in eligible)
    plant_taxa = sum(int(row.get("accepted_plant_taxa_count", "0") or 0) for row in eligible)
    routes = Counter(row.get("source_route", "unknown") for row in real)

    print(f"screened studies: {len(real)}")
    print(f"Target A eligible: {len(target_a)}")
    print(f"Target B eligible: {len(target_b)}")
    print(f"independent study-landscapes: {len(landscapes)}")
    print(f"regions: {len(regions)}")
    print(f"plant-level use records: {plant_records}")
    print(f"sum of accepted plant taxa (not deduplicated across studies): {plant_taxa}")
    print("source-route screening counts:")
    for route, count in sorted(routes.items()):
        print(f"  {route}: {count}")

    if len(target_a) >= 7 and len(landscapes) >= 10 and plant_records >= 500:
        print("decision: selection_meta_analysis_ready")
    elif len(landscapes) >= 8 and len(regions) >= 3 and plant_records >= 300:
        print("decision: provisional_comparative_analysis_ready")
    elif len(landscapes) >= 5 and plant_records >= 150:
        print("decision: descriptive_synthesis_ready")
    else:
        print("decision: continue_adaptive_discovery")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python score_registry.py path/to/study_registry.csv")
    raise SystemExit(main(sys.argv[1]))
