"""Run the declared antagonist-relief-gate analyses on the committed effect rows.

Pooling and context dependence for the four larceny strata declared in
``empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_PROTOCOL_V1.md``.
It reads the committed effect rows, so it needs no network access and CI can
re-run it; regenerating those rows from the source deposit is
``scripts/ingest_deposited_larceny_dataset.py``.

.. code-block:: bash

    python scripts/run_larceny_gate.py artifacts/supplement/larceny_gate

Every number it prints comes from ``random_effects_pool``,
``subgroup_analysis``, ``meta_regression``, ``leave_one_cluster_out``, and
``egger_small_study_test`` unmodified.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from trait_architecture.broad_meta_analysis import (
    META_EFFECT_OUTPUT_FIELDS,
    META_SUMMARY_FIELDS,
    meta_analysis,
    read_csv_rows,
    write_csv_rows,
)
from trait_architecture.context_dependence import write_context_outputs


LARCENY_STRATUM_PREFIXES = ("HF_", "HP_", "HR_")

DEFAULT_ROOT = Path("empirical/broad_reality_evidence")
DEFAULT_GATE = DEFAULT_ROOT / "larceny_gate"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir")
    parser.add_argument("--effects", default=str(DEFAULT_GATE / "larceny_effect_rows.csv"))
    parser.add_argument("--coding", default=str(DEFAULT_GATE / "larceny_moderator_coding.csv"))
    parser.add_argument("--strata", default=str(DEFAULT_ROOT / "broad_meta_analysis_strata.csv"))
    parser.add_argument("--registry", default=str(DEFAULT_GATE / "larceny_moderator_registry.csv"))
    args = parser.parse_args(argv)

    effect_rows = read_csv_rows(args.effects)
    strata = read_csv_rows(args.strata)
    coding_rows = read_csv_rows(args.coding)
    registry = read_csv_rows(args.registry)

    all_summaries, contributing_effects, _ = meta_analysis(effect_rows, strata)
    summaries = [
        row for row in all_summaries
        if str(row["stratum_id"]).startswith(LARCENY_STRATUM_PREFIXES)
    ]
    contributing = [
        row for row in contributing_effects
        if str(row.get("stratum_id", "")).startswith(LARCENY_STRATUM_PREFIXES)
    ]

    destination = Path(args.out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    write_csv_rows(destination / "larceny_pooled_summary.csv", META_SUMMARY_FIELDS, summaries)
    write_csv_rows(
        destination / "larceny_contributing_effects.csv", META_EFFECT_OUTPUT_FIELDS, contributing
    )
    context = write_context_outputs(destination, effect_rows, coding_rows, strata, registry)

    pooled = {
        str(row["stratum_id"]): {
            "independent_clusters": row["independent_clusters"],
            "pooled_effect": row["pooled_effect"],
            "ci_low": row["ci_low"],
            "ci_high": row["ci_high"],
            "two_sided_p_value": row["two_sided_p_value"],
            "I_squared_percent": row["I_squared_percent"],
            "pooled_direction": row["pooled_direction"],
            "analysis_status": row["analysis_status"],
        }
        for row in summaries
    }
    diagnostics = {
        "pooled_strata": pooled,
        "context_dependence": context,
        "interpretation_boundary": (
            "Secondary analysis of a deposited effect-size table (Leal et al. 2025, Ecology, "
            "doi:10.1002/ecy.70036). Not an independent literature search. Under declared bridge "
            "assumption B2 the fitness arrow constrains whether the multiplicative H gate on the "
            "antagonist-relief channel is open; it does not estimate the channel, the mixed "
            "partial, or any environmental derivative of it."
        ),
    }
    (destination / "larceny_gate_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(diagnostics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
