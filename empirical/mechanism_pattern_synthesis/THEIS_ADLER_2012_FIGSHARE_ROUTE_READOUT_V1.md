# Theis & Adler (2012) — publisher-linked Figshare route audit

## Source pair

```text
primary article DOI:    10.1890/11-0825.1
publisher-linked DOI:   10.6084/m9.figshare.c.3304428
collection title:       Advertising to the enemy: enhanced floral fragrance increases beetle attraction and reduces plant reproduction
resource DOI reported by Figshare: 10.1890/11-0825.1
```

The publisher explicitly links the Figshare collection as research data pertaining to the article. The collection identity therefore passes the source-linkage gate.

## Public collection contents

A bounded Figshare v2 API audit recovered exactly one child article:

```text
Figshare article id: 3552648
DOI:                10.6084/m9.figshare.3552648.v1
title:              Appendix A. Methods, results, and figure for trapping experiments.
files:              1
file:               appendix-A.htm
file id:            5621076
size:               41,034 bytes
```

No tabular file or raw observation table for the main fragrance × pollination × florivore field experiment is present in the publisher-linked collection.

## Consequence for quantitative reanalysis

The public repository route does **not** support a new raw-data reanalysis of the main experiment. The collection contains a supplementary appendix for trapping experiments, not the observation-level data needed to recompute the focal fragrance effects on florivore attraction, pollinator attraction, or seed production.

Therefore:

```text
main-experiment raw data recovered:       no
new uncertainty-bearing effect extracted: no
Figshare route status:                    closed for main-experiment reanalysis
```

This is an access/data-availability result, not a biological null.

## What the primary article still supports

The source-reported experimental directions remain admissible as Tier-4 directional evidence:

```text
enhanced fragrance -> increased florivore attraction
enhanced fragrance -> no detected increase in pollinator attraction
enhanced fragrance -> decreased seed production
```

The first two directions can be represented in the mechanism ledger without inventing an effect magnitude. The reproductive consequence is retained as same-study context rather than used as a separate route coefficient.

## Evidence classification

```text
A_to_antagonism: source-adjudicated directional experimental evidence (Tier 4)
A_to_pollination: source-adjudicated no-detected-increase state (Tier 4)
same-system multi-route: yes
direct A x D: no
raw-data quantitative promotion: blocked by public collection contents
```

The important negative result is methodological: a publisher label such as “research data pertaining to this article” does not guarantee that the archived object contains the focal experiment's raw data. The synthesis retains the primary source result while refusing to manufacture a numerical effect from a supplementary trapping appendix.
