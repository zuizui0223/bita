# Erica 2026 hold-out source audit v1

## Source

Coetzee A, Seymour CL, Spottiswoode CN, Pirie MD, van der Niet T. 2026.
**Is bee-avoidance by bird-pollinated flowers driven by nectar robbing in Erica?**
*Functional Ecology* 40:1046-1060.
DOI: `10.1111/1365-2435.70276`.

Source checked: publisher open-access full text and article-linked dataset statement on 2026-09-18.

## Why it qualifies as a hold-out candidate

This study was published in 2026 and is not one of the systems used to formulate the existing effective-domain rule.

For the visitor-rate analysis the authors used 27 populations from 12 bird-pollinated *Erica* species across 11 natural communities. Robbing and pollination were scored on flowers in the same population-level study, and models included mechanical floral traits.

The focal candidate D axis is:

```text
corolla length
```

in an ornithophilous system where nectar robbers are predominantly bees and legitimate pollinators are sunbirds.

This gives an architecture code that can be stated before using the focal response coefficients:

```text
pre_outcome_domain_code = SEPARATED
separating_coordinate   = geometry
defence_modality        = physical/access
```

Rationale: long tubular bird-pollinated flowers create different access geometry for short-bodied/short-mouthpart bee robbers versus legitimate avian pollinators. This is the study's declared mechanical bee-avoidance context, not a label invented from the response sign.

## Source-reported matched outcomes

In the population-level mixed models:

```text
nectar robbing ~ corolla length:
t = -2.0, p = 0.04

pollination rate ~ corolla length:
t = +2.0, p = 0.05
```

Corolla stickiness did not significantly predict either robbing or pollination in these models.

The authors interpret the combined mechanical-trait pattern as increasing corolla length potentially reducing robbing while increasing pollination.

## Hold-out interpretation

Pre-outcome prediction from geometry:

```text
longer corolla
-> lower bee robbing
-> pollination preserved or increased
```

Observed qualitative state matches that prediction.

However:

- the study is observational/comparative rather than a randomized corolla-length manipulation;
- p=0.05 on pollination is boundary evidence, not a license to call a universal positive effect;
- the 27 populations / 12 species are nested data within one publication, not 27 independent BITA study clusters;
- the source's primary question concerns bee-avoidance and colour, so the BITA mechanical-trait use is a secondary re-framing.

## Adjudication

```text
primary empirical source:          PASS
2020-2026 hold-out window:         PASS
same-system antagonist outcome:    PASS
same-system pollination outcome:   PASS
pre-outcome architecture code:     PASS (SEPARATED / geometry)
independent study cluster count:   1
strict causal D manipulation:      NO
hold-out candidate status:         ELIGIBLE_COMPARATIVE
```

Do not merge this system into derivation evidence when scoring hold-out performance.
