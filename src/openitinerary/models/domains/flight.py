from typing import Literal

from pydantic import Field

from openitinerary.models.place import BasePlace
from openitinerary.models.segment_type import PlaceType, SegmentType
from openitinerary.models.segments import TransportSegment


class AirportPlace(BasePlace):
    type: Literal[PlaceType.AIRPORT] = PlaceType.AIRPORT
    iata_code: str | None = None
    icao_code: str | None = None


class FlightSegment(TransportSegment):
    type: Literal[SegmentType.FLIGHT] = SegmentType.FLIGHT
    flight_number: str = Field(
        description="The well known flight number of this flight. Airline Code + Flight Number e.g PR101"
    )
    pnr: str | None = Field(
        default=None,
        description="The airline passenger name record (PNR) or record locator.",
    )
    start_place: AirportPlace = Field(description="Details about the origin airport of the flight")
    end_place: AirportPlace = Field(description="Details about the destination airport of the flight")
