from __future__ import annotations

import csv
import json

from trait_architecture.d_a_caruso_index_probe import (
    CARUSO_DOI,
    probe_caruso_index,
    summarise,
    write_outputs,
)


def _json_responder(url: str):
    if "api.crossref.org" in url:
        return 200, {"message": {"resource": {"primary": "https://onlinelibrary.wiley.com/doi/10.1111/evo.13639"}}}
    if "api.unpaywall.org" in url:
        return 200, {"best_oa_location": {"url": "https://example.org/caruso"}}
    if "api.openalex.org" in url:
        return 200, {"locations": [{"landing_page_url": "https://example.org/caruso-repository"}]}
    if "api.datacite.org" in url:
        return 200, {
            "data": [{
                "attributes": {
                    "doi": "10.5061/dryad.test123",
                    "types": {"resourceTypeGeneral": "Dataset"},
                    "relatedIdentifiers": [{"relatedIdentifier": CARUSO_DOI}],
                }
            }]
        }
    raise AssertionError(url)


def test_explicit_datacite_relation_is_a_dataset_candidate_not_an_effect() -> None:
    rows = probe_caruso_index(
        fetch_json=_json_responder,
        fetch_html=lambda _url: (200, "<html></html>"),
        unpaywall_email="actions@users.noreply.github.com",
    )
    candidates = [row for row in rows if row.access_status == "dataset_candidate_related_to_source_doi"]
    assert len(candidates) == 1
    assert candidates[0].candidate_url == "https://doi.org/10.5061/dryad.test123"
    assert candidates[0].related_to_source_doi == "explicit_related_identifier"
    assert "effect" not in candidates[0].do_not_infer.casefold() or "effect size" in candidates[0].do_not_infer.casefold()
    report = summarise(rows)
    assert report["explicitly_related_dataset_count"] == 1
    assert report["next_action"] == "resolve_dataset_metadata_and_primary_study_index"


def test_publisher_dataset_host_link_is_only_a_candidate_route() -> None:
    rows = probe_caruso_index(
        fetch_json=lambda _url: (200, {"message": {}}),
        fetch_html=lambda _url: (200, '<a href="https://datadryad.org/stash/dataset/doi:10.5061/dryad.xyz">Data</a>'),
        unpaywall_email="actions@users.noreply.github.com",
    )
    candidates = [row for row in rows if row.probe_source == "publisher_landing" and row.candidate_url]
    assert len(candidates) == 1
    assert candidates[0].candidate_kind == "dataset_landing"
    assert candidates[0].related_to_source_doi == "not_asserted"
    assert summarise(rows)["dataset_candidate_count"] == 1


def test_failed_metadata_routes_are_reported_without_guessing(tmp_path) -> None:
    rows = probe_caruso_index(
        fetch_json=lambda _url: (503, None),
        fetch_html=lambda _url: (403, ""),
        unpaywall_email="actions@users.noreply.github.com",
    )
    report = write_outputs(tmp_path, rows)
    written = list(csv.DictReader((tmp_path / "d_a_caruso_index_probe.csv").open(encoding="utf-8")))
    saved = json.loads((tmp_path / "d_a_caruso_index_probe_report.json").read_text(encoding="utf-8"))
    assert report["dataset_candidate_count"] == 0
    assert saved["next_action"] == "retain_caruso_as_system_seed_only_no_public_index_route_recovered"
    assert all("effect_value" not in row for row in written)
