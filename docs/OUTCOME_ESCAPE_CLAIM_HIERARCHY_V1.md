# Outcome escape claim hierarchy v1

## Decision

A positive attraction-by-defence interaction is not synonymous with release of an attraction conflict. The four-cell outcome surface supports three nested claims that must be reported separately.

For one declared attraction contrast `A`, one declared antagonist-reducing contrast `D`, and one declared reproductive outcome scale, define

```text
A0 = W10 - W00
     attraction effect when defence is low

A1 = W11 - W01
     attraction effect when defence is high

Delta_AD W = W11 - W10 - W01 + W00
           = A1 - A0
```

The claim hierarchy is

```text
Level 1  positive interaction relief:  Delta_AD W > 0
Level 2  constraint release:           A0 <= 0 and A1 > 0
Level 3  strict sign reversal:         A0 < 0 and A1 > 0
```

Thus

```text
strict reversal
    => constraint release
    => positive interaction relief
```

The reverse implications do not hold.

## Level 1 — positive interaction relief

`Delta_AD W > 0` means that adding defence shifts the effect of attraction in a positive direction:

```text
A1 > A0
```

This is a real outcome-level result. It answers whether `D` improves the marginal reproductive return to the declared `A` contrast on the declared outcome scale.

It does **not** require `A0` or `A1` to be positive. For example,

```text
A0 = -0.80
A1 = -0.20
Delta_AD W = +0.60
```

shows strong positive interaction relief even though attraction remains detrimental in both defence states.

The historical project token

```text
ESCAPE_IDENTIFIED
```

is retained for backwards compatibility with registered Stage-1 outputs. It is an alias for an uncertainty-identified positive total interaction only. New reports must also show the Level-2 and Level-3 statuses whenever `A0` and `A1` are estimable.

## Level 2 — nonpositive-to-positive constraint release

A stronger claim is that attraction was not beneficial without defence but became beneficial with defence:

```text
A0 <= 0
A1 > 0
```

For supplied uncertainty intervals, the registered sufficient decision is

```text
upper(A0) <= 0
lower(A1) > 0
```

This is the minimum outcome pattern that justifies language such as:

> the second trait released the declared attraction contrast from a non-beneficial one-trait state on this reproductive scale.

Even this claim does not show that pollinators and antagonists stopped using the same cue. It is functional release, not informational or architectural escape.

## Level 3 — strict negative-to-positive reversal

The strongest local outcome statement is

```text
A0 < 0
A1 > 0
```

with the interval rule

```text
upper(A0) < 0
lower(A1) > 0
```

This establishes a strict negative-to-positive reversal of the attraction effect between the two defence states. A zero-compatible `A0` can support Level 2 but cannot support Level 3.

## Kessler 2008 — current partial-identification result

Kessler, Gase & Baldwin (2008; DOI `10.1126/science.1160072`) provides the closest manipulated `A × D`-like field surface. The current registered aggregate enumeration uses the published 474 informative flowers, 87 capsules, EV proportion band 34.5–35.5%, low-cell bands 11.5–14.5%, and four denominator-balance profiles.

Across every compatible integer allocation in those profiles:

```text
A0 = W10 - W00       in [-0.0299275, +0.0299275]
A1 = W11 - W01       in [+0.2001327, +0.2398387]
Delta_AD W            minimum +0.1710239
```

The ordering is now sharper than a rounded arithmetic example:

```text
A1 > 0 for every compatible allocation
A0 spans zero
Delta_AD > 0 for every compatible allocation
```

Thus the aggregate evidence partially identifies the Stage-1 surface:

```text
Level 1 total-interaction sign:        strong positive aggregate anchor
A1 defended attraction effect:         sign-identified positive under declared restrictions
A0 undefended attraction effect:       sign unresolved within approximately ±0.03
Level 2:                               unresolved because A0_max > 0
Level 3:                               unresolved because A0_max > 0
```

The smallest descriptive epsilon for which every compatible allocation satisfies `A0 <= epsilon` is `0.0299275`, about three percentage points on the capsule-probability scale. This is an identified-set width, **not** a retrospectively chosen equivalence margin and not a basis for relabeling Level 2.

The registered decision is therefore

```text
A1_POSITIVE_A0_SIGN_UNRESOLVED_PARTIAL_IDENTIFICATION
```

rather than an undifferentiated `Levels 2/3 unresolved` statement.

However, these sets are not source/design-based confidence intervals. Exact genotype-by-day denominators, plant clustering and the source ANOVA remain unrecovered. The broadest auxiliary logit 95% interval can cross zero. Consequently the formal source-scale status remains:

```text
Level 1: positive sign anchor; formal source uncertainty unresolved
Level 2: unresolved
Level 3: unresolved
```

Systemic nicotine suppression also limits the intervention-scope claim. The source-faithful surface is not automatically a flower-exclusive defence experiment.

Canonical receipts:

- `empirical/identification_design/KESSLER_2008_STAGE1_PARTIAL_IDENTIFICATION_RECEIPT_V2.json`
- `empirical/identification_design/KESSLER_2008_STAGE1_PARTIAL_IDENTIFICATION_RECEIPT_V2.md`
- `empirical/identification_design/KESSLER_2008_IDENTIFICATION_REAUDIT_V3.md`

## Separate mechanism-identification ladder

The outcome hierarchy does not allocate the result among ecological channels. Under the BITA bookkeeping identity,

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

where the terms represent antagonist relief, pollinator interference, and a remaining joint channel whose interpretation as cost requires an independent assay.

A Level-1, Level-2 or Level-3 outcome can therefore be established before point-identifying the channels. Conversely, complete channel allocation is an explanation of the outcome, not a substitute for measuring `A0`, `A1` and `Delta_AD W`.

The two ladders are orthogonal:

```text
Outcome ladder
interaction relief -> constraint release -> strict reversal

Explanation ladder
identified set -> partial channel bounds -> selective channel allocation -> independent joint-cost validation
```

## Separation from SCH

SCH asks why one attraction coordinate becomes conflicted when pollinators and antagonists respond to the same cue. Its strongest escape endpoint is informational or architectural separation of receiver-facing cues.

BITA asks whether a distinct antagonist-reducing trait changes the reproductive return to attraction. Even Level-3 strict reversal can occur while antagonists continue to detect the original cue. Therefore none of the BITA outcome levels demonstrates:

- cue privacy;
- cue modularization;
- a historical shared-to-private transition;
- lineage branching;
- disappearance of the original receiver overlap.

## Reporting contract

Every analysis or manuscript statement about escape must report four items:

1. the declared `A`, `D` and outcome scale;
2. `A0`, `A1` and `Delta_AD W` with compatible uncertainty or an explicit identified set;
3. the highest supported outcome level;
4. the separate mechanism-identification and intervention-scope status.

Do not use an unqualified statement such as “defence released the conflict” when only `Delta_AD W > 0` is established. When `A1` is sign-identified but `A0` spans zero, report that asymmetry directly rather than collapsing both contrasts into `unresolved`.
