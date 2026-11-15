"""Reproducible source-family audit for heterogeneous BITA empirical programmes.

A publication, source data file, experimental population, variant or mutation
is NOT automatically an independent evolutionary origin. No pooled effect is fit.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "empirical/trait_architecture_history/cross_system_evidence_v1.csv"
OUTPUT = ROOT / "empirical/trait_architecture_history/cross_system_evidence_readout_v1.json"
EXCLUDED = {"outside_primary_functional_division", "outside_primary_architecture"}

def summarize(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("empty programme registry")
    ids = [r["source_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate paper/programme source id")
    for r in rows:
        if not r["programme_family"] or not r["study_doi"] or not r["source_url"]:
            raise ValueError("missing DOI, family, or source provenance")
        for key in ("independent_history_contrast", "architecture_origin_identified",
                    "poolable_same_endpoint"):
            if r[key] not in ("True", "False"):
                raise ValueError("invalid triage value for "+key)
    admitted = [r for r in rows if r["evidence_layer"] not in EXCLUDED]
    if any(r["poolable_same_endpoint"] == "True" for r in admitted):
        raise ValueError("a new prespecified common estimand is required for pooling")
    families = sorted({r["programme_family"] for r in admitted})
    return {
        "source_publications_n": len(rows),
        "all_unique_programme_families_n": len({r["programme_family"] for r in rows}),
        "primary_source_publications_n": len(admitted),
        "primary_independent_programme_families_n": len(families),
        "context_only_source_publications_n": len(rows) - len(admitted),
        "matched_history_programme_families_n": len({
            r["programme_family"] for r in admitted
            if r["independent_history_contrast"] == "True"}),
        "identified_architecture_origin_programme_families_n": len({
            r["programme_family"] for r in admitted
            if r["architecture_origin_identified"] == "True"}),
        "new_source_studies_with_quantitative_contrasts_n": 1,
        "new_nonpoolable_endpoint_contrasts_n": 2,
        "pooled_meta_analysis_performed": False,
        "primary_programme_families": families,
        "scientific_boundary": (
            "Evidence map; five non-exchangeable programme families, not five "
            "replicates of architecture evolution. Architecture-origin causation, "
            "matched historical states, K(u), and common effect estimands remain "
            "unidentified. Despres mutation pairs and crossing events are selected "
            "assay observations, not independent biological transitions. "
            "Mihajlovic figures 2/3 were SHA-pinned from the publisher, with two non-poolable replicate-line effects audited; no absolute cross-study effect.")
    }

def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    result = summarize(rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
