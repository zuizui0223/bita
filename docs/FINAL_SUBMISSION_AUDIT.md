# Final submission audit — partial-identification canonical state

Primary target: **Ecology — Concepts & Synthesis**

Canonical paper:

> **From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence**

The governing contribution is an ecological identification framework joined to a bounded Mechanism → Pattern synthesis. The algebra is not sold as mathematical novelty.

## 1. Scientific spine

Primary measurable interaction:

```text
Delta_AD W = W11 - W10 - W01 + W00
```

Channel bookkeeping:

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

If only `Delta_AD W = delta` is observed, channel allocation belongs to

```text
I(delta) = {(rho, iota, kappa): rho - iota - kappa = delta}.
```

Thus total-interaction estimation does not point-identify mechanism, but additional information can **partially identify** it. The central recovered bound is

```text
kappa_delta >= 0
=> rho_delta - iota_delta >= Delta_AD W.
```

For positive `Delta_AD W`, this forces a positive biotic balance conditional on the stated kappa restriction while leaving rho and iota individually unidentified.

Point identification uses a selective 16-cell

```text
A × D × antagonist access × pollinator access
```

design. `m0_delta` is measured or justified. The rho and iota cross-context invariance gaps are one `A×D×G×P` four-way contrast up to sign, so a non-zero four-way value rejects the simple separable-channel model. `U_delta = rho_delta - iota_delta - Delta_AD W` remains unallocated; interpreting it as kappa requires an independent A×D assay.

The final inference ladder is:

```text
interaction detection
→ identified set
→ partial identification
→ point identification
→ independent joint-channel validation
```

## 2. Mechanism → Pattern bridge

Retained recurrence evidence:

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

These overlapping categories establish constituent-channel recurrence, not natural prevalence or rho/iota/kappa magnitudes.

The 17-system audit is now interpreted as a **fragmented identification frontier**. Kessler 2008, Egan 2021, *Impatiens capensis*, and *Pedicularis rex* occupy complementary design faces. Screened-set facts remain:

```text
independent joint-cost assay:       0
full rho/iota/kappa identification: 0
```

The constituent channels recur, but their joint allocation remains unidentified. The stronger conclusion is that existing studies already constrain different dimensions of the allocation problem while none closes all of them.

## 3. Existing-data anchors

- **Kessler et al. 2008:** closest trait-factorial anchor; published aggregate constraints preserve a positive discrete reproductive interaction, with formal uncertainty and systemic-nicotine scope unresolved.
- **Egan et al. 2021:** complementary consumer-factorial anchor; no independently manipulated floral A×D pair.
- **Impatiens capensis:** observational A×D plus randomized interaction-treatment modification; all eight target HC3 intervals cross zero; not channel identification.
- **Pedicularis rex:** selective-access defence-system anchor without independent attraction manipulation.

No study-specific numerical rho/iota/kappa values or bounds are inferred from these near misses.

## 4. Historical analyses retained but demoted

The 2,592 finite evaluations and 77.2% selectivity-window precision remain Appendix technical sensitivity only. Leal and Sasidharan modules remain reproducible provenance/possible companion work. The theorem-led manuscript remains versioned but is not canonical.

## 5. Inference boundaries

```text
marginal recurrence
!= total interaction
!= assumption-indexed partial identification
!= point-identified channel interaction
!= full allocation
```

Therefore route counts are not prevalence; total interaction is not a unique mechanism; partial bounds must declare assumptions; randomized context modification is not selective exclusion; `U_delta` is not kappa; zero cost assays does not imply kappa=0; and a non-zero four-way term rejects separability.

## 6. Reader-facing and package QA

Current canonical pre-metadata package:

```text
Main Document: 29 pages
Appendix S1:   12 pages
Main figures:   5
```

Validated state for the fully integrated scientific head:

- CI — PASS on Python 3.10 / 3.11 / 3.12;
- identification candidate build — PASS;
- canonical Ecology build — PASS;
- page target — PASS with one Main-page margin;
- full-page visual QA — PASS on all **29 Main + 12 Appendix = 41 pages**;
- no blank pages, clipping, overlap, broken glyphs, missing figures, or broken equations;
- identified-set equations, kappa-bound, design-fragmentation text, Figure 1 reinterpretation, and Appendix projection algebra — readable;
- `Theorem 1` / 77.2% headline — absent from Main;
- 2,592 / 77.2% — Appendix technical material only.

## 7. Submission decision

**Science: GO on the partial-identification claim set. Reader-facing scientific/package QA: PASS. External submission: pending author-controlled metadata/sign-off.**

Remaining blockers are final authors/affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence, any portal-requested reviewer fields, all-author approval/no-simultaneous-submission confirmation, and one final rebuild/page-by-page QA after those fields are inserted.

The governing rule is now: **state exactly what the current evidence constrains, distinguish bounds from point identification, and choose the next observation that most shrinks the remaining identified set.**