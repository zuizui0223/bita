from pathlib import Path

import pytest

pytestmark = pytest.mark.prose_contract

ROOT = Path(__file__).resolve().parents[1]
EMAIL = ROOT / "submission" / "THIRD_NETWORK_CAPE_COLLABORATION_EMAIL_V1.md"
PACKET = ROOT / "submission" / "THIRD_NETWORK_CAPE_FIRST_CONTACT_PACKET_V1.md"


def test_cape_first_contact_is_send_ready_but_not_auto_send() -> None:
    email = EMAIL.read_text(encoding="utf-8")
    packet = PACKET.read_text(encoding="utf-8")

    assert "send-ready draft; explicit author send approval still required" in email
    assert "[current affiliation]" not in email
    assert "[email]" not in email
    assert "Graduate School of Agriculture, Kyoto University" in email
    assert "zhang.ruiqi.77h@st.kyoto-u.ac.jp" in email

    assert "steenhuisens@ufs.ac.za" in packet
    assert "jeremy.midgley@uct.ac.za" in packet
    assert "CC" in packet
    assert "none on the first message" in packet
    assert "EXTERNAL_SEND = AUTHOR_APPROVAL_REQUIRED" in packet
    assert "No message has been sent" in packet


def test_first_contact_packet_preserves_outcome_blindness() -> None:
    text = PACKET.read_text(encoding="utf-8")

    for token in (
        ">=5 flowering Protea species",
        ">=5 non-flying mammal species",
        "THIRD_NETWORK_COLLABORATION_RESPONSE_SCHEMA_V1.csv",
        "SITE_EXPOSED",
        "SYSTEM_EXPOSED",
        "Do not expand recipients simply to increase the chance of a favorable site.",
    ):
        assert token in text
