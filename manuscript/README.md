# Manuscript directory

## Canonical manuscript

`MANUSCRIPT_IDENTIFICATION_DESIGN.md` is the sole active submission manuscript source.

The historical `MANUSCRIPT_THEORETICAL_ECOLOGY.md` remains versioned for provenance only; it does not define the current paper or submission package.

The original first-order shared-cue question is also kept outside this submission mainline. Its coverage audit and paper framework now belong to the separate [SCH repository](https://github.com/zuizui0223/sch). That transfer does not change the estimand or claim ceiling of the canonical BITA manuscript.

## Sister-paper / Chapter 2 position

BITA is the mechanistic second chapter of a two-paper floral conflict programme.

- **SCH / Chapter 1 — one trait, dual audience.** For one attraction/display coordinate `A`, ask whether pollinators and antagonists track the same cue and whether the resulting first-order attraction–antagonism conflict can be escaped. Its natural estimands are `M_A`, `G_A`, and `S_A = M_A - G_A`; it does not require a second trait `D` or an attraction-by-defence interaction.
- **BITA / Chapter 2 — two traits, mechanism allocation.** Introduce a distinct antagonist-reducing trait `D` and ask whether defence changes the reproductive return to attraction, whether that change is large enough to release a non-beneficial attraction effect, and which biological channel generated the observed `A×D` interaction.

The chapter transition is therefore

```text
SCH:  A -> pollinator benefit and antagonist exposure
          |
          v
      Is the one-trait conflict shared, separable, or evolvable?

BITA: add D as a candidate escape route
          |
          v
      Does D improve the return to A, does it cross the release threshold,
      and can the resulting A×D interaction be allocated to mechanism?
```

This division prevents duplicate publication claims. SCH owns shared-cue overlap, one-trait trade-off/evolvability, cue modularization and historical shared-to-private transitions. BITA owns two-trait interaction relief, functional constraint release, partial/point identification of antagonist-relief and pollinator-interference channels, the crossed consumer design, and the independent joint-cost assay. BITA may cite the one-trait problem as motivation but must not claim that an `A×D` interaction demonstrates cue privatization or historical signal evolution.

Reader-facing framing should therefore present BITA as a conditional escape-route paper: **given a floral attraction axis that can carry both mutualist benefit and antagonist exposure, when can adding defence restore the reproductive return to attraction, and what experiment identifies why?**

## Current paper architecture

The canonical paper is an explicit **Mechanism → Pattern → Identification** synthesis with a partial-identification middle layer:

```text
1. measure the discrete A×D interaction
2. represent compatible channel allocations as an identified set
3. shrink that set with explicit biological bounds / partial measurements
4. establish cross-system recurrence of the constituent ecological channels
5. audit which identification dimensions existing studies already cover
6. use selective A×D×antagonist×pollinator interventions for point identification
7. validate any remaining joint channel with an independent cost assay
```

The central algebra is

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

and, for `Delta_AD W = delta`, the total interaction alone defines

```text
I(delta) = {(rho, iota, kappa): rho - iota - kappa = delta}.
```

A key recoverable partial-identification statement is

```text
kappa_delta >= 0
=> rho_delta - iota_delta >= Delta_AD W.
```

This is an assumption-indexed bound on the biotic balance, not a universal theorem. Point identification requires selective channel interventions, explicit handling of `m0_delta`, a successful `A×D×G×P` separability diagnostic, and independent evidence for the joint-cost channel.

## Mechanism → Pattern result

The retained recurrence synthesis contains 56 route records across 25 independent biological clusters and covers all four constituent marginal pathway families. These records establish recurrence capacity, not natural prevalence or channel-interaction magnitudes.

The 16-system high-information audit is interpreted as a **fragmented identification frontier**. Kessler 2008, Egan 2021, *Impatiens capensis*, and *Pedicularis rex* occupy complementary design faces; no screened system closes all dimensions. Thus existing biology is not absent—the information needed for mechanism allocation is distributed across different experiments.

## Main figures

1. Figure 1 — a total A×D interaction defines an identified set rather than a unique mechanism.
2. Figure 2 — the 16-cell crossed consumer design and four-way separability diagnostic.
3. Figure 3 — independent joint-cost assay versus the unallocated residual.
4. Figure 4 — constituent-channel recurrence plus the fragmented identification frontier.
5. Figure 5 — executable roadmap from interaction detection through partial to point identification.

## Supporting Information

`manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md` is the active Appendix S1. It retains the detailed identified-set projection algebra, Kessler reconstruction, *Impatiens* retrofit, 16-system audit, 56/25 recurrence details, and the historical 2,592-grid / 77.2% technical sensitivity material.

## Current package state

Validated pre-metadata package:

```text
Main Document: 29 pages
Appendix S1:   12 pages
Main figures:   5
```

All 41 pages have been visually inspected. Remaining external-submission work is author-controlled metadata/sign-off followed by one exact rebuild and final page-by-page QA.
