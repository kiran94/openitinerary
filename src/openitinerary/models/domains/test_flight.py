from uuid import uuid4

import pytest
from pydantic import ValidationError

from openitinerary.models.domains.flight import AirportPlace, FlightSegment
from openitinerary.models.itinerary import Itinerary
from openitinerary.version import OPEN_ITINERARY_SCHEMA_URL


def airport_payload(name: str = "Ninoy Aquino International Airport") -> dict:
    return {
        "type": "airport",
        "name": {"values": [{"language": "en", "value": name}]},
        "country": "PH",
        "timezone": "Asia/Manila",
        "coordinate": {"latitude": 14.5086, "longitude": 121.0198},
        "iata_code": "MNL",
        "icao_code": "RPLL",
    }


def flight_payload() -> dict:
    return {
        "id": str(uuid4()),
        "type": "flight",
        "title": {"values": [{"language": "en", "value": "Manila to Tokyo"}]},
        "start_time_utc": "2026-08-07T03:00:00Z",
        "start_place": airport_payload(),
        "end_place": airport_payload("Narita International Airport"),
        "flight_number": "PR424",
    }


def test_flight_segment_requires_flight_number():
    payload = flight_payload()
    del payload["flight_number"]

    with pytest.raises(ValidationError):
        FlightSegment.model_validate(payload)


def test_flight_segment_accepts_optional_pnr():
    payload = flight_payload()
    payload["pnr"] = "ABC123"

    segment = FlightSegment.model_validate(payload)

    assert segment.pnr == "ABC123"


@pytest.mark.parametrize("field", ["start_place", "end_place"])
def test_flight_segment_rejects_non_airport_places(field: str):
    payload = flight_payload()
    payload[field]["type"] = "location"

    with pytest.raises(ValidationError):
        FlightSegment.model_validate(payload)


def test_itinerary_parses_flight_segment():
    itinerary = Itinerary.model_validate(
        {
            "$schema": OPEN_ITINERARY_SCHEMA_URL,
            "id": "test-itinerary",
            "title": "Test itinerary",
            "segments": [flight_payload()],
        }
    )

    assert isinstance(itinerary.segments[0], FlightSegment)
    assert isinstance(itinerary.segments[0].start_place, AirportPlace)
    assert itinerary.segments[0].flight_number == "PR424"
