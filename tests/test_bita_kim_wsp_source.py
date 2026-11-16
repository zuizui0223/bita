"""Kim 2016 original Supplementary Table 2 source and selected-fan guardrails."""
import copy
import json
from pathlib import Path
import pytest

from scripts.analyze_bita_kim_wsp_source import (
    SOURCE_SHA256, ARTICLE_SHA256, analyze_rows, parse_source_pdf,
    verify_source_article_jats,
)

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "empirical/trait_architecture_history/kim2016_wsp_table2_readout.json"


def frozen():
    return json.loads(FROZEN.read_text(encoding="utf8"))


def test_source_table_has_26_strains_not_20_independent_origin_rows():
    r = frozen()
    assert r["paper_doi"] == "10.1038/ncomms10508"
    assert r["source_pdf_sha256"] == SOURCE_SHA256
    assert r["parent_article_jats_sha256"] == ARTICLE_SHA256
    assert r["source_table_strains_n"] == 26
    assert r["source_classes"] == {
        "published_ancestor": 2, "Constructed isolate": 19, "Evolved isolate": 5}
    assert r["phenotype_counts"] == {
        "Wildtype": 1, "Mucoid": 10, "Dry": 9, "Non-mucoid": 6}
    assert r["published_separately_selected_dry_fans_sequenced_n"] == 20
    assert r["original_article_methods_confirmation"]["per_fan_allele_data_available_in_supp_table2"] is False
    assert r["per_20_fan_allele_frequency_identified"] is False
    assert r["gene_specific_mutation_origin_rate_identified"] is False
    assert r["all_ancestral_plated_colonies_total_identified"] is False


def test_evolved_genes_and_constructed_mutations_never_counted_as_origins():
    r = frozen()
    assert r["evolved_dry_representative_strains_n"] == 4
    assert r["evolved_dry_representative_targets_gene_count"] == {
        "wspA": 2, "wspC": 1, "wspE": 1}
    assert r["representative_dry_wsp_target_genes"] == ["wspA", "wspC", "wspE"]
    assert r["evolved_M_reversion_entries_n"] == 1
    assert r["constructed_matching_D_allele"] == "wspC:D"
    assert r["constructed_Wsp_knockout_negative_controls"] == [
        "ΔwspC", "ΔwspD", "ΔwspCΔwspD"]
    assert r["evolved_representative_entries_are_not_an_unbiased_origin_denominator"] is True
    by = {a["strain"]: a for a in r["table_rows"]}
    assert by["Pf0-1DV (D)"]["genotype"] == by["wspC:D"]["genotype"]
    assert by["Pf0-1DV (D)"]["source_reference"] == "Evolved isolate"
    assert by["wspC:D"]["source_reference"] == "Constructed isolate"
    assert by["wspE#"]["phenotype"] == "Mucoid"


def test_frozen_result_recomputes_from_full_26_row_catalogue():
    r = frozen()
    recalculated = analyze_rows(r["table_rows"])
    for key, value in recalculated.items():
        assert r[key] == value
    assert r["original_article_methods_confirmation"]["selected_dry_fans_sequenced_according_to_methods"] == 20


def test_mutated_phenotype_reference_and_genotype_fail_closed():
    r = frozen()["table_rows"]
    bad = copy.deepcopy(r)
    by = {a["strain"]: a for a in bad}
    by["wspC:D"]["source_reference"] = "Evolved isolate"
    with pytest.raises(ValueError, match="strain classes"):
        analyze_rows(bad)
    bad = copy.deepcopy(r)
    by = {a["strain"]: a for a in bad}
    by["Pf0-1DV (D)"]["genotype"] = "Pf0-1MV (wspZΔ1269-70)"
    with pytest.raises(ValueError, match="allele"):
        analyze_rows(bad)
    with pytest.raises(ValueError, match="source PDF"):
        parse_source_pdf(b"bad-pdf")
    with pytest.raises(ValueError, match="JATS SHA256"):
        verify_source_article_jats(b"not-source")


def test_no_new_phylogenetic_meta_fitness_or_startup_cost():
    r = frozen()
    assert r["fitness_gain_per_genotype_estimated_from_table"] is False
    assert "20/20" in r["claim_ceiling"]
    assert "K(u)" in r["claim_ceiling"]
    assert "20 selected" in r["claim_ceiling"]
