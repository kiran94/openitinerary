import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from openitinerary.adapters import InputContent
from openitinerary.adapters.html_adapter import HtmlAdapter


def test_html_adapter_get_expected_media_types():
    assert HtmlAdapter().get_expected_media_types() == {"text/html"}


def test_html_adapter_rejects_unsupported_media_type():
    content = InputContent(b"", "application/pdf")

    with pytest.raises(ValueError, match="application/pdf is not supported"):
        asyncio.run(HtmlAdapter().load(content))


def test_html_adapter_extracts_visible_text_and_preserves_non_latin_text():
    content = InputContent(
        b"""
        <html>
          <head><style>.hidden { display: none; }</style><script>ignored()</script></head>
          <body>
            <h1>Best Western Hotel Fino Tokyo Akihabara</h1>
            <p>Taito-ku, Ueno 5-1-6</p>
            <p class="hidden">Cancelled booking</p>
            <p>\xe5\x8f\xb0\xe6\x9d\xb1\xe5\x8c\xba\xe4\xb8\x8a\xe9\x87\x8e 5-1-6, \xe5\x8f\xb0\xe6\x9d\xb1\xe5\x8c\xba, \xe6\x9d\xb1\xe4\xba\xac\xe9\x83\xbd</p>
            <a href="https://maps.example.com/?q=35.7032,139.7755">Map</a>
            <noscript>ignored fallback</noscript><template>ignored template</template><svg>ignored svg</svg>
          </body>
        </html>
        """,
        "text/html",
    )

    assert asyncio.run(HtmlAdapter()._extract(content)) == (
        "Best Western Hotel Fino Tokyo Akihabara\n"
        "Taito-ku, Ueno 5-1-6\n"
        "\u53f0\u6771\u533a\u4e0a\u91ce 5-1-6, \u53f0\u6771\u533a, \u6771\u4eac\u90fd\n"
        "Map\n"
        "(href: https://maps.example.com/?q=35.7032,139.7755)"
    )


def test_html_adapter_excludes_explicitly_hidden_content():
    content = InputContent(
        b"""
        <body>
          <p>Confirmed booking</p>
          <p hidden>Cancelled booking</p>
          <p aria-hidden="true">Unselected option</p>
          <p style="display: none">Responsive duplicate</p>
          <p style="DISPLAY : NONE">Hidden modal content</p>
          <p aria-hidden="false">Visible itinerary detail</p>
        </body>
        """,
        "text/html",
    )

    assert asyncio.run(HtmlAdapter()._extract(content)) == "Confirmed booking\nVisible itinerary detail"


@patch("openitinerary.adapters.html_adapter.agent_factory")
def test_html_adapter_load_passes_extracted_text_to_agent(agent_factory: Mock):
    expected_segments = [Mock(name="segment")]
    agent = agent_factory.return_value
    agent.run = AsyncMock(return_value=Mock(output=expected_segments))
    content = InputContent(b"<p>English</p><p>\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e</p>", "text/html")

    actual = asyncio.run(HtmlAdapter().load(content))

    assert actual == expected_segments
    agent.run.assert_awaited_once_with("English\n\u65e5\u672c\u8a9e")
