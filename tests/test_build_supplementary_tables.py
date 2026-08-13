from __future__ import annotations
import csv,importlib.util,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/"scripts"/"run_part_i_robustness.py"; CONFIG=ROOT/"configs"/"part_i_robustness_grid.json"

def load(name):
    path=ROOT/"scripts"/name; spec=importlib.util.spec_from_file_location(name,path); assert spec and spec.loader; m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def summary(tmp):
    out=tmp/"part_i"; subprocess.run([sys.executable,str(RUNNER),str(CONFIG),str(out)],cwd=ROOT,check=True); return out/"part_i_full_tested_set_summary.csv"

def rows(path):
    with path.open(newline="",encoding="utf-8") as h: return list(csv.DictReader(h))

def test_s1_s3_contracts(tmp_path):
    m=load("build_supplementary_tables_s1_s3.py"); out=tmp_path/"tables"; m.write(out/"TABLE_S1_PARAMETERS_AND_SCALING.csv",m.s1()); m.write(out/"TABLE_S2_LOCAL_CASES.csv",m.s2(summary(tmp_path))); m.write(out/"TABLE_S3_MECHANISM_PATTERN_LEDGER.csv",m.s3())
    assert len(rows(out/"TABLE_S2_LOCAL_CASES.csv"))==162
    s3=rows(out/"TABLE_S3_MECHANISM_PATTERN_LEDGER.csv"); assert len(s3)==56; assert len({r["independence_cluster"] for r in s3})==25
    assert {r["record_type"] for r in rows(out/"TABLE_S1_PARAMETERS_AND_SCALING.csv")} >= {"model_parameter","scenario_override","response_shape","finite_grid","numerical_rule"}

def test_s4_s6_contracts(tmp_path):
    m=load("build_supplementary_tables_s4_s6.py"); out=tmp_path/"tables"; m.write(out/"TABLE_S4_CONDITIONALITY_AND_CONTEXT.csv",m.s4()); m.write(out/"TABLE_S5_DIRECT_IDENTIFICATION_AUDITS.csv",m.s5()); m.write(out/"TABLE_S6_PATTERN_EXPANSION_SCREENING.csv",m.s6())
    s4=rows(out/"TABLE_S4_CONDITIONALITY_AND_CONTEXT.csv"); assert len({r["study_or_system"] for r in s4 if r["record_type"]=="sign_switch"})==17; assert sum(r["record_type"]=="context_program" for r in s4)==7
    s5=rows(out/"TABLE_S5_DIRECT_IDENTIFICATION_AUDITS.csv"); assert any(r["audit_family"]=="direct_AxD" and "verified" in r["status_or_result"] for r in s5); assert not any(r["audit_family"]=="direct_joint_cost" and r["decision"]=="Direct_joint_cost" for r in s5)
    s6=rows(out/"TABLE_S6_PATTERN_EXPANSION_SCREENING.csv"); assert {"B8","B9"} <= {r["batch_id"] for r in s6}; assert not any(r["batch_id"] in {"B8","B9"} and r["new_admissible_pattern_class"].lower()=="true" for r in s6)
