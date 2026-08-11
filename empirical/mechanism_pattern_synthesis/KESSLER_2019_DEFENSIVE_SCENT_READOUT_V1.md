# Kessler, Bing, Haverkamp & Baldwin (2019) — defensive function of benzyl acetone

## Source identity

```text
article DOI: 10.1111/1365-2435.13332
plant:       Nicotiana attenuata
focal trait: benzyl acetone (BA), a floral volatile
mutant:      CHAL — floral BA emission silenced
control:     EV — empty-vector control emitting BA
public data: EDMOND DOI 10.17617/3.24, declared by the article
```

## Role assignment

BA is a **dual-function single floral trait**. Prior work in this system establishes its pollinator-attracting role, while this study experimentally tests a defensive function against floral herbivory.

This architecture is important for the synthesis but must not be transformed into a direct `A x D` record: one volatile molecule does not create two independent trait axes simply because it has two ecological functions.

The eligible route here is therefore:

```text
BA defensive expression -> floral antagonist colonization / damage
```

## Field evidence

The paper compares BA-silenced CHAL and BA-emitting EV plants across multiple field seasons. The source reports the following plant-infestation states:

```text
2011
  CHAL: 52.9% infested
  EV:   17.6% infested
  Fisher exact P = 0.035

2014
  CHAL: 37.1% infested
  EV:   10.3% infested
  Fisher exact P = 0.013

2016
  CHAL: 23.1% infested
  EV:    0.0% infested
  Fisher exact P = 0.098
```

The same direction appears across years: removing BA increases colonization by the chrysomelid florivore *Diabrotica undecimpunctata*. The source also reports greater floral damage on CHAL plants.

Exact year-specific treatment sample sizes are not inferred from the rounded percentages. Consequently, this readout does not back-calculate odds ratios or standard errors from the percentages and P-values.

## Temporal mechanism

The defensive phenotype is temporally aligned with BA emission. During the early part of the night, when EV flowers emit BA, scent-silenced CHAL flowers receive more feeding damage. During the second half of the night, when EV flowers cease BA emission, the damage difference disappears.

This is registered separately in `SIGN_SWITCH_LEDGER_V1.csv` because it identifies **trait-expression timing** as a mechanism moderator rather than treating an all-night aggregate as the only defensible response.

## Sensory / bioassay support

The study also shows that *D. undecimpunctata* can detect BA and that behavioural/physiological responses depend on concentration. These experiments strengthen the interpretation that the field phenotype is mediated by the floral volatile rather than by an unrelated constitutive difference between transformed lines.

They are not counted as independent study replications of the field result.

## Public-data route

The article explicitly cites:

```text
Kessler, Bing, Haverkamp & Baldwin (2019)
EDMOND Digital Repository
DOI 10.17617/3.24
```

EDMOND is a Dataverse-based Max Planck repository. A bounded audit workflow now queries the public Dataverse API by persistent DOI and records only file names, schemas, candidate columns and numerical ranges. Observation-level rows are never written to the repository or Actions artifact.

The public-data audit is used only to determine whether the year-specific field results can be promoted to an uncertainty-bearing quantitative effect. Until exact treatment sample counts and source-aligned response rows are recovered, the field record remains source-reported directional/percentage evidence.

## Evidence classification

```text
D_to_antagonism:               experimental, source-verified
flower-specific defence:       yes
single-trait dual function:    yes
same-system A x D:             no — one biological trait axis
field quantitative SE effect:  pending public-data audit
context switch:                time of night / BA emission state
independence cluster:          one Kessler-et-al.-2019 study cluster
```

## Mechanistic implication

This study adds an important mechanism class to the synthesis: an attractive floral signal can itself be defensive against a floral antagonist. That does **not** imply universal functional synergy. Instead it shows why trait-role orientation must be separated from trait identity: the same molecule can occupy different ecological channels, and its net evolutionary effect depends on who encounters it, at what concentration, and when it is expressed.
