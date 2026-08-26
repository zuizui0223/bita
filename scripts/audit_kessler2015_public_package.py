"""Inventory the public eLife supplementary package for Kessler et al. 2015.

The audit answers a narrow reproducibility question: does the publisher-hosted
additional-files ZIP contain machine-readable numeric/source-data candidates
that could support a new uncertainty-bearing factorial reconstruction?

The script records filenames, sizes and coarse file classes only. It does not
infer that image/PDF supplements contain recoverable numeric data.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from collections import Counter
from pathlib import Path


MACHINE_EXTENSIONS = {
    ".csv", ".tsv", ".xls", ".xlsx", ".ods", ".json", ".rds", ".rdata",
    ".sav", ".dta", ".mat", ".npz", ".npy", ".txt",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".svg", ".eps"}
DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".rtf"}


def classify(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix in MACHINE_EXTENSIONS:
        return "machine_readable_candidate"
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in DOCUMENT_EXTENSIONS:
        return "document"
    return "other"


def audit(zip_path: Path) -> dict[str, object]:
    with zipfile.ZipFile(zip_path) as archive:
        files = []
        for item in archive.infolist():
            if item.is_dir():
                continue
            file_class = classify(item.filename)
            files.append({
                "path": item.filename,
                "bytes": item.file_size,
                "extension": Path(item.filename).suffix.lower(),
                "file_class": file_class,
            })
    counts = Counter(item["file_class"] for item in files)
    machine = [item for item in files if item["file_class"] == "machine_readable_candidate"]
    return {
        "analysis_id": "kessler_2015_public_package_inventory_v1",
        "study_doi": "10.7554/eLife.07641",
        "package_url": "https://cdn.elifesciences.org/articles/07641/elife-07641-supp-v1.zip",
        "file_count": len(files),
        "class_counts": dict(sorted(counts.items())),
        "machine_readable_candidate_count": len(machine),
        "machine_readable_candidates": machine,
        "files": files,
        "interpretation_rule": (
            "A zero candidate count supports only the claim that the publisher ZIP lacks obvious machine-readable source-data files. "
            "It does not prove that no numeric values could be digitized from figures, and it does not repair the invalid-D or missing-consumer-toggle identification gates."
        ),
    }


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Kessler et al. 2015 public-package inventory v1",
        "",
        "Source: eLife `10.7554/eLife.07641`, publisher-hosted all-additional-files ZIP.",
        "",
        f"Files: **{report['file_count']}**; obvious machine-readable candidates: **{report['machine_readable_candidate_count']}**.",
        "",
        "## Files",
        "",
        "| path | bytes | class |",
        "|---|---:|---|",
    ]
    for item in report["files"]:  # type: ignore[index]
        lines.append(f"| `{item['path']}` | {item['bytes']} | {item['file_class']} |")
    lines += [
        "",
        "## Identification interpretation",
        "",
        str(report["interpretation_rule"]),
        "",
        "Even if a machine-readable file is present, the study remains a strict identification near miss unless the second phenotype axis is independently justified as antagonist-reducing D and the required consumer/baseline/joint-cost gates are met.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("out_md", type=Path)
    args = parser.parse_args(argv)
    report = audit(args.zip_path)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    args.out_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"file_count": report["file_count"], "machine_candidates": report["machine_readable_candidate_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
