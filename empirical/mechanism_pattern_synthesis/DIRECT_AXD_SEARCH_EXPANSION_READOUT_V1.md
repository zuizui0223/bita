# Direct `A x D` search expansion readout v1

## Scope

This readout records the current high-information direct-interaction audit under the strict active definition:

```text
A = declared floral attraction/signal axis
D = independently justified flower-specific defence/access axis
unit = same biological panel with defensible linkage
result = an A x D interaction, factorial contrast, or equivalent joint term
```

An herbivore treatment is not itself `D`. A whole-plant or leaf defence is not silently promoted to flower-specific `D`. A dual-function single trait is not split into two artificial axes.

## Current high-information audit

Twelve candidate systems have now received a source/model-level decision in `DIRECT_AXD_AUDIT_V1.csv`.

```text
strict Tier-1 direct A x D:                         1
factorial floral phenotype but second axis not D:   1
near-direct / ecological-cost but D outside strict floral organ gate: 3
flower-specific A + D measured but no eligible AxD term: 2
joint/multiroute context but no distinct eligible D or AxD: 3
linkage-blocked candidate:                          1
single-trait dual-function case:                    1
```

The exact category labels above are descriptive summaries of the source decisions, not literature frequencies.

### Strict Tier 1

`Impatiens capensis` (Soper Gorden & Adler 2018) remains the only strict current cluster. The deposited individual-plant panel contains pre-treatment flower redness and floral condensed tannins and supports explicit `A_z:D_z` terms on two reproductive components. Both interaction confidence intervals include zero, and the point estimates differ in sign between fruit and seed components. The result is direct but unresolved.

### Factorial floral phenotype that fails the D-orientation gate

Kessler et al. (2015), `Nicotiana attenuata`, independently silenced benzylacetone floral scent and nectar production and generated the double-silenced cross. The design therefore contains a genuine 2 x 2 floral-phenotype contrast. However, nectar removal is a **reward restriction**, not an independently justified antagonist-reducing defence/access phenotype. Re-labelling `no nectar` as `D` solely because it reduces hawkmoth oviposition would define the trait role from the response being tested.

The paper also reports four-line Friedman/pairwise comparisons rather than a formal uncertainty-bearing scent x nectar interaction. A public eLife supplementary audit recovered only figure-image supplements and no raw Figure-2 outcome table. This route is closed as strict Tier 1 and retained instead as high-value same-system `A -> pollination` / `A -> antagonism` evidence.

## Near-direct designs outside the strict flower-specific D gate

### Trifolium repens

Santangelo et al. (2019) is a genuine trait-interaction near miss. The experiment factorially crossed cyanogenic HCN defence, herbivory and pollination, and fitted reproductive-trait x HCN terms including significant banner-petal-size interactions in the herbivory context. However, HCN is a Mendelian **whole-plant** antiherbivore defence rather than a separately established flower-specific D axis. It is retained as cross-organ sensitivity evidence instead of weakening the organ gate.

### Fragaria vesca

Egan et al. (2021) uses a full pollination x herbivory **ecological-agent factorial** and estimates how those agents alter selection on nine attraction/defence traits. The defence-related metabolites are leaf-derived and the fitted interactions are trait x pollination / trait x herbivory, not attraction-trait x defence-trait. This is context-dependent selection evidence, not direct `A x D`.

### Brassica rapa resistance-selection experiment

Strauss et al. (1999), DOI `10.1111/j.1558-5646.1999.tb04525.x`, used artificial selection to produce high- and low-myrosinase populations with corresponding high and low flea-beetle resistance. Resistance regime and herbivore damage altered floral traits, while pollinator foraging was greater on low-resistance undamaged plants. This is strong **ecological-cost-of-resistance in the currency of pollination** evidence. It is not strict Tier 1 because the focal D is a whole-plant resistance-selection regime rather than a demonstrated flower-specific defence phenotype, and the source does not identify a floral A-trait x D-trait reproductive interaction.

This source is retained for the cross-organ ecological-cost layer and the joint-cost search context rather than being used to manufacture a floral `A x D` effect.

## Flower-specific A and D jointly measured, but no eligible interaction term

### Asclepias syriaca

García et al. (2024) now has a closed direct-A×D decision. The source measures **floral latex separately from leaf latex** on the same plants as floral attraction/reward traits, so it passes the organ and linkage gates unusually well. However, the published phenotypic-selection model contains the standardized trait **main effects only**; the authors state that they lacked power for nonlinear selection analyses. No florivory was observed.

Adding petal-width x floral-latex or another correlational-selection term now would therefore be a new post-hoc analysis rather than recovery of a source-identified interaction. The source remains a high-information joint-trait selection case, but it is not Tier 1.

### Gelsemium sempervirens

Irwin & Adler (2006) measures pollination-associated floral traits and defensive nectar chemistry on the same plants, but the reported models use separate trait main effects plus trait-by-site/morph terms. No attraction-by-defence interaction is identified.

## Other exclusion classes

- `Gymnadenia odoratissima`: strong quantitative `A_to_antagonism`, but no distinct D axis in the linked panel.
- `Raphanus sativus`: signal/defence architecture is linked, but no direct A×D reproductive interaction is identified.
- `Brassica rapa` Knauer & Schiestl: attraction traits mediate both pollinators and ovipositing antagonists, but there is no separately measured D phenotype.
- `Dalechampia`: plausible joint trait context remains blocked by individual-level cross-file linkage.
- `Hypericum calycinum`: visual and defensive functions are carried by the same pigment chemistry, leaving one dual-function trait axis rather than A and D.

## Why the negative classifications matter

The audit now repeatedly identifies **different structural reasons** why seemingly relevant pollinator–herbivore studies fail to identify the theoretical mixed partial:

```text
1. defence is measured on the wrong organ;
2. the experiment manipulates ecological agents rather than a defence phenotype;
3. A and D are jointly measured but their interaction is not fitted;
4. signal and defence are the same biological trait, leaving only one axis;
5. source data streams cannot be linked at the claimed biological unit;
6. a factorial floral phenotype exists but the second axis fails the D-orientation gate; or
7. resistance-selection lines create an ecological-cost comparison without identifying a flower-specific A x D trait interaction.
```

A broad keyword search for `pollinator + herbivore + defence + interaction` would therefore dramatically overstate direct evidence.

## Current interpretation

The direct-interaction search is **not yet formally saturated**, but adding further high-information candidates has so far expanded the same exclusion/design classes rather than producing a second strict Tier-1 system.

The current defensible provisional statement is:

> Joint pollinator–herbivore selection and ecological-cost experiments are substantially easier to locate than empirical designs that separately identify a floral attraction axis and a flower-specific defence axis and then estimate their interaction on a linked biological outcome.

This statement concerns the screened high-information candidates only and is not a prevalence estimate for the literature.

## Remaining Gate-A work

1. continue the registered `DX01`–`DX06` query families until new batches cease yielding new eligible **design classes**, not merely new papers in already adjudicated exclusion classes;
2. record query-by-query yields, duplicate/exclusion classes and any new strict candidate;
3. issue a formal saturation receipt only when the stopping rule is met;
4. keep cross-organ resistance-cost studies as sensitivity/context evidence rather than weakening the strict flower-specific D definition to increase Tier-1 count.
