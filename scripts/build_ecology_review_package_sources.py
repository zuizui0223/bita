from pathlib import Path

import build_ecology_submission_sources as builder


ROOT = Path(__file__).resolve().parents[1]
builder.TABLES = ROOT / "submission" / "ecology" / "ECOLOGY_MAIN_TABLES_COMPACT.md"


def _shorten_review_title_page() -> None:
    path = builder.OUT / "MANUSCRIPT_ECOLOGY_SUBMISSION.md"
    text = path.read_text(encoding="utf-8")
    start = text.index("**Open Research statement:**")
    end = text.index("\n\n**Key words/phrases:**", start)
    statement = (
        "**Open Research statement:** Review-stage analysis code, source-adjudication products, "
        "and machine-readable data products are available at `https://github.com/zuizui0223/bita`. "
        "The exact accepted data/code version will be deposited in a permanent versioned archive "
        "and cited in the final article in accordance with ESA Open Research policy."
    )
    path.write_text(text[:start] + statement + text[end:], encoding="utf-8")


if __name__ == "__main__":
    builder.main()
    _shorten_review_title_page()
