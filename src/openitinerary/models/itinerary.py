from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from openitinerary.models.domains.accommodation import AccommodationSegment
from openitinerary.models.domains.activity import ActivitySegment, TourSegment
from openitinerary.models.domains.flight import FlightSegment
from openitinerary.models.domains.train import TrainSegment
from openitinerary.models.domains.transfer import TransferSegment
from openitinerary.version import OPEN_ITINERARY_VERSION

Segment = Annotated[
    FlightSegment | TrainSegment | AccommodationSegment | TransferSegment | ActivitySegment | TourSegment,
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
