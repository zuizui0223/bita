from __future__ import annotations

from trait_architecture.impatiens_factorial_balance_audit import _baseline_value, _label, _summary


def _row(robbing: str, florivory: str, pollination: str, redness: float = 10.0, tannin: float = 2.0, date: float = 100.0) -> dict[str, str]:
    return {
        "Robbing": robbing,
        "Florivory": florivory,
        "Pollination": pollination,
        "Early_Season_Flower_Redness": str(redness),
        "Early_Season_Condensed_Tannins": str(tannin),
        "Date_of_First_CH_Flower": str(date),
    }


def test_factorial_label_has_all_assignment_factors() -> None:
    assert _label(_row("Y", "N", "Y")) == "Robbing_Y|Florivory_N|Pollination_Y"


def test_baseline_transform_and_summary_are_aggregate_only() -> None:
    row = _row("N", "Y", "N", tannin=3.0)
    assert _baseline_value(row, "Early_Season_Flower_Redness", "identity") == 10.0
    assert round(_baseline_value(row, "Early_Season_Condensed_Tannins", "log1p"), 6) == round(1.38629436112, 6)
    summary = _summary([1.0, 2.0, 3.0])
    assert summary == {"n": 3, "mean": 2.0, "sd": 1.0, "min": 1.0, "max": 3.0}


def test_non_assignment_levels_are_rejected() -> None:
    bad = _row("maybe", "Y", "N")
    try:
        _label(bad)
    except ValueError as error:
        assert "Robbing" in str(error)
    else:
        raise AssertionError("invalid assignment level should fail")
