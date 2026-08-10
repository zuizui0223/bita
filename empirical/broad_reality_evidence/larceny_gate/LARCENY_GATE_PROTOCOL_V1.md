# Antagonist-relief gate: pre-registered secondary analysis of a deposited effect dataset

**Status: written and committed before any pooled estimate, subgroup estimate, meta-regression,
or moderator verdict was computed.** What had been inspected beforehand is stated in §8.

## 1. Why the empirical target moved

The previously declared target was the `D -> legitimate pollinator use` route, feeding the
mutualist-interference magnitude `iota`. That target was not abandoned for being wrong. It was
abandoned for being unreachable: 11 of its 15 screened include-candidates sit behind paywalls this
execution environment cannot read, leaving on the order of one to two extractable clusters against
a declared threshold of five. `IOTA_PATHWAY_FEASIBILITY_V1.md` records that finding and it stands.

What changed is not the literature. It is that GitHub code search became answerable from this
environment, which makes the **deposited-data layer** searchable for the first time. Deposited
effect-size tables from published syntheses carry per-primary-study group means, dispersions, and
sample sizes — the exact quantities the extraction protocol asks a human reader to copy out of a
full text. Reaching them does not require reaching the publisher.

## 2. Source dataset

```text
repository   https://github.com/lacaleal/Meta-analysis_larcenists
commit       04663ff895b300fc957c4a32f661e5f73ca95217
file         complete_hedges.csv
publication  Leal et al. 2025, Ecology, "Costs of floral larceny: A meta-analytical evaluation of
             nectar robbing and nectar theft on animal-pollinated plants"
doi          10.1002/ecy.70036
```

267 effect rows, 69 study clusters, 60 plant species. Each row carries `n`, `mean`, and `sd` for a
larcenist-exposed group and an unexposed control group, plus the four context variables used below.

**This is a secondary analysis of someone else's synthesis, and that is a limit on what it can
claim.** The search, screening, inclusion decisions, and extraction were performed by those
authors. This analysis inherits their inclusion criteria and any extraction error in them. It is
not an independent literature search and must never be reported as one. Its contribution is the
mapping onto the declared channel, the recomputation in §4, and the context-dependence verdict
under this repository's calibrated machinery.

## 3. What this measures in the theory

The implemented corollary's antagonist-relief contribution is

```text
rho = H * d_A * e_F
```

`H` is floral-antagonist pressure and it enters **multiplicatively**. Every previously declared
route measures a trait slope (`d_A`, `e_F`, `c_D`, `b_A`); none measures `H`. Yet `H` gates the
whole channel, and the gate has a sharp consequence:

```text
if H = 0 then rho = 0, so W_AD = -iota - kappa <= 0 whenever iota, kappa >= 0
```

That is, **if floral antagonists impose no realised cost, the local A x D mixed partial is
unconditionally non-positive and there is no conditionality to explain.** The project's whole
theoretical claim — that attraction x defence becomes *conditional* — requires the gate to be open.
Nothing in this repository has tested that.

### Bridge assumption B2 (declared, not demonstrated)

> The pooled oriented log response ratio of larcenist exposure on plant reproductive success is a
> monotone increasing function of `H`, and equals zero exactly when `H = 0`, holding `d_A` and
> `e_F` fixed.

Under B2:

| pooled result | licensed statement |
|---|---|
| interval excludes zero, negative | `H > 0` for this antagonist guild; the relief channel has material to act on and `W_AD` is genuinely contested |
| interval includes zero | no evidence that `H > 0` for this guild; on this evidence `rho ≈ 0` and the corollary predicts unconditional substitutability |

B2 is an assumption. It is not tested here and it is not implied by the corollary.

### Declared routes and strata

Three routes are added to the declared route vocabulary, because no existing route has an
antagonist as the exposure:

| route | expected sign | what it is for |
|---|---|---|
| `H_to_fitness` | negative | the gate on `rho` |
| `H_to_pollination` | negative | **assumption audit**, not a channel estimate (see below) |
| `H_to_reward` | negative | the mechanism linking the two |

`H_to_pollination` is an audit of the corollary itself. The corollary treats pollinator service `P`
and antagonist pressure `H` as separable exogenous regimes. If larcenist exposure depresses
legitimate visitation, `P` is not exogenous to `H`, and the separable environmental comparative
statics in `README.md` are a special case rather than a description. A non-zero result here
constrains the model; it does not estimate a channel.

Strata declared, all on the log-response-ratio scale, `design_class = comparative`:

```text
HF_larceny_female_lrr_comparative      H_to_fitness       female reproductive success   primary
HP_larceny_visitation_lrr_comparative  H_to_pollination   legitimate visitation rate    audit
HR_larceny_nectar_lrr_comparative      H_to_reward        nectar standing crop          mechanism
HF_larceny_male_lrr_comparative        H_to_fitness       male reproductive success     secondary
```

`design_class` is `comparative` for every stratum **so that the experimental/observational split
can be tested as a declared moderator rather than assumed by partitioning the stratum key.**

## 4. Extraction rule: recompute, do not copy

The deposited `yi`/`vi` columns are **not** used as the effect. Every effect is recomputed from the
deposited group means, dispersions, and sample sizes by this repository's own
`effect_estimate` on `effect_input_type = group_means`. Two reasons, both found before this
protocol was written and both recorded in the committed audit table:

1. **The deposited metric is mislabelled.** The file is named `complete_hedges.csv`, its metadata
   calls `yi` "Effect size (Hedges'g)", and the analysis script computes `escalc("ROM", ...)` —
   a log response ratio. Recomputation confirms the script: 260 of 267 rows reproduce
   `ln(mean_larcenist / mean_control)` and its ROM variance to within 1e-6, and **zero** rows
   reproduce Hedges' g. The deposited values are log response ratios. This is fortunate rather
   than merely correct: it puts the arrow on the same scale as every other declared route.
2. **Seven rows disagree with their own group means.** Three have `yi` equal to the negative of
   `ln(mean_larcenist / mean_control)`; four match on the point estimate but not on the variance.

Declared handling of the seven:

- The three **sign-discrepant** rows are set `analysis_status = not_eligible` with reason
  `deposited_effect_sign_disagrees_with_deposited_group_means`. Which side is correct cannot be
  settled without the source articles, which this environment cannot reach, so neither side is
  silently adopted. A declared sensitivity run includes them at the deposited sign.
- The four **variance-discrepant** rows are retained; the point estimates agree and the variance is
  recomputed by the standard ROM formula.

Rows whose group means are not both strictly positive cannot yield a log response ratio and are
excluded with reason `non_positive_group_mean`.

## 5. Independence and within-study aggregation

The 267 rows are not independent: 69 clusters contribute up to 11 effects each. A study cluster is
one publication, following the source dataset's `study` field, which is this repository's declared
independence rule applied to the source's own grouping.

**Every cluster is reduced to exactly one effect per stratum before analysis.** For a cluster with
`m` effects, values `y_i` and variances `v_i`:

```text
aggregate value    = (1/m) * sum(y_i)
aggregate variance = (1/m^2) * [ sum(v_i) + rho_w * sum_{i != j} sqrt(v_i * v_j) ]
```

`rho_w` is the assumed within-cluster correlation among effects. **The declared primary value is
`rho_w = 1.0`**, the maximally conservative choice: it assumes the within-study effects carry no
independent information and inflates the aggregate variance accordingly. Sensitivity runs at
`rho_w = 0.5` and `rho_w = 0.0` are declared in advance and reported alongside.

This is stricter than the cluster-robust machinery already in the repository, which tolerates
multiple effects per cluster. It is chosen so that the pooled estimate and every moderator analysis
run on the identical, fully independent one-effect-per-study set.

Consequence, declared in advance: a cluster that spans more than one level of a moderator cannot be
assigned a level after aggregation. Such clusters are coded `not_applicable` for that moderator
only, with the basis recorded. At most four of 48 clusters are affected on any one moderator.

## 6. Declared moderators

On the primary stratum, thresholds carried over from the committed design power analysis
(5 clusters per level, 10 total, for confirmatory moderators; 3 and 6 for exploratory):

| moderator | levels | reference | role |
|---|---|---|---|
| `larcenist_type` | `nectar_robbing`, `nectar_theft` | `nectar_robbing` | primary |
| `reproductive_assurance` | `self_compatible`, `self_incompatible` | `self_incompatible` | confirmatory |
| `larceny_assignment` | `experimental_manipulation`, `observational_contrast` | `experimental_manipulation` | design audit |
| `interaction_players` | `insect_insect`, `insect_bird`, `bird_bird` | `insect_insect` | exploratory |

### `larcenist_type` is the theory-relevant contrast

Nectar **robbers** pierce the corolla from outside. Nectar **thieves** enter the flower legitimately
and remove reward without transferring pollen. A flower-specific barrier trait `D` — corolla
thickness, tube length, calyx armature — is a defence against *piercing*. It is close to useless
against a thief that uses the legitimate entrance.

So `e_F`, barrier efficacy, is high against robbers and low against thieves, and the declared
mechanistic hypothesis is:

> **H1**: nectar robbing imposes a more negative effect on reproductive success than nectar theft.

The theory consequence runs in **both** directions, which is why the test is worth running either
way:

- **If robbing is the costlier**: the barrier trait relieves the antagonist that actually matters.
  `H` and `e_F` are large together, `rho` is substantial, and the conditional regime of the
  corollary is reachable in nature.
- **If theft is the costlier**: the costly antagonist is the one a corolla barrier cannot exclude.
  `e_F` is small exactly where `H` is large, their product collapses, `rho` is small, and
  `W_AD ≈ -iota - kappa` — attraction and defence are **substitutes, not conditionally
  complementary**, for this antagonist guild.

`reproductive_assurance` is the model's own auxiliary moderator `R`. The corollary carries
`(1 - c_R * R)` on the pollination-mediated term, so self-compatibility should buffer a
pollination-mediated fitness cost. Declared hypothesis: the effect is less negative in
self-compatible species.

## 7. Analysis, fixed in advance

Executed by the already-committed and already-power-tested code, unmodified:
`random_effects_pool`, `subgroup_analysis`, `meta_regression`, `leave_one_cluster_out`,
`egger_small_study_test`.

Reporting rules carried over unchanged:

- Inference on a moderator comes from the **random-effects meta-regression contrast** with
  cluster-robust standard errors on cluster-count degrees of freedom. The fixed-effect
  `Q_between` is descriptive only; its false-positive rate reaches 0.60 under realistic
  heterogeneity.
- `context_dependent_direction_reversal` requires both level intervals to exclude zero with
  opposite signs.
- A null is "not detected at the declared design", never evidence of no effect.

## 8. Disclosure: what was known before this was written

Honesty about pre-registration requires saying what was already seen.

- **The dataset's structure was inspected first**: column names, 267/69/60 counts, moderator level
  names, and cluster counts per level. The thresholds in §6 were checked against those counts, so
  they are feasible by construction rather than by luck.
- **Nine of 267 effect values were read**: two rows during schema inspection and seven during the
  metric verification in §4. No pooled, subgroup, or moderator estimate was computed.
- **The source publication's headline findings were read** in a search result before this protocol
  was written. They report that robbers had no effect on female or male reproductive success while
  thieves reduced both, and that effects were unrelated to mating system or to robber/pollinator
  identity.

That last point matters, so it is stated plainly rather than buried: **hypothesis H1 in §6 is
declared in the direction the source publication contradicts.** It is written from the barrier
mechanism, not from the data, and it is left standing as declared. This analysis therefore claims
no discovery. It is a re-analysis, on a different question, of a result already in the literature,
and its value is the theory mapping in §3 and §6 — which the source publication does not make and
was not trying to make.

## 9. Boundaries

- Nectar larceny is **one** floral-antagonist guild. `H` in the corollary is antagonist pressure in
  general. Nothing here licenses generalisation to florivores, bud predators, or seed predators.
- The result is a marginal route effect. It is not the mixed partial, not a channel curvature, and
  not an environmental derivative of the mixed partial.
- The pooled estimate is a property of the studies the source authors included. Their inclusion
  criteria, not this repository's, define the population.
- Under B2 the pooled arrow constrains whether `rho` can be non-zero. Without B2 it remains a
  statement about realised larceny costs and nothing more.
