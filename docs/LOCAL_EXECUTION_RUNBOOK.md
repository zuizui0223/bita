# Running the empirical half locally

Everything blocking the meta-analysis is a property of the web execution environment, not of this
repository or of the literature. On an ordinary machine the whole pipeline runs. This runbook is
the shortest path from a clone to a pooled estimate with a moderator verdict.

## 0. What local access changes, and what it does not

| capability | web environment | local machine |
|---|---|---|
| Crossref, OpenAlex, Europe PMC, Unpaywall | refused by egress policy | works |
| Dryad, Zenodo, OSF, Dataverse, figshare | refused | works |
| PMC open-access full text | partial, via connector only | works |
| **paywalled publisher full text** | refused | **works only with institutional access** |
| GitHub, GitLab, Bitbucket | works | works |

Local access removes the network constraint completely. It does not remove a subscription
constraint. Of the 15 screened include-candidates, **11 have no PMC record** and sit in *Ecology*,
*Ecology Letters*, *Oecologia*, *Current Biology*, *Journal of Chemical Ecology*, and *Journal of
Insect Physiology*. With a university login these are normally readable; without one they are not,
and interlibrary loan or an author request is the remaining route.

The declared thresholds are 5 independent clusters for pooling and 10 for the primary moderator.
The candidate set is roughly 14 clusters, so **reading those 11 is what converts the candidate set
into a meta-analysis.**

## 1. Set up

```bash
git clone https://github.com/zuizui0223/bita
cd bita
git checkout claude/attraction-defense-conditional-olom0x

python -m venv .venv && source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest          # 102 tests; confirms the analysis layer is intact
```

No third-party runtime dependency is used. Every analysis module is standard library only.

## 2. Re-run the declared search, undecomposed

```bash
python scripts/fetch_declared_search.py \
  empirical/broad_reality_evidence/iota_pathway/local_run --queries c_D d_A
```

Europe PMC imposes no boolean-operator cap, so this executes the query **exactly as declared** in
`IOTA_PATHWAY_SEARCH_STRATEGY_v1.md`. The decomposition amendment forced by the connector's
20-operator limit does not apply, which makes the local run the cleaner execution of the
pre-registration. It writes `search_log.csv`, `search_hits.csv`, and `search_diagnostics.json`,
and it retrieves the `d_A` route as well — the highest-leverage parameter by the committed
value-of-information ranking.

The script screens nothing. Screening is a judgement against declared criteria, not a query.

## 3. Screen

Apply §2 and §3 of `IOTA_PATHWAY_EXTRACTION_PROTOCOL_v1.md` to every retrieved record and append
to `screening_decisions_v1.csv` in its existing schema. The 42 decisions already committed are
reusable; six of them are `metadata_not_retrieved` and need finishing first.

Record every exclusion with its reason. The reason vocabulary already in the file maps to the
declared taxonomy in `scripts/audit_screening_endpoint_mismatch.py`; a new reason must be added
there too, or it surfaces as `unclassified` rather than being absorbed into a rate.

## 4. Read the full texts and extract

This is the step that cannot be automated and is the whole remaining cost. For each included
study, take from the article, its supplement, or its deposited dataset:

```text
treatment and comparator response means
their dispersion (SD, SE, or CI)
sample sizes per group
the manipulated concentration, and a citable natural range for the focal system
the assay context and the pollinator functional group
a source locator for every number
```

Append rows to `empirical/broad_reality_evidence/broad_effect_extractions.csv` with
`effect_orientation = positive_is_more_declared_trait_more_declared_outcome`, so a negative value
means more barrier trait and less legitimate pollinator use. Studies reporting the reverse
contrast are sign-flipped at extraction, with the flip noted in `extraction_note`.

Then code the declared moderators into `iota_moderator_coding.csv`, one row per effect per
moderator, each with an explicit `coding_basis`. A test enforces that no target-stratum effect can
enter without its coding.

## 5. Run the analysis

```bash
python scripts/run_broad_meta_analysis.py \
  empirical/broad_reality_evidence/broad_route_records.csv \
  empirical/broad_reality_evidence/broad_effect_extractions.csv \
  empirical/broad_reality_evidence/broad_meta_analysis_strata.csv \
  artifacts/literature

python scripts/run_context_dependence.py \
  empirical/broad_reality_evidence/broad_effect_extractions.csv \
  empirical/broad_reality_evidence/iota_pathway/iota_moderator_coding.csv \
  empirical/broad_reality_evidence/broad_meta_analysis_strata.csv \
  empirical/broad_reality_evidence/iota_pathway/iota_moderator_registry.csv \
  artifacts/iota_pathway
```

Below the declared thresholds these report `insufficient_independent_clusters` and
`insufficient_moderator_capacity` and no estimate. That is the code refusing to over-claim, not a
failure. At or above them you get the pooled random-effects estimate with heterogeneity, the
subgroup pooling, the meta-regression contrast with cluster-robust errors, leave-one-cluster-out
influence, and the context-dependence verdict.

## 6. Feed the estimate back into the theory

```bash
python -c "from trait_architecture.empirical_leverage import cost_from_log_response_ratio as f; \
           print(f(POOLED_LRR, TRAIT_CONTRAST))"

python scripts/run_empirical_leverage.py \
  configs/part_i_robustness_grid.json C_D_CENTRE C_D_HALF_WIDTH artifacts/leverage
```

This reports which regime classifications the interval settles. Expect it to settle direction and
context dependence, not the regime map: 97 of 216 declared points are insensitive to `c_D`
altogether, and settling 80% of the rest needs a half-width of 0.20.

## 7. Reporting rules that travel with the result

- A null on a moderator is **"not detected at a design powered for a halving"**, never evidence of
  no effect. The declared detectable effect is in §7 of the extraction protocol.
- The fixed-effect `Q_between` is descriptive only; its false-positive rate reaches 0.60 under
  realistic heterogeneity. Inference comes from the meta-regression contrast.
- A synthesis built only from PubMed- or Europe PMC-indexed records is a synthesis of that indexed
  subset and must say so.
- Under bridge assumption B1 the pooled arrow gives `sign(iota)`; without it, it remains a
  marginal-route statement. B1 is declared, not demonstrated.
- The measured channel is **fourth of five** by value of information. Do not present it as the
  place where the sign is decided.

## 8. Commit back

```bash
git add empirical/ && git commit && git push
```

CI re-runs every declared analysis and the integrity tests on push, so a mis-shaped effect row or
an uncoded moderator fails the build rather than reaching a readout.
