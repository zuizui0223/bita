"""Recompute a secondary, source-locked trait-integration pattern in real cichlids.

The data are 88 published African cichlid species with oral/lower-pharyngeal
jaw shape PC1..PC5 and ecological metadata, from Conith & Albertson (2021).
This is NOT a measurement of BITA's shared-world fitness cost, conflict load,
evolutionary origins, or evolutionary accessibility. Do not mix with the
540 entirely hypothetical BITA scenario cells.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import urllib.request
from collections import Counter
from pathlib import Path

SOURCE_REPOSITORY = "andrewjohnconith/cichlid_OJPJ"
SOURCE_COMMIT = "575a148a6c6cb90ee957d4290cf3e2d141ca9c14"
INPUTS = {
    "oral": {
        "path": "MacroevolutionSetUp/MacroDataLOJ_Mean_20210518.csv",
        "blob_sha1": "c47c60c655a8cef745cb14cca261449a873913a4",
        "bytes": 8653,
    },
    "pharyngeal": {
        "path": "MacroevolutionSetUp/MacroDataLPJ_Mean_20210518.csv",
        "blob_sha1": "d733f122b0b7db0590a9215e200b90502ff24403",
        "bytes": 8661,
    },
}
TRAITS = tuple(f"PC{k}" for k in range(1, 6))
METADATA = ("TaxaID", "Clade", "Lake", "Diet")
EXPECTED_TAXA = 88
DEFAULT_OUTPUT = Path("artifacts/bita_cichlid_public_integration_v1.json")


def verify_blob(label: str, data: bytes) -> None:
    expected = INPUTS[label]
    if len(data) != expected["bytes"]:
        raise ValueError(f"{label} source length mismatch")
    blob = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()
    if blob != expected["blob_sha1"]:
        raise ValueError(f"{label} source blob mismatch")


def load_rows(label: str, data: bytes) -> list[dict]:
    verify_blob(label, data)
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=None))
    if reader.fieldnames != [*METADATA, *TRAITS]:
        raise ValueError(f"{label} source header drift: {reader.fieldnames}")
    parsed = []
    seen = set()
    for row in reader:
        taxon = row["TaxaID"]
        if not taxon or taxon in seen:
            raise ValueError(f"{label} duplicate or missing TaxaID")
        seen.add(taxon)
        scores = [float(row[key]) for key in TRAITS]
        if not all(math.isfinite(x) for x in scores):
            raise ValueError(f"{label} non-finite PC score")
        parsed.append({
            "TaxaID": taxon,
            "Clade": row["Clade"],
            "Lake": row["Lake"],
            "Diet": row["Diet"],
            "pc": scores,
        })
    if len(parsed) != EXPECTED_TAXA:
        raise ValueError(f"{label} taxon-count drift: {len(parsed)}")
    return parsed


def source_url(label: str) -> str:
    path = INPUTS[label]["path"]
    return f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{SOURCE_COMMIT}/{path}"


def fetch_source(label: str) -> bytes:
    req = urllib.request.Request(source_url(label), headers={"User-Agent": "bita-public-empirical-audit/1.0"})
    with urllib.request.urlopen(req, timeout=40) as response:
        data = response.read(100_000)
    verify_blob(label, data)
    return data


def join_inputs(oral_rows: list[dict], pharyngeal_rows: list[dict]) -> list[dict]:
    opposing = {row["TaxaID"]: row for row in pharyngeal_rows}
    if {row["TaxaID"] for row in oral_rows} != set(opposing):
        raise ValueError("oral/pharyngeal species IDs do not match")
    joined = []
    for row in oral_rows:  # Preserve source row order for seeded permutation.
        other = opposing[row["TaxaID"]]
        if any(row[field] != other[field] for field in METADATA):
            raise ValueError("source ecology metadata mismatch between modules")
        joined.append({
            "clade": row["Clade"],
            "diet": row["Diet"],
            "oral": row["pc"],
            "pharyngeal": other["pc"],
        })
    return joined


def residualized_matrix(data: list[dict], axis: str, k: int) -> list[list[float]]:
    """Equal-standardize source PC axes then subtract *coarse clade* means.

    Not a phylogenetic covariance model or raw morphological performance assay.
    """
    n = len(data)
    result = [row[axis][:k].copy() for row in data]
    for j in range(k):
        mean = sum(row[j] for row in result) / n
        sd = math.sqrt(sum((row[j]-mean)**2 for row in result)/(n-1))
        if sd <= 0:
            raise ValueError(f"{axis} zero-variance PC")
        for row in result:
            row[j] = (row[j]-mean)/sd
    clades = list(dict.fromkeys(row["clade"] for row in data))
    for clade in clades:
        idx = [i for i, row in enumerate(data) if row["clade"] == clade]
        for j in range(k):
            mean = sum(result[i][j] for i in idx)/len(idx)
            for i in idx:
                result[i][j] -= mean
    return result


def rv_coefficient(x: list[list[float]], y: list[list[float]]) -> float:
    if len(x) != len(y) or not x or len(x[0]) != len(y[0]):
        raise ValueError("mismatched module arrays")
    k = len(x[0])
    xx = [[0.0]*k for _ in range(k)]
    yy = [[0.0]*k for _ in range(k)]
    xy = [[0.0]*k for _ in range(k)]
    for xr, yr in zip(x, y):
        for a in range(k):
            for b in range(k):
                xx[a][b] += xr[a]*xr[b]
                yy[a][b] += yr[a]*yr[b]
                xy[a][b] += xr[a]*yr[b]
    ss = lambda m: sum(v*v for r in m for v in r)
    return ss(xy)/math.sqrt(ss(xx)*ss(yy))


def permuted_rv(data: list[dict], k: int, *, permutations: int = 4999, seed: int = 987654321) -> dict:
    """Coarse-clade-restricted species-label permutation, *not* phylogenetic PGLS."""
    if permutations <= 0:
        raise ValueError("permutations must be positive")
    x = residualized_matrix(data, "oral", k)
    y = residualized_matrix(data, "pharyngeal", k)
    obs = rv_coefficient(x, y)
    groups = [
        [i for i, row in enumerate(data) if row["clade"] == clade]
        for clade in dict.fromkeys(row["clade"] for row in data)
    ]
    state = seed & 0xFFFFFFFF
    exceeds, scores = 0, []
    for _ in range(permutations):
        indices = list(range(len(data)))
        for group in groups:
            shuffled = group.copy()
            for j in range(len(shuffled)-1, 0, -1):
                state = (state*1664525+1013904223) & 0xFFFFFFFF
                selected = int((state/4294967296)*(j+1))
                shuffled[j], shuffled[selected] = shuffled[selected], shuffled[j]
            for a, b in zip(group, shuffled):
                indices[a] = b
        null = rv_coefficient(x, [y[i] for i in indices])
        scores.append(null)
        if null >= obs-1e-12:
            exceeds += 1
    scores.sort()
    return {
        "pc_axes": k,
        "rv": obs,
        "permutations": permutations,
        "permutation_p": (exceeds+1)/(permutations+1),
        "null_rv_mean": sum(scores)/permutations,
        "null_rv_q95": scores[int(.95*permutations)],
    }



def diet_r2(matrix: list[list[float]], diet_labels: list[str]) -> float:
    """Among-diet fraction of variance in coarse-clade-demeaned jaw PCs."""
    if len(matrix) != len(diet_labels) or not matrix:
        raise ValueError("diet trait array mismatch")
    denominator = sum(v*v for row in matrix for v in row)
    if denominator <= 0:
        raise ValueError("zero residual jaw variance")
    groups: dict[str, list[int]] = {}
    for i, diet in enumerate(diet_labels):
        groups.setdefault(diet, []).append(i)
    explained = 0.0
    for idx in groups.values():
        for j in range(len(matrix[0])):
            mean = sum(matrix[i][j] for i in idx)/len(idx)
            explained += len(idx)*mean*mean
    return explained/denominator


def diet_permuted(
    data: list[dict], k: int, module: str, *,
    permutations: int = 4999, seed: int = 2468101213,
) -> dict:
    """Exploratory diet labels permuted within coarse source clades."""
    if permutations <= 0:
        raise ValueError("permutations must be positive")
    mat = residualized_matrix(data, module, k)
    diet = [r["diet"] for r in data]
    obs = diet_r2(mat, diet)
    groups = [
        [i for i, row in enumerate(data) if row["clade"] == clade]
        for clade in dict.fromkeys(row["clade"] for row in data)
    ]
    state = seed & 0xFFFFFFFF
    exceeds, null_scores = 0, []
    for _ in range(permutations):
        shuffled_labels = diet.copy()
        for clade_idx in groups:
            within = [diet[i] for i in clade_idx]
            for j in range(len(within)-1, 0, -1):
                state = (state*1664525+1013904223) & 0xFFFFFFFF
                swap = int((state/4294967296)*(j+1))
                within[j], within[swap] = within[swap], within[j]
            for i, label in zip(clade_idx, within):
                shuffled_labels[i] = label
        value = diet_r2(mat, shuffled_labels)
        null_scores.append(value)
        if value >= obs-1e-12:
            exceeds += 1
    null_scores.sort()
    return {
        "pc_axes": k,
        "jaw_module": module,
        "r2_ecology": obs,
        "permutations": permutations,
        "permutation_p": (exceeds+1)/(permutations+1),
        "null_r2_mean": sum(null_scores)/permutations,
        "null_r2_q95": null_scores[int(.95*permutations)],
    }


def analyze(oral: bytes, pharyngeal: bytes) -> dict:
    pairs = join_inputs(load_rows("oral", oral), load_rows("pharyngeal", pharyngeal))
    return {
        "analysis": "BITA_CICHLID_RESIDUAL_MODULE_INTEGRATION_V1",
        "data_level": "REAL_PUBLIC_SPECIES_TRAIT_DATA",
        "source_paper": "Conith & Albertson (2021), Nature Communications, DOI 10.1038/s41467-021-25755-5",
        "source_repo": SOURCE_REPOSITORY,
        "pinned_commit": SOURCE_COMMIT,
        "source_files": INPUTS,
        "n_species": len(pairs),
        "source_diet_counts": dict(sorted(Counter(r["diet"] for r in pairs).items())),
        "source_clade_counts": dict(sorted(Counter(r["clade"] for r in pairs).items())),
        "assay": "RV between separately derived jaw-PC score matrices, globally standardized per PC and demeaned by coarse source clade; 4999 pharyngeal-label permutations within source clades",
        "results": [permuted_rv(pairs, k) for k in (3, 5)],
        "diet_associations": [
            diet_permuted(pairs, k, module)
            for k in (3, 5) for module in ("oral", "pharyngeal")
        ],
        "claim_limit": (
            "Residual cross-module covariance across 88 sampled species is an "
            "observational integration signature, not an estimated trade-off "
            "strength, functional independence, evolutionary cause, origin of "
            "jaw decoupling, or test of the BITA activation cost. Clade-stratified "
            "permutation is not a phylogenetic comparative model. Diet classes "
            "are source-coded and covary with clade, so diet R-squared is not "
            "causal selection or an empirical BITA conflict-strength estimate."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    results = analyze(fetch_source("oral"), fetch_source("pharyngeal"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(results, sort_keys=True))


if __name__ == "__main__":
    main()
