"""Audit aggregate coding domains and publication dependence in Sasidharan et al. 2023 Table S1.

This helper deliberately writes aggregate counts only. It never persists observation-level
rows from the deposited workbook. The goal is to fix the source coding before fitting the
predeclared bita reproduction/sensitivity analysis.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import io
import json
import re
import statistics
from pathlib import Path
from typing import Any

from audit_sasidharan2023_pmc_supplement import (
    _download_package,
    _oa_package_url,
    _supplement_from_package,
)

SHEET = "S1"
DOMAIN_COLUMNS = (
    "Insect function",
    "Detection",
    "GC-EAD or EAG or SCR/SSR",
    "Physio_resp",
    "Physio_No_resp",
    "Behaviour_test",
    "Behaviour choice",
    "Behaviour_pos",
    "Behaviour_neg",
    "No_behav_reps",
)
REFERENCE_COLUMN = "Reference (doi TBA)"
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.I)


def _value_key(value: Any) -> str:
    if value is None:
        return "<missing>"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        if float(value).is_integer():
            return str(int(value))
        return str(value)
    text = re.sub(r"\s+", " ", str(value).strip())
    return text if text else "<missing>"


def _cluster_key(reference: Any) -> tuple[str, bool]:
    text = "" if reference is None else re.sub(r"\s+", " ", str(reference).strip())
    if not text:
        return "<missing>", False
    match = DOI_RE.search(text)
    if match:
        doi = match.group(0).rstrip(".,;)").lower()
        return f"doi:{doi}", True
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    return f"ref:{normalized}", False


def run(output_path: str | Path) -> dict[str, Any]:
    import openpyxl  # type: ignore

    oa_url = _oa_package_url()
    package, package_url, package_attempts = _download_package(oa_url)
    supplement_name, supplement, _ = _supplement_from_package(package)
    workbook = openpyxl.load_workbook(io.BytesIO(supplement), read_only=True, data_only=True)
    ws = workbook[SHEET]

    rows = ws.iter_rows(values_only=True)
    headers_raw = next(rows)
    headers = ["" if value is None else str(value).strip() for value in headers_raw]
    index = {name: i for i, name in enumerate(headers) if name}
    missing_required = [name for name in (*DOMAIN_COLUMNS, REFERENCE_COLUMN, "Compound", "Genus", "Insect species") if name not in index]
    if missing_required:
        raise RuntimeError(f"missing expected S1 columns: {missing_required}; headers={headers}")

    domains = {column: Counter() for column in DOMAIN_COLUMNS}
    cluster_rows: Counter[str] = Counter()
    cluster_genera: dict[str, set[str]] = defaultdict(set)
    cluster_roles: dict[str, set[str]] = defaultdict(set)
    cluster_fvocs: dict[str, set[str]] = defaultdict(set)
    raw_reference_strings: set[str] = set()
    doi_rows = 0
    missing_reference_rows = 0
    analyzed_rows = 0

    for row in rows:
        if not any(value is not None and str(value).strip() for value in row):
            continue
        compound = row[index["Compound"]]
        insect = row[index["Insect species"]]
        role = row[index["Insect function"]]
        # Ignore footnotes/trailing notes that do not identify a test row.
        if not (compound and insect and role):
            continue
        analyzed_rows += 1
        for column in DOMAIN_COLUMNS:
            domains[column][_value_key(row[index[column]])] += 1

        reference = row[index[REFERENCE_COLUMN]]
        if reference is None or not str(reference).strip():
            missing_reference_rows += 1
        else:
            raw_reference_strings.add(re.sub(r"\s+", " ", str(reference).strip()))
        cluster, has_doi = _cluster_key(reference)
        doi_rows += int(has_doi)
        cluster_rows[cluster] += 1
        genus = _value_key(row[index["Genus"]])
        role_key = _value_key(role)
        compound_key = _value_key(compound)
        if genus != "<missing>":
            cluster_genera[cluster].add(genus)
        if role_key != "<missing>":
            cluster_roles[cluster].add(role_key)
        if compound_key != "<missing>":
            cluster_fvocs[cluster].add(compound_key)

    sizes = sorted(cluster_rows.values())
    role_combo_counts = Counter(
        "+".join(sorted(roles)) if roles else "<none>"
        for roles in cluster_roles.values()
    )
    report = {
        "source": {
            "supplement_name": supplement_name,
            "oa_package_url_used": package_url,
            "oa_package_attempts": package_attempts,
            "sheet": SHEET,
        },
        "analyzed_test_rows": analyzed_rows,
        "domains": {column: dict(counter.most_common()) for column, counter in domains.items()},
        "publication_dependence": {
            "reference_column": REFERENCE_COLUMN,
            "unique_reference_strings": len(raw_reference_strings),
            "unique_clusters": len(cluster_rows),
            "rows_with_doi_cluster": doi_rows,
            "rows_missing_reference": missing_reference_rows,
            "cluster_size_min": min(sizes) if sizes else None,
            "cluster_size_median": statistics.median(sizes) if sizes else None,
            "cluster_size_max": max(sizes) if sizes else None,
            "role_combination_cluster_counts": dict(role_combo_counts),
            "paired_pollinator_florivore_clusters": sum(
                1 for roles in cluster_roles.values()
                if {role.lower() for role in roles} >= {"pollinator", "florivore"}
            ),
            "clusters_with_multiple_genera": sum(1 for values in cluster_genera.values() if len(values) > 1),
            "clusters_with_multiple_fvocs": sum(1 for values in cluster_fvocs.values() if len(values) > 1),
        },
        "guardrails": [
            "Only aggregate category counts and dependence summaries are persisted.",
            "Reference strings and observation-level workbook rows are not written to the artifact.",
            "The publication key prefers a DOI embedded in the source reference and otherwise uses the full normalized source reference string.",
        ],
    }
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        result = run(args.output)
    except Exception as error:
        safe = f"{type(error).__name__}: {error}".replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error title=Sasidharan S1 domain audit failure::{safe}")
        raise
    print(json.dumps({
        "analyzed_test_rows": result["analyzed_test_rows"],
        "publication_dependence": result["publication_dependence"],
    }, indent=2))
