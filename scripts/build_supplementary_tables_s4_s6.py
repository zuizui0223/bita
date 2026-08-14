from __future__ import annotations
import argparse,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SYN=ROOT/"empirical"/"mechanism_pattern_synthesis"

def read(path,strict=False):
    with path.open(newline="",encoding="utf-8") as h:
        out=[]
        for r in csv.DictReader(h):
            if strict and None in r: raise ValueError(f"overflow {path.name}: {r[None]}")
            out.append({k:str(v or "").strip() for k,v in r.items() if k is not None})
        return out

def write(path,rows):
    if not rows: raise ValueError(f"empty {path.name}")
    fields=[]
    for r in rows:
        for k in r:
            if k not in fields: fields.append(k)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def s4():
    rows=[]; switch_paths=[SYN/"SIGN_SWITCH_LEDGER_V1.csv"]+sorted(SYN.glob("EXPANSION_SIGN_SWITCH_BATCH_*_V1.csv"))
    for p in switch_paths:
        for r in read(p,p.name.startswith("EXPANSION_")):
            rows.append({"record_type":"sign_switch","source_file":p.name,"record_id":r.get("switch_id",""),"study_or_system":r.get("study_id",""),"doi_or_sources":r.get("doi",""),"route_or_context_axis":r.get("route","") or r.get("contrast_axis",""),"contrast_axis":r.get("contrast_axis",""),"level_1":r.get("level_1",""),"state_1":r.get("state_1",""),"level_2":r.get("level_2",""),"state_2":r.get("state_2",""),"interpretation":r.get("interpretation",""),"counted_in_route_N":"not_added_as_separate_route_N"})
    if len({r["study_or_system"] for r in rows if r["study_or_system"]})!=17: raise ValueError("S4 switch-cluster count drift")
    ctx=read(SYN/"EXPANSION_CONTEXT_PROGRAMS_V1.csv",True)
    if len(ctx)!=7: raise ValueError("S4 context-program count drift")
    for r in ctx:
        rows.append({"record_type":"context_program","source_file":"EXPANSION_CONTEXT_PROGRAMS_V1.csv","record_id":r.get("program_id",""),"study_or_system":r.get("system",""),"doi_or_sources":r.get("source_dois",""),"route_or_context_axis":r.get("context_axis",""),"contrast_axis":r.get("pattern_state",""),"level_1":"","state_1":"","level_2":"","state_2":"","interpretation":r.get("admitted_inference",""),"counted_in_route_N":"no"})
    return rows

def s5():
    rows=[]
    for r in read(SYN/"DIRECT_AXD_AUDIT_V1.csv",True): rows.append({"audit_family":"direct_AxD","audit_id":r.get("audit_id",""),"study_id":r.get("study_id",""),"doi":r.get("doi",""),"plant_taxon":r.get("plant_taxon",""),"A_axis":r.get("A_axis",""),"D_axis":r.get("D_axis",""),"candidate_measure":r.get("joint_outcome",""),"status_or_result":r.get("direct_AxD_term_status",""),"decision":r.get("tier_decision",""),"reason":r.get("reason",""),"next_action":r.get("next_action","")})
    for r in read(SYN/"JOINT_COST_AUDIT_V1.csv",True): rows.append({"audit_family":"direct_joint_cost","audit_id":r.get("audit_id",""),"study_id":r.get("study_id",""),"doi":r.get("doi",""),"plant_taxon":r.get("plant_taxon",""),"A_axis":r.get("A_axis",""),"D_axis":r.get("D_axis",""),"candidate_measure":r.get("candidate_cost_evidence",""),"status_or_result":r.get("result",""),"decision":r.get("tier_decision",""),"reason":r.get("reason",""),"next_action":r.get("next_action","")})
    if not any(r["audit_family"]=="direct_AxD" and "verified" in r["status_or_result"] for r in rows): raise ValueError("S5 lost verified direct A×D candidate")
    if any(r["audit_family"]=="direct_joint_cost" and r["decision"]=="Direct_joint_cost" for r in rows): raise ValueError("unexpected direct joint-cost estimate")
    return rows

def s6():
    paths=[SYN/"FIXED_258_PRIORITY_RESCREEN_BATCH_1_V1.csv"]+sorted(SYN.glob("PRIORITY_RESCREEN_BATCH_*_V1.csv")); rows=[]
    for p in paths:
        for r in read(p,True):
            source=r.get("source","") or r.get("source_id","") or r.get("source_or_family",""); doi=r.get("doi","") or r.get("doi_or_locator",""); axis=r.get("pattern_axis","") or r.get("target_axis","") or r.get("current_pattern_value",""); new=r.get("new_admissible_pattern_class","") or ("true" if "NEW_CONTEXT_CLASS" in r.get("decision","") else "not_explicit")
            rows.append({"source_file":p.name,"batch_id":r.get("batch_id",""),"source":source,"doi_or_locator":doi,"plant_system":r.get("plant_system",""),"target_or_pattern_axis":axis,"decision":r.get("decision",""),"new_admissible_pattern_class":new,"reason":r.get("reason","") or r.get("current_pattern_value",""),"next_action":r.get("next_action","")})
    b8=[r for r in rows if r["batch_id"]=="B8"]; b9=[r for r in rows if r["batch_id"]=="B9"]
    if not b8 or not b9 or any(r["new_admissible_pattern_class"].lower()=="true" for r in b8+b9): raise ValueError("S6 stopping condition drift")
    return rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("outdir",type=Path); a=ap.parse_args()
    write(a.outdir/"TABLE_S4_CONDITIONALITY_AND_CONTEXT.csv",s4()); write(a.outdir/"TABLE_S5_DIRECT_IDENTIFICATION_AUDITS.csv",s5()); write(a.outdir/"TABLE_S6_PATTERN_EXPANSION_SCREENING.csv",s6()); print("wrote Supplementary Tables S4-S6")
if __name__=="__main__": main()
