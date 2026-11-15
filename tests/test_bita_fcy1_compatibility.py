"""Source-locked positive Fcy1 heteromer compatibility network; no pooled trait effect."""
import copy
import json
from pathlib import Path

import pytest

from scripts.analyze_bita_fcy1_compatibility import analyze, load_pairs

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical/trait_architecture_history/despres2024_indep_crosses_source.csv"
OUT = ROOT / "empirical/trait_architecture_history/despres2024_compatibility_readout.json"


def test_author_source_sample_and_independence_units():
    data = analyze(load_pairs(SOURCE))
    assert data["study_doi"] == "10.1126/science.ado5719"
    assert data["source_blob_sha"] == "36839a3fd2eb05a521a070d11e60cde1748a682e"
    assert data["positive_pair_edges"] == 207
    assert data["positive_unique_alleles"] == 103
    assert data["positive_colony_observations"] == 887
    assert data["positive_distinct_codon_cross_identifiers"] == 613
    assert data["pairs_with_ge2_source_cross_identifiers"] == 104
    assert data["pairs_with_one_source_cross_identifier"] == 103
    assert data["no_unselected_negative_pair_denominator"] is True
    assert data["independent_evolutionary_origins_estimated"] is False


def test_positive_graph_topology_and_recurrence_sensitivity():
    data = analyze(load_pairs(SOURCE))
    layers = data["positive_graph_thresholds"]
    assert layers["ge1"]["edges"] == 207
    assert layers["ge1"]["vertices"] == 103
    assert layers["ge1"]["component_sizes"] == [97, 2, 2, 2]
    assert layers["ge1"]["top_alleles_by_distinct_positive_partners"][0] == {
        "allele": "M100W", "partners": 39
    }
    assert layers["ge1"]["top_alleles_by_distinct_positive_partners"][1] == {
        "allele": "R73D", "partners": 33
    }
    assert layers["ge2"]["edges"] == 104
    assert layers["ge2"]["vertices"] == 53
    assert layers["ge2"]["largest_component_vertices"] == 44
    assert layers["ge3"]["edges"] == 73
    assert layers["ge3"]["vertices"] == 38
    assert layers["ge3"]["largest_component_vertices"] == 29
    assert layers["ge5"]["edges"] == 38
    assert layers["ge5"]["vertices"] == 25
    assert layers["ge5"]["largest_component_vertices"] == 16


def test_positive_observation_recurrence_is_not_sampled_prevalence():
    data = analyze(load_pairs(SOURCE))
    assert data["frequency_missing_n"] == 51
    assert data["frequency_finite_n"] == 156
    assert data["descriptive_spearman_frequency_vs_cross_recovery"] == pytest.approx(
        0.4779347876797335, abs=1e-12
    )
    assert data["poolable_study_effects_added"] == 0
    assert data["meta_analysis_performed"] is False
    assert "not a random sample" in data["claim_boundary"]
    assert "not 613 independent evolutionary origins" in data["claim_boundary"]


def test_raises_on_duplicate_reverse_pair():
    rows = load_pairs(SOURCE)
    copied = copy.deepcopy(rows[0])
    copied["allele_1"], copied["allele_2"] = copied["allele_2"], copied["allele_1"]
    rows.append(copied)
    with pytest.raises(ValueError, match="duplicate unordered"):
        analyze(rows)


def test_raises_on_impossible_cross_count():
    rows = load_pairs(SOURCE)
    rows[0]["n_indep_crosses"] = rows[0]["n_observed"] + 1
    with pytest.raises(ValueError, match="exceeds"):
        analyze(rows)


def test_raises_on_invalid_allele_and_self_loop():
    rows = load_pairs(SOURCE)
    rows[0]["allele_2"] = rows[0]["allele_1"]
    with pytest.raises(ValueError, match="same allele"):
        analyze(rows)


def test_author_original_row_identity_is_contiguous():
    rows = load_pairs(SOURCE)
    assert [r["source_index"] for r in rows] == list(range(207))
    rows[1]["source_index"] = rows[0]["source_index"]
    with pytest.raises(ValueError, match="index"):
        analyze(rows)


def test_readout_matches_source_recomputation():
    assert OUT.is_file()
    data = json.loads(OUT.read_text(encoding="utf-8"))
    recomputed = analyze(load_pairs(SOURCE))
    assert data["positive_pair_edges"] == recomputed["positive_pair_edges"]
    assert data["positive_graph_thresholds"] == recomputed["positive_graph_thresholds"]
    assert data["descriptive_spearman_frequency_vs_cross_recovery"] == pytest.approx(
        recomputed["descriptive_spearman_frequency_vs_cross_recovery"], abs=1e-12
    )
    assert data["claim_boundary"] == recomputed["claim_boundary"]
