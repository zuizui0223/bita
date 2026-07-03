from __future__ import annotations

from trait_architecture.depth_saturation_audit_adjudication import summarize_depth_audit
from trait_architecture.priority_leak_audit_adjudication import make_sheet


def _packet(audit_group: str, candidate_id: str) -> dict[str, str]:
    return {
        "audit_group": audit_group,
        "route_family_audit": "A_to_antagonism",
        "audit_rank": "1",
        "candidate_id": candidate_id,
        "doi": f"10.1/{candidate_id}",
        "title": "Flower study",
        "publication_year": "2020",
        "container_title": "Plant Ecology",
        "landing_page_url": "https://doi.org/example",
        "source_queries": "AH01",
        "route_families": "A_to_antagonism",
        "metadata_A_signal": "true",
        "metadata_B_signal": "false",
        "metadata_P_signal": "false",
        "metadata_H_signal": "true",
        "metadata_W_signal": "false",
        "metadata_biology_context_term_count": "3",
        "shallow_screen_status": "priority_for_shallow_source_coding",
        "shallow_screen_reason": "test",
        "crossref_lookup_status": "success",
        "crossref_message_type": "journal-article",
        "crossref_title": "Flower study",
        "crossref_published_year": "2020",
        "crossref_container_title": "Plant Ecology",
        "crossref_abstract_available": "true",
        "crossref_abstract_text": "Floral trait and florivory.",
        "source_packet_warning": "screening only",
    }


def _coded(row: dict[str, str], *, present: bool) -> dict[str, str]:
    row = dict(row)
    row.update({
        "source_screen_status": "included_for_source_coding",
        "source_access_status": "fulltext_available",
        "study_type": "observational",
        "taxon": "Plantus example",
        "primary_study_id": row["candidate_id"],
        "study_cluster_id": row["candidate_id"],
        "screen_exclusion_reason": "",
        "route_screen_status": "direct_route_present" if present else "direct_route_absent",
        "route_screen_reason": "direct trait outcome model" if present else "outcome is not the requested route",
        "source_locator": "Table 1",
        "coder_id": "tester",
        "coding_date": "2026-07-03",
        "coding_note": "",
    })
    return row


def test_depth_summary_compares_screened_head_and_tail_within_group() -> None:
    sheet = make_sheet([
        _packet("head_priority", "head"),
        _packet("tail_priority", "tail"),
        _packet("head_biological_nonpriority", "head-bio"),
        _packet("tail_biological_nonpriority", "tail-bio"),
    ])
    coded = [
        _coded(sheet[0], present=True),
        _coded(sheet[1], present=False),
        _coded(sheet[2], present=False),
        _coded(sheet[3], present=True),
    ]

    summary, comparisons, diagnostics = summarize_depth_audit(coded)

    assert len(summary) == 4
    priority = next(row for row in comparisons if row["screen_group"] == "priority")
    biological = next(row for row in comparisons if row["screen_group"] == "biological_nonpriority")
    assert priority["head_direct_route_yield"] == "1.000000"
    assert priority["tail_direct_route_yield"] == "0.000000"
    assert priority["tail_minus_head_yield"] == "-1.000000"
    assert biological["tail_minus_head_yield"] == "1.000000"
    assert all(row["comparison_status"] == "comparable_screened_strata" for row in comparisons)
    assert diagnostics["overall_route_screen_status_counts"]["direct_route_present"] == 2
