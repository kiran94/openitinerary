from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime

from open_itinerary.models.common import Booking, Organization, MultilingualText
from open_itinerary.models.place import Place
from open_itinerary.models.segment_type import SegmentType


class BaseSegment(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        use_enum_values=True,
    )

    id: UUID = Field(description="Globally unique identifier for the segment.")
    type: SegmentType = Field(description="Kind of itinerary segment, such as flight, hotel, activity, or train.")
    title: MultilingualText = Field(description="Brief traveller-facing label for the segment.")
    description: MultilingualText | None = Field(
        default=None, description="Additional traveller-facing details about the segment."
    )
    start_time_utc: datetime = Field(description="Segment start date and time, expressed in UTC.")
    end_time_utc: datetime | None = Field(description="Segment end date and time, expressed in UTC when known.")
    operator: Organization | None
    booking: Booking | None


class TransportSegment(BaseSegment):
    start_place: Place | None
    end_place: Place | None
