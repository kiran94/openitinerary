from typing import Literal

from pydantic import Field
from open_itinerary.models.place import Place
from open_itinerary.models.segment_type import SegmentType
from open_itinerary.models.segments import BaseSegment


class AccommodationSegment(BaseSegment):
    type: Literal[SegmentType.ACCOMMODATION] = SegmentType.ACCOMMODATION
    place: Place = Field(description="information about where the accommodation is location")
