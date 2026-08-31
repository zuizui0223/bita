from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "empirical" / "identification_design" / "HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv"


def _rows():
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_high_information_coverage_has_declared_systems() -> None:
    rows = _rows()
    assert len(rows) == 17
    ids = {row["study_id"] for row in rows}
    assert "Kessler_Gase_Baldwin_2008_Nicotiana" in ids
    assert "Egan_2021_Fragaria" in ids
    assert "Gorden_Adler_2018_Impatiens_capensis" in ids
    assert "Sun_Huang_2015_Pedicularis_rex" in ids


def test_trait_factorial_and_consumer_factorial_are_split_across_anchors() -> None:
    rows = {row["study_id"]: row for row in _rows()}

    kessler = rows["Kessler_Gase_Baldwin_2008_Nicotiana"]
    assert kessler["trait_factorial_status"] == "full_2x2_A_D_like_factorial"
    assert kessler["highest_recoverable_layer"] == "direct_discrete_trait_interaction"
    assert kessler["G_toggle_status"] == "no"
    assert kessler["P_toggle_status"] == "no"

    egan = rows["Egan_2021_Fragaria"]
    assert egan["G_toggle_status"] == "herbivory_presence_absence"
    assert egan["P_toggle_status"] == "pollination_open_vs_hand"
    assert egan["trait_factorial_status"] == "no_A_D_trait_factorial"
    assert egan["highest_recoverable_layer"] == "consumer_agent_factorial_with_trait_selection"


def test_no_screened_anchor_has_independent_kappa_assay() -> None:
    rows = _rows()
    assert all(row["independent_kappa_status"] == "no" for row in rows)


def test_no_screened_anchor_claims_full_channel_identification() -> None:
    rows = _rows()
    forbidden = {"full_channel_identification", "rho_iota_kappa_identified"}
    assert not any(row["highest_recoverable_layer"] in forbidden for row in rows)
