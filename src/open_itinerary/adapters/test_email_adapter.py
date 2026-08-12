from email.message import EmailMessage

import pytest

from open_itinerary.adapters import InputContent
from open_itinerary.adapters.email_adapter import EmailAdapter


def _email_content(message: EmailMessage) -> InputContent:
    return InputContent(message.as_bytes(), "message/rfc822")


def test_email_adapter_get_expected_media_types():
    assert EmailAdapter().get_expected_media_types() == {"message/rfc822"}


def test_email_adapter_rejects_unsupported_media_type():
    with pytest.raises(ValueError, match="text/plain is not supported"):
        EmailAdapter()._extract(InputContent(b"Booking confirmation", "text/plain"))


def test_email_adapter_extracts_plain_text_body():
    message = EmailMessage()
    message.set_content("Booking confirmation\nReference: ABC123")

    assert EmailAdapter()._extract(_email_content(message)) == "Booking confirmation\nReference: ABC123"


def test_email_adapter_prefers_plain_text_over_html():
    message = EmailMessage()
    message.set_content("Plain booking confirmation")
    message.add_alternative("<p>HTML booking confirmation</p>", subtype="html")

    assert EmailAdapter()._extract(_email_content(message)) == "Plain booking confirmation"


def test_email_adapter_falls_back_to_html_body():
    message = EmailMessage()
    message.set_content("<p>HTML booking confirmation</p>", subtype="html")

    assert EmailAdapter()._extract(_email_content(message)) == "<p>HTML booking confirmation</p>"


def test_email_adapter_raises_when_message_has_no_body():
    message = EmailMessage()
    message.make_mixed()
    message.add_attachment(b"PDF attachment", maintype="application", subtype="pdf")

    with pytest.raises(ValueError, match="could not find any content"):
        EmailAdapter()._extract(_email_content(message))
