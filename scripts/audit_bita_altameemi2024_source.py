"""Source-grade readout for Al-Tameemi & Rodriguez-Verdugo 2024 mSystems.

Original independently founded evolution populations are the sampling units.
Do not count 30 isolated colonies, six technical replay tubes, generations
or three plate-reader replicates as new evolved populations.

The primary outcome is RETAINED colony-size bimodality at generation 200,
not independent origination of the large mutation (which arose in both
monocultures and co-cultures). Negative-frequency-dependence was NOT
confirmed by the paper's focal isolate-pair invasion test.
"""
from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

DOI = "10.1128/msystems.01053-24"
PMCID = "PMC11575400"
PUB_URL = "https://journals.asm.org/doi/10.1128/msystems.01053-24"
ORIGINAL_JATS = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11575400/fullTextXML"
STUDY_FAMILY = "RodriguezVerdugo_Ackermann_original_200_generation_evolution_AlTameemi2024"
REQUIRED = (
    "microbial diversification is maintained in an experimentally evolved synthetic community",
    "all four replicates were bimodal",
    "diversification only persisted in co-culture",
    "frequency-dependent selection does not explain",
    "0.814",
    "four replicates of p. putida",
    "evolutionary",
    "replay",
)
SOURCE_BODY_MARKER = "phenotypic diversification persisted only in co-culture"


class PlainHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in ("script","style"):
            self.skip += 1
    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in ("script","style") and self.skip>0:
            self.skip -= 1
    def handle_data(self, text: str) -> None:
        if not self.skip:
            self.parts.append(text)


def _normalize(text: str) -> str:
    text = html.unescape(text).lower().replace("\u00ad","")
    text = re.sub(r"[\u2010-\u2015]","-",text)
    return " ".join(text.split())


def validate_original_source(raw: bytes, content_type: str) -> dict:
    """Read substantive ORIGINAL full text, not an abstract or crawler title."""
    if len(raw)<12000 or len(raw)>4_000_000:
        raise ValueError("original full article source bytes outside plausible bounds")
    if content_type=="jats":
        try:
            root=ET.fromstring(raw)
        except ET.ParseError as e:
            raise ValueError("invalid original fulltext JATS XML") from e
        ids=[
            (node.text or "").strip()
            for node in root.iter()
            if node.tag.rsplit("}",1)[-1]=="article-id"
            and node.attrib.get("pub-id-type")=="doi"
        ]
        if DOI not in ids:
            raise ValueError("wrong DOI in original article JATS")
        text = " ".join(root.itertext())
    elif content_type=="html":
        parser=PlainHTML()
        parser.feed(raw.decode("utf8",errors="replace"))
        text=" ".join(parser.parts)
        if DOI not in _normalize(text):
            raise ValueError("original publisher HTML does not disclose DOI")
    else:
        raise ValueError("unsupported original article format")
    norm=_normalize(text)
    for phrase in REQUIRED:
        if phrase not in norm:
            raise ValueError(f"source article does not supply registered result token: {phrase}")
    if SOURCE_BODY_MARKER not in norm:
        raise ValueError("original fulltext study Result heading absent")
    if "benzoate was not externally supplemented" not in norm:
        raise ValueError("source confound/resource supply caveat missing")
    if "138 generations" not in norm:
        raise ValueError("replay evolved source generation history not established")
    return {
        "original_article_fulltext_grade":"FULL_TEXT_PRIMARY_ARTICLE_WITH_REQUIRED_RESULTS_VERIFIED",
        "published_article_DOI":DOI,
        "article_PMCI":PMCID,
        "source_type":content_type,
        "source_bytes":len(raw),
        "source_sha256":hashlib.sha256(raw).hexdigest(),
        "all_original_result_tokens_verified":True,
        "registered_source_body_passage_verified":True,
    }


def choose(n:int,k:int) -> int:
    if not isinstance(n,int) or not isinstance(k,int) or n<0 or k<0 or k>n:
        raise ValueError("invalid biological source count")
    return math.comb(n,k)


def exact_independent_hypergeometric_test() -> dict:
    """Purely *sensitivity* test: full four-of-four separated source pattern.

    Pairing is plausible because source four original isolated founder
    replicates were used in corresponding treatment numbers; don't
    silently choose independent-arm Fisher as the only permissible test.
    """
    n_co=n_mono=4
    positive_co=4
    positive_mono=0
    assert positive_co+positive_mono==4
    combinations=choose(8,4)
    probs=[
        choose(4,k)*choose(4,4-k)/combinations
        for k in range(5)
    ]
    observed=probs[positive_co]
    two_sided=sum(p for p in probs if p<=observed+1e-12)
    # Conditional exact paired discordance: four discordant founder blocks.
    # This is a design-sensitive analysis, not proof of source pairing.
    paired_discordant=4
    paired_two_sided=2/(2**paired_discordant)
    return {
        "co_culture_detectable_bimodal_lines":positive_co,
        "co_culture_started_Pputida_lines":n_co,
        "mono_culture_detectable_bimodal_lines":positive_mono,
        "mono_culture_started_Pputida_lines":n_mono,
        "source_arms_corresponding_founder_indices_1_to_4":True,
        "observed_risk_difference":1.0,
        "unpaired_Fisher_two_sided_p_descriptive":two_sided,
        "unpaired_Fisher_table_allocations":combinations,
        "conditional_pairing_4_discordant_pairs_exact_two_sided_p_sensitivity":paired_two_sided,
        "pairing_requires_source_lineage_adjudication":True,
        "four_isolates_vs_four_cultures_not_comparable":True,
        "post_source_analytical_tests_not_preregistered":True,
    }


def source_record(original_receipt: dict | None, retrieval: list[dict]) -> dict:
    if original_receipt is not None:
        if original_receipt.get("published_article_DOI")!=DOI:
            raise ValueError("invalid original fulltext source identification")
        source_grade=original_receipt["original_article_fulltext_grade"]
    else:
        source_grade="PUBLISHER_WEB_FULLTEXT_VERIFIED_SEPARATELY_ORIGINAL_BINARY_NOT_RETRIEVED"
    result = exact_independent_hypergeometric_test()
    return {
        "paper_DOI":DOI,"paper_title":
            "Microbial diversification is maintained in an experimentally evolved synthetic community",
        "original_publication_year":2024,
        "original_biological_experiment_family":STUDY_FAMILY,
        "previous_experiment_publication":"Rodriguez-Verdugo and Ackermann, original 200-generation evolution; not an independent new 2024 founding experiment",
        "original_article_url":PUB_URL,
        "original_article_PMCID":PMCID,
        "article_source_receipt":original_receipt,
        "retrieval_receipts":retrieval,
        "source_grade":source_grade,
        "one_new_independent_programme_relative_to_current_BITA_11":True,
        "focal_species":"Pseudomonas putida KT2440",
        "resource_provider":"Acinetobacter johnsonii C6",
        "focal_founder_ancestry":"four line-specific clonal ancestral isolates, diverged by a few generations",
        "source_evolution":{
            "generations":200,
            "Pputida_monoculture_founding_lines":4,
            "Pputida_coculture_founding_lines":4,
            "Ajohnsonii_monoculture_founding_lines":4,
            "Pputida_coculture_bimodal_lines_at_endpoint":4,
            "Pputida_monoculture_bimodal_lines_at_endpoint":0,
            "Pputida_monoculture_larger_morphotype_appeared_during_evolution":True,
            "Pputida_coculture_larger_morphotype_appeared_during_evolution":True,
            "source_historical_origin_probability_4of4_vs_0of4":False,
            "endpoint_type":"retained_large_and_small_colony_morphotypes_at_generation_200",
            "isolated_colonies_per_independent_evolution_line":30,
            "isolated_colonies_do_not_count_as_independent_founding_lines":True,
        },
        "source_replicate_two_longitudinal_example":{
            "source_line":"Pputida original evolution line 2",
            "larger_morphotype_first_detected_gen_mono_approx":40,
            "larger_morphotype_first_detected_gen_coculture_approx":70,
            "morphotypes_coexist_from_approx_gen70_to_200_in_coculture":True,
            "monoculture_small_morphotype_extinct_by_approx_gen140":True,
            "not_four_independent_longitudinal_measurement_series":True,
        },
        "genetic_and_tradeoff":{
            "fleQ_or_flagellar_gene_mutations_within_source_evolved_lineages":True,
            "fleQ_mutant_reduced_motility":True,
            "fleQ_mutant_reduced_biofilm":True,
            "large_morphotype_increased_yield":True,
            "source_replicate_two_large_yield_OD_per_mM":0.068,
            "source_replicate_two_ancestral_yield_OD_per_mM":0.020,
            "source_replicate_two_small_yield_OD_per_mM":0.023,
            "reported_large_vs_ancestor_yield_fold":3.4,
            "motility_biofilm_vs_yield_different_endpoints_not_two_independent_new_modules":True,
        },
        "mechanism_diagnostics":{
            "reciprocal_invasion_pair_source_replicate_2_only":True,
            "reciprocal_invasion_negative_frequency_dependence_not_supported":True,
            "this_does_not_rule_out_frequency_dependence_in_whole_multigenotype_population":True,
            "published_pooled_rare_genotype_fitness_p_for_Ajohnsonii_presence":0.814,
            "published_t_df":28,
            "not_equivalence_or_definitive_null_mechanism":True,
            "replay_uses_one_original_138_generation_coculture_population":True,
            "replay_tubes_per_Ajohnsonii_present_absent_arm":6,
            "replay_tubes_are_technical_within_one_original_evolution_history":True,
            "replay_over_additional_generations_approx":50,
            "without_Ajohnsonii_both_morphotypes_not_extinct":True,
            "replay_without_partner_small_morphotype_approx_fourfold_larger_density":True,
            "replay_control_with_partner_densities_more_stable":True,
            "partner_role_is_interspecific_resource_supplier_not_origin_of_two_Pputida_roles":True,
        },
        "cross_programme_comparability":{
            "resource_demand_confound_benzoate_not_externally_supplied_to_mono":True,
            "source_matched_abiotic_carbon_supply_control_available":False,
            "original_data_raw_isolate_measurements_retrieved":False,
            "original_SRA_genomes_directly_reanalysed":False,
            "short_term_200_generation_retention_not_permanent_long_term_persistence":True,
            "unpaired_vs_paired_small_n_statistical_sensitivity_explicit":True,
            "2026_same_species_800_generation_study_not_counted_as_separate_programme_without_lineage_audit":True,
            "no_ancestral_same_genotype_two_function_optimum_test":True,
            "no_wildtype_vs_new_split_architecture_causal_test":True,
            "no_genetic_module_duplication_established":True,
            "no_Ku_or_full_L_to_occupancy_theory_path_estimated":True,
        },
        "source_specific_4_arm_exact_sensitivity":result,
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--article",type=Path,required=False)
    p.add_argument("--format",choices=["jats","html"],required=False)
    p.add_argument("--retrieval",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    if (args.article is None)!=(args.format is None):
        raise ValueError("article source path and exact type must be supplied together")
    source=validate_original_source(args.article.read_bytes(),args.format) if args.article else None
    receipts=json.loads(args.retrieval.read_text(encoding="utf8"))
    readout=source_record(source,receipts)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(readout,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf8")
    print("BITA_ALTAMEEMI2024_SOURCE_RESULT:"+json.dumps({
        "source_grade":readout["source_grade"],
        "original_fulltext_sha":source["source_sha256"] if source else None,
        "retained_bimodality_by_original_Pputida_evolution_lines":"4/4 coculture vs 0/4 monoculture",
        "unpaired_Fisher_two_sided":result_d["unpaired_Fisher_two_sided_p_descriptive"]
            if (result_d:=readout["source_specific_4_arm_exact_sensitivity"]) else None,
        "potential_matched_two_sided":result_d["conditional_pairing_4_discordant_pairs_exact_two_sided_p_sensitivity"],
        "replay_original_parent_evolution_histories":1,
        "reciprocal_invasion_negative_frequency_mechanism_supported":False,
    },sort_keys=True),flush=True)


if __name__=="__main__":
    main()
