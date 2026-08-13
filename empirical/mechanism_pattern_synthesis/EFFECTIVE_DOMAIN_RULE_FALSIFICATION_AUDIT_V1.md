# Effective-domain rule falsification audit v1

## Purpose

Stress-test the current mechanism-first universality candidate rather than accumulate supporting examples.

Candidate rule:

> A flower-specific antagonist-reducing trait preserves pollination only when antagonist and pollinator interaction channels remain sufficiently separated in their effective exposure/access domains. When those domains overlap, pollinator interference can appear. When antagonists bypass the defended domain, antagonist reduction fails.

This audit asks whether the rule predicts both supportive and adverse cases using criteria specified before reading the focal outcome.

## Predeclared three-state prediction

For a focal floral D trait, classify the geometry before using the outcome:

1. `SEPARATED` — antagonist and pollinator differ in susceptibility, access route, spatial contact, timing, dose/exposure, or functional mode.
2. `OVERLAPPED` — the same defensive exposure/access filter is expected to affect both antagonist and pollinator channels.
3. `BYPASSED` — the antagonist can avoid or circumvent the defended exposure/access domain.

Predictions:

```text
SEPARATED -> D can reduce antagonist use with weak/null pollinator penalty
OVERLAPPED -> antagonist reduction may coexist with pollinator interference
BYPASSED -> focal D should show weak/null antagonist reduction on the bypassed route
```

The rule is falsified by repeated cases in which the preclassified state gives the opposite qualitative outcome without a defensible change in biological unit or response stage.

## Stress-test cases

| System | Pre-outcome domain classification | Observed outcome | Prediction check | Role |
|---|---|---|---|---|
| `Codonopsis lanceolata` slippery perianth | `SEPARATED`: wax/slippery ant access surface; legitimate hornet uses an inner foothold/contact zone | artificial bridges increase ant entry; ants shorten pollinator visits; pollinator contact zone remains usable | PASS | independent physical support |
| `Pedicularis rex` water barrier | `SEPARATED` by attack geometry: seed predator must cross barrier; nectar robber can bypass it; legitimate visitors use different route | strong seed-predator reduction; tested robber/pollinator visitation approximately null | PASS | attack-mode support |
| `Thunia alba` spur-enclosing bract | `SEPARATED` by functional route: architecture changes whether the same visitor acts legitimately or robs | intact bract reduces robbery and increases pollinia transfer/fruit set without increasing arrival rate | PASS | functional-routing support |
| `Chrysothemis friedrichsthaliana` water calyx | `SEPARATED` by developmental timing: pre-anthesis oviposition barrier, pollination after anthesis | water removal raises specialist moth infestation; generalists/ants not equivalently blocked | PASS | temporal support |
| `Bejaria resinosa` floral stickiness | `OVERLAPPED`: sticky petal/sepal surface can trap or exclude insects regardless of mutualist/antagonist role | florivory reduced, but insect mutualists can also be excluded; no clean pollinator-guild rescue interaction | PASS | adverse/boundary case |
| `Salvia` calyx/access candidate | `BYPASSED`: robber can attack exposed corolla rather than cross the putative calyx barrier | manipulation does not reduce robber visitation; other fitness effects occur through non-focal functions | PASS | bypass/focal-D failure case |
| `Rivest/Lupinus` pollen alkaloid candidate | consumer/guild susceptibility uncertain; focal antagonist route not established | pollen thieves not reduced; bacterial pattern not cleanly reproduced in isolate assay | DOES NOT QUALIFY AS FOCAL D | prevents circular admission |

## Independent ecological-agent factorials

`Helleborus` and `Fragaria` show that pollinator and antagonist effects on fitness/selection are non-additive or context-dependent. These are useful external checks on the proposition that interaction balance changes with ecological context, but they do not independently manipulate a validated floral A and flower-specific D. They therefore support context sensitivity but are not used to rescue the trait-level rule.

## Falsification assessment

The current rule survives the strongest available physical boundary cases because adverse outcomes are predicted from domain overlap or bypass rather than being reclassified after seeing the outcome.

Crucially:

- `Bejaria` would contradict a weaker claim such as "physical floral defence is generally pollinator-safe"; it does not contradict domain separation because its defended surface is broad.
- `Salvia` would contradict a weaker claim such as "a barrier-like floral structure necessarily functions as antagonist defence"; it instead shows that a bypassed channel fails the operational D gate.
- `Rivest/Lupinus` prevents chemistry from being labelled D merely because it is defence-like; antagonist reduction must be demonstrated.

Thus the candidate universal object is not `physical vs chemical`, not `strong vs weak defence`, and not a fixed trait category. It is the separation or overlap of effective consumer domains.

## Remaining possible falsifiers

The rule is not considered final until the following targeted challenges are exhausted:

1. find a clearly `SEPARATED` floral D manipulation that repeatedly causes strong legitimate-pollinator interference despite preserved domain separation;
2. find a clearly `OVERLAPPED` D manipulation that repeatedly preserves pollination without an alternative separation mechanism;
3. find a clearly `BYPASSED` antagonist route that is nevertheless strongly reduced by the focal D without another causal channel;
4. test whether direct crossed A x D sign changes can be predicted from independently coded domain/context states rather than only described post hoc.

## Current validation status

`SUPPORTED BUT NOT YET FINAL`.

The rule has survived explicit adverse and bypass cases across multiple physical implementations. The highest-value remaining test is prospective coding of direct-factorial/context cases, especially Kessler 2015, before using their A x D outcome sign.
