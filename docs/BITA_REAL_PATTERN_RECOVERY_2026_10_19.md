# BITA main hypothesis: original-data ecological pattern recovery (2026-10-19)

## Main question, and what counts as empirical support

**Question:** When two ecological functions conflict, does investing in a partly specialized phenotype track the ecological pressure creating that conflict? Does an already structurally divided animal phenotype nevertheless retain functional/evolutionary integration?

This document is **an original-data reanalysis of previously published public studies**, not new natural-history data collection, a cross-taxon meta-analysis, or a completed test of historical shared-trait → differentiated-trait evolution.

The existing BITA theoretical question is conditional: differentiated trait architecture is globally advantageous if recovered shared-axis conflict exceeds added architecture cost (\`R-K>0\`); with an assumed front-loaded startup cost, an evolutionary fitness valley can additionally preserve balance despite a globally fitter split state. The real data below **do not measure R, K, K(u), mutation size, ancestral trait state or phylogenetic transition**. They address observable, relevant ecological predictions **upstream** of those unmeasured mechanisms.

## Plant: original HUSCAP 2025 source, not substituted 2022 Dryad

**System:** *Peucedanum multivittatum* (Japanese alpine andromonoecious Apiaceae).

- Article: Kudo & Shibata (2025), *Journal of Ecology*, DOI \`10.1111/1365-2745.70130\`.
- Article's own primary repository: Hokkaido University HUSCAP, DOI **\`10.14943/hu95572\`**.
- Exact raw ZIP: \`https://eprints.lib.hokudai.ac.jp/repo/huscap/all/95572/Kudo%24Shibata_JEcol_Data.zip\`.
- Verified ZIP SHA256: **\`07d9f718d58b795553d50c2cb2b33e9a7dd3df9e34b5c1757ed55d5674c777ca\`**.
- \`All_Plots_Data.csv\`: 685 individual rows, 5 geographic plots (HA, HL, HC, HD, KD) sampled over 2020–2023, totaling 19 plot×year contexts. Columns include numbers of perfect and male flowers, initial/final fruit, oviposition, predation fraction and height.
- \`HA_Plot_Data.csv\`: 106 individuals with direct paternity-based sired-seed measurements and estimated female output.
- Official ZIP includes the source research's R analysis script, but the analyses below are **new explicitly post-open exploratory estimands**; they do not claim to reproduce its exact GLMM parameterization.
- Two registered earlier Dryad DOIs refer to **other, older studies**. Their file contents must not be silently treated as original 2025 study data.
- No source individual-level rows/identifiers were re-uploaded to BITA or included in GitHub artifacts.

### Result A — among ecological contexts, more antagonism coincides with more specialization

Operational male-biased allocation:

    male_fraction = MflowerN / (MflowerN + HflowerN)

At the plot×year grain, 18 contexts contain predation-rate observations (one entire HA-year's predation field is missing); Spearman \`rho(male_fraction, predation_fraction)=+0.719298\`. Using the more-observed egg variable across 19 contexts gives \`rho(male_fraction, mean_eggs)=+0.745614\`.

These 18/19 points are **not independent**: the same five plots are sampled in multiple years.

After averaging available years within the **five geographic plot units**:

- \`rho=+0.9000\`, exact **two-sided p=10/120=0.08333**, using all 120 label permutations of the five plots.
- For the balanced **2022–2023 subset**, \`rho=1.0000\`, exact \`p=2/120=0.01667\`, but **this subset was inspected after data access** and must not be presented as independent preregistered confirmation.
- Each calendar-year plot rank association was positive (rho \`0.8, 0.8, 0.9, 0.9\` for 2020–2023). Year-specific signs share the same plots and are not four independent ecological replications.
- Leaving any of the five plots out of the raw plot×year descriptive comparison retains positive rho (range \`0.5607–0.7802\`), but this is sensitivity, not a cluster-valid confidence interval.

Thus **the exposure-allocation gradient is directional and persistent, with only five independent geographic plot units**. The main all-year independent-plot exact test is **not** below 0.05.

### Result B — within one ecological context, male allocation tracks less antagonist access

Define 19 plot×year fixed-effect contexts. On individual plants, the new exploratory conditional regression is

    outcome ~ male_fraction + log(1+total_flower_count) + height + plot×year FE.

Reported coefficients are after within-context centering and Frisch–Waugh–Lovell residualization, with 4,999 Freedman–Lane residual permutations restricted to the same contexts. These permutation p-values are **not automatically valid site-cluster causal p-values**; count heteroskedasticity and genotype/plant dependence remain risks.

| Response | Complete individual observations | Contexts | Male-fraction beta | Change for +0.10 male fraction | Within-context residual perm p |
|---|---:|---:|---:|---:|---:|
| \`log(1+eggs)\` | **672** | 19 | **-1.212736** | **-0.121274** log units | **0.0002** |
| observed seed-predation fraction | **511** | 18 | **-0.188544** | **-0.018854** (≈1.89 percentage points) | **0.0052** |

Leave-one-geographic-plot-out fitted slopes are negative for **all five omissions** in both responses.

**More conservative five-geographic-plot uncertainty:**

- Oviposition: delete-one-plot jackknife SE \`0.400670\`; exploratory t(4) interval for beta **[-2.32517, -0.10030]**, still below zero.
- Predation: jackknife SE \`0.086255\`; exploratory t(4) interval **[-0.42803, +0.05094]**, **includes zero**. Accordingly the plot-independent evidence for fewer eggs is stronger than for lower final predation rates.
- These are **small-five-cluster heuristic intervals**, not randomized treatment confidence intervals. Predation rates have **162/685 NA entries**; adding height and other validity checks leaves 511 for the conditional model (174 excluded). Do not silently regard missing predation as zero.

**Interpretation:** Across contexts, predation and male allocation are positively associated; **within** context, controlling total display and height, allocation toward male flowers is associated with *fewer* predator eggs on plants. This two-scale pattern is a biologically informative signature consistent with exposure-dependent allocation and potential partial functional separation. The original papers had already discussed predator-driven male-biased sex allocation; this is a transparent **independent raw-data reanalysis**, not discovery of the entire biological phenomenon.

### Result C — is paternal function preserved?

The separate HA plot paternity data comprise **106** individuals.

Exploratory pairwise rank correlations (9,999 shuffled-label permutations):

- male-flower fraction versus estimated final female fruits: rho **-0.45250**, p **0.0001**;
- male-flower fraction versus genetically assigned sired seeds: rho **-0.01499**, p **0.8786**;
- **total** flower display versus sired seeds: rho **+0.29056**, p **0.0024**.

A post-open conditional OLS \`log(1+sired_seeds) ~ male_fraction + log(1+total_display) + height\` gives beta **+0.52030**, residual permutation p **0.2216** (n=106). There is **no detected negative male-allocation association** in these metrics, but **p>0.05 is not an equivalence demonstration** and male and female relative fitness are not calibrated on one joint evolutionary currency. The negative female-output association is also partly structurally expected because more male-only flowers mean fewer seed-bearing perfect flowers at a constrained total display.

### Result D — a discriminator: fewer exposed flowers, not demonstrated active deterrence

After seeing the initial within-context association, we explicitly tested a competing **compositional opportunity explanation**: if plants have fewer perfect/seed-bearing flowers, an egg-laying moth simply has fewer valid hosts. Under fixed total display, raising the male-only fraction *necessarily decreases* the perfect-flower count. Hence the original male-fraction coefficient alone cannot tell apart avoidance through reduced host number from any additional deterrent effect of male flowers.

We fitted the identical samples/plot×year fixed effects/height controls, but replaced **log(total flowers)** with **log(1+perfect flower count)**. The difference is a post-open sensitivity across two nonnested conditioning targets, **not** a measured causal mediation fraction.

| Outcome | n | β with total-display control | β with perfect-flower control | Perfect-control residual permutation p | Five-plot exploratory t(4) β interval |
|---|---:|---:|---:|---:|---|
| log(1+predator eggs) | 672 | −1.212736 | **−0.294548** | **0.1448** | **[−1.08454, +0.49544]** |
| observed predation fraction | 511 | −0.188544 | **−0.112799** | **0.2298** | **[−0.32596, +0.10036]** |

The direct egg coefficient is considerably attenuated, and both site-level heuristic intervals include zero. On the same covariate/individual samples, these data **do not establish extra active repellence by male flowers beyond variation in the number of exposed perfect flowers**. It remains possible but unidentified. Do not turn the difference between coefficients into “percentage mediated” because the numerator, structural composition and residual causal associations are not identified separately.

### Result E — does reduced initial female opportunity pay off through retention?

For a paired **final/initial fruit** comparison, only **532/685** population rows have the required interpretable endpoints. Explicitly excluded: **77 missing required values**, **73 with zero initial fruits** (ratio undefined) and **3 with final fruits exceeding initial fruits**. These exclusions may be nonrandom, and the apparently comparable stages are not guaranteed a direct single-fruit survival trace.

Using the **exact same 532 plants**, with plot×year fixed effects, log(total flowers) and height:

| Response | Male-fraction β | Difference at +0.10 fraction | Within-context perm p | Small-five-plot t(4) 95% interval for β |
|---|---:|---:|---:|---|
| log(1+initial fruits) | **−1.790699** | −0.179070 log units | 0.0002 | [−2.40133, −1.18007] |
| log(1+final fruits) | **−1.166587** | −0.116659 log units | 0.0002 | [−2.09539, −0.23778] |
| final / initial fruit fraction | **+0.177475** | +0.017747 fraction units | 0.0082 | **[−0.06950, +0.42445]** |
| log(1+final) − log(1+initial) | **+0.624112** | +0.062411 | 0.0010 | **[−0.28036, +1.52859]** |

The common-support difference of log slopes is verified algebraically: `−1.166587 − (−1.790699) = +0.624112`. Crucially, **the exploratory five-plot intervals for both residual/retention gains include zero**. Site-wise residual-permutation p-values on hundreds of plants alone would overstate independent ecological replication. This does **not** establish a net increase in intact female output, despite numerically greater retention of the fruits that formed. The decrease in initial output is also partly deterministic: fewer perfect flowers means fewer seed-bearing opportunities.

### Interpretation after trying to falsify the apparent benefit

The strongest supported BITA-relevant signature is **conditional allocation away from an exposed seed-bearing module, with opportunity costs**, not proof of an independently evolved defensive organ. Male flowers can contribute to display/pollen-donor function without adding the same female fruit target, but the data do not establish that increasing male allocation preserves siring **equivalently** or yields higher combined male+female fitness.

The more ambitious story, “male flowers actively deter moths and improve total fitness, therefore high-antagonism environments caused modularization,” is **not supported by these data**. Under the observable, narrower story, the ecological environment can change the *value* of already-existing partial functional separation, while the evolutionary origin of that separation remains unresolved.

### Claim boundary for Peucedanum

**Recovered:** Strong directional context-dependent male-biased allocation, a within-context negative association with predator eggs when total display is controlled, and a demonstrable female opportunity cost. **When perfect-flower target number replaces total display, the extra negative egg association is no longer resolved.** The apparent post-initial fruit retention association has a five-plot uncertainty interval including zero; male allocation versus siring remains inconclusive.

**Not recovered:** Randomized effect of changing flower-class allocation, evolution of sex allocation from an ancestral architecture, joint male+female absolute fitness optimum, BITA theoretical parameters \`K\`, \`s\`, \`K(u)\`, or a mutation-fixation route. Five plots are neither five speciation transitions nor a representative sample of the plant kingdom.

## Animal: source-pinned phylogenetic integration of oral versus pharyngeal jaws

**Source:** Conith & Albertson (2021), *Nature Communications*, DOI 10.1038/s41467-021-25755-5; author's original repository andrewjohnconith/cichlid_OJPJ, immutable Git commit 575a148a6c6cb90ee957d4290cf3e2d141ca9c14.

Published oral and lower pharyngeal jaw species-mean PC1–PC5 scores are joined by **88 exact matching taxon IDs**. Each of the two CSV inputs is pinned to the author's original Git blob. The published original time-scaled Newick phylogeny is also source-pinned (full **1,712** species; Git blob SHA1 23076ac2c895a92aaf36cebfa059124ec1139bd7). Pruning to the 88 sampled species yields **87 standardized Felsenstein phylogenetic independent contrasts** under the stated Brownian branch-variance assumption.

### Previous coarse-clade calculation — descriptive, not phylogenetic correction

After standardizing separate PC axes and demeaning by coarse author-defined clade, 4,999 pharyngeal-label permutations *within* broad clades gave:

- first 3 PC dimensions: **RV=0.103462**, p **0.0058**;
- first 5 PC dimensions: **RV=0.186222**, p **0.0002**.

Diet-category associations with five-dimensional shape were oral jaw **R²=0.135143, p=0.0004** and pharyngeal jaw **R²=0.152144, p=0.0002**. The source diet categories are not a direct measurement of a capture-vs-processing trade-off, and the coarse-clade randomization is **not** a full phylogenetic analysis.

### New actual-tree analysis — positive cross-module covariation remains after PIC

Independently transform both jaw-module PC matrices into contrasts on the **same** pruned source tree. Center and standardize each contrast PC axis separately; compute RV on the paired 87-contrast matrices, and compare against **4,999 permutations of entire pharyngeal contrast vectors** (whole-vector exchangeability under the assumed Brownian model; not free reshuffling of individual PC dimensions).

| Phylogenetic assumption | n contrasts | PC axes per module | RV | p, PIC-row permutation |
|---|---:|---:|---:|---:|
| **Original source tree branch lengths** | 87 | 5 (primary) | **0.145319** | **0.0024** |
| Original source branch lengths | 87 | 3 (dimension sensitivity) | **0.138451** | **0.0006** |
| Equal branch lengths, **post-open** | 87 | 5 | **0.138304** | **0.0002** |
| Twice the original terminal branch lengths, **post-open** | 87 | 5 | **0.151200** | **0.0012** |

The central result is **not** an artifact of *only* removing the five coarse clade means: the same phylogenetic tree accounts for shared ancestry, yet oral and pharyngeal jaw evolutionary shape contrasts remain associated under this estimator. These post-open branch-variance alterations preserve the signal; they do not validate a universally correct Brownian model or identify the evolutionary cause.

**Claim ceiling:** RV of phylogenetic contrasts measures evolutionary *covariation of traits*, not direct force-motion functional performance, genetic covariance, whether residual pleiotropy persisted from ancestral jaw architecture, causal diet effects, the historical origin of two modules, or BITA's theoretical coupling coefficient lambda / architecture cost K(u). One phylogenetic assemblage with 88 sampled species is **not** 88 independent evolutionary origins of functional specialization. The author's own shape-landmark phylogenetic PLS test is a different, earlier analysis; our PC-based RV is **a new reproducible estimator on the same published system, not an independent biological replication**.

Machine-readable result: docs/BITA_CICHLID_PHYLOGENETIC_READOUT_V1.json. Code: scripts/analyze_bita_cichlid_phylogenetic_contrasts.py. Live original-tree CI: .github/workflows/analyze-bita-cichlid-phylogenetic-contrasts.yml.

## How the two taxa constrain BITA

**Plant:** allocation toward a specialized reproductive floral class correlates with antagonist exposure; within contexts it predicts both fewer eggs and fewer fruits when total display is held constant. **The egg association weakens after conditioning on the number of vulnerable perfect flowers, and five-plot intervals do not resolve greater fruit retention**. Thus the evidence concerns exposure reallocation and trade-off, not proven active deterrence or improved net fitness.

**Fish:** two functionally distinct jaw modules exhibit residual **phylogenetic evolutionary covariation** under independent contrasts (RV5=0.1453, p=0.0024, n=87 contrasts); coevolution persists across two alternative branch-length sensitivity assumptions. Morphological separation therefore **does not imply independent evolutionary shape trajectories** in this system. This does **not** identify genetic pleiotropy or the underlying adaptation route.

Those observations fit two separate components of the broader BITA architecture story. They are **not two compatible effect sizes for meta-analysis**, and the evolutionary accessibility mechanism from the 540 theoretical parameter cells is **untested** by either species-level dataset. Because the two studies and their traits were selected for conceptual relevance rather than sampled under an outcome-blind cross-taxon search, do not claim systematic universality.

## Code and reproducibility

- Exact HUSCAP source ZIP audit: \`scripts/audit_bita_peucedanum2025_huscap.py\`.
- Original tables/readout: \`scripts/inspect_bita_peucedanum2025_raw.py\`.
- Between-plot/year & paternity analysis: \`scripts/analyze_bita_peucedanum2025_population_patterns.py\`.
- Within-context conditional fit with plot omission and small-five-site uncertainty: \`scripts/analyze_bita_peucedanum2025_within_context.py\`.
- Live source and reanalysis CI: \`.github/workflows/probe-bita-peucedanum2025-huscap.yml\`.
- Vulnerable-target vs total-display exposure comparison and matched female-fruit retention: \`scripts/analyze_bita_peucedanum2025_exposure_recovery.py\`, tested with \`tests/test_analyze_bita_peucedanum2025_exposure_recovery.py\` and original-data GitHub workflow \`.github/workflows/analyze-bita-peucedanum2025-exposure-recovery.yml\`.
- Fish source-locked analysis/CI: \`scripts/analyze_bita_cichlid_public_integration.py\` / \`.github/workflows/analyze-bita-cichlid-public-integration.yml\`.
- Full tree-based cichlid independent contrasts, 1,712-tip tree, 87 PICs and alternate-branch sensitivity: scripts/analyze_bita_cichlid_phylogenetic_contrasts.py; docs/BITA_CICHLID_PHYLOGENETIC_READOUT_V1.json; .github/workflows/analyze-bita-cichlid-phylogenetic-contrasts.yml.

The data input is verified and processed by GitHub CI at its **source archive DOI**; only aggregated, source-backed receipts are uploaded. All scripts label their outputs as observational/exploratory and fail closed on corrupt inputs.

**Next substantive step:** Test prospective predictions across additional phylogenetically independent biological systems with *commensurable* trait-function conflict and modularity measures. Independently estimate the relative shared/differentiated fitness load, coupling, construction cost and genetic accessibility before claiming the proposed evolutionary barrier occurred in nature.
