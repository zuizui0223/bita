# Biotic Interaction Trait Architecture

A manuscript repository for a route-based theory of when floral attraction and
defence/access traits become complementary or substitutable, with a linked
*Impatiens capensis* empirical case study and supporting route-level literature
evidence.

## Manuscript scope

The submission has three evidence layers with different inferential roles:

```text
1. Theory
   Derive the local A × D mixed partial and identify the route balance that switches
   attraction-defence regimes.

2. Impatiens empirical case study
   Test observable route components in one linked system while separating
   observational trait associations from randomized treatment effects.

3. Literature support
   Retain only verified route-level patterns as external context; do not estimate
   universal causal parameters from heterogeneous studies.
```

The repository is intentionally not a general archive of abandoned data-discovery
experiments. One-off probes, candidate-harvest pipelines, superseded queues, and
historical cleanup notes are removed once they are no longer required to reproduce the
current manuscript.

## Central result

The theoretical model predicts conditional rather than universal attraction-defence
relationships. Across the declared robustness grid, both complementary and
substitutable regimes occur, and the sign shifts with the balance between
antagonist-mediated benefit, pollination obstruction, and shared cost.

The *Impatiens* case study provides an asymmetric empirical anchor:

```text
- a floral-tannin candidate is associated with lower pollinator use;
- the same candidate is not resolved as protective against natural floral damage;
- randomized imposed florivory reduces chasmogamous fruit production.
```

These empirical results constrain parts of the route structure but do not estimate the
full theoretical mixed partial.

## Theory and robustness

Core files:

```text
theory/README.md
configs/part_i_robustness_grid.json
trait_architecture/model.py
trait_architecture/robustness.py
scripts/run_part_i_robustness.py
scripts/build_part_i_manuscript_readout.py
scripts/build_part_i_regime_figure_svg.py
docs/PART_I_ROBUSTNESS_PROTOCOL.md
docs/MANUSCRIPT_RESULTS_V2.md
.github/workflows/validate-current-theory-meta.yml
```

The declared sweep contains 162 local phenotype × interaction cases, four biological
parameter scenarios, and four predeclared functional-form variants, for 2,592 local
A × D mixed-partial evaluations. The generated theory figure reports theoretical grid
summaries, not empirical probabilities.

## Impatiens empirical core

The primary empirical case uses the title-validated *Impatiens capensis* Dryad archive.
Raw rows are retrieved at runtime and kept in memory; committed outputs are aggregate
model reports, audits, readouts, and figures.

Core files:

```text
docs/EMPIRICAL_PIVOT_IMPATIENS_V1.md
docs/IMPATIENS_RESULTS_LOCK_V1.md
docs/MANUSCRIPT_RESULTS_TABLES_V1.md
configs/impatiens_response_scale_models.json
configs/impatiens_randomized_fitness_models.json
trait_architecture/impatiens_response_scale_models.py
trait_architecture/impatiens_factorial_fitness_models.py
trait_architecture/impatiens_theory_bridge.py
trait_architecture/impatiens_channel_ledger_svg.py
.github/workflows/run-impatiens-empirical-core.yml
```

Inference is separated explicitly:

```text
Observational associations:
  flower redness / floral tannins -> pollinator use
  flower redness / floral tannins -> natural floral damage
  redness × tannins -> CH seed component

Randomized assignment contrasts:
  supplemental robbing × florivory × pollination -> CH fruit and seed components
```

## Literature support

The literature layer is supporting evidence, not the main result and not a universal
parameter calibration. The retained material focuses on verified route-level effects
and integrity checks.

Core files:

```text
empirical/broad_reality_evidence/PART_B_RESULTS_READOUT_v1.md
empirical/broad_reality_evidence/part_b_arrow_effects.csv
scripts/validate_part_b_integrity.py
.github/workflows/part-b-integrity.yml
```

Candidate-harvest workflows, repository-receipt probes, matched-flower discovery
pipelines, and superseded v0 evidence queues are outside the submission path and are
not retained as active implementation.

## Manuscript layer

Current writing files:

```text
docs/MANUSCRIPT_SKELETON_V1.md
docs/MANUSCRIPT_RESULTS_V2.md
docs/MANUSCRIPT_RESULTS_TABLES_V1.md
docs/IMPATIENS_RESULTS_LOCK_V1.md
```

Next writing targets are the Methods, Discussion, Figure 1 conceptual diagram, and
final abstract/title package.

## Claims not made

The manuscript does not claim:

```text
- causal effects of flower redness or floral tannins;
- resolved floral-tannin protection against natural damage;
- total lifetime fitness;
- an empirical estimate of the Part A mixed partial;
- calibration of c_AD;
- direct empirical observation of complementarity or substitutability;
- universal cross-species causal parameters.
```
