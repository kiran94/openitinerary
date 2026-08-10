from enum import StrEnum
from typing import Literal

from pydantic import Field

from open_itinerary.models.places import Place
from open_itinerary.models.segment_type import SegmentType
from open_itinerary.models.segments import BaseSegment


class BaseActivitySegment(BaseSegment):
    type: Literal[SegmentType.ACTIVITY] = SegmentType.ACTIVITY
    place: Place = Field(description="The activity venue, tour meeting point or starting location")


class ActivityType(StrEnum):
    ATTRACTION = "attraction"
    EVENT = "event"
    CLASS = "class"
    WELLNESS = "wellness"
    DINING = "dining"
    SHOW = "show"
    # The activity is understood but does not match a category in this schema version.
    OTHER = "other"


class ActivitySegment(BaseActivitySegment):
    type: Literal[SegmentType.ACTIVITY] = SegmentType.ACTIVITY

    # None means the source did not provide enough information to classify the activity.
    activity_type: ActivityType | None = None


class TourSegment(BaseActivitySegment):
    type: Literal[SegmentType.TOUR] = SegmentType.TOUR
    stops: list[Place] = Field(default=[], description="Places visited by the tour, in itinerary order.")
