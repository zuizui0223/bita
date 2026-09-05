from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from trait_architecture.dimensional_release import REQUIRED_FIELDS, analyze_dimensional_release


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError("CSV has no data rows")

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(f"blank required field {field!r} on CSV line {i}")
        unit_id = row["unit_id"]
        if unit_id in seen:
            raise ValueError(f"duplicate unit_id {unit_id!r}")
        seen.add(unit_id)
        try:
            float(row["x_measured"])
            float(row["function1_value"])
            float(row["function2_value"])
            float(row["fitness_value"])
        except ValueError as exc:
            raise ValueError(f"invalid numeric value on CSV line {i}") from exc
        if row["y_state"] not in {"0", "1"}:
            raise ValueError(f"y_state must be 0/1 on CSV line {i}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze BITA empirical dimensional release")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("sch_receipt_path", type=Path)
    parser.add_argument("config_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = read_rows(args.csv_path)
    sch_receipt = json.loads(args.sch_receipt_path.read_text(encoding="utf-8"))
    config = json.loads(args.config_path.read_text(encoding="utf-8"))
    result = analyze_dimensional_release(rows, sch_receipt, config)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
