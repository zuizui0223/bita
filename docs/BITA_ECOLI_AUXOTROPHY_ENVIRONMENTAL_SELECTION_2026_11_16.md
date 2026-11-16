# Environmental compensation permits evolved functional loss: an original source-figure audit

Date: 2026-11-16. **One additional independent experimental-evolution research programme**; source-verified figure-level outcome reanalysis. The source paper is D'Souza & Kost (2016), *PLOS Genetics*, DOI [10.1371/journal.pgen.1006364](https://doi.org/10.1371/journal.pgen.1006364), original [PMC5096674](https://pmc.ncbi.nlm.nih.gov/articles/PMC5096674/).

This is not a new wet-lab experiment, a historical origin of reciprocal division of labor, a random sample of naturally selected specialized systems or an empirical calibration of BITA's activation cost K(u).

## What is new in this branch

The parent BITA forward-division-of-labour PR #375 addressed a **positive-fan-selected** Wsp genotype panel: it does not contain the parent all-colonies denominator. This independent E. coli study begins with **one common prototrophic ancestor**, then independently evolves **8 populations with 20 externally supplied amino acids** and **8 in the absence of exogenous amino acids**. For each population at each figure sample, the authors plated and phenotyped **1,000 colony isolates** for growth without amino acids. The **biological replication unit is the evolved population** (8 per arm), not the 1,000 plated diagnostic clones or the 96 repeated population×timepoint visual cells.

Original primary data provenance:

- Publisher [Figure 2 original full-resolution PNG](https://journals.plos.org/plosgenetics/article/figure/image?size=large&id=10.1371/journal.pgen.1006364.g002), **3,233 × 3,124 pixels**, SHA-256 `71da8f3c1707d1ade887d4030446d1869f9fd33b05fa8cfed6fb3cd49823bd8b`.
- Original [Europe PMC full-text JATS](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5096674/fullTextXML), SHA-256 `6eb810ff515b2aa0a7ccb4190067e97810e7cbaca26bc2947d1ef720f77e0e97`.
- Original PLOS supplementary PDFs: [S1 Table](https://journals.plos.org/plosgenetics/article/file?id=10.1371/journal.pgen.1006364.s004&type=supplementary) SHA-256 `249f0657f5ce93f155b6ef9b23a59437f5c205ddc3436ea1fdbf71db37074ca7`; [S2 Table](https://journals.plos.org/plosgenetics/article/file?id=10.1371/journal.pgen.1006364.s005&type=supplementary) SHA-256 `a0bc2dbb9a4bf5c590bb59cfce226986bfa1bdd94274489ebae25413d70b2ab4`; [S3 Table](https://journals.plos.org/plosgenetics/article/file?id=10.1371/journal.pgen.1006364.s006&type=supplementary) SHA-256 `3047c6a82418eb18378f1d60546f88656db6c9a7ce237ab7bcd9196235dfb0af`.
- Exact original pixels, not visual guesses about the source image: `scripts/analyze_bita_ecoli_auxotrophy_fig2.py` samples the inner center and four offsets of each source Figure 2 A/B heatmap cell, with **fail-closed black-versus-pink classification**, original figure size and original image SHA gates. It recovers **96 source-published color cells (2 regimes × 8 evolved populations × 6 generations)**. These are **categorical detection indicators only**. PLOS figure color shades encode approximate proportion categories, not exact raw colony counts.

## Evolved populations with detectable auxotrophs

| Generation | With environmental amino acids | Without amino acids |
|---:|---:|---:|
| 0 | 0 / 8 | 0 / 8 |
| 250 | 0 / 8 | 0 / 8 |
| 500 | 0 / 8 | 1 / 8 |
| 1,000 | 4 / 8 | 0 / 8 |
| 1,500 | 2 / 8 | 2 / 8 |
| **2,000** | **6 / 8** | **0 / 8** |

The **same clock time endpoint** at generation 2,000 yields an **observed difference of +75 percentage points (6/8 vs 0/8)**. This is a newly computed **exploratory post-source** two-sided Fisher exact **p=0.00699300699**, with Wilson–Newcombe **95% interval [+27.95,+92.85] percentage points** for the difference. These exact n=8 counts have been independently recalculated with SciPy Fisher and statsmodels confidence interval code in the source audit workflow. The original article reported the 6/8 (75%) final prevalence for the AA regime; the exact two-arm comparison is a new post hoc effect readout from published heatmap colors, **not a preregistered experiment-level hypothesis test**.

The presence/absence matrix is **NOT** an incident-event panel. From the source figure, **7/8 AA lines** and **3/8 non-AA lines** had at least one detectable auxotroph across the six inspection times. An AA line (R1) detected auxotrophy at 1,500 generations but not at 2,000. In non-AA, all three previously detected positive line IDs have no positive heatmap cell at 2,000. Non-detection in 1,000 screened colonies at the endpoint does **not prove that mutations never arose or that the genotype became extinct**: the population-level auxotroph frequency may simply fall below the screen detection threshold. Do not analyze all 96 figure cells as 96 independent evolution lines, infer exact mutation origin time from the first positive heatmap cell, or treat a cell's pink shade as its raw number of auxotrophic CFUs.

**Environmental identification boundary:** amino-acid supply affects the **selective benefit of losing biosynthesis**, but also causes differences in total evolved population density and hence mutation opportunities. The study documents direct competitive advantages of selected auxotrophs in externally supplied conditions; the figure comparison does **not independently isolate selection strength from mutation supply, crossfeeding abundance, or genotype-specific selection**. Auxotrophy is a **one-way metabolic dependency** that can be rescued by supplemented medium; it need not represent reciprocal functional division between two lineages.

## Two source-internal quality discrepancies newly exposed

The source figure and primary Results are not completely mutually consistent:

1. **Lineage label discrepancy:** the primary Results text describes the non-AA 500-generation auxotroph detection as **R3**, while the original Figure 2 B heatmap marks **R2**. Neither alternative changes the timepoint-level count of **1/8** or the generation-2,000 comparison, but **lineage-ID-specific evolutionary origin claims must be suspended** pending author/source clarification.
2. **Strain count discrepancy:** supplementary **S1 Table** lists **60**, **256**, and **157** assayed auxotrophic strains at generations 1,000, 1,500, and 2,000 in the AA-supplemented treatment, summing to **473**. The primary Results text reports **n=483** AA-derived strains for the trait-count analysis. The non-AA S1 counts **18+19=37** agree with the paper's n=37. No unexplained 10-count discrepancy was filled, discarded, or reclassified to force agreement. These isolate counts are **not** independent founding population counts.

The S2 original supplemental mutation annotations record **18 structural and 19 regulatory** annotation occurrences associated with auxotrophs (vs 5 and 6 respectively among sequenced prototroph backgrounds). These values count genetic annotation **events**, not 37 independent genotypes/lineages. S3 original Table contains **six AA-evolved auxotroph genotypes, two non-AA-evolved auxotrophs and six matched prototroph genomes**. These are a deliberately selected sequenced subsample of the 16 original evolution populations; do **not** treat eight sequenced auxotroph genomes as eight independent adaptive origins or extrapolate them to mutation target frequencies among all evolutionary lineages.

## Original raw Dryad data access: still unresolved, not falsified

The original article's Data Availability names [Dryad DOI 10.5061/dryad.9b47j](https://doi.org/10.5061/dryad.9b47j). The official public API returned the dataset manifest with two original files:

- `Data_from_Dsouza_Kost_2016.xlsx` (**131,418 bytes**, advertised **MD5-format** digest `05526ec2e2507d8ad14dfd2487be3f18`);
- `Genome_diff_evolved_mutants.zip` (**216,828 bytes**, advertised **MD5-format** digest `b1a32507e0d57ece016ca383f6469e73`).

Authenticated-looking official file download URLs responded **HTTP 401** anonymously, and no original raw file bytes were downloaded. The file metadata's 32-character values are **MD5-format digests, not verified SHA-256 hashes**. This branch therefore offers the source-authorized **figure-level category analysis**, not a full replicate-by-time trajectory model or a reanalysis of the author's unabridged original genome changes. No access restrictions were circumvented.

## Connection to the SCH–SLK–BITA research boundary

This data answers a more precise question than a positive-only division-of-labour vignette: **under a matched ancestral genotype, when does environmental access to a formerly self-supplied function predict detectable evolved loss of that function?** It directly provides **16 independent evolving populations with both positives and negatives**, a common 2,000-generation horizon, and source-verifiable trait-loss status. It supports selection/accessibility of *metabolic dependency*, but not **the initial advantage of splitting two jointly optimized functions into separate persistent organs or reproductive specialist species**.

The broader specialization theory predates this project (e.g. Rüffler, Hermisson & Wagner 2012, DOI 10.1073/pnas.1110521109). The canonical BITA mechanism-identification paper is frozen separately in `manuscript/CLAIM_FREEZE.md`; architecture gain/accessibility/retention belong to SLK or the historical Chapter 2 research programme, not to the current BITA identification manuscript. This record is a new empirical **technical provenance** source, not authorization to reassign the manuscript's scientific claim.

## Reproduction

Run original-source verification GitHub Actions `bita-ecoli-auxotrophy-fig2-original-test.yml`: downloads Figure 2 PNG, JATS and three source supplementary PDFs with exact SHA gates; scans all 96 original figure color-cell interiors, fails on ambiguous colors or altered source lineage totals; source-checks the Table S1 473-versus-483 conflict, S2 annotation counts and S3 selected genome IDs; recomputes the generation-2,000 2×2 exact test and 95% interval; independently checks via SciPy and statsmodels; and requires the newly produced result to match the committed frozen `empirical/trait_architecture_history/dsouza2016_aa_auxotrophy_fig2_readout.json`. Full copyrighted original PLOS file bytes remain outside the GitHub repository.

Source-readout remains Draft PR #376. No `main` merge, journal submission, full raw-source redistribution or active BITA manuscript edits.
