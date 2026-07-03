from __future__ import annotations

import csv
import json

from trait_architecture.d_a_elife_probe import candidate_urls, probe_target, read_target, write_outputs


def _target() -> dict[str, str]:
    return {
        "candidate_id": "dA_cand_schiestl2015",
        "source": "doi:10.7554/eLife.07641",
        "trait_class": "scent_and_nectar",
        "antagonism_outcome": "hawkmoth_oviposition",
    }


def _crossref(url: str):
    assert "10.7554%2FeLife.07641" in url
    return 200, {
        "message": {
            "link": [
                {"URL": "https://elifesciences.org/articles/07641.xml"},
                {"URL": "https://elifesciences.org/articles/07641.pdf"},
            ]
        }
    }


def test_candidate_urls_deduplicate_crossref_and_standard_elife_routes() -> None:
    urls = candidate_urls("10.7554/eLife.07641", _crossref)
    assert urls[0] == ("crossref_link", "https://elifesciences.org/articles/07641.xml")
    assert urls.count(("elife_xml", "https://elifesciences.org/articles/07641.xml")) == 0
    assert ("elife_html", "https://elifesciences.org/articles/07641") in urls
    assert ("elife_pdf", "https://elifesciences.org/articles/07641.pdf") in urls


def test_probe_classifies_xml_pdf_and_html_without_reading_content() -> None:
    responses = {
        "https://elifesciences.org/articles/07641.xml": (200, "application/xml", b"<?xml version='1.0'?><article/>"),
        "https://elifesciences.org/articles/07641.pdf": (200, "application/pdf", b"%PDF-1.7 fake"),
        "https://elifesciences.org/articles/07641": (200, "text/html", b"<html><head></head></html>"),
    }

    receipts = probe_target(
        _target(),
        fetch_json=_crossref,
        fetch_prefix=lambda url: responses[url],
    )
    states = {row.source_url: row.access_status for row in receipts}
    assert states["https://elifesciences.org/articles/07641.xml"] == "public_xml_prefix_recovered"
    assert states["https://elifesciences.org/articles/07641.pdf"] == "public_pdf_prefix_recovered"
    assert states["https://elifesciences.org/articles/07641"] == "public_html_prefix_recovered"
    assert all("Do not infer" in row.do_not_infer for row in receipts)


def test_read_target_and_write_outputs(tmp_path) -> None:
    path = tmp_path / "candidates.csv"
    fields = list(_target())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(_target())
    assert read_target(path)["candidate_id"] == "dA_cand_schiestl2015"

    receipts = probe_target(
        _target(),
        fetch_json=_crossref,
        fetch_prefix=lambda _url: (200, "application/xml", b"<?xml version='1.0'?><article/>"),
    )
    report = write_outputs(tmp_path / "out", receipts)
    saved = json.loads((tmp_path / "out" / "d_a_elife_source_probe_report.json").read_text(encoding="utf-8"))
    assert report["xml_prefix_recovered"] >= 1
    assert saved["url_count"] == len(receipts)
