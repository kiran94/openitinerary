from typing import Literal

from pydantic import Field

from open_itinerary.models.place import Place
from open_itinerary.models.segment_type import SegmentType, PlaceType
from open_itinerary.models.segments import TransportSegment


class AirportPlace(Place):
    type: Literal[PlaceType.AIRPORT] = PlaceType.AIRPORT
    iata_code: str | None = None
    icao_code: str | None = None


class FlightSegment(TransportSegment):
    type: Literal[SegmentType.FLIGHT] = SegmentType.FLIGHT
    flight_number: str = Field(
        description="The well known flight number of this flight. Airline Code + Flight Number e.g PR101"
    )
    start_place: AirportPlace = Field(description="Details about the origin airport of the flight")
    end_place: AirportPlace = Field(description="Details about the destination airport of the flight")
