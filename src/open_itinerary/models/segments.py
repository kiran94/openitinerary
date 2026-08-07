from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime

from open_itinerary.models.common import Booking, Organization, MultilingualText
from open_itinerary.models.place import BasePlace
from open_itinerary.models.segment_type import SegmentType


class BaseSegment(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        use_enum_values=True,
    )

    id: UUID = Field(description="Globally unique identifier for the segment.")
    type: SegmentType = Field(description="Kind of itinerary segment, such as flight, hotel, activity, or train.")
    title: MultilingualText = Field(description="Summary title of the segment.")
    description: MultilingualText | None = Field(description="Additional description about the Segment", default=None)

    start_time_utc: datetime = Field(description="The start datetime of the segment, expressed in UTC")
    end_time_utc: datetime | None = Field(
        description="The end datetime of the segment (if known), expressed in UTC",
        default=None,
    )

    operator: Organization | None = Field(
        description="The organization operating or providing the service.",
        default=None,
    )
    booking: Booking | None = Field(description="booking information about the segment.", default=None)


class TransportSegment(BaseSegment):
    start_place: BasePlace | None
    end_place: BasePlace | None
