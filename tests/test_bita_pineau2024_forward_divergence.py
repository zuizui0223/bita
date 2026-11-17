"""Pineau 2024 registered source / biological denominator contract.

No individual isolate/competition well is ever a new evolution replicate.
"""
import math
import pytest

from scripts.audit_bita_pineau2024_forward_divergence import (
    DOI, PMCID, PO_LINE_VOLUMES, ORIGINAL_AUTHOR_POSITIVE_LINE_IDS,
    AUTHOR_REPO_COMMIT, AUTHOR_F2_GIT_BLOB_SHA1,
    git_blob_sha1, wilson, check_article_jats,
    check_unparsed_original_xlsx,
)


def test_source_identity_and_five_evolving_populations_are_frozen():
    assert DOI == "10.1038/s41559-024-02367-y"
    assert PMCID == "PMC11090753"
    assert AUTHOR_REPO_COMMIT == "071affa79f16f0a469f099058372a7488c35c0c2"
    assert AUTHOR_F2_GIT_BLOB_SHA1 == "4b5dba14b244b335294ca28be52a77c5dc278d79"
    assert len(PO_LINE_VOLUMES) == 5
    assert [label for label, ratio in PO_LINE_VOLUMES if ratio > 10] == list(
        ORIGINAL_AUTHOR_POSITIVE_LINE_IDS
    )
    assert PO_LINE_VOLUMES == (
        ("PO-1", 2.0), ("PO-2", 1.5), ("PO-3", 37.0),
        ("PO-4", 27.0), ("PO-5", 16.0)
    )


def test_wilson_3_of_5_biological_replicates_not_cluster_replicates():
    lo, hi = wilson(3, 5)
    assert lo == pytest.approx(0.2307242812760129, abs=1e-12)
    assert hi == pytest.approx(0.8823792257673522, abs=1e-12)
    assert lo < 0.6 < hi
    with pytest.raises(ValueError, match="n must"):
        wilson(6, 5)
    with pytest.raises(ValueError, match="n must"):
        wilson(1, 0)


def test_source_article_gate_requires_both_doi_and_original_line_claim():
    xml = (b'<article><front><article-meta>'
           b'<article-id pub-id-type="doi">10.1038/s41559-024-02367-y</article-id>'
           b'</article-meta></front><body><p>'
           b'Emergence and maintenance of stable coexistence: '
           b'three of five populations, PO-3 PO-4 PO-5, at 715 transfers. '
           b'Small and large yeast, oxygen constraint.'
           b'</p></body></article>')
    d = check_article_jats(xml)
    assert d["three_of_five_source_text_gate"] is True
    with pytest.raises(ValueError, match="DOI"):
        check_article_jats(xml.replace(b'10.1038/s41559-024-02367-y', b'other-doi'))
    with pytest.raises(ValueError, match="3/5"):
        check_article_jats(xml.replace(b'three of five populations', b'none of five populations'))
    with pytest.raises(ValueError, match="valid JATS"):
        check_article_jats(b'<article>')


def test_binary_workbook_not_spreadsheet_reanalyzed_or_from_unverified_bytes():
    with pytest.raises(ValueError, match="ZIP/XML XLSX"):
        check_unparsed_original_xlsx(b'not an actual workbook')
    with pytest.raises(ValueError, match="fingerprint"):
        check_unparsed_original_xlsx(b"PK\x03\x04"+b'tampered workbook')


def test_git_sha_uses_github_blob_framing():
    import hashlib
    data = b"abc"
    canonical = hashlib.sha1(b"blob 3\0abc").hexdigest()
    assert git_blob_sha1(data) == canonical


def test_frozen_derived_readout_keeps_competition_and_evolution_replicates_separate():
    import json
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    file=root/"empirical/trait_architecture_history/pineau2024_original_forward_divergence.json"
    d=json.loads(file.read_text(encoding="utf8"))
    evo=d["single_evolution_programme"]
    fit=d["source_audit"]["figure2_code_fit"]
    original=d["source_audit"]["original_workbook_bytes"]
    assert evo["independent_initial_aerobic_populations"] == 5
    assert evo["authors_dimorphism_successes"] == 3
    assert evo["authors_dimorphism_failures"] == 2
    assert evo["sampled_small_and_large_isolates_per_evolution_population"] == 20
    assert [p["evolved_population"] for p in evo["line_specific_outcomes_from_published_article"]
            if p["authors_endpoint_phenotypically_dimorphic"]] == ["PO-3","PO-4","PO-5"]
    assert fit["source_code_fitted_large_delta_intercept"] == pytest.approx(.095083)
    assert fit["source_code_fitted_large_delta_slope"] == pytest.approx(-1.0274)
    assert fit["equilibrium_large_fraction_recovered_from_fit"] == pytest.approx(.09254720654078255)
    assert fit["original_standard_O2_competition_code_series"] == 8
    assert fit["original_high_O2_competition_code_series"] == 7
    assert fit["publisher_high_O2_figure_caption_n"] == 6
    assert fit["high_O2_count_discrepancy_unresolved"] is True
    assert original["original_raw_workbook_bytes"] == 1535384
    assert original["original_raw_workbook_sha256"] == "b6bc44d5085344292b5b33cac81369652b25e56f0947c1057cfc00ae4947057f"
    assert original["workbook_cells_analyzed"] is False
    assert d["source_audit"]["jats"]["article_binary_verified"] is False
    guards=d["comparability_and_scope"]
    assert guards["no_primary_cross_treatment_risk_ratio_or_fisher_test"] is True
    assert guards["not_20_independent_evolution_origin_replicates_per_population"] is True
    assert guards["oxygen_intervention_tests_retention_not_de_novo_origin"] if "oxygen_intervention_tests_retention_not_de_novo_origin" in guards else d["mechanism_and_maintenance"]["oxygen_intervention_tests_retention_not_de_novo_origin"]
