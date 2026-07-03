from trait_architecture.d_a_source_resolver import (
    NCBI_IDCONV,
    doi_from_source,
    resolve_candidate_source,
    resolve_candidates,
    resolve_source_doi,
    summarise,
)


def _fetcher(crossref=None, idconv=None):
    """fetch_json that serves canned idconv and Crossref payloads.

    ``idconv`` maps an identifier substring -> doi; ``crossref`` maps a DOI
    substring -> Crossref message payload.
    """

    crossref = crossref or {}
    idconv = idconv or {}

    def fetch(url):
        if "idconv" in url:
            for ident, doi in idconv.items():
                if ident in url:
                    return 200, {"records": [{"doi": doi}]}
            return 200, {"records": [{"status": "error"}]}
        for key, payload in crossref.items():
            if key in url:
                return 200, payload
        return 404, None

    return fetch


def test_doi_from_source_only_accepts_doi_prefix():
    assert doi_from_source("doi:10.7554/eLife.07641") == "10.7554/eLife.07641"
    assert doi_from_source("pmid:27325896") == ""


def test_resolve_source_doi_handles_each_identifier_kind():
    fetch = _fetcher(idconv={"27325896": "10.1111/evo.12912", "PMC11442331": "10.3390/x"})
    assert resolve_source_doi("doi:10.7554/eLife.07641", fetch_json=fetch)[:2] == ("10.7554/eLife.07641", "declared_doi")
    assert resolve_source_doi("pmid:27325896", fetch_json=fetch)[:2] == ("10.1111/evo.12912", "pmid_idconv")
    assert resolve_source_doi("url:ncbi.nlm.nih.gov/pmc/articles/PMC11442331", fetch_json=fetch)[:2] == ("10.3390/x", "pmcid_idconv")
    # A DOI embedded directly in a URL is preferred over any id-conversion.
    assert resolve_source_doi("url:doi.org/10.1093/aob/mct303", fetch_json=fetch)[:2] == ("10.1093/aob/mct303", "doi_in_url")
    # A bare URL with no recoverable identifier is honest missingness.
    assert resolve_source_doi("url:research.franklin.uga.edu/anderson", fetch_json=fetch)[1] == "unresolvable"


def test_fulltext_link_classified():
    payload = {"message": {"type": "journal-article", "is-referenced-by-count": 42,
                           "license": [{"URL": "cc-by"}],
                           "link": [{"content-type": "application/pdf"}, {"content-type": "text/xml"}]}}
    receipt = resolve_candidate_source(
        {"candidate_id": "dA_cand_schiestl2015", "source": "doi:10.7554/eLife.07641"},
        fetch_json=_fetcher(crossref={"10.7554": payload}),
    )
    assert receipt.resolved == "true"
    assert receipt.resolution_method == "declared_doi"
    assert receipt.access_state == "oa_or_fulltext_link_present"
    assert receipt.fulltext_link_count == "2"
    assert "application/pdf" in receipt.fulltext_content_types
    assert receipt.license_present == "true"


def test_pmid_resolves_then_crossref_classifies():
    payload = {"message": {"type": "journal-article", "link": [{"content-type": "application/pdf"}]}}
    receipt = resolve_candidate_source(
        {"candidate_id": "dA_cand_conflicting_seedpred", "source": "pmid:27325896"},
        fetch_json=_fetcher(crossref={"10.1111": payload}, idconv={"27325896": "10.1111/evo.12912"}),
    )
    assert receipt.resolution_method == "pmid_idconv"
    assert receipt.doi == "10.1111/evo.12912"
    assert receipt.access_state == "oa_or_fulltext_link_present"


def test_linked_dataset_relation_takes_priority():
    payload = {"message": {"type": "journal-article",
                           "link": [{"content-type": "application/pdf"}],
                           "relation": {"is-supplemented-by": [{"id": "10.5061/dryad.x"}]}}}
    receipt = resolve_candidate_source(
        {"candidate_id": "c", "source": "doi:10.1/x"},
        fetch_json=_fetcher(crossref={"10.1": payload}),
    )
    assert receipt.access_state == "linked_data_relation_present"
    assert "is-supplemented-by" in receipt.data_relation_types


def test_metadata_only_when_no_links():
    payload = {"message": {"type": "journal-article"}}
    receipt = resolve_candidate_source(
        {"candidate_id": "c", "source": "doi:10.2/y"},
        fetch_json=_fetcher(crossref={"10.2": payload}),
    )
    assert receipt.access_state == "metadata_only"


def test_unresolvable_and_crossref_unresolved_states():
    unresolvable = resolve_candidate_source(
        {"candidate_id": "c", "source": "url:example.org/no-id"}, fetch_json=_fetcher()
    )
    assert unresolvable.access_state == "no_doi_resolved"
    assert unresolvable.resolution_method == "unresolvable"

    unresolved = resolve_candidate_source(
        {"candidate_id": "c", "source": "doi:10.9/missing"}, fetch_json=_fetcher()
    )
    assert unresolved.access_state == "crossref_unresolved"


def test_summarise_counts_states_and_methods():
    rows = [
        {"candidate_id": "a", "source": "doi:10.7554/eLife.07641"},
        {"candidate_id": "b", "source": "url:example.org/no-id"},
    ]
    payload = {"message": {"type": "journal-article", "link": [{"content-type": "application/pdf"}]}}
    receipts = resolve_candidates(rows, fetch_json=_fetcher(crossref={"10.7554": payload}))
    summary = summarise(receipts)
    assert summary["candidate_count"] == 2
    assert summary["counts_by_access_state"]["oa_or_fulltext_link_present"] == 1
    assert summary["counts_by_access_state"]["no_doi_resolved"] == 1
    assert summary["counts_by_resolution_method"]["declared_doi"] == 1
    assert summary["counts_by_resolution_method"]["unresolvable"] == 1
