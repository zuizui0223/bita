from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"

OLD_KEYWORDS = "**Keywords:** causal identification; floral defence; floral traits; florivory; factorial experiment; pollination; trait interaction"
NEW_KEYWORDS = "**Keywords:** causal identification; factorial experiment; floral defence; floral traits; florivory; pollination; trait interaction"

DISCLOSURE = """### 5.4 Computational and AI-assisted workflow transparency

OpenAI ChatGPT and Anthropic Claude were used for code-generation assistance, structured literature triage, reproducibility checks, and manuscript drafting/editing. AI-generated output was not treated as empirical evidence, and these tools did not determine study inclusion, evidence classification, or statistical conclusions. Source claims, numerical results, code, and citations were checked against the underlying analyses and sources. The authors retain responsibility for all scientific decisions and content.
"""

PORTAL_OLD_KEYWORDS = """- causal identification
- floral defence
- floral traits
- florivory
- factorial experiment
- pollination
- trait interaction"""
PORTAL_NEW_KEYWORDS = """- causal identification
- factorial experiment
- floral defence
- floral traits
- florivory
- pollination
- trait interaction"""

PORTAL_AI_OLD = """### Use of generative AI or language tools

Preserve the final disclosure required by the journal/portal. Authors remain responsible for all claims, citations, code, analyses, and text. Do not infer author approval of disclosure wording."""
PORTAL_AI_NEW = """### Use of generative AI or language tools

Current manuscript disclosure:

> OpenAI ChatGPT and Anthropic Claude were used for code-generation assistance, structured literature triage, reproducibility checks, and manuscript drafting/editing. AI-generated output was not treated as empirical evidence, and these tools did not determine study inclusion, evidence classification, or statistical conclusions. Source claims, numerical results, code, and citations were checked against the underlying analyses and sources. The authors retain responsibility for all scientific decisions and content.

Preserve the disclosure required by the final journal/portal and obtain author approval of the exact submitted wording."""


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    manuscript = MAN.read_text(encoding="utf-8")
    manuscript = replace_once(manuscript, OLD_KEYWORDS, NEW_KEYWORDS, "manuscript keywords")
    if "### 5.4 Computational and AI-assisted workflow transparency" in manuscript:
        raise RuntimeError("AI disclosure already present; one-shot patch should not be rerun")
    marker = "\n\n## 6. Discussion\n"
    manuscript = replace_once(manuscript, marker, "\n\n" + DISCLOSURE + marker, "discussion marker")
    MAN.write_text(manuscript, encoding="utf-8")

    portal = PORTAL.read_text(encoding="utf-8")
    portal = replace_once(portal, PORTAL_OLD_KEYWORDS, PORTAL_NEW_KEYWORDS, "portal keywords")
    portal = replace_once(portal, PORTAL_AI_OLD, PORTAL_AI_NEW, "portal AI disclosure")
    portal = portal.replace("- [ ] keywords are synchronized after final copy edit;", "- [x] keywords are synchronized with the canonical manuscript;")
    PORTAL.write_text(portal, encoding="utf-8")


if __name__ == "__main__":
    main()
