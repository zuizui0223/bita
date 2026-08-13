from __future__ import annotations
import argparse,csv,json
from dataclasses import asdict
from pathlib import Path
from trait_architecture.model import ModelParameters

ROOT=Path(__file__).resolve().parents[1]
SYN=ROOT/"empirical"/"mechanism_pattern_synthesis"
BASE=("MASTER_LEDGER_V1.csv","LEDGER_BATCH_2_V1.csv","LEDGER_BATCH_3_V1.csv","LEDGER_BATCH_4_V1.csv","LEDGER_BATCH_5_V1.csv")

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

def s1():
    cfg=json.loads((ROOT/"configs"/"part_i_robustness_grid.json").read_text())
    rows=[]
    for k,v in asdict(ModelParameters()).items():
        rows.append({"record_type":"model_parameter","group":"baseline_default","id":"baseline","parameter":k,"value":v,"note":"qualitative scaffold; not empirically calibrated"})
    for sc in cfg["parameter_scenarios"]:
        for k,v in sc.get("overrides",{}).items(): rows.append({"record_type":"scenario_override","group":"parameter_scenario","id":sc["scenario_id"],"parameter":k,"value":v,"note":"declared finite sensitivity scenario"})
    for f in cfg["functional_forms"]:
        for k in ("attraction_saturation","defence_saturation","joint_cost_curvature"): rows.append({"record_type":"response_shape","group":"functional_form","id":f["form_id"],"parameter":k,"value":f[k],"note":"endpoint-normalized on A,D in [0,1]"})
    for k,v in cfg["phenotype_and_regime_grid"].items(): rows.append({"record_type":"finite_grid","group":"coordinate_grid","id":"endpoint_normalized_grid_v2","parameter":k,"value":";".join(map(str,v)),"note":"unweighted declared grid; not prevalence"})
    rows.append({"record_type":"numerical_rule","group":"tolerance","id":"endpoint_normalized_grid_v2","parameter":"neutral_tolerance","value":cfg["neutral_tolerance"],"note":"absolute numerical zero tolerance"})
    return rows

def s2(path):
    rows=read(path,True)
    if len(rows)!=162: raise ValueError(f"S2 expected 162 cases, found {len(rows)}")
    return rows

def s3():
    rows=[]
    for name in BASE:
        rows += [{"source_file":name,**r} for r in read(SYN/name)]
    for p in sorted(SYN.glob("EXPANSION_LEDGER_BATCH_*_V1.csv")):
        rows += [{"source_file":p.name,**r} for r in read(p,True)]
    if len(rows)!=56: raise ValueError(f"S3 expected 56 records, found {len(rows)}")
    if len({r["independence_cluster"] for r in rows if r.get("independence_cluster")})!=25: raise ValueError("S3 independent-cluster count drift")
    return rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("full_summary",type=Path); ap.add_argument("outdir",type=Path); a=ap.parse_args()
    write(a.outdir/"TABLE_S1_PARAMETERS_AND_SCALING.csv",s1())
    write(a.outdir/"TABLE_S2_LOCAL_CASES.csv",s2(a.full_summary))
    write(a.outdir/"TABLE_S3_MECHANISM_PATTERN_LEDGER.csv",s3())
    print("wrote Supplementary Tables S1-S3")
if __name__=="__main__": main()
