# Reference audit v1 — integrated theory + mechanism-pattern manuscript

## Scope

This audit checks the references actually used by `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md` after the theory+synthesis reconstruction. It records authoritative bibliographic verification, removes obsolete legacy references, and protects known corrections before journal-specific formatting.

This file is a submission-quality control record. It does not change scientific results.

## Current in-text reference spine

The integrated manuscript now retains 13 cited references:

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

- Leal et al. (2025)
- Sasidharan, Junker, Eilers & Müller (2023)
- Soper Gorden & Adler (2018)

## Verified metadata for central references

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
| Stevenson et al. 2017 | *Functional Ecology* 31:65–75; DOI `10.1111/1365-2435.12761` | verified and corrected in manuscript |
| Leal et al. 2025 | *Ecology* 106:e70036; DOI `10.1002/ecy.70036` | verified |
| Sasidharan et al. 2023 | *Annals of Botany* 132:1–14; DOI `10.1093/aob/mcad064` | verified |
| Soper Gorden & Adler 2018 | *American Journal of Botany* 105:1835–1846; DOI `10.1002/ajb2.1182` | verified |

## Corrections applied to the canonical manuscript

### Stevenson et al. 2017

The obsolete draft incorrectly identified the cited paper as an *Annual Review of Entomology* article with DOI `10.1146/annurev-ento-031616-035013`.

The canonical manuscript now carries the verified identity:

```text
Stevenson PC, Nicolson SW, Wright GA (2017)
Plant secondary metabolites in nectar: impacts on pollinators and ecological functions.
Functional Ecology 31:65–75.
doi:10.1111/1365-2435.12761
```

### Armbruster legacy entry

The obsolete bibliography contained an incorrect and uncited Armbruster entry that paired the title `Floral integration, modularity, and accuracy...` with unrelated *New Phytologist* metadata/DOI `10.1111/nph.12930`.

Because the reconstructed manuscript does not cite that source, it was removed rather than reassigned a role.

## Uncited legacy references pruned

The following entries occurred only in the obsolete bibliography and were removed from the canonical manuscript because the reconstructed body does not cite them:

- Armbruster legacy entry;
- Fenster et al. (2004);
- Harder & Johnson (2009);
- Krupnick, Weis & Campbell (1999);
- McCall & Irwin (2006);
- Mothershead & Marquis (2000);
- Schiestl & Johnson (2013).

This is editorial cleanup only; no theory, evidence result, or inference changed.

## Regression protection

`tests/test_manuscript_references.py` protects the known correction state by requiring:

- the verified Stevenson *Functional Ecology* citation and DOI;
- absence of the obsolete Stevenson DOI/journal identity;
- absence of the incorrect Armbruster DOI/title pairing and the six other uncited legacy entries;
- presence of the central quantitative-module and direct-interaction DOIs.

## Remaining reference work

Before portal submission:

1. apply the target journal's exact reference style;
2. decide whether the journal requires full author lists rather than `et al.` in the bibliography;
3. run a final citation-to-reference consistency check after any last wording edit;
4. verify the final PDF/export has not introduced typography or DOI-link errors.

## Current decision

```text
central reference identities checked:      yes
known Stevenson metadata error:            corrected
known Armbruster legacy error:             removed
uncited legacy references:                 pruned
scientific bibliography cleanup:           complete
journal-specific formatting:               still required
final post-edit consistency pass:           still required
```

The reference task is now bounded formatting/consistency work, not additional literature discovery.
