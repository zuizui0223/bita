# Trait-barrier hysteresis first-open result v1

Status: **PRIMARY INFERENCE GATE FAILED / DO NOT PROMOTE**

Preregistration:
`TRAIT_BARRIER_HYSTERESIS_PREREG_V1.md`

First opened: 2026-10-07
Branch: `analysis/ecological-stability-evolutionary-transience-v1`

## Recovered temporal support

Public EPHI inputs:

```text
interaction rows                         = 54,471
camera rows                              = 6,198
eligible clean timestamped deployments   = 5,165
timestamped interaction rows             = 53,279
interactions uniquely assigned to deployment = 46,276
ambiguous deployment assignments         = 0
```

The frozen treatment was the first observed Diglossa `piercing=yes` event in a
deployment with the requested symmetric pre/post coverage. The frozen control was
the first explicit legitimate Diglossa feeding event in a deployment with no
observed Diglossa piercing anywhere in that deployment.

## Primary +/-12 h analysis

```text
eligible breach deployments  = 9
eligible control deployments = 0
breach sites                 = 2
breach plant species         = 8

hummingbird events before    = 27
hummingbird events after     = 34
```

Because the frozen control arm contains zero eligible deployments:

```text
PRIMARY SITE-STRATIFIED DIFFERENCE-IN-DIFFERENCES = NOT IDENTIFIABLE
MIXED BREACH/CONTROL SITES                         = 0
PRIMARY GATE                                       = FAIL
```

The preregistered primary permutation test, bootstrap contrast, and causal-style
breach-versus-control interpretation therefore cannot be computed.

## Breach-only descriptive pattern

These quantities are retained only to show whether the temporal direction is at
least internally stable. They are **not** substitutes for the failed primary test.

Mean post-minus-pre change in barrier-hummingbird robbery events:

```text
+/- 6 h:  n=10, mean Delta = -0.40
+/-12 h:  n= 9, mean Delta = +0.67
+/-24 h:  n= 4, mean Delta = -0.75
```

The sign changes across the frozen windows.

For the +/-12 h window:

```text
median Delta barrier robbery = 0
mean Delta barrier legitimate = -0.89
mean Delta accessible robbery = 0

conditional barrier robbery-share change:
n with defined pre/post shares = 3
mean Delta share = -0.165

barrier hummingbird species participation:
mean post-minus-pre species count = -0.44

fraction of breach deployments with a post-breach barrier robber
not already represented among pre-breach barrier robbers = 1/9 = 0.111
```

These sparse descriptive quantities do not supply a stable hysteresis signature.

## Frozen single-flower sensitivity

```text
eligible breach deployments with camera_flowers_count = 1: 0
eligible controls:                                      0
```

The highest-specificity sensitivity is therefore unavailable.

## Decision

The preregistered promotion conditions are not met.

Do not claim from EPHI that a prior Diglossa breach makes a static bill–tube barrier
history-dependent. The biological mechanism remains plausible and is explicitly
identified as unresolved in the Aubert study, but this public dataset does not
contain the treatment/control support needed to test it.

The correct status is:

> **not testable with the frozen EPHI temporal design, with unstable breach-only
> descriptive direction.**

No weaker post-hoc pooled test should replace the failed primary design.
