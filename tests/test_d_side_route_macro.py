from __future__ import annotations

from scripts.summarize_d_side_route_macro import summarize_registry


def test_route_macro_summary_counts_unique_programs_and_modalities() -> None:
    rows = [
        {"study_program_id":"A","broad_modality":"chemical","pollination_followup":"yes","pollination_state_family":"CONTEXT_DEPENDENT"},
        {"study_program_id":"B","broad_modality":"chemical","pollination_followup":"yes","pollination_state_family":"INTERFERENCE"},
        {"study_program_id":"C","broad_modality":"physical","pollination_followup":"no","pollination_state_family":"NOT_MEASURED"},
        {"study_program_id":"D","broad_modality":"physical","pollination_followup":"yes","pollination_state_family":"NULL_COMPATIBLE"},
        {"study_program_id":"E","broad_modality":"reward_access","pollination_followup":"yes","pollination_state_family":"IMPROVED"},
    ]
    out = summarize_registry(rows)
    assert out["unique_study_programs"] == 5
    assert out["modality_counts"] == {"chemical":2,"physical":2,"reward_access":1}
    assert out["pollination_followup_programs"] == 4
    assert out["pollination_state_counts"] == {
        "CONTEXT_DEPENDENT":1,
        "IMPROVED":1,
        "INTERFERENCE":1,
        "NULL_COMPATIBLE":1,
    }


def test_followup_coverage_is_reported_by_modality() -> None:
    rows = [
        {"study_program_id":"A","broad_modality":"chemical","pollination_followup":"yes","pollination_state_family":"CONTEXT_DEPENDENT"},
        {"study_program_id":"B","broad_modality":"chemical","pollination_followup":"no","pollination_state_family":"NOT_MEASURED"},
        {"study_program_id":"C","broad_modality":"physical","pollination_followup":"no","pollination_state_family":"NOT_MEASURED"},
        {"study_program_id":"D","broad_modality":"physical","pollination_followup":"yes","pollination_state_family":"NULL_COMPATIBLE"},
    ]
    out = summarize_registry(rows)
    assert out["pollination_followup_by_modality"]["chemical"] == {"measured":1,"total":2}
    assert out["pollination_followup_by_modality"]["physical"] == {"measured":1,"total":2}


def test_duplicate_program_ids_are_rejected() -> None:
    rows = [
        {"study_program_id":"A","broad_modality":"chemical","pollination_followup":"yes","pollination_state_family":"INTERFERENCE"},
        {"study_program_id":"A","broad_modality":"chemical","pollination_followup":"yes","pollination_state_family":"INTERFERENCE"},
    ]
    try:
        summarize_registry(rows)
    except ValueError as exc:
        assert "duplicate study_program_id" in str(exc)
    else:
        raise AssertionError("duplicate program ids must fail")
