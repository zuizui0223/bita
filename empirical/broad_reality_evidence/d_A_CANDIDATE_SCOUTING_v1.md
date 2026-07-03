# d_A candidate scouting v1 (unverified leads for the sign-conflict resolution)

## What this is

B5 ranks `d_A` (attraction -> floral antagonism) as the top-priority arrow: its two
current anchors disagree on sign and it has the highest regime leverage. This file
is a scouting pass to feed that arrow with real candidate studies, so the
`pollination_generalization` moderator (and a second independent cluster) can be
coded per `D_A_MODERATOR_CODING_PROTOCOL_v1.md`.

## Honesty boundary (read first)

These are **unverified candidate leads**, not effects and not verified direction
records. Each row carries only:

- a source (DOI/PMID/URL),
- the direction reported **at the abstract level**, and
- the pollinator-breadth context as reported.

No effect size, no verified sign, and no final moderator level is asserted here.
A candidate enters `d_A_moderator_coding_queue.csv` only after a human resolves its
DOI, extracts a direct `A -> floral antagonism` estimate with a denominator and
uncertainty, confirms the trait is an independent attraction predictor (not a
treatment contrast), and codes the moderator level with a cited basis. This
follows the repository rule that query membership or abstract co-mention is never
an effect.

## Candidates

See `d_A_candidate_scouting_v1.csv`. Highlights:

- **Schiestl et al. 2015, eLife (`10.7554/eLife.07641`), Brassica rapa.** Selection
  lines: floral scent and nectar increase *both* pollinator visitation and hawkmoth
  (herbivore) oviposition. A direct, manipulative `d_A > 0` candidate on a
  generalized (bee + moth) system. Strongest single lead.
- **Caruso, Eisen, Martin & Sletvold 2019, Evolution (`10.1111/evo.13639`).**
  Meta-analysis of agents of selection on floral traits. **Caveat (see
  `docs/PART_B_CRITICAL_APPRAISAL_v1.md` L4):** its effect metric is a *selection
  gradient* (β), which is not a `trait -> antagonism` effect. Use it only to
  identify candidate **systems** (via its Dryad database), then extract the marginal
  `d_A` estimate from each primary study. Never enter a selection gradient as a
  `d_A` effect.
- **Geographic conflicting selection, pollinators vs seed predators (PMID
  27325896).** Floral exsertion increases seed predation, and the strength varies
  across populations -- a built-in moderator contrast.
- **Trollius ranunculoides, PLoS One (`10.1371/journal.pone.0118299`).** Explicitly
  generalized pollination; useful as a `generalized`-level anchor once an
  antagonism outcome is confirmed.

## Reproducible source resolution (C3)

`scripts/resolve_d_a_candidate_sources.py` (module
`trait_architecture/d_a_source_resolver.py`, CI
`.github/workflows/resolve-d-a-candidate-sources.yml`) resolves each candidate to a
DOI — directly, via NCBI id-conversion for `pmid:`/PMC leads, or a DOI embedded in
a `url:` — then resolves that DOI against the public Crossref API and writes a
deterministic access receipt (does the DOI resolve, is a full-text link advertised,
is a dataset linked). It is access/relation metadata only — no article text, no
effect. On the current table **6 of 8 leads resolve to a full-text link**
(declared DOIs: Schiestl 2015, Caruso 2019, Trollius; id-converted: the PMID
seed-predation study and the two PMC leads Parnassia, Aerides); the two remaining
plain-URL leads (Phlox, Iris) are honestly `unresolvable` and need a DOI. This
makes the "which leads are reachable" step reproducible in CI, so the only manual
work left is the verified numeric extraction itself.

## How this advances B3

Target: two independent clusters at each `pollination_generalization` level.
Generalized-level leads (Brassica rapa, Trollius, plus the existing Impatiens
anchor pending coding) and more specialized systems (the existing Gymnadenia
anchor, plus Caruso-mined clusters) can populate both levels. Once coded, rerun
`scripts/run_part_b_support.py` with the queue; the
`d_A_display_stronger_where_pollination_generalized` contrast moves from
`insufficient_levels` to a verdict.

## Provenance

Scouted 2026-07-03 via web search on floral-attraction/florivory and
agents-of-selection literature. Sources:
[Schiestl 2015 eLife](https://elifesciences.org/articles/07641),
[Caruso 2019 Evolution](https://onlinelibrary.wiley.com/doi/abs/10.1111/evo.13639),
[Moreira 2019 Ecology](https://esajournals.onlinelibrary.wiley.com/doi/full/10.1002/ecy.2707),
[conflicting selection seed predators (PubMed)](https://pubmed.ncbi.nlm.nih.gov/27325896/),
[Phlox hirsuta (Ann Bot)](https://academic.oup.com/aob/article/113/5/887/160290),
[Trollius ranunculoides (PLoS One)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118299),
[Parnassia wightiana (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11442331/).
