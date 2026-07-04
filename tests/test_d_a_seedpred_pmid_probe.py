from __future__ import annotations

import csv
import json

from trait_architecture.d_a_seedpred_pmid_probe import (
    PMID,
    _candidate,
    probe_candidate,
    write_outputs,
)


def _candidate_row() -> dict[str, str]:
    return {
        "candidate_id": "dA_cand_conflicting_seedpred",
        "source": f"pmid:{PMID}",
        "trait_class": "floral_exsertion_display",
        "antagonism_outcome": "seed_predation",
    }


def _idconv(_url: str):
    return 200, {"records": [{"pmid": PMID, "doi": "10.1111/example.12345", "pmcid": "PMC5555555"}]}


def _direct_model_xml(_url: str):
    return 200, b"""<article>
      <front><article-meta><article-id pub-id-type='doi'>10.1111/example.12345</article-id></article-meta></front>
      <body>
        <sec><title>Seed-predation model</title>
          <p>Floral exsertion predicted seed predation in a generalized linear model.</p>
        </sec>
      </body>
      <table-wrap><label>Table 2</label><caption><p>Exsertion and seed predation model.</p></caption></table-wrap>
    </article>"""


def test_pmc_screen_requires_colocated_observational_model_context() -> None:
    row = probe_candidate(_candidate_row(), fetch_json=_idconv, fetch_xml=_direct_model_xml)
    assert row.doi == "10.1111/example.12345"
    assert row.pmcid == "PMC5555555"
    assert row.source_access_status == "fulltext_xml_recovered"
    assert row.xml_retrieval_route == "europe_pmc_fulltext_xml"
    assert row.route_structure_signal == "candidate_observational_trait_to_seed_predation_model_needs_numeric_context_check"
    assert "exsertion" in row.matched_trait_terms
    assert "seed predat" in row.matched_antagonist_terms
    assert "generalized linear" in row.matched_model_terms
    assert row.shared_section_titles == "Seed-predation model"
    assert row.relevant_table_labels == "Table 2"


def test_ncbi_efetch_fallback_is_used_after_europe_pmc_404() -> None:
    def fetch_xml(url: str):
        if "europepmc" in url:
            return 404, b""
        assert "eutils.ncbi.nlm.nih.gov" in url
        assert "id=5555555" in url
        return _direct_model_xml(url)
    row = probe_candidate(_candidate_row(), fetch_json=_idconv, fetch_xml=fetch_xml)
    assert row.source_access_status == "fulltext_xml_recovered"
    assert row.xml_retrieval_route == "ncbi_pmc_efetch"


def test_pmcid_missing_stops_before_xml_read() -> None:
    row = probe_candidate(
        _candidate_row(),
        fetch_json=lambda _url: (200, {"records": [{"pmid": PMID, "doi": "10.1111/example.12345"}]}),
        fetch_xml=lambda _url: (_ for _ in ()).throw(AssertionError("must not fetch XML without PMCID")),
    )
    assert row.idconv_status == "resolved_no_pmcid"
    assert row.source_access_status == "no_pmc_fulltext_route"
    assert row.route_structure_signal == "not_available"


def test_term_cooccurrence_without_model_context_does_not_open_c4() -> None:
    xml = b"""<article><body><sec><title>Discussion</title>
      <p>Floral exsertion and seed predation were discussed.</p>
    </sec></body></article>"""
    row = probe_candidate(_candidate_row(), fetch_json=_idconv, fetch_xml=lambda _url: (200, xml))
    assert row.route_structure_signal == "term_cooccurrence_without_model_context"
    assert row.direct_route_screen_status == "both_term_families_present_needs_human_route_coding"


def test_registered_lookup_and_output_exclude_effect_fields(tmp_path) -> None:
    scouting = tmp_path / "scouting.csv"
    with scouting.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "source", "trait_class", "antagonism_outcome"])
        writer.writeheader(); writer.writerow(_candidate_row())
    assert _candidate(scouting)["candidate_id"] == "dA_cand_conflicting_seedpred"
    row = probe_candidate(_candidate_row(), fetch_json=_idconv, fetch_xml=_direct_model_xml)
    report = write_outputs(tmp_path / "out", [row])
    saved = json.loads((tmp_path / "out" / "d_a_seedpred_pmid_probe_report.json").read_text(encoding="utf-8"))
    written = list(csv.DictReader((tmp_path / "out" / "d_a_seedpred_pmid_probe.csv").open(encoding="utf-8")))
    assert report["candidate_observational_direct_route"] == 1
    assert saved["fulltext_xml_recovered"] == 1
    assert "effect_value" not in written[0]
    assert "standard_error" not in written[0]
