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

The new fifth face is Theis & Adler (2012). The publisher abstract states that fragrance, pollination and florivores were manipulated. A contemporaneous *American Scientist* report of the study gives the factorial detail: fragrance enhancement was crossed with repeated beetle removal, and half of the female flowers within each of the four fragrance × beetle combinations received supplemental hand pollination. This is coded as an `A × G × pollination-supplementation` bridge, not as a target pollinator-access toggle, because hand pollination does not create pollinator absence/presence.

The complementary hypercube-face readout additionally records:

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

## Main-promotion checkpoint

The frontier result has now passed focused scientific regression tests and has been promoted on the PR branch into the canonical manuscript and Figure 4:

- Section 4.2 now states the 17-system hypercube-face / design-fragmentation result;
- Section 4.6 adds Theis & Adler 2012 as an `A×G×P_supplementation` bridge and preserves strict treatment-equivalence boundaries;
- Discussion and Conclusions now state that lower-dimensional experimental faces already exist but remain distributed across systems;
- Figure 4 now shows A×D (Kessler), consumer G×P (Egan), and A×G×P-supplementation (Theis) faces above the unchanged Impatiens retrofit;
- the focused bibliography now contains 13 references including Theis & Adler 2012;
- Appendix S1 now points to the 17-system frontier and hypercube-face products.

The one-shot promotion workflow and script removed themselves after the focused suite passed. The promoted bot commit is `c7da4cc8180a5bf87f3d9d892ae8c2caaa13480a`.

## Remaining release gate

Before merge, the promoted state must still pass the normal full CI, submission-scope, canonical package build and figure export on a normal user-authored head. The exact rendered Main/Appendix page counts and page-by-page visual QA must then be refreshed. No merge should occur before those checks are complete.
