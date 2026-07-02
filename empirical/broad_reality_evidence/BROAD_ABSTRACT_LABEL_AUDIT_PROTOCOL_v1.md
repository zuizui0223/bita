# Broad abstract label audit protocol v1

## Purpose

The fixed L1 broad abstract map is intentionally high recall. This audit measures
whether its predicted A/B/P/H edge labels actually describe the flower-context
content of the corresponding Crossref abstract.

It is **not** a new literature search, an effect-size extraction, a direct causal
screen, or a calibration of the attraction--defence model parameters.

## Fixed source boundary

The audit packet is drawn only from `fixed-broad-abstract-evidence-map`, built
from the fixed L1 corpus. Candidate IDs, query membership, and the number of
candidate papers are never changed by this protocol.

## Sampling design

| Stratum | Rule | Target |
|---|---|---:|
| joint A+B+P+H | Census every predicted joint record | all 11 current records |
| A→P | Sample nonjoint predicted positives, stratified as empirical/nonreview versus other; joint census records are included separately | up to 25 nonjoint |
| A→H | Same | up to 25 nonjoint |
| B→H | Same; current nonjoint frame is small enough for census | all 21 nonjoint + 11 joint |
| B→P | Same | up to 25 nonjoint |
| edge-none flower control | Flower-context abstracts with no predicted A→P, A→H, B→H, or B→P label, stratified by source bucket | up to 25 |

The packet can contain fewer physical rows than the sum of targets because a
single abstract can belong to multiple audit strata. Its `audit_strata` field
preserves every stratum membership.

## Human codes

For each selected abstract, set `coding_status=reviewed` only after coding:

```text
human_floral_context
human_A
human_B
human_P
human_H
human_W
human_flower_specific_B
human_study_role
human_shared_cost
```

Binary fields use `yes`, `no`, `uncertain`, or `not_applicable`.

`human_flower_specific_B=yes` requires that the relevant barrier or defence is
measured or discussed on the flower, nectar, inflorescence, or another
reproductive organ. Leaf, stem, bark, or generic whole-plant defences do not
satisfy this condition.

## What counts as a coherent predicted edge

| Predicted label | Human coherence criterion |
|---|---|
| A→P | flower context + A + P |
| A→H | flower context + A + H |
| B→H | flower context + B + flower-specific B + H |
| B→P | flower context + B + flower-specific B + P |
| joint | flower context + A + B + flower-specific B + P + H |

Study role does not determine whether a broad label is coherent. It is recorded
separately so the final report can distinguish empirical-language coverage from
reviews, background statements, and indirect studies.

## Calibration output

The summary script writes:

- label precision by target label, source bucket, and sampling scope;
- label-calibrated candidate coverage for each edge;
- control-stratum missed-edge rate;
- audit completion status.

For noncensus strata, calibrated coverage is a beta-binomial uncertainty range.
For census strata, it is the observed human-coherent count. A coverage estimate is
withheld until every selected row in every partition of that edge is reviewed.

## Interpretation boundary

The final calibrated numbers estimate the amount of **abstract-level candidate
coverage** in the fixed corpus. They cannot be described as counts of confirmed
causal studies, evidence of a biological null, pooled effect sizes, or numerical
values of `b_A`, `d_A`, `e_F`, `c_D`, `c_AD`, or `c_R`.
