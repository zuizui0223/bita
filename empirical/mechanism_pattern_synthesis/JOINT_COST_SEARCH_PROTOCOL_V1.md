# Direct joint-cost (`kappa`) search protocol v1

## Purpose

This protocol defines what empirical evidence may inform the theory's direct joint-cost term and, equally importantly, what may not.

After the orientation gate, the theory contains

```text
W_AD = rho - iota - kappa
```

where `kappa` is the direct curvature/cost associated with joint investment in the declared floral attraction axis `A` and the distinct flower-specific defence/access axis `D`.

The joint-cost search is therefore **not** a generic search for papers using the word `trade-off` or `cost of defence`.

## Strict eligible design

A study is strict joint-cost evidence only if all of the following are satisfied:

```text
1. a declared floral attraction/signal/reward axis A is measured or manipulated;
2. a distinct, independently justified flower-specific defence/access axis D is measured or manipulated;
3. A and D are linked on the same biological units or experimental allocation budget;
4. the study measures a direct resource, energetic, biosynthetic, construction, allocation, opportunity-cost, or fitness-cost quantity that can distinguish joint A+D investment from separate marginal costs;
5. the cost is not mediated solely through pollinator/antagonist behaviour;
6. the inference is not based only on negative trait covariance;
7. the evidence does not require re-labelling a pollinator reward reduction as defence from the response being tested.
```

Examples of potentially eligible evidence would include:

- experimental manipulation of a fixed carbon/nitrogen/energy budget allocated jointly to floral display/reward and flower defence with direct resource or fitness accounting;
- biochemical flux or construction-cost measurements showing an additional cost of producing both a floral attractant and a flower-specific defensive compound/structure;
- factorial A×D trait manipulation where ecological visitors are controlled/excluded and the interaction itself reduces plant performance through intrinsic construction/allocation costs.

None of these examples is assumed to exist.

## Explicit exclusion classes

### Defence cost alone

A demonstrated energetic or fitness cost of glucosinolate, alkaloid, latex, trichome or other defence production is a `D` marginal cost, not `kappa`, unless joint A+D expenditure is measured.

### Attraction/reward cost alone

A demonstrated seed/energy cost of nectar, petals, floral scent or other attractive structure is an `A` marginal cost, not `kappa`.

### Ecological pollinator interference

If highly defended flowers receive poorer pollinator service because of chemistry, morphology or rewards, the evidence belongs to the pollinator-interference channel. It is not direct construction/allocation cost simply because the paper calls it a cost of resistance.

### Agent-induced trade-off inference

Herbivory or defence induction that reduces floral scent/display may be compatible with resource reallocation, hormonal cross-talk, damage, phenology or adaptive plasticity. Without direct allocation accounting it is not `kappa`.

### Negative A–D covariance or phenotypic integration

A negative correlation between attraction and defence may arise from allocation, pleiotropy, linkage, selection, environmental covariance or measurement architecture. Covariance alone does not identify a direct resource cost.

Conversely, weak/no integration does not prove `kappa=0`.

### Cross-organ cost

Foliar/whole-plant defence costs that reduce flower number, petal size or reproduction are biologically valuable context but do not satisfy the active strict flower-specific D definition.

### Functional substitution / energy-saving inference

A defensive nectar compound that permits lower sugar reward while maintaining pollinator use may suggest reduced attraction cost, but a behavioural assay does not directly measure plant resource savings or joint A+D cost unless plant expenditure is quantified.

## Registered query families

Use the fixed `JC01`–`JC03` queries from `SEARCH_REGISTRY_V1.csv` as the backbone and expand them with source-specific synonyms only to improve recall:

```text
JC01  floral attraction defence allocation cost
JC02  flower signal resistance tradeoff allocation
JC03  floral display chemical defence covariance resource cost
```

Expansion synonyms may include:

```text
construction cost
energetic cost
carbon allocation
nitrogen allocation
biosynthetic cost
metabolic flux
resource budget
opportunity cost
cost of nectar / scent / petals
cost of floral defence
physiological trade-off
```

The inclusion definition must not change in response to low yield.

## Search-batch stopping rule

The strict joint-cost search stops when **two consecutive expansion batches**, each screening all three registered JC families with non-identical recall expansions, yield:

```text
zero new strict eligible joint-cost study
and
zero new eligible joint-cost design class
```

A new paper that merely instantiates an already adjudicated exclusion class does not reset the stopping rule.

A new design class resets the count even if the study ultimately fails strict eligibility, because it may expose a previously unexamined way of identifying direct cost.

## Evidence-gap rule

If the stopping rule is met with zero strict eligible studies, Gate F may pass as a **documented empirical evidence gap**.

The manuscript may then state only that the registered search did not identify direct A+D construction/allocation evidence. It may not state that `kappa=0`, that direct joint costs do not exist, or that separate marginal costs can be added to estimate `kappa`.

## Search outputs

Each expansion batch records:

```text
query family
primary examples screened
strict eligible count
new design class count
exclusion class
source basis
decision
```

The final saturation receipt must preserve:

- strict eligible count;
- recurring exclusion/design classes;
- distinction between intrinsic allocation cost and ecological pollinator interference;
- the bounded claim supported by a zero-yield search, if applicable.
