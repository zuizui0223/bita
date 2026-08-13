# Exposure-threshold selectivity audit v1

## Purpose

Test the mechanism-first prediction that `interaction selectivity` can be a **state** rather than a fixed trait label: a defence can suppress an antagonist while preserving pollination at one dose/exposure regime, then lose that selectivity when legitimate pollinators cross their own behavioural threshold.

This audit uses only source-adjudicated systems already admitted to the matched-defence queue plus primary-source verification. It does not estimate `W_AD`, `rho`, `iota`, or `kappa`.

## 1. Polemonium viscosum — dose-dependent loss of selectivity

Focal floral defence: 2-phenylethanol (2PE).

The admitted source record already establishes:

- high 2PE: ant deterrence plus reduced bumblebee visitation/pollination;
- moderate 2PE: resource-protection benefit without a detected pollination cost.

Adjudication:

```text
moderate expression -> guarded/selective state
high expression     -> non-selective pollinator-interference state
```

This is a within-mechanism dose switch, not evidence that 2PE is intrinsically selective or non-selective.

## 2. Asclepias spp. — exposure-duration threshold

Primary source: Jones & Agrawal 2016, Ecology, DOI `10.1002/ecy.1483`.

Source-verified state:

- individual `Bombus impatiens` in single foraging bouts did **not** avoid cardenolides at the highest reported natural nectar concentrations;
- colony-level deterrence emerged after several days of foraging;
- monarch flower foraging was not deterred;
- monarch oviposition was reduced on plants paired with cardenolide-laced flowers.

Adjudication:

```text
short exposure -> pollinator-null / selective-compatible state
extended exposure -> pollinator deterrence emerges
antagonist response -> response-stage selective: oviposition negative, flower foraging null
```

Thus time/exposure duration can move the same floral chemical across the pollinator-interference boundary.

## 3. Nicotiana attenuata — response-stage rather than arrival suppression

Primary source: Kessler & Baldwin 2007, The Plant Journal, DOI `10.1111/j.1365-313X.2006.02995.x`.

Source-verified state:

- nectar repellents decreased pollinator nectaring time and nectar volume removed;
- the same repellents increased visit number, especially in hummingbirds;
- fewer ants visited repellent-containing nectar;
- nicotine-silenced plants had 68–70% more nectar removed per night than wild type in native populations.

The source explicitly reports an inverse relation between visit duration and visit number, including 112 visits to the nicotine treatment versus 64 to the benzylacetone treatment in one hummingbird assay context.

Adjudication:

```text
antagonist access/use -> reduced
pollinator arrival count -> can increase
pollinator handling / consumption -> reduced
```

This is not one scalar `pollinator cost`. The apparent sign depends on response stage. A defence can preserve or raise encounter/arrival while reducing per-visit exploitation.

## 4. Gelsemium sempervirens — non-selective high-defence state

Primary source: Adler & Irwin 2005, Ecology, DOI `10.1890/05-0118`.

The experiment manipulated gelsemine in nectar. High-alkaloid plants caused nectar robbers and most pollinators to probe fewer flowers and spend less time per flower. High alkaloids also reduced a male-reproduction proxy (fluorescent-dye donation) by roughly one-third to one-half, while female reproductive measures were not detectably changed.

The source used an artificially high 0.5% treatment in 2002 and a lower 0.025% treatment in 2004. The published results indicate broad visitor deterrence at the high treatment and more mixed species-specific responses in the lower-treatment year.

Adjudication:

```text
high defence expression -> non-selective visitor deterrence
lower/natural-range expression -> heterogeneous species-specific response
```

This is an important counterweight to guarded-defence examples: defence benefit and pollinator cost can coexist, and stronger expression need not remain selective.

## 5. Aconitum lycoctonum — threshold separation

The existing source audit records strong reduction in robber consumption at a 20 ppm alkaloid checkpoint and a negative pollinator-visitation association across natural nectar-alkaloid variation. Primary-source interpretation places the sharp decline in legitimate-pollinator visitation at substantially higher natural alkaloid concentrations than the low-dose robber deterrence checkpoint.

Adjudication:

```text
antagonist-response threshold < pollinator-interference threshold
```

The exact ratio is retained as a source-specific threshold pattern rather than promoted to a universal numeric constant.

## Cross-system result

Across independent chemical systems, selectivity repeatedly changes with **dose, duration, and response stage**:

```text
Polemonium: expression level
Asclepias:  exposure duration + consumer response stage
Nicotiana:  visitor response stage
Gelsemium:  expression level / species identity
Aconitum:    separated consumer thresholds
```

The emerging mechanism-level pattern is therefore sharper than `selective vs non-selective defence`:

> A defence creates a selective window when antagonist susceptibility is reached before legitimate-pollinator interference. The window can close as expression or cumulative exposure increases, and its apparent width depends on which behavioural or reproductive response is measured.

This pattern is recurrent across distinct taxa and chemical classes, but the literature does not yet support a single pooled threshold ratio because dose units, consumer endpoints, time scales, and covariance structures differ.

## Theory-facing interpretation

A useful qualitative empirical condition is:

```text
antagonist response threshold < realised D exposure < pollinator interference threshold
```

Within that window, `rho`-compatible antagonist relief can increase without a correspondingly large `iota`-compatible pollinator penalty. Once realised exposure crosses the pollinator threshold, the same defence can move toward a substitution-favouring state.

This is a mechanism-first empirical switching rule, not an estimate of the mixed partial `W_AD`.

## Status

```text
independent threshold/exposure systems: >=5
chemical mechanism replication:         strong
physical mechanism threshold evidence:  still thinner
common pooled threshold scale:           unavailable
switching-rule status:                   RECURRENT_QUANTITATIVE_PROVISIONAL
```
