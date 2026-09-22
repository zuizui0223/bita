from __future__ import annotations

import pytest

from scripts.evaluate_third_network_route_reliability import (
    evaluate_rows,
    expected_double_code_ids,
)


def _rows(n: int = 20) -> list[dict[str, str]]:
    rows = []
    for i in range(n):
        rows.append(
            {
                "event_id": f"E{i:03d}",
                "dataset_role": "CONFIRMATORY",
                "route_code": "L" if i % 3 else "B",
                "visitor_id_confidence": "HIGH",
                "clip_quality": "PASS",
                "coder_id": "PRIMARY",
                "double_coded": "false",
                "second_route_code": "",
            }
        )

    selected = expected_double_code_ids(rows)
    for row in rows:
        if row["event_id"] in selected:
            row["double_coded"] = "true"
            row["second_route_code"] = row["route_code"]
    return rows


def test_route_reliability_passes_exact_seeded_twenty_percent_subset() -> None:
    rows = _rows(20)
    result = evaluate_rows(rows)
    assert result["status"] == "ROUTE_RELIABILITY_PASS"
    assert result["double_coded_events"] == 4
    assert result["double_code_fraction"] == 0.2
    assert result["raw_agreement_LBAN"] == 1.0
    assert result["kappa_LBAN"] == 1.0


def test_double_code_subset_is_outcome_blind_and_deterministic() -> None:
    rows = _rows(30)
    first = expected_double_code_ids(rows)
    altered = [dict(row, route_code=("A" if row["route_code"] == "L" else "N")) for row in rows]
    second = expected_double_code_ids(altered)
    assert first == second


def test_reliability_fails_when_kappa_is_below_target() -> None:
    rows = _rows(30)
    for row in rows:
        if row["double_coded"] == "true":
            row["second_route_code"] = "B" if row["route_code"] != "B" else "L"
    result = evaluate_rows(rows)
    assert result["status"] == "ROUTE_RELIABILITY_RECODE_REQUIRED"
    assert result["kappa_LBAN"] < 0.8


def test_posthoc_double_code_subset_is_rejected() -> None:
    rows = _rows(20)
    selected = [row for row in rows if row["double_coded"] == "true"]
    unselected = [row for row in rows if row["double_coded"] == "false"]
    selected[0]["double_coded"] = "false"
    selected[0]["second_route_code"] = ""
    unselected[0]["double_coded"] = "true"
    unselected[0]["second_route_code"] = unselected[0]["route_code"]

    with pytest.raises(ValueError, match="DOUBLE_CODE_SUBSET_MISMATCH"):
        evaluate_rows(rows)


def test_degenerate_single_category_kappa_fails_closed() -> None:
    rows = _rows(20)
    for row in rows:
        row["route_code"] = "L"
        if row["double_coded"] == "true":
            row["second_route_code"] = "L"

    with pytest.raises(ValueError, match="ROUTE_RELIABILITY_KAPPA_NOT_ESTIMABLE"):
        evaluate_rows(rows)
