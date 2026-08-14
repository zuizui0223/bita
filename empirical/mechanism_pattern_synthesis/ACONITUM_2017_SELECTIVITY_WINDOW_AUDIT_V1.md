# Aconitum 2017 nectar-defence selectivity-window audit v1

## Source

Barlow SE et al. 2017. **Distasteful Nectar Deters Floral Robbery.** *Current Biology* 27:2552–2558.e3. DOI `10.1016/j.cub.2017.07.012`.

Study system: *Aconitum napellus* and *A. lycoctonum*, long-tubed flowers primarily pollinated by long-tongued *Bombus hortorum* and occasionally robbed by short-tongued *B. terrestris*.

## Primary-source threshold result

The paper reports two distinct sensitivity regimes for the same nectar-alkaloid axis:

```text
nectar robber B. terrestris: deterrence above ~20 ppm
legitimate pollinator visits: sharp decline around 200–380 ppm
```

The primary article explicitly concludes that nectar alkaloids are more distasteful to robbers than to pollinating bees, while also noting that sufficiently high concentrations deter pollinators.

## Existing repository quantitative anchors

The source-audited ledger already retains:

- *A. lycoctonum* field pollinator-visitation association: Fisher-z transformed correlation `-0.794306`, `SE=0.301511`, `n=14` (direction source-consistent; exact source-model subset remains unresolved, so sensitivity status only);
- *A. lycoctonum* 20-ppm *B. terrestris* consumption cell: mean 3.022 uL versus sucrose reference 28.276 uL, a descriptive 89.3% reduction;
- *A. napellus* 20-ppm cell independently shows the same within-publication pattern but is not a second independent study cluster.

These two lanes are not subtracted because one is a field correlation and the other a laboratory dose assay.

## Mechanism-first interpretation

Aconitum provides a clear **selectivity window** rather than a binary selective/nonselective classification.

At low-to-moderate alkaloid concentrations, robbers cross their aversion threshold while legitimate pollinators remain below their sharp deterrence threshold. At sufficiently high concentrations, pollinator gustatory sensitivity becomes constraining.

Thus:

```text
low dose:       little realised defence
intermediate:   robber deterrence >> pollinator cost   [selective window]
high dose:      robber deterrence + pollinator cost    [selectivity collapses]
```

This independently matches the dose-switch logic in *Polemonium viscosum*, despite different plant taxa, alkaloid/volatile chemistry, and visitor configuration.

## Universality role

The important replication is therefore not “all defences are selective.” It is the higher-level switching rule:

> selectivity depends on relative response thresholds of antagonist and mutualist consumers, creating an expression window in which antagonist relief can be gained before pollinator interference becomes large.

This is a concrete empirical mechanism that can map onto the theoretical balance between antagonist relief and pollinator interference.

## Status

```text
flower-specific D gate:          PASS
same D affects both guilds:      PASS
selectivity-window evidence:     STRONG
cross-system dose-switch match:  Polemonium + Aconitum
formal matched pooled contrast:  NOT YET SCALE-COMPATIBLE
universality role:               THRESHOLD-SEPARATION ANCHOR
```

## Inference boundary

The threshold separation is not a direct estimate of `W_AD`, `rho-iota`, or `kappa`. Field visitation and laboratory consumption are distinct response lanes and are not numerically combined without a defensible common scale and dependence model.
