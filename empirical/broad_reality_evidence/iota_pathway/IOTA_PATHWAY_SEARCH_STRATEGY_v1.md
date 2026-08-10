# Pre-registered search strategy (v1)

The extraction protocol declares what counts as an eligible effect. It does not declare how
candidate studies are found, and a synthesis whose search was improvised after seeing results is
not reproducible. This document fixes the search before it is run.

It is written against the retrieval route that is actually available: the PubMed MCP connector
already installed for this account. Section 5 states, in advance, the coverage limitation that
route imposes, so the limitation is part of the pre-registration rather than a caveat added once
the numbers are in.

Status: **not yet executed.** The connector is toggled off for this conversation, so no query in
this document has been run and no count in section 6 has been filled.

## 1. Databases

| source | role | access |
|---|---|---|
| PubMed | primary declared database | MCP connector (`search_articles`, `get_article_metadata`, `get_full_text_article`) |
| PubMed related-article graph | supplementary | `find_related_articles` on every included record |
| reference lists of included studies | supplementary | manual, from retrieved full text |
| the committed reading queue | seed set | `iota_reading_queue.csv`, 15 candidates |

No other database is declared, because no other is reachable. If the network policy is later
widened, adding a database is a protocol amendment and must be recorded as v2 with the reason and
the date, not folded silently into v1.

## 2. Declared query — target stratum (`c_D`)

Route `B_to_pollination`, chemical barrier to legitimate pollinator use.

```text
(nectar[tiab] OR pollen[tiab] OR floral[tiab] OR flower[tiab] OR flowers[tiab])
AND (alkaloid[tiab] OR alkaloids[tiab] OR "secondary metabolite"[tiab] OR "secondary metabolites"[tiab]
     OR "secondary compound"[tiab] OR "secondary compounds"[tiab] OR toxin[tiab] OR toxins[tiab]
     OR nicotine[tiab] OR caffeine[tiab] OR amygdalin[tiab] OR grayanotoxin[tiab]
     OR gelsemine[tiab] OR anabasine[tiab] OR iridoid[tiab] OR phenolic[tiab])
AND (pollinator[tiab] OR pollinators[tiab] OR pollination[tiab] OR bee[tiab] OR bees[tiab]
     OR bumblebee[tiab] OR bumblebees[tiab] OR Bombus[tiab] OR "Apis mellifera"[tiab]
     OR hummingbird[tiab] OR hummingbirds[tiab] OR visitation[tiab] OR foraging[tiab]
     OR preference[tiab] OR consumption[tiab])
```

## 3. Declared query — highest-leverage route (`d_A`)

Route `A_to_antagonism`, attraction trait to floral antagonist damage. The value-of-information
ranking places this parameter first, so its search is declared now rather than after the target
stratum is finished.

```text
(floral[tiab] OR flower[tiab] OR flowers[tiab] OR inflorescence[tiab] OR inflorescences[tiab])
AND ("display size"[tiab] OR "flower number"[tiab] OR "flower size"[tiab] OR "corolla size"[tiab]
     OR color[tiab] OR colour[tiab] OR scent[tiab] OR volatile[tiab] OR volatiles[tiab]
     OR "floral signal"[tiab] OR "floral signals"[tiab] OR attractiveness[tiab])
AND (florivory[tiab] OR florivore[tiab] OR florivores[tiab] OR "floral herbivory"[tiab]
     OR "flower damage"[tiab] OR "bud predation"[tiab] OR "seed predation"[tiab]
     OR herbivory[tiab] OR "nectar robbing"[tiab])
```

## 4. Declared limits and supplementary searching

- **Date range:** no lower bound; upper bound is the date the search is executed, which is recorded
  in the search log.
- **Language:** reports in English are screened; non-English records are logged and excluded with
  the reason `language_not_screened`, and their count is reported rather than hidden.
- **Publication type:** primary reports only. Reviews and meta-analyses are not eligible but their
  reference lists are mined, and each is recorded as `used_as_reference_source`.
- **Supplementary searching:** `find_related_articles` is run once on every included record, and
  the reference list of every retrieved full text is screened. Both are logged as separate
  discovery routes so their yield can be reported separately from the database query.
- **Seed set:** the 15 committed reading-queue candidates are screened under the same criteria as
  database hits. Their identifiers are verified with `convert_article_ids` or
  `lookup_article_by_citation`, which clears the `unverified_from_search_result` flags.

## 5. Declared coverage limitation

PubMed indexes biomedical literature. Its coverage of pollination and floral ecology is real but
**partial and non-random**: journals such as *Oecologia*, *Proceedings of the Royal Society B*,
*PLOS ONE*, and *Scientific Reports* are indexed, whereas several of the field's core venues —
*Ecology*, *Oikos*, *Functional Ecology*, *Journal of Ecology*, *American Journal of Botany* — are
largely absent unless individual articles are deposited in PMC.

Three consequences are declared in advance:

1. A stratum that reaches capacity from this search alone is a synthesis of the
   **PubMed-indexed subset** of the literature, and must be reported with that wording.
2. The resulting sample may be biased toward venues with a physiological, toxicological, or
   pollinator-health framing, which plausibly correlates with the declared `dose_realism` and
   `assay_context` moderators. Any moderator result must be read with that confound stated.
3. The declared small-study and asymmetry diagnostics do not detect this. Database coverage bias
   is not funnel asymmetry, and the Egger test must not be cited as evidence against it.

This limitation is a reason to widen the network policy later, not a reason to withhold the
search now.

## 6. Screening flow and the counts to record

Recorded at each stage, per query, in a committed search log:

```text
records returned by the declared query
records after deduplication
records excluded at title and abstract, with reason
full texts sought
full texts unavailable, with the access barrier recorded
full texts screened
studies excluded at full text, with reason
studies included
independent study clusters represented
effects extracted
```

A record whose full text cannot be retrieved is logged as `full_text_unavailable` with the
barrier named. It is never coded from its abstract and never entered into the quantitative layer;
the abstract-level direction registry is a separate evidence level and stays separate.

## 7. Deduplication and clustering

Deduplication is by DOI first, then by PMID, then by normalized title and first-author surname and
year. Study-cluster assignment follows the extraction protocol: one experimental system, one field
season or assay series, one research group. Two reports of the same manipulation on the same
population share a cluster, and the earlier report is the cluster's primary record.

## 8. Amendment rule

Any change to the queries, the databases, the limits, or the screening criteria after execution
begins is recorded as a new version of this document, with the date, the reason, and the counts
already collected under the previous version. Reporting a result under a search strategy that was
edited to fit it would defeat the purpose of writing this down.
