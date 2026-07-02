"""End-to-end verification of the finalized broad-evidence primary products.

The finalized design (BROAD_META_ANALYSIS_PROTOCOL.md) has two primary products
reproducible from committed data — the source-adjudicated direction map and the
audit-only yield meta-analysis core — and one deferred pooled effect-size layer
that must remain empty until Layer 4 primary-source recovery. These tests pin the
headline results so the design and the committed inputs cannot silently diverge.
"""

from __future__ import annotations

from pathlib import Path

from trait_architecture.broad_meta_analysis import (
    direction_map,
    meta_analysis,
    read_csv_rows,
    read_strata,
)
from trait_architecture.evidence_yield_meta_analysis import AUDIT_FIELDS, read_rows
from trait_architecture.evidence_yield_meta_model import build_evidence_yield_meta

ROOT = Path(__file__).parents[1]
BROAD = ROOT / "empirical" / "broad_reality_evidence"
ROUTE_RECORDS = BROAD / "broad_route_records.csv"
EFFECT_EXTRACTIONS = BROAD / "broad_effect_extractions.csv"
STRATA = BROAD / "broad_meta_analysis_strata.csv"
AUDIT_YIELD = BROAD / "priority_leak_audit" / "priority_leak_audit_yield_by_route_group_v1.csv"


def test_direction_map_primary_product_reproduces_the_one_supported_cell():
    """Primary product 1: the committed direction records yield exactly one
    channel cell with enough clusters to read a sign, and it is compatible."""
    cells = direction_map(read_csv_rows(ROUTE_RECORDS))
    supported = [c for c in cells if c["direction_map_status"] != "insufficient_directional_clusters"]

    assert len(supported) == 1
    cell = supported[0]
    assert cell["route"] == "B_to_pollination"
    assert cell["trait_class"] == "chemical_barrier"
    assert cell["design_class"] == "manipulation"
    assert cell["independent_clusters"] == 3
    assert cell["evaluable_direction_count"] == 3
    assert cell["compatible_count"] == 3
    assert cell["direction_map_status"] == "mostly_compatible_with_channel_assumption"


def test_deferred_pooled_layer_is_empty_by_design():
    """Deferred layer: no committed effect is eligible, so no stratum pools."""
    summaries, used_rows, diagnostics = meta_analysis(
        read_csv_rows(EFFECT_EXTRACTIONS), read_strata(STRATA)
    )
    assert diagnostics["eligible_primary_effect_count"] == 0
    assert diagnostics["pooled_stratum_count"] == 0
    assert used_rows == []
    assert summaries  # strata are configured; they are simply all insufficient
    assert all(row["analysis_status"] == "insufficient_independent_clusters" for row in summaries)


def test_yield_meta_core_reproduces_from_audit_without_the_corpus():
    """Primary product 2 core: the priority-vs-nonpriority enrichment meta and
    the audit-calibrated rates reproduce from committed audit data alone, and the
    projection layer is explicitly skipped rather than emitting fake zeros."""
    audit_rows = read_rows(AUDIT_YIELD, AUDIT_FIELDS)
    route_rows, effects, diagnostics, summary = build_evidence_yield_meta([], audit_rows)

    assert diagnostics["screened_corpus_supplied"] is False
    assert diagnostics["projection_layer_status"] == "skipped_corpus_not_supplied"

    # audit-derived rates remain valid without the corpus
    ap_priority = next(
        r for r in route_rows if r["route"] == "A_to_pollination" and r["audit_group"] == "priority"
    )
    assert float(ap_priority["audit_direct_route_yield"]) > 0
    assert float(ap_priority["posterior_direct_rate_mean"]) > 0
    # projections must be blanked, never zero-filled, when the corpus is absent
    assert ap_priority["equal_yield_projection_mean"] == ""
    assert ap_priority["l2_candidate_memberships"] == ""
    assert ap_priority["projection_boundary"].startswith("corpus_not_supplied")

    # enrichment meta pools across informative routes; result is non-significant
    assert summary["analysis"] == "priority_vs_biological_nonpriority_direct_yield"
    assert int(summary["included_route_comparisons"]) == 4
    assert int(summary["excluded_double_zero_routes"]) == 1
    low = float(summary["ci_low_odds_ratio"])
    high = float(summary["ci_high_odds_ratio"])
    assert low < 1.0 < high  # confidence interval crosses 1: no significant enrichment
    b_to_p = next(e for e in effects if e["route"] == "B_to_pollination")
    assert b_to_p["status"] == "uninformative_double_zero_direct_yield"
