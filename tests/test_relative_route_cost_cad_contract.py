from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAD = ROOT / 'hardware' / 'relative_route_cost_flower_v1.scad'
README = ROOT / 'hardware' / 'RELATIVE_ROUTE_COST_CAD_README_V1.md'

def test_cad_scaffold_preserves_visible_reference_geometry() -> None:
    text = SCAD.read_text(encoding='utf-8')
    assert 'top_disc_d = 50;' in text
    assert 'visible_tube_len = 20;' in text
    assert 'entry_d = 2.5;' in text
    assert 'lateral_entry_below_top = 5;' in text

def test_cad_scaffold_has_shared_reservoir_and_variable_sleeve_modules() -> None:
    text = SCAD.read_text(encoding='utf-8')
    assert 'module flower_body()' in text
    assert 'module sleeve_insert(length_mm=6)' in text
    assert 'module shutter_plug()' in text
    assert 'module reservoir_cartridge()' in text
    assert 'reward_plane_z = 14;' in text
    assert 'length_mm >= 2 && length_mm <= 10' in text

def test_cad_readme_keeps_biological_cost_unfrozen() -> None:
    text = README.read_text(encoding='utf-8')
    assert 'engineering starting point, not a frozen biological manipulation' in text
    assert 'Only the Stage-0 handling-time calibration defines biological route cost' in text
