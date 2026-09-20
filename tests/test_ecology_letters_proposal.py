from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "submission" / "ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_V0.md"
EMAIL = ROOT / "submission" / "ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_EMAIL_V1.md"


def _proposal_words(text: str) -> list[str]:
    marker = "**Provisional title:**"
    after = text.split(marker, 1)[1]
    body = after.split("\n\n", 1)[1].strip()
    body = body.replace("**", "")
    return [token for token in re.split(r"\s+", body) if token]


def test_el_synthesis_proposal_is_within_300_word_limit() -> None:
    text = PROPOSAL.read_text(encoding="utf-8")
    words = _proposal_words(text)
    assert len(words) <= 300
    assert len(words) >= 200


def test_el_synthesis_proposal_contains_required_editorial_elements() -> None:
    text = PROPOSAL.read_text(encoding="utf-8")
    lower = text.lower()
    assert "general routing problem" in lower
    assert "broader ecological principle" in lower
    assert "lead author works on" in lower
    assert "two public network analyses independently recover" in lower
    assert "1,378 bird × plant × site units" in text


def test_el_proposal_email_targets_both_editorial_addresses() -> None:
    text = EMAIL.read_text(encoding="utf-8")
    lower = text.lower()
    assert "ecolets@cefe.cnrs.fr" in text
    assert "ecolets2@cefe.cnrs.fr" in text
    assert "Synthesis proposal" in text
    assert "two public network analyses independently recover" in lower
    assert "Ruiqi Zhang" in text


def test_el_proposal_email_does_not_claim_submission_or_invitation() -> None:
    text = EMAIL.read_text(encoding="utf-8").lower()
    assert "i would like to propose" in text
    assert "we have been invited" not in text
    assert "submitted manuscript" not in text
