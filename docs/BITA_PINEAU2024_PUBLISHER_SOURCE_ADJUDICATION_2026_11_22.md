# Pineau (2024): adjudication of duplicated Day40 Fig5A source vectors and publication-grade evidence

**2026-11-22, additive Draft continuation of [PR #382](https://github.com/zuizui0223/bita/pull/382).** This is one original programme, not an extra empirical replicate. The canonical active BITA paper concerns *trait interaction versus ecological mechanism*; the legacy architecture Chapter 2 / SLK provenance is the only potential home for this functional-specialization system. This file changes no manuscript.

## Current decision: retain both exclusions; no publisher-level rescue

Original study: Pineau et al. (2024), *Nature Ecology & Evolution*, [doi:10.1038/s41559-024-02367-y](https://doi.org/10.1038/s41559-024-02367-y); author [data/code repository](https://github.com/Ratcliff-Lab/coexistence-paper), pinned to Git commit `071affa79f16f0a469f099058372a7488c35c0c2`. An author-manuscript listing of a separately attached publisher `Source data` XLSX exists at [PMC11090753](https://pmc.ncbi.nlm.nih.gov/articles/PMC11090753/); **its bytes have not been independently retrieved**.

The following two documented **single-paper official routes** were actually tried by read-only GitHub Actions. Neither yielded a usable second XLSX.

| Provider and attempt | Actual response | Adjudication |
|---|---|---|
| PMC article attachment, `PMC11090753/bin/NIHMS1986110-supplement-Source_data.xlsx` | HTTP **404** | No file bytes or provenance |
| Europe PMC `PMC11090753/supplementaryFiles?includeInlineImage=false` | HTTP response not a valid XLSX or supplementary ZIP (observed **292 and 297 bytes** in separate requests) | Not a second workbook and not an independent recheck |

These observations document what the stated endpoints returned in this audit. The transient error-response body length is deliberately excluded from the frozen reproducibility receipt, while a genuinely downloaded XLSX would retain its content hash and byte size. They **do not establish that no alternative online publisher copy exists**, nor do they establish that the publisher copy is identical to or corrected relative to the author GitHub version. **An accessible, separately deposited publication file remains an unmet source gate.** Do not claim publisher independent confirmation or publisher correction.

The original GitHub author XLSX was reacquired and SHA-verified: Git object `8f7d01b388489374aba210db96495f387d4338e2`, SHA-256 `b6bc44d5085344292b5b33cac81369652b25e56f0947c1057cfc00ae4947057f`, **1,535,384 bytes**. In its `Fig5A` source, **Excel column 6 (Large l1 Day40)** and **column 24 (Small s1 Day40)** have **164 exactly matching original Excel row/area-value pairs**. They also have the same independently derived column-data SHA256: `51cc4ba233b1e248db2a16ceafb794566cf09047de7f1c91b99a30dec00f130f`. The other 40 column hashes are kept in the derived-only audit receipt to support exact future verification; original raw vectors and author workbook are not copied into BITA.

**Correct choice:** Since the true underlying Day40 microscopic measurement identity cannot be assigned to one of these two distinct experimental populations, **quarantine both** as independent Day40 endpoints. Never choose the copy that happens to preserve the larger effect. The R code's references to separate local source image-area files establish *intended* source distinctions but do **not** independently confirm their contents without the actual imaging files.

## Scientific result retained after source correction

| Question | Direct original-source support | Adjudicated strength and denominator |
|---|---|---|
| Forward origin of clearly differentiated Small/Large phenotype populations | Original 715-transfer aerobically evolved PO-1…PO-5 experiment | **3/5** original independently evolving populations with observed phenotypic dimorphism. Descriptive 95% Wilson interval **0.231–0.882**; one publication, no universal origin probability |
| Maintenance of an already evolved specialist pair | PO-4 competition Figure 2 original Excel + author MATLAB code | Standard oxygen: **8** complete competition trajectories, equilibrium `p_L ≈ 0.09255` from an independently re-fitted frequency-change line; supplemental oxygen: **7** source trajectories with mean final Large fraction **0.85645**. Paper caption's high-O₂ `n=6` and Methods' initial `n=5` remain unresolved; competition cultures do not add independent forward origins |
| Reverse size shift when the partner is absent | Original Figure 5 `Fig5A` cluster-area values, author R source, with both Day40 duplicates quarantined | **3 Small** replay populations increase (mean **+9.012 μm**), **2 Large** decrease (mean **−5.976 μm**) from first to Day40. These are five source-adjudicated final trajectories, not the full seven plotted lines |
| Claim that 7 distinct replay lines have independently valid Day40 measurements | **Fails** original-source duplicate audit | Do **not** claim 7/7 or use unfiltered Small mean +14.826 μm / Large mean −8.006 μm as primary |
| Genetic modular division of two previously balanced within-individual functions; independent startup cost `K(u)`; ancestral trade-off allocation | Not observed in Pineau original figure source | **Not identified** |

The source author's published analyses and the new original workbook reconstructions differ in inferential grain: cluster areas are *nested* within populations and times; the selected PO-4 competition assays are *nested* within one already-diverged genotype pair; five original PO evolution populations are the independent forward evolutionary units. No pooled p value or meta-analytic effect should count these strata as separate research programmes.

### Manuscript-ready evidence paragraph for the *historical architecture programme only*

> Independent experimental evolution in snowflake yeast provides a direct example in which a common multicellular ancestor generated divergent growth- and settling-associated phenotypes in three of five aerobically evolved populations (Pineau et al., 2024). The already diverged Small/Large pair showed a source-reproducible, oxygen-dependent frequency response, consistent with resource-mediated maintenance rather than a new origin event. In competitor-removal replay, three source-validated Small populations increased in biomass-weighted mean cluster radius (mean change +9.01 μm) and two Large populations decreased (−5.98 μm). Two additional Day40 endpoints were excluded because the deposited source repeated the same 164 area measurements under distinct population labels; the publisher's separately advertised source-data file could not be independently obtained for adjudication. These results are consistent with ecological maintenance of differentiated phenotypes and return toward intermediate sizes when competitor pressure is removed, but do not identify an ancestral within-individual module split, the independent occurrence rate of a new genetic architecture, or a generalized `K(u)` threshold.

The statement is a **source-bounded within-study integration**, not confirmation of the wider general trait architecture theory or the active BITA trait-interaction mechanism-allocation manuscript.

## Exact reproduction and status

- `scripts/audit_bita_pineau2024_publisher_source.py`: read-only single-article official source download recognition and SHA-verified author-column vector comparison, with an explicit "not retrieved" source grade.
- `tests/test_bita_pineau2024_publisher_source.py`: synthetic named XLSX/ZIP verification, exact cross-population column identity and frozen accessible-source gate.
- `.github/workflows/bita-pineau2024-official-publisher-supplement-source-adjudication.yml`: pinned author source, two official publisher route attempts, no original XLSX committed, only aggregate receipt.
- `empirical/trait_architecture_history/pineau2024_publisher_source_adjudication.json`: frozen machine-auditable publisher-access receipt plus 42 source column SHA-256 digests.
- Prior parent [PR #382](https://github.com/zuizui0223/bita/pull/382) retains the complete source-corrected Fig5A population reanalysis and its tests; its original source and CI gates are green.

The remaining evidence hinge is **independently authenticated l1 Day40 and s1 Day40 raw imaging/area files**, or a publisher original source that differs materially from the GitHub workbook and can be tied to the culture identities. If unavailable, maintain the **3 Small + 2 Large conservative endpoints** as final. Stop repeated slicing of the same published Excel; next substantive generality evidence requires an independently conducted evolution programme with founder-line denominators.

**No edits to canonical manuscript, SLK, any parent scientific code, or main. No merge or external submission.**
