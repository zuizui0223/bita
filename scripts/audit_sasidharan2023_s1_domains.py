"""Audit aggregate coding domains and publication dependence in Sasidharan et al. 2023 S1.

Only aggregate counts and citation-fingerprint diagnostics are persisted. Literal source
references and observation-level workbook rows are never written to the artifact.
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
    "Insect function", "Detection", "GC-EAD or EAG or SCR/SSR",
    "Physio_resp", "Physio_No_resp", "Behaviour_test", "Behaviour choice",
    "Behaviour_pos", "Behaviour_neg", "No_behav_reps",
)
REFERENCE_COLUMN = "Reference (doi TBA)"
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.I)
DOI_PREFIX_RE = re.compile(r"https?\s*:?\s*/?/?\s*(?:dx\.)?doi\.org\s*/?", re.I)


def _value_key(value: Any) -> str:
    if value is None:
        return "<missing>"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(int(value)) if float(value).is_integer() else str(value)
    text = re.sub(r"\s+", " ", str(value).strip())
    return text if text else "<missing>"


def _reference_text(reference: Any) -> str:
    return "" if reference is None else re.sub(r"\s+", " ", str(reference).strip())


def _doi(reference: Any) -> str | None:
    match = DOI_RE.search(_reference_text(reference))
    return match.group(0).rstrip(".,;)").lower() if match else None


def _citation_stem(reference: Any) -> str:
    """Normalize the bibliographic citation after removing DOI decoration.

    This is an audit fingerprint, not a fuzzy bibliographic merge: only exact normalized
    stems are considered the same study.
    """
    text = _reference_text(reference).lower()
    text = DOI_RE.sub(" ", text)
    text = DOI_PREFIX_RE.sub(" ", text)
    text = re.sub(r"\bdoi\b", " ", text)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def run(output_path: str | Path) -> dict[str, Any]:
    import openpyxl  # type: ignore

    oa_url = _oa_package_url()
    package, package_url, package_attempts = _download_package(oa_url)
    supplement_name, supplement, _ = _supplement_from_package(package)
    workbook = openpyxl.load_workbook(io.BytesIO(supplement), read_only=True, data_only=True)
    ws = workbook[SHEET]

    rows = ws.iter_rows(values_only=True)
    headers: list[str] | None = None
    index: dict[str, int] | None = None
    header_absolute_row: int | None = None
    for absolute_row, candidate in enumerate(rows, start=1):
        cleaned = ["" if value is None else str(value).strip() for value in candidate]
        candidate_index = {name: i for i, name in enumerate(cleaned) if name}
        if {"Compound", "Insect function", REFERENCE_COLUMN}.issubset(candidate_index):
            headers = cleaned
            index = candidate_index
            header_absolute_row = absolute_row
            break
    if headers is None or index is None:
        raise RuntimeError("could not locate the S1 header row")

    required = (*DOMAIN_COLUMNS, REFERENCE_COLUMN, "Compound", "Genus", "Insect species")
    missing_required = [name for name in required if name not in index]
    if missing_required:
        raise RuntimeError(f"missing expected S1 columns: {missing_required}; headers={headers}")

    domains = {column: Counter() for column in DOMAIN_COLUMNS}
    raw_references: Counter[str] = Counter()
    stem_rows: Counter[str] = Counter()
    stem_roles: dict[str, set[str]] = defaultdict(set)
    stem_genera: dict[str, set[str]] = defaultdict(set)
    stem_fvocs: dict[str, set[str]] = defaultdict(set)
    stem_dois: dict[str, set[str]] = defaultdict(set)
    doi_rows = 0
    missing_reference_rows = 0
    analyzed_rows = 0

    for row in rows:
        if not any(value is not None and str(value).strip() for value in row):
            continue
        compound = row[index["Compound"]]
        insect = row[index["Insect species"]]
        role = row[index["Insect function"]]
        if not (compound and insect and role):
            continue
        analyzed_rows += 1
        for column in DOMAIN_COLUMNS:
            domains[column][_value_key(row[index[column]])] += 1

        reference = row[index[REFERENCE_COLUMN]]
        text = _reference_text(reference)
        if not text:
            missing_reference_rows += 1
            continue
        raw_references[text] += 1
        stem = _citation_stem(reference)
        stem_rows[stem] += 1
        stem_roles[stem].add(_value_key(role))
        genus = _value_key(row[index["Genus"]])
        if genus != "<missing>":
            stem_genera[stem].add(genus)
        stem_fvocs[stem].add(_value_key(compound))
        doi = _doi(reference)
        if doi:
            doi_rows += 1
            stem_dois[stem].add(doi)

    sizes = sorted(stem_rows.values())
    doi_values = {doi for values in stem_dois.values() for doi in values}
    doi_stems = {stem for stem, values in stem_dois.items() if values}
    fallback_stems = set(stem_rows) - doi_stems
    role_combo_counts = Counter(
        "+".join(sorted(roles)) if roles else "<none>" for roles in stem_roles.values()
    )
    doi_conflict_stems = sum(1 for values in stem_dois.values() if len(values) > 1)

    report = {
        "source": {
            "supplement_name": supplement_name,
            "oa_package_url_used": package_url,
            "oa_package_attempts": package_attempts,
            "sheet": SHEET,
            "header_absolute_row": header_absolute_row,
        },
        "analyzed_test_rows": analyzed_rows,
        "domains": {column: dict(counter.most_common()) for column, counter in domains.items()},
        "publication_dependence": {
            "reference_column": REFERENCE_COLUMN,
            "published_final_study_count": 32,
            "unique_reference_strings": len(raw_references),
            "unique_dois": len(doi_values),
            "unique_exact_citation_stems": len(stem_rows),
            "doi_bearing_stems": len(doi_stems),
            "fallback_stems_without_doi": len(fallback_stems),
            "citation_stems_with_multiple_dois": doi_conflict_stems,
            "rows_with_doi": doi_rows,
            "rows_missing_reference": missing_reference_rows,
            "cluster_size_min": min(sizes) if sizes else None,
            "cluster_size_median": statistics.median(sizes) if sizes else None,
            "cluster_size_max": max(sizes) if sizes else None,
            "role_combination_cluster_counts": dict(role_combo_counts),
            "paired_pollinator_florivore_clusters": sum(
                1 for roles in stem_roles.values()
                if {role.lower() for role in roles} >= {"pollinator", "florivore"}
            ),
            "clusters_with_multiple_genera": sum(1 for values in stem_genera.values() if len(values) > 1),
            "clusters_with_multiple_fvocs": sum(1 for values in stem_fvocs.values() if len(values) > 1),
            "matches_published_study_count": len(stem_rows) == 32,
        },
        "guardrails": [
            "Only aggregate category counts and citation-fingerprint summaries are persisted.",
            "Literal reference strings and observation-level workbook rows are not written to the artifact.",
            "Citation-stem clustering is exact after DOI decoration, punctuation and whitespace removal; no fuzzy bibliographic merges are applied.",
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
