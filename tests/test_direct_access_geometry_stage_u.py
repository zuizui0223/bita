from scripts.validate_direct_access_geometry_stage_u import validate


def test_stage_u_batch_2_is_screened_but_search_remains_open() -> None:
    result = validate()
    assert result == {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_STAGE_U_V1",
        "candidate_records": 23,
        "eligible_new_programs": 9,
        "duplicate_records": 1,
        "ineligible_records": 13,
        "eligible_direction_counts": {
            "POSITIVE": 5,
            "NULL": 3,
            "OPPOSITE": 0,
            "MIXED": 1,
        },
        "stage_u_search_complete": False,
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
        "status": "STAGE_U_BATCH_2_SCREENED_SEARCH_CONTINUES",
    }
