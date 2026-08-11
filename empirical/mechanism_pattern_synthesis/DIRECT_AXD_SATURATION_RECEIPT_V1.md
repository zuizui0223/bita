# Direct `A x D` search saturation receipt v1

## Decision

**Gate A — direct interaction search: PASS under the registered v1 search universe and stopping rule.**

The dedicated direct-interaction search was not stopped because a desired number of positive studies was reached. It was stopped because the preregistered query families ceased yielding new **eligible direct-design classes**.

## Registered search families

The fixed families in `SEARCH_REGISTRY_V1.csv` are:

```text
DX01  direct interaction: attraction + defence + interaction/fitness
DX02  joint attractive/defensive trait architecture
DX03  pollinator/herbivore/defence factorial or selection designs
DX04  floral signal/pigment + defence/secondary chemistry interaction designs
DX05  scent + defence + pollinator/herbivore designs
DX06  nectar/reward + defensive chemistry/access + mutualist/antagonist designs
```

The registered stopping rule is:

```text
until_two_consecutive_expansion_batches_yield_no_new_eligible_direct_design_class
```

## Expansion batches

### Batch 1

`DIRECT_AXD_QUERY_BATCH_1_V1.csv` screened all six families and yielded:

```text
new strict Tier-1 A x D clusters: 0
```

The batch broadened the **exclusion architecture** — whole-plant resistance costs, comparative A–D covariance, ecological-agent factorials, dual-function traits, floral-blend component partitioning and single-D multiconsumer studies — but did not identify a new design satisfying the strict floral A + flower-specific D + interaction-outcome contract.

### Batch 2

`DIRECT_AXD_QUERY_BATCH_2_3_V1.csv` again screened all six families using additional primary examples, including Helleborus, Lobelia, Iris, Delphinium, Brassica and floral-scent systems.

```text
new strict Tier-1 A x D clusters:          0
new eligible direct-design classes:        0
all hits mapped to adjudicated exclusions: yes
```

This is the **first consecutive no-new-eligible-design batch** under the stopping rule.

### Batch 3

A further targeted pass emphasized flower-specific physical/access traits, nectar-robbing resistance, floral chemistry, trait–fitness studies and pollinator–herbivore selection systems, including Caryopteris, Tirpitzia, Primula, Aconitum, Delphinium and nectar-guide designs.

```text
new strict Tier-1 A x D clusters:          0
new eligible direct-design classes:        0
all hits mapped to adjudicated exclusions: yes
```

This is the **second consecutive no-new-eligible-design batch**.

The v1 stopping rule is therefore satisfied.

## Strict result after saturation

The current strict direct-interaction layer contains:

```text
eligible independent clusters: 1
eligible cluster: Gorden_Adler_2018_Impatiens_capensis
```

Its two reproductive-component interaction estimates are direct but unresolved:

```text
CH fruits per plant per day:
  A x D = -0.0820 ± 0.0548 SE
  95% CI includes zero

seeds per CH fruit:
  A x D = +0.1040 ± 0.1043 SE
  95% CI includes zero
```

The point estimates differ in sign across reproductive components, so the saturated strict layer does **not** support a universal direct interaction sign.

## What the search repeatedly found instead

The negative search result is structurally informative. Near-miss studies repeatedly fall into a small set of designs:

```text
1. ecological-agent factorials
   pollination x herbivory changes fitness or selection, but D is an agent/treatment rather than a defence phenotype;

2. cross-organ defence
   a floral attraction trait interacts with or is selected under a leaf/whole-plant defence, but the D organ gate fails;

3. joint A and D measurements without A x D
   both trait families are present in the same plants, but only marginal/main effects are fitted;

4. dual-function single traits
   one pigment, scent, guide or morphology changes both mutualist and antagonist behaviour, leaving one phenotype axis rather than A and D;

5. floral-blend component partitioning
   different scent compounds divide attractive and defensive functions, but their interaction on a common outcome is not estimated;

6. single-D multiconsumer studies
   a defensive nectar/access trait affects pollinators and antagonists, but there is no independently varied attraction axis;

7. comparative A–D covariance
   attraction and defence architectures covary across species, but there is no linked within-system interaction outcome;

8. linkage failure
   otherwise promising data cannot be linked at the biological unit required for an A x D estimate.
```

These classes explain why broad searches for `pollinator + herbivore + defence + interaction` greatly overstate the amount of evidence that actually identifies the theoretical mixed partial.

## Scientific interpretation

The saturated search supports the following bounded result:

> In the registered search universe, direct empirical estimation of an interaction between a distinct floral attraction axis and a flower-specific defence/access axis is rare. The literature much more commonly measures separate marginal routes, dual-function traits, ecological-agent interactions, cross-organ defence effects or comparative covariance. The one strict current direct cluster is itself sign-unresolved across reproductive components.

This is an **evidence-gap result**, not a claim that no additional eligible study could ever be discovered outside the registered search universe.

## Why the search can stop

Continuing indefinitely would now violate the purpose of the preregistered stopping rule. Three expansion passes have been completed, including two consecutive passes with no new eligible direct-design class. Additional papers in already-adjudicated exclusion classes would increase citation count without changing the inferential state of the strict direct layer.

A later manuscript reviewer or newly discovered primary source can reopen Gate A only by supplying a candidate that plausibly changes the eligible-design universe.

## Gate status

```text
Gate A direct A x D search saturation: PASS
strict direct A x D independent clusters: 1
strict direct sign resolved: no
absence of a broad direct evidence base: formal evidence gap
```

This gate does not unfreeze the manuscript by itself. Gates C, F and G remain open; Gate E is already satisfied.