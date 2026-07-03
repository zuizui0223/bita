from __future__ import annotations

import csv
import json

from trait_architecture.d_a_pmc_screen import (
    read_candidates,
    screen_candidate,
    screen_candidates,
    write_outputs,
)


XML = b"""<?xml version='1.0' encoding='UTF-8'?>
<article>
  <front><article-meta><article-id pub-id-type='doi'>10.1234/example</article-id></article-meta></front>
  <body>
    <sec><title>Methods</title><p>Staminode display was measured with florivorous beetle visitation.</p></sec>
    <table-wrap><label>Table 2</label><caption><p>Staminode display and beetle visitation.</p></caption></table-wrap>
  </body>
</article>
"""
INTERVENTION_XML = b"""<?xml version='1.0' encoding='UTF-8'?>
<article><body>
  <sec><title>Staminodes Removal Experiments</title><p>Staminode removal treatment was applied.</p></sec>
  <sec><title>Florivory Dynamics</title><p>Florivorous beetle damage was recorded.</p></sec>
</body></article>
"""
REVERSE_XML = b"""<?xml version='1.0' encoding='UTF-8'?>
<article><body>
  <sec><title>Influence of Floral Antagonists on Pollinator Behavior</title>
  <p>Florivory altered pollinator foraging behavior and reproductive fitness.</p></sec>
</body></article>
"""


def _row(source: str = "url:ncbi.nlm.nih.gov/pmc/articles/PMC1234567") -> dict[str, str]:
    return {
        "candidate_id": "dA_pmc",
        "source": source,
        "taxon": "Example",
        "trait_class": "nectar_mimic_staminode_display",
        "antagonism_outcome": "florivorous_beetle_visitation",
    }


def test_pmc_screen_reports_term_cooccurrence_and_locators_without_effect() -> None:
    row = screen_candidate(_row(), fetch_xml=lambda _url: (200, XML))

    assert row.source_access_status == "fulltext_xml_recovered"
    assert row.doi == "10.1234/example"
    assert row.direct_route_screen_status == "both_term_families_present_needs_human_route_coding"
    assert row.route_structure_signal == "term_cooccurrence_without_experiment_link"
    assert "staminode" in row.matched_trait_terms
    assert "beetle" in row.matched_antagonist_terms
    assert row.matched_section_titles == "Methods"
    assert row.matched_table_labels == "Table 2"
    assert "Do not infer" in row.do_not_infer


def test_pmc_screen_flags_candidate_trait_intervention_structure_without_extracting_effect() -> None:
    row = screen_candidate(_row(), fetch_xml=lambda _url: (200, INTERVENTION_XML))

    assert row.route_structure_signal == "candidate_A_to_H_experiment_structure_needs_numeric_context_check"
    assert "Staminodes Removal Experiments" in row.trait_intervention_section_titles
    assert "Florivory Dynamics" in row.antagonist_outcome_section_titles
    assert row.direct_route_screen_status == "both_term_families_present_needs_human_route_coding"


def test_pmc_screen_flags_probable_reverse_route() -> None:
    row = screen_candidate(_row(), fetch_xml=lambda _url: (200, REVERSE_XML))

    assert row.route_structure_signal == "probable_H_to_P_or_downstream_structure"
    assert "Influence of Floral Antagonists on Pollinator Behavior" in row.reverse_route_section_titles
    assert row.direct_route_screen_status == "one_term_family_present_not_direct_route"


def test_pmc_screen_keeps_access_failure_separate_from_absence() -> None:
    row = screen_candidate(_row(), fetch_xml=lambda _url: (404, b""))

    assert row.source_access_status == "xml_access_or_parse_failed"
    assert row.direct_route_screen_status == "not_screened"
    assert row.route_structure_signal == "not_available"
    assert "HTTP 404" in row.screen_note


def test_read_candidates_selects_only_registered_pmc_sources(tmp_path) -> None:
    path = tmp_path / "candidates.csv"
    fields = list(_row())
    rows = [_row(), _row("doi:10.1/no-pmc")]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    selected = read_candidates(path)
    assert len(selected) == 1
    assert selected[0]["candidate_id"] == "dA_pmc"


def test_write_outputs_contains_only_screen_metadata(tmp_path) -> None:
    rows = screen_candidates([_row()], fetch_xml=lambda _url: (200, INTERVENTION_XML))
    report = write_outputs(tmp_path, rows)

    with (tmp_path / "d_a_pmc_fulltext_screen.csv").open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    saved = json.loads((tmp_path / "d_a_pmc_fulltext_screen_report.json").read_text(encoding="utf-8"))
    assert written[0]["candidate_id"] == "dA_pmc"
    assert "effect_value" not in written[0]
    assert report["both_term_families_present"] == 1
    assert report["candidate_A_to_H_experiment_structure"] == 1
    assert saved["pmc_candidate_count"] == 1
