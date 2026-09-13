from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "THEORY_TO_REALITY_PATTERN_RECOVERY_V1.md"
CONCORDANCE = ROOT / "docs" / "THREE_CHAPTER_PATTERN_SYNTHESIS_CONCORDANCE_V1.md"
PROMOTION = ROOT / "empirical" / "mechanism_pattern_synthesis" / "BITA_META_ANALYSIS_PROMOTION_RULE_V1.md"
REGISTRY = ROOT / "empirical" / "mechanism_pattern_synthesis" / "BITA_QUANTITATIVE_LANE_REGISTRY_V1.csv"
LARCENY = ROOT / "empirical" / "broad_reality_evidence" / "larceny_gate" / "LARCENY_GATE_READOUT_V1.md"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md"
STATUS = ROOT / "docs" / "PUBLICATION_STATUS.md"


def _rows() -> list[dict[str, str]]:
    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_pattern_protocol_matches_active_mechanism_identification_ownership() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    lower = text.lower()
    assert "mathematical identification mechanism" in text
    assert "Delta_AD W" in text
    assert "trait interaction" in text
    assert "RECURRENT_CONSTITUENT_BIOLOGY" in text
    assert "FRAGMENTED_IDENTIFICATION" in text
    assert "56 directional route records from 25 independent biological clusters" in text
    assert "17 high-information systems" in text
    assert "architecture-value quantities" in lower
    assert "slk" in lower
    assert "final mechanism-allocation gap" in text


def test_active_manuscript_places_pattern_before_next_experiment() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "Trait interaction is not ecological mechanism" in text
    assert "56 directional route records from 25 independent biological clusters" in text
    assert "17 high-information systems" in text
    assert text.index("## 5. The empirical pattern") < text.index("## 6. Designing the next identifiable experiment")
    assert "None closes the entire sequence" in text


def test_quantitative_registry_has_three_directionally_resolved_routes_one_uncertain_and_empty_full_allocation() -> None:
    rows = _rows()
    assert len(rows) == 5
    by_id = {row["lane_id"]: row for row in rows}

    expected_clusters = {
        "BITA_Q1_larceny_female": 48,
        "BITA_Q2_larceny_visitation": 22,
        "BITA_Q3_larceny_reward": 28,
        "BITA_Q4_larceny_male": 11,
        "BITA_Q5_complete_mechanism_allocation": 0,
    }
    for lane, n in expected_clusters.items():
        assert int(by_id[lane]["independent_clusters"]) == n

    for lane in (
        "BITA_Q1_larceny_female",
        "BITA_Q2_larceny_visitation",
        "BITA_Q3_larceny_reward",
    ):
        assert float(by_id[lane]["ci_high"]) < 0

    male = by_id["BITA_Q4_larceny_male"]
    assert float(male["ci_low"]) < 0 < float(male["ci_high"])
    assert "uncertain" in male["claim_ceiling"].lower()

    strict = by_id["BITA_Q5_complete_mechanism_allocation"]
    assert strict["analysis_status"] == "NOT_AVAILABLE"
    assert int(strict["effect_count"]) == 0
    assert "separability" in strict["claim_ceiling"]
    assert "independent remaining-channel assay" in strict["claim_ceiling"]


def test_registry_points_to_current_frozen_larceny_readout() -> None:
    rows = _rows()
    source = "empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_READOUT_V1.md"
    assert all(row["source_basis"] == source for row in rows[:4])
    assert (ROOT / source).exists()
    text = LARCENY.read_text(encoding="utf-8")
    for token in ("**48**", "−0.210", "−0.291", "−0.483", "−0.148"):
        assert token in text


def test_promotion_rule_is_fail_closed_and_does_not_backfill_mechanism() -> None:
    text = PROMOTION.read_text(encoding="utf-8")
    for phrase in (
        "focal A x D total interaction",
        "selective antagonist intervention",
        "selective pollinator intervention",
        "four-way separability diagnostic",
        "independent assay for any remaining joint channel",
        "unmeasured residual is not called joint cost by subtraction",
        "conditional on that admission",
        "not an independent test of recurrence",
    ):
        assert phrase in text
    assert "companion SLK spine" in text


def test_three_paper_concordance_preserves_current_ownership_and_literature_first_order() -> None:
    text = CONCORDANCE.read_text(encoding="utf-8")
    assert "SCH / BALANCE / BITA" in text
    assert "design the strongest focal causal experiment last" in text
    assert "trait interaction != ecological mechanism" in text
    assert "architecture-value transport" in text
    assert "companion SLK flagship" in text
    assert "### BITA final gap" in text
    assert "strict mechanism-allocation lane remains empty" in text


def test_publication_status_and_new_protocol_agree_on_claim_ceiling() -> None:
    status = STATUS.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    assert "Trait interaction is not ecological mechanism" in status
    assert "56 route records / 25 independent biological clusters / 17-system high-information frontier" in status
    assert "not the central novelty claim of the BITA paper" in status
    assert "not natural prevalence" in protocol
