import asyncio
import re
from email import policy
from email.parser import BytesParser
from io import BytesIO

from open_itinerary.adapters import Adapter, InputContent
from open_itinerary.adapters.agent import agent_factory
from open_itinerary.adapters.html_adapter import HtmlAdapter
from open_itinerary.models.itinerary import Segment


class EmailAdapter(Adapter):
    async def _extract(self, content: InputContent) -> str:
        return await asyncio.to_thread(self._extract_sync, content)

    def _extract_sync(self, content: InputContent) -> str:
        self.check_media_type(content)

        message = BytesParser(policy=policy.default).parse(BytesIO(content.data))

        if (body_part := message.get_body(preferencelist=("plain",))) and (
            plain_text := _clean_text(body_part.get_content())
        ):
            return plain_text

        if (html_part := message.get_body(preferencelist=("html",))) and (
            html_text := HtmlAdapter.extract_visible_text(html_part.get_content())
        ):
            return html_text

        raise ValueError("could not find any content from email message")

    async def _translate(self, content: str) -> list[Segment]:
        agent = agent_factory()
        result = await agent.run(content)
        return result.output

    def get_expected_media_types(self) -> set[str]:
        return {"message/rfc822"}


def _clean_text(text: str) -> str:
    text = text.replace("\xa0", " ").replace("\u200b", "")
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text).strip()
