# Mechanism-pattern source screening: execution series 1-2 readout

## Status

This is the first empirical execution series under `MECHANISM_PATTERN_UNIVERSALITY_PROTOCOL_V1.md`. It is not a manuscript result and does not alter the fixed theory.

The screen deliberately prioritizes high-information papers that jointly expose mutualist and antagonist pathways or explicit context switches. It is therefore **not a representative sample of the literature**, and fractions from this batch must not be interpreted as prevalence estimates.

## Source work completed

The first source screen established five strong same-system multi-route systems from the new search and then re-audited historical `bita` evidence branches for direct interaction and quantitative route evidence.

The active execution files now contain:

```text
14 source-adjudicated route records in the first seed ledger
7 quantitative/direct-interaction records in execution batch 2
6 independent systems with same-system multi-route or direct-interaction information
1 verified Tier-1 observational direct A x D cluster
1 exact-linked Tier-3 quantitative A -> antagonism cluster
```

The same-system systems currently registered are:

1. `Polemonium viscosum` — floral 2-phenylethanol;
2. `Gelsemium sempervirens` — nectar gelsemine;
3. `Asclepias` spp. — nectar cardenolides;
4. `Nicotiana attenuata` — nectar secondary metabolites / nicotine;
5. `Ipomopsis aggregata` — nectar concentration as robber resistance;
6. `Impatiens capensis` — flower redness, floral condensed tannins, visitor responses, natural florivory and reproductive components on one individual-plant panel.

`Hypericum calycinum` is retained at Tier 4 because the same pigment chemistry has a plausible visual-signal role and a directly demonstrated caterpillar-deterrent role, but the paper does not experimentally estimate a pollinator response to that chemistry.

## First empirical pattern: the same defence/filter route does not have one pollinator sign

### Dose dependence

In `Polemonium viscosum`, 2-phenylethanol deters flower-damaging ants. High expression also reduces bumblebee visitation and pollination, whereas moderate experimental levels increase nectar standing crop without a detected pollination cost.

This is a same-system example of antagonist relief co-occurring with a pollinator cost only in part of the trait-expression range.

### Time-scale dependence

In `Asclepias`, cardenolides at the highest reported natural concentrations do not deter individual bumble bees in single foraging bouts, but colony-level deterrence emerges after several days of foraging. The same treatment reduces monarch oviposition while not deterring monarch flower foraging.

Thus both exposure duration and antagonist outcome construct change the apparent route state.

### Outcome-construct dependence

In `Nicotiana attenuata`, nectar repellents reduce pollinator nectaring time and nectar removal but can increase visit number. The same chemical-filter module also reduces nectar-thieving ant visitation.

A generic `pollinator response` meta-analysis would therefore combine effects with opposite signs from the same biological study.

### A counterexample to universal pollinator interference

In `Ipomopsis aggregata`, dilute nectar is presented as resistance to nectar-robbing bumble bees yet does not deter legitimate hummingbird pollinators. This is an explicit same-system case where antagonist resistance is observed without a detectable pollinator-use cost.

## First direct observational A x D cluster

Historical `Impatiens capensis` workflow outputs were recovered from successful GitHub Actions run `28713490690` (artifact `8083707968`) and checked against the predeclared model configuration.

The same individual-plant panel explicitly fits:

```text
reproductive_component ~ A_z + D_z + A_z:D_z
                       + randomized interaction assignments + phenology
```

with early flower redness as `A` and early floral condensed tannins as the `D` axis. A linked same-species primary study (`10.1002/ecs2.1326`) provides the observational D-role basis by showing that floral condensed tannins are associated with lower nectar robbing, nectar thieving and florivory.

Two direct interaction estimates are available:

```text
CH fruits per plant per day
    n = 170
    A x D = -0.08204 ± 0.05483 SE
    95% CI [-0.18950, +0.02542]

seeds per CH fruit
    n = 85
    A x D = +0.10403 ± 0.10435 SE
    95% CI [-0.10049, +0.30855]
```

The point estimates have opposite signs and both intervals include zero. The correct direct-interaction result is therefore **unresolved and outcome-scale dependent**, not a claim of complementarity or substitutability.

## Quantitative A -> antagonism anchor

The historical exact-row-linkage `Gymnadenia odoratissima` analysis was promoted into the new execution ledger.

For 1,162 marked plants linked on `PlantID + Year + Region + Population`, the predeclared quasi-binomial logit model estimates:

```text
logit(florivory probability)
    ~ population x year intercepts
    + z(log1p(total floral scent))

beta = +0.56814
SE = 0.26854
95% CI = [0.04181, 1.09446]
p = 0.03437
```

This corresponds to approximately `exp(0.568) = 1.77` times the odds of per-flower florivory per 1 SD increase in log-transformed total floral scent. It is a same-day observational association, not a causal scent manipulation.

## Quantitative D -> pollinator anchor retained

One source-audited natural-range effect from Adler & Irwin (2005) remains in the first ledger:

```text
high gelsemine: 1.71 ± 0.25 SE visits, n = 38
low  gelsemine: 2.00 ± 0.31 SE visits, n = 37

ln response ratio = -0.156654
SE(lnRR)           =  0.213071
approx. 95% CI     = [-0.574, +0.261]
```

The point estimate is negative but individually imprecise. It is one quantitative route record inside a same-system D-to-pollinator / D-to-antagonist study, not an estimate of `iota`.

## Attraction-side evidence identified for the next extraction batch

The source screen identified high-information `A -> pollinator` / `A -> antagonist` systems that should now be promoted through numerical extraction where source uncertainty is recoverable:

- Andrews, Theis & Adler (2007), `Cucurbita`: three floral volatiles were tested against both specialist squash bees and cucumber beetles; one compound attracted both, one only the herbivore, and one only the pollinator.
- Theis & Adler (2012), `Cucurbita pepo`: experimentally enhanced fragrance increased florivore attraction rather than pollinator attraction and reduced seed production.
- Kessler et al. (2013), `Petunia`: transgenic volatile-silencing demonstrates defensive components within a floral scent bouquet; the exact pollinator endpoint must be audited before same-system Tier-2 promotion.

## Direct A x D audit result

Six high-information candidates have now been adjudicated in `DIRECT_AXD_AUDIT_V1.csv`.

Current state:

```text
Impatiens 2018       Tier 1 observational direct interaction
Irwin & Adler 2006   no A x D term in the audited models
Gymnadenia 2016      no D axis
Dalechampia          individual cross-file linkage not verified
Raphanus 2004        joint trait architecture, no direct A x D fitness term
Hypericum 2001       one dual-function pigment axis, not distinct A and D axes
```

Co-occurrence of attraction and defence traits is not enough. A study enters Tier 1 only when the joint interaction itself is identifiable on a declared outcome.

## Scientific consequence of the first execution series

The evidence already rejects a simplistic empirical target of the form

```text
D -> pollinator use has one universal negative sign.
```

It also shows why direct interaction evidence must retain outcome scale: the first eligible A x D study gives opposite, individually unresolved point estimates for two reproductive components.

The defensible synthesis target remains:

```text
which mechanisms recur,
which mechanisms co-occur in the same system,
what ecological context changes their direction or magnitude,
and how often direct A x D interactions are positive, negative, or unresolved on declared outcome scales?
```

## Next execution batch

1. Full-text extract Andrews et al. (2007) into separate compound x consumer route rows.
2. Expand the direct A x D search beyond the six adjudicated candidates and document saturation.
3. Build a quantitative `A -> antagonism` queue around Gymnadenia plus independent visual/scent studies with recoverable uncertainty.
4. Extract numerical `D -> antagonism` effects from same-system studies already source-verified.
5. Build study-level sign-switch tables before fitting moderator models.
6. Search direct A+D allocation/construction-cost evidence independently; do not infer `kappa` from covariance.
