# Targeted Stage-2 cell audit v1

## Purpose

Search only for evidence that can break the current strict Stage-2 bottleneck.

Highest-value missing cells are:

```text
SEPARATED + chemical + direction-supported pollinator state
OVERLAPPED + physical + direction-supported pollinator state
```

These cells matter because the current strict set perfectly confounds domain relation with broad defence modality.

This audit does **not** reopen generic floral-trait literature harvesting.

## Candidate 1 — Nicotiana attenuata benzylacetone linked program

Sources:

- Kessler et al. 2019, *Functional Ecology*, DOI `10.1111/1365-2435.13332`
- Haverkamp et al. 2016, *eLife*, DOI `10.7554/eLife.15039`

Focal trait:

```text
benzylacetone (BA) floral emission
```

Antagonist-side evidence:

```text
BA-emitting flowers deter Diabrotica undecimpunctata establishment and feeding.
BA-silenced CHAL flowers receive more florivore colonization/damage.
```

Pollinator-side evidence:

```text
BA-emitting flowers receive superior Manduca sexta pollination service,
including higher seed production after controlled moth visitation.
```

Architecture is biologically compatible with temporal domain separation:

```text
pre-dusk BA -> florivore deterrence
night BA    -> hawkmoth pollination function
```

### Adjudication

This is highly informative linked-program evidence and a strong bridge to the effective-domain interpretation.

It does **not** enter the frozen strict matched-D count because the antagonist and pollinator outcomes are resolved in different primary papers.

```text
same focal D:                     PASS
same plant biological system:    PASS
direction-supported pollination: PASS
direction-supported antagonism:  PASS
same primary study gate:         FAIL
strict Stage-2 increment:        0
linked-program value:            HIGH
```

Changing the gate now would be outcome-aware protocol drift.

## Candidate 2 — Aloe vryheidensis nectar phenolics

Source:

Johnson, Hargreaves & Brown 2006, *Ecology*, DOI
`10.1890/0012-9658(2006)87[2709:DBNFAA]2.0.CO;2`.

The phenolic-rich bitter nectar acts as a strong visitor filter:

- honey bees and sunbirds strongly reject the nectar;
- short-billed frugivorous/insectivorous birds that are effective pollinators tolerate/use it.

This is excellent susceptibility-based filtering evidence.

### Adjudication

The primary BITA matched-D gate requires an antagonist-reducing role, not simply exclusion of inefficient or mismatched visitors.

The source establishes filtering, but the rejected nectarivores are not cleanly demonstrated as a focal antagonist channel whose suppression provides the D benefit being analysed.

```text
flower-specific chemical filter: PASS
visitor susceptibility split:    PASS
effective pollinator retained:   PASS
strict antagonist-benefit gate:  FAIL / AMBIGUOUS
strict Stage-2 increment:        0
context value:                   HIGH
```

Keep as comparative filter context, not as a post-hoc positive matched-D system.

## Candidate 3 — Petunia hybrida floral volatile bouquet

Source:

Kessler et al. 2013, *Ecology Letters*, DOI `10.1111/ele.12038`.

The study uses transgenic floral-scent lines and shows that individual floral volatile components can reduce generalist florivore damage, while other bouquet components contribute to pollinator attraction.

### Adjudication

The crucial BITA unit is one focal D with both antagonist and pollinator outcomes.

Here the ecological solution is **compound partitioning within the bouquet** rather than one same-D axis:

```text
defensive compounds != pollinator-attracting compound(s)
```

This strongly supports multifunctional bouquet architecture but does not fill the strict same-D Stage-2 cell.

```text
experimental floral trait manipulation: PASS
antagonist defence:                    PASS
pollinator attraction in system:       PASS
same focal D on both sides:            FAIL
strict Stage-2 increment:              0
architecture context value:            HIGH
```

## Re-check of Bejaria resinosa

The existing Bejaria system remains an important physical overlap case.

The source shows that sticky flowers reduce florivory and can trap potentially mutualistic insects, but the paper explicitly treats the direct pollination cost as unresolved / requiring a different experiment.

Therefore it still cannot be promoted to:

```text
OVERLAPPED + physical + direction-supported pollinator impairment
```

without changing the evidence rule.

## Targeted-search result

```text
new strict Stage-2 systems admitted: 0
linked-program evidence added:       1
high-value context systems added:    2
frozen eligibility rule changed:     NO
```

This is scientifically useful because it identifies the bottleneck more sharply:

> the literature contains several compelling dual-function floral systems, but clean same-study evidence that simultaneously closes the antagonist-benefit and pollinator-cost sides for one focal D is genuinely rare.

## Consequence

Do not force a domain-versus-modality model from the current strict set.

The paper should retain:

```text
matched-D strict subset -> descriptive exact evidence
linked programs          -> mechanistic triangulation
within-D switches        -> conditionality evidence
community network        -> independent macro-scale validation
```

Future retrieval should remain targeted to the two missing strict cells rather than broadening the definition of D or weakening the same-study rule.
