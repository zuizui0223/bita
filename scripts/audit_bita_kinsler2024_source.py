"""Source-bound schema/provenance audit for Kinsler et al. 2024.

Author repository (unmodified source files, only aggregate statistics retained):
https://github.com/grantkinsler/EvolvingFront
Original study DOI: 10.1371/journal.pbio.3002848

No clone-level numerator is ever treated as independent evolution-lineage n.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path

SOURCE_COMMIT = "0de5873c853e08e78541cec4f50988f41327af47"
FILE_GIT_BLOBS = {
    "S1_Data.csv": "978383e99eae1065771fd46176095bbf65ca0b81",
    "S3_Data.csv": "8dcb160b94e8877002233a8e7e0e2d62445c46cb",
}
BASE = f"https://raw.githubusercontent.com/grantkinsler/EvolvingFront/{SOURCE_COMMIT}/data"
EXPECTED_S3_COLUMNS = [
    "barcode", "ancestor", "evolution_condition", "class_new", "gene",
    "evolution_fitness_per_cycle", "ResPerHour", "FerPerHour",
    "Fit2D_early_fitness", "isolated_evolution_condition",
]


def verify_git_source(data: bytes, path: str) -> dict:
    """Git content-addressed blob SHA (including Git blob header), not SHA256."""
    name = Path(path).name
    expected = FILE_GIT_BLOBS[name]
    sha = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if sha != expected:
        raise ValueError(f"author Git blob hash mismatch for {name}")
    return {
        "file": name,
        "git_blob_sha1": sha,
        "source_bytes": len(data),
        "bytes_sha256": hashlib.sha256(data).hexdigest(),
    }


def read_csv(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text = data.decode("utf-8-sig")
    f = io.StringIO(text, newline="")
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    if not headers or len(headers) != len(set(headers)):
        raise ValueError("missing or duplicated CSV header names")
    rows = list(reader)
    if not rows:
        raise ValueError("empty source CSV")
    if any(None in row for row in rows):
        raise ValueError("unparsed CSV surplus-field error")
    return headers, rows


def describe_rows(headers: list[str], rows: list[dict[str, str]]) -> dict:
    def counts(col: str, limit: int = 40) -> dict:
        vals = collections.Counter(str(r.get(col, "")) for r in rows)
        if len(vals) > limit:
            return {
                "distinct_values": len(vals), "too_many_values_to_inline": True,
                "empty_rows": vals.get("", 0),
            }
        return dict(sorted(vals.items()))
    categories = {}
    for col in (
        "ancestor", "evolution_condition", "isolated_evolution_condition",
        "class_new", "class", "ploidy", "source", "source_data",
        "mutation_class", "is_adaptive", "is_parental", "source_evolution",
        "evolution_replicate", "evolution_rep", "status"
    ):
        if col in headers:
            categories[col] = counts(col)
    missing = {k: sum(v.get(k, "").strip().lower() in {"", "nan", "na", "none"}
                      for v in rows) for k in headers}
    high_missing = {k: v for k, v in missing.items() if v > 0}
    distincts = {k: len({str(row.get(k, "")) for row in rows}) for k in headers}
    return {
        "rows": len(rows),
        "columns": len(headers),
        "headers": headers,
        "category_counts": categories,
        "columns_with_missing": high_missing,
        "column_distinct_counts": distincts,
        "barcode_presence": "barcode" in headers,
        "distinct_barcode_count": len({row["barcode"] for row in rows}) if "barcode" in headers else None,
    }


def audit_files(s1: bytes, s3: bytes) -> dict:
    sources = {
        "S1_Data.csv": verify_git_source(s1, "S1_Data.csv"),
        "S3_Data.csv": verify_git_source(s3, "S3_Data.csv"),
    }
    headers1, rows1 = read_csv(s1)
    headers3, rows3 = read_csv(s3)
    if headers3 != EXPECTED_S3_COLUMNS:
        raise ValueError(f"Unexpected author S3 source schema: {headers3!r}")
    s1data = describe_rows(headers1, rows1)
    s3data = describe_rows(headers3, rows3)
    if len(rows3) != 185 or len(set(r["barcode"] for r in rows3)) != 185:
        raise ValueError("S3 subset is not the original 185 distinct selected barcodes")
    cross = {
        "s1_barcode_column_exists": "barcode" in headers1,
        "s1_s3_barcode_overlap_count": None,
        "s3_not_in_s1_count": None,
        "s1_duplicate_barcode_rows": None,
        "s3_all_185_evo2d": all(r["evolution_condition"] == "Evo2D" for r in rows3),
        "s3_all_isolated_R2": all(r["isolated_evolution_condition"].endswith("_R2") for r in rows3),
    }
    if "barcode" in headers1:
        bc1 = [r["barcode"] for r in rows1]
        b1, b3 = set(bc1), {r["barcode"] for r in rows3}
        cross["s1_s3_barcode_overlap_count"] = len(b1 & b3)
        cross["s3_not_in_s1_count"] = len(b3 - b1)
        cross["s1_duplicate_barcode_rows"] = len(bc1) - len(b1)
    return {
        "source_study": "Kinsler_et_al_2024_PLoS_Biology",
        "primary_doi": "10.1371/journal.pbio.3002848",
        "author_repo": "grantkinsler/EvolvingFront",
        "author_repo_commit": SOURCE_COMMIT,
        "source_access": "author_public_GitHub_files_pinned_by_Git_object_SHA",
        "source_git_blobs": sources,
        "S1_original_source_schema_and_counts": s1data,
        "S3_original_source_schema_and_counts": s3data,
        "source_barcode_cross_checks": cross,
        "interpretation_ceiling": {
            "S3_is_selected_185_barcode_subset_not_185_evolving_populations": True,
            "source_raw_data_not_copied_to_own_repo": True,
            "no_causal_architecture_splitting_claim": True,
            "new_independent_publication_from_DSouza2016": True,
            "different_ancestor_genotypes_and_assay_phases_need_explicit_conditioning": True,
            "further_reanalysis_awaits_full_S1_schema_adjudication": True,
        },
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--s1", type=Path, required=True)
    p.add_argument("--s3", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = audit_files(args.s1.read_bytes(), args.s3.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    print("BITA_KINSLER_SOURCE_INVENTORY:" + json.dumps({
        "s1_rows": report["S1_original_source_schema_and_counts"]["rows"],
        "s1_headers": report["S1_original_source_schema_and_counts"]["headers"],
        "s1_categories": report["S1_original_source_schema_and_counts"]["category_counts"],
        "s3_rows": report["S3_original_source_schema_and_counts"]["rows"],
        "s3_categories": report["S3_original_source_schema_and_counts"]["category_counts"],
        "barcode_cross": report["source_barcode_cross_checks"],
    }, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
