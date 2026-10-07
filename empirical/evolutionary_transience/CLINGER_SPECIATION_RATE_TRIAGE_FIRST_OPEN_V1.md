# Clinger-state speciation-rate triage first-open result v1

Status: **DIRECTIONAL SIGNAL ONLY — NOT PROMOTED**

Source-state correction:
`COLWELL_FEEDING_STATE_CODING_CORRECTION_V1.md`

Preregistration:
`CLINGER_SPECIATION_RATE_TRIAGE_PREREG_V1.md`

Re-run with authoritative source coding: 2026-10-07

## Source state counts

The authoritative Colwell `Feeding style code` exactly reproduces the published
categories:

```text
clinger (codes 1–5)           = 66
on-wing piercer (code 6)      = 10  [excluded from binary contrast]
presumed non-clinger (code 7) = 144
```

Exact normalized Colwell × Barreto join: 169 species.

## Primary McGuire-DR result

Among species with a McGuire-tree rate:

```text
n = 159
clinger = 62
non-clinger = 97

geometric mean DR:
clinger     = 0.11445
non-clinger = 0.12867

clinger / non-clinger ratio = 0.88952
Delta log(DR) = -0.11707
Cliff's delta = -0.06967
```

Thus the raw direction is the preregistered direction: clingers have approximately
11% lower tip-level DR.

However, after preserving the observed number of clingers within each published
Barreto `Group` and permuting state labels only within groups:

```text
one-sided p = 0.36219
two-sided p = 0.36692
```

The observed difference is therefore not unusual relative to the broad-clade placement
of clingers.

## Frozen sensitivity: remove Coquettes

```text
n = 123
clinger = 35
non-clinger = 88

geometric mean DR:
clinger     = 0.11920
non-clinger = 0.12333

ratio = 0.96651
Delta log(DR) = -0.03406
Cliff's delta = -0.00455

group-stratified one-sided p = 0.86411
two-sided p = 0.90290
```

The sign remains negative but nearly all magnitude disappears.

## Secondary published rate estimates

All five secondary estimates are lower in clingers:

```text
DR BirdTree:
ratio = 0.93695
Delta log = -0.06513
group-stratified p(one-sided) = 0.40332

BAMM Lambda McGuire:
ratio = 0.92046
Delta log = -0.08288
p = 0.17219

BAMM Lambda BirdTree:
ratio = 0.99228
Delta log = -0.00775
p = 0.00771

Lambda ClaDS McGuire:
ratio = 0.90261
Delta log = -0.10247
p = 0.09508

Lambda ClaDS BirdTree:
ratio = 0.94908
Delta log = -0.05226
p = 0.19930
```

The preregistered directional triage rule is formally met:
- primary direction lower: YES;
- direction survives removal of Coquettes: YES;
- >=3/5 secondary outcomes lower: YES (5/5).

But the stronger biological interpretation is **not** promoted because:
1. the primary within-group null is not rejected;
2. removing Coquettes collapses the primary effect to ~3%;
3. one isolated secondary p-value cannot replace the frozen primary endpoint.

## Interpretation

The data are compatible with, but do not establish, lower speciation in clingers.

The most defensible readout is:

> The apparent lower tip-level speciation rate of clinging hummingbirds is largely
> explained by where clingers occur among broad hummingbird clades, especially the
> Coquette-rich state distribution, rather than by a strong within-clade clinger
> effect.

This weakens a simple state-dependent-diversification explanation for Colwell's
tip-heavy repeated origins.

## Next inference target

Do not optimize another speciation metric.

The unresolved non-obvious question is instead why a repeatedly acquired behavioural
innovation is so often tip-localized if it is not associated with a strong general
reduction in tip-level speciation rate.

The next route must discriminate among:
- high gain + high reversal (behavioural transience);
- repeated recent gain with insufficient time for diversification;
- ascertainment bias in documented clinging;
- clade-specific origin processes;
- morphology/behaviour decoupling after state acquisition.

A direct state-transition / dwell-time analysis across the phylogenetic ensemble is
the appropriate next test; tip-level speciation-rate fishing is closed.
