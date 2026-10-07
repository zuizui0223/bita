# Clinger-state speciation-rate triage preregistration v1

Status: **FROZEN BEFORE CLINGER × SPECIATION-RATE ASSOCIATION IS OPENED**

Frozen on: 2026-10-07
Branch: `analysis/ecological-stability-evolutionary-transience-v1`

## Purpose

This is a triage test for the separately preregistered
`ECOLOGICAL_STABILITY_EVOLUTIONARY_TRANSIENCE_PREREG_V1.md`.

It does not replace the full state-history / dwell-time analysis across the Colwell/Rangel
tree ensemble. It asks whether an already published set of hummingbird tip-level
speciation-rate estimates contains the directional signal expected if the clinging /
unorthodox-feeding state is macroevolutionarily transient.

## Frozen sources

### Behavioural state

Colwell et al. 2023, *The American Naturalist*,
doi:10.1086/726036; Harvard Dataverse doi:10.7910/DVN/THDJCI.

Primary state definition is unchanged from the parent preregistration:

- state 1 = source-defined **clinger**, reconstructed from the four feeding-style
  columns that require clinging;
- state 0 = source-defined presumed non-clinger.

No state is inferred from the Barreto outcomes.

### Speciation-rate outcomes

Barreto et al. 2023, *Proceedings of the Royal Society B*,
doi:10.1098/rspb.2022.1793;
Figshare doi:10.6084/m9.figshare.22493044.v1.

The public processed table contains the following outcome columns:
- `DR McGuire`
- `DR BirdTree`
- `BAMM Lambda McGuire`
- `BAMM Lambda BirdTree`
- `Lambda ClaDS McGuire`
- `Lambda ClaDS BirdTree`

The source also provides `Group`, `BirdTree`, and `McGuire tree` indicators.

## Primary outcome and statistic

Primary outcome:

```text
Y = log(DR McGuire)
```

restricted to species with:
- a non-missing Colwell clinger state;
- `McGuire tree = 1`;
- finite positive `DR McGuire`.

Primary effect statistic:

```text
Delta_DR =
mean[log(DR McGuire) | clinger]
-
mean[log(DR McGuire) | non-clinger]
```

Prediction under evolutionary transience:

```text
Delta_DR < 0
```

### Primary null

Permute clinger labels **within Barreto's published Group categories**, preserving
the observed number of clingers within each group. This protects the primary test
against a signal generated only by broad hummingbird clade membership.

Use 99,999 fixed-seed permutations (seed 20261007) when every mixed-state group has
at least two species; otherwise enumerate exact within-group label assignments where
computationally feasible and use Monte Carlo only for the remainder.

One-sided primary p-value is the fraction of permuted `Delta_DR` values <= observed.
Also report the two-sided permutation p-value and do not hide it.

## Secondary outcomes

Apply the same joined species set, log transform, direction and group-stratified
permutation logic separately to:

1. `DR BirdTree`
2. `BAMM Lambda McGuire`
3. `BAMM Lambda BirdTree`
4. `Lambda ClaDS McGuire`
5. `Lambda ClaDS BirdTree`

These are robustness diagnostics, not five interchangeable primary endpoints.

## Prespecified descriptive effect sizes

For every outcome report:

- number of clingers and non-clingers;
- geometric mean in each state;
- geometric-mean ratio = clinger / non-clinger;
- unstratified Cliff's delta;
- group-stratified permutation p-values.

Do not promote an isolated secondary metric if the primary DR-McGuire direction fails.

## Frozen sensitivities

### S1 — remove Coquettes

Repeat the primary test after excluding Barreto `Group = Coquettes`, because Colwell
identified the clearest deep clinging origin in this clade.

### S2 — direct name matches only

Primary analysis uses only exact normalized binomial name matches between Colwell and
Barreto. No post-outcome synonym reconciliation is allowed into the primary result.

A later taxonomic-reconciliation analysis may be reported as sensitivity only.

### S3 — clinger definition audit

The primary state is the source clinger classification. A narrower robbery-capable
state may be reconstructed later from the source feeding-mode columns, but it cannot
replace the primary state after outcomes are opened.

## Triage decision rule

The full 3000-tree state-history analysis remains worth pursuing as a leading
hypothesis only if:

1. `Delta_DR < 0` for the McGuire DR primary endpoint;
2. the same direction survives removal of Coquettes; and
3. at least three of the five secondary rate estimates are also lower in clingers.

The permutation p-value is evidence strength, not a binary gate by itself.

If the primary direction is >= 0, mark the speciation-rate version of the transience
hypothesis as falsified at triage and do not rescue it by selecting BAMM, ClaDS,
BirdTree, taxonomic remapping, or a different clinger definition.

## Claim ceiling

Even a supported result would show an association between a repeated behavioural state
and published tip-level speciation-rate estimates. It would not by itself demonstrate
state-dependent extinction, causal effects of robbery, or evolutionary dwell time.

Allowed if supported:

> Repeated evolution of unorthodox feeding is associated with lower tip-level
> speciation rates across broad hummingbird clades, consistent with ecological
> innovation that is macroevolutionarily transient.

Prohibited:
- `clinging causes extinction`;
- `cheating universally lowers diversification`;
- treating a tip-rate association as the full state-dependent diversification model.
