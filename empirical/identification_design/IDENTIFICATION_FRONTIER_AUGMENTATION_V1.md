# Identification frontier and minimum augmentation — v1

## Screened-set result

The current audit contains **17 high-information systems**. The strongest information modules are fragmented across different studies rather than accumulated in one design:

- direct A×D-like trait-factorial anchor: **1/17** (Kessler et al. 2008; systemic-D scope caveat);
- consumer-factorial anchor: **1/17** (Egan et al. 2021);
- randomized-context anchor around an observational A×D term: **1/17** (Soper Gorden & Adler 2018);
- selective-D system anchor: **1/17** (Sun & Huang 2015);
- manipulated A × antagonist-removal × pollination-supplementation bridge: **1/17** (Theis & Adler 2012);
- characterized `m0_delta`: **0/17**;
- independent joint-cost assay: **0/17**;
- full channel-allocation closure: **0/17**.

The five strongest frontier faces above are represented by **five different studies**. This is the empirical **design-fragmentation pattern**: sophisticated pieces of the target architecture already exist, including a three-factor attraction–consumer bridge, but they are distributed across systems.

Theis & Adler (2012) is especially informative because fragrance enhancement, repeated beetle removal, and supplemental hand pollination were crossed on female flowers. Hand pollination is not a pollinator-access toggle, so this remains a bridge rather than channel identification.

## Minimum-augmentation interpretation

No scalar distance is assigned. The relevant next step depends on the information face already occupied:

| anchor | current strength | minimum major augmentation | still required afterward |
|---|---|---|---|
| Kessler et al. 2008 | direct A×D-like trait factorial | resolve flower-specific D scope and add crossed selective G/P toggles to the existing A×D backbone | `m0_delta`; four-way separability; independent `kappa` assay |
| Egan et al. 2021 | consumer factorial | cross independently manipulable flower-specific A and D onto the existing consumer-factorial backbone | `m0_delta`; four-way separability; independent `kappa` assay |
| Soper Gorden & Adler 2018 | observational A×D + randomized context modification | randomize/cross valid A and D and replace intensity additions with selective G/P toggles | `m0_delta`; four-way separability; independent `kappa` assay |
| Sun & Huang 2015 | selective flower-associated D manipulation | add an independent attraction manipulation to the selective-D backbone | full A×D factorial; true selective G/P toggles; `m0_delta`; separability; independent `kappa` assay |
| Theis & Adler 2012 | manipulated A × beetle-removal × pollination-supplementation bridge | add a distinct flower-associated D and replace or complement hand pollination with a selective P-access toggle | full A×D factorial; `m0_delta`; four-way separability; independent `kappa` assay |

## Hierarchical bottleneck

The target design is not missing wholesale. Theis & Adler (2012) already crosses a manipulated attraction signal with an antagonist-removal treatment and a pollination-supplementation treatment; Kessler et al. (2008) supplies the strongest A×D-like trait factorial; Egan et al. (2021) supplies the strongest consumer-factorial backbone; and Sun & Huang (2015) supplies a selective-D mechanism. The bottleneck is their **intersection on valid A/D coordinates with selective consumer access and baseline/cost closure**.

`m0_delta` and independent `kappa` assays remain absent across the screened set, but they are downstream gates: many studies stop earlier because a distinct A/D factorial or target-style consumer access contrast is missing.

## Conditional partial-identification recovery from Kessler et al. 2008

The published rounded probability-scale interaction is `Delta_AD = +0.19 to +0.25`. For

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta,
```

an explicit same-scale restriction `kappa_delta >= 0` implies

```text
rho_delta - iota_delta >= Delta_AD W,
```

so within the published aggregate constraints

```text
rho_delta - iota_delta >= +0.19.
```

This is **not a confidence bound** because source-level factorial uncertainty is unrecovered. It is an assumption-indexed aggregate-constraint bound. A hidden synergistic joint channel would need magnitude at least 0.19 on that probability scale before the positive biotic balance could be erased at the lower end of the published range.

## Scientific consequence

> **Constituent channels recur, and multiple near-complete experimental modules already exist, but the modules occupy different studies. Mechanism allocation is blocked by design fragmentation rather than by absence of relevant biology.**

> **Reuse the strongest existing backbone and add the missing module that most shrinks the identified set.**

For Theis & Adler (2012), this means adding a distinct D coordinate and a true pollinator-access/baseline treatment to an existing A×G×pollination-supplementation backbone. For Kessler (2008), it means selective consumer interventions; for Egan (2021), valid crossed floral A/D coordinates; for *Pedicularis*, an independent attraction manipulation.

## Boundary

These counts describe the current **17-system high-information screen**, not literature prevalence. The augmentation labels are design recommendations derived from recorded blockers; they are not claims that the proposed additions are technically easy, uniquely optimal, or already validated. No study-specific `rho_delta`, `iota_delta`, or `kappa_delta` point values are inferred.
