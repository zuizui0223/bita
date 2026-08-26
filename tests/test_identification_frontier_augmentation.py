from __future__ import annotations

import csv
from pathlib import Path

from scripts.build_identification_frontier_augmentation import (
    EXTRA_FIELDS,
    SOURCE,
    augment_rows,
    build_readout,
)

ROOT = Path(__file__).resolve().parents[1]
COMMITTED = ROOT / "empirical" / "identification_design" / "IDENTIFICATION_FRONTIER_AUGMENTATION_V1.csv"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_all_screened_systems_have_one_frontier_classification() -> None:
    source = _rows(SOURCE)
    enriched = augment_rows(source)
    assert len(source) == 16
    assert len(enriched) == 16
    assert all(row["frontier_face"] for row in enriched)
    assert all(row["next_major_augmentation"] for row in enriched)
    assert all(row["remaining_gates_after_next_step"] for row in enriched)


def test_committed_matrix_matches_generator() -> None:
    source = _rows(SOURCE)
    expected = augment_rows(source)
    committed = _rows(COMMITTED)
    assert committed == expected
    assert all(field in committed[0] for field in EXTRA_FIELDS)


def test_four_complementary_anchor_faces_are_distinct_studies() -> None:
    rows = augment_rows(_rows(SOURCE))
    by_face = {row["frontier_face"]: row["study_id"] for row in rows}
    anchors = {
        by_face["direct_trait_factorial_anchor"],
        by_face["consumer_factorial_anchor"],
        by_face["randomized_context_anchor"],
        by_face["selective_D_system_anchor"],
    }
    assert len(anchors) == 4


def test_kessler_conditional_bound_is_assumption_indexed_not_a_confidence_bound() -> None:
    rows = augment_rows(_rows(SOURCE))
    kessler = next(row for row in rows if row["study_id"] == "Kessler_Gase_Baldwin_2008_Nicotiana")
    note = kessler["conditional_partial_id_note"]
    assert "+0.19_to_+0.25" in note
    assert "kappa>=0" in note
    assert "rho_minus_iota>=+0.19" in note
    assert "not_confidence_bound" in note


def test_readout_reports_fragmentation_without_prevalence_or_scalar_ranking() -> None:
    text = build_readout(augment_rows(_rows(SOURCE)))
    assert "direct A×D-like trait-factorial anchor: **1/16**" in text
    assert "consumer-factorial anchor: **1/16**" in text
    assert "characterized `m0_delta`: **0/16**" in text
    assert "independent joint-cost assay: **0/16**" in text
    assert "four different studies" in text
    assert "not literature prevalence" in text
    assert "No scalar distance is assigned" in text
