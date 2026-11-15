# BITA: The evolutionary exit from specialist architectures is experimentally accessible

**2026-11-15 — independent original-paper data recovery.** This is one additional bacterial evolutionary research programme. It tests the **reverse direction**, specialization-to-autonomy, and is not a test of the original historical origin of BITA's shared-to-split architecture.

## Main independent experimental case

**Chen et al. (2024), PNAS**, DOI [10.1073/pnas.2317182121](https://doi.org/10.1073/pnas.2317182121), [full PNAS original source (PMC11363282)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11363282/). An artificially separated `Pseudomonas stutzeri` naphthalene degradation pathway is partitioned between **Degrader** (naphthalene → salicylate) and **Detoxifier** (salicylate → further intermediates). The researchers serially evolved the mixture under three carbon-supply conditions for roughly 270–280 generations.

The exact deposited original XML was recovered directly from [Europe PMC fullTextXML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11363282/fullTextXML) and locked to SHA-256 **`64bfc840381c06b3fd417da5ea068a51d9c1854e67af22b8b7a54e54cc3494d6`**. The independent unit is an **experimental evolution population**, not a sequenced clone, time point, published figure, or parameter set.

### Primary started-cohort comparison

| Evolution condition | Autonomist evolved / originally started populations | Censoring/interpretation |
|---|---:|---|
| Constant mutualism (naphthalene every cycle) | **0/12** | Two lines became extinct after ~50 generations, leaving 10 in the later evolutionary analysis |
| Constant competition (pyruvate every cycle) | **0/12** | All 12 original lineages analyzed |
| Alternating mutualism and competition | **5/12** | Independent successful line IDs **1, 4, 6, 7, 11** |

**New post-publication exact tests**, conditional on the published population-success counts:

- **Fisher–Freeman–Halton 3×2 omnibus, probability-ordered two-sided**: **p = 0.0063025210** for `0/12, 0/12, 5/12`. This tests differences across all **three** regimes, not a pooled constant-regime `0/24` surrogate.
- **Censoring sensitivity**: treat the 2 extinct constant-mutualism lines as unavailable rather than nonsuccesses, giving `0/10, 0/12, 5/12`: exact omnibus **p = 0.0065982405**.
- Descriptive difference between fluctuating and each constant arm: **+41.67 percentage points**. Individual one-constant-arm Wilson–Newcombe 95% interval **[+8.69, +68.05] percentage points**, but all these tests are **post hoc**.
- Each exploratory two-sided 2×2 Fisher comparison `5/12 vs 0/12`: unadjusted **p = 0.0372671**; Holm-corrected **p = 0.0745342** across the two pairwise comparisons. Therefore, we **do not claim both pairwise comparisons individually significant at 5% after adjustment**.
- Constant-mutualism survivor-only pairwise sensitivity `5/12 vs 0/10`: Fisher two-sided **p = 0.0396446** (before adjustment).
- The source original 5/12 success proportion has 95% Wilson CI **[0.1933, 0.6805]**, reflecting uncertainty in this one experimental programme. No long-term natural prevalence estimate.

No re-randomization, preregistered power analysis or original longitudinal line-level observation matrix has been obtained. Exact test calculations assume the independent population assignments are exchangeable under a null with equal event probabilities and condition on the observed number of successful lineages. The two original extinctions were documented by the authors; they are **not retroactively edited out without sensitivity reporting**.

### Original genetic evidence is stronger than morphology or function alone

The authors recovered **four clones from each of the five successful populations** (20 selected isolates; not 20 independent evolutionary transitions). All examined isolates regained previously deleted functional genes at the ancestral genomic loci, consistent with homologous recombination and horizontal gene transfer (HGT). Original DNA-barcode ancestry implies **three independent successful lineages descend from Degrader and two from Detoxifier**. The authors consider DNA transformation a plausible transfer mechanism, but there is no direct real-time video/measurement of the exact DNA exchange events. The five independent outcome counts are original population-level histories, while the 20 isolate genome assays are **nested validation evidence**.

### Experimentally separating ecological opportunity from selection

With **constant naphthalene**, Autonomist has a fitness advantage but the complementing Detoxifier tends to vanish, reducing donor–recipient encounter and HGT opportunity. With **constant pyruvate**, coexistence and high cell density improve, but autonomous naphthalene degradation is not selected. Alternating substrates can therefore combine **(1) donor–recipient coexistence and high mutation/exchange opportunity** with **(2) selection favouring the reassembled function**.

In *independent new* constant-mutualism experiments, manually **reintroducing Detoxifier** raised observed Autonomist establishment to **3/12**; doing so at **higher inoculum density** yielded **6/12**, after 22 generations. The two new arms are **separate cohorts**, not repeated measurements of the original 12 constant-mutualism lines:

| New treatment | Evolved independent lineages |
|---|---:|
| Readd Detoxifier, initial OD600 0.05 | **3/12** |
| Readd Detoxifier, initial OD600 0.10 | **6/12** |

Descriptive density difference **+25 percentage points**; its exploratory two-sided Fisher **p = 0.4003**, 95% Newcombe interval **[−12.46,+54.42] percentage points**: **not resolved as a statistically different rate with n=12 per treatment**. The original reported approximate OD600 in the pyruvate versus naphthalene cycles is **~1.0 vs ~0.4**, but these are descriptive source values rather than an estimated controlled mediation effect of biomass on HGT.

The source paper's **mathematical model** assumes the emergence rate of reassembled genotypes rises with the **product of both specialist biomasses**. BITA can reuse the qualitative structure as an *unmeasured evolutionary-accessibility component*, e.g.

```
H_exit(T) = integral_0^T [HGT/functional-reassembly opportunity at t]
                         × [establishment conditional on the current environment] dt
```

This is a **conceptual hypothesis and attribution to the published source model**, not a newly measured real-world hazard or an identity with BITA's theoretical startup barrier `K(u)`. Even a locally stable differentiated functional state can cease being realized in a mutation/HGT-capable population: local optimum and absence of genetically accessible exits are different hypotheses.

## Separate source model simulations: never add to the 36 experimental cultures

Under their baseline model parameterization, the paper reports **59/100** simulation outcomes with Autonomist under fluctuation, **16/100** under constant mutualism and none under constant competition. Across **17,501 model parameter sets**, **2,269** produced autonomy only under fluctuation, **1,003** only under constant mutualism, **10,633** under both, and **3,596** under neither. These four partition cells sum to 17,501 and **are not 17,501 biological species, independent experimental origins, or empirical meta-analysis replicates**. Their broader variation demonstrates model dependence and is a warning against turning the experiment's experimental-exclusive 5/12 pattern into a universal law.

## Revised cross-system mechanism picture

The new study is independent from the preceding Bacillus, Pseudomonas aeruginosa, yeast Fcy1 and E. coli fluorescent protein data, but **different outcome currencies and interventions prohibit a pooled numerical specialization effect**.

1. **Forward common ancestor → specialised ecotypes:** Yang et al. (2020) [DOI 10.1128/AEM.00051-20](https://doi.org/10.1128/AEM.00051-20), in **one E. coli experimental history**, reports a reconstructed evolved three-ecotype crossfeeding community with higher yield/competitive fitness than its ancestor. The original source fit is not rerun here.
2. **Engineered specialization can improve short-term output but disappear by genetic adaptation:** Dragoš et al. (2018), Bacillus [DOI 10.1016/j.cub.2018.04.046](https://doi.org/10.1016/j.cub.2018.04.046) and [follow-up DOI 10.1038/s41564-018-0263-y](https://doi.org/10.1038/s41564-018-0263-y). They are **one related Bacillus programme**; current source-pinned evidence includes two evolved TasA-Cys lineages and partner swap, not a raw CFU time-series.
3. **Genetic reassembly by HGT creates autonomous organisms from an engineered two-species functional consortium:** Chen et al. (2024), **this P. stutzeri programme**, with five original independent autonomist-evolution replicates under alternation and 3/12–6/12 readdition experiments.
4. **Frequency-dependent coexistence without group output gain:** Mridha & Kümmerli (2022), [DOI 10.1111/jeb.14001](https://doi.org/10.1111/jeb.14001), P. aeruginosa iron acquisition specialists; the prior analysis uses **published t statistics** because the raw Dryad XLSX required authorization. Distinct Pseudomonas species and laboratory programme: do not count it as a paired replication of Chen.

The cross-system conclusion is **not** that all systems alternate between architectures, nor that functional division has a universal positive/negative pooled effect. Instead, three **separately identifiable axes** emerge: (i) opportunity for current differentiated architecture to produce value, (ii) coexistence/assembly constraints in the current population, (iii) accessibility and selective establishment of alternatives, potentially *including autonomy*. Fixed-genotype coexistence is **not an evolutionary guarantee** of differentiated architecture retention.

## Technical artifacts, claim ceiling and decision

New original-JATS parser and exact statistics: `scripts/analyze_bita_autonomy_reversal.py`; independent numerical and source test contracts: `tests/test_bita_autonomy_reversal.py`; source results JSON: `empirical/trait_architecture_history/chen2024_autonomy_reversal_readout.json`; cross-program source type and independence ledger: `empirical/trait_architecture_history/bita_forward_reverse_programmes_20261115.csv`.

Source-retrieval Actions commits the original publisher JATS to an **ephemeral run artifact** with SHA-256, then a second workflow recomputes and independently checks Fisher and Wilson–Newcombe results. The original published XML is not republished in this repository. Only scientifically essential source-provenance references and derived calculations are tracked.

**Not identified:** historical selection causing the **original separation** of the two metabolic functions, a within-line experimental specialization→autonomy→specialization loop or BITA hysteresis, a calibrated startup cost `K(u)`, identical conditional effect scales across species, or a natural frequency of trait splitting. This is an **independent reverse-transition experiment**. Retain all changes as **Draft**. No `main` merge, external study submission, manuscript modification or raw-source redistribution.
