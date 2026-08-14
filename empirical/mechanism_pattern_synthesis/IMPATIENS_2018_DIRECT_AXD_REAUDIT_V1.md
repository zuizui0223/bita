# Impatiens capensis 2018: direct A x D observational re-audit

## Decision

The Soper Gorden & Adler (2018) individual-plant panel is promoted from a generic matched-study candidate to **Tier 1 observational direct-interaction evidence**, with strict qualifications.

It qualifies because the same individual-plant panel jointly measures:

```text
A = early-season flower redness
D = early-season floral condensed tannins
W component 1 = chasmogamous fruits per plant per day
W component 2 = seeds per chasmogamous fruit
```

and the predeclared archived models explicitly contain the `A_z:B_z` interaction term.

This is not a causal A x D manipulation, not total lifetime fitness, and not an estimate of `rho`, `iota`, `kappa`, or `c_AD`.

## Source and rerun provenance

```text
article DOI: 10.1002/ajb2.1182
data DOI:    10.5061/dryad.0j96d17
unit:        individual plant (Plot_Number)
historical branch: impatiens-empirical-core
workflow:    Run Impatiens empirical core
workflow run: 28713490690
head SHA:    8248fe396deb4ee3a0b19cd18d352dab5761427f
artifact:    impatiens-empirical-core
artifact ID: 8083707968
artifact SHA-256: d7d9316bfc3d2131d2cda07a8c6701a237421a4698b49bcbef740e71610edd53
workflow conclusion: success
```

The archived analysis script downloads the title-validated Dryad archive, reads raw/processed observations in memory, constructs the declared complete-case panels, and fits HC3 OLS models. The model configuration explicitly declares both fitness-component models as:

```text
outcome_z ~ A_z + D_z + A_z:D_z
          + Robbing + Florivory + Pollination + phenology
```

The supplemental interaction treatments are randomized; the floral redness and condensed-tannin traits are not. The A x D coefficient is therefore a treatment-adjusted observational interaction.

## D-role gate

The 2018 configuration originally called floral condensed tannins a `floral chemical barrier candidate`, which was appropriately conservative.

For the present mechanism-pattern synthesis, the D role is supported by linked primary evidence in the same species. Soper Gorden & Adler (2016; `10.1002/ecs2.1326`) reported that pre-treatment floral condensed tannins were negatively associated with nectar robbing, nectar thieving, and florivory and concluded that condensed tannins may provide broad-spectrum floral defence in `Impatiens capensis`.

The D-role basis is therefore:

```text
role status: linked same-species floral-defence evidence
causal status of D role: observational
not claimed: manipulated tannin defence efficacy
```

This is sufficient for a Tier-1 **observational** direct-interaction record under the current protocol, but it must remain distinguishable from a factorial A x D manipulation.

## Direct A x D results

### Chasmogamous fruits per plant per day

```text
n = 170
A x D standardized slope = -0.0820432714
HC3 SE                   =  0.0548258278
95% CI                   = [-0.1895018939, +0.0254153511]
p (normal approximation) =  0.1345404114
```

The point estimate is substitutability-compatible on this reproductive component, but the interval includes zero.

### Seeds per chasmogamous fruit

```text
n = 85
A x D standardized slope = +0.1040306830
HC3 SE                   =  0.1043468068
95% CI                   = [-0.1004890582, +0.3085504242]
p (normal approximation) =  0.3187788530
```

The point estimate is complementarity-compatible on this reproductive component, but the interval includes zero.

## Same-panel marginal routes

The same individual panel also estimates the four constituent marginal routes:

| Route | n | Standardized slope | HC3 SE | 95% CI |
|---|---:|---:|---:|---:|
| A -> pollinator use | 81 | +0.00794 | 0.12327 | [-0.23367, +0.24955] |
| D -> pollinator use | 81 | -0.18069 | 0.12399 | [-0.42371, +0.06232] |
| A -> natural florivory | 154 | -0.09484 | 0.06959 | [-0.23124, +0.04155] |
| D -> natural florivory | 154 | +0.08983 | 0.07442 | [-0.05605, +0.23570] |

All four intervals include zero. The value of this study is therefore not a strong marginal sign result; it is the joint measurement architecture on one field population.

## Interpretation

This source gives the synthesis its first direct observational A x D interaction estimates, but it does **not** establish one interaction sign.

The two reproductive components have opposite point estimates and both are imprecise. The correct classification is:

```text
Tier 1 direct interaction: yes, observational
interaction sign: unresolved
component consistency: no
causal trait interaction: not identified
total lifetime fitness: not measured
joint allocation cost c_AD: not identified
```

This is scientifically useful for the new framing: even within one shared individual-level system, the apparent attraction-defence interaction can depend on which reproductive component defines the outcome scale.
