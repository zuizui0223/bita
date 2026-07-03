# Part B stopping-rule amendments v1

This is the line-level bridge between the existing (proof-route) stopping rules
and the Part B mechanism-level support route defined in
`PART_B_MECHANISM_META_STRATEGY_v1.md`. It changes **only sourcing and counting**.
The mathematics (Part A), the scale/design separation, and the honesty
prohibitions are all retained. Each amendment names the rule it supersedes and
the rule it keeps.

## A1 — count independence marginally, not at the joint panel

**Supersedes:**
- `BROAD_META_ANALYSIS_PROTOCOL.md` §"Primary product 1 — direction map":
  `< 3 evaluable independent clusters -> insufficient_directional_clusters`
- `EVIDENCE_ATLAS_v0.md` §"Stop role-specific synthesis before pooling":
  "at least two independent study clusters" per role × scale × causal-status.

**Change.** The `k >= 3` (direction) and `k >= 2/3/5` (pooling) thresholds are
evaluated **within a single arrow** (`b_A`, `d_A`, `e_F`, or `c_D`), across studies
that estimate that one arrow. Independence is judged per arrow, per scale, per
design class — not by whether the same study also measured the other three arrows.

**Retained.** "Multiple papers using the same field panel are one cluster." A
shared panel is still one cluster within an arrow.

## A2 — widen the sourcing population beyond the fixed co-mention corpus

**Supersedes:**
- `FIXED_CORPUS_CAPACITY_V1.md` Fixed decision 1: "Freeze L1/L2 discovery."
- `BROAD_META_ANALYSIS_PROTOCOL.md` prohibition:
  "Do not expand L1/L2 discovery in order to manufacture a poolable k."

**Change.** Each arrow may draw from its **own mature marginal literature**,
including the primary studies included in existing published meta-analyses for
that arrow. The fixed co-mention corpus (harvest #40, 17,933 records) remains
frozen **as the joint-panel discovery set**; it is no longer the sole population
for the four marginal arrows.

**Guardrail (why this is not "manufacturing k").** The original prohibition
targeted widening the *co-mention* corpus to force a *joint* poolable stratum.
Part B pools *marginal* effects from literatures that are independently mature, so
`k` is discovered, not manufactured. Every added study must independently pass the
per-arrow eligibility contract (trait role, outcome denominator, effect scale,
design class, uncertainty). Query membership is never an effect.

## A3 — restrict the co-location requirement to the joint-panel route

**Supersedes:**
- `theory_empirical_identifiability_reassessment.md` and
  `part_i_to_big_data_decision_table.md`: the "same plant/site/time unit"
  requirement, where currently applied program-wide.

**Change.** "Same plant / same site / same period / recoverable linked table" is a
requirement for the **joint-panel proof route only** (`M2`→`D1`→`D2`→`D3`). Part B
marginal arrows (`B1`/`B2`/`B3`) do **not** require the four arrows to share a unit,
because they never claim to identify the mixed partial. A `d_A` study and a `c_D`
study on different systems are two marginal contributions, not one joint panel.

**Retained.** No Part B output may be presented as a joint-panel `D1`/`D2`
identification. Two arrows on different units are never combined into a panel.

## A4 — add the conditionality and break-even outputs

**Extends** `BROAD_META_ANALYSIS_PROTOCOL.md` §"Deferred layer" (which permitted
only within-stratum pooling).

**Addition.**
- **B3 moderator layer.** Pre-declared moderators (`pollination generalization`,
  `display conspicuousness`, `access restriction`, `florivore pressure H`,
  `pollinator service P`) may be fitted within an arrow's effect-size envelope to
  test whether the arrow strength shifts in the theorem-predicted direction. This
  is the Part B headline.
- **B4 break-even bound.** Report the threshold `τ = H d_A e_F − P b_A c_D
  e^{−c_D D}(1−c_R R)` at which the predicted sign flips, as a function of the B2
  envelopes. `c_AD` is bounded, never estimated.

**Retained.** `c_AD` and `c_R·R` stay declared sensitivity axes
(`broad_evidence_to_regime_interface.md` parameter table is unchanged).

## A5 — unchanged prohibitions (explicitly carried forward)

All of the following remain in force verbatim from
`BROAD_META_ANALYSIS_PROTOCOL.md` §"Explicit prohibitions" and the atlas stopping
rules:

```text
- Do not pool signs as effect sizes.
- Do not pool different trait classes, effect scales, or design classes.
- Do not pool visitation, pollen transfer, fruit set, and seed set together.
- Do not invert a contrary effect to force agreement with the model.
- Do not call any Part B output a direct D1/D2 test.
- Do not use leaf/stem defence as a floral-barrier arrow without a declared bridge.
- Do not treat query membership or abstract co-mention as a measured effect.
```

## Net effect on the four-path status

Under A1–A3, the current inventory is re-counted per arrow rather than per joint
panel. The five verified Impatiens/Gymnadenia effects
(`four_path_effect_registry.csv`) remain valid single-cluster anchors, but they are
now the **seed** of four marginal literatures rather than the entire poolable
universe. The pending Gorden & Adler (2016) screen and the five `L4` exact-stratum
anchors keep their priority, and additionally each becomes a first cluster in its
arrow's B2 envelope.
