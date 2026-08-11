# Mechanism-pattern coverage audit v1

## Boundary

This is an audit of the currently committed **source-adjudicated ledger**, not an estimate of mechanism prevalence in nature or a replacement for route-specific meta-analysis.

The audit was generated successfully by `.github/workflows/build-mechanism-coverage-audit.yml` from the fixed ledger universe through `LEDGER_BATCH_5_V1.csv`.

```text
source-adjudicated effect/directional records: 38
independent biological study clusters:          14
same-system multi-route clusters:                10
registered context/sign-switch records:          11
sign-switch study clusters:                      11
```

## Route coverage

| Route | independent clusters | quantitative clusters | clean primary quantitative | quality-flagged clusters |
|---|---:|---:|---:|---:|
| `A_to_pollination` | 4 | 2 | 2 | 0 |
| `A_to_antagonism` | 5 | 3 | 3 | 0 |
| `D_to_antagonism` | 10 | 3 | 1 | 3 |
| `D_to_pollination` | 7 | 3 | 2 | 1 |
| `direct_AxD` | 1 | 1 | 1 | 0 |

`quantitative` means at least one finite effect plus finite SE exists inside the cluster. `clean primary quantitative` additionally requires `is_primary_effect=true` and no explicit discrepancy/unresolved/pending/blocked/sensitivity flag.

These counts deliberately do not treat different outcomes, doses, years, consumer taxa or plant species within one experiment as independent studies.

## A_to_pollination

Source-adjudicated clusters:

```text
Gorden_Adler_2018_Impatiens_capensis
Kessler_et_al_2015_Nicotiana
Theis_Adler_2012_Cucurbita
Theis_et_al_2014_Cucurbitaceae
```

Quantitative clusters:

```text
Gorden_Adler_2018_Impatiens_capensis
Theis_et_al_2014_Cucurbitaceae
```

The route is empirically covered but intentionally not forced into a common metric because direct visitation, pollinator-mediated seed output and comparative visitation coefficients are not interchangeable outcomes.

## A_to_antagonism

Source-adjudicated clusters:

```text
Gorden_Adler_2018_Impatiens_capensis
Gross_Sun_Schiestl_2016_Gymnadenia_odoratissima
Kessler_et_al_2015_Nicotiana
Theis_Adler_2012_Cucurbita
Theis_et_al_2014_Cucurbitaceae
```

Quantitative clusters:

```text
Gorden_Adler_2018_Impatiens_capensis
Gross_Sun_Schiestl_2016_Gymnadenia_odoratissima
Theis_et_al_2014_Cucurbitaceae
```

This route has now moved beyond the original single `Gymnadenia` anchor. It includes multiple independent floral-signal systems and both positive attraction-tracking and unresolved/opposite-direction cases.

## D_to_antagonism

Ten independent clusters are source-adjudicated:

```text
Adler_Irwin_2005_Gelsemium
Barlow_et_al_2017_Aconitum
Galen_2011_Polemonium
Gorden_Adler_2018_Impatiens_capensis
Gronquist_2001_Hypericum
Irwin_Adler_Brody_2004_Ipomopsis
Jones_Agrawal_2016_Asclepias
Kessler_Baldwin_2007_Nicotiana
Kessler_Bing_Haverkamp_Baldwin_2019_Nicotiana
Takeda_Kadokawa_Kawakita_2021
```

Three currently contain numerical estimates with uncertainty, but only `Barlow_et_al_2017_Aconitum` is presently counted as a clean primary quantitative cluster by the strict automated rule. `Impatiens` is unresolved, and the Kessler-2019 BA reconstruction is held behind the explicit 2014 source/deposit discrepancy.

The larger directional base is nevertheless important because it spans chemical, physical-access and dual-function scent mechanisms rather than one compound family.

## D_to_pollination

Seven independent clusters are source-adjudicated:

```text
Adler_Irwin_2005_Gelsemium
Barlow_et_al_2017_Aconitum
Galen_2011_Polemonium
Gorden_Adler_2018_Impatiens_capensis
Irwin_Adler_Brody_2004_Ipomopsis
Jones_Agrawal_2016_Asclepias
Kessler_Baldwin_2007_Nicotiana
```

Three have numerical effects with uncertainty. The route is especially important for conditionality because dose, reward compensation, exposure duration, consumer identity and response construct repeatedly alter the observed state.

## direct A x D

Strict direct joint-trait evidence remains the narrowest layer:

```text
eligible independent clusters: 1
cluster: Gorden_Adler_2018_Impatiens_capensis
interaction outcomes: CH fruits per day; seeds per CH fruit
```

Both interaction confidence intervals overlap zero and their point estimates have opposite signs across reproductive components. This is therefore direct but unresolved evidence, not a general positive/negative interaction result.

The dedicated direct-A×D candidate audit has expanded well beyond this one accepted cluster, but joint measurement, dual-function single traits, agent factorials, whole-plant defence axes and unlinked datasets are not upgraded to Tier 1 merely because they resemble the desired design.

## Same-system mechanism architecture

Ten clusters contain at least two marginal routes in the same biological system:

```text
Adler_Irwin_2005_Gelsemium              D->H, D->P
Barlow_et_al_2017_Aconitum              D->H, D->P
Galen_2011_Polemonium                   D->H, D->P
Gorden_Adler_2018_Impatiens             A->H, A->P, D->H, D->P
Irwin_Adler_Brody_2004_Ipomopsis        D->H, D->P
Jones_Agrawal_2016_Asclepias            D->H, D->P
Kessler_Baldwin_2007_Nicotiana          D->H, D->P
Kessler_et_al_2015_Nicotiana            A->H, A->P
Theis_Adler_2012_Cucurbita              A->H, A->P
Theis_et_al_2014_Cucurbitaceae          A->H, A->P
```

This is already enough empirical material to make same-system co-occurrence a central synthesis layer rather than relying exclusively on unrelated marginal studies.

## Context / sign-switch architecture

The registered sign-switch ledger contains 11 independent study clusters, currently spanning 11 distinct contrast axes:

```text
compound identity
consumer role x dose threshold
decision stage / outcome construct
dose naturalness
exposure duration
outcome construct
outcome scale
pollinator identity
reward context
time of night x trait expression
trait-expression level / dose
```

This breadth supports the new manuscript framing: conditionality is not confined to one idiosyncratic chemical system. Different kinds of ecological context repeatedly alter which mechanism channel is expressed.

The next step is not to average these contexts together. It is to collapse them into a smaller theory-facing moderator ontology and test only moderator classes with enough independent clusters.

## Completion-gate implications

### Gate B — all four marginal mechanisms

**Empirical coverage is satisfied at the source-adjudicated level.** All four marginal routes have explicit evidence states.

This is not equivalent to having four pooled meta-analyses.

### Gate C — at least two quantitative mechanism modules

**Not yet passed under the strict definition.** The ledger now contains multiple quantitative clusters, but compatible multi-study effects are still needed for a second true synthesis module. PR #124 remains one independent antagonist-pressure meta-analysis module.

A raw cluster count is not substituted for a quantitative synthesis.

### Gate D — sign-switch analysis

**Substantially advanced, not yet complete.** Eleven independent conditionality records are registered. The remaining task is to define a compact moderator ontology and perform formal within-compatible-lane tests where sample size permits.

### Gate E — same-system multi-route

**Evidence base is now substantial.** Ten source-adjudicated clusters satisfy the same-system rule. A formal study-level guarded-attraction / pollinator-interference classification is still required before calling the gate complete.

### Gates A, F and G

Still open:

- Gate A: direct A×D search saturation;
- Gate F: strict direct A+D joint-cost/allocation search saturation;
- Gate G: module-level independence, influence, heterogeneity and bias/robustness audits.

## Claim boundary

No count in this readout is a prevalence estimate. No marginal route is multiplied or combined into `W_AD`. Same-system multi-route evidence remains distinct from direct `A x D`, and quantitative sensitivity records with source discrepancies remain visibly flagged rather than silently promoted.