from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.plan_peucedanum_stage_b_common_support import (
    REQUIRED_FIELDS,
    SCHEMA,
    evaluate_design,
    read_rows,
)


def _rows() -> list[dict[str, str]]:
    rows = []
    for i in range(30):
        rows.append(
            {
                "unit_id": f"E{i:02d}",
                "perfect_available": "15",
                "male_available": "35",
                "total_available": "50",
            }
        )
    for i in range(30):
        rows.append(
            {
                "unit_id": f"L{i:02d}",
                "perfect_available": "8",
                "male_available": "42",
                "total_available": "50",
            }
        )
    return rows


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_common_support_requires_capacity_for_every_q_target(tmp_path: Path) -> None:
    path = tmp_path / "presurvey.csv"
    _write(path, _rows())
    receipt = evaluate_design(
        read_rows(path),
        retained_total=20,
        q_targets=[0.2, 0.4, 0.6],
        pilot_common_eligible_target=24,
        confirmatory_common_eligible_target=189,
    )
    assert receipt["schema_version"] == SCHEMA
    assert receipt["common_support_requirements"]["minimum_perfect_available"] == 12
    assert receipt["common_support_requirements"]["minimum_male_available"] == 16
    assert receipt["presurvey"]["n_common_eligible"] == 30
    assert receipt["presurvey"]["common_eligible_fraction"] == pytest.approx(0.5)
    assert len(receipt["presurvey"]["eligible_unit_ids"]) == 30
    assert receipt["screening_plans_using_wilson_lower95"]["pilot_target"]["plan"] is not None


def test_old_synthetic_40_flower_extreme_q_design_can_have_no_common_support(tmp_path: Path) -> None:
    path = tmp_path / "presurvey.csv"
    _write(path, _rows())
    receipt = evaluate_design(
        read_rows(path),
        retained_total=40,
        q_targets=[0.25, 0.50, 0.75],
    )
    assert receipt["common_support_requirements"]["minimum_perfect_available"] == 30
    assert receipt["common_support_requirements"]["minimum_male_available"] == 30
    assert receipt["presurvey"]["n_common_eligible"] == 0
    assert receipt["screening_plans_using_wilson_lower95"]["pilot_target"]["plan"] is None


def test_q_targets_must_be_exactly_realizable_as_integer_flower_counts(tmp_path: Path) -> None:
    path = tmp_path / "presurvey.csv"
    _write(path, _rows())
    with pytest.raises(ValueError, match="not exactly realizable"):
        evaluate_design(read_rows(path), retained_total=20, q_targets=[0.2, 0.33, 0.6])


def test_reader_rejects_inconsistent_flower_totals(tmp_path: Path) -> None:
    rows = _rows()
    rows[0]["total_available"] = "49"
    path = tmp_path / "bad.csv"
    _write(path, rows)
    with pytest.raises(ValueError, match="must equal total_available"):
        read_rows(path)


def test_registered_presurvey_template_has_exact_header() -> None:
    root = Path(__file__).resolve().parents[1]
    template = root / "empirical" / "identification_design" / "PEUCEDANUM_STAGE_B_PRESURVEY_TEMPLATE_V1.csv"
    with template.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
