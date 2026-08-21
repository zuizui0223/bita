"""Recover the published Parachnowitsch et al. 2019 supplementary sources.

The URLs are the exact Supplementary Material links exposed by the Oxford
Academic article page for doi:10.1093/aob/mcy132. The XLSX is exported losslessly
to CSV worksheets; the PPTX containing the supplementary figures is retained as
published. No biological interpretation or row reclassification occurs here.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

SIGNED_XLSX_URL = (
    "https://oup.silverchair-cdn.com/oup/backfile/Content_public/Journal/aob/123/2/"
    "10.1093_aob_mcy132/1/mcy132_suppl_aob-18212-s03.xlsx?Expires=2147483647&"
    "Key-Pair-Id=APKAIE5G5CRDK6RD3PGA&Signature="
    "vIOnArA5H-nmURmExZ9oYZxnMrRiy6FvTGXvCYSZD4ZKIovcaFKlW0Z-tu31EHL4gABZF7hPHV2mZYmqLyeEJzSpvZh8Qtdlmly7ZHIghp-I8AkXPEadFRHxtUbTEgWCPA46z653E7M80D5KebFHYKkMQ5LZn02apkAJx4HC9mx~PycHfJHngsnZe9jNu9qprw3yiXlqoybRlmXAN4qkTXu6F12tYJIl5WwB37sPPwrSUOq60mJi-gRhWvTsTsxXzgsq5WSrSQaSiUvnwBE76CmFPxyprCpHPdo~C30WYUEdyRuk35lx86oURQKRF2kgSNPwXE9jk9-guwjETBiNlA__"
)
SIGNED_PPTX_URL = (
    "https://oup.silverchair-cdn.com/oup/backfile/Content_public/Journal/aob/123/2/"
    "10.1093_aob_mcy132/1/mcy132_suppl_aob-18212-s01.pptx?Expires=2147483647&"
    "Key-Pair-Id=APKAIE5G5CRDK6RD3PGA&Signature="
    "R~OxPCFgPETW5gMNvDQt450CGLSIdxLOe8j8ev5B6Ruat7TSNFNbE1spf~spOx1Tfp5xW7IF0Sa23aBvKQA2II~KtyNDVnkn8A4tLmNfV6nNDDlMBDTmH1KhMGkyiMTRFSvfzbEnHibo8bNw24DUdCpNIa5oGJbTJrw6Y7Rr0vW5cUhjiCaHhGkCMu16g76a4prnpbhKtsmrgSHjX4qay0SPVNFZq~N5ozZwU6ZiY4CpRZaheOlbdWvZU88KE8vhi4a6t-~DBdAeJL1EqqlEJH0gZmTNqYVN5m7pELqb5D-tp3y3ajho1jgH2~Y3KyiEh74KifGqiO0yD81QMMEnpg__"
)
ARTICLE_URL = "https://academic.oup.com/aob/article/123/2/247/5055672"


def _load_recovery_module():
    script_path = Path(__file__).with_name("recover_parachnowitsch2019_supplement.py")
    spec = importlib.util.spec_from_file_location("parachnowitsch_recovery", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pptx_inventory(payload: bytes) -> dict[str, int]:
    path_names: list[str]
    from io import BytesIO
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        path_names = archive.namelist()
    return {
        "slides": sum(
            name.startswith("ppt/slides/slide") and name.endswith(".xml")
            for name in path_names
        ),
        "charts": sum(
            name.startswith("ppt/charts/chart") and name.endswith(".xml")
            for name in path_names
        ),
        "embedded_workbooks": sum(name.startswith("ppt/embeddings/") for name in path_names),
        "media_files": sum(name.startswith("ppt/media/") for name in path_names),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    module = _load_recovery_module()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    xlsx_payload = module._request(SIGNED_XLSX_URL, referer=ARTICLE_URL)
    if xlsx_payload[:2] != b"PK":
        preview = xlsx_payload[:300].decode("utf-8", errors="replace")
        raise RuntimeError(f"Signed XLSX response is not a ZIP package: {preview!r}")

    xlsx_path = output_dir / "parachnowitsch2019_supplement_s3.xlsx"
    xlsx_path.write_bytes(xlsx_payload)
    inventory = module.export_workbook(xlsx_path, output_dir)
    module._write_inventory(output_dir / "workbook_inventory.csv", inventory)

    pptx_payload = module._request(SIGNED_PPTX_URL, referer=ARTICLE_URL)
    if pptx_payload[:2] != b"PK":
        preview = pptx_payload[:300].decode("utf-8", errors="replace")
        raise RuntimeError(f"Signed PPTX response is not a ZIP package: {preview!r}")
    pptx_path = output_dir / "parachnowitsch2019_supplement_s1.pptx"
    pptx_path.write_bytes(pptx_payload)
    pptx_inventory = _pptx_inventory(pptx_payload)

    receipt = {
        "article_doi": "10.1093/aob/mcy132",
        "article_title": "Evolutionary ecology of nectar",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_link_basis": "Oxford Academic supplementary-material links",
        "xlsx": {
            "filename": xlsx_path.name,
            "sha256": hashlib.sha256(xlsx_payload).hexdigest(),
            "bytes": len(xlsx_payload),
            "sheet_count": len(inventory),
        },
        "pptx": {
            "filename": pptx_path.name,
            "sha256": hashlib.sha256(pptx_payload).hexdigest(),
            "bytes": len(pptx_payload),
            **pptx_inventory,
        },
        "interpretation_boundary": (
            "The published sources are preserved without reclassification. Every study row "
            "must still pass the project's B-role, outcome-lane, effect-metric, orientation, "
            "and independence gates before quantitative use."
        ),
    }
    (output_dir / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
