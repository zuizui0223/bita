from trait_architecture.d_a_source_resolver import (
    doi_from_source,
    resolve_candidate_source,
    resolve_candidates,
    summarise,
)


def _fetcher(mapping):
    """Return a fetch_json that serves canned Crossref payloads by DOI substring."""

    def fetch(url):
        for doi, payload in mapping.items():
            if doi in url:
                return 200, payload
        return 404, None

    return fetch


def test_doi_from_source_only_accepts_doi_prefix():
    assert doi_from_source("doi:10.7554/eLife.07641") == "10.7554/eLife.07641"
    assert doi_from_source("pmid:27325896") == ""
    assert doi_from_source("url:academic.oup.com/aob/article") == ""


def test_fulltext_link_classified():
    payload = {"message": {"type": "journal-article", "is-referenced-by-count": 42,
                           "license": [{"URL": "cc-by"}],
                           "link": [{"content-type": "application/pdf"}, {"content-type": "text/xml"}]}}
    receipt = resolve_candidate_source(
        {"candidate_id": "dA_cand_schiestl2015", "source": "doi:10.7554/eLife.07641"},
        fetch_json=_fetcher({"10.7554": payload}),
    )
    assert receipt.resolved == "true"
    assert receipt.access_state == "oa_or_fulltext_link_present"
    assert receipt.fulltext_link_count == "2"
    assert "application/pdf" in receipt.fulltext_content_types
    assert receipt.license_present == "true"


def test_linked_dataset_relation_takes_priority():
    payload = {"message": {"type": "journal-article",
                           "link": [{"content-type": "application/pdf"}],
                           "relation": {"is-supplemented-by": [{"id": "10.5061/dryad.x"}]}}}
    receipt = resolve_candidate_source(
        {"candidate_id": "c", "source": "doi:10.1/x"},
        fetch_json=_fetcher({"10.1": payload}),
    )
    assert receipt.access_state == "linked_data_relation_present"
    assert "is-supplemented-by" in receipt.data_relation_types


def test_metadata_only_when_no_links():
    payload = {"message": {"type": "journal-article"}}
    receipt = resolve_candidate_source(
        {"candidate_id": "c", "source": "doi:10.2/y"},
        fetch_json=_fetcher({"10.2": payload}),
    )
    assert receipt.access_state == "metadata_only"


def test_no_doi_and_unresolved_states():
    no_doi = resolve_candidate_source(
        {"candidate_id": "c", "source": "pmid:27325896"}, fetch_json=_fetcher({})
    )
    assert no_doi.access_state == "no_doi_supplied"
    assert no_doi.resolved == "false"

    unresolved = resolve_candidate_source(
        {"candidate_id": "c", "source": "doi:10.9/missing"}, fetch_json=_fetcher({})
    )
    assert unresolved.access_state == "crossref_unresolved"


def test_summarise_counts_states():
    rows = [
        {"candidate_id": "a", "source": "doi:10.7554/eLife.07641"},
        {"candidate_id": "b", "source": "pmid:1"},
    ]
    payload = {"message": {"type": "journal-article", "link": [{"content-type": "application/pdf"}]}}
    receipts = resolve_candidates(rows, fetch_json=_fetcher({"10.7554": payload}))
    summary = summarise(receipts)
    assert summary["candidate_count"] == 2
    assert summary["counts_by_access_state"]["oa_or_fulltext_link_present"] == 1
    assert summary["counts_by_access_state"]["no_doi_supplied"] == 1
