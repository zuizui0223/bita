# Biotic Interaction Trait Architecture

A reproducible **Mechanism → Pattern → Identification** study of floral attraction and defence. The canonical paper no longer treats a one-line inequality as the main result. Its central question is operational: **when an attraction trait (`A`) and a flower-associated antagonist-reducing trait (`D`) interact on reproduction, what experiment is required to identify the ecological channels that generated that interaction?**

## Current scientific result

For two experimentally meaningful levels of attraction and defence, the primary estimand is the discrete interaction

```text
Delta_AD W = W11 - W10 - W01 + W00
```

A total `Delta_AD W` does not identify how much of the interaction comes from antagonist relief, pollinator interference, or another joint channel. The repository therefore implements a crossed

```text
A × D × antagonist × pollinator
```

16-cell design. Channel contrasts are interpretable only when consumer interventions are selective and the same A/D coordinates are maintained across cells. Pollinator-independent reproduction (`m0_delta`) is measured or justified rather than assumed away. Dependence of the antagonist contrast on pollinator state and dependence of the pollinator contrast on antagonist state are the same `A×D×G×P` four-way interaction up to sign, providing an internal separability diagnostic.

The remaining residual

```text
U_delta = rho_delta - iota_delta - Delta_AD W
```

is kept **unallocated**. It is not called `kappa` by subtraction. A joint construction/allocation cost requires an independent `A×D` assay under standardized or suppressed biotic channels. The elementary algebra is retained only as a post-measurement consistency or hidden-channel sign diagnostic.

## Mechanism → Pattern bridge

The cross-system synthesis is retained in a bounded role. The source-adjudicated route architecture contains:

```text
56 route records
25 independent biological clusters
A -> pollination:        5 clusters
A -> antagonism:         8
D -> antagonism:        18
D -> pollination:       10
same-system multi-route:14
context/sign switch:    17
```

These overlapping counts show that the **constituent ecological pathways recur across systems**. They are not natural-prevalence estimates and they do not estimate `Delta_AD W`, `rho_delta`, `iota_delta`, or `kappa_delta`.

The stricter identification audit then asks whether those recurrent ingredients have been combined in one experiment. Across the current 16-system high-information screen, no study combines the full trait factorial, selective antagonist and pollinator interventions, pollinator-absent baseline characterization, and an independent joint-cost assay.

The resulting cross-system conclusion is:

> **The constituent channels recur, but their joint allocation remains unidentified.**

Kessler et al. (2008) supplies the closest trait-factorial anchor; Egan et al. (2021) supplies the complementary consumer-factorial structure; the public *Impatiens capensis* retrofit reaches randomized context modification of an observational `A×D` association but not channel identification. The missing object is their intersection.

## Canonical paper

Current reader-facing sources are:

- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` — canonical scientific text
- `manuscript/IDENTIFICATION_DESIGN_REFERENCES.md` — focused reference spine
- `manuscript/IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md` — Main figure captions
- `manuscript/identification_figures/` — canonical Figures 1–5
- `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md` — Appendix S1
- `docs/MECHANISM_PATTERN_IDENTIFICATION_BRIDGE.md` — recurrence/identification boundary
- `submission/` — Ecology review-package and portal documents

The historical theorem-led manuscript and its analyses remain versioned for provenance, but they are not the canonical submission source.

## Reproducibility core

Primary identification implementation and tests:

- `trait_architecture/identification.py`
- `tests/test_identification.py`
- `tests/test_identification_four_way.py`
- `tests/test_identification_coverage.py`
- `tests/test_mechanism_pattern_identification_bridge.py`

Empirical identification products:

- `empirical/identification_design/HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv`
- `empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json`
- `empirical/mechanism_pattern_synthesis/` — retained route-level recurrence evidence

The former 2,592 finite evaluations and 77.2% window precision remain as implementation/model-family sensitivity in Appendix S1. They are not empirical validation or natural-regime frequencies. Leal and Sasidharan quantitative modules remain reproducible historical analyses but are not Main identification evidence.

## Inference boundaries

The repository preserves these distinctions:

```text
marginal route recurrence
!= total A×D interaction
!= channel interaction
!= full mechanism allocation
```

Accordingly:

- route counts are not prevalence estimates;
- marginal route recurrence does not identify `rho_delta` or `iota_delta`;
- total `Delta_AD W` alone does not allocate mechanisms;
- randomized context modification is not the same as selective consumer exclusion;
- a non-zero `A×D×G×P` contrast rejects the simple separable-channel representation rather than being forced into one pair of channel estimands;
- `U_delta` is not `kappa` by definition;
- zero independent joint-cost assays in the screened set does not imply `kappa = 0`;
- finite-grid fractions are not probabilities of natural regimes.

## Submission state

The current pre-metadata Ecology Concepts & Synthesis package renders to **29 Main pages + 11 Appendix pages**, with five Main figures, and remains within the standard 30-page target. CI, submission-scope, candidate/canonical package builds, EPS export, and full-page visual QA have passed for this scientific content.

External submission remains blocked only by author-controlled fields and sign-off: final author order/names, affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence statement, any portal-requested reviewer information, all-author approval, and the final post-metadata rebuild/QA.