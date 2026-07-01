import pytest

from trait_architecture.broad_source_screening import (
    initial_source_screening_matrix,
    validate_source_screening_matrix,
)


def priority_candidate(**overrides: str) -> dict[str, str]:
    row = {
        "candidate_id": "doi:10.1/example",
        "doi": "10.1/example",
        "title": "Flower colour and pollination",
        "route_families": "A_to_pollination;A_to_antagonism",
        "shallow_screen_status": "priority_for_shallow_source_coding",
    }
    row.update(overrides)
    return row


def test_matrix_keeps_priority_provenance_but_no_inferred_source_evidence() -> None:
    matrix = initial_source_screening_matrix([priority_candidate()])

    assert matrix == [{
        "candidate_id": "doi:10.1/example",
        "doi": "10.1/example",
        "title": "Flower colour and pollination",
        "discovery_route_families": "A_to_pollination;A_to_antagonism",
        "source_screen_status": "unassessed",
        "source_access_status": "unassessed",
        "study_type": "",
        "taxon": "",
        "primary_study_id": "",
        "study_cluster_id": "",
        "screen_exclusion_reason": "",
        "coder_id": "",
        "coding_date": "",
        "coding_note": "",
    }]
    validate_source_screening_matrix(matrix)


def test_matrix_rejects_duplicate_priority_candidate() -> None:
    with pytest.raises(ValueError, match="duplicate priority candidate_id"):
        initial_source_screening_matrix([priority_candidate(), priority_candidate()])


def test_unassessed_matrix_cannot_contain_inferred_source_decision() -> None:
    matrix = initial_source_screening_matrix([priority_candidate()])
    matrix[0]["taxon"] = "Invented taxon"

    with pytest.raises(ValueError, match="cannot contain inferred source decisions"):
        validate_source_screening_matrix(matrix)
