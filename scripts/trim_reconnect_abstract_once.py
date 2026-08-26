from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


text = MAN.read_text(encoding="utf-8")
text = replace_once(
    text,
    "Under these conditions, a simple algebraic identity becomes a diagnostic for the sign of any still-unallocated joint channel rather than a standalone prediction theorem.",
    "The algebra then diagnoses the sign of any still-unallocated joint channel rather than serving as a standalone theorem.",
    "algebra sentence",
)
text = replace_once(
    text,
    "Kessler et al. (2008) provides a rare experimental attraction-by-defence-like trait factorial with a sign-robust positive discrete reproductive interaction under published aggregate constraints, whereas Egan et al. (2021) provides the complementary consumer-factorial structure without an experimentally crossed attraction-by-defence trait pair.",
    "Kessler et al. (2008) supplies a rare attraction-by-defence-like trait factorial, whereas Egan et al. (2021) supplies the complementary consumer factorial without experimentally crossed attraction and defence traits.",
    "existing-study sentence",
)
text = replace_once(
    text,
    "A retained source-adjudicated mechanism-route synthesis shows that the four constituent marginal pathways recur across 56 route records from 25 independent biological clusters; those records establish biological recurrence, not estimates of the channel interactions or total attraction-by-defence interaction.",
    "A retained synthesis shows that all four constituent marginal pathways recur across 56 route records from 25 independent biological clusters; this establishes recurrence, not channel identification.",
    "route recurrence sentence",
)
MAN.write_text(text, encoding="utf-8")
