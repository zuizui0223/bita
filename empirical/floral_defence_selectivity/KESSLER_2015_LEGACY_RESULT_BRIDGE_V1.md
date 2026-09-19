# Kessler 2015 legacy-result bridge into the floral-defence selectivity refocus

## Purpose

Preserve the existing Kessler 2015 BITA result while preventing a definition change from silently moving it into the primary narrow floral-defence corpus.

Primary source:

Kessler D, Kallenbach M, Diezel C, Rothe E, Murdock M, Baldwin IT. 2015.
**How scent and nectar influence floral antagonists and mutualists.**
*eLife* 4:e07641. DOI `10.7554/eLife.07641`.

Existing BITA provenance:

- `empirical/mechanism_pattern_synthesis/KESSLER_2015_DIRECT_AXD_ACCESS_LIMITATION_AUDIT_V1.md`
- `empirical/mechanism_pattern_synthesis/KESSLER_2015_FACTORIAL_REAUDIT_V1.md`
- direct A-by-D sign-heterogeneity results retained elsewhere in the repository.

## Why this is a bridge rather than a primary matched-D row

The manipulated nectar axis can be oriented as an antagonist-reducing access restriction because loss of nectar strongly reduces *Manduca sexta* oviposition.

However, nectar itself is also a reward. Nectar absence is therefore not equivalent to a conventional positively expressed defensive trait.

The repository has historically contained both interpretations:

```text
strict conventional-defence reading:
    nectar production / nectar absence is a reward axis
    -> do not silently relabel as D

broad antagonist-reducing access reading:
    nectar absence independently reduces antagonist oviposition
    -> can be used as a D-like access restriction in sensitivity analyses
```

Both are preserved.

## Reusable defence-side information

With nectar restriction oriented as the D-like axis:

```text
higher restriction = SWEET9 / nectar absent
lower restriction  = EV / nectar present
```

the source reports strong reduction of *M. sexta* oviposition when nectar is absent. This licenses the broad-access statement:

> nectar restriction reduces use of the flower by an ovipositing antagonist.

It does not license calling nectar absence a conventional floral defence.

## Reusable pollinator-context switch

The same nectar restriction has different pollination consequences across pollinators.

### Manduca sexta

Under single-species tent pollination:

```text
SWEET9 seed production = 44.6% of EV
P = 0.006
```

Thus nectar restriction carries a supported pollination cost for *M. sexta*.

### Hyles lineata

Under the same four-line architecture:

```text
SWEET9 seed production = 111.69% of EV
P = 0.578
```

The source states that nectar absence does not reduce pollination service by *H. lineata* when scent remains present. Only loss of both scent and nectar strongly reduces seed production.

This is a direct within-system consumer-identity switch in the pollinator-side cost of the same nectar restriction.

## Existing A x D result remains intact

The previous BITA direct-factorial result is not replaced.

Source-mean discrete interactions already recorded in the repository include opposite signs among pollinator contexts. That result remains evidence that direct attraction-by-access/reward interaction is context-dependent.

The new macro-analysis may cite this result as a mechanistic bridge, but it must not count the same publication as a new independent primary matched-D replication.

## Selectivity interpretation

Kessler 2015 therefore supplies a useful sensitivity result:

```text
antagonist-reducing access restriction
+
pollinator identity
->
large pollinator cost in one consumer
but little/no single-axis cost in another
```

This is consistent with BITA's broader claim that selectivity is an interaction property of trait × consumer context, not a fixed property of "chemical" or "physical" defence.

It is not by itself a test of antagonist-versus-pollinator effective-domain separation on one common fitness outcome.

## Analysis status

```text
primary narrow floral-defence corpus: EXCLUDED
broad access-restriction sensitivity: INCLUDED
legacy direct A x D result:           PRESERVED
independent cluster increment:        0
consumer-context switch value:        HIGH
```
