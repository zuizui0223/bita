from __future__ import annotations

import json

from trait_architecture.broad_reality_depth import (
    DepthSaturationCollector,
    write_depth_saturation_outputs,
)
from trait_architecture.broad_reality_evidence import Candidate


def _candidate(candidate_id: str, *, priority: bool, rank: int = 1) -> Candidate:
    return Candidate(
        candidate_id=candidate_id,
        doi="",
        title="Floral trait and pollination" if priority else "Flower biology",
        authors="",
        publication_year="2020",
        work_type="journal-article",
        container_title="Plant Ecology",
        publisher="",
        landing_page_url="",
        cited_by_count="",
        abstract_available=False,
        source_queries={"AP01"},
        route_families={"A_to_pollination"},
        query_ranks=[rank],
        metadata_A_signal=priority,
        metadata_P_signal=priority,
    )


def _query() -> dict[str, str]:
    return {
        "query_id": "AP01",
        "route_family": "A_to_pollination",
        "query_text": "floral trait pollination",
    }


def test_collector_records_rank_binned_metadata_yield() -> None:
    collector = DepthSaturationCollector(bin_size=2)
    collector.observe(
        _query(), 0,
        [_candidate("p", priority=True, rank=1), _candidate("u", priority=False, rank=2)],
        2,
    )
    collector.observe(_query(), 2, [_candidate("p2", priority=True, rank=3)], 1)

    rows = collector.ordered_records()
    assert [(row["rank_start"], row["rank_end"]) for row in rows] == [("1", "2"), ("3", "3")]
    assert rows[0]["candidate_memberships"] == "2"
    assert rows[0]["priority_memberships"] == "1"
    assert rows[0]["priority_membership_rate"] == "0.500000"
    memberships = collector.ordered_memberships()
    assert [row["query_rank"] for row in memberships] == ["1", "2", "3"]
    assert memberships[0]["shallow_screen_status"] == "priority_for_shallow_source_coding"
    assert "query-rank membership" in memberships[0]["membership_warning"]

    summary = collector.summary()
    assert summary["retrieved_candidate_memberships"] == 3
    assert summary["title_bearing_membership_rows"] == 3
    assert summary["priority_memberships"] == 2
    assert summary["overall_priority_membership_rate"] == 2 / 3
    assert summary["by_rank_bin"]["1-2"]["priority_membership_rate"] == 0.5
    assert "Do not automatically" in summary["decision_boundary"]


def test_collector_writes_table_and_explicit_boundary(tmp_path) -> None:
    collector = DepthSaturationCollector(bin_size=200)
    collector.observe(_query(), 0, [_candidate("p", priority=True)], 1)

    write_depth_saturation_outputs(tmp_path, collector)

    csv_text = (tmp_path / "broad_reality_evidence_depth_saturation.csv").read_text(encoding="utf-8")
    memberships = (tmp_path / "broad_reality_evidence_rank_memberships.csv").read_text(encoding="utf-8")
    summary = json.loads(
        (tmp_path / "broad_reality_evidence_depth_saturation_summary.json").read_text(encoding="utf-8")
    )
    assert "priority_memberships" in csv_text
    assert "metadata-only screening" in csv_text
    assert "query_rank" in memberships
    assert "query-rank membership" in memberships
    assert summary["query_count"] == 1


def test_collector_rejects_invalid_page_size_or_page_length() -> None:
    try:
        DepthSaturationCollector(bin_size=0)
    except ValueError as error:
        assert "positive" in str(error)
    else:
        raise AssertionError("zero bin size should fail")

    collector = DepthSaturationCollector(bin_size=1)
    try:
        collector.observe(_query(), 0, [], 2)
    except ValueError as error:
        assert "cannot exceed" in str(error)
    else:
        raise AssertionError("oversized observed page should fail")
