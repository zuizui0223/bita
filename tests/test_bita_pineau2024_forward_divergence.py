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
