# Search execution readout v1

The pre-registered search was executed against PubMed on 2026-08-10 through the PubMed MCP
connector. This readout records what was run, what came back, what was screened, and where the
run stopped. Machine-readable records are in `search_log_v1.csv` and `screening_decisions_v1.csv`.

According to PubMed. Included candidate studies are cited by DOI in section 4.

## 1. Amendment: the declared query had to be decomposed

The query declared in section 2 of `IOTA_PATHWAY_SEARCH_STRATEGY_v1.md` contains 35 boolean
operators. The connector rejects any query above 20 (`INVALID_QUERY`, `too many boolean
operators`). The declared query was therefore decomposed into sub-queries whose union
approximates it, each run and logged separately.

This is a protocol amendment and is recorded as such: the decomposition changes the retrieved set
in ways the union does not fully control, because a term dropped from one sub-query's outcome
block is not recovered by another sub-query unless it appears there. The affected blocks are
listed per sub-query in `search_log_v1.csv`. No inclusion criterion, moderator, threshold, or
outcome definition was changed.

## 2. Yield

| query | operators | total hits | returned | screened |
|---|---|---|---|---|
| declared full query | 35 | — | — | rejected by the connector |
| `C_D_A1` alkaloids × pollinator nouns | 15 | 118 | 100 | partially |
| `C_D_A2` alkaloids × behavioural outcomes | 14 | 110 | 100 | no |
| `C_D_A3` secondary-metabolite vocabulary × pollinator nouns | 15 | 250 | 100 | no |
| `C_D_D1` deterrence and preference vocabulary | 12 | **26** | 26 | **20 of 26** |
| `C_D_C1` choice-assay vocabulary | 10 | 128 | 60 | no |

`C_D_D1` is the highest-precision query for the declared outcome class and was prioritised for
screening. The connector returned metadata for 20 of the 26 requested records and then stopped;
the remaining six are logged as `metadata_not_retrieved` and must be screened when retrieval
resumes. They are not counted as screened and not counted as excluded.

## 3. Screening result

42 records carry a decision. All decisions are at title and abstract except one, noted below.

```text
include_candidate                  15
exclude                            20
exclude_from_c_D_flag_for_d_A       1
metadata_not_retrieved              6
```

Exclusion reasons cluster into four kinds, and the largest is the one the pre-registration
predicted: **outcome is not legitimate pollinator use.** Studies of parasite load, mortality,
detoxification physiology, and digestive performance dominate the PubMed-indexed subset of this
literature. They manipulate the right compounds in the right context but measure bee health
rather than flower use, so they cannot supply a barrier-to-use contrast.

One record was excluded at full text rather than abstract: Thorburn et al. 2015
([10.12688/f1000research.6870.2](https://doi.org/10.12688/f1000research.6870.2)). Its title and
abstract mention a consumption experiment, but the full text shows that experiment manipulates
incubation temperature, not the alkaloid, so it yields no barrier-to-use contrast.

## 4. Candidate set for extraction

Fifteen records are include-candidates pending full text. The ones bearing most directly on the
declared stratum and its moderators, according to PubMed:

- Tiedeken et al. 2014, deterrence thresholds against reported natural nectar concentrations —
  the primary source for the declared `dose_realism` moderator
  ([10.1242/jeb.097543](https://doi.org/10.1242/jeb.097543))
- Gegear et al. 2007, ecological context and pollinator deterrence by nectar alkaloids
  ([10.1111/j.1461-0248.2007.01027.x](https://doi.org/10.1111/j.1461-0248.2007.01027.x))
- Adler and Irwin 2011, gelsemine manipulated in wild plants with pollen deposition and removal
  ([10.1007/s00442-011-2153-3](https://doi.org/10.1007/s00442-011-2153-3))
- Irwin and Adler 2008, nectar secondary compounds and self-pollen transfer
  ([10.1890/07-1359.1](https://doi.org/10.1890/07-1359.1))
- Singaravelan et al. 2005, free-flying honeybee feeding responses to nectar-mimicking secondary
  compounds ([10.1007/s10886-005-8394-z](https://doi.org/10.1007/s10886-005-8394-z))
- Köhler et al. 2012, nectar nicotine deterrence in honeybees
  ([10.1016/j.jinsphys.2011.12.002](https://doi.org/10.1016/j.jinsphys.2011.12.002))
- Reinhard et al. 2009, feeding deterrence of pyrrolizidine alkaloids in honey bees
  ([10.1007/s10886-009-9690-9](https://doi.org/10.1007/s10886-009-9690-9))
- Vannette and Fukami 2016, nectar microbes altering metabolite effects on consumption
  ([10.1890/15-0858.1](https://doi.org/10.1890/15-0858.1))
- Barlow et al. 2017, nectar alkaloid concentration with pollinator and robber responses
  ([10.1016/j.cub.2017.07.012](https://doi.org/10.1016/j.cub.2017.07.012))

The full list with per-record reasons is in `screening_decisions_v1.csv`.

**No effect has been extracted.** Fifteen candidates is not fifteen clusters, and an abstract does
not license an effect row. Extraction requires the treatment and comparator responses, their
dispersion, sample sizes, and the concentration against a cited natural range — none of which is
in an abstract.

## 5. Identifier verification caught 13 errors

DOIs were first drafted from the model's own reading of the record list and then overwritten with
the values actually returned by the connector. **Thirteen of the drafted DOIs were wrong** and
were corrected; the corrections are visible in the commit diff for
`screening_decisions_v1.csv`.

This is recorded rather than quietly fixed because it is the concrete justification for the
protocol's rule that every identifier must come from the source. A plausible-looking DOI is not a
DOI. The six records with no retrieved metadata are left with blank identifier fields rather than
plausible guesses.

## 6. Where the run stopped, and what it changes

The PubMed connector disconnected mid-run. Remaining work, in order:

1. Screen the six `metadata_not_retrieved` records from `C_D_D1`.
2. Screen `C_D_C1`, `C_D_A2`, and `C_D_A3`, whose hits are logged but unscreened.
3. Retrieve full text for the 15 include-candidates and extract oriented effects with locators.
4. Code the declared moderators.

The coverage limitation declared in section 5 of the search strategy is now observed rather than
predicted. The include-candidates that measure field pollination outcomes sit in *Ecology*,
*Ecology Letters*, and *Oecologia* with no PMC record, while the records that are open in PMC are
predominantly the bee-health studies that screening excluded. Full-text access for the candidate
set therefore remains the binding constraint, and the network-policy route in
`empirical/retrieval_audit/RETRIEVAL_REACHABILITY_READOUT_V1.md` is still the one that resolves
it.
