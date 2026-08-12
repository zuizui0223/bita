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

Dependence, influence, sensitivity analyses, and extreme among-study heterogeneity remain explicit.

### Meta-analytic synthesis 2 — floral volatiles

The Sasidharan et al. 2023 deposited synthesis is reconstructed with a conservative 32-study-component dependence topology:

```text
florivore physiological detection  84/103
pollinator physiological detection 151/220
assembled risk difference           +0.129
leave-one-study-component-out       positive 32/32
```

Only three study components contain both physiological consumer roles and all three paired differences are zero, so the assembled contrast is not treated as a causal within-study role effect. Behavioral disagreements remain part of the context-dependence result.

### Theory-to-pattern scaffold

The heterogeneous route ledger is **not a grand meta-analysis**. It maps the quantitative and directional evidence onto the mechanism classes derived in Part I:

```text
38 source-adjudicated effect/directional records
14 independent biological study clusters
A_to_pollination:   4 clusters
A_to_antagonism:    5
D_to_antagonism:   10
D_to_pollination:   7
same-system:       10 clusters
context/sign switch: 11 clusters
direct A x D:       1 strict cluster, sign unresolved
direct joint cost:  0 strict estimates, kappa unidentified
```

Incompatible response constructs are not averaged merely to manufacture a pooled effect.

## Cross-system result

The empirical generality is deliberately specific:

> **recurrent constituent mechanisms + context-dependent balance**

The constituent processes required by the mathematical theory recur across independent systems, while dose, resources, exposure, consumer identity, response definition, and compound identity repeatedly alter which channel is expressed. This is the cross-system Pattern predicted by the conditional Mechanism; it is not a universal sign of `W_AD`.

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

The registered scientific gate is closed. The canonical manuscript is now a **mathematical Mechanism + meta-analytic Pattern** paper. Additional broad evidence searching is not a default blocker. Remaining submission actions are author-controlled metadata/licence/archive fields and the authenticated journal portal.
