"""Source-bound endpoint recovery; not new experiments or hysteresis estimates."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'scripts/analyze_bita_history_empirical_recovery.py'

@pytest.fixture
def mod():
    assert MODULE.is_file(), 'empirical recovery module is not implemented'
    spec = importlib.util.spec_from_file_location('recovery', MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_source_counts_not_31_as_full_denominator(mod):
    rows, meta = mod.load_inputs(ROOT)
    out = mod.analyze(rows, meta)
    assert out['started_populations'] == 48
    assert out['rescued_table_rows'] == 31
    assert out['groups']['mutator'] == {'started':24, 'rescue':21, 'hisA':9, 'trpA':11, 'unresolved':1, 'no_detected_rescue':3}
    assert out['groups']['nonmutator'] == {'started':24, 'rescue':10, 'hisA':0, 'trpA':10, 'unresolved':0, 'no_detected_rescue':14}

@pytest.mark.parametrize('a,b,p', [(21,10,.0020490192464945366),(9,0,.0015592377596215347),(11,10,1.)])
def test_exact_test_oracle(mod,a,b,p):
    assert mod.fisher_two_sided(a,24,b,24) == pytest.approx(p,abs=1e-14)
    assert mod.fisher_two_sided(b,24,a,24) == pytest.approx(p,abs=1e-14)


def test_ci_and_effect_oracles(mod):
    x = mod.contrast(21,24,10,24)
    assert x['risk_difference'] == pytest.approx(11/24)
    assert x['risk_difference_ci95_newcombe'] == pytest.approx([.18952268341326717,.648681091667503])
    assert x['risk_ratio'] == pytest.approx(2.1)
    assert x['risk_ratio_ci95_log_wald'] == pytest.approx([1.277615914671859,3.4517415988299254])


def test_zero_cells_do_not_receive_pseudocounts(mod):
    x=mod.contrast(9,24,0,24)
    assert x['risk_ratio'] is None
    assert x['risk_ratio_status'] == 'ZERO_REFERENCE_EVENT_PROBABILITY'
    assert x['risk_ratio_ci95_log_wald'] is None
    assert x['risk_difference_ci95_newcombe'] == pytest.approx([.16113307896753942,.5729003755732573])


def test_both_zero_events_and_wilson_boundaries(mod):
    assert mod.fisher_two_sided(0,24,0,24)==1
    assert mod.wilson(0,24)[0] == pytest.approx(0,abs=1e-15)
    assert mod.wilson(24,24)[1] == pytest.approx(1,abs=1e-15)
    x=mod.contrast(0,24,0,24)
    assert x['risk_ratio_status']=='BOTH_ZERO_UNDEFINED'
    assert x['risk_ratio'] is None

@pytest.mark.parametrize('x,n',[(-1,24),(25,24),(0,0),(1.2,24),(True,24)])
def test_invalid_counts_fail_closed(mod,x,n):
    with pytest.raises(ValueError):mod.wilson(x,n)


def test_source_duplicates_rejected(mod):
    rows,meta=mod.load_inputs(ROOT)
    with pytest.raises(ValueError,match='duplicate'):mod.analyze(rows+[rows[0]],meta)


def test_unresolved_is_rescue_not_missing_or_failure(mod):
    rows,meta=mod.load_inputs(ROOT)
    out=mod.analyze(rows,meta)
    assert out['groups']['mutator']['unresolved']==1
    assert sum(out['route_risk_difference_decomposition'].values()) == pytest.approx(out['contrasts']['rescue']['risk_difference'])


def test_invalid_routes_rejected(mod):
    rows,meta=mod.load_inputs(ROOT)
    rows[0]['route']='missing'
    with pytest.raises(ValueError,match='route'):mod.analyze(rows,meta)


def test_reported_total_conflict_fails_closed(mod):
    rows,meta=mod.load_inputs(ROOT)
    meta['groups']['mutator']['reported_rescue']=20
    with pytest.raises(ValueError,match='reported'):mod.analyze(rows,meta)


def test_background_prefix_guard(mod):
    rows,meta=mod.load_inputs(ROOT)
    rows[0]['background']='mutator'
    with pytest.raises(ValueError,match='background'):mod.analyze(rows,meta)


def test_holm_family_is_retained(mod):
    vals=mod.holm([.0020490192464945366,.0015592377596215347,1.])
    assert vals==pytest.approx([.004677713278864604,.004677713278864604,1.])


def test_claims_do_not_promote_accessibility_to_hysteresis(mod):
    rows,meta=mod.load_inputs(ROOT)
    out=mod.analyze(rows,meta)
    assert out['empirical_hysteresis_effect_identified'] is False
    assert out['gene_duplication_prevalence_estimated'] is False
    assert out['pooled_meta_analysis_performed'] is False
    assert out['new_quantitative_studies']==1
    assert 'PUBLISHED_TABLE' in out['data_level']
    json.dumps(out,allow_nan=False)


def test_frozen_json_reproduces(mod):
    path=ROOT/'empirical/trait_architecture_history/nasvall2026_reanalysis.json'
    assert path.is_file()
    rows,meta=mod.load_inputs(ROOT)
    assert json.loads(path.read_text())==mod.analyze(rows,meta)


def test_module_is_implemented():
    assert MODULE.is_file(), 'implementation is absent'


def test_publication_followup_is_not_independent_replication():
    import csv
    path=ROOT/'empirical/trait_architecture_history/publication_dependency_ledger.csv'
    rows=list(csv.DictReader(path.open()))
    assert len(rows)==4
    assert len({r['dependency_family'] for r in rows})==1
    assert rows[0]['programme_id']==rows[1]['programme_id']
    assert all(r['history_matched']=='False' for r in rows)
    assert all(r['bidirectional_test']=='False' for r in rows)


def test_amplification_ascertainment_never_becomes_absence(mod):
    rows,meta=mod.load_inputs(ROOT)
    assert sum(r['amplification_state']=='REPORTED_NO_DIVERGENCE' for r in rows)==1
    assert sum(r['amplification_state']=='NOT_CODED_AS_ABSENT' for r in rows)==30
    assert mod.analyze(rows,meta)['gene_duplication_prevalence_estimated'] is False
