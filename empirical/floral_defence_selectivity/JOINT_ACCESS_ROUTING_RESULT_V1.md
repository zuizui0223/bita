# Joint cross-network access-routing result v1

## Main result

Two independent public visitor networks were placed on the same directional construct:

> stronger constraint on the legitimate floral access route -> greater bypass / robbing propensity.

Raw observations were not pooled.

Network-specific standardized effects:

~~~text
Sakhalkar insects:
  n = 57 plant species
  rho = 0.346786
  permutation p = 0.0082 in the joint workflow

Aubert / EPHI birds:
  n = 1,378 bird × plant × site units
  site-adjusted rank rho = 0.350512
  within-site permutation p = 0.0001

Aubert global descriptive rho = 0.418262
~~~

The Aubert effect used in the joint statistic removes site-specific rank means before correlation, so among-site composition does not define the network contribution.

## Equal-network joint test

Networks were weighted equally.

Primary Fisher-z mean correlation:

[
r_J = 0.348651.
]

Two-sided stratified permutation result:

~~~text
joint p = 0.0001
permutations = 9,999
seed = 20260920
~~~

Arithmetic mean correlation:

~~~text
0.348649
~~~

Direction concordance:

~~~text
2 / 2 networks positive
~~~

Diagnostic null probability that both permuted network effects are positive:

~~~text
0.2536
~~~

This is close to the 0.25 value expected for two approximately symmetric independent directional nulls, unlike the earlier global-Aubert formulation that retained among-site composition.

## Interpretation

The result upgrades the network evidence from two parallel examples to one common cross-network test:

> **Across independent insect and bird visitor networks, stronger floral access constraint is associated with greater use of bypass / robbing routes.**

The comparable standardized effect sizes are notable:

~~~text
insects: rho = 0.347
birds:   rho = 0.351 after site adjustment
joint:   rho = 0.349
~~~

The analysis therefore supports a shared routing prediction without allowing the larger bird dataset to dominate the smaller insect dataset.

## Letter relevance

This is the strongest empirical result for a Letter framing because it tests one general prediction across independently assembled datasets and faunas.

The Letter claim can now be:

> access constraints reroute exploitation across independent visitor networks.

The literature / matched-D / within-system evidence should support mechanism and interpretation rather than carry the primary inferential burden.

## Boundaries

Do not call the joint statistic:

- a causal effect;
- a universal effect size;
- a random-effects meta-analysis;
- a raw-data pooled regression;
- evidence that tube length alone is causal in Sakhalkar;
- an exact replication of Aubert et al. 2026.

The joint result is an equal-network synthesis of standardized rank associations.

## Reproducibility

Workflow run: 35479028223

Artifact:

~~~text
id = 10595177156
digest = sha256:71f310d17940564bfb031f35183513aa9ac5173253d95c5f0586601fbcd07ba3
~~~

Frozen machine-readable result:

`empirical/floral_defence_selectivity/results/joint_access_routing.json`
