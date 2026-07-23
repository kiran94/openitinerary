from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from open_itinerary.models.domains.flight import FlightSegment
from open_itinerary.models.domains.train import TrainSegment
from open_itinerary.models.domains.accommodation import AccommodationSegment

Segment = Annotated[
    FlightSegment | TrainSegment | AccommodationSegment,
    Field(discriminator="type"),
]


class Itinerary(BaseModel):
    schema_version: str
    id: str | None = None
    title: str | None = None
    segments: list[Segment]
    created_at: datetime | None = None
    updated_at: datetime | None = None
