from __future__ import annotations

from pathlib import Path

from trait_architecture.floral_defence_selectivity import load_csv_rows, summarize_ecological_pattern


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "empirical" / "floral_defence_selectivity" / "results" / "analysis_ready_matched_systems.csv"


def test_current_selectivity_corpus_has_expected_premodel_pattern() -> None:
    rows = load_csv_rows(SNAPSHOT)
    summary = summarize_ecological_pattern(rows)

    assert summary["independent_clusters"] == 17
    assert summary["effective_defence_clusters"] == 16

    separated = summary["by_domain"]["SEPARATED"]
    assert separated["strict_preserved_or_improved"] == 2
    assert separated["strict_impaired"] == 0
    assert separated["null_compatible_no_detected_change"] == 4
    assert separated["unresolved_direct_pollinator"] == 1
    assert separated["pollinator_not_measured_directly"] == 2

    overlapped = summary["by_domain"]["OVERLAPPED"]
    assert overlapped["strict_preserved_or_improved"] == 0
    assert overlapped["strict_impaired"] == 1
    assert overlapped["pollinator_not_measured_directly"] == 1

    assert summary["transitional_mixed_clusters"] == 4
    assert summary["bypass_null_or_weak_defence_clusters"] == 1
    assert summary["strict_stage2_clusters"] == 3
    assert summary["strict_model_gate"] == "NOT_READY"


def test_null_compatible_rows_are_not_counted_as_strict_preservation() -> None:
    rows = load_csv_rows(SNAPSHOT)
    summary = summarize_ecological_pattern(rows)
    separated = summary["by_domain"]["SEPARATED"]

    assert separated["strict_preserved_or_improved"] == 2
    assert separated["null_compatible_no_detected_change"] == 4
    assert separated["strict_preserved_or_improved"] != (
        separated["strict_preserved_or_improved"] + separated["null_compatible_no_detected_change"]
    )
