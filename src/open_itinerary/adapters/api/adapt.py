import os

from fastapi import HTTPException, Response, UploadFile, status
from fastapi.routing import APIRouter

from open_itinerary.adapters import Adapter, DocumentExtractionError, InputContent
from open_itinerary.adapters.email_adapter import EmailAdapter
from open_itinerary.adapters.html_adapter import HtmlAdapter
from open_itinerary.adapters.pdf import PdfAdapter
from open_itinerary.models.itinerary import Segment

router = APIRouter()

_TAGS = ["Adapt"]

OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES = int(os.environ.get("OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES", "10485760"))  # 10MB


ALL_ADAPTERS: list[Adapter] = [PdfAdapter(), EmailAdapter(), HtmlAdapter()]


def determine_adapter(content_type: str | None) -> Adapter | None:
    if content_type is None:
        return None

    for adapter in ALL_ADAPTERS:
        if content_type in adapter.get_expected_media_types():
            return adapter
    return None


@router.post("/segment", response_model=list[Segment], tags=_TAGS)
async def adapt(file: UploadFile, response: Response) -> list[Segment]:
    """
    Convert a traditional file into an OpenItinerary Segment
    """

    try:
        adapter = determine_adapter(file.content_type)
        if not adapter:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"'{file.content_type}' is not supported"
            )

        if file.size and file.size > OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES:
            raise _upload_too_large_error()

        raw_file_data = await file.read(OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES + 1)

        # UploadFile.size is not reliable/guaranteed so we do a secondary check
        # here to check the actual file content size before pushing it to the adapter.
        if len(raw_file_data) > OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES:
            raise _upload_too_large_error()

        try:
            segments = await adapter.load(InputContent(raw_file_data, file.content_type))
        except DocumentExtractionError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc

        response.headers["X-Segment-Count"] = str(len(segments))
        return segments
    finally:
        await file.close()


def _upload_too_large_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
        detail=f"Uploaded file exceeds the configured limit of {OPEN_ITINERARY_MAX_UPLOAD_SIZE_BYTES} bytes",
    )
