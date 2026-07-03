from __future__ import annotations

import csv
import json

from trait_architecture.d_a_elife_screen import read_xml_receipt, screen_receipt, write_outputs


XML = b"""<?xml version='1.0' encoding='UTF-8'?>
<article><body>
  <sec><title>Nectar and scent treatment experiments</title>
    <p>Experimental nectar treatment altered floral scent and hawkmoth oviposition.</p>
    <xref ref-type='fig' rid='f1'>Fig 1</xref><xref ref-type='table' rid='t1'>Table 1</xref>
  </sec>
</body>
<fig id='f1'><label>Figure 1</label></fig>
<table-wrap id='t1'><label>Table 1</label></table-wrap>
</article>
"""


def _receipt(status: str = "public_xml_prefix_recovered") -> dict[str, str]:
    return {
        "candidate_id": "dA_cand_schiestl2015",
        "doi": "10.7554/eLife.07641",
        "source_label": "elife_xml",
        "source_url": "https://elifesciences.org/articles/07641.xml",
        "access_status": status,
        "http_status": "200",
        "content_type": "application/xml",
        "prefix_signature": "<?xml",
    }


def test_elife_xml_screen_yields_c4_route_locator_without_effect() -> None:
    screen = screen_receipt(_receipt(), fetch_xml=lambda _url: (200, XML))

    assert screen.source_access_status == "fulltext_xml_recovered"
    assert screen.route_structure_signal == "candidate_scent_reward_to_oviposition_structure_needs_numeric_context_check"
    assert screen.c4_extraction_status == "needs_manual_model_and_effect_context"
    assert "Nectar and scent treatment experiments" in screen.matched_section_titles
    assert screen.referenced_figure_labels == "Figure 1"
    assert screen.referenced_table_labels == "Table 1"
    assert "Do not infer" in screen.do_not_infer


def test_read_xml_receipt_prefers_elife_xml(tmp_path) -> None:
    path = tmp_path / "probe.csv"
    xml = _receipt()
    other = {**_receipt(), "source_label": "crossref_link", "source_url": "https://cdn.example/article.xml"}
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=xml)
        writer.writeheader()
        writer.writerows([other, xml])
    chosen = read_xml_receipt(path)
    assert chosen["source_label"] == "elife_xml"


def test_write_outputs_has_no_effect_field(tmp_path) -> None:
    screen = screen_receipt(_receipt(), fetch_xml=lambda _url: (200, XML))
    report = write_outputs(tmp_path, [screen])
    with (tmp_path / "d_a_elife_xml_screen.csv").open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    saved = json.loads((tmp_path / "d_a_elife_xml_screen_report.json").read_text(encoding="utf-8"))
    assert "effect_value" not in written[0]
    assert report["candidate_c4_structure"] == 1
    assert saved["screened_source_count"] == 1
