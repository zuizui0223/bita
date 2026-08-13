# Physical-domain noncircular stress test v1

## Question

Could the proposed `effective-domain separation` rule be merely a retrospective label applied after seeing pollinator outcomes?

To stress-test that possibility, this audit codes only **physical architecture available before reading the pollinator-response result**: where the barrier is located, which surface/path it modifies, whether the antagonist has a bypass route, and whether the pollinator uses the same or a different access geometry. The outcome is then compared against the architecture-based prediction.

This is a retrospective stress test, not a preregistered prospective validation, and it is therefore interpreted conservatively.

## Coding rule

Before using the reported pollinator outcome, classify a physical floral trait into one of three architecture states:

1. `SEPARATED`: antagonist and legitimate pollinator use demonstrably different surfaces, routes, stages, or functional paths;
2. `OVERLAPPED`: the same physical modification constrains the access geometry used by both antagonist and pollinator;
3. `BYPASSABLE`: the antagonist can reach the resource without crossing the focal barrier.

Predictions:

- `SEPARATED` -> antagonist reduction can coexist with maintained legitimate access/function;
- `OVERLAPPED` -> antagonist reduction should carry pollination interference;
- `BYPASSABLE` -> focal D should fail or be weak against that antagonist route.

## Systems

### 1. Codonopsis lanceolata — SEPARATED

Architecture-only coding:

- distal/abaxial perianth surfaces used by crawling ants carry slippery wax;
- the basal inner surface used as the legitimate hornet pollinator foothold is non-slippery / wax-poor.

Prediction before pollinator outcome: ant access should be filtered while the pollinator foothold remains usable.

Observed source pattern:

- bridging the slippery surface increases ant entry;
- introduced ants shorten hornet visits / evict visitors;
- the flower retains a mechanically usable pollinator foothold.

Result: **matches SEPARATED prediction**.

### 2. Thunia alba — SEPARATED / FUNCTIONAL-ROUTE FILTER

Architecture-only coding:

- the large bract encloses the nectar spur and pedicel;
- legitimate pollination uses the normal floral entrance/labellum route;
- removal exposes a shortcut through the spur wall.

Prediction: intact bracts should suppress the robbery shortcut without reducing arrival to the flower; removing the bract should shift visitor function toward robbery.

Observed source pattern:

- intact: 16 normal vs 3 robbery visits;
- bract removed: 5 normal vs 21 robbery visits;
- hourly visitation frequency does not differ (`P = 0.83`);
- removal reduces pollinia removal, deposition and fruit set.

Result: **matches SEPARATED / routing prediction**.

### 3. Polemonium viscosum — OVERLAPPED

Architecture-only coding:

- experimental tubularization constricts the corolla itself;
- ants and bumblebee pollinators both interact with the same corolla entrance/shape axis.

Prediction: a narrower tube can reduce ant entry but should also impose a legitimate-pollination cost because the access domain overlaps.

Observed source pattern:

- ants enter control flowers more often than experimentally tubular flowers;
- tubular flowers receive significantly less pollen and set fewer seeds.

Result: **matches OVERLAPPED prediction**.

This is a particularly useful falsification-side system because a physically effective defence is not guarded when the pollinator uses the same constrained geometry.

### 4. Salvia miltiorrhiza — BYPASSABLE

Architecture-only coding:

- the persistent calyx covers only part of the corolla tube;
- nectar robbers can bite the uncovered corolla and do not need to cross the shortened-cal\-yx boundary;
- legitimate pollination is by pollen collection at the upper lip rather than entry through the nectar tube.

Prediction: shortening the calyx should not materially change robber or pollinator visitation through those routes.

Observed source pattern:

- shortening the calyx changes neither robber visitation (`P = 0.593`) nor pollinator visitation (`P = 0.207`);
- the major fitness effect of calyx shortening is instead through floral longevity / post-floral function.

Result: **matches BYPASSABLE prediction**, and the focal calyx should not be promoted as an anti-robber D in this system.

### 5. Bejaria resinosa — BROAD / OVERLAPPED boundary

Architecture-only coding:

- stickiness is expressed broadly on petals and sepals;
- the sticky floral surfaces can contact multiple insect taxa rather than a narrowly antagonist-specific route.

Prediction: strong florivore protection may coexist with broad exclusion or potential costs to mutualistic insects; a clean guarded state should not be assumed.

Observed source pattern:

- stickiness strongly reduces florivory;
- trapped insects include bees and other potential mutualists;
- fruit-set effects are population/context dependent and the predicted simple rescue by hummingbird pollination is not supported by a significant stickiness x bird-exclusion interaction.

Result: **consistent with broad/overlapped boundary prediction**, but less decisive than the first four systems because direct pollinator impairment is not isolated as cleanly.

## Stress-test result

For the four most diagnostic systems with an explicit architecture prediction and a directly relevant manipulation/outcome (`Codonopsis`, `Thunia`, `Polemonium`, `Salvia`), the architecture-only state predicts the observed qualitative outcome class in all four cases:

```text
SEPARATED  -> preserved/rerouted legitimate function   Codonopsis, Thunia
OVERLAPPED -> defence + pollination interference       Polemonium
BYPASSABLE -> focal anti-antagonist route fails        Salvia
```

This does not prove a universal law: the audit is retrospective, small-N, and the systems are not sampled randomly. However, it addresses the strongest circularity objection. The rule is not defined solely by the response sign; independently observable geometry can generate an outcome prediction before the pollination result is invoked.

## What the rule should now mean

`Effective-domain separation` should be used narrowly as a **mechanism-level predictor of whether a focal D can discriminate interaction routes**, not as a synonym for any observed guarded outcome.

The empirically safer statement is:

> When antagonist and pollinator routes are physically or physiologically separable, selective defence is possible; when they share the constrained domain, interference is expected; when antagonists bypass the domain, defence efficacy disappears.

This predicts route state. It does not by itself identify total `W_AD`, because total curvature additionally depends on attraction-side effects and direct joint costs.

## Consequence

U6 remains a strong recurrent mechanism-level switching rule, but it must be separated from U7:

- U6: route-level selectivity / interference / failure architecture — strongly recurrent;
- U7: total attraction x defence fitness curvature — still sparse and unresolved.
