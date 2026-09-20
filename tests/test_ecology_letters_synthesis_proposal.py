from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "submission" / "ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_V0.md"
EMAIL = ROOT / "submission" / "ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_EMAIL_V1.md"


def _proposal_body(text: str) -> str:
    marker = "**Provisional title:**"
    after = text.split(marker, 1)[1]
    return after.split("\n\n", 1)[1].strip()


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w×–/-]+\b", text, flags=re.UNICODE))


def test_ecology_letters_synthesis_proposal_stays_within_300_words() -> None:
    text = PROPOSAL.read_text(encoding="utf-8")
    body = _proposal_body(text)
    assert _word_count(body) <= 300
    assert "broader ecological principle" in body.lower()
    assert "lead author" in body.lower()


def test_ecology_letters_proposal_email_uses_both_official_addresses() -> None:
    text = EMAIL.read_text(encoding="utf-8")
    assert "ecolets@cefe.cnrs.fr" in text
    assert "ecolets2@cefe.cnrs.fr" in text
    assert "Synthesis proposal" in text
    assert "Access and exposure domains organize floral defence selectivity" in text
