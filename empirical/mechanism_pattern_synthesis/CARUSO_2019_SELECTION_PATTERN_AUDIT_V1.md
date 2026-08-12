# Caruso et al. 2019 selection-level Pattern audit v1

## Source

Caruso CM, Eisen KE, Martin RA, Sletvold N. **A meta-analysis of the agents of selection on floral traits.** *Evolution* 73:4–14. DOI: `10.1111/evo.13639`.

Dryad dataset: `10.5061/dryad.2v8c5g0`.

The Dryad record contains the non-duplicated and analysis-duplicated experiment/study workbooks used in the published meta-analysis.

## Distinct Pattern question

This module does not ask whether antagonists reduce reward or visitation. It asks:

> How strongly do different environmental agents alter directional selection on floral traits, and does that change with floral trait class and pollinator guild?

That is a **selection-level context Pattern** downstream of the constituent ecological pathways.

## Published database architecture

The source reports:

```text
1,334 directional selection-gradient records from 55 articles in the broad database
755 records from 36 articles with directional gradients + standard errors used in the main meta-analytic analyses
35 species from 15 families
487 paired treatment contrasts ('studies') on the same trait and fitness component
```

The 755 main-analysis records are partitioned by floral trait category:

```text
flower-level attraction: 181
plant-level attraction:   265
pollination efficiency:   170
flowering phenology:      139
```

The paired environmental-manipulation studies include:

```text
supplemental hand pollination: 255
reduced pollination:           116
other biotic factors:           59
abiotic factors:                57
```

The 'other biotic' category can include herbivory, density of conspecifics, or heterospecific presence. It is therefore not a pure antagonist module.

## Published meta-analytic Pattern

The primary source reports:

1. supplemental-pollination effects on selection were stronger than effects of other biotic manipulations;
2. pollinator-mediated selection was similar in strength to abiotic-factor-mediated selection after multivariate control;
3. pollinator-mediated selection was stronger on pollination-efficiency traits than on attraction or phenology traits;
4. pollinator-mediated selection varied strongly among pollinator guilds;
5. the database had substantial taxonomic/design imbalance, including Orchidaceae overrepresentation and relatively few other-biotic/abiotic manipulations.

The analysis therefore independently supports **trait-class and interaction-partner dependence of the selection surface**.

## Theory-facing mapping

Admitted mapping:

```text
selection on floral traits is agent-dependent
selection magnitude is trait-class-dependent
selection magnitude is pollinator-guild-dependent
biotic context can change trait-fitness relationships
```

This is compatible with the paper's claim that a single context-free attraction–defence relation should not be expected across ecological states.

However, this module is one inferential layer farther from the focal local decomposition than the Leal, Sasidharan, or Haas-Desmarais modules.

## What it does NOT identify

```text
directional selection gradient beta != W_AD
change in beta between treatments != rho/iota/kappa
'other biotic' != antagonist pressure H in every study
pollination efficiency trait != attraction A by definition
floral attraction category != direct A x D design
```

It must never be used to claim that pollinators or antagonists estimate the focal mixed partial.

## Independence / overlap considerations

This database likely contains some primary studies that also appear in the 258-work discovery corpus or in the source-adjudicated route ledgers. Therefore:

- the module is independent as a **published quantitative synthesis framework**;
- its article/study counts must not be added to route-ledger cluster counts as new independent biological replication without DOI/study-level overlap auditing.

## Current adjudication

```text
source identity:               PASS
public deposited dataset:      PASS
quantitative meta-analysis:    PASS
selection-context axis:        DISTINCT
focal A x D identification:    NO
route-ledger independence:     NEEDS OVERLAP AUDIT
full local reanalysis:         NOT YET RUN
```

### Decision

**ADMIT_AS_SECONDARY_SELECTION_CONTEXT_CANDIDATE**

This is valuable because it tests a distinct Pattern level — whether environmental agents and pollinator guilds alter floral trait selection — but it should remain secondary until overlap with the current study ledgers is quantified and the Dryad data are reconstructed locally.

## Manuscript-ready conservative claim if promoted

> A separate meta-analysis of experimentally manipulated agents of selection compiled 755 directional selection-gradient records with uncertainty from 36 articles and found that the strength of selection on floral traits varied with the manipulated agent, floral trait class, and pollinator guild. This selection-level pattern is consistent with context-dependent floral fitness surfaces, but it does not identify the attraction–defence mixed partial or its component mechanisms.
