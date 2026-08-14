# Mechanism-pattern universality synthesis protocol v1

## Purpose

This protocol reframes the empirical half of `bita` around the mechanism structure already fixed by the theory. It does not add a new trait, parameter, theorem, or biological mechanism.

The empirical question is no longer whether one constituent route, especially `B_to_pollination`, has a universal mean sign. The primary question is:

> Across empirical floral systems, how repeatedly do the constituent mechanisms and context-dependent sign switches predicted by the attraction-defence theory occur, and which ecological conditions explain transitions between complementarity-compatible and substitutability-compatible patterns?

The theory remains the fixed local diagnostic

```text
W_AD = rho - iota - kappa
```

where `rho` is antagonist-relief curvature, `iota` is mutualist-interference curvature, and `kappa` is direct joint-cost curvature after the orientation gate has been established.

## Core empirical hypothesis

Floral attraction and flower-specific defence/access restriction do not have a universal relationship. Their relationship is conditional because the same phenotype can simultaneously affect mutualists, antagonists, and direct costs.

The empirical synthesis therefore tests the recurrence of the following mechanism patterns rather than forcing all studies into one grand mean:

1. attraction increases pollinator use or pollination (`A_to_pollination`);
2. attraction can also increase antagonist exposure or damage (`A_to_antagonism`);
3. defence/access restriction reduces antagonist access, abundance, or damage (`D_to_antagonism`);
4. the same defence/access restriction can reduce legitimate pollinator use (`D_to_pollination`);
5. the sign and magnitude of routes 1-4 can switch with dose, reward context, consumer identity, specialization, environmental pressure, and response construct;
6. direct joint `A x D` studies, when available, provide the strongest evidence about local complementarity or substitutability;
7. direct joint-cost evidence is treated as a distinct evidence gap and is not inferred from separate marginal routes.

## Meaning of universality

Universality is not defined as one pooled biological coefficient shared by all floral traits, taxa, consumers, and outcomes.

The primary universality targets are instead:

```text
mechanism recurrence
    = how often a theoretically required route is empirically observed

sign consistency
    = how consistently the oriented route sign agrees across comparable studies

sign-switch recurrence
    = whether the same route changes sign across declared ecological contexts

mechanism co-occurrence
    = whether multiple theoretically linked routes occur in the same biological system

direct interaction recurrence
    = the distribution of positive, negative, or unresolved A x D interactions in eligible joint studies

evidence gaps
    = theoretically decisive channels for which matched empirical evidence is sparse or absent
```

A general empirical conclusion may therefore be that the mechanism architecture is widely recurrent even when no route has a universal sign.

## Evidence hierarchy

Evidence is ranked by inferential proximity to the theoretical mixed partial.

### Tier 1: direct joint interaction evidence

Eligible studies jointly manipulate or measure one declared attraction trait `A` and one declared antagonist-reducing defence/access trait `D`, and report an `A x D` effect on a declared reproductive, pollination, antagonist, or other biologically justified outcome.

These studies may directly inform complementarity or substitutability in that system. They do not establish a universal interaction sign.

### Tier 2: same-system multi-route evidence

The same biological system measures at least two of the four marginal routes involving the same focal trait(s), consumers, or experimental panel.

These records are especially valuable for identifying trade-offs, guarded-attraction structure, consumer filtering, and route coupling.

### Tier 3: compatible single-route quantitative evidence

A study provides a numerical effect and uncertainty for one direct route within a biologically and statistically compatible stratum.

Meta-analysis is performed only within declared compatibility strata. Outcome constructs and effect metrics remain separated unless a justified measurement model is preregistered.

### Tier 4: source-adjudicated directional evidence

The direction of a direct route is recoverable from full text or a traceable primary result, but a compatible numerical effect cannot be extracted.

### Tier 5: candidate or access-limited evidence

Search candidates, abstract-only records, and inaccessible studies are retained for retrieval accounting but do not support a route direction or magnitude.

## Primary synthesis units

The master empirical ledger must preserve at least:

```text
study_id
independence_cluster
plant_taxon
trait_role                  A / D
trait_class                 visual / scent / display / reward / chemical / physical_access / other
partner_role                pollinator / floral_antagonist
route                       A_to_pollination / A_to_antagonism / D_to_antagonism / D_to_pollination / direct_AxD
outcome_construct           visitation / preference / pollen_transfer / damage / abundance / reproduction / other
study_design                manipulation / choice_assay / observational / comparative
source_effect_metric
oriented_effect
standard_error
context variables           dose, naturalness, reward, consumer identity, specialization, alternative resources, P/H proxies
source_locator
source_verification_state
```

`D` replaces historical `B` in prose only when referring to the fixed theoretical trait. Existing repository tables using `B` remain valid historical schemas and need not be rewritten solely for terminology.

## Quantitative synthesis rules

1. No cross-outcome grand mean is a primary result.
2. No cross-metric grand mean is a primary result without an explicit measurement model.
3. Multiple doses, taxa, years, and outcomes from one biological panel are dependent effects, not independent studies.
4. Natural and supra-natural doses are retained separately when reported.
5. Preference, visitation, residence/consumption, pollen transfer, damage, and reproduction remain distinct response constructs.
6. Random-effects or multilevel synthesis is allowed only after biological comparability and independence are documented.
7. Directional synthesis and evidence mapping remain legitimate outputs when numerical pooling is not defensible.
8. Direct `A x D` interaction studies are synthesized separately from marginal-route studies.

## Moderator priorities

Moderators are theory-motivated rather than convenience variables. Priority order is:

1. dose or trait-expression range, especially natural versus supra-natural;
2. reward context and alternative-resource quality;
3. pollinator or antagonist identity and specialization;
4. physical versus chemical versus signal mechanism;
5. experimental versus observational design;
6. pollinator-service and antagonist-pressure context when directly measured;
7. mating/reproductive-assurance context when directly relevant to the outcome.

Moderator nulls are interpreted against available power and are not treated as evidence of invariance.

## Theory-to-evidence mapping

The synthesis does not estimate `rho`, `iota`, `kappa`, or `W_AD` by combining unrelated marginal studies.

Instead it asks whether the biological routes required for those terms recur in nature and whether their conditionality matches the theory's central prediction that complementarity and substitutability arise from relative channel strength.

The following statements remain prohibited unless directly identified by study design:

```text
four marginal arrows prove a direct A x D mixed partial
publication counts calibrate model parameters
a route-level pooled effect estimates W_AD
finite-grid occupancy estimates prevalence in nature
separate A and D literatures establish a joint cost
```

## Existing evidence modules to retain

The new synthesis should preserve, not discard, the existing analyses:

- the canonical local theory and finite sensitivity analysis on `main`;
- the antagonist-pressure / nectar-larceny synthesis from PR #124 as a Tier 3/4 environmental-gate module;
- the source-audited `D_to_pollination` work from PR #125, including its dose- and reward-dependent sign changes;
- the broad Crossref retrieval corpus and source-coding infrastructure as the discovery layer.

These modules answer different levels of the evidence hierarchy and should not be forced into one common effect estimate.

## Primary manuscript claim under this protocol

The intended integrated paper is not a claim that the theory has been empirically proven.

The target claim is:

> A local mechanistic theory predicts that attraction-defence relationships switch between complementarity and substitutability according to the balance among antagonist relief, pollinator interference, and direct joint costs. A systematic empirical synthesis tests how broadly the constituent mechanisms, their co-occurrence, and their context-dependent sign switches recur across floral systems, while explicitly identifying the evidence needed to estimate the direct interaction.

## Freeze rule

Do not rewrite the canonical manuscript around this protocol until the completion gate in `empirical/mechanism_pattern_synthesis/COMPLETION_GATE_V1.md` is satisfied.
