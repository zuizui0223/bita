# Kessler et al. 2019 defensive-scent quantitative reconstruction protocol v1

## Fixed source

```text
article DOI: 10.1111/1365-2435.13332
dataset DOI: 10.17617/3.24
file: FIGURE 1. Diabrotica presence 2011. 2014. 2016.xlsx
plant: Nicotiana attenuata
antagonist: Diabrotica undecimpunctata
D axis: floral benzyl acetone (BA) emission
EV: BA-emitting empty-vector control
CHAL: BA-silenced line
```

This protocol is fixed before reading non-header observation values from the deposited Figure 1 workbook.

## Biological estimand

The study experimentally removes a flower-specific volatile that has a source-established defensive function against the floral antagonist. The estimand is therefore a `D_to_antagonism` effect:

> How strongly does the presence of floral BA reduce the probability that a plant is colonized by *D. undecimpunctata*?

BA is also a pollinator-attracting floral signal in this species. It remains a **dual-function single trait**, not two artificial A and D axes and not a direct `A x D` record.

## Eligible observations

Use only the three deposited worksheets `2011`, `2014`, and `2016` in the fixed Figure 1 file.

For each sheet retain one row per plant when all are available:

```text
line/genotype: EV or CHAL
plant identifier, when supplied
presence: 0 or 1
```

`number of beetles` is retained only as an audit field and is not the primary response.

Rules:

1. no imputation;
2. no exclusion based on observed outcome;
3. reject rather than silently recode any non-empty genotype label other than EV/CHAL;
4. require presence to be exactly 0 or 1;
5. where plant identifiers exist, require no duplicate plant identifier within genotype and year;
6. each field season remains a dependent effect inside one study cluster.

## Primary reconstruction

For each year form the exact 2 x 2 table:

```text
                 infested    not infested
EV (BA present)     a             b
CHAL (BA absent)    c             d
```

Report:

- exact counts and sample sizes by genotype;
- infestation proportions;
- the source-native two-sided Fisher exact P value;
- odds ratio `OR = (a*d)/(b*c)` when all cells are non-zero;
- log odds ratio and Wald SE `sqrt(1/a + 1/b + 1/c + 1/d)` when all cells are non-zero.

If any cell is zero, use a 0.5 Haldane-Anscombe correction **for the log-OR/SE only**, label that effect `continuity_corrected`, and keep the Fisher exact test on the uncorrected table.

Effect orientation is fixed as:

```text
logOR(EV versus CHAL infestation)
negative = BA emission is defence-compatible (lower infestation)
positive = BA emission is antagonist-facilitation-compatible
```

## Across-year study summary

Do not treat the three years as three independent literature studies.

A single descriptive within-study summary may be produced by inverse-variance weighting the year-specific log odds ratios. This summary is labelled `within_study_fixed_season_summary`, not a three-study meta-analysis. A leave-one-year-out summary is also reported because 2016 may contain a zero cell.

The source-reported year-specific results remain primary for source fidelity; the combined estimate exists only to create one study-cluster effect for later route-level synthesis.

## Secondary checks

- reproduce the source direction for 2011, 2014, and 2016;
- compare reconstructed Fisher P values with the reported values (`0.035`, `0.013`, `0.098`) as a data/source integrity check;
- audit whether the number-of-beetles column is consistent with the binary presence field, without fitting it as an alternative outcome.

## Prohibited uses

This reconstruction must not be called:

- a direct `A x D` interaction;
- an estimate of `rho`, `W_AD`, or `kappa`;
- three independent study replications;
- a causal effect of BA on total lifetime fitness;
- evidence that all attractive scents are defensive.

Only aggregate counts, coefficients, uncertainty, and diagnostics may be written to the repository or workflow artifacts. Observation-level records remain in memory.