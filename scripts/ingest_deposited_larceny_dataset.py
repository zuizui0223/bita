"""Ingest the deposited floral-larceny effect table into the declared schemas.

Executes the extraction rules pre-registered in
``empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_PROTOCOL_V1.md``:
recompute every effect from the deposited group means, quarantine rows that
disagree with their own group means, aggregate each study cluster to one effect
under a declared within-cluster correlation, and code the declared moderators.

The source table is a deposit of a published synthesis and is **not** vendored
into this repository, per the data policy in ``README.md``. Clone it first:

.. code-block:: bash

    git clone https://github.com/lacaleal/Meta-analysis_larcenists /tmp/larcenists
    git -C /tmp/larcenists checkout 04663ff895b300fc957c4a32f661e5f73ca95217

    python scripts/ingest_deposited_larceny_dataset.py \\
      /tmp/larcenists/complete_hedges.csv \\
      empirical/broad_reality_evidence/larceny_gate

Writes ``larceny_effect_rows.csv``, ``larceny_moderator_coding.csv``, and
``larceny_recomputation_audit.csv``. It computes no pooled estimate; pooling is
``scripts/run_broad_meta_analysis.py`` and ``scripts/run_context_dependence.py``.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from trait_architecture.broad_meta_analysis import EFFECT_FIELDS, write_csv_rows
from trait_architecture.context_dependence import MODERATOR_CODING_FIELDS
from trait_architecture.deposited_effect_ingest import (
    AUDIT_FIELDS,
    build_cluster_effects,
    declared_effect_row,
    read_group_contrasts,
)


SOURCE_REPOSITORY = "https://github.com/lacaleal/Meta-analysis_larcenists"
SOURCE_COMMIT = "04663ff895b300fc957c4a32f661e5f73ca95217"
SOURCE_FILE = "complete_hedges.csv"
SYNTHESIS_DOI = "10.1002/ecy.70036"
SOURCE_BASIS = "deposited_effect_size_table_of_published_synthesis"

#: One declared stratum per deposited outcome family.
STRATA: dict[str, dict[str, str]] = {
    "female": {
        "stratum_id": "HF_larceny_female_lrr_comparative",
        "route": "H_to_fitness",
        "trait_class": "nectar_larceny",
        "outcome_class": "female_reproductive_success",
        "effect_metric": "log_response_ratio",
        "design_class": "comparative",
        "effect_prefix": "LGF",
    },
    "visitation": {
        "stratum_id": "HP_larceny_visitation_lrr_comparative",
        "route": "H_to_pollination",
        "trait_class": "nectar_larceny",
        "outcome_class": "visitation_rate",
        "effect_metric": "log_response_ratio",
        "design_class": "comparative",
        "effect_prefix": "LGP",
    },
    "nectar": {
        "stratum_id": "HR_larceny_nectar_lrr_comparative",
        "route": "H_to_reward",
        "trait_class": "nectar_larceny",
        "outcome_class": "nectar_standing_crop",
        "effect_metric": "log_response_ratio",
        "design_class": "comparative",
        "effect_prefix": "LGR",
    },
    "male": {
        "stratum_id": "HF_larceny_male_lrr_comparative",
        "route": "H_to_fitness",
        "trait_class": "nectar_larceny",
        "outcome_class": "male_reproductive_success",
        "effect_metric": "log_response_ratio",
        "design_class": "comparative",
        "effect_prefix": "LGM",
    },
}

#: Declared moderator name -> (source column, level renaming).
#: Renaming exists so the committed coding reads as declared ecology rather than
#: as the source file's private vocabulary. ``NA`` maps to nothing and is coded
#: ``not_applicable``.
MODERATORS: dict[str, tuple[str, dict[str, str]]] = {
    "larcenist_type": ("Larcenist_type", {
        "Robbers": "nectar_robbing",
        "Thieves": "nectar_theft",
    }),
    "reproductive_assurance": ("self_compatible", {
        "yes": "self_compatible",
        "no": "self_incompatible",
    }),
    "larceny_assignment": ("type_study", {
        "Experimental": "experimental_manipulation",
        "Non-Experimental": "observational_contrast",
    }),
    "interaction_players": ("players", {
        "insect-insect": "insect_insect",
        "insect-bird": "insect_bird",
        "bird-bird": "bird_bird",
    }),
}

CODER_ID = "deterministic_ingest_of_deposited_moderator_columns"


def read_semicolon_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle, delimiter=";")
        ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_csv", help=f"path to the deposited {SOURCE_FILE}")
    parser.add_argument("out_dir")
    parser.add_argument(
        "--within-cluster-correlation", type=float, default=1.0,
        help="declared rho_w for within-cluster aggregation (primary run: 1.0)",
    )
    parser.add_argument(
        "--include-quarantined", action="store_true",
        help="declared sensitivity run: retain rows whose deposited sign disagrees with their group means",
    )
    args = parser.parse_args(argv)

    source_rows = read_semicolon_csv(args.source_csv)
    if not source_rows:
        parser.error("the deposited table is empty")

    effect_rows: list[dict[str, object]] = []
    coding_rows: list[dict[str, object]] = []
    audit_rows: list[dict[str, object]] = []
    stratum_counts: dict[str, dict[str, int]] = {}

    for metric, stratum in STRATA.items():
        subset = [row for row in source_rows if row.get("Type_of_metric") == metric]
        if not subset:
            continue
        contrasts = read_group_contrasts(
            subset,
            row_id_field="sample",
            cluster_field="study",
            treatment_prefix="larcenist",
            control_prefix="control",
            effect_field="yi",
            variance_field="vi",
        )
        cluster_effects, audits = build_cluster_effects(
            contrasts,
            correlation=args.within_cluster_correlation,
            include_quarantined=args.include_quarantined,
        )
        for audit in audits:
            audit["source_metric"] = metric
        audit_rows.extend(audits)

        by_cluster = {row["study"]: row for row in subset}
        for cluster_effect in cluster_effects:
            cluster = str(cluster_effect["study_cluster_id"])
            effect_id = f"{stratum['effect_prefix']}_{cluster}"
            members = [row for row in subset if row["study"] == cluster]
            species = sorted({row.get("sp_plant", "") for row in members} - {""})
            taxon = species[0] if len(species) == 1 else f"multiple_species:{len(species)}"
            locator = (
                f"{SOURCE_REPOSITORY}@{SOURCE_COMMIT}:{SOURCE_FILE}"
                f" rows[sample]={cluster_effect['source_row_ids']};"
                f" synthesis_doi={SYNTHESIS_DOI}; primary_study_label={cluster}"
            )
            note = (
                f"Recomputed as ln(mean_larcenist/mean_control) from deposited group means; "
                f"{cluster_effect['source_row_count']} deposited effect(s) aggregated to one "
                f"cluster effect at within-cluster correlation rho_w="
                f"{args.within_cluster_correlation:g}. Secondary analysis of a deposited table; "
                f"not an independent extraction from the primary article."
            )
            effect_rows.append(declared_effect_row(
                cluster_effect,
                effect_id=effect_id,
                stratum=stratum,
                taxon=taxon,
                doi="",
                source_basis=SOURCE_BASIS,
                source_locator=locator,
                extraction_note=note,
            ))

            for moderator_name, (column, renaming) in MODERATORS.items():
                raw_levels = sorted({row.get(column, "") for row in members} - {""})
                mapped = sorted({renaming[level] for level in raw_levels if level in renaming})
                if len(mapped) == 1 and len(raw_levels) == 1:
                    coding_rows.append({
                        "effect_id": effect_id,
                        "moderator_name": moderator_name,
                        "moderator_value": mapped[0],
                        "coding_basis": (
                            f"deposited column '{column}' = '{raw_levels[0]}', constant across the "
                            f"{len(members)} deposited row(s) of this study cluster"
                        ),
                        "coder_id": CODER_ID,
                        "coding_date": "2026-08-10",
                        "coding_status": "coded",
                    })
                else:
                    reason = (
                        "undeclared or missing level in the deposited column"
                        if not mapped else
                        "study cluster spans more than one declared level; the level is not "
                        "assignable after the declared one-effect-per-cluster aggregation"
                    )
                    coding_rows.append({
                        "effect_id": effect_id,
                        "moderator_name": moderator_name,
                        "moderator_value": "",
                        "coding_basis": f"deposited column '{column}' = {raw_levels or ['<blank>']}: {reason}",
                        "coder_id": CODER_ID,
                        "coding_date": "2026-08-10",
                        "coding_status": "not_applicable",
                    })

        stratum_counts[stratum["stratum_id"]] = {
            "deposited_rows": len(subset),
            "clusters_with_effect": len(cluster_effects),
            "quarantined_rows": sum(
                1 for audit in audits if str(audit.get("handling", "")).startswith("excluded")
            ),
        }
        del by_cluster

    destination = Path(args.out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    write_csv_rows(destination / "larceny_effect_rows.csv", EFFECT_FIELDS, effect_rows)
    write_csv_rows(destination / "larceny_moderator_coding.csv", MODERATOR_CODING_FIELDS, coding_rows)
    write_csv_rows(destination / "larceny_recomputation_audit.csv", AUDIT_FIELDS, audit_rows)

    verdict_counts: dict[str, int] = {}
    for audit in audit_rows:
        key = str(audit["agreement_verdict"])
        verdict_counts[key] = verdict_counts.get(key, 0) + 1

    diagnostics = {
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": SOURCE_COMMIT,
        "source_file": SOURCE_FILE,
        "synthesis_doi": SYNTHESIS_DOI,
        "within_cluster_correlation": args.within_cluster_correlation,
        "include_quarantined": args.include_quarantined,
        "deposited_rows_read": len(source_rows),
        "effect_rows_emitted": len(effect_rows),
        "moderator_coding_rows": len(coding_rows),
        "recomputation_verdicts": verdict_counts,
        "per_stratum": stratum_counts,
        "interpretation_boundary": (
            "These are effect rows, not a result. Every value is recomputed from group means "
            "deposited by the authors of a published synthesis; this is a secondary analysis of "
            "that deposit and inherits its inclusion criteria. It is not an independent literature "
            "search and must not be reported as one."
        ),
    }
    (destination / "larceny_ingest_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(diagnostics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
