# Antagonist-relief gate: results

Pre-registered in `LARCENY_GATE_PROTOCOL_V1.md`, committed at `0e36eac` before any estimate here
was computed. Reproduce with:

```bash
python scripts/run_larceny_gate.py artifacts/supplement/larceny_gate
```

**This is the project's first quantitative meta-analysis.** It is a secondary analysis of a
deposited effect-size table (Leal et al. 2025, *Ecology*, doi:10.1002/ecy.70036), not an
independent literature search. §6 states what that costs.

## 1. The gate is open

All effects are oriented log response ratios of larcenist-exposed against unexposed flowers, one
aggregated effect per independent study cluster, DerSimonian–Laird random effects.

| stratum | route | clusters | pooled LRR | 95% CI | *p* | as % change | *I*² |
|---|---|---|---|---|---|---|---|
| **female reproductive success** | `H_to_fitness` | **48** | **−0.210** | −0.351, −0.070 | **0.0034** | **−19.0%** [−29.6, −6.7] | 99.5 |
| nectar standing crop | `H_to_reward` | 28 | −0.483 | −0.757, −0.210 | 0.0005 | −38.3% [−53.1, −19.0] | 99.3 |
| legitimate visitation | `H_to_pollination` | 22 | −0.291 | −0.523, −0.059 | 0.014 | −25.2% [−40.7, −5.7] | 97.5 |
| male reproductive success | `H_to_fitness` | 11 | −0.148 | −1.154, +0.857 | 0.77 | −13.8% [−68.5, +136] | 100.0 |

Under declared bridge assumption B2, the female arrow supports one **necessary condition**:

> **`H > 0` for this floral-antagonist guild.** Realised antagonist pressure is not zero, so the
> antagonist-relief channel `rho = H · d_A · e_F` is not forced to zero by a closed gate.

Had the interval covered zero, `rho ≈ 0` would have forced `W_AD = −iota − kappa ≤ 0` — attraction
and defence unconditionally substitutable, with no conditionality left to explain. That specific
way of ruling out the conditional regime is now removed, on 48 independent study clusters across 60
plant species.

**This is constituent-path evidence and nothing more.** It does not estimate `rho`, `d_A`, `e_F`,
`iota`, `kappa`, or `W_AD`, and it does not identify `M_AD`. A cross-curvature needs a design that
varies `A` and `D` jointly; no study in this dataset does. B2 is an interpretive assumption
attached to this readout, not part of the fixed theory, and the theory was not modified to
accommodate it — the `H_to_*` routes extend the empirical route vocabulary to admit a non-trait
exposure, leaving the corollary untouched.

The male arrow is uninformative, not null: `tau²` = 2.69 and *I*² = 99.998% on 11 clusters. It is
reported because it was declared, and it should not be read as evidence of no effect.

### The mechanism chain: three arrows, but not a demonstrated chain

```text
larceny exposure  ->  nectar standing crop  ->  legitimate visitation  ->  female fitness
                            -38.3%                    -25.2%                  -19.0%
                          (28 clusters)            (22 clusters)          (48 clusters)
```

Each link is separately estimated and each excludes zero, and the magnitudes attenuate
monotonically in the direction the mechanism predicts. **That is weaker evidence than it looks,
and an earlier version of this readout overstated it as "intact end to end."**

The three arrows come from three largely *different* sets of studies. Testing the chain properly
means asking whether it holds *within* studies that measured more than one link:

```text
clusters measuring all three outcomes                                5
of those, all three arrows negative                                  2
clusters measuring both nectar and visitation                       11
within-study correlation of reward depletion with visitation loss   r = -0.17
```

A real reward-depletion mechanism predicts a **positive** correlation there: the studies where
larcenists strip the most nectar should be the studies where visitation falls most. The observed
correlation is slightly negative and, at k = 11, indistinguishable from zero. **The chain is not
demonstrated within studies; it is an alignment of three marginal means across different study
sets.** No conclusion follows about whether the fitness cost is reward mediated.

The reward arrow is the only stratum with no detected funnel asymmetry (§4).

### The pattern is a weak central tendency, not a general rule

The confidence intervals in the table describe the precision of the *mean*. They say nothing about
what the next study would find. With `tau` between 0.46 and 1.64, the 95% prediction intervals do:

| stratum | pooled | `tau` | 95% prediction interval | clusters negative | individually significant |
|---|---|---|---|---|---|
| female | −0.210 | 0.464 | **−1.13, +0.71** | 35/48 (73%) | 21 neg, 2 **pos**, 25 null |
| nectar | −0.483 | 0.674 | **−1.83, +0.87** | 20/28 (71%) | 15 neg, 2 **pos**, 11 null |
| visitation | −0.291 | 0.496 | **−1.29, +0.71** | 14/22 (64%) | 9 neg, 3 **pos**, 10 null |
| male | −0.148 | 1.640 | −3.52, +3.22 | 8/11 | 4 neg, 1 pos, 6 null |

**Every prediction interval covers zero, and covers it widely.** For female reproductive success a
new system could plausibly show anything from a 68% loss to a 100% gain. The sign is not universal
either: two to three clusters per stratum are *significantly positive* — `Irwin & Brody 2000`
returns significantly positive effects on both visitation and female fitness, so in that system
larceny measurably **helped**.

This does not weaken the §1 conclusion, which is about the mean and is what the `H` gate needs. It
sharply bounds everything else. The honest summary is:

> The direction of realised larceny cost is clear. Its magnitude in any particular system is not,
> and neither is its sign.

That is fully consistent with §3: heterogeneity is enormous and none of the four declared context
axes explains it. Read together, the two results say the same thing from opposite ends — **`H` is
itself a strongly context-dependent quantity, and this analysis cannot say what governs it.**

## 2. The corollary's separability assumption fails

`H_to_pollination` was declared as an **audit, not a channel estimate**. The corollary treats
pollinator service `P` and antagonist pressure `H` as separable exogenous regimes, and the
environmental comparative statics in `README.md` are written on that basis. The measured arrow says
they are not separable: larcenist exposure depresses legitimate visitation by 25.2%
[5.7, 40.7], on 22 clusters.

The failure has a **determinate direction**, which is what makes it useful rather than merely
awkward. Differentiating the implemented corollary while allowing `P` to depend on `H`:

```text
separable form   dW_AD/dH = d_A·e_F
measured form    dW_AD/dH = d_A·e_F - (dP/dH)·b_A·c_D·exp(-c_D·D)·(1 - c_R·R)
```

With `dP/dH < 0` and every factor in the second term non-negative, the correction is **positive**.
So rising antagonist pressure pushes `W_AD` toward conditional complementarity *faster* than the
separable model predicts, because antagonists erode the interference channel at the same time as
they load the relief channel. The separable expressions in `README.md` are a conservative special
case with respect to this specific conclusion.

This does not rescue any particular regime classification, and it is not a licence to reinterpret
the Part I grid. It identifies one named assumption as measurably false and states which way the
error runs.

## 3. No context dependence detected — along any declared axis

Six pre-registered moderator analyses. Inference is the random-effects meta-regression contrast
with cluster-robust CR1 errors on cluster-count degrees of freedom; the fixed-effect `Q_between` is
descriptive only.

| analysis | clusters | contrast | 95% CI | *p* | heterogeneity explained | verdict |
|---|---|---|---|---|---|---|
| `larcenist_type` (female) | 48 | −0.324 | −0.772, +0.124 | 0.153 | 2.0% | no detected context dependence |
| `reproductive_assurance` | 47 | −0.229 | −0.551, +0.092 | 0.157 | 0% | no detected context dependence |
| `larceny_assignment` | 44 | +0.060 | −0.244, +0.364 | 0.693 | 7.9% | no detected context dependence |
| `interaction_players` | 37 | ≤0.020 | — | 0.99 | 0% | no detected context dependence |
| `larcenist_type` (visitation) | 21 | −0.208 | −0.814, +0.397 | 0.481 | 0% | no detected context dependence |
| `larcenist_type` (nectar) | 28 | +0.177 | −0.552, +0.905 | 0.622 | 0% | no detected context dependence |

**These nulls must be read as "not detected at the declared design."** The committed power
analysis sets the detectable contrast at roughly 0.69 on this scale at 5 clusters per level. The
largest observed contrast is 0.32. The design was never able to resolve a contrast this size, and
the protocol said so before the data were touched.

### The declared hypotheses, honestly scored

`H1` predicted that **robbing** — the larcenist a corolla barrier can exclude — is the costlier.
The point estimates run the other way:

```text
nectar theft    -0.405  [-0.697, -0.113]   -33.3%   7 clusters
nectar robbing  -0.173  [-0.322, -0.023]   -15.9%  41 clusters
```

Both levels individually exclude zero; the contrast between them does not. **H1 is not supported,
and its converse is not established either.** The direction agrees with the source publication,
which reports theft as the damaging larcenist — but that publication's inference rests on a
phylogenetic multilevel model this repository does not implement, and the contrast is not
resolvable under the declared analysis. Recording the declared hypothesis as unsupported is the
point of declaring it.

The theory consequence sketched in the protocol therefore stays **open**. If the theft-costlier
direction is real, `e_F` is small exactly where `H` is large, their product collapses, and the
antagonist-relief channel is weaker than the open gate in §1 suggests. Settling that needs more
clusters at the theft level than the 7 available here.

`reproductive_assurance` also ran opposite to its declared direction. Self-**compatible** species
showed the more negative effect (−25.4% [−38.4, −9.8]) and self-**incompatible** species an
interval covering zero (−6.0% [−25.5, +18.6]) — the reverse of the buffering the corollary's
`(1 − c_R·R)` term predicts. The contrast is not significant (*p* = 0.157), so this is a
direction to test, not a finding.

### The real result here is that the moderators explain nothing

Residual `tau²` barely moves from unconditional `tau²` in every analysis: 0–8% of heterogeneity
explained, and exactly 0% in four of six. With *I*² at 97–99.5%, the effect of floral larceny is
**enormously** variable across studies and **none of the four declared ecological context axes
captures that variation.** Whatever makes larceny costly in one system and harmless in another, it
is not larcenist type, not mating system, not study design, and not the functional-group pairing.

That is a substantive negative result about where to look next, and it is more informative than
any of the individual nulls.

## 4. Funnel asymmetry, and why it is not simply publication bias

| stratum | Egger intercept | *p* | verdict |
|---|---|---|---|
| female | −0.599 | 1.6e−09 | asymmetry detected |
| visitation | +0.293 | 0.021 | asymmetry detected |
| nectar | −0.003 | 0.98 | no detected asymmetry |

The female stratum shows strong asymmetry and it is reported rather than buried: taken at face
value it means small studies report more negative larceny effects, and the pooled −0.210 may be
inflated in magnitude.

It should not be taken entirely at face value. For a **log response ratio** the sampling variance
is a function of the group means themselves, so the effect and its standard error are
mathematically dependent, and Egger-type regression on this metric is known to over-detect
asymmetry. The two facts that the asymmetry runs in *opposite directions* on the female and
visitation strata, and is absent on the reward stratum, are more consistent with that artefact than
with a single coherent publication filter.

What can be said without resolving it: the **direction** of the female arrow does not depend on any
single cluster. Leave-one-cluster-out across all 48 clusters — and all clusters in every one of the
six analyses — leaves the pooled direction unchanged in 100% of refits.

## 5. Robustness to the declared ingest choices

Pooled effects under every pre-declared variant:

| variant | female | visitation | nectar |
|---|---|---|---|
| `rho_w = 1.0` (primary, conservative) | −0.2105 | −0.2907 | −0.4834 |
| `rho_w = 0.5` | −0.2101 | −0.2975 | −0.4900 |
| `rho_w = 0.0` | −0.2082 | −0.3071 | −0.4980 |
| + the 3 quarantined sign-discrepant rows | −0.2152 | −0.2833 | −0.4459 |

All three arrows keep their sign, magnitude, and exclusion of zero throughout. The within-cluster
correlation assumption is not doing any work.

```bash
python scripts/ingest_deposited_larceny_dataset.py SOURCE.csv OUT --within-cluster-correlation 0.5
python scripts/ingest_deposited_larceny_dataset.py SOURCE.csv OUT --include-quarantined
```

## 6. What this is not

- **Not an independent literature search.** The search, screening, and extraction were done by the
  authors of the source synthesis. Their inclusion criteria define the population, and any error in
  their extraction is inherited. `larceny_recomputation_audit.csv` records every row this
  repository could and could not reproduce from the deposited group means.
- **Not a discovery.** The source publication reported on this dataset first. The contribution here
  is the channel mapping in §1–§2 and the declared context-dependence verdict, neither of which
  that publication was attempting.
- **Not general to floral antagonists.** Nectar larceny is one guild. `H` in the corollary is
  antagonist pressure in general, and nothing here licenses transfer to florivores, bud predators,
  or seed predators.
- **Not the mixed partial.** These are marginal route effects. Under B2 the fitness arrow
  constrains whether `rho` can be non-zero; it does not estimate `rho`, `d_A`, `e_F`, or `W_AD`.
- **Not `d_A`.** The committed value-of-information ranking puts `attraction_tracking` first of
  five. This measures the gate that multiplies it, not the parameter itself. The highest-leverage
  measurement remains unmade.

## 7. Data integrity note on the source deposit

Recomputing all 267 deposited rows from their own group means, before any analysis:

```text
reproduced as log response ratio          260
variance disagrees, point estimate agrees   4   retained, variance recomputed
sign disagrees                              3   quarantined; sensitivity run in §5
reproduced as Hedges' g                     0
```

The deposited file is named `complete_hedges.csv` and its metadata describes `yi` as "Effect size
(Hedges'g)", but the deposited analysis script computes `escalc("ROM", ...)` and the numbers
reproduce log response ratios exactly. **The label is wrong; the numbers are right.** This is
recorded because it is material to anyone reusing that deposit — and because it happens to be
convenient here, putting the arrow on the same scale as every other declared route in this
repository.

The three sign-discrepant rows cannot be adjudicated without the source articles, which this
environment cannot reach. Neither side was adopted silently; §5 reports both.
