from pathlib import Path

import build_ecology_submission_sources as builder


ROOT = Path(__file__).resolve().parents[1]
builder.TABLES = ROOT / "submission" / "ecology" / "ECOLOGY_MAIN_TABLES_COMPACT.md"


if __name__ == "__main__":
    builder.main()
