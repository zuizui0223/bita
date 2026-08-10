"""Recover the Parachnowitsch et al. 2019 XLSX from its published signed URL.

The signed URL is the exact Supplementary Material S3 link exposed by the Oxford
Academic article page for doi:10.1093/aob/mcy132. This wrapper reuses the workbook
inventory/export functions in ``recover_parachnowitsch2019_supplement.py`` and
performs no biological interpretation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

SIGNED_XLSX_URL = (
    "https://oup.silverchair-cdn.com/oup/backfile/Content_public/Journal/aob/123/2/"
    "10.1093_aob_mcy132/1/mcy132_suppl_aob-18212-s03.xlsx?Expires=2147483647&"
    "Key-Pair-Id=APKAIE5G5CRDK6RD3PGA&Signature="
    "vIOnArA5H-nmURmExZ9oYZxnMrRiy6FvTGXvCYSZD4ZKIovcaFKlW0Z-tu31EHL4gABZF7hPHV2mZYmqLyeEJzSpvZh8Qtdlmly7ZHIghp-I8AkXPEadFRHxtUbTEgWCPA46z653E7M80D5KebFHYKkMQ5LZn02apkAJx4HC9mx~PycHfJHngsnZe9jNu9qprw3yiXlqoybRlmXAN4qkTXu6F12tYJIl5WwB37sPPwrSUOq60mJi-gRhWvTsTsxXzgsq5WSrSQaSiUvnwBE76CmFPxyprCpHPdo~C30WYUEdyRuk35lx86oURQKRF2kgSNPwXE9jk9-guwjETBiNlA__"
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir")
    args = parser.parse_args(argv)

    module = _load_recovery_module()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    payload = module._request(SIGNED_XLSX_URL, referer=ARTICLE_URL)
    if payload[:2] != b"PK":
        preview = payload[:300].decode("utf-8", errors="replace")
        raise RuntimeError(f"Signed supplement response is not XLSX: {preview!r}")

    xlsx_path = output_dir / "parachnowitsch2019_supplement_s3.xlsx"
    xlsx_path.write_bytes(payload)
    inventory = module.export_workbook(xlsx_path, output_dir)
    module._write_inventory(output_dir / "workbook_inventory.csv", inventory)

    receipt = {
        "article_doi": "10.1093/aob/mcy132",
        "article_title": "Evolutionary ecology of nectar",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_url": SIGNED_XLSX_URL,
        "source_link_basis": "Oxford Academic Supplementary Material S3 link",
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "sheet_count": len(inventory),
        "interpretation_boundary": (
            "The workbook and worksheets are preserved without reclassification. "
            "Every study row must still pass the project's B-role, outcome-lane, "
            "effect-metric, and independence gates before quantitative use."
        ),
    }
    (output_dir / "source_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
