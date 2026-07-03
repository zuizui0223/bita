"""Screen the registered eLife scent/reward d_A XML source.

Usage:
    python scripts/screen_d_a_elife_xml.py \
      artifacts/d_a_elife_source_probe/d_a_elife_source_probe.csv \
      artifacts/d_a_elife_xml_screen

Output is a locator for manual C4 reading, not an extracted effect.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.d_a_elife_screen import read_xml_receipt, screen_receipt, write_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("probe_csv")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)
    report = write_outputs(args.out_dir, [screen_receipt(read_xml_receipt(args.probe_csv))])
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
