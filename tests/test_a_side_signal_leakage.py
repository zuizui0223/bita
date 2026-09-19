from __future__ import annotations

from pathlib import Path

from trait_architecture.floral_defence_selectivity import load_csv_rows


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "empirical" / "floral_defence_selectivity" / "a_side_signal_leakage_registry.csv"


def test_a_side_signal_leakage_registry_has_five_paired_programs() -> None:
    rows = load_csv_rows(REGISTRY)
    assert len(rows) == 5
    assert len({row["study_program_id"] for row in rows}) == 5
    assert len({row["doi"] for row in rows}) == 5


def test_scored_a_side_states_recover_shared_or_antagonist_biased_tracking() -> None:
    rows = load_csv_rows(REGISTRY)
    scored = [row for row in rows if row["paired_state"] != "UNRESOLVED"]
    counts = {
        state: sum(row["paired_state"] == state for row in scored)
        for state in {row["paired_state"] for row in scored}
    }
    assert len(scored) == 4
    assert counts == {"SHARED_TRACKING": 3, "ANTAGONIST_BIASED": 1}
    assert not any(row["paired_state"] == "MUTUALIST_EXCLUSIVE" for row in scored)


def test_impatiens_is_kept_unresolved() -> None:
    rows = load_csv_rows(REGISTRY)
    row = next(row for row in rows if row["study_program_id"] == "Impatiens_2018")
    assert row["paired_state"] == "UNRESOLVED"
    assert row["pollinator_state"] == "NULL_COMPATIBLE"
    assert row["antagonist_state"] == "UNRESOLVED"
