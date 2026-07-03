from __future__ import annotations

import csv
import json

from trait_architecture.d_a_elife_c4_context import assess_probe_csv, assess_receipt


RECEIPT = {
    "candidate_id": "dA_cand_schiestl2015",
    "doi": "10.7554/eLife.07641",
    "source_url": "https://elifesciences.org/articles/07641.xml",
}


def _xml(*, include_table: bool = False, include_context: bool = True) -> bytes:
    table = "<table-wrap id='t1'><label>Table 1</label></table-wrap>" if include_table else ""
    text = (
        "Oviposition trials used control plants and recorded eggs per plant per day. "
        "Replication n = 12; standard error was reported and a generalized linear model was fitted."
        if include_context else "This section contains unrelated observations."
    )
    if include_table:
        text += " See Table 1."
    return f"""<?xml version='1.0'?>
    <article>
      <body>
        <sec><title>Oviposition trials</title><p>{text}</p></sec>
      </body>
      <fig id='f2'><label>Figure 2.</label><caption><p>Primary comparison.</p></caption></fig>
      {table}
    </article>""".encode()


def test_context_without_numeric_table_remains_non_B2() -> None:
    row = assess_receipt(RECEIPT, fetch_xml=lambda _url: (200, _xml(include_table=False)))
    assert row.oviposition_section_locator == "Oviposition trials"
    assert row.figure_2_locator == "Figure 2."
    assert row.control_context_signal == "located"
    assert row.uncertainty_context_signal == "located"
    assert row.numeric_table_context_signal == "not_located"
    assert row.c4_decision == "retain_as_directional_or_C4_evidence_not_B2"


def test_context_with_table_is_only_a_manual_numeric_candidate() -> None:
    row = assess_receipt(RECEIPT, fetch_xml=lambda _url: (200, _xml(include_table=True)))
    assert row.numeric_table_context_signal == "located"
    assert row.c4_readout_status == "context_fields_present_needs_manual_numeric_verification"
    assert row.c4_decision == "manual_numeric_extraction_required_before_B2"
    assert "Do not infer" in row.do_not_infer


def test_assess_probe_csv_writes_structured_fields_only(tmp_path) -> None:
    probe = tmp_path / "probe.csv"
    with probe.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "doi", "source_label", "source_url", "access_status"])
        writer.writeheader()
        writer.writerow({**RECEIPT, "source_label": "elife_xml", "access_status": "public_xml_prefix_recovered"})
    report = assess_probe_csv(probe, tmp_path / "out", fetch_xml=lambda _url: (200, _xml()))
    rows = list(csv.DictReader((tmp_path / "out" / "d_a_elife_c4_context.csv").open(encoding="utf-8")))
    saved = json.loads((tmp_path / "out" / "d_a_elife_c4_context_report.json").read_text(encoding="utf-8"))
    assert report["non_B2_contexts"] == 1
    assert saved["numeric_context_candidates"] == 0
    assert "effect_value" not in rows[0]
