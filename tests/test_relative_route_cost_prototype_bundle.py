from __future__ import annotations

from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts'/'export_relative_route_cost_prototype_bundle.py'
WORKFLOW=ROOT/'.github'/'workflows'/'build-relative-route-cost-prototypes.yml'

def test_prototype_export_contract_contains_all_candidate_sleeves() -> None:
    text=SCRIPT.read_text(encoding='utf-8')
    assert 'for length in range(2,11)' in text
    assert 'recommended_print_quantity":2' in text
    assert 'ENGINEERING_PROTOTYPE_ONLY_NOT_FROZEN' in text
    assert 'PROTOTYPE_ONLY_NOT_FROZEN.txt' in text

def test_prototype_workflow_checks_expected_inventory() -> None:
    text=WORKFLOW.read_text(encoding='utf-8')
    assert 'part_file_count"]==12' in text
    assert 'total_recommended_print_quantity"]==38' in text
    assert 'set(range(2,11))' in text
