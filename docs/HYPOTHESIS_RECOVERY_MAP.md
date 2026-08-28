# Original-hypothesis recovery map

## Audit conclusion

The repository history contains two different scientific targets.

1. The original one-trait target asks how changing one attraction/display trait affects pollinator benefit, antagonist cost, and plant reproduction.
2. The canonical BITA target asks how an attraction trait `A` and a distinct antagonist-reducing trait `D` interact, and what observations identify the allocation of `Delta_AD W` among channels.

The first target was not recovered by the second. Its evidence remained in the repository, but its role was reduced to background, constituent recurrence, or historical quantitative context.

## Where the one-trait hypothesis remains

### 1. Introduction-level motivation

`manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` states that floral colour, scent, display and reward can attract pollinators while exposing flowers to florivores, seed predators and nectar robbers. In the canonical paper this is motivation, not the estimand.

### 2. The 13 attraction-side clusters

The canonical route table contains:

```text
A_to_pollination: 5 independent clusters
A_to_antagonism:  8 independent clusters
```

These are the empirical substrate of the one-trait question. In BITA they are explicitly classified as constituent routes and prohibited from estimating `Delta_AD W`, `rho_delta`, `iota_delta`, or `kappa_delta`.

### 3. Sasidharan et al. 2023

`empirical/mechanism_pattern_synthesis/SASIDHARAN_2023_REPRO_READOUT_V1.md` reports a current-deposit florivore-minus-pollinator physiological-detection difference of about `+0.129`, positive in 32/32 leave-one-component-out refits, and recurrent shared attraction with rarer shared repulsion. The same file also records the decisive limits: the contrast is assembled across studies, only three study components contain paired physiological data for both roles, and it is not a causal within-study role effect.

The canonical README now labels this as a reproducible historical analysis rather than Main identification evidence. That is correct for the two-trait paper and confirms that the module was not used to recover the one-trait hypothesis.

## Current two-trait estimand

The active manuscript is `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`. Its primary estimand is

```text
Delta_AD W = W11 - W10 - W01 + W00.
```

The 16-system audit asks about a much stronger design intersection: crossed A/D traits, selective antagonist and pollinator interventions, pollinator-absent baseline characterization, and an independent joint-channel assay. The 56 route records from 25 clusters establish recurrence only.

## Necessary correction to the recovery diagnosis

Moving from two traits back to one removes the cross-trait allocation problem, but it does not make channel allocation automatic. In general,

```text
Delta_A W = Delta_A M - Delta_A G - Delta_A C.
```

The one-trait contrasts `Delta_A M` and `Delta_A G` can be estimated separately, and their biotic balance computed, under a **weaker design** that measures or intervenes on both channels on the same `A` contrast. This does not require `D`, an `A x D` interaction, or the BITA 16-cell design. Selective intervention is one route to causal channel estimates but is deliberately not a requirement for the initial coverage count. Total `W(A)` alone still cannot separate the terms, and direct attraction cost must be standardized or measured before using `S_A = Delta_A M - Delta_A G`.

## Repository boundary

| Lane | Scientific role | Canonical status |
|---|---|---|
| `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` | two-trait interaction and mechanism identification | active BITA submission |
| `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md` | historical theorem-led A-by-D synthesis | provenance only |
| `empirical/mechanism_pattern_synthesis/` | source-adjudicated route and historical quantitative evidence | retained dependency/evidence layer |
| [SCH](https://github.com/zuizui0223/sch) | fail-closed one-trait coverage audit and shared-cue paper framework | separate repository; not in BITA submission |

No existing BITA result is deleted or reclassified upward. SCH imports frozen ledger tables with hashes and links to preserved BITA evidence under its original source and claim ceilings.
