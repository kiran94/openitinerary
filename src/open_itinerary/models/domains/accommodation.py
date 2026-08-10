from typing import Literal

from pydantic import Field

from open_itinerary.models.common import MultilingualText
from open_itinerary.models.places import Place
from open_itinerary.models.segment_type import SegmentType
from open_itinerary.models.segments import BaseSegment


class AccommodationSegment(BaseSegment):
    type: Literal[SegmentType.ACCOMMODATION] = SegmentType.ACCOMMODATION
    place: Place = Field(description="information about where the accommodation is location")
    unit_type: MultilingualText | None = Field(
        default=None,
        description=(
            "The booked accommodation unit or space type, as named by the provider, "
            "such as 'Deluxe Double or Twin Room with River View', "
            "'Entire two-bedroom apartment', or 'Bed in a 6-bed mixed dormitory'."
        ),
    )
