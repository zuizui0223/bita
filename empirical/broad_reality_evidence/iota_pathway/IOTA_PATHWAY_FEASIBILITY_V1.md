# Feasibility of the declared meta-analysis: the binding number

Short version: **the literature is large enough and the access is not.**

## 1. There is no meta-analysis yet

```text
eligible effect rows in broad_effect_extractions.csv   0
independent study clusters with an extracted effect    0
pooled estimates                                       0
moderator verdicts                                     0
```

Nothing in this repository constitutes a quantitative meta-analysis of the declared pathway.
The search log, the screening decisions, the exclusion classification, the design power analysis,
and the value-of-information ranking are all preparatory or diagnostic. None of them is a
substitute for effect sizes, and none should be reported as partial progress toward the pooled
estimate. They are progress toward knowing what to extract and what an estimate would be worth.

## 2. The candidate set clears the declared thresholds — in principle

Screening produced 15 include-candidates. Two of them (Adler and Irwin on *Gelsemium*, 2008 and
2011) are the same system and research group and share one study cluster under the declared
independence rule, giving roughly **14 independent clusters** if every candidate survives full text.

Against the declared capacity thresholds:

```text
pooled stratum, exploratory        3 clusters     candidate set clears it
pooled stratum, stability          5 clusters     candidate set clears it
primary moderator                 10 clusters     candidate set clears it
```

Not every candidate will survive: several measure learning or memory rather than use of the
flower, and full text may show the same mismatch that removed one record already. A realistic
surviving yield is smaller than 14. But the shortfall the target faces is not that this literature
contains too few studies.

## 3. The binding number

Of the 15 candidates, **4 have a PMC record and 11 do not.**

| candidate | venue | full text |
|---|---|---|
| Tiedeken et al. 2014 | J Exp Biol | PMC4006588 |
| self-medication preference assay 2015 | F1000Research | PMC4406194 |
| nicotine and bumblebee learning 2017 | Sci Rep | PMC5434031 |
| caffeine and pollinator memory 2013 | Science | PMC4521368 |
| the other **11** | Ecology ×3, Ecol Lett, Oecologia, J Chem Ecol ×3, J Insect Physiol, Curr Biol | **none** |

Of the four reachable ones, two measure learning or memory rather than use of the flower and may
not carry an extractable use endpoint at all. So the reachable set supports on the order of
**one to two extractable clusters**, against a threshold of five for pooling and ten for the
primary moderator.

That is the whole problem in one line: **11 of the 15 studies that could supply the estimate sit
in journals this environment cannot reach.** Every one of the field-pollination candidates —
*Ecology*, *Ecology Letters*, *Oecologia*, *Current Biology* — is among them.

## 4. What this changes

It settles which constraint to act on. The options are not "find more studies" or "loosen the
criteria":

- **Widening the environment's network policy** to permit publisher and data-repository hosts
  converts a ~14-cluster candidate set into an extractable one. This is the only route that
  reaches the paywalled majority. See
  `empirical/retrieval_audit/RETRIEVAL_REACHABILITY_READOUT_V1.md`.
- **Supplying the 11 full texts or their supplementary tables directly** achieves the same thing
  for this specific candidate set, with no policy change.
- Restoring the PubMed connector alone recovers screening and the four PMC records. It does not
  reach the other eleven, so on its own it does not produce the meta-analysis.

Loosening the inclusion criteria to admit the reachable bee-health studies would raise the row
count and destroy the result: those studies measure the consumer, not the flower's use, so
pooling them would estimate something other than the declared channel.

## 5. Status

The empirical half of the project's target is **not met, and cannot be met from what this
environment can currently read.** The theory half stands. The machinery, the pre-registration, the
declared detectable effect, and the value-of-information ranking are complete and tested, and they
will execute without modification the moment the 11 paywalled full texts become readable.
