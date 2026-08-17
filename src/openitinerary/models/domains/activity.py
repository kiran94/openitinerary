from enum import StrEnum
from typing import Literal

from pydantic import Field

from openitinerary.models.places import Place
from openitinerary.models.segment_type import SegmentType
from openitinerary.models.segments import BaseSegment


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
    place: Place = Field(description="The activity venue.")

    # None means the source did not provide enough information to classify the activity.
    activity_type: ActivityType | None = None


class TourSegment(BaseActivitySegment):
    type: Literal[SegmentType.TOUR] = SegmentType.TOUR
    place: Place = Field(description="The tour meeting, pickup, or starting location.")
    stops: list[Place] | None = Field(
        default=None,
        description=(
            "Places visited by the tour, in itinerary order. Pickup and drop-off locations are excluded unless they "
            "are genuine itinerary stops."
        ),
    )
    drop_off_place: Place | None = Field(
        default=None,
        description="Where the traveller is dropped off after the tour, if known.",
    )
