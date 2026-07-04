from __future__ import annotations

import csv
import json

from trait_architecture.d_a_phlox_abstract_screen import PHLOX_DOI, _candidate, screen_candidate, write_outputs


def _candidate_row() -> dict[str, str]:
    return {
        "candidate_id": "dA_cand_phlox_hirsuta",
        "source": "url:academic.oup.com/aob/article/113/5/887",
        "trait_class": "floral_display_size",
        "antagonism_outcome": "florivory",
    }


def _fruit_set_abstract(_url: str):
    return 200, """<html><body>
    <p>Multiple linear regressions were used to identify factors that explain variation in percentage fruit set.</p>
    <p>Florivorous beetle density, floral display size, local conspecific density and pre-dispersal seed predation were quantified and their effects on the ability of flowers to produce fruits were assessed.</p>
    </body></html>"""


def _pubmed_lookup(_url: str):
    return 200, {"esearchresult": {"idlist": ["24557879"]}}


def _pubmed_abstract(_url: str):
    return 200, b"""<PubmedArticleSet><PubmedArticle><MedlineCitation><Article><Abstract>
    <AbstractText>Multiple linear regressions were used to identify factors that explain variation in percentage fruit set. Florivorous beetle density and floral display size were quantified and their effects on the ability of flowers to produce fruits were assessed.</AbstractText>
    </Abstract></Article></MedlineCitation></PubmedArticle></PubmedArticleSet>"""


def test_parallel_predictors_of_fruit_set_are_not_direct_d_a() -> None:
    row = screen_candidate(_candidate_row(), fetch_html=_fruit_set_abstract)
    assert row.doi == PHLOX_DOI
    assert row.abstract_access_status == "publisher_abstract_recovered"
    assert "fruit set" in row.response_terms
    assert "floral display size" in row.display_predictor_terms
    assert "florivorous beetle density" in row.florivory_predictor_terms
    assert "multiple linear regressions" in row.regression_terms
    assert row.direct_display_to_florivory_model_signal == "parallel_predictors_of_fruit_set_not_direct_d_A"
    assert row.route_assignment == "candidate_screened_context_only"


def test_pubmed_fallback_reproduces_parallel_predictor_decision() -> None:
    row = screen_candidate(
        _candidate_row(),
        fetch_html=lambda _url: (_ for _ in ()).throw(RuntimeError("publisher blocked")),
        fetch_json=_pubmed_lookup,
        fetch_xml=_pubmed_abstract,
    )
    assert row.pubmed_id == "24557879"
    assert row.abstract_access_status == "pubmed_abstract_recovered"
    assert row.abstract_retrieval_route == "pubmed_esearch_then_efetch"
    assert row.direct_display_to_florivory_model_signal == "parallel_predictors_of_fruit_set_not_direct_d_A"


def test_exhausted_abstract_routes_do_not_infer_route() -> None:
    row = screen_candidate(
        _candidate_row(),
        fetch_html=lambda _url: (_ for _ in ()).throw(RuntimeError("publisher blocked")),
        fetch_json=lambda _url: (200, {"esearchresult": {"idlist": []}}),
        fetch_xml=lambda _url: (_ for _ in ()).throw(AssertionError("must not fetch XML without PMID")),
    )
    assert row.abstract_access_status == "abstract_routes_exhausted"
    assert row.direct_display_to_florivory_model_signal == "not_screened"
    assert row.route_assignment == "retain_unverified_candidate"


def test_registered_lookup_and_outputs_contain_no_effect_fields(tmp_path) -> None:
    scouting = tmp_path / "scouting.csv"
    with scouting.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "source", "trait_class", "antagonism_outcome"])
        writer.writeheader(); writer.writerow(_candidate_row())
    assert _candidate(scouting)["candidate_id"] == "dA_cand_phlox_hirsuta"
    row = screen_candidate(_candidate_row(), fetch_html=_fruit_set_abstract)
    report = write_outputs(tmp_path / "out", [row])
    saved = json.loads((tmp_path / "out" / "d_a_phlox_abstract_screen_report.json").read_text(encoding="utf-8"))
    written = list(csv.DictReader((tmp_path / "out" / "d_a_phlox_abstract_screen.csv").open(encoding="utf-8")))
    assert report["parallel_fruit_set_predictor_structure"] == 1
    assert saved["abstract_recovered"] == 1
    assert "effect_value" not in written[0]
    assert "standard_error" not in written[0]
