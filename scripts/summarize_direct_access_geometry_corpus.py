"""Validate and summarize the direct access-geometry -> robbery discovery corpus.

This corpus is supporting evidence only. The script deliberately does not compute
a p-value, sign test, pooled effect, or network-k statistic.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1.csv"
)

REQUIRED_COLUMNS = (
    "study_id",
    "year",
    "doi",
    "fauna",
    "plant_scope",
    "study_scale",
    "access_predictor",
    "robbery_outcome",
    "direction",
    "effect_detail",
    "network_k_eligible",
    "reason_not_k",
    "source_role",
    "notes",
)
ALLOWED_DIRECTIONS = {"POSITIVE", "NULL", "OPPOSITE", "MIXED"}
ALLOWED_K = {"YES", "NO"}


def summarize(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        rows = list(reader)

    if fieldnames != REQUIRED_COLUMNS:
        raise ValueError(
            "DIRECT_CORPUS_SCHEMA_MISMATCH:"
            f"expected={REQUIRED_COLUMNS}:observed={fieldnames}"
        )
    if not rows:
        raise ValueError("DIRECT_CORPUS_EMPTY")

    study_ids = [row["study_id"].strip() for row in rows]
    if any(not value for value in study_ids):
        raise ValueError("DIRECT_CORPUS_EMPTY_STUDY_ID")
    if len(set(study_ids)) != len(study_ids):
        raise ValueError("DIRECT_CORPUS_DUPLICATE_STUDY_ID")

    invalid_direction = sorted(
        {
            row["direction"].strip()
            for row in rows
            if row["direction"].strip() not in ALLOWED_DIRECTIONS
        }
    )
    if invalid_direction:
        raise ValueError("DIRECT_CORPUS_INVALID_DIRECTION:" + ",".join(invalid_direction))

    invalid_k = sorted(
        {
            row["network_k_eligible"].strip()
            for row in rows
            if row["network_k_eligible"].strip() not in ALLOWED_K
        }
    )
    if invalid_k:
        raise ValueError("DIRECT_CORPUS_INVALID_K_FLAG:" + ",".join(invalid_k))

    k_eligible = [row for row in rows if row["network_k_eligible"].strip() == "YES"]
    if k_eligible:
        raise ValueError(
            "DIRECT_CORPUS_CANNOT_PROMOTE_NETWORK_K:"
            + ",".join(row["study_id"] for row in k_eligible)
        )

    for row in rows:
        if not row["access_predictor"].strip():
            raise ValueError(f"DIRECT_CORPUS_MISSING_ACCESS_PREDICTOR:{row['study_id']}")
        if not row["robbery_outcome"].strip():
            raise ValueError(f"DIRECT_CORPUS_MISSING_ROBBERY_OUTCOME:{row['study_id']}")
        if not row["reason_not_k"].strip():
            raise ValueError(f"DIRECT_CORPUS_MISSING_K_EXCLUSION:{row['study_id']}")

    direction_counts = Counter(row["direction"].strip() for row in rows)
    fauna_counts = Counter(row["fauna"].strip() for row in rows)

    return {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1",
        "status": "DISCOVERY_SUPPORT_ONLY_NOT_NETWORK_K",
        "study_programs": len(rows),
        "direction_counts": {
            key: direction_counts.get(key, 0)
            for key in ("POSITIVE", "NULL", "OPPOSITE", "MIXED")
        },
        "fauna_counts": dict(sorted(fauna_counts.items())),
        "network_k_contribution": 0,
        "primary_joint_network_k_remains": 2,
        "formal_recurrence_test_permitted": False,
        "claim": (
            "Direct access-geometry/robbery tests extend beyond the two standardized "
            "networks, but this discovery corpus cannot be used as a prevalence "
            "estimate, sign test, pooled effect, or additional network replicate."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = summarize(args.corpus)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
