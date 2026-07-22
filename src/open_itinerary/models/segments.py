from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from enum import StrEnum
from datetime import datetime

from open_itinerary.models.common import Booking, Organization
from open_itinerary.models.place import Place


class SegmentType(StrEnum):
    FLIGHT = "flight"
    # HOTEL = "hotel"
    # ACTIVITY = "activity"
    # TRAIN = "train"
    # TRANSFER = "transfer"
    # CAR_RENTAL = "car_rental"
    # FERRY = "ferry"
    # CRUISE = "cruise"


class BaseSegment(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        use_enum_values=True,
    )

    id: UUID = Field(description="Globally unique identifier for the segment.")
    type: SegmentType = Field(description="Kind of itinerary segment, such as flight, hotel, activity, or train.")
    title: MultilingualText = Field(default=None, description="Brief traveller-facing label for the segment.")
    description: MultilingualText | None = Field(
        default=None, description="Additional traveller-facing details about the segment."
    )
    start_time_utc: datetime = Field(description="Segment start date and time, expressed in UTC.")
    end_time_utc: datetime | None = Field(description="Segment end date and time, expressed in UTC when known.")
    start_place: Place | None
    end_place: Place | None
    operator: Organization | None
    booking: Booking | None
