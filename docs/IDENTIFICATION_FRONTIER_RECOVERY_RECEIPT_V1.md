# Identification-frontier recovery receipt v1

## Scientific result

The high-information audit is expanded to **17 systems** and recast from a binary `0/17 full identification` statement into a non-scalar identification frontier.

Fixed screened-set occupancy:

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

The five leading modules are carried by **five different studies**. The interpretation is therefore **design fragmentation**: relevant experimental information exists, but on orthogonal study backbones.

The new fifth face is Theis & Adler (2012). The source audit supports fragrance enhancement crossed with beetle removal and supplemental hand pollination. This is coded as an `A × G × pollination-supplementation` bridge, not as a target pollinator-access toggle, because hand pollination does not create pollinator absence/presence.

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

## Conditional partial-identification recovery

Kessler et al. 2008 has a published rounded probability-scale `Delta_AD` range of `+0.19 to +0.25`. Under the explicit same-scale auxiliary restriction `kappa_delta >= 0`, the accounting identity yields

```text
rho_delta - iota_delta >= +0.19
```

within those aggregate constraints. This is not a confidence bound because the factorial SE/CI is unrecovered, and it is not an empirical estimate of kappa.

## Main promotion state

The frontier result is promoted on the PR branch into the canonical manuscript and Figure 4:

- Abstract now reports **17 screened high-information systems**;
- Section 4.2 names the empirical pattern a **fragmented identification frontier**;
- Section 4.6 adds Theis & Adler 2012 as an `A×G×P_supplementation` bridge and preserves strict treatment-equivalence boundaries;
- Discussion and Conclusions state that lower-dimensional experimental faces already exist but remain distributed across systems;
- Figure 4 shows the complementary experimental faces and 17-system coverage;
- the focused bibliography includes Theis & Adler 2012;
- Appendix S1 points to the 17-system frontier and hypercube-face products.

The one-shot Abstract/Main synchronization surfaces removed themselves after their focused regression suite passed. The latest promotion bot commit is `9c8b4e44db1198a75147984304b9af24bd5ba8f5`.

## Full release gate

This user-authored receipt update exists to trigger the normal repository checks on the promoted state. Merge remains blocked until the same head passes:

1. full CI on Python 3.10 / 3.11 / 3.12;
2. submission-scope;
3. identification candidate package;
4. canonical Ecology package;
5. Fig1–Fig5 EPS export;
6. refreshed Main/Appendix page counts and page-by-page visual QA.

No merge should occur before those checks are complete.
