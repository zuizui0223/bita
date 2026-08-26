# Identification frontier and minimum augmentation — v1

## Screened-set result

The current audit contains **16 high-information systems**. The strongest information modules are fragmented across different studies rather than accumulated in one design:

- direct A×D-like trait-factorial anchor: **1/16** (Kessler et al. 2008; systemic-D scope caveat);
- consumer-factorial anchor: **1/16** (Egan et al. 2021);
- randomized-context anchor around an observational A×D term: **1/16** (Soper Gorden & Adler 2018);
- selective-D system anchor: **1/16** (Sun & Huang 2015);
- characterized `m0_delta`: **0/16**;
- independent joint-cost assay: **0/16**;
- full channel-allocation closure: **0/16**.

The first four anchor classes are represented by **four different studies**. This is the empirical **design-fragmentation pattern**: the literature already contains much of the necessary biology and several sophisticated experimental modules, but those modules are distributed across systems.

This is more informative than reporting only `0/16 full identification`. It says where the information already exists and which existing designs are worth extending.

## Minimum-augmentation interpretation

No scalar distance is assigned. The relevant next step depends on the information face already occupied:

| anchor | current strength | minimum major augmentation | still required afterward |
|---|---|---|---|
| Kessler et al. 2008 | direct A×D-like trait factorial | resolve flower-specific D scope and add crossed selective G/P toggles to the existing A×D backbone | `m0_delta`; four-way separability; independent `kappa` assay |
| Egan et al. 2021 | consumer factorial | cross independently manipulable flower-specific A and D onto the existing consumer-factorial backbone | `m0_delta`; four-way separability; independent `kappa` assay |
| Soper Gorden & Adler 2018 | observational A×D + randomized context modification | randomize/cross valid A and D and replace intensity additions with selective G/P toggles | `m0_delta`; four-way separability; independent `kappa` assay |
| Sun & Huang 2015 | selective flower-associated D manipulation | add an independent attraction manipulation to the selective-D backbone | full A×D factorial; true selective G/P toggles; `m0_delta`; separability; independent `kappa` assay |

The important point is that these are different experimental backbones. A new study does not necessarily need to start from zero: it can reuse the strongest existing module and add the missing one.

## A hierarchical bottleneck appears

Only one screened system reaches the direct A×D-like trait-factorial layer, and even that system has a D-scope caveat. Conversely, the strongest consumer-factorial design lacks a valid crossed floral A/D pair. Thus the immediate bottleneck is not simply “collect more consumer data.” It is the **intersection of biologically valid trait coordinates and selective consumer interventions on the same outcome surface**.

`m0_delta` and independent `kappa` assays are absent in all 16 screened systems, but these are downstream gates: most studies stop before reaching the point at which those quantities would complete an otherwise identified A×D channel design.

## Conditional partial-identification recovery from Kessler et al. 2008

The published rounded probability-scale interaction is

```text
Delta_AD = +0.19 to +0.25.
```

For the accounting relation

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta,
```

an explicit same-scale restriction `kappa_delta >= 0` implies

```text
rho_delta - iota_delta >= Delta_AD W.
```

Therefore, **conditional on the published rounded interaction range and on `kappa_delta >= 0`**, the biotic balance is bounded below by

```text
rho_delta - iota_delta >= +0.19.
```

This is **not a confidence bound**. The source-level factorial SE/CI is unrecovered, and `kappa_delta >= 0` is an explicit auxiliary restriction rather than an empirical result. The statement is an aggregate-constraint partial-identification consequence.

The equivalent break-even view is useful. A hidden synergistic joint channel would need magnitude at least equal to the positive total interaction before it could erase the positive biotic balance. Across the published rounded probability-scale range, the break-even `kappa_delta` threshold is approximately

```text
-0.19 to -0.25.
```

Again, this is a sensitivity threshold, not a sampling interval.

## What the other anchors add

### Egan et al. 2021

The key asset is not a trait-interaction estimate but an existing consumer-factorial backbone. The minimum scientifically meaningful augmentation is therefore to add independently manipulable, flower-specific attraction and defence coordinates rather than to repeat another consumer experiment.

### Soper Gorden & Adler 2018

The public data demonstrate that randomized ecological context can modify an observational A×D term, but all eight targeted HC3 intervals cross zero and the treatments are interaction-intensity additions rather than selective consumer exclusions. More regression cannot turn this dataset into channel identification. The next information gain requires a new trait/intervention design.

### Sun & Huang 2015

The water-holding bract manipulation is useful because it demonstrates plausible consumer selectivity. The missing module is attraction: add an independent A manipulation before attempting a full crossed consumer experiment.

## Scientific consequence

The cross-system synthesis can now be stated more precisely:

> **Constituent channels recur, and the strongest experimental modules already exist, but the modules occupy different studies. Mechanism allocation is therefore blocked by design fragmentation rather than by absence of relevant biology.**

The practical synthesis is:

> **Reuse the strongest existing backbone and add the missing module that most shrinks the identified set.**

For a trait-factorial backbone this means selective consumer interventions; for a consumer-factorial backbone it means biologically valid crossed floral A/D coordinates; for a selective-D backbone it means an independent attraction manipulation. `m0_delta`, separability and independent joint-cost evidence remain downstream gates rather than reasons to discard those existing backbones.

## Boundary

These counts describe the current **16-system high-information screen**, not literature prevalence. The augmentation labels are design recommendations derived from the recorded blockers; they are not claims that the proposed additions are technically easy, uniquely optimal, or already validated in the named systems. No study-specific `rho_delta`, `iota_delta`, or `kappa_delta` point values are inferred.
