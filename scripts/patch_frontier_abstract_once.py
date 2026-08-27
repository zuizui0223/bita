from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Keep the manuscript Abstract and the portal Abstract on the same screened-set count.
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

# Name the empirical structure explicitly without turning the screened set into prevalence.
manuscript = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
text = manuscript.read_text(encoding="utf-8")
old = "The empirical pattern is therefore **design fragmentation** rather than absence of relevant biology or experimental competence."
new = "The empirical pattern is therefore a **fragmented identification frontier**: the missing information reflects design fragmentation rather than absence of relevant biology or experimental competence."
if old not in text:
    raise RuntimeError("missing fragmented-frontier promotion target")
manuscript.write_text(text.replace(old, new), encoding="utf-8")
