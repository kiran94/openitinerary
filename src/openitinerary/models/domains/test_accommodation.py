from uuid import uuid4

import pytest
from pydantic import ValidationError

from openitinerary.models.domains.accommodation import AccommodationSegment
from openitinerary.models.domains.flight import AirportPlace
from openitinerary.models.domains.train import TrainStation
from openitinerary.models.itinerary import Itinerary
from openitinerary.models.place import GenericPlace


def place_payload(place_type: str = "location", name: str = "Test place") -> dict:
    return {
        "type": place_type,
        "name": {"values": [{"language": "en", "value": name}]},
        "country": "PH",
        "timezone": "Asia/Manila",
        "coordinate": {"latitude": 14.5995, "longitude": 120.9842},
    }


def accommodation_payload() -> dict:
    return {
        "id": str(uuid4()),
        "type": "accommodation",
        "title": {"values": [{"language": "en", "value": "Hotel stay"}]},
        "start_time_utc": "2026-08-07T03:00:00Z",
        "place": place_payload(),
    }


@pytest.mark.parametrize(
    ("place_type", "expected_type"),
    [
        ("location", GenericPlace),
        ("airport", AirportPlace),
        ("train_station", TrainStation),
    ],
)
def test_accommodation_segment_accepts_all_place_variants(place_type: str, expected_type: type):
    payload = accommodation_payload()
    payload["place"] = place_payload(place_type)

    segment = AccommodationSegment.model_validate(payload)

    assert isinstance(segment.place, expected_type)


@pytest.mark.parametrize("value", [pytest.param(None), pytest.param("missing")])
def test_accommodation_segment_rejects_missing_or_null_place(value: str | None):
    payload = accommodation_payload()
    if value == "missing":
        del payload["place"]
    else:
        payload["place"] = value

    with pytest.raises(ValidationError):
        AccommodationSegment.model_validate(payload)


def test_accommodation_segment_accepts_optional_unit_type():
    payload = accommodation_payload()
    payload["unit_type"] = {"values": [{"language": "en", "value": "Deluxe Double Room"}]}

    segment = AccommodationSegment.model_validate(payload)

    assert len(segment.unit_type.values) == 1
    assert segment.unit_type.values[0].value == "Deluxe Double Room"


def test_itinerary_parses_accommodation_segment():
    itinerary = Itinerary.model_validate(
        {
            "id": "test-itinerary",
            "title": "Test itinerary",
            "segments": [accommodation_payload()],
        }
    )

    assert isinstance(itinerary.segments[0], AccommodationSegment)
    assert isinstance(itinerary.segments[0].place, GenericPlace)
