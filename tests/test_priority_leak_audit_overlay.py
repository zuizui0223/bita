from trait_architecture.priority_leak_audit_adjudication import PACKET, make_sheet
from trait_architecture.priority_leak_audit_overlay import apply_overlay


def packet_row() -> dict[str, str]:
    row = {field: "" for field in PACKET}
    row.update({
        "audit_group": "priority",
        "route_family_audit": "A_to_pollination",
        "audit_rank": "1",
        "candidate_id": "doi:10.1000/example",
        "doi": "10.1000/example",
        "title": "Example",
        "crossref_lookup_status": "success",
        "crossref_abstract_available": "true",
    })
    return row


def overlay_row() -> dict[str, str]:
    return {
        "audit_group": "priority",
        "route_family_audit": "A_to_pollination",
        "audit_rank": "1",
        "candidate_id": "doi:10.1000/example",
        "doi": "10.1000/example",
        "source_screen_status": "included_for_source_coding",
        "source_access_status": "abstract_only",
        "study_type": "manipulation",
        "taxon": "Example plant",
        "primary_study_id": "example_study",
        "study_cluster_id": "example_panel",
        "screen_exclusion_reason": "",
        "route_screen_status": "direct_route_present",
        "route_screen_reason": "Direct target trait and pollination outcome comparison.",
        "source_locator": "Crossref deposited abstract",
        "coder_id": "tester",
        "coding_date": "2026-07-02",
        "coding_note": "Audit only.",
    }


def test_overlay_applies_without_replacing_packet_metadata() -> None:
    packet = [packet_row()]
    sheet = apply_overlay(packet, [overlay_row()])

    assert sheet[0]["title"] == "Example"
    assert sheet[0]["route_screen_status"] == "direct_route_present"
    assert sheet[0]["study_cluster_id"] == "example_panel"


def test_overlay_rejects_doi_mismatch() -> None:
    row = overlay_row()
    row["doi"] = "10.1000/other"
    try:
        apply_overlay([packet_row()], [row])
    except ValueError as error:
        assert "DOI does not match" in str(error)
    else:
        raise AssertionError("expected DOI mismatch error")


def test_unmodified_rows_stay_unassessed() -> None:
    packet = [packet_row()]
    sheet = apply_overlay(packet, [])
    expected = make_sheet(packet)

    assert sheet == expected
