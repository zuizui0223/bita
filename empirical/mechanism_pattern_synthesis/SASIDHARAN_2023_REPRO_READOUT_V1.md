# Sasidharan et al. 2023 deposited-synthesis readout v1

## Decision

**Gate C contribution: PASS as a defensible deposited-synthesis reanalysis with explicit source discrepancy.**

Sasidharan et al. (2023; DOI `10.1093/aob/mcad064`, PMCID `PMC10550281`) can serve as the second biologically distinct quantitative mechanism module required by `COMPLETION_GATE_V1.md`.

This is **not** an exact reproduction of every printed table and is **not** a primary-effect meta-analysis. Its admissible role is narrower: a source-audited quantitative cross-study module for how floral volatile compounds are detected by, and behaviorally affect, pollinators and florivores, with study dependence and repeated-unit disagreement retained explicitly.

The manuscript remains frozen until the other completion gates are satisfied.

## Why this qualifies for Gate C

The current PMC-deposited workbook supports all of the following:

1. observation coding can be reconstructed without inventing a cross-assay continuous effect;
2. the article's final **32-study** structure is recovered conservatively;
3. a numerical physiological-detection contrast can be reconstructed from unique `FVOC x insect x role` test units;
4. study influence can be audited by leaving out each of the 32 recovered study components;
5. repeated behavioral disagreements can be identified as real cross-study/context heterogeneity rather than silently deduplicated;
6. paper-versus-current-deposit discrepancies are bounded and reported rather than resolved by arbitrary row choice.

That satisfies the Gate C requirement for a defensible reanalysis of a deposited synthesis. It also supplies the study-independence/influence component required by Gate G for this module, while leaving the study-composition limitation explicit.

## Source identity and coding

Source:

- article DOI: `10.1093/aob/mcad064`
- PMCID: `PMC10550281`
- deposited workbook: `mcad064_suppl_supplementary_data.xlsx`
- sheets: `S1`–`S5`
- focal response ledger: `S1`
- analyzed S1 test rows: `517`

The source is categorical. Physiological response is encoded as response/no-response fields; behavioral choice is encoded as `+`, `-`, `0`, or missing. No common standardized continuous effect size is manufactured across GC-EAD/EAG/SCR/SSR and behavioral assays.

## Conservative recovery of the 32 studies

Literal source references are not copied into the repository outputs. The audit instead normalizes citation text and constructs study components under a deliberately conservative rule:

- exact normalized citation stems are identical labels;
- different citation stems are linked only when they share an explicit DOI;
- fuzzy similarity is diagnostic only and never causes an automatic merge.

Current deposit diagnostics:

- raw reference strings: `36`
- exact citation stems: `35`
- DOI-free stems: `3`
- conservative study components after exact-stem/shared-DOI linking: **`32`**
- article-reported final study count: **`32`**
- components containing both pollinator and florivore records: `4`

Thus the study count is recovered without a discretionary fuzzy bibliographic merge.

## Physiological detection: current deposited synthesis

The article defines the total-level source unit as an unrepeated combination of FVOC and insect; the role is retained because pollinator and florivore responses are contrasted. Under the current PMC S1 deposit:

| role | detected | not detected | total | detected fraction |
|---|---:|---:|---:|---:|
| pollinator | 151 | 69 | 220 | 0.6864 |
| florivore | 84 | 19 | 103 | 0.8155 |

Current-deposit contrast:

- florivore minus pollinator risk difference: **`+0.1292`** (~`+12.9` percentage points)
- risk ratio: **`1.188`**
- odds ratio: **`2.020`**
- Yates-corrected chi-square on the current deposited counts: `chi-square = 5.272`, `P = 0.0217`
- detection conflicts among repeated source units: `0`

The printed article table gives exactly the same pollinator counts (`151/69`) but gives florivores as `83/19` (`n=102`). The current deposit therefore contains **one additional detected florivore source unit** relative to the printed table. The reanalysis uses the current deposited data and records this discrepancy; it does not delete a row to force agreement.

## Study-dependence sensitivity

### Leave-one-study-component-out

Using the conservatively recovered 32 study components, the current-deposit risk difference was recomputed after deleting each component in turn:

- runs: `32`
- minimum florivore-minus-pollinator difference: `+0.0873`
- median: `+0.1274`
- maximum: `+0.2065`
- positive direction: **`32/32`**
- zero: `0/32`
- negative: `0/32`

Therefore the assembled test-unit contrast is not produced by any single study component.

### Equal-weight study-role summary

Giving each study-role unit equal weight rather than each FVOC-insect test:

- florivore: `18` study-role units; mean detected fraction `0.919`; median `1.0`
- pollinator: `17` study-role units; mean detected fraction `0.825`; median `1.0`

The direction remains the same in the unweighted study-role mean, but the distributions are strongly ceilinged.

### Same-study warning

Only **three** study components contain physiological-detection data for both functional roles. In those three paired components:

- median florivore-minus-pollinator difference: `0`
- positive: `0`
- zero: `3`
- negative: `0`

This is the critical interpretation boundary. The `+12.9` percentage-point contrast is a **cross-study assembled pattern**, robust to single-study deletion, but it is **not demonstrated as a within-study causal or paired role effect**. Study-by-role composition remains a plausible contributor.

## Behavioral response: heterogeneity must be retained

The current deposit contains `264` unique `FVOC x insect x role` units with coded behavioral response. Six repeated units are discordant across source studies.

All six disagreements are **attraction (`+`) versus no response (`0`)**, not attraction versus repulsion:

- pollinator discordant units: `5`
- florivore discordant units: `1`
- units spanning multiple recovered study components: **`6/6`**
- units spanning multiple plant genera: `5/6`

This is direct evidence that nominally repeated FVOC-insect response combinations can change state across study/context. It should be used as conditionality evidence, not cleaned away by selecting the first or last row.

Current-deposit category bounds after retaining those six conflicts:

- florivore (`n=159` unique coded units): attractive `35–36`, repellent `9`, no response `114–115`
- pollinator (`n=105` unique coded units): attractive `32–37`, repellent `7`, no response `61–66`

The published florivore denominator (`159`) is compatible with the current deposit if the single `+/0` repeat is resolved as no response. The published pollinator denominator (`112`) and repellent count (`9`) cannot be recovered from the current S1 by any resolution of the five `+/0` conflicts. Therefore the current deposited S1 and the printed Table 2 behavioral source universe are not identical.

No single reconstructed behavioral grand effect is promoted as the module's main quantitative result.

## Shared pollinator/florivore FVOCs and Table 3

Under direct choice coding in the current deposit:

- behavioral FVOCs across the eight focal genera: `99` versus printed total `102`
- FVOCs tested against both functional roles: **`32`**, exactly matching the printed total
- shared attractive recurrence: `9` in the current deposit versus printed total `8`
- shared repellent recurrence: **`1`**, matching the printed total

No tested denominator rule reproduces every printed genus-level count and total simultaneously.

The printed Table 3 also contains an internal arithmetic issue independent of the current deposit: its genus-level shared-attractive cells sum to `7`, while the printed total is `8`. Consequently, significance based on one chosen shared-attraction count is source-version sensitive and must not be treated as a definitive threshold result.

The defensible statement is directional: **shared attraction is recurrent, shared repulsion is rarer, but the exact shared-attraction count is source-version dependent.**

## Gate C adjudication

### PASS criterion satisfied

Sasidharan 2023 is admitted as:

`quantitative_deposited_synthesis_reanalysis_with_source_discrepancy`

It is independent of the antagonist-pressure/larceny module and targets a different trait-mediated mechanism layer. It has:

- source-audited numerical response data;
- a conservatively reconstructed 32-study dependence structure;
- a quantitative current-deposit physiological endpoint;
- leave-one-study-component-out influence analysis;
- explicit behavior-state heterogeneity;
- explicit source-version uncertainty rather than forced reconciliation.

The machine-readable canonical adjudication is `PASS_AS_DEPOSITED_REANALYSIS`. The older DOI-first `publication_dependence` block produced by `reconstruct_sasidharan2023_fvoc.py` is retained only as a low-level **noncanonical legacy diagnostic** because it splits citation variants into 34 clusters. Canonical dependence comes from `audit_sasidharan2023_citation_topology.py`, which recovers 32 study components.

### What this PASS does not mean

Gate C passing does **not** mean all Gates A–H pass, and it does not unfreeze manuscript reconstruction by itself.

## Allowed claims

1. In the current deposited synthesis, physiological detection was more frequent among assembled florivore tests than pollinator tests by about `12.9` percentage points.
2. That assembled contrast remained positive after removing each of the 32 recovered study components individually.
3. The contrast is not established as a within-study role effect; paired both-role detection data are sparse and show no difference in the three available paired components.
4. Behavioral responses are context dependent: six repeated FVOC-insect-role units switch between attraction and no response across studies.
5. Thirty-two genus-specific FVOCs with behavioral coding are shared across pollinator and florivore testing in the current deposit, matching the article's printed shared total.
6. Shared attraction is recurrent and shared repulsion is rarer, while the exact attractive count is source-version/table dependent.

## Prohibited claims

Do not claim that:

- florivores universally or causally detect floral volatiles more strongly than pollinators;
- the `+12.9` percentage-point difference estimates a bita model parameter;
- the deposited test-unit proportions are prevalence in nature;
- Sasidharan estimates the direct `A x D` interaction or `W_AD`;
- the behavior counts form an exact reproducible grand effect across the published and current deposited versions;
- a single Table 3 shared-attraction `P` value is definitive;
- the 32 studies are independent primary replications of one homogeneous biological effect.

## Reproducibility

Canonical audit code on the PR branch:

- `scripts/audit_sasidharan2023_pmc_supplement.py`
- `scripts/audit_sasidharan2023_s1_domains.py`
- `scripts/audit_sasidharan2023_citation_topology.py`
- `scripts/reconstruct_sasidharan2023_fvoc.py`
- `scripts/adjudicate_sasidharan2023_gate_c.py`
- `.github/workflows/audit-sasidharan2023-pmc-supplement.yml`

Successful canonical workflow validation:

- validated head: `ab969f510c35a35e6baceb7a99e62b6e7d5c28dd`
- workflow run: `31485414190`
- result: `success`
- canonical adjudication: `PASS_AS_DEPOSITED_REANALYSIS`
- artifact: `9098889748`
- artifact ZIP SHA-256: `631f3e2c2063094a6ec6b1052d0c200457a9607be407283827c51d923c4a5164`

The canonical artifact contains five aggregate/schema products, including `sasidharan2023_gate_c_canonical.json`. Literal observation rows and source references are not persisted by the audit scripts.
