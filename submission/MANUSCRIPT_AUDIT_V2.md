# Manuscript audit — paperization state

## Verdict

**Scientific conclusion: frozen and internally coherent. Reader-facing manuscript: paperized around the one-sided selectivity bound. External submission: pending human-controlled metadata/release/rendering only.**

Canonical title:

> **When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns**

Canonical architecture:

```text
1 Introduction
2 Part I — Mechanistic theory: mechanism and principle
3 Part I results — mechanistic sign regimes
4 Part II — Meta-analysis and cross-study pattern synthesis
5 Part II results — meta-analytic patterns across systems
6 Integration — from mechanism to pattern
7 Conclusions
```

## 1. Part I — Mechanism: PASS

The paper preserves:

```text
W_AD = M_AD - G_AD - C_AD
orientation gate
W_AD = rho - iota - kappa
```

The identity is not sold as novelty. The strongest result is the one-sided bound:

```text
if kappa >= 0 and W_AD > 0, then rho > iota
```

Therefore complementarity cannot occur outside the selectivity window under the declared non-negative joint-cost premise. The converse is false when positive joint cost is present.

Implementation verification remains:

```text
2,592 declared endpoint-normalized evaluations
0 complementary evaluations outside the window
window precision 77.2%
~23% of in-window evaluations substitutable
zero-joint-cost limit: exact window/sign equivalence
```

These fractions are finite-design occupancies, not prevalence estimates.

Proposition 1, the orientation boundary, environmental derivative conditions, parameterization caveat, and distinction between proof and numerical verification remain intact.

## 2. Failure mode and falsifiability: PASS

Outside-window complementarity requires

```text
kappa < rho - iota <= 0
```

so negative joint-cost curvature is necessary for failure of the bound and a sufficiently negative value is sufficient within the declared family.

The manuscript correctly treats non-negative joint cost as a model premise rather than established biology. Direct `c_AD` remains empirically unidentified.

The next tests have distinct roles:

- **2 × 2 allocation design:** applicability/falsification gate for joint-cost curvature;
- **full A × D factorial:** total-interaction calibration and channel allocation.

## 3. Part II — Pattern: PASS

Canonical saturated evidence state:

```text
56 route-level records
25 independent biological study clusters
A -> pollination:         5
A -> antagonism:          8
D -> antagonism:         18
D -> pollination:        10
same-system multi-route: 14
context/sign-switch:     17
context-only programs:    7  (excluded from route-ledger N)
direct total A x D:       sparse / unresolved
direct joint cost:        0 strict estimates
```

The route ledger is correctly presented as a source-adjudicated Pattern scaffold rather than a grand cross-outcome meta-analysis.

### Leal floral-larceny module: PASS

Canonical pooled state remains approximately:

```text
female reproductive success  LRR -0.210  48 clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

The reader-facing interpretation is appropriately narrower than a universal antagonist-cost law:

- female fitness negative in 35/48 clusters;
- 95% prediction interval approximately `-1.13` to `+0.71`;
- declared moderators explain only 0–8% of heterogeneity;
- pooled directions remain robust under the declared sensitivity/influence framework.

Thus the H/exposure gate can be open on average but remains system dependent.

The reward → visitation → female-fitness sequence remains constituent-path evidence only; the manuscript does not claim an end-to-end causal mechanism.

### Sasidharan floral-volatile module: PASS with composition boundary

Canonical state remains:

```text
32 conservative study components
florivore physiological detection 84/103
pollinator physiological detection 151/220
assembled risk difference +0.129
LOCO direction positive 32/32
```

The paired-role limitation and study-composition caveat remain explicit. The assembled contrast is not relabelled a causal within-study role effect.

### Secondary contextual syntheses: PASS with status separation

Haas-Desmarais et al. (2026), Caruso et al. (2019), and Junker & Blüthgen (2010) remain secondary contextual/cross-synthesis modules. Their scales and study/observation counts are not pooled with the reproduced modules or route-ledger N.

## 4. Mechanism → Pattern linkage: PASS

The supported integrated conclusion is:

> **one-sided mechanistic theorem + recurrent but context-dependent empirical Pattern**

The empirical half demonstrates recurrence, switching, same-system linkage, gate opening, and identification gaps. It does not calibrate `rho`, `iota`, `kappa`, or total `W_AD`.

The main reader-facing distinction is now clear:

- **structurally general:** the one-sided impossibility boundary under its premise;
- **empirically recurrent:** constituent pathways and switching architectures;
- **context dependent:** exposure and realised balance inside the permissive region;
- **decisive next test:** joint-cost curvature, followed separately by a full factorial calibration.

## 5. Novelty boundary: PASS

The manuscript does not claim novelty for:

- cross-trait curvature or correlational selection;
- pollinators and antagonists jointly shaping plant fitness;
- floral attraction exposing flowers to antagonists;
- defence carrying pollination costs;
- non-additive mutualist/antagonist effects;
- context dependence itself.

The defensible novelty is the combination of:

1. a mechanism-facing orientation and non-identifiability architecture;
2. the one-sided selectivity-window theorem;
3. identification of sufficiently negative joint-cost curvature as the unique escape route in the declared family;
4. conversion of the theorem's applicability into a tractable 2 × 2 allocation test;
5. a theory-structured cross-system synthesis that preserves incompatible outcome scales and evidence levels.

## 6. Reader-facing paperization: PASS for current text

The current manuscript now:

- foregrounds the one-sided bound in the title;
- gives the theorem, failed converse, 56/25 Pattern state, H-gate heterogeneity, and `c_AD` test in the Abstract;
- shortens the Introduction while preserving prior art and the ecological inference gap;
- retains Methods/Results numerical states unchanged;
- ends the Conclusion on a falsification/calibration programme rather than generic calls for more data;
- synchronizes portal metadata and cover-letter framing.

Remaining editorial work is human reading/visual QA, not further scientific discovery by default.

## 7. Inference-boundary audit: PASS

The manuscript/package preserves:

```text
marginal route evidence != W_AD
same-system evidence != direct total A x D
route counts != prevalence
finite-grid occupancy != prevalence
Leal pooled effects != rho/iota/kappa/W_AD
Sasidharan assembled contrast != causal paired role effect
zero strict joint-cost estimates != kappa = 0
2 x 2 focal-pair applicability test != global universality
W_AD != automatic evolutionary trajectory/covariance prediction
```

## 8. Figures, tables, supplement, references: PASS / release rerun pending

- Main Figures 1–3 retain canonical SVG sources.
- Tables 1–4 remain synchronized to Mechanism/Pattern roles.
- Supplementary Figures S1–S4 and Tables S1–S6 retain reproducible builders.
- Quantitative robustness remains in the supplement rather than overloading the main Pattern figure.
- Scientific reference spine remains regression-protected.
- Final release-commit figure/supplement build and rendered citation/reference QA remain pending.

## 9. External-submission blockers

These are human/release controls rather than scientific gaps:

- final author order/publication names;
- affiliations and corresponding-author details;
- ORCIDs;
- CRediT roles;
- funding/no-funding statement and acknowledgements;
- competing-interest confirmation;
- repository licence;
- five conflict-checked reviewer suggestions;
- exact immutable release/tag and archival DOI;
- final rendered manuscript/supplement visual QA;
- all-author approval;
- authenticated journal-portal submission.

## Final decision

**The manuscript no longer needs additional broad evidence searching to become scientifically coherent. The repository should remain in paperization/release mode unless a specific claim is falsified, a reviewer exposes a concrete evidence/provenance gap, or an inference-boundary correction becomes necessary.**
