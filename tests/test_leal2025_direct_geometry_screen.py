from scripts.validate_leal2025_direct_geometry_screen import validate


def test_historical_label_screen_is_complete_but_source_denominator_is_closed() -> None:
    result = validate()
    assert result == {
        "schema": "BITA_LEAL2025_DIRECT_GEOMETRY_SCREEN_V1",
        "historical_study_field_labels": 56,
        "screened_unambiguous_labels": 54,
        "ineligible_no_geometry_test": 50,
        "eligible_direct_geometry_test": 4,
        "eligible_directions": {
            "POSITIVE": 2,
            "NULL": 1,
            "OPPOSITE": 0,
            "MIXED": 1,
        },
        "provenance_conflict_labels": ["Varma&Sinu2019", "Zhangetal2009a"],
        "source_resolved_program_denominator_ready": False,
        "formal_recurrence_result_open": False,
        "status": "LABEL_SCREEN_COMPLETE_SOURCE_REPAIR_REQUIRED",
    }
