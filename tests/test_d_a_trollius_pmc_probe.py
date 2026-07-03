from __future__ import annotations

import csv
import json

from trait_architecture.d_a_trollius_pmc_probe import (
    TROLLIUS_DOI,
    _candidate_row,
    probe_trollius,
    write_outputs,
)


def _candidate() -> dict[str, str]:
    return {
        "candidate_id": "dA_cand_trollius",
        "source": f"doi:{TROLLIUS_DOI}",
        "trait_class": "floral_size_and_traits",
        "antagonism_outcome": "resolve_whether_antagonism_measured",
    }


def _pmc_search(_url: str):
    return 200, {
        "resultList": {
            "result": [{"doi": TROLLIUS_DOI, "pmcid": "PMC4444444", "pmid": "12345678"}]
        }
    }


def _candidate_route_xml(_url: str):
    xml = b"""<article>
      <front><article-meta><article-id pub-id-type='doi'>10.1371/journal.pone.0118299</article-id></article-meta></front>
      <body>
        <sec><title>Floral size removal experiment</title><p>Floral size treatment and florivory response were assessed.</p></sec>
        <sec><title>Florivory dynamics</title><p>Beetle florivory and floral size are reported.</p></sec>
      </body>
    </article>"""
    return 200, xml


def test_pmc_heading_screen_can_flag_candidate_route_without_effect_extraction() -> None:
    row = probe_trollius(_candidate(), fetch_json=_pmc_search, fetch_xml=_candidate_route_xml)
    assert row.pmcid == "PMC4444444"
    assert row.pmid == "12345678"
    assert row.source_access_status == "fulltext_xml_recovered"
    assert row.route_structure_signal == "candidate_A_to_H_experiment_structure_needs_numeric_context_check"
    assert "floral size" in row.matched_trait_terms
    assert "florivor" in row.matched_antagonist_terms
    assert "effect" in row.do_not_infer.casefold()


def test_no_pmcid_stops_before_fulltext_screen() -> None:
    row = probe_trollius(
        _candidate(),
        fetch_json=lambda _url: (200, {"resultList": {"result": [{"doi": TROLLIUS_DOI, "pmid": "12345678"}]}}),
        fetch_xml=lambda _url: (_ for _ in ()).throw(AssertionError("must not fetch XML without PMCID")),
    )
    assert row.source_access_status == "no_pmc_fulltext_route"
    assert row.direct_route_screen_status == "not_screened"
    assert row.route_structure_signal == "not_available"


def test_registered_candidate_lookup_and_output_exclude_effect_values(tmp_path) -> None:
    scouting = tmp_path / "scouting.csv"
    with scouting.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "source", "trait_class", "antagonism_outcome"])
        writer.writeheader(); writer.writerow(_candidate())
    assert _candidate_row(scouting)["candidate_id"] == "dA_cand_trollius"
    row = probe_trollius(_candidate(), fetch_json=_pmc_search, fetch_xml=_candidate_route_xml)
    report = write_outputs(tmp_path / "out", [row])
    saved = json.loads((tmp_path / "out" / "d_a_trollius_pmc_probe_report.json").read_text(encoding="utf-8"))
    written = list(csv.DictReader((tmp_path / "out" / "d_a_trollius_pmc_probe.csv").open(encoding="utf-8")))
    assert report["candidate_direct_route_structure"] == 1
    assert saved["pmc_fulltext_recovered"] == 1
    assert "effect_value" not in written[0]
    assert "standard_error" not in written[0]
