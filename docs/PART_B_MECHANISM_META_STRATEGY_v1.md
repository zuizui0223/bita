# Part B: mechanism-level meta-analysis strategy (support, not proof)

## Purpose and decision

This document reframes the empirical meta-analysis from a **proof route** to a
**support route**, and splits the research program into two self-standing parts:

```text
Part A  mathematics     exact local condition + functional-form/regime robustness map
Part B  meta-analysis   real-world support that the model's premise mechanisms hold
                        with the predicted signs, and that their relative strength
                        shifts across ecological regimes as the theorem requires
```

The earlier design tried to identify the mixed partial itself from matched joint
panels (`D1`/`D2`/`D3`). That is the correct route to *proof*, but under the fixed
co-mention corpus the funnel collapses to zero poolable strata
(`meta_analysis_intake/FIXED_CORPUS_CAPACITY_V1.md`). Part B does not need that.

The change is one sentence:

> Stop trying to pool the joint panel. Pool the four marginal mechanisms
> separately, from their own mature literatures, and let the Part A expression
> combine them.

Part A is unchanged. Part B is a redesign of what is estimated, from which
population, and at what claim level.

## Why the previous route collapsed, and what Part B changes

| | Previous (proof route) | Part B (support route) |
|---|---|---|
| Estimand | the mixed partial `∂²W/∂A∂D` on one biological unit | the four marginal arrows `b_A, d_A, e_F, c_D`, each on its own |
| Population | one self-harvested co-mention corpus (17,933 → 0 poolable) | four mature marginal literatures, one per arrow |
| Independence counted | at the joint-panel level (max 1 cluster per path) | marginally, within each arrow (k ≥ 3 is reachable) |
| Headline result | a pooled interaction sign | a **moderator/conditionality** result matching the theorem |
| Unmeasured `c_AD` | blocks the total-sign claim | handled by a break-even/sensitivity threshold |
| Claim level | numerical identification of Part I | empirical support for Part I's premises and its conditionality |

Part B does not overrule `BROAD_META_ANALYSIS_PROTOCOL.md`; it supersedes the
*sourcing and counting* rules that made pooling unreachable. See
`PART_B_STOPPING_RULE_AMENDMENTS_v1.md` for the line-level changes.

## The mathematical hook

Part A's exact local condition is retained verbatim:

\[
\frac{\partial^2 W}{\partial A\,\partial D}
=
\underbrace{H\,d_A e_F}_{\text{tracking}\times\text{barrier}}
-
\underbrace{P\,b_A c_D e^{-c_D D}(1-c_R R)}_{\text{pollination obstruction}}
-
\underbrace{c_{AD}}_{\text{shared cost}}.
\]

The theorem is a statement about **premises implying a conditional sign**. Support
for the theorem therefore does not require measuring the left-hand side. It
requires showing that:

1. each premise arrow exists in nature with the sign the model assumes (B1/B2); and
2. the arrows' relative strength moves across ecological regimes so that the sign
   the theorem predicts to flip actually does (B3); with
3. the one unmeasurable term `c_AD` bounded by a transparent threshold (B4).

## The four marginal arrows and their literatures

Each arrow is a separate meta-analysis with its **own** eligible population. A
study is eligible for an arrow if it estimates that one directional link; it does
**not** need the other three arrows, nor the same plant/site/time as any other
arrow. That co-location requirement belongs only to the joint-panel proof route.

| Arrow | Estimand | Predicted sign | Natural literature |
|---|---|---|---|
| `b_A` | attraction/display trait → pollination/visitation | positive | pollinator-mediated selection; display–visitation |
| `d_A` | attraction/display trait → floral antagonism (florivory, robbing, seed predation) | positive (if antagonists track) | "attractive flowers attract enemies" |
| `e_F` | flower-specific barrier/defence → floral antagonism | negative | floral defence / florivory reduction |
| `c_D` | flower-specific barrier/defence → pollination/access | negative | morphological/chemical access filters |

`d_A` is the empirical crux: its sign and magnitude, relative to `b_A c_D`, are
what put a system in the complementary or the substitutable regime.

## Part B layers (weak → strong)

### B1 — direction meta-analysis (sign / vote-count)

For each arrow, is the predicted sign the majority direction across independent
clusters? Uses a sign test / vote-count over `positive | negative | mixed | null`.
Studies with no extractable effect size still count here, so **every arrow is
covered**. The existing Layer-3 direction map and its 13 anchors live here; Part B
widens the population from the co-mention corpus to the marginal literatures.

```text
report per arrow:  n_clusters, fraction matching predicted sign, and the label
  < 3 evaluable clusters            -> insufficient_directional_clusters
  >= 3 and >= 80% predicted sign    -> premise_supported
  >= 3 and <= 20% predicted sign    -> premise_contradicted
  otherwise                          -> context_dependent (feeds B3)
```

`context_dependent` is not a failure. It is the signal that B3 should look for a
moderator.

### B2 — effect-size envelope (scale-compatible pooling, per arrow)

Within an arrow, pool only inside one effect scale and one design class, oriented
so positive = *more declared trait, more declared outcome*:

```text
visitation / visits          log response ratio (LRR)
damage incidence             log odds ratio (log-OR)
fruit/seed/fitness           standardized regression slope
```

The output is a **role × scale × design envelope** (central tendency + spread +
heterogeneity), not a single "trade-off" number. Pooling gate is unchanged in
form but **counted marginally within the arrow**:

```text
k < 3 independent clusters  -> envelope withheld; report effects + gap
k >= 3                       -> exploratory DerSimonian–Laird random-effects
k >= 5                       -> stability-eligible random-effects
```

This is where the 0-pool collapse is resolved: the four marginal literatures are
individually mature, so `k >= 3` is reachable without manufacturing candidates.

### B3 — conditionality / moderator test (the headline)

The theorem's actual claim is that the sign is **regime-conditional**. So Part B's
primary result is a moderator analysis, not a grand mean. Pre-declared moderators
map to the terms that the theorem says drive the flip:

```text
d_A increases with pollination generalization / display conspicuousness ?
c_D becomes more negative with morphological/chemical access restriction ?
the net channel balance (d_A e_F - b_A c_D) moves with florivore pressure H
  and pollinator service P in the predicted direction ?
```

Support at B3 = effect signs/magnitudes shift across ecological context in the
direction that Part A predicts changes the mixed-partial sign. This tests the
theorem's own content (conditionality), is more informative than a pooled mean,
and does not overclaim a universal sign.

### B4 — break-even bound for the unmeasured `c_AD`

`c_AD` (shared allocation cost) is not recoverable from the channel literatures
and is **not** estimated. Instead, given the B2 envelopes, report the threshold at
which the predicted sign flips:

\[
\tau \;=\; H\,d_A e_F \;-\; P\,b_A c_D\,e^{-c_D D}(1-c_R R),
\qquad
\frac{\partial^2 W}{\partial A\,\partial D} > 0 \iff c_{AD} < \tau .
\]

The empirically anchored, falsifiable statement becomes:

> Given the meta-analytic channel envelopes, the model predicts local
> complementarity unless the shared floral A×B allocation cost exceeds `τ`.

`c_AD` and `c_R·R` stay declared sensitivity axes. B4 turns "we cannot measure it"
into a quantitative, testable boundary rather than a blocked claim.

## Empirically informed regime map

B2 envelopes and B3 moderators feed the existing parameter-envelope machinery to
redraw Part A's regime map with empirical ranges:

```text
per-arrow envelopes (B2)  ->  parameter_envelopes.py scenarios
moderator slopes  (B3)    ->  which regime cells the real data occupy
break-even τ      (B4)    ->  complementary / substitutable / boundary label per cell
```

Reuses `trait_architecture/parameter_envelopes.py`,
`trait_architecture/evidence_yield_meta_analysis.py`, and
`trait_architecture/broad_meta_analysis.py` (pooling + recovery already exist and
are covered by `tests/test_broad_meta_analysis.py`).

## Claim level (honest boundary)

Part B is licensed to say:

> The model's premise mechanisms are present in the published record with the
> assumed signs, and their relative strength shifts across ecological regimes in
> the direction the theorem requires for the local attraction–defence sign to
> change. This is empirical **support** for the conditional regime map.

Part B is **not** licensed to say:

- that the mixed partial's sign has been identified in any single system
  (that is the joint-panel `D1`/`D2` route, deferred to Part III/IV);
- that a pooled marginal effect is a trade-off or a causal adaptation;
- that separate A→P and B→H literatures establish an A–B covariance;
- that leaf/stem defence substitutes for a floral-barrier arrow.

## Prohibitions (carried over and extended)

```text
- Do not pool signs (B1) as effect sizes (B2).
- Do not pool across effect scales or design classes within an arrow.
- Do not merge the four arrows into one pooled "trade-off" mean.
- Do not invert a contrary effect to force agreement.
- Do not present any Part B output as a D1/D2 joint-panel identification.
- Do not estimate c_AD; only bound it via the B4 threshold.
- Do not count two arrows on different units as a joint panel just because both
  appear in Part B.
```

## Deliverables

```text
B1  broad_direction_map.csv                     (widened to marginal literatures)
B2  per-arrow effect-size envelopes             (role × scale × design)
B3  moderator/conditionality summary            (headline)
B4  break-even τ table + sensitivity on c_AD/c_R
    empirically_informed_regime_map.csv         (Part A map re-labelled by real ranges)
```

The paper's Part B result is the B3 conditionality finding plus the B4 break-even
regime map — support for the theorem's conditionality, with proof-level joint-panel
identification kept as a clearly separated future part.
