from __future__ import annotations

from scripts.validate_relative_route_cost_hardware import validate_hardware

def _manifest() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for i in range(4):
        rows.append({
            "module_id": f"BODY{i+1:03d}",
            "module_type": "body",
            "manufacturing_batch": "B1",
            "geometry_version": "G1",
            "top_disc_diameter_mm": "50.0",
            "visible_tube_length_mm": "20.0",
            "top_aperture_diameter_mm": "2.5",
            "lateral_aperture_diameter_mm": "2.5",
            "lateral_aperture_offset_below_top_mm": "5.0",
            "route": "",
            "insert_effective_distance_mm": "",
            "material": "test",
            "surface_finish": "test",
            "inspection_date": "2026-09-30",
            "dimension_tolerance_pass": "true",
            "notes": "",
        })
    for route, prefix in (("legitimate", "L"), ("bypass", "B")):
        for distance in (2, 3, 4):
            rows.append({
                "module_id": f"{prefix}{distance:03d}",
                "module_type": "insert",
                "manufacturing_batch": "B1",
                "geometry_version": "G1",
                "top_disc_diameter_mm": "",
                "visible_tube_length_mm": "",
                "top_aperture_diameter_mm": "",
                "lateral_aperture_diameter_mm": "",
                "lateral_aperture_offset_below_top_mm": "",
                "route": route,
                "insert_effective_distance_mm": str(float(distance)),
                "material": "test",
                "surface_finish": "test",
                "inspection_date": "2026-09-30",
                "dimension_tolerance_pass": "true",
                "notes": "",
            })
    return rows

def _qc(*, wet: bool = False, loads: int = 20) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for load in range(1, loads + 1):
        rows.append({
            "qc_run_id": "QC1",
            "module_id": "BODY001",
            "legitimate_insert_id": "L002",
            "bypass_insert_id": "B002",
            "reward_volume_ul": "3.0",
            "reward_concentration": "50%",
            "load_number": str(load),
            "delay_to_inspection_s": "10",
            "top_entrance_wet": "true" if wet and load == 1 else "false",
            "lateral_entrance_wet": "false",
            "overflow": "false",
            "cross_route_leakage": "false",
            "shared_reservoir_confirmed": "true",
            "shutter_legitimate_pass": "true",
            "shutter_bypass_pass": "true",
            "external_cue_identity_pass": "true",
            "cleaning_compatibility_pass": "true",
            "notes": "",
        })
    return rows

def test_hardware_bench_qc_passes_clean_assembly() -> None:
    result = validate_hardware(_manifest(), _qc())
    assert result["body_count"] == 4
    assert result["tested_assembly_count"] == 1
    assert result["passes_stage0_hardware_gate"] is True

def test_hardware_bench_qc_fails_any_wetting() -> None:
    result = validate_hardware(_manifest(), _qc(wet=True))
    assert result["passes_stage0_hardware_gate"] is False
    assembly = next(iter(result["assemblies"].values()))
    assert assembly["checks"]["no_entrance_wetting"] is False

def test_hardware_bench_qc_requires_20_loads() -> None:
    result = validate_hardware(_manifest(), _qc(loads=19))
    assert result["passes_stage0_hardware_gate"] is False
    assembly = next(iter(result["assemblies"].values()))
    assert assembly["checks"]["loads_ge_20_with_first_20_present"] is False

def test_hardware_manifest_fails_out_of_tolerance_body() -> None:
    manifest = _manifest()
    manifest[0]["top_disc_diameter_mm"] = "51.0"
    result = validate_hardware(manifest, _qc())
    assert result["passes_stage0_hardware_gate"] is False
    assert "BODY001:top_disc_diameter_mm" in result["manifest_failures"]
