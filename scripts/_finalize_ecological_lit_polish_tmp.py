from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / 'manuscript' / 'MANUSCRIPT_THEORETICAL_ECOLOGY.md'
PORTAL = ROOT / 'submission' / 'AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md'
REFTEST = ROOT / 'tests' / 'test_manuscript_references.py'
REFAUDIT = ROOT / 'submission' / 'REFERENCE_AUDIT_V1.md'
LITAUDIT = ROOT / 'docs' / 'LITERATURE_POSITIONING_AUDIT_2026-08-21.md'
FIT = ROOT / 'submission' / 'ECOLOGY_CONCEPTS_SYNTHESIS_FIT_AUDIT.md'


def rep(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected 1, found {n}')
    return text.replace(old, new, 1)

text = MAN.read_text(encoding='utf-8')

# Keep abstract <=250 words while preserving the explicit simplicity message.
text = rep(
    text,
    'The algebra is deliberately elementary: the decomposition is bookkeeping, and its ecological payoff is a one-sided bound—when joint-cost curvature is non-negative, complementarity can occur only where antagonist relief exceeds pollinator interference.',
    'The algebra is deliberately elementary: bookkeeping yields a one-sided bound—under non-negative joint-cost curvature, complementarity requires antagonist relief to exceed pollinator interference.',
    'abstract compression',
)

# Two highest-value missing close precedents.
text = rep(
    text,
    'Non-pollinator agents can impose direct or indirect selection on floral traits, including conflict when antagonists and pollinators share trait preferences (Strauss and Whittall 2006), and attraction and resistance have explicitly been considered as linked targets of pollinator- and herbivore-mediated selection (Adler 2008).',
    'Non-pollinator agents can impose direct or indirect selection on floral traits, including conflict when antagonists and pollinators share trait preferences (Strauss and Whittall 2006), and florivory has been framed explicitly as the intersection of pollination and herbivory because damage to flowers can alter both direct reproduction and pollination pathways (McCall and Irwin 2006). Attraction and resistance have likewise been considered as linked targets of pollinator- and herbivore-mediated selection (Adler 2008).',
    'McCall background',
)
text = rep(
    text,
    'Empirical work further shows that these effects can depend on herbivore identity, feeding mode, visitor identity, and plant state (Rusman et al. 2018), while pollinator-mediated selection itself is well known to vary with antagonists, resources, community context, populations, and years (Sletvold 2019).',
    'Empirical work further shows that these effects can depend on herbivore identity, feeding mode, visitor identity, and plant state (Rusman et al. 2018). A full-factorial manipulation of herbivory and pollination in woodland strawberry further showed that selection on defence- and attraction-related traits depended on the other interaction partner (Egan et al. 2021), while pollinator-mediated selection itself is well known to vary with antagonists, resources, community context, populations, and years (Sletvold 2019).',
    'Egan background',
)
text = rep(
    text,
    'The close literature provides rich mechanisms and conditional predictions, but it does not by itself supply the focal one-sided exclusion rule used here for the local \\(A\\times D\\) fitness curvature under an explicit joint-cost sign premise.',
    'The close literature provides rich mechanisms, factorial manipulations of ecological agents, and conditional predictions, but it does not by itself supply the focal one-sided exclusion rule used here for the local \\(A\\times D\\) fitness curvature under an explicit joint-cost sign premise. In particular, manipulating pollination and herbivory can identify diffuse or conflicting selection on measured traits without constituting a factorial manipulation of the focal attraction and defence traits themselves (Egan et al. 2021).',
    'Egan gap boundary',
)

text = rep(
    text,
    'Earlier work already proposed tissue specificity and inducibility as ways to reduce conflict between defence and pollinator attraction (Kessler and Halitschke 2009), and later integrative and empirical studies show that herbivore-plant-pollinator effects can depend on the identity and mode of the interacting consumers (Lucas-Barbosa 2016; Rusman et al. 2018).',
    'Earlier work already framed florivory as an explicit bridge between pollination and herbivory (McCall and Irwin 2006), proposed tissue specificity and inducibility as ways to reduce conflict between defence and pollinator attraction (Kessler and Halitschke 2009), and showed that herbivore-plant-pollinator effects can depend on the identity and mode of interacting consumers (Lucas-Barbosa 2016; Rusman et al. 2018).',
    'McCall discussion',
)
text = rep(
    text,
    'This interpretation is consistent with long-standing evidence that pollinator-mediated selection varies with antagonists, resources, community context, populations, and years (Sletvold 2019).',
    'This interpretation is consistent with long-standing evidence that pollinator-mediated selection varies with antagonists, resources, community context, populations, and years (Sletvold 2019), and with factorial evidence that the selective effect of one interaction partner can depend on the presence or ecological effect of the other (Egan et al. 2021).',
    'Egan discussion',
)

# References: Egan after Catford, McCall after Lucas-Barbosa.
text = rep(
    text,
    'Catford JA, Wilson JRU, Pyšek P, Hulme PE, Duncan RP (2022) Addressing context dependence in ecology. *Trends in Ecology & Evolution* 37:158–170. https://doi.org/10.1016/j.tree.2021.09.007\n\nHaas-Desmarais',
    'Catford JA, Wilson JRU, Pyšek P, Hulme PE, Duncan RP (2022) Addressing context dependence in ecology. *Trends in Ecology & Evolution* 37:158–170. https://doi.org/10.1016/j.tree.2021.09.007\n\nEgan PA, Muola A, Parachnowitsch AL, Stenberg JA (2021) Pollinators and herbivores interactively shape selection on strawberry defence and attraction. *Evolution Letters* 5:636–643. https://doi.org/10.1002/evl3.262\n\nHaas-Desmarais',
    'Egan reference',
)
text = rep(
    text,
    'Lucas-Barbosa D (2016) Integrating studies on plant-pollinator and plant-herbivore interactions. *Trends in Plant Science* 21:125–133. https://doi.org/10.1016/j.tplants.2015.10.013\n\nPage',
    'Lucas-Barbosa D (2016) Integrating studies on plant-pollinator and plant-herbivore interactions. *Trends in Plant Science* 21:125–133. https://doi.org/10.1016/j.tplants.2015.10.013\n\nMcCall AC, Irwin RE (2006) Florivory: the intersection of pollination and herbivory. *Ecology Letters* 9:1351–1365. https://doi.org/10.1111/j.1461-0248.2006.00975.x\n\nPage',
    'McCall reference',
)
MAN.write_text(text, encoding='utf-8')

# Sync portal abstract.
portal = PORTAL.read_text(encoding='utf-8')
abstract = text.split('## Abstract\n\n', 1)[1].split('\n\n**Keywords:**', 1)[0].strip()
before, rest = portal.split('### Abstract\n\n', 1)
_, after = rest.split('\n\n### Keywords', 1)
PORTAL.write_text(before + '### Abstract\n\n' + abstract + '\n\n### Keywords' + after, encoding='utf-8')

# Reference tests.
r = REFTEST.read_text(encoding='utf-8')
r = r.replace('        "McCall AC, Irwin RE",\n', '')
r = r.replace(
    '        "10.1093/oso/9780198570851.003.0007",\n',
    '        "10.1093/oso/9780198570851.003.0007",\n        "10.1111/j.1461-0248.2006.00975.x",\n        "10.1002/evl3.262",\n',
)
r = r.replace(
    '        "Sletvold 2019": "Sletvold N (2019)",\n',
    '        "Sletvold 2019": "Sletvold N (2019)",\n        "McCall and Irwin 2006": "McCall AC, Irwin RE (2006)",\n        "Egan et al. 2021": "Egan PA, Muola A, Parachnowitsch AL, Stenberg JA (2021)",\n',
)
r = r.replace('assert len(entries) == 29', 'assert len(entries) == 31')
REFTEST.write_text(r, encoding='utf-8')

# Reference audit: update live counts and remove McCall from legacy-pruned list.
a = REFAUDIT.read_text(encoding='utf-8')
a = a.replace('**29 bibliography entries**', '**31 bibliography entries**')
a = a.replace('exactly **29** bibliography entries', 'exactly **31** bibliography entries')
a = a.replace('Eight close conceptual/context references were added', 'Ten close conceptual/context references were added')
a = a.replace('Adler (2008), Catford et al. (2022), Johnson et al. (2015), Kessler & Halitschke (2009), Lucas-Barbosa (2016), Rusman et al. (2018), Sletvold (2019), and Strauss & Whittall (2006).', 'Adler (2008), Catford et al. (2022), Egan et al. (2021), Johnson et al. (2015), Kessler & Halitschke (2009), Lucas-Barbosa (2016), McCall & Irwin (2006), Rusman et al. (2018), Sletvold (2019), and Strauss & Whittall (2006).')
a = a.replace('- McCall & Irwin (2006)\n', '')
REFAUDIT.write_text(a, encoding='utf-8')

# Targeted audit: record why these two are high-value close precedents.
la = LITAUDIT.read_text(encoding='utf-8')
if '## 6. Final close-precedent additions' not in la:
    la += '''\n\n## 6. Final close-precedent additions\n\nTwo further sources were added after a second targeted search:\n\n- McCall & Irwin (2006) explicitly framed florivory as the intersection of pollination and herbivory, including direct reproductive damage, indirect pollination pathways, and application of plant-defence theory to flowers. It is therefore foundational prior art for the biological problem, not evidence for the present one-sided theorem.\n- Egan et al. (2021) used a full-factorial manipulation of herbivory and pollination to quantify interactive selection on defence- and attraction-related traits. This is a particularly close empirical precedent. Its manipulated factors are ecological agents, however, rather than a factorial manipulation of one focal attraction trait and one focal defence trait; it therefore sharpens rather than closes the present `A × D` identification gap.\n\nNo further broad Pattern search was opened. The audit remains a manuscript-positioning exercise.\n'''
    LITAUDIT.write_text(la, encoding='utf-8')

fit = FIT.read_text(encoding='utf-8')
if 'McCall & Irwin (2006)' not in fit:
    fit += '\nFinal close-precedent check also added McCall & Irwin (2006) and Egan et al. (2021); the latter is explicitly distinguished as a factorial manipulation of ecological agents rather than the focal attraction × defence trait interaction.\n'
    FIT.write_text(fit, encoding='utf-8')
