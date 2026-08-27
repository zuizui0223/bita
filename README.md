# Biotic Interaction Trait Architecture

A reproducible **Mechanism → Pattern → Identification** study of floral attraction and defence. The canonical paper asks an operational question: **when attraction (`A`) and a flower-associated antagonist-reducing trait (`D`) interact on reproduction, what can the observed interaction already constrain, and what additional observations are required to identify the ecological channels that generated it?**

## Current scientific result

For two experimentally meaningful attraction and defence levels, the primary estimand is

```text
Delta_AD W = W11 - W10 - W01 + W00
```

A total `Delta_AD W` does not point-identify antagonist relief (`rho_delta`), pollinator interference (`iota_delta`), and the remaining joint channel (`kappa_delta`). If `Delta_AD W = delta`, compatible allocations form the identified set

```text
I(delta) = {(rho, iota, kappa): rho - iota - kappa = delta}
```

so measuring the same total surface more precisely cannot by itself collapse mechanism uncertainty to one point. Explicit biological restrictions or channel-specific measurements can, however, shrink this set. In particular,

```text
kappa_delta >= 0
=> rho_delta - iota_delta >= Delta_AD W
```

which recovers the historical one-sided result as a **partial-identification bound on the biotic balance**, not as a universal theorem about nature.

The inference ladder is therefore:

```text
interaction detection
→ identified set
→ partial identification under declared bounds
→ point identification after selective crossed interventions
→ independent joint-channel validation
```

## Point-identification design

The repository implements a crossed

```text
A × D × antagonist × pollinator
```

16-cell design. Channel contrasts are interpretable only when consumer interventions are selective and the same A/D coordinates are maintained across cells. Pollinator-independent reproduction (`m0_delta`) is measured or justified rather than assumed away. Dependence of the antagonist contrast on pollinator state and dependence of the pollinator contrast on antagonist state are the same `A×D×G×P` four-way interaction up to sign, providing an internal separability diagnostic.

The remaining residual

```text
U_delta = rho_delta - iota_delta - Delta_AD W
```

is kept **unallocated**. It is not called `kappa` by subtraction. A joint construction/allocation channel requires an independent `A×D` assay under standardized or suppressed biotic pathways.

## Mechanism → Pattern bridge

The source-adjudicated recurrence layer contains:

```text
56 route records
25 independent biological clusters
A -> pollination:         5 clusters
A -> antagonism:          8
D -> antagonism:         18
D -> pollination:        10
same-system multi-route: 14
context/sign switch:     17
```

These overlapping counts show that the **constituent ecological pathways recur across systems**. They are not natural-prevalence estimates and they do not estimate `Delta_AD W`, `rho_delta`, `iota_delta`, or `kappa_delta`.

The stricter 16-system audit shows a second pattern: **design fragmentation**. Existing studies occupy complementary faces of an identification frontier rather than all failing in the same way. Kessler et al. (2008) supplies the closest trait-factorial side; Egan et al. (2021) the complementary consumer-factorial side; the public *Impatiens capensis* retrofit reaches randomized context modification of an observational `A×D`; *Pedicularis rex* supplies a selective-defence system anchor. No screened system closes all allocation dimensions or contains an independent joint-cost assay.

The cross-system conclusion retains the earlier boundary:

> **The constituent channels recur, but their joint allocation remains unidentified.**

The refined conclusion is:

> **The constituent channels recur, current studies constrain different parts of their allocation, but the full joint mechanism is not yet point-identified.**

The useful next question is no longer only “is the mechanism identified?” but **which additional measurement or intervention most shrinks the remaining identified set?**

## Canonical paper

Current reader-facing sources:

- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` — canonical scientific text
- `manuscript/IDENTIFICATION_DESIGN_REFERENCES.md` — focused reference spine
- `manuscript/IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md` — Main figure captions
- `manuscript/identification_figures/` — canonical Figures 1–5
- `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md` — Appendix S1
- `docs/PARTIAL_IDENTIFICATION_FRONTIER_V1.md` — identified-set / bound derivation
- `docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md` — recurrence/identification boundary
- `submission/` — Ecology review-package and portal documents

The historical theorem-led manuscript and its analyses remain versioned for provenance; they are not the canonical submission source.

## Reproducibility core

Primary identification implementation and tests:

- `trait_architecture/identification.py`
- `trait_architecture/partial_identification.py`
- `tests/test_identification.py`
- `tests/test_identification_four_way.py`
- `tests/test_identification_coverage.py`
- `tests/test_partial_identification.py`
- `tests/test_partial_identification_balance.py`
- `tests/test_partial_identification_manuscript_integration.py`

Empirical products include:

- `empirical/identification_design/HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv`
- `empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json`
- `empirical/mechanism_pattern_synthesis/` — retained route-level recurrence evidence

The former 2,592 finite evaluations and 77.2% window precision remain implementation/model-family sensitivity in Appendix S1. They are not empirical validation or natural-regime frequencies. Leal and Sasidharan quantitative modules remain reproducible historical analyses but are not Main identification evidence.

## Inference boundaries

```text
marginal route recurrence
!= total A×D interaction
!= partial channel bounds
!= point-identified channel interaction
!= full mechanism allocation
```

Accordingly:

- route counts are not prevalence estimates;
- total `Delta_AD W` alone leaves an identified set rather than a unique mechanism;
- partial-identification claims are conditional on explicitly declared bounds;
- randomized context modification is not selective consumer exclusion;
- a non-zero `A×D×G×P` contrast rejects the simple separable-channel representation;
- `U_delta` is not `kappa` by definition;
- zero independent joint-cost assays does not imply `kappa = 0`;
- finite-grid fractions are not probabilities of natural regimes.

## Submission state

The current pre-metadata Ecology Concepts & Synthesis package renders to **29 Main pages + 12 Appendix pages**, with five Main figures, and remains within the standard 30-page target with one Main-page margin. CI and canonical/candidate package builds passed for the integrated scientific head, and all **41 rendered pages** were visually inspected with no blank pages, clipping, overlap, broken glyphs, missing figures, or broken equations.

External submission remains blocked only by author-controlled fields and sign-off: final author order/names, affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence statement, any portal-requested reviewer information, all-author approval, and the final post-metadata rebuild/QA.