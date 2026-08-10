"""Classify screening exclusions and report the endpoint-mismatch rate.

Screening the declared search produced a result that is worth reading as evidence
rather than as bookkeeping: most excluded records were not off topic. They
manipulate a flower-associated chemical, in a floral context, on a pollinating
insect — and then measure something other than the flower's use.

That distinction matters for the theory. A study that feeds bees an alkaloid and
records parasite load is measuring the consumer. The mutualist channel of the
local interaction is about how the barrier trait changes *use of the flower*, so
such a study cannot supply a barrier-to-use contrast no matter how well it is
done. The manuscript already argues that channel-specific measurement is what the
literature lacks; this script quantifies that claim on the screened set.

The mapping from recorded reason to exclusion class is declared here in one
place, so the tabulation is reproducible and auditable rather than a judgement
re-made at reporting time.

Usage:
    python scripts/audit_screening_endpoint_mismatch.py \
      empirical/broad_reality_evidence/iota_pathway/screening_decisions_v1.csv \
      artifacts/screening_audit
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from trait_architecture.broad_meta_analysis import read_csv_rows, write_csv_rows


CLASS_FIELDS = ("exclusion_class", "records", "share_of_exclusions", "meaning")

#: Declared mapping from the reason recorded at screening to an exclusion class.
#: A reason that is absent from this mapping is reported as `unclassified` rather
#: than silently bucketed, so adding a new reason cannot quietly change a rate.
REASON_CLASS: dict[str, str] = {
    "outcome_is_parasite_load_and_mortality_not_pollinator_use": "endpoint_measures_the_consumer",
    "outcome_is_pathogen_load_not_pollinator_use": "endpoint_measures_the_consumer",
    "outcome_is_pathogen_not_pollinator_use": "endpoint_measures_the_consumer",
    "outcome_is_parasite_load_and_toxicity_not_pollinator_use": "endpoint_measures_the_consumer",
    "physiological_detoxification_outcome": "endpoint_measures_the_consumer",
    "physiological_metabolism_outcome": "endpoint_measures_the_consumer",
    "digestive_physiology_outcome": "endpoint_measures_the_consumer",
    "gustatory_neuron_response_to_sugars_not_a_barrier_trait": "trait_is_not_a_barrier",
    "non_protein_amino_acids_lack_a_declared_antagonist_reduction_role": "trait_is_not_a_barrier",
    "floral_scent_is_an_attraction_signal_not_a_barrier_trait": "trait_is_not_a_barrier",
    "floral_volatiles_are_an_attraction_signal_not_a_barrier_trait": "trait_is_not_a_barrier",
    "outcome_is_nectar_chemistry_not_pollinator_use": "endpoint_is_the_trait_itself",
    "descriptive_nectary_anatomy_and_chemistry": "descriptive_no_contrast",
    "descriptive_nectar_chemistry": "descriptive_no_contrast",
    "descriptive_floral_micromorphology": "descriptive_no_contrast",
    "review_without_primary_data": "not_primary_research",
    "commentary_without_primary_data": "not_primary_research",
    "off_topic_plant_molecular_regulation": "off_topic",
    "off_topic_plant_metabolism": "off_topic",
}

CLASS_MEANING: dict[str, str] = {
    "endpoint_measures_the_consumer": (
        "right trait, right context, wrong endpoint: the study measures parasite load, mortality, "
        "detoxification, or digestive physiology rather than use of the flower"
    ),
    "trait_is_not_a_barrier": (
        "the manipulated or measured trait has no declared antagonist-reduction role, so it is not "
        "the focal barrier trait"
    ),
    "endpoint_is_the_trait_itself": "the response variable is nectar chemistry rather than pollinator use",
    "descriptive_no_contrast": "descriptive anatomy or chemistry with no treatment and comparator",
    "not_primary_research": "review or commentary without primary data",
    "off_topic": "outside the subject area entirely",
    "unclassified": "reason not present in the declared mapping",
}

EXCLUDED_DECISIONS = {"exclude", "exclude_from_c_D_flag_for_d_A"}


def classify(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    excluded = [row for row in rows if row.get("decision") in EXCLUDED_DECISIONS]
    counts = Counter(REASON_CLASS.get(row.get("reason", ""), "unclassified") for row in excluded)
    total = len(excluded)

    class_rows = [
        {
            "exclusion_class": name,
            "records": count,
            "share_of_exclusions": f"{count / total:.6f}" if total else "",
            "meaning": CLASS_MEANING.get(name, ""),
        }
        for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]

    decisions = Counter(row.get("decision", "") for row in rows)
    screened = sum(
        count for decision, count in decisions.items() if decision != "metadata_not_retrieved"
    )
    consumer = counts.get("endpoint_measures_the_consumer", 0)

    summary = {
        "records_with_a_decision": len(rows),
        "records_screened": screened,
        "records_not_screened": decisions.get("metadata_not_retrieved", 0),
        "include_candidates": decisions.get("include_candidate", 0),
        "exclusions": total,
        "exclusions_by_class": dict(counts),
        "endpoint_measures_the_consumer_share_of_exclusions": (
            f"{consumer / total:.6f}" if total else ""
        ),
        "endpoint_measures_the_consumer_share_of_screened": (
            f"{consumer / screened:.6f}" if screened else ""
        ),
        "unclassified_reasons": sorted(
            {row.get("reason", "") for row in excluded if row.get("reason", "") not in REASON_CLASS}
        ),
        "interpretation_boundary": (
            "These are properties of the screened set, which came predominantly from one "
            "high-precision sub-query of one database. They describe what this search returned. "
            "They are not an estimate of the composition of the wider literature, and they are not "
            "evidence about nature."
        ),
    }
    return class_rows, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("screening_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)

    rows = read_csv_rows(args.screening_csv)
    class_rows, summary = classify(rows)

    destination = Path(args.out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    write_csv_rows(destination / "screening_exclusion_classes.csv", CLASS_FIELDS, class_rows)
    (destination / "screening_endpoint_mismatch_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
