# Fcy1 positive complementation network: independent-source recovery (2026-11-15)

**Status:** published-source reanalysis; no new experiment, natural prevalence, independent historical transition or pooled meta-analysis. This is a distinct biochemical empirical lane from Salmonella rescue and E. coli coGFP selection.

## Question and source

Can distinct pairs of imperfect components produce a functional whole, rather than requiring one uniquely correct split architecture? In the *engineered* yeast Fcy1 assay, many distinct two-allele combinations can restore function. This documents accessible functional configurations, not the historical selection that caused a new organ or duplicate to arise.

**Primary study:** Després et al. (2024), Science, DOI [10.1126/science.ado5719](https://doi.org/10.1126/science.ado5719), "Compensatory mutations potentiate constructive neutral evolution by gene duplication". Fcy1 is normally a homomeric enzyme; the study screened loss-of-function alleles for rescue when distinct variants coexpress as a heteromer.

**Original data:** [Landrylab/Despres_et_al_2024 / validations_analysis/indep_crosses.csv](https://github.com/Landrylab/Despres_et_al_2024/blob/main/validations_analysis/indep_crosses.csv). Source Git blob SHA-1: **36839a3fd2eb05a521a070d11e60cde1748a682e**. The local source copy has the same Git blob SHA and 7,197 bytes. The author-generating analysis lives in single_colony_genotyping/single_colony_genotyping.ipynb, including construction of the independent-cross count table. The table is **selected positive genotypes only**, not an exhaustive positive/negative screening frame.

## Denominator audit: distinct units that must not be conflated

| Source level | Count | Meaning |
|---|---:|---|
| Unique unordered **positive allele-pair types** | **207** | observed compatible types after original study filters |
| Unique alleles incident to a positive pair | **103** | observed distinct Fcy1 variants in the positive table |
| Selected positive colony observations | **887** | sum of author field n_observed |
| Distinct codon-by-cross positive identifiers | **613** | sum of author field n_indep_crosses |
| Positive pairs with at least two distinct positive cross identifiers | **104/207** | 50.24% of positive types repeated |
| Positive pairs with one positive cross identifier | **103/207** | 49.76% of positive types seen once |

**Neither 887 nor 613 is a universal denominator of all screened genotype opportunities.** The positive table does not identify unconditional functional-complementation prevalence, and 613 positive codon-cross identifiers are not 613 independent evolutionary origins.

## Positive-only compatibility graph and repeat-cross sensitivity

Define one vertex per observed allele and an undirected edge for each observed positive heteromer pair. Edge weights represent recurrence of source-positive cross identifiers, *not fitness gain*.

| Minimum source-positive cross identifiers per pair | Positive edges | Alleles present | Largest connected component | Total components |
|---|---:|---:|---:|---:|
| 1 | **207** | **103** | **97** | **4** |
| 2 | **104** | **53** | **44** | **3** |
| 3 | **73** | **38** | **29** | **3** |
| 5 | **38** | **25** | **16** | **3** |

The largest graph component persists when dropping single-cross records. On the full graph, variant M100W has **39** distinct positive partner alleles, R73D **33**, R73G **24**, Y79S **17**. Five high-degree alleles account for 30.43% of the 414 positive edge endpoints. This is **conditional on positive discovery**, not a sampling-adjusted probability and not a proven mechanism for preferred natural pair formation.

**Ascertainment audit:** source expected allele-pair frequency (log2) is available for **156/207** positive pairs; missing for 51. Within the 156 positive records with finite values, the descriptive midrank Spearman correlation of expected precursor frequency with distinct positive cross count is **rho=+0.477935**. No ordinary pair-level p value is promoted, because alleles are shared between edges, all records are selected positives, and frequency missingness may be nonrandom. Precursor abundance may contribute to repeated recovery and network concentration.

The primary publication independently states that 192/207 positive pairs involve variants among 16 positions and that 148/207 include a variant with likely catalytic loss of function. Those particular residue/function annotations are **paper-reported background**, not newly recoded from the pair CSV.

A connected graph component is a list of compatible pair observations. It is **not** a demonstrated one-mutation viable path among vertices, a fully adaptive network, or evidence that each edge evolved separately.

## Implications for BITA

- **Architecture feasibility:** Functional reconstitution can emerge from individually nonfunctional components through positive trans-epistasis. This supports an experimentally demonstrable alternative to assuming that functional division must always arise from directional selection for a globally superior architecture.
- **Evolutionary history not identified:** Mutants were generated and screened by design. The positive network does not show historical neutral fixation of 207 natural lineages or the time order of duplicate-origin and loss-of-function events in natural populations.
- **No universal architecture benefit coefficient:** We cannot estimate BITA's shared-vs-divided fitness margin, startup cost K(u), the residual interference coefficient lambda, or its entry/benefit/persistence threshold from source positive-pair counts.
- **Do not pool other source programmes:** Salmonella HisA/TrpF uses physiological rescue, eLife coGFP uses fluorescent-positive fraction and ancestor-normalized fluorescence, Peucedanum uses ecological allocation, and cichlids use morphology covariance. A common effect scale has not been established.

This is **one independent biochemical programme**, not 207 evolutionary replications and not a pooled cross-taxon meta-analysis.

## Reproduction, remaining evidence and release boundary

Run from the root of the BITA repository:

    python -m scripts.analyze_bita_fcy1_compatibility
    python -m pytest -q tests/test_bita_fcy1_compatibility.py

Inspect data, generated readout, analysis script and tests in empirical/trait_architecture_history and scripts/tests. The separate audit-bita-fcy1-compatibility GitHub Actions job reproduces and archives the source count hierarchy.

A full estimated *rate* of complementation needs the eligible genotype-pair sample frame including true negatives, exposure/selection probabilities and independent assay denominators. A historical transition claim further needs ancestral controls, genotype-step sequence, and common-fitness comparisons.

**No active manuscript edits, main merge, external deposit or journal submission.** Preserve as Draft pending source and biological review.
