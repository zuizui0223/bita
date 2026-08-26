# Identification coverage readout v1

## Scope

This readout asks a different question from the existing Mechanism → Pattern ledger:

> Given the new discrete identification design, which quantities can existing studies actually recover?

It is an **anchor audit**, not a literature-frequency estimate. Four deliberately high-information systems were chosen because they fail at different identification gates.

## Required estimands

The target design distinguishes:

```text
Delta_AD W_full              directly observed total interaction
rho_delta                    A-dependent antagonist relief
iota_increment_delta         A-dependent pollinator-mediated increment loss
m0_delta                     A×D interaction in pollinator-absent mutualist/reproductive baseline
iota_total_delta             iota_increment_delta - m0_delta
U_delta                      rho_delta - iota_total_delta - Delta_AD W_full
kappa_assay_delta            independent A×D cost-curvature assay
```

`U_delta` is not automatically relabelled as `kappa_delta`.

## Anchor 1 — Soper Gorden & Adler 2018, Impatiens capensis

Repository provenance: `IMPATIENS_2018_DIRECT_AXD_REAUDIT_V1.md`.

The Dryad-backed rerun is the strongest current total-interaction anchor because the same individual-plant panel jointly measures:

```text
A = early-season flower redness
D = early-season floral condensed tannins
```

and fits `A_z:D_z` on two reproductive components.

Current reproduced results:

```text
CH fruits per plant per day
n = 170
A×D slope = -0.0820
HC3 95% CI = [-0.1895, +0.0254]

seeds per CH fruit
n = 85
A×D slope = +0.1040
HC3 95% CI = [-0.1005, +0.3086]
```

Thus even the total interaction is sign-unresolved and outcome-component dependent. More importantly for the new framework, these are observational trait interactions, not a two-level causal A×D manipulation, and the study lacks crossed selective antagonist/pollinator interventions.

Recoverable now:

```text
treatment-adjusted observational total A×D terms
same-panel marginal consumer routes
```

Not recoverable:

```text
rho_delta
iota_increment_delta
m0_delta
iota_total_delta
independent kappa_delta
```

This study therefore demonstrates the distinction between **estimating a total interaction** and **identifying its causal channels**.

## Anchor 2 — Kessler et al. 2015, Nicotiana attenuata

Repository provenance: `DIRECT_AXD_AUDIT_V1.csv` and `DIRECT_AXD_SEARCH_EXPANSION_READOUT_V1.md`.

RNAi independently silences benzylacetone scent and nectar production, including the double-silenced cross, so the study contains a genuine 2×2 floral-phenotype architecture. It is nevertheless not a strict A×D identification design because the second axis is a pollinator reward restriction rather than an independently justified antagonist-reducing defence axis.

The source compares four lines with Friedman/pairwise procedures rather than reporting an uncertainty-bearing scent×nectar factorial interaction. The current public-supplement audit recovered figure-image supplements but no raw Figure-2 outcome table.

Recoverable now:

```text
four experimental phenotype cells
same-system pollinator-mediated seed-production and Manduca-oviposition directions
```

Identification stops because:

```text
D orientation fails
no crossed selective consumer toggles
no m0_delta estimate
no independent joint-cost assay
```

This is a **factorial phenotype near miss**: a 2×2 experiment alone is not enough if the axes do not map to the causal estimands.

## Anchor 3 — Kessler et al. 2008, Nicotiana attenuata

Repository provenance: `DIRECT_AXD_NEAR_STRICT_MATRIX_V2.csv`.

This system is closer to the intended biological roles: floral benzylacetone provides an attraction axis and nectar nicotine is an antagonist-relevant repellent axis. The existing audit records a 2×2 transgenic phenotype structure and a rounded discrete interaction signal, but the nicotine intervention is systemic/organ-scope sensitive and the source audit did not establish an uncertainty-bearing A×D estimate.

It is retained as a **near-direct D-scope case**, not promoted to identified rho/iota/kappa.

## Anchor 4 — Sun & Huang 2015, Pedicularis rex

Repository provenance: `PEDICULARIS_REX_2015_BARRIER_AUDIT_V1.md`.

This experiment manipulates a flower-associated physical defence mechanism:

```text
D = water-holding cupulate bract state
manipulation = drain retained water
```

Published responses in the same system show:

```text
legitimate pollinator visitation: no detected treatment effect (P = 0.958)
nectar-robber visitation:         no detected treatment effect (P = 0.951)
seed predation:                   strong treatment effect (P < 0.0001)
```

The system has no independent attraction manipulation, so it does not estimate `rho_delta`. Its value for the new framework is different: it shows a plausible **system-selection architecture** in which a physical barrier has a strong effect on one antagonist mode without a detected pollinator response.

That makes it a candidate template for building selective interventions by body size, attack route, or behavioural access rather than using nonselective bags or broad insecticides.

## Cross-anchor result

The four anchors expose four distinct failure modes:

```text
1. total A×D can be estimated observationally, but channels are not identified;
2. a 2×2 floral factorial exists, but the second axis is not D;
3. a near-direct A/D phenotype exists, but D scope and uncertainty remain unresolved;
4. a selective D mechanism exists, but there is no A manipulation.
```

None of the four currently identifies the full sequence

```text
Delta_AD W_full + rho_delta + iota_total_delta + independent kappa_delta.
```

That absence is not yet a prevalence claim for the literature. It is a concrete demonstration that the new design asks for information that the closest existing studies provide only in pieces.

## Immediate empirical implication

The next study should not merely add another A×D regression. It should deliberately combine:

1. an experimentally manipulable A axis;
2. an experimentally manipulable flower-specific D axis;
3. selective G and P interventions crossed with A×D;
4. a measurement or justified zero for `m0_delta`;
5. a separate A×D allocation/construction-cost assay.

The theory then functions as an identification and sign-diagnostic framework rather than as a standalone prediction theorem.
