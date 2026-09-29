# Direct access-geometry boundary-case mechanism audit v1

## Purpose

This audit asks whether the six non-positive programs in the frozen 33-program
formal frame (four OPPOSITE, two MIXED) are mechanistically compatible with the
relative-route-cost boundary

```text
dC_legitimate/dx - dC_bypass/dx
```

without converting the formal-frame direction distribution into a success-rate
test.

## Coding rule

The mechanism code is based on source descriptions of what the focal geometry
physically constrains. The coding question is:

> Does the focal geometry directly harden the bypass/robbery route, or is the
> bypass-cost component not separately identified?

Codes:

- `BYPASS_HARDENED_DIRECT`: source evidence directly identifies the focal
  geometry as obstructing robber entry / bypass use.
- `MECHANICAL_AVOIDANCE_NOT_ROUTE_SEPARATED`: the trait is described as a
  mechanical avoidance trait, but legitimate- and bypass-route costs are not
  separately estimated.
- `ALTERNATIVE_BEHAVIORAL_PREFERENCE`: the source offers a behavioral/context
  mechanism rather than measured bypass hardening.
- `WITHIN_PROGRAM_MORPH_HETEROGENEITY` or `POPULATION_HETEROGENEITY`: no
  single route-cost sign is licensed across the reported strata.

This is a **post hoc mechanistic audit**, not a preregistered or independently
blinded validation. The six programs were selected because their frozen formal
directions are OPPOSITE or MIXED. Therefore no enrichment p-value or predictive
accuracy is computed from this subset.

## Result

Among the four OPPOSITE programs:

- **Thunia alba** and **Meehania urticifolia** are direct bypass-hardening cases:
  the focal bract/calyx architecture physically protects the robbery route.
- **Erica** is a mechanical-avoidance case, but the study does not separately
  identify the cost of legitimate versus bypass access.
- **Impatiens oxyanthera** is not a clean bypass-hardening case; the primary
  article discusses robber preference / niche differentiation as a plausible
  explanation for lower robbery at larger spur-circle diameter.

The two MIXED programs do not support one stable route-cost sign: Tirpitzia
differs by floral morph and Polygala by population.

Therefore the boundary audit supports a narrower statement than “the theory
predicts all reversals”: **the clearest direct bypass-hardening systems fall in
the opposite-direction class, while other reversals require either unresolved
route decomposition or additional behavioral/context mechanisms.**

## Formal-search asymmetry

Within the 33-program OpenAlex denominator:

```text
pre-existing programs recovered in frame: 23
  positive 15 | null 5 | opposite 1 | mixed 2
  opposite = 1/23 = 4.3%

new programs recovered by formal frame: 10
  positive 7 | null 0 | opposite 3 | mixed 0
  opposite = 3/10 = 30.0%
```

This is descriptive, not an inferential comparison. It shows that the formal
outcome-blind search recovered a substantially larger share of reverse-direction
programs than the pre-existing targeted corpus, which is a reason to retain the
formal frame rather than treating the earlier corpus as direction-neutral.

## Claim boundary

Do not use this audit to claim:

- that all opposite cases were prospectively predicted;
- that bypass hardening explains every reversal;
- that 2/2 direct bypass-hardening cases is a success rate;
- that the 1/23 versus 3/10 contrast estimates literature-wide publication or
  discovery bias.

A confirmatory sign-prediction test would require an architecture code frozen for
**all 33 programs** without access to the direction field, ideally by an
independent coder.
