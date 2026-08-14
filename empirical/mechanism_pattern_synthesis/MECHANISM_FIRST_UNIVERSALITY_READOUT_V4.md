# Mechanism-first universality readout v4

## Scientific frame

This project proceeds **Mechanism -> predicted Pattern -> replication/universality test**.

The empirical objective is not a universal grand mean. It is to ask whether the mechanism classes and switching rules fixed in Part I recur independently across taxa, consumer guilds, signal modalities and defence implementations.

## Current prediction status

| Prediction | Status | Current basis |
|---|---|---|
| U1 antagonist cost / relief opportunity | **RECURRENT_STRONG** | Leal quantitative synthesis + independent herbivory synthesis context |
| U2 attraction is not mutualist-exclusive | **RECURRENT_CROSS_MODAL_PROVISIONAL** | scent + visual bract size + petal size + colour + recombinant colour/scent systems; quantitative Dalechampia visual anchor |
| U3 flower-specific defence can reduce antagonist access/use | **RECURRENT_STRONG** | 18 independent D->antagonism clusters across chemical and physical mechanisms |
| U4 defence-to-pollinator effect is not universally negative | **CONDITIONAL_RECURRENT** | matched D systems show negative, null, positive/routing states |
| U5 interaction selectivity / guarded defence | **RECURRENT_QUANTITATIVE_PROVISIONAL** | Catalpa + Pedicularis + Thunia matched numeric anchors plus independent Codonopsis spatial-selectivity implementation |
| U6 selectivity-window switching rule | **RECURRENT_STRONG_CROSS_MODAL** | chemical dose/exposure/response thresholds plus physical spatial/access geometry |
| U7 direct floral A x D sign | **UNIDENTIFIED / FIELD_DESIGN_GAP** | one unresolved strict Impatiens cluster; multiple near-miss factorial/decomposition designs fail trait-level gate |
| U8 direct joint intrinsic cost kappa | **UNIDENTIFIED / FIELD_DESIGN_GAP** | zero strict direct estimates after targeted design audit |

## U2 — shared attraction tracking now crosses signal modalities

The recurrence is no longer dominated by floral scent.

### Olfactory systems

Sasidharan and multiple primary systems show that floral volatile axes can be detected or used by mutualists and antagonists. Quantitative source-level examples include `Gymnadenia`, `Cucurbita`, and dual-function `Nicotiana` systems.

### Visual display — Dalechampia

For `Dalechampia scandens`, the same showy involucral bract axis predicts both pollinator use and seed predation. A +1 SD increase in bract area is source-predicted to change:

```text
patch visitation probability  83.1% -> 94.4%
seed predation probability      ~0.2% -> ~2.5%
```

The corresponding approximate logit changes from the rounded source predictions are +1.232 and +2.549, respectively. These are descriptive model translations, not re-estimated coefficients.

### Visual display — Hibiscus

Experimental petal-size reduction in `Hibiscus moscheutos` shows that petals function as pollinator visual cues while intact/larger petals also receive more adult pollen-predator use. Complete petal removal strongly disrupts pollinator use; the antagonist effect is response-stage specific because petal size affects adult pollen-predator density but not later seed predation.

### Additional visual systems

`Raphanus` colour, `Silene` colour+scent recombinant axes, and other source-adjudicated visual systems independently extend antagonist tracking outside scent.

### U2 interpretation

The recurrent object is therefore not one chemical modality:

> floral apparency signals that improve discoverability to mutualists can also be available to antagonists across olfactory and visual implementations.

U2 remains provisional rather than promoted to a universal numeric effect because compatible uncertainty-bearing `A -> antagonism` effects remain sparse across modalities.

## U5/U6 — physical geometry closes the chemical-only loophole

The selectivity-window rule is no longer supported mainly by chemical concentration systems.

### Codonopsis spatial selectivity

In `Codonopsis lanceolata`, epicuticular wax crystals are spatially restricted:

```text
abaxial + distal adaxial surfaces: slippery / wax-covered
basal adaxial pollinator foothold:  non-slippery / wax-poor
```

The basal inner surface is the region where legitimate `Vespa` pollinators place their forelegs during nectar collection and reproductive contact. By contrast, ant approach surfaces are slippery.

Artificial bridges that bypass the slippery surface increase ant entry. Independent ant-introduction experiments show why this matters: ants shorten hornet visit duration by causing visitors to withdraw.

This is a **spatial/access-geometry selectivity window**: defence is expressed where antagonists need access while a pollinator contact zone remains mechanically usable.

### Fritillaria local bypass

In the same study program, `Fritillaria` tepal hairs provide gripping structures that ants can exploit on some surfaces. This demonstrates that geometry can locally close or bypass the defensive filter, analogous to threshold crossing in chemical systems.

### Cross-modal switching principle

Chemical systems generate selectivity through different response thresholds and cumulative exposure; physical systems generate it through differential access geometry. Both instantiate the same abstract rule:

> antagonist and pollinator interaction channels can be separated only while their effective response/access domains remain distinct.

The higher-level switching rule is therefore **cross-modal** rather than chemical-specific.

## Direct A x D and kappa — the missing design is now explicit

A targeted missing-design matrix records the closest studies and the exact gate each fails.

Current state:

- `Impatiens capensis` remains the only strict trait-level direct `A x D` cluster; reproductive-component interaction estimates are unresolved.
- `Helleborus` gives a clean ecological-agent factorial but does not independently manipulate floral A and D traits.
- `Fragaria` gives factorial pollination x herbivory and diffuse selection on attraction/defence-related traits, but no A:D trait interaction.
- `Cucurbita`, `Petunia`, and `Nicotiana` decompose signal functions or dual-function compounds, but do not provide two independently varied A and D axes on a shared fitness outcome.
- candidate chemistry studies that fail the focal D-role or flower-organ gate are not promoted merely to fill the matrix.

Thus U7/U8 should now be described as **field-design gaps** unless a new strict source is recovered, not as evidence that the interaction or joint cost is absent.

## Current strongest empirical synthesis

> Attraction signals repeatedly expose flowers to both mutualists and antagonists across olfactory and visual modalities. Flower-specific defence repeatedly reduces antagonist access through chemically and physically distinct implementations. Whether pollination is preserved depends on whether antagonist and pollinator response/access domains remain separable. Chemical dose and cumulative exposure can close that separation; physical spatial geometry can create or bypass it. The recurrent empirical object is therefore a cross-modal selectivity-window switching rule, not one universal sign of attraction–defence association.

## What remains unsupported

- a universal positive or negative `W_AD`;
- a universal numeric threshold ratio;
- a common effect scale pooling visitation, handling, predation, oviposition and fitness;
- `kappa = 0`;
- prevalence claims from the route ledger.

## Remaining targeted tasks

1. Recover additional scale-compatible matched D effects only where source structure genuinely permits it.
2. Seek one more independent **physical** system where pollinator-preserving geometry is directly manipulated, to test physical replication beyond the Takeda program.
3. Seek additional uncertainty-bearing **non-scent A -> antagonism** effects; prioritize visual-display manipulations with antagonist counts and sample sizes.
4. Continue strict A x D search only for studies independently varying validated floral A and flower-specific D on a shared reproductive/fitness outcome.
5. If U7/U8 remain empty after the registered targeted classes are exhausted, freeze them as empirical design gaps rather than broad-search blockers.
6. Do not fit a common selectivity meta-regression unless a genuinely compatible outcome lane reaches sufficient independent systems.

## Current stop decision

```text
broad pattern-class search:             saturated
U2 cross-modal shared tracking:         recurrent, quantitative coverage still incomplete
U5 selective-state recurrence:          quantitative in >=3 independent matched systems
U6 switching-rule recurrence:           strong across chemical + physical implementations
strict direct A x D:                    one unresolved cluster
strict joint cost:                      zero
scientific evidence work:               CONTINUE TARGETED ONLY
```
