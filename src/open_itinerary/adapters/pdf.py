import asyncio
from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from open_itinerary.adapters import Adapter, DocumentExtractionError, InputContent
from open_itinerary.adapters.agent import agent_factory
from open_itinerary.models.itinerary import Segment


class PdfAdapter(Adapter):
    async def _extract(self, content: InputContent) -> str:
        return await asyncio.to_thread(self._extract_sync, content)

    def _extract_sync(self, content: InputContent) -> str:
        self.check_media_type(content)

        try:
            reader = PdfReader(BytesIO(content.data))
            extracted_content = "".join(page.extract_text() or "" for page in reader.pages)
        except PdfReadError as exc:
            raise DocumentExtractionError("could not extract content from PDF document") from exc

        return extracted_content

    async def _translate(self, content: str) -> list[Segment]:
        agent = agent_factory()
        result = await agent.run(content)
        return result.output

    def get_expected_media_types(self) -> set[str]:
        return {"application/pdf"}
