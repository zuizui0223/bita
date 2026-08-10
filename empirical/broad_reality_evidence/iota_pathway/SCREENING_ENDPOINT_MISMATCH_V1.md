# Screening endpoint-mismatch readout v1

Reproduce with:

```bash
python scripts/audit_screening_endpoint_mismatch.py \
  empirical/broad_reality_evidence/iota_pathway/screening_decisions_v1.csv \
  empirical/broad_reality_evidence/iota_pathway
```

## 1. Why the exclusions are worth reading

Screening usually produces bookkeeping. Here it produced something closer to a result, so it is
recorded separately from the search execution readout.

Most excluded records were not off topic. They manipulate a flower-associated chemical, present it
in a floral context, and give it to a pollinating insect — and then measure something other than
the insect's use of the flower.

That distinction is exactly the one the local theory turns on. The mutualist channel concerns how a
barrier trait changes *use of the flower*. A study that feeds bees an alkaloid and records parasite
load is measuring the consumer, and it cannot supply a barrier-to-use contrast however well it is
done.

## 2. Classification of the exclusions

36 records screened, 15 include-candidates, 21 exclusions. Every recorded reason mapped to a
declared class; none fell through to `unclassified`.

| exclusion class | records | share of exclusions |
|---|---|---|
| **endpoint measures the consumer** | **7** | **0.33** |
| not primary research | 4 | 0.19 |
| trait is not a barrier | 4 | 0.19 |
| descriptive, no contrast | 3 | 0.14 |
| off topic | 2 | 0.10 |
| endpoint is the trait itself | 1 | 0.05 |

`endpoint measures the consumer` covers parasite load, pathogen load, mortality, detoxification,
metabolic fate, digestive performance, and gustatory neuron response. It is the largest single
class, exceeding every other reason, and it is 19% of all screened records.

Adding `endpoint is the trait itself` — where the response variable is nectar chemistry rather than
pollinator behaviour — brings the endpoint-related share of exclusions to 8 of 21.

## 3. What this supports, and what it does not

**Supports.** The manuscript argues that distinguishing the three channels requires measurements
targeted at each channel, and that the existing record establishes route plausibility without
supplying channel curvature. This screen puts an observation behind that argument: within a set of
studies retrieved by a query written to find barrier-to-pollinator-use effects, the most common
reason a study could not be used was that it measured the consumer's physiology rather than the
flower's use. The measurements exist; they are aimed elsewhere.

**Does not support.** This is a property of the screened set, not of the literature. The set came
predominantly from one high-precision sub-query of one database, and PubMed indexes this field
partially and non-randomly — a bias that plausibly *inflates* the consumer-physiology share,
because bee-health work is exactly what a biomedical index covers best. The share reported here
must therefore not be quoted as the composition of the pollination-cost literature. Six further
records from the same query remain unscreened.

## 4. Reading it against the value-of-information ranking

The two results point the same way from different directions. The value-of-information analysis
found that the tractable channel is not the decisive one. This screen finds that even within the
tractable channel, a substantial share of the retrievable literature measures the wrong endpoint.
Together they say the constituent-pathway synthesis will be built from a smaller and more
scattered evidence base than the raw hit counts suggest, which is a reason to state its claim
narrowly rather than to abandon it.

## 5. Boundary

Counts describe the screened set at the time of the run. The reason-to-class mapping is declared in
`scripts/audit_screening_endpoint_mismatch.py`; a reason absent from that mapping is reported as
`unclassified` rather than absorbed, so adding a new reason cannot quietly change a rate.
