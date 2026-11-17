# Pineau et al. 2024: source-bounded forward divergence and maintenance of two evolved specialist lineages

Date: 2026-11-17. **Standalone independent publication added as a research-programme-level biological evidence route**, stacked on Kinsler 2024 Draft PR #379; no change to `main`, the active BITA mechanism-identification manuscript, the Ecology Letters access-routing Letter, or the SLK theoretical statement.

## What this independently addresses

Pineau R. M. et al. (2024), *Nature Ecology & Evolution* **8:1010–1020**. DOI **[10.1038/s41559-024-02367-y](https://doi.org/10.1038/s41559-024-02367-y)**, PMCID **PMC11090753**. [Publisher source](https://www.nature.com/articles/s41559-024-02367-y). The system is *Saccharomyces cerevisiae* snowflake yeast from a **common, engineered ACE2-deletion multicellular founder**, undergoing sequential growth and gravitational-settling selection. Compared with the earlier D'Souza auxotrophy presence/absence and Kinsler selected-clone pleiotropy, this gives **new lineages with divergent functional niches and documented coexistence within a real evolving population**.

Do not reinterpret this as de novo construction of an organ, permanently genetically isolated gene module, or obligate reciprocal cellular labour division. Here the unit of specialization is **alternative, coexisting multicellular yeast genotypes**, with Small better at growth through oxygen capture and Large better at surviving size-selective settling.

## Original biological denominator and the five line outcomes

Five *independently evolving* obligately aerobic (PO) populations were passaged over **715 daily transfers**, estimated at approximately **4,300 generations**; the study contains five populations each of two additional metabolic regimes (PM and PA), but only the PO treatment is directly quantified by the published uniform t715 isolate-screen outcome. Each PO population was characterized with **10 isolated small + 10 isolated large clusters**. These 100 isolates are within-line assay samples, **not n=100 independent evolution experiments**.

The paper's Extended Data Figure 1 and Results assign the following outcomes:

| Original evolving line | Large-isolate/small-isolate **cluster volume** fold | Author-coded t715 dimorphism |
|---|---:|---|
| PO-1 | 2.0× | not clear |
| PO-2 | 1.5× | not clear |
| **PO-3** | **37×** | detected |
| **PO-4** | **27×** | detected |
| **PO-5** | **16×** | detected |

**Empirical result**: **3/5 independent aerobic evolved populations** exhibited the large-small dimorphism (two do not). The study provides both positive and negative evolution-line denominators. A new, descriptive 95% Wilson interval for the observed 3/5 is **[0.231, 0.882]**, broad because the genuine sample size is five. It is **not** a universal evolution-origin frequency, and the classification is based on the authors' phenotypic measurement and judgement, not a preregistered 10× threshold selected here.

**Non-aerobic context is contextual, not a second equal endpoint cohort.** Authors state that no equivalent dimorphism emerged in the mixotrophic and anaerobic MuLTEE trajectories, each with five evolution lines. However, their accessible comparison includes earlier experimental screens and metabolic/genetic differences; a source-equivalent all-three-regime t715 20-isolate-per-line denominator is not established here. We do **not** promote `3/5 versus 0/10` to a matched exact treatment effect or estimate the causal probability of diversification under aerobic versus non-aerobic conditions.

## Mechanism and persistence are separate from origin prevalence

**Lineage divergence.** The source reports genomic evidence from PO-3 Large and Small isolates whose genetic changes are non-overlapping, supporting a deep ancestral split. This is not complete genetic tracing for all five evolution populations, and the original authors do not identify a two-module ancestor with a quantified internal allocation cost.

**Maintenance experiment.** In competitions of one selected PO-4 Small/Large pair, standard oxygen availability (~26% present atmospheric level, PAL) produces negative frequency dependence and convergence on **approximately 9% Large**, despite varied initial frequencies. Providing supplemental oxygen (~84% PAL) increases the Large proportion to roughly **86%** in a *different competition assay*. These are phenotype frequency outcomes within the **already differentiated** pair, **not new de novo divergence events**. The descriptive +77-percentage-point shift between rounded published fractions does not carry a between-evolution-population CI.

**Original author's analysis-script numerical recovery.** Figure 2 MATLAB source `F2.m`, from [Ratcliff-Lab/coexistence-paper](https://github.com/Ratcliff-Lab/coexistence-paper), pinned to Git commit `071affa79f16f0a469f099058372a7488c35c0c2` (file Git blob SHA-1 `4b5dba14b244b335294ca28be52a77c5dc278d79`) reports a fitted per-competition **Large frequency change**:

```text
Delta frequency(Large) = +0.095083 - 1.0274 × starting frequency(Large)
Estimated zero-change frequency: 0.095083 / 1.0274 ≈ 0.09255
```

This is a source-code-derived re-expression of its **already fitted** slope/intercept, not an independent refit to the eight raw competition trajectories or a new ecological effect. It recovers the published equilibrium value near 9.3%. **Eight competitions do not increase the n=5 evolutionary-origin denominator**.

**High-O₂ assay-n audit:** The source code plots **7 high-O₂ series**, while the publisher's Figure 2 caption refers to **n=6**, and the Methods separately describe an experiment beginning with **five replicate populations**. These three numbers need not represent the same samples or definition. Without reconstructing the underlying workbook/experimental metadata, the difference is **unresolved** and not "fixed" by choosing one. Our result does not calculate a high-O₂ pooled standard error or a 7/6/5 population test.

## Explicit biological explanation and surviving alternatives

The source-backed causal *maintenance* interpretation is that oxygen diffusion and limited resource access reduce the growth performance of Large clusters, while settling selection rewards their larger size. When Large becomes frequent it incurs a resource-competition disadvantage; when rare its settling advantage allows it to persist. This creates a frequency-dependent ecological niche split.

The contribution to the historical SCH–SLK–BITA Chapter 2 programme is **direct positive evidence for the forward emergence of alternative specialized phenotype lineages from one ancestor** and for ecological retention under a specific growth-versus-survival trade-off. This is substantially stronger than merely finding separate positive/negative functional effects in randomly selected evolved clones.

The remaining claim boundary is strict: the evidence does **not** establish that a single individual was historically balanced at both functions, that physical/genetic submodules were duplicated or split, or that BITA startup `K(u)`, functional conflict `L`, invasion and persistence thresholds have been estimated from these data. The theoretically modelled `L → R → Phi → accessibility → invasion → fixation → occupancy` chain belongs to SLK, and the active BITA paper still owns **trait interaction ≠ ecological mechanism**. Do not reassign the observed trade-off to an identified BITA `W_AD` allocation.

## Verified source and reproducibility limitations

- Published article and original [Europe PMC deposited full text](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11090753/fullTextXML), checked by DOI and exact 3/5 line statement.
- Author code `F2.m`, Git blob SHA-1 `4b5dba14b244b335294ca28be52a77c5dc278d79`, used for source-equilibrium reconstruction.
- Original public [12-sheet source workbook](https://github.com/Ratcliff-Lab/coexistence-paper/blob/071affa79f16f0a469f099058372a7488c35c0c2/data_used_to_generate_figs_in_coexistence_paper.xlsx), Git blob SHA-1 `8f7d01b388489374aba210db96495f387d4338e2`. Binary bytes are SHA-gated in an ephemeral read-only workflow. **The workbook's internal cells, the original trajectory data and SRA raw reads are not reanalyzed.**
- Script `scripts/audit_bita_pineau2024_forward_divergence.py` + tests `tests/test_bita_pineau2024_forward_divergence.py` + isolated read-only Actions workflow. Derived-only canonical JSON is frozen in `empirical/trait_architecture_history/pineau2024_original_forward_divergence.json` after the first successful original-source execution.
- No third-party raw records or full copyrighted publication text are copied to BITA.

**Status and next experiment:** Independent forward differentiation and ecological maintenance are observed. The next decisive test must measure the *whole ancestral two-function performance and architecture cost* before and after differentiation, with the **number of all originally started evolution lines and failed origins**, plus genotype-matched function and fitness across consumer/resource environments. Do not pad the current one-programme evidence with clone- or competition-level pseudo-replication.
