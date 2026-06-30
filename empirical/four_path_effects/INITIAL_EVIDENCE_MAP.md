# Initial four-path evidence map

## Scope and reading rule

This map summarizes the effect registry after the first independently extracted
*Gymnadenia odoratissima* record. It is an **evidence-coverage map**, not a
meta-analysis and not a test of the Part I mixed partial.

Effects stay separated by role, reported scale, and causal status. A positive
or negative coefficient in this table is a direction on the study's declared
outcome scale, not evidence for adaptive selection or a universal interaction
regime.

## Current registry coverage

| Part I path | Registered studies | Reported scale strata | Current evidence state |
|---|---:|---|---|
| `A_to_pollination` | 1 | standardized regression slope: 1 | one observational *Impatiens* record |
| `A_to_antagonism` | 2 | standardized regression slope: 1; log odds ratio: 1 | two observational records, but different traits, outcomes, and scales |
| `B_to_antagonism` | 1 | standardized regression slope: 1 | one observational *Impatiens* record |
| `B_to_pollination` | 1 | standardized regression slope: 1 | one observational *Impatiens* record |

All five registered effects are observational. There is no manipulated effect
record, no independently calibrated shared A×B allocation cost, and no D2/D3
fitness-surface panel.

## Registered effect map

| Effect role | Study context | Trait candidate | Outcome | Estimate on reported scale | Registry status |
|---|---|---|---|---|---|
| `A_to_pollination` | *Impatiens capensis*, individual field panel | floral-lip redness | reproductive-organ-contact visits per hour | standardized slope +0.008; 95% CI −0.234 to +0.250 | observational; scale-specific synthesis input |
| `A_to_antagonism` | *Impatiens capensis*, individual field panel | floral-lip redness | average natural floral tissue loss | standardized slope −0.095; 95% CI −0.231 to +0.042 | observational; scale-specific synthesis input |
| `A_to_antagonism` | *Gymnadenia odoratissima*, 13 population-year individual panel | total floral scent amount | eaten flowers / total flowers | log odds ratio +0.568; 95% CI +0.042 to +1.094 | observational; `scale_specific_only` |
| `B_to_antagonism` | *Impatiens capensis*, individual field panel | floral condensed tannins | average natural floral tissue loss | standardized slope +0.090; 95% CI −0.056 to +0.236 | observational; scale-specific synthesis input |
| `B_to_pollination` | *Impatiens capensis*, individual field panel | floral condensed tannins | reproductive-organ-contact visits per hour | standardized slope −0.181; 95% CI −0.424 to +0.062 | observational; scale-specific synthesis input |

## What can be concluded now

1. The registry is no longer a single-study, four-arrow structure: it has a
   second, independently extracted `A_to_antagonism` observation from a different
   plant system and floral trait class.
2. The two `A_to_antagonism` records cannot be pooled: they use different trait
   candidates, antagonist outcomes, and effect scales. Their different estimated
   directions are therefore not a replicated contradiction or a regime result.
3. There is no role × scale × causal-status stratum with at least two compatible
   independent studies. A pooled mean, parameter envelope, or general direction
   is not yet identified.
4. The current evidence is compatible with the project premise that floral
   attraction-antagonist links can be context- and trait-specific. It is not
   evidence for a universal positive or negative attraction–antagonism relation.

## Concrete evidence gaps

```text
highest gap:   manipulated floral B → floral-antagonism effects
next gap:      individual-level floral A → pollination effects in new systems
then:          replicated compatible-scale observational effects for every path
still absent:  independently measured floral B plus all four paths in one panel
still absent:  shared A×B allocation/cost evidence
```

The next literature work should therefore stop expanding broad M0 discovery and
prioritize sources that can fill one of these sparse role × scale strata with a
recoverable effect estimate and denominator.

## Interpretation boundary

This document does not convert visitor rates, tissue-loss percentages, and
binomial florivory odds into a common metric. It also does not use observational
records as causal model parameters. The proper next output is a role-specific
synthesis only after at least two compatible independent effects exist within a
role × scale × causal-status stratum.
