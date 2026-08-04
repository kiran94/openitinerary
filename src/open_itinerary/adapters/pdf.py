from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader
from open_itinerary.adapters import InputContent
from open_itinerary.adapters import Adapter
from open_itinerary.adapters.agent import agent_factory
from open_itinerary.models.itinerary import Segment


class PdfAdapter(Adapter):
    def _extract(self, content: InputContent) -> str:
        expected_media_types = self.get_expected_media_types()

        if content.media_type not in expected_media_types:
            raise ValueError(
                f"{content.media_type} is not supported by this adapter. Expected {','.join(expected_media_types)}"
            )

        with TemporaryDirectory() as directory:
            path = Path(directory) / "input.pdf"
            path.write_bytes(content.data)

            reader = PdfReader(path)
            extracted_content = "".join(page.extract_text() or "" for page in reader.pages)

        return extracted_content

    def _translate(self, content: str) -> list[Segment]:
        agent = agent_factory()
        result = agent.run_sync(content)
        return result.output

    def get_expected_media_types(self) -> set[str]:
        return {"application/pdf"}
