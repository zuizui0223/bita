"""Export a non-frozen prototype STL bundle from the route-cost OpenSCAD scaffold."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

CAD_DEFAULT = Path("hardware/relative_route_cost_flower_v1.scad")

def _sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def _render(openscad: str, cad: Path, output: Path, definitions: list[str]) -> None:
    cmd=[openscad,"-o",str(output)]
    for definition in definitions:
        cmd.extend(["-D",definition])
    cmd.append(str(cad))
    completed=subprocess.run(cmd,check=False,text=True,capture_output=True)
    if completed.returncode!=0:
        raise RuntimeError(
            f"OpenSCAD failed for {output.name}: "
            + ((completed.stdout or "")+(completed.stderr or ""))
        )
    if not output.is_file() or output.stat().st_size==0:
        raise RuntimeError(f"missing/empty STL: {output}")

def export_bundle(
    cad: str|Path,
    output_dir: str|Path,
    *,
    openscad: str="openscad",
) -> dict[str,object]:
    cad=Path(cad)
    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=True)
    files:list[dict[str,object]]=[]

    fixed=[
        ("flower_body.stl",['part="body"'],4,"flower_body"),
        ("route_shutter.stl",['part="shutter"'],8,"route_isolation_shutter"),
        ("reward_cartridge.stl",['part="reservoir"'],8,"shared_reward_cartridge"),
    ]
    for name,defs,qty,role in fixed:
        path=out/name
        _render(openscad,cad,path,defs)
        files.append({
            "file":name,
            "role":role,
            "recommended_print_quantity":qty,
            "sha256":_sha256(path),
            "bytes":path.stat().st_size,
        })

    for length in range(2,11):
        name=f"guided_sleeve_{length:02d}mm.stl"
        path=out/name
        _render(openscad,cad,path,['part="sleeve"',f"sleeve_length={length}"])
        files.append({
            "file":name,
            "role":"guided_sleeve",
            "guided_sleeve_length_mm":length,
            "recommended_print_quantity":2,
            "sha256":_sha256(path),
            "bytes":path.stat().st_size,
        })

    marker=out/"PROTOTYPE_ONLY_NOT_FROZEN.txt"
    marker.write_text(
        "These STL files are engineering prototypes only.\n"
        "Physical dimensions must be measured into the module manifest.\n"
        "Stage -1 bench QC and Stage 0 biological calibration remain required.\n",
        encoding="utf-8",
    )

    manifest={
        "schema":"BITA_RELATIVE_ROUTE_COST_PROTOTYPE_BUNDLE_V1",
        "status":"ENGINEERING_PROTOTYPE_ONLY_NOT_FROZEN",
        "cad_file":str(cad),
        "cad_sha256":_sha256(cad),
        "parts":files,
        "part_file_count":len(files),
        "total_recommended_print_quantity":sum(
            int(item["recommended_print_quantity"]) for item in files
        ),
        "next_gate":(
            "Print parts, assign physical module IDs, measure them into the module "
            "manifest, and pass Stage -1 bench QC before bee exposure."
        ),
    }
    manifest_path=out/"prototype_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8"
    )
    return manifest

def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("output_dir")
    parser.add_argument("--cad",default=str(CAD_DEFAULT))
    parser.add_argument("--openscad",default="openscad")
    args=parser.parse_args()
    print(json.dumps(export_bundle(args.cad,args.output_dir,openscad=args.openscad),indent=2,sort_keys=True))

if __name__=="__main__":
    main()
