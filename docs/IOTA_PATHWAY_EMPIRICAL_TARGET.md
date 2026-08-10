# Empirical target: the mutualist-interference constituent pathway

## The completion target this document serves

The project's intended finished form has two halves.

```text
Theory     the local attraction x defence relationship is conditional, because its
           sign is the balance of antagonist relief, mutualist interference, and
           direct joint-cost curvature
Empirical  for at least one constituent pathway of that balance, a quantitative
           meta-analysis over multiple independent studies shows the pathway's
           realised direction in nature and whether that direction is
           context dependent
```

The theory half is delivered by the manuscript, `theory/`, `trait_architecture/sign_criterion.py`,
and the endpoint-normalized sensitivity analysis. This document specifies the empirical half:
which constituent pathway is targeted, what a meta-analysis of that pathway can and cannot say
about the theory, and which declared assumption carries the connection.

## Why a constituent pathway and not the mixed partial

Proposition 1 of the manuscript is a non-identifiability result: the total outcome surface
`W(A,D)`, even observed without error, does not decompose into `M_AD`, `G_AD`, and `C_AD`.
A meta-analysis of total fitness interactions therefore cannot deliver the mechanistic content
of the theory no matter how many studies it pools.

The identification failure is specific to inference from *total* `W`. It does not apply to a
literature that measures one channel directly. The published record for floral biology contains
exactly that: manipulative studies that change a flower-associated barrier trait and measure
legitimate pollinator use, which is a measurement inside the mutualist channel `M` rather than a
measurement of total fitness. That is why the empirical target is a constituent pathway.

## The declared target pathway

```text
route          B_to_pollination
trait class    chemical_barrier
outcome class  pollinator_preference_or_foraging
design class   manipulation
effect metric  log_response_ratio
stratum        BP_chemical_pollinator_use_lrr_manipulation
```

This pathway feeds the mutualist-interference magnitude `iota` in

```text
W_AD = rho - iota - kappa.
```

It was selected over the alternatives for three reasons. It is the only channel whose primary
literature is dominated by *manipulations* of the focal trait rather than observational trait
covariation. It is the channel where the current abstract-level registry already has three
independent primary clusters in one compatibility cell. And it is the channel with a published
history of explicit context dependence — concentration, assay, and pollinator identity — so a
null moderator result is informative rather than merely underpowered.

The physical-barrier counterpart (`BP_physical_visitation_lrr_manipulation`) is screened in the
same reading queue but is not the declared primary target.

## The bridge assumption

Within the implemented corollary (`trait_architecture/model.py`), the mutualist channel is

```text
M(A,D) = P * (b_0 + b_A * A) * exp(-c_D * D) * (1 - c_R * R),
```

so

```text
M_AD  = -P * b_A * c_D * exp(-c_D * D) * (1 - c_R * R)
iota  = -M_AD = P * b_A * c_D * exp(-c_D * D) * (1 - c_R * R).
```

With `P > 0`, `b_A > 0`, and `c_R * R < 1`, this gives

```text
sign(iota) = sign(c_D).
```

The measured pathway supplies `c_D` directly, because in the corollary the pollinator-access
term is multiplicatively separable in `D`. For a manipulation contrasting a treatment level
`d1` against a control level `d0` on the declared trait scale, the oriented log response ratio of
pollinator use is

```text
LRR = ln( access(d1) / access(d0) ) = -c_D * (d1 - d0).
```

Therefore, **under bridge assumption B1 below**:

```text
LRR < 0   <=>  c_D > 0  <=>  iota > 0   (mutualist interference is present)
LRR = 0   <=>  c_D = 0  <=>  iota = 0   (and then W_AD = rho - kappa)
LRR > 0   <=>  c_D < 0                  (the corollary's orientation gate fails)
```

The last line matters: a positive pooled effect is not a nuisance result. It falsifies the
orientation gate `M_AD <= 0` for the systems that produced it, and the oriented form
`W_AD = rho - iota - kappa` is then invalid there.

### B1 — declared bridge assumption

> The effect of the focal barrier trait `D` on legitimate pollinator use is multiplicatively
> separable from the focal attraction trait `A`: changing `D` rescales pollinator access by a
> factor that does not depend on `A`.

B1 is what converts a marginal arrow into a channel-curvature sign. It is an assumption, not a
finding, and it is testable: a study that measures pollinator use under a factorial manipulation
of both `A` and `D` either supports it or refutes it. No such study is verified in the current
registry, which is why B1 is stated here rather than assumed silently. Without B1, the pooled
arrow remains a statement about the marginal route only, and the manuscript's existing wording
— that a negative `D -> pollinator use` response does not by itself establish `M_AD < 0` —
continues to apply unchanged.

## What the declared moderators test

| Moderator | Theory quantity it addresses |
|---|---|
| `dose_realism` (categorical) | Whether `c_D > 0` holds at concentrations the focal systems actually express, or only above them. A level reversal means `iota` is not a fixed property of the trait label. |
| `log_dose_multiple_of_natural_maximum` (continuous) | Whether `c_D` is a constant. Under the corollary, `LRR / (d1 - d0)` is dose-invariant. A significant slope means the exponential access form is too rigid and `c_D` must be carried as dose dependent. |
| `assay_context` (categorical) | Whether the measured route effect transfers from paired-choice laboratory assays to free-foraging field pollination, i.e. whether the measurement layer is the pollination channel of the theory. |
| `pollinator_functional_group` (categorical) | Whether `iota` is partner-specific; declared before extraction so a null is reportable. |

Context dependence in the pollinator-service direction is separate. In the corollary
`d iota / d P = b_A * c_D * exp(-c_D * D) * (1 - c_R * R) > 0` whenever `c_D > 0`, so a study
set stratified by pollinator service would speak to `d W_AD / d P`. The current queue does not
support that stratification and the analysis is not declared.

## Inference boundary

A completed meta-analysis of this pathway licenses statements of the form:

- the realised direction of the `D -> legitimate pollinator use` route across independent
  systems, with its uncertainty and heterogeneity;
- whether that direction or magnitude changes with the declared context moderators;
- under B1, the sign of `iota` and whether the corollary's orientation gate survives.

It does not license, and must not be reported as:

- an estimate of `rho` (antagonist relief) or `kappa` (direct joint-cost curvature);
- an estimate of the complete local mixed partial `W_AD`;
- an estimate of `d W_AD / d H` or `d W_AD / d P`;
- a claim about how common either sign of `W_AD` is in nature;
- trait covariance, correlational selection, an optimum, or an evolutionary trajectory.

One channel constrains one term of a three-term balance. That is the honest ceiling of this
empirical half, and it is enough to convert the conditional theory from a possibility argument
into a claim with one empirically anchored term.

## Status

The analysis machinery, the compatibility stratum, the moderator registry, and the extraction
protocol are committed and executable. The effect table is empty, so every declared analysis
currently returns `insufficient_moderator_capacity` by design rather than by omission. See
`empirical/broad_reality_evidence/iota_pathway/IOTA_PATHWAY_EXTRACTION_PROTOCOL_v1.md` for the
extraction protocol and the current retrieval blocker.
