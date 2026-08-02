from pathlib import Path
from tempfile import TemporaryDirectory

from langchain_community.document_loaders.pdf import PyPDFLoader
from open_itinerary.adapters import InputContent
from open_itinerary.adapters import Adapter
from open_itinerary.models.segments import BaseSegment


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

            loader = PyPDFLoader(str(path))
            docs = loader.load()

        extracted_content = "".join([d.page_content for d in docs])
        return extracted_content

    def _translate(self, content: str) -> BaseSegment:

        pass

    def get_expected_media_types(self) -> set[str]:
        return {"application/pdf"}
