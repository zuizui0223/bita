# Adler & Irwin (2005) — *Gelsemium sempervirens* D→antagonism readout

## Source

```text
article DOI: 10.1890/05-0118
trait:       nectar gelsemine concentration
antagonist:  Xylocopa virginica nectar robber
```

The primary article experimentally manipulated nectar gelsemine in two field years. The 2002 high treatment (0.5% gelsemine) was deliberately above the natural range; the 2004 high treatment (0.025%) was within the natural range. Low treatments received no added gelsemine.

## Why outcome stage must remain explicit

The experiment separates the initial decision to visit a plant from behavior after the robber begins foraging. These are not interchangeable antagonist responses.

### Initial plant entry

The paper reports no treatment effect on the total number of nectar-robber visits to plants in either year:

```text
robber plant visits: F < 0.5, P > 0.5 in both years
```

This route state is therefore `no_detected_effect` for antagonist plant entry.

### Within-plant use after entry

In 2002, the supra-natural high-gelsemine treatment reduced *Xylocopa*:

```text
proportion of flowers probed/robbed: 22% lower
mean time spent per flower:            9% lower
```

The source reports a significant treatment effect on visitor behavior in the 2002 multivariate/univariate analysis context. The exact coefficient/SE needed for a compatible effect-size row is not recoverable from the prose alone, so these percentages are retained as source-reported relative changes rather than converted to an uncertainty-bearing meta-analytic effect.

In 2004, at the natural-range high treatment, the proportion of flowers robbed was approximately one-third lower, but the effect was not significant in the MANOVA and was only marginal in the univariate test. Time-per-flower responses also depended on floral morph:

```text
pin:   low 6.32 ± 0.78 s; high 8.68 ± 0.74 s
thrum: low 11.00 ± 1.82 s; high 7.47 ± 1.95 s
```

These morph-specific time contrasts must not be averaged into a generic robber-deterrence effect without the original interaction model.

## Evidence classification

```text
D_to_antagonism mechanism:       source verified
plant-entry visitation response: null / no detected treatment effect
within-plant robbed fraction:    negative at supra-natural dose; weaker/marginal at natural-range dose
within-flower residence time:    negative at supra-natural dose; morph-dependent at natural-range dose
quantitative Tier-3 effect:       not registered from these percentages alone
same-system Tier-2 status:       retained
```

## Mechanistic implication

Gelsemine does not primarily prevent a nectar robber from arriving at the plant. Its clearest effect occurs after tasting, by changing how intensively a robber exploits flowers. This makes `decision stage` an empirical moderator: a synthesis that combines plant-entry visitation with within-plant exploitation would obscure the defensive route.

This readout does not establish that gelsemine increases plant fitness. The same experiment also documents pollinator costs, so antagonist deterrence and mutualist interference remain separate channels.
