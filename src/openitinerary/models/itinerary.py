from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from openitinerary.models.domains.accommodation import AccommodationSegment
from openitinerary.models.domains.activity import ActivitySegment, TourSegment
from openitinerary.models.domains.flight import FlightSegment
from openitinerary.models.domains.train import TrainSegment
from openitinerary.models.domains.transfer import TransferSegment
from openitinerary.version import OPEN_ITINERARY_SCHEMA_URL, OPEN_ITINERARY_VERSION

Segment = Annotated[
    FlightSegment | TrainSegment | AccommodationSegment | TransferSegment | ActivitySegment | TourSegment,
    Field(discriminator="type"),
]


class Itinerary(BaseModel):
    model_config = ConfigDict(validate_by_name=True, serialize_by_alias=True)

    schema_uri: str = Field(
        alias="$schema",
        description="Canonical URI of the JSON Schema used to validate this itinerary.",
        json_schema_extra={"const": OPEN_ITINERARY_SCHEMA_URL},
    )
    schema_version: str = Field(
        description="The schema version of open itinerary being used.",
        default=OPEN_ITINERARY_VERSION,
        json_schema_extra={"const": OPEN_ITINERARY_VERSION},
    )
    id: str | None = Field(description="Unique identifier for the Itinerary")
    title: str | None = Field(description="Title of the Itinerary")
    segments: list[Segment] = Field(
        description="A collection of travel activities. Segments should represent a coherent sequence and should normally be ordered by start_time_utc."
    )
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("schema_uri")
    @classmethod
    def validate_schema_uri(cls, schema_uri: str) -> str:
        if schema_uri != OPEN_ITINERARY_SCHEMA_URL:
            raise ValueError(f"$schema must be {OPEN_ITINERARY_SCHEMA_URL}")

        return schema_uri

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, schema_version: str) -> str:
        if schema_version != OPEN_ITINERARY_VERSION:
            raise ValueError(f"schema_version must be {OPEN_ITINERARY_VERSION}")

        return schema_version
