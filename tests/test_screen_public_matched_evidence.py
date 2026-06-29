import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "screen_public_matched_evidence.py"
SPEC = importlib.util.spec_from_file_location("public_evidence_screen", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def candidate(candidate_id: str, **overrides: str) -> dict[str, str]:
    row = {
        "candidate_id": candidate_id,
        "seed_routes": "A",
        "seed_query_ids": "A01",
        "title": "A floral trait candidate",
        "authors": "Author",
        "publication_year": "2024",
        "doi": "https://doi.org/10.1000/ARTICLE",
        "landing_page_url": "https://publisher.example/article",
        "open_access_url": "https://publisher.example/article.pdf",
        "is_open_access": "True",
        "metadata_match_score": "5",
        "metadata_attraction_signal": "True",
        "metadata_barrier_signal": "True",
        "metadata_pollination_signal": "True",
        "metadata_antagonist_signal": "True",
        "metadata_recoverability_signal": "True",
    }
    row.update(overrides)
    return row


def test_normalise_doi_handles_urls_and_query_strings() -> None:
    assert MODULE.normalise_doi("https://doi.org/10.1000/ABC?source=x") == "10.1000/abc"
    assert MODULE.normalise_doi("doi:10.1000/ABC.") == "10.1000/abc"


def test_page_resource_extraction_keeps_supplement_repository_and_table_leads() -> None:
    supplements, machine, repositories = MODULE.extract_page_resources(
        [
            ("https://publisher.example/supporting-information.pdf", "Supporting Information"),
            ("https://zenodo.org/record/1", "Dataset"),
            ("https://zenodo.org/record/1/data.csv", "CSV"),
        ]
    )

    assert supplements == ["https://publisher.example/supporting-information.pdf"]
    assert machine == ["https://zenodo.org/record/1/data.csv"]
    assert repositories == ["https://zenodo.org/record/1", "https://zenodo.org/record/1/data.csv"]


def test_datacite_returns_only_explicitly_related_nonarticle_datasets() -> None:
    payload = {
        "data": [
            {
                "attributes": {
                    "doi": "10.5061/dryad.example",
                    "url": "https://datadryad.org/stash/dataset/doi:10.5061/dryad.example",
                    "types": {"resourceTypeGeneral": "Dataset"},
                    "relatedIdentifiers": [
                        {"relatedIdentifier": "https://doi.org/10.1000/article", "relationType": "IsSupplementTo"}
                    ],
                }
            },
            {
                "attributes": {
                    "doi": "10.1000/other-article",
                    "types": {"resourceTypeGeneral": "Text"},
                    "relatedIdentifiers": [
                        {"relatedIdentifier": "10.1000/article", "relationType": "IsCitedBy"}
                    ],
                }
            },
            {
                "attributes": {
                    "doi": "10.5281/zenodo.unrelated",
                    "types": {"resourceTypeGeneral": "Dataset"},
                    "relatedIdentifiers": [],
                }
            },
        ]
    }

    found = MODULE.datacite_related_datasets(payload, "10.1000/article")

    assert found == [
        {
            "doi": "10.5061/dryad.example",
            "url": "https://datadryad.org/stash/dataset/doi:10.5061/dryad.example",
            "relation_types": "IsSupplementTo",
        }
    ]


def test_screen_preserves_each_candidate_and_never_auto_promotes_to_d1(monkeypatch) -> None:
    monkeypatch.setattr(
        MODULE,
        "fetch_html_links",
        lambda url, timeout: (
            "fetched_html",
            [("https://figshare.com/file.csv", "download csv")],
            url,
        ),
    )
    monkeypatch.setattr(
        MODULE,
        "query_datacite",
        lambda doi, timeout: ("queried", []),
    )

    screened, report = MODULE.screen_candidates(
        [candidate("first"), candidate("second", is_open_access="False", open_access_url="")],
        timeout_seconds=1,
        sleep_seconds=0,
        fetch_landing_pages=True,
    )

    assert report["candidate_count"] == 2
    assert len(screened) == 2
    assert all(row["automatic_evidence_level"] == "M0_candidate_needs_full_text" for row in screened)
    assert screened[0]["public_evidence_action"] == "retrieve_public_table_then_full_text_screen"
    assert "No missing link is evidence of no data" in screened[0]["automatic_screen_warning"]
