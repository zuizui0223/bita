from __future__ import annotations

from trait_architecture.depth_saturation_audit import build_depth_audit_sample
from trait_architecture.depth_saturation_audit_packet import build_depth_audit_abstract_packet


def _row(candidate_id: str, rank: int) -> dict[str, str]:
    return {
        "query_id": "AH01",
        "route_family": "A_to_antagonism",
        "query_rank": str(rank),
        "candidate_id": candidate_id,
        "doi": "10.1/shared",
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
    }


def test_depth_packet_preserves_group_and_caches_doi_lookup() -> None:
    queue, _ = build_depth_audit_sample(
        [_row("head", 1), _row("tail", 2)],
        head_rank_max=1,
        tail_rank_min=2,
        tail_rank_max=2,
        per_route_stratum_group=10,
    )
    calls: list[str] = []

    def fake_request(url: str) -> dict[str, object]:
        calls.append(url)
        return {
            "message": {
                "type": "journal-article",
                "title": ["Resolved flower study"],
                "issued": {"date-parts": [[2020]]},
                "container-title": ["Plant Ecology"],
                "abstract": "<jats:p>Floral trait and herbivory.</jats:p>",
            }
        }

    packet = build_depth_audit_abstract_packet(queue, request_json=fake_request)

    assert len(packet) == 2
    assert len(calls) == 1
    assert {row["audit_group"] for row in packet} == {"head_priority", "tail_priority"}
    assert all(row["crossref_lookup_status"] == "success" for row in packet)
    assert all(row["crossref_abstract_available"] == "true" for row in packet)
