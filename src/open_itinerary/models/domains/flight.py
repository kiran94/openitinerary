from typing import Literal

from open_itinerary.models.place import Place
from open_itinerary.models.segment_type import SegmentType
from open_itinerary.models.segments import TransportSegment


class AirportPlace(Place):
    type: Literal[SegmentType.FLIGHT] = SegmentType.FLIGHT
    iata_code: str | None = None
    icao_code: str | None = None


class FlightSegment(TransportSegment):
    type: Literal[SegmentType.FLIGHT] = SegmentType.FLIGHT
    flight_number: str
    start_place: AirportPlace
    end_place: AirportPlace
