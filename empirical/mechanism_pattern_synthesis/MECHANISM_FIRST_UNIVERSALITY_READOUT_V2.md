# Mechanism-first universality readout v2

## Decision frame

Part I fixes the mechanism first. Part II is therefore evaluated as a **replication and universality test of theory-predicted constituent mechanisms and switching rules**, not as a search for an empirical pattern from which a mechanism is inferred after the fact.

The existing 56-record / 25-cluster route architecture is retained as the frozen discovery base. New universality audits do not increment route N unless they independently pass the focal trait/organ/realized-function gates.

## Current prediction statuses

```text
U1 antagonist cost / relief opportunity       RECURRENT_STRONG
U2 attraction shared by mutualists/antagonists RECURRENT_PROVISIONAL
U3 flower-specific defensive efficacy          RECURRENT_STRONG
U4 pollinator interference from defence        CONDITIONAL_RECURRENT
U5 interaction selectivity / guarded defence   RECURRENT_QUANTITATIVE_PROVISIONAL
U6 switching-rule recurrence                   RECURRENT_STRONG
U7 direct A x D sign                            UNIDENTIFIED / WEAK
U8 direct joint cost kappa                      UNIDENTIFIED
```

## U5 — replicated selective-defence state

Three independent systems now provide numeric matched evidence for one defence axis against antagonist and legitimate-pollination responses:

### Catalpa speciosa — consumer selectivity

Floral nectar iridoids strongly reduce exploitation in two potential-thief assays (`LRR=-1.2742`, `SE=0.2291`; `LRR=-0.9430`, `SE=0.2344`) while legitimate bee reward consumption is approximately unchanged (`LRR=-0.0102`, `SE=0.0187`).

### Pedicularis rex — attack-mode selectivity

A water-filled floral barrier strongly reduces seed predation (`beta=-0.072`, `SE=0.007`) but does not detectably change nectar-robber visits (`beta=-0.014`, `SE=0.225`) or legitimate pollinator visits (`beta=+0.012`, `SE=0.224`). Robbers physically bypass the barrier.

### Thunia alba — functional-mode selectivity

The intact bract strongly reduces robbery (`LRR=-1.7663`, `SE=0.2039`), leaves visitor arrival approximately unchanged (`LRR=+0.0370`, `SE=0.1630`), and increases pollinia removal (`+1.2953`, `SE=0.2532`), deposition (`+1.1520`, `SE=0.3532`), and fruit set (`+1.2556`, `SE=0.4207`). The same Bombus changes ecological function rather than visitor identity.

These outcomes are not pooled because response scales and within-study covariances differ. Their evidentiary value is **independent recurrence of the same mechanism-level state across distinct implementations**, not a fabricated grand effect.

## U6 — the stronger replicated switching rule

The emerging universal candidate is now more precise than “context dependence.” Selectivity itself changes with relative consumer thresholds, dose, attack route, and functional mode.

### Polemonium viscosum — within-mechanism dose switch

Moderate 2PE protects floral resources without a detected pollination cost, whereas high 2PE deters ants but also reduces bumblebee visitation and pollination. The same defence therefore moves from guarded-compatible to interference state as expression increases.

### Aconitum spp. — threshold-separation window

Nectar robbers are deterred above roughly 20 ppm alkaloids, whereas legitimate pollinator visitation declines sharply only around 200–380 ppm. The result defines an intermediate concentration window in which antagonist sensitivity is crossed before pollinator sensitivity.

Across Polemonium and Aconitum, distinct plant taxa and chemical systems independently support the same higher-level rule:

> **selective defence exists when the antagonist response threshold is crossed before the legitimate-pollinator interference threshold; selectivity collapses when defence expression exceeds the pollinator threshold.**

This is a stronger and more mechanistic generalization than classifying whole traits as “selective” or “non-selective.”

## Falsification test — defence chemistry is not sufficient

Rivest et al. 2024, Lupinus argenteus, is retained as a deliberate falsification/context case rather than promoted into route N.

Pollen alkaloids occur in the floral reward/reproductive tissue, but they do not predict lower thrips or pollen-beetle abundance. Field bacterial abundance is negatively associated with pollen alkaloids, yet direct thermopsine assays on three common bacterial isolates are null and bacterial harm to plant fitness is not established. Pollinator visit number is positive with pollen alkaloids, bout duration is shorter, and total flowers visited is approximately unchanged.

This falsifies a chemistry-alone rule and supports a more general formulation:

> **realised floral defence depends on defence expression × consumer susceptibility × attack/exposure route × response stage.**

A compound can be chemically defensive yet fail to instantiate focal `D` against a particular antagonist guild.

## Current higher-level empirical conclusion

The empirical evidence now supports the following mechanism-first working pattern:

> Floral attraction is repeatedly exposed to shared tracking by mutualists and antagonists. Flower-specific defensive mechanisms repeatedly reduce antagonist access, but their pollinator cost is not universal. Across independent chemical and physical systems, selective states recur when antagonist and pollinator interactions differ in susceptibility, access route, timing, or visitor function. Independent dose studies further show that this selectivity occupies a response window rather than being an immutable trait property. Thus **relative interaction thresholds and access geometry**, rather than defence presence alone, are the strongest current empirical candidates for determining whether antagonist relief can be gained without pollinator interference.

This pattern is compatible with the theoretical complementarity/substitutability balance, but it is not a direct empirical estimate of `W_AD` because direct `A x D` and joint-cost evidence remain unresolved.

## What would falsify the current candidate rule

The universality claim should be weakened if targeted matched studies repeatedly show any of the following:

1. strong antagonist reduction only at doses below the antagonist threshold inferred from the focal defence;
2. pollinator interference consistently appears before or at lower expression than antagonist relief;
3. attack-mode or consumer-selective barriers repeatedly fail to preserve legitimate function;
4. additional independent systems show no reproducible threshold/access/consumer structure and instead produce idiosyncratic signs with no mechanism-level alignment.

These cases must be retained, not screened away.

## Remaining scientific tasks

1. Finish the matched-D queue for Gelsemium, Asclepias, Nicotiana and remaining source-capable systems, coding both selective and non-selective states.
2. Recover uncertainty-bearing dose/threshold contrasts where source structure permits, especially Polemonium and Aconitum.
3. Test whether a common **threshold-ratio / selectivity-window** metric can be defined without mixing incompatible response lanes. If not, document exact underidentification.
4. Expand quantitative A -> antagonism coverage so shared attraction tracking is tested across scent, visual display and colour with more than direction counts.
5. Continue targeted search for strict shared-unit/factorial `A x D` and direct joint-cost estimates.
6. Recompute U1–U8 after each targeted batch; stop only when the mechanism-level replication statuses and counterexamples stabilize.

## Current stop decision

```text
class saturation:                   reached
mechanism-first universality:       ACTIVE
matched selective numeric anchors:  3 independent systems
independent dose/threshold switches: 2 systems
explicit falsification contexts:    1 registered system
U5:                                 RECURRENT_QUANTITATIVE_PROVISIONAL
U6:                                 RECURRENT_STRONG
direct A x D:                       unresolved
kappa:                              unidentified
scientific evidence work:           CONTINUE
```
