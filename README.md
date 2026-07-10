# Biotic Interaction Trait Architecture

A theory-to-evidence manuscript project on when floral attraction and floral
defence/access traits become complementary, substitutable, or empirically
unresolved.

## Current manuscript claim

The project is no longer trying to force a universal pooled four-arrow meta-analysis.
The current manuscript structure is:

```text
Part A: formal conditional attraction-defence theory
Part B: literature evidence map and evidence-gap audit
Part C: Impatiens capensis response-scale empirical case study
Part D: synthesis and future empirical design
```

The central empirical result is asymmetric:

```text
The floral-tannin candidate in Impatiens is associated with lower pollinator use,
but it is not resolved as protective against natural floral damage. Separately,
randomized imposed florivory reduces chasmogamous fruit production.
```

This is a case-study constraint on the theory, not a direct empirical proof of
complementarity, substitutability, a total-fitness mixed partial, or `c_AD`.

## Formal framework

For floral attraction/access traits `A` and defence/access-restriction traits `D`,
the target is a conditional regime map rather than a universal trade-off:

```text
biotic interaction regime -> expected attraction-defence relationship
```

The qualitative theory asks how the sign of the attraction-defence interaction
depends on:

```text
A -> pollinator benefit
A -> antagonist exposure
D -> pollinator cost
D -> antagonist suppression
shared A × D cost
```

Key theory files:

```text
docs/PART_I_ROBUSTNESS_PROTOCOL.md
configs/part_i_robustness_grid.json
trait_architecture/robustness.py
scripts/run_part_i_robustness.py
```

## Literature evidence map

The literature route is now an evidence map and generalisation boundary. Broad
searches, route screens, and source audits show that directly comparable effect
estimates are sparse and heterogeneous. The clearest cross-study support remains a
`D -> pollinator use` cost-like direction in some chemical-barrier systems, while
other routes are not yet poolable as universal parameters.

Important boundaries:

```text
Query membership is not an effect.
Abstract co-mention is not a route estimate.
Selection gradients are not automatically trait -> antagonist effects.
Effects are pooled only inside compatible trait/outcome/metric/design strata.
```

Key evidence-map files:

```text
empirical/broad_reality_evidence/PART_B_RESULTS_READOUT_v1.md
empirical/broad_reality_evidence/D_A_PUBLIC_C4_READOUT_V1.md
empirical/broad_reality_evidence/D_A_CARUSO_PRIMARY_INDEX_READOUT_V1.md
empirical/broad_reality_evidence/D_A_TROLLIUS_ROUTE_READOUT_V1.md
empirical/broad_reality_evidence/D_A_SEEDPRED_ROUTE_READOUT_V1.md
empirical/broad_reality_evidence/D_A_PHLOX_ABSTRACT_READOUT_V1.md
empirical/broad_reality_evidence/d_A_candidate_scouting_v1.csv
scripts/validate_part_b_integrity.py
.github/workflows/part-b-integrity.yml
```

## Impatiens empirical core

The primary empirical product is the title-validated `Impatiens capensis` Dryad
archive. Raw rows are retrieved at runtime and kept in memory; repository outputs are
aggregate audits, model reports, readouts, and figures.

The empirical core separates observational trait-channel associations from
randomized downstream treatment effects:

```text
Observational:
  early flower redness / floral tannins -> pollinator use
  early flower redness / floral tannins -> natural floral damage
  redness × tannins -> CH seed component

Randomized:
  supplemental robbing × florivory × pollination -> CH fruit and seed components
```

Key empirical files:

```text
docs/EMPIRICAL_PIVOT_IMPATIENS_V1.md
docs/IMPATIENS_RESULTS_LOCK_V1.md
docs/MANUSCRIPT_RESULTS_V1.md
docs/MANUSCRIPT_RESULTS_TABLES_V1.md
configs/impatiens_response_scale_models.json
configs/impatiens_randomized_fitness_models.json
trait_architecture/impatiens_response_scale_models.py
trait_architecture/impatiens_factorial_fitness_models.py
trait_architecture/impatiens_theory_bridge.py
trait_architecture/impatiens_channel_ledger_svg.py
.github/workflows/run-impatiens-empirical-core.yml
```

## Manuscript writing layer

The writing layer is intentionally locked to current results. It should not add new
hypotheses, parameters, or claims beyond the result lock.

Current writing files:

```text
docs/CURRENT_REVIEW_AND_CLEANUP_PLAN_V1.md
docs/MANUSCRIPT_SKELETON_V1.md
docs/MANUSCRIPT_RESULTS_V1.md
docs/MANUSCRIPT_RESULTS_TABLES_V1.md
```

Next writing targets:

```text
1. Methods v1 for theory, evidence map, and Impatiens models.
2. Discussion v1 using the asymmetric Impatiens result.
3. Figure/table polish.
```

## Claims not made

The current project does **not** claim:

```text
causal effects of flower redness or floral tannins;
resolved floral-tannin protection against natural damage;
total lifetime fitness;
an empirical Part A mixed partial;
calibration of c_AD;
direct observation of complementarity or substitutability;
universal cross-species parameter estimates.
```

## Cleanup policy

One-off exploratory source-probe workflows can be retired once their outcomes are
converted into readouts or the manuscript path no longer uses them. Do not delete
Impatiens empirical-core code, Part A theory code, Part B integrity guards, or source
readouts that justify stopping decisions.
