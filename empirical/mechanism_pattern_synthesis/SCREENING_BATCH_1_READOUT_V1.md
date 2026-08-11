# Mechanism-pattern source screening: batch 1 readout

## Status

This is the first empirical execution batch under `MECHANISM_PATTERN_UNIVERSALITY_PROTOCOL_V1.md`. It is not a manuscript result and does not alter the fixed theory.

The batch deliberately prioritizes high-information papers that jointly expose mutualist and antagonist pathways or explicit context switches. It is therefore **not a representative sample of the literature**, and fractions from this batch must not be interpreted as prevalence estimates.

## Source work completed

Twelve studies were source-screened against the direct `A x D`, same-system multi-route, context-switch, and joint-cost targets.

The first seeded master ledger contains:

```text
14 source-adjudicated route records
6 independent biological study clusters
5 Tier-2 same-system multi-route clusters
1 Tier-4 directional dual-function cluster
0 verified direct A x D interaction clusters
```

The five Tier-2 clusters currently seeded are:

1. `Polemonium viscosum` — floral 2-phenylethanol;
2. `Gelsemium sempervirens` — nectar gelsemine;
3. `Asclepias` spp. — nectar cardenolides;
4. `Nicotiana attenuata` — nectar secondary metabolites / nicotine;
5. `Ipomopsis aggregata` — nectar concentration as robber resistance.

`Hypericum calycinum` is retained at Tier 4 because the same pigment chemistry has a plausible visual-signal role and a directly demonstrated caterpillar-deterrent role, but the paper does not experimentally estimate a pollinator response to that chemistry.

## First empirical pattern: the same defence/filter route does not have one pollinator sign

The seeded records already contain several different forms of conditionality.

### Dose dependence

In `Polemonium viscosum`, 2-phenylethanol deters flower-damaging ants. High expression also reduces bumblebee visitation and pollination, whereas moderate experimental levels increase nectar standing crop without a detected pollination cost.

This is a direct same-system example of antagonist relief co-occurring with a pollinator cost only in part of the trait-expression range.

### Time-scale dependence

In `Asclepias`, cardenolides at the highest reported natural concentrations do not deter individual bumble bees in single foraging bouts, but colony-level deterrence emerges after several days of foraging. The same treatment reduces monarch oviposition while not deterring monarch flower foraging.

Thus both exposure duration and antagonist outcome construct change the apparent route state.

### Outcome-construct dependence

In `Nicotiana attenuata`, nectar repellents reduce pollinator nectaring time and nectar removal but can increase visit number. The same chemical-filter module also reduces nectar-thieving ant visitation.

A generic `pollinator response` meta-analysis would therefore combine effects with opposite signs from the same biological study.

### A counterexample to universal pollinator interference

In `Ipomopsis aggregata`, dilute nectar is presented as resistance to nectar-robbing bumble bees yet does not deter legitimate hummingbird pollinators. This is an explicit same-system case where antagonist resistance is observed without a detectable pollinator-use cost.

## Quantitative anchor added

One source-audited natural-range effect from Adler & Irwin (2005) was promoted into the new ledger rather than copied as a prose direction only.

For the 2004 field manipulation:

```text
high gelsemine: 1.71 ± 0.25 SE visits, n = 38
low  gelsemine: 2.00 ± 0.31 SE visits, n = 37

ln response ratio = -0.156654
SE(lnRR)           =  0.213071
approx. 95% CI     = [-0.574, +0.261]
```

The point estimate is negative but individually imprecise. It is retained as one quantitative route record inside a same-system multi-route study, not as a stand-alone validation of `iota`.

## Attraction-side evidence identified for the next batch

The first search also identified high-information `A -> pollinator` / `A -> antagonist` systems that should now be promoted through full-text extraction:

- Andrews, Theis & Adler (2007), `Cucurbita`: three floral volatiles were tested against both specialist squash bees and cucumber beetles; one compound attracted both, one only the herbivore, and one only the pollinator.
- Theis & Adler (2012), `Cucurbita pepo`: experimentally enhanced fragrance increased florivore attraction rather than pollinator attraction and reduced seed production.
- Kessler et al. (2013), `Petunia`: transgenic volatile-silencing demonstrates defensive components within a floral scent bouquet; the exact pollinator endpoint must be audited before same-system Tier-2 promotion.

These studies are valuable because the new synthesis needs the attraction side (`A -> P`, `A -> H`) as seriously as the defence side.

## Direct A x D status

No Tier-1 direct `A x D` interaction is verified in this first batch.

This is not treated as evidence that such studies do not exist. Three high-priority audits remain:

1. Irwin & Adler (2006), `Gelsemium sempervirens`: directly tests phenotypic correlations between pollination-associated distyly and herbivore-resistance secondary compounds and then examines floral visitors. Full model tables must be checked for an actual `A x D` interaction term.
2. Strauss & Irwin (2004), wild radish: links petal-colour polymorphism to inducible glucosinolate defence. It is strong joint-trait architecture but does not, from the currently verified source, identify a direct A x D fitness interaction or allocation cost.
3. The historical `bita` matched-system branches should be re-audited for any study that genuinely varied/measured both focal axes in the same biological panel.

Until an interaction term or equivalent factorial contrast is source-verified, none of these is counted as Tier 1.

## Scientific consequence of batch 1

The first source batch already rejects a simplistic empirical target of the form

```text
D -> pollinator use has one universal negative sign.
```

The more defensible synthesis target is exactly the one defined in the new protocol:

```text
which mechanisms recur,
which mechanisms co-occur in the same system,
and what ecological context changes their direction or magnitude?
```

The current examples show that dose, exposure duration, response construct, and consumer role can all alter the empirical expression of the pollinator-interference pathway.

## Next execution batch

1. Full-text extract Andrews et al. (2007) into separate compound x consumer route rows.
2. Full-text audit Irwin & Adler (2006) for a genuine direct `A x D` coefficient or factorial contrast.
3. Re-audit historical matched-system branches for direct interaction candidates rather than marginal arrows.
4. Start quantitative `A -> antagonism` and `D -> antagonism` extraction queues, prioritizing studies with raw data or reported means/uncertainty.
5. Keep outcome constructs separate; do not pool visit number with residence/consumption, pollen transfer, or reproduction.
