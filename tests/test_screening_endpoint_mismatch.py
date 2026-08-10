from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.audit_screening_endpoint_mismatch import REASON_CLASS, classify
from trait_architecture.broad_meta_analysis import read_csv_rows


ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "empirical" / "broad_reality_evidence" / "iota_pathway" / "screening_decisions_v1.csv"


def test_every_recorded_exclusion_reason_has_a_declared_class() -> None:
    """A reason outside the declared mapping must surface, not be absorbed."""

    _, summary = classify(read_csv_rows(SCREENING))

    assert summary["unclassified_reasons"] == []


def test_unmapped_reasons_are_reported_rather_than_bucketed() -> None:
    rows = [
        {"decision": "exclude", "reason": "a_reason_nobody_declared"},
        {"decision": "exclude", "reason": "review_without_primary_data"},
    ]

    class_rows, summary = classify(rows)

    assert summary["unclassified_reasons"] == ["a_reason_nobody_declared"]
    assert {row["exclusion_class"] for row in class_rows} == {"unclassified", "not_primary_research"}


def test_shares_are_computed_over_exclusions_and_screened_records() -> None:
    rows = read_csv_rows(SCREENING)
    class_rows, summary = classify(rows)

    assert summary["records_with_a_decision"] == len(rows)
    assert summary["records_screened"] + summary["records_not_screened"] == len(rows)
    assert sum(int(row["records"]) for row in class_rows) == summary["exclusions"]

    # Shares are written rounded to six decimals, so they need not sum exactly.
    shares = [float(row["share_of_exclusions"]) for row in class_rows]
    assert pytest.approx(sum(shares), abs=1e-5) == 1.0
    assert shares == sorted(shares, reverse=True)


def test_committed_summary_matches_a_fresh_classification() -> None:
    committed = json.loads(
        (SCREENING.parent / "screening_endpoint_mismatch_summary.json").read_text(encoding="utf-8")
    )
    _, fresh = classify(read_csv_rows(SCREENING))

    for key in (
        "records_with_a_decision",
        "records_screened",
        "include_candidates",
        "exclusions",
        "exclusions_by_class",
        "endpoint_measures_the_consumer_share_of_exclusions",
    ):
        assert committed[key] == fresh[key], key


def test_consumer_endpoint_is_the_largest_declared_exclusion_class() -> None:
    """The readout's headline claim, guarded against silent drift."""

    class_rows, summary = classify(read_csv_rows(SCREENING))

    assert class_rows[0]["exclusion_class"] == "endpoint_measures_the_consumer"
    assert summary["exclusions_by_class"]["endpoint_measures_the_consumer"] > max(
        count
        for name, count in summary["exclusions_by_class"].items()
        if name != "endpoint_measures_the_consumer"
    )


def test_mapping_covers_only_reasons_and_not_decisions() -> None:
    assert "include_candidate" not in REASON_CLASS
    assert "metadata_not_retrieved" not in REASON_CLASS
