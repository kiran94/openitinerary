import re

from bs4 import BeautifulSoup, NavigableString
from soupsieve import SelectorSyntaxError

from open_itinerary.adapters import Adapter, InputContent
from open_itinerary.adapters.agent import agent_factory
from open_itinerary.models.itinerary import Segment


class HtmlAdapter(Adapter):
    def _extract(self, content: InputContent) -> str:
        self.check_media_type(content)
        return self.extract_visible_text(content.data)

    @staticmethod
    def extract_visible_text(html: bytes | str) -> str:
        """Extract visible, meaningful text from an HTML document."""
        result = BeautifulSoup(html, "html.parser")

        for stylesheet in result.find_all("style"):
            for selector, declarations in re.findall(r"([^{}]+)\{([^{}]+)\}", stylesheet.get_text()):
                if not _is_hidden_style(declarations):
                    continue

                try:
                    for element in result.select(selector.strip()):
                        element.decompose()
                except SelectorSyntaxError:
                    # Email stylesheets may contain unsupported CSS syntax.
                    continue

        # Remove whitespace to reduce the context window.
        for element in result(["script", "style", "noscript", "template", "svg"]):
            element.decompose()

        # Hidden content can contain cancelled bookings, unselected options, modal
        # content, or responsive duplicates that must not be sent to the agent.
        for element in result.find_all(
            lambda tag: (
                tag.has_attr("hidden")
                or tag.get("aria-hidden", "").strip().lower() == "true"
                or _is_hidden_style(tag.get("style", ""))
            )
        ):
            element.decompose()

        # Links can contain useful structured data, such as map coordinates, that is
        # not present in their visible label.
        for link in result.find_all("a", href=True):
            link.append(NavigableString(f" (href: {link['href']})"))

        return "\n".join(result.stripped_strings)

    async def _translate(self, content: str) -> list[Segment]:
        agent = agent_factory()
        result = await agent.run(content)
        return result.output

    def get_expected_media_types(self) -> set[str]:
        return {"text/html"}


def _is_hidden_style(style: str) -> bool:
    normalized_style = "".join(style.lower().split())
    return "display:none" in normalized_style or "visibility:hidden" in normalized_style
