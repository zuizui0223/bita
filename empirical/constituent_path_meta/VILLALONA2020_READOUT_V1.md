# Villalona et al. 2020: source-complete pathway audit

## Status

The primary article and its publisher supplement are now source-complete for the reported cardenolide-consumption trials. The study contributes strong directional and context evidence, but no canonical cross-study effect is created because the source does not report the group means and dependence information required for a compatible standardized effect.

## Recovered source

The Springer supplementary Word file for doi `10.1007/s00442-020-04701-0` was recovered through GitHub Actions and rendered to seven pages. The relevant material is:

- Table S3: common-milkweed nectar cardenolide concentrations;
- Table S4: species-specific treatment, time, and treatment-by-time tests for three consumption-choice trials;
- Table S5: species-specific survival comparisons.

The receipt, checksum, and exact workflow/artifact identifiers are stored in `VILLALONA2020_SOURCE_RECEIPT_V1.json`.

## Biological role gate

The study uses ouabain as a milkweed-relevant cardenolide treatment. Milkweed cardenolides are established chemical defences, and the linked same-system Jones and Agrawal study measures both antagonist and pollinator responses to nectar cardenolides. The study therefore passes the existing linked B-role gate. This does not mean that every experimental dose is ecologically realistic.

## Dose and species result

The source yields a sharper result than a generic negative `B -> pollinator use` arrow.

```text
measured common-milkweed nectar        approximately 0.5-1.5 ng/uL
field-realistic range used in argument up to 100 ng/uL
supra-natural treatment                1000 ng/uL
```

Across the three bee species:

- Within 0-100 ng/uL, `B. griseocollis` and `B. bimaculatus` showed no treatment difference.
- Within 0-100 ng/uL, `B. impatiens` consumed more at 25 than at 100 ng/uL, with the 25-vs-control contrast also tending positive.
- At 1000 ng/uL, `B. griseocollis` showed near-complete avoidance and `B. impatiens` reduced consumption.
- `B. bimaculatus` did not show a treatment effect in the four-dose trial.
- At the highest dose, illness, mortality, and time-dependent consumption changes complicate interpretation as a simple preference response.

Thus, the same defence-linked compound class produces null, positive, and negative pollinator-use responses depending on dose and pollinator species. The strongest negative effects occur at the treatment that also causes illness and lies far above the concentration measured in common-milkweed nectar.

## Why no effect row is promoted

Table S4 reports omnibus F tests and Tukey groups, but not the treatment means, standard errors, or within-individual covariance needed to convert repeated consumption measurements into a common Hedges-g or log-response-ratio effect. Deriving a binary effect from the omnibus F statistic would collapse species, time, or repeated-measure structure and would not be comparable with the existing outcome-specific effects.

The correct current state is therefore:

```text
source-complete directional study       yes
strict linked B-role gate                yes
independent study cluster                one
outcome lane                             volume consumed / choice
canonical quantitative effect            no
reason                                   means and dependence unavailable
```

## Implication for the fixed theory

This source strengthens the conditional rather than universal interpretation already fixed in the project. Defence-linked floral chemistry can reduce pollinator use, but the cost is not a stable property of the compound label. It can be absent or reversed at lower concentrations and differs among legitimate pollinator species.

The study does not estimate `iota`, `rho`, `kappa`, or `W_AD`, and it is not counted as multiple replications because it contains several species, trials, doses, and time points.

## Manuscript decision

The manuscript remains frozen. This readout is an empirical checkpoint only.
