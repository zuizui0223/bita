# Biotic Interaction Trait Architecture

Reproducible **Mechanism → Pattern** study of one focal floral attraction trait (`A`), one focal flower-specific barrier/defence trait (`D`), and one declared outcome scale (`W`).

The canonical paper is now explicitly divided into two scientific halves:

```text
Part I — Mechanism
mathematical theory / local sign principle / sensitivity

Part II — Pattern
meta-analysis / quantitative cross-study synthesis / recurrence and conditionality
```

The paper is not “theory + illustrative literature.” Part I derives why and when attraction and defence become locally complementary or substitutable. Part II tests which mechanism-derived patterns recur across independent systems, where their state changes with context, and which quantities remain unidentified.

The **fixed theoretical core** and the **mechanism-pattern empirical synthesis** are kept inferentially separate: the synthesis asks **what is recurrent, what is context dependent, and what remains unidentified**. The finite sensitivity analysis **is not an empirically calibrated regime map**, and none of the route counts estimates prevalence in nature.

## Part I — Mechanism

For a declared `A`–`D` pair and declared `W` scale, the local mixed partial

```text
W_AD = d2W / dA dD
```

measures how one focal trait changes the other's local marginal effect on that declared outcome scale.

The signed bookkeeping identity is

```text
W_AD = M_AD - G_AD - C_AD
```

and does not uniquely identify biological mechanisms from total `W` alone.

After the focal orientation gate is established,

```text
W_AD = rho - iota - kappa

rho   = antagonist-relief magnitude
iota  = mutualist/pollinator-interference magnitude
kappa = direct joint-cost curvature
```

Local complementarity requires `rho > iota + kappa`; local substitutability requires the reverse inequality. The result is local and does not by itself imply trait covariance, genetic correlation, an evolutionary trajectory, a stable optimum, or an evolved environmental cline.

### One-sided selectivity bound

The balance yields one stronger structural statement than the bookkeeping identity. Define the **selectivity window** as the region where antagonist relief exceeds pollinator interference before direct joint cost is charged. Under the declared non-negative `relief - interference - cost` family,

```text
W_AD > 0  =>  inside the selectivity window
```

so **complementarity does not occur outside the window**. Across all 2,592 declared evaluations there are zero counterexamples. The converse is false: window precision is 77.2%, so about 23% of in-window evaluations are still substitutable. With joint cost set to zero, the window becomes the exact criterion.

The bound can fail only if joint-cost curvature is negative and sufficiently large in magnitude. Because `c_AD` is not directly measured in the strict evidence layer, its sign is the minimal empirical gate for the biological applicability of this one-sided theorem.

Within a neighbourhood where the orientation gate remains valid,

```text
W_AD(P,H) = rho(P,H) - iota(P,H) - kappa(P,H)

dW_AD/dH = d rho/dH - d iota/dH - d kappa/dH
dW_AD/dP = d rho/dP - d iota/dP - d kappa/dP
```

Greater antagonist pressure or pollinator service has no universal direction unless the corresponding derivative inequality is satisfied.

The canonical endpoint-normalized sensitivity run contains 2,592 declared mixed-partial evaluations. Its percentages are unweighted occupancies of the finite design, not empirical probabilities or prevalence estimates. Reproductive assurance `R` remains only an auxiliary background moderator, not a third focal trait.

## Part II — Pattern

Part II uses meta-analysis only where outcomes admit defensible common quantitative scales and preserves a source-adjudicated pattern scaffold where they do not.

### Meta-analysis 1 — floral larceny

The Leal et al. 2025 deposited study-level data are reanalysed with study-cluster random-effects meta-analysis on oriented log response ratios:

```text
female reproductive success  LRR -0.210  48 independent clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

Dependence, influence, sensitivity analyses, and extreme among-study heterogeneity remain explicit. For female reproductive success, 35/48 clusters are negative, but the 95% prediction interval is -1.13 to +0.71 and significantly positive systems occur. Six declared moderator analyses explain only 0-8% of the heterogeneity. The antagonist-pressure gate is therefore open on average, not universal, and the declared context axes do not yet locate its variation.

The apparent nectar -> visitation -> female-fitness sequence is not treated as a demonstrated within-study mechanism: only five clusters measured all three outcomes, two had all three negative, and the within-study nectar-visitation association across eleven shared clusters is `r = -0.17`.

### Meta-analytic synthesis 2 — floral volatiles

The Sasidharan et al. 2023 deposited synthesis is reconstructed with a conservative 32-study-component dependence topology:

```text
florivore physiological detection  84/103
pollinator physiological detection 151/220
assembled risk difference           +0.129
leave-one-study-component-out       positive 32/32
```

Only three study components contain both physiological consumer roles and all three paired differences are zero, so the assembled contrast is not treated as a causal within-study role effect. Behavioral disagreements remain part of the context-dependence result.

### Secondary contextual syntheses

Three additional published syntheses are retained without pooling their incompatible scales with the two reproduced modules:

- Haas-Desmarais et al. 2026: 171 studies / 1,348 study cases; publisher supplement package independently retrieved and hashed; herbivory is not relabelled as focal `D`.
- Caruso et al. 2019: main selection analysis of 755 gradients with SE from 36 articles; Dryad landing/API metadata verified, file-byte access currently blocked; selection gradients are not `W_AD`.
- Junker & Blüthgen 2010: 18 publications / 425 floral-scent response observations; floral-resource dependence is an independent consumer-filtering pattern, not a pollinator/antagonist identity map.

### Theory-to-pattern scaffold

The heterogeneous route ledger is **not a grand meta-analysis**. It maps quantitative and directional evidence onto the mechanism classes derived in Part I. After the registered saturation expansion:

```text
56 source-adjudicated effect/directional records
25 independent biological study clusters
A_to_pollination:    5 clusters
A_to_antagonism:     8
D_to_antagonism:    18
D_to_pollination:   10
same-system:        14 clusters
context/sign switch: 17 clusters
context-only programs: 7, excluded from route-ledger N
direct A x D:        1 strict cluster, sign unresolved
direct joint cost:   0 strict estimates, kappa unidentified
```

The expansion adds visual and multidimensional attraction-signal systems, chemically and physically distinct flower-specific defence mechanisms, guarded states, spatial/temporal/attack-mode filtering, visitor functional-mode switching, and lifecycle-stage role reversal. Incompatible response constructs are not averaged merely to manufacture a pooled effect.

## Cross-system result

The empirical generality is deliberately hierarchical:

> **recurrent constituent mechanisms + context-dependent balance inside a one-sided selectivity window**

Route separation, guarded defence, and consumer filtering recur across independent systems, but the theorem fixes their role: they identify where complementarity can occur, not that it must occur. Exposure (`H` relative to `P`) moves the window and is demonstrably heterogeneous. Direct joint-cost curvature determines whether the strongest one-sided bound is biologically applicable, yet its sign remains unmeasured. The cross-system Pattern therefore supports a moving permissive window rather than a universal positive or negative `W_AD`.

## Mechanism → Pattern inference boundary

The active submission must preserve:

```text
marginal route evidence
!= same-system evidence
!= direct A x D evidence
!= complete W_AD decomposition
```

Therefore:

- neither meta-analytic module estimates `rho`, `iota`, `kappa`, or `W_AD`;
- route/study/deposit counts are not prevalence estimates or model parameters;
- one direct `A x D` cluster is not generalized to a universal sign;
- zero strict joint-cost studies means `kappa` is unidentified, not zero.

## Manuscript and figures

Canonical manuscript:

- `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`
- `manuscript/TABLES_THEORETICAL_ECOLOGY.md`

Visual split:

```text
Figures 1–2 + Tables 1–2 = Part I Mechanism
Figure 3 + Tables 3–4     = Part II Pattern
Supplementary Figure S4   = quantitative robustness
```

Figure 3 is generated reproducibly from the same evidence universe as the canonical mechanism-coverage audit and is byte-checked by CI. Figures 1–3 also have a validated reproducible EPS export workflow.

## Current decision

The scientific story is closed at a deliberately one-sided boundary: the bookkeeping identity is not the novelty; the strongest structural result is the selectivity-window theorem, and Part II establishes recurrent pathways plus a heterogeneous antagonist-pressure gate without claiming a universal total sign. The next empirical hinge is the sign of `c_AD`, testable first with a 2 x 2 allocation experiment; a full `A x D` factorial remains the harder route to total `W_AD`.

Additional broad evidence searching is not a default blocker for this claim set. Remaining submission actions are author-controlled metadata/licence/archive fields and the authenticated journal portal.
