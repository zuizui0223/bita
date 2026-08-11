# Reference audit v1 — integrated theory + mechanism-pattern manuscript

## Scope

This audit checks the references actually used by `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md` after the theory+synthesis reconstruction. It separates verified central references from legacy bibliography entries that are no longer cited, and records known metadata corrections before journal-specific formatting.

This file is a submission-quality control record. It does not change scientific results.

## Current in-text reference spine

The integrated manuscript currently relies on the following literature groups:

### Multivariate selection / total cross-trait curvature

- Lande & Arnold (1983)
- Phillips & Arnold (1989)
- Blows & Brooks (2003)

### Pollinator–antagonist interaction modification / ecological motivation

- Herrera et al. (2002)
- Knauer, Bakhtiari & Schiestl (2018)

### Floral defence / nectar chemistry / pollinator-response plausibility

- Strauss et al. (1999)
- Theis & Adler (2012)
- Wright et al. (2013)
- Richardson et al. (2015)
- Stevenson, Nicolson & Wright (2017)

### Quantitative synthesis and direct-interaction anchors

- Leal, Koski, Irwin & Bronstein (2025)
- Sasidharan, Junker, Eilers & Müller (2023)
- Soper Gorden & Adler (2018)

## Verified metadata for central references

The following metadata/DOI identities were checked against publisher, journal, PubMed/PMC, or institutional records during the current audit.

| Reference | Verified bibliographic identity | Audit state |
|---|---|---|
| Lande & Arnold 1983 | *Evolution* 37:1210–1226; DOI `10.2307/2408842` | verified |
| Phillips & Arnold 1989 | *Evolution* 43:1209–1222; DOI `10.2307/2409357` | verified |
| Blows & Brooks 2003 | *The American Naturalist* 162:815–820; DOI `10.1086/378905` | verified |
| Herrera et al. 2002 | *PNAS* 99:16823–16828; DOI `10.1073/pnas.252362799` | verified |
| Knauer et al. 2018 | *Nature Communications* 9:1367; DOI `10.1038/s41467-018-03792-x` | verified |
| Strauss et al. 1999 | *Evolution* 53:1105–1113; DOI `10.1111/j.1558-5646.1999.tb04525.x` | verified |
| Theis & Adler 2012 | *Ecology* 93:430–435; DOI `10.1890/11-0825.1` | verified |
| Wright et al. 2013 | *Science* 339:1202–1204; DOI `10.1126/science.1228806` | verified |
| Richardson et al. 2015 | *Proceedings of the Royal Society B* 282:20142471; DOI `10.1098/rspb.2014.2471` | verified |
| Stevenson et al. 2017 | *Functional Ecology* 31:65–75; DOI `10.1111/1365-2435.12761` | **manuscript bibliography correction required** |
| Leal et al. 2025 | *Ecology* 106(3):e70036; DOI `10.1002/ecy.70036`; authors Laura C. Leal, Matthew H. Koski, Rebecca E. Irwin, Judith L. Bronstein | verified |
| Sasidharan et al. 2023 | *Annals of Botany* 132(1):1–14; DOI `10.1093/aob/mcad064` | verified |
| Soper Gorden & Adler 2018 | *American Journal of Botany* 105(11):1835–1846; DOI `10.1002/ajb2.1182` | verified |

## Known bibliography corrections

### 1. Stevenson et al. entry is wrong in the current draft bibliography

The current manuscript reference list carries:

```text
Stevenson PC, Nicolson SW, Wright GA (2017)
Plant secondary metabolites in nectar: impacts on pollinators and ecological functions.
Annual Review of Entomology 62:117–138.
doi:10.1146/annurev-ento-031616-035013
```

That metadata is not the cited article. The correct identity is:

```text
Stevenson PC, Nicolson SW, Wright GA (2017)
Plant secondary metabolites in nectar: impacts on pollinators and ecological functions.
Functional Ecology 31:65–75.
doi:10.1111/1365-2435.12761
```

This must be corrected before portal submission.

### 2. Armbruster legacy entry is incorrect and unused

The current bibliography contains:

```text
Armbruster WS, Pélabon C, Bolstad GH, Hansen TF (2014)
Floral integration, modularity, and accuracy: distinguishing complex adaptations from genetic constraints.
New Phytologist 204:92–105.
doi:10.1111/nph.12930
```

The DOI `10.1111/nph.12930` belongs to a different *New Phytologist* article. The title `Floral integration, modularity, and accuracy...` corresponds instead to a 2004 Oxford University Press book chapter by Armbruster, Pélabon, Hansen & Mulder.

The integrated manuscript does not cite this legacy entry in the body. The safer action is therefore to **remove it**, not to preserve it by inventing a replacement role.

## Legacy references no longer used in the reconstructed manuscript

Current text search shows the following names only in the reference list, not in the manuscript body. Unless reintroduced by a deliberate text edit, they should be pruned during final bibliography cleanup:

- Armbruster et al. legacy entry described above;
- Fenster et al. (2004);
- Harder & Johnson (2009);
- Krupnick, Weis & Campbell (1999);
- McCall & Irwin (2006);
- Mothershead & Marquis (2000);
- Schiestl & Johnson (2013).

Removing an unused reference is editorial cleanup, not a change to the theory or empirical synthesis.

## Reference-formatting rule for the final pass

Before submission:

1. retain only references actually cited in the canonical manuscript;
2. verify title, authors, year, journal/book, volume/issue, pages/article number, and DOI from a primary/publisher or authoritative bibliographic source;
3. replace abbreviated `et al.` in the reference list only according to the target journal's reference style, not ad hoc;
4. keep in-text `et al.` usage separate from full bibliography-author requirements;
5. ensure every study named in Results/Discussion has a bibliography entry and every bibliography entry has an in-text role;
6. apply *Theoretical Ecology* formatting only after the scientific bibliography is clean.

## Current decision

```text
central reference identities checked:       yes
known metadata errors found:                2 legacy/current entries
known used-reference correction required:  Stevenson et al. 2017
known unused erroneous entry:               Armbruster legacy entry
legacy unused references to prune:          7 entries total (including Armbruster)
reference audit complete for submission:    no — manuscript bibliography still needs the recorded cleanup
```

The reference audit is no longer an open-ended literature search. The remaining work is a bounded bibliography edit plus a final citation-to-reference consistency check.
