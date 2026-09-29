"""Generate blocked confirmatory condition schedules for the route-cost experiment."""
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

CONDITIONS = ["LL", "HL", "LH", "HH"]
BLOCKS = 10
SEED = 20260929


def _read_bees(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("bee file is empty")
    required = {"bee_id", "colony_id"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"missing bee columns: {sorted(missing)}")
    ids = [str(row["bee_id"]).strip() for row in rows]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("bee_id values must be nonblank and unique")
    return rows


def generate_schedule(
    bees: list[dict[str, str]],
    *,
    seed: int = SEED,
) -> list[dict[str, object]]:
    rng = random.Random(seed)
    out: list[dict[str, object]] = []
    global_order = 0
    for bee_index, row in enumerate(bees):
        bee = str(row["bee_id"]).strip()
        colony = str(row["colony_id"]).strip()
        if not colony:
            raise ValueError("colony_id is required")
        familiarization_first = "legitimate" if bee_index % 2 == 0 else "bypass"
        for block in range(1, BLOCKS + 1):
            order = list(CONDITIONS)
            rng.shuffle(order)
            for within_block, condition in enumerate(order, start=1):
                global_order += 1
                out.append(
                    {
                        "bee_id": bee,
                        "colony_id": colony,
                        "block": block,
                        "within_block_order": within_block,
                        "planned_condition": condition,
                        "familiarization_first_route": familiarization_first,
                        "global_schedule_row": global_order,
                    }
                )
    return out


def run(bee_csv: str | Path, output_csv: str | Path, *, seed: int = SEED) -> int:
    rows = generate_schedule(_read_bees(bee_csv), seed=seed)
    path = Path(output_csv)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "bee_id",
        "colony_id",
        "block",
        "within_block_order",
        "planned_condition",
        "familiarization_first_route",
        "global_schedule_row",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bee_csv")
    parser.add_argument("output_csv")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(run(args.bee_csv, args.output_csv, seed=args.seed))
