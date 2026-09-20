# Joint cross-network access-routing analysis protocol v1

## Objective

Convert the two independent network results from parallel corroboration into one predeclared cross-network statistical test.

Common directional construct:

> **greater constraint on the legitimate floral access route -> greater bypass / robbing propensity**

The raw predictors and responses differ across datasets, so raw observations are not pooled.

## Network-specific standardized effects

### Sakhalkar 2023

Inferential unit: plant species.

Access-constraint proxy: tube length.

Bypass-response proxy: (robbing - thieving) / (robbing + thieving).

Effect: Spearman rho.

### Aubert / EPHI

Inferential unit: bird species × plant species × site.

Access-constraint proxy: log(flower tube / bird bill).

Bypass-response proxy: robbery rate.

Effect: Spearman rho.

## Joint statistic

Each network contributes one rank correlation. To prevent the much larger Aubert/EPHI dataset from overwhelming the Sakhalkar network solely by sample size, networks receive equal weight.

Primary joint statistic:

[
r_J =
	anhleft(
rac{operatorname{atanh}(r_S)+operatorname{atanh}(r_A)}{2}
ight).
]

The arithmetic mean correlation is also reported as a descriptive sensitivity.

## Permutation null

Sakhalkar: shuffle bypass-response values across plant species.

Aubert/EPHI: shuffle robbery-rate values within site only.

Thus the Aubert null preserves site composition and each site's observed robbery-rate distribution.

For every permutation:

1. recompute each network Spearman correlation;
2. combine them with the same equal-network Fisher-z statistic;
3. compare the absolute joint statistic with the observed absolute statistic.

Primary p-value is two-sided.

## Why this is appropriate for the Letter question

This analysis tests one general prediction across independent systems while respecting their different data structures.

It does not assume identical raw effect scales, a common sampling variance, a common visitor guild, or that 1,378 Aubert pair-sites equal 1,378 independent networks.

The inferential claim is:

> **the same standardized access-routing association recurs across two independent visitor networks.**

It is stronger than merely listing two separate significant results, but weaker than a many-study random-effects meta-analysis.

## Claim boundaries

Do not call this:

- a pooled causal effect;
- a universal effect size;
- a conventional random-effects meta-analysis;
- evidence that tube length alone is the causal mechanism in Sakhalkar;
- an exact replication of Aubert et al. 2026.

The joint test concerns the common rank-based direction of access constraint and bypass propensity.

## Reproducibility

Implementation: `scripts/analyze_joint_access_routing.py`

Tests: `tests/test_joint_access_routing.py`

Workflow: `.github/workflows/analyze-joint-access-routing.yml`

Raw species and site identifiers are not emitted in the aggregate result.
