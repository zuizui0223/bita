# Ecological stabilization–evolutionary transience test v1

Status: **FROZEN BEFORE NEW OUTCOME ANALYSIS**

Frozen on: 2026-10-07
Branch: `analysis/ecological-stability-evolutionary-transience-v1`

## Scientific question

Can the same bypass behaviour that increases short-term ecological access and can
stabilize a mutualistic community nevertheless be an evolutionarily transient lineage
state?

The motivating cross-scale tension is explicit in the prior literature:

- Duchenne et al. (2023, PLOS Biology, doi:10.1371/journal.pbio.3002434) showed that
  innovative cheating can increase plant–pollinator community persistence under a
  restricted parameter region, but their model contains no evolutionary dynamics and
  explicitly leaves the evolutionary stability of those ecological equilibria open.
- Colwell et al. (2023, American Naturalist, doi:10.1086/726036) documented 66 known
  clinging hummingbird species among 220 measured species, inferred more than twenty
  independent origins of clinging, and noted qualitatively that many inferred origins
  are near tips and may indicate limited persistence/diversification. They did not
  perform a state-dependent diversification test.
- McGuire et al. (2014, Current Biology, doi:10.1016/j.cub.2014.03.016) provide the
  time-calibrated hummingbird phylogenetic framework.
- Aubert et al. (2026, Oikos, doi:10.1002/oik.11552) show that bird–flower access
  mismatch predicts nectar robbery in the Ecuadorian network analysed elsewhere in
  BITA.

The target is therefore **not** to rediscover that clinging/robbery evolved repeatedly,
that clingers have shorter bills/longer hallux claws, or that mismatch predicts
robbery. Those results are prior knowledge.

## Hypothesis

### H1 — ecological stabilization–evolutionary transience

A bypass-capable feeding state can expand ecological access while having lower
macroevolutionary persistence than orthodox legitimate feeding.

The non-obvious prediction is a cross-scale sign reversal:

```text
short ecological timescale:
innovative bypass -> access to otherwise unavailable resources
                   -> community persistence can increase

macroevolutionary timescale:
bypass-capable lineage state -> reduced lineage persistence/diversification
                              -> repeated gains concentrated near tips
```

This is not a claim that cheating is universally destabilizing. The hypothesis is that
ecological persistence of a community and evolutionary persistence of the behavioural
state are different response variables and can move in opposite directions.

## Primary state definition

The primary behavioural state follows Colwell et al. rather than being recoded after
seeing results:

- state 1 = **clinger**: any of the four feeding styles in Colwell et al. that require
  clinging while feeding;
- state 0 = **presumed non-clinger / orthodox** under the source classification.

Species that only use pierces while on the wing are not promoted to state 1 in the
primary analysis because the proposed mechanism concerns the clinging state used in
the published phylogenetic reconstruction.

A secondary analysis may use a broader **bypass-capable** state that includes
on-wing piercing, but it cannot replace the primary state.

## Data sources

1. Colwell et al. Harvard Dataverse
   doi:10.7910/DVN/THDJCI
   - Supplemental Spreadsheet S1 supplies the frozen feeding-style classification.
2. Colwell/Rangel Zenodo
   doi:10.5281/zenodo.7489569
   - `PGLS_Inputs.zip` contains 3000 plausible phylogenies and the morphology inputs
     used by the source study.
3. McGuire et al. Dryad
   doi:10.6078/D1C135
   - molecular alignment / time-calibrated phylogenetic source.
4. EPHI / Aubert public interaction data
   Zenodo 10.5281/zenodo.14185547 / Dryad 10.5061/dryad.rn8pk0pqx
   - used only for an ecological mechanism bridge, not for the macroevolutionary
     state-persistence statistic.

## Outcome hierarchy

### Primary outcome: lineage persistence, not raw tip prevalence

Estimate whether clinger state is associated with lower lineage persistence using
phylogeny-aware, state-conditioned branch information.

The primary implementation must use the source tree ensemble rather than one hand-picked
tree. For every usable tree:

1. prune to species with frozen state labels;
2. reconstruct state histories under a two-state continuous-time Markov model;
3. estimate state-specific total occupied branch time and the distribution of
   continuous dwell lengths for state 0 and state 1;
4. calculate
   `R_persist = median_dwell_state1 / median_dwell_state0`.

Primary prediction:

```text
R_persist < 1
```

The reported estimate is the median across tree/history replicates with a 95% interval
across the full phylogenetic/history ensemble.

### Secondary outcome A: diversification proxy

Use a tip-level diversification proxy computed from time-calibrated branch lengths
(equal-splits / inverse terminal-path measure) and compare state 1 versus state 0
with a phylogenetically structured null that preserves the observed number of state-1
tips and transition tendency.

Prediction:

```text
diversification_proxy(state1) < diversification_proxy(state0)
```

This outcome is secondary because trait-dependent diversification inference is
sensitive to model misspecification.

### Secondary outcome B: repeated-origin descendant depth

For independently reconstructed state-1 origins, record descendant crown depth and
number of extant state-1 descendants before a return to state 0.

Prediction:

```text
state1 origins are disproportionately shallow / small
relative to histories simulated under the fitted transition process
without state-dependent lineage persistence.
```

The published qualitative statement that many clinging origins lie near tips is
**not** treated as a blind discovery. This analysis asks whether the pattern exceeds
the fitted transition-process expectation.

## Negative controls / safeguards

- Repeat across the phylogenetic ensemble; do not select the tree that maximizes the effect.
- Repeat after excluding the Coquette clade, because it contains the clearest deep
  clinging origin.
- Repeat with the 12 phylogenetically uncertain taxa excluded.
- Do not infer extinction from tip prevalence alone.
- Do not use BiSSE as the sole inferential engine.
- If state-history uncertainty makes dwell-time ratios non-identifiable, report that
  failure instead of substituting a simpler post-hoc endpoint.
- The ecological-stability result from Duchenne et al. is prior literature, not a
  result generated by this test.

## Ecological bridge (separate from macroevolutionary primary test)

Using EPHI interaction-level records and Colwell feeding-style labels, ask whether
documented clingers/bypass-capable hummingbirds retain use of flowers beyond the
legitimate bill–tube matching domain more strongly than orthodox species.

This bridge is supportive only. Niche expansion via innovative cheating is already
known from Duchenne et al. (2023), so a positive bridge cannot serve as the novelty claim.

## Decision rule

Promote the cross-scale hypothesis only if:

1. the primary lineage-persistence statistic is directionally below 1 across the
   phylogenetic ensemble;
2. the conclusion survives exclusion of Coquettes and phylogenetically uncertain taxa;
3. at least one independent secondary macroevolutionary diagnostic agrees in direction.

If these conditions fail, retain the result as a falsification and do not rewrite the
existing Ecology Letters Letter around this hypothesis.

## Novelty boundary frozen before analysis

Allowed claim if supported:

> A behavioural bypass that can stabilize ecological communities may be
> macroevolutionarily transient; repeated innovation can therefore coexist with low
> evolutionary persistence.

Prohibited claims:

- first evidence that nectar robbing exists;
- first evidence that mismatch promotes robbery;
- first evidence that clinging evolved repeatedly;
- first demonstration that clingers have shorter bills or longer claws;
- universal claim that cheating lowers diversification;
- causal claim that robbery itself causes lower diversification without an
  independent causal design.
