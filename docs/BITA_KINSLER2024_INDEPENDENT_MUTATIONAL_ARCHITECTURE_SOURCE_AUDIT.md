# Independent yeast mutational architecture: original-source intake, not a frequency-of-origins test

Date: 2026-11-17. This work continues the earlier E. coli 16-population Figure 2 saturation at PR #378, but **does not reuse any of that publication's lineages**.

## New independently published source, narrowly admitted

**Kinsler G, Li Y, Sherlock G, Petrov DA (2024)**, *PLoS Biology* **22:e3002848**, DOI https://doi.org/10.1371/journal.pbio.3002848.

Original publication experimentally extends five distinct first-step **Saccharomyces cerevisiae** genotype backgrounds (CYR1, GPB2, TOR1, IRA1 missense, IRA1 nonsense). Its barcoded second-step evolution and phenotype assays distinguish fermentation versus respiration growth-phase performance, and additionally measure stationary-phase performance. The article reports an approximately 85% first-step fermentation+respiration pleiotropic-improvement fraction, about 35% among selected second-step adaptive-clone classes for two-day Evo2D, and about 13% for three-day Evo3D; these are *author-reported sample/measurement-error-conditioned estimates*, **not new measurements or all initial evolution-lineage origin rates**. (Fig. 3 and published Results). It also documents costs to fermentation accompanying many second-step respiration gains, and selection-conditioned behavior of stationary performance.

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

## Completed original-source quantitative analysis (parent-relative `S1_Data.csv`)

The original-author `S1_Data.csv` is **not one homogeneous 2024 dataset**. It contains **4,633 unique barcode rows** assembled across `This_study=1,250`, `Aggeli2020=2,459`, `Li2019=442`, and `Venkataram2015=482`. The smaller S3 contains 185 selected Evo2D/R2 rows already present in S1, not another 185 experiments. Source acquisition and original Git-blob fingerprints passed read-only GitHub Actions verification.

The following results use the *already deposited, parent-relative* `FerPerHour_relative`, `ResPerHour_relative`, and `StaPerHour_relative` columns. We did not invent an ancestral-reference subtraction or silently pool raw measurements in their place. The table contains **selected isolated clones**, not independent mutation-origination opportunities.

| Selected adaptive-clone stratum | Clones | Fer and Res both >0 | Res>0 / Fer<0 |
|---|---:|---:|---:|
| Evo2D adaptive haploid | 241 | 64 (26.6%) | 174 |
| Evo2D high-fitness diploid | 65 | 45 (69.2%) | 20 |
| **Evo2D all selected adaptive classes** | **306** | **109 (35.6%)** | **194** |
| Evo3D adaptive haploid | 186 | 18 (9.7%) | 168 |
| Evo3D high-fitness diploid | 16 | 7 (43.8%) | 9 |
| **Evo3D all selected adaptive classes** | **202** | **25 (12.4%)** | **177** |

The remaining Evo2D 3/306 clones have fermentation improvement without respiration improvement. All percentages are **raw sign-based clone descriptives**, not the original authors' full measurement-error-based resampling or phylogenetically/lineage-independent effects. The displayed 109/306 and 25/202 numerically reconstruct the published rounded **35% and 13%**, *only after retaining both high-fitness diploid and adaptive haploid categories*. Reporting 64/241 alone as the whole published Evo2D sample would be a denominator error.

### Original stationary-phase numerator reconciliation

A second trap: `StaPerHour_relative > 0` would count **110/306 Evo2D** and **178/202 Evo3D**, not the paper's reported **77/306** and **160/202**. The deposited error-field threshold `StaPerHour_relative > StaPerHour_error` instead reproduces the original published counts **exactly**, as well as their two-function breakdown:

| Source-defined numerical check | Evo2D | Evo3D |
|---|---:|---:|
| all selected adaptive clones | 306 | 202 |
| stationary improvement beyond source error field | **77** | **160** |
| of these, Fer & Res both positive | **7** | **5** |
| of these, remaining Fer–Res patterns | **70** | **155** |

This is a **numerical source-rule reconstruction**, not independent verification of how the deposited `_error` fields were statistically estimated or of the paper's uncertainty intervals. The original raw-sign and thresholded indicators are both retained separately. A conservative `2 × deposited error` sensitivity is available for the Fer–Res outcomes but is **not** substituted for the author's own statistical model.

### Source and ancestral-background composition alter interpretation

Of the 508 Evo2D+Evo3D selected adaptive clone rows, **387 are tagged `This_study`** and **121 `Aggeli2020`**. Evo2D includes the earlier source (121), whereas Evo3D is from `This_study` (202). As a result, the unadjusted **109/306 versus 25/202** difference combines environmental treatment with historical source and parental-genotype composition. It is not a design-matched causal estimate for Evo2D versus Evo3D.

A strict descriptive sensitivity on the **two parental genotypes present in both environments and marked `This_study`** gives:

| Matched first-step genotype | Evo2D Fer+Res both >0 | Evo3D Fer+Res both >0 |
|---|---:|---:|
| IRA1 missense | 23/90 (25.6%) | 13/30 (43.3%) |
| IRA1 nonsense | 17/95 (17.9%) | 1/134 (0.7%) |

Their equal-two-background descriptive mean is **21.725% Evo2D and 22.040% Evo3D**, versus their *clone-weighted* 40/185 (21.6%) and 14/164 (8.5%). The IRA1 missense and nonsense directions disagree. The contrast cannot be reduced to a single universally positive shift towards module-specific adaptation without controlling source and genotype composition. The statistical population-replicate mapping is not identified by S1's columns alone.

## What this independently strengthens and what is not yet identified

**Empirically grounded:** Subsequent adaptation has a heterogeneous functional scope. Numerous selected clones increase respiration at the expense of fermentation; the frequency of both-functional gains varies with ancestral genotype, source publication, treatment and ploidy class. In the source, stationary-phase responses are themselves context- and trait-dependent. This is relevant to **pleiotropy versus more modular adaptive effects in one genotype**, an external independent research programme from the E. coli auxotrophy study.

**Not identified:** the frequency of independent historical origins of reciprocal functional differentiation, the true evolutionary success rate over *all* initial evolution lineages, selection coefficients for architecture itself, two complementary coexisting specialist genotypes, organ/module duplication and retention, fixed genetic independence, or BITA `K(u)` startup/invasion threshold. The source schema does not supply a clean independent evolving-population ID for all S1 barcodes. No cluster-robust inferential p-values, meta-analysis or cross-paper pooled effect is reported. The author source provides useful *directional mechanism plausibility* and exposes design gaps, **not confirmation of trade-off-driven historical architecture evolution**.

## Reproducibility and next evidence gate

Read-only source audit and numerical regeneration are implemented as:

- `scripts/audit_bita_kinsler2024_source.py`
- `scripts/analyze_bita_kinsler2024_parent_relative.py`
- `tests/test_bita_kinsler2024_source.py` and `tests/test_bita_kinsler2024_parent_relative.py`
- `.github/workflows/bita-kinsler2024-original-author-source-audit.yml`
- Frozen aggregate inventory `empirical/trait_architecture_history/kinsler2024_author_source_inventory.json`
- Frozen parent-relative readout `empirical/trait_architecture_history/kinsler2024_parent_relative_readout.json`

Workflow reads only pinned author files, checks git-blob fingerprints and JSON equality, and fails closed on changed publication denominators, missing uncertainty columns or mismatched source-published numerators. Original entire CSVs are **not copied** to BITA.

**Next substantive independent design:** Find a study with a complete set of *founding evolutionary lineages (positives and negatives)*, genotype-linked functions of the ancestor and evolved descendants, distinct independently measured trade-off, and a longitudinal architecture transition. Another uncontrolled slice of the same selected Kinsler clone table cannot identify historical adaptation probabilities.

**Project ownership:** The active BITA mechanism-identification paper stays separate. SCH owns identification of functional conflict, SLK / historical Chapter 2 owns architecture value and evolutionary entry/retention; the present source remains scientific provenance only. **No `main` or manuscript edits, merges or external submissions.**
