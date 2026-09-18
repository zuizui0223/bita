# Defence-side conditionality readout v1

## Purpose

This layer preserves the earlier BITA sign/state-switch work and reuses only the defence-side clusters that are relevant to the floral-defence selectivity refocus.

Source-of-record:

`empirical/mechanism_pattern_synthesis/SIGN_SWITCH_LEDGER_V1.csv`

New filtered registry:

`empirical/floral_defence_selectivity/d_side_conditionality_registry.csv`

No legacy row is deleted or rewritten.

## Corpus

The original sign-switch ledger contains 11 independent study clusters.

Eight are defence-side:

```text
D-side conditionality clusters: 8

primary macro axes:
dose / expression:              2
exposure / reward context:     2
consumer identity:             1
response stage:                2
temporal expression:           1
```

These are independent publication/study clusters. Multiple doses, response endpoints, or time points within one study are retained as dependent contrasts rather than independent replications.

## Ecological result

The defence effect is not a fixed property of a chemical or physical trait.

Across the retained D-side systems, realised state changes with:

1. **dose or trait expression** — `Polemonium` and `Asclepias syriaca`;
2. **exposure or reward context** — colony exposure in `Asclepias`, reward compensation in `Gelsemium`;
3. **consumer identity / response threshold** — `Aconitum`;
4. **response stage or construct** — `Nicotiana` pollinator arrival versus handling/consumption and `Gelsemium` robber arrival versus within-plant exploitation;
5. **temporal expression** — the defensive BA effect in `Nicotiana` tracks the early-night emission window.

Thus the same nominal D axis can occupy guarded, interfering, compensated, stage-specific, or temporarily inactive states.

## Ordered exposure subset

Four independent systems provide an especially interpretable ordered exposure/intensity pattern:

- `Polemonium`: moderate 2PE -> no detected pollination cost; high 2PE -> pollinator interference;
- `Asclepias` colony exposure: single bout -> no detected avoidance; multi-day exposure -> deterrence;
- `Asclepias syriaca`: natural-range dose -> null/non-monotonic; strongly elevated dose -> negative consumption response;
- `Aconitum`: antagonist consumption is suppressed at tens of ppm, whereas pronounced pollinator interference occurs at substantially higher concentrations.

These systems support a threshold-window interpretation:

```text
antagonist response threshold
<
pollinator interference threshold
```

in some systems, with the guarded window closing as exposure increases.

The outcome metrics differ and are not pooled into one synthetic effect size.

## Relation to the cross-system matched-D result

The two evidence layers answer complementary questions.

```text
matched-D corpus:
    across systems, does effective-domain architecture predict
    antagonist suppression with or without pollinator cost?

D-side conditionality:
    within systems, which ecological axes move the same D
    between guarded and interfering states?
```

The second result therefore explains why a static chemical-versus-physical classification is insufficient.

## Claim ceiling

Supported:

> Defence selectivity is state-dependent across multiple independent systems, with recurrence of dose/expression, exposure/reward, consumer, response-stage, and temporal controls.

Not yet supported:

- one universal numerical threshold ratio;
- a pooled cross-outcome moderator coefficient;
- natural prevalence of each state;
- a claim that all eight systems represent the same mechanism quantitatively.

## Main-paper role

This result should become a main Results subsection after the matched-D cross-system result, not a methods warning or supplementary footnote.

It is inherited from previous BITA work but reinterpreted as a substantive ecological result:

> **selectivity is dynamic, and the dimensions that open or close the selective window recur across independent floral systems.**
