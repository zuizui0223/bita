from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for relative in (
    "manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md",
    "submission/AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md",
):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    old = "Across 16 screened high-information systems"
    new = "Across 17 screened high-information systems"
    if old not in text:
        raise RuntimeError(f"missing 16-system abstract target in {relative}")
    path.write_text(text.replace(old, new), encoding="utf-8")
