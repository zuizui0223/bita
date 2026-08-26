# Final submission audit — identification-design canonical state

## Audit purpose

This is the live scientific and submission audit for the canonical paper:

> **From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence**

Primary target: **Ecology — Concepts & Synthesis**.

The governing scientific claim is not a one-sided theorem. It is an **identification framework** joined to a bounded Mechanism → Pattern synthesis.

## 1. Scientific spine

For two experimentally meaningful levels of attraction (`A`) and defence (`D`), the primary estimand is

```text
Delta_AD W = W11 - W10 - W01 + W00
```

A total attraction-by-defence interaction can be measured while the ecological channels generating it remain unidentified.

The proposed general experiment crosses:

```text
A × D × antagonist access × pollinator access
```

for 16 cells. Channel interpretation requires selective consumer interventions and comparable A/D coordinates across all cells.

The design also includes its own structural check: pollinator-dependence of the antagonist-relief contrast and antagonist-dependence of the pollinator-increment contrast are the same `A×D×G×P` four-way interaction up to sign. A non-zero four-way contrast therefore rejects the simple separable-channel representation.

Pollinator-independent reproduction is measured or justified through `m0_delta`. The residual

```text
U_delta = rho_delta - iota_delta - Delta_AD W
```

remains unallocated. It is not defined as kappa. A joint construction/allocation cost requires a separate A×D assay under standardized or suppressed biotic channels.

The algebra is used only after measurement as a consistency/sign diagnostic for any still-unallocated joint channel.

## 2. Mechanism → Pattern bridge

The retained source-adjudicated synthesis contains:

```text
56 route records
25 independent biological clusters
A -> pollination: 5
A -> antagonism:  8
D -> antagonism: 18
D -> pollination: 10
same-system:      14
context switches: 17
```

These categories overlap. They establish that the constituent ecological channels recur across systems; they do not estimate natural prevalence, `Delta_AD W`, `rho_delta`, `iota_delta`, or `kappa_delta`.

The stricter identification audit contains 16 high-information systems. Current fixed result:

```text
independent joint-cost assay:       0
full rho/iota/kappa identification: 0
```

Thus the integrated cross-system conclusion is:

> **The constituent channels recur, but their joint allocation remains unidentified.**

## 3. Existing-data anchors

- **Kessler et al. 2008:** closest trait-factorial anchor; positive discrete reproductive interaction across published aggregate constraints, with unresolved formal uncertainty and systemic-nicotine scope caveat.
- **Egan et al. 2021:** complementary consumer-factorial anchor; no independently manipulated floral A×D pair.
- **Impatiens capensis:** observational A×D plus randomized interaction-treatment modification; all eight target HC3 intervals cross zero; context modification is estimable, channel identification is not.
- **Pedicularis rex:** demonstrates a plausible selective-access physical-defence system, but lacks an independent attraction manipulation.

## 4. Historical analyses retained but demoted

The 2,592 finite evaluations and 77.2% selectivity-window precision remain in Appendix S1 as implementation/model-family sensitivity only. They are not empirical validation or natural-regime frequencies.

Leal and Sasidharan quantitative modules remain reproducible for provenance and possible companion work, but are not Main identification evidence.

The historical theorem-led manuscript remains versioned and is not the canonical submission source.

## 5. Inference boundaries

The active paper preserves:

```text
marginal route recurrence
!= total A×D interaction
!= channel interaction
!= full mechanism allocation
```

Therefore:

- route counts are not prevalence;
- finite-grid fractions are not prevalence;
- marginal A→P / A→G / D→G / D→P evidence does not estimate rho/iota;
- randomized context modification is not selective consumer exclusion;
- `U_delta` is not kappa by definition;
- zero independent joint-cost assays does not imply kappa = 0;
- a non-zero four-way interaction is evidence against separability rather than a nuisance term to absorb.

## 6. Reader-facing and visual QA

Current canonical pre-metadata package:

```text
Main Document: 29 pages
Appendix S1:   11 pages
Main figures:   5
```

Validation state:

- CI — PASS on Python 3.10 / 3.11 / 3.12;
- submission-scope — PASS;
- identification candidate build — PASS;
- canonical Ecology build — PASS;
- Fig1–Fig5 EPS export — PASS;
- full-page visual QA — PASS on all 29 Main + 11 Appendix pages;
- Figure 4 recurrence/identification panel — readable at review-page scale;
- `Theorem 1` and 77.2% headline — absent from Main;
- 2,592 / 77.2% — Appendix technical material only.

## 7. Current submission decision

**Science: GO. Reader-facing repository-source QA: PASS. External submission: pending human-controlled metadata/sign-off.**

Remaining blockers:

1. final author order/publication names and affiliations;
2. corresponding author/e-mail and ORCIDs;
3. final CRediT roles;
4. funding, acknowledgments, and competing-interest statement;
5. repository/software/data licence statement where applicable;
6. reviewer information only if requested by the portal;
7. all-author approval and no-simultaneous-submission confirmation;
8. final post-metadata package rebuild and page-by-page visual QA.

The governing rule is now: **preserve the distinction between recurrent biological ingredients and identified channel allocation while keeping the paper operationally executable.**