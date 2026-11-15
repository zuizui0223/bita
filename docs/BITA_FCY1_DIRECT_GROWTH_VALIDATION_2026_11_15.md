# BITA Fcy1 direct growth validation — original plates, not just screen-positive pairs (2026-11-15)

**Study:** Després et al. (2024), *Science*, DOI 10.1126/science.ado5719. This is an original-source **within-study reanalysis**, not a new experiment, a new independent evolution programme, or a cross-study meta-analysis.

## New answer

**A selected set of Fcy1 loss-of-function alleles supports several functional heteromeric rescue configurations, and the initial positive-only selection screen is incomplete.** Previously PR #366 had recovered 207 selected positive pairs, but without a denominator of phenotyped negative pairs. This follow-up recovers direct phenotypes for an author-selected 18-variant validation panel, explicitly including pairs not found in the positive screen.

The full panel consists of 18 × 19/2 = **171 unordered combinations**, of which **153 have two distinct allele types** and **18 are same-allele controls**. The strict biological question is heteromeric complementation, so the 153 distinct-allele combinations are primary.

## Direct assays at 16 µg/ml cytosine; growth threshold 0.02 OD/h

**Strict distinct-allele heteromer pairs** (one pair is unmeasured; n=152 directly classified):

| Published initial screen | Direct growth ≥0.02 OD/h | Direct growth <0.02 OD/h | Unmeasured |
|---|---:|---:|---:|
| Screen positive | **24** | **3** | 0 |
| Not detected in screen | **3** | **122** | **1** |

Conditional on this deliberately chosen validation panel, 24/27 screen positives (88.9%) reproduce above threshold, and the direct-growth assay discovers three pairs the screen did not record. The apparent screening specificity among measured distinct-allele pairs is 122/125 (97.6%). These fractions are **conditional assay agreement measures**, not population frequencies of heteromerization, adaptation, gene duplication or historical accessibility. Pairs share parent alleles and crossing opportunities, so they are not independent evolutionary transitions; no naive binomial or pairwise Fisher causal p value is claimed.

**Three screen-unobserved functional distinct-allele pairs** had strong direct growth:

| Pair | Measured mean OD/h | Reciprocal directions |
|---|---:|---:|
| E64C + M100W | **0.13196** | 2 |
| I156P + R73G | **0.11204** | 2 |
| M100W + R53D | **0.11634** | 2 |

The three screen-positive pairs without demonstrated growth above threshold were E69L+H62C (0.00380 OD/h), H62C+Y79S (0.00636), and L74P+Y79S (0.00620), **each with only one reciprocal orientation measured**. Consequently these are not definitive biochemical failures for the unmeasured reciprocal arrangement. H62C+L74P is unmeasured in both directions and remains missing, not negative.

## Author-documented exclusion: resolved original source discrepancy

The original **peer-reviewed Methods** explicitly exclude the same-allele `M93G + M93G` diploid-stock sample because of **cross-contamination with another genotype** (Després et al. 2024, section *Mating and growth rate measurements*; [source full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10888846/)). It is present in the deposited raw workbook (apparent 0.13188 OD/h), but this contaminated measurement is **not valid biological growth evidence**.

An earlier extraction noted an apparent discrepancy: directly taking all source workbook values yielded 168 measured of 171 genotypes and an extra screening-negative/growth-positive same-allele control. The discrepancy is **resolved**, not unexplained, by following the explicit published exclusion. The corrected all-171-panel classification matches the author's saved notebook exactly: **TP 24 / FP 3 / FN 3 / TN 137**, **4 unclassified**, **167 measured**. The excluded workbook value is preserved solely as audit provenance. The distinct-mutant subset remains **153 pairs / 152 measured / TP24 FP3 FN3 TN122 / 1 unmeasured**. No heteromer rescue count is changed.

**Source availability:** the author repository contains **22**, not 24, original \`plate_*_*.xlsx\` growth files; \`plate_6_C.xlsx\` and \`plate_6_D.xlsx\` are absent. They are **not imputed**. All 2304 source layout wells are retained as bookkeeping entries before the author's explicit filters, and missing coordinates remain missing.

## Source chain and direct reconstruction

Pinned original author Git commit: \`f124cef96a3b5806a096b679b2bd57b68aec6514\`.

Original screen-positive CSV Git blob: \`36839a3fd2eb05a521a070d11e60cde1748a682e\`.

Original validation notebook Git blob: \`2ebafd783a94506aa349e46a1429fb2c98c16319\`.

Original paths used:
- \`validations_analysis/data/array_LOF.csv\` (2304-well layout)
- \`validations_analysis/data/validations_mat_a_nat.xlsx\` and \`validations_mat_alpha_hph.xlsx\` (strain-number/genotype maps)
- \`validations_analysis/lofxlof_crosses/plate_*_[A-D].xlsx\` (22 available files)
- \`validations_analysis/indep_crosses.csv\` (initial screen-positive pair identity)

The new \`scripts/analyze_bita_fcy1_validation.py\` reproduces the author's OD/h slope estimator: for each 15-minute time-series well, take the median of the **five largest first differences ×4** before 21 hours, then average source reciprocal orientations when both are observed, following the original notebook's missingness rule. A source-specific well is excluded according to the author's notebook, and the exact source well-to-allele layout is retained.

Reproduce on GitHub Actions: [Fcy1 raw plate audit run #43683966411](https://github.com/zuizui0223/bita/actions/runs/43683966411) **success**, including source genotype verification, 22 raw sheets, original table SHA, all 171 mean-growth outcomes and unit tests. The full derived per-pair values and 22-workbook SHA256 manifest are saved as Actions artifact ID **14149900663**. The committed \`despres2024_growth_validation_summary.json\` freezes key counts and their strict biological interpretation; the full per-pair readout is an artifact, not rehosted original raw XLSX data.

## Scientific meaning and claim ceiling

Fcy1 source data demonstrate **multiple viable molecular compensations**, including three directly viable non-observed screen combinations. This supports *architecture feasibility*, and it demonstrates why observational absence in a filtered screen is not identical to a biochemical impossibility. The source paper supports constructive-neutral evolutionary routes via gene duplication and reciprocal compensation. Neither our positive network nor this assay verifies those historical routes actually fixed in nature.

Do **not** claim:
- 207 positives / 613 positive crossing identifiers / 171 selected genotype pairs are a representative natural prevalence or independent evolutionary origins;
- direct growth restoration establishes increased optimal whole-organism fitness over an ancestral shared architecture (the WT comparator and its resource costs have not been jointly manipulated here);
- absent source variants are genuine negatives outside the 18-variant assay;
- the original contaminated M93G/M93G workbook signal is biological evidence; the authors explicitly excluded it;
- one engineered experimental programme identifies BITA's startup cost K(u), theoretical entry/global/fold threshold or species-level historical divergence;
- this Fcy1 growth contrast can be pooled numerically with Salmonella physiological rescue, coGFP fluorescence, Peucedanum floral allocation or cichlid jaw covariance without predeclared common estimands.

**Next evidence path:** expand independently phenotyped negative/control comparisons within source studies, then seek historical/phylogenetically independent functional-module transitions. This current empirical work remains separate from the Ecology Letters nectar-robbery Letter. Preserve Draft until scientific review; do not merge or submit externally.
