from uuid import uuid4

import pytest
from pydantic import ValidationError

from openitinerary.models.domains.train import TrainSegment, TrainStation
from openitinerary.models.itinerary import Itinerary


def station_payload(name: str = "Tokyo Station") -> dict:
    return {
        "type": "train_station",
        "name": {"values": [{"language": "en", "value": name}]},
        "country": "JP",
        "timezone": "Asia/Tokyo",
        "coordinate": {"latitude": 35.6812, "longitude": 139.7671},
    }


def train_payload() -> dict:
    return {
        "id": str(uuid4()),
        "type": "train",
        "title": {"values": [{"language": "en", "value": "Tokyo to Kyoto"}]},
        "start_time_utc": "2026-08-07T03:00:00Z",
        "start_place": station_payload(),
        "end_place": station_payload("Kyoto Station"),
    }


def test_train_segment_defaults_to_no_train_number():
    segment = TrainSegment.model_validate(train_payload())

    assert segment.train_number is None


def test_train_segment_accepts_optional_train_number():
    payload = train_payload()
    payload["train_number"] = "Nozomi 21"

    segment = TrainSegment.model_validate(payload)

    assert segment.train_number == "Nozomi 21"


@pytest.mark.parametrize("field", ["start_place", "end_place"])
def test_train_segment_rejects_non_station_places(field: str):
    payload = train_payload()
    payload[field]["type"] = "airport"

    with pytest.raises(ValidationError):
        TrainSegment.model_validate(payload)


def test_itinerary_parses_train_segment():
    itinerary = Itinerary.model_validate(
        {
            "id": "test-itinerary",
            "title": "Test itinerary",
            "segments": [train_payload()],
        }
    )

    assert isinstance(itinerary.segments[0], TrainSegment)
    assert isinstance(itinerary.segments[0].end_place, TrainStation)
    assert itinerary.segments[0].end_place.name.values[0].value == "Kyoto Station"
