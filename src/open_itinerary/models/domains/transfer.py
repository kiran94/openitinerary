from enum import StrEnum
from typing import Literal

from pydantic import Field

from open_itinerary.models.places import Place
from open_itinerary.models.segment_type import SegmentType
from open_itinerary.models.segments import TransportSegment


class TransferMode(StrEnum):
    TAXI = "taxi"
    PRIVATE_CAR = "private_car"
    RIDE_HAIL = "ride_hail"
    SHUTTLE = "shuttle"


class TransferSegment(TransportSegment):
    type: Literal[SegmentType.TRANSFER] = SegmentType.TRANSFER
    transfer_mode: TransferMode = Field(description=("How the pre-booked road transfer is provided."))
    start_place: Place
    end_place: Place
