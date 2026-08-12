import asyncio
from io import BytesIO
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pypdf import PdfWriter

from open_itinerary.adapters import InputContent
from open_itinerary.adapters.pdf import PdfAdapter


def test_pdf_adapter_get_expected_media_types():
    adapter = PdfAdapter()

    expected = {"application/pdf"}
    actual = adapter.get_expected_media_types()

    assert expected == actual


def test_pdf_adapter_load_not_pdf():
    content = InputContent(b"", "application/html")
    adapter = PdfAdapter()

    with pytest.raises(ValueError, match="not supported"):
        asyncio.run(adapter.load(content))


@patch("open_itinerary.adapters.pdf.agent_factory")
def test_pdf_adapter_load(agent_factory: Mock):
    pdf_buffer = BytesIO()
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=72, height=72)
    pdf_writer.write(pdf_buffer)

    expected_segments = [Mock(name="segment")]
    agent = agent_factory.return_value
    agent.run = AsyncMock(return_value=Mock(output=expected_segments))

    content = InputContent(pdf_buffer.getvalue(), "application/pdf")
    adapter = PdfAdapter()

    actual = asyncio.run(adapter.load(content))

    assert actual == expected_segments
    agent.run.assert_awaited_once_with("")
