# Integrated floral trait--animal interaction meta-analysis v1

## Central empirical question

The project asks whether attraction (`A_flower`) and defence/access restriction
(`B_flower`) have different directional effects on the two animal interaction
partners:

```text
pollinators
floral antagonists (florivores, nectar thieves, and other flower-using enemies)
```

The quantitative layer therefore starts from one **large integrated effect
database**, not from four isolated small meta-analyses.

## One master ledger

Every full-text effect is entered into a common ledger with these mandatory
axes:

```text
trait_role                 A_flower / B_flower
partner_role               pollinator / floral_antagonist
mechanism_class            chemical / physical_access / visual / temporal / reward / mixed / other
outcome_construct          use / preference / visitation / attack / damage / abundance / pollen transfer / reproduction / learning
study_design               direct experiment / choice assay / observational association / natural comparison
source_effect_metric       Fisher-z / r / Hedges-g / log odds / log response ratio / log rate ratio
dose and context           natural relation, alternative resources, consumer specialization
study/species identity     dependence structure
```

Mechanism, outcome, design, metric, and context are **moderators**. They are not
used to discard effects or create separate primary meta-analyses in advance.

## Effect orientation

Every numerical effect is oriented before modelling so that:

```text
positive value = a higher focal floral trait produces a higher measured response
                 by the focal animal consumer
```

This lets the primary `trait_role × partner_role` term compare the four
empirical cells directly:

| Trait role | Partner | Model-compatible direction |
|---|---|---|
| A | pollinator | positive |
| A | floral antagonist | often positive / context-dependent |
| B | pollinator | often negative / context-dependent |
| B | floral antagonist | often negative |

A result that differs from these directions is retained. It may identify a
mechanism or ecological context where the simplified theory is incomplete.

## Common-scale layer and native-metric layer

The common-scale analysis uses Fisher's z of the standardized directional
association between higher trait expression and consumer response. The ledger
records documented transformations from:

- reported Fisher-z;
- correlation r;
- Hedges' g;
- log odds ratio, using an explicitly labelled log-odds-to-SMD approximation.

Log response ratios and log rate ratios stay in the master ledger but are
initially retained in a native-metric lane. They are not discarded, and they
are not silently coerced into Fisher-z. A metric-aware measurement model or a
predeclared sensitivity analysis may use them later.

## Primary integrated model

```text
z_effect_i ~ trait_role_i * partner_role_i
           + mechanism_class_i
           + outcome_construct_i
           + study_design_i
           + dose_relation_i
           + consumer_specialization_i
           + alternative_resource_context_i
           + trait_role_i:partner_role_i:mechanism_class_i
           + (1 | independent_study_id)
           + (1 | species)
```

The primary term is `trait_role × partner_role`, not a separate B-to-P pooled
mean. This model asks whether A and B are functionally differentiated across
pollinators and antagonists while keeping mechanism and context visible.

## What this model can and cannot establish

### It can assess

- whether A and B have different broad associations with pollinators and
  floral antagonists;
- whether chemical, physical, visual, temporal, or reward mechanisms alter
  those associations;
- whether outcome layer, design, dose, consumer specialization, and alternative
  resources explain heterogeneity;
- whether the broad empirical pattern is consistent with functional separation
  needed for attraction--defence complementarity.

### It cannot establish alone

- the within-system causal `A × B` interaction;
- the shared-cost term `c_AD`;
- that a pathway difference automatically proves complementarity or substitution;
- a universal biological coefficient across traits, consumers, and contexts.

These require joint-system studies and remain connected, but separate,
evidence layers.

## Candidate map versus numerical effects

The fixed corpus currently contributes 1,318 candidate abstracts and 1,526
candidate-route rows. Those counts measure screening capacity only. They are
not included studies, independent effects, or numerical support for any model
coefficient.

The balance dashboard always reports candidate rows and full-text numerical
effects side by side, so high recall cannot be mistaken for a completed
meta-analysis.
