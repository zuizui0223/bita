"""Render and validate the relative-route-cost OpenSCAD scaffold."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


EXPECTED = {
    "body": [50.0, 50.0, 21.5],
    "sleeve_6mm": [3.4, 3.4, 6.0],
    "reservoir": [8.0, 8.0, 8.4],
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _render(openscad: str, cad: Path, out: Path, definitions: list[str]) -> str:
    cmd = [openscad, "-o", str(out)]
    for definition in definitions:
        cmd.extend(["-D", definition])
    cmd.append(str(cad))
    completed = subprocess.run(cmd, check=False, text=True, capture_output=True)
    log = (completed.stdout or "") + (completed.stderr or "")
    if completed.returncode != 0:
        raise RuntimeError(f"OpenSCAD render failed: {log}")
    if not out.is_file() or out.stat().st_size == 0:
        raise RuntimeError("OpenSCAD produced no STL")
    return log


def validate(cad: Path, receipt: Path, *, openscad: str = "openscad") -> dict[str, object]:
    import trimesh

    frozen = json.loads(receipt.read_text(encoding="utf-8"))
    cad_sha = _sha256(cad)
    if cad_sha != frozen["cad_sha256"]:
        raise ValueError(
            f"CAD SHA256 drift: expected {frozen['cad_sha256']}, got {cad_sha}"
        )

    version = subprocess.run(
        [openscad, "--version"], check=False, text=True, capture_output=True
    )
    version_text = ((version.stdout or "") + (version.stderr or "")).strip()

    specs = {
        "body": ['part="body"'],
        "sleeve_6mm": ['part="sleeve"', "sleeve_length=6"],
        "reservoir": ['part="reservoir"'],
    }
    results: dict[str, object] = {}
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, definitions in specs.items():
            stl = root / f"{name}.stl"
            log = _render(openscad, cad, stl, definitions)
            mesh = trimesh.load(stl, force="mesh")
            extents = [float(value) for value in mesh.extents]
            components = len(mesh.split(only_watertight=False))
            expected = EXPECTED[name]
            if not mesh.is_watertight:
                raise ValueError(f"{name} mesh is not watertight")
            if components != 1:
                raise ValueError(f"{name} has {components} connected components")
            if any(abs(obs - exp) > 0.05 for obs, exp in zip(extents, expected)):
                raise ValueError(
                    f"{name} extents drift: expected {expected}, got {extents}"
                )
            results[name] = {
                "watertight": bool(mesh.is_watertight),
                "connected_components": components,
                "extents_mm": extents,
                "stl_bytes": stl.stat().st_size,
                "openscad_log_contains_simple_yes": "Simple:        yes" in log,
            }

    return {
        "analysis_name": "relative_route_cost_cad_render_validation",
        "cad_file": str(cad),
        "cad_sha256": cad_sha,
        "openscad_version": version_text,
        "renders": results,
        "passes": True,
        "claim_boundary": (
            "Rendering validates CAD topology and dimensions only; printed parts still "
            "require Stage -1 measurement and bench QC."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cad")
    parser.add_argument("receipt")
    parser.add_argument("output")
    parser.add_argument("--openscad", default="openscad")
    args = parser.parse_args()
    result = validate(Path(args.cad), Path(args.receipt), openscad=args.openscad)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
