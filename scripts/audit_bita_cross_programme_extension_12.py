"""v2 independent-programme evidence extension: Al-Tameemi 2024 (12th source).

Creates a NEW additive version rather than rewriting the source-verified
11-programme v1 or changing the canonical mechanism-identification BITA
manuscript. The new source is one study/programme despite a preceding
publication that used the same originally evolving ancestor populations.

Central contrast: persistently bimodal phenotype after 200 generations
versus actual origin of mutant morphology (which occurred in both arms).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.audit_bita_cross_programme_architecture_chain import (
    SOURCE as ORIGINAL_SOURCE_DIR,
    read_source_catalogue, synthesize, row,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical" / "trait_architecture_history"
PARENT_FILE = "bita_architecture_cross_programme_evidence_20261124.json"
NEW_FILE = "altameemi2024_source_grade_evolution_and_nfds_readout.json"
EXPECTED_ARTICLE_SHA256 = "f264ccad7af897c9836ac1144ffc5d8cbdede97a034684ec7d2b9b799b223af0"
DOI = "10.1128/msystems.01053-24"


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def extend(source_dir: Path = SOURCE) -> dict:
    originals, prior_digests = read_source_catalogue(source_dir)
    original= synthesize(originals,prior_digests)
    parent_raw=(source_dir / PARENT_FILE).read_bytes()
    previous=json.loads(parent_raw)
    demand(previous==original,"previous 11-programme original-source readout changed or forked")
    new_raw=(source_dir / NEW_FILE).read_bytes()
    addition=json.loads(new_raw)
    demand(addition["paper_DOI"]==DOI,"wrong source study DOI for Al-Tameemi")
    receipt=addition["article_source_receipt"]
    demand(receipt is not None and
           receipt["source_sha256"] == EXPECTED_ARTICLE_SHA256 and
           receipt["original_article_fulltext_grade"]==
           "FULL_TEXT_PRIMARY_ARTICLE_WITH_REQUIRED_RESULTS_VERIFIED",
           "new programme lacks original full-text verified published JATS source")
    demand(addition["original_article_PMCID"]=="PMC11575400",
           "wrong original peer-reviewed article")
    demand(addition["one_new_independent_programme_relative_to_current_BITA_11"] is True,
           "this source is not the 12th distinct audited programme")
    evo=addition["source_evolution"]
    demand((evo["Pputida_coculture_bimodal_lines_at_endpoint"],
            evo["Pputida_coculture_founding_lines"],
            evo["Pputida_monoculture_bimodal_lines_at_endpoint"],
            evo["Pputida_monoculture_founding_lines"]) == (4,4,0,4),
           "Al-Tameemi independent founder population retention denominator changed")
    demand(evo["Pputida_monoculture_larger_morphotype_appeared_during_evolution"] and
           evo["Pputida_coculture_larger_morphotype_appeared_during_evolution"],
           "origination and retained bimodality must remain separate")
    tests=addition["source_specific_4_arm_exact_sensitivity"]
    demand(abs(tests["unpaired_Fisher_two_sided_p_descriptive"]-2/70)<1e-14,
           "original n4+n4 Fisher reference changed")
    demand(tests["conditional_pairing_4_discordant_pairs_exact_two_sided_p_sensitivity"]==.125,
           "founder pairing sensitivity must not be removed")
    mech=addition["mechanism_diagnostics"]
    demand(mech["reciprocal_invasion_pair_source_replicate_2_only"] and
           mech["reciprocal_invasion_negative_frequency_dependence_not_supported"] and
           mech["this_does_not_rule_out_frequency_dependence_in_whole_multigenotype_population"],
           "negative frequency dependent focal test was overpromoted")
    demand(mech["without_Ajohnsonii_both_morphotypes_not_extinct"] and
           mech["replay_tubes_are_technical_within_one_original_evolution_history"],
           "one-history replay could not be reported as multiple independent origins")
    limits=addition["cross_programme_comparability"]
    demand(limits["resource_demand_confound_benzoate_not_externally_supplied_to_mono"],
           "source acknowledged abiotic resource difference cannot be erased")
    demand(limits["no_ancestral_same_genotype_two_function_optimum_test"] and
           limits["no_genetic_module_duplication_established"],
           "morphotype retention cannot be promoted to ancestral modular split")
    demand(limits["2026_same_species_800_generation_study_not_counted_as_separate_programme_without_lineage_audit"],
           "possible overlapping future 2026 evolution series may not be independent studies")

    prior=[dict(r) for r in previous["entries"]]
    demand(len(prior)==11 and len({r["original_publication_doi"] for r in prior})==11,
           "parent research programme family changed")
    demand(DOI not in {r["original_publication_doi"] for r in prior},
           "2024 paper's original evolution programme already present")
    new_entry=row(
        "PINEAU2024", "Pseudomonas putida",
        "four P. putida coculture and four monoculture independently founded evolution lines at gen 200; technical replay only one historical line",
        {"coculture_bimodal_at_200_generations":4,
         "coculture_founding_populations":4,
         "monoculture_bimodal_at_200_generations":0,
         "monoculture_founding_populations":4,
         "original_full_text_sha256":receipt["source_sha256"]},
        "Retained colony-size polymorphism for four co-culture populations but not four monoculture populations; pure morphotype origin occurred in both.",
        has_current_or_recent_maintenance_intervention=True,
        layer="environment_dependent_phenotypic_polymorphism_retention_mechanism_unresolved",
        source_limit="Representative fleQ/small pair reciprocal invasion did not support NFDS, which is not proof the whole evolved multigenotype population lacks frequency dependence; replay one founder lineage, six technical tubes per arm. No abiotic benzoate supply matching and not a reciprocal two-function module split.",
    )
    # row(...) is restricted to the original v1 DOI registry and intentionally
    # refuses new unreviewed IDs. Build a compatible row using its schema as
    # a TEMPLATE rather than altering original v1 or DOI source registry.
    new_entry["programme_id"]="ALTAMEEMI2024"
    new_entry["original_publication_doi"]=DOI
    new_entry["organism"]="Pseudomonas putida + Acinetobacter johnsonii"
    new_entry["evidence_class"]="community_dependent_retained_polymorphism_without_focal_NFDS_support"
    new_entry["registered_source_counts"]={
        "coculture_bimodal_at_gen200":4,
        "coculture_started_evolving_Pputida_lines":4,
        "monoculture_bimodal_at_gen200":0,
        "monoculture_started_evolving_Pputida_lines":4,
        "unpaired_Fisher_two_sided_p_descriptive":tests["unpaired_Fisher_two_sided_p_descriptive"],
        "paired_founder_McNemar_two_sided_p_sensitivity":tests["conditional_pairing_4_discordant_pairs_exact_two_sided_p_sensitivity"],
        "replay_independent_original_evolution_histories":1,
        "replay_technical_cultures_per_condition":6,
        "focal_invader_genotype_pair_source_evolution_line":2,
    }
    new_entry["correct_inference_unit"]="four independently founded coculture/monoculture P. putida line pairs, and one selected original evolved population for replay"
    new_entry["source_supported_observation"]="Both larger and small colony genotypes are retained at generation 200 in all four coculture evolved lines but no monoculture evolved lines. Larger type originated in both environments; focal two-genotype invasion failed to support NFDS, while whole-community replay depends on crossfeeding species presence."
    new_entry["forward_founder_denominator_available"]=False
    new_entry["observed_forward_specialist_phenotype_or_partner_emergence"]=False
    new_entry["maintenance_or_group_intervention_present"]=True
    new_entry["de_novo_mutant_role_origin_observed"]=False
    new_entry["reverse_autonomy_or_partner_exit_observed"]=False
    new_entry["source_specific_limit"]="Complete 4+4 founder denominator for retained two-morphotype state, NOT a tested frequency of role splitting. Isolates show yield/motility trade-offs but a small morphotype is not proven to specialize in complementary function. Unmatched carbon resource levels; a single genotype-pair NFDS test inconclusive."
    new_entry["authoritative_existing_original_source_receipts"]=[NEW_FILE]
    new_entry["retained_two_morphotypes_in_coculture_after_evolution"]=True
    new_entry["founder_denominator_for_endpoint_polymorphism_available"]=True
    new_entry["focal_NFDS_mechanism_identified"]=False
    new_entry["known_resource_supplier_effect_not_separable_from_carbon_supply"]=True
    new_entry["modern_2026_related_followup_not_counted_as_extra_programme"]=True
    entries=prior+[new_entry]
    demand(len(entries)==12 and len({r["programme_id"] for r in entries})==12,
           "new research programme duplication")

    counts=dict(previous["descriptive_catalogue_counts_not_natural_prevalence"])
    counts["programmes_with_registered_maintenance_or_group_intervention"]+=1
    counts.update({
        "programmes_with_complete_founder_denominators_for_maintained_Pputida_bimodality":1,
        "programmes_with_focal_two_genotype_NFDS_unconfirmed_despite_observed_bimodality":1,
        "programmes_with_confounded_biotic_vs_abiotic_resource_supply":1,
    })
    demand(counts["programmes_with_registered_maintenance_or_group_intervention"]==6,
           "new context maintenance study not counted, or prior count altered")
    demand(counts["programmes_with_forward_specialist_phenotype_or_partner_emergence"]==3,
           "distinct colony morphotypes falsely promoted to complementary functional role splitting")
    demand(counts["programmes_with_unscreened_founder_denominator_for_forward_specialization"]==1,
           "retention 4/4 wrongly relabelled as forward ROLE origin")
    demand(counts["programmes_closing_L_to_occupancy_full_chain"]==0 and
           counts["programmes_identifying_historical_ancestral_within_genotype_two_function_module_split"]==0,
           "incompatible source promoted to full ancestral two-function mechanism")

    digest=dict(previous["source_receipts_sha256"])
    digest[NEW_FILE]=hashlib.sha256(new_raw).hexdigest()
    mapping=dict(previous["programme_to_receipt_mapping"])
    mapping["ALTAMEEMI2024"]=[NEW_FILE]
    contract=dict(previous["interpretation_contract"])
    contract.update({
        "AlTameemi_and_original_2019_200_generation_evolution_same_programme":True,
        "AlTameemi_2026_potential_followup_not_automatically_independent":True,
        "new_4of4_vs0of4_measures_retained_polymorphism_not_first_origin_frequency":True,
        "source_NFDS_unconfirmed_in_focal_pair_not_proof_of_no_NFDS_globally":True,
        "Fisher_vs_possible_founder_pairing_exact_tests_not_conflated":True,
        "technically_replicated_replay_of_one_line_not_six_independent_origins":True,
        "biotic_resource_supplementation_confounded":True,
        "programmes_still_unpooled":True,
    })
    demand(contract["no_meta_analysis"] and
           contract["no_inferred_cross_programme_effect_size_or_origin_rate"],
           "incomparable study endpoints cannot be statistically pooled")
    return {
        "title":"Historical architecture programme-level evidence v2: co-culture maintained morphotypes, source-negative focal NFDS",
        "version":"v2_additive_2026_11_24",
        "predecessor_11_programme_SHA256":hashlib.sha256(parent_raw).hexdigest(),
        "source_grade":"original_source_JATS_11_previous_machine_source_receipts_plus_new_original_2024_mSystems_fulltext",
        "programme_sampling_frame":"purposefully selected and non-exhaustive original studies; NOT systematic literature meta-analysis",
        "number_of_unique_independent_research_programmes":12,
        "number_of_distinct_machine_read_source_receipts":14,
        "source_receipts_sha256":digest,
        "programme_to_receipt_mapping":mapping,
        "entries":entries,
        "descriptive_catalogue_counts_not_natural_prevalence":counts,
        "new_12th_programme_specific_claim":{
            "article_doi":DOI,
            "independent_founding_line_retained_bimodality_exposure":"4/4 co-culture versus 0/4 monoculture at 200 generations",
            "founder_4x4_unpaired_reference_p":2/70,
            "paired_original_founder_block_reference_p":.125,
            "negative_focal_clone_pair_NFDS_test_not_supported":True,
            "whole_population_crossfed_replay_no_morphotype_extinction_with_partner_removed":True,
            "replay_technical_6_per_arm_not_independent_parent_histories":True,
            "not_original_two_task_module_origin":True,
            "biotic_vs_resource_supplied_not_deconfounded":True,
        },
        "interpretation_contract":contract,
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-dir",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    d=extend(args.source_dir)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf8")
    print("BITA_CROSS_PROGRAMME_V2_EXTEND_12:"+json.dumps({
        "independent_original_programmes":d["number_of_unique_independent_research_programmes"],
        "machine_source_receipts":d["number_of_distinct_machine_read_source_receipts"],
        "source_specific_retained_bimodality":d["new_12th_programme_specific_claim"]["independent_founding_line_retained_bimodality_exposure"],
        "source_Fisher_sensitivity":d["new_12th_programme_specific_claim"]["founder_4x4_unpaired_reference_p"],
        "source_pairing_sensitivity":d["new_12th_programme_specific_claim"]["paired_original_founder_block_reference_p"],
        "coverage":d["descriptive_catalogue_counts_not_natural_prevalence"],
    },sort_keys=True))


if __name__=="__main__":
    main()
