from __future__ import annotations

import csv
import json

from trait_architecture.d_a_pmc_reading_targets import build_target, build_targets, read_screen, write_outputs


XML = b"""<?xml version='1.0' encoding='UTF-8'?>
<article>
  <body>
    <sec><title>Staminodes Removal Experiments</title>
      <p>A generalized linear model was used.</p><xref ref-type='fig' rid='f1'>Fig. 1</xref>
    </sec>
    <sec><title>Florivory Dynamics</title>
      <p>A binomial model analyzed damage.</p><xref ref-type='table' rid='t1'>Table 1</xref>
    </sec>
  </body>
  <fig id='f1'><label>Figure 1</label></fig>
  <table-wrap id='t1'><label>Table 1</label></table-wrap>
</article>
"""


def _screen(signal: str = "candidate_A_to_H_experiment_structure_needs_numeric_context_check") -> dict[str, str]:
    return {
        "candidate_id": "dA_cand_parnassia",
        "pmcid": "PMC1234567",
        "doi": "10.1234/example",
        "trait_class": "nectar_mimic_staminode_display",
        "antagonism_outcome": "florivorous_beetle_visitation",
        "trait_intervention_section_titles": "Staminodes Removal Experiments",
        "antagonist_outcome_section_titles": "Florivory Dynamics",
        "route_structure_signal": signal,
    }


def test_build_target_preserves_c4_section_and_figure_table_locators() -> None:
    target = build_target(_screen(), fetch_xml=lambda _url: (200, XML))

    assert target.empirical_track == "visual_display"
    assert target.source_access_status == "fulltext_xml_recovered"
    assert target.target_trait_intervention_sections == "Staminodes Removal Experiments"
    assert target.target_antagonist_outcome_sections == "Florivory Dynamics"
    assert target.referenced_figure_labels == "Figure 1"
    assert target.referenced_table_labels == "Table 1"
    assert "generalized linear" in target.model_method_terms
    assert "binomial" in target.model_method_terms
    assert target.c4_extraction_status == "needs_manual_model_and_effect_context"
    assert "Do not infer" in target.do_not_infer


def test_read_screen_keeps_only_viable_route_structure(tmp_path) -> None:
    path = tmp_path / "screen.csv"
    valid = _screen()
    excluded = _screen("probable_H_to_P_or_downstream_structure")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=valid)
        writer.writeheader()
        writer.writerows([valid, excluded])
    rows = read_screen(path)
    assert len(rows) == 1
    assert rows[0]["candidate_id"] == "dA_cand_parnassia"


def test_write_targets_has_no_effect_field(tmp_path) -> None:
    targets = build_targets([_screen()], fetch_xml=lambda _url: (200, XML))
    report = write_outputs(tmp_path, targets)

    with (tmp_path / "d_a_pmc_c4_reading_targets.csv").open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    saved = json.loads((tmp_path / "d_a_pmc_c4_reading_targets_report.json").read_text(encoding="utf-8"))
    assert "effect_value" not in written[0]
    assert report["visual_display_targets"] == 1
    assert saved["target_count"] == 1
