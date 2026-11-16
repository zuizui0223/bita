# BITA forward architectural differentiation: two *observed* microbial mechanisms (2026-11-16)

**Status:** original published-study JATS audited and machine-read; original wet-lab replicate vectors not obtained. These are independent **research programmes**, not the new discovery of differentiation, a systematic sample of all microbial research, or the identification of a universal evolutionary rate. This evidence is complementary to PR #373's separate **specialist → autonomy** evolution study.

## 1. Direct de novo emergence of a new partner — Kim, Levy & Foster (2016)

Primary publication: [*Nature Communications* DOI 10.1038/ncomms10508](https://doi.org/10.1038/ncomms10508), original [PMC4748119](https://pmc.ncbi.nlm.nih.gov/articles/PMC4748119/). SHA-256 of original Europe PMC JATS: `a876e838044cb44ab28c47a1f9e243df3172c15650ad52f56be1e1a1d5c8ab68`.

- Starting genotype **M** of *Pseudomonas fluorescens* is **not a demonstrably optimal generalist of two original functions**. It already has an *rsmE* frameshift that creates a mucoid/polymer-producing state. Clonally plated M repeatedly generates distinct dry/wrinkled **D** mutants from local spreading fans.
- Original Methods specifically state **20 dry morphotypes, each selected from one spreading fan of a separately isolated M colony**, underwent *wsp* sequencing. The Results say all tested types had one *wsp* mutation, with examples including a 2-nucleotide *wspC:D* in-frame fusion and *wspE*/*wspA* regulatory variants.
- These 20 are **chosen positive fans, not all plated founding colonies**: do not report an origin frequency 20/20, 20 independent research studies or a mutational rate.
- **Functionally discriminating manipulations**: M supplies an extracellular mucoid wetting polymer; D lies behind it to push the spreading front. A mixed M+D colony spreads and has more CFU than either single-colony state (original Figure 1 mixed-vs-single CFU ANOVA **p=0.000957**; individual Tukey comparisons p<0.01). The polymer-deficient **M*** lacks the source mucoid lubrication and loses spreading despite D's presence (original Figure 4 ANOVA **p=0.000167**). Engineering the 2-nt *wspC:D* change re-creates the D phenotype and partner-enabled spreading.
- At fixed-genotype mixing frequencies, the population converges to roughly **10% M and 90% D**, regardless of starting mix, demonstrating condition-specific negative frequency dependence. Source Figure 2 averages **three colonies per initial mixing ratio**, not three newly originated evolved D lineages per plotted time.
- Bidirectional *reappearance of a missing complementary morphotype* is reported by the paper, including re-emergence after loss of Wsp signalling by different mutation targets. This is not historical restoration of a two-function WT cell and not a BITA forward-and-back hysteresis loop.

**Identification grade:** real independently mutated phenotype / source role-reconstitution / group output gain; no unbiased origin rate, ancestor whole-organism shared-two-function optimum, component startup-cost barrier or genetic-state-matched stable hysteresis.

## 2. Repeated terminal differentiation within clonal colonies — Zhang et al. (2020)

Primary publication: [*Science Advances* DOI 10.1126/sciadv.aay5781](https://doi.org/10.1126/sciadv.aay5781), [PMC6962034](https://pmc.ncbi.nlm.nih.gov/articles/PMC6962034/); Europe PMC original JATS SHA-256 `bfe5787f48f0c2dde277d9d6db6387180472b55c182c5d45738309e45cc0d092`.

- *Streptomyces coelicolor* WT clone M145 produces spores and antibiotic compounds. Genome instability generates descendants with large terminal chromosomal deletions/amplifications. These mutant clones specialize in heightened antimicrobial activity at an individual reproductive cost.
- **28 of 30 selected mutant strains** produce significantly fewer spores than WT (original per-strain comparison p<0.01), sometimes up to a four-order-of-magnitude decline. These 30 selected strains are **not** 30 independent molecular origins; they are a phenotype-screen-selected set with shared genotype ancestry.
- Reduced spores and antibiotic output anticorrelate (published **F(1,29)=26.58, r²=0.478, p<0.001**); independently measured genome deletion-size relationships use **F(1,7)=12.32**, r²≈0.638 for fitness decline, and **F(1,7)=37.97**, r²≈0.844 for increased antibiotic activity. Those df imply a nine-observation genetic subset, not 30 full-sequence independent evolved taxa.
- Mixing mutated producer **9H1A** with WT in a direct starting-frequency manipulation increases antibacterial output across mutant fractions (published **F(2,7)=107.7, r²=0.969, p<0.001**). In the same experimentally manipulated composition series, colony-wide reproduction remains approximately unpenalized **up to about 50% mutants**; beyond that, spores decline (**F(2,7)=37.95, r²=0.916, p<0.001**). These F statistics test quadratic fraction dependence; **they are not a direct mean WT-versus-split effect size**, nor is 0.50 a statistically estimated BITA critical fold/entry point.
- Figure 4 re-calculated source F-to-R² checks are 107.7×2/(107.7×2+7)=**0.968525**, and 37.95×2/(37.95×2+7)=**0.915561**, within original rounded r². This is an arithmetic verification of an **existing** published experiment.
- Antibiotic spectrum is not a single fully measured universal benefit: four screened variants inhibited panels of 48 naturally isolated streptomycetes, 40 of which had at least one variant with stronger inhibition than WT. Those are target-isolate responses nested in one microbial programme, **not 40 successful independent molecular innovations**.
- Strong **asymmetric clonal fertility** matters: terminal mutant cells contribute public-good defence but are selected against for individual reproduction; the parent genotype can regenerate mutant producer cells in subsequent colonies. The mutant population is **not a stably reproducing specialized descendant lineage** or a full multispecies mutualism.
- Original Dryad DOI [10.5061/dryad.bnzs7h462](https://doi.org/10.5061/dryad.bnzs7h462) lists one workbook `Data_Dryad_DoL-Zheren_Zhang.xlsx`, **81,045 bytes**, expected SHA-256 `a23b8ac0f31fe52d76d5f1ebc1dcf3ddab3f9e8f769cea154b10e89c02a6c82e`. File REST endpoint HTTP **401**, dataset REST download **401**, alternative file-stream returned **200 but only 4,268 bytes of non-XLSX content**. The actual 81,045-byte workbook was **not retrieved or validated**. The reanalysis here is of peer-reviewed JATS statistics, not republished raw individual observations.

**Identification grade:** functional separation and individual-vs-colony fitness tradeoff on the *same manipulated composition axis*. Still lacks founding spontaneous-origin frequency among unscreened colonies, directly observed heritable long-term separated lineages, and a calibrated architecture startup penalty.

## 3. Reconcile without falsely pooling

**Two distinct positive architectural mechanisms exist in source experiments:**

| Mechanism | Variation route | Division phenotype | Group-level currency | Retention unit |
|---|---|---|---|---|
| Kim 2016 | regulator/c-di-GMP-altering mutations after mucoid M ancestor | M lubricates + D pushes | colony spreading, CFUs | interacting but genetically distinct morphotypes, negative frequency dependence |
| Zhang 2020 | terminal chromosome deletion/amplification in clonal colony | reproductive cells vs high antibiotic-output, low-reproduction cells | antibacterial activity and total spore production | parent continually regenerates terminal mutants, rather than mutant lineage fixation |

Both have source-reported positive collective outcomes, **but the benefits cannot share a standardized raw effect estimate** (CFUs/spreading versus inhibition zones/spore production), and the 20 and 30 selected mutant assays do not define independent replicated whole-program evolution rates. A meta-analysis that simply divides the number of positive reports by report count would be outcome-definition and ascertainment bias.

**Compare with existing negative/reversal programmes:** P. aeruginosa specialists can coexist under high iron limitation yet reduce output relative to WT (PR #370). Engineering B. subtilis EPS/TasA split can improve biofilm CFU but collapse after adaptation (PRs #371–372). P. stutzeri separated functions can reunify via HGT under alternating substrates (PR #373, experimental original 5/12 fluctuating vs 0/12 constant regimes). The latter is a **reverse transition**, not a contradictory forward rate.

For the next theory-to-reality test, separately code:
- *Upstream generative accessibility*: discrete new morphotype via few regulatory changes vs terminal chromosomal deletion, gene duplication or HGT.
- *Current functional dividend*: physically joint function and colony-level payoff minus appropriately measured parental generalist baseline.
- *Persistence route*: an independently reproducing partner vs terminal non-reproducing daughters produced anew, and availability of autonomous exits.

This adds genuine source-backed, independent **forward division-of-labour** mechanisms but **does not calibrate** the abstract `K(u)`, `tau`, global/fold/entry thresholds, or matched historical two-function morphological divergence. In particular the Kim M ancestor was preadapted to secrete the wetting polymer; it was not the model's shared optimum for two explicitly measured tasks. Even in Zhang's WT, division of labour emerges by recurrent terminal somatic genomic degeneration rather than stable fixation of an allele encoding two independent adult trait axes.

## Reproducibility and scope

Source files: original Europe PMC XMLs for PMC4748119 and PMC6962034, locally SHA-locked, preserved temporarily in GitHub Actions artifacts; **not** committed as copyrighted complete article text.

Computational audit: `scripts/analyze_bita_forward_dol.py`; test suite `tests/test_bita_forward_dol.py`; result `empirical/trait_architecture_history/kim_zhang_forward_dol_readout.json`; two source-intake and source-stat GitHub Actions workflows; independent Dryad source-access gate with explicit 401/non-XLSX status.

All additions reside in Draft PR #374 based on reverse transition PR #373. No `main` merge, no publication, no external dataset rehosting and no changes to the active Ecology Letters manuscript.
