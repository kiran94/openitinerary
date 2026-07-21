from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from open_itinerary.models.segments import BaseSegment


class Itinerary(BaseModel):
    schema_version: str
    id: str | None = None
    title: str | None = None
    segments: list[BaseSegment]
    created_at: datetime | None = None
    updated_at: datetime | None = None
