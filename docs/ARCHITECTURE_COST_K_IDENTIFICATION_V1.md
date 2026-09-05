# Architecture cost K identification v1

## Purpose

The common SCH–BITA critical surface is

```text
Phi = s L_S* - K = 0.
```

The remaining conceptual danger is to treat every measured cost in a two-trait system as the same `K`. They are not.

This document separates three quantities.

## 1. Local joint-channel cost is not K

The existing BITA mechanism-identification framework may estimate a local two-trait joint channel such as `kappa_delta` from an independent `A x D` cost/allocation assay.

That quantity asks:

> once the two trait coordinates already exist, does expressing them jointly create an interaction-specific cost or benefit relative to their local factorial expectations?

It is a local channel allocation quantity.

Therefore:

```text
kappa_delta
!= architecture cost K.
```

A local joint curvature can be zero while maintaining the second module remains costly, or nonzero while the long-run architecture itself has negligible fixed maintenance cost.

## 2. Functional-state deployment cost

Some BITA experiments manipulate an already existing second functional state, for example water retained versus drained in a pre-existing floral structure.

An independently measured additional cost of turning on or using that state may be called

```text
K_state.
```

If `K_state` is measured on the same reproductive-fitness scale as the SCH conflict budget, the projection

```text
s L_S,component* - K_state
```

defines a **contemporary functional-state criticality**.

This is useful experimentally, but it does not establish that evolving or maintaining the structure itself is worthwhile.

Important: if `best W(y1)-best W(y0)` already uses a total common fitness endpoint that includes deployment costs, do not subtract `K_state` again. In that design the net state comparison has already absorbed those costs.

## 3. Structural architecture maintenance cost

The theoretical `K` in the Chapter-2 architecture model is stronger. It denotes the additional cost attributable to the differentiated architecture itself relative to the shared architecture, beyond the trait-mismatch/coupling terms already represented in the model.

Call an empirical version

```text
K_arch.
```

Possible components include:

- developmental construction and maintenance;
- constitutive energetic/resource burden;
- regulatory/coordination burden;
- pleiotropic or opportunity costs that remain after the focal functions are standardized;
- survival/reproduction costs of possessing the additional architecture even when focal functional benefits are experimentally held fixed.

A valid `K_arch` estimate needs a comparator in which the additional axis is absent, reduced, or independently varied while the focal functional performance and common fitness scale are made commensurable.

A manipulation that merely disables the function of an extant structure normally identifies `K_state`, not `K_arch`.

## 4. Architecture-level C2 gate

Only when all terms are compatible may the paper evaluate

```text
Phi_arch
 = s L_S,component* - K_arch.
```

Required:

```text
SCH conflict receipt
fitness_scale_id identical to BITA cost scale
+ decoupling s for the same context
+ independent K_arch estimate
+ no double counting of costs already inside L_S or coupling.
```

The sign is:

```text
Phi_arch < 0  shared architecture favoured
Phi_arch = 0  architecture critical surface
Phi_arch > 0  differentiated architecture favoured.
```

## 5. State-level C2 gate

For an experimentally toggled second functional state, a parallel operational quantity is

```text
Phi_state
 = s L_S,component* - K_state.
```

or, if the observed total-fitness comparison already includes all state costs,

```text
Phi_state,net
 = best W_differentiated_state - best W_shared_like_state.
```

The net form should be preferred when valid because it avoids reconstructing costs by subtraction.

A positive `Phi_state` or `Phi_state,net` supports contemporary functional-state release, not evolutionary origin of an architecture.

## 6. Relation to within_bita_optimum_fitness_gain

The registered dimensional-release analyzer returns

```text
within_bita_optimum_fitness_gain
 = best W(x|y1) - best W(x|y0).
```

This is a net difference between two states inside an extant BITA system. It may contain benefits and costs of deploying `y`.

Therefore:

```text
within_bita_optimum_fitness_gain
!= K_arch
!= kappa_delta.
```

It can directly establish a state-level net fitness advantage if the two y states are a defensible shared-like versus differentiated comparison, but it cannot by itself estimate the fixed evolutionary architecture cost.

## 7. Current empirical status

```text
local joint-channel / kappa machinery:        IMPLEMENTED
functional-state net fitness comparison:      IMPLEMENTED
SCH fitness-scale conflict budget estimator:  IMPLEMENTED IN SCH
K_state independent cost lane:                DESIGN-DEPENDENT / NOT GENERALLY IDENTIFIED
K_arch structural maintenance cost:           NOT YET IDENTIFIED
architecture-level numeric C2 in nature:      NOT YET IDENTIFIED.
```

The absence of `K_arch` is now a specific measurement gap, not an undefined residual.

## 8. Fail-closed projection

Use:

```text
scripts/project_sch_conflict_budget_into_bita.py
```

with an SCH `SCH_COMPONENT_CONFLICT_BUDGET_V1` receipt and
`BITA_CRITICAL_SURFACE_COST_CONFIG_TEMPLATE_V1.json`.

The projection refuses:

- mismatched fitness scales;
- `kappa`-labelled sources masquerading as `K`;
- undefined cost semantics;
- decoupling outside `[0,1]`.

It reports functional-state versus structural-architecture claim levels separately and propagates declared intervals conservatively.
