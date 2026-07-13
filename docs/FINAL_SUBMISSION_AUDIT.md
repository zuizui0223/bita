# Final submission audit

## Audit purpose

This audit checks whether the active repository tells one coherent submission story and whether auxiliary components are being mistaken for additional focal claims.

## Primary submission spine

The manuscript-facing repository now has one primary claim:

```text
For one declared floral attraction trait A,
one declared flower-specific barrier/defence trait D,
and one declared outcome scale W,
the local A x D mixed partial can be interpreted mechanistically only after
channel definitions and orientation conditions have been established.
```

The active sensitivity analysis asks how that local sign behaves across a finite declared set of biological parameter scenarios and endpoint-normalized response-shape variants.

## Decision on reproductive assurance R

`R` is retained in the implemented corollary as an auxiliary background moderator of the pollination-mediated channel.

It is **not**:

- a third focal trait in the manuscript claim;
- an omnibus reproductive strategy axis;
- a separate empirical target of the current paper.

A paired audit of the current declared grid showed that changing `R` from `0.0` to `0.5` changes the local sign in 16 of 1,296 otherwise matched scenario × response-shape evaluations. The effect is therefore small but not identically zero. Removing `R` silently would alter a small subset of results; retaining it transparently as an auxiliary moderator is the more reproducible choice.

The manuscript should not lead with `R`, interpret its current parameterization biologically, or claim that the paper develops a three-trait theory.

## Decision on the literature layer

The current literature registry remains preliminary context only.

Reasons:

- current directional records are abstract-level;
- coding is machine-assisted and single-coder;
- the registry has not undergone full-text verification;
- independent duplicate coding or documented adjudication is not yet complete;
- the quantitative extraction table does not calibrate the focal model.

Therefore the literature layer is not a second independent submission claim and must not be described as a systematic meta-analysis validating the regime map.

## Submission language to preserve

Use:

```text
one primary local-theory claim
finite-set sensitivity analysis
auxiliary background moderator R
preliminary literature context
```

Avoid:

```text
two equal submission claims
three-trait theory
empirically calibrated regime map
full-text systematic review
universal attraction-defence law
```

## Remaining implementation audit

The mathematical and submission narrative are now separated from historical research directions. Any future cleanup should be judged by one rule: a change must improve the reproducibility or interpretation of the active focal-pair theory without silently changing the scientific question.
