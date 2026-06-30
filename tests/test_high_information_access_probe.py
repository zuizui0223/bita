from urllib.error import HTTPError

from trait_architecture.high_information_access_probe import (
    HostIntervalFetcher,
    probe_content_url,
    run_access_probe,
)


class FakeFetcher:
    def prefix(self, url: str):
        if "pdf" in url:
            return 206, url, "application/pdf", b"%PDF-1.7"
        return 200, url, "text/html", b"<html><title>Paywall</title>"

    def json(self, url: str):
        if "zenodo.org/api/records/55" in url:
            return 200, {
                "metadata": {
                    "related_identifiers": [
                        {"identifier": "10.1/example", "relation": "IsSupplementTo"}
                    ]
                }
            }
        return 404, {}


def high(candidate_id: str, oa_url: str) -> dict[str, str]:
    return {
        "candidate_id": candidate_id,
        "title": "Example floral study",
        "doi": "10.1/example",
        "metadata_signal_count": "4",
        "triage_cohort": "high_information_empirical_candidate",
        "open_access_url": oa_url,
    }


def test_high_cohort_pdf_and_manifest_identity_are_separate() -> None:
    audit_rows = [high("openalex:W1", "https://repo.example/article.pdf")]
    source_receipts = [
        {
            "candidate_id": "openalex:W1", "study_doi": "10.1/example", "provider": "Zenodo",
            "source_kind": "repository_metadata_candidate", "resolution_status": "manifest_recovered",
            "request_url": "https://zenodo.org/api/records?q=example", "landing_page_url": "",
            "content_url": "https://zenodo.org/api/records/55/files/data.csv/content", "content_type": "", "notes": "fixture",
        },
        {
            "candidate_id": "openalex:W1", "study_doi": "10.1/example", "provider": "DataCite",
            "source_kind": "repository_metadata_candidate", "resolution_status": "landing_page_only",
            "request_url": "https://api.datacite.org/dois?query=example", "landing_page_url": "https://doi.org/10.2/landing",
            "content_url": "", "content_type": "", "notes": "landing fixture",
        },
    ]

    summaries, access, identities, report = run_access_probe(
        audit_rows, source_receipts, fetcher=FakeFetcher(), max_workers=1
    )

    assert len(access) == 1
    assert access[0].access_status == "public_pdf_prefix_recovered"
    assert len(identities) == 1
    assert identities[0].identity_status == "exact_article_relation_verified"
    assert summaries[0]["next_lane"] == "bounded_fulltext_screen_pdf_candidate"
    assert summaries[0]["repository_manifest_candidate_count"] == "1"
    assert report["repository_identity_probe_count"] == 1


def test_html_prefix_does_not_become_pdf_candidate() -> None:
    audit_rows = [high("openalex:W2", "https://repo.example/landing")]
    summaries, access, _, _ = run_access_probe(audit_rows, [], fetcher=FakeFetcher(), max_workers=1)

    assert access[0].access_status == "public_html_prefix_recovered"
    assert summaries[0]["next_lane"] == "verify_html_article_identity_before_text_screen"


def test_http_denial_is_reported_not_dropped() -> None:
    def denied(_url: str):
        raise HTTPError(_url, 403, "Forbidden", hdrs=None, fp=None)

    receipt = probe_content_url(
        candidate_id="openalex:W3", study_doi="10.1/example", source_label="fixture",
        source_url="https://publisher.example/file.pdf", fetch_prefix=denied,
    )

    assert receipt.access_status == "access_denied_or_required"
    assert receipt.http_status == "403"
