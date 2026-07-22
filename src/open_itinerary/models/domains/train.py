from typing import Literal

from open_itinerary.models.place import Place
from open_itinerary.models.segment_type import SegmentType
from open_itinerary.models.segments import BaseSegment


class TrainStation(Place):
    type: Literal[SegmentType.TRAIN] = SegmentType.TRAIN


class TrainSegment(BaseSegment):
    type: Literal["train"] = "train"

    train_number: str | None = None

    start_place: TrainStation
    end_place: TrainStation
