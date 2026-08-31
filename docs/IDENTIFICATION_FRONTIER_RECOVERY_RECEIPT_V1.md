# Identification-frontier recovery receipt v1

## Scientific result

A **17-system candidate frontier** is retained separately from the current 16-system canonical manuscript coverage. The candidate frontier adds Theis & Adler (2012) as a source-audited structural bridge without silently promoting the canonical manuscript, Figure 4, or submission package.

Candidate screened-set occupancy:

```text
direct A×D-like trait-factorial anchor:             1/17
consumer-factorial anchor:                          1/17
randomized-context A×D anchor:                      1/17
selective-D system anchor:                          1/17
A×antagonist-removal×pollination-supplement bridge: 1/17
m0_delta characterized:                             0/17
independent kappa assay:                            0/17
full allocation closure:                            0/17
```

The five leading modules are carried by five different studies. The candidate interpretation is therefore **design fragmentation**: relevant experimental information exists, but on orthogonal study backbones.

The new fifth face is Theis & Adler (2012). The source audit supports fragrance enhancement crossed with beetle removal and supplemental hand pollination. This is coded as an `A × G × P_supplementation` bridge, not as a target pollinator-access toggle, because hand pollination does not create pollinator absence/presence.

The complementary hypercube-face readout records:

```text
A×D-like face                          Kessler et al. 2008
A×G×pollination-supplementation face  Theis & Adler 2012
D×G×pollination-supplementation face  Santangelo et al. 2019
G×P consumer-factorial backbone       Egan et al. 2021
observed A/D + randomized context     Soper Gorden & Adler 2018
selective-D mechanism                 Sun & Huang 2015
```

These are structural faces, not equivalent treatments and not a scalar study ranking.

## Conditional partial-identification boundary

The frontier product retains the older source-rounded Kessler probability-scale sensitivity (`Delta_AD = +0.19 to +0.25`) only as provenance. The canonical post-PR-153 result is stronger and authoritative: registered aggregate restrictions identify `A1` as positive while `A0` remains narrowly zero-compatible, so Level 1 has a strong aggregate anchor whereas Level 2/3 remain unresolved under source/design uncertainty. No candidate-frontier product may overwrite that hierarchy.

## Canonical promotion state

The 17-system frontier is **not yet promoted** into the canonical manuscript or Figure 4. Files are deliberately separated as:

```text
HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv = current canonical 16-system coverage
HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv = 17-system candidate frontier
```

The candidate generators and focused tests consume V2. Existing manuscript/Figure builders continue to consume V1 until a dedicated promotion PR updates all reader-facing surfaces and target-journal packages together.

## Promotion gate

Promotion requires all of the following in one later PR:

1. preserve the Level-1 / Level-2 / Level-3 outcome hierarchy;
2. preserve the registered Kessler A0/A1 partial-identification result;
3. update manuscript, Figure 4, supplement, references and package text from 16 to 17 systems;
4. identify Theis & Adler only as `A × G × pollination-supplementation`, never as a selective P-access design;
5. rebuild the Theoretical Ecology package and pass full CI.

Until those gates pass, the 17-system result is a validated candidate frontier rather than the canonical submission count.
