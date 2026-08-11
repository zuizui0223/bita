# Mechanism-pattern synthesis — status after Batch 3

## Scope

Batch 3 moves the branch from an initial source-seeded mechanism map toward multiple independent empirical anchors while preserving the strict distinction among:

```text
direct A x D interaction evidence
same-system marginal routes
single-route quantitative effects
source-adjudicated directional effects
direct A+D joint-cost evidence
```

No result below is an estimate of `W_AD = rho - iota - kappa`.

## 1. Direct interaction state

### Strict current Tier 1

One strict observational cluster remains verified:

```text
Soper Gorden & Adler 2018 — Impatiens capensis
A = early flower redness
D = early floral condensed tannins
unit = individual plant

CH fruits/day:
  A x D = -0.0820 ± 0.0548 SE, n = 170
  95% CI crosses zero

seeds/CH fruit:
  A x D = +0.1040 ± 0.1043 SE, n = 85
  95% CI crosses zero
```

The opposite point directions across reproductive components are retained as an unresolved outcome-scale difference, not a confirmed sign reversal.

### Direct-search architecture

Eleven high-information candidate systems have received source/model-level decisions. The most common failures are now explicit:

- defence measured in leaves or as a whole-plant state rather than as flower-specific D;
- antagonist manipulation mistaken for a defence phenotype;
- A and D both measured but no A x D term fitted;
- a dual-function single trait incorrectly offering only one biological axis;
- unresolvable individual linkage; or
- a factorial floral phenotype whose second axis is a reward rather than defensible D.

Kessler et al. (2015) is now closed as strict Tier 1 despite its full scent × nectar factorial: nectar absence is a reward-restriction phenotype, not an independently justified defence trait, and the public supplement contains no raw Figure-2 outcome table for a formal interaction reconstruction.

The remaining unusually well-aligned candidate is García et al. (2024), because it measures **floral latex separately from leaf latex** together with floral attraction traits in the same common-milkweed individuals. A public Appendix I/II audit has been implemented, but no A x D reanalysis is permitted until the primary source fixes the relevant variable definitions and source model.

## 2. Attraction tracking: A → antagonist

Batch 3 establishes two independent quantitative anchors plus two additional experimental directional systems.

### Quantitative anchor 1 — Gymnadenia

```text
Gross, Sun & Schiestl 2016
n = 1,162 individual linked inflorescences
A = total floral scent
H = eaten flowers / total flowers
beta = +0.56814
SE   =  0.26854
95% CI = [0.04181, 1.09446]
```

This is a same-day observational association, not a causal scent manipulation.

### Quantitative anchor 2 — Cucurbita comparative panel

Theis et al. (2014) reports source-model coefficients for the same sesquiterpenoid axis within *Cucurbita*:

```text
A → squash-bee visitation:
  beta = +0.096 ± 0.034 SE
  95% CI = [0.029, 0.163]

A → cucumber-beetle flower use:
  beta = +2.91 ± 1.28 SE
  95% CI = [0.40, 5.4]
```

The two effects remain on their source scales and are not pooled. Their value is mechanistic: one floral signal axis positively predicts both a specialist pollinator and a specialist floral antagonist within the same comparative panel.

### Additional experimental systems

Theis & Adler (2012): enhanced floral fragrance increases florivore attraction without a detected increase in pollinator attraction and reduces seed production. The publisher-linked Figshare collection was verified but contains only a trapping-experiment Appendix A, not raw data for the focal field experiment. The study remains Tier 4 directional rather than being converted into an unsupported effect size.

Kessler et al. (2015): benzylacetone scent silencing strongly reduces *Manduca sexta*-mediated seed production and also reduces *M. sexta* oviposition. The pollination effect is sharply consumer-dependent: *Hyles lineata* pollination shows little dependence on scent alone. This study is retained as Tier 2 same-system attraction tracking rather than forced into direct A x D.

## 3. Defence efficacy: D → antagonist

The branch now contains chemical and physical flower-specific defence mechanisms.

### Gelsemium nectar gelsemine

Initial nectar-robber plant entry is not detectably reduced, whereas within-plant exploitation declines after tasting. In the 2002 supra-natural treatment, high gelsemine reduced the proportion of flowers probed by 22% and time per flower by 9%. The natural-range 2004 response was weaker/marginal and morph-dependent. Decision stage is therefore retained as a moderator.

### Asclepias nectar cardenolides

Jones & Agrawal (2016) manipulated cardenolides in flower nectar independently of leaf traits using paired full-sibling plants. For monarch oviposition:

```text
20 female butterflies
Poisson GLMM
nectar stimulus: chi-square = 13.87, df = 1, P < 0.001
sucrose-only flowers received 61% more eggs per female than cardenolide-laced flowers
```

The source reports no coefficient/SE, so the Wald statistic and relative percentage are not reverse-engineered into a pseudo-effect size.

### Slippery floral surfaces

Takeda, Kadokawa & Kawakita (2021) directly bypassed slippery perianth barriers with non-slippery bridges:

```text
Codonopsis lanceolata:
  bridged 28% vs control 10% flowers receiving ants at least once
  source GLMM P < 0.001

Fritillaria koidzumiana:
  bridged 45% vs control 5.1%
  source GLM P << 0.001
```

This adds an unambiguously flower-specific **physical-access** D mechanism to a literature otherwise dominated by nectar chemistry.

### Aconitum next quantitative target

Barlow et al. (2017) is now in the source-audit pipeline. The primary accepted manuscript explicitly declares Figshare `10.6084/m9.figshare.5165350` for biological-assay, nectar/galea alkaloid and bumblebee–alkaloid bioassay data. This is a high-priority target because the same nectar-alkaloid axis deters nectar robbers at lower concentrations than those that substantially reduce pollinator visitation. A bounded public-data audit is implemented before any reanalysis.

## 4. Context switches are now a primary data product

`SIGN_SWITCH_LEDGER_V1.csv` currently fixes nine within-study conditionality patterns, including:

```text
Polemonium: dose
Asclepias: exposure duration
Nicotiana: pollinator-response construct
Gelsemium: reward compensation
Asclepias/Villalona: natural vs elevated dose
Impatiens: reproductive-component scale, unresolved direct A x D
Cucurbita/Andrews: floral-scent compound identity
Gelsemium: antagonist decision stage
Nicotiana/Kessler: pollinator identity
```

These are dependent within-study contrasts, not nine independent replications. Their role is to identify moderators that would be erased by a generic route-level mean.

## 5. Direct joint cost remains unidentified

Three high-information joint-trait systems have been audited for the `kappa` layer.

```text
direct measured A+D allocation/construction cost: 0 verified
```

Theis et al. (2014) explicitly tested simple allocation-tradeoff correlations and found no attractive/reward trait correlated with leaf or floral cucurbitacins (`|r| < 0.25`, all `P > 0.05`). Thosteman et al. (2024) reports low integration between floral scent and foliar defence chemistry. Wild radish links petal colour and glucosinolate architecture but does not measure a direct resource cost.

These are negative or non-cost architecture results. None identifies `kappa`, and none permits `kappa = 0`.

## 6. Public-data route audits that produced negative results

Two important archive audits are now explicitly closed rather than silently ignored:

- Theis & Adler (2012): publisher-linked Figshare contains a trapping-experiment appendix only, not focal main-experiment raw data.
- Kessler et al. (2015): public eLife supplement ZIP contains three TIFF figure supplements but no raw Figure-2 outcome table.

These outcomes prevent unsupported numerical reconstruction and are retained as data-availability results, not biological nulls.

## 7. Completion-gate state

```text
Gate A direct-interaction search:          active; 11 high-information candidates adjudicated, not saturated
Gate B all four marginal routes:           substantially improved; each now has source-verified empirical state
Gate C >=2 quantitative mechanism modules: increasingly plausible, but metric-compatible synthesis still sparse
Gate D sign-switch analysis:               study-level switch ledger active; formal moderator models not yet justified
Gate E same-system multi-route audit:       active with multiple independent systems
Gate F direct joint cost:                   active; 0 direct cost studies verified
Gate G synthesis bias/robustness:           premature for sparse compatible strata
Gate H theory/empiricism boundary:          currently preserved
```

## Current scientific readout

The accumulating evidence is no longer well described by a single question such as whether defence reduces pollinator visitation on average.

The stronger current empirical pattern is:

> Floral signals can be tracked by both mutualists and antagonists; flower-specific defences can suppress antagonist access or use; and the pollinator cost of those defences is conditional on dose, reward, consumer identity, exposure duration, and the response construct being measured. Direct attraction-by-defence evidence remains rare and, in the only strict current individual-level cluster, unresolved across reproductive components.

This supports the mechanism-pattern synthesis architecture without claiming that the theoretical mixed partial has been broadly estimated.

## Immediate next work

1. close the García public-appendix/model route without inventing a source model;
2. inspect the article-declared Barlow et al. (2017) Figshare data and, if eligible, predeclare and fit a quantitative Aconitum D→antagonist / D→pollinator module;
3. continue direct A x D search saturation using the now-stable failure-mode taxonomy;
4. deepen independent quantitative A→antagonist and D→antagonist strata only when the source metric and uncertainty are recoverable; and
5. keep the manuscript frozen and PR #126 in draft until the completion gate is actually met.
