from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "empirical" / "floral_defence_selectivity"


def test_old_bita_evidence_assets_remain_present() -> None:
    required = [
        ROOT / "manuscript/supplementary/tables/TABLE_S3_MECHANISM_PATTERN_LEDGER.csv",
        ROOT / "empirical/mechanism_pattern_synthesis/OUTCOME_BLIND_DOMAIN_MODERATOR_MATRIX_V1.csv",
        ROOT / "empirical/mechanism_pattern_synthesis/CATALPA_1982_MATCHED_SELECTIVITY_EFFECTS_V1.md",
        ROOT / "empirical/mechanism_pattern_synthesis/PEDICULARIS_2015_MATCHED_SELECTIVITY_EFFECTS_V1.md",
        ROOT / "empirical/mechanism_pattern_synthesis/THUNIA_2024_MATCHED_SELECTIVITY_EFFECTS_V1.md",
        ROOT / "empirical/mechanism_pattern_synthesis/HOLDOUT_DOMAIN_RULE_VALIDATION_PROTOCOL_V1.md",
    ]
    assert all(path.exists() for path in required)


def test_canonical_readme_preserves_earlier_bita_provenance() -> None:
    text = (MODULE / "README.md").read_text(encoding="utf-8")
    assert "does **not** delete earlier BITA results" in text
    assert "56-route / 25 historical cluster-label / 17-system" in text


def test_milestone_readout_reports_current_counts_and_claim_ceiling() -> None:
    text = (MODULE / "MILESTONE1_READOUT.md").read_text(encoding="utf-8")
    assert "17 independent matched-system clusters" in text
    assert "Stage 2 strict: 3" in text
    assert "Stage 2 null-compatible: 4" in text
    assert "Stage 2 transition: 4" in text
    assert "hold-out clusters: 1" in text
    assert "systematic-expansion clusters: 2" in text
    assert "does not yet establish" in text
    assert "56 directional route records" in text


def test_original_same_system_d_side_is_fully_inherited() -> None:
    registry = (MODULE / "matched_system_registry.csv").read_text(encoding="utf-8")
    assert "Ipomopsis_2004" in registry
    assert "Impatiens_2018" in registry


def test_phlox_systematic_expansion_is_preserved_as_a_new_matched_system() -> None:
    registry = (MODULE / "matched_system_registry.csv").read_text(encoding="utf-8")
    outcomes = (MODULE / "outcome_codes.csv").read_text(encoding="utf-8")
    assert "Phlox_2011" in registry
    assert "Phlox_2011" in outcomes
