from scripts.validate_direct_access_geometry_formal_frame import validate


def test_formal_frame_is_frozen_but_not_open_for_inference() -> None:
    result = validate()
    assert result == {
        "schema": "BITA_DIRECT_ACCESS_GEOMETRY_FORMAL_FRAME_V1",
        "historical_frame_studies": 56,
        "direct_discovery_programs": 13,
        "discovery_overlap_with_historical_frame": 3,
        "discovery_not_in_historical_frame": 10,
        "formal_recurrence_result_open": False,
        "primary_standardized_network_k": 2,
        "status": "FRAME_FROZEN_SCREENING_REQUIRED",
    }
