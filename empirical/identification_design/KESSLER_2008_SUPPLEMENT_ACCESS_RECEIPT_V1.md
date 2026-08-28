# Kessler 2008 supplement access receipt v1

## Decision

The Kessler, Gase & Baldwin (2008) attraction-by-nicotine field factorial remains the strongest manipulated `A × D` reproductive-outcome anchor in BITA, but its source-level factorial uncertainty could not be recovered from the currently registered public Science routes.

The registered probe ran in GitHub Actions run `33187904211` at branch head `d4dcc805422626adf0b4cafeecfb78b692b1614f`.

```text
supplement_status:       NOT_RECOVERED_FROM_REGISTERED_PUBLIC_ROUTES
Fig. S8A text status:    NOT_EVALUABLE
registered routes tried: 5
HTTP result:             403 on all 5 routes
```

## What remains directly recoverable from the article

The public article record still establishes the high-value experimental structure:

```text
EV    BA present, nicotine present
PMT   BA present, nicotine suppressed
CHAL  BA suppressed, nicotine present
CP    BA suppressed, nicotine suppressed
```

For female pollinator-mediated outcrossing, the article reports:

- 601 antherectomized flowers across five experimental days;
- 127 flowers on one windy day produced no capsules and had no active pollinators;
- 474 flowers remained on the four informative days;
- 87 capsules were produced before later herbivore/plant-loss attrition;
- EV averaged about 35% capsule production;
- PMT, CHAL and CP each averaged about 12–14%;
- the source points to Fig. S8A for individual-day values.

Those published aggregate constraints keep the descriptive discrete interaction sign positive across the rounded cell range, as recorded in `KESSLER_2008_FACTORIAL_SIGN_ROBUSTNESS_V1.md`.

## What the failed supplement recovery changes

It does **not** demote the direct manipulated factorial. It changes the precise unresolved gate.

```text
A manipulated:                       YES
D-candidate manipulated:             YES
common female reproductive outcome:  YES
published aggregate A×D sign:        POSITIVE / robust to rounded range
source interaction SE or CI:         NOT RECOVERED
exact day-by-genotype values:        NOT RECOVERED
formal interval wholly > 0:          NOT ESTABLISHED
```

The missing object is therefore no longer “a manipulated A×D common reproductive surface.” Kessler 2008 already provides one. The missing object is **uncertainty-bearing interaction identification on that surface**, plus the separate mechanism-allocation measurements required for `rho_delta`, `iota_delta` and `kappa_delta`.

## Claim boundary

A publisher-access failure is not evidence that the source interaction was nonsignificant. Equally, rounded genotype means are not a license to invent a source interaction SE or CI.

The valid paper-level wording is:

> A field manipulation of floral attraction and nicotine yields a sign-robust positive discrete reproductive interaction under the published aggregate constraints, but exact day-level data or a source-reported factorial uncertainty are not currently recoverable from the registered public supplement routes. The sign is therefore stronger than an observational near miss but still below a formally uncertainty-identified positive escape event.

## Next gate

1. Search lawful alternative archives or author-deposited supporting material for Fig. S8A / day-by-genotype values without changing the estimand.
2. In parallel, quantify the strongest assumption-indexed aggregate uncertainty bound possible from the 474-flower / 87-capsule constraints, while keeping it explicitly distinct from the source day-stratified analysis.
3. If source-level uncertainty remains inaccessible, retain Kessler as `DIRECT_FACTORIAL_SIGN_POSITIVE_FORMAL_UNCERTAINTY_UNRESOLVED` and prioritize another manipulated `A × D` system with complete uncertainty rather than returning to observational endpoint mining.
