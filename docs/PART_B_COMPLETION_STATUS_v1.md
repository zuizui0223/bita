# Part B completion status v1

## Statement

The Part B **meta-analysis framework is code-complete and reproducible**. Every
analytical layer, the orchestration pipeline, the honesty guards, and the source
routing run deterministically and are reproduced in CI. The only remaining input
is verified numeric effect data, which enters through the existing schema and
flows through the pipeline automatically.

"Complete" here means the *method* is finished, not that the *evidence base* is
full — filling the arrows with verified effects is ongoing data work by design.

## What is done (reproducible + CI)

| Layer / step | Implementation | CI |
|---|---|---|
| B1 direction map | `broad_meta_analysis.direction_map` | `part-b-pipeline.yml` |
| B2 per-arrow envelopes | `broad_meta_analysis.meta_analysis` | `part-b-pipeline.yml` |
| B3 moderator/conditionality | `part_b_moderator.moderator_contrast` | `part-b-pipeline.yml` |
| B4 break-even bound on `c_AD` | `part_b_support` | `part-b-pipeline.yml` |
| B5 evidence + regime-leverage priority | `part_b_arrow_evidence` | `part-b-pipeline.yml` |
| Orchestration (B1–B5) | `part_b_pipeline` / `scripts/run_part_b_support.py` | `part-b-pipeline.yml` |
| Honesty guard (no unverified leakage) | `scripts/validate_part_b_integrity.py` | `part-b-integrity.yml` |
| Candidate source resolution (C3) | `d_a_source_resolver` / `scripts/resolve_d_a_candidate_sources.py` | `resolve-d-a-candidate-sources.yml` |
| Critical appraisal (limits L1–L4) | `docs/PART_B_CRITICAL_APPRAISAL_v1.md` | — |

Test coverage: `tests/test_part_b_*.py` and `tests/test_d_a_source_resolver.py`
(full suite green).

## Reproduce end to end

```text
# analysis (B1–B5) from committed inputs
python scripts/run_part_b_support.py \
  empirical/broad_reality_evidence/broad_route_records.csv \
  empirical/broad_reality_evidence/part_b_arrow_effects.csv \
  empirical/broad_reality_evidence/part_b_arrow_strata.csv \
  configs/part_b_moderator_hypotheses.json \
  configs/part_b_break_even_scenarios.json \
  artifacts/part_b_support

# honesty guard
python scripts/validate_part_b_integrity.py \
  empirical/broad_reality_evidence/part_b_arrow_effects.csv \
  empirical/broad_reality_evidence/d_A_candidate_scouting_v1.csv \
  empirical/broad_reality_evidence/d_A_moderator_coding_queue.csv

# candidate source feasibility (C3)
python scripts/resolve_d_a_candidate_sources.py \
  empirical/broad_reality_evidence/d_A_candidate_scouting_v1.csv \
  artifacts/d_a_source_receipts
```

All three are also runnable as GitHub Actions (`workflow_dispatch` or on the
matching PR paths).

## The single remaining step (human sign-off, by policy)

What is **not** automated is the verified numeric extraction: reading a resolved
full text, extracting the direct `A -> antagonism` estimate with its denominator
and uncertainty, confirming the trait is an independent predictor, judging
independence, and coding the moderator level with a cited basis. This is gated on
human sign-off by the repository's integrity contract ("query membership or
abstract co-mention is never an effect"), not by any technical limit. The
reproducible layers above take every lead right up to that step:

```text
scout candidates  ->  resolve DOI + access (CI)  ->  [HUMAN: verify + extract]  ->  queue -> pipeline (CI)
```

Once a verified effect is entered in `part_b_arrow_effects.csv` (or the d_A
moderator queue), rerunning the pipeline produces the updated B2 envelope / B3
verdict with no further code changes.

## What unblocks the first real result

Per B5, in priority order:

1. Two verified `d_A` clusters at each `pollination_generalization` level (leads
   resolved: Schiestl 2015, Caruso-mined, seed-predation, Parnassia, Aerides) ->
   first B3 conditionality verdict. Also register a `trait_class` (visual vs scent)
   moderator (appraisal L3).
2. A second independent cluster per arrow -> first B2 pooled envelope.
3. Declare the effect -> dimensionless-parameter scale bridge (appraisal L2) ->
   upgrades B4 from sensitivity to empirical, yielding the empirically informed
   regime map (the Part B headline).
