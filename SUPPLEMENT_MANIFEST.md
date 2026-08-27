# Supplement manifest — canonical partial-identification paper

Canonical target:

> **From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence**

The theorem-led manuscript remains provenance only. The active Main is the identification-design manuscript with Mechanism → Pattern recurrence and an explicit partial-identification layer.

## 1. Canonical sources

- Main: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- references: `manuscript/IDENTIFICATION_DESIGN_REFERENCES.md`
- captions: `manuscript/IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md`
- figures: `manuscript/identification_figures/`
- Appendix: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- identified-set derivation: `docs/PARTIAL_IDENTIFICATION_FRONTIER_V1.md`
- package builder: `scripts/build_ecology_review_package_sources.py`

Primary implementation:

- `trait_architecture/identification.py`
- `trait_architecture/partial_identification.py`
- `empirical/identification_design/HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv`
- `empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json`
- `empirical/mechanism_pattern_synthesis/`

## 2. Canonical scientific core

```text
Delta_AD W = W11 - W10 - W01 + W00
Delta_AD W = rho_delta - iota_delta - kappa_delta
I(delta) = {(rho,iota,kappa): rho-iota-kappa=delta}
```

Inference sequence:

```text
interaction detection
→ identified set
→ partial identification under explicit restrictions
→ crossed A × D × antagonist × pollinator interventions
→ m0 correction + four-way separability test
→ point identification of biotic channels
→ independent joint-channel assay / diagnostic
```

Central recovered partial bound:

```text
kappa_delta >= 0
=> rho_delta - iota_delta >= Delta_AD W
```

This is conditional on a defensible kappa restriction. It is not a universal theorem.

Required boundaries:

- total `Delta_AD W` does not uniquely allocate rho/iota/kappa;
- partial-identification statements must name their bounds/assumptions;
- the 16-cell design still requires selective interventions and comparable A/D coordinates;
- rho/iota invariance views are one four-way interaction up to sign; this is the `A×D×G×P separability diagnostic`;
- non-zero four-way coupling rejects separability;
- total iota requires `m0_delta` handling;
- `U_delta` is unallocated, not kappa by definition;
- kappa requires an independent A×D joint-cost assay.

## 3. Mechanism → Pattern recurrence layer

Retained recurrence layer:

```text
56 source-adjudicated route records
25 independent biological clusters
A -> pollination: 5
A -> antagonism:  8
D -> antagonism: 18
D -> pollination: 10
same-system:      14
context/sign switch: 17
```

These counts establish recurrence only and do not estimate `Delta_AD W`, `rho_delta`, `iota_delta`, or `kappa_delta`.

Across the 16-system high-information screen, trait-factorial, consumer-factorial, randomized context-modification, and selective-defence information occurs in complementary studies. No screened system closes all allocation dimensions and no independent joint-cost assay is present. The audit is therefore interpreted as a **fragmented identification frontier**, not merely a 0/16 failure count.

## 4. Existing-data identification stress tests

- **Kessler et al. 2008 — trait-factorial anchor:** aggregate `Delta_AD` approximately +0.19 to +0.25, interaction OR approximately 2.77 to 4.71; formal uncertainty and systemic-D scope remain unresolved.
- **Egan et al. 2021 — consumer-factorial anchor:** complementary consumer-factorial structure.
- **Soper Gorden & Adler 2018 — public-data retrofit:** observational A×D plus randomized context modification; all eight target HC3 intervals cross zero.
- **Pedicularis rex:** selective-access defence anchor without independent attraction manipulation.

```text
independent joint-cost assay:       0
full rho/iota/kappa identification: 0
```

These studies are not assigned invented rho/iota/kappa values or bounds.

## 5. Main figures

1. Figure 1 — total trait interaction defines an identified set rather than a unique mechanism.
2. Figure 2 — crossed 16-cell intervention design and separability diagnostic.
3. Figure 3 — independent joint-channel assay versus unallocated residual.
4. Figure 4 — 56/25 recurrence plus fragmented identification frontier and empirical anchors.
5. Figure 5 — executable roadmap from interaction detection through partial to point identification.

## 6. Appendix S1 boundary

The active Appendix retains:

- exact identified-set projection algebra and assumption-indexed partial-identification examples;
- distinction between structural projection intervals and sampling uncertainty intervals;
- Kessler 2008 reconstruction;
- *Impatiens* retrofit;
- 16-system identification-frontier details;
- 56/25 recurrence evidence and boundary;
- 2,592 finite evaluations and 77.2% grid-specific precision as technical sensitivity only;
- continuous-limit / finite-difference and response-shape sensitivity material.

Leal and Sasidharan remain reproducible historical modules, not Main evidence.

## 7. Historical quantitative provenance retained

Leal et al. 2025 provenance remains pinned:

```text
canonical commit: ed33b25593c0d90ad6657753f6f5501d9efc7b82
preregistration:  0e36eac
first results:    965d657
source synthesis: doi:10.1002/ecy.70036
```

Historical values and the Sasidharan reconstruction remain preserved with their original inference boundaries and do not validate the identification framework.

## 8. Open Research package

Exports include the route ledger, high-information identification coverage, *Impatiens* aggregate retrofit, and historical provenance products. Review-stage access is via public GitHub; accepted-version permanent archiving is an acceptance-stage requirement.

## 9. Current rendered state

```text
Main Document: 29 pages
Appendix S1:   12 pages
Main figures:   5
```

All **41 pages** were visually inspected after partial-identification integration and Main compaction. No blank pages, clipping, overlap, broken glyphs, missing figure content, or broken equations were found. The Main remains within the 30-page target with one-page headroom.

## 10. External-submission boundary

Only author-controlled metadata/sign-off remains: author order/names/affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence, portal-only reviewer fields if requested, all-author approval and no-simultaneous-consideration confirmation. After insertion, rebuild and inspect the exact package again.