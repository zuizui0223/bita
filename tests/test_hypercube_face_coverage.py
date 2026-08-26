from __future__ import annotations

import csv
from pathlib import Path

from scripts.build_hypercube_face_coverage import FIELDS, SOURCE, build_rows

ROOT = Path(__file__).resolve().parents[1]
COMMITTED = ROOT / "empirical" / "identification_design" / "HYPERCUBE_FACE_COVERAGE_V1.csv"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_committed_hypercube_faces_match_generator() -> None:
    expected = build_rows(_rows(SOURCE))
    committed = _rows(COMMITTED)
    assert committed == expected
    assert list(committed[0]) == FIELDS
    assert len(committed) == 6


def test_complementary_trait_consumer_faces_exist_but_full_face_does_not() -> None:
    rows = _rows(COMMITTED)
    labels = {row["face_label"] for row in rows}
    assert "A_x_D_trait_face" in labels
    assert "A_x_G_x_Psupp_face" in labels
    assert "D_x_G_x_Psupp_plus_observed_A_face" in labels
    assert "G_x_P_consumer_face_plus_observed_A_D" in labels
    assert all(row["strict_target_status"] != "full_ADGP" for row in rows)


def test_hand_pollination_is_not_silently_promoted_to_pollinator_access() -> None:
    rows = {row["study_id"]: row for row in _rows(COMMITTED)}
    assert rows["Theis_Adler_2012_Cucurbita"]["P_intervention"] == "supplemental_hand_pollination"
    assert "not_target_P" in rows["Theis_Adler_2012_Cucurbita"]["strict_target_status"]
    assert rows["Santangelo_2019_Trifolium"]["P_intervention"] == "hand_pollination"
    assert "nonaccess_P" in rows["Santangelo_2019_Trifolium"]["strict_target_status"]


def test_face_anchors_are_different_studies() -> None:
    rows = _rows(COMMITTED)
    by_label = {row["face_label"]: row["study_id"] for row in rows}
    main_faces = {
        by_label["A_x_D_trait_face"],
        by_label["A_x_G_x_Psupp_face"],
        by_label["D_x_G_x_Psupp_plus_observed_A_face"],
    }
    assert len(main_faces) == 3
