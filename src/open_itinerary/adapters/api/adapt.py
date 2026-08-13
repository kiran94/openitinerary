from fastapi import Response, UploadFile
from fastapi.routing import APIRouter

from open_itinerary.adapters import Adapter, InputContent
from open_itinerary.adapters.email_adapter import EmailAdapter
from open_itinerary.adapters.html_adapter import HtmlAdapter
from open_itinerary.adapters.pdf import PdfAdapter
from open_itinerary.models.itinerary import Segment

router = APIRouter()

_TAGS = ["Adapt"]

ALL_ADAPTERS: list[Adapter] = [PdfAdapter(), EmailAdapter(), HtmlAdapter()]


def determine_adapter(content_type: str) -> Adapter:
    for adapter in ALL_ADAPTERS:
        if content_type in adapter.get_expected_media_types():
            return adapter


@router.post("/segment", response_model=list[Segment], tags=_TAGS)
async def adapt(file: UploadFile, response: Response) -> list[Segment]:
    """
    Convert a traditional file into an OpenItinerary Segment
    """

    raw_file_data = await file.read()
    await file.close()

    adapter = determine_adapter(file.content_type)
    segments = await adapter.load(InputContent(raw_file_data, file.content_type))

    response.headers["X-Segment-Count"] = str(len(segments))
    return segments
