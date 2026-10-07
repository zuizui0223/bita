from __future__ import annotations

import json
from pathlib import Path

from scripts.summarize_direct_access_geometry_route_rate_identifiability import (
    summarize,
)

ROOT = Path(__file__).resolve().parents[1]
FRAME = (
    ROOT
    / "empirical"
    / "floral_defence_selectivity"
    / "formal_bibliographic_frame_v2"
)
AUDIT = FRAME / "DIRECT_ACCESS_GEOMETRY_ROUTE_RATE_IDENTIFIABILITY_AUDIT_V1.csv"
SUMMARY = FRAME / "DIRECT_ACCESS_GEOMETRY_ROUTE_RATE_IDENTIFIABILITY_SUMMARY_V1.json"


def test_route_rate_identifiability_audit_is_complete_and_frozen() -> None:
    observed = summarize(AUDIT)
    frozen = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert observed == frozen

    assert observed["source_frame_programs"] == 33
    assert observed["strict_zero_inclusive_both_route_programs"] == 7
    assert observed["not_strict_zero_inclusive_both_route_programs"] == 26
    assert observed["class_counts"] == {
        "BOTH_ROUTE_COUNTS_NO_ZERO_INCLUSIVE_DENOMINATOR": 1,
        "CONDITIONAL_ROUTE_CHOICE_ONLY": 6,
        "OTHER_ROUTE_RESOLVED_NOT_RATE_IDENTIFIABLE": 1,
        "ROBBERY_PREVALENCE_ONLY": 18,
        "UNRESOLVED_SOURCE": 0,
        "ZERO_INCLUSIVE_BOTH_ROUTE_RATES": 7,
    }
    assert observed["strict_program_ids"] == [
        "Adler_Leege_Irwin_2016",
        "Bhandari_Das_Karmakar_2024",
        "Lara_Ornelas_2001",
        "Newman_Thomson_2005_Linaria",
        "Tie_et_al_2023",
        "Wang_et_al_2013_Impatiens",
        "Wu_Gao_2024_Thunia_alba",
    ]


def test_route_rate_audit_claim_is_descriptive_not_prevalence_inference() -> None:
    result = summarize(AUDIT)
    assert result["status"] == "POST_HOC_DESIGN_AUDIT_COMPLETE"
    assert "post-hoc finite-frame design audit" in result["claim"]
    assert "all ecological literature" in result["claim"]
    assert "does_not_increment_standardized_network_k" in result["claim_boundaries"]
    assert "strict_class_requires_common_zero_inclusive_denominator" in result["claim_boundaries"]
