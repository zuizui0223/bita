# Submission scope — BITA access-routing Letter

Primary forward route: **Ecology Letters — Letter**.

Primary manuscript:

`manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`

## Canonical question

> **When legitimate access becomes more constrained, does exploitation simply decline, or does it reroute toward bypass?**

## 1. Primary prediction

```text
access mismatch increases
        ->
legitimate route becomes less usable
        ->
if bypass remains available:
bypass / robbing propensity increases
```

The prediction is ordinal and does not require one common mechanistic coefficient across taxa.

## 2. Primary empirical test — Ecuador birds

```text
n = 1,378 bird × plant × site units
18 Ecuador sites
barrier robbery     = 0.30698
accessible robbery  = 0.08139
difference          = +0.22560
global mismatch rho = 0.41826
site-adjusted rho   = 0.3505
within-site permutation p = 0.0001
15 / 17 comparable sites in same direction
min >= 5 interactions:
  n = 702
  difference = +0.264
  rho = 0.505
  p = 0.0001
```

This is an observational all-Ecuador extension, not an exact replication of the source three-transect GLMM.

## 3. Independent corroboration — Sakhalkar insects

```text
n = 57 plant species
rho = 0.346786
permutation p = 0.0086
full multitrait model p = 0.2016
tube-length block p = 0.2110
```

The licensed claim is access-geometry association, not a unique causal tube-length effect.

## 4. Joint network test

```text
r_A = 0.3505
r_S = 0.3468
equal-network Fisher-z rho_J = 0.3487
joint permutation p = 0.0001
independent network contributions k = 2
```

Raw observations are never pooled. The joint test does not estimate between-network heterogeneity, a population mean across networks, or generality beyond the two systems.

Both analyses are observational and are not pooled onto one effect scale.

## 5. Third independent network priority

The current (k=2) ceiling is now the highest-priority unresolved scientific limit.

A confirmatory third-network protocol is frozen in:

- `empirical/floral_defence_selectivity/THIRD_ACCESS_ROUTING_NETWORK_PREREG_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CANDIDATE_REGISTRY_V1.csv`

The third network must be an independently sampled **non-Insecta / non-Aves** visitor fauna and recover the same predeclared estimand:

~~~text
greater legitimate-route access constraint
        ->
greater bypass / robbing propensity
~~~

Dataset selection cannot use the observed outcome direction. Candidates whose relevant outcome direction was already exposed are permanently excluded from the confirmatory lane.

Until a third eligible network is found and tested under the frozen protocol:

~~~text
JOINT_NETWORK_K = 2
K3_GENERALITY_TEST = PREREGISTERED_PENDING_DATASET
K3_GENERALITY_TEST = PENDING_OUTCOME_BLIND_DATASET
~~~

## 6. Mechanistic context only

The broader floral-defence evidence package remains useful for interpretation:

```text
17 unique D-side study programs
10 same-defence pollinator follow-ups
8 independent within-D state-switch systems
```

Matched effective-domain classifications are author-coded and have not yet undergone outcome-blind independent recoding. They are therefore not treated as independent validation in the Letter, and the 11/11 state alignment is not a headline or confirmatory result.

These counts describe evidence structure, not natural prevalence, and they are not pooled into one grand meta-analytic effect.

## 7. Required claim boundaries

Do not claim:

- either network establishes causality;
- Sakhalkar uniquely identifies tube length;
- the two networks estimate a universal effect;
- `k=2` demonstrates network-wide generality;
- source-audited domain coding is independently validated;
- matched-domain alignment estimates prevalence or a confirmatory success rate;
- the access-routing result identifies evolutionary origin of floral barriers.

## 8. Ecology Letters initial-submission archive gate

Before external upload, deposit the CI-built analysis-data/code archive in a DOI-bearing repository.

Required archive contents:

~~~text
57-row anonymous Sakhalkar species analysis table
1,378-row anonymous Aubert/EPHI pair-site analysis table
column metadata
exact reproduction code
frozen aggregate outputs
repository commit receipt
~~~

The archive DOI must appear in the manuscript Data accessibility statement and title page. Public source DOIs alone do not replace this submission-stage archive.

Current state:

~~~text
ARCHIVE_STAGING = READY
ARCHIVE_DOI = REQUIRED
~~~

## 9. Preserved reserve papers

Extended Synthesis:

- `manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md`
- `manuscript/CLAIM_FREEZE_MACRO_V0.md`
- `submission/ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_V0.md`
- `submission/FUNCTIONAL_ECOLOGY_ADAPTATION_V0.md`

Mechanism-identification foundation:

The preserved inference principle remains `trait interaction != ecological mechanism`; it constrains interpretation but is not the Letter headline.
The mechanism-identification manuscript is preserved support and is no longer the primary submission identity.

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- `manuscript/CLAIM_FREEZE.md`

## 10. Current state

```text
PRIMARY_FORWARD_PAPER = ACCESS_ROUTING_LETTER
PRIMARY_DATASET = AUBERT_EPHI_ALL_ECUADOR
INDEPENDENT_CORROBORATION = SAKHALKAR_INSECTS
JOINT_NETWORK_K = 2
EXTENDED_SYNTHESIS = PRESERVED_RESERVE
REPRODUCIBLE_ANALYSES = READY
LETTER_PACKAGE = READY
DATA_CODE_ARCHIVE = STAGING_READY_DOI_REQUIRED
AUTHOR_CONTROLLED_METADATA = REQUIRED
EXTERNAL_SUBMISSION = BLOCKED_PENDING_DOI_AND_AUTHOR_FIELDS
```
