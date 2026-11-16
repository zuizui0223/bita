# Independent yeast mutational architecture: original-source intake, not a frequency-of-origins test

Date: 2026-11-17. This work continues the earlier E. coli 16-population Figure 2 saturation at PR #378, but **does not reuse any of that publication's lineages**.

## New independently published source, narrowly admitted

**Kinsler G, Li Y, Sherlock G, Petrov DA (2024)**, *PLoS Biology* **22:e3002848**, DOI https://doi.org/10.1371/journal.pbio.3002848.

Original publication experimentally extends five distinct first-step **Saccharomyces cerevisiae** genotype backgrounds (CYR1, GPB2, TOR1, IRA1 missense, IRA1 nonsense). Its barcoded second-step evolution and phenotype assays distinguish fermentation versus respiration growth-phase performance, and additionally measure stationary-phase performance. The article reports an approximately 85% first-step fermentation+respiration pleiotropic-improvement fraction, 35% among second-step adaptive haploids from two-day Evo2D, and 13% among three-day Evo3D; these are *author-reported sample/measurement-error-conditioned estimates*, **not new measurements or all initial evolution-lineage origin rates**. (Fig. 3 and published Results). It also documents costs to fermentation accompanying many second-step respiration gains, and selection-conditioned behavior of stationary performance.

The prior BITA/SCH/SLK evidence ledgers do not list this independent publication. This is distinct from previously examined Kim 2016, Zhang 2020, Chen 2024, and D'Souza & Kost 2016 sources. **New source != new source-proven rate of historical two-task architectural splitting**.

## Exact original deposited data path

- **Primary published source:** https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3002848
- **Publisher's named author deposit:** https://zenodo.org/records/13336585
- **Author's public analysis/data repository:** https://github.com/grantkinsler/EvolvingFront
- **Pinned published-author Git commit:** `0de5873c853e08e78541cec4f50988f41327af47` (2024-08-17).
- `data/S1_Data.csv` immutable Git blob SHA-1 `978383e99eae1065771fd46176095bbf65ca0b81`.
- `data/S3_Data.csv` immutable Git blob SHA-1 `8dcb160b94e8877002233a8e7e0e2d62445c46cb`.

The Git **blob** SHA-1 is calculated with the Git 'blob [bytes]\\0' header and is *not* a SHA-256 of the CSV. CI verifies the original content-addressed Git objects, and also records a separate SHA-256 digest. No copyrighted raw files or long specimen rows are copied into this repository. The two author CSVs are archived as a source **inventory artifact containing only aggregate schema and counts**.

## First source-scope trap caught before biological modeling

The smaller `S3_Data.csv` contains **185 unique barcode rows**, comprising five first-step parental backgrounds:

- IRA1 missense: 82
- IRA1 nonsense: 59
- CYR1: 32
- TOR1: 7
- GPB2: 5

All 185 have `evolution_condition=Evo2D`, `isolated_evolution_condition` ending in `_R2`; 140 are annotated `adaptive_haploid` and 45 `high_fitness_diploids`. This is **not** all isolated second-step mutants across Evo2D/Evo3D and **not** 185 independent evolving populations; these rows are a selected subset with evolution-fitness estimates used for one targeted published analysis.

The paper describes **two evolution replicates** for each barcoded initial population in Evo2D, but clone counts within a replicate are nested. The complete S1 inventory must be inspected before any phase-composition estimate or parent-relative effect can be recovered. The paper itself also notes that the high-fitness secondary clones have frequency-dependent measurement effects, and the authors used only early fitness-measurement timepoints for their main estimates; careless repooling of different timepoints would misestimate functional effects.

## Scientific purpose and strict claim ceiling

This dataset can test the **mutational scope of subsequent adaptation** on a common performance coordinate system (fermentation, respiration, stationary), conditioned on parental genotype and evolution protocol. It is an external empirical case relevant to **pleiotropy versus modular adaptive effects**. It does not by itself test ecological coexistence of complementary specialists or the initial historical split of a single two-function module into two jointly maintained modules.

For inference, distinguish at least four nested units:

1. The **single original publication/research programme** (one independent empirical programme in the BITA catalogue).
2. The five **founding adaptive genotype backgrounds** (not five independent species/experiments).
3. The individual independently evolving **population replicates** of a specified environment (e.g. Evo2D_R1/R2).
4. The sequenced **isolated barcoded adaptive clones**, nested within these populations, with high selection/measurement ascertainment.

No n=185 independent-population test, no post hoc two-step 'mutation origin probability' from an isolated sample, no independent publication count for individual assays. The authors' original percentages must remain attributed to their source until a like-for-like source reanalysis and denominator audit succeeds.

## Next source-aware numeric step

From the pinned author `S1_Data.csv`, identify all combinations of `ancestor`, `evolution_condition`, replicate/provenance and `class_new`. Reconstruct **parent-relative** performance differences in fermentation and respiration by original source's background-specific neutral reference rules, retaining measurement errors and excluding genotype-ploidy/fitness assay mismatches. Compare selected adaptive-clone conditional distributions across Evo2D/Evo3D, and report a sensitivity with **equal weight for parental genotype and where possible for independent evolution replicate**, alongside the cell/clone-weighted descriptive estimate. If source rows do not expose reliable evolutionary population IDs or parent matched contrasts, declare **not identifiable** instead of inventing them.

The paper's method specifies neutral barcode means as the parent reference for CYR1/GPB2/TOR1/IRA1 missense and a named first-step barcode parental reference for IRA1 nonsense. This difference must be reflected in any reanalysis before a sign quadrant is reported.

**Existing project boundary:** the active BITA manuscript still owns trait-interaction mechanism identification, while SLK/historical Chapter 2 owns architecture-value, invasion and fixation. This independent yeast experiment remains isolated quantitative input, not manuscript promotion.

## Status

Original-author source inventory CI is the first gate. **No public external action, merge, or manuscript modification** is authorized by a successful intake receipt.
