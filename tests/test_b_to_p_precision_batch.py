from trait_architecture.b_to_p_precision_batch import select_b_to_p_precision_batch


def candidate(candidate_id: str, *, b: str, p: str, abstract: str = "true", review: str = "false", rank: str = "1") -> dict[str, str]:
    return {
        "candidate_id": candidate_id,
        "doi": candidate_id.removeprefix("doi:"),
        "title": f"Title {candidate_id}",
        "route_families": "B_to_pollination",
        "metadata_B_signal": b,
        "metadata_P_signal": p,
        "abstract_available": abstract,
        "metadata_review_signal": review,
        "query_rank_min": rank,
    }


def test_precision_queue_requires_both_metadata_signals() -> None:
    rows = [
        candidate("doi:bp", b="true", p="true", rank="4"),
        candidate("doi:b-only", b="true", p="false", rank="1"),
        candidate("doi:p-only", b="false", p="true", rank="1"),
    ]

    queue = select_b_to_p_precision_batch(rows, limit=25)

    assert [row["candidate_id"] for row in queue] == ["doi:bp"]
    assert queue[0]["focus_route_families"] == "B_to_pollination"
    assert queue[0]["metadata_B_signal"] == "true"
    assert queue[0]["metadata_P_signal"] == "true"
    assert queue[0]["coding_status"] == "unassessed"


def test_precision_queue_prefers_access_and_nonreview_before_query_rank() -> None:
    rows = [
        candidate("doi:noabstract", b="true", p="true", abstract="false", rank="1"),
        candidate("doi:review", b="true", p="true", review="true", rank="1"),
        candidate("doi:primary", b="true", p="true", rank="10"),
    ]

    queue = select_b_to_p_precision_batch(rows, limit=1)

    assert queue[0]["candidate_id"] == "doi:primary"


def test_precision_queue_limit_is_enforced() -> None:
    rows = [candidate(f"doi:{index}", b="true", p="true", rank=str(index)) for index in range(5)]

    queue = select_b_to_p_precision_batch(rows, limit=2)

    assert len(queue) == 2
    assert [row["queue_rank"] for row in queue] == ["1", "2"]
