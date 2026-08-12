from bs4 import BeautifulSoup, NavigableString

from open_itinerary.adapters import Adapter, InputContent
from open_itinerary.adapters.agent import agent_factory
from open_itinerary.models.itinerary import Segment


class HtmlAdapter(Adapter):
    def _extract(self, content: InputContent) -> str:
        expected_media_types = self.get_expected_media_types()

        if content.media_type not in expected_media_types:
            raise ValueError(
                f"{content.media_type} is not supported by this adapter. Expected {','.join(expected_media_types)}"
            )

        result = BeautifulSoup(content.data, "html.parser")

        # remove whitespace to reduce the context window
        for element in result(["script", "style", "noscript", "template", "svg"]):
            element.decompose()

        # Hidden content can contain cancelled bookings, unselected options, modal
        # content, or responsive duplicates that must not be sent to the agent.
        for element in result.find_all(
            lambda tag: tag.has_attr("hidden")
            or tag.get("aria-hidden", "").strip().lower() == "true"
            or "display:none" in "".join(tag.get("style", "").lower().split())
        ):
            element.decompose()

        # Links can contain useful structured data, such as map coordinates, that is
        # not present in their visible label.
        for link in result.find_all("a", href=True):
            link.append(NavigableString(f" (href: {link['href']})"))

        result = "\n".join(result.stripped_strings)
        return result

    def _translate(self, content: str) -> list[Segment]:
        agent = agent_factory()
        result = agent.run_sync(content)
        return result.output

    def get_expected_media_types(self) -> set[str]:
        return {"text/html"}
