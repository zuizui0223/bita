# Direct attraction–defence joint-cost audit v1

## Question

The theory contains a direct joint-cost curvature term, `kappa`, separate from antagonist relief and pollinator interference. The empirical question is therefore narrow:

> Is there a source-verified study that directly measures an allocation, construction, physiological, or intrinsic fitness cost that depends jointly on a declared floral attraction axis `A` and a distinct flower-specific defence/access axis `D`?

Trait covariance, genetic linkage, pleiotropy, marginal A/D costs, agent-induced resource-reallocation inference, or failure to detect a negative correlation do not by themselves identify this term.

## Search status

The strict search is now complete under `JOINT_COST_SEARCH_PROTOCOL_V1.md`.

Five expansion batches screened all registered `JC01`–`JC03` families. Batches 4 and 5 both yielded:

```text
new strict joint-cost studies:          0
new eligible joint-cost design classes: 0
```

The preregistered stopping rule is therefore satisfied. See `JOINT_COST_SATURATION_RECEIPT_V1.md`.

**Gate F is passed as a documented evidence gap.** This is not a claim that `kappa=0`.

## Audited evidence classes

`JOINT_COST_AUDIT_V1.csv` now contains 13 high-information source decisions. The search repeatedly recovered several biologically real but inferentially different kinds of cost.

### 1. A–D covariance / integration

#### Theis et al. (2014), Cucurbitaceae

The paper explicitly tested an allocation-tradeoff prediction. Across varieties, neither leaf nor floral cucurbitacins correlated with any measured floral attractive or reward trait:

```text
|r| < 0.25
P > 0.05 for all comparisons
```

This is useful negative evidence against a simple phenotypic tradeoff, but it is **not** a direct cost measurement. Weak covariance can occur even when physiological costs exist, and strong covariance can arise from shared genetics or selection without an allocation cost.

#### Thosteman et al. (2024), Arabis alpina

A common-garden study quantified integration among floral scent, foliar volatiles and foliar glucosinolates and found little evidence that attraction and defensive chemical groups were strongly integrated. This suggests evolutionary independence of those chemical axes, not absence of a direct construction cost. The D axes are additionally foliar rather than flower-specific.

#### Wild radish joint signal/defence architecture

Petal-colour polymorphism is associated with aspects of glucosinolate architecture, but genetic linkage/pleiotropy and selection remain alternatives to resource limitation. No direct expenditure variable is measured.

### 2. Ecological cost of resistance

Strauss et al. (1999) experimentally selected high- and low-resistance Brassica lines. Resistance and herbivore damage changed floral traits and pollinator foraging.

This is a genuine ecological cost of resistance, but it does not measure an intrinsic resource term depending on simultaneous A and flower-specific D investment. Calling it `kappa` would confound direct construction cost with pollinator-interference / floral-phenotype pathways.

### 3. Agent-induced or evolutionary resource-reallocation inference

Ramos & Schiestl (2019) found that herbivory compromised the experimental evolution of attractive floral signals under bee pollination. The work is highly relevant to multiple-agent evolution, but the physiological allocation link among defence compounds, floral signals and rewards was not directly measured.

Likewise, herbivory-induced floral-signal studies and simulated-damage studies can show reduced reproductive/floral investment while leaving resource reallocation, hormonal cross-talk, tissue damage, phenology and adaptive plasticity as competing mechanisms.

These are mechanism hypotheses, not direct `kappa` measurements.

### 4. Marginal D cost or flower-specific D allocation

Defence-cost experiments in Brassica directly test the cost of investing in glucosinolates. Flower-specific studies in Nicotiana and Lomatia resolve the regulation or tissue localization of floral defensive compounds.

These studies demonstrate that D production and deployment can be biologically costly or tightly regulated. They still do not identify the **additional joint cost** of producing A and D simultaneously.

### 5. Nectar-secondary-metabolite allocation hypotheses

Manson and colleagues quantify flower-specific nectar defensive chemistry and its ecological consequences. Allocation, transport and production costs are discussed as potential explanations for observed concentrations, but are not directly measured together with an independent A investment.

This distinction is useful because it shows that even close nectar-chemistry systems generally identify `D_to_pollination` or `D_to_antagonism`, not the intrinsic joint cost.

### 6. Functional substitution / lower reward-cost hypothesis

Liu et al. (2007) show that nectar phenolics and sugar interact nonlinearly in bee responses and propose that phenolic-rich nectar may maintain pollinators with lower sugar expenditure.

This is a clever possible energy-saving mechanism, but the experiment measures visitor behaviour rather than the plant's actual resource expenditure. A reduced required reward is not a measured A+D joint construction cost.

### 7. Direct attractive/reward trait cost with a dual historical function

Dalechampia resin provides one of the closest conceptual near misses. Experimental reward manipulation shows that resin reward production can reduce seed production, so the attraction/reward trait has a direct reproductive cost. Resin also has an ancestral defensive function.

However, reward and defence are functions of the **same material**, not simultaneous investment in a distinct attraction axis and distinct D axis. This identifies an A marginal cost and an exaptation architecture, not `kappa`.

## Current strict evidence state

```text
source-audited high-information joint-cost candidates:   13
strict measured A+D allocation/construction cost:         0 verified studies
strict kappa effect estimates:                            0
simple A-D covariance/tradeoff panels:                     present
marginal A costs:                                          present
marginal D costs:                                          present
agent-induced resource-reallocation inference:            present
kappa identified:                                          no
kappa estimated as zero:                                   no
```

## Scientific result

The saturated search supports the bounded statement:

> The empirical literature readily provides marginal costs of attraction or defence, ecological interference, inferred resource reallocation, and tests of attraction–defence integration. In the registered search universe, we did not identify a study that directly accounts for an intrinsic additional cost of simultaneously producing a distinct floral attraction trait and a flower-specific defence/access trait.

This is an **empirical-identifiability gap**, not evidence that the biological cost is absent.

## Consequence for the integrated synthesis

`kappa` must remain empirically unidentified. The manuscript must not manufacture it from:

```text
A cost + D cost
negative A-D covariance
resistance effects on pollinators
herbivory-induced reduction in floral signals
single-material reward/defence systems
```

The canonical theoretical sensitivity analysis is therefore not a temporary substitute to be deleted. It is the correct way to show how the attraction–defence sign changes across plausible direct-cost values until experiments explicitly measure the missing quantity.

## Completion-gate decision

```text
Gate F direct joint-cost search: PASS
mode: documented saturated evidence gap
```

With Gates A and E also passed, the main empirical bottleneck now shifts to **Gate C: a second independent, genuinely quantitative multi-study mechanism module**, with the Sasidharan et al. 2023 deposited floral-volatile synthesis currently the highest-value candidate. Gate G robustness/bias then remains before manuscript reconstruction.