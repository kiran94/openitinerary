from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from open_itinerary.models.domains.flight import FlightSegment
from open_itinerary.models.domains.train import TrainSegment
from open_itinerary.models.domains.accommodation import AccommodationSegment
from open_itinerary.models.domains.transfer import TransferSegment
from open_itinerary.version import OPEN_ITINERARY_VERSION


Segment = Annotated[
    FlightSegment | TrainSegment | AccommodationSegment | TransferSegment,
    Field(discriminator="type"),
]


class Itinerary(BaseModel):
    schema_version: str = Field(
        description="The schema version of open itinerary being used.", default=OPEN_ITINERARY_VERSION
    )
    id: str | None = Field(description="Unique identifier for the Itinerary")
    title: str | None = Field(description="Title of the Itinerary")
    segments: list[Segment] = Field(
        description="A collection of travel activities. Segments should represent a coherent sequence and should normally be ordered by start_time_utc."
    )
    created_at: datetime | None = None
    updated_at: datetime | None = None
