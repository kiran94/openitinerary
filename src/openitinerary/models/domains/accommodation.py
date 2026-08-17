from typing import Literal

from pydantic import Field

from openitinerary.models.common import MultilingualText
from openitinerary.models.places import Place
from openitinerary.models.segment_type import SegmentType
from openitinerary.models.segments import BaseSegment


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
