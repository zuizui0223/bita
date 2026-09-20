# Two-network access-routing validation readout v1

## Question

Does the BITA access-routing prediction recur in independently assembled visitor networks with different animal faunas and different response constructions?

Prediction:

> increasing mismatch between the legitimate visitor's access morphology and the floral access domain should increase relative use of bypass / robbing routes.

## Network 1 — Sakhalkar et al. 2023, Afrotropical insect visitors

Inferential unit:

~~~text
plant species
~~~

Scorable species:

~~~text
57 cheating-exposed species with tube length
~~~

Response:

~~~text
B = (robbing - thieving) / (robbing + thieving)
~~~

Observed:

~~~text
Spearman rho[tube length, route balance] = 0.346786
permutation p = 0.0086
~~~

Direction:

> longer flowers are associated with relatively more robbing / bypass than thieving through the floral opening.

Claim boundary:

- observational species-level association;
- source-defined multitrait sensitivity does not isolate tube length as a unique partial driver;
- interpretation is therefore about access geometry rather than tube length alone.

## Network 2 — Aubert / EPHI all-Ecuador bird–flower extension

Inferential unit:

~~~text
bird species × plant species × site
~~~

Coverage:

~~~text
18 Ecuador sites
1,378 pair-site units
~~~

Barrier definition:

~~~text
M = log(flower tube / bird bill)
barrier = flower tube > bill
~~~

Observed:

~~~text
mean robbery rate
  barrier    = 0.30698
  accessible = 0.08139
  difference = +0.22560
  permutation p = 0.0001

rho[M, robbery rate] = 0.41826
permutation p = 0.0001
~~~

Site robustness:

~~~text
17 comparable sites
15 with barrier > accessible robbery
mean within-site difference = +0.14399
sign-test p = 0.00235
site-stratified permutation p = 0.0001
~~~

Direction:

> flowers that exceed the legitimate visitor's bill length are associated with higher nectar-robbing rates.

Claim boundary:

- observational all-18-site extension;
- not an exact replication of Aubert et al. 2026 three-transect GLMM;
- effectively a hummingbird result because only one trait-matched flowerpiercer pair-site is available;
- sparse pair-site exclusions do not remove the association.

## Cross-network result

~~~text
independent public datasets: 2
faunas:                      insects + birds
predicted routing direction: positive in both
effect-size pooling:         NOT DONE
~~~

The two datasets use different predictors, response scales and inferential grains:

~~~text
Sakhalkar:
  plant-level route balance
  longer floral access geometry
  robbing relative to thieving

Aubert/EPHI:
  bird × plant × site robbery rate
  flower-tube / bill mismatch
  robbery under access barrier
~~~

Therefore their numerical effect sizes are not commensurate and must not be pooled.

The defensible cross-network conclusion is:

> **Two independently assembled visitor networks, spanning insect and bird faunas, recover the same qualitative access-routing prediction: stronger mismatch with the legitimate floral access route is associated with greater use of bypass / robbing.**

## What this adds to BITA

This layer is stronger than a single-network example because recurrence occurs under:

- different continents;
- different visitor taxa;
- different cheating classifications;
- different inferential units;
- independently assembled public datasets.

It is still not causal evidence for floral defence.

The network layer therefore supports the generality of the routing consequence of access mismatch, while the matched-D and within-system layers remain responsible for the defence-selectivity mechanism.

## Sources

- Sakhalkar et al. 2023 paper DOI 10.1002/ecs2.4696
- Sakhalkar data DOI 10.5281/zenodo.8398202
- Aubert et al. 2026 paper DOI 10.1002/oik.11552
- EPHI mirror DOI 10.5281/zenodo.14185547
- `results/sakhalkar2023_network_result.json`
- `results/aubert2026_zenodo_extension.json`
- `SAKHALKAR_MULTITRAIT_SENSITIVITY_V1.md`
- `AUBERT_ZENODO_EXTENSION_V1.md`
