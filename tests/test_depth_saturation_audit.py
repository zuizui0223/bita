from __future__ import annotations

import json

import pytest

from trait_architecture.depth_saturation_audit import (
    build_depth_audit_sample,
    write_depth_audit_outputs,
)


def _row(candidate_id: str, rank: int, status: str, *, route: str = "A_to_antagonism", query_id: str = "AH01") -> dict[str, str]:
    return {
        "query_id": query_id,
        "route_family": route,
        "query_rank": str(rank),
        "candidate_id": candidate_id,
        "doi": f"10.1/{candidate_id}",
        "title": f"Flower study {candidate_id}",
        "publication_year": "2020",
        "container_title": "Plant Ecology",
        "landing_page_url": "https://doi.org/example",
        "source_queries": query_id,
        "route_families": route,
        "metadata_A_signal": "true",
        "metadata_B_signal": "false",
        "metadata_P_signal": "false",
        "metadata_H_signal": "true",
        "metadata_W_signal": "false",
        "metadata_biology_context_term_count": "3",
        "shallow_screen_status": status,
        "shallow_screen_reason": "test",
    }


def test_head_tail_queue_is_route_balanced_and_excludes_head_tail_overlap() -> None:
    priority = "priority_for_shallow_source_coding"
    biological = "biological_context_needs_route_screen"
    rows = [
        _row("head-priority", 10, priority),
        _row("head-biological", 20, biological),
        _row("overlap", 100, priority),
        _row("tail-priority", 1700, priority),
        _row("tail-biological", 1800, biological),
        _row("overlap", 1750, priority, query_id="AH02"),
        _row("duplicate-tail", 1900, priority, query_id="AH03"),
        _row("duplicate-tail", 1650, priority, query_id="AH04"),
        _row("tail-other-route", 1700, priority, route="B_to_pollination", query_id="BP01"),
    ]

    sample, summary = build_depth_audit_sample(rows, per_route_stratum_group=10)

    by_group = {(row["route_family_audit"], row["audit_group"]): row for row in sample}
    assert ("A_to_antagonism", "head_priority") in by_group
    assert ("A_to_antagonism", "tail_priority") in by_group
    tail_ids = {
        row["candidate_id"] for row in sample
        if row["route_family_audit"] == "A_to_antagonism" and row["depth_stratum"] == "tail"
    }
    assert "overlap" not in tail_ids
    assert "duplicate-tail" in tail_ids
    duplicate = next(row for row in sample if row["candidate_id"] == "duplicate-tail")
    assert duplicate["query_rank"] == "1650"
    assert summary["tail_candidates_excluded_due_to_head_overlap_by_route"]["A_to_antagonism"] == 1
    assert summary["availability_after_within_cell_deduplication"]["A_to_antagonism"]["tail"]["priority"] == 2


def test_depth_audit_rejects_overlapping_or_invalid_strata() -> None:
    with pytest.raises(ValueError, match="tail ranks"):
        build_depth_audit_sample([], head_rank_max=200, tail_rank_min=200)
    with pytest.raises(ValueError, match="positive"):
        build_depth_audit_sample([], per_route_stratum_group=0)
    with pytest.raises(ValueError, match="positive integer"):
        build_depth_audit_sample([_row("bad", 1, "priority_for_shallow_source_coding") | {"query_rank": "x"}])


def test_depth_audit_writes_queue_and_summary(tmp_path) -> None:
    priority = "priority_for_shallow_source_coding"
    input_csv = tmp_path / "memberships.csv"
    header = list(_row("x", 1, priority))
    values = _row("x", 1, priority)
    input_csv.write_text(",".join(header) + "\n" + ",".join(values[field] for field in header) + "\n", encoding="utf-8")

    summary = write_depth_audit_outputs(input_csv, tmp_path / "out", head_rank_max=1, tail_rank_min=2, tail_rank_max=2)

    queue = (tmp_path / "out" / "depth_saturation_audit_queue.csv").read_text(encoding="utf-8")
    written_summary = json.loads((tmp_path / "out" / "depth_saturation_audit_summary.json").read_text(encoding="utf-8"))
    assert "head_priority" in queue
    assert summary["sampled_row_count"] == 1
    assert "metadata-to-source-coding" in written_summary["interpretation_boundary"]
