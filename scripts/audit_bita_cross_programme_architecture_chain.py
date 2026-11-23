"""Cross-programme scientific evidence matrix for historical trait differentiation.

This uses frozen, source-audited receipts from earlier distinct research
programmes; it DOES NOT pool non-exchangeable effect sizes, create a
representative systematic sample, or change the live BITA mechanism paper.

A programme is unique even when there are multiple source papers, different
experimental arms, several artifacts, timepoints or assay replicates. Source
observations are checked at the biological denominator of each claim.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "empirical" / "trait_architecture_history"
SOURCE_FILES = (
    "chen2024_autonomy_reversal_readout.json",
    "bacillus2018_conditional_history_readout.json",
    "kim_zhang_forward_dol_readout.json",
    "pineau2024_original_forward_divergence.json",
    "pineau2024_f2_workbook_source_reanalysis.json",
    "pineau2024_f5_original_replay_readout.json",
    "pineau2024_publisher_source_adjudication.json",
    "dsouza2016_aa_auxotrophy_fig2_readout.json",
    "kinsler2024_parent_relative_readout.json",
    "mridha2022_published_stats_readout.json",
    "mihajlovic2025_replica_reanalysis.json",
    "despres2024_matched_summary.json",
    "nasvall2026_reanalysis.json",
)
DOI = {
    "PINEAU2024": "10.1038/s41559-024-02367-y",
    "KIM2016": "10.1038/ncomms10508",
    "ZHANG2020": "10.1126/sciadv.aay5781",
    "BACILLUS_DRAGOS": "10.1038/s41564-018-0263-y",
    "CHEN2024": "10.1073/pnas.2317182121",
    "DSOUZA2016": "10.1371/journal.pgen.1006364",
    "KINSLER2024": "10.1371/journal.pbio.3002848",
    "MRIDHA2022": "10.1111/jeb.14001",
    "COGFP2025": "10.7554/eLife.97216.3",
    "DESPRES2024": "10.1126/science.ado5719",
    "NASVALL2026": "10.1093/g3journal/jkag167",
}
ROLES = {
    "PINEAU2024": "forward_phenotypic_lineage_divergence_with_retention_intervention",
    "KIM2016": "forward_cooperative_morphotype_emergence_positive_selected_fans",
    "ZHANG2020": "recurrent_terminal_specialization_not_stable_reproducing_lineage",
    "BACILLUS_DRAGOS": "engineered_division_and_evolutionary_dependency_escape",
    "CHEN2024": "reverse_specialists_to_autonomous_genotype",
    "DSOUZA2016": "environment_contingent_function_loss_not_reciprocal_split",
    "KINSLER2024": "selected_mutant_pleiotropy_vs_modular_effects",
    "MRIDHA2022": "engineered_specialist_group_payoff_vs_coexistence",
    "COGFP2025": "gene_duplication_without_observed_subfunctionalization",
    "DESPRES2024": "engineered_heteromer_rescue_without_origin_history",
    "NASVALL2026": "genetic_background_conditioned_rescue_not_module_origin",
}
INDIVIDUAL_SOURCE_PATHS = {
    "PINEAU2024": [
        "pineau2024_original_forward_divergence.json",
        "pineau2024_f2_workbook_source_reanalysis.json",
        "pineau2024_f5_original_replay_readout.json",
        "pineau2024_publisher_source_adjudication.json",
    ],
    "KIM2016": ["kim_zhang_forward_dol_readout.json"],
    "ZHANG2020": ["kim_zhang_forward_dol_readout.json"],
    "BACILLUS_DRAGOS": ["bacillus2018_conditional_history_readout.json"],
    "CHEN2024": ["chen2024_autonomy_reversal_readout.json"],
    "DSOUZA2016": ["dsouza2016_aa_auxotrophy_fig2_readout.json"],
    "KINSLER2024": ["kinsler2024_parent_relative_readout.json"],
    "MRIDHA2022": ["mridha2022_published_stats_readout.json"],
    "COGFP2025": ["mihajlovic2025_replica_reanalysis.json"],
    "DESPRES2024": ["despres2024_matched_summary.json"],
    "NASVALL2026": ["nasvall2026_reanalysis.json"],
}
EXPECTED_SEPARATE_SOURCE_BYTES = 13


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def exact_ratio(x: int, n: int) -> float:
    need(isinstance(x,int) and isinstance(n,int) and n>0 and 0<=x<=n,
         "invalid original biological event denominator")
    return x/n


def read_source_catalogue(source_dir: Path = SOURCE) -> tuple[dict,dict]:
    files = {}
    digests = {}
    for filename in SOURCE_FILES:
        name=source_dir/filename
        raw=name.read_bytes()
        files[filename] = json.loads(raw)
        digests[filename] = hashlib.sha256(raw).hexdigest()
    need(len(files)==EXPECTED_SEPARATE_SOURCE_BYTES,
         "source receipt inventory missing or deduplicated incorrectly")
    return files,digests


def check_sources(f: dict) -> None:
    k=f["kim_zhang_forward_dol_readout.json"]
    b=f["bacillus2018_conditional_history_readout.json"]
    ch=f["chen2024_autonomy_reversal_readout.json"]
    ds=f["dsouza2016_aa_auxotrophy_fig2_readout.json"]
    ki=f["kinsler2024_parent_relative_readout.json"]
    mr=f["mridha2022_published_stats_readout.json"]
    cg=f["mihajlovic2025_replica_reanalysis.json"]
    dp=f["despres2024_matched_summary.json"]
    nv=f["nasvall2026_reanalysis.json"]
    p=f["pineau2024_original_forward_divergence.json"]
    f2=f["pineau2024_f2_workbook_source_reanalysis.json"]
    f5=f["pineau2024_f5_original_replay_readout.json"]
    pub=f["pineau2024_publisher_source_adjudication.json"]

    # DOI/source identity is required for every programme, including the
    # two independent 2016/2020 programmes living in one provenance file.
    checks={
        "KIM2016":k["kim_source_readout"]["doi"],
        "ZHANG2020":k["zhang_source_readout"]["doi"],
        "BACILLUS_DRAGOS":b["paper_doi"],
        "CHEN2024":ch["source_doi"],
        "DSOUZA2016":ds["doi"],
        "KINSLER2024":ki["source_doi"],
        "MRIDHA2022":mr["study_doi"],
        "COGFP2025":cg["doi"],
        "DESPRES2024":dp["study_doi"],
        "NASVALL2026":nv["study_doi"],
        "PINEAU2024":p["publication"]["doi"],
    }
    need(set(checks)==set(DOI),"distinct research-programme identity changed")
    for key,actual in checks.items():
        need(actual == DOI[key],f"{key} original programme DOI source changed")
    need(f5["article_doi"]==DOI["PINEAU2024"],"Pineau replay DOI mismatch")
    need(pub["source_doi"]==DOI["PINEAU2024"],"Pineau publisher source DOI mismatch")
    need(f2["source"]["sha256"]==f5["original_git_pinned_xlsx"]["sha256"]
         ==pub["original_author_source_receipt"]["sha256"],
         "Pineau original XLSX provenance differs across studies")
    need(pub["publisher_source_downloaded"] is False,"publisher copy newly available, re-adjudicate!")
    need(pub["publisher_comparison"]["quarantine_author_l1_and_s1_day40_retained"] is True,
         "Pineau publisher duplicate source quarantine removed without adjudication")
    need(f5["original_Fig5A_source_duplicate_audit"]["cross_population_duplicate_pairs"]==1,
         "Pineau exact measured duplicate gate changed")
    need(f5["original_Fig5A_source_duplicate_audit"]["exact_duplicate_source_column_pairs"][0][
        "identical_excel_row_and_numeric_value_pairs"]==164,
         "Pineau original duplicate count changed")
    need(f5["primary_quarantined_independent_day40_endpoints"]["small"][
        "independent_original_population_day40_endpoints_after_QA"]==3,
        "Pineau source valid Small endpoints changed")
    need(f5["primary_quarantined_independent_day40_endpoints"]["large"][
        "independent_original_population_day40_endpoints_after_QA"]==2,
        "Pineau source valid Large endpoints changed")

    src=p["single_evolution_programme"]
    need((src["authors_dimorphism_successes"],
          src["independent_initial_aerobic_populations"])==(3,5),
         "Pineau independent forward evolution founder denominator changed")
    need((f2["standard_O2_reanalysis"]["complete_trajectory_count"],
          f2["high_O2_reanalysis"]["complete_trajectory_count"])==(8,7),
         "Pineau same-source competition assays no longer matched")

    need((ch["three_regime_success_counts"],
          ch["three_regime_started_counts"])==([0,0,5],[12,12,12]),
         "Chen reverse evolution environment denominator changed")
    need(ch["forward_specialization_origin_identified"] is False,
         "Chen reverse-to-autonomy must not be reclassified as forward origin")
    need(b["effects"]["mixed_delta_eps_extinct"]=={"events":4,"n":6},
         "Bacillus coevolution partner persistence endpoint changed")
    need(b["effects"]["historical_ancestral_architecture_origin_identified"] is False,
         "engineered Bacillus must not become de novo original split")
    endpoint=ds["primary_endpoint"]
    need((endpoint["aa_positive_populations"],
          endpoint["aa_evolutionary_populations"],
          endpoint["nonAA_positive_populations"],
          endpoint["nonAA_evolutionary_populations"])==(6,8,0,8),
         "D'Souza auxotrophy observation denominator changed")
    need(ds["genetic_auxotrophy_equivalent_to_reciprocal_division_of_labour"] is False,
         "D'Souza function loss cannot be promoted to reciprocal functional split")
    counts=ki["publisher_count_reconstruction"]
    need((counts["Evo2D"]["selected_adaptive_clones"],
          counts["Evo2D"]["both_fermentation_respiration_positive"],
          counts["Evo3D"]["selected_adaptive_clones"],
          counts["Evo3D"]["both_fermentation_respiration_positive"])==(306,109,202,25),
         "Kinsler selected isolate counts changed")
    need(ki["interpretation_ceiling"]["single_evolved_clone_not_an_independent_evolution_population"] is True,
         "Kinsler selected clone unit must not be independent programme")
    need([r["productivity_direction_vs_wildtype"] for r in mr["conditions"]]==[
        "higher","not_resolved","lower","lower"],
        "Mridha conditional specialist group payoff signs changed")
    need(mr["independent_studies_n"]==1 and mr["environmental_strata_n"]==4,
         "Mridha four media cannot become four independent papers")
    need(cg["independent_biological_replicates_per_group"]==3
         and cg["evolutionary_origin_or_hysteresis_identified"] is False,
         "coGFP duplication model cannot become successful two-function split")
    need((dp["strict_both_parent_nonfunctional_and_pair_functional"],
          dp["both_parent_homomers_directly_measured_nonfunctional_pairs"])==(22,105),
         "Fcy1 source matched pair denominators changed")
    need(dp["historical_evolutionary_origins_estimated"] is False,
         "Fcy1 source selected cross panels not independent evolved origins")
    need((nv["groups"]["mutator"]["rescue"],nv["groups"]["mutator"]["started"],
          nv["groups"]["nonmutator"]["rescue"],nv["groups"]["nonmutator"]["started"])==(21,24,10,24),
         "Näswall genetic route source founding denominators changed")
    need(nv["empirical_hysteresis_effect_identified"] is False,
         "Näswall genetic background readout not a hysteresis observation")
    need(k["comparison"]["independent_research_programmes"]==2,
         "Kim and Zhang must remain TWO independent original programmes")
    need(k["kim_source_readout"]["selected_successes_all_plated_denominator_observed"] is False,
         "Kim selected fans do not identify origin frequency")


def row(id: str,taxon: str,original_unit: str,counts:dict,empirical_claim:str,
        has_forward_founder_denominator:bool=False,
        has_observed_forward_diff:bool=False,
        has_current_or_recent_maintenance_intervention:bool=False,
        has_de_novo_mutant_origin:bool=False,
        has_reverse_exit:bool=False,
        has_original_controlled_module_split:bool=False,
        has_matched_ancestral_conflict_measure:bool=False,
        layer:str="contextual_boundary",
        source_limit:str="") -> dict:
    if id not in DOI or id not in ROLES:
        raise ValueError("unknown original source programme")
    return {
        "programme_id":id,
        "original_publication_doi":DOI[id],
        "organism":taxon,
        "evidence_class":ROLES[id],
        "evidence_layer":layer,
        "correct_inference_unit":original_unit,
        "registered_source_counts":counts,
        "source_supported_observation":empirical_claim,
        "forward_founder_denominator_available":has_forward_founder_denominator,
        "observed_forward_specialist_phenotype_or_partner_emergence":has_observed_forward_diff,
        "maintenance_or_group_intervention_present":has_current_or_recent_maintenance_intervention,
        "de_novo_mutant_role_origin_observed":has_de_novo_mutant_origin,
        "reverse_autonomy_or_partner_exit_observed":has_reverse_exit,
        "ancestral_within_genotype_two_function_module_split_identified":has_original_controlled_module_split,
        "matched_ancestral_shared_coordinate_conflict_fitness_assayed":has_matched_ancestral_conflict_measure,
        "fully_identifies_L_R_Phi_K_accessibility_invasion_fixation_occupancy":False,
        "source_specific_limit":source_limit,
        "authoritative_existing_original_source_receipts":INDIVIDUAL_SOURCE_PATHS[id],
    }


def synthesize(f:dict,source_hashes:dict)->dict:
    check_sources(f)
    pineau=f["pineau2024_original_forward_divergence.json"]
    f2=f["pineau2024_f2_workbook_source_reanalysis.json"]
    f5=f["pineau2024_f5_original_replay_readout.json"]
    ch=f["chen2024_autonomy_reversal_readout.json"]
    bac=f["bacillus2018_conditional_history_readout.json"]
    kimzhang=f["kim_zhang_forward_dol_readout.json"]
    ds=f["dsouza2016_aa_auxotrophy_fig2_readout.json"]
    kin=f["kinsler2024_parent_relative_readout.json"]
    mr=f["mridha2022_published_stats_readout.json"]
    cg=f["mihajlovic2025_replica_reanalysis.json"]
    dp=f["despres2024_matched_summary.json"]
    nv=f["nasvall2026_reanalysis.json"]

    psmall=f5["primary_quarantined_independent_day40_endpoints"]["small"]
    plarge=f5["primary_quarantined_independent_day40_endpoints"]["large"]
    psource=pineau["single_evolution_programme"]
    tab=[]

    tab.append(row(
        "PINEAU2024","Saccharomyces cerevisiae",
        "five independent PO aerobic founding evolution populations; PO-4 competition pair; QA-valid replays 3 Small + 2 Large",
        {"evolved_divergent_populations":psource["authors_dimorphism_successes"],
         "evolved_PO_populations_started":psource["independent_initial_aerobic_populations"],
         "PO4_standard_O2_competitions":f2["standard_O2_reanalysis"]["complete_trajectory_count"],
         "PO4_supplemented_O2_competitions":f2["high_O2_reanalysis"]["complete_trajectory_count"],
         "QA_valid_Small_replay_day40_populations":psmall["independent_original_population_day40_endpoints_after_QA"],
         "QA_valid_Large_replay_day40_populations":plarge["independent_original_population_day40_endpoints_after_QA"],
         "excluded_duplicated_original_area_pairs":164,
         "QA_valid_Small_mean_day40_minus_first_radius_um":psmall["mean_per_valid_line_day40_minus_initial_um"],
         "QA_valid_Large_mean_day40_minus_first_radius_um":plarge["mean_per_valid_line_day40_minus_initial_um"],
         "PO4_standard_equilibrium_from_raw_F2A":f2["standard_O2_reanalysis"]["first_last_fit"]["equilibrium_if_slope_nonzero"],
         "PO4_high_O2_mean_final_large_fraction":f2["high_O2_reanalysis"]["first_last_fit"]["mean_final_fraction"]},
        "Founder PO phenotype divergence with two failed lines; PO4 oxygen-sensitive coexistence and QA-validated reverse size shift when competitor is removed",
        has_forward_founder_denominator=True,has_observed_forward_diff=True,
        has_current_or_recent_maintenance_intervention=True,
        layer="forward_phenotypic_origin_and_ecological_maintenance",
        source_limit="One single study; phenotypic alternative yeast lineage divergence is not a genetic two-function module split. QA duplicates quarantine both l1/s1 Day40; publisher raw xlsx unavailable."))
    kk=kimzhang["kim_source_readout"]
    tab.append(row("KIM2016","Pseudomonas fluorescens",
        "preselected positive independent spreading-fan contexts; colony CFU and polymer-engineered controls",
        {"individually_chosen_successful_D_fan_mutants":kk["dry_mutants_sequenced_from_separate_fans"],
         "CFU_mixed_single_source_figure_anova_p":kk["figure_1_single_vs_mixed_cfu_anova_p"],
         "polymer_loss_control_anova_p":kk["figure_4_lubrication_control_cfu_anova_p"],
         "source_M_equilibrium_fraction_approx":kk["source_stable_M_fraction_approx"]},
        "New complementary Dry role from Mucoid background, required polymer and collective spread; no denominator of all founding colonies",
        has_observed_forward_diff=True,has_de_novo_mutant_origin=True,
        has_current_or_recent_maintenance_intervention=True,
        layer="forward_partner_emergence_without_unscreened_denominator",
        source_limit="Parent already rsmE-mutant, selected successful D fans only, not an ancestral two-function generalist or unbiased probability of origin."))
    zz=kimzhang["zhang_source_readout"]
    tab.append(row("ZHANG2020","Streptomyces coelicolor",
        "source-selected terminal mutant clones, nested in parent colony; colony mixing frequency",
        {"selected_mutants":zz["selected_mutant_strains"],
         "selected_mutants_reduced_spore_production":zz["selected_mutants_with_reduced_spore_production"],
         "antibiotic_fraction_model_F":zz["fig4_antibiotic_vs_mutant_fraction_F"],
         "spore_fraction_model_F":zz["fig4_spore_fitness_vs_mutant_fraction_F"]},
        "Somatic-like terminal genome variants hyperproduce antibiotics at clone fertility cost; parents regenerate terminal differentiation",
        has_observed_forward_diff=True,has_de_novo_mutant_origin=True,
        has_current_or_recent_maintenance_intervention=True,
        layer="terminal_functional_division_no_stable_specialist_line",
        source_limit="Thirty selected clones are not 30 biological origins, terminal mutants lack stable independent reproduction; no raw original Figure4 mixing values."))
    z=bac["effects"]["mixed_delta_eps_extinct"]
    tab.append(row("BACILLUS_DRAGOS","Bacillus subtilis",
        "independently evolved mixed pellicle culture, not engineered EPS/TasA clone count",
        {"mixed_cultures_eps_partner_extinct":z["events"],
         "mixed_cultures_started":z["n"],
         "monoculture_eps_dependency_escape_events":bac["effects"]["monoculture_delta_eps_autonomy"]["events"],
         "monoculture_eps_started":bac["effects"]["monoculture_delta_eps_autonomy"]["n"]},
        "Engineered complementary EPS/TasA partner association sometimes raises short-run pellicle output but Δeps partner is lost in four of six coevolved mixed cultures",
        has_current_or_recent_maintenance_intervention=True,has_reverse_exit=True,
        layer="engineered_split_evolutionary_instability",
        source_limit="Two source publications from the same programme; engineered division, not a newly evolved forward origin."))
    tab.append(row("CHEN2024","Pseudomonas stutzeri",
        "independently started evolution lines within each of three carbon regimes",
        {"autonomist_events_by_regime":ch["three_regime_success_counts"],
         "started_lines_by_regime":ch["three_regime_started_counts"],
         "sequenced_successful_evolution_lines":ch["fluctuating_genetic_origins"]["independent_lineages"]},
        "Specialist pair genetically regains whole-pathway autonomist in 5/12 alternating lines, not in either constant 0/12 arm",
        has_reverse_exit=True,layer="reverse_architecture_exit",
        source_limit="Genetic reacquisition consistent with HGT; reverse direction only; simulated parameter sets not biological programmes."))
    e=ds["primary_endpoint"]
    tab.append(row("DSOUZA2016","Escherichia coli",
        "16 independent evolving populations (8 with amino acids and 8 without); 96 repeated assay cells",
        {"AA_supplied_detectable_auxotroph_lines_gen2000":e["aa_positive_populations"],
         "AA_supplied_started_lines":e["aa_evolutionary_populations"],
         "no_AA_detectable_auxotroph_lines_gen2000":e["nonAA_positive_populations"],
         "no_AA_started_lines":e["nonAA_evolutionary_populations"]},
        "Environment-dependent terminal detectability of evolved auxotrophy, not independently identified mutation-origin frequency or reciprocal role split",
        layer="conditional_function_loss_context",
        source_limit="Source figure cells are repeated assays and detection can change without genotype origin/extinction; original Dryad workbook inaccessible."))
    ek=kin["publisher_count_reconstruction"]
    tab.append(row("KINSLER2024","Saccharomyces cerevisiae",
        "selected barcoded adaptive clone, nested in evolution condition, ancestral background and historical publication",
        {"Evo2D_selected_clones":ek["Evo2D"]["selected_adaptive_clones"],
         "Evo2D_both_function_gain_clones":ek["Evo2D"]["both_fermentation_respiration_positive"],
         "Evo3D_selected_clones":ek["Evo3D"]["selected_adaptive_clones"],
         "Evo3D_both_function_gain_clones":ek["Evo3D"]["both_fermentation_respiration_positive"],
         "total_older_and_current_S1_clone_rows":kin["S1_all_rows"]},
        "Phenotypic scope of selected adaptive mutations across fermentation and respiration depends on backgrounds, source and assay class",
        layer="conditional_mutational_effect_scope",
        source_limit="S1 pools 2024 and prior publication clones; not an unscreened mutation origin sample, nor independently evolved 306/202 populations."))
    tab.append(row("MRIDHA2022","Pseudomonas aeruginosa",
        "engineered mixed-specialist culture under iron environmental strata, not de novo origin",
        {"experimental_blocks":mr["design"]["independent_experimental_blocks"],
         "environmental_strata":mr["environmental_strata_n"],
         "WT_relative_group_payoff_directions":[q["productivity_direction_vs_wildtype"] for q in mr["conditions"]]},
        "Specialist mix can coexist with negative frequency dependence while mixed group productivity switches from above to below WT across iron regimes",
        has_current_or_recent_maintenance_intervention=True,
        layer="payoff_and_occupancy_are_distinct",
        source_limit="Engineered split; growth AUC source reported and Dryad raw values unavailable; negative frequency dependence not an adaptive origin."))
    tab.append(row("COGFP2025","Escherichia coli",
        "independent replicate fluorescence evolution lines per one vs two gene copies",
        {"independent_lines_per_copy_number":cg["independent_biological_replicates_per_group"],
         "two_gene_copy_subfunctionalization_in_source":False},
        "A second gene copy can change robustness or fluorescent-cell fraction without observed division into different specialized functions",
        layer="duplication_negative_control",
        source_limit="One vs two copy GFP adaptation, not forward division of two distinct tasks or a historical module split."))
    tab.append(row("DESPRES2024","Saccharomyces cerevisiae",
        "matched engineered mutant allele pair with both parental homomer growth controls",
        {"strict_heteromer_rescue_pairs":dp["strict_both_parent_nonfunctional_and_pair_functional"],
         "pairs_with_both_parent_controls":dp["both_parent_homomers_directly_measured_nonfunctional_pairs"]},
        "Engineered Fcy1 heteromer can rescue function of two defective homomer pairs, demonstrating complementation but not historical architecture origin",
        layer="complementation_without_origins",
        source_limit="Shared component alleles; 105 mutant combinations not independent evolutionary origin events; no matched original WT optimal shared genotype."))
    tab.append(row("NASVALL2026","Salmonella",
        "48 independently started populations across mutator and nonmutator genetic backgrounds",
        {"mutator_rescued_lines":nv["groups"]["mutator"]["rescue"],
         "mutator_started":nv["groups"]["mutator"]["started"],
         "nonmutator_rescued_lines":nv["groups"]["nonmutator"]["rescue"],
         "nonmutator_started":nv["groups"]["nonmutator"]["started"]},
        "Different genetic backgrounds grant different physiological-rescue routes, not an observed division into two complementary modules",
        layer="background_conditioned_genetic_accessibility",
        source_limit="Not a matched split/history experiment; rescue is not emergence of two jointly maintained specialist units or hysteresis."))

    ids=[r["programme_id"] for r in tab]
    need(len(ids)==len(DOI)==11 and len(set(ids))==len(ids)
         and set(ids)==set(DOI),"source family duplication or missing programme")
    need(sum(x["forward_founder_denominator_available"] for x in tab)==1,
         "incorrect creation of replicated forward origin denominator")
    need(sum(x["observed_forward_specialist_phenotype_or_partner_emergence"] for x in tab)==3,
         "changed descriptive selection of forward programmes")
    need(sum(x["ancestral_within_genotype_two_function_module_split_identified"] for x in tab)==0,
         "source readout incorrectly promoted to independent ancestral genetic two-task module split")
    need(sum(x["fully_identifies_L_R_Phi_K_accessibility_invasion_fixation_occupancy"] for x in tab)==0,
         "no source closes SLK causal chain")
    for x in tab:
        need(x["source_specific_limit"].strip()!="","unbounded source claim")
        need(all(k in source_hashes for k in x["authoritative_existing_original_source_receipts"]),
             "source readout missing from index")
    # Do not add counts from distinct incomparable event definitions to one
    # binomial denominator, a meta-analysis, or a universal mechanism rate.
    digest = {id:sorted(INDIVIDUAL_SOURCE_PATHS[id]) for id in ids}
    return {
        "title":"Original-source programme-grain architecture evolution evidence map",
        "time_scope":"2026-11-24 curated source-frozen repository programme",
        "programme_sampling_frame":"purposefully selected original-source research programmes, NOT a systematic sample",
        "number_of_unique_independent_research_programmes":len(tab),
        "number_of_distinct_machine_read_source_receipts":len(source_hashes),
        "source_receipts_sha256":source_hashes,
        "programme_to_receipt_mapping":digest,
        "entries":tab,
        "descriptive_catalogue_counts_not_natural_prevalence":{
            "programmes_with_forward_specialist_phenotype_or_partner_emergence":3,
            "programmes_with_unscreened_founder_denominator_for_forward_specialization":1,
            "programmes_with_registered_maintenance_or_group_intervention":sum(x["maintenance_or_group_intervention_present"] for x in tab),
            "programmes_with_reverse_autonomy_or_partner_exit":sum(x["reverse_autonomy_or_partner_exit_observed"] for x in tab),
            "programmes_identifying_historical_ancestral_within_genotype_two_function_module_split":0,
            "programmes_closing_L_to_occupancy_full_chain":0,
        },
        "source_verified_non_pooling_examples":{
            "Pineau_aerobic_divergence":"3 of 5 independent founding evolution lines",
            "Pineau_competitor_removed_3_small_mean_radius_change_um":psmall["mean_per_valid_line_day40_minus_initial_um"],
            "Pineau_competitor_removed_2_large_mean_radius_change_um":plarge["mean_per_valid_line_day40_minus_initial_um"],
            "Pineau_excluded_identical_area_pairs":164,
            "Chen_alternating_reverse_autonomy":"5/12 vs 0/12,0/12 in other carbon regimes",
            "Bacillus_evolved_engineered_partner_loss":"4/6, same Bacillus programme as short-run benefit",
            "D_Souza_gen2000_auxotrophy_detection":"6/8 supplemented vs 0/8 not supplemented",
            "Kinsler_phenotype_both_gain_selected_clones":"109/306 Evo2D vs 25/202 Evo3D, not evolution replicates",
            "Mridha_payoff_direction":"higher in iron replete, unresolved in plain CAA, lower in both chelator conditions",
        },
        "interpretation_contract":{
            "stage_separation":"forward biological emergence != immediate group payoff != ecological retention != evolutionary escape",
            "same_source_repeated_assays_never_relabelled_as_new_programmes":True,
            "Pineau_4_derivative_receipts_count_as_one_programme":True,
            "Kim_and_Zhang_shared_receipt_count_as_two_separate_original_programmes":True,
            "Bacillus_two_article_programme_counted_once":True,
            "programmes_with_different_event_definitions_never_pooled":True,
            "no_meta_analysis":True,
            "no_inferred_cross_programme_effect_size_or_origin_rate":True,
            "no_prevalence_in_nature_or_complete_literature_universe":True,
            "no_matched_original_shared_vs_differentiated_cost_bridge_Ku":True,
            "active_BITA_mechanism_identification_paper_untouched":True,
            "legacy_architecture_chapter2_and_SLK_owned_by_theory_companion":True,
            "focal_experiment_is_not_this_literature_synthesis":True,
        },
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-dir",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    f,digests=read_source_catalogue(args.source_dir)
    q=synthesize(f,digests)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(q,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf8")
    print("BITA_CROSS_PROGRAMME_SOURCE_GRADE:"+json.dumps({
        "count_programmes":q["number_of_unique_independent_research_programmes"],
        "source_receipts":q["number_of_distinct_machine_read_source_receipts"],
        "coverage":q["descriptive_catalogue_counts_not_natural_prevalence"],
        "independent_programmes":list(DOI),
        "Pineau_complete_source_identity":len(q["programme_to_receipt_mapping"]["PINEAU2024"])==4,
        "no_pool":q["interpretation_contract"]["no_meta_analysis"],
    },sort_keys=True))


if __name__=="__main__":
    main()
