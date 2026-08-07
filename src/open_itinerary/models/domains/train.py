from typing import Literal

from open_itinerary.models.place import BasePlace
from open_itinerary.models.segment_type import PlaceType, SegmentType
from open_itinerary.models.segments import TransportSegment


class TrainStation(BasePlace):
    type: Literal[PlaceType.TRAIN_STATION] = PlaceType.TRAIN_STATION


class TrainSegment(TransportSegment):
    type: Literal[SegmentType.TRAIN] = SegmentType.TRAIN
    train_number: str | None = None
    start_place: TrainStation
    end_place: TrainStation
