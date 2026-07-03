# Part B: layered evidence strategy v2 (trial, diagnose, pivot)

## Why this revision exists

Part B was initially framed as four separate marginal meta-analyses supporting the
Part A interaction theorem. That remains a useful **data-collection scaffold**, but
it cannot be the required final result: the current records differ in trait class,
outcome layer, design, and effect metric, and separate marginal arrows do not
identify an `A × D` interaction.

This version keeps all usable evidence while preventing an artificial grand mean.
The analysis proceeds in layers and changes its primary claim when the capacity
diagnostic shows that a numerical synthesis is not defensible.

## Evidence roles

| Layer | Input requirement | Result that may be stated | Result that may not be stated |
|---|---|---|---|
| I. Direct interaction | Same study manipulates/measures A and D jointly and reports an `A × D` effect on pollen transfer, fruit/seed output, or another reproductive response. | Direct empirical test of complementarity/substitutability in that system. | General theorem proof from one system. |
| II. Quantitative route effect | Compatible trait × outcome × metric × design stratum; recoverable estimate and uncertainty. | Individual estimates; cautious stratum-specific summary when capacity permits. | A common four-arrow effect or theoretical derivative estimate. |
| III. Directional route evidence | Direct route and oriented sign are source-adjudicated, but a compatible numerical effect is unavailable. | Directional support / contradiction map. | Effect magnitude or formal pooled estimate. |
| IV. Candidate / access-limited evidence | Candidate is unassessed, excluded, or has insufficient source access. | Evidence-gap and retrieval map. | Support for any pathway direction. |

All included records remain visible in one of these roles. A record never moves to a
stronger role without the required source information.

## Quantitative capacity labels

The capacity diagnostic uses the pre-registered stratum thresholds but gives them
narrow meanings.

```text
k = 0   no quantitative effect
k = 1   individual quantitative estimate
k = 2   multiple estimates, but no heterogeneity assessment
k >= 3 and below stability threshold
        exploratory synthesis candidate only
k >= stability threshold
        stable synthesis candidate, subject to biological comparability and bias review
```

The `k >= 3` label is not a claim that a meta-analysis is complete, reliable, or
representative. It only permits a clearly labelled exploratory summary if the
studies answer the same narrow question.

## Trial sequence

1. Run the C0 evidence-capacity audit on all committed records.
2. Extract numerical effects only from the fixed high-value reading queues; retain
   the source locator, denominator, uncertainty, and natural-dose context.
3. Add direct-interaction candidates only after an explicit factorial `A × D`
   screen; do not infer these records from four marginal arrows.
4. Re-run C0 after each small, source-audited batch.
5. Let the resulting capacity, not a target number of papers, determine the
   primary empirical output.

## Pivot rules

The project pivots from a meta-analysis-centred Part B to an evidence-map-centred
Part B when any of the following holds after the registered queues and targeted
source screens are exhausted:

```text
- no compatibility stratum reaches exploratory quantitative capacity;
- apparent clusters require mixing trait classes, response layers, designs, or
  effect metrics to become poolable;
- most route evidence remains directional-only because uncertainty, denominators,
  or treatment contrasts cannot be recovered;
- no direct factorial A × D study is verified.
```

Under a pivot, the paper's empirical contribution is:

```text
1. a reproducible evidence map across the four marginal pathways;
2. an inventory of individual numerical effects, without a false common mean;
3. directional support where numerical standardisation is unavailable;
4. a direct-interaction evidence gap that specifies the needed future experiment.
```

This is not a fallback of lesser quality. It is the correct claim level when the
published record is structurally fragmented.

## Current expectation

The current committed inputs contain five verified numerical anchors, each alone in
its exact compatibility stratum, plus thirteen primary directional records. C0 is
therefore expected to recommend a multilayer evidence map with an individual-effect
inventory, not a four-arrow pooled meta-analysis. That expectation is a property of
the current registry and is re-tested automatically whenever records are added.

## Boundary to Part A

Part A remains the exact theorem:

\[
\frac{\partial^2 W}{\partial A\partial D}
= H d_A e_F
- P b_A c_D e^{-c_DD}(1-c_RR)
- c_{AD}.
\]

Layered Part B evidence informs whether the theorem's marginal mechanisms occur in
nature and where evidence is absent. It does not estimate the mixed partial,
identify `c_AD`, or turn a set of unrelated marginal studies into a joint-panel
interaction test.
