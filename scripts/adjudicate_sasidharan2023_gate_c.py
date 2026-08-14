"""Combine Sasidharan 2023 audits into the canonical Gate C readout artifact.

This script deliberately treats the old DOI-first publication grouping in
`reconstruct_sasidharan2023_fvoc.py` as non-canonical. Canonical study dependence comes
from `audit_sasidharan2023_citation_topology.py`, which recovers the article's 32 studies
using exact citation identity and explicit shared DOI links only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _read(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _risk_difference(reconstruction: dict[str, Any]) -> float:
    detection = reconstruction["table2_reconstruction"]["detection"]
    poll = detection["Pollinator"]
    flor = detection["Florivore"]
    poll_p = poll["detected"] / (poll["detected"] + poll["not_detected"])
    flor_p = flor["detected"] / (flor["detected"] + flor["not_detected"])
    return flor_p - poll_p


def _published_table3_arithmetic(reconstruction: dict[str, Any]) -> dict[str, Any]:
    table3 = reconstruction["table3_reconstruction"]
    candidate = table3["candidate_denominator_definitions"][0]
    published_by_genus = {
        genus: values["published"]
        for genus, values in candidate["by_genus"].items()
    }
    printed_total = table3["published"]
    cell_sums = {
        key: sum(values[key] for values in published_by_genus.values())
        for key in ("behavioural_fvocs", "shared_both_roles", "shared_attractive", "shared_repellent")
    }
    checks = {
        key: cell_sums[key] == printed_total[key]
        for key in cell_sums
    }
    return {
        "printed_genus_cell_sums": cell_sums,
        "printed_totals": printed_total,
        "cell_sum_matches_printed_total": checks,
        "internally_arithmetic_consistent": all(checks.values()),
    }


def run(
    reconstruction_path: str | Path,
    topology_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    reconstruction = _read(reconstruction_path)
    topology = _read(topology_path)

    citation = topology["citation_topology"]
    sensitivity = topology["detection_study_sensitivity"]
    conflicts = topology["behaviour_conflicts"]
    table2 = reconstruction["table2_reconstruction"]
    table3 = reconstruction["table3_reconstruction"]

    if citation["conservative_components_same_doi_or_exact_stem"] != 32:
        raise RuntimeError("canonical conservative study topology no longer recovers 32 components")
    if not citation["matches_published_study_count"]:
        raise RuntimeError("canonical study count no longer matches the article's final study count")

    full_effect = sensitivity["full_current_deposit"]
    loo = sensitivity["leave_one_study_component_out"]
    paired = sensitivity["paired_both_role_components"]
    calculated_rd = _risk_difference(reconstruction)
    if abs(full_effect["florivore_minus_pollinator_risk_difference"] - calculated_rd) > 1e-12:
        raise RuntimeError("topology and reconstruction risk differences disagree")

    paper_detection = table2["published_detection"]
    current_detection = table2["detection"]
    current_minus_printed = {
        role: {
            category: current_detection[role].get(category, 0) - paper_detection[role].get(category, 0)
            for category in ("detected", "not_detected")
        }
        for role in ("Pollinator", "Florivore")
    }

    table3_arithmetic = _published_table3_arithmetic(reconstruction)
    choice_candidate = next(
        candidate for candidate in table3["candidate_denominator_definitions"]
        if candidate["mode"] == "choice_coded"
    )

    source_discrepancy_present = (
        any(delta != 0 for role in current_minus_printed.values() for delta in role.values())
        or not reconstruction["checkpoints"]["table2_behaviour_exact"]
        or not reconstruction["checkpoints"]["table3_exact"]
        or not table3_arithmetic["internally_arithmetic_consistent"]
    )

    gate_pass = (
        citation["matches_published_study_count"]
        and loo["runs"] == 32
        and loo["positive_direction_runs"] == 32
        and conflicts["discordant_units"] > 0
        and sensitivity["full_current_deposit"] is not None
    )

    result = {
        "canonical_status": {
            "gate_c_contribution": "PASS_AS_DEPOSITED_REANALYSIS" if gate_pass else "ADJUDICATION_REQUIRED",
            "source_discrepancy": source_discrepancy_present,
            "module_label": "quantitative_deposited_synthesis_reanalysis_with_source_discrepancy",
            "manuscript_status": "FROZEN_PENDING_OTHER_COMPLETION_GATES",
        },
        "canonical_study_topology": {
            "published_final_studies": citation["published_final_study_count"],
            "recovered_conservative_components": citation["conservative_components_same_doi_or_exact_stem"],
            "exact_citation_stems": citation["exact_citation_stems"],
            "doi_free_stems": citation["doi_free_stems"],
            "components_with_both_roles": citation["components_with_both_roles"],
            "rule": "exact normalized citation identity plus explicit shared DOI; fuzzy candidates never auto-merge",
        },
        "physiological_detection_current_deposit": {
            "counts": current_detection,
            "printed_article_counts": paper_detection,
            "current_minus_printed": current_minus_printed,
            "florivore_minus_pollinator_risk_difference": full_effect["florivore_minus_pollinator_risk_difference"],
            "florivore_over_pollinator_risk_ratio": full_effect["florivore_over_pollinator_risk_ratio"],
            "florivore_vs_pollinator_odds_ratio": full_effect["florivore_vs_pollinator_odds_ratio"],
            "leave_one_study_component_out": {
                "runs": loo["runs"],
                "risk_difference_min": loo["risk_difference_min"],
                "risk_difference_median": loo["risk_difference_median"],
                "risk_difference_max": loo["risk_difference_max"],
                "positive_direction_runs": loo["positive_direction_runs"],
                "zero_direction_runs": loo["zero_direction_runs"],
                "negative_direction_runs": loo["negative_direction_runs"],
            },
            "equal_weight_study_role_fractions": sensitivity["equal_weight_study_role_fractions"],
            "paired_both_role_components": {
                "n": paired["n"],
                "median_difference": paired["median_difference"],
                "positive": paired["positive"],
                "zero": paired["zero"],
                "negative": paired["negative"],
            },
            "interpretation": "robust assembled cross-study test-unit pattern, not a demonstrated within-study causal role effect",
        },
        "behaviour_context_dependence": {
            "unique_coded_units": conflicts["global_fvoc_insect_role_units_with_coded_behaviour"],
            "discordant_units": conflicts["discordant_units"],
            "choice_set_counts": conflicts["choice_set_counts"],
            "role_counts": conflicts["role_counts"],
            "study_component_span": conflicts["study_component_span"],
            "genus_span": conflicts["genus_span"],
            "current_deposit_category_bounds": conflicts["current_deposit_category_bounds"],
            "interpretation": "discordant repeated units are retained as cross-study/context heterogeneity rather than arbitrarily deduplicated",
        },
        "shared_fvoc_audit": {
            "choice_coded_current_deposit_total": choice_candidate["total"],
            "printed_table3_arithmetic": table3_arithmetic,
            "interpretation": "shared-both-role total is recoverable but exact shared-attraction count is source-version/table dependent",
        },
        "legacy_output_boundary": {
            "reconstruct_sasidharan2023_fvoc_publication_dependence": "NONCANONICAL_LEGACY_DIAGNOSTIC",
            "reason": "the reconstruction script's DOI-first key splits citation variants and yields 34 clusters; canonical dependence is the 32-component citation topology audit",
            "canonical_dependence_source": "audit_sasidharan2023_citation_topology.py",
        },
        "allowed_claims": [
            "The current deposited synthesis has a higher assembled physiological-detection fraction for florivore than pollinator tests by about 12.9 percentage points.",
            "That assembled contrast remains positive in all 32 leave-one-study-component-out runs.",
            "The contrast is not established as a same-study role effect; only three components have paired physiological-detection data and all three have zero difference.",
            "Six repeated FVOC-insect-role behavioural units switch between attraction and no response across studies, demonstrating context dependence in the deposited evidence.",
        ],
        "prohibited_claims": [
            "Do not call the detection contrast universal, causal, or prevalence in nature.",
            "Do not treat it as a bita model parameter or direct A x D estimate.",
            "Do not force behavioural or Table 3 counts to match the printed article by arbitrary conflict resolution.",
            "Do not use a single shared-attraction P value as definitive while printed cells, printed total, and current deposit disagree.",
        ],
    }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("reconstruction")
    parser.add_argument("topology")
    parser.add_argument("output")
    args = parser.parse_args()
    report = run(args.reconstruction, args.topology, args.output)
    print(json.dumps(report, indent=2, sort_keys=True))
