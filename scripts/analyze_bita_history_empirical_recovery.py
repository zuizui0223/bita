"""Reanalyze published endpoint counts, not raw growth or a hysteresis experiment.

Source: Nasvall & Abdalaal 2026, doi:10.1093/g3journal/jkag167, experiment 2.
Production uses only the standard library. All-started populations are denominators.
"""
from __future__ import annotations

import argparse
import csv
import json
from math import comb, exp, log, sqrt
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = Path('empirical/trait_architecture_history')
Z = NormalDist().inv_cdf(.975)


def _count(x: int, n: int) -> None:
    if type(x) is not int or type(n) is not int or n <= 0 or not 0 <= x <= n:
        raise ValueError('integer count 0 <= x <= positive n is required')


def wilson(x: int, n: int) -> tuple[float, float]:
    """Wilson score 95% interval for a single binomial endpoint probability."""
    _count(x, n)
    p = x / n
    den = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / den
    half = Z * sqrt(p * (1-p) / n + Z * Z / (4*n*n)) / den
    return max(0., centre-half), min(1., centre+half)


def fisher_two_sided(a: int, n1: int, b: int, n0: int) -> float:
    """Two-sided probability-ordering Fisher test; integer weights avoid ties."""
    _count(a, n1)
    _count(b, n0)
    successes = a+b
    denominator = comb(n1+n0, successes)
    observed_weight = comb(n1, a) * comb(n0, b)
    numerator = 0
    for x in range(max(0, successes-n0), min(n1, successes)+1):
        weight = comb(n1, x) * comb(n0, successes-x)
        if weight <= observed_weight:
            numerator += weight
    return numerator / denominator


def contrast(a: int, n1: int, b: int, n0: int) -> dict:
    """Difference and RR of endpoint proportions, not continuous-time rates."""
    _count(a, n1)
    _count(b, n0)
    p, q = a/n1, b/n0
    lo1, hi1 = wilson(a, n1)
    lo0, hi0 = wilson(b, n0)
    delta = p-q
    dci = [delta-sqrt((p-lo1)**2+(hi0-q)**2),
           delta+sqrt((hi1-p)**2+(q-lo0)**2)]
    if b == 0:
        rr, rci = None, None
        status = 'BOTH_ZERO_UNDEFINED' if a == 0 else 'ZERO_REFERENCE_EVENT_PROBABILITY'
    elif a == 0:
        rr, rci, status = 0., None, 'ZERO_EXPOSED_EVENTS_LOG_CI_UNDEFINED'
    else:
        rr = p/q
        se = sqrt(1/a-1/n1+1/b-1/n0)
        rci = [exp(log(rr)-Z*se), exp(log(rr)+Z*se)]
        status = 'FINITE_LOG_WALD_CI'
    return dict(
        mutator_events=a, mutator_started=n1,
        nonmutator_events=b, nonmutator_started=n0,
        mutator_proportion=p, nonmutator_proportion=q,
        risk_difference=delta, risk_difference_ci95_newcombe=dci,
        risk_ratio=rr, risk_ratio_ci95_log_wald=rci, risk_ratio_status=status,
        fisher_two_sided_p=fisher_two_sided(a, n1, b, n0),
    )


def holm(pvalues: list[float]) -> list[float]:
    """Holm adjusted p values; endpoints share populations and are not pooled."""
    if any(not 0 <= p <= 1 for p in pvalues):
        raise ValueError('p values must be in [0,1]')
    result = [0.] * len(pvalues)
    floor = 0.
    for rank, index in enumerate(sorted(range(len(pvalues)), key=pvalues.__getitem__)):
        floor = max(floor, min(1., pvalues[index]*(len(pvalues)-rank)))
        result[index] = floor
    return result


def load_inputs(root: Path = ROOT) -> tuple[list[dict], dict]:
    with (root/DIRECTORY/'nasvall2026_table1_experiment2.csv').open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    meta = json.loads((root/DIRECTORY/'nasvall2026_experiment2_metadata.json').read_text())
    return rows, meta


def analyze(rows: list[dict], meta: dict) -> dict:
    groups = {}
    if set(meta['groups']) != {'mutator', 'nonmutator'} or meta['experiment'] != 2:
        raise ValueError('wrong experiment or background set')
    for group, expected in meta['groups'].items():
        _count(expected['reported_rescue'], expected['started'])
        groups[group] = dict(started=expected['started'], rescue=0,
                             hisA=0, trpA=0, unresolved=0, no_detected_rescue=0)
    seen, strains = set(), set()
    for row in rows:
        ident, strain = row['population_id'], row['source_strain_id']
        if ident in seen or strain in strains:
            raise ValueError('duplicate population or source strain')
        seen.add(ident)
        strains.add(strain)
        if row['experiment'] != '2' or row['rescue'] != '1':
            raise ValueError('Table 1 extraction must contain experiment 2 rescued endpoints only')
        group = row['background']
        prefix = {'mutator':'2mutS', 'nonmutator':'2mut+'}.get(group)
        if prefix is None or not ident.startswith(prefix):
            raise ValueError('population background does not match source prefix')
        suffix = ident[len(prefix):]
        if not suffix.isdigit() or not 1 <= int(suffix) <= groups[group]['started']:
            raise ValueError('source population identifier is out of range')
        route = row['route']
        if route not in {'hisA', 'trpA', 'UNRESOLVED'}:
            raise ValueError('invalid or missing route; unresolved rescue must be explicit')
        if row['identification'] not in {'WGS', 'Sanger'}:
            raise ValueError('invalid source identification method')
        if row['amplification_state'] not in {'REPORTED_NO_DIVERGENCE','NOT_CODED_AS_ABSENT'}:
            raise ValueError('amplification surveillance must not be inferred')
        groups[group]['rescue'] += 1
        groups[group]['unresolved' if route == 'UNRESOLVED' else route] += 1
    for group, observed in groups.items():
        expected = meta['groups'][group]
        for endpoint in ('rescue', 'hisA', 'trpA', 'unresolved'):
            if observed[endpoint] != expected['reported_'+endpoint]:
                raise ValueError('table counts disagree with reported source aggregate')
        observed['no_detected_rescue'] = observed['started']-observed['rescue']
    m, n = groups['mutator'], groups['nonmutator']
    contrasts = {end:contrast(m[end],m['started'],n[end],n['started'])
                 for end in ('rescue','hisA','trpA')}
    corrected = holm([item['fisher_two_sided_p'] for item in contrasts.values()])
    for item, p in zip(contrasts.values(), corrected):
        item['holm_p_family_three'] = p
    differences = {end:m[end]/m['started']-n[end]/n['started']
                   for end in ('hisA','trpA','unresolved')}
    return dict(
        study_doi=meta['study_doi'], experiment=2,
        data_level=meta['data_level'],
        started_populations=sum(g['started'] for g in groups.values()),
        rescued_table_rows=len(rows), groups=groups, contrasts=contrasts,
        route_risk_difference_decomposition=differences,
        decomposition_is_arithmetic_not_causal_mediation=True,
        new_quantitative_studies=1, pooled_meta_analysis_performed=False,
        empirical_hysteresis_effect_identified=False,
        gene_duplication_prevalence_estimated=False,
        selection_regime_effect_identified=False,
        theoretical_parameters_calibrated=[],
        intervals_assume_independent_populations=True,
        source_url=meta['source_url'],
        claim_boundary=(
            'Exploratory reanalysis of one published experiment: background-associated '
            'physiological rescue and alternative gene-route access. Genetic background '
            'is not matched adaptation history. No K(u), entry or persistence threshold, '
            'genetic hysteresis, biochemical kinetic equivalence, or cross-study regime '
            'causal effect is identified. Table 1 is positive-outcome-selected; all '
            '48 started populations remain in the denominators. Endpoints share populations.'
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    rows, meta = load_inputs(args.root)
    result = analyze(rows, meta)
    dest = args.root/DIRECTORY/'nasvall2026_reanalysis.json'
    dest.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps({'output':str(dest), 'rescue':result['contrasts']['rescue']}, indent=2))


if __name__ == '__main__':
    main()
