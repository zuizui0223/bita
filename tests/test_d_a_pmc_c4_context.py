from __future__ import annotations

import csv
import json

from trait_architecture.d_a_pmc_c4_context import assess_row, assess_screen_csv


ROW = {
    "candidate_id": "dA_cand_parnassia",
    "pmcid": "PMC11442331",
    "doi": "10.1002/ece3.70380",
    "trait_intervention_section_titles": "Staminodes Removal Experiments",
    "antagonist_outcome_section_titles": "Florivory Dynamics",
    "route_structure_signal": "candidate_A_to_H_experiment_structure_needs_numeric_context_check",
    "trait_class": "nectar_mimic_staminode_display",
    "antagonism_outcome": "florivorous_beetle_visitation",
}


def _xml(*, include_table: bool = False) -> bytes:
    table = "<table-wrap id='t1'><label>TABLE 1</label></table-wrap>" if include_table else ""
    table_reference = " See TABLE 1." if include_table else ""
    return f"""<?xml version='1.0'?>
    <article><body>
      <sec><title>Staminodes Removal Experiments</title>
        <p>Flowers were assigned to intact control and removal treatments. Replication n = 20; standard error was reported.</p>
      </sec>
      <sec><title>Florivory Dynamics</title>
        <p>Florivorous beetle damage per flower was analysed with a generalized linear model.{table_reference}</p>
        <xref ref-type='fig' rid='f3'>FIGURE 3</xref>{"<xref ref-type='table' rid='t1'>TABLE 1</xref>" if include_table else ""}
      </sec>
    </body><fig id='f3'><label>FIGURE 3</label></fig>{table}</article>""".encode()


def test_figure_only_context_remains_non_B2() -> None:
    result = assess_row(ROW, fetch_xml=lambda _url: (200, _xml(include_table=False)))
    assert result.referenced_figure_labels == "FIGURE 3"
    assert result.referenced_table_labels == ""
    assert result.control_context_signal == "located"
    assert result.numeric_table_context_signal == "not_located"
    assert result.c4_decision == "retain_as_directional_or_C4_evidence_not_B2"


def test_relevant_table_makes_manual_numeric_candidate_only() -> None:
    result = assess_row(ROW, fetch_xml=lambda _url: (200, _xml(include_table=True)))
    assert result.referenced_table_labels == "TABLE 1"
    assert result.numeric_table_context_signal == "located"
    assert result.c4_readout_status == "context_fields_present_needs_manual_numeric_verification"
    assert result.c4_decision == "manual_numeric_extraction_required_before_B2"
    assert "Do not infer" in result.do_not_infer


def test_assess_screen_csv_writes_no_effect_field(tmp_path) -> None:
    path = tmp_path / "screen.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROW))
        writer.writeheader()
        writer.writerow(ROW)
    report = assess_screen_csv(path, tmp_path / "out", fetch_xml=lambda _url: (200, _xml()))
    rows = list(csv.DictReader((tmp_path / "out" / "d_a_pmc_c4_context.csv").open(encoding="utf-8")))
    saved = json.loads((tmp_path / "out" / "d_a_pmc_c4_context_report.json").read_text(encoding="utf-8"))
    assert report["non_B2_contexts"] == 1
    assert saved["numeric_context_candidates"] == 0
    assert "effect_value" not in rows[0]
