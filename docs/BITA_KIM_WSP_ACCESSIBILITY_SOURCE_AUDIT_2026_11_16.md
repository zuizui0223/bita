# BITA source boundary: evolutionary accessibility of a new complementary Wsp morphotype

Date: 2026-11-16. **One published Pseudomonas fluorescens research programme**; exploratory source reanalysis of source-identified representative genotypes and engineered controls, not a new biological experiment, mutation rate or meta-analysis.

## Why this source was re-opened

Kim, Levy & Foster (2016), *Nature Communications* DOI [10.1038/ncomms10508](https://doi.org/10.1038/ncomms10508), reported that a mucoid M *P. fluorescens* parental background gives rise to dry/wrinkly D mutants; mixed M+D colonies spread and achieve greater CFU output than either genotype alone. The main paper explains an extracellular wetting polymer supplied by M and D's pushing role. The Wsp signalling/c-di-GMP pathway is the chief repeated genetic route.

The forward-differentiation register in [parent PR #374](https://github.com/zuizui0223/bita/pull/374) correctly records **20 dry isolates sequenced, each from a selected spreading fan arising from a separately plated M colony**. It does **not** provide a count of all founded colonies, including those that never produced fans. The source was reopened to see whether the **mutation identity of each of the 20 selected D colonies** is actually available.

## Actually recovered original supplementary PDF

Publisher's original [Supplementary Information PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fncomms10508/MediaObjects/41467_2016_BFncomms10508_MOESM747_ESM.pdf), 9 pages, 1,263,822 bytes, source SHA256 **`deadd620be9018aa3b7f196971a243c703a69db50e49364fe17f6d667a671475`**. Author Supplementary Table 2 is **PDF page 7**. Article main JATS (PMC4748119) SHA256 **`a876e838044cb44ab28c47a1f9e243df3172c15650ad52f56be1e1a1d5c8ab68`**. The PDF was visually rendered and the table inspected, as well as machine-extracted with text-word positions and four original source columns (strain/genotype/phenotype/reference).

**Original Table 2 contains exactly 26 source strain entries:**

| Source category in the table | Entries |
|---|---:|
| `Evolved isolate` | **5** |
| `Constructed isolate` | **19** |
| Previously reported M ancestor and WT parent | **2** |
| **Total** | **26** |

The five source-labelled evolved strains are **four Dry representative variants plus one Mucoid evolved return variant**. The four distinct labelled D constructs map to three Wsp gene targets:

| Selected representative evolved Dry genotype | Source variant | Locus |
|---|---|---|
| `Pf0-1DV (D)` | `wspCΔ1269-70`, a two-base coding deletion making WspC:D fusion | **wspC** |
| `WspAΔ850-933` | `wspAΔ850-933`, 84-nt in-frame deletion | **wspA** |
| `WspAA381V` | `wspAC1142T`, coding A381V | **wspA** |
| `WspED648G` | `wspEA1943G`, coding D648G | **wspE** |

The **fifth evolved** source strain `wspE#` has `WspAΔ850-933 (wspEC134A)` background and regained **Mucoid** phenotype. This is a reported D-to-M phenotypic return in an already-mutated WspA background; it is **not a fifth de novo M-to-D source pathway**.

**Do not write that two of twenty independent D origins were wspA, one of twenty wspC, and one of twenty wspE.** The four evolved Dry strains in Table 2 are representative *reference strains* for this paper. The original Methods' 20 separately selected, sequenced D variants are **not all represented as 20 individually labelled mutation calls in Supplementary Table 2**. Thus, among the selected twenty, the relative frequency of each Wsp locus and allele is **not identified** here. Nor is the probability of a spreading fan among all original M colonies.

## Critical source discrimination: evolved versus engineered

The published **engineered** `wspC:D` strain has exactly the same WspCD fusion coding change as the evolved reference `Pf0-1DV (D)`, and has Dry morphology. This is a molecular **reconstitution control**, not a second natural evolved origin.

Constructed **ΔwspC**, **ΔwspD**, and **ΔwspCΔwspD** strains all remain Mucoid in the original table. That distinguishes the source's WspCD fusion phenotype from a simple null knockout of each whole gene. Constructed polymer-negative **M***, genotype `ΔPfl01_3834`, is Non-mucoid and in the original main paper fails to spread with D. This supports a complementary wetting/pushing mechanism, but **the table itself contains strain categories and dry/mucoid morphology, not independently measured new group-fitness effects**.

Additional labelled transposon insertions and fluorescent/antibiotic marker constructs are also deliberately included among the 19 constructed entries. Neither an engineered mutation nor a marker cassette is an evolutionary repeat.

## Mechanism and novelty placement

Evidence is positive for:
1. **Genuinely de novo emergence** of a complementary D morphotype from separately plated M ancestors (the main paper's selected-fan design);
2. **Multiple genotypic access routes** to a similar D phenotype (WspA, WspC and WspE among four labelled representative strains), including a specific reconstructed WspC:D gain/rewiring control;
3. **A reverse access route** from evolved Dry WspA background to Mucoid state via WspE change.

Evidence is **not** available here for:
- mutation rate, proportion of all original colonies that evolve DoL, target frequency among the twenty sequenced selected-fan isolates, or unbiased genotype fitness distribution;
- original M being an optimized **ancestral two-function generalist**: the source M already has an `rsmE` frameshift producing wetting polymer;
- stable inheritance of permanently specialized organismal trait axes across species;
- BITA's proposed front-loaded startup cost `K(u)`, local versus global division threshold, or historical phenotypic hysteresis;
- a new finding of the general functional trade-off mechanism. Rueffler, Hermisson & Wagner (2012), DOI [10.1073/pnas.1110521109](https://doi.org/10.1073/pnas.1110521109), already derived general fitness-landscape conditions for division of labour. The Kim evidence is an **experimental mutational accessibility example**, not a novel general performance-curvature theorem.

**Internal paper ownership:** the repo's `manuscript/CLAIM_FREEZE.md` and canonical `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` currently allocate architecture benefit/accessibility to **SLK**, while active BITA focuses on **identifying ecological channels of observed trait interaction**. This dossier is source-checked **legacy Chapter 2 / trait-architecture technical provenance**, NOT authorization to expand the active BITA identification manuscript or rewrite the already-frozen publication division.

## Reproducibility

`scripts/analyze_bita_kim_wsp_source.py` reads **original PDF page 7 using word coordinates** and revalidates the original main article Methods statement that 20 independently selected positive fans were sequenced. The source audit uses both file SHA256 values and rejects changes in table structure, allele labels, genotype provenance, evolved/constructed class totals or source Methods.

`empirical/trait_architecture_history/kim2016_wsp_table2_readout.json` records all 26 source strain rows with their genotype and reference provenance. `tests/test_bita_kim_wsp_source.py` checks counts, reconstructed fusion, all three Wsp deletion negative controls, the sequential WspE return, and refusal to make all-colony incidence claims. The source PDF and full copyrighted original article XML remain in read-only GitHub Actions artifacts, not rehosted in the repository.

This source-only addition remains in Draft PR #375, unmerged. No changes to `main`, canonical manuscript, SLK results or journal submission.
