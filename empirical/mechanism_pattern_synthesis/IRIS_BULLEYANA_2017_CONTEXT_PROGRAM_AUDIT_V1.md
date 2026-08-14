# Iris bulleyana 2017 florivory–pollination context audit v1

## Scope

Two 2017 studies in *Iris bulleyana* provide unusually explicit evidence that antagonist damage and resource/tissue context can alter pollinator behaviour and reproductive outcomes.

They are admitted only to the **environmental/context Pattern layer**. Neither florivory treatment nor protection of a resource is the focal defence trait `D`.

## Study 1 — Ye et al. 2017

Ye Z-M, Jin X-F, Wang Q-F, Yang C-F, Inouye DW. **Pollinators shift to nectar robbers when florivory occurs, with effects on reproductive success in Iris bulleyana (Iridaceae).** *Plant Biology* 19:760–766. DOI `10.1111/plb.12581`.

### Published Pattern

The source reports:

- sawflies damaged the calyx/nectary;
- three bumblebee species acted as pollinators;
- the short-tongued pollinator *Bombus friseanus* became a nectar robber when a sawfly-created hole was available;
- robbing bouts had shorter flower handling time than legitimate visits;
- pollinator visitation decreased in damaged flowers;
- seed production decreased in damaged flowers;
- supplementary hand pollination removed the seed-production difference between damaged and undamaged flowers;
- bumblebees visited fewer flowers per plant in the florivore-exposed plot.

### Pattern classes

```text
antagonist pressure -> pollinator service coupling
consumer functional-role switching
resource depletion / access-route context
pollination limitation mediating reproductive cost
```

The same Bombus species can therefore change from mutualistic pollinator to nectar robber after florivore-created structural damage.

## Study 2 — Zhu et al. 2017

Zhu Y-R, Yang M, Vamosi JC, Armbruster WS, Wan T, Gong Y-B. **Feeding the enemy: loss of nectar and nectaries to herbivores reduces tepal damage and increases pollinator attraction in Iris bulleyana.** *Biology Letters* 13:20170271. DOI `10.1098/rsbl.2017.0271`.

Dryad dataset DOI: `10.5061/dryad.dp062`, containing `Herbivory and pollination rates.xls` and the R analysis code.

### Published Pattern

The experiment protected nectar/nectaries from herbivores and compared tissue damage and pollinator visitation with unmanipulated controls.

The source reports:

- nectar/nectaries were strongly preferred by herbivores under natural conditions;
- protecting nectar/nectaries redirected herbivore damage toward tepals;
- protecting nectar/nectaries significantly reduced pollinator visitation (`coefficient = -0.68`, `P = 0.003` in the published analysis);
- the interpretation is that nectar/nectaries can function as sacrificial resources that divert herbivory away from showy tepals important for pollinator attraction.

### Pattern classes

```text
alternative-resource context
tissue-specific antagonist allocation
indirect antagonist -> attraction pathway
pollinator response mediated by which floral tissue is damaged
```

## Why the linked program is useful

Together these studies demonstrate that antagonist pressure is not merely a scalar amount of 'damage'. The **location and behavioural route of damage** changes which pollination pathway is expressed:

```text
sawfly-created access hole -> pollinator can switch to robber
nectary availability -> herbivores concentrate on sacrificial tissue
nectary protection -> more tepal damage -> lower pollinator visitation
```

This adds mechanistic resolution to the Haas-Desmarais 2026 meta-analytic finding that tissue and natural/simulated damage mode strongly moderate herbivory effects on floral traits, pollinator attraction, and reproduction.

## Independence boundary

The two Iris papers share a plant system and regional research context. Until field-site/year/panel overlap is explicitly reconciled, they should **not** be counted as two independent biological replications in any route-count total.

They can nevertheless supply two source-verified context mechanisms because the manipulations and response questions differ.

## Theory boundary

Not admitted:

```text
florivory treatment = D
sacrificial nectar = D
pollinator-to-robber switch = W_AD
-0.68 pollinator coefficient = iota
H-induced visitation change = dW_AD/dH
```

Admitted:

> antagonist context can alter pollinator behaviour, floral tissue damage, and reproductive limitation through coupled pathways, so empirical `H` cannot generally be treated as an isolated additive axis.

## Current adjudication

```text
primary source identities:        PASS
context mechanisms:               PASS
public data route for Zhu 2017:   PASS
focal D route eligibility:        NO
direct A x D eligibility:         NO
meta-analytic module status:      NO, source-level context replication
```

### Decision

**PROMOTE_TO_ENVIRONMENTAL_PATTERN_LAYER**
