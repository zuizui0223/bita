# d_A moderator coding protocol v1 (resolve the sign conflict)

## Why this exists

B5 ranks `d_A` (attraction -> floral antagonism) as the highest-priority arrow:
its two current anchors disagree on sign (Impatiens visual `-0.09` vs Gymnadenia
scent `+0.57`) and it has the largest regime leverage. The B5 recommendation is
therefore **not** "collect more `d_A` studies" but "code a moderator that could
explain the sign conflict, then test it with B3".

The pre-registered moderator (from `configs/part_b_moderator_hypotheses.json`) is
`pollination_generalization`, with the Part A prediction that antagonist tracking
of attractive display is **stronger under generalized pollination**, i.e. the
`specialized -> generalized` contrast is predicted **positive**.

## What to code

Fill `d_A_moderator_coding_queue.csv` (same schema as the Part B effect table plus
`moderator_variable` / `moderator_level`). For each `d_A` effect cluster:

```text
moderator_variable = pollination_generalization      (fixed for this queue)
moderator_level    in { specialized, generalized }   (coded, with a cited basis)
```

Coding rule for `pollination_generalization` (declare the basis in
`extraction_note`; do not infer from taxon name alone):

```text
specialized   the study system's pollination is carried by one or a few
              functional groups / a narrow guild, per the paper's own reporting
generalized   pollination is carried by many functional groups / an open guild
```

If the paper does not state pollinator breadth with enough evidence, leave
`moderator_level` blank and record `coding_status = insufficient_basis`. A blank
level is honest missingness, never a default.

## The two existing anchors

Both real anchors are pre-listed in the queue with `moderator_variable` set and
`moderator_level` **blank**. Their level is a coding decision that must cite the
source's pollinator-breadth evidence; it is intentionally not pre-filled here.

## How many clusters are needed

A `moderator_supported` / `moderator_contradicted` verdict requires **>= 2
independent clusters at each level** (`min_clusters_per_level: 2`). With two
anchors total, at least two to four additional independent `d_A` clusters are
needed so that both `specialized` and `generalized` reach two clusters. Draw new
clusters from the `d_A` seed queries in
`configs/part_b_arrow_literature_seeds.json`; each must pass the per-arrow
eligibility contract before it is added.

## How to run B3 once coded

```text
python scripts/run_part_b_support.py \
  empirical/broad_reality_evidence/broad_route_records.csv \
  empirical/broad_reality_evidence/d_A_moderator_coding_queue.csv \
  empirical/broad_reality_evidence/part_b_arrow_strata.csv \
  configs/part_b_moderator_hypotheses.json \
  configs/part_b_break_even_scenarios.json \
  artifacts/part_b_support
```

Read `part_b_b3_moderator_contrasts.csv`: the
`d_A_display_stronger_where_pollination_generalized` row moves from
`insufficient_levels` to a verdict once both levels have >= 2 clusters. A
`moderator_supported` result is the first real B3 conditionality finding; a
`moderator_contradicted` result is an equally valid finding and is never recoded.
