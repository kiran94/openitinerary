from typing import Literal

from openitinerary.models.place import BasePlace
from openitinerary.models.segment_type import PlaceType, SegmentType
from openitinerary.models.segments import TransportSegment


class TrainStation(BasePlace):
    type: Literal[PlaceType.TRAIN_STATION] = PlaceType.TRAIN_STATION


class TrainSegment(TransportSegment):
    type: Literal[SegmentType.TRAIN] = SegmentType.TRAIN
    train_number: str | None = None
    start_place: TrainStation
    end_place: TrainStation
