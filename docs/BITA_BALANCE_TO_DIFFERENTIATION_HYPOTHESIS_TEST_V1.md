# BITA main hypothesis: why balance persists, why functions differentiate, and when evolution cannot reach the better architecture

**Status:** new theory-only numerical test; independent of the active nectar-robbery Letter. This is **not** empirical confirmation of evolutionary history or a newly discovered general specialization principle.

## Focal question, with phenotype scope made explicit

Within an organism, why can two tasks that were formerly controlled by one multifunctional trait coordinate remain balanced, or instead become partly assigned to **two differentiated trait coordinates**? This tests within-phenotype functional division, **not** population polymorphism, disruptive selection, sympatric speciation, or diversification into separate species. Those require additional ecological/genetic models.

Existing related theory includes Rüffler, Hermisson & Wagner (2012, PNAS, DOI 10.1073/pnas.1110521109) and Guillaume & Otto (2012, Genetics, DOI 10.1534/genetics.112.143214). BITA does not claim to be first to show that trade-offs can favour functional specialization.

## H0/H1 and the previously established optimized comparison

Let two functions have optima theta_1, theta_2 on a shared trait, functional weights w_1,w_2>0, distance d=|theta_1-theta_2| and residual cross-talk lambda>=0. Set h=w_1*w_2/(w_1+w_2).

For one shared coordinate z the optimized compromise loss is:

    L = h*d^2.

A two-coordinate architecture optimized with quadratic residual cross-talk has

    s = h/(h+lambda)
    recoverable compromise loss R = s*L
    net optimized architectural margin Phi = R-K

for a **fixed** architecture cost K, as in existing BITA. This identifies when the phenotype with separate coordinates would be **globally fitter**, not whether small genetic/developmental steps can evolve it.

- H0-BALANCE: R<=K, so an extra coordinate does not improve optimized fitness after paying K.
- H1-DIFFERENTIATION: R>K, so a suitably formed differentiated phenotype could be favoured.
- Both can occur with L>0: the presence of a trade-off is not sufficient.

## New, expressly additional assumption: gradual separation with a startup burden

Define 0<=u<=1 as the fraction of the **raw function-optimum distance** assigned to independent coordinates; u=0 denotes one shared state, and x-y=u(theta_1-theta_2). Keep the functional weighted centre at the SCH optimum. The gain relative to the shared optimum **before development cost** is

    G(u) = d^2*[2*h*u - (h+lambda)*u^2].

Unlike the fixed K, now assume a continuous but steeply saturating developmental/activation cost:

    K(u) = K_cap*[1-exp(-u/tau)]

with tau>0 and K_cap>=0. This **cost shape is not derived from plant data**. The new invasion landscape is

    Phi(u) = G(u)-K(u)
    Phi(0)=0
    Phi'(0) = 2*h*d^2 - K_cap/tau.

Consequently the following two inequalities can coexist:

    max_{0<u<=1} Phi(u) > 0       (differentiated architecture globally favoured)
    Phi'(0) < 0                 (small uphill changes away from balance disfavoured).

An exact, **sufficient not necessary**, parameter window for both is

    2*h*d^2*tau < K_cap < s*h*d^2.

Why? The lower bound makes Phi'(0)<0; the upper bound makes Phi(s)>=R-K_cap>0 since K(s)<=K_cap. Its interval is nonempty when **tau < s/2**. Thus sufficiently front-loaded startup costs make an **evolutionary-access gap** possible even though the differentiated optimum is fitter.

This is a condition on an **assumed fitness landscape**, not a genetic invasion proof: mutation sizes, genotype-to-phenotype mapping, effective population size, drift, migration, and developmental feasibility remain unmeasured.

## A fixed synthetic contrast: three regimes from the same trade-off model

Choose w_1=w_2=1, lambda=0.5, K_cap=0.15, tau=0.05; vary only d. Here h=0.5, s=0.5.

| d | Best gain max Phi(u) | Phi'(0) | Theoretical regime |
|---:|---:|---:|---|
| 0.5 | 0 | -2.75 | shared/balanced globally best |
| 0.8 | +0.0100068 | -2.36 | globally better differentiated, locally trapped |
| 1.0 | +0.1000068 | -2.00 | globally better differentiated, locally trapped |
| 1.5 | +0.4125068 | -0.75 | globally better differentiated, locally trapped |
| 2.0 | +0.8500068 | +1.00 | direct small-step gain possible |

In the d=1 example, the first positive-fitness separation occurs at **u=0.176958854...**. From u=0 a deterministic, strictly uphill mutation-proposal walk capped at u-step 0.10 cannot move. With a permitted step up to 0.25 it jumps the valley and climbs to around u=0.5. This establishes a **mutation-step-sensitive accessibility signature under the declared uphill rule**, not a measured mutation effect or a prediction of actual fixation.

The sufficient lower global-gain distance bound for these parameters is sqrt(K_cap/(s*h))=**0.774596669...**; this is NOT the numerically identified exact transition. The small-step gradient flips at d=sqrt(K_cap/(2*h*tau))=**1.732050808...**.

## Decisive cost-shape negative control: the same endpoint cost is not enough

The fitness valley is **not a generic consequence** of adding a cost to trait differentiation. Replace the front-loaded saturating cost by a **linear** cost calibrated to be exactly the same at full separation:

    K_linear(u) = K_sat(1) * u
    Phi_linear(u) = [2*h*d^2-K_sat(1)]*u - (h+lambda)*d^2*u^2.

This is a **concave quadratic**, so if Phi_linear has any positive maximum at u>0, its derivative at zero must already be positive. It cannot have the global-gain/local-trap classification. Therefore the accessibility gap in the constructed example depends on **startup cost curvature (or another source of nonconvexity)**, not on the endpoint cost alone.

For the same dimensionless d=1 configuration, both cost models pay approximately **0.15 at u=1**:

- front-loaded saturating cost: local gradient **-2.00**, best gain **+0.100007**, first beneficial jump **u≈0.17696**;
- matched endpoint linear cost: local gradient **+0.850**, best gain **+0.180625**, optimum **u≈0.425**, and **no local trap**.

A negative control applied to all **540** declared grid cells confirms that the concave-linear-cost model has **zero** global-gain/local-trap cases. This is a test of the model's causal **assumption** about developmental cost distribution, not a claim that real organisms pay saturating rather than linear costs.

## Finite robustness grid — no natural-prevalence interpretation

Sweep these **540 wholly hypothetical parameter cells** (3 functional-weight pairs x 4 coupling values x 3 cost caps x 3 activation scales x 5 conflict distances):

- shared/global optimum: **205/540**;
- differentiated global advantage with local fitness trap: **175/540**;
- small-step invasion possible: **160/540**.

For **167** non-boundary cells satisfying the strict analytic sufficient-window margins by more than 1e-9 fitness units, the expected global-gain/local-trap classification was recovered **167/167**; none violated the condition. Six nominally strict comparisons lie within the declared machine-near-boundary tolerance and are **not** counted as verification. These are tests and illustrations of algebra and numerical implementation, **not 175 ecological systems, not a meta-analysis, and not evidence that one strategy occurs in 32% of nature**.

Reproduction:
    
    python -m scripts.analyze_evolutionary_accessibility
    pytest -q tests/test_evolutionary_accessibility.py

Code: \`trait_architecture/evolutionary_accessibility.py\`. Output: \`docs/BITA_EVOLUTIONARY_ACCESSIBILITY_READOUT_V1.json\` when the script is executed.

## What the real-world BITA evidence currently tests — and fails to test

### Partial ecological pattern recovered, but no threshold identified

1. **Peucedanum multivittatum**: the repository's source-extracted Kudo & Shibata (2025) five-population final-fruit selection gradients for perfect-flower production were **-0.035, -0.029, +0.034, +0.008, +0.026** along early-to-late phenological/predation contexts. Male versus perfect flowers are distinct *functional states*, with male pollen/display potential and different seed-predator exposure (see \`docs/BITA_PEUCEDANUM_SELECTION_ARCHITECTURE_V1.md\` and \`empirical/identification_design/PEUCEDANUM_OBSERVATIONAL_CRITICAL_BRACKET_V1.json\`). This demonstrates **observational context-dependent selection and partial floral differentiation**, but does NOT measure h, s, K, tau, mutational steps, a paired ancestral/shared architecture or true Phi.
2. **Pedicularis rex**: published exsertion trade-off (pollination versus seed predation) and protective cupulate-bract manipulation provide a prospective within-system x-by-y architecture assay. The registered y knockout and x manipulation have not supplied a measured shared-versus-differentiated fitness bridge or ancestral transition (see \`docs/BITA_PEDICULARIS_XY_DIMENSIONAL_RELEASE_EXPERIMENT_V1.md\`).
3. **Cichlid jaw and Dalechampia modules**: published module separation and redeployment are architecture-state and history examples, not fitted tests of the newly assumed K(u) or its accessibility trap (see \`docs/TRAIT_DIFFERENTIATION_EMPIRICAL_BRIDGES.md\`).

The existing 56 directional floral route records / 25 independent clusters explain ecological channel recurrence and identification limits after traits differ. They are **not** a dataset of evolutionary transitions from a single shared trait to two independent trait axes, and should **not** be counted as 25 replications of this hypothesis.

### 2026-10-19 source-verified real-world update — ecological allocation, not evolutionary origin

Original-source reanalysis is documented, with the fixed input hashes and complete inferential ceiling, in **`docs/BITA_REAL_PATTERN_RECOVERY_2026_10_19.md`** (Draft PR #361). Its two taxonomic data lanes must not be pooled as if they measured a common trade-off strength.

For *Peucedanum multivittatum*, the correct 2025 Hokkaido University source **10.14943/hu95572** provided **685 plant observations across five plots and four years**, plus **106 paternity-panel plants**. Male allocation tracks predation across 18 plot×years (`rho=0.7193`) but five-plot exact `rho=0.9, p_two-sided=0.0833`. Within the same plot×year, after total-display and height adjustment, more male allocation correlates with fewer predator eggs **and** fewer initial/final fruits, so the candidate conflict has an observable female-opportunity cost.

**Decisive alternative explanation:** replacing log(total floral display) with log(number of perfect flowers) as control on the *same 672 plants* reduces the male-allocation/egg coefficient from **−1.2127 to −0.2945**; post-open residual permutation `p=0.1448`, and five-geographic-plot t(4) sensitivity interval **[−1.0845,+0.4954]** includes zero. The available evidence therefore does **not** isolate active predator deterrence by male flowers beyond simply exposing fewer seed-bearing perfect flowers. Coefficient attenuation is not an identified mediated fraction.

A matched 532-plant initial/final fruit subset shows a predicted female production cost. Final/initial retention trends positive by **+0.01775** for a +0.10 male-fraction difference, but the five-plot interval `[−0.0695,+0.4244]` for the unscaled coefficient **includes zero**, as does the common-support `log1p(final)-log1p(initial)` coefficient interval. Female protection may be traded against initial opportunity, but a net seed-fitness benefit is not established. Male fitness equivalence was not demonstrated by the 106-plant paternity panel.

Separately, original jaw-shape data for **88 cichlid species** initially showed residual oral/pharyngeal covariance (RV5=0.1862, coarse-clade permutation p=0.0002), with morphology in both modules related to diet. This result has now passed a stricter **actual-tree phylogenetic independent-contrast** test: from a source-pinned tree of 1,712 tips, 88 matched fish species yield 87 evolutionary contrasts; five-axis PIC RV=**0.145319**, whole-contrast permutation p=**0.0024**. Under two explicitly post-open branch-length alternatives, RV=**0.138304** (p=0.0002) and **0.151200** (p=0.0012); three-axis original-tree RV=**0.138451** (p=0.0006). This supports **evolutionary morphological integration persisting across distinct anatomical modules**, not a measured genetic BITA coupling lambda, ecological trade-off strength, or an origin-of-modularity architecture-switch fitness threshold. The signal partly corroborates the original authors' earlier phylogenetic jaw-integration finding and is not an independent biological radiation.

**Verdict:** real-world **functional conflict and context-dependent allocation patterns are recovered**, but the empirical critical surface `Phi=R-K=0` and hypothesized activation-cost invasion barrier are still **NOT IDENTIFIED**. This is a substantive partial test, including an unresolved alternative mechanism, **not** confirmation that trade-offs caused evolutionary origination of new modules.

### Falsification plan, kept downstream of the theoretical test

At least two forms of data are needed: (1) a **paired common-fitness** shared-versus-differentiated architecture contrast to estimate the fitness margin, and (2) real **developmental/genetic accessibility information** capable of estimating \`K(u)\` and feasible change sizes. Additional genetic/phylogenetic comparisons are needed to infer historical transitions or among-lineage differentiation.

The local-trap mechanism is **falsified for a focal system** if arbitrarily small heritable shifts away from u=0 improve fitness in the relevant ecological context, or if costs are demonstrated to rise slowly enough that Phi'(0)>=0. The global differentiation premise fails when commensurable maximal fitness under two coordinates is no greater than the balanced state. Different mechanisms (frequency dependence, spatially varying selection, antagonistic pleiotropy) can yield diverged phenotypes without the proposed startup-cost mechanism.

## Interpretation / decision

**Mathematical hypothesis test: positive, conditional on stated assumptions.** Cost, decoupling and accessibility together partition BALANCE, GLOBALLY_FAVOURED_BUT_LOCALLY_TRAPPED and SMALL_STEP_ACCESSIBLE regimes.

**Biological/historical confirmation: NOT ACHIEVED.** The published observational states are compatible with functional differentiation, but do not identify the architecture gain, startup-cost shape, heritability or mutation steps. Do not present the numerically classified hypothetical regimes as evidence that real traits evolved for this reason.

**Scope:** this Chapter-2 BITA line is separate from the current *Ecology Letters* nectar-robbery Letter and should not overwrite its original analysis or release workflow.
